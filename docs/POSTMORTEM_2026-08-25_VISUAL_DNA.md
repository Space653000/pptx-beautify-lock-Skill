# Postmortem — v0.3 Visual QA False Pass / v0.3 視覺驗收誤通過

Date: 2026-08-25

## Summary / 摘要

A real-deck review exposed two defects that v0.3 could incorrectly pass:

1. **Template placeholder leakage / placeholder 與真正內容重疊**
   - e.g. a generic `presentation title` remained visible underneath the real title.
2. **Source visual DNA drift / 來源主色調漂移**
   - a source deck whose visual system was predominantly white/light was redesigned with a dark-navy canvas treatment without explicit user authorization.

A third requirement was added during the same review:

3. **Traditional Chinese + English typography / 繁中英文雙語字體**
   - typography must be glyph-safe and visually coherent for both scripts; Latin-only fonts must not silently force uncontrolled CJK fallback.

## Root cause / 根因

v0.3 focused on:

- protected content semantics
- geometry/layout lint
- generic rendered readability

It did **not** make source-theme fidelity or bilingual typography explicit machine-readable delivery gates. The rendered QA checklist also did not have a dedicated template-placeholder-artifact field in the earliest real-deck run.

Therefore a deck could be content-correct and structurally valid while still being visually wrong for the source presentation.

## Corrective actions / 修正措施

v0.4 introduces:

- `references/THEME_DISCOVERY.md`
- `references/TYPOGRAPHY_BILINGUAL.md`
- `scripts/pptx_theme_profile.py`
- Theme Discovery before any design decision
- light/dark/mixed source polarity guard
- rendered `theme_fidelity_preserved` check
- rendered `bilingual_typography_clean` check
- blocking `no_template_placeholder_artifacts` check
- linter detection for generic placeholder leakage
- linter warning for CJK text assigned to Latin-oriented fonts
- regression output `THEME_GUARD_PASS` and `THEME_FIDELITY_PASS`

## Revised delivery contract / 修正版交付契約

A fully qualified v0.4 final deck requires:

```text
CONTENT_LOCK_PASS=true
THEME_FIDELITY_PASS=true
LAYOUT_QA_PASS=true
VISUAL_QA_PASS=true
REGRESSION_PASS=true
DELIVERY_PASS=true
```

`visual_qa.json` schema 3 requires every slide to pass:

```text
no_template_placeholder_artifacts=true
theme_fidelity_preserved=true
bilingual_typography_clean=true
```

in addition to the existing overlap/clipping/readability/layout checks.

## Status of earlier five-deck outputs / 舊 5 份輸出狀態

The earlier five beautified decks were evaluated under the older contract. After this postmortem, their prior `DELIVERY_PASS=true` status must **not** be interpreted as v0.4-qualified final delivery.

They are **superseded candidates requiring reprocessing/review under v0.4**.

This is intentional fail-closed behavior: quality evidence must match the current contract rather than preserving a historical PASS label.
