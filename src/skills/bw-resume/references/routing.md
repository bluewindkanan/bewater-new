# Global resume routing

Use reads only. Never invoke a state-changing command from this router.

## Scan order

1. Read `_bewater/config.yaml`, `_bewater/ledger.yaml`,
   `_bewater/conditions.yaml`, and `_bewater/records/`; collect branch-applicable
   open conditions.
2. Verify active G1/G2 baseline pointers and their source decisions. Any
   active-baseline mismatch is a blocker.
3. Inspect gate and backtrack records for `pending` or `manual-repair` action
   plans. Derive ownership from persisted root fields and record type: root `gate`
   with `gate: G1` routes to **bw-strategy-gate**; `gate: G2` routes to
   **bw-concept-gate**; a backtrack record is identified by record type plus
   `backtrack_id` and routes to **bw-backtrack**. A single persisted recovery
   owner takes precedence over normal stage routing. A conflict between record
   type and root fields, corrupt data, or unknown ownership fails closed.
4. Inspect lifecycle heads before using the branch stage map.

## Ideate lifecycle scan

For the current branch, resolve all `idea-pool` and `concept-portfolio` revision
chains:

- zero Idea Pools → route to **bw-ideate** / **bw-concept-seed**;
- more than one Pool chain → corruption; fail closed;
- stale Pool `input_snapshot` → revise that Pool chain via **bw-concept-seed**;
- any OA with fewer than 10 Seeds, or an empty `shortlist.confirmed` → pending
  divergence or human shortlist checkpoint;
- zero Concept Portfolios after confirmed Seeds → route to
  **bw-concept-development**;
- more than one Portfolio chain → corruption; fail closed;
- Concepts awaiting refine/pivot/split/merge/kill/recycle or a human convergence
  decision → route to **bw-concept-development**;
- `exit.selected_concept_ids` outside 2–4, or any selected Concept whose hard
  criteria fail → Ideate is not handoff-ready.

Surface human checkpoints without writing them. Validate exact Pool, Seed,
Opportunity, and OA lineage; never infer identity from Markdown headings.

## Shape lifecycle scan

For `current_stage: shape`, verify the exact selected Concept Portfolio handoff
and inspect every current Solution chain:

- no Solution, invalid source Concept lineage, or an incomplete Solution with
  exact `content_gaps` → **bw-shape** / **bw-solution-shape**;
- unlisted omissions, unjustified applicability exceptions, invalid path, or
  body projection drift → fail closed and surface validation errors;
- open Solution assumptions or Achilles obligations → **bw-experiment**;
- complete but human-unvalidated Solution → pending validation checkpoint;
- complete validated Solution without the required narrative →
  **bw-investment-narrative**;
- 1–2 complete validated Solutions plus the narrative → **bw-concept-gate**.

Never set `validation_status: validated` or choose a G2 exit.

## Stage map

When no recovery or lifecycle checkpoint owns the next action:

| Current stage | Recommended skill |
| --- | --- |
| `immersion` | **bw-immersion** |
| `discover` | **bw-discover** |
| `define` | **bw-define** |
| `ideate` | **bw-ideate** |
| `shape` | **bw-shape** |

For `handoff-ready`, report `active_execution_handoff` and the next human
decision, then stop. Unknown stages fail closed.

Return current branch, current stage, blockers, next human decision, and exactly
one recommended skill or `none`. Never produce artifacts. Never choose a gate exit. Lifecycle contract:
`../_bw-shared/idea-concept-solution-lifecycle.md`.
