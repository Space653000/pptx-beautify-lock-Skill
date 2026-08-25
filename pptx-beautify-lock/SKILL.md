---
name: pptx-beautify-lock
description: Beautify or repair an existing PowerPoint while freezing all source content. 適用於既有 PPT/PPTX 的自動美化、排版修復、重疊與 overflow 修正；文字、數字、表格資料、圖表資料、圖片內容、備註、頁數與頁面順序不得擅自變更，只允許重新設計視覺層。
license: MIT
metadata:
  version: "0.1.0"
  languages: "zh-TW,en"
  compatibility: "Claude Code, Codex, ChatGPT Skills, Agent-Skills-compatible coding agents"
---

# PPTX Beautify Lock / PowerPoint 內容鎖定美化

## 使命 / Mission

把既有 PowerPoint 變成**明顯更漂亮、更一致、更專業、可直接上台**的版本，同時維持來源內容 100% 不變。

Turn an existing PowerPoint deck into a materially better-designed, presentation-ready deck while keeping source content unchanged.

> **內容是不可變的；視覺層可以大幅重做。**  
> **Content is immutable; the visual layer may be redesigned aggressively.**

本 Skill 的角色是 **Visual Designer + Layout Engineer**，不是文案編輯、翻譯、分析師或校稿員。

---

## 絕對不變條件 / Absolute invariant

**CONTENT MUST REMAIN SEMANTICALLY IDENTICAL. / 內容必須語意與資料完全一致。**

若「更漂亮」與「內容不變」衝突，永遠以內容不變為最高優先。

開始前必讀：

1. `references/CONTENT_LOCK.md`
2. `references/DESIGN_RULES.md`
3. `references/QA_RULES.md`

---

## 凍結內容 / Frozen content

不得擅自變更：

- 投影片頁數與順序 / slide count and order
- 所有可見文字，包括標點、數字、單位、公式、符號、大小寫、語言 / all visible text
- 表格儲存格值、列欄順序、合併關係與資料結構 / table content and semantics
- 圖表類別、系列名稱、來源數值、公式、cached values、embedded workbook / chart data
- 圖片與媒體實際 payload / image and media bytes
- 圖片裁切狀態 / image crop state
- Speaker Notes / 備註文字
- embedded files / 嵌入檔案

嚴禁：

- 改寫 / rewrite
- 摘要 / summarize
- 縮短或擴寫 / shorten or expand
- 翻譯 / translate
- 校正文法、拼字、標點 / grammar or spelling correction
- 新增或刪除內容 / add or delete content
- 合併或拆分投影片 / merge or split slides
- 改變投影片順序 / reorder slides

---

## 允許修改的視覺層 / Allowed visual changes

可依需要大幅調整：

- 字型 / font family
- 字級 / font size
- 粗細、強調、顏色 / weight, emphasis, color
- 文字框位置、大小、內距 / text-box geometry and margins
- 行距、段距、對齊 / line spacing, paragraph spacing, alignment
- 物件 x/y、width/height / object geometry
- 留白、grid、alignment / whitespace and alignment
- 表格欄寬、列高、padding、fill、border、header styling
- 圖表配色、字型、legend、axis、plot-area 等「不碰資料」的 styling
- 背景、fill、border、shadow、accent
- 圖片位置與顯示大小；不得替換圖片，不得改 crop
- 視覺階層、版面構成、平衡、節奏
- 修復 accidental overlap、overflow、clipping、out-of-bounds

---

## Fit-first 原則 / When content does not fit

如果內容塞不下，**禁止改字或刪字**。

依序嘗試：

1. 重新配置 layout
2. 擴大可用內容區
3. 減少不必要 padding / margins
4. 重分配 whitespace
5. 移動或縮放鄰近物件
6. 改用更適合的 table / multi-column layout
7. 最後才降低字級，而且不得低於 `DESIGN_RULES.md` 的可讀性門檻

Do not solve overflow by rewriting content.

---

## 強制工作流程 / Mandatory workflow

### Phase 0 — Backup

永遠保留原始檔；不得原地覆蓋。

Recommended:

```text
input.pptx
input.original.pptx
output.beautified.pptx
```

### Phase 1 — Content snapshot

在任何修改之前執行：

```bash
python scripts/pptx_content_lock.py snapshot input.pptx --out content_manifest.json
```

或使用等效工具完成相同驗證。

### Phase 2 — Inspect the original deck

- render 全部投影片（若環境支援）
- 檢查 hierarchy、spacing、alignment、table density
- 找出 overlap、overflow、clipping、out-of-bounds
- 找出跨頁不一致的 typography / color / spacing

### Phase 3 — Visual-only redesign

可以重做整個視覺系統，但不得碰 frozen content。

優先使用**原生 PowerPoint 可編輯物件**。不得為了省事把整頁 flatten 成單一圖片。

### Phase 4 — Layout QA

執行：

```bash
python scripts/verify_layout.py output.beautified.pptx
```

並在可能時 render 全部投影片做視覺檢查。

### Phase 5 — Content verification

執行：

```bash
python scripts/pptx_content_lock.py verify input.pptx output.beautified.pptx
```

只有看到：

```text
CONTENT_LOCK_PASS=true
```

才可以交付。

若 `CONTENT_LOCK_PASS=false`，不得交付，必須修復差異後重新驗證。

---

## 美化目標 / Design target

不是「勉強不重疊」就算完成。

目標：

- executive-ready / 可直接對主管簡報
- strong visual hierarchy
- clean alignment grid
- consistent spacing rhythm
- coherent typography
- readable tables
- restrained, professional color system
- high information density without visual chaos
- no unintended overlap or clipping
- consistent cross-slide design language

---

## Fail-closed / 保守失敗策略

遇到以下情況，**寧可判定失敗，也不要自行猜測內容是否可改**：

- content verifier 無法確認一致
- chart embedded data 無法安全比較
- media 被替換或重新編碼
- notes / embedded objects 讀取失敗
- 修改工具會不可避免地重寫來源內容

Report the limitation instead of claiming success.

---

## 對 AI 的最短啟動指令 / Minimal activation prompt

```text
Use pptx-beautify-lock on this PPTX.
啟用 CONTENT LOCK：內容 100% 凍結，只重做視覺層。
不得修改文字、數字、表格資料、圖表資料、圖片內容、備註、頁數或頁面順序。
自動修復字型、字級、位置、留白、對齊、表格尺寸、色彩、背景、視覺階層、overlap、overflow。
完成後一定要跑 content verification 與 layout QA；只有 CONTENT_LOCK_PASS=true 才能交付。
```
