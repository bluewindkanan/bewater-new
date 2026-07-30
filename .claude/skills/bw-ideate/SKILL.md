---
name: bw-ideate
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Ideate.
---

# bw-ideate

A **router** for the Ideate stage (Concept module). Orient/resume/status/route; never
produce artifacts (spec §4). Ideate broadens each opportunity area into many early concepts
and narrows by standard (bewater-core §5.2.1).

## On invoke

- Confirm `current_stage` is `ideate`.
- Report Ideate status: concept count per opportunity area, convergence progress.
- Route to **bw-concept-card** (generate/complete/evaluate/converge concepts) — see
  `references/stage.md`. Present the choice and stop when ambiguous.

The concept convergence checkpoint (Ideate → Shape) is a lightweight self-check, not a gate:
≥3 concepts expressible in ≤5 words, ≥2 provoke healthy anxiety, all pass the strategy
filter. Hand the concept portfolio to Shape (`bw-shape`). Cite `../_bw-shared/glossary.md`.
