#!/usr/bin/env python3
"""PPTX Linter for pptx-beautify-lock.

繁體中文：掃描 PowerPoint 幾何、字級、重疊、邊界與字型一致性風險。
English: Scan PPTX geometry, typography, overlap, edge and font consistency risks.

This tool never modifies the input file.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass

try:
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE
except ImportError:
    print("ERROR=python-pptx is required. Install with: pip install python-pptx", file=sys.stderr)
    raise SystemExit(3)


@dataclass
class Finding:
    slide: int
    severity: str
    rule: str
    message_zh_TW: str
    message_en: str
    objects: list[str]


def _box(shape):
    return (shape.left, shape.top, shape.left + shape.width, shape.top + shape.height)


def _area(b):
    return max(0, b[2] - b[0]) * max(0, b[3] - b[1])


def _intersection(a, b):
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    if x2 <= x1 or y2 <= y1:
        return 0
    return (x2 - x1) * (y2 - y1)


def _visible_text(shape):
    return bool(getattr(shape, "has_text_frame", False) and (shape.text or "").strip())


def _font_sizes(shape):
    values = []
    if not getattr(shape, "has_text_frame", False):
        return values
    for p in shape.text_frame.paragraphs:
        for r in p.runs:
            if r.font.size is not None:
                values.append(float(r.font.size.pt))
    return values


def _font_names(shape):
    names = set()
    if not getattr(shape, "has_text_frame", False):
        return names
    for p in shape.text_frame.paragraphs:
        for r in p.runs:
            if r.font.name:
                names.add(r.font.name.strip())
    return names


def _background_like(shape, sw, sh):
    return _area(_box(shape)) >= 0.85 * sw * sh


def scan_presentation(path: str, tiny_pt: float = 11.0, overlap_threshold: float = 0.15,
                      edge_margin_ratio: float = 0.01, max_fonts_per_slide: int = 4):
    prs = Presentation(path)
    sw, sh = prs.slide_width, prs.slide_height
    findings: list[Finding] = []

    for sidx, slide in enumerate(prs.slides, 1):
        shapes = list(slide.shapes)
        slide_fonts = set()

        for i, shape in enumerate(shapes):
            name = getattr(shape, "name", f"shape-{i}")
            l, t, r, b = _box(shape)

            if shape.width <= 0 or shape.height <= 0:
                findings.append(Finding(sidx, "ERROR", "non-positive-geometry",
                    "物件寬度或高度不是正值", "Object has non-positive geometry", [name]))
                continue

            if l < 0 or t < 0 or r > sw or b > sh:
                findings.append(Finding(sidx, "ERROR", "out-of-bounds",
                    "物件超出投影片邊界", "Object extends beyond slide bounds", [name]))

            # Edge risk: ignore backgrounds and deliberate full-bleed images/shapes.
            if not _background_like(shape, sw, sh):
                mx, my = sw * edge_margin_ratio, sh * edge_margin_ratio
                if l < mx or t < my or (sw - r) < mx or (sh - b) < my:
                    findings.append(Finding(sidx, "INFO", "unsafe-edge-margin",
                        "物件非常接近投影片邊界，請確認是否為刻意設計",
                        "Object is very close to a slide edge; confirm this is intentional", [name]))

            sizes = _font_sizes(shape)
            if sizes and min(sizes) < tiny_pt:
                findings.append(Finding(sidx, "WARNING", "tiny-text",
                    f"偵測到 {min(sizes):.1f} pt 的小字，可能影響投影可讀性",
                    f"Detected {min(sizes):.1f} pt text; projected readability may be poor", [name]))

            slide_fonts |= _font_names(shape)

        if len(slide_fonts) > max_fonts_per_slide:
            findings.append(Finding(sidx, "WARNING", "too-many-fonts",
                f"同頁偵測到 {len(slide_fonts)} 種明確字型，視覺一致性風險偏高",
                f"Detected {len(slide_fonts)} explicit font families on one slide", sorted(slide_fonts)))

        # Conservative overlap heuristic.
        for i in range(len(shapes)):
            a = shapes[i]
            if _background_like(a, sw, sh) or getattr(a, "shape_type", None) == MSO_SHAPE_TYPE.GROUP:
                continue
            for j in range(i + 1, len(shapes)):
                b = shapes[j]
                if _background_like(b, sw, sh) or getattr(b, "shape_type", None) == MSO_SHAPE_TYPE.GROUP:
                    continue
                if not (_visible_text(a) or _visible_text(b)):
                    continue
                ba, bb = _box(a), _box(b)
                inter = _intersection(ba, bb)
                if inter <= 0:
                    continue
                denom = min(_area(ba), _area(bb))
                if denom <= 0:
                    continue
                ratio = inter / denom
                if ratio >= overlap_threshold:
                    findings.append(Finding(sidx, "WARNING", "suspicious-overlap",
                        f"兩個物件疑似重疊 {ratio:.1%}，需 render 確認是否為刻意",
                        f"Two objects overlap by {ratio:.1%}; render review is required",
                        [getattr(a, "name", "A"), getattr(b, "name", "B")]))

    errors = sum(1 for f in findings if f.severity == "ERROR")
    warnings = sum(1 for f in findings if f.severity == "WARNING")
    infos = sum(1 for f in findings if f.severity == "INFO")
    return {
        "slides_checked": len(prs.slides),
        "lint_errors": errors,
        "lint_warnings": warnings,
        "lint_infos": infos,
        "LINT_PASS": errors == 0,
        "findings": [asdict(f) for f in findings],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="PPTX Linter / PowerPoint 版面檢查器")
    ap.add_argument("pptx")
    ap.add_argument("--tiny-pt", type=float, default=11.0)
    ap.add_argument("--overlap-threshold", type=float, default=0.15)
    ap.add_argument("--edge-margin-ratio", type=float, default=0.01)
    ap.add_argument("--max-fonts-per-slide", type=int, default=4)
    ap.add_argument("--json", action="store_true", help="Output full JSON findings")
    args = ap.parse_args()

    try:
        result = scan_presentation(
            args.pptx,
            tiny_pt=args.tiny_pt,
            overlap_threshold=args.overlap_threshold,
            edge_margin_ratio=args.edge_margin_ratio,
            max_fonts_per_slide=args.max_fonts_per_slide,
        )
    except Exception as exc:
        print("LINT_PASS=false")
        print(f"ERROR={exc}", file=sys.stderr)
        return 3

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"LINT_PASS={'true' if result['LINT_PASS'] else 'false'}")
        print(f"slides_checked={result['slides_checked']}")
        print(f"lint_errors={result['lint_errors']}")
        print(f"lint_warnings={result['lint_warnings']}")
        print(f"lint_infos={result['lint_infos']}")
        for f in result["findings"]:
            objs = ", ".join(f["objects"])
            print(f"{f['severity']}: slide {f['slide']} [{f['rule']}] {f['message_zh_TW']} ({objs})")

    return 0 if result["LINT_PASS"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
