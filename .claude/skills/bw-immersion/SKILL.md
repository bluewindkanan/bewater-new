---
name: bw-immersion
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Immersion.
---

# bw-immersion

A **router** for the Immersion stage (Start module). You orient, resume, report status,
and route "what next?" — you never produce artifacts (spec §4). Immersion aligns the team
on the proposition and seeds the first assumptions (bewater-core §5.0).

## On invoke

- Confirm the active branch's `current_stage` is `immersion`; if not, defer to bw-start.
- Report Immersion status: is there a project charter? are root assumptions seeded?
- Route the next action to **bw-project-charter** (draft/revise the charter, seed root
  assumptions) — see `references/stage.md`. Present the capability choice and stop when
  the next action is ambiguous.

Immersion is complete when stakeholders agree on proposition + success criteria and ≥3
initial assumptions exist (bewater-core §5.0). Hand off to Discover (`bw-discover`).
Cite `../_bw-shared/glossary.md`.
