# Routing and reconcile procedure

## Before recommending downstream work, scan

1. **Open conditions** in `conditions.yaml` — any `status: open` condition blocks the
   next gate and must be surfaced.
2. **Active-baseline validity** — for the active branch, read `active_baselines.G1/G2`;
   if a referenced baseline file is missing or its source decision is `invalidated`,
   the branch is needs-rebase and no gate may proceed.
3. **Pending / manual-repair actions** — read gate and backtrack records under
   `_bewater/records/`; if any `action_plan.action_status` is `pending` or
   `manual-repair`, resume idempotent recovery (verify each ordered step applied or
   intentionally skipped) before new work.

## Direct-write protocol (every state write)

Announce target files → acquire `_bewater/.bw-lock` (`bwkit lock acquire`) → read current
revisions → mutate only intended records preserving unknown fields → `bwkit cas commit
<path> --expected <rev>` with bumped text on stdin → re-read and verify.
On revision conflict, stop without writing and request a manual merge. One active
bewater writer per project.

## Decision authority

A gate cannot record a decision while its single accountable person is null or ambiguous.
Surface this during reconcile; do not invent a decision maker.

