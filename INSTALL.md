# 安裝方式 / Installation

本 repo 同時提供：

1. **Plugin marketplace 安裝**
2. **直接安裝 `pptx-beautify-lock/` Skill 目錄**
3. **只貼 GitHub URL，由 Agent bootstrap**

## Claude Code — Plugin marketplace

```bash
claude plugin marketplace add https://github.com/Space653000/pptx-beautify-lock-Skill
claude plugin install pptx-beautify-lock@space653000-pptx
```

## URL-only bootstrap / Claude Code + Codex 共用

Repository checkout 後：

```bash
# Claude Code
python scripts/install_skill.py --target claude --force

# Codex
python scripts/install_skill.py --target codex --force

# Both
python scripts/install_skill.py --target both --force
```

成功：

```text
INSTALL_PASS=true
```

Typical local targets：

```text
~/.claude/skills/pptx-beautify-lock/
~/.codex/skills/pptx-beautify-lock/
```

若宿主版本的 Skills 路徑不同，以該版本支援的 Agent Skills 安裝機制為準。

## 只貼 URL / URL-only use

把 PPTX 給 AI 並貼：

```text
https://github.com/Space653000/pptx-beautify-lock-Skill
```

然後說：

```text
Use pptx-beautify-lock v0.6 Global Design Jury on this PPTX.
內容 100% 凍結，不 rebrand、不套通用模板。
先分析 Source Theme + Brand Terrain + Deck Identity + Layout Skeleton，再美化。
只有 DELIVERY_V06_PASS=true 才交付 final PPTX。
```

根目錄入口：

- Claude Code: `CLAUDE.md`
- Codex/coding agents: `AGENTS.md`
- generic URL-only agent: `AI_BOOTSTRAP.md`

## Python dependencies

```bash
pip install -r requirements.txt
```

完整品質流程還需要宿主具備 PPTX 編輯與 render 能力。無 renderer 只能產生 structural candidate，不能宣稱 v0.6 final。

## v0.6 required finish line

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
SPATIAL_QA_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
COMPOSITION_QA_PASS=true
DECK_IDENTITY_PASS=true
GLOBAL_DESIGN_JURY_PASS=true
REGRESSION_V06_PASS=true
DELIVERY_V06_PASS=true
```

`DELIVERY_PASS=true` / `DELIVERY_V05_PASS=true` 是舊版相容欄位，不是 v0.6 完成條件。
