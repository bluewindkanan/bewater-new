# BeWater evals

Phase 1a authors **scenario manifests** (`<skill>/scenarios/`) and **RED controls**
(`<skill>/red/`) only. The fresh-context LLM GREEN runs (spec §11.1 — 3 repetitions, 5/5
for safety-critical) are the **deferred Phase-1 acceptance gate** and are executed in a
separate pass once the Phase 1b G1 closed loop is in place. Structural correctness is
covered now by `scripts/verify.py` and the per-skill pytest; state-write correctness rides
on the Plan-1 `bwkit` CAS.

## Phase 1b

Phase 1b adds the four Define capabilities and `bw-strategy-gate`. The gate's
safety-critical scenarios (`g1-go`, `g1-no-authority`) carry `repetition_count: 5` for the
deferred fresh-context LLM gate (§11.1). The G1 state mechanics (decision record → action
plan → baseline + branch advance → idempotent re-run) are proven deterministically by
`tests/test_g1_closed_loop.py` via `bwkit plan apply`, independent of any LLM run.
