---
name: bw-resume
description: Use when the user wants to resume or continue without naming a stage, requests global or cross-stage status, returns after interrupted work, faces ambiguous branches, or explicitly invokes bw-resume at any time.
---

# bw-resume

A global, read-only **router** for an initialized BeWater project. It reports project state and the
next human decision, then recommends exactly one downstream skill when the state supports that
recommendation. It never produces artifacts, never chooses a gate exit, and never writes state.

## Invocation boundary

- A direct, specific capability or gate request bypasses this router and goes to that skill.
- An unspecified resume or continue request, global or cross-stage status request, interrupted
  session, or ambiguous branch is handled here. The user may also invoke this skill explicitly at
  any time.
- A request that names one stage and resolves to one branch goes directly to that stage router.

## On invoke

1. Read `_bewater/config.yaml`, `_bewater/ledger.yaml`, `_bewater/conditions.yaml`, and
   `_bewater/records/`. If the initialized state is absent, incomplete, unreadable, or internally
   inconsistent, report that deployment or project status is incomplete and stop. Do not create or
   repair state.
2. Resolve the branch. If there are multiple active branches and the user did not identify one,
   report the candidates and ask the human to choose before continuing. Do not write a selection.
3. Scan blockers and pending work before normal stage routing by following
   `references/routing.md`.
4. Report the current branch, current stage, blockers, next human decision, and recommended skill.
   If no safe recommendation exists, say so and stop.

Unknown stages, malformed records, corrupt state, and conflicting recovery ownership fail closed.
This router does not execute an action plan, does not write state, and does not produce a draft
artifact.
