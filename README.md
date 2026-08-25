# pptx-beautify-lock-Skill v0.6

**繁體中文為主 / English compatible**

給 Claude Code、ChatGPT / Codex 與其他 Agent 使用的 **PowerPoint 內容 100% 凍結＋來源風格鎖定＋版面骨骼智慧＋世界級 Global Design Jury** Skill。

> **Content Lock**：文字、數字、表格資料、圖表資料、圖片內容、頁面順序與 protected semantics 不得擅自改。  
> **Theme / Identity Lock**：未授權不得 rebrand，也不得把不同 deck 洗成同一種 AI 模板。  
> **Layout Intelligence**：沒有 overlap 還不夠；grid、spacing、reading order、visual balance、peer alignment 都要成立。  
> **Global Design Jury**：不模仿 Apple/NVIDIA/顧問公司的皮，而是用 Purpose、Hierarchy、Simplicity、Craft、Executive Communication、Technical Focus 的世界級標準驗收。

## v0.6 核心理念

```text
Soul / 靈魂
→ Frame / 框架
→ Skeleton / 骨骼
→ Joints / 關節
→ Limbs / 肢體
→ Skin / 外觀
→ Global Design Jury / 世界級評審
```

先理解 source 的品牌、內容任務、audience、density 與空間 DNA，最後才碰顏色、卡片、陰影、漸層等表皮。

## 完整流程

```text
Content Snapshot
→ Source Theme + Deck Identity Discovery
→ Source Render / Brand Terrain / Slide-role Discovery
→ PPTX Linter
→ Auto Formatter
→ Layout Intelligence / Spatial QA
→ Design Agent
→ Content + Theme + Spatial Guards
→ Render Visual QA
→ Composition QA
→ Global Design Jury round 1
→ repair / refine
→ Global Design Jury round 2
→ Regression v0.6
```

## Global Design Jury

每份 final 同時通過三個 lens：

```text
Purpose / Hierarchy / Simplicity / Craft
Executive Communication
Domain / Slide-role Fit
```

每頁核心評分至少包含：

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

Default world-class floors：

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

## Authoritative entry points / 權威入口

```text
pptx-beautify-lock/SKILL.md
```

核心 references：

```text
pptx-beautify-lock/references/CONTENT_LOCK.md
pptx-beautify-lock/references/THEME_DISCOVERY.md
pptx-beautify-lock/references/TYPOGRAPHY_BILINGUAL.md
pptx-beautify-lock/references/LAYOUT_INTELLIGENCE.md
pptx-beautify-lock/references/GLOBAL_DESIGN_JURY.md
```

研究依據：[`docs/DESIGN_RESEARCH_V06_GLOBAL_JURY.md`](docs/DESIGN_RESEARCH_V06_GLOBAL_JURY.md)  
五種風格 benchmark：[`docs/GLOBAL_DESIGN_BENCHMARK_V06.md`](docs/GLOBAL_DESIGN_BENCHMARK_V06.md)

## v0.6 最終交付門檻

Fully qualified final PPTX 必須：

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

`DELIVERY_PASS=true` / `DELIVERY_V05_PASS=true` 都只是舊版相容欄位，不代表 v0.6 世界級 final。

## 最快使用：直接貼 GitHub URL

```text
https://github.com/Space653000/pptx-beautify-lock-Skill
```

再告訴 Agent：

```text
Use pptx-beautify-lock v0.6 Global Design Jury on this PPTX.
內容 100% 凍結，不 rebrand、不套通用模板。
先分析 Source Theme + Brand Terrain + Deck Identity + Layout Skeleton，再美化。
只有 DELIVERY_V06_PASS=true 才交付 final。
```

若宿主允許本機寫入與程式執行：

```bash
# Claude Code
python scripts/install_skill.py --target claude --force

# Codex
python scripts/install_skill.py --target codex --force

# Both
python scripts/install_skill.py --target both --force
```

成功：

```text
INSTALL_PASS=true
```

> 單純貼 URL 不能繞過宿主安全權限。若禁止下載、執行或寫入 Skills 目錄，Agent 必須直接從 repo 使用 Skill，並明確回報「未持久安裝」。

## Plugin 安裝

### Claude Code

```bash
claude plugin marketplace add https://github.com/Space653000/pptx-beautify-lock-Skill
claude plugin install pptx-beautify-lock@space653000-pptx
```

完整安裝與 URL bootstrap 說明：[`INSTALL.md`](INSTALL.md) / [`AI_BOOTSTRAP.md`](AI_BOOTSTRAP.md)
