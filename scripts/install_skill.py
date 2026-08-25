#!/usr/bin/env python3
"""Install pptx-beautify-lock into Claude Code and/or Codex skill directories.

Designed for the "paste the GitHub URL and let the agent bootstrap itself" flow.
The script only copies this repository's `pptx-beautify-lock/` directory; it does
not download arbitrary code or modify shell profiles.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "pptx-beautify-lock"
TARGETS = {
    "claude": Path.home() / ".claude" / "skills" / "pptx-beautify-lock",
    "codex": Path.home() / ".codex" / "skills" / "pptx-beautify-lock",
}


def install_one(name: str, target: Path, force: bool) -> dict:
    if not SOURCE.is_dir() or not (SOURCE / "SKILL.md").is_file():
        raise SystemExit(f"Invalid repository checkout: missing {SOURCE / 'SKILL.md'}")

    existed = target.exists()
    if existed and not force:
        return {
            "target": name,
            "path": str(target),
            "status": "already-installed",
            "changed": False,
        }

    if existed:
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, target)

    return {
        "target": name,
        "path": str(target),
        "status": "installed" if not existed else "updated",
        "changed": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Install pptx-beautify-lock Skill")
    parser.add_argument(
        "--target",
        choices=("claude", "codex", "both", "auto"),
        default="auto",
        help="Where to install. auto installs to detected harness directories; if none exist, installs both.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing installed copy with the repository copy.",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable status")
    args = parser.parse_args()

    if args.target == "both":
        selected = ["claude", "codex"]
    elif args.target in TARGETS:
        selected = [args.target]
    else:
        detected = [name for name, path in TARGETS.items() if path.parent.parent.exists()]
        selected = detected or ["claude", "codex"]

    results = [install_one(name, TARGETS[name], args.force) for name in selected]
    payload = {
        "INSTALL_PASS": True,
        "source": str(SOURCE),
        "results": results,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("INSTALL_PASS=true")
        for result in results:
            print(f"{result['target']}={result['status']} path={result['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
