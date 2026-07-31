---
name: bw-shape
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Shape.
---

# bw-shape

A **router** for the Shape stage. Orient, resume, report status, and route; never produce artifacts.
Shape develops selected concepts into validated dual-sided solutions with business cases and
investment narratives, and plans L4+ behavioral experiments for each Achilles Heel.

## On invoke

- Confirm `current_stage` is `shape`.
- Report Shape status: which concepts are being shaped, open experiments + their Kill/Proceed state,
  Achilles-Heel / open-L4 resolution progress, count of solutions at `validated` status.
- Route to the matching capability — see `references/stage.md`. Present the choice and stop when
  ambiguous. When G2 readiness is met, point to **bw-concept-gate**.

bw-start and this router scan open conditions and active-baseline validity before recommending
downstream work.
