# pptx-beautify-lock-Skill

**繁體中文為主 / English compatible**

這是一個給 Claude Code、ChatGPT / Codex 與其他 AI Agent 使用的 **PowerPoint 自動美化 Skill**。

核心要求只有一句：

> **內容 100% 凍結，AI 只准重新設計視覺層。**

A cross-agent PowerPoint beautification skill with a hard content lock:

> **Preserve presentation content exactly. Redesign only the visual layer.**

---

## 四大模組 / Four-stage architecture

```text
SOURCE PPTX
   ↓
1. PPTX LINTER
   找出跑版、重疊、字太小、邊界、字型與一致性問題
   ↓
2. AUTO FORMATTER
   自動修復幾何、對齊、間距、字級、表格、圖表配置
   ↓
3. DESIGN AGENT
   在 Content Lock 下重新設計整體視覺系統
   ↓
4. REGRESSION TEST
   驗證內容零變更、版面無退化、PPTX 可交付
   ↓
FINAL PPTX
```

The four stages are:

1. **PPTX Linter** — detect layout defects and consistency risks.
2. **Auto Formatter** — conservatively repair geometry and formatting.
3. **Design Agent** — aggressively improve the visual layer only.
4. **Regression Test** — prove content integrity and layout quality before delivery.

---

## 內容凍結 / Content Lock

來源 `.pptx` 是唯一內容真實來源。

**絕對不能改：**

- 投影片頁數與順序
- 所有文字、標點、數字、單位、公式、符號、語言
- 表格結構、列欄順序、合併關係、所有 cell values
- 圖表 categories、series、source values、formulas、cached data、embedded workbook
- 圖片/影音 payload
- 圖片 crop state
- Speaker Notes
- embedded files

AI 不得為了排版方便而：

- 改寫
- 摘要
- 翻譯
- 校正文法、拼字或標點
- 新增或刪除內容
- 合併或拆分投影片
- 改變頁面順序
- 用生成圖片或相似圖片替代原圖
- 將整頁可編輯內容 flatten 成一張圖片

---

## 可以改的視覺層 / Visual layer may change

- 字型、字級、粗細、顏色
- 文字框位置、尺寸、內距
- 行距、段距、alignment
- 物件位置與大小
- whitespace、grid、alignment、distribution
- 表格欄寬、列高、cell padding、fill、border
- chart styling、legend、axis、plot area，但不得改 chart data
- 背景、shadow、border、accent、visual hierarchy
- 圖片顯示位置與大小，但不得換圖或改 crop
- overlap、overflow、clipping、out-of-bounds 修復

如果內容塞不下，**只能重排版，不准改字。**

---

## Repo 結構 / Repository layout

```text
.
├── README.md
├── INSTALL.md
├── AGENTS.md
├── CLAUDE.md
├── AI_BOOTSTRAP.md
├── requirements.txt
├── tests/
│   └── test_content_lock_contract.py
├── .github/workflows/
│   └── test.yml
└── pptx-beautify-lock/
    ├── SKILL.md
    ├── references/
    │   ├── CONTENT_LOCK.md
    │   ├── LINTER_RULES.md
    │   ├── AUTO_FORMATTER_RULES.md
    │   ├── DESIGN_AGENT_RULES.md
    │   ├── REGRESSION_TEST_RULES.md
    │   ├── DESIGN_RULES.md
    │   └── QA_RULES.md
    └── scripts/
        ├── pptx_content_lock.py
        ├── pptx_lint.py
        ├── verify_layout.py
        └── pptx_regression.py
```

---

## 未來最簡單的用法 / Fastest use

把 PPTX 給 AI，再貼這個 repository URL，然後只要說：

```text
Read this repository and use pptx-beautify-lock/SKILL.md.

請對這份 PPTX 執行：
PPTX Linter → Auto Formatter → Design Agent → Regression Test。

啟用 CONTENT LOCK：內容 100% 凍結，只允許重新設計視覺層。
不得修改文字、數字、表格資料、圖表資料、圖片內容、crop、備註、頁數或頁面順序。

自動修復字型、字級、位置、留白、對齊、表格尺寸、色彩、背景、視覺階層、overlap、overflow，並將整體設計提升到專業可上台品質。

不要逐頁問我；自行完成。
只有 CONTENT_LOCK_PASS=true、LAYOUT_QA_PASS=true、REGRESSION_PASS=true 才能交付。
```

---

## 可執行工具 / Executable quality gates

### 1. 建立內容快照

```bash
python pptx-beautify-lock/scripts/pptx_content_lock.py snapshot input.pptx --out content_manifest.json
```

### 2. PPTX Linter

```bash
python pptx-beautify-lock/scripts/pptx_lint.py input.pptx --json
```

### 3. 美化後驗證內容

```bash
python pptx-beautify-lock/scripts/pptx_content_lock.py verify input.pptx output.beautified.pptx
```

必須得到：

```text
CONTENT_LOCK_PASS=true
```

### 4. Regression Test

```bash
python pptx-beautify-lock/scripts/pptx_regression.py input.pptx output.beautified.pptx
```

必須得到：

```text
REGRESSION_PASS=true
CONTENT_LOCK_PASS=true
LAYOUT_QA_PASS=true
```

---

## 為什麼不是只寫一段 Prompt？

因為「AI 說它沒有改內容」不等於真的沒有改內容。

這個 repo 使用 machine-verifiable gates：

- semantic content manifest
- media / embedded payload hashing
- chart semantics comparison
- image crop-state comparison
- PPTX layout linting
- source-vs-output regression comparison
- automated contract tests

Prompt-only promises are not proof. The repository includes executable verification.

---

## 自動測試 / Automated tests

GitHub Actions 會執行 Content Lock contract tests，其中至少驗證：

- **只改字級/位置 → PASS**
- **改一個文字 → FAIL**
- **改一個表格數值 → FAIL**
- Linter 可解析有效 PPTX

本機可執行：

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

---

## Claude Code / Codex

真正可安裝的 Skill 目錄：

```text
pptx-beautify-lock/
```

若直接開啟整個 repo：

- Claude Code 會看到 `CLAUDE.md`
- Codex / coding agents 可讀 `AGENTS.md`
- 只拿到 URL 的其他 AI 可先讀 `AI_BOOTSTRAP.md`

詳細安裝方式請見 `INSTALL.md`。

---

## 設計目標 / Design target

不是「不重疊」就算成功，而是同時做到：

- executive-ready
- clean, modern, restrained
- strong visual hierarchy
- consistent typography and spacing
- readable tables and charts
- no unintended overlap / overflow / clipping
- consistent cross-slide design language
- native PowerPoint editability whenever possible
- **source content remains unchanged**

---

## Fail closed / 保守失敗策略

如果 AI 或工具無法證明內容一致，必須判定失敗，而不是猜測。

如果環境無法讀取、修改 PPTX 或執行驗證，也必須明確說明限制，不能假裝已安全完成。

The workflow must fail closed whenever content integrity cannot be verified.
