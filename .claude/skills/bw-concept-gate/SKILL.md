---
name: bw-concept-gate
description: Use when the user asks for G2 readiness or a concept-gate decision after Shape.
---

# bw-concept-gate

The **G2 / concept gate** — a constrained adjudicator (spec §6). You assemble evidence, present the
five permitted exits, stop for the accountable human, then write and apply the chosen action. **You
never choose an exit** (§6.2). G2 authority is **investment-decision** level — one level above G1's
product-owner.

## Flow (§6.2 — identical shape to G1)

1. Resolve the branch, subject references (1–2 validated solutions + the investment narrative), the
   single accountable investment-decision person, the trigger, and input revisions.
2. Reconcile pending or manual-repair prior gate/backtrack actions (resume idempotently).
3. Evaluate each G2 criterion pass/fail/unknown against `../_bw-shared/gate-criteria.md`; separate
   structural, hard-evidence (L4+), and human-judgment criteria. Run `bwkit check integrity` on the
   subject artifacts first; stop on corruption.
4. Display open conditions, current Achilles Heels, open historical L4 obligations.
5. Present only the methodology-permitted exits and the exact action for each
   (`references/exits.md`).
6. **Stop for the accountable human.** If the G2 accountable person is null/ambiguous or below
   investment-decision level, render a readiness report and stop without a decision record.
7. Preallocate every ID; write the complete decision record + action plan with `action_status:
   pending` BEFORE any other state change (`references/decision-record-template.md`,
   `references/action-plan.md`).
8. Apply the action via `bwkit plan apply` (idempotent, resumable); record each step
   applied/skipped/failed.
9. Verify resulting state, show the diff, then mark `action_status: applied`. Conflicts go to
   `manual-repair`, never silent pending.

The non-delegable rule (§6.3, §6.7): human judgment resolves qualitative criteria; it cannot relabel
L1–L3 evidence as L4, waive a missing required artifact, or record `exit: go` while a required G2
criterion fails.
