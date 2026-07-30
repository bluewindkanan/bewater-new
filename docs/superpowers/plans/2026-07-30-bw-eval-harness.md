# BeWater Eval Harness (§11.1 Fresh-Context Gate) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the fresh-context LLM eval harness that the spec defers as the Phase-2 acceptance gate (§11.1), so BeWater's behavioral scenarios (routing / human-convergence / gate-evidence judgment / the G2 hard rule) can be run, judged, and recorded — completing Phase-2 acceptance and unblocking Phase 3 (§10.5). The harness spawns an isolated `claude` session per repetition (temp HOME + repo-external product cwd; target skill absent for RED, copied in for GREEN), captures the transcript + filesystem diff, judges assertions mechanically (structured checks + the legacy `src/bw` oracle), flags semantic assertions for a human reviewer, and writes per-run result records that `scripts/verify.py` (§11.3) then gates on.

**Architecture:** A new `evals/_harness/` runtime (stdlib + PyYAML, authoring-time only — not shipped, not bwkit) layered on the existing `loader.py` + `manifest_schema.json`: `result.py` (run-result schema + store), `isolation.py` (temp product cwd + temp HOME + controlled skill set), `runner.py` (spawn headless `command claude -p --output-format json` in the isolated env), `judge.py` (mechanical check engine + oracle + semantic flagging), and an orchestrator CLI (`python -m evals._harness ...`). The judge avoids LLM-judging-LLM circularity (§11.1): structured `checks` in manifests drive deterministic verdicts; the legacy `src/bw` oracle (`validate`, `gate_scan`) judges mechanical state behaviors; NL assertions without a structured check are marked `needs-review` with a reviewer slot. `scripts/verify.py` gains §11.3 result-gate checks (every scenario has complete results; every RED fails a target behavior; every GREEN passes required checks + triggers no forbidden behavior; manual judgments carry reviewer identity).

**Tech Stack:** Python ≥3.11 (stdlib + PyYAML in tests/harness only). Headless `claude` CLI (v2.1.156, available) via `--print`/`--output-format json`. pytest + pytest-cov (80% floor on the harness Python, per §11.3). No new shipped runtime dependencies; the harness is authoring-only.

## Global Constraints

- **Spec authority:** `docs/superpowers/specs/2026-07-27-bewater-decision-phase-skills-design.md` v5.1 + H1a. §11.1 behavioral TDD (fresh-context, isolated HOME, repo-external cwd, RED then GREEN, 3 reps / 5 for safety-critical, result fields, cost-control tiers); §11.2 required scenario matrix; §11.3 automated verification (incl. result-gate checks).
- **Authoring-only, not shipped:** the harness lives under `evals/_harness/` + `scripts/`; it is NOT part of `bwkit` and is NOT installed by `install.sh`. It never chooses a gate exit and never mutates real project state (it operates only inside disposable temp dirs).
- **No LLM-judging-LLM (§11.1 cost control):** deterministic behaviors (ID allocation, revision CAS, versioned refs, integrity/lineage) are already covered by `tests/` + `bwkit` — the harness does NOT re-run them. Only behavioral scenarios use fresh-context eval. Assertions are judged by structured `checks` + the `src/bw` oracle; semantic assertions are flagged `needs-review` (human), never auto-passed by an LLM.
- **True isolation per §11.1 step 2/4:** each rep runs in a fresh process with an isolated temporary HOME (so no user/global skills leak) and a repository-external temporary product cwd; dependency skills (`installed_dependency_skills`) are installed into the temp product's `.claude/skills/` and held fixed; the target skill is the experimental variable (absent for RED, copied in for GREEN). cwd, model, prompt, dependency skills, global skills, and fixtures are fixed across RED/GREEN.
- **RED must fail ≥1 target behavior; GREEN must pass every required check and trigger no forbidden behavior.** Safety-critical gate scenarios (those with `repetition_count: 5`) must pass 5/5.
- **TDD:** deterministic modules (result/isolation/judge/orchestrator-glue) get failing tests first; the `claude` subprocess runner is unit-tested with a mocked subprocess (command/env/output parsing) and validated end-to-end only in the pilot task. The actual fresh-context runs ARE the eval — they are not unit-tested.
- **Legacy untouched except as a read-only judge:** `src/bw` (`validate`, `gate_scan`) is imported read-only by the judge; it is not modified or deleted here (deletion is Phase 3, §10.5).
- **Commit convention:** `feat(eval): …`, `test(eval): …`, `docs(eval): …`.

---

## File Structure

```
bewater-new/
├── evals/_harness/
│   ├── loader.py                         # existing (manifest load/validate)
│   ├── manifest_schema.json              # MODIFY (T1): add optional `checks` + result-gate fields
│   ├── result.py                         # CREATE (T1): run-result schema + read/write
│   ├── isolation.py                      # CREATE (T2): temp product cwd + temp HOME + skill-set control
│   ├── runner.py                         # CREATE (T3): spawn headless claude, capture transcript
│   ├── judge.py                          # CREATE (T4): check engine + src/bw oracle + needs-review
│   ├── orchestrator.py                   # CREATE (T5): per-scenario RED/GREEN loop, rep tiering, aggregate
│   └── __main__.py                       # CREATE (T5): `python -m evals._harness run ...`
├── scripts/verify.py                     # MODIFY (T6): §11.3 result-gate checks
└── tests/
    ├── test_eval_result.py               # CREATE (T1)
    ├── test_eval_isolation.py            # CREATE (T2)
    ├── test_eval_runner.py               # CREATE (T3, mocked subprocess)
    ├── test_eval_judge.py                # CREATE (T4)
    ├── test_eval_orchestrator.py         # CREATE (T5)
    └── test_verify_eval_gate.py          # CREATE (T6)
```

No skill changes, no bwkit changes, no installer changes. The pilot (T7) is verify/run-only and may add `checks:` to a small number of existing manifests + store real GREEN/RED results.

---

## Task 1: Run-result schema + manifest `checks` field (`result.py`, schema)

**Files:**
- Create: `evals/_harness/result.py`, `tests/test_eval_result.py`
- Modify: `evals/_harness/manifest_schema.json` (add optional `checks`)

**Interfaces:**
- Produces: the run-result record (§11.1 result fields) + a structured `checks` vocabulary on manifests.
  - `result.RESULT_FIELDS` and `result.write_result(eval_root, skill, mode, scenario_id, rep, payload) -> Path` writing `evals/{skill}/{green|red}/{scenario_id}-r{rep}.json`; `result.read_results(eval_root, skill, mode, scenario_id) -> list[dict]`.
  - Result payload fields (§11.1): `scenario_id, target_skill, mode (red|green), repetition, fresh_context_id, cwd, temp_home, project_local_skills, global_skills, model, transcript_path, checks: [{id, type, verdict (pass|fail|needs-review), detail}], forbidden_triggered: [], verdict (green|red|needs-review), reviewer (null until a human signs a needs-review)`.
  - Manifest gains optional `checks: [{id, type, params}]` (structured, machine-checkable) alongside the NL `required_assertions`/`forbidden_behaviors`. Check `type` vocabulary (initial): `transcript_contains`, `transcript_regex_present`, `transcript_regex_absent`, `fs_no_new_files`, `fs_wrote_file_matching`, `oracle_validate_ok`. (loader's required-key set is unchanged; `checks` is optional.)

- [ ] **Step 1: Write the failing test**

```python
# tests/test_eval_result.py
"""TDD for eval result records (spec §11.1) + manifest checks field."""
from __future__ import annotations
import json
from pathlib import Path
import yaml
from evals._harness import result, loader


def test_write_and_read_result_roundtrip(tmp_path: Path):
    payload = {
        "scenario_id": "BWSG-S1", "target_skill": "bw-strategy-gate", "mode": "green",
        "repetition": 1, "fresh_context_id": "ctx-1", "cwd": "/tmp/x", "temp_home": "/tmp/h",
        "project_local_skills": ["bw-strategy-gate"], "global_skills": [],
        "model": "claude-x", "transcript_path": "/tmp/t.jsonl",
        "checks": [{"id": "presents_exits", "type": "transcript_regex_present",
                    "verdict": "pass", "detail": "matched Go|Kill"}],
        "forbidden_triggered": [], "verdict": "green", "reviewer": None,
    }
    p = result.write_result(tmp_path, "bw-strategy-gate", "green", "BWSG-S1", 1, payload)
    assert p.name == "BWSG-S1-r1.json"
    rs = result.read_results(tmp_path, "bw-strategy-gate", "green", "BWSG-S1")
    assert len(rs) == 1 and rs[0]["verdict"] == "green"


def test_manifest_accepts_optional_checks(tmp_path: Path):
    m = tmp_path / "s.yaml"
    m.write_text(yaml.safe_dump({
        "scenario_id": "X-S1", "target_skill": "bw-start", "prompt": "p",
        "required_assertions": ["a"], "forbidden_behaviors": [], "repetition_count": 3,
        "checks": [{"id": "c1", "type": "transcript_contains", "params": {"needle": "bw-"}}],
    }))
    data = loader.load_manifest(m)            # must not raise
    assert data["checks"][0]["type"] == "transcript_contains"


def test_verdict_is_needs_review_when_any_check_needs_review(tmp_path: Path):
    payload = {"scenario_id": "X", "target_skill": "bw-start", "mode": "green", "repetition": 1,
               "fresh_context_id": "c", "cwd": "", "temp_home": "", "project_local_skills": [],
               "global_skills": [], "model": "", "transcript_path": "",
               "checks": [{"id": "sem", "type": "transcript_contains", "verdict": "needs-review",
                           "detail": ""}], "forbidden_triggered": [], "verdict": "needs-review",
               "reviewer": None}
    p = result.write_result(tmp_path, "bw-start", "green", "X", 1, payload)
    assert json.loads(p.read_text())["verdict"] == "needs-review"
```

Extend `evals/_harness/manifest_schema.json`: add `"checks"` to `properties` (optional array of `{id, type, params}`) — do NOT add it to `required`.

- [ ] **Step 2: Run test to verify it fails** — `pytest tests/test_eval_result.py -v` → FAIL (no `result.py`).

- [ ] **Step 3: Write minimal implementation** — `evals/_harness/result.py` (write/read JSON under `evals/{skill}/{green|red}/{scenario_id}-r{rep}.json`; `verdict` derived = `needs-review` if any check is `needs-review` else `green` if all `pass` else `red`). Keep `loader.py` unchanged (it already ignores unknown optional keys).

- [ ] **Step 4: Run test to verify it passes** — `pytest tests/test_eval_result.py -v` → PASS.

- [ ] **Step 5: Commit**

```bash
git add evals/_harness/result.py evals/_harness/manifest_schema.json tests/test_eval_result.py
git commit -m "feat(eval): run-result schema + manifest checks field (§11.1)"
```

---

## Task 2: Isolation primitives (`isolation.py`)

**Files:**
- Create: `evals/_harness/isolation.py`, `tests/test_eval_isolation.py`

**Interfaces:**
- Produces: `isolation.Sandbox` (a context manager) that creates a repo-external temp product cwd + temp HOME, installs the fixed dependency-skill set into `<product>/.claude/skills/`, and for GREEN copies in the target skill (RED leaves it absent). Methods/attrs: `product_cwd`, `temp_home`, `env` (a dict with `HOME`, `ANTHROPIC_API_KEY` passed through, cwd-appropriate vars), `installed_skills`. Cleans up on exit.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_eval_isolation.py
"""TDD for eval isolation: repo-external cwd + temp HOME + controlled skill set (§11.1 step 2/4)."""
from __future__ import annotations
from pathlib import Path
from evals._harness import isolation

REPO = Path(__file__).resolve().parents[1]


def test_green_sandbox_copies_target_skill_and_deps(tmp_path):
    with isolation.Sandbox(repo=REPO, product_root=tmp_path / "prod",
                           home_root=tmp_path / "home", target_skill="bw-start",
                           dependency_skills=["bw-immersion"], mode="green") as sb:
        skills_dir = sb.product_cwd / ".claude" / "skills"
        assert (skills_dir / "bw-start" / "SKILL.md").exists()       # target present (GREEN)
        assert (skills_dir / "bw-immersion" / "SKILL.md").exists()   # dependency present
        assert sb.temp_home.exists()
        assert sb.env["HOME"] == str(sb.temp_home)
    # cleaned up
    assert not (tmp_path / "prod").exists()


def test_red_sandbox_omits_target_keeps_deps(tmp_path):
    with isolation.Sandbox(repo=REPO, product_root=tmp_path / "prod",
                           home_root=tmp_path / "home", target_skill="bw-start",
                           dependency_skills=["bw-immersion"], mode="red") as sb:
        skills_dir = sb.product_cwd / ".claude" / "skills"
        assert not (skills_dir / "bw-start").exists()                # target absent (RED)
        assert (skills_dir / "bw-immersion" / "SKILL.md").exists()   # dependency still present


def test_product_cwd_is_outside_repo(tmp_path):
    with isolation.Sandbox(repo=REPO, product_root=tmp_path / "prod",
                           home_root=tmp_path / "home", target_skill="bw-start",
                           dependency_skills=[], mode="green") as sb:
        assert REPO not in sb.product_cwd.parents
```

- [ ] **Step 2: Run test to verify it fails** — `pytest tests/test_eval_isolation.py -v` → FAIL.

- [ ] **Step 3: Write minimal implementation** — `isolation.Sandbox` copies `<repo>/.claude/skills/<name>` into the temp product `.claude/skills/` for each dependency and (GREEN only) the target; builds `env` from `os.environ` with `HOME` overridden to the temp home; `tempfile.mkdtemp`-based dirs under caller-supplied roots; cleanup in `__exit__`. Copy via `shutil.copytree`.

- [ ] **Step 4: Run test to verify it passes** — `pytest tests/test_eval_isolation.py -v` → PASS.

- [ ] **Step 5: Commit**

```bash
git add evals/_harness/isolation.py tests/test_eval_isolation.py
git commit -m "feat(eval): isolation sandbox (temp HOME + repo-external cwd + skill-set control)"
```

---

## Task 3: Fresh-context runner (`runner.py`, mocked-subprocess TDD)

**Files:**
- Create: `evals/_harness/runner.py`, `tests/test_eval_runner.py`

**Interfaces:**
- Produces: `runner.run_once(prompt, sandbox, model=None) -> dict` that spawns headless `command claude -p <prompt> --output-format json` (resolved from the real `claude` binary, not the shell function) with `cwd=sandbox.product_cwd`, `env=sandbox.env`, captures stdout (the JSON result incl. transcript), and returns `{"returncode", "stdout", "transcript_path", "fresh_context_id"}`. The subprocess invocation is parameterized so tests inject a fake runner.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_eval_runner.py
"""TDD for the fresh-context runner. Subprocess is faked; the real claude run is the pilot (T7)."""
from __future__ import annotations
from pathlib import Path
from evals._harness import runner


class _FakeSandbox:
    def __init__(self, tmp_path: Path):
        self.product_cwd = tmp_path / "prod"; self.product_cwd.mkdir()
        self.temp_home = tmp_path / "home"; self.temp_home.mkdir()
        self.env = {"HOME": str(self.temp_home), "ANTHROPIC_API_KEY": "k", "PATH": "/usr/bin"}


def test_run_once_invokes_headless_claude_with_cwd_and_env(tmp_path, monkeypatch):
    captured = {}
    def fake_popen(cmd, **kw):
        captured["cmd"] = cmd
        captured["cwd"] = kw.get("cwd")
        captured["env"] = kw.get("env")
        class R:
            returncode = 0
            def communicate(self): return (b'{"result":"hi","session_id":"s1"}', b"")
        return R()
    monkeypatch.setattr(runner, "_popen", fake_popen)
    sb = _FakeSandbox(tmp_path)
    out = runner.run_once("Status please", sb, model="claude-test")
    assert "claude" in captured["cmd"][0] or captured["cmd"][0].endswith("claude")
    assert "-p" in captured["cmd"]
    assert captured["cwd"] == sb.product_cwd
    assert captured["env"]["HOME"] == sb.env["HOME"]
    assert out["returncode"] == 0
    assert out["fresh_context_id"] == "s1"


def test_run_once_records_nonzero_exit(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "_popen", lambda cmd, **kw:
                        type("R", (), {"returncode": 1, "communicate": lambda self: (b"", b"boom")})())
    out = runner.run_once("p", _FakeSandbox(tmp_path))
    assert out["returncode"] == 1 and out["fresh_context_id"] is None
```

- [ ] **Step 2: Run test to verify it fails** — `pytest tests/test_eval_runner.py -v` → FAIL.

- [ ] **Step 3: Write minimal implementation** — `runner.py`: resolve the real `claude` binary (`shutil.which("claude")`, falling back to `command claude` via `bash -lc`); build `cmd = [claude, "-p", prompt, "--output-format", "json"]` (+ `--model` if given); `_popen` wraps `subprocess.Popen(..., stdout=PIPE, stderr=PIPE, text=False)`; parse the JSON stdout for `session_id` → `fresh_context_id`; persist the raw stdout as the transcript under the sandbox temp home; return the dict.

- [ ] **Step 4: Run test to verify it passes** — `pytest tests/test_eval_runner.py -v` → PASS.

- [ ] **Step 5: Commit**

```bash
git add evals/_harness/runner.py tests/test_eval_runner.py
git commit -m "feat(eval): fresh-context runner (headless claude, cwd+env isolated)"
```

---

## Task 4: Judge (`judge.py` — check engine + src/bw oracle + needs-review)

**Files:**
- Create: `evals/_harness/judge.py`, `tests/test_eval_judge.py`

**Interfaces:**
- Produces: `judge.judge(manifest, run_artifact, sandbox) -> dict` returning `{checks: [...], forbidden_triggered: [...], verdict, reviewer: None}`. Implements the check `type` vocabulary: `transcript_contains`/`transcript_regex_present`/`transcript_regex_absent` (grep the transcript), `fs_no_new_files` (no new files under given paths relative to product_cwd), `fs_wrote_file_matching` (a file matching a glob was written), `oracle_validate_ok` (run `bw.validate`/`bw.gate_scan` read-only over the product `_bewater/` and assert no errors). Any NL `required_assertion` without a matching structured `check` is emitted as `verdict: needs-review` (human). Forbidden behaviors map to `fs_*`/`transcript_*` checks where possible; otherwise `needs-review`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_eval_judge.py
"""TDD for the judge: structured checks + oracle + needs-review (§11.1 no LLM-judging-LLM)."""
from __future__ import annotations
from pathlib import Path
from evals._harness import judge


def _manifest(checks, assertions=None, forbidden=None):
    return {"scenario_id": "S", "target_skill": "bw-start", "prompt": "p",
            "required_assertions": assertions or [], "forbidden_behaviors": forbidden or [],
            "repetition_count": 1, "checks": checks}


def test_transcript_regex_present_pass(tmp_path):
    t = tmp_path / "t.jsonl"; t.write_text('the gate presents Go and Kill exits\n')
    m = _manifest([{"id": "exits", "type": "transcript_regex_present",
                    "params": {"pattern": r"\b(Go|Kill)\b"}}])
    out = judge.judge(m, {"transcript_path": str(t)}, type("SB", (), {"product_cwd": tmp_path})())
    assert out["checks"][0]["verdict"] == "pass" and out["verdict"] == "green"


def test_fs_no_new_files_detects_a_write(tmp_path):
    (tmp_path / "_bewater-output").mkdir()
    (tmp_path / "_bewater-output" / "ART-1.md").write_text("x")  # forbidden artifact write
    m = _manifest([], forbidden=["writes an artifact"])
    out = judge.judge(m, {"transcript_path": str(tmp_path / "t.jsonl")},
                      type("SB", (), {"product_cwd": tmp_path})())
    assert "writes an artifact" in out["forbidden_triggered"]


def test_nl_assertion_without_check_is_needs_review(tmp_path):
    m = _manifest([], assertions=["presents the five permitted exits"])  # no structured check
    out = judge.judge(m, {"transcript_path": str(tmp_path / "t.jsonl")},
                      type("SB", (), {"product_cwd": tmp_path})())
    assert out["verdict"] == "needs-review"
    assert any(c["verdict"] == "needs-review" for c in out["checks"])
```

- [ ] **Step 2: Run test to verify it fails** — `pytest tests/test_eval_judge.py -v` → FAIL.

- [ ] **Step 3: Write minimal implementation** — `judge.py`: dispatch on `check["type"]`; read transcript from `run_artifact["transcript_path"]`; for `fs_*` resolve paths against `sandbox.product_cwd`; `oracle_validate_ok` imports `bw.validate`/`bw.gate_scan` in a try/except (legacy drift → `needs-review`, never crash the harness). Derive `verdict` = `needs-review` if any check/review-item is `needs-review`, else `green` if all pass + no forbidden triggered, else `red`.

- [ ] **Step 4: Run test to verify it passes** — `pytest tests/test_eval_judge.py -v` → PASS.

- [ ] **Step 5: Commit**

```bash
git add evals/_harness/judge.py tests/test_eval_judge.py
git commit -m "feat(eval): judge (structured checks + src/bw oracle + needs-review)"
```

---

## Task 5: Orchestrator + CLI (`orchestrator.py`, `__main__.py`)

**Files:**
- Create: `evals/_harness/orchestrator.py`, `evals/_harness/__main__.py`, `tests/test_eval_orchestrator.py`

**Interfaces:**
- Produces: `orchestrator.run_scenario(eval_root, repo, manifest, mode, reps, model=None, run_once=runner.run_once) -> list[dict]` (one result per rep) and `run_skill(...)`/`run_all(...)`. Per rep: build Sandbox → run_once → judge → write_result. Reps default to `manifest["repetition_count"]`. The orchestrator is fully injectable (`run_once`, sandbox factory) so it is unit-tested without any real LLM call. CLI: `python -m evals._harness run --skill <name> [--mode red|green] [--rep N] [--all] [--model M]`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_eval_orchestrator.py
"""TDD for the orchestrator. run_once is faked; no real LLM call."""
from __future__ import annotations
from pathlib import Path
import yaml
from evals._harness import orchestrator, result

REPO = Path(__file__).resolve().parents[1]


def _fake_runner(transcript_text):
    def _run(prompt, sandbox, model=None):
        t = sandbox.temp_home / "t.jsonl"
        t.write_text(transcript_text)
        return {"returncode": 0, "transcript_path": str(t), "fresh_context_id": "ctx"}
    return _run


def test_run_scenario_green_writes_reps(tmp_path):
    m = {"scenario_id": "BWSH-S1", "target_skill": "bw-shape", "prompt": "p",
         "required_assertions": ["routes"], "forbidden_behaviors": ["writes an artifact"],
         "repetition_count": 2,
         "checks": [{"id": "routes", "type": "transcript_contains", "params": {"needle": "bw-concept-gate"}}]}
    rs = orchestrator.run_scenario(tmp_path, REPO, m, mode="green", reps=2,
                                   run_once=_fake_runner("see bw-concept-gate next\n"))
    assert len(rs) == 2
    files = list((tmp_path / "bw-shape" / "green").glob("BWSH-S1-r*.json"))
    assert len(files) == 2 and all(json_load(f)["verdict"] == "green" for f in files)


def json_load(f):
    import json
    return json.loads(Path(f).read_text())


def test_run_scenario_red_must_fail_a_target_behavior(tmp_path):
    # RED = target absent; a well-formed RED transcript should miss the routing token -> red verdict
    m = {"scenario_id": "BWSH-R1", "target_skill": "bw-shape", "prompt": "p",
         "required_assertions": ["routes"], "forbidden_behaviors": [],
         "repetition_count": 1,
         "checks": [{"id": "routes", "type": "transcript_contains", "params": {"needle": "bw-concept-gate"}}]}
    rs = orchestrator.run_scenario(tmp_path, REPO, m, mode="red", reps=1,
                                   run_once=_fake_runner("i do not know what to do\n"))
    assert rs[0]["verdict"] == "red"
```

- [ ] **Step 2: Run test to verify it fails** — `pytest tests/test_eval_orchestrator.py -v` → FAIL.

- [ ] **Step 3: Write minimal implementation** — `orchestrator.py` wires isolation → runner → judge → result per rep; `__main__.py` is an argparse CLI over `run_skill`/`run_all` (both delegate to `run_scenario`). Discover manifests via `loader.load_manifest`.

- [ ] **Step 4: Run test to verify it passes** — `pytest tests/test_eval_orchestrator.py -v` → PASS.

- [ ] **Step 5: Commit**

```bash
git add evals/_harness/orchestrator.py evals/_harness/__main__.py tests/test_eval_orchestrator.py
git commit -m "feat(eval): orchestrator + CLI (per-scenario RED/GREEN loop, rep tiering)"
```

---

## Task 6: §11.3 result-gate checks in `scripts/verify.py`

**Files:**
- Modify: `scripts/verify.py`, `tests/test_verify_eval_gate.py`

**Interfaces:**
- Produces: `check_eval_results()` — for every scenario manifest under `evals/*/scenarios/` + `evals/*/red/`, assert (a) there are `repetition_count` result records with complete §11.1 fields; (b) every RED control's aggregate verdict is `red` (failed ≥1 target behavior); (c) every GREEN result verdict is `green` (all checks pass, no forbidden triggered); (d) any `needs-review` result carries a non-null `reviewer`. **Before results exist, this check is SKIPPED with a clear `eval results: not yet run (deferred §11.1)` notice** (not a failure) — so it lands safely before the pilot runs.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_verify_eval_gate.py
"""TDD for the §11.3 eval result-gate in verify.py (skips cleanly before results exist)."""
from __future__ import annotations
from pathlib import Path
import json
import verify


def test_check_eval_results_skips_when_no_results():
    ok, detail = verify.check_eval_results()
    # no results stored yet anywhere -> skip, not fail
    assert ok is True
    assert any("deferred" in str(d) or "not yet" in str(d) for d in detail) or detail == []


def test_check_eval_results_fails_on_green_with_untriggered_red_requirement(tmp_path, monkeypatch):
    # fabricate a RED result that wrongly passed (verdict green) -> gate must fail
    fake_evals = tmp_path / "evals"
    skill = fake_evals / "bw-start" / "red"; skill.mkdir(parents=True)
    (skill / "BWST-R1-r1.json").write_text(json.dumps({
        "scenario_id": "BWST-R1", "target_skill": "bw-start", "mode": "red", "repetition": 1,
        "verdict": "green", "fresh_context_id": "c", "cwd": "", "temp_home": "",
        "project_local_skills": [], "global_skills": [], "model": "", "transcript_path": "",
        "checks": [], "forbidden_triggered": [], "reviewer": None}))
    monkeypatch.setattr(verify, "EVALS", fake_evals)
    monkeypatch.setattr(verify, "list_eval_scenarios", lambda root: [("bw-start", "red", "BWST-R1", 1)],
                       raising=False)
    ok, detail = verify.check_eval_results()
    assert ok is False and any("red" in str(d).lower() for d in detail)
```

- [ ] **Step 2: Run test to verify it fails** — `pytest tests/test_verify_eval_gate.py -v` → FAIL.

- [ ] **Step 3: Write minimal implementation** — add `check_eval_results()` to `verify.py` (+ a `list_eval_scenarios(EVALS)` helper that walks `evals/*/scenarios|red/*.yaml` via `loader.load_manifest`). Skip (return `(True, ["eval results: deferred (§11.1)"])`) when zero result JSONs exist; otherwise enforce (a)–(d). Register `("eval-results", check_eval_results())` in `main()`.

- [ ] **Step 4: Run test to verify it passes** — `pytest tests/test_verify_eval_gate.py -v` → PASS; then `python scripts/verify.py` still prints `verified 20 skill(s)` (the new check skips cleanly).

- [ ] **Step 5: Commit**

```bash
git add scripts/verify.py tests/test_verify_eval_gate.py
git commit -m "feat(eval): §11.3 result-gate checks in verify (skip-until-run, then enforce)"
```

---

## Task 7: Pilot + acceptance (real fresh-context run on a subset)

**Files:** verify/run-only; may add `checks:` to a few manifests + store real results.

- [ ] **Step 1: Add structured `checks` to the pilot scenarios** — at minimum: a routing scenario (`bw-start` or `bw-shape`, RED+GREEN) and the two G1 safety-critical scenarios (`bw-strategy-gate/scenarios/g1-go`, `g1-no-authority`, `repetition_count: 5`). Map their NL assertions to structured checks (`transcript_contains` the routed skill / the five exits; `fs_no_new_files` for "no artifact written"; `transcript_regex_absent` for "does not record an exit"). Keep the NL assertions for human readability.

- [ ] **Step 2: Run the pilot end-to-end**

```bash
# one routing skill, RED then GREEN, 3 reps
python -m evals._harness run --skill bw-shape --mode red  --rep 3
python -m evals._harness run --skill bw-shape --mode green --rep 3
# G1 safety-critical, 5 reps (cost-significant; this is the real acceptance sample)
python -m evals._harness run --skill bw-strategy-gate --mode green --rep 5
```

Expected: RED results aggregate `red` (target absent → routing/exit assertions fail); GREEN results aggregate `green` (or `needs-review` for any assertion lacking a structured check — those get a human reviewer + `reviewer` filled). Capture any isolation/headless-claude feasibility failures here and fix the harness (not the plan).

- [ ] **Step 3: Acceptance gate**

```bash
pytest -q                                                # full suite incl. new harness tests, green
pytest --cov=evals._harness --cov=scripts/verify --cov-fail-under=80 -q   # harness ≥80%
python scripts/verify.py                                 # 20 skills + eval-results check now enforcing on pilot results
```

- [ ] **Step 4: Document the full-run cost estimate** — in `evals/README.md`, add the Phase-2-eval section: per-skill behavioral scenario count × reps, the 5× safety-critical set (both gates), and the estimated fresh-context-call total. This is the cost sign-off the human reviews before the full 20-skill run.

- [ ] **Step 5: Commit**

```bash
git add evals/ evals/README.md
git commit -m "test(eval): pilot fresh-context run (bw-shape routing + G1 safety-critical) + cost estimate"
```

---

## Self-Review

**1. Spec coverage (§11.1 behavioral TDD + §11.3 result gate):**
- §11.1 fresh-context, isolated HOME, repo-external cwd, target absent/present → T2 isolation ✓
- §11.1 RED then GREEN, 3 reps / 5 safety-critical, result fields → T1 result + T5 orchestrator ✓
- §11.1 no LLM-judging-LLM (structured checks + src/bw oracle + human review) → T4 judge ✓
- §11.1 cost control (deterministic already covered; only behavioral via LLM) → orchestrator runs only scenario manifests; deterministic matrix items stay in `tests/` ✓
- §11.2 scenario matrix — the matrix is the coverage target the full run (post-pilot) exercises; the harness runs whatever manifests exist ✓
- §11.3 result-gate checks (complete results, RED fails, GREEN passes, reviewer on manual) → T6 ✓

**Deferred (out of this plan, by design):**
- The full 20-skill behavioral run (the actual Phase-2 acceptance sign-off) — gated on the T7 cost estimate + human sign-off; the harness + pilot prove it is runnable.
- Adding structured `checks` to every behavioral manifest — T7 does the pilot subset; full population is part of the run.
- Phase 3 legacy disposition (§10.5) — unblocked once the full run passes; this plan does NOT delete `src/bw` (judge imports it read-only).

**2. Placeholder scan:** none. Every step carries real test code; the runner is unit-tested with a faked subprocess and validated for real only in the pilot (the LLM run is the eval, not a unit test).

**3. Interface consistency:**
- result payload fields ↔ judge output ↔ orchestrator write_result — consistent across T1/T4/T5 ✓
- manifest `checks: [{id,type,params}]` ↔ judge check-type dispatch — consistent T1/T4 ✓
- `run_once(prompt, sandbox, model)` signature — defined T3, injected T5 ✓
- `Sandbox(repo, product_root, home_root, target_skill, dependency_skills, mode)` — defined T2, used T3/T5 ✓

**4. Scope check:** the harness is one cohesive authoring-only deliverable that makes §11.1 runnable and §11.3 enforceable, without touching skills/bwkit/installer. The expensive part (full LLM run) is deliberately gated behind the T7 cost estimate + human sign-off.

**5. Feasibility risk:** the runner depends on headless `command claude -p --output-format json` behaving under an overridden `HOME`. T7 (pilot) is the feasibility gate — if isolation breaks claude's auth/config, fix the harness there (e.g., carry the API key + minimal config into the temp HOME) before any full run.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-07-30-bw-eval-harness.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — dispatch a fresh subagent per task (T1–T7), review between tasks. T1–T6 are deterministic (cheap implementers); T7 is the real-LLM pilot (run in the controller session, cost-visible).

**2. Inline Execution** — execute T1–T6 inline, run the T7 pilot with explicit cost visibility.

**Cost note for the human:** T1–T6 add only deterministic tests (no LLM cost). The LLM cost is entirely in T7's pilot (≈ a handful of skills × 3–5 fresh-context `claude` runs) and the later full run. **Do not start T7 / the full run without confirming the cost estimate.** Phase 3 (§10.5) follows once the full run passes.
