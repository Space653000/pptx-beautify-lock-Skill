# CLAUDE.md

當任務是**既有 PPT/PPTX 不改內容，只美化、修排版、修重疊/overflow、統一格式或重新設計視覺**時，Claude Code 必須先讀並執行：

```text
pptx-beautify-lock/SKILL.md
```

For existing-PowerPoint visual-only redesign, that Skill is the authoritative workflow.

**Content Lock 的唯一定義：** `pptx-beautify-lock/references/CONTENT_LOCK.md`。

完整 final delivery 必須由 Skill 的 regression gate 證明：

```text
DELIVERY_PASS=true
```

不要在本檔維護另一份流程或凍結清單；行為更新只改 authoritative Skill/references。