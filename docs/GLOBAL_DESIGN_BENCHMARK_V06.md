# v0.6 Global Design Benchmark Corpus

Purpose: prevent a false sense of quality from testing only one corporate engineering deck.

A release candidate should be pressure-tested against **radically different presentation languages**. Passing means each deck improves while retaining its own identity; it does **not** mean every deck converges on one aesthetic.

## Real regression anchors

### MEC engineering review

Expected identity:

- dark branded cover / light technical body
- PEGATRON + MEC brand terrain
- dense engineering tables and L/R charts
- corporate footer / date / status zones

Known failures that must never return:

- large title panel suppresses MEC brand identity
- status badge competes with PEGATRON
- `AGENDA` / `THANK YOU` master artifacts compete with real content
- data body becomes top-heavy with unexplained dead space
- L/R peer charts drift in size or rails

### KORE / Microsoft-style engineering review

Expected identity:

- light technical canvas
- restrained Microsoft-like corporate visual language already present in source
- data density remains accessible

Known failure that must never return:

- AI arbitrarily converts a light engineering deck into generic dark-tech styling

## Five synthetic style families

### 1. Keynote launch minimal

Tests:

- one dominant idea
- stage readability
- visual pause
- restrained secondary elements
- strong craft without decorative excess

Failure examples:

- adding dashboard cards to a hero statement
- excessive labels, badges, or UI chrome
- generic dark gradient replacing source brand

### 2. Executive strategy / board review

Tests:

- decision path
- evidence hierarchy
- scan efficiency
- dense but controlled information
- footnotes/details subordinate to the main decision structure

Failure examples:

- visual polish without a clear evidence path
- equal visual weight for headline, status, proof, and detail
- over-decoration that reduces scan speed

### 3. AI compute / technical keynote

Tests:

- technical-density control
- stage readability
- charts/diagrams as focal evidence
- scaffolding restraint
- clear platform/system/comparison structure

Failure examples:

- black/green costume used as a shortcut
- too many small technical labels for stage distance
- gridlines/borders louder than data

### 4. Luxury / editorial / premium brand

Tests:

- typographic expression
- art direction
- asymmetric balance
- whitespace as structure
- source brand personality

Failure examples:

- converting editorial asymmetry into corporate cards
- over-gridding a deliberately quiet composition
- replacing brand typography character with generic sans

### 5. Research / academic / evidence-led

Tests:

- figure-caption relationship
- method/result/evidence hierarchy
- citation legibility
- high-density grouping
- traceability of claims and figures

Failure examples:

- hiding citations to make the page look cleaner
- decorative hero treatment that weakens evidence
- shrinking figures below readable size to preserve a template

## Diversity acceptance test

A multi-deck benchmark batch should satisfy:

```text
all decks: CONTENT_LOCK_PASS=true
all decks: THEME_FIDELITY_PASS=true
all decks: DECK_IDENTITY_PASS=true
all decks: GLOBAL_DESIGN_JURY_PASS=true
all decks: DELIVERY_V06_PASS=true
```

Additionally, the reviewer must explicitly confirm that the five families remain visually distinguishable by:

- canvas / spatial behavior
- typography character
- density
- composition pattern
- accent logic
- image/data treatment

If the batch looks like five color variants of one template, the benchmark fails even when every individual deck is tidy.
