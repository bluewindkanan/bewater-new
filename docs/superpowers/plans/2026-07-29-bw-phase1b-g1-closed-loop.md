# BeWater Phase 1b — G1 Closed Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the Phase 1 G1 loop (spec §10.3): build the four Define-stage capabilities (directional hypothesis, strategy statement, opportunity areas, assumption map), the narrow `bwkit` action-plan applier, and `bw-strategy-gate` (all five G1 exits), so a fresh project can reach every G1 exit, resume after interruption, preserve branch/ledger integrity, and never record Go when G1 evidence or authority is unresolved.

**Architecture:** Four capability skills under `.claude/skills/bw-*/` produced by the same self-contained pattern as Plan 2a (SKILL.md + skill-local `references/` + eval manifests + a structural pytest reusing `tests/skill_helpers.py`). The state-write primitive is extended with one new stdlib-only `bwkit` module — `applier.py` — a schema-agnostic, idempotent, resumable action-plan runner that reuses `cas.commit` + `cas.acquire_lock` and never parses business YAML (the caller builds a JSON op-list; bwkit enforces the deterministic mechanism). `bw-strategy-gate` is a constrained adjudicator: it assembles evidence, presents the five permitted G1 exits, stops for the accountable human, preallocates IDs, writes the full decision record + action plan, then applies the plan via `bwkit plan apply` and records status back. Behavioral (fresh-context LLM) evals remain deferred to the phase-end gate (decision 2026-07-29); each task authors scenario manifests + deterministic structural/integration tests now.

**Tech Stack:** Python ≥3.11 (stdlib-only `bwkit`; PyYAML only in tests/schemas/harness). pytest + pytest-cov. Skills are markdown + `name`/`description`-only frontmatter. No new runtime dependencies.

## Global Constraints

- **Spec authority:** `docs/superpowers/specs/2026-07-27-bewater-decision-phase-skills-design.md` v5.1 + H1a. §4 catalog; §5 state contract (§5.3 ledger, §5.4 artifacts, §5.6 conditions); §5.7 direct-write; §6 gate contract (§6.1–6.6); §8.3 backtrack; §9.4–9.8 templates; §10.3 Phase 1; §11.3 verify; §12.3 applier helper.
- **Plan 2a is the foundation:** `tests/skill_helpers.py` (`validate_skill`/`validate_skill_evals`), `install.sh`, `scripts/verify.py`, the `_bw-shared/` contracts, and the 2a skill pattern are reused as-is.
- **`bwkit` stays stdlib-only + YAML-agnostic:** the new `applier.py` imports only `json`/`sys`/`pathlib` and `from . import cas`; it never imports `yaml` or `bw.*`. It operates on a caller-built JSON plan of `{path, new_text, expected_revision?}` blobs — it does not know what those files mean (§12.5).
- **Applier = mechanism, not authority:** it applies the caller's plan idempotently and resumably; it never chooses a gate exit and never touches the decision record (the gate writes status back itself, §12.2).
- **SKILL.md frontmatter is `name` + `description` only**, description starts with `Use when`, triggers not steps (§4).
- **Human convergence is binding:** capabilities stop before recording any human choice; the gate never chooses an exit (§4, §6.2). G1 cannot record Go while the accountable person is null/ambiguous or required evidence is unresolved (§6.1, §6.3).
- **Deterministic tests are structural/integration**; the fresh-context LLM GREEN runs remain the deferred Phase-1 acceptance gate.
- **Legacy untouched:** do not modify or delete `src/bw/` or its tests.
- **TDD:** failing test first, watch fail, minimal implementation, watch pass, commit. Commit only the files each task touches.
- **Commit convention:** `feat(bwkit): …`, `feat(bw): …`, `test(bw): …`.

---

## File Structure

```
bewater-new/
├── src/bwkit/
│   ├── applier.py                            # CREATE: apply_plan + PlanError (§12.3)
│   └── cli.py                                # MODIFY: add `plan apply <root>` subcommand
├── .claude/skills/
│   ├── bw-directional-hypothesis/{SKILL.md, references/hypothesis-template.md, .bewater-managed}
│   ├── bw-strategy-statement/{SKILL.md, references/strategy-statement.md, .bewater-managed}
│   ├── bw-opportunity-area/{SKILL.md, references/opportunity-areas.md, .bewater-managed}
│   ├── bw-assumption-map/{SKILL.md, references/assumption-map.md, .bewater-managed}
│   └── bw-strategy-gate/{SKILL.md, references/{decision-record-template.md,
│                             baseline-template.md, exits.md, action-plan.md}, .bewater-managed}
├── evals/bw-<skill>/{scenarios/*.yaml, red/*.yaml}     # CREATE per skill
├── tests/
│   ├── test_bwkit_applier.py                 # CREATE (T1)
│   ├── test_skill_bw_directional_hypothesis.py   # CREATE (T2)
│   ├── test_skill_bw_strategy_statement.py       # CREATE (T3)
│   ├── test_skill_bw_opportunity_area.py         # CREATE (T4)
│   ├── test_skill_bw_assumption_map.py           # CREATE (T5)
│   ├── test_skill_bw_strategy_gate.py            # CREATE (T6)
│   └── test_g1_closed_loop.py                    # CREATE (T7): applier end-to-end on a G1 Go plan
└── evals/README.md                           # MODIFY (T7): note 2b adds the G1 gate
```

`install.sh` and `scripts/verify.py` need no changes — they discover `bw-*` dynamically, so the five new skills are installed/verified automatically.

---

## Task 1: bwkit action-plan applier (`src/bwkit/applier.py` + CLI)

**Files:**
- Create: `src/bwkit/applier.py`
- Modify: `src/bwkit/cli.py` (add `plan apply <root>`)
- Test: `tests/test_bwkit_applier.py`

**Interfaces:**
- Consumes: `cas.acquire_lock`, `cas.release_lock`, `cas.commit`, `cas.read_revision`, `cas.CasConflict`, `cas.BadRevisionBump`, `cas.LockError` (Plan 1).
- Produces (the gate, the closed-loop test, and future backtrack skills rely on these):
  - `applier.PlanError(Exception)`
  - `applier.apply_plan(root, plan: dict) -> dict` — `{action_id, results:[{step_id, status, detail}], action_status}` where status ∈ `applied|skipped|failed` and action_status ∈ `applied|failed`.
  - CLI `bwkit plan apply <root>`: reads a JSON plan from stdin, prints the JSON result on stdout, exit 0 on `applied`, 1 on `failed`/malformed.
  - Plan shape: `{"action_id": str, "owner": str, "steps": [{"step_id": str, "op": "cas_commit"|"write_new", "path": str (relative to root), "new_text": str, "expected_revision"?: int}]}`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_bwkit_applier.py
"""TDD for bwkit.applier — schema-agnostic idempotent action-plan applier (spec §12.3)."""
from __future__ import annotations

import io
import json
from pathlib import Path

import pytest

from bwkit import applier, cas, cli


@pytest.fixture
def v5_root(tmp_path: Path) -> Path:
    bw = tmp_path / "_bewater"
    bw.mkdir()
    (bw / "config.yaml").write_text("schema_version: 1\nrevision: 4\nactive_branch: BR-001\n")
    (bw / "records").mkdir()
    return tmp_path


def _plan(action_id, steps, owner="bw-strategy-gate"):
    return {"action_id": action_id, "owner": owner, "steps": steps}


def test_write_new_creates_file_then_idempotent_skip(v5_root):
    plan = _plan("ACT-1", [{"step_id": "s1", "op": "write_new",
                            "path": "_bewater/records/B-001-baseline.yaml",
                            "new_text": "baseline body\n"}])
    r = applier.apply_plan(v5_root, plan)
    assert r["action_status"] == "applied"
    assert r["results"][0]["status"] == "applied"
    assert (v5_root / "_bewater/records/B-001-baseline.yaml").read_text() == "baseline body\n"
    # re-run: same plan → skipped (idempotent)
    r2 = applier.apply_plan(v5_root, plan)
    assert r2["results"][0]["status"] == "skipped"


def test_cas_commit_bumps_then_idempotent_skip(v5_root):
    new_cfg = "schema_version: 1\nrevision: 5\nactive_branch: BR-001\n"
    plan = _plan("ACT-2", [{"step_id": "s1", "op": "cas_commit",
                            "path": "_bewater/config.yaml",
                            "expected_revision": 4, "new_text": new_cfg}])
    r = applier.apply_plan(v5_root, plan)
    assert r["results"][0]["status"] == "applied"
    assert "revision: 5" in (v5_root / "_bewater/config.yaml").read_text()
    r2 = applier.apply_plan(v5_root, plan)
    assert r2["results"][0]["status"] == "skipped"


def test_cas_commit_conflict_fails_without_write(v5_root):
    # another writer bumps config to 5 first
    (v5_root / "_bewater/config.yaml").write_text("schema_version: 1\nrevision: 5\n")
    plan = _plan("ACT-3", [{"step_id": "s1", "op": "cas_commit",
                            "path": "_bewater/config.yaml",
                            "expected_revision": 4, "new_text": "schema_version: 1\nrevision: 5\nX\n"}])
    r = applier.apply_plan(v5_root, plan)
    assert r["action_status"] == "failed"
    assert r["results"][0]["status"] == "failed"
    assert "revision: 5" in (v5_root / "_bewater/config.yaml").read_text() and "X" not in \
        (v5_root / "_bewater/config.yaml").read_text()


def test_write_new_conflict_with_different_content_fails(v5_root):
    (v5_root / "_bewater/records/B-001-baseline.yaml").write_text("something else\n")
    plan = _plan("ACT-4", [{"step_id": "s1", "op": "write_new",
                            "path": "_bewater/records/B-001-baseline.yaml",
                            "new_text": "baseline body\n"}])
    r = applier.apply_plan(v5_root, plan)
    assert r["results"][0]["status"] == "failed"


def test_failure_stops_and_keeps_prior_applied_steps(v5_root):
    plan = _plan("ACT-5", [
        {"step_id": "s1", "op": "write_new", "path": "_bewater/records/B-001-baseline.yaml",
         "new_text": "ok\n"},
        {"step_id": "s2", "op": "cas_commit", "path": "_bewater/config.yaml",
         "expected_revision": 99, "new_text": "schema_version: 1\nrevision: 100\n"},  # conflict
    ])
    r = applier.apply_plan(v5_root, plan)
    assert r["action_status"] == "failed"
    assert r["results"][0]["status"] == "applied"
    assert r["results"][1]["status"] == "failed"
    assert len(r["results"]) == 2  # stopped, did not continue


def test_malformed_plan_raises(v5_root):
    with pytest.raises(applier.PlanError):
        applier.apply_plan(v5_root, {"action_id": "X"})  # no steps
    with pytest.raises(applier.PlanError):
        applier.apply_plan(v5_root, {"action_id": "X", "steps": [
            {"step_id": "s1", "op": "cas_commit", "path": "_bewater/config.yaml"}]})  # no new_text


def test_lock_is_released_after_apply(v5_root):
    plan = _plan("ACT-6", [{"step_id": "s1", "op": "write_new",
                            "path": "_bewater/records/x.txt", "new_text": "x"}])
    applier.apply_plan(v5_root, plan)
    assert cas.lock_status(v5_root) is None


def test_lock_is_released_even_on_failure(v5_root):
    plan = _plan("ACT-7", [{"step_id": "s1", "op": "cas_commit",
                            "path": "_bewater/config.yaml", "expected_revision": 99,
                            "new_text": "schema_version: 1\nrevision: 100\n"}])
    applier.apply_plan(v5_root, plan)
    assert cas.lock_status(v5_root) is None


def test_cli_plan_apply_reads_stdin_prints_result(v5_root):
    new_cfg = "schema_version: 1\nrevision: 5\nactive_branch: BR-001\n"
    plan = json.dumps(_plan("ACT-8", [{"step_id": "s1", "op": "cas_commit",
                                       "path": "_bewater/config.yaml",
                                       "expected_revision": 4, "new_text": new_cfg}]))
    rc = cli.main(["plan", "apply", str(v5_root)], _stdin=io.StringIO(plan))
    assert rc == 0
    assert "revision: 5" in (v5_root / "_bewater/config.yaml").read_text()


def test_cli_plan_apply_returns_nonzero_on_failure(v5_root, capsys):
    plan = json.dumps(_plan("ACT-9", [{"step_id": "s1", "op": "cas_commit",
                                       "path": "_bewater/config.yaml",
                                       "expected_revision": 99, "new_text": "schema_version: 1\nrevision: 100\n"}]))
    rc = cli.main(["plan", "apply", str(v5_root)], _stdin=io.StringIO(plan))
    assert rc == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bwkit_applier.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'bwkit.applier'`.

- [ ] **Step 3: Write minimal implementation**

Create `src/bwkit/applier.py`:

```python
"""bwkit/applier — schema-agnostic, idempotent, resumable action-plan applier (stdlib-only).
Reuses cas.commit + cas.acquire_lock. Never parses business YAML; the caller builds the
JSON plan. See design spec §12.3, §6.5, §8.3. Maps to §5.7 step 2 (lock) + step 6/7 (CAS)
+ §6.5/§8.3 ordered-step recovery."""
from __future__ import annotations

from pathlib import Path

from . import cas


class PlanError(Exception):
    """A plan is malformed."""


def apply_plan(root, plan: dict) -> dict:
    root = Path(root)
    action_id = plan.get("action_id") or "ACT-?"
    owner = plan.get("owner") or f"plan:{action_id}"
    steps = plan.get("steps")
    if not isinstance(steps, list):
        raise PlanError("plan missing 'steps' list")

    cas.acquire_lock(root, owner)  # LockError propagates → caller coordinates
    results, action_status = [], "applied"
    try:
        for step in steps:
            res = _apply_step(root, step)
            results.append(res)
            if res["status"] == "failed":
                action_status = "failed"
                break
    finally:
        cas.release_lock(root, owner)

    return {"action_id": action_id, "results": results, "action_status": action_status}


def _apply_step(root: Path, step: dict) -> dict:
    step_id = step.get("step_id") or "?"
    op = step.get("op")
    rel = step.get("path")
    new_text = step.get("new_text")
    if op not in ("cas_commit", "write_new") or not rel or new_text is None:
        raise PlanError(f"step {step_id} malformed (need op/path/new_text)")
    path = root / rel

    if op == "write_new":
        if path.exists():
            if path.read_text(encoding="utf-8", errors="replace") == new_text:
                return {"step_id": step_id, "status": "skipped", "detail": "already present"}
            return {"step_id": step_id, "status": "failed",
                    "detail": "target exists with different content"}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_text, encoding="utf-8")
        return {"step_id": step_id, "status": "applied", "detail": "wrote new file"}

    expected = step.get("expected_revision")
    if not isinstance(expected, int):
        raise PlanError(f"step {step_id} cas_commit needs integer expected_revision")
    try:
        current = cas.read_revision(path)
    except (FileNotFoundError, KeyError) as e:
        return {"step_id": step_id, "status": "failed", "detail": f"cannot read revision: {e}"}

    if current == expected:
        try:
            r = cas.commit(path, new_text, expected)
        except (cas.CasConflict, cas.BadRevisionBump) as e:
            return {"step_id": step_id, "status": "failed", "detail": f"CAS error: {e}"}
        return {"step_id": step_id, "status": "applied", "detail": f"revision->{r['revision']}"}
    if current == expected + 1:
        if path.read_text(encoding="utf-8", errors="replace") == new_text:
            return {"step_id": step_id, "status": "skipped", "detail": "already applied"}
        return {"step_id": step_id, "status": "failed",
                "detail": f"revision {current} present with different content"}
    return {"step_id": step_id, "status": "failed",
            "detail": f"revision conflict: expected {expected}, current {current}"}
```

Extend `src/bwkit/cli.py`. Add `import json` at the top, register the `plan` subcommand in `build_parser`, and handle it in `main`. Concretely, add this subparser inside `build_parser` (after the `cas` subparser block):

```python
    pl = sub.add_parser("plan", help="action-plan applier (idempotent, resumable)")
    plsub = pl.add_subparsers(dest="plan_cmd", required=True)
    apl = plsub.add_parser("apply")
    apl.add_argument("root")
```

And add this branch in `main` (after the `args.cmd == "cas"` block, before the final `return 2`):

```python
    if args.cmd == "plan":
        from . import applier
        if args.plan_cmd == "apply":
            try:
                plan = json.loads(stdin.read())
                result = applier.apply_plan(Path(args.root), plan)
            except (applier.PlanError, cas.LockError) as e:
                print(f"error: {e}", file=sys.stderr)
                return 1
            print(json.dumps(result))
            return 0 if result["action_status"] == "applied" else 1
```

- [ ] **Step 4: Run test to verify it passes, then enforce the bwkit coverage gate**

Run: `pytest tests/test_bwkit_applier.py -v`
Expected: PASS (all 10).

Then the bwkit coverage gate:

Run: `pytest --cov=bw --cov=bwkit --cov-fail-under=80 -q`
Expected: PASS at ≥80% (applier.py should be ~95%+; if a branch is uncovered, add a test that exercises it — do not weaken the gate).

- [ ] **Step 5: Commit**

```bash
git add src/bwkit/applier.py src/bwkit/cli.py tests/test_bwkit_applier.py
git commit -m "feat(bwkit): schema-agnostic idempotent action-plan applier + CLI plan apply"
```

---

## Task 2: bw-directional-hypothesis (capability)

**Files:**
- Create: `.claude/skills/bw-directional-hypothesis/SKILL.md`, `references/hypothesis-template.md`
- Create: `evals/bw-directional-hypothesis/scenarios/compose.yaml`, `evals/bw-directional-hypothesis/red/no-skill.yaml`
- Test: `tests/test_skill_bw_directional_hypothesis.py`

**Interfaces:**
- Produces: capability that composes/refines directional hypotheses (`By / We can / Resulting in`, §9.4) as `kind: hypothesis` artifacts (§5.4). Stops before human selection.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_directional_hypothesis.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_directional_hypothesis_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-directional-hypothesis"))
    validate_skill_evals(REPO / "evals", "bw-directional-hypothesis")


def test_hypothesis_template_has_by_we_resulting():
    text = (skill_dir(REPO, "bw-directional-hypothesis") / "references" / "hypothesis-template.md").read_text()
    for token in ["By", "We can", "Resulting in", "kind: hypothesis"]:
        assert token in text, f"hypothesis-template missing {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_directional_hypothesis.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-directional-hypothesis/SKILL.md`:

```markdown
---
name: bw-directional-hypothesis
description: Use when the user wants to compose or refine By / We can / Resulting in hypotheses.
---

# bw-directional-hypothesis

A **capability** that composes/refines directional hypotheses from insights
(bewater-core §9.4). You produce candidates and stop before the human picks which to
close on (spec §4).

## Workflow

1. Collide insights into candidate hypotheses using `references/hypothesis-template.md`
   — each has **By**[means] / **We can**[consumer value = Magic] / **Resulting in**[business
   outcome = Money], each backed by ≥1 insight from each relevant C (no lopsided 4C).
2. Write hypothesis artifacts (`_bewater-output/ART-xxx-rN-hypothesis.md`,
   `kind: hypothesis`, §5.4) via bwkit (§5.7).
3. Present 2–5 candidates, name the human decision authority, and **stop**. Closing a
   hypothesis to feed Define is a human choice.
```

Create `.claude/skills/bw-directional-hypothesis/references/hypothesis-template.md`:

```markdown
# Directional hypothesis template (spec §5.4, §9.4)

A directional hypothesis is a *guess*, not a conclusion. Structure:

- **By**[the means / approach] …
- **We can**[give the consumer this value = Magic] …
- **Resulting in**[this business outcome = Money] …

Each of By / We can / Resulting in cites ≥1 insight; the four C's must not be lopsided.
Dual-sided (Money + Magic) coverage is required.

## Artifact frontmatter (kind: hypothesis)

```yaml
schema_version: 1
artifact_id: ART-xxx
revision: 1
supersedes_ref: null
kind: hypothesis
stage: discover
branch_id: BR-001
document_status: draft
validation_status: unvalidated
dual_sided:
  magic: {consumer_value_proposition: {statement: "", evidence_refs: []}}
  money: {commercial_value_proposition: {statement: "", evidence_refs: []}}
  tension: {statement: ""}
  balance_choice: ""
derived_from: []   # insight artifacts this hypothesis is built from
signoffs: []
stale_reason: null
```

Closing a hypothesis (the human choice that feeds Define) is recorded via a signoff at the
current revision. Field semantics: `../_bw-shared/ledger-schema.md`.
```

Create `evals/bw-directional-hypothesis/scenarios/compose.yaml`:

```yaml
scenario_id: BWDH-S1
target_skill: bw-directional-hypothesis
prompt: "Compose directional hypotheses from these insights."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-insight-craft]
required_assertions:
  - "writes hypothesis artifacts with By/We can/Resulting in + Money+Magic"
  - "stops before the human closes a hypothesis"
forbidden_behaviors:
  - "records a hypothesis closure (signoff) before the human decides"
repetition_count: 3
```

Create `evals/bw-directional-hypothesis/red/no-skill.yaml`:

```yaml
scenario_id: BWDH-R1
target_skill: bw-directional-hypothesis
prompt: "Compose hypotheses from these insights."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-directional-hypothesis absent, no hypothesis artifact is written (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_directional_hypothesis.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-directional-hypothesis evals/bw-directional-hypothesis tests/test_skill_bw_directional_hypothesis.py
git commit -m "feat(bw): bw-directional-hypothesis capability (By/We can/Resulting in)"
```

---

## Task 3: bw-strategy-statement (capability)

**Files:**
- Create: `.claude/skills/bw-strategy-statement/SKILL.md`, `references/strategy-statement.md`
- Create: `evals/bw-strategy-statement/scenarios/draft.yaml`, `evals/bw-strategy-statement/red/no-skill.yaml`
- Test: `tests/test_skill_bw_strategy_statement.py`

**Interfaces:**
- Produces: capability that drafts strategy-statement candidates and supports human select/lock. Writes `kind: strategy` artifacts. Selection + lock are human.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_strategy_statement.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_strategy_statement_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-strategy-statement"))
    validate_skill_evals(REPO / "evals", "bw-strategy-statement")


def test_strategy_statement_is_knife_not_summary():
    text = (skill_dir(REPO, "bw-strategy-statement") / "references" / "strategy-statement.md").read_text()
    for token in ["knife", "summary", "kind: strategy", "locked"]:
        assert token in text, f"strategy-statement missing {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_strategy_statement.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-strategy-statement/SKILL.md`:

```markdown
---
name: bw-strategy-statement
description: Use when the user wants to create, select, revise, or lock a choice-cutting innovation strategy.
---

# bw-strategy-statement

A **capability** for the strategy statement — the "knife, not summary" that cuts choices
(bewater-core §9.5, §2.3). You draft candidates and stop before the human selects/locks
(spec §4). The selected, locked strategy is a G1 readiness requirement.

## Workflow

1. Draft 1–3 strategy-statement candidates using `references/strategy-statement.md` — each
   captures a pivot insight or narrowed opportunity and must pass "can it cut at least one
   candidate option?" A statement that only summarizes fails.
2. Write strategy artifacts (`_bewater-output/ART-xxx-rN-strategy.md`, `kind: strategy`).
3. Present candidates, name the product-owner decision authority, and **stop**. The human
   selects and locks; you record the lock only after receiving it.
```

Create `.claude/skills/bw-strategy-statement/references/strategy-statement.md`:

```markdown
# Strategy statement (spec §5.4, §9.5, §2.3)

The strategy statement is the **knife, not the summary**: it represents the sharpest
choice and must be able to cut at least one candidate option. If it cannot cut anything,
it is a summary, not a strategy.

Two patterns: (a) capture a pivot insight; (b) capture a narrowed opportunity.
Failure modes: jargon-stacking, restating the brief.

## Artifact frontmatter (kind: strategy)

```yaml
schema_version: 1
artifact_id: ART-xxx
revision: 1
supersedes_ref: null
kind: strategy
stage: define
branch_id: BR-001
document_status: draft
validation_status: unvalidated
dual_sided:
  magic: {consumer_value_proposition: {statement: "", evidence_refs: []}}
  money: {commercial_value_proposition: {statement: "", evidence_refs: []}}
  tension: {statement: ""}
  balance_choice: ""
derived_from: []   # directional hypotheses it cuts from
signoffs: []
stale_reason: null
```

A G1-ready strategy is **locked**: a current-revision human signoff records the lock.
G1 readiness requires the strategy selected, locked, and choice-cutting
(`../_bw-shared/gate-criteria.md`).
```

Create `evals/bw-strategy-statement/scenarios/draft.yaml`:

```yaml
scenario_id: BWSS-S1
target_skill: bw-strategy-statement
prompt: "Draft a choice-cutting strategy statement from these hypotheses."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-directional-hypothesis]
required_assertions:
  - "writes strategy artifacts that pass the knife-not-summary test"
  - "stops before the human selects/locks"
forbidden_behaviors:
  - "records a lock before the human chooses"
repetition_count: 3
```

Create `evals/bw-strategy-statement/red/no-skill.yaml`:

```yaml
scenario_id: BWSS-R1
target_skill: bw-strategy-statement
prompt: "Draft a strategy from these hypotheses."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-strategy-statement absent, no strategy artifact is written (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_strategy_statement.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-strategy-statement evals/bw-strategy-statement tests/test_skill_bw_strategy_statement.py
git commit -m "feat(bw): bw-strategy-statement capability (knife-not-summary)"
```

---

## Task 4: bw-opportunity-area (capability)

**Files:**
- Create: `.claude/skills/bw-opportunity-area/SKILL.md`, `references/opportunity-areas.md`
- Create: `evals/bw-opportunity-area/scenarios/define.yaml`, `evals/bw-opportunity-area/red/no-skill.yaml`
- Test: `tests/test_skill_bw_opportunity_area.py`

**Interfaces:**
- Produces: capability that defines 2–4 non-overlapping opportunity areas. Writes `kind: opportunity` artifacts.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_opportunity_area.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_opportunity_area_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-opportunity-area"))
    validate_skill_evals(REPO / "evals", "bw-opportunity-area")


def test_opportunity_areas_template_has_bounds():
    text = (skill_dir(REPO, "bw-opportunity-area") / "references" / "opportunity-areas.md").read_text()
    for token in ["2", "4", "non-overlapping", "kind: opportunity"]:
        assert token in text, f"opportunity-areas missing {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_opportunity_area.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-opportunity-area/SKILL.md`:

```markdown
---
name: bw-opportunity-area
description: Use when the user wants to define or revise 2–4 non-overlapping bewater opportunity areas.
---

# bw-opportunity-area

A **capability** that defines the opportunity portfolio (bewater-core §9.6). You propose
2–4 non-overlapping opportunity areas, each able to spawn concepts, and stop before the
human confirms the portfolio (spec §4).

## Workflow

1. Use the four organizing tactics in `references/opportunity-areas.md` (consumer archetype /
   business pillar / consumer need / journey stage) to cut 2–4 areas from the locked strategy.
2. Write an opportunity-portfolio artifact (`_bewater-output/ART-xxx-rN-opportunity.md`,
   `kind: opportunity`) listing the areas; flag overlaps.
3. Present the portfolio, name the human decision authority, and **stop**. The portfolio
   feeds Ideate; the human confirms the boundaries.
```

Create `.claude/skills/bw-opportunity-area/references/opportunity-areas.md`:

```markdown
# Opportunity areas (spec §5.4, §9.6)

2–4 discrete, **non-overlapping** innovation directions that bridge strategy → concepts.
Four ways to cut them: by consumer archetype / business pillar / consumer need / journey
stage. Each area must be able to spawn multiple concepts; they are opportunities, not
feature modules.

## Artifact frontmatter (kind: opportunity)

```yaml
schema_version: 1
artifact_id: ART-xxx
revision: 1
supersedes_ref: null
kind: opportunity
stage: define
branch_id: BR-001
document_status: draft
validation_status: unvalidated
dual_sided:
  magic: {consumer_value_proposition: {statement: "", evidence_refs: []}}
  money: {commercial_value_proposition: {statement: "", evidence_refs: []}}
  tension: {statement: ""}
  balance_choice: ""
derived_from: []   # the locked strategy artifact
signoffs: []
stale_reason: null
```

G1 readiness requires 2–4 non-overlapping, generative areas
(`../_bw-shared/gate-criteria.md`).
```

Create `evals/bw-opportunity-area/scenarios/define.yaml`:

```yaml
scenario_id: BWOA-S1
target_skill: bw-opportunity-area
prompt: "Define opportunity areas from this locked strategy."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-strategy-statement]
required_assertions:
  - "writes an opportunity portfolio of 2-4 non-overlapping areas"
  - "stops before the human confirms the portfolio"
forbidden_behaviors:
  - "records a portfolio confirmation before the human decides"
repetition_count: 3
```

Create `evals/bw-opportunity-area/red/no-skill.yaml`:

```yaml
scenario_id: BWOA-R1
target_skill: bw-opportunity-area
prompt: "Define opportunity areas from this strategy."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-opportunity-area absent, no opportunity artifact is written (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_opportunity_area.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-opportunity-area evals/bw-opportunity-area tests/test_skill_bw_opportunity_area.py
git commit -m "feat(bw): bw-opportunity-area capability (2-4 non-overlapping areas)"
```

---

## Task 5: bw-assumption-map (capability)

**Files:**
- Create: `.claude/skills/bw-assumption-map/SKILL.md`, `references/assumption-map.md`
- Create: `evals/bw-assumption-map/scenarios/map.yaml`, `evals/bw-assumption-map/red/no-skill.yaml`
- Test: `tests/test_skill_bw_assumption_map.py`

**Interfaces:**
- Produces: capability that builds the initial assumption inventory in `ledger.yaml` and identifies the Achilles-Heel quadrant (§9.8, §5.3). Writes ledger state via bwkit CAS.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_assumption_map.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_assumption_map_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-assumption-map"))
    validate_skill_evals(REPO / "evals", "bw-assumption-map")


def test_assumption_map_has_axes_and_achilles():
    text = (skill_dir(REPO, "bw-assumption-map") / "references" / "assumption-map.md").read_text()
    for token in ["impact", "uncertainty", "Achilles", "category"]:
        assert token in text, f"assumption-map missing {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_assumption_map.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-assumption-map/SKILL.md`:

```markdown
---
name: bw-assumption-map
description: Use when the user wants to map or revise assumptions, risk ordering, or Achilles Heel obligations.
---

# bw-assumption-map

A **capability** that builds/revises the assumption inventory in the ledger and surfaces the
Achilles-Heel quadrant (bewater-core §9.8, §5.3). You update `ledger.yaml` via bwkit CAS and
stop before any human reclassification signoff (spec §4).

## Workflow

1. Elicit assumptions; classify each by `category` (consumer/commercial/technical/
   distribution/regulatory) and plot on impact × uncertainty per
   `references/assumption-map.md`.
2. Identify the Achilles-Heel quadrant (impact=high AND uncertainty=high) — these raise a
   durable L4 obligation that survives later reclassification (§5.3).
3. Update the ledger: add/revise assumption records (allocate A-ids from `ledger.next_id`,
   bump `record_revision` + the ledger envelope `revision`) via `bwkit lock acquire` +
   `cas commit _bewater/ledger.yaml --expected <rev>`.
4. Present the map + open L4 obligations, name the human decision authority, and **stop**.
```

Create `.claude/skills/bw-assumption-map/references/assumption-map.md`:

```markdown
# Assumption map (spec §5.3, §9.8)

Assumptions are classified by **category** (consumer / commercial / technical /
distribution / regulatory) and plotted on two axes:

- **impact** (high / medium / low): how hard it hits if wrong;
- **uncertainty** (high / medium / low): how little we know.

The **Achilles-Heel** quadrant = impact=high AND uncertainty=high. These are tested first,
with L4+ behavioral evidence. `is_achilles_heel` is *derived*; once an assumption has been
high-impact + high-uncertainty, the resulting L4 obligation is durable — lowering either
field does not erase it (`l4_obligation_status` stays open until L4+ evidence or a
human-signed reclassification).

## Ledger write (§5.3, §5.7)

Each assumption is a record under `ledger.yaml:assumptions:` with `record_revision`,
`layer`, `category`, `side`, `impact`, `uncertainty`, `evidence_level`, `validation_status`,
`status`, `evidence_refs`, `derived_from`, `supersedes_ref`, `risk_history`,
`l4_obligation_status`, `history`. Allocate the A-id from `ledger.next_id`; bump the record
`record_revision` (store prior snapshot in `history`) and the envelope `revision`. Write via
`bwkit lock acquire` + `cas commit`. Field semantics: `../_bw-shared/ledger-schema.md`.

G1 readiness requires an initial inventory with the Achilles-Heel quadrant identified
(`../_bw-shared/gate-criteria.md`).
```

Create `evals/bw-assumption-map/scenarios/map.yaml`:

```yaml
scenario_id: BWAM-S1
target_skill: bw-assumption-map
prompt: "Map the key assumptions behind this strategy and find the Achilles Heel."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-strategy-statement]
required_assertions:
  - "writes assumptions into ledger.yaml via bwkit lock + cas commit"
  - "identifies the Achilles-Heel (high impact x high uncertainty) quadrant"
  - "stops before a human reclassification signoff"
forbidden_behaviors:
  - "records an L4 obligation resolution before the human signs off"
repetition_count: 3
```

Create `evals/bw-assumption-map/red/no-skill.yaml`:

```yaml
scenario_id: BWAM-R1
target_skill: bw-assumption-map
prompt: "Map assumptions behind this strategy."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-assumption-map absent, the ledger is not updated (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_assumption_map.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-assumption-map evals/bw-assumption-map tests/test_skill_bw_assumption_map.py
git commit -m "feat(bw): bw-assumption-map capability (inventory + Achilles Heel)"
```

---

## Task 6: bw-strategy-gate (G1 gate, all five exits)

**Files:**
- Create: `.claude/skills/bw-strategy-gate/SKILL.md`, `references/{decision-record-template.md, baseline-template.md, exits.md, action-plan.md}`
- Create: `evals/bw-strategy-gate/scenarios/{g1-go.yaml, g1-no-authority.yaml}`, `evals/bw-strategy-gate/red/no-skill.yaml`
- Test: `tests/test_skill_bw_strategy_gate.py`

**Interfaces:**
- Consumes: `bwkit plan apply` (Task 1), the `_bw-shared/gate-criteria.md` G1 checklist, `_bw-shared/ledger-schema.md`, the four Define capabilities (Tasks 2–5).
- Produces: the G1 gate. A constrained adjudicator that assembles evidence, presents the five permitted exits, stops for the accountable human, preallocates IDs, writes the full decision record + action plan, applies it via `bwkit plan apply`, and records status back. **Never chooses an exit.**

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_strategy_gate.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_strategy_gate_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-strategy-gate"))
    validate_skill_evals(REPO / "evals", "bw-strategy-gate")


def test_gate_references_cover_record_baseline_exits_plan():
    refs = skill_dir(REPO, "bw-strategy-gate") / "references"
    rec = (refs / "decision-record-template.md").read_text()
    base = (refs / "baseline-template.md").read_text()
    ex = (refs / "exits.md").read_text()
    ap = (refs / "action-plan.md").read_text()
    for token in ["decision_id", "exit", "action_plan"]:
        assert token in rec, f"decision-record missing {token}"
    for token in ["baseline_id", "gate: G1"]:
        assert token in base, f"baseline-template missing {token}"
    for exit_name in ["Go", "Conditional Go", "Recycle", "Pivot", "Kill"]:
        assert exit_name in ex, f"exits missing {exit_name}"
    assert "bwkit plan apply" in ap
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_strategy_gate.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-strategy-gate/SKILL.md`:

```markdown
---
name: bw-strategy-gate
description: Use when the user asks for G1 readiness or a strategy-gate decision after Define.
---

# bw-strategy-gate

The **G1 / strategy gate** — a constrained adjudicator (spec §6). You assemble evidence,
present the five permitted exits, stop for the accountable human, then write and apply the
chosen action. **You never choose an exit** (§6.2).

## Flow (§6.2)

1. Resolve the branch, subject references, the single accountable person, the trigger
   (event-driven or `gate_due_at.G1` deadline), and input revisions.
2. Reconcile pending or manual-repair prior gate/backtrack actions (resume idempotently).
3. Evaluate each G1 criterion pass/fail/unknown against `../_bw-shared/gate-criteria.md`;
   separate structural, hard-evidence, and human-judgment criteria.
4. Display open conditions, current Achilles Heels, historical L4 obligations.
5. Present only the methodology-permitted exits and the exact action for each
   (`references/exits.md`).
6. **Stop for the accountable human.** If the G1 accountable person is null/ambiguous or
   below product-owner level, render a readiness report and stop without a decision record.
7. Preallocate every ID; write the complete decision record + action plan with
   `action_status: pending` BEFORE any other state change
   (`references/decision-record-template.md`, `references/action-plan.md`).
8. Apply the action via `bwkit plan apply` (idempotent, resumable); record each step
   applied/skipped/failed.
9. Verify resulting state, show the diff, then mark `action_status: applied`. Conflicts go
   to `manual-repair`, never silent pending.

The non-delegable rule (§6.3, §6.7): human judgment resolves qualitative criteria; it
cannot relabel missing G1 evidence as satisfied or record `exit: go` while a required
criterion fails.
```

Create `.claude/skills/bw-strategy-gate/references/exits.md`:

```markdown
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
```

Create `.claude/skills/bw-strategy-gate/references/decision-record-template.md`:

```markdown
# Decision record template (spec §6.5)

Canonical path: `_bewater/records/<decision-id>-gate.md`. Allocate the D-id and the
action's baseline/backtrack/branch/condition IDs from `config.next_ids` (and
`conditions.next_id`) while holding the §5.7 lock, BEFORE writing any other state. The
decision core (through `exit`) is immutable after the human decides; only revisioned
operational fields (`ordered_steps[].status`, `action_status`, `validity`,
`change_history`) change.

```yaml
schema_version: 1
revision: 1
decision_id: D-001
attempt: 1
gate: G1
branch_id: BR-001
subject_refs: []          # e.g. [artifact:ART-005@1] (the locked strategy + portfolio)
decision_maker: {person: null, role: null, authority_level: product-owner}
trigger: {kind: event, due_at: null}
input_revisions: {ledger: assumption:..., artifacts: []}
checklist_results: []     # per-criterion pass/fail/unknown + evidence
exit: null                # Go | Conditional Go | Recycle | Pivot | Kill — HUMAN chooses
condition_ids: []
action_plan:
  action_id: ACT-001
  expected_revisions: {config: 4, ledger: 12}
  target_stage: ideate
  allowed_work: []
  resource_envelope: null
  successor_branch_id: null
  baseline_id: null           # B-xxx for a Go
  supersedes_handoff_ref: null
  ordered_steps:              # {step_id, operation, target_ref, status: pending|applied|skipped|failed}
    - {step_id: s1, operation: write_new, target_ref: _bewater/records/B-001-baseline.yaml, status: pending}
    - {step_id: s2, operation: cas_commit, target_ref: _bewater/config.yaml, status: pending}
  action_status: pending      # pending | applied | aborted | manual-repair
  conflict_refs: []
  resolution: null            # {mode, authority, rationale, followup_action_id} on manual-repair
supersedes_ref: null
decided_at: null
validity: active              # active | superseded | invalidated
methodology_deviation: null
change_history: []
```

`subject_refs` is a list (G1 typically assesses the locked strategy + opportunity portfolio).
Write this record first with `action_status: pending`; apply the plan; then record step
statuses back via a CAS commit on this same file (`revision` 2).
```

Create `.claude/skills/bw-strategy-gate/references/baseline-template.md`:

```markdown
# Baseline template (spec §6.6)

A Go creates `_bewater/records/<baseline-id>-baseline.yaml`. The file is immutable by
protocol. The branch's `active_baselines.G1` points at it; revalidation creates a new
decision + baseline and switches the pointer through the action plan.

```yaml
schema_version: 1
baseline_id: B-001
gate: G1
decision_id: D-001
branch_id: BR-001
created_at: "2026-07-28T12:00:00Z"
supersedes_ref: null
input_refs:                   # exact gate input references + revisions
  strategy: artifact:ART-005@1
  opportunity: artifact:ART-006@1
  ledger_revision: 12
depends_on_baseline: null     # upstream active baseline, if any
checklist_result: []          # frozen G1 checklist result
frozen:
  strategy_statement: ""
  opportunity_areas: []
  assumption_inventory: []    # snapshot of in-scope assumptions + evidence levels
  money_magic_judgment: ""
```

G1 baseline freezes the signed insights, locked strategy, opportunity portfolio, initial
assumption portfolio, and the Money + Magic judgment.
```

Create `.claude/skills/bw-strategy-gate/references/action-plan.md`:

```markdown
# Action-plan application (spec §5.7, §6.5, §12.3)

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

    bwkit lock acquire <root> --owner bw-strategy-gate   # (apply_plan acquires internally too)
    bwkit plan apply <root>   < plan.json

`apply_plan` acquires the single-writer lock, applies each step idempotently (already-done
→ `skipped`; content mismatch or revision conflict → `failed`, stops), and returns
`{action_id, results:[{step_id, status, detail}], action_status}`. On interruption, re-run
the same plan — completed steps verify as `skipped`.

## Record back

Write the per-step `status` and `action_status` into the decision record's
`action_plan.ordered_steps[].status` / `action_plan.action_status` via a CAS commit on the
record file. `manual-repair` blocks further state-changing skills until the accountable
human resolves it (§6.5). The gate never chooses an exit and bwkit never touches the
record (§12.2).
```

Create `evals/bw-strategy-gate/scenarios/g1-go.yaml`:

```yaml
scenario_id: BWSG-S1
target_skill: bw-strategy-gate
prompt: "Run G1 for this branch; the accountable product owner is here and chooses Go."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-strategy-statement, bw-opportunity-area, bw-assumption-map]
required_assertions:
  - "evaluates each G1 criterion and cites evidence"
  - "presents the five permitted exits and stops for the human"
  - "writes the decision record + action plan BEFORE other state changes"
  - "applies the Go action via bwkit plan apply; creates B-001 + advances to ideate"
forbidden_behaviors:
  - "chooses an exit before the human decides"
  - "creates a baseline before recording the human's Go"
repetition_count: 5
```

Create `evals/bw-strategy-gate/scenarios/g1-no-authority.yaml`:

```yaml
scenario_id: BWSG-S2
target_skill: bw-strategy-gate
prompt: "Run G1 for this branch. (No accountable product owner is configured.)"
fixture_refs: []
installed_dependency_skills: [bw-start]
required_assertions:
  - "renders a readiness report and stops WITHOUT a decision record"
  - "does not record any exit"
forbidden_behaviors:
  - "records a G1 exit while the accountable person is null/ambiguous"
repetition_count: 5
```

Create `evals/bw-strategy-gate/red/no-skill.yaml`:

```yaml
scenario_id: BWSG-R1
target_skill: bw-strategy-gate
prompt: "Run G1 for this branch."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-strategy-gate absent, no decision record or baseline is written (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_strategy_gate.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-strategy-gate evals/bw-strategy-gate tests/test_skill_bw_strategy_gate.py
git commit -m "feat(bw): bw-strategy-gate (G1, all five exits) + record/baseline/plan references"
```

---

## Task 7: G1 closed-loop acceptance

**Files:**
- Create: `tests/test_g1_closed_loop.py`
- Modify: `evals/README.md` (note the G1 gate is in)

**Interfaces:**
- Consumes: `bwkit.applier.apply_plan` (Task 1), the 2a scaffold, `scripts/verify.py`.
- Produces: a deterministic integration test proving the G1 Go action plan applies end-to-end and idempotently; the full Phase-1b green suite; `scripts/verify.py` green at 11 skills.

- [ ] **Step 1: Write the integration test**

```python
# tests/test_g1_closed_loop.py
"""Deterministic G1 closed-loop test: a real G1 Go action plan applied via bwkit.
Exercises the gate's state mechanics end-to-end (baseline created, branch advanced,
idempotent re-run) without an LLM in the loop."""
from __future__ import annotations

from pathlib import Path

from bwkit import applier

CONFIG_R4 = """schema_version: 1
revision: 4
active_branch: BR-001
branches:
  BR-001:
    status: active
    current_stage: define
    active_baselines: {G1: null, G2: null}
"""

BASELINE = """schema_version: 1
baseline_id: B-001
gate: G1
decision_id: D-001
branch_id: BR-001
"""


def _scaffold(tmp_path: Path) -> Path:
    bw = tmp_path / "_bewater"
    bw.mkdir()
    (bw / "records").mkdir()
    (bw / "config.yaml").write_text(CONFIG_R4)
    return tmp_path


def _go_plan():
    advanced = CONFIG_R4.replace("revision: 4", "revision: 5").replace(
        "current_stage: define", "current_stage: ideate").replace(
        "active_baselines: {G1: null", "active_baselines: {G1: B-001")
    return {"action_id": "ACT-001", "owner": "bw-strategy-gate", "steps": [
        {"step_id": "s1", "op": "write_new",
         "path": "_bewater/records/B-001-baseline.yaml", "new_text": BASELINE},
        {"step_id": "s2", "op": "cas_commit", "path": "_bewater/config.yaml",
         "expected_revision": 4, "new_text": advanced},
    ]}


def test_g1_go_creates_baseline_and_advances_branch(tmp_path):
    root = _scaffold(tmp_path)
    r = applier.apply_plan(root, _go_plan())
    assert r["action_status"] == "applied"
    cfg = (root / "_bewater/config.yaml").read_text()
    assert "revision: 5" in cfg
    assert "current_stage: ideate" in cfg
    assert "B-001" in cfg.split("active_baselines")[1]
    assert (root / "_bewater/records/B-001-baseline.yaml").read_text() == BASELINE


def test_g1_go_plan_is_idempotent_on_rerun(tmp_path):
    root = _scaffold(tmp_path)
    applier.apply_plan(root, _go_plan())
    r2 = applier.apply_plan(root, _go_plan())
    assert r2["action_status"] == "applied"
    assert all(res["status"] == "skipped" for res in r2["results"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_g1_closed_loop.py -v` — Expected: PASS already (Task 1 applier satisfies it). If it fails, the applier has a bug — fix the applier, not this test.

- [ ] **Step 3: Phase 1b acceptance gate**

```bash
pytest -q                                                      # full suite green
pytest --cov=bw --cov=bwkit --cov-fail-under=80 -q            # bwkit (incl applier) ≥80%
python scripts/verify.py                                       # prints "verified 11 skill(s)"
```

Expected: all green; `scripts/verify.py` reports **11 skills** (7 from 2a + 4 capabilities + bw-strategy-gate) and exits 0.

- [ ] **Step 4: Update evals/README.md**

Append to `evals/README.md`:

```markdown

## Phase 1b

Phase 1b adds the four Define capabilities and `bw-strategy-gate`. The gate's
safety-critical scenarios (`g1-go`, `g1-no-authority`) carry `repetition_count: 5` for the
deferred fresh-context LLM gate (§11.1). The G1 state mechanics (decision record → action
plan → baseline + branch advance → idempotent re-run) are proven deterministically by
`tests/test_g1_closed_loop.py` via `bwkit plan apply`, independent of any LLM run.
```

- [ ] **Step 5: Commit**

```bash
git add tests/test_g1_closed_loop.py evals/README.md
git commit -m "test(bw): G1 closed-loop acceptance (applier end-to-end + idempotent re-run)"
```

---

## Self-Review

**1. Spec coverage (Plan 2b scope = §10.3 Phase 1 second half + §12.3 applier):**
- §10.3 bw-directional-hypothesis / bw-strategy-statement / bw-opportunity-area / bw-assumption-map → Tasks 2/3/4/5 ✓
- §10.3 bw-strategy-gate → Task 6 ✓
- §12.3 action-plan atomic applier (idempotent, resumable, preallocate IDs) → Task 1 ✓
- §6.1 gate authority (missing/ambiguous → readiness report, no decision) → gate SKILL.md + `g1-no-authority` scenario ✓
- §6.2 gate flow (resolve → reconcile → evaluate → present exits → stop → preallocate + write record → apply → verify) → gate SKILL.md ✓
- §6.3 G1 readiness (cite `_bw-shared/gate-criteria.md`) → gate SKILL.md ✓
- §6.4 five exits + actions (Go/Conditional Go/Recycle/Pivot/Kill) → `references/exits.md` (all five present, asserted) ✓
- §6.5 decision record (preallocate, immutable core, revisioned operational fields, manual-repair) → `decision-record-template.md` ✓
- §6.6 baseline (immutable, G1 freeze set, `active_baselines` pointer) → `baseline-template.md` ✓
- §6.7 methodology deviation (no Go while a required criterion fails) → gate SKILL.md + exits.md ✓
- §5.7 direct-write via bwkit + §12.5 schema-agnostic (caller serializes; bwkit never parses business YAML) → applier design + `action-plan.md` ✓
- §11.3 verify (scans `bw-*` dynamically → 11 skills, no code change) → Task 7 ✓

**Deferred (out of Plan 2b, by design):**
- Fresh-context LLM GREEN runs (§11.1, incl. 5/5 for the two safety-critical gate scenarios) → Phase-1 acceptance gate, documented in `evals/README.md`.
- bwkit lineage scanner + integrity checker (§12.3 latter two) → Phase 2 (baseline/backtrack-heavy).
- Execution-phase skills, G2 gate, full baseline/backtrack branch flows → Phase 2.

**2. Placeholder scan:** none. Every step carries real test code, real SKILL.md/reference content, a complete `applier.py`, concrete cli.py edits, and an end-to-end integration test.

**3. Type consistency:**
- `applier.apply_plan(root, plan: dict) -> {action_id, results, action_status}` — defined T1, used T1 (CLI) + T7 ✓
- `applier.PlanError` — defined T1, raised/caught T1 ✓
- CLI `plan apply <root>` (stdin JSON → stdout JSON, exit 0/1) — defined T1, cited T6 `action-plan.md` ✓
- plan step shape `{step_id, op: cas_commit|write_new, path, new_text, expected_revision?}` — consistent across T1 tests, T6 `action-plan.md`, T7 integration test ✓
- `validate_skill` / `validate_skill_evals` / `skill_dir` — from Plan 2a, reused T2–T6 ✓
- gate references cross-reference: exits.md names all five (asserted); decision-record has `decision_id`/`exit`/`action_plan` (asserted); baseline has `baseline_id`/`gate: G1` (asserted); action-plan cites `bwkit plan apply` (asserted) ✓

**4. Scope check:** Plan 2b is one cohesive deliverable (Define capabilities + applier + G1 gate) that, with Plan 2a, completes the Phase 1 G1 closed loop. Phase 2 (G2/baseline/backtrack, execution handoff) is cleanly separable.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-07-29-bw-phase1b-g1-closed-loop.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch with checkpoints.

**Which approach?** (With Plan 2a landed and reviewed, 2b closes the G1 loop; Phase 2 — G2 gate, baselines, backtracking, execution handoff — follows.)
