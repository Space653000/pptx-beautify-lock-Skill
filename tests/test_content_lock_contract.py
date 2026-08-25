from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "pptx-beautify-lock" / "scripts" / "pptx_content_lock.py"
LINT = ROOT / "pptx-beautify-lock" / "scripts" / "pptx_lint.py"
VISUAL_QA = ROOT / "pptx-beautify-lock" / "scripts" / "visual_qa_gate.py"
REGRESSION = ROOT / "pptx-beautify-lock" / "scripts" / "pptx_regression.py"


def run_script(script: Path, *args: str):
    return subprocess.run(
        [sys.executable, str(script), *map(str, args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class ContentLockContractTests(unittest.TestCase):
    def make_source(self, path: Path):
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        box = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(5), Inches(1))
        run = box.text_frame.paragraphs[0].add_run()
        run.text = "內容不可修改 / Content must not change 123.45%"
        run.font.size = Pt(18)

        table_shape = slide.shapes.add_table(2, 2, Inches(1), Inches(2.2), Inches(5), Inches(1.5))
        table = table_shape.table
        table.cell(0, 0).text = "項目"
        table.cell(0, 1).text = "數值"
        table.cell(1, 0).text = "A"
        table.cell(1, 1).text = "42"
        prs.save(path)

    def assert_content_passes(self, src: Path, out: Path):
        result = run_script(LOCK, "verify", src, out)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("CONTENT_LOCK_PASS=true", result.stdout)

    def assert_content_fails(self, src: Path, out: Path):
        result = run_script(LOCK, "verify", src, out)
        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("CONTENT_LOCK_PASS=false", result.stdout)

    def test_visual_only_change_passes_content_lock(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "src.pptx"
            out = Path(td) / "visual_only.pptx"
            self.make_source(src)

            prs = Presentation(src)
            text_shape = prs.slides[0].shapes[0]
            for p in text_shape.text_frame.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(30)
                    r.font.bold = True
            text_shape.left = Inches(1.5)
            prs.save(out)

            self.assert_content_passes(src, out)

    def test_run_segmentation_change_passes_content_lock(self):
        """Restyling tools may split one text run into several without changing text."""
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "one-run.pptx"
            out = Path(td) / "two-runs.pptx"

            prs = Presentation()
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            box = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(5), Inches(1))
            paragraph = box.text_frame.paragraphs[0]
            paragraph.add_run().text = "Hello world"
            prs.save(src)

            prs2 = Presentation(src)
            paragraph2 = prs2.slides[0].shapes[0].text_frame.paragraphs[0]
            paragraph2.clear()
            r1 = paragraph2.add_run()
            r1.text = "Hello "
            r1.font.bold = True
            r2 = paragraph2.add_run()
            r2.text = "world"
            r2.font.italic = True
            prs2.save(out)

            self.assert_content_passes(src, out)

    def test_text_change_fails_content_lock(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "src.pptx"
            out = Path(td) / "changed_text.pptx"
            self.make_source(src)

            prs = Presentation(src)
            prs.slides[0].shapes[0].text = "內容被修改 / Content changed"
            prs.save(out)

            self.assert_content_fails(src, out)

    def test_table_value_change_fails_content_lock(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "src.pptx"
            out = Path(td) / "changed_table.pptx"
            self.make_source(src)

            prs = Presentation(src)
            prs.slides[0].shapes[1].table.cell(1, 1).text = "43"
            prs.save(out)

            self.assert_content_fails(src, out)

    def test_table_merge_semantics_change_fails_content_lock(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "merged.pptx"
            out = Path(td) / "split.pptx"

            prs = Presentation()
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            table = slide.shapes.add_table(2, 2, Inches(1), Inches(1), Inches(5), Inches(2)).table
            table.cell(0, 0).text = "Merged"
            table.cell(0, 1).text = ""
            table.cell(1, 0).text = "A"
            table.cell(1, 1).text = "B"
            table.cell(0, 0).merge(table.cell(0, 1))
            prs.save(src)

            prs2 = Presentation(src)
            prs2.slides[0].shapes[0].table.cell(0, 0).split()
            prs2.save(out)

            self.assert_content_fails(src, out)

    def test_hyperlink_target_change_fails_content_lock(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "link-a.pptx"
            out = Path(td) / "link-b.pptx"

            prs = Presentation()
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            box = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(5), Inches(1))
            run = box.text_frame.paragraphs[0].add_run()
            run.text = "Open link"
            run.hyperlink.address = "https://example.com/a"
            prs.save(src)

            prs2 = Presentation(src)
            run2 = prs2.slides[0].shapes[0].text_frame.paragraphs[0].runs[0]
            run2.hyperlink.address = "https://example.com/b"
            prs2.save(out)

            self.assert_content_fails(src, out)

    def test_swapping_hyperlinks_between_objects_fails_content_lock(self):
        """The same global link set is not enough; links must remain with their objects."""
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "links-source.pptx"
            out = Path(td) / "links-swapped.pptx"

            prs = Presentation()
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            for index, (label, target) in enumerate((
                ("Document A", "https://example.com/a"),
                ("Document B", "https://example.com/b"),
            )):
                box = slide.shapes.add_textbox(Inches(1), Inches(1 + index), Inches(5), Inches(0.7))
                run = box.text_frame.paragraphs[0].add_run()
                run.text = label
                run.hyperlink.address = target
            prs.save(src)

            prs2 = Presentation(src)
            a_run = prs2.slides[0].shapes[0].text_frame.paragraphs[0].runs[0]
            b_run = prs2.slides[0].shapes[1].text_frame.paragraphs[0].runs[0]
            a_run.hyperlink.address = "https://example.com/b"
            b_run.hyperlink.address = "https://example.com/a"
            prs2.save(out)

            self.assert_content_fails(src, out)

    def test_hidden_slide_state_change_fails_content_lock(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "hidden.pptx"
            out = Path(td) / "shown.pptx"

            prs = Presentation()
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            slide.shapes.add_textbox(Inches(1), Inches(1), Inches(4), Inches(1)).text = "Hidden slide"
            slide._element.set("show", "0")
            prs.save(src)

            prs2 = Presentation(src)
            prs2.slides[0]._element.set("show", "1")
            prs2.save(out)

            self.assert_content_fails(src, out)

    def test_linter_public_cli_parses_valid_deck(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "src.pptx"
            self.make_source(src)
            result = run_script(LINT, src, "--json")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(1, payload["slides_checked"])
            self.assertIn("LINT_PASS", payload)

    def test_linter_detects_tiny_text_inside_table(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "tiny-table.pptx"
            self.make_source(src)
            prs = Presentation(src)
            cell = prs.slides[0].shapes[1].table.cell(1, 1)
            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(6)
            prs.save(src)

            result = run_script(LINT, src, "--json")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            rules = [finding["rule"] for finding in payload["findings"]]
            self.assertIn("tiny-text", rules)

    def test_visual_qa_public_gate_requires_every_slide_and_check(self):
        with tempfile.TemporaryDirectory() as td:
            report_path = Path(td) / "visual_qa.json"
            checks = {
                "no_unintended_overlap": True,
                "no_clipping_or_overflow": True,
                "content_visible": True,
                "text_readable": True,
                "hierarchy_clear": True,
                "alignment_consistent": True,
                "tables_charts_readable": True,
                "style_consistent": True,
            }
            report = {
                "schema": 1,
                "slide_count": 2,
                "render_engine": "PowerPoint",
                "reviewer": "AI vision reviewer",
                "overall_pass": True,
                "slides": [
                    {"slide": 1, "score": 90, "checks": dict(checks)},
                    {"slide": 2, "score": 88, "checks": dict(checks)},
                ],
            }
            report_path.write_text(json.dumps(report), encoding="utf-8")
            good = run_script(VISUAL_QA, report_path, "--expected-slides", "2")
            self.assertEqual(0, good.returncode, good.stdout + good.stderr)
            self.assertIn("VISUAL_QA_PASS=true", good.stdout)

            report["slides"][1]["checks"]["no_clipping_or_overflow"] = False
            report_path.write_text(json.dumps(report), encoding="utf-8")
            bad = run_script(VISUAL_QA, report_path, "--expected-slides", "2")
            self.assertNotEqual(0, bad.returncode)
            self.assertIn("VISUAL_QA_PASS=false", bad.stdout)

    def test_regression_requires_visual_report_for_delivery(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "src.pptx"
            out = Path(td) / "out.pptx"
            self.make_source(src)
            Presentation(src).save(out)

            result = run_script(REGRESSION, src, out, "--require-visual-qa")
            self.assertNotEqual(0, result.returncode)
            self.assertIn("DELIVERY_PASS=false", result.stdout)
            self.assertIn("VISUAL_QA_PASS=false", result.stdout)

    def test_plugin_manifests_point_to_installable_skill(self):
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual("pptx-beautify-lock", plugin["name"])
        self.assertIn("./pptx-beautify-lock", plugin["skills"])
        self.assertTrue((ROOT / "pptx-beautify-lock" / "SKILL.md").exists())
        self.assertEqual("space653000-pptx", marketplace["name"])
        self.assertEqual(plugin["name"], marketplace["plugins"][0]["name"])


if __name__ == "__main__":
    unittest.main()
