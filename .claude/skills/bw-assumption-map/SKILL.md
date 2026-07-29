---
name: bw-assumption-map
description: Use when the user wants to map or revise assumptions, risk ordering, or Achilles Heel obligations.
---

# bw-assumption-map

A **capability** that builds/revises the assumption inventory in the ledger and surfaces the
Achilles-Heel quadrant (bewater-core §9.8, §5.3). You update `ledger.yaml` via bwkit CAS and
stop before any human reclassification signoff (spec §4).

## Workflow

1. Elicit assumptions; classify each by `category` (consumer/commercial/technical/
   distribution/regulatory) and plot on impact × uncertainty per
   `references/assumption-map.md`.
2. Identify the Achilles-Heel quadrant (impact=high AND uncertainty=high) — these raise a
   durable L4 obligation that survives later reclassification (§5.3).
3. Update the ledger: add/revise assumption records (allocate A-ids from `ledger.next_id`,
   bump `record_revision` + the ledger envelope `revision`) via `bwkit lock acquire` +
   `cas commit _bewater/ledger.yaml --expected <rev>`.
4. Present the map + open L4 obligations, name the human decision authority, and **stop**.
