---
name: bw-start
description: Use when the user wants to start a bewater decision-phase project, resume without a known stage, or reconcile ambiguous or pending project state.
---

# bw-start

The entry point for bewater. You orient, reconcile, report status, and route — you never produce artifacts and never choose a gate exit (spec §4).

## When invoked

1. **No `_bewater/` in cwd** → bootstrap a project. Follow `references/state-bootstrap.md` verbatim: create the v5 tree, write the default config/ledger/conditions, create branch `BR-001` at `immersion`, set `active_branch`. Write state only through the §5.7 direct-write protocol (acquire `_bewater/.bw-lock` via bwkit, then `cas commit`).
2. **`_bewater/` exists** → reconcile before recommending anything (spec §4.6, §10.5):
   - read `config.yaml` (active branch/branches, stage, decision authority), `ledger.yaml`, `conditions.yaml`;
   - scan **open conditions** and **active-baseline validity**;
   - detect pending or manual-repair gate/backtrack action plans; if found, resume the idempotent recovery rather than starting new work;
   - if several branches are active and the user did not name one, **ask the human to choose before writing state**.
3. **Global / unspecified resume / ambiguous branch** → handled here; a request that names one stage and resolves to one branch routes to that stage's router.

## Routing precedence (§4)

(a) a direct, specific work request → the matching capability or gate;
(b) new project, global status, unspecified resume, pending recoverable action, or ambiguous branch → bw-start (here);
(c) one stage named + one branch → that stage's router.

Report the current stage and the next human decision, then stop. See `references/routing.md` and cite `../_bw-shared/ledger-schema.md` and `../_bw-shared/glossary.md` for field/term authority.
