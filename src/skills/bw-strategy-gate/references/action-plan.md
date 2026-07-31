# Action-plan application

The gate builds a JSON plan of deterministic write-ops and applies it via bwkit. bwkit is
schema-agnostic — it sees only `{path, new_text, expected_revision?}`, never business
fields. The gate is responsible for serializing each target's new text (bump the envelope
`revision` in config/ledger/conditions; new files for baseline/decision/backtrack).

## Build the plan

One `steps` entry per ordered action. `cas_commit` for revisioned files
(`_bewater/config.yaml`, `ledger.yaml`, `conditions.yaml`); `write_new` for new immutable
records (`_bewater/records/B-001-baseline.yaml`, a backtrack record). Example G1 Go plan:

```json
{"action_id": "ACT-001", "owner": "bw-strategy-gate", "steps": [
  {"step_id": "s1", "op": "write_new",
   "path": "_bewater/records/B-001-baseline.yaml", "new_text": "<baseline yaml>"},
  {"step_id": "s2", "op": "cas_commit", "path": "_bewater/config.yaml",
   "expected_revision": 4,
   "new_text": "<config with revision: 5, current_stage: ideate, active_baselines.G1: B-001>"}
]}
```

## Apply

    bwkit plan apply <root>   < plan.json

`apply_plan` acquires the single-writer lock, applies each step idempotently (already-done
→ `skipped`; content mismatch or revision conflict → `failed`, stops), and returns
`{action_id, results:[{step_id, status, detail}], action_status}`. On interruption, re-run
the same plan — completed steps verify as `skipped`.

## Record back

Write the per-step `status` and `action_status` into the decision record's
`action_plan.ordered_steps[].status` / `action_plan.action_status` via a CAS commit on the
record file. `manual-repair` blocks further state-changing skills until the accountable
human resolves it. The gate never chooses an exit and bwkit never touches the record.
