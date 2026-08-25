# CLAUDE.md

> 繁體中文優先 / Traditional Chinese first.

當 Claude Code 開啟此 repository，任何「既有 PPTX 不改內容、只修排版與視覺」的任務，都必須把下列檔案視為正式規範：

```text
pptx-beautify-lock/SKILL.md
```

When this repository is opened in Claude Code, treat that Skill as the authoritative workflow for existing-PowerPoint beautification tasks.

## 強制管線 / Mandatory pipeline

```text
1. PPTX Linter
2. Auto Formatter
3. Design Agent
4. Regression Test
```

## Absolute rule / 絕對規則

**CONTENT LOCK is mandatory. / 內容 100% 凍結。**

不得改寫、摘要、翻譯、校正文法拼字、增刪、合併、拆分或重排來源內容。只能重新設計視覺層。

Never rewrite, summarize, translate, spell-correct, add, delete, merge, split, or reorder source content. Only redesign the visual layer.

## Before delivery / 交付前

1. 建立 source content snapshot。
2. 執行 `scripts/pptx_lint.py`。
3. 做 visual-only format/design repair。
4. 再跑 Linter。
5. 執行 `scripts/pptx_content_lock.py verify`。
6. 執行 `scripts/pptx_regression.py`。
7. 可 render 時逐頁做 Visual QA。

只有以下全部成立才可交付：

```text
CONTENT_LOCK_PASS=true
LAYOUT_QA_PASS=true
REGRESSION_PASS=true
```

若 aesthetics 與 content fidelity 衝突，永遠以 content fidelity 為最高優先。
