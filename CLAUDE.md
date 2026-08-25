# CLAUDE.md

When this repository is opened in Claude Code, treat `pptx-beautify-lock/SKILL.md` as the authoritative workflow for any existing-PowerPoint beautification task.

## Absolute rule

**CONTENT LOCK is mandatory.**

Never rewrite, summarize, translate, spell-correct, add, delete, merge, split, or reorder source content. Only redesign the visual layer.

Before delivery:

1. snapshot source content,
2. perform visual-only redesign,
3. run layout QA,
4. run content verification,
5. deliver only when `CONTENT_LOCK_PASS=true`.

If a conflict exists between aesthetics and content fidelity, content fidelity wins.
