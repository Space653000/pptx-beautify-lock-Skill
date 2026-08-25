# pptx-beautify-lock-Skill v0.5

**繁體中文為主 / English compatible**

給 Claude Code、ChatGPT / Codex 與其他 Agent 使用的 **PowerPoint 內容 100% 凍結＋來源風格鎖定＋版面骨骼智慧美化 Skill**。

> **Content Lock**：文字、數字、表格資料、圖表資料、圖片內容、頁面順序與 protected semantics 不得擅自改。  
> **Theme Lock**：未授權不得把 source light/dark/mixed 或品牌色系換皮。  
> **Bilingual Typography**：繁體中文＋英文都必須 glyph-safe、協調、可讀。  
> **Layout Intelligence**：沒有 overlap 還不夠；品牌地形、grid、spacing、reading order、visual balance、peer alignment 都要過關。

## v0.5 的核心改變

真實 MEC 壓測證明 v0.4 的一個重大盲點：**Content Lock PASS + Theme Guard PASS + no overlap，仍可能做出位置很怪的投影片。**

因此 v0.5 將美感拆成六層：

```text
Soul / 靈魂
→ Frame / 框架
→ Skeleton / 骨骼
→ Joints / 關節
→ Limbs / 肢體
→ Skin / 外觀
```

Design Agent 必須先理解 source brand terrain 與 layout skeleton，最後才碰 color/card/shadow 等表皮。

## 完整流程

```text
Content Snapshot
→ Source Theme Discovery / Visual DNA
→ Source Render + Slide-role / Brand-terrain discovery
→ PPTX Linter
→ Auto Formatter
→ Layout Intelligence / Spatial QA
→ Design Agent
→ Content + Theme + Spatial Guards
→ Render Visual QA
→ Render Composition QA
→ Regression v0.5
```

## v0.5 新增能力

- **Spatial QA**：偵測 foreground solid-fill 遮擋、peer chart/image rail drift、品牌背景新增大型 solid region 的風險、dense-data top-heavy risk。
- **Composition QA**：逐頁 source-vs-final render 評分 brand chrome、grid alignment、peer alignment、spacing rhythm、reading order、visual balance、slide-role fit、decorative restraint。
- **Evidence-based review**：不能只填「看起來很好」；每頁要留下 source comparison、grid rails、reading order、brand anchors 證據。
- **Dense technical layout rules**：POWER / THD / HOHD 等 summary + table + L/R chart 頁面，以 peer system 與 footer safe zone 重構。
- **Branded cover rules**：full-slide branded background 不再被當成空白地板；大面積 title panel 必須證明不會壓住 logo/department identity/hero art。
- **Backward-compatible regression**：保留 v0.4 `DELIVERY_PASS` 欄位，但 v0.5 final 只認 `DELIVERY_V05_PASS=true`。

## Authoritative entry points / 權威入口

```text
pptx-beautify-lock/SKILL.md
pptx-beautify-lock/references/CONTENT_LOCK.md
pptx-beautify-lock/references/THEME_DISCOVERY.md
pptx-beautify-lock/references/TYPOGRAPHY_BILINGUAL.md
pptx-beautify-lock/references/LAYOUT_INTELLIGENCE.md
pptx-beautify-lock/references/DESIGN_AGENT_RULES.md
pptx-beautify-lock/references/RENDER_VISUAL_QA.md
```

設計研究與來源：

```text
docs/DESIGN_RESEARCH_2026-08-25.md
```

## 最終交付門檻

Fully qualified v0.5 final PPTX 必須：

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

`DELIVERY_PASS=true` 只保留給 v0.4 相容性；**不得拿它當 v0.5 final 證明。**

若不能 render，只能產生 structural candidate。

## 最快使用：直接貼 GitHub URL

```text
https://github.com/Space653000/pptx-beautify-lock-Skill
```

再告訴 Agent：

```text
Read this repository and use pptx-beautify-lock/SKILL.md.
啟用 Content Lock + Theme Lock + Layout Intelligence。
先辨識 Source Theme、Brand Terrain、Slide Role 與 Layout Skeleton，再美化。
執行 Spatial QA + Render Visual QA + Composition QA。
只有 DELIVERY_V05_PASS=true 才交付 final PPTX。
```

## Self-install / 自動安裝

若宿主允許本機寫入與程式執行：

```bash
# Claude Code
python scripts/install_skill.py --target claude --force

# Codex
python scripts/install_skill.py --target codex --force

# Both
python scripts/install_skill.py --target both --force
```

成功條件：

```text
INSTALL_PASS=true
```

> GitHub URL 不能繞過 Claude Code / Codex 的宿主 sandbox。若禁止下載、執行或寫入 Skills 目錄，Agent 必須直接從 repo 使用 Skill，不能假裝已持久安裝。

## v0.5 QA commands

```bash
python scripts/pptx_content_lock.py verify source.pptx candidate.pptx
python scripts/pptx_theme_profile.py compare source.pptx candidate.pptx --json
python scripts/pptx_lint.py candidate.pptx --json
python scripts/pptx_layout_intelligence.py source.pptx candidate.pptx --json
python scripts/visual_qa_gate.py visual_qa.json --expected-slides <N>
python scripts/composition_qa_gate.py composition_qa.json --expected-slides <N>
python scripts/pptx_regression.py source.pptx candidate.pptx \
  --visual-qa-report visual_qa.json --require-visual-qa \
  --composition-qa-report composition_qa.json --require-composition-qa
```

## Design research basis

v0.5 的 grid/alignment/whitespace/hierarchy 原則參考並重新操作化自公開第一方/作者來源，包括 Apple HIG、Apple Keynote alignment guides、Presentation Zen 的 alignment/proximity/contrast/repetition，以及 Duarte 的 whitespace/hierarchy/unity/data-display 原則。具體來源與本 repo 原創 synthesis 的區分寫在 `docs/DESIGN_RESEARCH_2026-08-25.md`。
