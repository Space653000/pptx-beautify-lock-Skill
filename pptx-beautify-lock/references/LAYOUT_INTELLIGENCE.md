# Layout Intelligence / 空間構圖與版面骨骼契約

> v0.5 adds a stricter rule: **沒有重疊 ≠ 排版正確；排版正確 ≠ 好看。**
>
> A slide is not qualified merely because every object fits inside the canvas.

本文件與 `CONTENT_LOCK.md`、`THEME_DISCOVERY.md` 並列為 Design Agent 的前置契約。

## 1. Six-layer anatomy / 六層投影片解剖

設計順序固定：

1. **Soul / 靈魂** — source brand、theme、tone、內容任務、page-role pattern。
2. **Frame / 框架** — safe area、full-bleed terrain、master/layout brand chrome、header/footer reservation。
3. **Skeleton / 骨骼** — grid rails、columns、rows、baselines、gutters、spacing rhythm、visual center of gravity。
4. **Joints / 關節** — title/status/summary/table/chart/footer 彼此的 proximity、reading order、parent-child relationship。
5. **Limbs / 肢體** — 真正的文字、表格、圖表、圖片、label、badge、callout。
6. **Skin / 外觀** — font、size、color、fill、border、shadow、tint、radius、decorative treatment。

**不得從 Skin 開始。** 先套漂亮字體、卡片和深色區塊，但沒有建立 Skeleton，視為 design failure。

## 2. Source Spatial Discovery / 設計前先讀空間 DNA

在任何重排之前：

1. Render source 全部頁面。
2. 每頁分類 slide role：`cover / agenda / section / data / comparison / image-led / closing / other`。
3. 找出 source 的 persistent anchors：
   - logo / company name / department identity
   - recurring header/footer
   - copyright / confidentiality
   - page number / status / date zones
   - full-slide branded background image
4. 找出 content anchors：title、subtitle、summary、table、chart/image groups。
5. 標記 **brand-safe zones** 與 **content-safe zones**。
6. 找出 source repeated rails：left edge、right edge、centerline、table/chart top rail、footer baseline。
7. 建立 reading order：第一眼 → 第二眼 → 第三眼。

如果品牌識別被烘焙進 full-slide layout/master image，不能因為 XML 裡沒有獨立 logo shape 就把它當空白背景。**Render 是權威。**

## 3. Anchor classes / 物件四種錨點

### A. Protected semantic content

內容可移動但不可改語意。Content Lock 永遠優先。

### B. Brand chrome / 品牌地形

Logo、公司名、部門識別、品牌線條、footer、background hero art。預設視為必須尊重的視覺地形。

- 不要蓋住。
- 不要把主要內容硬塞進品牌識別上。
- 不要用新增大面積 opaque panel 讓品牌背景失去作用。
- 若 source 本身就是以 panel 承載內容，可沿用其位置邏輯。

### C. Structural anchors / 骨架錨點

Title rail、table rail、chart pair rail、summary rail、footer baseline。可以重設，但同一頁內必須形成一致系統；同角色跨頁應重複。

### D. Decoration / 裝飾

只有在改善 hierarchy、grouping、navigation 或 brand continuity 時才存在。否則刪除。

## 4. Grid rules / Grid 不是模板，是關係

不強制每份 deck 都用相同 12-column template。優先從 source 找既有 rails；若 source 太亂，再建立新的少量 rails。

### Required relationships

- 同群組文字框，至少共用一條主要 left/right/center rail。
- 同角色 peer visuals（例如 L/R charts）應共用 top rail、bottom rail，尺寸相同或有可解釋比例。
- chart title 應對齊 chart plot/object edge，而不是漂浮。
- table + summary 若同列，top edge 應視覺對齊。
- title + status + logo 不得互搶同一個 top band。
- footer 必須有自己的 reserve zone；正文不侵入。

### Tolerance guidance

以下是機器 QA 的 conservative guidance，不是創意禁令：

- peer top drift：`<= 2.5%` slide height
- peer width/height drift：`<= 4.5%` slide dimension
- normal content safe margins：通常約 `3–6%`，full-bleed 元素例外
- spacing 應使用少數重複 gap，而不是每一段不同距離

若刻意打破 grid，必須在 render QA 能清楚證明它提升構圖，而不是 accidental drift。

## 5. Spacing rhythm / 留白必須有節奏

Whitespace 是 active structure。

- group internal gap < group-to-group gap
- 標題與副標應比標題與下一區塊更靠近
- summary/table/charts 之間使用一致的 vertical rhythm
- 不要把所有內容擠在上半部、下半部留下無理由的大洞
- 也不要為了填滿空白，把 chart/table 無限制放大

**空白的目的：分組、導視、平衡、呼吸。**

## 6. Reading order / 觀看順序

每頁必須能在 3 秒內說出：

1. 這頁是什麼？
2. 第一個該看哪裡？
3. 下一個該看哪裡？

閱讀順序由位置、size、contrast、proximity 共同建立；不能只靠字級。

## 7. Slide-role composition / 不同頁型不同骨架

### Cover

- source brand identity 優先。
- title 放入已有 negative space / quiet zone。
- 不以巨大 opaque rectangle 覆蓋 source hero/department identity，除非 source 本來就如此。
- date / subtitle 與 title group 有明確關係，不可孤立漂浮。
- **不得為美觀更改 date string representation**；例如 source `20260819` 不得自動改成 `2026/08/19`。

### Agenda / Contents

- 需要清楚 scanning path。
- 避免 master sample text 與真正內容競爭。
- row/step spacing 一致。

### Section

- 允許較強的 whitespace 與 scale contrast。
- 不要把 section page 當 data page 填滿。

### Dense technical / data slide

建議順序：

```text
header / title / status
↓
summary + table / key parameters
↓
chart/image row(s)
↓
footer brand zone
```

- L/R、Before/After、A/B chart 必須先視為 peer system。
- 同一 row 的 peer charts 等寬、等高、共用 top/bottom rail，除非資料本身需要不同 aspect。
- 表格 header hierarchy 一致，grid/borders 不應比內容更搶眼。
- data slide 若主要內容在頁高約 75% 前就結束、下方仍有大面積可用 body space，應進入 vertical-balance review。

### Closing

保留品牌 ending identity。不要讓 `Thank you` 與 template `THANK YOU` 重複競爭。

## 8. The MEC regression examples / 這次 MEC 問題必須被抓到

v0.5 的規則必須能把以下情況至少升級成 review blocker：

1. branded full-slide cover 上，原本透明 title box 被新增為大面積 solid panel；即使沒有蓋到文字，也可能壓住 MEC / brand identity。
2. data slide 的 title、updated badge、PEGATRON zone、summary、table 沒有形成同一 top-band system。
3. L/R charts 雖然沒有互相 overlap，但 chart headings、chart tops、sizes 或 gutters 不一致。
4. 主要資料全部擠在上半部，下方留下大量無理由空白，整頁重心失衡。
5. decorative accent/fill 沒有服務 hierarchy，只是在『加設計感』。

## 9. Machine checks vs visual judgement / 機器與視覺各負責什麼

### `pptx_layout_intelligence.py`

只抓高信心結構問題：

- foreground solid-fill occlusion
- branded/full-bleed background 上新增大型 solid content region → warning + render review
- peer visual rail/size drift
- data-body top-heavy risk

### `composition_qa_gate.py`

要求逐頁 render review 評估真正美感骨架：

- brand chrome
- grid alignment
- peer alignment
- spacing rhythm
- reading order
- visual balance
- role fit
- decorative restraint

Machine geometry **不能取代 vision review**；vision review 也不能跳過 machine guards。

## 10. Exit rule / v0.5 完成規則

完全合格必須：

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
SPATIAL_QA_PASS=true
VISUAL_QA_PASS=true
COMPOSITION_QA_PASS=true
REGRESSION_V05_PASS=true
DELIVERY_V05_PASS=true
```

任何一項 false：不得宣稱 v0.5 final。
