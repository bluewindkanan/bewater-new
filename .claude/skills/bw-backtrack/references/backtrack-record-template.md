# Backtrack record template (spec §8.3)

Canonical path: `_bewater/records/<backtrack-id>-backtrack.yaml`. Allocate the BT-id from
`config.next_ids.backtrack` and the action's IDs while holding the §5.7 lock, BEFORE other state
change.

```yaml
schema_version: 1
revision: 1
backtrack_id: BT-001
branch_id: BR-001
trigger_ref: assumption:A-001@4        # the falsified/changed upstream record
affected_refs: []                      # transitive dependents (lineage.transitive_dependents output)
baseline_refs: []                      # affected baseline:B-xxx pointers
loop_type: small                       # small | large (active_baselines touch => large)
target_stage: shape                    # the named earlier stage the branch resets to
gates_to_rerun: []                     # gate:D-xxx refs for a large loop
decision_maker: {person: null, role: null, authority_level: null}
decided_at: null
status: planned                        # planned | active | resolved
action_plan:
  action_id: ACT-002
  expected_revisions: {config: 6}
  ordered_steps:                       # {step_id, operation, target_ref, status: pending|applied|skipped|failed}
    - {step_id: s1, operation: cas_commit, target_ref: _bewater/config.yaml, status: pending}
  action_status: pending               # pending | applied | aborted | manual-repair
  conflict_refs: []
  resolution: null                     # {mode, authority, rationale, followup_action_id}
change_history: []
```

Status becomes `resolved` only after every required ordered step is verified applied or intentionally
skipped. Field semantics: `../_bw-shared/ledger-schema.md`.
