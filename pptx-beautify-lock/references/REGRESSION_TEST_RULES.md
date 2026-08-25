# Regression Test / 回歸測試規範

Regression Test 是最後的**品質證明**，不是單純重新跑一次 Linter。

## Gate A — Content Integrity

以 [`CONTENT_LOCK.md`](CONTENT_LOCK.md) 為 protected-semantics 唯一定義，使用：

```bash
python scripts/pptx_content_lock.py verify source.pptx output.pptx
```

必須：

```text
CONTENT_LOCK_PASS=true
```

目前 verifier 會保守檢查至少：slide order/count、visible/master/SmartArt text、Office Math、table values/merge topology、chart text/data/formulas/caches、media payload/crop、notes、comments/annotations、accessibility text、hyperlinks/actions/external targets、hidden slide state、transition/timing semantics 與 embedded payloads。

## Gate B — Structural Layout QA

使用 `pptx_lint.py` 比較 baseline/output。

Hard requirements：

- final `lint_errors == 0`
- hard errors 不得比 source 增加
- `tiny-text` / `table-density-risk` 等 blocking readability warnings 不得比 source 惡化
- output 可正常解析

## Gate C — Visual QA

幾何 heuristic 無法判斷「刻意疊圖」與「真的撞版」，也無法可靠證明文字實際 render 沒有 clipping/overflow。

因此完整交付必須依 [`RENDER_VISUAL_QA.md`](RENDER_VISUAL_QA.md) render 全部頁面並建立 `visual_qa.json`。

Visual QA 會 adjudicate suspicious overlap、dense text、cross-slide style 等 heuristic findings。

## Gate D — Delivery

完整命令：

```bash
python scripts/pptx_regression.py source.pptx output.pptx \
  --visual-qa-report visual_qa.json \
  --require-visual-qa
```

正式 final deck 必須：

```text
CONTENT_LOCK_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
REGRESSION_PASS=true
DELIVERY_PASS=true
```

其中：

- `REGRESSION_PASS`：本次要求的 structural + visual regression gate 通過
- `DELIVERY_PASS`：Content + Layout + Visual 三類品質證據全部齊全

若沒有 renderer/visual review，最多只能產生 structural candidate；不得以 `REGRESSION_PASS` 的部分結果冒充完整 `DELIVERY_PASS`。

## Fail closed

以下任一狀況直接 FAIL：

- protected semantic 無法安全驗證
- embedded/media payload 不一致
- source/output 重要內容關係無法解析
- final hard layout error > 0
- required visual QA 缺頁、缺 check、低於門檻或 overall fail

不要用「看起來差不多」取代證據。