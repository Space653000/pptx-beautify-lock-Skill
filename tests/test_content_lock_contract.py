from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "pptx-beautify-lock" / "scripts" / "pptx_content_lock.py"
LINT_PATH = ROOT / "pptx-beautify-lock" / "scripts" / "pptx_lint.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lock = load_module("pptx_content_lock", LOCK_PATH)
lint = load_module("pptx_lint", LINT_PATH)


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

            diffs = lock.diff(lock.build_manifest(str(src)), lock.build_manifest(str(out)))
            self.assertEqual([], diffs)

    def test_text_change_fails_content_lock(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "src.pptx"
            out = Path(td) / "changed_text.pptx"
            self.make_source(src)

            prs = Presentation(src)
            prs.slides[0].shapes[0].text = "內容被修改 / Content changed"
            prs.save(out)

            diffs = lock.diff(lock.build_manifest(str(src)), lock.build_manifest(str(out)))
            self.assertTrue(diffs)

    def test_table_value_change_fails_content_lock(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "src.pptx"
            out = Path(td) / "changed_table.pptx"
            self.make_source(src)

            prs = Presentation(src)
            table = prs.slides[0].shapes[1].table
            table.cell(1, 1).text = "43"
            prs.save(out)

            diffs = lock.diff(lock.build_manifest(str(src)), lock.build_manifest(str(out)))
            self.assertTrue(diffs)

    def test_linter_can_parse_valid_deck(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "src.pptx"
            self.make_source(src)
            result = lint.scan_presentation(str(src))
            self.assertEqual(1, result["slides_checked"])
            self.assertIn("LINT_PASS", result)


if __name__ == "__main__":
    unittest.main()
