# Source Theme Discovery & Theme Lock / 來源主色調辨識與色系鎖定

> **主色調是投影片的 Visual DNA。既有簡報的預設行為是「沿著原本的靈魂美化」，不是替它換一套 AI 喜歡的皮膚。**
>
> The default is source-faithful beautification, not arbitrary restyling.

## 1. Hard rule / 硬性原則

除非使用者明確要求「換色系 / rebrand / dark mode / light mode / new visual identity」，Design Agent **不得做色系極性翻轉**：

- light deck → dark deck：禁止
- dark deck → light deck：禁止
- 原本白底工程簡報 → 大面積深藍/黑底：禁止
- 原本品牌主色明確 → 換成無關主色：禁止

允許的是：在原主色系裡做更好的 contrast、spacing、tint/shade、accent hierarchy、table/chart styling。

## 2. Evidence priority / 辨識證據優先序

Theme Discovery 必須在任何美化前完成。證據權重由高到低：

1. **來源實際 render / rendered source slides**：最高權重。觀察整份 deck，而不是只看首頁。
2. **實際 slide canvas / large-area fills**：背景色、大面積矩形、band、section canvas。
3. **Master / Layout / Theme XML**：`lt1/dk1/accent1...`、master background、layout background。
4. **重複的內容視覺**：表格 header、圖表背景、axis/grid、品牌線條、反覆出現的 accent。
5. **單一圖片或單頁特殊色**：最低權重，不得用單一照片顏色推翻整份 deck。

### 重要：不要把 semantic color 誤認成 brand color

例如工程圖上的紅色 Upper/Lower Limit marker、警告紅、Pass/Fail 綠，是**語意色**，不代表整份簡報主色應變紅或綠。

## 3. Source Theme Profile / 來源視覺 DNA

開工前建立 `theme_profile.json`：

```bash
python scripts/pptx_theme_profile.py profile source.pptx --out theme_profile.json
```

至少記錄：

```json
{
  "canvas_mode": "light|dark|mixed|unknown",
  "confidence": 0.0,
  "slides": [],
  "theme_colors": {},
  "source_fonts": [],
  "theme_fonts": {},
  "accent_candidates": [],
  "review_required": true
}
```

若可 render，AI 必須用實際 source render 校正 machine profile。

## 4. Deck-level classification / 整份簡報分類

不得只看第一頁。

建議使用：

- content/data slides 權重 > title/closing slide
- 多數頁 canvas 模式決定 deck 主模式
- 若 title/section dark、data pages light，分類為 `mixed`，並保留這種 page-role pattern
- 若資料頁幾乎全部白底，視為 light technical deck，即使首頁有深色照片或品牌圖

### Engineering / technical deck 特別規則

若來源大量圖表具有：

- white chart canvas
- grey gridlines
- black/dark axis text
- sparse semantic red markers

且簡報本體也是 light canvas，預設維持 **light technical system**。可以升級表格、標題與 accent，但不得把整份轉成 dark dashboard。

## 5. Theme Lock / 色系鎖定

Theme profile 建立後，進入 `THEME_LOCK`：

### MUST PRESERVE

- light / dark / mixed canvas polarity
- 明確的品牌 hue family
- page-role pattern（例如：封面淺色、section accent、data page 白底）
- neutral family（white/off-white/grey/charcoal）的大方向
- 來源已建立的 semantic colors 意義

### MAY IMPROVE

- saturation / tint / shade
- contrast
- accent hierarchy
- border/grid neutralization
- table header intensity
- section accent strength
- background 可從 pure white 微調成 warm/cool off-white，但仍必須保持 `light`

### MUST NOT

- 因為「看起來比較高級」就把白底改深藍
- 因為 AI 常見模板偏 navy 就套 navy
- 從圖片抽一個高飽和色直接當全 deck 主色
- 把 semantic red/green 轉成 brand primary
- 每個 sigma / category 都建立一套互相競爭的主色系

## 6. Machine guard / 機器守門

美化後執行：

```bash
python scripts/pptx_theme_profile.py compare source.pptx output.pptx --json
```

高信心偵測到以下情況必須 FAIL：

- corresponding slide light → dark polarity inversion
- corresponding slide dark → light polarity inversion
- 大面積 dark visual mass 在 light source 上異常暴增

Machine guard 是保守底線；最終仍以 render visual review 判斷 `theme_fidelity_preserved`。

## 7. Render QA / 視覺確認

每一頁都要回答：

```text
theme_fidelity_preserved = true|false
```

判斷問題：

- 這頁仍像來源簡報的升級版嗎？
- 主色調、明暗極性、品牌氣質有沒有被 AI 自作主張改掉？
- source 是白底技術文件時，final 是否仍維持 light technical canvas？
- 新 accent 是協助 hierarchy，還是搶走內容主導權？

任何一頁 `theme_fidelity_preserved=false`，不得 final delivery。

## 8. User override / 使用者明確授權

只有使用者明確說出例如：

- 改成深色科技風
- 全面 rebrand
- 換成公司新 CI 色
- 不要沿用原色系

才解除 Theme Lock。

**Content Lock 與 Theme Lock 是不同層級：即使 Theme Lock 被解除，Content Lock 仍然有效。**
