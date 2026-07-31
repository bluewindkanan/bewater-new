---
name: bw-start
description: Use when the user wants to start a bewater decision-phase project, resume without a known stage, or reconcile ambiguous or pending project state.
---

# bw-start

The entry point for bewater. You orient, reconcile, report status, and route; you never produce
artifacts or choose a gate exit.

## When invoked

1. **No `_bewater/` in cwd** → bootstrap a project. Follow `references/state-bootstrap.md`: create
   the tree, write the default config/ledger/conditions, create branch `BR-001` at `immersion`, and
   set `active_branch`. Acquire `_bewater/.bw-lock` through bwkit, then commit state with CAS.
2. **`_bewater/` exists** → reconcile before recommending anything:
   - read `config.yaml` (active branch/branches, stage, decision authority), `ledger.yaml`, `conditions.yaml`;
   - scan **open conditions** and **active-baseline validity**;
   - detect pending or manual-repair gate/backtrack action plans; if found, resume the idempotent recovery rather than starting new work;
   - if several branches are active and the user did not name one, **ask the human to choose before writing state**.
3. **Global / unspecified resume / ambiguous branch** → handled here; a request that names one stage and resolves to one branch routes to that stage's router.

## Routing precedence

(a) a direct, specific work request → the matching capability or gate;
(b) new project, global status, unspecified resume, pending recoverable action, or ambiguous branch → bw-start (here);
(c) one stage named + one branch → that stage's router.

Report the current stage and the next human decision, then stop. Use `references/routing.md` and
`../_bw-shared/ledger-schema.md`.
