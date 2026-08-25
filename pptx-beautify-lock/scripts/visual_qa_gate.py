#!/usr/bin/env python3
"""Validate a rendered-slide visual QA report for pptx-beautify-lock.

The report is produced after an AI/human reviewer inspects every rendered slide.
This validator does not perform vision itself; it makes the review exhaustive,
machine-readable, and suitable for the final regression gate.
"""

from __future__ import annotations

import argparse
import json
import sys

REQUIRED_CHECKS = (
    "no_unintended_overlap",
    "no_clipping_or_overflow",
    "content_visible",
    "text_readable",
    "hierarchy_clear",
    "alignment_consistent",
    "tables_charts_readable",
    "style_consistent",
)


def validate_report(report: dict, expected_slides: int, min_score: float = 85.0):
    errors: list[str] = []

    if report.get("schema") != 1:
        errors.append("schema must be 1")

    if report.get("slide_count") != expected_slides:
        errors.append(
            f"slide_count {report.get('slide_count')!r} != expected {expected_slides}"
        )

    if not str(report.get("render_engine", "")).strip():
        errors.append("render_engine is required")
    if not str(report.get("reviewer", "")).strip():
        errors.append("reviewer is required")

    slides = report.get("slides")
    if not isinstance(slides, list):
        errors.append("slides must be a list")
        slides = []

    seen = set()
    for item in slides:
        if not isinstance(item, dict):
            errors.append("each slides[] item must be an object")
            continue
        slide_no = item.get("slide")
        if not isinstance(slide_no, int):
            errors.append("slide number must be an integer")
            continue
        if slide_no in seen:
            errors.append(f"duplicate slide review: {slide_no}")
        seen.add(slide_no)

        checks = item.get("checks")
        if not isinstance(checks, dict):
            errors.append(f"slide {slide_no}: checks object is required")
            checks = {}
        for key in REQUIRED_CHECKS:
            if checks.get(key) is not True:
                errors.append(f"slide {slide_no}: {key} must be true")

        score = item.get("score")
        if not isinstance(score, (int, float)):
            errors.append(f"slide {slide_no}: numeric score is required")
        elif score < min_score:
            errors.append(f"slide {slide_no}: score {score} < minimum {min_score}")

    expected = set(range(1, expected_slides + 1))
    missing = sorted(expected - seen)
    extra = sorted(seen - expected)
    if missing:
        errors.append(f"slides missing visual review: {missing}")
    if extra:
        errors.append(f"unexpected slide numbers in visual review: {extra}")

    if report.get("overall_pass") is not True:
        errors.append("overall_pass must be true")

    return not errors, errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Visual QA gate / 投影片 Render 視覺品質閘門")
    ap.add_argument("report", help="visual_qa.json")
    ap.add_argument("--expected-slides", type=int, required=True)
    ap.add_argument("--min-score", type=float, default=85.0)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        with open(args.report, "r", encoding="utf-8") as f:
            report = json.load(f)
        ok, errors = validate_report(report, args.expected_slides, args.min_score)
    except (OSError, json.JSONDecodeError) as exc:
        ok, errors = False, [str(exc)]

    result = {
        "VISUAL_QA_PASS": ok,
        "errors": errors,
        "expected_slides": args.expected_slides,
        "minimum_slide_score": args.min_score,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"VISUAL_QA_PASS={'true' if ok else 'false'}")
        print(f"visual_qa_errors={len(errors)}")
        for error in errors:
            print(f"ERROR: {error}")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
