# Auto Formatter 自動格式化規範 / Auto Formatter Rules

## 核心定位 / Role

Auto Formatter 是**保守的幾何與一致性修復器**。它先解決「亂、歪、擠、字太小、間距不一致、表格難讀」等問題，但不負責大幅改變視覺概念。

The Auto Formatter is a conservative geometry and consistency repair stage. It improves layout without changing content semantics.

## 可自動調整 / Allowed automatic changes

- x/y 位置、width/height
- 字型、字級、粗細、顏色
- 文字框內距、行距、段距、對齊
- 同類元素對齊、等距分布
- 表格欄寬、列高、cell padding、fill、border
- 圖表 legend、axis label、plot area 幾何與視覺樣式，但不得變更圖表資料
- 圖片顯示大小與位置；不得替換圖片、不得改 crop state
- 背景、線條、邊框、色彩與視覺階層

## 修復優先序 / Repair order

若發現 overflow、overlap 或過度擁擠：

1. 重新分配空間 / redistribute available space
2. 對齊到一致 grid / align to a consistent grid
3. 減少不必要 margins/padding
4. 調整鄰近物件尺寸與位置
5. 重新配置 table/chart/image 的佔比
6. 必要時調整字型或字級
7. 只有在仍無法容納時，交給 Design Agent 做更大幅度 layout redesign

**永遠不得以刪字、摘要、改寫、翻譯來解決空間不足。**

## 字級保守門檻 / Conservative font floor

除非來源本來更小，新的字級不應低於：

- 主標題 / title: 24 pt
- 次標題 / subtitle: 18 pt
- 一般正文 / body: 14 pt
- 表格與註記 / table/annotation: 11 pt

若資訊密度極高而無法符合門檻，標記 `DESIGN_ESCALATION_REQUIRED=true`，交由 Design Agent 重新構圖，而不是繼續縮字。

## 對齊與間距 / Alignment and spacing

- 優先使用清楚的左對齊與基準線。
- 同一群組的水平/垂直間距應一致。
- 標題、內文、圖表、表格之間保留可辨識層級的 whitespace。
- 不追求機械式平均分布；優先服務資訊階層。

## 表格 / Tables

Auto Formatter 可以將難讀的表格重新排得更清楚，但必須保留：

- row order
- column order
- merged-cell semantics
- every cell value
- units and footnotes

不得把表格資料摘要成卡片、圖示或其他資料結構；若 Design Agent 想改變呈現形式，也只能在**原表格仍完整保留**的前提下加強視覺，除非使用者另行明確授權內容轉換。

## 完成條件 / Completion gate

Auto Formatter 完成後必須重新執行 Linter。

若仍存在 `ERROR`，不得進入最終交付。
若僅剩視覺層級與美感問題，進入 Design Agent。
