# pptx-beautify-lock-Skill

A cross-agent **PowerPoint visual redesign skill with a hard content lock**.

> Preserve presentation content exactly. Redesign only the visual layer.

This repository is designed for AI coding agents such as **Claude Code, ChatGPT/Codex, and other Agent-Skills-compatible tools** that can access a `.pptx`, edit files, and run code.

## Core contract

The source `.pptx` is the single source of truth.

### Frozen content — MUST NOT change

- slide count and slide order
- all visible text, punctuation, numbers, units, formulas, symbols, and language
- table structure, merged-cell semantics, row/column order, and cell values
- chart categories, series names, source values, formulas, and embedded workbook data
- image/media bytes and image crop state
- speaker-note text
- embedded files and media payloads

The agent must never rewrite, summarize, translate, spell-correct, delete, add, merge, split, or reorder content just to make a slide easier to lay out.

### Visual layer — MAY change

- font family, size, weight, color
- text box size, margins, paragraph spacing, line spacing, alignment
- object position and size
- whitespace and grid alignment
- table row/column sizing and visual styling
- chart styling that does not change chart data
- fills, borders, shadows, backgrounds, accents, hierarchy
- image position and size while preserving the actual image and crop state
- slide-level composition
- accidental overlap, overflow, clipping, and out-of-bounds defects

## Fail-closed rule

If content cannot fit, **do not rewrite it**. The AI must instead change layout, resize regions, reduce padding, redistribute whitespace, or reduce font size within readability limits.

The final deck is accepted only if automated verification reports:

```text
CONTENT_LOCK_PASS=true
```

## Important limitation

Pasting this GitHub URL into an AI does **not** itself grant file-system access or PowerPoint-editing tools. The AI still needs access to the input `.pptx` and a way to edit files/run code. This repository exists so capable agents can discover and follow one strict workflow instead of improvising.

## Repository layout

```text
.
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── AI_BOOTSTRAP.md
└── pptx-beautify-lock/
    ├── SKILL.md
    ├── references/
    │   ├── CONTENT_LOCK.md
    │   ├── DESIGN_RULES.md
    │   └── QA_RULES.md
    └── scripts/
        ├── pptx_content_lock.py
        └── verify_layout.py
```

## Fastest use: paste this repo URL + attach a PPTX

Use this instruction:

```text
Read this repository and follow pptx-beautify-lock/SKILL.md.
Beautify the attached PPTX with CONTENT LOCK enabled.
Do not modify any content. Redesign only the visual layer.
Run content verification and visual/layout QA before delivery.
Only deliver when CONTENT_LOCK_PASS=true.
```

## Install as an Agent Skill

The installable skill is the `pptx-beautify-lock/` directory. It follows the open Agent Skills convention: `SKILL.md` plus optional `scripts/`, `references/`, and `assets/` resources.

- **Claude Code**: install/link the `pptx-beautify-lock/` directory into the Skills location supported by your Claude Code version, or open this repository directly and let `CLAUDE.md` route the agent to the Skill.
- **ChatGPT/Codex**: install the `pptx-beautify-lock/` directory through the Skills mechanism supported by your environment, or open this repository directly and let `AGENTS.md` route Codex to the Skill.

## Mandatory pipeline

```text
input.pptx
   ↓
immutable backup
   ↓
content snapshot / manifest
   ↓
render + inspect original slides
   ↓
visual-only redesign
   ↓
layout QA + render QA
   ↓
content verification
   ↓
PASS → final.pptx
FAIL → reject output and repair
```

Prompt-only promises are not enough for a 100% content-lock objective. The bundled verifier compares semantic content-bearing structures while intentionally ignoring permissible visual-format changes.

## Design objective

The skill is allowed to redesign aggressively. It should target executive-quality visual consistency, not merely move objects until warnings disappear. A valid result must be both:

1. **semantically identical**, and
2. **materially better designed**.

## License

MIT.
