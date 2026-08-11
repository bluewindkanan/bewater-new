---
name: bw-assumption-map
description: Use when the user wants to map or revise assumptions, risk ordering, or Achilles Heel obligations.
---

# bw-assumption-map

A **capability** that builds or revises the assumption ledger, identifies the Achilles-Heel
quadrant, and stops before human reclassification signoff.

## Workflow

1. Elicit assumptions; classify each by `category` (consumer/commercial/technical/
   distribution/regulatory) and plot on impact × uncertainty per
   `references/assumption-map.md`.
2. Identify the Achilles-Heel quadrant (impact=high AND uncertainty=high) — these raise a
   durable L4 obligation that survives later reclassification.
3. Update the ledger: add/revise assumption records (allocate A-ids from `ledger.next_id`,
   bump `record_revision` + the ledger envelope `revision`) via `bwkit lock acquire` +
   `cas commit _bewater/ledger.yaml --expected <rev>`.
   Concept assumptions use `layer: concept`, derive from an exact Concept Portfolio revision, and
   carry `source_concept_id`. Solution assumptions use `layer: solution` and derive from an exact
   Solution revision. Never copy or relayer Concept assumptions into a Solution.
4. For a Solution, compute the exact union of open Concept- and Solution-layer durable L4
   obligations. Report stale, missing, extra, or unresolved pinned references; never synthesize
   inheritance state.
5. Present the map + open L4 obligations, name the human decision authority, and **stop**.
