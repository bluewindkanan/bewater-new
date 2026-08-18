---
contract_id: bw-concept-independent-review
contract_version: 1
---

# Independent Concept review contract

This contract separates Concept production from Concept evaluation. Artifact
Markdown is the single source of truth. The reviewer returns a review payload;
it never writes an Artifact, ledger record, decision, or HTML.

## Isolation and input

Run the reviewer in a fresh context. Pass only:

1. the exact candidate Concept Portfolio payload;
2. its exact Idea Pool, Opportunity Portfolio, and Strategy references;
3. the referenced evidence and Concept assumptions needed to judge the batch;
4. this contract.

Do not pass producer reasoning or ask the reviewer to preserve the producer's
scores. The reviewer resolves the exact references, cannot mutate project
state, and returns structured findings. If isolation or an exact input is
unavailable, return no review and stop.

## Review scope

Review the complete active candidate batch for:

- exact confirmed-Seed and same-OA lineage;
- complete Who / What / How / What it replaces / Why Big blocks;
- distinct mechanisms at researchable, testable Concept altitude;
- overlap, false distinctions, and credible merge or split opportunities;
- Strategy and Opportunity Area fit;
- Consumer Magic, Commercial Money, and the unresolved tension;
- explicit falsifiable assumptions and useful pretest altitude;
- naming, pithy description, visualization, and comprehension; and
- whether the portfolio supports meaningful comparison and a global 2–4 choice.

The reviewer owns `evaluation.hard`, `evaluation.soft`, and
`recommended_action`. The action vocabulary is `refine`, `pivot`, `split`,
`merge`, `kill`, or `recycle-to-OA`.

## Review payload

Return this shape to the producer without persisting it directly:

```yaml
review:
  status: ready                       # ready | needs-revision
  iterations: 1
  reviewed_concept_ids: [CI-001]
  portfolio_findings:
    - concept_ids: [CI-001, CI-004]
      issue: mechanism-overlap
      recommendation: merge
concept_reviews:
  - concept_id: CI-001
    evaluation:
      hard: {}
      soft: {}
      revision_attempts: 0
      recommended_action: refine
    findings: []
```

`reviewed_concept_ids` equals the complete current candidate set, excluding
terminal killed or merged history. A `ready` payload cannot omit a candidate.
Every Concept receives exactly one review entry. Portfolio findings name the
affected IDs and a bounded recommendation.

## Authority and bounded loop

The reviewer may identify weak Concepts and recommend an action. It cannot
populate or alter human-only `shortlist.confirmed`, Concept `decision`,
`merge_into`, Portfolio `decisions`, or `exit.selected_concept_ids`. It cannot
sign a Gate or choose a lifecycle exit.

The producer may revise content from the review payload and request independent
verification. Run at most two review-and-revision cycles. If material findings
remain, return `needs-revision` and preserve them; never convert unresolved
judgment into `ready` merely because the loop ended.
