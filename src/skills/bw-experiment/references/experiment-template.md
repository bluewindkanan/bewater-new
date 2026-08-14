# Experiment template

An experiment is a pre-committed bet: thresholds fixed before results. File:
`_bewater-output/artifacts/EXP-xxx-rN-experiment.md` (append-only; `experiment:EXP-001@2` typed ref).

## Design approval — all fixed before execution

- target assumption references;
- method and target evidence level;
- metric and baseline;
- **Proceed threshold**;
- **Kill threshold**;
- treatment of inconclusive results;
- owner, timebox, and evidence-capture path.

An Achilles-Heel experiment MUST target L4+ behavioral evidence.

## Record result

- observed result and metric values;
- raw evidence references (each is an `evidence:E-xxx@n` entry in `_bewater/evidence.yaml`);
- achieved evidence level and why;
- conclusion: supported | falsified | inconclusive;
- proposed ledger changes;
- the human decision: proceed | kill | retest;
- artifact and ledger revisions changed by the result.

The human makes the Kill/Proceed decision. A falsified assumption initiates bw-backtrack.

## Evidence levels — L4+ is behavioral

| L4 | behavioral signal (non-real-transaction) | fake-site sign-up, ad CTR |
| L5 | real behavior / real payment | crowdfunding order, pilot purchase |
| L6 | sustained repeatable result | stable across multiple runs |

Achilles Heels must be validated with L4+ real-behavior evidence, not L1–L3 "say-so".

## Experiment menu — source for the method field

fake-website (sign-up intent) · social A/B (click intent, CTR ~0.9%) · crowdfunding (real WTP, L5)
· mom-test (real behavior, ask "what did you do") · related-worlds (analogue feasibility) · expert
interview (technical/regulatory, L2) · Van Westendorp (price band) · guerrilla interview (cheap
behavioral signal). Principle: keep it simple + define metrics first.

## Artifact frontmatter (kind: experiment)

```yaml
schema_version: 1
artifact_id: EXP-001
revision: 1
supersedes_ref: null
kind: experiment
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated
solution_ref: artifact:ART-010@2  # exact Solution revision under test in Shape
target_assumption_refs: []   # e.g. [assumption:A-003@2]
target_evidence_level: L4
proceed_threshold: ""
kill_threshold: ""
conclusion: null             # supported | falsified | inconclusive (filled on record)
derived_from: []
signoffs: []
stale_reason: null
```

`solution_ref` is required for a Shape-stage Solution experiment. It never
causes source-Concept assumptions to be copied or relayered. Allocate the EXP-id
from `config.next_ids.experiment`; write via bwkit. Field semantics:
`../_bw-shared/ledger-schema.md`.
