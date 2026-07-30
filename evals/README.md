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

## Phase 2b

Phase 2b adds the Shape stage (bw-shape + bw-experiment / bw-solution-shape / bw-investment-narrative),
the G2 gate (bw-concept-gate), and bw-backtrack. Safety-critical gate scenarios (`g2-go`,
`g2-no-authority`, `g2-conditional`) carry `repetition_count: 5` for the deferred fresh-context LLM
gate (§11.1). The G2 state mechanics (decision record → action plan → G2 baseline + execution
handoff + branch advance + idempotent re-run) are proven deterministically by
`tests/test_g2_closed_loop.py` via `bwkit plan apply`; backtrack impact is proven by
`tests/test_backtrack_lineage.py` via the Phase 2a `lineage.transitive_dependents` helper.

## Phase 2 Eval Gate (§11.1) — Pilot + Cost Estimate

The fresh-context eval harness (`evals/_harness/`) is pilot-ready (T1–T6 complete,
316 tests pass). Each behavioral scenario runs headless `claude -p` in an isolated
temp HOME + repo-external cwd; the 20-skill full run is the Phase-2 acceptance gate.

### Pilot Findings (2026-07-30, bw-shape × 3 reps)

| Metric | GREEN | RED |
|--------|-------|-----|
| Wall-clock per run | ~85s | ~38s |
| Verdict signal | routes_to_capability pass/fail (mechanical) | routes absent = correct RED |
| NL assertions | needs-review (human, per design) | needs-review (human) |

Feasibility confirmed: headless `claude` runs under isolated temp HOME with
`ANTHROPIC_API_KEY` passthrough. End-to-end discover→run→judge→write works.

### Full-Run Cost Estimate

| Item | Count |
|------|-------|
| Skills with GREEN scenarios | 20 |
| Skills with RED controls | 20 |
| Scenarios per skill (avg) | ~1.5 (GREEN) + 1 (RED) |
| Reps per scenario | 3 (standard), 5 (safety-critical: G1 + G2 gates) |
| **Total fresh-context runs** | **~140** |
| **Estimated wall-clock** | **~2.5 hours** |
| **Token cost** | significant (every run is a fresh context, no cache reuse) |

Safety-critical scenarios (×5 reps): `bw-strategy-gate` (g1-go, g1-no-authority),
`bw-concept-gate` (g2-go, g2-no-authority, g2-conditional).

### Pre-Flight Checklist

Before the full run:
- [x] Transcript persisted to durable `evals/{skill}/{mode}/` (F1)
- [x] GREEN result path aligned: `scenarios/` manifests → `green/` results (F2)
- [x] Verify gate accepts partial coverage (F3)
- [x] Structured `checks:` added to bw-shape orient manifest
- [ ] Remaining manifests: add `checks:` fields mapping NL assertions → mechanical checks
- [ ] Run `python -m evals bw-shape --mode green --rep 3` (verify GREEN routing)
- [ ] Run full `python -m evals --all --mode red && python -m evals --all --mode green`
- [ ] Human review all `needs-review` items, fill `reviewer` field
- [ ] `python scripts/verify.py` → eval-results gate enforces all scenarios
