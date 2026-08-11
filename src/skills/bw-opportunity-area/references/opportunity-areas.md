# Opportunity areas

2–4 discrete, **non-overlapping** innovation directions that bridge strategy → concepts.
Four ways to cut them: by consumer archetype / business pillar / consumer need / journey
stage. Each area must be able to spawn multiple concepts; they are opportunities, not
feature modules.

## Artifact frontmatter (kind: opportunity)

```yaml
schema_version: 1
artifact_id: ART-001
revision: 1
supersedes_ref: null
kind: opportunity
stage: define
branch_id: BR-001
document_status: draft
validation_status: unvalidated
opportunity_areas:
  - id: OA-001
    name: ""
    audience: ""
    opportunity: ""
    consumer_value: ""
    commercial_value: ""
    source_insight_refs: []
dual_sided:
  magic: {consumer_value_proposition: {statement: "", evidence_refs: []}}
  money: {commercial_value_proposition: {statement: "", evidence_refs: []}}
  tension: {statement: ""}
  balance_choice: ""
derived_from: []
signoffs: []
stale_reason: null
```

`OA-NNN` IDs are artifact-local, stable, and never reused across this chain's
revision history. The Markdown body renders `opportunity_areas[]`; headings such
as `OA-1` are not authoritative references. G1 readiness requires 2–4
non-overlapping, generative entries in the current Portfolio head
(`../_bw-shared/gate-criteria.md`).
