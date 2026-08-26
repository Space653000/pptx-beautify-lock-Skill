# Regression Guardrails v0.6.1 / 嚴格回歸防護

這份規則是 v0.6.1 的 release blocker。目的不是讓單頁看起來更好，而是避免「修 A 壞 B、修 B 壞 C」。

## 1. Full-deck invariant / 全簡報不變量

任何單頁、單表、單字型、單 placeholder 修正之後，都必須重新檢查 **整份簡報全部頁面**。局部成功不等於 release success。

```text
repair slide N
→ rerender ALL slides
→ rerun ALL structural/content/theme guards
→ compare against last known-good full-deck baseline
→ only then mark the repair as accepted
```

如果第 N 頁變好，但任何先前已通過的頁面變差：該 repair 必須回滾或繼續修正，不能交付。

## 2. Three-pass release review / 三輪完整審查

Launcher/production release 至少執行三輪全頁審查：

1. **Soul / 靈魂** — source identity、theme、brand terrain、slide role、audience。
2. **Skeleton + Muscle / 骨骼＋肌肉** — rails、grid、alignment、peer systems、tables、charts、spacing、reading order、content density。
3. **Skin + Regression / 表皮＋回歸** — typography、font portability、color craft、micro-spacing、placeholder artifacts、render fidelity、all-slides regression。

每一輪都必須覆蓋所有 slides；不得抽樣。

## 3. Empty placeholder purge / 空 placeholder 清除

如果 placeholder 沒有 protected content，而且 final render 仍可見/可攔截點擊/會造成 layout collision：應移除或隱藏。

Hard failures：

- 空 title/body placeholder 與真正標題/副標重疊。
- `presentation title`、`Event name or presentation title`、`Speaker name or subtitle`、`Click to add...` 等 template/example artifacts 出現在 final render。
- master/layout artifact 與有效內容競爭焦點。

不得為了消除 placeholder 而刪除真正 source content。

## 4. Font portability gate / 字型可攜性

PowerPoint 最終交付不能只在生成環境看起來正常。

### Required

- 繁中＋英文混排必須使用 Windows/Office 可安全顯示的字體鏈。
- 若使用非標準字型，必須證明目標環境可用或嵌入字型合法可行；否則改用安全 fallback。
- 不能只檢查 XML 的 `font.name`；必須用實際 PowerPoint/LibreOffice/可比 renderer 檢查 final render。
- 發現 serif fallback、巨大字體、裁切、行高變形、字寬改變導致換行時：FAIL。

預設 conservative fallback：

```text
Traditional Chinese: Microsoft JhengHei / Noto Sans CJK TC where target availability is proven
Latin: Aptos / Microsoft JhengHei compatible mixed runs
```

不要因追求漂亮而使用會在客戶 Windows/PowerPoint silently fallback 的脆弱字型。

## 5. Sibling data-slide parity / 同族資料頁一致性

若來源存在 POWER / THD / HOHD、L/R、6σ/5σ/4σ 或任何語意同族頁面，Design Agent 必須先建立 family system，再處理個別頁。

同族頁預設共享：

- title rail
- status/date rail
- summary card geometry
- table header/body style
- table border/fill hierarchy
- table font hierarchy and padding
- chart title relationship
- L/R chart peer alignment
- footer/brand reservations
- spacing rhythm

資料結構不同（例如 HOHD 只有 3 個 frequency columns）可以改變 table width/column count，但**視覺語法不能退回原始醜表格**。

若 POWER 已美化，但 THD/HOHD 仍使用舊表格語言：FAIL。

## 6. Brand terrain isolation / 品牌地形隔離

Cover 或 branded master 頁尤其容易被局部修正破壞。

- 不用大面積 panel 蓋住 logo、department identity、tagline 或 baked-in master imagery。
- 新增的標題區必須避開 source brand anchors。
- Header status、logo、title 必須有清楚 visual ownership，不互搶同一 band。
- 修資料頁後必須再檢 cover / agenda / closing，因為全域字型或 master 修改可能造成回歸。

## 7. Native preview reality check / 真實預覽檢查

在 Windows/Office 交付情境中，至少要有一輪針對實際 Office-compatible render 的檢查。若 automated renderer 與使用者看到的 PowerPoint 預覽不同，**使用者實際 PowerPoint render 優先**。

不得用「我們的 PNG 看起來正常」否定使用者在 PowerPoint 中看到的 clipping / fallback / overlap。

## 8. Repair transaction / 修正交易

每次 repair 應視為 transaction：

```text
baseline full-deck fingerprints
→ apply minimal repair
→ content verify
→ theme verify
→ full render
→ full-deck visual/composition/jury review
→ compare previously passing slides
→ commit repair only if no regression
```

如果不知道某個改動會不會影響其他頁：先在副本測試，不直接修改唯一 candidate。

## 9. Release criteria

除了 v0.6 原有 Gate，v0.6.1 production workflow 另要求：

```text
EMPTY_PLACEHOLDER_PASS=true
FONT_PORTABILITY_PASS=true
SIBLING_STYLE_PARITY_PASS=true
FULL_DECK_REGRESSION_PASS=true
THREE_PASS_REVIEW_PASS=true
```

這五項任一無法證明：不宣稱 production final。
