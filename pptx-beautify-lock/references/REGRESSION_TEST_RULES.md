# Regression Test 回歸測試規範 / Regression Test Rules

## 目的 / Purpose

Regression Test 是最後品質閘門。它必須同時證明兩件事：

1. **內容沒有任何未授權變更。**
2. **版面品質沒有退化到不可交付。**

The output deck is valid only if both content integrity and layout quality gates pass.

## Gate A — Content Integrity / 內容完整性

必須使用 `pptx_content_lock.py verify` 或等效機制，比對：

- slide count/order
- every visible text run value
- table cell values and table structure
- chart formulas/cached values/series semantics
- media payload hashes
- image crop states
- notes text
- embedded package payloads

唯一允許結果：

```text
CONTENT_LOCK_PASS=true
```

任何差異都視為 regression failure。

## Gate B — Layout QA / 版面品質

至少檢查：

- no out-of-bounds object
- no non-positive geometry
- no severe unintended overlap
- no severe tiny-text regression
- slide count preserved
- output PPTX can be parsed successfully

若環境可 render，還必須進行逐頁 render QA。

## Gate C — Regression against baseline / 與基準比較

除了驗證絕對門檻，建議比較來源與輸出：

- `out_of_bounds`: 不得增加
- `severe_overlaps`: 不得增加
- `tiny_text`: 原則上不得增加；若來源原本很小，輸出不得更小
- `font_family_count`: 不應無理由增加
- `visual inconsistency warnings`: 不應增加

如果美化後造成更多硬錯誤，即使視覺看似更漂亮，也必須 FAIL。

## Gate D — Deliverability / 可交付性

最後輸出必須：

- 是有效 `.pptx`
- 不覆寫唯一原始檔
- 可由 PowerPoint-compatible reader 解析
- 保持原生可編輯物件為優先
- 不得用整頁圖片取代原本可編輯內容

## 建議輸出 / Recommended output

```text
REGRESSION_PASS=true
CONTENT_LOCK_PASS=true
LAYOUT_QA_PASS=true
baseline_layout_errors=8
output_layout_errors=0
baseline_layout_warnings=17
output_layout_warnings=4
```

## Fail closed / 保守失敗

只要無法證明內容一致或無法安全解析重要物件，必須：

```text
REGRESSION_PASS=false
```

不得用「看起來應該沒問題」取代驗證。
