---
name: bw-backtrack
description: Use when an assumption is falsified or an artifact changes and the project must route the correct baseline-aware backtrack loop.
---

# bw-backtrack

A **capability** for baseline-aware backtracking. On a falsified assumption or a changed artifact
revision, compute downstream impact, classify the loop size, propose routing, and stop for the
accountable human. Never silently edit a confirmed baseline or auto-apply a plan.

## Workflow

1. Identify the trigger (a falsified assumption or changed artifact) — `trigger_ref`.
2. **Build the lineage edge model** from the four edge kinds (`references/lineage.md`) and call
   `lineage.transitive_dependents(edges, [trigger_ref])` → the transitive `affected_refs` + per-node
   depth (backtrack-depth proxy). Run `bwkit check integrity` on the subject first; stop on
   corruption.
3. **Classify loop size** by inspecting the branch's `active_baselines` pointers
   (`references/loop-size.md`): if the change touches a baseline item → **large** loop (the original
   gate must rerun); otherwise a feature/concept change may be a **small** local reframe.
4. Assemble the BT-record + ordered action plan (`references/backtrack-record-template.md`). A
   large-loop plan orders: invalidate affected gate decisions → clear affected active-baseline
   pointers → archive any active execution handoff → append stale/invalidated artifact revisions →
   change branch stage → THEN schedule gate reruns.
5. Preallocate IDs; write the BT-record with `action_status: pending` BEFORE other state change;
   present the proposed routing + evidence, name the accountable human, and **stop**. After
   confirmation, apply via `bwkit plan apply`; record step statuses back. `bw-start` reconciles a
   pending/manual-repair backtrack with the same idempotent recovery as a gate action.

Routing by change depth: root premise → Discover + G1 recertify; opportunity/strategy →
Define + G1; feature/concept (no baseline touched) → Ideate/Shape local reframe.
