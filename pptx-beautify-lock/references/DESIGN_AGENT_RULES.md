# Design Agent 規範 / Design Agent Rules

## Role / 角色

Design Agent 只負責視覺重構，但 v0.5 明確規定：**視覺重構必須先建立版面骨骼，不能先套樣式。**

完整前置契約：

- [`CONTENT_LOCK.md`](CONTENT_LOCK.md)
- [`THEME_DISCOVERY.md`](THEME_DISCOVERY.md)
- [`TYPOGRAPHY_BILINGUAL.md`](TYPOGRAPHY_BILINGUAL.md)
- [`LAYOUT_INTELLIGENCE.md`](LAYOUT_INTELLIGENCE.md)

## v0.5 design order / 設計順序

```text
Soul / source visual DNA
→ Frame / brand terrain + safe zones
→ Skeleton / rails + grid + spacing rhythm
→ Joints / grouping + reading order
→ Limbs / text + table + chart + image placement
→ Skin / typography + color + fills + borders
```

**禁止反過來。** 若 AI 先加 navy panel、cards、gradient、漂亮字體，再想辦法把內容塞進去，視為錯誤流程。

## 1. Source render first / 來源 render 先於設計

若可 render，必須 render source 全頁。至少每頁辨識：

- slide role
- brand chrome / logo / footer / department identity
- full-bleed background terrain
- title/content/footer safe zones
- recurring alignment rails
- visual center of gravity
- intended reading order

品牌識別若烘焙在 layout/master full-slide image 中，也必須視為真實視覺內容。不能因為 `slide.shapes` 看不到獨立 logo 就把該區當空白。

## 2. Source theme first / Beautify ≠ Rebrand

- source light → final 保持 light
- source dark → final 保持 dark
- source mixed → 保留 page-role pattern
- source 有品牌主色 → 沿用 hue family

semantic red/green（limit、pass/fail）不能被誤當 brand primary。

## 3. Skeleton first / 骨骼優先

每頁先決定少量 rails：

- outer safe margins
- title rail
- content columns
- summary/table top rail
- chart/image row rails
- footer baseline

同角色物件必須對齊到共同 rails。Keynote-style precision 是概念參考：edge、center、equal size、equal spacing 都應有明確關係，而不是靠肉眼隨意拖放。

### Peer components

L/R、Before/After、A/B、四象限等 peer visuals：

- 同列優先等高等寬
- 共用 top/bottom rail
- labels 對齊各自 visual left edge
- gutter 一致
- 若 aspect ratio 必須不同，需要由內容本身解釋，不能只是 layout drift

## 4. Brand terrain / 品牌地形不可被新設計壓住

特別是 branded cover：

- 保留 source logo / department identity / footer / hero art 的呼吸空間
- 大面積 opaque title panel 不是預設解法
- 若要增加 panel，先確認它落在 source quiet zone，而不是覆蓋品牌主視覺
- title、subtitle、date 應構成一個 group，不要讓 date 漂在無關位置
- 不為了排版改寫 date string：`20260819` 不能自行變 `2026/08/19`

## 5. Spacing rhythm / 留白有階層

Whitespace 是骨骼的一部分：

- 同組 internal gap 較小
- 組與組之間 gap 較大
- 重複頁型使用重複 gap
- 不把 dense content 全部擠在上半部、底部留大洞
- 不為填滿空白而把 chart/table 無限制放大

如果一頁看起來「位置怪」，先查 rails、grouping、vertical rhythm、visual balance，不要先換顏色。

## 6. Hierarchy and reading order / 階層與視線順序

每頁必須讓 reviewer 能在約 3 秒說出：

1. 這頁是什麼？
2. 第一眼看哪裡？
3. 第二眼看哪裡？
4. 哪些是同一組？

位置、字級、contrast、proximity 共同建立 hierarchy；不能只靠粗體與大字。

## 7. Restraint / 美感不是裝飾量

優先移除無作用的 framing、cards、lines、badges、shadows。Decorative element 必須至少服務其中一項：

- hierarchy
- grouping
- navigation
- brand continuity

否則不要加。

## 8. Dense technical/data slides / 工程資料頁

POWER / THD / HOHD 這類頁面，預設先建立：

```text
header/title/status band
↓
summary + table band
↓
peer chart/image band
↓
footer brand zone
```

要求：

- title/status/logo 各有自己的 anchor，不互搶
- summary/table 視覺 top edge 對齊
- 同 row charts 共用尺寸與 rails
- chart headings 貼著各自 chart system
- table border/grid 要退居內容之後
- 盡量使用完整 body 高度取得平衡，但不能侵入 footer

## 9. Bilingual typography / 繁中英文兼容

- mixed CJK/Latin 優先 bilingual-safe family
- pure Latin 才可使用 Latin-specific family
- `% / σ / Hz / dB / 負號 / 數字` 技術符號要 render 正常
- glyph fallback 造成 baseline、overflow、字重跳動都要修

## 10. Placeholder vs brand chrome / 不要把品牌當 placeholder

Generic template prompts（`presentation title`, `Click to add title`）應停用；但品牌 logo、department identity、copyright、hero art 不是 placeholder。

若 source 真正內容與 master artifact 衝突：

1. 保留真正內容
2. 辨識 artifact vs brand chrome
3. 用 content-safe layout/visibility/geometry 解決
4. render source/final 比對
5. 再跑 Content Lock

## 11. Repair loop / 修復循環

最多 3 輪：

```text
source render + theme + layout discovery
→ design
→ Content Lock
→ Theme Guard
→ Spatial QA
→ render all slides
→ Visual QA
→ Composition QA
→ repair
```

若 Spatial QA 出現 warning，Composition QA 必須直接針對該頁證明 brand / balance / grid 沒問題；不能忽略 warning 後自行給高分。

## 12. Exit gate / v0.5 完成門檻

Design Agent 不得用「看起來不錯」當結論。完全合格需要：

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
SPATIAL_QA_PASS=true
VISUAL_QA_PASS=true
COMPOSITION_QA_PASS=true
REGRESSION_V05_PASS=true
DELIVERY_V05_PASS=true
```

任何 false：candidate 不是 v0.5 final。
