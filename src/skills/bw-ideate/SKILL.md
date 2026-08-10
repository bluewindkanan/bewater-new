---
name: bw-ideate
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Ideate.
---

# bw-ideate

A **router** for the Ideate stage. Orient, resume, report status, and route; never produce
artifacts. Ideate runs an explicit concept lifecycle: each opportunity area is
diverged into a seed pool, then a single concept portfolio is developed,
evaluated, and converged.

## On invoke

- Confirm `current_stage` is `ideate`.
- Report Ideate status across the lifecycle — see `references/stage.md`:
  - seed counts per opportunity area and shortlist confirmation state;
  - concept lifecycle states (developed / evaluated / needs-revision);
  - revision blockers (a concept at the two-proposal cap awaiting recycle-to-OA);
  - portfolio readiness (whether `exit.selected_concept_ids` holds 2–4).
- Route to the matching capability and stop when ambiguous:
  - diverge or revise a seed pool → **bw-concept-seed**;
  - develop, evaluate, revise, or converge concepts → **bw-concept-development**.

The Ideate → Shape handoff is the `concept-portfolio` with 2–4 selected concepts
(`exit.selected_concept_ids`), each with `decision: selected` and hard criteria
passing. It is a lightweight readiness check, not a gate. Hand the portfolio to
Shape (`bw-shape`).
