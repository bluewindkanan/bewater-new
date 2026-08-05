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
  - assumption:A-001@1
  - assumption:A-002@1
  - assumption:A-003@1
signoffs: []
stale_reason: null
```

Allocate the first ID from `config.next_ids.artifact`. A later revision uses the same artifact ID
and `supersedes_ref: artifact:ART-002@1`. `derived_from` must exactly match the current Charter and
complete active root-assumption revision snapshot. Snapshot mismatch means stale; never modify an
old file to refresh it.

## Body

Every key judgment must include all five labels: **Charter basis → External signal → Assessment
inference → Implication → What would change this view**. Keep the trace compact. Inline source
markers must resolve to the sources in section 8. If the research does not support a label, write
**Not established in current sources** and treat the gap as a limitation; never manufacture text
or a citation merely to fill the label.

Use this compact trace directly after each key judgment (one line is acceptable):

> **Charter basis:** ... → **External signal:** ... → **Assessment inference:** ... →
> **Implication:** ... → **What would change this view:** ...

Do not rely on a section-level labeling note as a substitute for the trace attached to the
judgment it supports.

### 1. Overall Preliminary Conclusion

- One-sentence preliminary judgment.
- Why the space is worth further exploration.
- The largest unknown.

### 2. Professional Perspectives

- **Magic:** potential value for the person in the Charter situation.
- **Money:** possible commercial value, investment logic, and leverageable assets.
- **Innovation:** the mechanism or behavior change that may be genuinely different.

### 3. Candidate Insights

State 2–3 non-obvious candidate judgments. Call them Candidate Insights, never formal Insights,
Facts, Evidence, or Accepted Beliefs.

### 4. Core Conflict / Tension

State the single most important conflict in value, behavior, commercial logic, or scope.

### 5. Most Promising Direction

Name one priority opportunity direction and at most two alternative exploration directions. Keep
them opportunity-led; do not prescribe a solution.

### 6. Key Risks

List at most three risks. For each, include a disconfirming signal under **What would change this
view**.

### 7. Discover Mission

- One priority research mission.
- Two key questions.
- One item not to optimize yet.

### 8. Research Boundary & Sources

State source sparsity, conflicts, coverage limits, method limits, and the distinction between
Charter basis, External signal, and Assessment inference. List the 1–5 sources actually used with
exact title, publisher, date when available, and exact retrieved URL.

This report is not a Gate, contains no score or readiness label, and must not decide whether to
invest or proceed. It does not modify the Charter, does not change assumption validation, does not
change `current_stage`, and does not write a signoff or Evidence wrapper.
