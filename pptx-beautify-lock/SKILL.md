---
name: pptx-beautify-lock
description: "Beautify, repair, restyle, or auto-format an existing PPT/PPTX while preserving protected content, source visual DNA, brand terrain, spatial composition, and deck identity. 既有 PowerPoint 需要美化、修重疊/overflow、統一繁中英文雙語字體、重新設計視覺與版面骨骼，但文字/數據/圖片等內容不可變。Runs Content Lock → Theme Discovery → Linter → Auto Formatter → Layout Intelligence → Design Agent → Render Visual QA → Composition QA → Global Design Jury → Regression v0.6."
license: MIT
metadata:
  version: "0.6.0"
  languages: "zh-TW,en"
  compatibility: "Claude Code, Codex, ChatGPT Skills, Agent-Skills-compatible coding agents"
---

# PPTX Beautify Lock v0.6 — Global Design Jury

**繁體中文為主要說明語言；English is retained for cross-agent compatibility.**

## Core contracts / 核心契約

1. **Content Lock** — protected semantics immutable。
2. **Theme Lock** — 未授權不得 arbitrary rebrand / light↔dark flip。
3. **Bilingual Typography** — 繁中＋英文 glyph-safe、協調、可讀。
4. **Layout Intelligence** — brand terrain、grid rails、spacing rhythm、reading order、visual balance、peer alignment 都是正式品質條件。
5. **Deck Identity Guard** — 美化後仍必須是原 deck 的成熟版本，不可模板化收斂。
6. **Global Design Jury** — 世界級不是套某品牌的皮；要同時通過 Purpose/Hierarchy/Simplicity/Craft、Executive Communication、Domain/Role Fit 三個 lens。

必讀：

- `references/CONTENT_LOCK.md`
- `references/THEME_DISCOVERY.md`
- `references/TYPOGRAPHY_BILINGUAL.md`
- `references/LAYOUT_INTELLIGENCE.md`
- `references/DESIGN_AGENT_RULES.md`
- `references/RENDER_VISUAL_QA.md`
- `references/GLOBAL_DESIGN_JURY.md`

## Why v0.6 / 為什麼再升級

v0.5 能抓內容、主色、placeholder、基本幾何與構圖問題，但「整齊」仍不等於「全球頂級」。

v0.6 的關鍵原則：

> **不是學 Apple 的皮，而是學 Purpose、Hierarchy、Simplicity、Craft 的苛刻程度；不是學顧問公司的模板，而是學 executive communication 的結構；不是學 technical keynote 的配色，而是學資訊密度與視覺焦點的控制。**

世界級 final 必須讓每一頁都能回答：

```text
Why does this slide exist?
What is the first thing to see?
What is the second thing to see?
Why is every element here?
Why does this still unmistakably belong to the source deck?
```

## Full pipeline / 完整品質管線

```text
SOURCE PPTX
  → Content Snapshot
  → Source Theme Discovery
  → Source Render + Slide-role / Brand-terrain / Personality discovery
  → PPTX Linter
  → Auto Formatter
  → Layout Intelligence / Spatial QA
  → Design Agent — Skeleton before Skin
  → Content + Theme + Spatial Guards
  → Render Visual QA
  → Render Composition QA
  → Global Design Jury round 1
  → repair / refine
  → Global Design Jury round 2
  → Regression v0.6
  → FINAL PPTX
```

## 0. Preflight

1. 能讀 source `.pptx`、寫 candidate、執行 scripts。
2. 不覆寫 source。
3. 若 source 有 animation/transition/hyperlink/OLE/SmartArt/comments/accessibility metadata，優先原檔就地修改視覺屬性。
4. 無 renderer 時只能 structural candidate，不能宣稱 v0.6 final。
5. 不得先挑「漂亮模板」。先理解 source soul / audience / role。

## 1. Content Snapshot

```bash
python scripts/pptx_content_lock.py snapshot source.pptx --out content_manifest.json
```

## 2. Source Theme + Identity Discovery

```bash
python scripts/pptx_theme_profile.py profile source.pptx --out theme_profile.json
```

必須同時看 source render，記錄：

- light / dark / mixed
- brand terrain / master chrome
- recurring rails
- typography character
- density profile
- image / chart language
- recurring signature motifs
- audience / slide roles

若品牌識別烘焙在 full-slide layout/master image，render 才是權威。

## 3. Source Spatial Discovery

逐頁辨識：

- slide role
- brand-safe / content-safe zones
- title / status / logo / footer reservations
- peer systems
- reading order
- vertical balance
- repeated rails / baselines / gutters

不要把 cover、agenda、section、dense-data、keynote、brand editorial 套成同一種骨架。

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

## 6. Design Agent — Soul → Frame → Skeleton → Joints → Limbs → Skin

依 `LAYOUT_INTELLIGENCE.md`：

```text
Soul
→ Frame
→ Skeleton
→ Joints
→ Limbs
→ Skin
```

不得從 Skin 開始。

### Required design behavior

- brand terrain 不被大面積 panel 壓住
- title/status/logo 不互搶 header band
- summary/table 共用合理 rails
- peer charts / images 共用可解釋的尺寸、top/bottom rail、gutter
- spacing 使用少數重複節奏
- dense body 不無理由 top-heavy
- decoration 必須服務 hierarchy / grouping / navigation / brand continuity
- source `20260819` 不得為了美觀改成 `2026/08/19`
- 不得把所有 deck 做成 rounded-card / dark-tech / gradient template

## 7. Spatial QA

```bash
python scripts/pptx_layout_intelligence.py source.pptx candidate.pptx --json
```

Hard requirement：

```text
SPATIAL_QA_PASS=true
```

Warnings 必須在 Composition QA 被逐頁處理。

## 8. Render Visual QA

Render source + final 全頁：

```bash
python scripts/visual_qa_gate.py visual_qa.json --expected-slides <N>
```

必須：

```text
VISUAL_QA_PASS=true
```

## 9. Render Composition QA

逐頁評估：

- brand chrome
- occlusion
- grid alignment
- peer alignment
- spacing rhythm
- reading order
- visual balance
- slide-role fit
- decorative restraint

```bash
python scripts/composition_qa_gate.py composition_qa.json --expected-slides <N>
```

必須：

```text
COMPOSITION_QA_PASS=true
```

## 10. Global Design Jury / 世界級評審

依 `GLOBAL_DESIGN_JURY.md` 產生 `global_design_jury.json`。

### Three mandatory lenses

```text
purpose_hierarchy_craft
executive_communication
domain_role_fit
```

### Core world-class dimensions

每頁至少評：

```text
purpose
hierarchy
simplicity
craft
composition
typography
spacing_rhythm
color_discipline
source_identity
signal_to_noise
glance_readability
executive_readiness
```

Default thresholds：

```text
every core dimension >= 90
source_identity >= 95
craft >= 92
slide_jury_score >= 93
deck_jury_score >= 93
identity_fidelity_score >= 95
archetype_fit_score >= 92
generic_template_risk <= 10
review_rounds >= 2
```

Role-specific dimensions 依 keynote / executive / technical / research / brand / comparison / section-closing 分別評估。

執行：

```bash
python scripts/global_design_jury_gate.py global_design_jury.json --expected-slides <N>
```

必須：

```text
DECK_IDENTITY_PASS=true
GLOBAL_DESIGN_JURY_PASS=true
```

### 3-second glance test

不要求 3 秒讀懂所有細節；要求 3 秒內能辨識：

1. 這頁的任務
2. 第一個 focal point
3. 主要資訊結構

## 11. Craft requires two review rounds

v0.6 final 至少兩輪：

```text
render → jury round 1 → repair/refine → render → jury round 2
```

第一輪若沒有修改，第二輪仍必須獨立重驗。

不允許「一次生成 → 自己打 95 分 → final」。

## 12. Regression v0.6

```bash
python scripts/pptx_regression.py source.pptx candidate.pptx \
  --visual-qa-report visual_qa.json --require-visual-qa \
  --composition-qa-report composition_qa.json --require-composition-qa \
  --global-jury-report global_design_jury.json --require-global-jury
```

Fully qualified v0.6 final **只接受**：

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
```

Legacy `DELIVERY_PASS=true` / `DELIVERY_V05_PASS=true` 不得作為 v0.6 世界級 final 證明。

## 13. Benchmark / Style Diversity

發佈前應參考：

```text
docs/GLOBAL_DESIGN_BENCHMARK_V06.md
```

至少壓測：

- keynote launch minimal
- executive strategy
- technical keynote / engineering review
- luxury / editorial brand
- research / academic evidence-led

加上真實 MEC / KORE regression anchors。

如果五種 deck 最後看起來只是同一套模板換顏色：FAIL。

## 14. Fail closed

遇到 verifier 無法判定、render 失敗、brand terrain 不清楚、font fallback 不可控、任何 v0.6 Gate 未通過：

- 保留 source 與最近 Content-Lock-safe candidate
- 回報 slide number + failed gate
- 不刪內容、不換圖、不 flatten、不假裝 final

## Minimal activation / 最短啟用語句

```text
Use pptx-beautify-lock v0.6 Global Design Jury on this PPTX.
內容 100% 凍結，不 rebrand、不套通用模板。
先分析 Source Theme + Brand Terrain + Deck Identity + Layout Skeleton，再美化。
執行 Linter → Auto Formatter → Spatial QA → Design Agent → Render Visual QA → Composition QA → Global Design Jury ×2 → Regression v0.6。
只有 DELIVERY_V06_PASS=true 才交付 final。
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
DECK_IDENTITY_PASS=true|false
GLOBAL_DESIGN_JURY_PASS=true|false
REGRESSION_V06_PASS=true|false
DELIVERY_V06_PASS=true|false
```
