# No-Degradation / Source-Faithful Safe-Only Contract

This rule exists because an automatic beautifier can make a presentation objectively worse even while preserving all text and numbers. Content Lock is necessary, but it is not sufficient.

## Core principle

> **Original wins ties. If the source is already acceptable and the engine cannot prove that a visual change fixes a real defect without creating a new one, preserve the source.**

This is the presentation equivalent of a Hippocratic / do-no-harm rule.

## Source-faithful means conservative, not creative

For the default `自動（忠於原稿 / Source-faithful）` mode:

- existing geometry is locked: x/y/width/height/rotation/z-order must not change;
- existing typography scale is locked: font size, font family, bold/italic/underline, paragraph fitting and wrapping must not change;
- existing table geometry and visual formatting are locked;
- existing picture/media geometry and crop state are locked;
- theme/master/layout/background/brand terrain are locked;
- source slide count/order and protected content are locked;
- generic beautification such as cardification, new panels, forced title enlargement, palette replacement or table recoloring is forbidden.

The default offline Source-faithful change budget is intentionally tiny:

1. proofing metadata may be set to suppress editor-only red spell-check squiggles;
2. no other visual mutation is allowed unless a future rule has an explicit defect detector, a bounded repair, and a regression proof.

This means Source-faithful may look almost identical to the source. That is correct behavior when the source is already better than the generic formatter.

## Defect-driven editing

A visual mutation is allowed only when all of these are true:

1. **Known defect:** a specific defect is detected, such as clipping, overflow, real-content occlusion, template sample text collision, unusable font fallback, or sibling-page regression.
2. **Local repair:** the change is limited to the minimum objects needed to fix that defect.
3. **Bounded change:** the allowed properties are enumerated before editing.
4. **Before/after proof:** the candidate fixes the known defect.
5. **No new regression:** the candidate introduces no new overflow, collision, hierarchy loss, typography inflation, theme drift, or sibling inconsistency.
6. **Full-deck regression:** repairing one slide must not invalidate previously acceptable slides.

If any item cannot be proven, rollback that change.

## Safe-change budget

Think of every visual edit as spending a risk budget.

### Zero/near-zero risk

- proofing metadata only;
- non-rendering metadata that does not affect content or geometry.

### Medium risk — requires explicit defect evidence

- x/y/width/height changes;
- text margins/alignment/wrap/autofit;
- font family/size/weight;
- table row/column sizing;
- border/fill changes;
- image/chart repositioning.

### High risk — forbidden in Source-faithful mode

- new card/panel systems;
- dark/light polarity change;
- major palette change;
- large title-scale changes;
- re-templating a deck;
- changing master/layout/background identity;
- global table restyling without a sibling-family defect detector.

## Original-is-better gate

For each slide:

```text
SOURCE_QUALITY
    vs
CANDIDATE_QUALITY
```

The candidate may replace the source only if it has a measurable improvement and no new regression.

If quality is equal, uncertain, renderer evidence is unavailable, or the candidate merely looks "different":

```text
KEEP_SOURCE_SLIDE=true
```

## Offline engine rule

The offline engine is deterministic and does not have human-level visual judgment. Therefore its default Source-faithful mode must be more conservative than the AI Skill.

Offline Source-faithful must not attempt a generic redesign. It should preserve the PPTX exactly except for specifically allowlisted non-destructive metadata changes.

Creative/transformative presets are explicit opt-in modes and are not equivalent to Source-faithful.

## Required gates

A Source-faithful offline result may claim success only when all are true:

```text
CONTENT_LOCK_PASS=true
SOURCE_PACKAGE_STRUCTURE_PASS=true
SOURCE_GEOMETRY_LOCK_PASS=true
SOURCE_TYPOGRAPHY_LOCK_PASS=true
SOURCE_TABLE_STYLE_LOCK_PASS=true
SOURCE_MEDIA_LOCK_PASS=true
SOURCE_THEME_IDENTITY_LOCK_PASS=true
SAFE_CHANGE_BUDGET_PASS=true
NO_DEGRADATION_GATE_PASS=true
FINAL_OUTPUT_REOPEN_PASS=true
```

## Engineering lesson

A beautifier must optimize for **net visual improvement**, not for the number of properties it changed.

A no-op is better than a harmful edit.
