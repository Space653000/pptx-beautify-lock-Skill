from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install_skill.py"


class InstallerContractTests(unittest.TestCase):
    def test_installs_same_skill_for_claude_and_codex(self):
        with tempfile.TemporaryDirectory() as td:
            env = dict(os.environ)
            env["HOME"] = td
            result = subprocess.run(
                [sys.executable, str(INSTALLER), "--target", "both", "--force"],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("INSTALL_PASS=true", result.stdout)

            claude = Path(td) / ".claude" / "skills" / "pptx-beautify-lock" / "SKILL.md"
            codex = Path(td) / ".codex" / "skills" / "pptx-beautify-lock" / "SKILL.md"
            source = ROOT / "pptx-beautify-lock" / "SKILL.md"

            self.assertTrue(claude.is_file())
            self.assertTrue(codex.is_file())
            self.assertEqual(source.read_bytes(), claude.read_bytes())
            self.assertEqual(source.read_bytes(), codex.read_bytes())


if __name__ == "__main__":
    unittest.main()
