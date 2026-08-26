from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PORTABLE = ROOT / "launcher" / "pptx_beautify_portable.py"
WORKFLOW = ROOT / ".github" / "workflows" / "build-windows-launcher.yml"


def load_portable():
    import sys

    launcher = str(ROOT / "launcher")
    if launcher not in sys.path:
        sys.path.insert(0, launcher)
    spec = importlib.util.spec_from_file_location("pptx_beautify_portable_test", PORTABLE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PortableLauncherTests(unittest.TestCase):
    def test_in_process_script_runner_captures_output_and_exit_code(self):
        module = load_portable()
        logs: list[str] = []
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = root / "probe.py"
            script.write_text("print('PORTABLE_PROBE_OK')\nraise SystemExit(0)\n", encoding="utf-8")
            rc = module._run_python_script(script, [], root, logs.append)
        self.assertEqual(rc, 0)
        self.assertIn("PORTABLE_PROBE_OK", logs)

    def test_in_process_script_runner_preserves_nonzero_exit(self):
        module = load_portable()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = root / "probe_fail.py"
            script.write_text("raise SystemExit(7)\n", encoding="utf-8")
            rc = module._run_python_script(script, [], root, lambda _: None)
        self.assertEqual(rc, 7)

    def test_portable_entry_does_not_spawn_sys_executable_for_python_scripts(self):
        text = PORTABLE.read_text(encoding="utf-8")
        self.assertNotIn("[sys.executable", text)
        self.assertIn("runpy.run_path", text)
        self.assertIn("archive/refs/heads/main.zip", text)

    def test_windows_build_targets_portable_entry_and_bundles_pptx_runtime(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("launcher/pptx_beautify_portable.py", workflow)
        self.assertIn("-r requirements.txt", workflow)
        self.assertIn("--collect-all pptx", workflow)


if __name__ == "__main__":
    unittest.main()
