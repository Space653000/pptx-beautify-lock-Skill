# v0.5 Three-Pass Audit — 2026-08-25

Scope: `pptx-beautify-lock` v0.5 Layout Intelligence / Composition QA upgrade triggered by real MEC slide regressions.

Reference skill catalog used for audit selection:

`Space653000/Claude-code-ChatGPT-Codex---SKILL`

Selected methods:

- `research`
- `public-skill-distiller`
- `adversarial-plan-review`
- `diagnosing-bugs`
- `tdd`
- `code-review`
- `codebase-design`
- `improve-codebase-architecture`

The three passes below are intentionally different review axes. They are not the same checklist repeated three times.

---

## Pass 1 — Adversarial plan / design-direction review

### Question attacked

Could the proposed Layout Intelligence rules create a new one-template-fits-all system or reject legitimate asymmetric layouts?

### Findings

#### 1. Peer-chart pairing was initially too broad — FIXED

Initial logic compared similarly sized visuals by horizontal separation and could accidentally compare a chart in row 1 against a chart in row 2 of a 2x2 grid.

Risk: false `sibling-visual-rail-drift` failures on valid multi-row technical layouts.

Disposition:

- Added same-row evidence via vertical-overlap ratio.
- Peer comparison now requires meaningful vertical overlap before enforcing common top/size rails.
- Added `tests/test_layout_peer_rows.py` to lock the regression.

#### 2. Large panel over a branded cover must not be an unconditional hard error — ACCEPTED AS REVIEW WARNING

The MEC failure showed a large filled title region can suppress department identity and hero art. However, some legitimate branded decks deliberately use a panel in a quiet zone.

Disposition:

- `brand-background-occlusion-risk` is a warning that forces source-vs-final Composition QA.
- Actual content occlusion is still a hard error.
- The design rule says panels must earn their place and preserve brand terrain; it does not ban panels globally.

#### 3. “Apple-like” must not become “copy Apple” — FIXED IN MODEL

Disposition:

- Public research is translated into general principles: purpose, consistency, simplicity/hierarchy, craft, precision alignment, whitespace, contrast/proximity/repetition.
- The repository defines its own six-layer slide anatomy and page-role rules.
- Source theme and brand remain primary; no Apple visual template is imposed.

### Pass 1 result

**PASS after one material correction.**

---

## Pass 2 — Diagnosis + TDD + code/spec review

### Tight repros used

1. Foreground solid rectangle placed over protected title text.
   - Expected: Spatial QA fails on exact symptom.
2. Same decorative rectangle moved behind content.
   - Expected: Spatial QA passes.
3. 2x2 chart grid.
   - Expected: no cross-row peer-alignment false positive.
4. Composition report with one weak dimension but artificially high overall score.
   - Expected: Composition QA fails.
5. v0.5 regression without a Composition QA report.
   - Expected: fail closed; no `DELIVERY_V05_PASS=true`.
6. v0.5 regression with both valid Visual QA and Composition QA evidence.
   - Expected: strict delivery passes.

### Findings

#### 1. New regression interface had an always-true expression — FIXED

The first implementation emitted `COMPOSITION_QA_REQUIRED` through an `... or True` expression. Behavior was intentionally always-required, but the expression was noisy and misleading.

Disposition:

- Replaced with explicit `COMPOSITION_QA_REQUIRED=True` and explanatory comment.
- Simplified strict v0.5 pass expression to its actual invariant: structural + visual + composition.

#### 2. Strict delivery needed its own integration seam — ADDED

Unit tests for Spatial QA and Composition QA were not enough to prove the orchestrating regression gate failed closed.

Disposition:

- Added `tests/test_v05_delivery_contract.py`.
- It verifies both positive and fail-closed paths through the public regression CLI.

#### 3. Legacy compatibility is intentionally preserved

`REGRESSION_PASS` / `DELIVERY_PASS` remain for v0.4 consumers.

The v0.5 authoritative docs explicitly prohibit treating legacy `DELIVERY_PASS=true` as a v0.5 final. Strict final requires `DELIVERY_V05_PASS=true`.

### CI evidence

GitHub Actions run on the v0.5 branch/PR completed successfully after the test and regression changes.

### Pass 2 result

**PASS after two implementation/testability corrections.**

---

## Pass 3 — Codebase design / agent navigability / provenance review

### Architecture review

The new capability is split at two deliberate seams:

1. `pptx_layout_intelligence.py`
   - machine structural evidence
   - conservative high-confidence geometry/occlusion/rail findings
   - does not pretend to understand subjective beauty

2. `composition_qa_gate.py`
   - validates exhaustive render-based, source-vs-final human/vision review evidence
   - requires per-slide checks, dimension scores, and explicit anchors/rails/reading-order evidence

This separation keeps the machine guard deterministic and the aesthetic review explicit rather than mixing heuristics and subjective scoring into one opaque function.

### Agent entry-point audit — STALE v0.4 GATES FOUND AND FIXED

The following active front doors still told future Claude/Codex agents that `DELIVERY_PASS=true` alone was sufficient:

- `AI_BOOTSTRAP.md`
- `AGENTS.md`
- `CLAUDE.md`
- `INSTALL.md`

Disposition:

- Updated all four to v0.5.
- They now route agents through Source Theme + Brand Terrain + Layout Skeleton + Spatial QA + Visual QA + Composition QA.
- They explicitly require `DELIVERY_V05_PASS=true` for a qualified v0.5 final.

### Provenance / research review

`docs/DESIGN_RESEARCH_2026-08-25.md` explicitly separates:

1. what public sources support;
2. the operational principle inferred from those sources;
3. this repository's original implementation model.

Public research includes first-party Apple HIG/Keynote guidance and public material from Presentation Zen and Duarte. The repo does not copy a proprietary template or claim those authors created the six-layer anatomy.

### Pass 3 result

**PASS after correcting four stale agent entry points.**

---

## Final audit conclusion

Three independent review axes each found something useful:

- Pass 1 found a **design-rule false-positive risk**.
- Pass 2 found a **regression-code clarity issue and missing integration seam**.
- Pass 3 found **four stale URL/bootstrap entry points** that could have caused Claude Code/Codex to silently use the weaker v0.4 finish line.

The v0.5 design is accepted only after those corrections.

Authoritative final contract:

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
SPATIAL_QA_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
COMPOSITION_QA_PASS=true
REGRESSION_V05_PASS=true
DELIVERY_V05_PASS=true
```

Core principle:

> **A slide with intact content and zero overlap can still be visually wrong. v0.5 therefore treats spatial composition as a first-class deliverable, not a cosmetic afterthought.**
