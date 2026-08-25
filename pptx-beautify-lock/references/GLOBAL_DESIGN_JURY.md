# Global Design Jury / 世界級投影片評審契約

> v0.6 的目標不是模仿任何公司或顧問品牌的外觀，而是把一線設計與溝通團隊對 **Purpose、Hierarchy、Simplicity、Craft、Executive Communication、Technical Focus** 的品質要求轉成可驗證的 PowerPoint 交付門檻。
>
> **A world-class deck is not a template. It is a disciplined decision system.**

本文件與 `CONTENT_LOCK.md`、`THEME_DISCOVERY.md`、`LAYOUT_INTELLIGENCE.md` 並列為 v0.6 final 的權威契約。

## 1. What “world-class” means / 世界級不是什麼

世界級 **不是**：

- Apple-like 白底大字
- NVIDIA-like 黑底螢光色
- consulting-like 藍色 action-title 模板
- 全頁 rounded cards
- 全頁 glassmorphism / gradient
- 所有品牌被洗成同一個「AI 科技風」

世界級 **是**：

1. **Purpose** — 一頁只要一眼就知道這頁的任務。
2. **Hierarchy** — 第一眼、第二眼、第三眼由 order / spacing / contrast / scale 建立，而不是靠裝飾。
3. **Simplicity** — 不是少，而是剛剛好；每個元素都必須有存在理由。
4. **Craft** — X/Y、baseline、gutter、line length、字重、色彩、圖表比例、表格密度都經過刻意決策。
5. **Executive Communication** — 高階讀者能快速判斷：這頁是什麼、重要在哪、下一步該看哪裡。
6. **Technical Focus** — 密集工程/資料頁仍能讓數據成為主角，scaffolding 退到背景，comparisons 清楚。
7. **Source Identity** — 美化後仍然是「原本這一份簡報的成熟版本」，不是被換皮成另一家公司。

## 2. Three jury lenses / 三個互相制衡的評審視角

v0.6 不是單一美感分數。每份 deck 必須同時通過三個 jury lenses：

### Lens A — Purpose / Hierarchy / Simplicity / Craft

檢查：

- primary purpose 是否清楚
- focal point 是否唯一或有明確優先序
- order / spacing / contrast 是否形成 hierarchy
- decoration 是否服務內容
- typography / spacing / alignment / proportion 是否精準
- 是否有「只是看起來很設計」但沒有功能的元素

### Lens B — Executive Communication

檢查：

- 3 秒內能否辨識 page purpose 與 focal system
- reading path 是否自然
- evidence 是否排在正確層級
- 高階客戶能否快速區分 headline / context / proof / status / detail
- footer / logo / badges / labels 是否沒有搶主角
- dense page 是否仍可 scan

Content Lock 可能禁止改寫成 action title；此時 jury 應評估 **現有內容是否被最佳化呈現**，不得以「標題不夠像顧問公司」為由改內容。

### Lens C — Domain / Slide-role Fit

不同頁型用不同標準：

- `keynote_launch`
- `executive_strategy`
- `technical_review`
- `research_academic`
- `brand_editorial`
- `comparison`
- `agenda_section_closing`
- `mixed`

不得用 keynote 的極簡標準去摧毀 engineering detail，也不得用 engineering 密度去做 luxury/editorial cover。

## 3. Global core checks / 每頁不可妥協的布林檢查

每一頁都必須：

```text
purpose_is_clear=true
focal_point_is_unambiguous=true
hierarchy_is_structural=true
spacing_is_intentional=true
typography_is_crafted=true
color_is_disciplined=true
source_identity_is_preserved=true
signal_to_noise_is_high=true
glance_test_pass=true
brand_and_status_do_not_compete=true
no_generic_template_skin=true
```

任一 false：`GLOBAL_DESIGN_JURY_PASS=false`。

## 4. Global scores / 每頁世界級評分

每頁必須提供：

```text
purpose
hierarchy
simplicity
craft
composition
typography
spacing_rhythm
color_discipline
source_identity
signal_to_noise
glance_readability
executive_readiness
```

預設 world-class thresholds：

- 每一核心 dimension `>= 90`
- `source_identity >= 95`
- `craft >= 92`
- `slide_jury_score >= 93`
- 不允許 overall score 掩蓋弱項

`slide_jury_score` 若比 dimension average 高超過 3 分，視為評分失真。

## 5. Deck Identity Guard / 每份簡報必須有自己的靈魂

Deck-level identity 必須記錄 source 與 final 的 personality evidence：

- canvas polarity / light-dark-mixed
- dominant accent logic
- typography character
- density profile
- geometry language
- brand terrain
- image / chart language
- recurring signature motifs

必須：

```text
source_personality_preserved=true
no_template_convergence=true
no_unjustified_cardification=true
no_unjustified_dark_techification=true
no_unjustified_gradientization=true
no_brand_personality_erasure=true
```

Deck-level scores：

- `identity_fidelity_score >= 95`
- `archetype_fit_score >= 92`
- `generic_template_risk <= 10`

這一層用來防止：

> 五份不同 deck 經過 AI 後，全部變成同一套深藍＋cyan＋rounded-card。

## 6. Role-specific jury / 不同類型的世界級標準

### A. Keynote / Product Launch

重點：

- 一個 dominant idea
- stage readability
- intentional visual pause
- hero image / statement 不被 secondary UI 搶走
- 少量元素但不是資訊不足
- emotion / brand tone coherent

Role scores：

```text
stage_readability
single_idea_focus
visual_pause
emotional_tone_fit
hero_focus
```

### B. Executive Strategy / Board / Customer Review

重點：

- decision path clear
- evidence priority clear
- status / risk / recommendation 不互相混淆
- scan path 可在數秒內建立
- footnotes/details 存在但不搶焦點

Role scores：

```text
decision_path_clarity
evidence_priority
scan_efficiency
status_risk_clarity
executive_density_control
```

### C. Technical Review / Engineering / Data

重點：

- charts/tables 是主角，不是 decorations
- comparison rails 清楚
- gridlines/borders/scaffolding 退到背景
- limit / threshold / anomaly / delta 一眼可定位
- high-density 仍然 legible
- L/R、A/B、Before/After peer systems 一致

Role scores：

```text
data_legibility
comparison_structure
scaffolding_restraint
focal_evidence
technical_density_control
```

### D. Research / Academic

重點：

- figure / caption / result relationship
- method / evidence / conclusion 不混在同一 hierarchy
- citations / notes 可讀
- high information density 仍有 grouping

Role scores：

```text
figure_caption_relation
method_result_structure
citation_legibility
research_density_control
evidence_traceability
```

### E. Brand / Editorial / Luxury

重點：

- typography expression
- art direction consistency
- whitespace as structure
- asymmetry 若存在要有明確 balance
- brand personality 不被 corporate template 消毒

Role scores：

```text
typographic_expression
art_direction
whitespace_control
asymmetric_balance
brand_expression
```

### F. Agenda / Section / Closing

重點：

- navigation clarity
- pace / pause
- template artifact = 0
- source brand ending/section identity 被尊重

Role scores：

```text
navigation_clarity
pacing
brand_continuity
artifact_cleanliness
transition_role_fit
```

## 7. 3-second glance test / 3 秒測試

每頁的 glance test 不是要求 3 秒讀完所有工程數據，而是 3 秒內能回答：

1. 這頁的任務是什麼？
2. 第一個該看哪裡？
3. 這頁是哪一種資訊結構？

例如 technical review 頁：

> 「這是 POWER 6σ limits；上方是 limit table；下方是 L/R comparison。」

能做到即屬 pass；不要求 3 秒理解每個 frequency value。

## 8. Craft requires iteration / 世界級不接受一次生成即宣稱完成

v0.6 final 至少要有：

```text
review_rounds >= 2
```

第一輪：source-vs-candidate jury。

第二輪：修正後重新 render，再做 jury。

若第一輪沒有任何修改，第二輪仍必須是獨立 verification pass。

## 9. Evidence / 不准 AI 自嗨式打分

Global Jury 每頁必須留下：

```text
primary_purpose
focal_point
reading_order
grid_or_alignment_logic
spacing_logic
source_identity_anchors
what_was_removed_or_restrained
why_this_is_not_a_generic_template
```

Deck-level 必須留下：

```text
source_personality
final_personality
identity_evidence
jury_lenses
review_rounds
```

只有分數、沒有 evidence：FAIL。

## 10. Final v0.6 gate

Fully qualified v0.6 final 必須：

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
SPATIAL_QA_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
COMPOSITION_QA_PASS=true
DECK_IDENTITY_PASS=true
GLOBAL_DESIGN_JURY_PASS=true
REGRESSION_V06_PASS=true
DELIVERY_V06_PASS=true
```

`DELIVERY_V05_PASS=true` 只能代表通過舊版 v0.5，不足以稱為 v0.6 世界級 final。
