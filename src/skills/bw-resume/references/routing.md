# Global resume routing

## Scan order

Use only reads. Never invoke a state-changing command from this router.

1. **Open conditions** — collect every `status: open` entry in `conditions.yaml` that applies to
   the selected branch. Report each as a blocker to the affected gate.
2. **Active-baseline validity** — inspect `active_baselines.G1` and `active_baselines.G2` for the
   current branch. A missing referenced baseline, an invalidated source decision, or a branch
   mismatch is an active-baseline blocker.
3. **Pending recovery** — inspect gate and backtrack records under `_bewater/records/`. An
   `action_plan.action_status` of `pending` or `manual-repair` takes precedence over normal stage
   routing. Derive ownership from persisted root fields, never from a guessed action plan owner:
   a gate record's root `gate` field maps `gate: G1` → **bw-strategy-gate** and `gate: G2` →
   **bw-concept-gate**; a backtrack record is identified by its record type and `backtrack_id` and
   maps to **bw-backtrack**. A conflict between record type and root fields, or more than one
   recovery owner, fails closed. bw-resume does not execute the plan or write step status.

If any record is unknown, corrupt, contradictory, or lacks a single recovery owner, fail closed and
make manual inspection the next human decision.

## Stage map

When no pending recovery owns the next action, map the selected branch's `current_stage`:

| Current stage | Recommended skill |
| --- | --- |
| `immersion` | **bw-immersion** |
| `discover` | **bw-discover** |
| `define` | **bw-define** |
| `ideate` | **bw-ideate** |
| `shape` | **bw-shape** |

For `handoff-ready`, report `active_execution_handoff` and the next human decision, then stop
without recommending a decision-phase capability. Any other stage value is unknown and must fail
closed.

## Output contract

Return a compact status block with:

- current branch;
- current stage;
- blockers, including open conditions and invalid active baselines;
- next human decision;
- recommended skill, or `none` when routing fails closed or the branch is handoff-ready.

Never produce artifacts and never choose a gate exit.
