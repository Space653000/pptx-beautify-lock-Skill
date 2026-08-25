---
name: pptx-beautify-lock
description: "Beautify, repair, restyle, or auto-format an existing PPT/PPTX while preserving protected content and the source visual DNA. 既有 PowerPoint 需要美化、修排版、修重疊/overflow、統一繁中英文雙語字體或重新設計視覺，但文字/數據/圖片等內容不可變，且未授權時不得翻轉原主色調。Runs Content Lock → Source Theme Discovery → PPTX Linter → Auto Formatter → Design Agent → Render Visual QA → Regression Test."
license: MIT
metadata:
  version: "0.4.0"
  languages: "zh-TW,en"
  compatibility: "Claude Code, Codex, ChatGPT Skills, Agent-Skills-compatible coding agents"
---

# PPTX Beautify Lock

**繁體中文為主要說明語言；English is used for cross-agent compatibility.**

## Leading contracts / 核心契約

1. **Content Lock**：protected semantics immutable。
2. **Theme Lock**：未經使用者明確授權，不得把來源 light/dark/mixed visual DNA 翻轉或 arbitrary rebrand。
3. **Bilingual Typography**：繁體中文＋英文都必須 glyph-safe、協調、可讀。

Content Lock 唯一定義：[`references/CONTENT_LOCK.md`](references/CONTENT_LOCK.md)。

Theme / Typography：

- [`references/THEME_DISCOVERY.md`](references/THEME_DISCOVERY.md)
- [`references/TYPOGRAPHY_BILINGUAL.md`](references/TYPOGRAPHY_BILINGUAL.md)

完整品質管線：

```text
SOURCE PPTX
  → Content Snapshot
  → Source Theme Discovery / Visual DNA
  → PPTX Linter
  → Auto Formatter
  → Design Agent
  → Content + Theme Guard
  → Render Visual QA
  → Regression Test
  → FINAL PPTX
```

---

## 0. Preflight / 開工條件

1. 確認能讀 source `.pptx`、寫新的 `.pptx`、執行 scripts。
2. 不原地覆寫來源。
3. 讀 `CONTENT_LOCK.md`、`THEME_DISCOVERY.md`、`TYPOGRAPHY_BILINGUAL.md`。
4. 若來源有 animation/transition/hyperlink/OLE/SmartArt/comments/accessibility metadata，優先原檔就地修改視覺屬性。
5. 無 renderer 時只能做 structural candidate，不得宣稱 fully qualified delivery。

---

## 1. Content snapshot / 內容基準

```bash
python scripts/pptx_content_lock.py snapshot source.pptx --out content_manifest.json
```

**Gate:** snapshot 成功。

---

## 2. Source Theme Discovery / 先找主色調，不先設計

在任何 design decision 前：

```bash
python scripts/pptx_theme_profile.py profile source.pptx --out theme_profile.json
```

必須辨識：

- `light / dark / mixed / unknown` canvas
- page-role pattern
- theme/master/accent colors
- large-area background/fill evidence
- source explicit fonts / theme fonts
- source content 是否偏 light technical / dark presentation / branded corporate 等

若可 render，必須看**來源 render**校正 machine profile；不得只看首頁。

### Default rule

- 原本白底 → 保持 light
- 原本 dark → 保持 dark
- mixed → 保留各頁角色模式
- 原已有主色 → 沿用 hue family

除非使用者明確要求換色系，**Beautify ≠ Rebrand**。

**Gate:** `theme_profile.json` 已建立。

---

## 3. PPTX Linter / 找出問題

讀 [`references/LINTER_RULES.md`](references/LINTER_RULES.md)：

```bash
python scripts/pptx_lint.py source.pptx --json > lint.before.json
```

必查：

- out-of-bounds / invalid geometry
- overlap
- template placeholder leakage
- tiny text / dense tables
- unsafe margins
- title/font consistency
- CJK/Latin fallback risk（能偵測時）

Linter 是 structural/heuristic；真正 overflow、美觀、theme fidelity、字體 fallback 仍以 render 為準。

---

## 4. Auto Formatter / 低風險機械修復

讀 [`references/AUTO_FORMATTER_RULES.md`](references/AUTO_FORMATTER_RULES.md)。

先修：grid、alignment、spacing、geometry、table sizing、text margins、chart plot area。

不得：

- 改內容
- 翻轉來源主色調
- 為科技感任意加入大面積 navy/black
- 用 Latin-only font 承擔繁中 mixed text

修改後立即：

```bash
python scripts/pptx_content_lock.py verify source.pptx candidate.pptx
python scripts/pptx_theme_profile.py compare source.pptx candidate.pptx --json
python scripts/pptx_lint.py candidate.pptx --json > lint.after-format.json
```

**Gate:** Content Lock PASS；Theme Guard 無 blocking inversion；hard errors 不增加。

---

## 5. Design Agent / 視覺重構

讀：

- [`references/DESIGN_AGENT_RULES.md`](references/DESIGN_AGENT_RULES.md)
- [`references/DESIGN_RULES.md`](references/DESIGN_RULES.md)

目標：**source-faithful executive-ready redesign**。

允許大幅改 composition、grid、cards、table/chart style、typography hierarchy，但：

- Content Lock 永遠有效
- Theme Lock 預設有效
- 繁中＋英文都要安全漂亮
- 真正內容優先於 generic placeholder
- 保留 native editable objects

### Repair loop

最多 3 輪：

```text
design
→ Content Lock verify
→ Theme Guard compare
→ render
→ visual review
→ repair
```

---

## 6. Render Visual QA / 逐頁真的看

讀 [`references/RENDER_VISUAL_QA.md`](references/RENDER_VISUAL_QA.md)。

Render 全部 source/final slides（來源能 render 時），產生 `visual_qa.json` schema 3。

每頁必須包含：

- no unintended overlap
- no clipping/overflow
- content visible/readable
- hierarchy/alignment/table/chart/style
- no template placeholder artifacts
- **theme_fidelity_preserved**
- **bilingual_typography_clean**

```bash
python scripts/visual_qa_gate.py visual_qa.json --expected-slides <N>
```

**Gate:** `VISUAL_QA_PASS=true`。

---

## 7. Regression Test / 最終品質閘門

```bash
python scripts/pptx_regression.py source.pptx candidate.pptx \
  --visual-qa-report visual_qa.json \
  --require-visual-qa
```

Fully qualified final 只接受：

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
REGRESSION_PASS=true
DELIVERY_PASS=true
```

任何 false：candidate 不是 final。

---

## 8. Fail closed / 保守失敗

遇到 verifier 無法判定、theme confidence 低、重要物件遺失、font fallback 不可控、render 失敗或任何 Gate 未通過：

- 保留 source 與最近 Content-Lock-safe candidate
- 明確回報失敗 Gate / slide
- 不改內容、不刪內容、不換圖、不 flatten slide 來硬過關

---

## 9. Agent autonomy / 自動化行為

當使用者要求「既有 PPT 內容不變，只美化」：

- 自動啟用本 Skill
- 不逐頁詢問一般排版偏好
- **先辨識來源主色調與字體，再開始設計**
- 若沒有使用者 rebrand 指令，預設沿用 source visual DNA
- 自動完成 Snapshot → Theme Discovery → Lint → Format → Design → Render QA → Regression

---

## 10. Minimal activation / 最短指令

```text
Use pptx-beautify-lock on this PPTX.
啟用 Content Lock + Theme Lock。
先辨識來源主色調與繁中/英文字體，再美化。
自動執行 Theme Discovery → Linter → Auto Formatter → Design Agent → Render Visual QA → Regression Test。
只有 DELIVERY_PASS=true 才交付 final PPTX。
```

---

## 11. Final report / 最終回報

```text
OUTPUT=<path/to/final.pptx>
SOURCE_CANVAS_MODE=light|dark|mixed|unknown
OUTPUT_CANVAS_MODE=light|dark|mixed|unknown
CONTENT_LOCK_PASS=true|false
THEME_FIDELITY_PASS=true|false
LAYOUT_QA_PASS=true|false
VISUAL_QA_PASS=true|false
REGRESSION_PASS=true|false
DELIVERY_PASS=true|false
LINT_ERRORS=<N>
LINT_WARNINGS=<N>
```

不要只回覆「已美化完成」；每個品質 Gate 都是交付的一部分。
