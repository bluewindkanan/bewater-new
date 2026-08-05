schema_version: 1
revision: 1
decision_id: D-001
attempt: 1
gate: G1
branch_id: BR-001
subject_refs: []
decision_maker: {person: "Eval Owner", role: "Product Owner", authority_level: product-owner}
trigger: {kind: event, due_at: null}
input_revisions: {ledger: 1, artifacts: []}
checklist_results: []
exit: Go
condition_ids: []
action_plan:
  action_id: ACT-001
  expected_revisions: {config: 2, ledger: 1}
  target_stage: ideate
  allowed_work: []
  resource_envelope: null
  successor_branch_id: null
  baseline_id: B-001
  supersedes_handoff_ref: null
  ordered_steps:
    - {step_id: s1, operation: write_new, target_ref: _bewater/records/B-001-baseline.yaml, status: pending}
    - {step_id: s2, operation: cas_commit, target_ref: _bewater/config.yaml, status: pending}
  action_status: pending
  conflict_refs: []
  resolution: null
supersedes_ref: null
decided_at: "2026-07-31T00:00:00Z"
validity: active
methodology_deviation: null
change_history: []
