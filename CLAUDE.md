# Grit-CART Project

Research repo — not a code project. No build system, no tests, no dependencies.

## What This Is

Grit-CART framework research: Grok conversation → 5 parallel agent evaluations → synthesis → articles. All content is markdown/HTML.

## Current Focus

Project is complete. Both articles published, README has full framework summary.

## Key Files

- `README.md` — Framework summary with CART traits table, comparison table, ecosystem model
- `grok-conversation-grit-cart.md` — Source transcript (9 Grok exchanges)
- `evaluations/` — 5 agent evaluations + synthesis
- `growth-mindset-grit-research-notes.md` — 6th agent deep dive (human-triggered)
- `articles/2026-02-15-from-tweet-to-treatise.md` — Main article (process narrative)
- `articles/2026-02-15-universal-paste-pattern.md` — Meta article (publishing automation)
- `articles/generate_covers.py` — PIL script for cover images (3 sizes)

## Publishing

Articles were published to Substack, LinkedIn, and Twitter using browser automation skills:
- `/publish-to-substack` — ProseMirror, execCommand title, heading merge fix
- `/publish-to-linkedin` — ProseMirror, H2→H3, no X embed
- `/publish-to-twitter` — DraftJS, 100-char title limit, ~1000 words

All use the universal paste pattern (ClipboardEvent with text/html). Tables must be pre-converted to `<ul>`.

## Session Log

| Date | Summary |
|------|---------|
| 2026-02-15 | Initial research session: Grok extraction, 5-agent evaluation, synthesis, growth mindset deep dive, article, cross-platform publishing, 3 publishing skills created |
| 2026-02-15 | Meta article session: wrote Universal Paste Pattern article, cover images, README expanded with framework summary tables |
