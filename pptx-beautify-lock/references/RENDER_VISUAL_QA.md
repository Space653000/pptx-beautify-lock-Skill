# Render Visual QA / Render 後視覺品質契約

本文件只處理一件事：**AI 必須看過美化後每一頁的實際 render，才可以宣稱「非常好看且沒有視覺瑕疵」。**

This reference defines the rendered-slide review required before a fully qualified delivery.

## 何時必讀 / Trigger

當環境具備任何 PPTX render 能力時，Design Agent 完成後必須讀本文件並執行完整 Visual QA。

同時必讀：

- [`THEME_DISCOVERY.md`](THEME_DISCOVERY.md)
- [`TYPOGRAPHY_BILINGUAL.md`](TYPOGRAPHY_BILINGUAL.md)

## Render 優先順序 / Render preference

1. Microsoft PowerPoint native render
2. 宿主既有 PowerPoint/Slides renderer
3. LibreOffice headless 或其他可信 renderer

必須 render **全部投影片**，不能只抽查首頁或問題頁。

## Source-vs-final comparison / 來源與完成版對照

若來源可 render，應同時 render source 與 final，至少逐頁確認：

- final 仍是 source 的升級版，而不是無授權 rebrand
- light/dark/mixed canvas pattern 未被翻轉
- 真正主標題/副標仍完整可見
- generic placeholder/sample text 沒有洩漏
- 繁中與英文都使用穩定、協調的 glyph/font rendering

對 title/section/data pages 不得只看首頁判斷整份 theme。

## Visual QA 每頁必查 / Required checks per slide

每一頁都必須明確判定以下十一項：

- `no_unintended_overlap`
- `no_clipping_or_overflow`
- `content_visible`
- `text_readable`
- `hierarchy_clear`
- `alignment_consistent`
- `tables_charts_readable`
- `style_consistent`
- `no_template_placeholder_artifacts`
- `theme_fidelity_preserved`
- `bilingual_typography_clean`

### `no_template_placeholder_artifacts=false` examples

- 真正標題存在，但仍顯示 `presentation title`
- `Click to add title` / `Click to add subtitle` 被 render
- template sample text 與真正內容重疊
- 修 overlap 時錯刪真正內容，只留下 placeholder

### `theme_fidelity_preserved=false` examples

- source 白底/light technical deck，被改成大面積深藍/黑底
- source dark deck 被改成 white corporate deck
- source 原有品牌 hue 被無關的新主色取代
- source 的 semantic red/green 被誤當成整份 deck brand color
- source 是 mixed page-role system，但 final 把所有頁強制統一成單一 dark/light canvas

### `bilingual_typography_clean=false` examples

- 繁中缺字、tofu、□
- 英文好看但繁中掉成不可控 fallback 字體
- 同一標題中英文 baseline/weight 明顯不協調
- mixed CJK/Latin run 套 Latin-only font，造成字體跳動
- `% / σ / Hz / dB / 負號 / 數字` 等技術符號 render 異常
- fallback 導致 clipping/overflow

任何一項 false，都不得 final delivery。

## 分數 / Score

每頁給 `0–100` 視覺品質分數。預設門檻：**每頁 >= 85**。

分數不可抵銷任何 boolean defect。

## visual_qa.json schema 3

```json
{
  "schema": 3,
  "slide_count": 1,
  "render_engine": "Microsoft PowerPoint",
  "reviewer": "AI vision reviewer",
  "overall_pass": true,
  "slides": [
    {
      "slide": 1,
      "score": 92,
      "checks": {
        "no_unintended_overlap": true,
        "no_clipping_or_overflow": true,
        "content_visible": true,
        "text_readable": true,
        "hierarchy_clear": true,
        "alignment_consistent": true,
        "tables_charts_readable": true,
        "style_consistent": true,
        "no_template_placeholder_artifacts": true,
        "theme_fidelity_preserved": true,
        "bilingual_typography_clean": true
      },
      "notes": ""
    }
  ]
}
```

驗證：

```bash
python scripts/visual_qa_gate.py visual_qa.json --expected-slides <N>
```

必須：

```text
VISUAL_QA_PASS=true
```

## Repair loop / 修復循環

最多自動跑 3 輪：

```text
source render/profile
→ final render
→ review every slide
→ repair
→ Content Lock verify
→ Theme Guard compare
→ render again
```

### Theme repair priority / 色系修復

若 source light、candidate dark：

1. 保留所有真正內容。
2. 回到 source canvas polarity。
3. 從 source theme/accent 建立較精緻的 tint/shade，而不是選新主色。
4. 再 render source/final 對照。
5. 再跑 Content Lock + Theme Guard。

### Placeholder repair priority / Placeholder 修復

1. 保留真正來源內容。
2. 不修改受保護 master/layout semantics。
3. 優先使用 content-safe layout / placeholder instance handling。
4. render 確認 artifact 消失。
5. 再跑 Content Lock。

### Typography repair priority / 字體修復

1. 確認目標平台實際存在的 CJK-safe font。
2. mixed CJK/Latin 優先改回單一 bilingual-safe family。
3. 若使用中英分字族，只對 pure-Latin run 套 Latin font。
4. render 檢查繁中、英文、數字與技術符號。
5. 再跑 Content Lock。

若第 3 輪仍有 blocking defect：

- 保留 Content Lock
- `VISUAL_QA_PASS=false`
- 不得 fully qualified delivery
- 回報未解決頁碼與原因

## Final regression command

```bash
python scripts/pptx_regression.py source.pptx output.pptx \
  --visual-qa-report visual_qa.json \
  --require-visual-qa
```

Fully qualified final 必須同時：

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
REGRESSION_PASS=true
DELIVERY_PASS=true
```
