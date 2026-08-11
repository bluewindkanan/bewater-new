# Directional hypothesis template

A directional hypothesis is a *guess*, not a conclusion. Structure:

- **By**[the means / approach] …
- **We can**[give the consumer this value = Magic] …
- **Resulting in**[this business outcome = Money] …

Each of By / We can / Resulting in cites ≥1 insight; the four C's must not be lopsided.
Dual-sided (Money + Magic) coverage is required.

One artifact contains 2–5 candidates in a single file, matching the insight portfolio pattern.

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
derived_from: ["artifact:ART-INSIGHT@1"]
signoffs: []
stale_reason: null
```

## Body — candidate sections

Each candidate gets its own numbered section:

### Candidate 1: [short label]

**By**[…]
- Insight 支撑: insight:ART-xxx@N:罗马数字

**We can**[…]
- Insight 支撑: insight:ART-xxx@N:罗马数字

**Resulting in**[…]
- Insight 支撑: insight:ART-xxx@N:罗马数字

**4C 覆盖:**
- Consumer: …
- Company: …
- Competitor: …
- Category: …

**Dual-sided:**
- Magic: [consumer value proposition statement]
- Money: [commercial value proposition statement]
- Tension: [statement of the inherent tension]
- Balance choice: [which side the hypothesis leans toward, if any]

**状态:** draft · unvalidated · 未关闭

---

### Candidate 2: [short label]

… same structure for candidates 2–5 …

## Signoff recording

Closing a hypothesis for the remaining Define work is recorded via a signoff at the current
revision — one signoff per closed candidate:

```yaml
signoffs:
  - hypothesis: 1
    role: product-owner
    dual_sided:
      magic: {consumer_value_proposition: {statement: "", evidence_refs: []}}
      money: {commercial_value_proposition: {statement: "", evidence_refs: []}}
      tension: {statement: ""}
      balance_choice: ""
    signed_at: "2026-08-07T00:00:00Z"
```

Field semantics: `../_bw-shared/ledger-schema.md`.
