# AI Bootstrap / AI 啟動入口

> 給只拿到 GitHub repository URL 的 AI 使用。Traditional Chinese first; English included.

如果使用者提供此 repo URL 與一份既有 `.pptx`，並要求「內容不改、只美化」，請直接執行本 repo 的正式 Skill：

```text
pptx-beautify-lock/SKILL.md
```

## 啟動條件 / Activation

以下語意應啟動本 Skill：

- 美化這份 PPT，但不要改內容
- 修復醜掉或跑版的 PowerPoint
- 只改排版、字體、位置、表格與視覺
- content lock
- visual redesign only
- keep all text/data/images exactly the same
- fix overlap / overflow / layout without rewriting

## 強制執行順序 / Required order

```text
1. Read SKILL.md and all mandatory references
2. Backup source PPTX
3. Create content snapshot
4. PPTX Linter
5. Auto Formatter
6. Design Agent
7. Re-run Linter
8. Content verification
9. Regression Test
10. Render-based Visual QA when available
11. Deliver only if all hard gates pass
```

## Hard gates / 硬性門檻

```text
CONTENT_LOCK_PASS=true
LAYOUT_QA_PASS=true
REGRESSION_PASS=true
```

## Safety / 保守策略

若 AI 沒有能力：

- 讀取 PPTX
- 修改/輸出 PPTX
- 執行驗證腳本

就必須明確說明限制，不得假裝已安全完成。

If the agent cannot inspect/edit PPTX files or execute verification, it must state that limitation instead of claiming the deck was safely beautified.
