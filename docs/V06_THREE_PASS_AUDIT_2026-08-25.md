# v0.6 Global Design Jury — Three-Pass Audit

Date: 2026-08-25

Scope: upgrade `pptx-beautify-lock` from v0.5 spatial/composition quality to a stricter world-class design-delivery contract without turning every deck into the same visual template.

Review toolbox reference:

`Space653000/Claude-code-ChatGPT-Codex---SKILL`

Selected methods for this audit:

- `research`
- `public-skill-distiller`
- `adversarial-plan-review`
- `diagnosing-bugs`
- `tdd`
- `code-review`
- `codebase-design`
- `improve-codebase-architecture`

The three passes deliberately attack different failure classes.

---

## Pass 1 — Adversarial design-direction review

### Attack question

Could “Global Design Jury” accidentally force every deck toward one high-scoring visual language?

### Findings

#### 1. World-class must be principles, not costumes — ACCEPTED / ENFORCED

The v0.6 contract explicitly rejects shortcut mimicry:

- no Apple-white-space costume
- no NVIDIA black/green costume
- no consultant-blue costume
- no universal rounded-card system
- no automatic dark-tech / gradient conversion

Instead the core jury evaluates Purpose, Hierarchy, Simplicity, Craft, Executive Communication, Domain/Role Fit, and Source Identity.

#### 2. One universal slide-role rubric would bias the deck — FIXED BY ROLE LENSES

Keynote, engineering review, executive strategy, academic research, and luxury/editorial slides have different legitimate density and composition behavior.

Disposition:

- Added role-specific score sets for `keynote_launch`, `executive_strategy`, `technical_review`, `research_academic`, `brand_editorial`, `agenda_section_closing`, `comparison`, and `other`.
- Core world-class dimensions remain common; role dimensions prevent keynote minimalism from destroying engineering detail and prevent technical density from polluting editorial/launch pages.

#### 3. “Executive readiness” must mean audience readiness, not consulting style — CLARIFIED

The core score `executive_readiness` is interpreted as readiness for high-level external/internal review: fast scan, clear purpose, controlled hierarchy, no distracting chrome. It does not authorize content rewriting or consulting-template styling.

### Pass 1 result

**PASS.** The design system remains source-first and role-aware rather than template-first.

---

## Pass 2 — TDD / code-review / loophole attack

### Attack question

Can the machine gate be gamed with high averages, fake review rounds, incomplete slide coverage, or deck-level scores that hide page-level identity loss?

### Tight regression cases

1. One core score = 89, overall still 94.
   - Must fail.
2. `generic_template_risk = 11`.
   - Must fail Deck Identity.
3. A required jury lens missing.
   - Must fail.
4. `review_rounds = 2` but no review history.
   - Must fail.
5. Round 1 reviews zero slides.
   - Must fail.
6. A single slide `source_identity = 94` while deck identity score is 97.
   - Must fail both Global Jury and Deck Identity.
7. Regression called with Visual + Composition QA but no Global Jury.
   - v0.6 must fail closed.
8. Full valid Visual + Composition + Global Jury evidence.
   - v0.6 delivery must pass.

### Findings and corrections

#### 1. Review rounds were initially self-asserted — FIXED

Initial v0.6 required `review_rounds >= 2`, but a caller could claim `2` without proving two review passes.

Disposition:

- Added mandatory `review_history`.
- History length must equal `review_rounds`.
- Each round records reviewer, render fingerprint/reference, findings, action/verification, verdict.
- Final round must pass.

#### 2. A review round could still omit pages — FIXED

Even with review history, a reviewer could theoretically inspect only a sample.

Disposition:

- Every round now requires `slides_reviewed`.
- Every round must cover every slide exactly once.
- Sampling cannot certify v0.6 final.

#### 3. Deck Identity could miss a per-slide identity failure — FIXED

Initial `DECK_IDENTITY_PASS` only aggregated deck-level `deck_identity.*` errors.

Disposition:

- Per-slide `source_identity_is_preserved`, `source_identity` score, and generic-template-skin failures now propagate into Deck Identity failure.

#### 4. High overall scores cannot hide weak dimensions — ENFORCED

- Every core dimension has an independent floor.
- Every role dimension has an independent floor.
- Slide/deck overall scores are bounded against dimension averages to catch inflated self-scoring.

### Pass 2 result

**PASS after closing three material loopholes.**

---

## Pass 3 — Agent distribution / architecture / navigability review

### Attack question

Will Claude Code / Codex actually install and execute the v0.6 contract, or will stale front doors silently route them to v0.5 behavior?

### Findings

#### 1. Active entry points updated — PASS

Updated:

- `AGENTS.md`
- `CLAUDE.md`
- `AI_BOOTSTRAP.md`
- `INSTALL.md`
- `README.md`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

All now route a qualified final to `DELIVERY_V06_PASS=true`.

#### 2. Installer remains distribution-complete — PASS

`scripts/install_skill.py` copies the entire `pptx-beautify-lock/` directory into Claude/Codex skill locations, therefore v0.6 references, `global_design_jury_gate.py`, and the report schema travel together with `SKILL.md`.

#### 3. Architecture keeps deterministic checks separate from aesthetic judgement — PASS

The system is intentionally layered:

```text
Content Lock              deterministic semantics
Theme Guard               deterministic / heuristic source fidelity
Spatial QA                conservative geometry checks
Visual QA                 rendered visual correctness
Composition QA            skeleton / balance review
Global Design Jury        purpose / craft / audience / role / identity
Regression v0.6           fail-closed orchestration
```

The code does not pretend that geometry alone can prove beauty, and the jury does not replace machine content/theme/spatial safeguards.

#### 4. Research provenance separated from repository-original rules — PASS

`docs/DESIGN_RESEARCH_V06_GLOBAL_JURY.md` distinguishes:

- public source guidance;
- repository inference/distillation;
- repository-original thresholds and mechanisms.

NVIDIA is treated only as an observational technical-keynote benchmark, not as a design specification. Apple/Microsoft/Google/Duarte/Presentation Zen principles are distilled into general quality criteria rather than copied visual skins.

### Pass 3 result

**PASS.** Agent front doors, distribution, architecture, and provenance are aligned with v0.6.

---

## Final audit contract

A fully qualified v0.6 final requires:

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

World-class floors include:

```text
core dimensions >= 90
source_identity >= 95
craft >= 92
slide_jury_score >= 93
deck_jury_score >= 93
identity_fidelity_score >= 95
archetype_fit_score >= 92
generic_template_risk <= 10
review_rounds >= 2
full slide coverage in every review round
```

Core principle:

> **The target is not one globally fashionable style. The target is globally elite design discipline applied to the source deck's own identity, audience, role, and information density.**
