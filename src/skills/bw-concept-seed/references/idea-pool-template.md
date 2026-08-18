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
    review:
      status: ready                    # ready | needs-revision
      iterations: 1
      findings: []                     # batch findings; no hidden Seed scoring
    shortlist:
      recommended_cuts:                # AI recommendation; complement is 5–8
        - seed_id: CS-010
          reason: duplicate            # duplicate|weak-distinctiveness|oa-misaligned|strategy-misaligned|unclear
          rationale: "Uses the same intervention mechanism as CS-003."
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

Every OA contains 10–15 Seeds. `review` is the lightweight batch check: it
records unresolved quality findings without deciding for the human. Every
recommended cut references a Seed in the same OA and includes both a controlled
reason and a specific rationale. The complement of `recommended_cuts` contains
5–8 Seeds. A populated `confirmed` also contains 5–8 same-OA Seeds and must have
a matching human decision.

An AI recommendation leaves `decisions: []`. After explicit human confirmation,
the next revision populates `shortlist.confirmed` and records the same IDs with
this human-only decision schema:

```yaml
decisions:
  - type: confirm-shortlist
    opportunity_area_id: OA-001
    seed_ids: [CS-001, CS-002, CS-003, CS-004, CS-005]
    decided_by:
      name: ""
      role: ""
      type: human
```

Legacy revisions may contain `shortlist.recommended` as an elimination ID list.
Readers label that data legacy and do not fabricate rationales or review state.
New revisions use only `recommended_cuts`.

Field semantics: `../_bw-shared/ledger-schema.md`; lifecycle contract:
`../_bw-shared/idea-concept-solution-lifecycle.md`.
