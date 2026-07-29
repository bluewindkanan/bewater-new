# Decision record template (spec §6.5)

Canonical path: `_bewater/records/<decision-id>-gate.md`. Allocate the D-id and the
action's baseline/backtrack/branch/condition IDs from `config.next_ids` (and
`conditions.next_id`) while holding the §5.7 lock, BEFORE writing any other state. The
decision core (through `exit`) is immutable after the human decides; only revisioned
operational fields (`ordered_steps[].status`, `action_status`, `validity`,
`change_history`) change.

```yaml
schema_version: 1
revision: 1
decision_id: D-001
attempt: 1
gate: G1
branch_id: BR-001
subject_refs: []
decision_maker: {person: null, role: null, authority_level: product-owner}
trigger: {kind: event, due_at: null}
input_revisions: {ledger: assumption-rev, artifacts: []}
checklist_results: []
exit: null
condition_ids: []
action_plan:
  action_id: ACT-001
  expected_revisions: {config: 4, ledger: 12}
  target_stage: ideate
  allowed_work: []
  resource_envelope: null
  successor_branch_id: null
  baseline_id: null
  supersedes_handoff_ref: null
  ordered_steps:
    - {step_id: s1, operation: write_new, target_ref: _bewater/records/B-001-baseline.yaml, status: pending}
    - {step_id: s2, operation: cas_commit, target_ref: _bewater/config.yaml, status: pending}
  action_status: pending
  conflict_refs: []
  resolution: null
supersedes_ref: null
decided_at: null
validity: active
methodology_deviation: null
change_history: []
```

`subject_refs` is a list (G1 typically assesses the locked strategy + opportunity portfolio).
Write this record first with `action_status: pending`; apply the plan; then record step
statuses back via a CAS commit on this same file (`revision` 2).
