# AI Bootstrap

Use this file when an AI assistant is given only the repository URL.

## Task routing

If the task involves an existing `.pptx` and the user wants it prettier without changing content:

1. Read `pptx-beautify-lock/SKILL.md` completely.
2. Read all referenced files it marks as mandatory.
3. Treat the source PPTX as immutable source-of-truth content.
4. Create a semantic snapshot before editing.
5. Redesign only the visual layer.
6. Run layout QA and content-lock verification.
7. Do not deliver unless verification passes.

## Canonical user shorthand

The following should activate the skill:

- "beautify this PPT without changing content"
- "fix this ugly deck"
- "repair PPT layout only"
- "content lock"
- "visual redesign only"
- "keep all text/data/images exactly the same"

## Safety behavior

When the agent lacks the ability to inspect/edit PPTX files or execute the verifier, it must state that limitation rather than claiming that the deck has been safely beautified.
