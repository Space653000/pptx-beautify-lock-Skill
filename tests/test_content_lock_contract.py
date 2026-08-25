from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "pptx-beautify-lock" / "scripts" / "pptx_content_lock.py"
LINT_PATH = ROOT / "pptx-beautify-lock" / "scripts" / "pptx_lint.py"
VISUAL_QA_PATH = ROOT / "pptx-beautify-lock" / "scripts" / "visual_qa_gate.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


lock = load_module("pptx_content_lock", LOCK_PATH)
lint = load_module("pptx_lint", LINT_PATH)
visual_qa = load_module("visual_qa_gate", VISUAL_QA_PATH)


class ContentLockContractTests(unittest.TestCase):
    def make_source(self, path: Path):
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        box = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(5), Inches(1))
        run = box.text_frame.paragraphs[0].add_run()
        run.text = "內容不可修改 / Content must not change 123.45%"
        run.font.size = Pt(18)

        rows, cols = 2, 2
        table_shape = slide.shapes.add_table(rows, cols, Inches(1), Inches(2.2), Inches(5), Inches(1.5))
        table = table_shape.table
        table.cell(0, 0).text = "項目"
        table.cell(0, 1).text = "數值"
        table.cell(1, 0).text = "A"
        table.cell(1, 1).text = "42"
        prs.save(path)

    def assert_content_same(self, src: Path, out: Path):
        diffs = lock.diff(lock.build_manifest(str(src)), lock.build_manifest(str(out)))
        self.assertEqual([], diffs)

    def assert_content_changed(self, src: Path, out: Path):
        diffs = lock.diff(lock.build_manifest(str(src)), lock.build_manifest(str(out)))
        self.assertTrue(diffs)

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

            self.assert_content_same(src, out)

    def test_text_change_fails_content_lock(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "src.pptx"
            out = Path(td) / "changed_text.pptx"
            self.make_source(src)

            prs = Presentation(src)
            prs.slides[0].shapes[0].text = "內容被修改 / Content changed"
            prs.save(out)

            self.assert_content_changed(src, out)

    def test_table_value_change_fails_content_lock(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "src.pptx"
            out = Path(td) / "changed_table.pptx"
            self.make_source(src)

            prs = Presentation(src)
            table = prs.slides[0].shapes[1].table
            table.cell(1, 1).text = "43"
            prs.save(out)

            self.assert_content_changed(src, out)

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

            self.assert_content_changed(src, out)

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

            self.assert_content_changed(src, out)

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

            self.assert_content_changed(src, out)

    def test_linter_can_parse_valid_deck(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "src.pptx"
            self.make_source(src)
            result = lint.scan_presentation(str(src))
            self.assertEqual(1, result["slides_checked"])
            self.assertIn("LINT_PASS", result)

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

            result = lint.scan_presentation(str(src))
            rules = [f["rule"] for f in result["findings"]]
            self.assertIn("tiny-text", rules)

    def test_visual_qa_gate_requires_every_slide_and_every_check(self):
        good_checks = {key: True for key in visual_qa.REQUIRED_CHECKS}
        report = {
            "schema": 1,
            "slide_count": 2,
            "render_engine": "PowerPoint",
            "reviewer": "AI vision reviewer",
            "overall_pass": True,
            "slides": [
                {"slide": 1, "score": 90, "checks": dict(good_checks)},
                {"slide": 2, "score": 88, "checks": dict(good_checks)},
            ],
        }
        ok, errors = visual_qa.validate_report(report, expected_slides=2, min_score=85)
        self.assertTrue(ok, errors)

        report["slides"][1]["checks"]["no_clipping_or_overflow"] = False
        ok, errors = visual_qa.validate_report(report, expected_slides=2, min_score=85)
        self.assertFalse(ok)
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
