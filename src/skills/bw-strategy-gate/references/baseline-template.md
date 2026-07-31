# Baseline template

A Go creates `_bewater/records/<baseline-id>-baseline.yaml`. The file is immutable by
protocol. The branch's `active_baselines.G1` points at it; revalidation creates a new
decision + baseline and switches the pointer through the action plan.

```yaml
schema_version: 1
baseline_id: B-001
gate: G1
decision_id: D-001
branch_id: BR-001
created_at: "2026-07-28T12:00:00Z"
supersedes_ref: null
input_refs:
  strategy: artifact:ART-005@1
  opportunity: artifact:ART-006@1
  ledger_revision: 12
depends_on_baseline: null
checklist_result: []
frozen:
  strategy_statement: ""
  opportunity_areas: []
  assumption_inventory: []
  money_magic_judgment: ""
```

G1 baseline freezes the signed insights, locked strategy, opportunity portfolio, initial
assumption portfolio, and the Money + Magic judgment.
