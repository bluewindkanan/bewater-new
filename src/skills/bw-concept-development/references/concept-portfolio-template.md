# Concept Portfolio template

One `concept-portfolio` revision chain holds the branch's developed,
researchable Concepts and human convergence decisions. File:
`_bewater-output/artifacts/ART-NNN-rN-concept-portfolio.md`.

```yaml
schema_version: 1
artifact_id: ART-009
revision: 1
supersedes_ref: null
kind: concept-portfolio
stage: ideate
branch_id: BR-001
document_status: draft
validation_status: unvalidated
strategy_ref: artifact:ART-006@2
opportunity_ref: artifact:ART-007@1
idea_pool_ref: artifact:ART-008@2
review:
  status: ready                       # ready | needs-revision
  iterations: 1                      # at most 2 review-and-revision cycles
  reviewed_concept_ids: [CI-001]     # exact current candidate set
  portfolio_findings: []
concepts:
  - id: CI-001
    item_revision: 1
    opportunity_area_id: OA-001
    source_seed_id: CS-001
    parent_ids: []
    name: ""
    pithy_description: ""              # five words or fewer where language permits
    consumer_insight: ""
    commercial_insight: ""
    idea_definition: ""
    who_its_for: ""
    how_it_works: ""                   # mechanism-level, not full Solution flow
    what_it_replaces: ""
    why_big: ""
    visualization: ""                   # one-line picture-in-words (alt + fallback)
    visualization_spec:                 # optional: deterministic SVG wireframe input
      screens: []                       #   [{caption: "", bullets: [""]}]
    design_principles: []
    dual_sided:
      magic:
        consumer_value_proposition: {statement: "", evidence_refs: []}
        consumer_target: {statement: "", evidence_refs: []}
      money:
        commercial_value_proposition: {statement: "", evidence_refs: []}
        leverageable_assets: {statement: "", evidence_refs: []}
      tension: {statement: ""}
      balance_choice: ""
    evaluation:
      hard: {}                        # independent reviewer only
      soft: {}                        # independent reviewer only
      revision_attempts: 0
      recommended_action: refine       # reviewer: refine|pivot|split|merge|kill|recycle-to-OA
    assumption_refs: []                # assumption:A-NNN@record_revision
    decision: null                     # null|selected|killed|merged; human only
    merge_into: null
decisions: []                          # human select|kill|merge records
exit:
  selected_concept_ids: []             # 2–4 human-selected CI-NNN IDs
derived_from: []
signoffs: []
stale_reason: null
```

`opportunity_ref` must equal the referenced Idea Pool snapshot. Every Concept's
OA must equal the OA group containing its confirmed source Seed. A merge creates
a new Concept with both `parent_ids`; it does not mutate either parent.

Every confirmed Seed in each OA's 5–8 set produces exactly one initial Concept,
and no other initial Concept is allowed. `reviewed_concept_ids` equals all
current candidates shown for convergence; killed and merged history remains in
`concepts[]` but is excluded. `review.status: needs-revision` blocks a human
selection prompt. The independent reviewer owns evaluation and recommendations;
only explicit human input may populate terminal fields or the exit.

Legacy Portfolios referencing an Idea Pool with `shortlist.recommended` remain
readable and are labelled not reviewed under this contract. No consumer may
infer missing review content.

Field semantics: `../_bw-shared/ledger-schema.md`; lifecycle contract:
`../_bw-shared/idea-concept-solution-lifecycle.md`.
