---
name: pptx-beautify-lock
description: "Beautify, repair, restyle, or auto-format an existing PPT/PPTX while preserving its content. 既有 PowerPoint 需要美化、修排版、修重疊/overflow、統一字體表格或重新設計視覺，但文字/數據/圖片等內容不可變時使用。Runs PPTX Linter → Auto Formatter → Design Agent → Regression Test with hard Content Lock."
license: MIT
metadata:
  version: "0.3.0"
  languages: "zh-TW,en"
  compatibility: "Claude Code, Codex, ChatGPT Skills, Agent-Skills-compatible coding agents"
---

# PPTX Beautify Lock

**繁體中文為主要說明語言；English is used for cross-agent compatibility.**

## Leading rule: Content Lock / 核心規則

**Content Lock = protected semantics immutable; visual presentation may be redesigned aggressively.**

本 Skill 的 Content Lock 唯一定義在 [`references/CONTENT_LOCK.md`](references/CONTENT_LOCK.md)。開始修改 PPTX 前先讀該文件；若其他文件與它衝突，以 `CONTENT_LOCK.md` 為準。

這是一條四階段品質管線，不是文案重寫流程：

```text
SOURCE PPTX
  → PPTX Linter
  → Auto Formatter
  → Design Agent
  → Regression + Render Visual QA
  → FINAL PPTX
```

---

## 0. Preflight / 開工條件

1. 確認能讀取來源 `.pptx`、寫出新的 `.pptx`、執行驗證腳本。
2. 保留唯一來源檔，不原地覆寫。
3. 讀 `references/CONTENT_LOCK.md`。
4. 若來源含 animation、transition、hyperlink/action、hidden slides、OLE/embedded workbook、SmartArt、comments 或 accessibility metadata，優先**原檔就地修改視覺屬性**，避免重建造成 protected semantics 遺失。
5. 如果環境無法 render 投影片，可以做 structural candidate，但**不能宣稱 fully qualified delivery**。

**Completion criterion:** source path 與 output path 不同，且 Content Lock 已讀取。

---

## 1. Snapshot / 內容基準

在任何修改前：

```bash
python scripts/pptx_content_lock.py snapshot source.pptx --out content_manifest.json
```

保留 manifest 作為 regression 基準。

**Completion criterion:** snapshot 成功且來源 PPTX 可解析。

---

## 2. PPTX Linter / 找出問題

讀 [`references/LINTER_RULES.md`](references/LINTER_RULES.md)，執行：

```bash
python scripts/pptx_lint.py source.pptx --json > lint.before.json
```

Linter 只診斷，不修改。它負責 structural/heuristic 問題，例如：

- out-of-bounds / invalid geometry
- suspicious overlap
- tiny text
- table density risk
- unsafe edge margin
- excessive/isolated explicit font families
- dense text regions requiring render review
- title/cross-slide consistency risk

不要把 heuristic warning 當成視覺真相；真正的 overflow/clipping/美觀仍需 render。

**Completion criterion:** `lint.before.json` 已生成，所有 findings 都有可定位的 slide/rule。

---

## 3. Auto Formatter / 先修機械性問題

讀 [`references/AUTO_FORMATTER_RULES.md`](references/AUTO_FORMATTER_RULES.md)。

先做低風險、可逆、幾何優先的修改：

1. 建立一致 grid / margins / spacing rhythm。
2. 修正 out-of-bounds 與明顯非刻意 overlap。
3. 統一同角色文字的 typography hierarchy。
4. 改善 text-box margins / paragraph spacing / alignment。
5. 改善 table row/column geometry、padding 與 styling。
6. 改善 chart plot-area / legend / labels 的空間配置，不碰 protected data/text semantics。
7. 內容塞不下時改 layout；Content Lock 不因版面困難而放寬。

修改後：

```bash
python scripts/pptx_content_lock.py verify source.pptx candidate.pptx
python scripts/pptx_lint.py candidate.pptx --json > lint.after-format.json
```

若 Content Lock 失敗，立即回復/修正該輪變更，不帶著內容差異進 Design Agent。

**Completion criterion:** `CONTENT_LOCK_PASS=true`，且 structural hard errors 不比 baseline 多。

---

## 4. Design Agent / 視覺重構

讀：

- [`references/DESIGN_AGENT_RULES.md`](references/DESIGN_AGENT_RULES.md)
- [`references/DESIGN_RULES.md`](references/DESIGN_RULES.md)

目標不是「沒重疊」而已，而是 **executive-ready、乾淨、現代、專業、跨頁一致**。

可以大幅改變 visual composition，例如單欄/雙欄、多區塊、cards、bands、table/chart styling、typography、background、whitespace 與 hierarchy；但 Content Lock 始終有效。

優先保留 PowerPoint native editable objects。不要用整頁截圖/圖片逃避排版。

### Repair loop

Design Agent 最多自動跑 3 輪：

```text
design → content verify → render → visual review → repair
```

每輪都先過 Content Lock，再進下一輪。

**Completion criterion:** Content Lock 仍 PASS，且 Design Agent 已完成可 render 的 candidate。

---

## 5. Render Visual QA / 真的看每一頁

若環境具備 renderer，讀 [`references/RENDER_VISUAL_QA.md`](references/RENDER_VISUAL_QA.md)。

Render **全部頁面**，逐頁檢查並產生 `visual_qa.json`。不得只抽查首頁或 Linter 標記頁。

驗證：

```bash
python scripts/visual_qa_gate.py visual_qa.json --expected-slides <N>
```

Fully qualified delivery 必須：

```text
VISUAL_QA_PASS=true
```

若沒有 render 能力，狀態必須保持 `VISUAL_QA_PASS=false` / `VISUAL_QA_REQUIRED=true`，不可自行腦補通過。

**Completion criterion:** 每一頁都有 visual review；八個 required visual checks 全為 true，且每頁分數達門檻。

---

## 6. Regression Test / 最終品質閘門

讀：

- [`references/REGRESSION_TEST_RULES.md`](references/REGRESSION_TEST_RULES.md)
- [`references/QA_RULES.md`](references/QA_RULES.md)

完整交付執行：

```bash
python scripts/pptx_regression.py source.pptx candidate.pptx \
  --visual-qa-report visual_qa.json \
  --require-visual-qa
```

正式 final deck 只接受：

```text
CONTENT_LOCK_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
REGRESSION_PASS=true
DELIVERY_PASS=true
```

任何一個 false：candidate 仍不是 final。

**Completion criterion:** `DELIVERY_PASS=true`。

---

## 7. Fail closed / 保守失敗

遇到 verifier 無法安全判定 protected semantic、重要物件被工具丟失、render 無法完成、或任何品質 Gate 未通過時：

- 保留來源檔與最近一次 Content-Lock-safe candidate。
- 明確回報失敗 Gate 與受影響頁面/語意。
- 不用改內容、刪內容、換圖或 flatten slide 來換取通過。

---

## 8. Agent autonomy / 自動化行為

當使用者給現有 PPTX 並要求「內容不變，只美化/修版」：

- 自動啟用本 Skill，不要求使用者記住 Skill 名稱。
- 除非缺少必要品牌規範，不逐頁詢問排版偏好；自行採專業、克制、現代的設計語言。
- 自動完成 Lint → Format → Design → Render QA → Regression。
- 使用者若明確授權修改某一小部分內容，只解除該範圍的鎖；其他 protected semantics 仍維持 Content Lock。

---

## 9. Minimal activation / 最短啟動指令

```text
Use pptx-beautify-lock on this PPTX.
啟用 Content Lock，只重新設計視覺層。
自動執行 Linter → Auto Formatter → Design Agent → Render Visual QA → Regression Test。
只有 DELIVERY_PASS=true 才交付 final PPTX。
```

---

## 10. Final report / 最終回報

```text
OUTPUT=<path/to/final.pptx>
CONTENT_LOCK_PASS=true|false
LAYOUT_QA_PASS=true|false
VISUAL_QA_PASS=true|false
REGRESSION_PASS=true|false
DELIVERY_PASS=true|false
LINT_ERRORS=<N>
LINT_WARNINGS=<N>
```

不要只回覆「已美化完成」；品質 Gate 是交付的一部分。