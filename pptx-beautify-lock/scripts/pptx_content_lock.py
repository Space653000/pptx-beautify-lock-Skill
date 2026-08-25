#!/usr/bin/env python3
"""PPTX semantic content-lock snapshot and verifier.

繁體中文：建立 PPTX 內容 manifest，並比對美化前後是否有未授權的內容層差異。
English: Create and compare semantic manifests for PPTX files.

Design intent:
- Ignore presentation-only formatting that the skill explicitly allows.
- Preserve semantic/functional content conservatively.
- Fail closed when a protected semantic changes.

This is not a byte-for-byte package comparer. It normalizes unstable relationship
IDs where practical while locking text, tables, charts, links/actions, media,
notes, embedded payloads, accessibility text, slide visibility, animation and
transition semantics, and other content-bearing structures covered below.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import sys
import zipfile
from pathlib import PurePosixPath
import xml.etree.ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
}
R_ID = "{%s}id" % NS["r"]
R_EMBED = "{%s}embed" % NS["r"]
R_LINK = "{%s}link" % NS["r"]

TABLE_SEMANTIC_ATTRS = {"gridSpan", "rowSpan", "hMerge", "vMerge"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_key(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def local_name(name: str) -> str:
    if "}" in name:
        return name.rsplit("}", 1)[1]
    return name


def read_xml(zf: zipfile.ZipFile, path: str):
    try:
        return ET.fromstring(zf.read(path))
    except KeyError:
        return None


def rels_path(part_path: str) -> str:
    p = PurePosixPath(part_path)
    return str(p.parent / "_rels" / (p.name + ".rels"))


def resolve_target(source_part: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(source_part), target))


def relationships(zf: zipfile.ZipFile, source_part: str) -> dict[str, dict]:
    root = read_xml(zf, rels_path(source_part))
    out = {}
    if root is None:
        return out
    for rel in list(root):
        rid = rel.attrib.get("Id")
        target = rel.attrib.get("Target", "")
        mode = rel.attrib.get("TargetMode")
        typ = rel.attrib.get("Type", "")
        if rid:
            out[rid] = {
                "target": target if mode == "External" else resolve_target(source_part, target),
                "external": mode == "External",
                "type": typ,
            }
    return out


def text_values(root) -> list[str]:
    if root is None:
        return []
    return [el.text if el.text is not None else "" for el in root.findall(".//a:t", NS)]


def canonical_element(node) -> dict | None:
    """Serialize an XML subtree semantically, independent of namespace prefixes."""
    if node is None:
        return None
    attrs = {local_name(k): v for k, v in sorted(node.attrib.items(), key=lambda kv: local_name(kv[0]))}
    return {
        "tag": local_name(node.tag),
        "attrs": attrs,
        "text": node.text or "",
        "children": [canonical_element(child) for child in list(node)],
    }


def extract_math(root) -> list[dict]:
    if root is None:
        return []
    # oMath elements are the formula-bearing units. Capturing each locks formula semantics.
    return [canonical_element(node) for node in root.findall(".//m:oMath", NS)]


def extract_tables(root) -> list[list[list[dict]]]:
    tables = []
    if root is None:
        return tables
    for tbl in root.findall(".//a:tbl", NS):
        rows = []
        for tr in tbl.findall("./a:tr", NS):
            cells = []
            for tc in tr.findall("./a:tc", NS):
                vals = [x.text if x.text is not None else "" for x in tc.findall(".//a:t", NS)]
                semantic_attrs = {
                    k: v for k, v in sorted(tc.attrib.items()) if local_name(k) in TABLE_SEMANTIC_ATTRS
                }
                cells.append({
                    "text": "".join(vals),
                    "merge": semantic_attrs,
                })
            rows.append(cells)
        tables.append(rows)
    return tables


def chart_semantics(chart_root) -> dict:
    if chart_root is None:
        return {}
    formulas = [x.text or "" for x in chart_root.findall(".//c:f", NS)]
    values = [x.text or "" for x in chart_root.findall(".//c:v", NS)]
    series_text = [x.text or "" for x in chart_root.findall(".//c:tx//c:v", NS)]
    points = []
    for node in chart_root.findall(".//c:pt", NS):
        v = node.find("./c:v", NS)
        points.append({"idx": node.attrib.get("idx"), "v": "" if v is None or v.text is None else v.text})
    return {
        "texts": text_values(chart_root),
        "formulas": formulas,
        "values": values,
        "series_text": series_text,
        "points": points,
    }


def slide_order(zf: zipfile.ZipFile) -> list[str]:
    pres = read_xml(zf, "ppt/presentation.xml")
    if pres is None:
        return []
    rels = relationships(zf, "ppt/presentation.xml")
    out = []
    for sid in pres.findall(".//p:sldId", NS):
        rid = sid.attrib.get(R_ID)
        rel = rels.get(rid or "")
        if rel and not rel["external"]:
            out.append(rel["target"])
    return out


def crop_states(zf: zipfile.ZipFile, root, rels: dict[str, dict]) -> list[dict]:
    out = []
    if root is None:
        return out
    for blip_fill in root.findall(".//p:blipFill", NS):
        blip = blip_fill.find("./a:blip", NS)
        src = blip_fill.find("./a:srcRect", NS)
        rid = None
        if blip is not None:
            rid = blip.attrib.get(R_EMBED) or blip.attrib.get(R_LINK)
        image_hash = None
        image_target = None
        rel = rels.get(rid or "")
        if rel:
            image_target = rel["target"]
            if not rel["external"]:
                try:
                    image_hash = sha256(zf.read(rel["target"]))
                except KeyError:
                    image_hash = "MISSING"
        out.append({
            "image_sha256": image_hash,
            "image_target": image_target if rel and rel["external"] else None,
            "srcRect": dict(sorted(src.attrib.items())) if src is not None else {},
        })
    return sorted(out, key=stable_key)


def hyperlink_semantics(root, rels: dict[str, dict]) -> list[dict]:
    if root is None:
        return []
    out = []
    for tag in ("hlinkClick", "hlinkMouseOver"):
        for node in root.findall(f".//a:{tag}", NS):
            rid = node.attrib.get(R_ID)
            rel = rels.get(rid or "")
            attrs = {}
            for key, value in sorted(node.attrib.items(), key=lambda kv: local_name(kv[0])):
                if key != R_ID:
                    attrs[local_name(key)] = value
            out.append({
                "kind": tag,
                "attrs": attrs,
                "relationship": None if rel is None else {
                    "target": rel["target"],
                    "external": rel["external"],
                    "type": rel["type"],
                },
            })
    return sorted(out, key=stable_key)


def external_relationship_semantics(rels: dict[str, dict]) -> list[dict]:
    return sorted(
        [
            {"target": rel["target"], "type": rel["type"]}
            for rel in rels.values()
            if rel["external"]
        ],
        key=stable_key,
    )


def accessibility_semantics(root) -> list[dict]:
    """Preserve accessibility text while allowing object names/geometry to change."""
    if root is None:
        return []
    out = []
    for node in root.iter():
        if local_name(node.tag) != "cNvPr":
            continue
        title = node.attrib.get("title")
        descr = node.attrib.get("descr")
        if title is not None or descr is not None:
            out.append({"title": title or "", "descr": descr or ""})
    return sorted(out, key=stable_key)


def transition_timing_semantics(root) -> dict:
    if root is None:
        return {"transition": None, "timing": None}
    transition = root.find("./p:transition", NS)
    timing = root.find("./p:timing", NS)
    return {
        "transition": canonical_element(transition),
        "timing": canonical_element(timing),
    }


def notes_semantics(zf: zipfile.ZipFile, notes_path: str) -> dict:
    root = read_xml(zf, notes_path)
    rels = relationships(zf, notes_path)
    return {
        "texts": text_values(root),
        "math": extract_math(root),
        "hyperlinks": hyperlink_semantics(root, rels),
        "external_relationships": external_relationship_semantics(rels),
        "accessibility": accessibility_semantics(root),
    }


def slide_manifest(zf: zipfile.ZipFile, slide_path: str) -> dict:
    root = read_xml(zf, slide_path)
    rels = relationships(zf, slide_path)
    media = []
    charts = []
    notes = None
    embeddings = []

    for rel in rels.values():
        if rel["external"]:
            continue
        target = rel["target"]
        typ = rel["type"]
        if "image" in typ or "audio" in typ or "video" in typ or target.startswith("ppt/media/"):
            try:
                media.append({"sha256": sha256(zf.read(target))})
            except KeyError:
                media.append({"missing": posixpath.basename(target)})
        elif "chart" in typ or target.startswith("ppt/charts/"):
            charts.append(chart_semantics(read_xml(zf, target)))
        elif "notesSlide" in typ or target.startswith("ppt/notesSlides/"):
            notes = notes_semantics(zf, target)
        elif "oleObject" in typ or "package" in typ or target.startswith("ppt/embeddings/"):
            try:
                embeddings.append({"sha256": sha256(zf.read(target))})
            except KeyError:
                embeddings.append({"missing": posixpath.basename(target)})

    return {
        "texts": text_values(root),
        "math": extract_math(root),
        "tables": extract_tables(root),
        "crop_states": crop_states(zf, root, rels),
        "media": sorted(media, key=stable_key),
        "charts": sorted(charts, key=stable_key),
        "notes": notes,
        "embeddings": sorted(embeddings, key=stable_key),
        "hyperlinks": hyperlink_semantics(root, rels),
        "external_relationships": external_relationship_semantics(rels),
        "accessibility": accessibility_semantics(root),
        "slide_show": None if root is None else root.attrib.get("show", "1"),
        "transition_timing": transition_timing_semantics(root),
    }


def package_hashes(zf: zipfile.ZipFile, prefix: str) -> list[dict]:
    out = []
    for name in sorted(zf.namelist()):
        if name.startswith(prefix) and not name.endswith("/"):
            out.append({"sha256": sha256(zf.read(name))})
    return sorted(out, key=stable_key)


def annotation_hashes(zf: zipfile.ZipFile) -> list[dict]:
    protected = []
    for name in sorted(zf.namelist()):
        lowered = name.lower()
        if not name.startswith("ppt/") or name.endswith("/"):
            continue
        if (
            "/comments/" in lowered
            or "commentauthors" in lowered
            or "/persons/" in lowered
            or "threadedcomment" in lowered
        ):
            protected.append({"sha256": sha256(zf.read(name))})
    return sorted(protected, key=stable_key)


def package_text_semantics(zf: zipfile.ZipFile, prefixes: tuple[str, ...]) -> list[dict]:
    """Protect visible/master/SmartArt text stored outside slide XML."""
    out = []
    for name in sorted(zf.namelist()):
        if not name.endswith(".xml") or not name.startswith(prefixes):
            continue
        root = read_xml(zf, name)
        texts = text_values(root)
        math = extract_math(root)
        if texts or math:
            out.append({"part": name, "texts": texts, "math": math})
    return out


def build_manifest(path: str) -> dict:
    with zipfile.ZipFile(path, "r") as zf:
        order = slide_order(zf)
        slides = [slide_manifest(zf, p) for p in order]
        manifest = {
            "schema": 3,
            "slide_count": len(order),
            "slides": slides,
            # Exact package media set: original image/audio/video payloads may not be
            # replaced, removed, re-encoded, or silently supplemented.
            "package_media": package_hashes(zf, "ppt/media/"),
            "package_embeddings": package_hashes(zf, "ppt/embeddings/"),
            "annotations": annotation_hashes(zf),
            "off_slide_text": package_text_semantics(
                zf,
                ("ppt/slideMasters/", "ppt/slideLayouts/", "ppt/diagrams/data"),
            ),
        }
    canonical = stable_key(manifest).encode("utf-8")
    manifest["semantic_sha256"] = sha256(canonical)
    return manifest


def diff(a, b, path="$", diffs=None):
    if diffs is None:
        diffs = []
    if type(a) is not type(b):
        diffs.append(f"{path}: type {type(a).__name__} != {type(b).__name__}")
        return diffs
    if isinstance(a, dict):
        for key in sorted(set(a) | set(b)):
            if key == "semantic_sha256":
                continue
            if key not in a:
                diffs.append(f"{path}.{key}: added")
            elif key not in b:
                diffs.append(f"{path}.{key}: removed")
            else:
                diff(a[key], b[key], f"{path}.{key}", diffs)
    elif isinstance(a, list):
        if len(a) != len(b):
            diffs.append(f"{path}: length {len(a)} != {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            diff(x, y, f"{path}[{i}]", diffs)
    elif a != b:
        diffs.append(f"{path}: {a!r} != {b!r}")
    return diffs


def cmd_snapshot(args) -> int:
    manifest = build_manifest(args.pptx)
    payload = json.dumps(manifest, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(payload + "\n")
        print(f"manifest={args.out}")
    else:
        print(payload)
    print(f"semantic_sha256={manifest['semantic_sha256']}")
    return 0


def cmd_verify(args) -> int:
    before = build_manifest(args.source)
    after = build_manifest(args.output)
    diffs = diff(before, after)
    ok = not diffs
    print(f"CONTENT_LOCK_PASS={'true' if ok else 'false'}")
    print(f"source_sha256={before['semantic_sha256']}")
    print(f"output_sha256={after['semantic_sha256']}")
    print(f"content_differences={len(diffs)}")
    if diffs:
        print("--- differences / 差異 ---")
        for item in diffs[:200]:
            print(item)
        if len(diffs) > 200:
            print(f"... {len(diffs) - 200} more differences omitted")
    return 0 if ok else 2


def main() -> int:
    parser = argparse.ArgumentParser(description="PPTX Content Lock verifier / PPTX 內容凍結驗證器")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("snapshot", help="Create semantic manifest / 建立內容快照")
    p1.add_argument("pptx")
    p1.add_argument("--out")
    p1.set_defaults(func=cmd_snapshot)

    p2 = sub.add_parser("verify", help="Verify source vs output / 比對美化前後內容")
    p2.add_argument("source")
    p2.add_argument("output")
    p2.set_defaults(func=cmd_verify)

    args = parser.parse_args()
    try:
        return args.func(args)
    except (zipfile.BadZipFile, ET.ParseError, OSError) as exc:
        print("CONTENT_LOCK_PASS=false")
        print(f"ERROR={exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
