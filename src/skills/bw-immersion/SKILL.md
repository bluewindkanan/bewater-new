---
name: bw-immersion
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Immersion.
---

# bw-immersion

A **router** for the Immersion stage. You orient, resume, report status, and route "what next?";
you never produce artifacts. Immersion aligns the team on the proposition and seeds root assumptions.

## On invoke

- Confirm the active branch's `current_stage` is `immersion`; if not, defer to bw-start.
- Report Immersion status: is there a project charter? are root assumptions seeded?
- Route the next action to **bw-project-charter** (draft/revise the charter, seed root
  assumptions) — see `references/stage.md`. Present the capability choice and stop when
  the next action is ambiguous.

Immersion is complete when stakeholders agree on proposition and success criteria and at least three
initial assumptions exist. Hand off to Discover (`bw-discover`).
