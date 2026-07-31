# State bootstrap (authoritative v5 scaffold)

When bootstrapping, create the directories and write these files verbatim (substitute
`updated_at` with the real ISO-8601 time),
each through a bwkit `cas commit` with `--expected 0`-equivalent first write (for the
initial file, write it directly, then all subsequent edits go through CAS).

## Directory layout

    _bewater/
    ├── config.yaml
    ├── ledger.yaml
    ├── conditions.yaml
    └── records/
    _bewater-output/

## config.yaml

```yaml
schema_version: 1
revision: 1
updated_at: "2026-07-28T12:00:00Z"
updated_by: bw-start
next_ids:
  branch: 2
  artifact: 1
  experiment: 1
  decision: 1
  baseline: 1
  backtrack: 1
  action: 1
  evidence: 1
project:
  name: ""
  success_criteria: []
decision_authority:
  G1:
    level: product-owner
    accountable_person: null
    accountable_role: null
  G2:
    level: investment-decision
    accountable_person: null
    accountable_role: null
active_branch: BR-001
active_execution_handoff: null
branches:
  BR-001:
    status: active
    current_stage: immersion
    parent_ids: []
    merged_into: null
    gate_due_at:
      G1: null
      G2: null
    inherited_assumption_refs: []
    excluded_assumption_refs: []
    inherited_condition_ids: []
    needs_rebase_refs: []
    active_baselines:
      G1: null
      G2: null
```

## ledger.yaml

```yaml
schema_version: 1
revision: 1
next_id: 1
updated_at: "2026-07-28T12:00:00Z"
updated_by: bw-start
assumptions: {}
```

## conditions.yaml

```yaml
schema_version: 1
revision: 1
next_id: 1
updated_at: "2026-07-28T12:00:00Z"
updated_by: bw-start
conditions: {}
```

The first real edit to any of these files bumps `revision` to 2 via `bwkit cas commit
<path> --expected 1` with the bumped text on stdin (bwkit verifies the bump and keeps a
rotating backup). Field semantics: see `../_bw-shared/ledger-schema.md`.
