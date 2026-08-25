#!/usr/bin/env python3
"""Regression quality gate for pptx-beautify-lock.

Checks semantic content integrity, structural/layout regression, and optionally
requires an exhaustive rendered-slide visual QA report before delivery.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCKING_WARNING_RULES = {"tiny-text", "table-density-risk"}


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _warning_counts(result: dict) -> Counter:
    return Counter(
        finding["rule"]
        for finding in result.get("findings", [])
        if finding.get("severity") == "WARNING"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="PPTX Regression Test / PPTX 回歸測試")
    ap.add_argument("source", help="Original source PPTX / 原始 PPTX")
    ap.add_argument("output", help="Beautified output PPTX / 美化後 PPTX")
    ap.add_argument("--visual-qa-report", help="visual_qa.json created after rendered-slide review")
    ap.add_argument("--require-visual-qa", action="store_true",
                    help="Fail delivery unless exhaustive rendered-slide visual QA passes")
    ap.add_argument("--min-visual-score", type=float, default=85.0)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        lock = _load("pptx_content_lock", "pptx_content_lock.py")
        lint = _load("pptx_lint", "pptx_lint.py")
        visual_gate = _load("visual_qa_gate", "visual_qa_gate.py")

        before_manifest = lock.build_manifest(args.source)
        after_manifest = lock.build_manifest(args.output)
        content_diffs = lock.diff(before_manifest, after_manifest)
        content_ok = len(content_diffs) == 0

        baseline = lint.scan_presentation(args.source)
        output = lint.scan_presentation(args.output)

        no_error_regression = output["lint_errors"] <= baseline["lint_errors"]
        final_hard_errors_zero = output["lint_errors"] == 0

        before_warnings = _warning_counts(baseline)
        after_warnings = _warning_counts(output)
        blocking_warnings_not_worse = all(
            after_warnings[rule] <= before_warnings[rule]
            for rule in BLOCKING_WARNING_RULES
        )

        # Heuristic warning counts may legitimately change after a real redesign
        # (e.g. intentional text-over-shape composition). They must be adjudicated
        # by rendered visual QA rather than blindly treated as regressions.
        heuristic_warning_rules = sorted(
            (set(before_warnings) | set(after_warnings)) - BLOCKING_WARNING_RULES
        )
        heuristic_warnings_remaining = any(after_warnings[rule] > 0 for rule in heuristic_warning_rules)

        structural_ok = (
            content_ok
            and no_error_regression
            and final_hard_errors_zero
            and blocking_warnings_not_worse
        )

        visual_ok = False
        visual_errors: list[str] = []
        if args.visual_qa_report:
            try:
                with open(args.visual_qa_report, "r", encoding="utf-8") as f:
                    report = json.load(f)
                visual_ok, visual_errors = visual_gate.validate_report(
                    report,
                    output["slides_checked"],
                    args.min_visual_score,
                )
            except (OSError, json.JSONDecodeError) as exc:
                visual_ok, visual_errors = False, [str(exc)]
        elif args.require_visual_qa:
            visual_errors = ["--require-visual-qa was set but no --visual-qa-report was provided"]

        regression_ok = structural_ok and (visual_ok if args.require_visual_qa else True)
        delivery_ok = structural_ok and visual_ok

        result = {
            "REGRESSION_PASS": regression_ok,
            "DELIVERY_PASS": delivery_ok,
            "CONTENT_LOCK_PASS": content_ok,
            "LAYOUT_QA_PASS": final_hard_errors_zero and blocking_warnings_not_worse,
            "VISUAL_QA_PASS": visual_ok,
            "VISUAL_QA_REQUIRED": args.require_visual_qa or heuristic_warnings_remaining,
            "content_differences": len(content_diffs),
            "content_difference_preview": content_diffs[:100],
            "visual_qa_errors": visual_errors,
            "baseline": {
                "slides_checked": baseline["slides_checked"],
                "lint_errors": baseline["lint_errors"],
                "lint_warnings": baseline["lint_warnings"],
                "lint_infos": baseline["lint_infos"],
                "warning_rules": dict(before_warnings),
            },
            "output": {
                "slides_checked": output["slides_checked"],
                "lint_errors": output["lint_errors"],
                "lint_warnings": output["lint_warnings"],
                "lint_infos": output["lint_infos"],
                "warning_rules": dict(after_warnings),
            },
            "checks": {
                "no_error_regression": no_error_regression,
                "final_hard_errors_zero": final_hard_errors_zero,
                "blocking_warnings_not_worse": blocking_warnings_not_worse,
                "heuristic_warnings_remaining": heuristic_warnings_remaining,
            },
        }

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for key in (
                "REGRESSION_PASS",
                "DELIVERY_PASS",
                "CONTENT_LOCK_PASS",
                "LAYOUT_QA_PASS",
                "VISUAL_QA_PASS",
                "VISUAL_QA_REQUIRED",
            ):
                print(f"{key}={'true' if result[key] else 'false'}")
            print(f"content_differences={result['content_differences']}")
            print(f"baseline_layout_errors={baseline['lint_errors']}")
            print(f"output_layout_errors={output['lint_errors']}")
            print(f"baseline_layout_warnings={baseline['lint_warnings']}")
            print(f"output_layout_warnings={output['lint_warnings']}")
            if visual_errors:
                print("--- visual QA errors / 視覺 QA 錯誤 ---")
                for item in visual_errors:
                    print(item)
            if content_diffs:
                print("--- content differences / 內容差異 ---")
                for item in content_diffs[:100]:
                    print(item)

        return 0 if regression_ok else 2

    except Exception as exc:
        if args.json:
            print(json.dumps({"REGRESSION_PASS": False, "DELIVERY_PASS": False, "ERROR": str(exc)}, ensure_ascii=False, indent=2))
        else:
            print("REGRESSION_PASS=false")
            print("DELIVERY_PASS=false")
            print(f"ERROR={exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
