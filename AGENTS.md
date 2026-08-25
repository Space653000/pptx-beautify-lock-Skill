# AGENTS.md

當 ChatGPT Codex / Codex 因使用者貼上此 repository URL 而取得/開啟本 repo 時，先執行一次 bootstrap：

```bash
python scripts/install_skill.py --target codex --force
```

如果環境禁止寫入 `~/.codex/skills`，不要中止任務；直接使用 repo 內的 Skill，並回報未能持久安裝。

當任務是**既有 PPT/PPTX 不改內容，只美化、修排版、修重疊/overflow、統一格式、調整圖表/表格/文字位置或重新設計視覺**時，先讀並執行：

```text
pptx-beautify-lock/SKILL.md
```

v0.6 不允許只用「沒有 overlap」或「看起來漂亮」宣稱完成。必須：

```text
Source Theme + Brand Terrain + Deck Identity discovery
→ Layout Intelligence / Spatial QA
→ Render Visual QA
→ Composition QA
→ Global Design Jury × 2 review rounds
→ Regression v0.6
```

權威契約：

```text
pptx-beautify-lock/references/CONTENT_LOCK.md
pptx-beautify-lock/references/THEME_DISCOVERY.md
pptx-beautify-lock/references/TYPOGRAPHY_BILINGUAL.md
pptx-beautify-lock/references/LAYOUT_INTELLIGENCE.md
pptx-beautify-lock/references/GLOBAL_DESIGN_JURY.md
```

Fully qualified **v0.6** delivery requires:

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
SPATIAL_QA_PASS=true
VISUAL_QA_PASS=true
COMPOSITION_QA_PASS=true
DECK_IDENTITY_PASS=true
GLOBAL_DESIGN_JURY_PASS=true
REGRESSION_V06_PASS=true
DELIVERY_V06_PASS=true
```

Legacy `DELIVERY_PASS=true` / `DELIVERY_V05_PASS=true` 不得作為 v0.6 final 證明。
