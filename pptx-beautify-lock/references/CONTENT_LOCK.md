# CONTENT LOCK / 內容凍結規範

## 核心原則 / Core principle

來源 PPTX 是唯一真實來源。AI 的任務是重新設計視覺，不是改內容。

The source PPTX is the single source of truth. The AI may redesign presentation, not meaning or data.

## MUST PRESERVE / 必須完全保留

1. Slide count and order / 頁數與順序
2. Visible text / 所有可見文字
3. Numbers, units, formulas, punctuation, symbols / 數字、單位、公式、標點、符號
4. Table structure and values / 表格結構與儲存格值
5. Chart categories, series, formulas, values, cached values, embedded workbook / 圖表資料
6. Image and media bytes / 圖片與媒體內容
7. Image crop state / 圖片裁切狀態
8. Speaker-note text / 備註文字
9. Embedded-file payloads / 嵌入檔案

## MUST NOT / 絕對禁止

- rewrite / 改寫
- summarize / 摘要
- translate / 翻譯
- shorten or expand / 縮寫或擴寫
- correct spelling, grammar, capitalization, punctuation / 校正文法、拼字、大小寫或標點
- change number formatting when it changes textual representation / 改變會影響文字呈現的數字格式
- replace an image with a visually similar image / 用相似圖片替換
- regenerate media / 重新編碼媒體
- recreate charts from guessed data / 猜測圖表資料重建
- alter table merge semantics / 改變儲存格合併語意
- delete "redundant" content / 刪除 AI 認為多餘的內容

## MAY CHANGE / 可修改

Only presentation properties: geometry, typography, spacing, alignment, colors, borders, backgrounds, shadows, table dimensions, chart styling, and other non-semantic visual properties.

只允許視覺層：位置、大小、字型、字級、間距、對齊、配色、邊框、背景、陰影、表格尺寸、圖表樣式與其他不改變內容的呈現屬性。

## Conflict rule / 衝突處理

If visual quality requires content mutation, visual quality loses.

若要變漂亮就必須改內容，則不得執行該視覺方案。

## Verification rule / 驗證規則

Prompt compliance is not proof. Run a machine-readable comparison whenever possible.

AI 說「沒有改」不算證明；應使用機器可驗證的 manifest/diff。

Final acceptance requires:

```text
CONTENT_LOCK_PASS=true
```
