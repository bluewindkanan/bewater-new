# Charter persistence plan

This is the **only allowed project-state mutation path** after L0 validation and the Charter
self-review passes. L0 is fail-closed: a failed staged Charter or ledger must emit no action plan and
must cause zero project-state writes.

```text
PYTHONPATH=_bewater python3 -m bwkit plan apply .
```

Do not inspect the runtime or invoke CLI `--help`. Stage the complete Charter, ledger, and config
texts outside the project, then use the provided emitter and pipe it directly to the applier:

```text
python3 .claude/skills/bw-project-charter/scripts/emit_write_plan.py \
  --action-id project-charter:ART-001@1 \
  --owner bw-project-charter \
  --artifact-path _bewater-output/ART-001-r1-charter.md \
  --artifact-file /tmp/charter.md \
  --ledger-file /tmp/ledger.yaml \
  --cas-step ledger _bewater/ledger.yaml 2 /tmp/ledger.yaml \
  --cas-step artifact-counter _bewater/config.yaml 2 /tmp/config.yaml \
| PYTHONPATH=_bewater python3 -m bwkit plan apply .
```

`--ledger-file` must be the same staged file supplied to the ledger `cas-step`. The emitter runs
`scripts/validate_draft.py` before printing JSON. On a validation failure it prints diagnostics to
standard error, exits non-zero, and emits no plan. Do not bypass that check or pipe an unvalidated
plan to the applier.

Never use Edit or Write on project state. Never use shell redirection, a heredoc, or a general-purpose script to create or change
`_bewater/` or `_bewater-output/` files directly. A script may serialize the plan to standard output
only; `bwkit plan apply` must perform every project-state write.

For a first Charter, construct one ordered plan with:

1. `write_new` for the immutable Charter revision under `_bewater-output/`;
2. `cas_commit` for the complete ledger revision containing 3–5 new active root assumptions and
   the advanced assumption counter;
3. `cas_commit` for the complete config revision with `next_ids.artifact` advanced once.

The Charter step must precede ledger and config updates so an identical resumable retry can skip the
already-appended revision and complete only the missing CAS-protected steps. A later Charter revision
uses the same ART ID, adds the next immutable revision with `write_new`, updates changed assumptions
through one ledger `cas_commit`, and does not advance the artifact counter.

Require `action_status: applied` and every step to be `applied` or `skipped`. If any step fails, do
not repair files directly; re-read the heads and counters, then resume the identical plan or fail
closed. Run revision-chain integrity after the transaction succeeds.
