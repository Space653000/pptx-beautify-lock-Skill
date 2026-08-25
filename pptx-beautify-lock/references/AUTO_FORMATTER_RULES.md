# Auto Formatter 自動格式化規範 / Auto Formatter Rules

## 核心定位 / Role

Auto Formatter 是**保守的幾何與一致性修復器**。它先解決「亂、歪、擠、字太小、間距不一致、表格難讀」等問題，不負責替簡報換品牌或換明暗色系。

The Auto Formatter repairs layout while preserving Content Lock **and the discovered source Theme Lock**.

開始前必須已有：

- `content_manifest.json`
- `theme_profile.json`

並讀：

- `THEME_DISCOVERY.md`
- `TYPOGRAPHY_BILINGUAL.md`

## 可自動調整 / Allowed automatic changes

- x/y、width/height
- 字型、字級、粗細、顏色（受 Theme Lock + bilingual typography 約束）
- text-box margins、line/paragraph spacing、alignment
- 同類元素對齊、等距分布
- table column/row sizing、padding、fill、border
- chart legend/axis/plot-area geometry 與 style，但不得變更 data
- 圖片顯示大小與位置；不得替換、不得改 crop state
- 背景、線條、邊框、accent，但只能在來源 visual DNA 內優化

## Theme-safe formatting / 色系安全

Auto Formatter **不得主動創建新主色系**。

- source light → 保持 light canvas
- source dark → 保持 dark canvas
- source mixed → 保留 page-role pattern
- 可以用 source accent 的 tint/shade
- semantic red/green 不得被誤當 brand primary
- 不得用大面積 navy/black 來「增加科技感」，除非 source 本來如此或使用者授權

## Bilingual-safe formatting / 繁中英文安全

- 優先沿用來源中已穩定的 CJK-safe font
- 換字體時優先 Noto Sans TC / Microsoft JhengHei / PingFang TC / Source Han Sans TC 等實際可用字族
- Aptos / Inter / Arial / Helvetica 類只用於 pure-Latin run；含繁中的 mixed run 不得整段套用
- 表格預設使用單一 CJK-safe family，以降低 fallback 與 alignment drift

## 修復優先序 / Repair order

若發現 overflow、overlap 或擁擠：

1. 重新分配空間
2. 對齊一致 grid
3. 減少不必要 margins/padding
4. 調整鄰近物件尺寸與位置
5. 重新配置 table/chart/image 比例
6. 必要時調整字型/字級，但保持 bilingual-safe
7. 仍無法容納才交給 Design Agent 重構

**永遠不得用刪字、摘要、翻譯、改寫來解決空間不足。**

## 字級保守門檻 / Conservative font floor

除非來源本來更小：

- 主標題：24 pt
- 次標題：18 pt
- 一般正文：14 pt
- 表格/註記：11 pt

低於門檻仍塞不下 → `DESIGN_ESCALATION_REQUIRED=true`。

## Template placeholder / 母片提示文字

若偵測到 `presentation title` / `click to add title` 等 generic template text：

- 真正來源內容優先
- 不刪真正標題
- 優先停用 placeholder instance、改 content-safe layout 或重新安排 layout assignment
- 不能修改受 Content Lock 保護的 master/layout 語意來硬解

## 表格 / Tables

必須保留：row order、column order、merged-cell semantics、every cell value、units、footnotes。

不得把原表格摘要成卡片後移除原表格。

## 完成條件 / Completion gate

Auto Formatter 後執行：

```bash
python scripts/pptx_content_lock.py verify source.pptx candidate.pptx
python scripts/pptx_theme_profile.py compare source.pptx candidate.pptx --json
python scripts/pptx_lint.py candidate.pptx --json
```

Content Lock / Theme Guard 任一 blocking failure，不得進 Design Agent。
