#!/usr/bin/env python3
"""PyInstaller entry point for the beautify-only Windows EXE."""
from __future__ import annotations

import sys

import pptx_beautify_gui as core


def _portable_self_test() -> int:
    """Validate the compiled launcher contract without opening the GUI."""
    try:
        expected_url = "https://github.com/Space653000/pptx-beautify-lock-Skill"
        expected_features = ("input_pptx", "output_pptx", "style", "beautify")
        if core.CANONICAL_SKILL_URL != expected_url:
            return 10
        if tuple(core.PRODUCT_FEATURES) != expected_features:
            return 11
        if len(core.STYLE_PRESETS) < 3:
            return 12
        if core.SKILL_INSTALL_ENABLED:
            return 13
        if core.REPOSITORY_BOOTSTRAP_ENABLED:
            return 14
        if core.BACKUP_ENABLED:
            return 15
        if core.AGENT_MODE_SELECTOR_ENABLED:
            return 16
        if not callable(core.App):
            return 17
        return 0
    except Exception:
        return 18


if __name__ == "__main__":
    if "--portable-self-test" in sys.argv:
        raise SystemExit(_portable_self_test())
    core.App().mainloop()
