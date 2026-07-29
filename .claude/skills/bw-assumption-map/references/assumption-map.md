# Assumption map (spec §5.3, §9.8)

Assumptions are classified by **category** (consumer / commercial / technical /
distribution / regulatory) and plotted on two axes:

- **impact** (high / medium / low): how hard it hits if wrong;
- **uncertainty** (high / medium / low): how little we know.

The **Achilles-Heel** quadrant = impact=high AND uncertainty=high. These are tested first,
with L4+ behavioral evidence. `is_achilles_heel` is *derived*; once an assumption has been
high-impact + high-uncertainty, the resulting L4 obligation is durable — lowering either
field does not erase it (`l4_obligation_status` stays open until L4+ evidence or a
human-signed reclassification).

## Ledger write (§5.3, §5.7)

Each assumption is a record under `ledger.yaml:assumptions:` with `record_revision`,
`layer`, `category`, `side`, `impact`, `uncertainty`, `evidence_level`, `validation_status`,
`status`, `evidence_refs`, `derived_from`, `supersedes_ref`, `risk_history`,
`l4_obligation_status`, `history`. Allocate the A-id from `ledger.next_id`; bump the record
`record_revision` (store prior snapshot in `history`) and the envelope `revision`. Write via
`bwkit lock acquire` + `cas commit`. Field semantics: `../_bw-shared/ledger-schema.md`.

G1 readiness requires an initial inventory with the Achilles-Heel quadrant identified
(`../_bw-shared/gate-criteria.md`).
