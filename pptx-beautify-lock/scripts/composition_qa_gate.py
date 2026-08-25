#!/usr/bin/env python3
"""Validate the v0.5 spatial-composition QA report.

Render Visual QA answers "is anything visibly broken?".
Composition QA answers the stricter question: "does this slide have a coherent
skeleton, rhythm, balance, reading order, and respect for source brand terrain?"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

COMPOSITION_QA_SCHEMA = 1

REQUIRED_CHECKS = (
    "brand_chrome_respected",
    "content_not_occluded",
    "grid_alignment_coherent",
    "peer_components_aligned",
    "spacing_rhythm_coherent",
    "reading_order_clear",
    "visual_balance_coherent",
    "slide_role_composition_fit",
    "decorative_elements_earn_their_place",
)

REQUIRED_SCORES = (
    "hierarchy",
    "alignment",
    "spacing",
    "balance",
    "brand_fidelity",
    "restraint",
    "data_legibility",
)


def validate_report(
    report: dict,
    expected_slides: int,
    min_dimension: float = 88.0,
    min_overall: float = 90.0,
):
    errors: list[str] = []

    if report.get("schema") != COMPOSITION_QA_SCHEMA:
        errors.append(f"schema must be {COMPOSITION_QA_SCHEMA}")
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

        scores = item.get("scores")
        if not isinstance(scores, dict):
            errors.append(f"slide {slide_no}: scores object is required")
            scores = {}

        dimensions = []
        for key in REQUIRED_SCORES:
            value = scores.get(key)
            if not isinstance(value, (int, float)):
                errors.append(f"slide {slide_no}: numeric score {key} is required")
                continue
            dimensions.append(float(value))
            if value < min_dimension:
                errors.append(
                    f"slide {slide_no}: {key} score {value} < minimum {min_dimension}"
                )

        overall = item.get("composition_score")
        if not isinstance(overall, (int, float)):
            errors.append(f"slide {slide_no}: composition_score is required")
        elif overall < min_overall:
            errors.append(
                f"slide {slide_no}: composition_score {overall} < minimum {min_overall}"
            )

        if dimensions and isinstance(overall, (int, float)):
            average = sum(dimensions) / len(dimensions)
            if overall > average + 5:
                errors.append(
                    f"slide {slide_no}: composition_score is implausibly higher "
                    f"than dimension average {average:.1f}"
                )

        evidence = item.get("evidence")
        if not isinstance(evidence, dict):
            errors.append(f"slide {slide_no}: evidence object is required")
            evidence = {}
        for key in ("source_comparison", "grid_rails", "reading_order", "brand_anchors"):
            value = evidence.get(key)
            if isinstance(value, str):
                present = bool(value.strip())
            elif isinstance(value, list):
                present = bool(value)
            else:
                present = False
            if not present:
                errors.append(f"slide {slide_no}: evidence.{key} is required")

    expected = set(range(1, expected_slides + 1))
    missing = sorted(expected - seen)
    extra = sorted(seen - expected)
    if missing:
        errors.append(f"slides missing composition review: {missing}")
    if extra:
        errors.append(f"unexpected slide numbers in composition review: {extra}")
    if report.get("overall_pass") is not True:
        errors.append("overall_pass must be true")

    return not errors, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Composition QA gate / 空間構圖品質閘門")
    parser.add_argument("report")
    parser.add_argument("--expected-slides", type=int, required=True)
    parser.add_argument("--min-dimension", type=float, default=88.0)
    parser.add_argument("--min-overall", type=float, default=90.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        report = json.loads(Path(args.report).read_text(encoding="utf-8"))
        ok, errors = validate_report(
            report,
            args.expected_slides,
            args.min_dimension,
            args.min_overall,
        )
    except Exception as exc:
        ok, errors = False, [str(exc)]

    result = {
        "COMPOSITION_QA_PASS": ok,
        "composition_qa_schema": COMPOSITION_QA_SCHEMA,
        "required_checks": list(REQUIRED_CHECKS),
        "required_scores": list(REQUIRED_SCORES),
        "errors": errors,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"COMPOSITION_QA_PASS={'true' if ok else 'false'}")
        print(f"composition_qa_errors={len(errors)}")
        for error in errors:
            print(f"ERROR: {error}")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
