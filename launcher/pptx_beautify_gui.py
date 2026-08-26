#!/usr/bin/env python3
"""Windows desktop launcher for pptx-beautify-lock.

The launcher is intentionally thin: it selects a local PPTX, ensures the canonical
Skill is installed for Claude Code and/or Codex, delegates the actual redesign to
an agent, then runs machine-checkable local guards. It never overwrites the
source presentation.

Only Python standard library modules are used so the source launcher can run on a
normal Windows Python installation. A GitHub Actions workflow builds a portable
Windows .exe with PyInstaller.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_TITLE = "PPTX Beautify Lock — Global Design Jury"
CANONICAL_REPO = "https://github.com/Space653000/pptx-beautify-lock-Skill"
DEFAULT_BACKUP = r"C:\0\_Infinite\_AI\01\_Projects\pptx-beautify-lock-Skil"
FINAL_SUFFIX = "__TOP_TIER_FINAL.pptx"

PROMPT_TEMPLATE = r"""
Use the installed `pptx-beautify-lock` Skill as the controlling contract.

SOURCE PPTX: {source}
FINAL OUTPUT (must be exactly this path): {output}
WORKSPACE / QA EVIDENCE DIR: {workdir}

Goal:
Create a top-tier global technology customer presentation while preserving 100%
of protected content and the source deck's own identity. The visual standard must
be suitable for executive and engineering reviews at top global technology firms.
Do NOT imitate a brand's superficial skin. Apply Purpose, Hierarchy, Simplicity,
Craft, executive communication structure, technical-density control, and source
identity fidelity.

MANDATORY NON-NEGOTIABLES:
- Never overwrite SOURCE PPTX.
- Content Lock is absolute: do not rewrite, summarize, translate, spell-correct,
  add, delete, reorder, merge, split, or change protected text/data/media/notes.
- Detect the source Theme / Brand Terrain / Deck Identity before changing layout.
- Preserve the source's light/dark/mixed visual DNA unless explicitly instructed.
- Traditional Chinese + English typography must be glyph-safe and visually
  coherent on Windows/PowerPoint. Avoid fragile fonts that silently fall back.
- Empty placeholders and template artifacts must never cover valid content.
- POWER/THD/HOHD or equivalent sibling data-slide families must use a coherent
  table, title, summary, chart, gutter, rail, and typography system unless their
  data structure objectively requires a different geometry.
- Fix A without breaking B: after every repair, regression-check all previously
  passing slides. Never declare a local repair complete until the complete deck
  has been rerendered and rechecked.
- Render source and candidate. XML-only inspection is insufficient.
- Perform at least THREE full-deck review passes for this launcher workflow:
  Pass 1 = Soul/identity, Pass 2 = Skeleton/muscle/layout, Pass 3 = Skin/craft and
  final regression. Each pass must cover every slide.
- If any final gate cannot be proved, FAIL CLOSED and report the failed slide/gate.

REQUIRED PIPELINE:
Content Snapshot -> Theme/Identity Discovery -> Linter -> Auto Formatter ->
Layout Intelligence -> Design Agent -> Content/Theme/Spatial Guards -> full render
-> Visual QA -> Composition QA -> Global Design Jury -> repair/refine -> full render
-> independent full-deck review -> final full render -> Regression.

REQUIRED QA FILES under WORKSPACE / QA EVIDENCE DIR:
- visual_qa.json
- composition_qa.json
- global_design_jury.json
- final_report.txt

The final_report.txt must explicitly contain:
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
SPATIAL_QA_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
COMPOSITION_QA_PASS=true
DECK_IDENTITY_PASS=true
GLOBAL_DESIGN_JURY_PASS=true
REGRESSION_V06_PASS=true
DELIVERY_V06_PASS=true

Do not claim success unless every line is true and the final PPTX exists at the
exact requested output path.
""".strip()

REVIEW_PROMPT = r"""
Act as an independent senior presentation-design QA/release reviewer.
Use the installed `pptx-beautify-lock` Skill as the controlling contract.

ORIGINAL SOURCE: {source}
CANDIDATE TO AUDIT AND, ONLY IF NEEDED, REPAIR IN PLACE: {output}
QA EVIDENCE DIR: {workdir}

Do not redesign for personal taste. Audit every slide against the source.
Specifically attack regressions caused by prior fixes: empty placeholders,
master/template artifacts, font fallback, title clipping, brand-terrain occlusion,
inconsistent sibling-table styling, rail drift, chart misalignment, text/table
crowding, and any situation where fixing one slide degraded another.

Perform a complete rerender of the whole deck. If any defect exists, repair only
what is needed and then rerender/recheck ALL slides again. Preserve protected
content exactly. Regenerate visual_qa.json, composition_qa.json,
global_design_jury.json, and final_report.txt. Release only if every required v0.6
gate is true. Otherwise fail closed and write the exact failed slide/gate.
""".strip()


def _which(name: str) -> str | None:
    return shutil.which(name)


def _run(cmd: list[str], cwd: Path, log, env: dict[str, str] | None = None) -> int:
    log("$ " + subprocess.list2cmdline(cmd))
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=merged_env,
    )
    assert proc.stdout is not None
    for line in proc.stdout:
        log(line.rstrip())
    return proc.wait()


def installed_skill_dirs() -> list[Path]:
    home = Path.home()
    return [
        home / ".claude" / "skills" / "pptx-beautify-lock",
        home / ".codex" / "skills" / "pptx-beautify-lock",
    ]


def locate_skill_dir() -> Path | None:
    for path in installed_skill_dirs():
        if (path / "SKILL.md").is_file() and (path / "scripts").is_dir():
            return path
    return None


def install_from_checkout(repo_dir: Path, log) -> bool:
    installer = repo_dir / "scripts" / "install_skill.py"
    if not installer.is_file():
        log(f"ERROR: missing installer: {installer}")
        return False
    rc = _run([sys.executable, str(installer), "--target", "both", "--force"], repo_dir, log)
    return rc == 0


def update_canonical_repo(cache_dir: Path, log) -> Path | None:
    git = _which("git")
    if not git:
        log("ERROR: git.exe not found. Install Git for Windows or place a repo checkout beside this launcher.")
        return None
    repo_dir = cache_dir / "pptx-beautify-lock-Skill"
    if (repo_dir / ".git").is_dir():
        if _run([git, "fetch", "origin", "main"], repo_dir, log) != 0:
            return None
        # Fast-forward only; never discard local modifications.
        if _run([git, "merge", "--ff-only", "origin/main"], repo_dir, log) != 0:
            log("ERROR: local cache has divergent/local changes. Resolve them instead of overwriting.")
            return None
    else:
        cache_dir.mkdir(parents=True, exist_ok=True)
        if _run([git, "clone", "--depth", "1", CANONICAL_REPO, str(repo_dir)], cache_dir, log) != 0:
            return None
    return repo_dir


def agent_command(engine: str, prompt: str) -> list[str] | None:
    if engine == "Claude Code":
        exe = _which("claude")
        return [exe, "-p", prompt] if exe else None
    if engine == "Codex":
        exe = _which("codex")
        return [exe, "exec", prompt] if exe else None
    raise ValueError(engine)


def run_local_structural_guards(skill_dir: Path, source: Path, output: Path, workdir: Path, log) -> bool:
    scripts = skill_dir / "scripts"
    checks = [
        [sys.executable, str(scripts / "pptx_content_lock.py"), "verify", str(source), str(output)],
        [sys.executable, str(scripts / "pptx_theme_profile.py"), "compare", str(source), str(output), "--json"],
        [sys.executable, str(scripts / "pptx_layout_intelligence.py"), str(source), str(output), "--json"],
        [sys.executable, str(scripts / "pptx_lint.py"), str(output), "--json"],
    ]
    ok = True
    for cmd in checks:
        if not Path(cmd[1]).is_file():
            log(f"ERROR: missing QA script: {cmd[1]}")
            return False
        rc = _run(cmd, workdir, log)
        ok = ok and rc == 0
    return ok


def final_report_is_green(workdir: Path) -> tuple[bool, str]:
    report = workdir / "final_report.txt"
    if not report.is_file():
        return False, "final_report.txt is missing"
    text = report.read_text(encoding="utf-8", errors="replace")
    required = [
        "CONTENT_LOCK_PASS=true",
        "THEME_FIDELITY_PASS=true",
        "SPATIAL_QA_PASS=true",
        "LAYOUT_QA_PASS=true",
        "VISUAL_QA_PASS=true",
        "COMPOSITION_QA_PASS=true",
        "DECK_IDENTITY_PASS=true",
        "GLOBAL_DESIGN_JURY_PASS=true",
        "REGRESSION_V06_PASS=true",
        "DELIVERY_V06_PASS=true",
    ]
    missing = [item for item in required if item not in text]
    return (not missing, "OK" if not missing else "missing: " + ", ".join(missing))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("920x680")
        self.minsize(820, 580)
        self._q: queue.Queue[str] = queue.Queue()
        self._busy = False
        self._build()
        self.after(100, self._drain_log)

    def _build(self):
        root = ttk.Frame(self, padding=14)
        root.pack(fill="both", expand=True)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(6, weight=1)

        ttk.Label(root, text="PPTX Beautify Lock", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")
        ttk.Label(root, text="Content Lock + Global Design Jury + full-deck regression", font=("Segoe UI", 10)).grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 12))

        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.engine_var = tk.StringVar(value="Dual: Claude → Codex")

        ttk.Label(root, text="來源 PPTX").grid(row=2, column=0, sticky="w", padx=(0, 8))
        ttk.Entry(root, textvariable=self.input_var).grid(row=2, column=1, sticky="ew")
        ttk.Button(root, text="選擇檔案…", command=self._browse_input).grid(row=2, column=2, padx=(8, 0))

        ttk.Label(root, text="輸出資料夾").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(root, textvariable=self.output_var).grid(row=3, column=1, sticky="ew", pady=6)
        ttk.Button(root, text="選擇資料夾…", command=self._browse_output).grid(row=3, column=2, padx=(8, 0), pady=6)

        ttk.Label(root, text="執行模式").grid(row=4, column=0, sticky="w", padx=(0, 8))
        engine = ttk.Combobox(root, textvariable=self.engine_var, state="readonly", values=[
            "Dual: Claude → Codex",
            "Dual: Codex → Claude",
            "Claude Code",
            "Codex",
        ])
        engine.grid(row=4, column=1, sticky="w")

        btns = ttk.Frame(root)
        btns.grid(row=5, column=0, columnspan=3, sticky="ew", pady=12)
        ttk.Button(btns, text="1. 安裝 / 更新 Skill", command=self._start_install).pack(side="left")
        ttk.Button(btns, text="2. 頂級美化", command=self._start_run).pack(side="left", padx=8)
        ttk.Button(btns, text="全面備份", command=self._start_backup).pack(side="left")
        ttk.Button(btns, text="開啟輸出資料夾", command=self._open_output).pack(side="left", padx=8)

        self.log = tk.Text(root, wrap="word", height=20, font=("Consolas", 9))
        self.log.grid(row=6, column=0, columnspan=3, sticky="nsew")
        scroll = ttk.Scrollbar(root, orient="vertical", command=self.log.yview)
        scroll.grid(row=6, column=3, sticky="ns")
        self.log.configure(yscrollcommand=scroll.set)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(root, textvariable=self.status_var).grid(row=7, column=0, columnspan=3, sticky="w", pady=(8, 0))

    def _browse_input(self):
        path = filedialog.askopenfilename(filetypes=[("PowerPoint", "*.pptx"), ("All files", "*.*")])
        if path:
            self.input_var.set(path)
            if not self.output_var.get():
                self.output_var.set(str(Path(path).parent / "PPTX_Beautified"))

    def _browse_output(self):
        path = filedialog.askdirectory()
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
            messagebox.showwarning(APP_TITLE, "已有工作正在執行。")
            return
        self._busy = True
        self.status_var.set("Running…")
        def wrapper():
            try:
                target()
            except Exception as exc:
                self._emit(f"FATAL: {exc}")
            finally:
                self._busy = False
                self.status_var.set("Ready")
        threading.Thread(target=wrapper, daemon=True).start()

    def _cache_root(self) -> Path:
        base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
        return base / "pptx-beautify-lock"

    def _ensure_install(self) -> bool:
        repo = update_canonical_repo(self._cache_root(), self._emit)
        return bool(repo and install_from_checkout(repo, self._emit))

    def _start_install(self):
        self._thread(lambda: messagebox.showinfo(APP_TITLE, "Skill 安裝 / 更新完成。") if self._ensure_install() else messagebox.showerror(APP_TITLE, "Skill 安裝失敗，請看 Log。"))

    def _start_backup(self):
        def work():
            repo = update_canonical_repo(Path(DEFAULT_BACKUP).parent, self._emit)
            if not repo:
                messagebox.showerror(APP_TITLE, "備份失敗，請看 Log。")
                return
            target = Path(DEFAULT_BACKUP)
            if repo != target:
                if target.exists():
                    self._emit(f"Backup target already exists: {target}")
                else:
                    shutil.copytree(repo, target)
                    self._emit(f"Backup copied to: {target}")
            messagebox.showinfo(APP_TITLE, f"備份完成：\n{target}")
        self._thread(work)

    def _start_run(self):
        def work():
            src = Path(self.input_var.get().strip()).expanduser()
            if not src.is_file() or src.suffix.lower() != ".pptx":
                messagebox.showerror(APP_TITLE, "請先選擇有效的 .pptx 檔案。")
                return
            outdir = Path(self.output_var.get().strip() or (src.parent / "PPTX_Beautified"))
            outdir.mkdir(parents=True, exist_ok=True)
            if not self._ensure_install():
                messagebox.showerror(APP_TITLE, "Skill 安裝 / 更新失敗。")
                return
            skill = locate_skill_dir()
            if not skill:
                messagebox.showerror(APP_TITLE, "找不到已安裝的 pptx-beautify-lock Skill。")
                return

            stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            workdir = outdir / ".pptx_beautify_work" / f"{src.stem}_{stamp}"
            workdir.mkdir(parents=True, exist_ok=True)
            source_copy = workdir / "SOURCE.pptx"
            shutil.copy2(src, source_copy)
            final = outdir / f"{src.stem}{FINAL_SUFFIX}"

            mode = self.engine_var.get()
            if mode.startswith("Dual: Claude"):
                engines = ["Claude Code", "Codex"]
            elif mode.startswith("Dual: Codex"):
                engines = ["Codex", "Claude Code"]
            else:
                engines = [mode]
            for eng in engines:
                if agent_command(eng, "test") is None:
                    messagebox.showerror(APP_TITLE, f"找不到 {eng} CLI。請先安裝並登入。")
                    return

            primary_prompt = PROMPT_TEMPLATE.format(source=source_copy, output=final, workdir=workdir)
            cmd = agent_command(engines[0], primary_prompt)
            assert cmd is not None
            self._emit(f"=== PRIMARY: {engines[0]} ===")
            rc = _run(cmd, workdir, self._emit)
            if rc != 0 or not final.is_file():
                messagebox.showerror(APP_TITLE, f"主要 Agent 未成功產生 Final。\n工作目錄：{workdir}")
                return

            if len(engines) == 2:
                self._emit(f"=== INDEPENDENT REVIEW: {engines[1]} ===")
                review = REVIEW_PROMPT.format(source=source_copy, output=final, workdir=workdir)
                cmd2 = agent_command(engines[1], review)
                assert cmd2 is not None
                if _run(cmd2, workdir, self._emit) != 0:
                    messagebox.showerror(APP_TITLE, f"第二 Agent 審核失敗。\n工作目錄：{workdir}")
                    return

            self._emit("=== LOCAL STRUCTURAL RELEASE GUARDS ===")
            structural = run_local_structural_guards(skill, source_copy, final, workdir, self._emit)
            report_ok, report_msg = final_report_is_green(workdir)
            if not structural or not report_ok:
                messagebox.showerror(APP_TITLE, f"Release Gate 未通過：{report_msg}\n保留候選檔供檢查：\n{final}\nQA：{workdir}")
                return

            self._emit(f"DELIVERY_V06_PASS=true\nFINAL={final}")
            messagebox.showinfo(APP_TITLE, f"完成並通過 Release Gate：\n{final}")
        self._thread(work)

    def _open_output(self):
        path = Path(self.output_var.get().strip() or ".")
        path.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            os.startfile(str(path))  # type: ignore[attr-defined]
        else:
            subprocess.Popen(["xdg-open", str(path)])


if __name__ == "__main__":
    App().mainloop()
