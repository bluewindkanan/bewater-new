# Initial Assessment artifact template

Target a **60-second read** at the top, **1–2 screens** overall, and **600–900 words**. The complete
report is a hard **no more than 900 words**. The artifact is append-only.
Aim for 650–700 words on the first draft so the trace labels and source list remain within the hard cap
without a compression pass.
A reassessment keeps the same artifact ID, increments `revision`, and points `supersedes_ref` to
the preceding Assessment revision.

## Frontmatter

```yaml
schema_version: 1
artifact_id: ART-002
revision: 1
supersedes_ref: null
kind: initial-assessment
stage: immersion
branch_id: BR-001
document_status: draft
validation_status: unvalidated
derived_from:
  - artifact:ART-001@1
signoffs: []
stale_reason: null
```

Allocate the first ID from `config.next_ids.artifact`. A later revision uses the same artifact ID
and `supersedes_ref: artifact:ART-002@1`. On the same branch, derived_from must contain exactly
one entry: the exact Charter revision only. A Charter revision mismatch means stale; never modify
an old file to refresh it.

## Body

Every key judgment must include all five labels: **Charter basis → External signal → Assessment
inference → Implication → What would change this view**. Keep the trace compact. Inline source
markers must resolve to the sources in section 5. If the research does not support a label, write
**Not established in current sources** and treat the gap as a limitation; never manufacture text
or a citation merely to fill the label.

Use this compact trace directly after each key judgment (one line is acceptable):

> **Charter basis:** ... → **External signal:** ... → **Assessment inference:** ... →
> **Implication:** ... → **What would change this view:** ...

Do not rely on a section-level labeling note as a substitute for the trace attached to the
judgment it supports.

### 1. Overall Preliminary Conclusion

- One-sentence calibrated preliminary judgment that names what would flip it, not a generic
  "worth exploring".
- Why the space is worth further exploration.
- The largest unknown.
- **Direction-level kill signal:** the single external observation whose appearance flips the
  conclusion to "not worth exploring". Pre-registered knockout criterion (Stage-Gate must-meet
  logic); not a Gate decision and no score.

### 2. Professional Perspectives

- **Magic:** potential value for the person in the Charter situation.
- **Money:** possible commercial value, investment logic, and leverageable assets.
- **Innovation:** the mechanism or behavior change that may be genuinely different.

### 3. Material Risks & Unknowns (pre-mortem)

Assume the direction proved fruitless within ~90 days of exploration, then state the most likely
reasons — prospective hindsight surfaces ~30% more failure causes than "what could go wrong"
(Klein). List at most three, ranked by how quickly a disconfirming signal could settle each. For
each, state the concrete observation under **What would change this view** that would prove the
risk wrong. Preserve material Charter Unknowns and distinguish them from externally surfaced
risks.

### 4. What to Inspect Next (core deliverable)

This checklist is the report's core output — a verdict becomes useful only through its next
action. Give a short inspection checklist grounded in the Charter and external reality check;
each item must be specific enough to act on: what to observe, whom to ask, how many cases, over
what period. Do not turn it into a Research Design, Discover Mission, priority direction, or
downstream handoff. Discover may reuse each item only as a candidate seed question with
independent source verification.

### 5. Research Boundary & Sources

State source sparsity, conflicts, coverage limits, method limits, and the distinction between
Charter basis, External signal, and Assessment inference. List only the sources actually used,
each with exact title, publisher, date when available, and exact retrieved URL. The count is not
a target: fewer well-attributed sources beat padded ones, and a visibly source-sparse report is
preferred to a padded one. Every External signal must resolve to a listed source; anything
unsourced is labeled **Assessment inference**.

This report is not a Gate, contains no score or readiness label, and must not decide whether to
invest or proceed. It does not modify the Charter, does not change assumption validation, does not
change `current_stage`, and does not write a signoff or Evidence wrapper. It is not an input to
Research or the Knowledge Base, does not create Evidence, does not create or update assumptions,
and must not be consumed by Discover as Evidence. Discover may read a matching Assessment's
`What to Inspect Next` only as candidate seed questions for research planning, each independently
source-verified before promotion; `Material Risks` and the Assessment's judgments stay advisory and
do not flow into Research.
