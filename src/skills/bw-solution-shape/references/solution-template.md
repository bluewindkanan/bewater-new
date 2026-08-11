# Solution template

A solution is a sharply-defined dual-sided concept with a business case. Concept → solution paths:
`linear-refine` / `pivot` / `hybridize` (merge concepts) / `scope-extend`; do not invent outside
the selected Concept boundary. File:
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
source_concepts:
  portfolio_ref: artifact:ART-012@2
  concept_ids: [CI-001]
  path: linear-refine             # linear-refine | pivot | hybridize | scope-extend
definition:
  name: ""
  pithy_proposition: ""
  what_it_is: ""
  who_its_for: ""
  dual_sided:
    money:
      commercial_value_proposition: ""
      leverageable_assets: ""
    magic:
      consumer_value_proposition: ""
      consumer_target: ""
    tension: ""
    balance_choice: ""
  dimensions:
    path_to_market: ""
    right_to_win: ""
    product_or_service_platform: ""
    source_of_business: ""
    product_or_service_design: ""
    enabling_technology: ""
    reason_to_believe: ""
    branding: ""
    consumer_experience: ""
how_it_works:
  - step: 1
    action: ""
    consumer_benefit: ""
    operational_benefit: ""
    strategic_rationale: ""
    legal_regulatory_rationale: ""
    evidence_refs: []
    design_refs: []
how_to_implement:
  - phase: ""
    timing: ""
    objective: ""
    jobs_to_be_done: []
    capabilities_and_assets: []
    owner: ""
    dependencies: []
    risks: []
    open_questions: []
    pilot_and_rollout: ""
how_it_makes_money:
  revenue_streams: []
  pricing_and_volume_logic: ""
  adoption_retention_frequency_assumptions:
    - assumption: ""
      source: ""
  development_and_operating_costs:
    - assumption: ""
      source: ""
  scenarios:
    base:
      revenue: null
      margin: null
      earnings: null
      investment: null
      payback: ""
    aggressive:
      revenue: null
      margin: null
      earnings: null
      investment: null
      payback: ""
  sensitivity: []
  unresolved_model_gaps: []
validation:
  consumer_desire:
    claim: ""
    evidence_refs: []
  commercial_value:
    claim: ""
    evidence_refs: []
  feasibility_and_implementation:
    claim: ""
    evidence_refs: []
  achilles_assumption_refs: []
  experiment_refs: []
  evidence_refs: []
  invalidated_claims: []
content_gaps: []
applicability_exceptions: []
signoffs: []
stale_reason: null
```

The body is the deterministic Markdown projection of the five canonical blocks. Financial
assumptions use `assumption` + `source`, with reasoning carried in the surrounding business case
and investment narrative. Field semantics: `../_bw-shared/ledger-schema.md`; lifecycle contract:
`../_bw-shared/idea-concept-solution-lifecycle.md`.
