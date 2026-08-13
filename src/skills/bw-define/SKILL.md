---
name: bw-define
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Define.
---

# bw-define

A **router** for the Define stage. Orient, resume, report status, and route; never produce
artifacts. Define begins with research evidence from Discover, crafts insights (F/P/E/T), then
refines them into an innovation strategy and opportunity areas before G1.

## On invoke

- Confirm `current_stage` is `define`.
  - If `current_stage` is `discover` and research is at Insight Readiness: report that the
    stage must advance to `define` before Define capabilities can run. Present the choice to
    advance the stage (human decision → CAS commit `current_stage: define`) and stop.
  - If `current_stage` is any other value: defer to `bw-resume`.
- Report Define status: insights signed? directional hypotheses closed? strategy selected/locked?
  opportunity portfolio (2–4)? assumption initial inventory + Achilles-Heel quadrant? Money+Magic
  initial judgment?
- If no current insights are signed, route first to **bw-insight-craft**. If insights exist but no
  directional hypothesis is closed, route to **bw-directional-hypothesis**. Otherwise route to the
  remaining Define capabilities (see `references/stage.md`). If the G1 inventory or Achilles review
  is incomplete, route to **bw-assumption-map** even when Research projected zero assumptions.
  When the subject is G1-ready or a
  deadline has fallen, route to **bw-strategy-gate**. Present the choice and stop when ambiguous.

Define completes at the G1 gate decision. Use `../_bw-shared/gate-criteria.md`.
