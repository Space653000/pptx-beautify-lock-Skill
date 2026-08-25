# v0.6 Global Design Jury — Public Research Basis

Date: 2026-08-25

This document separates **public source guidance** from this repository's own operational rules. The goal is not to clone any company's visual skin.

## 1. Apple — purpose, hierarchy, simplicity, craft

Public sources:

- https://developer.apple.com/design/human-interface-guidelines/design-principles
- https://developer.apple.com/videos/play/wwdc2026/250/

Source-supported ideas:

- Design starts with purpose / intention.
- Simplicity means removing the unnecessary, not merely looking minimal.
- Clear hierarchy uses order, spacing, and contrast to guide attention.
- Every element should earn its place.
- Craft means deliberate attention to detail and iteration.

Repository distillation:

> v0.6 does **not** create an “Apple template.” It requires every slide to prove purpose, hierarchy, simplicity, and craft regardless of palette or brand.

## 2. Microsoft Fluent — space creates relationships

Public sources:

- https://fluent2.microsoft.design/layout
- https://fluent2.microsoft.design/typography
- https://fluent2.microsoft.design/design-principles

Source-supported ideas:

- Spacing and proximity communicate relationship and grouping.
- Empty space can create hierarchy and focus.
- Consistent spacing creates visual rhythm.
- Alignment organizes and balances a composition and supports hierarchy.
- Typographic hierarchy makes content scannable.

Repository distillation:

> Grid, rails, spacing rhythm, baseline relationships, and whitespace are first-class structural evidence, not cosmetic polish.

## 3. Google / Material-related public guidance — systematic spacing and typography

Public sources:

- https://developers.google.com/cars/design/automotive-os/design-system/layout
- https://developers.google.com/cars/design/android-auto/design-system/typography
- https://developers.google.com/style/headings

Source-supported ideas:

- Grid/keyline systems and repeated spacing values create coherent structure.
- Typography uses semantic levels to establish hierarchy.
- Font choice should remain legible and language-safe; Google guidance recommends Noto Sans for languages not covered by Google Sans/Roboto in the cited system.
- Heading structure should reflect logical hierarchy rather than being used only as visual styling.

Repository distillation:

> v0.6 uses a small repeated spacing vocabulary and semantic type roles, but it does not force Material appearance onto a PowerPoint deck.

## 4. Duarte — glance media / three-second test

Public source:

- https://www.duarte.com/blog/the-three-second-test/

Source-supported idea:

- Slides can be evaluated as glance media: a viewer should quickly recognize what catches the eye and what the slide is about.

Repository distillation:

> The v0.6 glance test does **not** require a dense engineering slide to be fully understood in three seconds. It requires page purpose, focal system, and information structure to be identifiable in about that time.

## 5. Presentation Zen — contrast, repetition, alignment, proximity

Public source:

- https://www.presentationzen.com/chapter6_pages.pdf

Source-supported ideas:

- Contrast, repetition, alignment, and proximity are foundational graphic-design relationships.
- Alignment connects objects to an implied structure.
- Proximity communicates grouping.
- Repetition creates consistency.
- Contrast creates energy and distinction.

Repository distillation:

> These principles are implemented as structural relationships and QA evidence, not as a visual theme.

## 6. NVIDIA GTC — technical keynote as an observational benchmark, not a rule source

Public sources:

- https://www.nvidia.com/gtc/keynote/
- https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-s81595/

What the public material supports:

- GTC keynote is explicitly a business/executive technical keynote covering platforms, systems, ecosystems, accelerated computing, AI factories, and related technical concepts.
- The 2026 keynote transcript includes moments where a single chart is described as summarizing strategy, showing the importance of visual evidence as a focal object in technical communication.

Repository inference:

> NVIDIA is **not** treated as a proprietary design specification. v0.6 extracts only the generic communication requirement: technical keynotes need disciplined information density, clear focal evidence, legible comparative structure, and strong stage readability.

## 7. What v0.6 deliberately refuses to copy

The Global Design Jury must reject style mimicry as a substitute for quality:

- no Apple-white-space costume
- no NVIDIA black/green costume
- no generic consultant-blue costume
- no Material-card costume
- no one-size-fits-all rounded-card system

Instead it asks:

```text
Does this slide serve its purpose?
Is hierarchy obvious?
Is spacing intentional?
Is the craft precise?
Does the page fit its audience and role?
Is the source identity still unmistakably itself?
```

## 8. Repository-original implementation

The following are original operational constructs in this repository, not claims attributed to the public sources above:

- Soul → Frame → Skeleton → Joints → Limbs → Skin
- `GLOBAL_DESIGN_JURY_PASS`
- `DECK_IDENTITY_PASS`
- global core score thresholds
- role-specific jury lenses
- `generic_template_risk`
- required two-round jury review
- v0.6 fail-closed delivery contract
