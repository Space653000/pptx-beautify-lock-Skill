# PPTX Linter 規範 / PPTX Linter Rules

> 繁體中文為主；English follows each rule where useful.

## 目的 / Purpose

Linter 只負責**找出可量化的版面問題與風險**，不改內容、不自行美化。

The linter detects measurable layout and consistency defects. It must not rewrite or mutate presentation content.

## 必查項目 / Mandatory checks

### Geometry / 幾何
- 任何物件超出投影片邊界 / out-of-bounds objects
- 寬或高 <= 0 的異常物件 / non-positive geometry
- 文字框、表格、圖表、圖片之間的可疑重疊 / suspicious overlaps
- 重要物件離頁面安全邊界過近 / unsafe edge margins
- 同頁同類物件對齊誤差過大 / alignment drift

### Typography / 字體
- 過小字級 / tiny text
- 同一頁使用過多字型 / too many font families per slide
- 標題層級不一致 / inconsistent title hierarchy
- 字體尺寸階層混亂 / inconsistent font-size hierarchy
- 中英文混排時 fallback font 風險 / CJK-Latin fallback risk

### Spacing / 間距
- 物件間距極小或不一致 / cramped or inconsistent spacing
- 標題與正文間距不一致 / title-body spacing drift
- 表格 cell padding 或 row height 過小 / table density risk

### Tables / 表格
- 表格超出頁面 / table out of bounds
- 欄寬極端不均 / extreme column imbalance
- 文字過密 / excessive text density
- header/body 視覺層級不足 / weak header-body hierarchy

### Consistency / 跨頁一致性
- 頁面尺寸不一致不得發生 / slide size must be consistent
- 重複角色的元素（標題、頁碼、頁尾）位置漂移 / repeated-role position drift
- 色彩系統失控 / uncontrolled color count
- 標題字級、正文最低字級、留白節奏跨頁不一致 / cross-slide typography and spacing drift

## Severity / 嚴重度

- `ERROR`: 可能造成內容不可見、裁切、超出頁面或明顯錯誤。不得交付。
- `WARNING`: 高機率影響可讀性或視覺品質，需由 Auto Formatter / Design Agent 處理。
- `INFO`: 可改善但不阻擋交付。

## Linter 不得做的事 / Forbidden

- 不得改寫、刪除、摘要、翻譯內容。
- 不得把長文字判定為「應縮短」。只能判定為 `fit risk`。
- 不得因為重疊就直接刪除其中一個物件。
- 不得把整頁轉為圖片來規避排版問題。

## 輸出契約 / Output contract

Linter 應輸出可供下一階段處理的機器可讀結果，至少包含：

```text
LINT_PASS=true|false
lint_errors=N
lint_warnings=N
slides_checked=N
```

若支援 JSON，建議每個 finding 至少包含：

```json
{
  "slide": 3,
  "severity": "WARNING",
  "rule": "suspicious-overlap",
  "objects": ["TextBox 7", "Table 2"],
  "message_zh_TW": "文字框與表格疑似重疊",
  "message_en": "Text box may overlap the table"
}
```
