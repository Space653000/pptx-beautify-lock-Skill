#!/usr/bin/env python3
"""Regression quality gate for pptx-beautify-lock.

Checks both semantic content integrity and layout regression.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    ap = argparse.ArgumentParser(description="PPTX Regression Test / PPTX 回歸測試")
    ap.add_argument("source", help="Original source PPTX / 原始 PPTX")
    ap.add_argument("output", help="Beautified output PPTX / 美化後 PPTX")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        lock = _load("pptx_content_lock", "pptx_content_lock.py")
        lint = _load("pptx_lint", "pptx_lint.py")

        before_manifest = lock.build_manifest(args.source)
        after_manifest = lock.build_manifest(args.output)
        content_diffs = lock.diff(before_manifest, after_manifest)
        content_ok = len(content_diffs) == 0

        baseline = lint.scan_presentation(args.source)
        output = lint.scan_presentation(args.output)

        # Hard layout errors must not increase and the final deck must have zero hard errors.
        no_error_regression = output["lint_errors"] <= baseline["lint_errors"]
        final_hard_errors_zero = output["lint_errors"] == 0

        # Warning count is heuristic; it should not increase. If it does, require manual review.
        warnings_not_worse = output["lint_warnings"] <= baseline["lint_warnings"]

        regression_ok = content_ok and no_error_regression and final_hard_errors_zero and warnings_not_worse

        result = {
            "REGRESSION_PASS": regression_ok,
            "CONTENT_LOCK_PASS": content_ok,
            "LAYOUT_QA_PASS": final_hard_errors_zero,
            "content_differences": len(content_diffs),
            "content_difference_preview": content_diffs[:100],
            "baseline": {
                "slides_checked": baseline["slides_checked"],
                "lint_errors": baseline["lint_errors"],
                "lint_warnings": baseline["lint_warnings"],
                "lint_infos": baseline["lint_infos"],
            },
            "output": {
                "slides_checked": output["slides_checked"],
                "lint_errors": output["lint_errors"],
                "lint_warnings": output["lint_warnings"],
                "lint_infos": output["lint_infos"],
            },
            "checks": {
                "no_error_regression": no_error_regression,
                "final_hard_errors_zero": final_hard_errors_zero,
                "warnings_not_worse": warnings_not_worse,
            },
        }

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for key in ("REGRESSION_PASS", "CONTENT_LOCK_PASS", "LAYOUT_QA_PASS"):
                print(f"{key}={'true' if result[key] else 'false'}")
            print(f"content_differences={result['content_differences']}")
            print(f"baseline_layout_errors={baseline['lint_errors']}")
            print(f"output_layout_errors={output['lint_errors']}")
            print(f"baseline_layout_warnings={baseline['lint_warnings']}")
            print(f"output_layout_warnings={output['lint_warnings']}")
            if content_diffs:
                print("--- content differences / 內容差異 ---")
                for item in content_diffs[:100]:
                    print(item)

        return 0 if regression_ok else 2

    except Exception as exc:
        if args.json:
            print(json.dumps({"REGRESSION_PASS": False, "ERROR": str(exc)}, ensure_ascii=False, indent=2))
        else:
            print("REGRESSION_PASS=false")
            print(f"ERROR={exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
