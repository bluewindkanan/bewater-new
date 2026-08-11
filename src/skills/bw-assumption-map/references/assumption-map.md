# Assumption map

Assumptions are classified by **category** (consumer / commercial / technical /
distribution / regulatory) and plotted on two axes:

- **impact** (high / medium / low): how hard it hits if wrong;
- **uncertainty** (high / medium / low): how little we know.

The **Achilles-Heel** quadrant = impact=high AND uncertainty=high. These are tested first,
with L4+ behavioral evidence. `is_achilles_heel` is *derived*; once an assumption has been
high-impact + high-uncertainty, the resulting L4 obligation is durable — lowering either
field does not erase it (`l4_obligation_status` stays open until L4+ evidence or a
human-signed reclassification).

## Ledger write

Each assumption is a record under `ledger.yaml:assumptions:` with `record_revision`,
`layer`, `category`, `side`, `impact`, `uncertainty`, `evidence_level`, `validation_status`,
`status`, `evidence_refs`, `derived_from`, `supersedes_ref`, `risk_history`,
`l4_obligation_status`, `history`. Allocate the A-id from `ledger.next_id`; bump the record
`record_revision` (store prior snapshot in `history`) and the envelope `revision`. Write via
`bwkit lock acquire` + `cas commit`. Field semantics: `../_bw-shared/ledger-schema.md`.

G1 readiness requires an initial inventory with the Achilles-Heel quadrant identified
(`../_bw-shared/gate-criteria.md`).

## Concept-layer assumptions

Concept-level assumptions surfaced in Ideate (by bw-concept-development) are
mapped like any other assumption: `layer: concept`, classified by `category`,
plotted on impact × uncertainty. Each carries `derived_from` set to the exact
`concept-portfolio` revision it came from and a validated `source_concept_id`
(the `CI-NNN` it belongs to), so a portfolio-item change propagates to its
assumptions. Achilles-Heel concept assumptions raise the same durable L4
obligation and are resolved downstream in Shape/G2, not at Ideate. Lifecycle
contract: `../_bw-shared/idea-concept-solution-lifecycle.md`.

## Solution-layer assumptions

Solution assumptions use `layer: solution` and `derived_from` the exact Solution
revision that introduced them. A Solution references, but never copies or
relayers, source-Concept assumptions. Its pinned Achilles snapshot must equal
the exact union of open durable L4 obligations from every selected source
Concept plus open Solution-layer obligations. References include stable ID and
record revision (`assumption:A-NNN@record_revision`); stale, missing, extra, or
unresolved pins fail validation.
