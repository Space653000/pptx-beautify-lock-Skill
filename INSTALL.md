# 安裝方式 / Installation

本專案的可安裝 Skill 位於：

```text
pptx-beautify-lock/
```

## Claude Code

將 `pptx-beautify-lock/` 放入或連結到 Claude Code 支援的 Skills 目錄，或直接用 Claude Code 開啟本 repo；根目錄 `CLAUDE.md` 會引導它讀取 `pptx-beautify-lock/SKILL.md`。

Typical pattern:

```text
~/.claude/skills/pptx-beautify-lock/
```

如果 Claude Code 版本的 Skills 路徑不同，以該版本官方設定為準。

## ChatGPT / Codex

將 `pptx-beautify-lock/` 安裝到目前 Codex / ChatGPT Skills 所支援的位置，或讓 Codex 直接開啟本 repo；根目錄 `AGENTS.md` 會將任務導向同一份 Skill。

Typical local pattern:

```text
~/.codex/skills/pptx-beautify-lock/
```

## Shared source / 共用一份來源

建議只維護一份 Skill source，再由 Claude Code 與 Codex 各自建立 symbolic link / junction，避免兩份規則日後分歧。

Example on Windows conceptually:

```text
C:\AI\SharedSkills\pptx-beautify-lock
          ↑                     ↑
~\.claude\skills\...      ~\.codex\skills\...
```

## Python dependency

內容驗證器使用 Python 標準函式庫；版面幾何 QA 需要：

```bash
pip install -r requirements.txt
```

## Recommended usage / 建議使用方式

給 AI 一份 PPTX，再貼上本 GitHub repo URL，並下達：

```text
Read this repository and use pptx-beautify-lock.
啟用 CONTENT LOCK：內容 100% 凍結，只重新設計視覺層。
完成後一定要通過 content verification 與 layout QA。
```
