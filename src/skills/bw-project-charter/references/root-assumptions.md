# Seeding root assumptions

Root assumptions capture 3–5 of the proposition's most uncertain, falsifiable claims at
`layer: root`. Allocate the A-id from `ledger.next_id`. Write via `bwkit lock acquire` + `cas
commit ledger.yaml --expected <rev>` (bump the ledger envelope `revision` and the record's
`record_revision`). For every assumption, the Charter's Discover handoff records the evidence
needed and the disconfirming signal.

Persist these records only after the Charter self-review passes. After CAS succeeds,
capture every active root assumption on the branch as an exact typed snapshot such as
`assumption:A-001@1`; downstream Assessment lineage includes the complete snapshot.

## Assumption record (root)

```yaml
A-001:
  record_revision: 1
  statement: ""
  branch_id: BR-001
  layer: root              # root | strategy | opportunity | concept | feature
  category: consumer       # consumer | commercial | technical | distribution | regulatory
  side: money              # money | magic | both
  impact: high             # high | medium | low
  uncertainty: high        # high | medium | low
  evidence_level: L1       # user-provided starting point; not validated evidence
  validation_status: untested   # untested | testing | supported | falsified | inconclusive
  status: active           # active | killed | merged
  evidence_refs: []
  derived_from: []
  supersedes_ref: null
  risk_history: []
  l4_obligation_status: open
  history: []
```

`is_achilles_heel` is derived (impact=high AND uncertainty=high) and raises a durable L4
obligation. Field semantics: `../_bw-shared/ledger-schema.md`.
