---
name: bw-concept-gate
description: Use when the user asks for G2 readiness or a concept-gate decision after Shape.
---

# bw-concept-gate

The **G2 / concept gate** assembles evidence, presents the five permitted exits, stops for the
accountable human, then writes and applies the chosen action. **You never choose an exit.** G2
authority is **investment-decision** level — one level above G1's product-owner.

## Flow

1. Resolve the branch, subject references (1–2 complete validated Solutions + the investment narrative), the
   single accountable investment-decision person, the trigger, and input revisions.
2. Reconcile pending or manual-repair prior gate/backtrack actions (resume idempotently).
3. Evaluate each G2 criterion pass/fail/unknown against `../_bw-shared/gate-criteria.md`; reuse the
   shared Solution completeness, Focused/Detailed/Persuasive, projection, financial provenance,
   and Achilles-union predicates rather than judging a narrative shell. Separate structural,
   hard-evidence (L4+), and human-judgment criteria. Run `bwkit check integrity` on the subject
   artifacts first; stop on corruption.
4. Display open conditions, current Achilles Heels, open historical L4 obligations.
5. Use `AskUserQuestion` to present only the methodology-permitted exits and the exact action
   for each (`references/exits.md`). Include the current G2 criteria status, open conditions,
   Achilles Heels, and any L4 obligations. Each exit option must clearly state what action will
   be taken. If the permitted exits outnumber the host question tool's option limit, present the
   exits as text and stop; a tool cap must never hide a permitted exit.
6. **Stop for the accountable human.** If the G2 accountable person is null/ambiguous or below
   investment-decision level, render a readiness report and stop without a decision record.
7. Preallocate every ID; write the complete decision record + action plan with `action_status:
   pending` BEFORE any other state change (`references/decision-record-template.md`,
   `references/action-plan.md`).
8. Apply the action via `bwkit plan apply` (idempotent, resumable); record each step
   applied/skipped/failed.
9. Verify resulting state, show the diff, then mark `action_status: applied`. Conflicts go to
   `manual-repair`, never silent pending.

The non-delegable rule: human judgment resolves qualitative criteria; it cannot relabel L1–L3
evidence as L4, waive a missing required artifact, or record `exit: go` while a required criterion fails.
