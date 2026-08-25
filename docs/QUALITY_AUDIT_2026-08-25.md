# Quality Audit — 2026-08-25

**Repository:** `Space653000/pptx-beautify-lock-Skill`  
**Audit fixed point:** `343c72b0d7ad1ee3b690815a3e86d602c069cb6f`  
**Primary language:** 繁體中文；English for cross-agent compatibility.

## Audit method / 審查方法

本次審查依 `Space653000/Claude-code-ChatGPT-Codex---SKILL` 的 `ask-matt` 路由原則，選擇最小但足夠的 skill set：

1. **writing-for-agents** — 檢查 Skill/AGENTS/CLAUDE 文件是否有清楚 pointer、single source of truth、progressive disclosure、可檢查 completion criteria，並減少 duplicated policy/sprawl。
2. **code-review** — 以兩個互相獨立的軸檢查：
   - **Standards axis:** 是否符合上述 agent-document/testing standards。
   - **Spec axis:** 是否真的達成「內容凍結，只改視覺，自動 Lint/Format/Design/Regression，可供 Claude/Codex 使用」。
3. **tdd** — 將測試移到 public CLI seams；用行為契約證明 PASS/FAIL，而不是綁定內部函式。
4. **adversarial-plan-review mindset** — 主動尋找 verifier 可能漏掉、誤判或讓 AI 偷渡內容變更的反例。

## Standards axis findings / 規範軸

### S1 — Policy duplication / 規則重複

**Before:** `README.md`, `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, `AI_BOOTSTRAP.md` 都維護相似 Content Lock 清單，容易 drift。

**Fix:**

- `references/CONTENT_LOCK.md` 成為 protected semantics 的唯一權威定義。
- `SKILL.md` 保留 ordered actions + completion criteria。
- root entry-point files 縮成 strong pointers，不再複製整套規則。

### S2 — Skill sprawl / 主流程過長

**Before:** 主 `SKILL.md` 混合大量 reference 與操作步驟。

**Fix:** 採 progressive disclosure：Linter、Formatter、Design、Render QA、Regression 各有 reference，主 Skill 只保留流程與 hard gates。

### S3 — Weak completion criteria / 完成界線不夠可驗證

**Fix:** 每一 phase 加上 checkable completion criterion；最終完成不再是「已美化」，而是：

```text
DELIVERY_PASS=true
```

### S4 — Implementation-coupled tests / 測試綁內部實作

**Before:** tests 直接 import verifier/linter internals。

**Fix:** contract tests 改走真正公開 seam：

```text
python pptx_content_lock.py ...
python pptx_lint.py ...
python visual_qa_gate.py ...
python pptx_regression.py ...
```

內部可以重構，只要 CLI 行為契約不變，測試就不應壞。

### S5 — Duplicate layout QA implementations

**Before:** `pptx_lint.py` 與 `verify_layout.py` 各自有一套 geometry/overlap 邏輯。

**Fix:** `pptx_lint.py` 成為 single source of truth；`verify_layout.py` 只保留 legacy compatibility wrapper。

## Spec axis findings / 需求軸

### P1 — Content Lock originally covered too little

初版主要保護 text/table values/chart cache/media/crop/notes/embeddings，但 PowerPoint 還有會改變內容或行為的隱性 semantics。

**Added protection:**

- table merge topology
- hyperlink/action targets
- accessibility alt/title/description
- hidden/shown slide state
- transition and animation/timing semantics
- comments/threaded comments
- master/layout/SmartArt text
- Office Math semantics
- embedded/OLE payloads
- package media payload sets
- custom XML / ActiveX / macro-like opaque protected payloads
- external content relationship targets

### P2 — Global value comparison could miss wrong associations

若兩個物件交換 hyperlink/semantic metadata，全 deck 仍可能擁有相同 global value set，但內容行為已改。

**Fix:** schema 4 content manifest 以 content-bearing object 建立 protected-semantic records，並將 text/table/media/link/accessibility 關聯保留在同一 object record 中。

### P3 — Run-level text comparison produced false positives

純字型重設可能把一個 text run 拆成兩個 run；文字完全不變卻被判 regression。

**Fix:** verifier 在 paragraph level 正規化 text，同時保留 list level/bullet semantics；忽略 run segmentation 與 font formatting。

### P4 — Linter missed table text and cross-slide signals

**Fix:**

- 掃描 table-cell text/font sizes
- recurse grouped shapes for text metrics
- table-density risk
- dense-text render-review hints
- cross-slide explicit-font outliers
- title-layout consistency hints

### P5 — Geometry checks cannot prove visual quality

OOXML coordinates不能證明：真正 text overflow、clipping、intentional vs accidental overlap、hierarchy、spacing、balance、table readability。

**Fix:** 新增 rendered Visual QA contract：

```text
render every slide
→ review every slide
→ visual_qa.json
→ visual_qa_gate.py
```

完整 delivery 必須有 `VISUAL_QA_PASS=true`。

### P6 — Regression warning count was an invalid beauty proxy

總 warning 數可能因刻意的 text-over-shape design 增加，反而誤殺好設計。

**Fix:**

- hard structural errors 必須為 0
- tiny-text/table-density 等 readability warnings 不得惡化
- ambiguous overlap/design heuristics 交給 render Visual QA adjudicate

### P7 — GitHub URL was not a convenient installable package

**Fix:** 新增：

```text
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
```

marketplace identity 使用 `space653000-pptx`，避免與另一個 `space653000` marketplace identity 衝突。

## Contract tests / 行為契約測試

目前自動測試涵蓋至少：

- visual-only typography/geometry change → PASS
- run segmentation changes but identical paragraph text → PASS
- visible text change → FAIL
- table value change → FAIL
- table merge semantics change → FAIL
- hyperlink target change → FAIL
- hyperlink association swap between objects → FAIL
- hidden slide state change → FAIL
- table tiny text detected by Linter
- Visual QA report must cover every slide and every required check
- `--require-visual-qa` without report cannot produce delivery pass
- plugin manifests point to the installable Skill

## Final delivery contract / 最終交付契約

Fully qualified output requires all five gates:

```text
CONTENT_LOCK_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
REGRESSION_PASS=true
DELIVERY_PASS=true
```

## Residual limitations / 剩餘限制

1. **Aesthetics are not mathematically provable.** `visual_qa.json` makes the reviewer exhaustive and auditable, but visual quality still depends on the render engine and AI/human reviewer quality.
2. **True text overflow is a renderer concern.** `python-pptx` geometry heuristics cannot replace PowerPoint/LibreOffice/host rendering.
3. **PowerPoint is an open-ended OOXML container.** The verifier protects many known and opaque semantic payloads conservatively, but exotic vendor/proprietary extensions may require a new semantic adapter. Uncertain protected semantics should fail closed.
4. **Editing-tool fidelity matters.** Rebuilding a complex deck from scratch can discard transitions, actions, embedded objects or extension parts. The Skill therefore prefers in-place visual edits for complex decks.
5. **Plugin CLI syntax is harness-version dependent.** Manual Agent Skill installation remains the fallback if a future Claude/Codex release changes marketplace commands.

## Review disposition / 審查結論

The architecture after this audit is deliberately layered:

```text
Content Lock = invariant
Linter = structural evidence
Auto Formatter = low-risk repair
Design Agent = visual transformation
Render Visual QA = appearance evidence
Regression Test = release gate
```

No remaining known finding in this audit justifies relaxing Content Lock. Future changes should preserve the same fixed-point review pattern: **Standards axis + Spec axis + public-seam regression tests**.