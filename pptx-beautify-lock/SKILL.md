---
name: pptx-beautify-lock
description: "Strictly beautify, repair, restyle, or auto-format an existing PPT/PPTX while preserving protected content, source visual DNA, brand terrain, spatial composition, and deck identity. 既有 PowerPoint 需要頂級美化、修重疊/overflow、統一繁中英文雙語字體、重新設計視覺與版面骨骼，但文字/數據/圖片等內容不可變。Runs Content Lock → Theme/Identity Discovery → Linter → Auto Formatter → Layout Intelligence → Design Agent → full render → Visual/Composition QA → Global Design Jury → full-deck regression."
license: MIT
metadata:
  version: "0.6.1"
  languages: "zh-TW,en"
  compatibility: "Claude Code, Codex, ChatGPT Skills, Agent-Skills-compatible coding agents"
---

# PPTX Beautify Lock v0.6.1 — Strict Production Release

**繁體中文為主要說明語言；English is retained for cross-agent compatibility.**

## Mission / 任務

把既有 PPTX 美化到可進入全球頂級科技客戶的 executive / engineering review，同時把來源內容視為不可變契約。

不是把所有投影片洗成同一套模板；先理解來源的靈魂、品牌、角色、資訊密度與視覺 DNA，再把「原本那份簡報」升級成熟。

> **不是學 Apple 的皮，而是學 Purpose、Hierarchy、Simplicity、Craft 的苛刻程度；不是學顧問公司的模板，而是學 executive communication 的結構；不是學 technical keynote 的配色，而是學資訊密度與視覺焦點的控制。**

## Mandatory references / 必讀規範

開始修改前必須讀：

- `references/CONTENT_LOCK.md`
- `references/THEME_DISCOVERY.md`
- `references/TYPOGRAPHY_BILINGUAL.md`
- `references/LAYOUT_INTELLIGENCE.md`
- `references/DESIGN_AGENT_RULES.md`
- `references/RENDER_VISUAL_QA.md`
- `references/GLOBAL_DESIGN_JURY.md`
- `references/REGRESSION_GUARDRAILS.md`

## Core contracts / 核心契約

1. **Content Lock** — protected semantics immutable。
2. **Theme Lock** — 未授權不得 rebrand / light↔dark flip。
3. **Bilingual Typography** — 繁中＋英文 glyph-safe、PowerPoint-safe、協調、可讀。
4. **Layout Intelligence** — brand terrain、grid rails、spacing rhythm、reading order、visual balance、peer alignment 都是正式品質條件。
5. **Deck Identity Guard** — final 必須仍明確屬於 source deck，不得模板化收斂。
6. **Global Design Jury** — Purpose/Hierarchy/Simplicity/Craft、Executive Communication、Domain/Role Fit 三個 lens 全部通過。
7. **No-regression transaction** — 修 A 不能壞 B；任何 repair 後都要重跑全簡報。

## Hard content lock / 內容 100% 凍結

禁止：

- rewrite / summarize / translate / spell-correct / expand / shorten
- change text, punctuation, numbers, units, formulas
- change table values or semantic structure
- change chart source values/categories/series semantics
- replace images/media or alter protected image crop semantics
- add/delete/reorder/merge/split slides or protected content
- silently normalize `20260819` → `2026/08/19`

允許：

- x/y, width/height
- font family/size/weight/color when content remains identical
- margins, alignment, spacing, fill, border, background
- table row/column sizing and visual styling
- chart styling that does not change chart data
- decorative native shapes with no protected semantic content

如果內容塞不下：**先重排版，不准刪內容。**

## Full pipeline / 完整品質管線

```text
SOURCE PPTX
  → immutable backup
  → Content Snapshot
  → Source Theme + Deck Identity + Brand Terrain discovery
  → Source full render
  → slide-role / family / peer-system discovery
  → PPTX Linter
  → Auto Formatter
  → Layout Intelligence / Spatial QA
  → Design Agent — Soul → Frame → Skeleton → Joints → Limbs → Skin
  → Content + Theme + Spatial Guards
  → full render
  → Visual QA
  → Composition QA
  → Global Design Jury round 1
  → repair/refine
  → full render of ALL slides
  → Global Design Jury round 2
  → production regression pass 3
  → final full render of ALL slides
  → Regression v0.6.1
  → FINAL PPTX
```

## 0. Preflight

1. 不覆寫 source。
2. 建立工作副本與 source content snapshot。
3. 若 source 有 animation/transition/hyperlink/OLE/SmartArt/comments/accessibility metadata，優先原檔就地修改視覺屬性。
4. 無 renderer 時只能 structural candidate，不能宣稱 production final。
5. 不得先挑「漂亮模板」；先理解 source soul / audience / role。
6. 對 Windows/Office 交付，字型必須通過 portability review；不能只在生成環境正常。

## 1. Content Snapshot

```bash
python scripts/pptx_content_lock.py snapshot source.pptx --out content_manifest.json
```

任何中途 repair 後都可以立即：

```bash
python scripts/pptx_content_lock.py verify source.pptx candidate.pptx
```

若 `CONTENT_LOCK_PASS=false`：立即停止該 candidate。

## 2. Theme / Identity / Brand Terrain Discovery

```bash
python scripts/pptx_theme_profile.py profile source.pptx --out theme_profile.json
```

同時看 source render，記錄：

- light / dark / mixed
- brand terrain / master chrome
- recurring rails / baselines / gutters
- typography character
- density profile
- image/chart/table language
- signature motifs
- cover / agenda / section / data / comparison / closing roles
- sibling families，例如 POWER / THD / HOHD、6σ / 5σ / 4σ、L/R

若 XML 與實際 render 衝突，以 render 為準。

## 3. Linter

```bash
python scripts/pptx_lint.py source.pptx --json > lint.before.json
```

至少檢查：geometry、out-of-bounds、placeholder artifacts、tiny text、table density、CJK fallback、suspicious overlap。

## 4. Auto Formatter

先做低風險機械修復：

- alignment / spacing
- text margins
- table row/column sizing
- chart/image peer geometry
- consistent status/title/footer rails

每輪都執行 Content Verify + Theme Compare + Linter。

## 5. Design Agent — Skeleton before Skin

```text
Soul
→ Frame
→ Skeleton
→ Joints
→ Limbs
→ Skin
```

### Required behavior

- brand terrain 不被大面積 panel 蓋住
- title/status/logo 不互搶 header band
- summary/table 共用可解釋的 rails
- peer charts/images 共用尺寸、top/bottom rail、gutter，除非資料本質要求例外
- spacing 只使用少數有節奏的 tiers
- dense body 不無理由 top-heavy
- decoration 必須服務 hierarchy/grouping/navigation/brand continuity
- 不得 rounded-card / dark-tech / gradient template convergence
- cover、agenda、data、closing 不能共用錯誤骨架

## 6. Sibling family parity / 同族頁一致性

若 POWER 已套用成熟 table system，THD / HOHD 不得保留舊式裸表格。

同族頁預設共享：

- title rail
- status rail
- summary card system
- table header/frequency/data-row hierarchy
- table font, fill, border, padding language
- chart title and L/R peer relationship
- footer/brand reservation
- spacing rhythm

資料欄數不同只允許 geometry adaptation，不允許 visual language regression。

## 7. Empty placeholder / master artifact rule

Final render 不得出現或被空 placeholder 影響：

- `presentation title`
- `Event name or presentation title`
- `Speaker name or subtitle`
- `Click to add...`
- empty title/body placeholder covering actual content
- master `AGENDA` / `THANK YOU` 或類似 artifact 與有效內容競爭

空 placeholder 沒有 protected content 時可移除；有效 source content 必須保留。

## 8. Font portability / 雙語字型

- Traditional Chinese + English 必須 glyph-safe。
- 不能只看 XML font name；必須檢實際 Office-compatible render。
- 若看到 serif fallback、巨大字體、裁切、行高異常、換行漂移：FAIL。
- Windows/Office conservative fallback 優先使用 Aptos / Microsoft JhengHei 或已證明目標環境可用的 Noto Sans CJK TC。
- 不為了美感使用客戶環境可能沒有的脆弱字型。

## 9. Spatial QA

```bash
python scripts/pptx_layout_intelligence.py source.pptx candidate.pptx --json
```

Hard requirement：

```text
SPATIAL_QA_PASS=true
```

Warnings 必須在 Composition QA 被逐頁解決或合理說明。

## 10. Full render + Visual QA

Render source + final **所有頁面**。

```bash
python scripts/visual_qa_gate.py visual_qa.json --expected-slides <N>
```

必須：

```text
VISUAL_QA_PASS=true
```

如果 automated PNG 與使用者實際 PowerPoint 預覽不一致，以實際 Office/PowerPoint 現象為優先 defect evidence。

## 11. Composition QA

逐頁評估：

- brand chrome respected
- no content occlusion
- grid alignment coherent
- peer components aligned
- spacing rhythm coherent
- reading order clear
- visual balance coherent
- slide-role composition fit
- decorative elements earn their place
- template placeholder artifacts absent
- theme fidelity preserved
- bilingual typography clean

```bash
python scripts/composition_qa_gate.py composition_qa.json --expected-slides <N>
```

必須 `COMPOSITION_QA_PASS=true`。

## 12. Global Design Jury

依 `GLOBAL_DESIGN_JURY.md`，每頁至少評：

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
```

Round 1 與 Round 2 都必須覆蓋全部 slides，不能抽樣。

```bash
python scripts/global_design_jury_gate.py global_design_jury.json --expected-slides <N>
```

必須：

```text
DECK_IDENTITY_PASS=true
GLOBAL_DESIGN_JURY_PASS=true
```

## 13. Production three-pass full-deck review

v0.6.1 production workflow 至少：

```text
Pass 1 = Soul / identity / theme / role
Pass 2 = Skeleton + Muscle / layout / tables / charts / density
Pass 3 = Skin + final regression / typography / craft / Office render
```

每一輪都看 **全簡報所有頁**。

**Fix A without breaking B**：每次 repair 後都要 rerender 全頁並確認所有先前 PASS 的頁面沒有 regression。

## 14. Regression

```bash
python scripts/pptx_regression.py source.pptx candidate.pptx \
  --visual-qa-report visual_qa.json --require-visual-qa \
  --composition-qa-report composition_qa.json --require-composition-qa \
  --global-jury-report global_design_jury.json --require-global-jury
```

Fully qualified production final 只接受：

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

另外 production review 必須人工/agent evidence 證明：

```text
EMPTY_PLACEHOLDER_PASS=true
FONT_PORTABILITY_PASS=true
SIBLING_STYLE_PARITY_PASS=true
FULL_DECK_REGRESSION_PASS=true
THREE_PASS_REVIEW_PASS=true
```

這五項任一無法證明：FAIL CLOSED。

## 15. Fail closed

遇到 verifier 無法判定、render 失敗、brand terrain 不清楚、font fallback 不可控、任何 Gate 未通過：

- 保留 source 與最近 Content-Lock-safe candidate
- 回報 slide number + failed gate
- 不刪內容、不換圖、不 flatten、不假裝 final

## Minimal activation / 最短啟用語句

```text
Use pptx-beautify-lock v0.6.1 strict production workflow on this PPTX.
內容 100% 凍結，不 rebrand、不套通用模板。
先分析 Source Theme + Brand Terrain + Deck Identity + Layout Skeleton。
執行全頁三輪：Soul → Skeleton/Muscle → Skin/Regression。
任何 repair 後都 rerender 全份，禁止修 A 壞 B。
只有 DELIVERY_V06_PASS=true 且 v0.6.1 五項 production guardrails 全 PASS 才交付 final。
```
