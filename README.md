# pptx-beautify-lock-Skill

**繁體中文為主 / English compatible**

給 Claude Code、ChatGPT / Codex 與其他 Agent 使用的 **PowerPoint 內容鎖定自動美化 Skill**。

> **Content Lock：protected semantics 100% 凍結，只重新設計視覺呈現。**

目標不是「把 PPT 重新寫一份」，而是把既有 `.pptx` 當成內容真實來源，執行：

```text
PPTX Linter
→ Auto Formatter
→ Design Agent
→ Render Visual QA
→ Regression Test
```

## v0.3 核心特色

- **硬性 Content Lock**：machine-readable semantic manifest/diff
- **PPTX Linter**：geometry、tiny text、table density、overlap、edge、font/title consistency heuristics
- **Auto Formatter / Design Agent contract**：AI 可大幅重做 layout/typography/table/chart styling
- **Rendered Visual QA**：要求 AI/人逐頁看實際 render，不用 geometry heuristic 假裝「好看」
- **Regression Test**：Content + Layout + Visual 三類證據整合
- **Plugin marketplace packaging**：可供 Claude Code / Codex 類 harness 安裝
- **Traditional Chinese first + English compatibility**
- **GitHub Actions contract tests**

## Single source of truth

正式 Agent 流程：

```text
pptx-beautify-lock/SKILL.md
```

Content Lock 唯一定義：

```text
pptx-beautify-lock/references/CONTENT_LOCK.md
```

不要從 README 推測細部規則；Agent 應讀 `SKILL.md` 與它在各階段指向的 references。

## 最終交付門檻

Fully qualified final PPTX 必須得到：

```text
CONTENT_LOCK_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
REGRESSION_PASS=true
DELIVERY_PASS=true
```

如果環境不能 render，最多只能產生 structural candidate；不可把它宣稱為完整 final。

## 最快使用方式：直接貼 GitHub URL

把原始 PPTX 給 AI，再貼：

```text
https://github.com/Space653000/pptx-beautify-lock-Skill
```

下指令：

```text
Read this repository and use pptx-beautify-lock/SKILL.md on this PPTX.
啟用 Content Lock，只重新設計視覺層。
自動執行 Linter → Auto Formatter → Design Agent → Render Visual QA → Regression Test。
只有 DELIVERY_PASS=true 才交付 final PPTX。
```

## Plugin 安裝

### Claude Code

```bash
claude plugin marketplace add https://github.com/Space653000/pptx-beautify-lock-Skill
claude plugin install pptx-beautify-lock@space653000-pptx
```

### ChatGPT / Codex

若目前 harness 支援 plugin marketplace：

```bash
codex plugin marketplace add Space653000/pptx-beautify-lock-Skill
codex
/plugins
```

選擇 `space653000-pptx` → `pptx-beautify-lock`。

也可直接安裝/連結 `pptx-beautify-lock/` 到 Agent Skills 目錄；詳見 [`INSTALL.md`](INSTALL.md)。

## Executable quality gates

### Content snapshot

```bash
python pptx-beautify-lock/scripts/pptx_content_lock.py snapshot source.pptx --out content_manifest.json
```

### Linter

```bash
python pptx-beautify-lock/scripts/pptx_lint.py source.pptx --json > lint.before.json
```

### Content verification

```bash
python pptx-beautify-lock/scripts/pptx_content_lock.py verify source.pptx output.pptx
```

### Render Visual QA report validation

```bash
python pptx-beautify-lock/scripts/visual_qa_gate.py visual_qa.json --expected-slides <N>
```

### Final regression

```bash
python pptx-beautify-lock/scripts/pptx_regression.py source.pptx output.pptx \
  --visual-qa-report visual_qa.json \
  --require-visual-qa
```

## Repo 結構

```text
.
├── README.md
├── INSTALL.md
├── AGENTS.md
├── CLAUDE.md
├── AI_BOOTSTRAP.md
├── requirements.txt
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .github/workflows/
│   └── test.yml
├── tests/
│   └── test_content_lock_contract.py
└── pptx-beautify-lock/
    ├── SKILL.md
    ├── references/
    │   ├── CONTENT_LOCK.md
    │   ├── LINTER_RULES.md
    │   ├── AUTO_FORMATTER_RULES.md
    │   ├── DESIGN_AGENT_RULES.md
    │   ├── DESIGN_RULES.md
    │   ├── RENDER_VISUAL_QA.md
    │   ├── REGRESSION_TEST_RULES.md
    │   └── QA_RULES.md
    └── scripts/
        ├── pptx_content_lock.py
        ├── pptx_lint.py
        ├── visual_qa_gate.py
        ├── pptx_regression.py
        └── verify_layout.py
```

## Content Lock 現在會保護什麼？

權威清單請看 `CONTENT_LOCK.md`。v0.3 verifier 已涵蓋的不只文字/數字/表格/圖片，也包含 hyperlink/action、table merge topology、accessibility text、hidden-slide state、transition/timing semantics、comments/annotations、master/layout/SmartArt text、Office Math、media/embedded payload 等容易被重建工具默默破壞的內容。

## 為什麼一定要 Render Visual QA？

OOXML/geometry 可以知道物件座標，卻無法可靠證明：

- 字真的沒有 overflow/clipping
- overlap 是刻意設計還是撞版
- 表格實際投影是否可讀
- hierarchy / spacing / balance 是否真的漂亮

所以「非常漂亮」必須經過 render → 每頁 review → repair，而不是只靠 Linter warning count。

## Automated tests

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

GitHub Actions 至少驗證：

- visual-only geometry/typography change → Content Lock PASS
- text/table value change → FAIL
- table merge semantics change → FAIL
- hyperlink target change → FAIL
- hidden-slide state change → FAIL
- table tiny text 可被 Linter 找到
- Visual QA report 必須逐頁且所有 checks 完整

## Design principle

有效輸出必須同時滿足：

1. **protected content/behavior unchanged**
2. **visual design materially improved**
3. **PowerPoint native editability preserved whenever practical**
4. **quality gates provide evidence, not promises**

Prompt-only promises are not proof.