# G2 decision record template

Canonical path: `_bewater/records/<decision-id>-gate.md`. Allocate the D-id and the action's
baseline/handoff/backtrack/branch/condition IDs from `config.next_ids` (and `conditions.next_id`)
while holding the lock, BEFORE writing any other state. The decision core (through `exit`) is
immutable after the human decides; only revisioned operational fields change.

```yaml
schema_version: 1
revision: 1
decision_id: D-001
attempt: 1
gate: G2
branch_id: BR-001
subject_refs: []          # e.g. [artifact:ART-007@2, artifact:ART-008@1] (1-2 validated solutions + narrative)
decision_maker: {person: null, role: null, authority_level: investment-decision}
trigger: {kind: event, due_at: null}
input_revisions: {ledger: "assumption:...", artifacts: []}
checklist_results: []     # per-criterion pass/fail/unknown + evidence
exit: null                # Go | Conditional Go | Recycle | Pivot | Kill — HUMAN chooses
condition_ids: []
action_plan:
  action_id: ACT-001
  expected_revisions: {config: 5, ledger: 12}
  target_stage: handoff-ready
  allowed_work: []
  resource_envelope: null
  successor_branch_id: null
  baseline_id: null           # B-xxx for a Go
  supersedes_handoff_ref: null   # gate:D-xxx whose handoff a Go replaces
  ordered_steps:              # {step_id, operation, target_ref, status: pending|applied|skipped|failed}
    - {step_id: s1, operation: write_new, target_ref: _bewater/records/B-001-baseline.yaml, status: pending}
    - {step_id: s2, operation: write_new, target_ref: _bewater-output/execution-handoff.md, status: pending}
    - {step_id: s3, operation: cas_commit, target_ref: _bewater/config.yaml, status: pending}
  action_status: pending      # pending | applied | aborted | manual-repair
  conflict_refs: []
  resolution: null            # {mode, authority, rationale, followup_action_id} on manual-repair
supersedes_ref: null
decided_at: null
validity: active              # active | superseded | invalidated
methodology_deviation: null
change_history: []
```

`subject_refs` lists the 1–2 validated solutions + the investment narrative under assessment. Write
this record first with `action_status: pending`; apply the plan; then record step statuses back via a
CAS commit on this same file (`revision` 2).
