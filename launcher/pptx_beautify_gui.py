#!/usr/bin/env python3
"""Minimal Windows PPTX beautifier launcher.

Product boundary:
- The Skill lives only at the canonical GitHub URL.
- This launcher does not install, clone, update, or back up the Skill.
- The launcher only lets the user choose input, output, and a visual style,
  then delegates the PPTX beautification task to an available AI coding agent.
"""
from __future__ import annotations

import os
from pathlib import Path
import queue
import shutil
import subprocess
import tempfile
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_TITLE = "PPTX Beautify v0.6.2"
CANONICAL_SKILL_URL = "https://github.com/Space653000/pptx-beautify-lock-Skill"

# Stable product contract used by the compiled EXE self-test. These flags are
# intentionally explicit so the test does not depend on source files being
# recoverable from inside a PyInstaller bundle.
PRODUCT_FEATURES = ("input_pptx", "output_pptx", "style", "beautify")
SKILL_INSTALL_ENABLED = False
REPOSITORY_BOOTSTRAP_ENABLED = False
BACKUP_ENABLED = False
AGENT_MODE_SELECTOR_ENABLED = False

STYLE_PRESETS = [
    "自動（忠於原稿 / Source-faithful）",
    "專業技術（Technical Clean）",
    "商務簡潔（Executive Minimal）",
    "現代極簡（Modern Minimal）",
    "高階科技簡報（Premium Tech, preserve source palette）",
]

PROMPT_TEMPLATE = r"""
Before touching the presentation, open and read this canonical Skill repository:
{skill_url}

Treat that GitHub repository as the controlling PPTX beautification contract for
this run. Do NOT install the Skill, do NOT clone/update/modify that repository,
and do NOT treat this EXE as the Skill. Read the URL and follow the repository's
current main-branch instructions.

INPUT PPTX:
{source}

OUTPUT PPTX (must be exactly this path):
{output}

USER VISUAL STYLE PREFERENCE:
{style}

TEMP WORKSPACE (temporary evidence/intermediate files only):
{workdir}

Task:
Beautify the entire input presentation and save the finished deck to OUTPUT PPTX.
Preserve protected content exactly as required by the Skill. Never overwrite the
input. Perform the full-deck QA/regression process required by the Skill before
claiming success.

The selected style is a visual direction only. Content Lock remains absolute.
When the selected style is "自動（忠於原稿 / Source-faithful）", preserve the
source deck's visual DNA, palette polarity, and identity. For any other selected
style, interpret it conservatively and professionally; do not change protected
content, and do not introduce unreadable typography or broken layout.

If you cannot access/read the canonical Skill URL or cannot prove the required
release gates, fail closed and explain the exact blocker. Do not fabricate PASS.
""".strip()


def _which(name: str) -> str | None:
    return shutil.which(name)


def agent_command(engine: str, prompt: str) -> list[str] | None:
    if engine == "Claude Code":
        exe = _which("claude")
        return [exe, "-p", prompt] if exe else None
    if engine == "Codex":
        exe = _which("codex")
        return [exe, "exec", prompt] if exe else None
    raise ValueError(engine)


def choose_agent() -> tuple[str, list[str]] | None:
    """Choose one available agent automatically; keep engine choice out of the UI."""
    claude = _which("claude")
    if claude:
        return "Claude Code", [claude]
    codex = _which("codex")
    if codex:
        return "Codex", [codex]
    return None


def _run(cmd: list[str], cwd: Path, log) -> int:
    log("$ " + subprocess.list2cmdline(cmd))
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=os.environ.copy(),
    )
    assert proc.stdout is not None
    for line in proc.stdout:
        log(line.rstrip())
    return proc.wait()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("900x560")
        self.minsize(780, 480)
        self._q: queue.Queue[str] = queue.Queue()
        self._busy = False
        self._build()
        self.after(100, self._drain_log)

    def _build(self):
        root = ttk.Frame(self, padding=16)
        root.pack(fill="both", expand=True)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(6, weight=1)

        ttk.Label(root, text="PPTX Beautify", font=("Segoe UI", 20, "bold")).grid(
            row=0, column=0, columnspan=3, sticky="w"
        )
        ttk.Label(
            root,
            text="只做一件事：依 GitHub Skill 規則美化 PowerPoint",
            font=("Segoe UI", 10),
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 16))

        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.style_var = tk.StringVar(value=STYLE_PRESETS[0])

        ttk.Label(root, text="1. 輸入 PPTX").grid(row=2, column=0, sticky="w", padx=(0, 10))
        ttk.Entry(root, textvariable=self.input_var).grid(row=2, column=1, sticky="ew")
        ttk.Button(root, text="選擇檔案…", command=self._browse_input).grid(row=2, column=2, padx=(8, 0))

        ttk.Label(root, text="2. 輸出 PPTX").grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
        ttk.Entry(root, textvariable=self.output_var).grid(row=3, column=1, sticky="ew", pady=10)
        ttk.Button(root, text="另存位置…", command=self._browse_output).grid(row=3, column=2, padx=(8, 0), pady=10)

        ttk.Label(root, text="3. 美化風格").grid(row=4, column=0, sticky="w", padx=(0, 10))
        style = ttk.Combobox(root, textvariable=self.style_var, values=STYLE_PRESETS)
        style.grid(row=4, column=1, sticky="ew")
        ttk.Label(root, text="可直接輸入自訂風格").grid(row=4, column=2, sticky="w", padx=(8, 0))

        ttk.Button(root, text="開始美化", command=self._start_run).grid(
            row=5, column=0, columnspan=3, sticky="ew", pady=(16, 12), ipady=6
        )

        self.log = tk.Text(root, wrap="word", height=14, font=("Consolas", 9))
        self.log.grid(row=6, column=0, columnspan=3, sticky="nsew")
        scroll = ttk.Scrollbar(root, orient="vertical", command=self.log.yview)
        scroll.grid(row=6, column=3, sticky="ns")
        self.log.configure(yscrollcommand=scroll.set)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(root, textvariable=self.status_var).grid(
            row=7, column=0, columnspan=3, sticky="w", pady=(8, 0)
        )

    def _browse_input(self):
        path = filedialog.askopenfilename(
            title="選擇來源 PowerPoint",
            filetypes=[("PowerPoint", "*.pptx"), ("All files", "*.*")],
        )
        if not path:
            return
        self.input_var.set(path)
        src = Path(path)
        if not self.output_var.get().strip():
            self.output_var.set(str(src.with_name(f"{src.stem}_Beautified.pptx")))

    def _browse_output(self):
        current = self.output_var.get().strip()
        initial_dir = str(Path(current).parent) if current else None
        initial_file = Path(current).name if current else "Beautified.pptx"
        path = filedialog.asksaveasfilename(
            title="選擇輸出 PowerPoint",
            defaultextension=".pptx",
            filetypes=[("PowerPoint", "*.pptx")],
            initialdir=initial_dir,
            initialfile=initial_file,
        )
        if path:
            self.output_var.set(path)

    def _emit(self, text: str):
        self._q.put(text)

    def _drain_log(self):
        try:
            while True:
                item = self._q.get_nowait()
                self.log.insert("end", item + "\n")
                self.log.see("end")
        except queue.Empty:
            pass
        self.after(100, self._drain_log)

    def _thread(self, target):
        if self._busy:
            messagebox.showwarning(APP_TITLE, "已有美化工作正在執行。")
            return
        self._busy = True
        self.status_var.set("Running…")

        def wrapper():
            try:
                target()
            except Exception as exc:
                self._emit(f"FATAL: {exc}")
                messagebox.showerror(APP_TITLE, f"美化失敗：\n{exc}")
            finally:
                self._busy = False
                self.status_var.set("Ready")

        threading.Thread(target=wrapper, daemon=True).start()

    def _start_run(self):
        def work():
            src = Path(self.input_var.get().strip()).expanduser()
            out = Path(self.output_var.get().strip()).expanduser()
            style = self.style_var.get().strip() or STYLE_PRESETS[0]

            if not src.is_file() or src.suffix.lower() != ".pptx":
                messagebox.showerror(APP_TITLE, "請選擇有效的來源 .pptx。")
                return
            if out.suffix.lower() != ".pptx":
                messagebox.showerror(APP_TITLE, "輸出必須是 .pptx 檔案。")
                return

            try:
                if src.resolve() == out.resolve():
                    messagebox.showerror(APP_TITLE, "輸出檔不可覆寫來源 PPTX。")
                    return
            except OSError:
                pass

            agent = choose_agent()
            if not agent:
                messagebox.showerror(
                    APP_TITLE,
                    "找不到 Claude Code 或 Codex CLI。\n請先安裝並登入其中一個 AI Agent。",
                )
                return
            engine, _ = agent

            out.parent.mkdir(parents=True, exist_ok=True)
            workdir = Path(tempfile.mkdtemp(prefix="pptx-beautify-"))
            self._emit(f"Skill URL: {CANONICAL_SKILL_URL}")
            self._emit(f"Agent: {engine}")
            self._emit(f"Input: {src}")
            self._emit(f"Output: {out}")
            self._emit(f"Style: {style}")

            prompt = PROMPT_TEMPLATE.format(
                skill_url=CANONICAL_SKILL_URL,
                source=src,
                output=out,
                style=style,
                workdir=workdir,
            )
            cmd = agent_command(engine, prompt)
            assert cmd is not None
            rc = _run(cmd, workdir, self._emit)
            if rc != 0:
                messagebox.showerror(APP_TITLE, f"{engine} 執行失敗，請查看 Log。")
                return
            if not out.is_file():
                messagebox.showerror(APP_TITLE, "AI 執行結束，但沒有產生指定的輸出 PPTX。")
                return

            self._emit("BEAUTIFY_PASS=true")
            messagebox.showinfo(APP_TITLE, f"美化完成：\n{out}")

        self._thread(work)


if __name__ == "__main__":
    App().mainloop()
