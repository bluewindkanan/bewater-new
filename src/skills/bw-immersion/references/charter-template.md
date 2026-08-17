# Charter artifact template

File: `_bewater-output/artifacts/ART-001-r1-charter.md` (append-only; a substantive edit writes
`ART-001-r2-charter.md` with `supersedes_ref: artifact:ART-001@1`). Allocate the ART id
from `config.next_ids.artifact` while holding the lock.

The first Charter transaction also binds the repository by setting a concise, non-empty
`config.project.name`. A later Charter revision retains that established name unless the revision is
still within the same project; unrelated project intent belongs in a different repository or working
directory.

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

The body must keep the user's voice separate from the agent's interpretation. A non-empty final body
is only document-presence evidence — it is never readiness.

### Intent trace

List 4–7 high-impact claims that shape the challenge, intent, outcome, scope, or balance choice.
This is a compact transparency aid, not a second artifact or a signoff. Every row has one provenance
label: `user-stated` (free-form user wording), `user-selected` (an AI candidate the user chose),
`agent-interpretation` (a faithful synthesis), or `unknown` (an acknowledged gap). Do not label a
model recommendation as a user statement or a verified fact.

| Claim | Provenance | Basis / exact user context | Calibration status |
|---|---|---|---|
| ... | user-stated / user-selected / agent-interpretation / unknown | ... | corrected / unchanged / declined / not-required |

### Original intent

- **User's own words:** preserve the strongest original wording; do not invent quotations.
- **Trigger / why now:** what observation, event, or frustration started the idea.
- **Desired change:** what the user hopes will become different.

### Project definition

- **Challenge:** the situation and problem worth addressing, without treating a solution as proven.
- **Intent and outcome:** the desired change and provisional proposition: who / what / how / why.
- **Target and situation:** a specific person in a specific context, including their desire.
- **Current behavior and alternatives:** what happens today, including workarounds and cost.
- **Provisional solution hypothesis:** the user's current idea of how it might work; it is not a
  validated direction; capture it at behavior level, not implementation parameters.
- **Scope:** included, excluded, and the first-cycle boundary.
- **Constraints:** material time, access, capability, regulatory, or resource boundaries.
- **Success definition:** observable user and business changes that would mean the project succeeded;
  this is a definition, not validated evidence.

### Money + Magic

- **Magic / consumer value proposition:** the value created in the person's situation.
- **Magic / consumer target:** the specific person, context, and desire.
- **Money / commercial value proposition:** how value may sustain the business.
- **Money / leverageable assets:** capabilities, relationships, access, data, or trust already
  available.
- **Tension and balance:** where Magic and Money reinforce or constrain one another and what remains
  unresolved.

### Current knowledge state

| Type | Content |
|---|---|
| **Known** | User-reported observations or sourced facts, with the provenance label preserved; self-report is not validation. `user-selected` and `agent-interpretation` are not Facts. |
| **Believed** | User/team beliefs that still need evidence, including selected recommendations where appropriate. |
| **Unknown** | Explicit gaps the project does not yet know; preserve `unknown` provenance. |
| **Tensions** | Contradictions between intent, behavior, value, and constraints. |

Stop at explicit Unknowns. Do not add research questions, methods, evidence needs, priority exits,
4C planning, assumption projections, or ledger references; Discover derives those from this exact
Charter revision. Discover's Research Objective reads `innovation challenge` from **Challenge**,
`research boundary` from **Scope + Constraints**, and `strategic uncertainties` from **Unknown +
Tensions**. The Charter does not pre-name these; Discover derives them from this exact revision.
