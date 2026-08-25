# AI Bootstrap / AI 啟動入口

如果使用者只貼這個 repository URL，再提供一份既有 `.pptx` 並要求**內容不改、只美化/修版/重新設計視覺**，把這個 repo 視為可自啟動的 Agent Skill package。

## 1. URL → 自動安裝 / Self-install

若宿主允許本機檔案與程式執行，先在 repository root 執行：

```bash
python scripts/install_skill.py --target auto --force
```

目標：

- Claude Code → `~/.claude/skills/pptx-beautify-lock/`
- ChatGPT Codex / Codex → `~/.codex/skills/pptx-beautify-lock/`

成功條件：

```text
INSTALL_PASS=true
```

若宿主支援 GitHub plugin marketplace，也可使用 repo 內 `.claude-plugin/` manifest；`scripts/install_skill.py` 是跨 Claude Code / Codex 的共同 bootstrap fallback。

> 若執行環境禁止寫入 user home、禁止執行程式、或沒有 local checkout，不能假裝已安裝；直接從目前 repo 讀取 `pptx-beautify-lock/SKILL.md` 執行，並回報安裝限制。

## 2. 自動啟用 Skill

安裝後或直接使用 repo 時，讀並執行：

```text
pptx-beautify-lock/SKILL.md
```

Trigger examples：

- 美化 PPT，不要改內容
- repair ugly/broken PowerPoint layout
- visual redesign only
- fix overlap / overflow without rewriting
- content lock
- 對齊圖表、表格、文字與品牌區域
- preserve source visual DNA / brand terrain

v0.5 必須先做 Source Theme + Brand Terrain + Layout Skeleton discovery，再進行 Design Agent。不能只修 overlap 或套一個漂亮模板。

權威契約：

```text
pptx-beautify-lock/references/CONTENT_LOCK.md
pptx-beautify-lock/references/THEME_DISCOVERY.md
pptx-beautify-lock/references/TYPOGRAPHY_BILINGUAL.md
pptx-beautify-lock/references/LAYOUT_INTELLIGENCE.md
```

若宿主沒有 PPTX 讀寫、程式執行或 render 能力，依 `SKILL.md` 回報能力限制；不要把未驗證 candidate 宣稱為 final。

A fully qualified **v0.5** final deck requires the Skill to report:

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
SPATIAL_QA_PASS=true
VISUAL_QA_PASS=true
COMPOSITION_QA_PASS=true
REGRESSION_V05_PASS=true
DELIVERY_V05_PASS=true
```

`DELIVERY_PASS=true` 只保留給 v0.4 backward compatibility，不得當成 v0.5 final 證明。
