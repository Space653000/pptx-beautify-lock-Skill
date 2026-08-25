# QA RULES / 品質驗證規範

## 交付門檻 / Delivery gate

最終檔必須同時通過：

1. **Content QA / 內容驗證**
2. **Layout QA / 幾何版面驗證**
3. **Visual QA / Render 後視覺驗證**

缺一不可；若環境缺少 render 能力，必須明確說明該限制，不得假裝已完成視覺驗證。

## 1. Content QA / 內容驗證

Run:

```bash
python scripts/pptx_content_lock.py verify source.pptx output.pptx
```

Mandatory result:

```text
CONTENT_LOCK_PASS=true
```

任何差異都必須先修正。

## 2. Layout QA / 版面驗證

Run:

```bash
python scripts/verify_layout.py output.pptx
```

必查：

- shapes outside slide boundary / 物件超出投影片
- suspicious unintended overlaps / 疑似非預期重疊
- zero/negative geometry / 異常尺寸
- extremely small text / 過小文字

注意：程式只能找「疑似」問題。合法的背景、裝飾、群組或疊圖可能產生 false positive，因此仍需 visual QA。

## 3. Visual QA / 視覺驗證

如果環境能 render PPTX，必須 render 全部頁面並逐頁檢查。

Score target:

| Metric | Target |
|---|---:|
| Content fidelity | 100% |
| Unintended overflow | 0 |
| Unintended clipping | 0 |
| Out-of-bounds objects | 0 |
| Alignment | >= 95/100 |
| Typography | >= 90/100 |
| Spacing | >= 90/100 |
| Visual hierarchy | >= 90/100 |
| Table readability | >= 90/100 |
| Cross-slide consistency | >= 90/100 |
| Overall design quality | >= 90/100 |

## Repair loop / 自動修復循環

建議最多 3 輪：

```text
redesign → render → inspect → repair → verify content
```

若 3 輪後仍無法達標，保留內容鎖定，回報剩餘視覺風險，不得用改內容換取通過。

## Final report / 最終報告

建議至少輸出：

```text
CONTENT_LOCK_PASS=true|false
LAYOUT_QA_PASS=true|false
VISUAL_QA_PASS=true|false|unavailable
slides_checked=N
content_differences=N
layout_warnings=N
```
