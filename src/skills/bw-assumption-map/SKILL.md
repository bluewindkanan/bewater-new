---
name: bw-assumption-map
description: Use when the user wants to map or revise assumptions, risk ordering, or Achilles Heel obligations.
---

# bw-assumption-map

A **capability** that completes or revises the G1 inventory in the assumption ledger, identifies
the Achilles-Heel quadrant, and stops before human reclassification signoff. Research Planning's
selective projection is only a starting point: accept both Research-derived roots and
grandfathered Charter-derived roots, including a legitimate zero-projection Research Plan.

## Workflow

1. Revisit any Research-derived or grandfathered Charter-derived roots, then elicit the remaining
   real strategy and opportunity risks required to complete the G1 inventory. Never create a fake
   assumption to satisfy readiness. Classify each by `category` (consumer/commercial/technical/
   distribution/regulatory) and plot on impact × uncertainty per
   `references/assumption-map.md`.
2. Identify the Achilles-Heel quadrant (impact=high AND uncertainty=high) — these raise a
   durable L4 obligation that survives later reclassification.
3. Update the ledger: add/revise assumption records (allocate A-ids from `ledger.next_id`,
   bump `record_revision` + the ledger envelope `revision`) via `bwkit lock acquire` +
   `cas commit _bewater/ledger.yaml --expected <rev>`.
   A Knowledge workpaper (`knowledge:K-NNN@n`) does not close an L4 obligation. A supported
   assumption or closed obligation requires an exact current `evidence:E-NNN@n` record; allocate
   new Evidence only from `evidence.yaml.next_evidence_id`.
   Concept assumptions use `layer: concept`, derive from an exact Concept Portfolio revision, and
   carry `source_concept_id`. Solution assumptions use `layer: solution` and derive from an exact
   Solution revision. Never copy or relayer Concept assumptions into a Solution.
4. For a Solution, compute the exact union of open Concept- and Solution-layer durable L4
   obligations. Report stale, missing, extra, or unresolved pinned references; never synthesize
   inheritance state.
5. Present the map + open L4 obligations, name the human decision authority, and **stop**.
