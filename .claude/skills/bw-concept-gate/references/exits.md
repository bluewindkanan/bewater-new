# G2 exits and actions (spec §6.4, §6.6)

The gate presents these five exits; the **human** chooses. Each row is the exact state action the
gate encodes into the decision record's action plan.

- **Go** — every required criterion passes and investment-decision authority is resolved; the
  project handoff slot is empty or the decision explicitly supersedes the active handoff.
  Action: create the immutable G2 baseline (`B-xxx`, `references/baseline-template.md`); advance the
  branch `current_stage: handoff-ready`; set `active_baselines.G2: B-xxx`; write the execution
  handoff (`_bewater-output/execution-handoff.md`, `references/handoff-template.md`) and set
  `config.active_execution_handoff: gate:D-xxx`. One active handoff per project; replacing the prior
  handoff sets `supersedes_handoff_ref` and archives the prior file as
  `execution-handoff-{prior-decision-id}-archived.md`.
- **Conditional Go** — a bounded, remediable gap has explicit conditions; never used to treat a
  failed G2 hard-evidence (L4) criterion as validated. Action: write condition-registry entries
  (`C-xxx` in `conditions.yaml`) before any allowed work; mark the gate conditional; enter a
  constrained closeout-directed state under an explicit `allowed_work` + `resource_envelope`; write
  only a provisional handoff (`_bewater-output/provisional-handoff-{decision-id}.md`). Do NOT create
  a validated baseline or occupy `active_execution_handoff`. Mandatory closeout (re-evaluate every
  criterion, stop for the same authority, record a new Go that supersedes this one) is required
  before the next gate is eligible.
- **Recycle** — more work needed without changing direction. Action: create a backtrack record
  (`BT-xxx` via bw-backtrack); set the branch to the named earlier stage; retain all evidence.
- **Pivot** — the direction/solution premise must materially change. Action: check active baselines
  first; create a successor branch; route the change depth (feature/concept → Ideate/Shape local
  reframe when no baseline touched; opportunity/strategy → Define + G1; root → Discover + G1);
  invalidate only dependent downstream decisions.
- **Kill** — no further resources. Action: invalidate prior active gate decisions, clear
  active-baseline pointers, archive/remove this branch's active execution-handoff projection and
  clear `config.active_execution_handoff`, close branch conditions with authority + reason, then mark
  the branch killed LAST. Preserve all artifacts, assumptions, experiments, evidence.

A human who insists on Go while a required criterion fails gets a **methodology deviation** record
instead — never `exit: go`, never a baseline, never an execution handoff (§6.7).
