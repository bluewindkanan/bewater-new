# Charter artifact template (spec §5.4, §9.1)

File: `_bewater-output/ART-001-r1-charter.md` (append-only; a substantive edit writes
`ART-001-r2-charter.md` with `supersedes_ref: artifact:ART-001@1`). Allocate the ART id
from `config.next_ids.artifact` while holding the §5.7 lock.

## Frontmatter

```yaml
schema_version: 1
artifact_id: ART-001
revision: 1
supersedes_ref: null
kind: charter
stage: immersion
branch_id: BR-001
document_status: draft
validation_status: unvalidated
dual_sided:
  magic:
    consumer_value_proposition:
      statement: ""        # what value we give the user
      evidence_refs: []
    consumer_target:
      statement: ""        # who, specifically — situation and desire, not "can solve X"
      evidence_refs: []
  money:
    commercial_value_proposition:
      statement: ""        # how the business works and earns
      evidence_refs: []
    leverageable_assets:
      statement: ""        # existing assets/capabilities that build the moat
      evidence_refs: []
  tension:
    statement: ""          # where Magic and Money constrain / reinforce each other
  balance_choice: ""
derived_from: []
signoffs: []
stale_reason: null
```

## Body

One-line proposition (who/what/how/why) + scope + constraints + success criteria. A non-empty
final body is only document-presence evidence — it is never readiness (spec §5.4).
