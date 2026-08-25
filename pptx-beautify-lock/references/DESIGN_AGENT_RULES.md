# Design Agent 規範 / Design Agent Rules

## 角色 / Role

Design Agent 負責在 **Content Lock 已建立、Source Theme Discovery 已完成、Linter 已完成、Auto Formatter 已做基礎修復** 後，進行大幅度但只限視覺層的重新設計。

The Design Agent may redesign composition aggressively, but it must preserve every frozen content element **and the source visual DNA unless the user explicitly requests a rebrand/theme change**.

## 設計目標 / Design target

- 專業、乾淨、現代、可直接上台
- executive-ready / management-ready
- 強烈但不誇張的視覺階層
- 清楚的 grid、alignment、spacing rhythm
- **沿著來源主色調、明暗極性與品牌氣質升級，不自行換皮**
- 繁中＋英文都清楚、漂亮、glyph-safe
- 跨頁一致的字體、色彩、標題與內容框架
- 高資訊密度仍保持可掃讀性

## Before design: Visual DNA / 設計前必讀

必須先讀：

- [`THEME_DISCOVERY.md`](THEME_DISCOVERY.md)
- [`TYPOGRAPHY_BILINGUAL.md`](TYPOGRAPHY_BILINGUAL.md)

並建立：

```bash
python scripts/pptx_theme_profile.py profile source.pptx --out theme_profile.json
```

如果環境可 render，必須看來源 render，尤其是首頁、section page、代表性 data/table/chart pages。

**不得在沒有 theme profile 的情況下直接決定 navy、black、gradient、corporate blue 等新主色。**

## 預設設計原則 / Default design principles

### 1. Source theme first / 來源主色優先

Beautify ≠ rebrand。

- source light → final 保持 light
- source dark → final 保持 dark
- source mixed → 保留 page-role pattern
- source 有品牌主色 → 以同 hue family 做 tint/shade/contrast 升級

除非使用者明確要求換色系，禁止 light ↔ dark 180° 翻轉。

### 2. Hierarchy first / 階層優先

先讓觀眾一眼知道：標題、結論、主要數據、支撐資訊、備註各是什麼角色。

### 3. Fewer visual systems / 減少視覺語言數量

每份簡報原則上控制：

- 1 個主要 bilingual-safe font family，或最多 1 套 CJK + 1 套 Latin pairing
- 來源既有主色 + 1–2 個受控輔助色 + neutrals
- 2–4 個主要字級層級

### 4. Bilingual typography / 繁中英文兼容

預設先選完整支援繁中的字族，讓中英文共享一致 baseline；只有在已驗證的 pure-Latin run 才考慮 Aptos/Inter 等 Latin family。

不得把含繁中的 mixed run 整段指定為 Latin-only font。

### 5. Preserve editability / 保持 PowerPoint 可編輯性

優先保留 native PowerPoint shapes、text boxes、tables、charts。不得把整頁 flatten 為單一圖片。

### 6. Content density without chaos / 高密度但不混亂

可以重排物件、改欄數、改卡片式布局、改圖片與表格比例，但不得改內容本體。

### 7. Visual consistency / 跨頁一致性

對同角色元素使用一致規則：

- title zone
- subtitle zone
- content grid
- footer/page number
- table headers
- chart title/legend/axis styling
- canvas polarity / background family
- bilingual font policy

## 允許的大幅重構 / Aggressive visual redesign allowed

- 單欄改雙欄或多欄
- 重新排列文字框、表格、圖片、圖表的空間關係
- 將零散文字框收斂到一致 grid
- 在**來源 Theme Lock 範圍內**重做區塊、卡片、分隔線、accent
- 重新設計表格視覺樣式
- 重新設計 chart visual styling
- 重新安排文字與圖片比例

但必須保持：

- 所有原文字仍存在且字元完全相同
- 所有表格資料與結構仍相同
- 所有圖表資料仍相同
- 所有圖片 payload 與 crop state 不變
- 頁面數與順序不變
- source canvas polarity / visual DNA 不被無授權翻轉

## 禁止的「假美化」 / Forbidden shortcuts

- 為了乾淨而刪掉一半文字
- 將內容改寫成三個 bullet
- 把表格資料改成摘要卡片並移除原表格
- 重新生成相似圖片替代原圖片
- 將整頁 rasterize / flatten 成圖片
- 因為版面不好處理就新增或刪除投影片
- **因為 AI 偏好深藍科技感，就把原本白底 deck 改 dark navy**
- **因為英文使用 Inter/Aptos，就讓繁中依賴不可控 fallback**
- 把圖表中的警告紅/limit red 誤當成整份 deck brand primary

## Template placeholder handling / 母片 placeholder

若 source/master/layout 帶有 `presentation title`、`click to add title` 等 generic placeholder：

- 真正來源內容優先
- final 不得 render generic template prompt
- 不得為了消除重疊而刪除真正標題
- 優先用 layout assignment、blank/content-safe layout、placeholder visibility/instance handling 解決
- 每輪都重新 Content Lock verify

## Visual QA / 視覺驗收

若環境可 render PPTX，必須逐頁看 render 結果，至少檢查：

- hierarchy
- alignment
- whitespace
- typography
- bilingual glyph/font consistency
- source-theme fidelity
- table readability
- chart readability
- image balance
- clipping
- overlap
- template-placeholder artifacts
- cross-slide consistency

若有能力使用 vision model，將 source + final render 當成 QA 輸入，但**不得讓 vision model 改寫內容**。

## 完成門檻 / Exit gate

Design Agent 完成後不得直接交付。至少先執行：

```bash
python scripts/pptx_theme_profile.py compare source.pptx candidate.pptx --json
python scripts/pptx_content_lock.py verify source.pptx candidate.pptx
```

Theme Guard 或 Content Lock 任一失敗，都必須 repair；通過後才進入 Render Visual QA + Regression Test。
