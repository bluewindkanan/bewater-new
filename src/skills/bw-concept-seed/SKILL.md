---
name: bw-concept-seed
description: Use when the user wants to diverge raw BeWater Idea Seeds across the Opportunity Portfolio and recommend development shortlists.
---

# bw-concept-seed

A **capability** for the divergent half of Ideate. Create or revise the one
branch-global Idea Pool, diverge raw Idea Seeds under every Opportunity Area,
run a lightweight Idea Pool review, recommend explicit OA-level cuts, and stop
for human confirmation. You recommend; the accountable human confirms. Never
hide a Seed you would rather cut.

## Workflow

1. Resolve the active branch, exact locked `strategy` revision, and exact
   `opportunity` revision. The Opportunity Portfolio must expose 2–4 canonical
   `opportunity_areas[]` with stable `OA-NNN` IDs.
2. Find the branch's existing `idea-pool` chain. If one exists, revise that
   chain. If its strategy or Opportunity input changed, record the new exact
   refs in `input_snapshot` on the next revision. Never create a second Pool
   chain for the branch.
3. For every OA, diverge 10–15 Seeds using brainstorm + “how might we”. This is
   a hard range: fewer than 10 requires further divergence and more than 15
   requires consolidation or replacement before the candidate revision is
   ready. Allocate
   `CS-NNN` IDs pool-wide, preserve them for the same Seed across revisions, and
   never reassign or reuse an ID.
4. Capture each Seed per `references/idea-pool-template.md`: one required `idea`
   sentence plus source-insight lineage. `cluster_id` and `strategy_filter` are
   system annotations, not developed Concept content.
5. Cluster near-duplicates (assign `cluster_id`) but keep every Seed visible,
   including duplicates, failed filters, and non-shortlisted items. `cluster_id`
   and `strategy_filter` are system annotations shown to the human as cut
   evidence, not developed Concept content.
6. Run the lightweight Idea Pool review as a batch check inside this capability.
   Check OA relevance, mechanism breadth, cosmetic variants, Strategy fit,
   one-sentence Seed altitude, source-Insight lineage, and whether the proposed
   cuts leave a credible comparison set. Do not perform Concept-level commercial
   feasibility analysis. Record `review.status`, `iterations`, and batch
   `findings`. If fewer than five credible Seeds remain, improve or replace weak
   Seeds; if the batch still cannot support a decision, record
   `review.status: needs-revision` and stop.
7. Recommend **elimination** separately for each OA in
   `shortlist.recommended_cuts`. Each cut is an object with the Seed ID, one
   reason code, and a required rationale. The allowed reasons are `duplicate`,
   `weak-distinctiveness`, `oa-misaligned`, `strategy-misaligned`, and `unclear`.
   The complement of the recommended cuts must contain 5–8 Seeds. All 10–15
   Seeds stay visible; the recommendation never hides a rejected item. Persist
   the AI recommendation revision via bwkit and stop. Do not populate
   `shortlist.confirmed` or invent a human decision.
8. After explicit human confirmation, require 5–8 IDs from each OA, append the
   next Pool revision, record the same IDs in `shortlist.confirmed` and the
   matching human checkpoint in `decisions[]`, and validate the chain. Fewer
   than five requires more divergence; more than eight requires another human
   cut. Concept development cannot begin until every OA has a valid checkpoint.

## Quantity and identity contract

Both 10–15 generated Seeds and 5–8 human-confirmed Seeds are hard per-OA ranges.
`CS-NNN` uniqueness and semantic identity span the entire Pool revision history,
not one OA group or one file. The lightweight review checks the whole batch; it
does not score Ideas individually or replace human confirmation. Every confirmed
Seed advances to full Concept development.

Legacy revisions with `shortlist.recommended` remain readable as elimination
lists. They are labelled legacy and not reviewed under this contract; never
invent missing rationales, review findings, or readiness. Every new revision
uses `recommended_cuts`.

This continuation checkpoint is not a gate or signoff. Field semantics:
`../_bw-shared/ledger-schema.md`; lifecycle contract:
`../_bw-shared/idea-concept-solution-lifecycle.md`.
