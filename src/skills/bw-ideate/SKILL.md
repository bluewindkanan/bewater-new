---
name: bw-ideate
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Ideate.
---

# bw-ideate

A **router** for the Ideate stage. Orient, resume, report status, and route; never produce
artifacts. Ideate runs an explicit concept lifecycle: each opportunity area is
diverged into a seed pool, then a single concept portfolio is developed,
independently reviewed, and converged.

## On invoke

- Confirm `current_stage` is `ideate`.
- Report Ideate status across the lifecycle — see `references/stage.md`:
  - the 10–15 Seed count, Idea Pool review, recommended-cut complement, and
    5–8 human-confirmed IDs for every Opportunity Area;
  - Concept production and independent Concept review states, including
    `review.status: ready | needs-revision` and candidate coverage;
  - revision blockers (a concept at the two-proposal cap awaiting recycle-to-OA);
  - portfolio readiness (whether `exit.selected_concept_ids` holds 2–4).
- Route to the matching capability and stop when ambiguous:
  - diverge or revise a seed pool → **bw-concept-seed**;
  - develop, evaluate, revise, or converge concepts → **bw-concept-development**.

The Ideate → Shape handoff is the `concept-portfolio` with 2–4 selected concepts
(`exit.selected_concept_ids`), each with `decision: selected` and hard criteria
passing. A new-contract Portfolio, identified by its exact Idea Pool's
`recommended_cuts`, also requires `review.status: ready`. A legacy Portfolio is
reported as not reviewed under the new contract; do not infer missing review
results. This is a lightweight readiness check, not a gate. Hand the portfolio
to Shape (`bw-shape`).
