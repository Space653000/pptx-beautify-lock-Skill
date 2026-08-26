import pathlib
import py_compile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class V061ProductizationTests(unittest.TestCase):
    def test_launcher_compiles(self):
        launcher = ROOT / "launcher" / "pptx_beautify_gui.py"
        self.assertTrue(launcher.is_file())
        py_compile.compile(str(launcher), doraise=True)

    def test_launcher_requires_full_deck_regression_and_dual_review(self):
        text = (ROOT / "launcher" / "pptx_beautify_gui.py").read_text(encoding="utf-8")
        for required in [
            "Fix A without breaking B",
            "THREE full-deck review passes",
            "Dual: Claude → Codex",
            "Dual: Codex → Claude",
            "CONTENT_LOCK_PASS=true",
            "GLOBAL_DESIGN_JURY_PASS=true",
            "DELIVERY_V06_PASS=true",
        ]:
            self.assertIn(required, text)

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

    def test_windows_backup_target_is_pinned(self):
        ps1 = (ROOT / "scripts" / "backup_to_windows.ps1").read_text(encoding="utf-8")
        self.assertIn(r"C:\0\_Infinite\_AI\01\_Projects\pptx-beautify-lock-Skil", ps1)
        self.assertIn("fast-forward only", ps1)
        self.assertIn("refuses to overwrite", ps1)


if __name__ == "__main__":
    unittest.main()
