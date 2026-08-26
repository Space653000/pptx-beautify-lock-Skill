#!/usr/bin/env python3
"""Portable Windows entry point for PPTX Beautify Lock.

This entry point wraps the normal GUI while removing two assumptions that are
unsafe in a PyInstaller one-file build:

1. ``sys.executable`` is the launcher EXE, not a general Python interpreter.
2. a random Windows PC may not have Git installed.

Canonical Python scripts are executed in-process by the Python runtime bundled
inside the EXE. The public canonical repository is refreshed from GitHub's main
branch ZIP for normal beautification/install flows. The optional full Git backup
button can still use the canonical PowerShell backup script and may require Git
because its purpose is to preserve repository history, not merely a source ZIP.
"""
from __future__ import annotations

import contextlib
import io
import os
from pathlib import Path
import runpy
import shutil
import sys
import tempfile
import traceback
import urllib.request
import zipfile

# Explicit imports make PyInstaller include the strict PPTX runtime dependencies.
# They are intentionally unused directly here.
import lxml  # noqa: F401
import PIL  # noqa: F401
import pptx  # noqa: F401

import pptx_beautify_gui as core

CANONICAL_ZIP = (
    "https://github.com/Space653000/pptx-beautify-lock-Skill/"
    "archive/refs/heads/main.zip"
)


def _run_python_script(
    script: Path,
    args: list[str],
    cwd: Path,
    log,
) -> int:
    """Execute a canonical Python script inside the bundled interpreter."""
    if not script.is_file():
        log(f"ERROR: missing Python script: {script}")
        return 2

    old_argv = sys.argv[:]
    old_cwd = Path.cwd()
    old_path = sys.path[:]
    capture = io.StringIO()
    code = 0

    try:
        os.chdir(cwd)
        sys.argv = [str(script), *args]
        # Match normal ``python path/to/script.py`` import behavior closely.
        for candidate in (str(script.parent), str(cwd)):
            if candidate not in sys.path:
                sys.path.insert(0, candidate)

        with contextlib.redirect_stdout(capture), contextlib.redirect_stderr(capture):
            try:
                runpy.run_path(str(script), run_name="__main__")
            except SystemExit as exc:
                if exc.code is None:
                    code = 0
                elif isinstance(exc.code, int):
                    code = exc.code
                else:
                    print(exc.code)
                    code = 1
            except Exception:
                traceback.print_exc()
                code = 1
    finally:
        sys.argv = old_argv
        sys.path[:] = old_path
        os.chdir(old_cwd)

    for line in capture.getvalue().splitlines():
        log(line)
    return code


def _download_main_checkout(cache_dir: Path, log) -> Path | None:
    """Refresh a clean canonical main snapshot without requiring Git."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    target = cache_dir / "pptx-beautify-lock-Skill"

    with tempfile.TemporaryDirectory(prefix="pptx-beautify-refresh-") as tmp:
        tmp_root = Path(tmp)
        archive = tmp_root / "main.zip"
        extracted = tmp_root / "extracted"
        extracted.mkdir()

        try:
            log(f"Downloading canonical main: {CANONICAL_ZIP}")
            request = urllib.request.Request(
                CANONICAL_ZIP,
                headers={"User-Agent": "PPTX-Beautify-Lock-v0.6.1"},
            )
            with urllib.request.urlopen(request, timeout=90) as response, archive.open("wb") as out:
                shutil.copyfileobj(response, out)

            with zipfile.ZipFile(archive) as zf:
                zf.extractall(extracted)

            roots = [p for p in extracted.iterdir() if p.is_dir()]
            if len(roots) != 1:
                log("ERROR: unexpected canonical ZIP layout")
                return None
            source = roots[0]

            required = [
                source / "scripts" / "install_skill.py",
                source / "pptx-beautify-lock" / "SKILL.md",
            ]
            if not all(path.is_file() for path in required):
                log("ERROR: downloaded canonical repository failed integrity check")
                return None

            staging = cache_dir / "pptx-beautify-lock-Skill.__new__"
            previous = cache_dir / "pptx-beautify-lock-Skill.__previous__"
            shutil.rmtree(staging, ignore_errors=True)
            shutil.rmtree(previous, ignore_errors=True)
            shutil.copytree(source, staging)

            if target.exists():
                target.rename(previous)
            staging.rename(target)
            shutil.rmtree(previous, ignore_errors=True)
            log(f"Canonical main refreshed: {target}")
            return target
        except Exception as exc:
            log(f"ERROR: canonical main refresh failed: {exc}")
            return None


def install_from_checkout(repo_dir: Path, log) -> bool:
    installer = repo_dir / "scripts" / "install_skill.py"
    rc = _run_python_script(
        installer,
        ["--target", "both", "--force"],
        repo_dir,
        log,
    )
    return rc == 0


def run_local_structural_guards(
    skill_dir: Path,
    source: Path,
    output: Path,
    workdir: Path,
    log,
) -> bool:
    scripts = skill_dir / "scripts"
    checks = [
        (scripts / "pptx_content_lock.py", ["verify", str(source), str(output)]),
        (
            scripts / "pptx_theme_profile.py",
            ["compare", str(source), str(output), "--json"],
        ),
        (
            scripts / "pptx_layout_intelligence.py",
            [str(source), str(output), "--json"],
        ),
        (scripts / "pptx_lint.py", [str(output), "--json"]),
    ]

    ok = True
    for script, args in checks:
        rc = _run_python_script(script, args, workdir, log)
        ok = ok and rc == 0
    return ok


# Patch the thin GUI's execution seams. All UI and release policy stay canonical
# to pptx_beautify_gui.py; only runtime/bootstrap mechanics change here.
core.update_canonical_repo = _download_main_checkout
core.install_from_checkout = install_from_checkout
core.run_local_structural_guards = run_local_structural_guards


if __name__ == "__main__":
    core.App().mainloop()
