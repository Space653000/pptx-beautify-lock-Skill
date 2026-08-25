#!/usr/bin/env python3
"""Legacy compatibility wrapper for PPTX layout QA.

New workflows should call pptx_lint.py directly. Keeping this entry point avoids
breaking older prompts while ensuring there is only one implementation of
layout findings.
"""

from __future__ import annotations

import argparse
import sys

try:
    from pptx_lint import scan_presentation
except ImportError as exc:
    print("LAYOUT_QA_PASS=false")
    print(f"ERROR={exc}", file=sys.stderr)
    raise SystemExit(3)


def main() -> int:
    ap = argparse.ArgumentParser(description="Legacy PPTX layout QA wrapper / 舊版版面 QA 相容入口")
    ap.add_argument("pptx")
    ap.add_argument("--overlap-threshold", type=float, default=0.15)
    ap.add_argument("--tiny-pt", type=float, default=11.0)
    args = ap.parse_args()

    try:
        result = scan_presentation(
            args.pptx,
            tiny_pt=args.tiny_pt,
            overlap_threshold=args.overlap_threshold,
        )
    except Exception as exc:
        print("LAYOUT_QA_PASS=false")
        print(f"ERROR={exc}", file=sys.stderr)
        return 3

    ok = result["lint_errors"] == 0
    print(f"LAYOUT_QA_PASS={'true' if ok else 'false'}")
    print(f"slides_checked={result['slides_checked']}")
    print(f"layout_errors={result['lint_errors']}")
    print(f"layout_warnings={result['lint_warnings']}")
    print("NOTE=verify_layout.py is a compatibility wrapper; use pptx_lint.py for full findings.")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
