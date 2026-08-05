---
name: bw-define
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Define.
---

# bw-define

A **router** for the Define stage. Orient, resume, report status, and route; never produce
artifacts. Define turns insights into an innovation strategy and opportunity areas before G1.

## On invoke

- Confirm `current_stage` is `define`.
- Report Define status: directional hypotheses closed? strategy selected/locked? opportunity
  portfolio (2–4)? assumption initial inventory + Achilles-Heel quadrant? Money+Magic
  initial judgment?
- If no current directional hypothesis is closed, route first to **bw-directional-hypothesis**.
  Otherwise route to the remaining Define capabilities (see `references/stage.md`); when the
  subject is G1-ready or a deadline has fallen, route to **bw-strategy-gate**. Present the choice
  and stop when ambiguous.

Define completes at the G1 gate decision. Use `../_bw-shared/gate-criteria.md`.
