# 安裝方式 / Installation

本 repo 同時提供：

1. **Plugin marketplace 安裝**（最省事）
2. **直接安裝 `pptx-beautify-lock/` Skill 目錄**
3. **只貼 GitHub URL，由 Agent 讀取 `SKILL.md`**

## Claude Code — Plugin marketplace

```bash
claude plugin marketplace add https://github.com/Space653000/pptx-beautify-lock-Skill
claude plugin install pptx-beautify-lock@space653000-pptx
```

Claude Code 內也可以使用對應 `/plugin` 指令加入 marketplace 與安裝 plugin。

安裝後，當任務是既有 PPTX「內容不變，只美化/修版」時，model 應依 Skill description 自動選用 `pptx-beautify-lock`。

## ChatGPT / Codex — Plugin marketplace

若目前 Codex/ChatGPT harness 支援 plugin marketplace：

```bash
codex plugin marketplace add Space653000/pptx-beautify-lock-Skill
codex
/plugins
```

選擇 `space653000-pptx` marketplace，安裝 `pptx-beautify-lock`。

## Editable Skill files / 直接安裝 Skill

真正的 Skill 目錄：

```text
pptx-beautify-lock/
```

Typical local patterns：

```text
~/.claude/skills/pptx-beautify-lock/
~/.codex/skills/pptx-beautify-lock/
```

若宿主版本的 Skills 路徑不同，以該版本支援的 Agent Skills 安裝機制為準。

也可以只維護一份 shared source，再對 Claude Code/Codex 建 symbolic link 或 Windows junction，避免規範分叉。

## 只貼 URL / URL-only bootstrap

把 PPTX 給 AI 並貼：

```text
https://github.com/Space653000/pptx-beautify-lock-Skill
```

然後說：

```text
Read this repository and use pptx-beautify-lock/SKILL.md on this PPTX.
啟用 Content Lock，只重新設計視覺層；只有 DELIVERY_PASS=true 才交付 final PPTX。
```

根目錄入口：

- Claude Code: `CLAUDE.md`
- Codex/coding agents: `AGENTS.md`
- generic URL-only agent: `AI_BOOTSTRAP.md`

## Python dependencies

驗證/Linter scripts 需要：

```bash
pip install -r requirements.txt
```

完整品質流程除了 Python scripts，還需要宿主本身具備 PPTX 編輯與 render 能力。若無 render 能力，依 `SKILL.md` 只能產生 structural candidate，不能宣稱完整 `DELIVERY_PASS=true`。