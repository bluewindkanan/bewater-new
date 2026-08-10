# Solution template

A solution is a sharply-defined dual-sided concept with a business case. Concept → solution paths:
linear refine / pivot / hybridize (merge concepts) / invent / scope-extend. File:
`_bewater-output/ART-xxx-rN-solution.md` (append-only; `ART-001-r3-solution.md` supersedes
`ART-001-r2-solution.md` via `supersedes_ref`).

A solution is G2-ready only at `validation_status: validated`, with a dual-sided body, a business
case, traceable evidence, and every Achilles Heel resolved by L4+ behavioral evidence.

## Artifact frontmatter (kind: solution)

```yaml
schema_version: 1
artifact_id: ART-001
revision: 1
supersedes_ref: null
kind: solution
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated    # unvalidated | in-review | validated | invalidated
dual_sided:
  magic:
    consumer_value_proposition:
      statement: ""
      evidence_refs: []
    consumer_target:
      statement: ""
      evidence_refs: []
  money:
    commercial_value_proposition:
      statement: ""
      evidence_refs: []
    leverageable_assets:
      statement: ""
      evidence_refs: []
  tension:
    statement: ""
  balance_choice: ""
derived_from: []                  # the concept-portfolio (artifact:ART-NNN@r) it springs from
signoffs: []
stale_reason: null
```

The body carries the solution narrative + business case (financial assumptions sourced with logic —
see bw-investment-narrative) and records the source Concept Item id (`CI-NNN`) from the consumed
portfolio revision along each concept→solution path. Field semantics:
`../_bw-shared/ledger-schema.md`; lifecycle contract: `../_bw-shared/concept-lifecycle.md`.
