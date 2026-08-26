#!/usr/bin/env python3
"""PyInstaller entry point for the beautify-only Windows EXE."""
from __future__ import annotations

import sys

import pptx_beautify_gui as core


def _portable_self_test() -> int:
    """Validate the compiled launcher contract without opening the GUI."""
    try:
        if core.CANONICAL_SKILL_URL != "https://github.com/Space653000/pptx-beautify-lock-Skill":
            return 10
        if len(core.STYLE_PRESETS) < 3:
            return 11
        source = __import__("inspect").getsource(core)
        banned = [
            "安裝 / 更新 Skill",
            "全面備份",
            "install_from_checkout",
            "update_canonical_repo",
            "backup_to_windows.ps1",
        ]
        if any(item in source for item in banned):
            return 12
        if "asksaveasfilename" not in source:
            return 13
        if "CANONICAL_SKILL_URL" not in source:
            return 14
        return 0
    except Exception:
        return 15


if __name__ == "__main__":
    if "--portable-self-test" in sys.argv:
        raise SystemExit(_portable_self_test())
    core.App().mainloop()
