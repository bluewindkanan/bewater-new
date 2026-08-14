# Initial Assessment write plan

This is the **only allowed project-state mutation path**. Build the JSON plan in memory or emit it
to standard output, then invoke:

```text
PYTHONPATH=_bewater python3 -m bwkit plan apply .
```

Do not inspect the runtime or invoke CLI `--help`. Stage only the artifact text and the complete
next config text outside the project, then use the provided emitter and pipe it directly to the
applier:

```text
python3 .claude/skills/bw-immersion/scripts/emit_assessment_plan.py \
  --action-id assessment:ART-002@1 \
  --owner bw-immersion \
  --artifact-path _bewater-output/artifacts/ART-002-r1-initial-assessment.md \
  --artifact-file /tmp/assessment.md \
  --cas-step artifact-counter _bewater/config.yaml 2 /tmp/config.yaml \
| PYTHONPATH=_bewater python3 -m bwkit plan apply .
```

`plan apply` acquires and releases the write lock. Do not call `bwkit lock acquire` separately.
Do not run Git, environment, executable, directory-tree, or CLI discovery commands; the fresh
sandbox and this reference are the complete execution interface.

Never use Edit or Write on project state. Never use shell redirection, a heredoc, or a
general-purpose script to create or change `_bewater/` or `_bewater-output/` files directly. A script may serialize the JSON plan to standard
output only; `bwkit plan apply` must perform every project-state write.

For the first Assessment, the emitter produces exactly this ordered shape:

```json
{
  "action_id": "assessment:ART-002@1",
  "owner": "bw-immersion",
  "steps": [
    {
      "step_id": "assessment-revision",
      "op": "write_new",
      "path": "_bewater-output/artifacts/ART-002-r1-initial-assessment.md",
      "new_text": "<complete confirmed artifact text>"
    },
    {
      "step_id": "artifact-counter",
      "op": "cas_commit",
      "path": "_bewater/config.yaml",
      "expected_revision": 2,
      "new_text": "<complete config with revision 3 and next_ids.artifact advanced once>"
    }
  ]
}
```

The artifact step must precede the counter step so a resumable retry can recognize an identical
append-only file before completing the CAS-protected counter update. For reassessment, use one
`write_new` step for the next revision of the existing ART ID; do not advance the artifact counter.

Require `action_status: applied` and every result to be `applied` or `skipped`. On any failed step,
do not repair state directly. Re-resolve the input snapshot and either resume the identical plan or
fail closed. After the plan succeeds, run revision-chain integrity with the exact emitter pipe; the
`check integrity` command takes JSON on stdin and takes no root argument:

```text
python3 .claude/skills/bw-immersion/scripts/emit_integrity_payload.py \
  --record ART-001 1 null \
  --record ART-002 1 null \
| PYTHONPATH=_bewater python3 -m bwkit check integrity
```

Do not claim success merely because the file exists. Once the integrity result is `ok: true`, return
the final response immediately with no more tool calls.

The artifact body must be on the same branch as its Charter and `derived_from` must contain exactly
one entry: the exact Charter revision only. Never add Assessment claims, source citations, or the
Assessment revision to Research, the Knowledge Base, assumptions, or Evidence.
