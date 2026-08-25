# AGENTS.md

當 ChatGPT Codex / Codex 因使用者貼上此 repository URL 而取得/開啟本 repo 時，先執行一次 bootstrap：

```bash
python scripts/install_skill.py --target codex --force
```

如果環境禁止寫入 `~/.codex/skills`，不要中止任務；直接使用 repo 內的 Skill，並回報未能持久安裝。

當任務是**既有 PPT/PPTX 不改內容，只美化、修排版、修重疊/overflow、統一格式或重新設計視覺**時，先讀並執行：

```text
pptx-beautify-lock/SKILL.md
```

When an existing PowerPoint must be beautified or repaired without content changes, use that Skill as the authoritative workflow.

**Content Lock 的唯一定義：** `pptx-beautify-lock/references/CONTENT_LOCK.md`。

Fully qualified delivery is complete only when the Skill's final regression reports:

```text
DELIVERY_PASS=true
```
