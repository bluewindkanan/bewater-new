# G1 exits and actions (spec §6.4)

The gate presents these five exits; the **human** chooses. Each row is the exact state
action the gate encodes into the decision record's action plan.

- **Go** — every required criterion passes and product-owner authority is resolved.
  Action: create the G1 baseline (`B-xxx`); advance the branch `current_stage: ideate`;
  set `active_baselines.G1: B-xxx`.
- **Conditional Go** — a bounded, remediable gap has explicit conditions; never used to
  treat a failed hard criterion as satisfied. Action: write condition-registry entries
  (`C-xxx` in `conditions.yaml`) before any allowed work; mark the gate conditional;
  advance the branch `current_stage: ideate`. Do NOT create a validated baseline. The next
  gate stays ineligible until a later Go supersedes this decision (re-evaluates every
  criterion, stops for the same authority, records a new Go).
- **Recycle** — more work needed without changing direction. Action: create a backtrack
  record (`BT-xxx`); set the branch to the named earlier stage; retain all evidence.
- **Pivot** — the direction/premise must materially change. Action: check active baselines
  first; create a successor branch; route the change depth (feature/concept → Ideate/Shape
  local reframe; opportunity/strategy → Define + G1; root → Discover + G1); invalidate
  only dependent downstream decisions.
- **Kill** — no further resources. Action: invalidate prior active gate decisions, clear
  active-baseline pointers, close branch conditions with authority + reason, then mark the
  branch killed LAST. Preserve all artifacts, assumptions, experiments, evidence.

A human who insists on Go while a required criterion fails gets a **methodology deviation**
record instead — never `exit: go`, never a baseline (§6.7).
