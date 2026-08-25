# Design Research 2026-08-25 — Layout Intelligence

本研究用於 `pptx-beautify-lock` v0.5。目的不是模仿某一套 Apple/Keynote 外觀，而是把公開設計原則轉成可執行的、來源忠實的投影片空間規則。

## Source-derived principles / 公開來源支持的原則

### Apple / Keynote

First-party sources:

- Apple Human Interface Guidelines — Design principles: https://developer.apple.com/design/human-interface-guidelines/design-principles
- Apple Keynote — Use alignment guides: https://support.apple.com/guide/keynote/use-alignment-guides-tan738df74cb/mac
- Apple Keynote — Position and align objects: https://support.apple.com/guide/keynote/position-and-align-objects-tanb46504b79/mac

Operational takeaways:

1. **Simplicity is organization, not emptiness.** Every element must earn its place; hierarchy should make what matters obvious.
2. **Consistency builds familiarity.** Once an alignment, spacing, or visual role is established, repeat it deliberately.
3. **Precision is structural.** Keynote exposes edge, center, equal-size, and equal-spacing guides because visual coherence depends on shared rails and controlled spacing, not eyeballed placement.
4. **Craft is detail discipline.** Great-looking output is the cumulative result of deliberate small decisions.

### Garr Reynolds / Presentation Zen

Public sources:

- Design Fundamentals — Contrast, Repetition, Alignment, Proximity: https://presentationzen.com/blog/design-fundamentals-contrast-repetition-alignment-proximity
- Presentation Zen Chapter 6 sample: https://www.presentationzen.com/chapter6_pages.pdf

Operational takeaways:

1. **Alignment creates invisible connections.** Objects that belong together should sit on common visual rails; nothing should look randomly placed.
2. **Proximity encodes grouping.** Related objects sit closer together than unrelated groups.
3. **Repetition creates unity.** Repeated title zones, gutters, chart sizes, table headers, and footer anchors give a deck one visual language.
4. **Contrast expresses hierarchy.** Difference should be intentional and meaningful, not decorative noise.
5. **Whitespace is active structure.** Empty space organizes and separates; it is not leftover area.

### Duarte

Public sources:

- Critique language for presentations: https://www.duarte.com/blog/techniques-for-using-critique-language-for-more-powerful-and-effective-presentations/
- Displaying data in presentations: https://www.duarte.com/blog/display-data-in-presentations/
- Presentation design / presenting principles: https://www.duarte.com/blog/presenting/

Operational takeaways:

1. **Whitespace drives focus.** Clutter reduces comprehension; open space must be intentionally allocated around groups.
2. **Hierarchy must reveal parent/child importance.** A viewer should know where to look first, second, and third.
3. **Unity comes from consistent placement and treatment.** Cross-slide coherence matters as much as per-slide polish.
4. **Data scaffolding should recede.** Gridlines, ticks, borders, and supporting chrome should be quieter than the data and semantic highlights.
5. **Design is not decoration.** A decorative element that does not improve meaning, grouping, navigation, or hierarchy should be removed.

## Repository-original synthesis / 本 Skill 的原創操作模型

The public sources above support general principles. The following model is this repository's implementation, not a copied source framework.

### The six-layer anatomy of a slide

1. **Soul / 靈魂** — source brand, theme, tone, content purpose, and page-role pattern.
2. **Frame / 框架** — slide edges, safe areas, full-bleed terrain, master/layout brand chrome, footer/header reservations.
3. **Skeleton / 骨骼** — grid rails, columns, rows, baselines, gutters, spacing rhythm, visual center of gravity.
4. **Joints / 關節** — relationships between title ↔ status ↔ summary ↔ table ↔ chart ↔ footer; proximity and reading order.
5. **Limbs / 肢體** — actual objects: text boxes, tables, charts, images, labels, badges, callouts.
6. **Skin / 外觀** — font, size, color, fill, line, shadow, tint, radius, and decorative treatment.

**Order matters:** Soul → Frame → Skeleton → Joints → Limbs → Skin. A beautiful skin on a broken skeleton is still a bad slide.

## MEC failure that motivated v0.5

The previous v0.4 MEC candidate could pass semantic, theme, and basic overlap checks while still feeling wrong. Two failure classes were visible:

- a large filled title region on the branded cover competed with or obscured the source's visual identity and negative space;
- dense POWER/THD/HOHD pages were mechanically clean but vertically top-heavy, with header/status/table/chart blocks not behaving as one spatial system.

Therefore v0.5 adds **Spatial QA** and a separate **Composition QA** instead of treating `no overlap` as equivalent to `good layout`.

## Non-negotiable conclusion

`Content Lock PASS + Theme Guard PASS + no overlap` is necessary but insufficient.

A fully qualified v0.5 delivery also needs evidence that:

- brand terrain is respected;
- major objects share coherent rails;
- peer visuals share size and alignment;
- spacing has rhythm;
- reading order is unambiguous;
- the page is visually balanced;
- decoration earns its place;
- each slide role uses an appropriate composition rather than a one-template-fits-all layout.
