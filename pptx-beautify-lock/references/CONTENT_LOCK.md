# CONTENT LOCK / 內容凍結規範

> **本文件是 Content Lock 的唯一權威定義。** 其他文件只應引用本規範，不應建立另一套不同的凍結清單。
>
> **This file is the single source of truth for Content Lock.**

## 核心原則 / Core principle

來源 PPTX 是唯一真實來源。AI 的任務是重新設計**呈現方式**，不是改變內容、資料、互動行為或隱藏語意。

The source PPTX is the single source of truth. The AI may redesign presentation properties, not protected semantics.

## MUST PRESERVE / 必須完全保留

### A. 頁面與文字 / Slides and text

- slide count and order / 頁數與順序
- visible text / 所有可見文字
- numbers, units, formulas, punctuation, symbols, capitalization, language
- text stored in slide masters/layouts when it is part of presentation content
- SmartArt/diagram data text
- Office Math formula semantics

### B. 表格與圖表 / Tables and charts

- table cell values and row/column order
- table merge topology (`gridSpan`, `rowSpan`, `hMerge`, `vMerge`)
- chart categories, series labels/order semantics, formulas, cached values, titles/labels
- embedded workbook/package payloads used by charts or OLE objects

### C. 圖片與媒體 / Images and media

- every original image/audio/video payload byte-for-byte
- original image crop state
- no replacement, removal, re-encoding, or silent addition of package media

若需要額外裝飾，優先使用 PowerPoint native shapes、fills、lines、icons already present in the source。新增外部圖片/影音屬於內容擴張，需使用者明確授權。

### D. 備註、註解與無障礙語意 / Notes, annotations and accessibility

- speaker-note text and protected note semantics
- comments/threaded comments and author/person annotation payloads
- alt text / accessibility title and description

### E. 互動與播放行為 / Interaction and playback semantics

除非使用者明確授權，以下亦視為 frozen semantics：

- hyperlinks and hyperlink targets
- mouse-over/click actions
- external relationship targets used by content
- hidden/shown slide state
- slide transitions
- animation/timing trees

這些項目即使「看起來不像內容」，改變後也可能使簡報傳達方式或使用行為不同，因此預設鎖定。

## MUST NOT / 絕對禁止

- rewrite / 改寫
- summarize / 摘要
- translate / 翻譯
- shorten or expand / 縮短或擴寫
- correct spelling, grammar, capitalization, punctuation / 校正文法、拼字、大小寫或標點
- change number formatting when it changes textual representation
- replace or regenerate media
- add new raster/media assets without explicit authorization
- recreate charts from guessed data
- alter table merge semantics
- delete content judged "redundant"
- change hyperlinks/actions/hidden state/animation/transition without authorization
- flatten editable slide content into a single full-slide image

## MAY CHANGE / 可修改

只有**非語意視覺層**可以修改，例如：

- geometry: x/y/width/height
- typography: font family, size, weight, color
- paragraph spacing/alignment and text-box margins
- whitespace, grid, distribution and z-order when protected content remains visible
- fills, borders, shadows, backgrounds and native decorative shapes
- table row height, column width, padding, fill, border and header styling
- chart typography, color, legend/axis/plot-area layout when chart data/text semantics remain unchanged
- image display position and size while preserving the original payload and crop state

## Conflict rule / 衝突處理

**If visual quality requires protected semantic mutation, visual quality loses.**

如果要變漂亮就必須改 protected content，必須換一個版面方案，而不是放寬 Content Lock。

## Verification rule / 驗證規則

Prompt compliance is not proof. Run a machine-readable comparison.

主要驗證器：

```bash
python scripts/pptx_content_lock.py verify source.pptx output.pptx
```

唯一可接受的內容結果：

```text
CONTENT_LOCK_PASS=true
```

若驗證器遇到無法安全解析的重要 protected semantic，採 **fail closed**：不得以「看起來一樣」宣稱通過。