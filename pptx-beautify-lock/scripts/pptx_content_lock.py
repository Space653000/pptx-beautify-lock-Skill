#!/usr/bin/env python3
"""PPTX semantic content-lock snapshot and verifier.

繁體中文：建立 PPTX protected-semantics manifest，比對美化前後是否有未授權變更。
English: Create and compare protected-semantic manifests for PPTX files.

Principles:
- Ignore allowed visual formatting and top-level object/z-order changes.
- Preserve text/data/media/behavior associations, not just global value bags.
- Normalize run segmentation so font/restyling tools may rebuild runs without a
  false content regression.
- Fail closed on protected semantics.
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
R_NS_PREFIX = "{%s}" % NS["r"]
R_ID = R_NS_PREFIX + "id"
R_EMBED = R_NS_PREFIX + "embed"
R_LINK = R_NS_PREFIX + "link"
TABLE_SEMANTIC_ATTRS = {"gridSpan", "rowSpan", "hMerge", "vMerge"}
VISUAL_RELATION_TYPE_FRAGMENTS = {
    "diagramLayout",
    "diagramQuickStyle",
    "diagramColors",
    "theme",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_key(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def local_name(name: str) -> str:
    return name.rsplit("}", 1)[1] if "}" in name else name


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


def canonical_element(node) -> dict | None:
    if node is None:
        return None
    attrs = {
        local_name(k): v
        for k, v in sorted(node.attrib.items(), key=lambda kv: local_name(kv[0]))
    }
    return {
        "tag": local_name(node.tag),
        "attrs": attrs,
        "text": node.text or "",
        "children": [canonical_element(child) for child in list(node)],
    }


def paragraph_semantics(root) -> list[dict]:
    """Protect paragraph text/list semantics while ignoring run formatting."""
    if root is None:
        return []
    out = []
    for p in root.findall(".//a:p", NS):
        text = "".join(node.text or "" for node in p.findall(".//a:t", NS))
        ppr = p.find("./a:pPr", NS)
        level = ppr.attrib.get("lvl") if ppr is not None else None
        bullet = None
        if ppr is not None:
            for child in list(ppr):
                kind = local_name(child.tag)
                if kind == "buChar":
                    bullet = {"kind": kind, "char": child.attrib.get("char", "")}
                    break
                if kind == "buAutoNum":
                    bullet = {
                        "kind": kind,
                        "type": child.attrib.get("type", ""),
                        "startAt": child.attrib.get("startAt"),
                    }
                    break
                if kind in {"buNone", "buBlip"}:
                    bullet = {"kind": kind}
                    break
        out.append({"text": text, "level": level, "bullet": bullet})
    return out


def extract_math(root) -> list[dict]:
    if root is None:
        return []
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
                semantic_attrs = {
                    local_name(k): v
                    for k, v in sorted(tc.attrib.items())
                    if local_name(k) in TABLE_SEMANTIC_ATTRS
                }
                cells.append({
                    "paragraphs": paragraph_semantics(tc),
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
        "paragraphs": paragraph_semantics(chart_root),
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
        external_target = None
        rel = rels.get(rid or "")
        if rel:
            if rel["external"]:
                external_target = rel["target"]
            else:
                try:
                    image_hash = sha256(zf.read(rel["target"]))
                except KeyError:
                    image_hash = "MISSING"
        out.append({
            "image_sha256": image_hash,
            "external_target": external_target,
            "srcRect": dict(sorted(src.attrib.items())) if src is not None else {},
        })
    return sorted(out, key=stable_key)


def accessibility_semantics(root) -> list[dict]:
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


def external_relationship_semantics(rels: dict[str, dict]) -> list[dict]:
    return sorted(
        [
            {"target": rel["target"], "type": rel["type"]}
            for rel in rels.values()
            if rel["external"]
        ],
        key=stable_key,
    )


def _relationship_payload(zf: zipfile.ZipFile, rel: dict) -> dict | None:
    typ = rel["type"]
    if any(fragment in typ for fragment in VISUAL_RELATION_TYPE_FRAGMENTS):
        return None
    if rel["external"]:
        return {"type": typ, "external": True, "target": rel["target"]}

    target = rel["target"]
    if target.startswith("ppt/media/"):
        try:
            return {"type": typ, "media_sha256": sha256(zf.read(target))}
        except KeyError:
            return {"type": typ, "media_sha256": "MISSING"}
    if target.startswith("ppt/charts/"):
        return {"type": typ, "chart": chart_semantics(read_xml(zf, target))}
    if target.startswith("ppt/embeddings/") or "oleObject" in typ or "package" in typ:
        try:
            return {"type": typ, "payload_sha256": sha256(zf.read(target))}
        except KeyError:
            return {"type": typ, "payload_sha256": "MISSING"}
    if "diagramData" in typ or target.startswith("ppt/diagrams/data"):
        data_root = read_xml(zf, target)
        return {
            "type": typ,
            "diagram_paragraphs": paragraph_semantics(data_root),
            "diagram_math": extract_math(data_root),
        }
    # Internal slide/action/unknown content-bearing relationships fail closed by target.
    return {"type": typ, "target": target}


def relationship_uses(zf: zipfile.ZipFile, root, rels: dict[str, dict]) -> list[dict]:
    if root is None:
        return []
    out = []
    for node in root.iter():
        for attr_name, rid in node.attrib.items():
            if not attr_name.startswith(R_NS_PREFIX):
                continue
            rel = rels.get(rid)
            if rel is None:
                out.append({
                    "element": local_name(node.tag),
                    "attr": local_name(attr_name),
                    "relationship": "MISSING",
                })
                continue
            payload = _relationship_payload(zf, rel)
            if payload is None:
                continue
            out.append({
                "element": local_name(node.tag),
                "attr": local_name(attr_name),
                "relationship": payload,
            })
    return sorted(out, key=stable_key)


def object_semantics(zf: zipfile.ZipFile, root, rels: dict[str, dict]) -> list[dict]:
    """Capture protected semantics per content-bearing object, independent of z-order."""
    if root is None:
        return []
    sp_tree = root.find(".//p:spTree", NS)
    if sp_tree is None:
        return []
    out = []
    skip = {"nvGrpSpPr", "grpSpPr", "extLst"}
    for child in list(sp_tree):
        kind = local_name(child.tag)
        if kind in skip:
            continue
        record = {
            "kind": kind,
            "paragraphs": paragraph_semantics(child),
            "math": extract_math(child),
            "tables": extract_tables(child),
            "crop_states": crop_states(zf, child, rels),
            "accessibility": accessibility_semantics(child),
            "relationships": relationship_uses(zf, child, rels),
        }
        if any(record[key] for key in record if key != "kind"):
            out.append(record)
    return sorted(out, key=stable_key)


def transition_timing_semantics(root) -> dict:
    if root is None:
        return {"transition": None, "timing": None}
    return {
        "transition": canonical_element(root.find("./p:transition", NS)),
        "timing": canonical_element(root.find("./p:timing", NS)),
    }


def notes_semantics(zf: zipfile.ZipFile, notes_path: str) -> dict:
    root = read_xml(zf, notes_path)
    rels = relationships(zf, notes_path)
    return {
        "objects": object_semantics(zf, root, rels),
        "external_relationships": external_relationship_semantics(rels),
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
        "objects": object_semantics(zf, root, rels),
        "media": sorted(media, key=stable_key),
        "charts": sorted(charts, key=stable_key),
        "notes": notes,
        "embeddings": sorted(embeddings, key=stable_key),
        "external_relationships": external_relationship_semantics(rels),
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


def special_payload_hashes(zf: zipfile.ZipFile) -> list[dict]:
    """Preserve macros/controls/custom XML and other opaque semantic payloads."""
    prefixes = (
        "customXml/",
        "ppt/activeX/",
        "ppt/ctrlProps/",
        "ppt/tags/",
        "ppt/vbaProject",
    )
    out = []
    for name in sorted(zf.namelist()):
        if name.endswith("/"):
            continue
        if name.startswith(prefixes):
            out.append({"part": name, "sha256": sha256(zf.read(name))})
    return out


def off_slide_semantics(zf: zipfile.ZipFile) -> list[dict]:
    prefixes = (
        "ppt/slideMasters/",
        "ppt/slideLayouts/",
        "ppt/notesMasters/",
        "ppt/handoutMasters/",
        "ppt/diagrams/data",
    )
    out = []
    for name in sorted(zf.namelist()):
        if not name.endswith(".xml") or not name.startswith(prefixes):
            continue
        root = read_xml(zf, name)
        rels = relationships(zf, name)
        objects = object_semantics(zf, root, rels)
        paragraphs = [] if objects else paragraph_semantics(root)
        math = [] if objects else extract_math(root)
        accessibility = [] if objects else accessibility_semantics(root)
        rel_uses = [] if objects else relationship_uses(zf, root, rels)
        if objects or paragraphs or math or accessibility or rel_uses:
            out.append({
                "part": name,
                "objects": objects,
                "paragraphs": paragraphs,
                "math": math,
                "accessibility": accessibility,
                "relationships": rel_uses,
                "external_relationships": external_relationship_semantics(rels),
            })
    return out


def package_external_relationships(zf: zipfile.ZipFile) -> list[dict]:
    out = []
    for name in sorted(zf.namelist()):
        if not name.endswith(".rels"):
            continue
        root = read_xml(zf, name)
        if root is None:
            continue
        for rel in list(root):
            if rel.attrib.get("TargetMode") == "External":
                out.append({
                    "rels_part": name,
                    "target": rel.attrib.get("Target", ""),
                    "type": rel.attrib.get("Type", ""),
                })
    return sorted(out, key=stable_key)


def build_manifest(path: str) -> dict:
    with zipfile.ZipFile(path, "r") as zf:
        order = slide_order(zf)
        slides = [slide_manifest(zf, p) for p in order]
        manifest = {
            "schema": 4,
            "slide_count": len(order),
            "slides": slides,
            "package_media": package_hashes(zf, "ppt/media/"),
            "package_embeddings": package_hashes(zf, "ppt/embeddings/"),
            "annotations": annotation_hashes(zf),
            "special_payloads": special_payload_hashes(zf),
            "off_slide_semantics": off_slide_semantics(zf),
            "package_external_relationships": package_external_relationships(zf),
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
