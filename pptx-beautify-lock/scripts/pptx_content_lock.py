#!/usr/bin/env python3
"""PPTX semantic content-lock snapshot and verifier.

繁體中文：
建立 PPTX 內容 manifest，並比對美化前後是否有內容層差異。
此工具刻意忽略多數視覺 formatting，但檢查文字、表格、圖表資料、
媒體 payload、圖片 crop、備註、嵌入檔案與投影片順序。

English:
Create and compare semantic manifests for PPTX files. The verifier is
intentionally conservative and fails closed when frozen content differs.
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
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}
R_ID = "{%s}id" % NS["r"]
R_EMBED = "{%s}embed" % NS["r"]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


def extract_tables(root) -> list[list[list[str]]]:
    tables = []
    if root is None:
        return tables
    for tbl in root.findall(".//a:tbl", NS):
        rows = []
        for tr in tbl.findall("./a:tr", NS):
            cells = []
            for tc in tr.findall("./a:tc", NS):
                vals = [x.text if x.text is not None else "" for x in tc.findall(".//a:t", NS)]
                cells.append("".join(vals))
            rows.append(cells)
        tables.append(rows)
    return tables


def extract_crop_states(root) -> list[dict]:
    out = []
    if root is None:
        return out
    for blip_fill in root.findall(".//p:blipFill", NS):
        blip = blip_fill.find("./a:blip", NS)
        src = blip_fill.find("./a:srcRect", NS)
        out.append({
            "embed_rid": blip.attrib.get(R_EMBED) if blip is not None else None,
            "srcRect": dict(sorted(src.attrib.items())) if src is not None else {},
        })
    return out


def chart_semantics(chart_root) -> dict:
    if chart_root is None:
        return {}
    # Capture formulas, string caches, numeric caches, categories, series names,
    # and explicit data labels as semantic chart content. Ignore style attrs.
    formulas = [x.text or "" for x in chart_root.findall(".//c:f", NS)]
    strings = [x.text or "" for x in chart_root.findall(".//c:v", NS)]
    tx = [x.text or "" for x in chart_root.findall(".//c:tx//c:v", NS)]
    pt = []
    for node in chart_root.findall(".//c:pt", NS):
        v = node.find("./c:v", NS)
        pt.append({"idx": node.attrib.get("idx"), "v": "" if v is None or v.text is None else v.text})
    return {"formulas": formulas, "values": strings, "series_text": tx, "points": pt}


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


def slide_manifest(zf: zipfile.ZipFile, slide_path: str) -> dict:
    root = read_xml(zf, slide_path)
    rels = relationships(zf, slide_path)

    media = []
    charts = []
    notes_text = []
    embeddings = []

    for rid, rel in sorted(rels.items()):
        if rel["external"]:
            continue
        target = rel["target"]
        typ = rel["type"]
        if "image" in typ or "audio" in typ or "video" in typ or target.startswith("ppt/media/"):
            try:
                media.append({"rid": rid, "sha256": sha256(zf.read(target)), "name": posixpath.basename(target)})
            except KeyError:
                media.append({"rid": rid, "missing": target})
        elif "chart" in typ or target.startswith("ppt/charts/"):
            charts.append({"rid": rid, "semantic": chart_semantics(read_xml(zf, target))})
        elif "notesSlide" in typ or target.startswith("ppt/notesSlides/"):
            notes_text = text_values(read_xml(zf, target))
        elif "oleObject" in typ or "package" in typ or target.startswith("ppt/embeddings/"):
            try:
                embeddings.append({"rid": rid, "sha256": sha256(zf.read(target)), "name": posixpath.basename(target)})
            except KeyError:
                embeddings.append({"rid": rid, "missing": target})

    return {
        "texts": text_values(root),
        "tables": extract_tables(root),
        "crop_states": extract_crop_states(root),
        "media": media,
        "charts": charts,
        "notes_text": notes_text,
        "embeddings": embeddings,
    }


def package_embeddings(zf: zipfile.ZipFile) -> list[dict]:
    out = []
    for name in sorted(zf.namelist()):
        if name.startswith("ppt/embeddings/") and not name.endswith("/"):
            out.append({"name": posixpath.basename(name), "sha256": sha256(zf.read(name))})
    return out


def build_manifest(path: str) -> dict:
    with zipfile.ZipFile(path, "r") as zf:
        order = slide_order(zf)
        slides = [slide_manifest(zf, p) for p in order]
        manifest = {
            "schema": 1,
            "slide_count": len(order),
            # Compare slides by semantic sequence, not internal rIds/filenames.
            "slides": slides,
            "package_embeddings": package_embeddings(zf),
        }
    canonical = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
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
            print(f"... {len(diffs)-200} more differences omitted")
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
