# Ideate Funnel, Independent Review, and HTML Decision Views

## Status

Approved 2026-08-18.

This design tightens the Idea-to-Concept funnel, separates Concept production
from Concept review, and makes the Idea Pool and Concept Portfolio usable as
human decision evidence in the generated HTML reader.

It extends `2026-08-18-concept-visualization-svg-design.md`. That design covers
Concept visualization and card rendering; this design covers the funnel,
review authority, and decision-oriented presentation that it deliberately left
out of scope.

## Design invariant

**Artifact Markdown is the single source of truth.**

- YAML frontmatter holds canonical structured facts, lineage, review results,
  and decisions.
- The Markdown body may explain those facts but cannot override them.
- HTML reads, computes, and projects Artifact Markdown. It never invents,
  repairs, persists, or becomes authoritative for business content.
- Human decisions create a new Artifact revision through the existing CAS and
  runtime path. They are never written into HTML or `_bewater/` by hand.

## Problem

The current lifecycle diverges 10–15 Idea Seeds per Opportunity Area, then
defaults to keeping uncertain Seeds and develops every confirmed Seed. In the
active case, three Opportunity Areas confirmed 9, 9, and 10 Seeds. The resulting
28 Concepts, plus two merge Concepts, produced 30 full cards. This is a direct
consequence of the current contract rather than a rendering accident.

The HTML reader also opens on the latest Solution and treats Idea Pool and
Concept Portfolio as ordinary artifact sections. Idea Seeds are present in the
Markdown body, while Concept fields are stored in frontmatter. Even when all
content is technically present, users do not receive a clear journey, an
OA-grouped comparison, reviewer findings, or an explicit decision handoff.

Finally, Concept production currently includes its own `evaluation.hard` and
`evaluation.soft` scoring. Adding a second review on top would duplicate work
and preserve producer bias. Review responsibility must be separated rather
than stacked.

## Target lifecycle

One branch-global Idea Pool and one branch-global Concept Portfolio remain the
lifecycle model. They cover all Opportunity Areas and retain their current
revision-chain and item-identity rules.

For every Opportunity Area:

```text
10–15 Idea Seeds
  -> lightweight pool review and elimination recommendation
  -> human confirms exactly 5–8 Seeds
  -> every confirmed Seed becomes one initial full Concept
  -> independent Concept review
```

Across the complete Concept Portfolio:

```text
all reviewed Concepts, grouped by OA
  -> human selects 2–4 Concepts in total
  -> Shape
```

There is no per-OA quota in the final 2–4 Concept selection. Review is a
capability checkpoint, not a new lifecycle stage or gate, and it never chooses
a human-controlled exit.

## Responsibility model

### Idea Pool quality check

Idea Pool review is a lightweight batch check inside the Seed workflow. It is
not a separate public stage. It checks whether the pool is ready for a human to
make an informed 5–8 Seed confirmation.

It reviews:

- direct relevance to the owning Opportunity Area;
- breadth and mechanism diversity across the 10–15 Seeds;
- duplicates and cosmetic variants;
- obvious Strategy or OA misalignment;
- consistent one-sentence Seed altitude;
- traceable source Insights; and
- whether proposed cuts leave 5–8 credible Seeds and explain every cut.

It does not conduct deep commercial feasibility analysis, expand Seeds into
Concepts, or reject uncertain Ideas merely because they lack Concept-level
detail.

### Independent Concept Reviewer

Concept review runs in a fresh reviewer context separate from the producer.
The reviewer receives the exact candidate Portfolio and its referenced inputs,
cannot mutate project state, and returns a structured review payload. The
producer may revise from that payload, after which the reviewer verifies the
new candidate. If an independent context cannot run, the workflow stops and
reports the missing review; producer self-review is not treated as equivalent.

The independent reviewer owns the existing per-Concept `evaluation.hard`,
`evaluation.soft`, and `recommended_action` results. The producer no longer
scores its own output.

The reviewer checks:

- exact confirmed-Seed and OA lineage;
- complete Who / What / How / What it replaces / Why Big blocks;
- a distinct mechanism at testable Concept altitude;
- overlap, merge, split, and false-Concept risks across the batch;
- Strategy and Opportunity Area fit;
- Consumer Magic, Commercial Money, and the unresolved tension between them;
- explicit, falsifiable assumptions and useful pretest altitude;
- naming, pithy description, visualization, and comprehension; and
- whether the full batch supports comparison and final selection.

The reviewer may recommend `refine`, `pivot`, `split`, `merge`, `kill`, or
`recycle-to-OA`. It cannot populate `shortlist.confirmed`, Concept `decision`,
`merge_into`, or `exit.selected_concept_ids`.

## Review loop

The review loop is bounded:

```text
producer candidate
  -> independent review
  -> producer revision
  -> independent verification
  -> reviewed Artifact revision
```

At most two review-and-revision cycles are allowed. The persisted Artifact uses
one of two review states:

- `ready`: the candidate can be presented for the next human decision;
- `needs-revision`: material findings remain after the bounded loop.

If unresolved findings remain, the Artifact records them honestly and HTML
shows them, but the next human decision is not presented as ready. Transient
candidates are working material, not project facts; the committed Artifact
revision containing the final review result is authoritative.

## Idea Pool contract

Replace the ambiguous elimination field `shortlist.recommended` with explicit
recommended cuts and rationales:

```yaml
opportunity_areas:
  - opportunity_area_id: OA-001
    seeds: []                         # 10–15
    review:
      status: ready                   # ready | needs-revision
      iterations: 1
      findings: []
    shortlist:
      recommended_cuts:
        - seed_id: CS-009
          reason: duplicate
          rationale: "Uses the same intervention mechanism as CS-003."
      confirmed: []                   # human only; exactly 5–8 when present
```

Recommended-cut reasons use a small vocabulary:

- `duplicate`;
- `weak-distinctiveness`;
- `oa-misaligned`;
- `strategy-misaligned`; or
- `unclear`.

The rationale is always required. A reason code alone is not sufficient.

Hard invariants:

- every OA contains 10–15 Seeds, inclusive;
- all Seed IDs remain visible and stable across revisions;
- recommended cuts reference Seeds in the same OA;
- the complement of `recommended_cuts` contains 5–8 Seeds;
- `confirmed`, when populated, contains 5–8 Seeds from the same OA;
- only explicit human input may populate `confirmed`; and
- Concept development cannot start until every OA has a valid confirmed set.

If fewer than five credible Seeds survive review, the pool is
`needs-revision`; the producer must improve or replace weak Seeds rather than
lower the minimum. If more than eight survive, the recommendation must make
the comparative cuts needed to reach the hard ceiling. The human may confirm a
different valid 5–8 set after seeing the complete pool.

Legacy `shortlist.recommended` data remains readable as an elimination list but
is rendered with a legacy label. New revisions use `recommended_cuts`.

## Concept Portfolio contract

The initial Concept set is a one-to-one development of the confirmed Seed set:

- every confirmed Seed resolves to exactly one initial `CI-NNN`;
- every initial Concept resolves to one confirmed Seed in the same OA;
- each OA therefore begins Concept review with 5–8 Concepts; and
- an unconfirmed or cross-OA Seed cannot produce a Concept.

The Portfolio adds batch-level review metadata while retaining reviewer-owned
per-Concept evaluation:

```yaml
review:
  status: ready                       # ready | needs-revision
  iterations: 2
  reviewed_concept_ids: [CI-001, CI-002]
  portfolio_findings:
    - concept_ids: [CI-001, CI-004]
      issue: mechanism-overlap
      recommendation: merge
concepts:
  - id: CI-001
    evaluation:
      hard: {}
      soft: {}
      revision_attempts: 1
      recommended_action: refine
```

`reviewed_concept_ids` must equal the current candidate set being presented.
A reviewer recommendation does not change terminal fields. If the human later
accepts a merge, the existing lineage rule creates a new `CI-NNN` and preserves
the parents. Any new active Concept must be reviewed before it can be selected.

The initial 5–8 count is the convergence batch produced from each OA. Later
human merge or kill decisions preserve all historical items but change the
active candidate set; terminal historical items do not inflate the decision
count or default card view.

## HTML information architecture

### Case journey

`artifacts.html` opens on a case-journey view rather than jumping directly to
the latest Solution. The journey is derived from Artifact kinds, stages,
revisions, review states, and decisions. Ideate exposes explicit Idea Pool and
Concept Portfolio entries with counts and current decision status.

No journey status is stored in HTML or hard-coded in JavaScript.

### Idea Pool decision view

The reader projects canonical Seed data by OA. Each OA header shows total Seed
count, recommended remaining count, confirmed count, and review state.

Every Seed row shows:

- ID and one-sentence Idea;
- source Insight references;
- cluster;
- Strategy filter;
- derived keep/cut recommendation;
- required cut rationale when applicable; and
- human confirmation state.

All 10–15 Seeds remain visible. Recommended cuts may be visually de-emphasized
but are never removed. Read-only filters may show all, recommended keeps, or
recommended cuts. Filters change presentation only. The page tells the human
to return the chosen `CS-` IDs in conversation; it does not collect or persist
the decision.

### Concept Portfolio decision view

The reader first shows a compact OA-grouped comparison table containing:

- Concept ID and name;
- pithy description;
- distinct mechanism;
- Consumer Magic;
- Commercial Money; and
- reviewer recommendation and key finding.

Full Concept cards follow the comparison table and project all canonical
fields, including Who / What / How / What it replaces / Why Big, Insights,
Money and Magic, tension, assumptions, principles, visualization, hard and soft
review results, and recommended action.

The default view contains current candidates only. Selected items remain
clearly marked; killed and merged history is available in a collapsed section.
Read-only filters may narrow by OA, review recommendation, or decision state.
The page tells the human to return 2–4 `CI-` IDs in conversation.

### Body and legacy behavior

Structured decision views are rendered from frontmatter. The Markdown body is
rendered afterward for explanatory notes and history. If body prose conflicts
with structured fields, the structured fields remain authoritative and
validation reports the inconsistency where it can be detected.

Legacy Artifacts without new review fields remain readable. HTML labels them
as not reviewed under the new contract and displays available content. It does
not infer missing rationales, review findings, or readiness.

## Validation and failure behavior

Runtime validation blocks:

- fewer than 10 or more than 15 Seeds in an OA;
- recommended cuts whose complement is outside 5–8;
- missing or foreign recommended-cut IDs;
- a populated confirmed set outside 5–8;
- a confirmed ID outside its OA;
- Concept development before all OA confirmations are valid;
- missing, duplicate, unconfirmed, or cross-OA initial Concept lineage;
- a review that omits a current candidate;
- Concept decision readiness while review is `needs-revision`; and
- a final selection outside 2–4 valid Concepts across the full Portfolio.

Structural validation enforces count, identity, lineage, and authority.
Judgment about novelty, quality, Magic, Money, or test altitude remains the
reviewer's responsibility and is recorded transparently rather than converted
into brittle schema rules.

## Testing

Implementation follows TDD and covers at least:

- Idea boundaries at 9, 10, 15, and 16;
- confirmed and recommended-remaining boundaries at 4, 5, 8, and 9;
- missing, duplicate, foreign, and cross-OA IDs;
- required recommended-cut rationales;
- blocked Concept generation from incomplete confirmation;
- exact initial confirmed-Seed-to-Concept lineage;
- reviewer attempts to populate human-only fields;
- exact coverage of current candidates by `reviewed_concept_ids`;
- HTML OA grouping, complete Seed visibility, comparison rows, full Concept
  cards, review findings, terminal-history collapse, and read-only filtering;
- legacy Artifact rendering without fabricated Review data; and
- an end-to-end three-OA funnel: 10–15 Seeds per OA, 5–8 confirmed and developed
  per OA, then 2–4 Concepts selected globally.

A regression test asserts the source-of-truth boundary: all business content
rendered into decision views must originate in parsed Artifact Markdown or be a
deterministic calculation from it. HTML fixtures cannot supply shadow business
data.

## Expected implementation surfaces

The implementation is expected to touch:

- `bw-concept-seed` and its Idea Pool template;
- `bw-concept-development` and its Concept Portfolio template;
- the shared Idea/Concept/Solution lifecycle contract;
- the Ideate router reference and affected eval scenarios;
- `src/bw/concept_lifecycle.py` and its tests;
- `src/bwkit/html.py` and its tests; and
- deployed skill copies generated through the installer.

Exact file sequencing belongs in the implementation plan. Source skill changes
must be deployed through the existing installer flow. Active project Artifacts
and generated lifecycle state are not regenerated by this design change; doing
so requires separate explicit authorization.

## Non-goals

- A new Ideate stage or gate.
- A second Idea Pool or Concept Portfolio per OA.
- HTML-based decision persistence or direct state mutation.
- Reviewer authority to confirm, select, merge, kill, sign, or choose an exit.
- Deep commercial feasibility review at the one-line Idea Seed layer.
- Regeneration of the active case's Artifact or state revisions.
