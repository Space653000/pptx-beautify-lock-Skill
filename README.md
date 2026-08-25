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

- **硬性 Content Lock**：machine-readable protected-semantics manifest/diff
- **PPTX Linter**：geometry、tiny text、table density、overlap、edge、font/title consistency heuristics
- **Auto Formatter / Design Agent contract**：AI 可大幅重做 layout/typography/table/chart styling
- **Rendered Visual QA**：要求逐頁檢查實際 render，不以 geometry heuristic 假裝「好看」
- **Regression Test**：Content + Layout + Visual 三類證據整合
- **Plugin marketplace packaging**：可供 Claude Code / Codex 類 harness 安裝
- **Traditional Chinese first + English compatibility**
- **GitHub Actions public-CLI contract tests**

## Authoritative entry points / 權威入口

正式 Agent 流程：

```text
pptx-beautify-lock/SKILL.md
```

Content Lock 唯一定義：

```text
pptx-beautify-lock/references/CONTENT_LOCK.md
```

Render 視覺驗證：

```text
pptx-beautify-lock/references/RENDER_VISUAL_QA.md
```

安裝方式：[`INSTALL.md`](INSTALL.md)  
本次嚴謹審查紀錄：[`docs/QUALITY_AUDIT_2026-08-25.md`](docs/QUALITY_AUDIT_2026-08-25.md)

README 只做導覽；Agent 應讀 `SKILL.md` 與它在每個 phase 指向的 references，避免重複規則長期 drift。

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

也可直接安裝/連結 `pptx-beautify-lock/` 到 Agent Skills 目錄；詳見 `INSTALL.md`。

## Executable quality gates

```bash
# 1. Source content snapshot
python pptx-beautify-lock/scripts/pptx_content_lock.py snapshot source.pptx --out content_manifest.json

# 2. Structural/heuristic lint
python pptx-beautify-lock/scripts/pptx_lint.py source.pptx --json > lint.before.json

# 3. Protected-semantic verification
python pptx-beautify-lock/scripts/pptx_content_lock.py verify source.pptx output.pptx

# 4. Render-review report validation
python pptx-beautify-lock/scripts/visual_qa_gate.py visual_qa.json --expected-slides <N>

# 5. Final release gate
python pptx-beautify-lock/scripts/pptx_regression.py source.pptx output.pptx \
  --visual-qa-report visual_qa.json \
  --require-visual-qa
```

## Content Lock 保護範圍

完整權威清單請看 `CONTENT_LOCK.md`。v0.3 verifier 已涵蓋文字/數值/表格/圖表/圖片之外，也保護容易被重建工具默默破壞的語意，包括：

- hyperlink/action association
- table merge topology
- accessibility text
- hidden-slide state
- transition/timing semantics
- comments/annotations
- master/layout/SmartArt text
- Office Math
- media/embedded/OLE payloads
- opaque custom XML / ActiveX / macro-like protected payloads

Verifier 以 content-bearing object 保留語意關聯，同時正規化 text-run segmentation，使純粹的字型/粗體/文字 run 重切不會被誤判成內容變更。

## 為什麼一定要 Render Visual QA？

OOXML/geometry 可以知道物件座標，卻無法可靠證明：

- 字真的沒有 overflow/clipping
- overlap 是刻意設計還是撞版
- 表格/圖表實際投影是否可讀
- hierarchy / spacing / balance 是否真的漂亮

因此「非常漂亮」必須經過：

```text
render every slide → review every slide → repair → verify again
```

## Automated tests

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

GitHub Actions 的 contract tests 目前至少驗證：

- visual-only geometry/typography change → PASS
- identical text with different run segmentation → PASS
- visible text/table value/table merge change → FAIL
- hyperlink target or object association change → FAIL
- hidden-slide state change → FAIL
- table tiny text 可被 Linter 找到
- Visual QA report 必須逐頁且所有 required checks 完整
- 沒有 Visual QA report 不得產生完整 delivery pass
- 完整且合格的 Visual QA + 無 regression → `DELIVERY_PASS=true`
- plugin manifests 指向可安裝 Skill

## Design principle

有效輸出必須同時滿足：

1. **protected content/behavior unchanged**
2. **visual design materially improved**
3. **PowerPoint native editability preserved whenever practical**
4. **quality gates provide evidence, not promises**

Prompt-only promises are not proof.