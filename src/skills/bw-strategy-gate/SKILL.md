---
name: bw-strategy-gate
description: Use when the user asks for G1 readiness or a strategy-gate decision after Define.
---

# bw-strategy-gate

The **G1 / strategy gate** assembles evidence, presents the five permitted exits, stops for the
accountable human, then writes and applies the chosen action. **You never choose an exit.**

## Flow

1. Resolve the branch, subject references, the single accountable person, the trigger
   (event-driven or `gate_due_at.G1` deadline), and input revisions.
2. Reconcile pending or manual-repair prior gate/backtrack actions (resume idempotently).
3. Evaluate each G1 criterion pass/fail/unknown against `../_bw-shared/gate-criteria.md`;
   count the 2–4 canonical `opportunity_areas[]` entries in the one current Opportunity Portfolio
   head, never separate Opportunity files. Separate structural, hard-evidence, and human-judgment
   criteria.
4. Display open conditions, current Achilles Heels, historical L4 obligations.
5. Use `AskUserQuestion` to present only the methodology-permitted exits and the exact action
   for each (`references/exits.md`). Include the current G1 criteria status, open conditions,
   Achilles Heels, and any L4 obligations. Each exit option must clearly state what action will
   be taken. If the permitted exits outnumber the host question tool's option limit, present the
   exits as text and stop; a tool cap must never hide a permitted exit.
6. **Stop for the accountable human.** If the G1 accountable person is null/ambiguous or
   below product-owner level, render a readiness report and stop without a decision record.
7. Preallocate every ID; write the complete decision record + action plan with
   `action_status: pending` BEFORE any other state change
   (`references/decision-record-template.md`, `references/action-plan.md`).
8. Apply the action via `bwkit plan apply` (idempotent, resumable); record each step
   applied/skipped/failed.
9. Verify resulting state, show the diff, then mark `action_status: applied`. Conflicts go
   to `manual-repair`, never silent pending.

The non-delegable rule: human judgment resolves qualitative criteria; it
cannot relabel missing G1 evidence as satisfied or record `exit: go` while a required
criterion fails.
