# Traditional Chinese + English Typography / 繁中英文雙語字體規範

> **字體必須同時服務繁體中文與英文。不能只讓英文漂亮，繁中卻靠不可控 fallback。**
>
> Typography must be visually coherent and glyph-safe for both Traditional Chinese and English.

## 1. Source-first / 先尊重來源

在美化前先盤點來源實際字型與 theme fonts：

```bash
python scripts/pptx_theme_profile.py profile source.pptx --out theme_profile.json
```

若來源已有一致、清楚、繁中完整且英文觀感合理的字體，優先沿用並只調整 size/weight/hierarchy。

只有在以下情況才主動換字體：

- source font 混亂或超過合理數量
- 繁中文字形缺失或依賴不可控 fallback
- 英文與繁中 baseline/weight 明顯不協調
- 字體在目標平台不可用
- 使用者明確要求新字體風格

## 2. Safe families / 繁中安全字族

實際使用前必須確認該字體在執行/交付環境存在。

### Cross-platform / 跨平台優先

- **Noto Sans TC**：首選的現代無襯線繁中/英文共用字族；適合技術、商務、工程簡報
- **Source Han Sans TC / 思源黑體 TC**：若環境存在，可作等價選擇
- **Noto Serif TC / Source Han Serif TC**：只在來源本身偏正式/出版/人文風格時使用，不作工程簡報預設

### Windows / Microsoft Office

- **Microsoft JhengHei / 微軟正黑體**：繁中相容與 Office 穩定度高
- **Microsoft JhengHei UI**：偏 UI/資訊密集用途，可用於表格與介面式頁面
- **Aptos / Aptos Display**：英文表現好，但不是繁中文字體；只能在確認繁中由指定 CJK 字族承接時使用

### macOS

- **PingFang TC / 蘋方-繁**：繁中顯示穩定

## 3. Recommended strategies / 推薦搭配策略

### Strategy A — One-family bilingual / 單字族雙語，最穩健

整份簡報使用一個完整支援繁中的 CJK family，同時讓它承擔 Latin glyph：

```text
Noto Sans TC
或 Microsoft JhengHei
或 PingFang TC
```

優點：

- 最少 fallback 風險
- 中文英文 baseline 一致
- 表格與工程資料穩定
- 跨頁一致性最好

這是本 Skill 的**預設保守策略**。

### Strategy B — Script-aware pairing / 中英分字族，高階但需驗證

若希望英文更精緻，可將**純英文 run** 使用 Aptos / Inter 類 Latin font，繁中 run 使用 Noto Sans TC / Microsoft JhengHei。

必要條件：

- 不能把包含繁中文字元的 mixed run 整段指定為 Latin-only font
- run segmentation 改變後必須 Content Lock PASS
- render 後必須確認 baseline、x-height、weight、line-height 協調
- 表格中的中英混排優先使用單一 CJK-safe family，避免欄列視覺跳動

## 4. Font fallback risk / fallback 風險

以下 Latin-oriented fonts 若直接套在包含繁中的文字 run，應視為 fallback risk：

- Arial
- Helvetica
- Inter
- Aptos
- Calibri
- Roboto

它們可以用於純 Latin run，但不應被當成繁中完整字族。

Linter 應對「CJK text + explicit Latin-only font」標記：

```text
WARNING cjk-font-fallback-risk
```

## 5. Visual hierarchy / 雙語視覺階層

建議值只是起點，仍要依來源密度調整：

- Cover title：28–40 pt
- Section title：24–34 pt
- Data-slide title：22–30 pt
- Body：16–22 pt
- Dense table：11–16 pt
- Footnote：10–12 pt

繁中通常比英文在相同 point size 下更密，因此不要只用英文字串測 fit。

## 6. Weight / 字重

- Title：Semibold/Bold
- Section：Semibold
- Body：Regular
- Table header：Medium/Semibold
- Numeric data：Regular/Medium

避免整頁 Bold；繁中字重過重會讓高資訊密度頁面顯得堵塞。

## 7. Engineering deck / 工程技術簡報

對圖表、Limit table、測試報告類簡報：

- 優先 Sans Serif
- 數字與單位要保持清楚，不使用裝飾字體
- 中英文標題最好共享同一視覺 baseline
- 表格內預設使用同一 CJK-safe family
- 不因為想「科技感」就使用窄體、極細體或純英文字體承擔繁中

## 8. Render QA / 最終字體驗證

每一頁必須回答：

```text
bilingual_typography_clean = true|false
```

至少檢查：

- 繁中沒有 tofu / □ / 缺字
- 沒有突然掉成不同中文字體
- 英文沒有因 CJK font 而顯得過度笨重或失衡
- 中英文 baseline、字重、行距協調
- 數字、% 、σ、Hz、dB、負號等技術符號清楚
- 標題/表格沒有因 fallback 導致 clipping/overflow

任何一頁 `bilingual_typography_clean=false`，不得 final delivery。

## 9. Do not ship fonts / 字體檔不可隨 Skill 散佈

Skill 只描述字體選擇與偵測規則，不應把系統或商業字體檔提交進 repository。
