---
name: bw-concept-development
description: Use when the user wants to develop confirmed Idea Seeds into researchable BeWater Concepts and prepare a bounded convergence batch.
---

# bw-concept-development

A **capability** for the convergent half of Ideate. Develop **every**
human-confirmed Idea Seed into a researchable Concept in the one branch-global
Concept Portfolio, evaluate them, and present one batch comparison. There is no
per-OA cap on how many confirmed Seeds are developed: selection of 2–4 Concepts
is the only convergence cut in Ideate, and it happens here at the rich-Concept
layer — never earlier at the one-line Seed layer. You propose and recommend;
the accountable human decides.

## Workflow

1. Resolve the exact `idea-pool` head and require human-confirmed Seeds. Resolve
   its exact `strategy_ref` and `opportunity_ref`; the Concept Portfolio must pin
   those same revisions.
2. Find the branch's existing `concept-portfolio` chain. Revise it when upstream
   inputs or Concepts change; never create a second Portfolio chain.
3. Develop **all** confirmed Seeds into canonical `concepts[]` per
   `references/concept-portfolio-template.md`. Allocate stable, portfolio-local
   `CI-NNN` IDs and record exact `opportunity_area_id` + `source_seed_id`.
   Reject a Concept whose Seed is unconfirmed or belongs to another OA group.
4. Fill the researchable-proposition fields without expanding into full
   Solution implementation or financial-case detail. `pithy_description` is
   five words or fewer where the language permits; `how_it_works` stays at
   mechanism altitude.
5. Evaluate hard criteria (exact lineage, one unresolved tension, distinct
   mechanism, Who/What/How/What it replaces/Why Big, strategy fit, useful
   pretest altitude, and Concept assumptions) and soft criteria
   (comprehension, credibility, appeal, differentiation, naming, visualization,
   design principles, Money/Magic, altitude, and healthy anxiety).
6. Create Concept-layer ledger assumptions derived from the exact Portfolio
   revision with validated `source_concept_id`; pin them as
   `assumption:A-NNN@record_revision`. Never embed or duplicate assumption
   records in the Portfolio.
7. Recommend exactly one action per Concept: `refine`, `pivot`, `split`,
   `merge`, `kill`, or `recycle-to-OA`. Route `recycle-to-OA` through
   **bw-backtrack**. A merge creates a new `CI-NNN` carrying
   both parents. Stop after two AI revision proposals unless the human
   explicitly asks for another pass.
8. Present one batch convergence view and stop before the human decision.

## After the human decision

Append the next Portfolio revision. Only explicit human input may populate
`selected`, `killed`, or `merged` in `decisions[]` and each Concept's terminal
fields. Populate `exit.selected_concept_ids` with 2–4 selected `CI-NNN` IDs.

This is a capability checkpoint, not a gate. Field semantics:
`../_bw-shared/ledger-schema.md`; lifecycle contract:
`../_bw-shared/idea-concept-solution-lifecycle.md`.
