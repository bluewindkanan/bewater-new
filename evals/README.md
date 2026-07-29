# BeWater evals

Phase 1a authors **scenario manifests** (`<skill>/scenarios/`) and **RED controls**
(`<skill>/red/`) only. The fresh-context LLM GREEN runs (spec §11.1 — 3 repetitions, 5/5
for safety-critical) are the **deferred Phase-1 acceptance gate** and are executed in a
separate pass once the Phase 1b G1 closed loop is in place. Structural correctness is
covered now by `scripts/verify.py` and the per-skill pytest; state-write correctness rides
on the Plan-1 `bwkit` CAS.
