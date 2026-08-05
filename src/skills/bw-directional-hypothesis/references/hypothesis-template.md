# Directional hypothesis template

A directional hypothesis is a *guess*, not a conclusion. Structure:

- **By**[the means / approach] …
- **We can**[give the consumer this value = Magic] …
- **Resulting in**[this business outcome = Money] …

Each of By / We can / Resulting in cites ≥1 insight; the four C's must not be lopsided.
Dual-sided (Money + Magic) coverage is required.

## Artifact frontmatter (kind: directional-hypothesis)

```yaml
schema_version: 1
artifact_id: ART-001
revision: 1
supersedes_ref: null
kind: directional-hypothesis
stage: define
branch_id: BR-001
document_status: draft
validation_status: unvalidated
dual_sided:
  magic: {consumer_value_proposition: {statement: "", evidence_refs: []}}
  money: {commercial_value_proposition: {statement: "", evidence_refs: []}}
  tension: {statement: ""}
  balance_choice: ""
derived_from: ["artifact:ART-INSIGHT@1"]
signoffs: []
stale_reason: null
```

Closing a hypothesis for the remaining Define work is recorded via a signoff at the current
revision. Field semantics: `../_bw-shared/ledger-schema.md`.
