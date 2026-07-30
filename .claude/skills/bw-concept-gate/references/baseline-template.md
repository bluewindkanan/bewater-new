# G2 baseline template (spec §6.6)

A G2 Go creates `_bewater/records/<baseline-id>-baseline.yaml`. The file is immutable by protocol.
The branch's `active_baselines.G2` points at it; revalidation creates a new decision + baseline and
switches the pointer through the action plan.

```yaml
schema_version: 1
baseline_id: B-001
gate: G2
decision_id: D-001
branch_id: BR-001
created_at: "2026-07-29T12:00:00Z"
supersedes_ref: null
input_refs:                   # exact gate input references + revisions
  solutions: []               # e.g. [artifact:ART-007@2]
  investment_narrative: artifact:ART-008@1
  ledger_revision: 12
depends_on_baseline: null     # upstream active G1 baseline, if any
checklist_result: []          # frozen G2 checklist result
frozen:
  validated_solutions: []     # solution + investment narrative artifact refs + revisions
  assumption_snapshot: []     # in-scope assumptions + validation conclusions + evidence levels + evidence refs
  open_observations: []       # open assumptions that remain observations, not gate blockers
  strategy_opportunity_lineage: []
```

A G2 baseline additionally freezes (spec §6.6): exact solution and investment-narrative artifact
references and revisions; a frozen snapshot of in-scope assumptions with validation conclusions,
evidence levels, and evidence references; open assumptions that remain observations rather than gate
blockers; and the strategy and opportunity lineage.
