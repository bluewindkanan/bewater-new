# G2 action-plan application (spec §5.7, §6.5, §6.6, §12.3)

The gate builds a JSON plan of deterministic write-ops and applies it via bwkit. bwkit is
schema-agnostic — it sees only `{path, new_text, expected_revision?}`. The gate serializes each
target's new text (bump the envelope `revision` in config/ledger/conditions; new files for the G2
baseline, the decision record, the handoff).

## Example G2 Go plan

```json
{"action_id": "ACT-001", "owner": "bw-concept-gate", "steps": [
  {"step_id": "s1", "op": "write_new",
   "path": "_bewater/records/B-001-baseline.yaml", "new_text": "<G2 baseline yaml>"},
  {"step_id": "s2", "op": "write_new",
   "path": "_bewater-output/execution-handoff.md", "new_text": "<handoff>"},
  {"step_id": "s3", "op": "cas_commit", "path": "_bewater/config.yaml",
   "expected_revision": 5,
   "new_text": "<config with revision: 6, current_stage: handoff-ready, active_baselines.G2: B-001, active_execution_handoff: gate:D-001>"}
]}
```

## Apply

    bwkit plan apply <root>   < plan.json

`apply_plan` acquires the single-writer lock, applies each step idempotently (already-done →
`skipped`; content mismatch or revision conflict → `failed`, stops), and returns
`{action_id, results:[{step_id, status, detail}], action_status}`. On interruption, re-run the same
plan — completed steps verify as `skipped`. Run `bwkit check integrity` on the subject artifacts
before presenting exits; on corruption, stop and surface the conflicting files (§5.4).

## Record back

Write the per-step `status` and `action_status` into the decision record's
`action_plan.ordered_steps[].status` / `action_plan.action_status` via a CAS commit on the record
file. `manual-repair` blocks further state-changing skills until the accountable human resolves it
(§6.5). The gate never chooses an exit and bwkit never touches the record (§12.2).
