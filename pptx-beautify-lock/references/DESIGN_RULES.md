# DESIGN RULES / 視覺設計規範

## 目標 / Goal

在完全不改內容的前提下，將投影片提升到專業商務/工程簡報等級，並**保留來源 Visual DNA**。

Upgrade the deck without changing content or arbitrarily replacing the source visual identity.

開始設計前必讀：

- [`THEME_DISCOVERY.md`](THEME_DISCOVERY.md)
- [`TYPOGRAPHY_BILINGUAL.md`](TYPOGRAPHY_BILINGUAL.md)

## 視覺優先順序 / Visual priorities

1. Source theme fidelity / 來源主色調忠實度
2. Hierarchy / 視覺階層
3. Readability / 可讀性
4. Bilingual typography / 繁中英文兼容
5. Alignment / 對齊
6. Spacing rhythm / 間距節奏
7. Consistency / 跨頁一致性
8. Density control / 資訊密度控制
9. Restraint / 避免過度裝飾

## Color / 主色調與配色

### Source-first rule

- source light → final 保持 light
- source dark → final 保持 dark
- source mixed → 保留原本 page-role pattern
- 原本已有品牌色 → 沿用同 hue family；只做 tint/shade/contrast 升級
- 不得因為 AI 偏好 navy/black 就把白底簡報改成深色

若來源是白底工程圖表、灰 grid、黑文字、紅色 limit marker，預設建立 **light technical visual system**；紅色是 semantic accent，不是全 deck brand primary。

### Allowed

- white → subtle off-white
- grey neutral refinement
- 原 accent 的較深/較淺色階
- table header、section band 使用來源 hue family
- semantic warning/pass/fail colors 保持原意

### Forbidden without user override

- light ↔ dark polarity inversion
- unrelated new primary hue
- high-saturation multi-color dashboard treatment
- 把圖表 marker 顏色誤升級成全 deck 主色

## Typography / 繁中英文雙語字體

### Default safe strategy

優先使用一個完整支援繁中的 Sans Serif 字族同時承擔中英文，例如：

- Noto Sans TC
- Microsoft JhengHei / 微軟正黑體
- PingFang TC / 蘋方-繁
- Source Han Sans TC / 思源黑體 TC

只有在環境已確認字體存在時使用。

### Latin pairing

Aptos / Inter / Arial / Helvetica 可用於**純英文 run**，但不得把包含繁中的 mixed run 整段指定為 Latin-only font，避免不可控 fallback。

若採中英分字族：

- 繁中：CJK-safe family
- 純英文：Latin family
- 數字與技術符號要 render 驗證 baseline/weight
- run segmentation 改變後仍需 Content Lock PASS

同一份簡報原則上最多 1 套 CJK + 1 套 Latin family。

Recommended minimums：

- Cover title: 28–40 pt
- Section title: 24–34 pt
- Data title: 22–30 pt
- Body: 16–22 pt
- Dense table: 11–16 pt
- Footnote: 10–12 pt

不要以過度縮小字級解決 overflow。

## Layout / 版面

- 使用一致 grid。
- 頁面四周保留安全邊界。
- 同層級元素使用一致起始線。
- 優先建立 1–3 個 visual anchors。
- 可重新排列既有物件，但不得改變內容或跨頁搬移內容。
- 真正標題優先；不得讓 generic template placeholder 疊在內容上。

## Tables / 表格

可修改：欄寬、列高、padding、header fill、border、alignment、font styling、size/placement。

不可修改：cell values、row/column order、merged-cell semantics、units、footnotes。

Design guidance：

- 減少不必要框線
- header 明顯但克制
- 數字通常右對齊
- 高密度表格優先用 CJK-safe 單一字族，避免 fallback 造成欄列跳動

## Charts / 圖表

可調整 visual style，但不得改 data。

Allowed：color palette within Theme Lock、font、legend、axis styling、label placement、plot-area size、background/border。

Forbidden：changing values、filtering、reordering data、未授權改 chart type、把 semantic red/green 改成其他含義。

## Images / 圖片

- 可移動與縮放
- 不可替換/重生成
- 預設不可改 crop state
- 保持 aspect ratio，除非來源本來即非等比例

## Visual repair / 版面修復

必須主動處理：

- unintended overlap
- template-placeholder artifacts
- clipping / overflow
- out-of-bounds
- inconsistent margins / alignment
- inconsistent font sizing
- CJK fallback / missing glyph risk
- table/chart collisions
- source-theme polarity drift

## Native editability / 可編輯性

優先保留 PowerPoint 原生可編輯物件。不得把整頁 flatten 成圖片來取得視覺效果。
