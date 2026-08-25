# Render Visual QA + Composition QA / Render 後雙層視覺品質契約

v0.5 將「視覺沒有壞掉」與「構圖真的好看」拆成兩層，避免 v0.4 的 false pass。

## Why two gates / 為什麼拆兩層

### Visual QA

回答：

- 有沒有 overlap / clipping / overflow？
- 內容是否可見、可讀？
- placeholder 是否洩漏？
- theme / bilingual typography 是否正常？

### Composition QA

回答更嚴格的問題：

- 品牌地形有沒有被新物件壓住？
- grid rails 是否一致？
- peer components 是否對齊、等尺寸？
- spacing 是否有節奏？
- reading order 是否清楚？
- visual balance 是否自然？
- 這個 layout 是否適合該 slide role？
- 裝飾是否真的有作用？

**Visual QA PASS 不代表 Composition QA PASS。**

## Render preference

1. Microsoft PowerPoint native render
2. 宿主 PowerPoint/Slides renderer
3. LibreOffice headless 或其他可信 renderer

Source 與 final 都要 render **全部投影片**。

## Source-vs-final evidence / 必須對照來源

每頁 review 都要看 source + final，而不是只看 final。尤其要確認：

- source brand logo / department identity / footer / hero art
- light/dark/mixed page-role pattern
- title/date/status 的來源角色
- source negative space / quiet zones
- technical chart/table 的 peer relationships

品牌識別若已烘焙在 full-slide layout image，仍算 visual anchor。

## Existing Visual QA schema 3

現有 `visual_qa.json` schema 3 保留，用於 technical visual defects：

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

驗證：

```bash
python scripts/visual_qa_gate.py visual_qa.json --expected-slides <N>
```

## New Composition QA schema 1

v0.5 另外必須產生 `composition_qa.json`。

每頁 checks：

- `brand_chrome_respected`
- `content_not_occluded`
- `grid_alignment_coherent`
- `peer_components_aligned`
- `spacing_rhythm_coherent`
- `reading_order_clear`
- `visual_balance_coherent`
- `slide_role_composition_fit`
- `decorative_elements_earn_their_place`

每頁 scores：

- `hierarchy`
- `alignment`
- `spacing`
- `balance`
- `brand_fidelity`
- `restraint`
- `data_legibility`

預設：每個 dimension `>= 88`，`composition_score >= 90`。任何 boolean false 都不能被高分抵銷。

此外每頁必須提供 evidence：

- `source_comparison`
- `grid_rails`
- `reading_order`
- `brand_anchors`

範例：

```json
{
  "schema": 1,
  "slide_count": 1,
  "render_engine": "Microsoft PowerPoint",
  "reviewer": "AI vision reviewer",
  "overall_pass": true,
  "slides": [
    {
      "slide": 1,
      "composition_score": 92,
      "checks": {
        "brand_chrome_respected": true,
        "content_not_occluded": true,
        "grid_alignment_coherent": true,
        "peer_components_aligned": true,
        "spacing_rhythm_coherent": true,
        "reading_order_clear": true,
        "visual_balance_coherent": true,
        "slide_role_composition_fit": true,
        "decorative_elements_earn_their_place": true
      },
      "scores": {
        "hierarchy": 92,
        "alignment": 94,
        "spacing": 91,
        "balance": 90,
        "brand_fidelity": 95,
        "restraint": 93,
        "data_legibility": 92
      },
      "evidence": {
        "source_comparison": "source and final cover reviewed side-by-side",
        "grid_rails": ["title-left", "brand-right", "footer-baseline"],
        "reading_order": ["title", "subtitle", "date"],
        "brand_anchors": ["PEGATRON", "MEC identity", "copyright"]
      },
      "notes": ""
    }
  ]
}
```

驗證：

```bash
python scripts/composition_qa_gate.py composition_qa.json --expected-slides <N>
```

必須：

```text
COMPOSITION_QA_PASS=true
```

## Specific false cases / 明確不合格例

### Brand chrome

- MEC/PEGATRON cover 的 title panel 壓過 department identity / hero art / tagline
- 把 full-slide brand background 當一般圖片隨意蓋住
- footer brand/copyright 被 body 侵入

### Grid / peer alignment

- L/R charts top edge 不同
- 同 role charts 尺寸不一致卻沒有內容理由
- chart heading 與 chart left edge 不對齊
- summary/table 應同列卻 top rail 漂移

### Spacing / balance

- title、status、table、charts 都擠在上半部，下方留下巨大無理由空白
- 同一頁每個 gap 都不同，沒有節奏
- 填滿空白導致 chart/table 過大或侵入 footer

### Decoration

- 新增 card/panel/line/shadow 只因為「看起來科技」
- decorative fill 沒有改善 hierarchy/grouping/navigation/brand continuity
- 大面積 panel 雖沒有文字 overlap，卻破壞 source visual identity

## Three-second test / 3 秒測試

Composition reviewer 每頁應能回答：

1. 這頁是什麼？
2. 第一眼看哪裡？
3. 第二眼看哪裡？
4. 哪些物件是同一組？

答不出來，`reading_order_clear=false` 或 `hierarchy` 分數不足。

## Repair loop

最多 3 輪：

```text
source render
→ candidate render
→ Spatial QA
→ Visual QA
→ Composition QA
→ repair rails / groups / whitespace / balance
→ Content Lock + Theme Guard
→ render again
```

若第 3 輪仍有 blocking defect：fail closed。

## v0.5 final command

```bash
python scripts/pptx_regression.py source.pptx output.pptx \
  --visual-qa-report visual_qa.json --require-visual-qa \
  --composition-qa-report composition_qa.json --require-composition-qa
```

完全合格：

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
SPATIAL_QA_PASS=true
VISUAL_QA_PASS=true
COMPOSITION_QA_PASS=true
REGRESSION_V05_PASS=true
DELIVERY_V05_PASS=true
```
