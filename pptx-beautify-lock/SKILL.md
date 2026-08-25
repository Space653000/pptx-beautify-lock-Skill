---
name: pptx-beautify-lock
description: "Beautify, repair, restyle, or auto-format an existing PPT/PPTX while preserving protected content, source visual DNA, brand terrain, and spatial composition. 既有 PowerPoint 需要美化、修重疊/overflow、統一繁中英文雙語字體、重新設計視覺與版面骨骼，但文字/數據/圖片等內容不可變。Runs Content Lock → Theme Discovery → Linter → Auto Formatter → Layout Intelligence → Design Agent → Render Visual QA → Composition QA → Regression."
license: MIT
metadata:
  version: "0.5.0"
  languages: "zh-TW,en"
  compatibility: "Claude Code, Codex, ChatGPT Skills, Agent-Skills-compatible coding agents"
---

# PPTX Beautify Lock v0.5

**繁體中文為主要說明語言；English is retained for cross-agent compatibility.**

## Core contracts / 核心契約

1. **Content Lock**：protected semantics immutable。
2. **Theme Lock**：未授權不得 arbitrary rebrand / light↔dark flip。
3. **Bilingual Typography**：繁中＋英文 glyph-safe、協調、可讀。
4. **Layout Intelligence**：不只禁止 overlap，還要保護 brand terrain、grid rails、spacing rhythm、reading order、visual balance、peer alignment。

必讀：

- `references/CONTENT_LOCK.md`
- `references/THEME_DISCOVERY.md`
- `references/TYPOGRAPHY_BILINGUAL.md`
- `references/LAYOUT_INTELLIGENCE.md`
- `references/DESIGN_AGENT_RULES.md`
- `references/RENDER_VISUAL_QA.md`

## Why v0.5 / 為什麼升級

v0.4 能攔截內容改動、主色翻轉、placeholder、基本 overlap 與 CJK fallback，但真實 MEC 壓測證明：**沒有幾何錯誤的 slide 仍可能構圖很怪。**

v0.5 將 slide design 拆成：

```text
Soul → Frame → Skeleton → Joints → Limbs → Skin
```

先讀 source visual DNA 與品牌地形，再建立骨骼，最後才做表皮設計。

## Full pipeline / 完整品質管線

```text
SOURCE PPTX
  → Content Snapshot
  → Source Theme Discovery
  → Source Render + Slide-role / Brand-terrain discovery
  → PPTX Linter
  → Auto Formatter
  → Layout Intelligence / Spatial QA
  → Design Agent
  → Content + Theme + Spatial Guards
  → Render Visual QA
  → Render Composition QA
  → Regression v0.5
  → FINAL PPTX
```

## 0. Preflight

1. 能讀 source `.pptx`、寫 candidate、執行 scripts。
2. 不覆寫 source。
3. 若 source 有 animation/transition/hyperlink/OLE/SmartArt/comments/accessibility metadata，優先原檔就地修改視覺屬性。
4. 無 renderer 時只能 structural candidate，不能宣稱 v0.5 fully qualified final。

## 1. Content snapshot

```bash
python scripts/pptx_content_lock.py snapshot source.pptx --out content_manifest.json
```

## 2. Source Theme Discovery

```bash
python scripts/pptx_theme_profile.py profile source.pptx --out theme_profile.json
```

必須同時看 source render。若品牌識別烘焙在 full-slide layout/master image，render 才是權威。

## 3. Source Spatial Discovery

逐頁辨識：

- slide role
- brand chrome / footer / logo / department identity
- content-safe / brand-safe zones
- repeated rails
- peer systems
- reading order
- vertical balance

不要把 cover、agenda、section、dense-data、closing 套成同一種模板。

## 4. Linter

```bash
python scripts/pptx_lint.py source.pptx --json > lint.before.json
```

抓 geometry、placeholder、tiny text、table density、CJK fallback、suspicious overlap 等。

## 5. Auto Formatter

先修低風險機械問題：alignment、spacing、geometry、table sizing、text margins、chart plot area。

每次修改後：

```bash
python scripts/pptx_content_lock.py verify source.pptx candidate.pptx
python scripts/pptx_theme_profile.py compare source.pptx candidate.pptx --json
python scripts/pptx_lint.py candidate.pptx --json > lint.after-format.json
```

## 6. Design Agent — Skeleton before Skin

依 `LAYOUT_INTELLIGENCE.md`：

```text
Soul
→ Frame
→ Skeleton
→ Joints
→ Limbs
→ Skin
```

重點：

- brand terrain 不被大面積 panel 壓住
- title/status/logo 不互搶 header band
- summary/table 共用合理 rails
- L/R 或 A/B peer charts 共用尺寸、top/bottom rail、gutter
- spacing 使用少數重複節奏
- dense body 不無理由 top-heavy
- decoration 必須服務 hierarchy/grouping/navigation/brand continuity
- source `20260819` 不得為了美觀改成 `2026/08/19`

## 7. Spatial QA / 機器骨骼檢查

```bash
python scripts/pptx_layout_intelligence.py source.pptx candidate.pptx --json
```

它會抓：

- foreground solid-fill occlusion
- branded/full-bleed background 上新增加大型 solid region 的 review risk
- peer visual rail/size drift
- dense-data vertical-balance risk

Hard requirement：

```text
SPATIAL_QA_PASS=true
```

Warnings 不等於 pass-through；它們必須在 Composition QA 被逐頁處理。

## 8. Render Visual QA

Render source + final 全頁，產生既有 `visual_qa.json` schema 3：

```bash
python scripts/visual_qa_gate.py visual_qa.json --expected-slides <N>
```

必須：

```text
VISUAL_QA_PASS=true
```

## 9. Render Composition QA / v0.5 美感骨骼閘門

另外產生 `composition_qa.json`，逐頁檢查：

- brand chrome
- occlusion
- grid alignment
- peer alignment
- spacing rhythm
- reading order
- visual balance
- slide-role fit
- decorative restraint

並提供 hierarchy/alignment/spacing/balance/brand/restraint/data-legibility 分數與 source-vs-final evidence。

```bash
python scripts/composition_qa_gate.py composition_qa.json --expected-slides <N>
```

必須：

```text
COMPOSITION_QA_PASS=true
```

## 10. Regression v0.5

```bash
python scripts/pptx_regression.py source.pptx candidate.pptx \
  --visual-qa-report visual_qa.json --require-visual-qa \
  --composition-qa-report composition_qa.json --require-composition-qa
```

Fully qualified v0.5 final **只接受**：

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
SPATIAL_QA_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
COMPOSITION_QA_PASS=true
REGRESSION_V05_PASS=true
DELIVERY_V05_PASS=true
```

`DELIVERY_PASS=true` 僅為 v0.4 backward-compatibility field；v0.5 不得拿它當完成證明。

## 11. Repair loop

最多 3 輪：

```text
design
→ content/theme/spatial guards
→ render all slides
→ visual QA
→ composition QA
→ repair rails / spacing / balance / brand zones
```

第 3 輪仍有 blocking defect：fail closed。

## 12. Fail closed

遇到 verifier 無法判定、render 失敗、brand terrain 不清楚、font fallback 不可控、任何 v0.5 Gate 未通過：

- 保留 source 與最近 Content-Lock-safe candidate
- 回報 slide number + failed gate
- 不刪內容、不換圖、不 flatten、不假裝 final

## Minimal activation / 最短啟用語句

```text
Use pptx-beautify-lock v0.5 on this PPTX.
內容 100% 凍結，不 rebrand。
先分析 Source Theme + Brand Terrain + Layout Skeleton，再美化。
執行 Linter → Auto Formatter → Spatial QA → Design Agent → Render Visual QA → Composition QA → Regression v0.5。
只有 DELIVERY_V05_PASS=true 才交付 final。
```

## Final report

```text
OUTPUT=<path>
CONTENT_LOCK_PASS=true|false
THEME_FIDELITY_PASS=true|false
SPATIAL_QA_PASS=true|false
LAYOUT_QA_PASS=true|false
VISUAL_QA_PASS=true|false
COMPOSITION_QA_PASS=true|false
REGRESSION_V05_PASS=true|false
DELIVERY_V05_PASS=true|false
```
