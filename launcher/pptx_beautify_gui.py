#!/usr/bin/env python3
"""Windows PPTX beautifier with offline-first runtime and optional rule updates."""
from __future__ import annotations

from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pptx_offline_engine import STYLE_PRESETS
from offline_runtime import LAUNCHER_VERSION, beautify_to_final
from update_manager import UPDATE_BRANCH

APP_TITLE = f"PPTX Beautify Offline v{LAUNCHER_VERSION}"
PRODUCT_FEATURES = ("input_pptx", "output_pptx", "style", "beautify")
BEAUTIFY_OFFLINE = True
CLOUD_AI_ENABLED = False
NETWORK_REQUIRED = False
OPTIONAL_UPDATE_CHECK = True
STYLE_CHOICES = list(STYLE_PRESETS.keys())


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("920x600")
        self.minsize(800, 520)
        self._q: queue.Queue[str] = queue.Queue()
        self._busy = False
        self._build()
        self.after(100, self._drain_log)

    def _build(self):
        root = ttk.Frame(self, padding=16)
        root.pack(fill="both", expand=True)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(7, weight=1)

        ttk.Label(root, text="PPTX Beautify — Offline-first", font=("Segoe UI", 20, "bold")).grid(
            row=0, column=0, columnspan=3, sticky="w"
        )
        ttk.Label(
            root,
            text="美化完全本機；有網路時只檢查 GitHub 規則更新，沒有網路照常執行",
            font=("Segoe UI", 10),
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 4))
        ttk.Label(
            root,
            text=f"Update channel: {UPDATE_BRANCH}",
            font=("Segoe UI", 9),
        ).grid(row=2, column=0, columnspan=3, sticky="w", pady=(0, 16))

        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.style_var = tk.StringVar(value=STYLE_CHOICES[0])

        ttk.Label(root, text="1. 輸入 PPTX").grid(row=3, column=0, sticky="w", padx=(0, 10))
        ttk.Entry(root, textvariable=self.input_var).grid(row=3, column=1, sticky="ew")
        ttk.Button(root, text="選擇檔案…", command=self._browse_input).grid(row=3, column=2, padx=(8, 0))

        ttk.Label(root, text="2. 輸出 PPTX").grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
        ttk.Entry(root, textvariable=self.output_var).grid(row=4, column=1, sticky="ew", pady=10)
        ttk.Button(root, text="另存位置…", command=self._browse_output).grid(row=4, column=2, padx=(8, 0), pady=10)

        ttk.Label(root, text="3. 美化風格").grid(row=5, column=0, sticky="w", padx=(0, 10))
        style = ttk.Combobox(root, textvariable=self.style_var, values=STYLE_CHOICES, state="readonly")
        style.grid(row=5, column=1, sticky="ew")
        ttk.Label(root, text="固定、可重現的本機風格規則").grid(row=5, column=2, sticky="w", padx=(8, 0))

        ttk.Button(root, text="開始美化", command=self._start_run).grid(
            row=6, column=0, columnspan=3, sticky="ew", pady=(16, 12), ipady=7
        )

        self.log = tk.Text(root, wrap="word", height=15, font=("Consolas", 9))
        self.log.grid(row=7, column=0, columnspan=3, sticky="nsew")
        scroll = ttk.Scrollbar(root, orient="vertical", command=self.log.yview)
        scroll.grid(row=7, column=3, sticky="ns")
        self.log.configure(yscrollcommand=scroll.set)

        self.status_var = tk.StringVar(value="Ready — Offline-capable")
        ttk.Label(root, textvariable=self.status_var).grid(
            row=8, column=0, columnspan=3, sticky="w", pady=(8, 0)
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
            self.output_var.set(str(src.with_name(f"{src.stem}_Offline_Beautified.pptx")))

    def _browse_output(self):
        current = self.output_var.get().strip()
        initial_dir = str(Path(current).parent) if current else None
        initial_file = Path(current).name if current else "Offline_Beautified.pptx"
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
                self.after(0, lambda: messagebox.showerror(APP_TITLE, f"美化失敗：\n{exc}"))
            finally:
                self._busy = False
                self.after(0, lambda: self.status_var.set("Ready — Offline-capable"))

        threading.Thread(target=wrapper, daemon=True).start()

    def _start_run(self):
        def work():
            src = Path(self.input_var.get().strip()).expanduser()
            out = Path(self.output_var.get().strip()).expanduser()
            style = self.style_var.get().strip() or STYLE_CHOICES[0]

            if not src.is_file() or src.suffix.lower() != ".pptx":
                raise ValueError("請選擇有效的來源 .pptx。")
            if out.suffix.lower() != ".pptx":
                raise ValueError("輸出必須是 .pptx 檔案。")
            if src.resolve() == out.resolve():
                raise ValueError("輸出檔不可覆寫來源 PPTX。")

            self._emit("BEAUTIFY_OFFLINE=true")
            self._emit("CLOUD_AI_ENABLED=false")
            self._emit("NETWORK_REQUIRED=false")
            self._emit("OPTIONAL_UPDATE_CHECK=true")
            self._emit(f"Input: {src}")
            self._emit(f"Output: {out}")
            self._emit(f"Style: {style}")

            report = beautify_to_final(src, out, style, self._emit, check_updates=True)

            if not out.is_file() or out.stat().st_size <= 0:
                raise RuntimeError(f"FINAL_OUTPUT_MISSING_AFTER_RETURN: {out}")

            self._emit(
                f"Summary: slides={report.slide_count}, tables={report.tables_styled}, "
                f"data_layouts={report.data_slides_structured}, "
                f"empty_placeholders={report.removed_empty_placeholders}, "
                f"template_artifacts={report.suppressed_template_artifacts}"
            )
            final_size = out.stat().st_size
            self.after(
                0,
                lambda: messagebox.showinfo(
                    APP_TITLE,
                    f"美化完成，而且輸出檔已重新開啟驗證：\n{out}\n\nSize: {final_size:,} bytes",
                ),
            )

        self._thread(work)


if __name__ == "__main__":
    App().mainloop()
