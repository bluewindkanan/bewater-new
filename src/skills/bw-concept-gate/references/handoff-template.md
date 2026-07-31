# Execution handoff template

A G2 Go writes `_bewater-output/execution-handoff.md` — derived output, regenerable from canonical
state, the source G2 decision projection handed to execution. One active handoff per project;
`config.active_execution_handoff` points directly to the source `gate:D-xxx` decision (no separate
handoff ID). Before replacing the current handoff, the G2
decision names the gate decision it supersedes (`supersedes_handoff_ref`); the skill moves the prior
file to `_bewater-output/execution-handoff-{prior-decision-id}-archived.md`.

```yaml
---
schema_version: 1
branch_id: BR-001
status: active
source_g2_decision: gate:D-001
baseline_ref: baseline:B-001
validated_solutions: []      # every validated solution in the G2 subject_refs
investment_narrative_ref: artifact:ART-008@1
financial_case: ""
open_assumptions_to_monitor: []   # observations to watch during execution
exact_source_revisions: {config: 5, ledger: 12}
---
```

The body carries the narrative + financial case handed to execution. A G2 Conditional Go may create
`_bewater-output/provisional-handoff-{decision-id}.md` (its condition IDs + resource envelope) — no
baseline reference, never `active_execution_handoff`, never presented as validated. If a handoff's G2
decision or baseline is invalidated, the backtrack action archives it, removes the projection, and
clears `config.active_execution_handoff` before further routing.
