---
name: pptx-beautify-lock
description: "PPTX Linter + Auto Formatter + Design Agent + Regression Test. 對既有 PowerPoint 啟用硬性 Content Lock：內容 100% 凍結，只允許重新設計視覺層；自動找出排版問題、修復格式、提升設計品質，最後以內容一致性與版面回歸測試把關。"
license: MIT
metadata:
  version: "0.2.0"
  languages: "zh-TW,en"
  compatibility: "Claude Code, Codex, ChatGPT Skills, Agent-Skills-compatible coding agents"
---

# PPTX Beautify Lock
## PPTX Linter + Auto Formatter + Design Agent + Regression Test

> **繁體中文為主要說明語言；English is included for cross-agent compatibility.**

## 0. 使命 / Mission

將任何既有 `.pptx` 在**不改內容**的前提下，自動修復並重新設計成更乾淨、更一致、更專業、更適合簡報的版本。

Beautify and repair an existing PowerPoint deck while preserving its source content exactly.

本 Skill 不是文案編輯器。它是一條四階段 PPTX 品質管線：

```text
SOURCE PPTX
   ↓
[1] PPTX LINTER
找出版面、字體、重疊、邊界、間距與一致性問題
   ↓
[2] AUTO FORMATTER
先做保守的幾何、字級、表格與一致性修復
   ↓
[3] DESIGN AGENT
在 Content Lock 下大幅重新設計視覺層
   ↓
[4] REGRESSION TEST
內容零變更 + 版面不得退化 + 可交付性驗證
   ↓
FINAL PPTX
```

---

# 1. 最高優先級：CONTENT LOCK / Absolute invariant

> **內容是不可變的；視覺層可以大幅重做。**  
> **Content is immutable; the visual layer may be redesigned aggressively.**

若「更漂亮」與「內容不變」衝突，永遠以內容不變為最高優先。

開始前必讀：

1. `references/CONTENT_LOCK.md`
2. `references/LINTER_RULES.md`
3. `references/AUTO_FORMATTER_RULES.md`
4. `references/DESIGN_AGENT_RULES.md`
5. `references/REGRESSION_TEST_RULES.md`
6. `references/DESIGN_RULES.md`
7. `references/QA_RULES.md`

---

# 2. 凍結內容 / Frozen content

以下內容不得擅自變更：

- 投影片頁數與頁面順序 / slide count and order
- 所有可見文字，包括標點、數字、單位、公式、符號、大小寫、語言 / all visible text
- 表格儲存格值、列欄順序、合併關係與資料語意 / table data and semantics
- 圖表類別、系列名稱、來源數值、公式、cached values、embedded workbook / chart data
- 圖片與影音的實際 payload / image and media bytes
- 圖片 crop state / 裁切狀態
- Speaker Notes / 備註文字
- embedded files / 嵌入檔案

## 絕對禁止 / Never

- rewrite / 改寫
- summarize / 摘要
- shorten or expand / 縮短或擴寫
- translate / 翻譯
- grammar/spelling/punctuation correction / 校正文法拼字標點
- add/delete content / 新增刪除內容
- merge/split slides / 合併拆分頁面
- reorder slides / 改變頁面順序
- replace an original image with a generated/similar image / 以生成圖片或相似圖片取代原圖
- flatten an editable slide into one full-slide image / 將整頁可編輯內容扁平化成單一圖片

如果使用者另行明確授權改內容，該授權只適用於使用者明確指定的範圍；其餘內容仍保持鎖定。

---

# 3. 允許修改的視覺層 / Allowed visual changes

可依需要大幅調整：

- 字型、字級、粗細、顏色
- 文字框位置、大小、內距
- 行距、段距、paragraph alignment
- 物件 x/y、width/height
- whitespace、grid、alignment、distribution
- 表格欄寬、列高、cell padding、fill、border、header styling
- 圖表 typography、colors、legend、axis、plot-area geometry；**不得改 chart data**
- 背景、fill、border、shadow、accent
- 圖片顯示位置與尺寸；**不得替換圖片、不得改 crop state**
- visual hierarchy、composition、balance、spacing rhythm
- 修復 accidental overlap、overflow、clipping、out-of-bounds

---

# 4. Phase 0 — 保留原始檔 / Backup first

永遠不得覆寫唯一來源檔。

建議：

```text
input.pptx
input.original.pptx
output.beautified.pptx
```

在任何修改前建立 Content Snapshot：

```bash
python scripts/pptx_content_lock.py snapshot input.pptx --out content_manifest.json
```

---

# 5. Phase 1 — PPTX Linter

執行：

```bash
python scripts/pptx_lint.py input.pptx --json > lint.before.json
```

Linter 只找問題，不修改內容。

至少檢查：

- out-of-bounds
- non-positive geometry
- suspicious overlap
- tiny text
- unsafe edge margins
- too many font families
- table density / readability risk
- cross-slide consistency risk

若工具環境支援 render，必須同時 render 全部投影片做視覺檢查。程式 heuristic 不能取代視覺 QA。

---

# 6. Phase 2 — Auto Formatter

Auto Formatter 先做**保守、可逆、幾何優先**的修復：

1. 建立一致 grid
2. 對齊同角色元素
3. 修正超出邊界
4. 修正非刻意 overlap
5. 統一 spacing / margins / padding
6. 修正過度混亂的 font family / size hierarchy
7. 改善 table row height / column width / cell padding
8. 改善 chart labels / legend / plot-area 空間

## 內容塞不下時 / Fit-first

**不得改字或刪字。**依序：

1. 重新配置 layout
2. 擴大可用內容區
3. 減少不必要 padding / margins
4. 重分配 whitespace
5. 移動或縮放鄰近物件
6. 改用更適合的欄位布局
7. 最後才降低字級，而且不得低於可讀性門檻；若仍塞不下，升級給 Design Agent 重構版面

Do not solve overflow by rewriting content.

Auto Formatter 完成後重新執行 Linter：

```bash
python scripts/pptx_lint.py output.beautified.pptx --json > lint.after-format.json
```

---

# 7. Phase 3 — Design Agent

Design Agent 可以**大幅重做視覺系統**，但 Content Lock 永遠有效。

目標：

- executive-ready / 可直接對主管與客戶簡報
- modern, clean, professional
- strong visual hierarchy
- consistent alignment grid
- disciplined whitespace
- coherent typography
- restrained color system
- readable tables and charts
- high information density without chaos
- cross-slide consistency

## 可大幅重構 / Aggressive layout redesign allowed

- 單欄改雙欄、多欄
- 重新安排文字、表格、圖表、圖片的空間關係
- 重做 title/content zones
- 使用 cards、bands、dividers、accent blocks
- 重做 table styling
- 重做 chart visual styling

但不得：

- 刪文字讓畫面看起來乾淨
- 把長段落摘要成幾點
- 移除表格只留摘要卡片
- 換掉圖片
- 改變 chart data
- 增刪或重排投影片

## 保持可編輯性 / Preserve editability

優先使用 PowerPoint native editable objects。若編輯工具支援 OOXML、PptxGenJS、python-pptx、PowerPoint automation 或其他可靠方式，應保持 text boxes / tables / charts / shapes 可編輯。

---

# 8. Phase 4 — Regression Test

完成視覺修改後，**不得直接交付**。

先執行內容驗證：

```bash
python scripts/pptx_content_lock.py verify input.pptx output.beautified.pptx
```

唯一允許：

```text
CONTENT_LOCK_PASS=true
```

再執行整體回歸測試：

```bash
python scripts/pptx_regression.py input.pptx output.beautified.pptx
```

期望：

```text
REGRESSION_PASS=true
CONTENT_LOCK_PASS=true
LAYOUT_QA_PASS=true
```

回歸測試至少保證：

- 內容一致
- final deck 沒有 hard out-of-bounds / invalid geometry
- layout hard errors 不得比來源更多
- heuristic warnings 原則上不得增加
- PPTX 可正常解析

如果環境可 render，必須 render 最終版逐頁做最後 Visual QA。

---

# 9. Fail-closed / 保守失敗策略

以下任一情況，**不得宣稱完成**：

- content verifier 無法證明一致
- chart data / embedded workbook 無法安全比較
- media 被重新編碼或替換
- crop state 改變
- notes / embedded objects 讀取失敗
- 修改工具不可避免地重寫 frozen content
- regression test 失敗

遇到不確定時，輸出 `FAIL` 與限制，而不是猜測。

---

# 10. 對 Agent 的行為要求 / Agent behavior

如果使用者提供 PPTX 與此 repository URL：

1. 先閱讀本 `SKILL.md` 與 references。
2. 確認能存取 PPTX 並有能力修改/產出檔案。
3. 不要逐頁詢問使用者排版偏好；除非使用者指定品牌規範，否則自行採專業、克制、現代的設計。
4. 自動完成 Lint → Format → Design → Regression。
5. 不要因為來源很醜就重新撰寫內容。
6. 只有所有硬性 Gate PASS 才交付 final PPTX。

如果環境**只能閱讀、不能修改 PPTX 或不能執行驗證**，明確說明能力限制；不得假裝已執行 Content Lock。

---

# 11. Claude Code / Codex 快速啟動 / Minimal activation

```text
Read this repository and use pptx-beautify-lock/SKILL.md.

請對提供的 PPTX 執行：
PPTX Linter → Auto Formatter → Design Agent → Regression Test。

啟用 CONTENT LOCK：內容 100% 凍結，只允許重新設計視覺層。
不得修改文字、數字、表格資料、圖表資料、圖片內容、crop、備註、頁數或頁面順序。

自動修復字型、字級、位置、留白、對齊、表格尺寸、色彩、背景、視覺階層、overlap、overflow，並把整體設計提升到專業可上台品質。

不要逐頁問我；自行完成。
只有 CONTENT_LOCK_PASS=true、LAYOUT_QA_PASS=true、REGRESSION_PASS=true 才能交付。
```

---

# 12. 最終交付報告 / Final delivery report

Agent 完成後應簡短回報：

```text
OUTPUT=<path/to/final.pptx>
CONTENT_LOCK_PASS=true
LINT_ERRORS=<N>
LINT_WARNINGS=<N>
LAYOUT_QA_PASS=true
REGRESSION_PASS=true
VISUAL_QA=PASS|MANUAL_REVIEW_REQUIRED
```

不要只說「已美化完成」；必須回報品質閘門結果。
