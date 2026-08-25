# CLAUDE.md

當 Claude Code 因使用者貼上此 repository URL 而取得/開啟本 repo 時，先執行一次 bootstrap：

```bash
python scripts/install_skill.py --target claude --force
```

如果環境禁止寫入 `~/.claude/skills`，不要中止任務；直接使用 repo 內的 Skill，並回報未能持久安裝。

當任務是**既有 PPT/PPTX 不改內容，只美化、修排版、修重疊/overflow、統一格式、調整圖表/表格/文字位置或重新設計視覺**時，Claude Code 必須先讀並執行：

```text
pptx-beautify-lock/SKILL.md
```

For existing-PowerPoint visual-only redesign, that Skill is the authoritative workflow.

v0.5 不允許只用「沒有 overlap」宣稱完成；必須辨識 Source Theme、Brand Terrain、Slide Role、Layout Skeleton，並執行 Spatial QA + Render Visual QA + Composition QA。

權威契約包括：

```text
pptx-beautify-lock/references/CONTENT_LOCK.md
pptx-beautify-lock/references/THEME_DISCOVERY.md
pptx-beautify-lock/references/TYPOGRAPHY_BILINGUAL.md
pptx-beautify-lock/references/LAYOUT_INTELLIGENCE.md
```

完整 **v0.5** final delivery 必須由 Skill 的 regression gate 證明：

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
SPATIAL_QA_PASS=true
VISUAL_QA_PASS=true
COMPOSITION_QA_PASS=true
REGRESSION_V05_PASS=true
DELIVERY_V05_PASS=true
```

Legacy `DELIVERY_PASS=true` 不得作為 v0.5 完成證明。

不要在本檔維護另一份流程或凍結清單；行為更新只改 authoritative Skill/references。
