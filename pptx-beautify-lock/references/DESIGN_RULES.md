# DESIGN RULES / 視覺設計規範

## 目標 / Goal

在完全不改內容的前提下，將投影片提升到專業商務簡報等級。

Upgrade the deck to professional presentation quality without changing content.

## 視覺優先順序 / Visual priorities

1. Hierarchy / 視覺階層
2. Readability / 可讀性
3. Alignment / 對齊
4. Spacing rhythm / 間距節奏
5. Consistency / 跨頁一致性
6. Density control / 資訊密度控制
7. Restraint / 避免過度裝飾

## Typography / 字體

- 優先使用系統可取得且跨平台穩定的字型。
- 繁中優先：Noto Sans TC、Microsoft JhengHei、PingFang TC 等實際可用字型。
- 英文優先：Aptos、Arial、Inter、Helvetica 類型；依環境可用性選擇。
- 同一份簡報主要字族不超過 2 套。
- 標題、內文、註解應形成清楚階層。
- 不要以過度縮小字級解決 overflow。

Recommended minimums unless the source format or use case demands otherwise:

- Title: 28–36 pt
- Section title: 24–32 pt
- Body: 16–22 pt
- Dense table: 12–16 pt
- Footnote: 10–12 pt

若為大型會議室簡報，應優先使用更大字級。

## Layout / 版面

- 使用一致 grid。
- 頁面四周保留安全邊界。
- 同層級元素使用一致起始線。
- 優先建立 1–3 個明確 visual anchors，不讓所有物件都搶注意力。
- 可重新排列既有物件，但不得改變其內容或跨頁搬移內容。
- 不得讓文字、表格、圖表貼近頁面邊界。

## Tables / 表格

可修改：

- 欄寬、列高
- cell padding
- header fill
- borders
- text alignment
- font styling
- table overall size and placement

不可修改：

- cell values
- row/column order
- merged-cell semantics
- units
- footnotes

Design guidance:

- 減少不必要的框線。
- header 要明顯但克制。
- 數字欄位通常右對齊。
- 同類單位與小數位呈現應保留來源文字，不自行格式化。

## Charts / 圖表

可調整 style，但不得改 data。

Allowed examples:

- color palette
- font
- legend position
- axis styling
- data-label placement
- plot-area size
- chart background/border

Forbidden examples:

- changing values
- filtering categories
- reordering data for storytelling
- replacing chart type when it could change interpretation without explicit user instruction

若更換 chart type 可能改變解讀，預設禁止。

## Images / 圖片

- 可以移動與縮放。
- 不可替換來源圖片。
- 不可重新生成。
- 預設不可改變 crop state。
- 避免拉伸變形；保持 aspect ratio，除非來源本來就是非等比例。

## Color / 配色

- 建立有限且一致的 palette。
- 背景與文字要有足夠對比。
- 強調色只用於真正需要 attention 的項目。
- 不要每個區塊使用不同高飽和色。

## Visual repair / 版面修復

必須主動處理：

- unintended overlap
- clipping
- overflow
- out-of-bounds
- inconsistent margins
- misalignment
- inconsistent font sizing
- table cells that visually collide
- chart labels that collide

## Native editability / 可編輯性

優先保留 PowerPoint 原生可編輯物件。

Do not flatten an entire slide to one image merely to obtain visual fidelity.
