---
name: bw-solution-shape
description: Use when the user wants to shape or revise selected concepts into validated dual-sided solutions.
---

# bw-solution-shape

A **capability** that develops selected concepts into validated dual-sided solutions. You shape
candidates and stop before the human's validation or Kill/Proceed choice. A G2-ready subject
carries one or two solutions at `validated` status.

## Workflow

1. Consume the Ideate `concept-portfolio` handoff (2–4 selected Concept Items).
   Carry each selected concept → solution via the bounded paths (`linear-refine`,
   `pivot`, `hybridize`, `scope-extend`; do not invent outside the selected Concept boundary)
   using `references/solution-template.md`,
   and record the exact portfolio revision plus the source Concept Item id on
   each concept→solution path (`derived_from` the portfolio; body carries the
   `CI-` id). Shape never reselects or invents concepts.
2. Fill the dual-sided solution (Magic: consumer_value_proposition + consumer_target; Money:
   commercial_value_proposition + leverageable_assets; tension; balance_choice) and attach a
   business case + traceable evidence. Achilles Heels must be resolved by L4+ experiments
   (bw-experiment) before a solution can be `validated`.
3. Write solution artifacts (`_bewater-output/ART-xxx-rN-solution.md`, `kind: solution`,
   `stage: shape`) via bwkit. Validate the revision chain with `bwkit check integrity`.
4. Use exact `content_gaps` and `applicability_exceptions` fields when a draft is incomplete.
5. Present 1–2 candidates + evidence, name the human decision authority, and **stop**. Setting
   `validation_status: validated` is a human judgment: the Solution is Focused, Detailed,
   Persuasive, and makes it impossible not to invest.
