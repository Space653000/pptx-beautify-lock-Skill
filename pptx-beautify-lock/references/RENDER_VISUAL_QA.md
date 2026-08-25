# Render Visual QA / Render 後視覺品質契約

本文件只處理一件事：**AI 必須看過美化後每一頁的實際 render，才可以宣稱「非常好看且沒有視覺瑕疵」。**

This reference defines the rendered-slide review required before a fully qualified delivery.

## 何時必讀 / Trigger

當環境具備任何 PPTX render 能力時，Design Agent 完成後必須讀本文件並執行完整 Visual QA。

## Render 優先順序 / Render preference

使用環境中已存在且可信任的 renderer；不要為了遵守名稱而改用較差的工具。

1. **Microsoft PowerPoint native render**（Windows/Office automation，可用時優先，最接近最終播放）
2. **宿主既有的 PowerPoint/Slides renderer**（例如 agent harness 已提供的 render/thumbnail 工具）
3. **LibreOffice headless** 或其他可重現的 PPTX renderer

必須 render **全部投影片**，不能只抽查首頁或問題頁。

## Visual QA 每頁必查 / Required checks per slide

每一頁都必須明確判定以下八項：

- `no_unintended_overlap`：沒有非刻意物件/文字重疊
- `no_clipping_or_overflow`：沒有文字、表格、圖表被裁切或溢出
- `content_visible`：來源內容沒有因層級、透明度、遮罩、z-order 而看不到
- `text_readable`：投影/螢幕閱讀尺寸合理
- `hierarchy_clear`：標題、重點、正文、次要資訊有清楚層級
- `alignment_consistent`：對齊、邊界、grid 不凌亂
- `tables_charts_readable`：表格與圖表標籤、欄列、legend/axis 清楚
- `style_consistent`：與整份 deck 的字體、色彩、spacing、元件語言一致

## 分數 / Score

每頁給 `0–100` 的視覺品質分數。預設交付門檻：**每頁 >= 85**。

分數只是輔助；八個 boolean checks **全部必須為 true**，不能用高分抵銷 clipping 或 unreadable text。

## visual_qa.json 格式

```json
{
  "schema": 1,
  "slide_count": 2,
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
        "style_consistent": true
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

必須得到：

```text
VISUAL_QA_PASS=true
```

## Repair loop / 修復循環

最多自動跑 3 輪：

```text
render → review every slide → repair visual defects → content verify → render again
```

每一輪修改後都要重新執行 Content Lock verification；不能假設視覺修復不會碰到內容。

若第 3 輪仍有 blocking visual defect：

- 保留 CONTENT LOCK
- `VISUAL_QA_PASS=false`
- 不得宣稱 fully qualified delivery
- 回報仍未解決的頁碼與原因

## Final regression command

完整品質交付建議使用：

```bash
python scripts/pptx_regression.py source.pptx output.pptx \
  --visual-qa-report visual_qa.json \
  --require-visual-qa
```

只有同時得到：

```text
CONTENT_LOCK_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
REGRESSION_PASS=true
DELIVERY_PASS=true
```

才可以宣稱內容鎖定且視覺品質已完整驗證。