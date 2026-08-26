# pptx-beautify-lock-Skill v0.6.1

**繁體中文為主 / English compatible**

給 Claude Code、ChatGPT / Codex 與其他 Agent 使用的 **PowerPoint 內容凍結＋來源風格鎖定＋版面智慧＋全簡報回歸防護** Skill。

核心原則：

> **Fix A without breaking B.** 任何 repair 後都要重新 render / review 全部 slides，不能修好一頁又弄壞另一頁。

## 1. Canonical Skill URL

這個 repository 就是唯一 canonical Skill source：

```text
https://github.com/Space653000/pptx-beautify-lock-Skill
```

要讓 AI 使用時，直接把這個 URL 給 Claude Code / Codex / ChatGPT，要求它先讀取最新版 `main` 再執行 PPTX 工作即可。

本 repo 不需要依賴另一個中央 Skill Catalog 才能成立。

## 2. 三個產品邊界完全分開

### A. Skill — AI Agent 路徑

只存在並維護在這個 GitHub repository。它定義 PPTX beautification / Content Lock / Theme Fidelity / QA / Regression 規則。

AI Agent 可直接讀這個 URL，使用完整 v0.6.1 Strict Production / Global Design Jury 能力。

### B. Windows Offline Beautifier EXE — 完全本機路徑

`PPTX-Beautify-Offline.exe` 是另一個**完全離線、規則式、可重現**的本機工具，只負責：

1. 任意選擇輸入 `.pptx`
2. 任意指定輸出 `.pptx`
3. 選擇美化風格
4. 按下 **開始離線美化**

執行時：

```text
不呼叫外部 AI
不讀 GitHub
不發 HTTP request
不需要網路
不需要 Git
不需要外部 Python
```

EXE 內建 `python-pptx` / Pillow / lxml 與 semantic Content Lock helper，採 deterministic local engine 做 placeholder cleanup、字體安全化、table parity、source accent、high-confidence cover/data-slide layout repair，最後以 Content Lock fail closed。

**重要界線：**完全離線版沒有大型語言／視覺模型，所以不是雲端 AI 的離線替身。它適合工程簡報的大量結構整理、一致化與保守美化；需要 bespoke art direction / 深度語意判斷時，仍使用上面的 canonical Skill URL 讓 AI Agent 執行。

詳細說明：[`launcher/README.md`](launcher/README.md)

### C. Standalone GitHub Backup BAT

`BACKUP-pptx-beautify-lock-Skill.bat` 是完全獨立的雙擊工具，只負責把這個 GitHub repository 完整抓到 BAT 所在資料夾。

它不啟動 PPTX 美化，也不啟動 Skill 安裝。

## 3. Strict Production Contract（AI Skill）

```text
Content Snapshot
→ Source Theme + Deck Identity + Brand Terrain
→ full source render
→ Linter
→ Auto Formatter
→ Layout Intelligence
→ Design Agent
→ Content / Theme / Spatial Guards
→ full render
→ Visual QA
→ Composition QA
→ Global Design Jury
→ repair / refine
→ full-deck rerender
→ independent full-deck review
→ final full-deck rerender
→ Regression
```

Production workflow 至少三輪完整審查：

```text
Pass 1 = Soul / 靈魂
Pass 2 = Skeleton + Muscle / 骨骼＋肌肉
Pass 3 = Skin + Regression / 表皮＋回歸
```

每一輪都必須覆蓋 **所有 slides**。

## 4. 特別強化的 release blockers

- **Empty placeholder purge** — 空 title/body placeholder、`presentation title`、`Speaker name or subtitle` 等不得擋有效內容。
- **Font portability** — 繁中＋英文要在 Windows/PowerPoint 實際可用；serif fallback、巨大字體、裁切、換行漂移直接 FAIL。
- **Sibling data-slide parity** — POWER / THD / HOHD、6σ / 5σ / 4σ、L/R 等同族頁要共享成熟 table/chart visual grammar。
- **Brand terrain isolation** — logo、department identity、tagline、master chrome 不被新 panel 壓住。
- **Full-deck regression** — 修任何一頁後重新 render / review 全簡報，確認先前通過頁面沒退化。

完整規則：[`pptx-beautify-lock/references/REGRESSION_GUARDRAILS.md`](pptx-beautify-lock/references/REGRESSION_GUARDRAILS.md)

## 5. AI Skill Final Gates

Fully qualified AI final 必須至少：

```text
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
EMPTY_PLACEHOLDER_PASS=true
FONT_PORTABILITY_PASS=true
SIBLING_STYLE_PARITY_PASS=true
FULL_DECK_REGRESSION_PASS=true
THREE_PASS_REVIEW_PASS=true
```

任一無法證明：FAIL CLOSED。

## 6. Build Windows offline beautifier

GitHub Actions workflow：

```text
build-windows-launcher
```

會建立：

```text
PPTX-Beautify-Offline.exe
```

artifact：

```text
PPTX-Beautify-Offline-Windows
```

Windows runner 必須真的執行 compiled EXE self-test。Self-test 會建立臨時 PPTX → 本機美化 → semantic Content Lock → 重新開啟輸出；未通過不得上傳 artifact。

## 7. Standalone backup

把：

```text
BACKUP-pptx-beautify-lock-Skill.bat
```

放到想保存 backup 的 Windows 資料夾，雙擊即可。

它會在 BAT 同層建立／更新：

```text
pptx-beautify-lock-Skill\
```

使用完整 Git clone，因此保留 repository 與 Git history；再次執行採 fast-forward only，不強制覆寫本地修改。
