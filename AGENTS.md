# AGENTS.md

> 繁體中文優先 / Traditional Chinese first. English included for compatibility.

本 repository 的正式 Agent Skill：

```text
pptx-beautify-lock/SKILL.md
```

當任務是「既有 PowerPoint 不改內容，只修排版、重做視覺、變得更漂亮」時，必須先讀完整 Skill 與其 mandatory references。

When the task is to beautify, repair, restyle, or professionally redesign an existing PowerPoint without changing its content, read and obey the Skill before editing.

## 強制管線 / Mandatory pipeline

```text
PPTX Linter
→ Auto Formatter
→ Design Agent
→ Regression Test
```

## 絕對規則 / Absolute rule

**CONTENT LOCK is mandatory. / 內容 100% 凍結。**

不得改寫、摘要、翻譯、校字、增刪、合併、拆分或重排來源內容。只允許修改視覺層。

Never rewrite, summarize, translate, spell-correct, add, delete, merge, split, or reorder source content. Only the visual layer may change.

## 交付門檻 / Delivery gates

交付前至少必須得到：

```text
CONTENT_LOCK_PASS=true
LAYOUT_QA_PASS=true
REGRESSION_PASS=true
```

如果環境可 render PPTX，還必須做逐頁 Visual QA。

Do not claim success when these gates cannot be verified.
