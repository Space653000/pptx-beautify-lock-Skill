from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
GUI = ROOT / "launcher" / "pptx_beautify_gui.py"
PORTABLE = ROOT / "launcher" / "pptx_beautify_portable.py"
WORKFLOW = ROOT / ".github" / "workflows" / "build-windows-launcher.yml"
BACKUP_BAT = ROOT / "BACKUP-pptx-beautify-lock-Skill.bat"


def load_portable():
    launcher = str(ROOT / "launcher")
    if launcher not in sys.path:
        sys.path.insert(0, launcher)
    spec = importlib.util.spec_from_file_location("pptx_beautify_portable_test", PORTABLE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PortableLauncherTests(unittest.TestCase):
    def test_portable_self_test_passes(self):
        module = load_portable()
        self.assertEqual(module._portable_self_test(), 0)

    def test_gui_has_only_input_output_style_beautify_product_controls(self):
        text = GUI.read_text(encoding="utf-8")
        self.assertIn("1. 輸入 PPTX", text)
        self.assertIn("2. 輸出 PPTX", text)
        self.assertIn("3. 美化風格", text)
        self.assertIn("開始美化", text)
        self.assertIn("asksaveasfilename", text)
        self.assertNotIn("安裝 / 更新 Skill", text)
        self.assertNotIn("全面備份", text)
        self.assertNotIn("執行模式", text)

    def test_gui_reads_canonical_skill_url_without_install_or_repo_bootstrap(self):
        text = GUI.read_text(encoding="utf-8")
        self.assertIn(
            "https://github.com/Space653000/pptx-beautify-lock-Skill",
            text,
        )
        self.assertIn("open and read this canonical Skill repository", text)
        self.assertNotIn("install_from_checkout", text)
        self.assertNotIn("update_canonical_repo", text)
        self.assertNotIn("backup_to_windows.ps1", text)
        self.assertNotIn("git clone", text.lower())

    def test_backup_is_a_separate_double_click_bat(self):
        text = BACKUP_BAT.read_text(encoding="utf-8")
        self.assertIn("%~dp0pptx-beautify-lock-Skill", text)
        self.assertIn("git clone", text)
        self.assertIn("fetch --all --tags --prune", text)
        self.assertIn("pull --ff-only", text)

    def test_windows_build_is_minimal_and_self_tests_compiled_exe(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("launcher/pptx_beautify_portable.py", workflow)
        self.assertIn("--name PPTX-Beautify", workflow)
        self.assertIn("--portable-self-test", workflow)
        self.assertNotIn("--collect-all pptx", workflow)
        self.assertNotIn("-r requirements.txt", workflow)


if __name__ == "__main__":
    unittest.main()
