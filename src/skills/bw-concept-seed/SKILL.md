---
name: bw-concept-seed
description: Use when the user wants to diverge raw BeWater Idea Seeds across the Opportunity Portfolio and recommend development shortlists.
---

# bw-concept-seed

A **capability** for the divergent half of Ideate. Create or revise the one
branch-global Idea Pool, diverge raw Idea Seeds under every Opportunity Area,
recommend OA-level **elimination** shortlists, and stop for human confirmation.
You recommend; the accountable human confirms. Never hide a Seed you would
rather cut.

## Workflow

1. Resolve the active branch, exact locked `strategy` revision, and exact
   `opportunity` revision. The Opportunity Portfolio must expose 2–4 canonical
   `opportunity_areas[]` with stable `OA-NNN` IDs.
2. Find the branch's existing `idea-pool` chain. If one exists, revise that
   chain. If its strategy or Opportunity input changed, record the new exact
   refs in `input_snapshot` on the next revision. Never create a second Pool
   chain for the branch.
3. For every OA, diverge 10–15 Seeds using brainstorm + “how might we”. Allocate
   `CS-NNN` IDs pool-wide, preserve them for the same Seed across revisions, and
   never reassign or reuse an ID.
4. Capture each Seed per `references/idea-pool-template.md`: one required `idea`
   sentence plus source-insight lineage. `cluster_id` and `strategy_filter` are
   system annotations, not developed Concept content.
5. Cluster near-duplicates (assign `cluster_id`) but keep every Seed visible,
   including duplicates, failed filters, and non-shortlisted items. `cluster_id`
   and `strategy_filter` are system annotations shown to the human as cut
   evidence, not developed Concept content.
6. Recommend an **elimination** shortlist separately for each OA in
   `shortlist.recommended`: **default to keep**; cut only a Seed that is clearly
   dead, a near-duplicate of a kept Seed, or off-strategy. The human must not
   blind-judge 10–15 one-line Seeds, so every recommended cut cites its
   evidence — the `cluster_id` it duplicates, or a `strategy_filter: fail`
   (off-strategy) / `partial` verdict. The confirmed count floats ~5–8 per OA
   (there is no 3–5 cap); **every** confirmed Seed then advances to full Concept
   development in bw-concept-development, with no sketch intermediate layer
   where a Seed could be cut on a thinner signal. Persist the AI recommendation
   revision via bwkit. Stop. Do not populate `shortlist.confirmed` or invent a
   human decision.
7. After explicit human confirmation, append the next Pool revision, record the
   confirmed IDs and checkpoint in `decisions[]`, and validate the chain.

## Quantity and identity contract

Ten Seeds per OA is a hard minimum. Fifteen is a soft ceiling: above it, warn and
preserve all Seeds; never truncate silently. `CS-NNN` uniqueness and semantic
identity span the entire Pool revision history, not one OA group or one file.

Confirmation is elimination-based and floats ~5–8 confirmed Seeds per OA: keep
when unsure, cut only the clearly dead, duplicate, or off-strategy. There is no
3–5 cap — the only hard convergence cut is selection of 2–4 Concepts later, at
the rich-Concept layer — so every confirmed Seed advances to full Concept
development.

This continuation checkpoint is not a gate or signoff. Field semantics:
`../_bw-shared/ledger-schema.md`; lifecycle contract:
`../_bw-shared/idea-concept-solution-lifecycle.md`.
