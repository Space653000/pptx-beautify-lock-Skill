# QA Rules / 品質驗證規範

本文件定義「什麼才算可以交付」。Content Lock 的 protected semantics 仍以 [`CONTENT_LOCK.md`](CONTENT_LOCK.md) 為唯一權威來源。

## Delivery gate / 交付門檻

完整 final PPTX 必須同時通過：

1. **Content QA** — protected semantics 無未授權變更
2. **Layout QA** — structural hard errors 為 0，blocking readability warnings 不退化
3. **Visual QA** — render 後逐頁檢查全部通過
4. **Regression QA** — source-vs-output 綜合回歸通過

正式交付結果：

```text
CONTENT_LOCK_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
REGRESSION_PASS=true
DELIVERY_PASS=true
```

## Content QA

```bash
python scripts/pptx_content_lock.py verify source.pptx output.pptx
```

任何 semantic diff 都必須先修正。

## Layout QA

主要 linter：

```bash
python scripts/pptx_lint.py output.pptx --json
```

`verify_layout.py` 僅保留為舊版相容入口；新工作流以 `pptx_lint.py` 為 structural findings 的 single source of truth。

Hard errors 包含 out-of-bounds / invalid geometry。Warnings 是 heuristic，其中 tiny text 與 table density 會作為 regression 的 blocking readability signals；suspicious overlap 等需要 render 判定。

## Visual QA

詳細規範：[`RENDER_VISUAL_QA.md`](RENDER_VISUAL_QA.md)。

必須 render 全部投影片並產生 `visual_qa.json`，然後：

```bash
python scripts/visual_qa_gate.py visual_qa.json --expected-slides <N>
```

預設每頁 visual score >= 85，而且每頁八個 required boolean checks 必須全部為 true。

## Regression QA

```bash
python scripts/pptx_regression.py source.pptx output.pptx \
  --visual-qa-report visual_qa.json \
  --require-visual-qa
```

Regression 不會單純用 warning 總數判斷設計好壞；真正的視覺 heuristic 由 render QA adjudicate，避免把刻意的設計疊圖誤判成 regression。

## Repair loop

最多 3 輪：

```text
repair → content verify → lint → render → visual review
```

每輪修改後都重新驗證 Content Lock。三輪後仍有 blocking defect，就回報未解問題並停止；Content Lock 不因美觀目標而放寬。