# Charter persistence plan

This is the **only allowed project-state mutation path** after L0 validation and the Charter
self-review passes. L0 is fail-closed: a failed staged Charter must emit no action plan and
must cause zero project-state writes.

```text
PYTHONPATH=_bewater python3 -m bwkit plan apply .
```

Do not inspect the runtime or invoke CLI `--help`. Stage the complete Charter and config
texts outside the project, then use the provided emitter and pipe it directly to the applier:

```text
python3 .claude/skills/bw-immersion/scripts/emit_charter_plan.py \
  --action-id charter:ART-001@1 \
  --owner bw-immersion \
  --artifact-path _bewater-output/ART-001-r1-charter.md \
  --artifact-file /tmp/charter.md \
  --cas-step artifact-counter _bewater/config.yaml 2 /tmp/config.yaml \
| PYTHONPATH=_bewater python3 -m bwkit plan apply .
```

The emitter runs `scripts/validate_draft.py` before printing JSON and rejects any ledger CAS step.
On a validation failure it prints diagnostics to
standard error, exits non-zero, and emits no plan. Do not bypass that check or pipe an unvalidated
plan to the applier.

Never use Edit or Write on project state. Never use shell redirection, a heredoc, or a general-purpose script to create or change
`_bewater/` or `_bewater-output/` files directly. A script may serialize the plan to standard output
only; `bwkit plan apply` must perform every project-state write.

For a first Charter, construct one ordered plan with:

1. `write_new` for the immutable Charter revision under `_bewater-output/`;
2. `cas_commit` for the complete config revision with `next_ids.artifact` advanced once.

The Charter step must precede the config update so an identical resumable retry can skip the
already-appended revision and complete only the missing CAS-protected steps. A later Charter revision
uses the same ART ID, adds the next immutable revision with `write_new`, and does not advance the
artifact counter. Charter persistence never mutates `_bewater/ledger.yaml`.

Require `action_status: applied` and every step to be `applied` or `skipped`. If any step fails, do
not repair files directly; re-read the heads and counters, then resume the identical plan or fail
closed. Run revision-chain integrity after the transaction succeeds.
