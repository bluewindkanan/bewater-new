---
name: bw-concept-development
description: Use when the user wants to develop confirmed Idea Seeds into researchable BeWater Concepts and prepare a bounded convergence batch.
---

# bw-concept-development

A **capability** for the convergent half of Ideate. Develop **every**
human-confirmed Idea Seed into a researchable Concept in the one branch-global
Concept Portfolio, obtain an independent Concept review, and present one batch
comparison. Production and review are separate responsibilities. You propose;
an independent reviewer evaluates and recommends; the accountable human decides.

## Workflow

1. Resolve the exact `idea-pool` head and require a matching human checkpoint
   with 5–8 confirmed Seeds in every OA. Resolve its exact `strategy_ref` and
   `opportunity_ref`; the Concept Portfolio must pin those same revisions. Stop
   if any OA is outside 5–8. When the Pool uses `recommended_cuts`, require its
   `review.status: ready`; missing or `needs-revision` review routes back to
   **bw-concept-seed**.
2. Find the branch's existing `concept-portfolio` chain. Revise it when upstream
   inputs or Concepts change; never create a second Portfolio chain.
3. Develop **all** confirmed Seeds into canonical `concepts[]` per
   `references/concept-portfolio-template.md`. Allocate stable, portfolio-local
   `CI-NNN` IDs and record exact `opportunity_area_id` + `source_seed_id`.
   Every confirmed Seed produces exactly one initial Concept and every initial
   Concept resolves one confirmed Seed in the same OA. Reject missing,
   duplicate, unconfirmed, or cross-OA lineage. Human-created merges and splits
   preserve their parent history and are not a loophole in the initial 1:1 set.
4. Fill the researchable-proposition fields without expanding into full
   Solution implementation or financial-case detail. `pithy_description` is
   five words or fewer where the language permits; `how_it_works` stays at
   mechanism altitude. Write `visualization` as one picture-in-words sentence
   and provide `visualization_spec` (one `screen` per key moment, each with a
   short `caption` and 1–4 `bullets`) so the reader renders a deterministic
   SVG wireframe.
5. Do not evaluate the Concepts you produced. Delegate the exact candidate
   Portfolio to a **fresh-context independent reviewer** under
   `references/concept-review-contract.md`. The reviewer receives only the
   exact candidate and its referenced inputs, cannot mutate project state, and
   returns the review payload. If isolated delegation is unavailable, stop and
   report the missing independent review; producer self-review is not a
   substitute.
6. Create Concept-layer ledger assumptions derived from the exact Portfolio
   revision with validated `source_concept_id`; pin them as
   `assumption:A-NNN@record_revision`. Never embed or duplicate assumption
   records in the Portfolio.
7. Apply the review's content findings without copying reviewer prose into
   human-only fields, then return the revised candidate to a fresh-context
   independent reviewer for verification. Run at most two review-and-revision
   cycles. The reviewer owns every Concept's `evaluation.hard`,
   `evaluation.soft`, and `recommended_action`; allowed actions are `refine`,
   `pivot`, `split`, `merge`, `kill`, or `recycle-to-OA`. Route
   `recycle-to-OA` through **bw-backtrack**.
8. Persist one reviewed Artifact revision with batch `review`, reviewer-owned
   evaluations, and the complete active candidate set. Use
   `review.status: ready` only when `reviewed_concept_ids` exactly covers every
   current candidate. After at most two cycles, record remaining material
   findings honestly as `review.status: needs-revision` and stop; do not present
   the human convergence decision as ready.
9. When `review.status: ready`, present one OA-grouped batch comparison and the
   full Concepts, then stop before the human decision.

## After the human decision

Append the next Portfolio revision. Only explicit human input may populate
`selected`, `killed`, or `merged` in `decisions[]` and each Concept's terminal
fields. Populate `exit.selected_concept_ids` with 2–4 selected `CI-NNN` IDs.
The independent reviewer is also barred from these human-only fields, including
`decision`, `merge_into`, and `exit.selected_concept_ids`. A human-approved new
merge or split is reviewed before it can be selected.

Legacy Concept Portfolios whose exact Idea Pool uses
`shortlist.recommended` remain readable and are labelled not reviewed under the
new contract. Do not infer missing evaluations, findings, or readiness. A new
Portfolio whose Idea Pool uses `recommended_cuts` must follow this review flow.

This is a capability checkpoint, not a gate. Field semantics:
`../_bw-shared/ledger-schema.md`; lifecycle contract:
`../_bw-shared/idea-concept-solution-lifecycle.md`.
