# pptx-beautify-lock-Skill v0.6.2

**繁體中文為主 / English compatible**

給 Claude Code、ChatGPT / Codex 與其他 Agent 使用的 **PowerPoint 內容凍結＋來源風格鎖定＋No-Degradation＋版面智慧＋全簡報回歸防護** Skill。

核心原則：

> **Original wins ties. Fix A without breaking B.** 原稿已經合理就不要為了「看起來有改」而亂改；任何 repair 後都要重新 render / review 全部 slides。

## 1. Canonical Skill URL

這個 repository 就是唯一 canonical Skill source：

```text
https://github.com/Space653000/pptx-beautify-lock-Skill
```

要讓 AI 使用時，直接把這個 URL 給 Claude Code / Codex / ChatGPT，要求它先讀取最新版 `main` 再執行 PPTX 工作即可。

## 2. 三個產品邊界完全分開

### A. Skill — AI Agent 路徑

只存在並維護在這個 GitHub repository。它定義 PPTX beautification / Content Lock / Theme Fidelity / No-Degradation / QA / Regression 規則。

AI Agent 使用完整 v0.6.2 Strict Production / Global Design Jury / Original-wins-ties 契約。

### B. Windows Offline Beautifier EXE — Offline-first 本機路徑

`PPTX-Beautify-Offline.exe` 只負責：

1. 任意選擇輸入 `.pptx`
2. 任意指定輸出 `.pptx`
3. 選擇本機規則風格
4. 按下 **開始離線美化**

美化本身完全本機：

```text
不呼叫 Claude / Codex / 雲端 AI
不需要 Git
不需要外部 Python
沒有網路也能完成美化
```

若有網路，EXE 只會短暫檢查 GitHub stable update channel 是否有較新的規則引擎；沒網路就跳過更新，不影響本機美化。

#### v0.7.3 Source-faithful Safe-only

預設：

```text
自動（忠於原稿 / Source-faithful）
```

現在是嚴格 **safe-only / no-degradation mode**：

- 不重排 geometry / z-order
- 不放大或替換既有字體
- 不修改 table geometry/style
- 不修改 image/media crop/position
- 不改 theme/master/layout/background/brand terrain
- 不為了讓畫面「不同」而新增 card/panel/gradient
- 預設只允許 proofing metadata 等不影響版面的低風險修正

而且輸出會做 PPTX package 級驗證：除 allowlisted proofing metadata 外，任何 slide visual XML 或其他 package part 發生變更都 FAIL CLOSED。

因此 Source-faithful 可能看起來幾乎和原稿一樣；如果原稿本來就比 generic formatter 好，這就是正確結果。

其他 `Technical Clean / Executive Minimal / Modern Minimal / Premium Tech` 是明確 opt-in 的 transformative styles，不等於 Source-faithful。

詳細說明：[`launcher/README.md`](launcher/README.md)

### C. Standalone GitHub Backup BAT

`BACKUP-pptx-beautify-lock-Skill.bat` 是完全獨立的雙擊工具，只負責把這個 GitHub repository 完整抓到 BAT 所在資料夾。

## 3. Strict Production Contract（AI Skill）

```text
Content Snapshot
→ Source Theme + Deck Identity + Brand Terrain
→ full source render
→ Source quality baseline
→ No-Degradation / Safe-change Budget
→ Linter
→ defect-driven Auto Formatter
→ Layout Intelligence
→ Design Agent
→ Content / Theme / Spatial / No-Degradation Guards
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
Pass 1 = Soul / 靈魂 / source baseline
Pass 2 = Skeleton + Muscle / 骨骼＋肌肉
Pass 3 = Skin + Regression / 表皮＋回歸
```

每一輪都必須覆蓋 **所有 slides**。

## 4. No-Degradation Rule

完整規格：[`pptx-beautify-lock/references/NO_DEGRADATION_RULES.md`](pptx-beautify-lock/references/NO_DEGRADATION_RULES.md)

每個視覺改動至少要證明：

```text
KNOWN_DEFECT=true
LOCAL_REPAIR=true
BOUNDED_CHANGE=true
BEFORE_AFTER_IMPROVEMENT=true
NO_NEW_REGRESSION=true
```

無法證明就 rollback。**A no-op is better than a harmful edit.**

## 5. 特別強化的 release blockers

- **No-Degradation / Original wins ties** — candidate 不得只是「不同」，必須淨改善。
- **Empty placeholder / template artifact** — 只有確認真的干擾有效內容才修，不能因為 placeholder 存在就亂刪。
- **Font portability** — 繁中＋英文要在 Windows/PowerPoint 實際可用；serif fallback、巨大字體、裁切、換行漂移直接 FAIL。
- **Sibling data-slide parity** — 只在確認同族頁與實際 inconsistency defect 後才統一 POWER / THD / HOHD 等 visual grammar。
- **Brand terrain isolation** — logo、department identity、tagline、master chrome 不被新 panel 壓住。
- **Full-deck regression** — 修任何一頁後重新 render / review 全簡報，確認先前通過頁面沒退化。

## 6. AI Skill Final Gates

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
NO_DEGRADATION_GATE_PASS=true
REGRESSION_V06_PASS=true
DELIVERY_V06_PASS=true
EMPTY_PLACEHOLDER_PASS=true
FONT_PORTABILITY_PASS=true
SIBLING_STYLE_PARITY_PASS=true
FULL_DECK_REGRESSION_PASS=true
THREE_PASS_REVIEW_PASS=true
```

任一無法證明：FAIL CLOSED。

## 7. Build Windows offline beautifier

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

Windows runner 必須真的執行 compiled EXE self-test。Self-test 未通過不得上傳 artifact。

## 8. Standalone backup

把：

```text
BACKUP-pptx-beautify-lock-Skill.bat
```

放到想保存 backup 的 Windows 資料夾，雙擊即可。

它會在 BAT 同層建立／更新完整 Git repository：

```text
pptx-beautify-lock-Skill\
```
