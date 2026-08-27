from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
GUI = ROOT / "launcher" / "pptx_beautify_gui.py"
ENGINE = ROOT / "launcher" / "pptx_offline_engine.py"
RUNTIME = ROOT / "launcher" / "offline_runtime.py"
UPDATER = ROOT / "launcher" / "update_manager.py"
PORTABLE = ROOT / "launcher" / "pptx_beautify_portable.py"
WORKFLOW = ROOT / ".github" / "workflows" / "build-windows-launcher.yml"
BACKUP_BAT = ROOT / "BACKUP-pptx-beautify-lock-Skill.bat"


def load_portable():
    for path in (ROOT / "launcher", ROOT / "pptx-beautify-lock" / "scripts"):
        value = str(path)
        if value not in sys.path:
            sys.path.insert(0, value)
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
        self.assertIn("開始離線美化", text)
        self.assertIn("asksaveasfilename", text)
        self.assertNotIn("安裝 / 更新 Skill", text)
        self.assertNotIn("全面備份", text)
        self.assertNotIn("執行模式", text)

    def test_beautification_stays_local_but_update_check_is_optional(self):
        gui = GUI.read_text(encoding="utf-8")
        engine = ENGINE.read_text(encoding="utf-8")
        updater = UPDATER.read_text(encoding="utf-8")
        self.assertIn("BEAUTIFY_OFFLINE = True", gui)
        self.assertIn("CLOUD_AI_ENABLED = False", gui)
        self.assertIn("NETWORK_REQUIRED = False", gui)
        self.assertIn("OPTIONAL_UPDATE_CHECK = True", gui)
        for forbidden in (
            "subprocess.Popen", "shutil.which", "claude.CMD", "codex exec",
            "PROMPT_TEMPLATE", "CANONICAL_SKILL_URL", "requests.get",
        ):
            self.assertNotIn(forbidden, gui + "\n" + engine)
        self.assertNotIn("urllib", engine)
        self.assertIn("urllib.request", updater)
        self.assertIn("fix/separate-skill-exe-backup-v062", updater)
        self.assertIn("beautify_to_final", gui)
        self.assertIn("CONTENT_LOCK_FAIL", engine)

    def test_runtime_requires_real_final_output_before_success(self):
        text = RUNTIME.read_text(encoding="utf-8")
        self.assertIn("os.replace(candidate, out)", text)
        self.assertIn("FINAL_OUTPUT_EXISTS=true", text)
        self.assertIn("FINAL_OUTPUT_REOPEN_PASS=true", text)
        self.assertIn("OFFLINE_BEAUTIFY_PASS=true", text)
        self.assertIn("OUTPUT_MISSING", text)

    def test_backup_remains_a_separate_double_click_bat(self):
        text = BACKUP_BAT.read_text(encoding="utf-8")
        self.assertIn("%~dp0pptx-beautify-lock-Skill", text)
        self.assertIn("git clone", text)
        self.assertIn("fetch --all --tags --prune", text)
        self.assertIn("pull --ff-only", text)

    def test_windows_build_bundles_local_pptx_runtime_and_self_tests_exe(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("python-pptx Pillow lxml", workflow)
        self.assertIn("--name PPTX-Beautify-Offline", workflow)
        self.assertIn("--hidden-import pptx_content_lock", workflow)
        self.assertIn("--portable-self-test", workflow)
        self.assertNotIn("BACKUP-pptx-beautify-lock-Skill.bat", workflow)


if __name__ == "__main__":
    unittest.main()
