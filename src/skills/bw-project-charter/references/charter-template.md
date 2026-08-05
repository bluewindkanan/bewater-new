# Charter artifact template

File: `_bewater-output/ART-001-r1-charter.md` (append-only; a substantive edit writes
`ART-001-r2-charter.md` with `supersedes_ref: artifact:ART-001@1`). Allocate the ART id
from `config.next_ids.artifact` while holding the lock.

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

### Original intent

- **User's own words:** preserve the strongest original wording; do not invent quotations.
- **Trigger / why now:** what observation, event, or frustration started the idea.
- **Desired change:** what the user hopes will become different.

### Structured interpretation

- **One-line proposition:** who / what / how / why.
- **Target and situation:** a specific person in a specific context, including their desire.
- **Current behavior and alternatives:** what happens today, including workarounds and cost.
- **Provisional solution hypothesis:** the user's current idea of how it might work; it is not a
  validated direction.
- **Success signals:** observable user and business changes.
- **Scope:** included, excluded, first-cycle boundary, and constraints.

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
| **Known** | User-reported observations or sourced facts, with the source label preserved; self-report is not validation. |
| **Believed** | User/team beliefs that still need evidence. |
| **Unknown** | Questions that Discover must answer. |
| **Tensions** | Contradictions between intent, behavior, value, and constraints. |

### Discover handoff

#### Core exploration question

What must we understand about the person, situation, current behavior, and surrounding system before
we can trust or reframe the proposition?

#### Beliefs to challenge

List the strongest accepted beliefs from the current intent and structured interpretation. Label
each as a candidate belief or hypothesis, never as a Fact.

#### Root assumption research map

| Assumption | 4C | Why it matters | Evidence needed | Disconfirming signal |
|---|---|---|---|---|
| A-001 | Consumer / Company / Category / Channel | ... | ... | ... |

#### Starting 4C questions

- **Consumer:** who is buying or doing this, and why in the actual situation?
- **Company:** what assets, capabilities, relationships, and constraints do we have?
- **Category:** what arena, alternatives, and default conventions shape the behavior?
- **Channel:** where does the behavior or decision happen, and how is access gained?

#### Research boundary

State what Discover should investigate first and what it should not assume, design, or optimize yet.
