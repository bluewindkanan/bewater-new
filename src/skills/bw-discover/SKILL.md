---
name: bw-discover
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Discover.
---

# bw-discover

A **router** for the Discover stage. Orient, resume, report status, and route; never produce
artifacts. Discover turns facts into insights and closes directional hypotheses.

## On invoke

- Confirm `current_stage` is `discover`.
- Report Discover status: 4C coverage, insight count/quality, learning-plan state.
- Route to **bw-4c-research** (plan/run/synthesize 4C + learning plan) and
  **bw-insight-craft** (facts→insights, F/P/E/T judgment). Present the choice and stop
  when ambiguous.

Discover hands directional hypotheses to Define (`bw-define`). Cite
`../_bw-shared/gate-criteria.md` (insight readiness).
