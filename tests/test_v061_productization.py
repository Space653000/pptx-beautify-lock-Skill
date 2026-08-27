import pathlib
import py_compile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class V061ProductizationTests(unittest.TestCase):
    def test_launcher_compiles(self):
        launcher = ROOT / "launcher" / "pptx_beautify_gui.py"
        self.assertTrue(launcher.is_file())
        py_compile.compile(str(launcher), doraise=True)

    def test_launcher_is_beautify_only_offline_capable_with_optional_update(self):
        text = (ROOT / "launcher" / "pptx_beautify_gui.py").read_text(encoding="utf-8")
        for required in [
            "1. 輸入 PPTX",
            "2. 輸出 PPTX",
            "3. 美化風格",
            "開始離線美化",
            "BEAUTIFY_OFFLINE = True",
            "CLOUD_AI_ENABLED = False",
            "NETWORK_REQUIRED = False",
            "OPTIONAL_UPDATE_CHECK = True",
        ]:
            self.assertIn(required, text)
        for forbidden in [
            "open and read this canonical Skill repository",
            "PROMPT_TEMPLATE",
            "subprocess.Popen",
            "Claude Code",
            "Codex CLI",
            "安裝 / 更新 Skill",
            "全面備份",
            "Dual: Claude → Codex",
            "Dual: Codex → Claude",
            "backup_to_windows.ps1",
        ]:
            self.assertNotIn(forbidden, text)

    def test_strict_guardrails_exist(self):
        guard = (ROOT / "pptx-beautify-lock" / "references" / "REGRESSION_GUARDRAILS.md").read_text(encoding="utf-8")
        for required in [
            "修 A 壞 B",
            "Empty placeholder",
            "Font portability",
            "Sibling data-slide parity",
            "POWER / THD / HOHD",
            "THREE_PASS_REVIEW_PASS=true",
        ]:
            self.assertIn(required, guard)

    def test_skill_is_v061_and_loads_guardrails(self):
        skill = (ROOT / "pptx-beautify-lock" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn('version: "0.6.1"', skill)
        self.assertIn("references/REGRESSION_GUARDRAILS.md", skill)
        self.assertIn("FULL_DECK_REGRESSION_PASS=true", skill)
        self.assertIn("FONT_PORTABILITY_PASS=true", skill)

    def test_backup_is_standalone_bat_next_to_repo_root(self):
        bat = ROOT / "BACKUP-pptx-beautify-lock-Skill.bat"
        self.assertTrue(bat.is_file())
        text = bat.read_text(encoding="utf-8")
        self.assertIn("%~dp0pptx-beautify-lock-Skill", text)
        self.assertIn("git clone", text)
        self.assertIn("pull --ff-only", text)
        self.assertFalse((ROOT / "scripts" / "backup_to_windows.ps1").exists())


if __name__ == "__main__":
    unittest.main()
