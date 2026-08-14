# Idea Pool template

One `idea-pool` revision chain serves the entire active branch. It groups 10–15
raw Idea Seeds under each Opportunity Area and records the exact Ideate input
snapshot. File: `_bewater-output/artifacts/ART-NNN-rN-idea-pool.md`.

```yaml
schema_version: 1
artifact_id: ART-008
revision: 1
supersedes_ref: null
kind: idea-pool
stage: ideate
branch_id: BR-001
document_status: draft
validation_status: unvalidated
input_snapshot:
  strategy_ref: artifact:ART-006@2
  opportunity_ref: artifact:ART-007@1
opportunity_areas:
  - opportunity_area_id: OA-001
    seeds:
      - id: CS-001
        idea: ""
        source_insight_refs: []
        cluster_id: null
        strategy_filter: pass          # pass | fail | partial
    shortlist:
      recommended: []                  # AI recommendation
      confirmed: []                    # accountable human only
decisions: []                          # human shortlist checkpoints
derived_from: []
signoffs: []
stale_reason: null
```

The active `branch_id`, not the snapshot hash, is the logical uniqueness key.
When either input ref changes, append a revision to this chain. Seed IDs are
unique pool-wide and never reassigned or reused across revision history. The
`idea` sentence is the only required human-facing Seed content; all other Seed
fields are lineage or system annotation.

An AI recommendation leaves `decisions: []`. After explicit human confirmation,
the next revision populates `shortlist.confirmed` and records the same IDs with
this human-only decision schema:

```yaml
decisions:
  - type: confirm-shortlist
    opportunity_area_id: OA-001
    seed_ids: [CS-001]
    decided_by:
      name: ""
      role: ""
      type: human
```

Field semantics: `../_bw-shared/ledger-schema.md`; lifecycle contract:
`../_bw-shared/idea-concept-solution-lifecycle.md`.
