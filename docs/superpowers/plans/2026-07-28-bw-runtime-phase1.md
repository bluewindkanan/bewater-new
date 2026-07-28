# bw Runtime (Phase 1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the minimal deterministic `bw` CLI that owns all bewater decision-phase state (assumption ledger + artifact frontmatter + gate records) and enforces invariants / referential integrity / dual-sided / G1 gate evidence / content-hash stale detection — the foundation the Phase 1 skills call.

**Architecture:** Python 3 package `bw` installed as a console script `bw`. Pure functions over a `_bewater/` directory: load YAML state → validate/transform → write back. Five command groups (`init`, `ledger`, `validate`, `hash`, `gate-scan`). No locks, no concurrency, no journal — single-user, single-session. Skills (Plan B) shell out to `bw`; they never edit state files directly.

**Tech Stack:** Python ≥3.11, PyYAML (the single allowed dependency — stdlib has no YAML, and state files / artifact frontmatter are YAML), pytest + pytest-cov (dev). Stdlib otherwise only.

## Global Constraints

- **Language:** Python ≥3.11. One runtime dep: `PyYAML`. Dev deps: `pytest`, `pytest-cov`, `ruff`.
- **Coverage floor:** ≥80% on `src/bw/`, enforced in CI/Task 11.
- **No state mutation outside `bw`:** the CLI is the single writer of `_bewater/state/**` and artifact frontmatter `hash`/`last_validated_against`.
- **Deterministic, no time:** never call `datetime.now()` inside the runtime for logic; dates are passed in by the caller (CLI flag `--date` or skill). Hashing excludes volatile fields (`updated_at`) — see Task 5.
- **Naming:** console script `bw`; package `bw`; state root `_bewater/`.
- **Spec authority:** `docs/superpowers/specs/2026-07-27-bewater-decision-phase-skills-design.md` (v2). Schemas in §5 are the contract.
- **TDD:** every task writes the failing test first, watches it fail, writes minimal code, watches it pass, commits. No batch.

---

## File Structure

```
bewater-new/
├── pyproject.toml              # package metadata, [project.scripts] bw, deps, pytest/cov/ruff config
├── src/bw/
│   ├── __init__.py
│   ├── cli.py                  # argparse entry: subcommands init/ledger/validate/hash/gate-scan
│   ├── paths.py                # find_project_root(), state paths
│   ├── io.py                   # load_ledger/save_ledger, read_artifact/write_artifact (YAML+frontmatter)
│   ├── schema.py               # dataclasses + enums + field validation
│   ├── hashing.py              # content hash + stale detection
│   ├── ledger_ops.py           # add/update/validate/trace/backtrack/baseline
│   ├── validate.py             # system-wide validate
│   ├── gate_scan.py            # G1 (G2 criteria added in Phase 2)
│   └── errors.py               # ValidationError, invariant violation types
└── tests/
    ├── conftest.py             # tmp_project fixture: creates a `_bewater/` in tmp_path
    ├── test_io.py
    ├── test_schema.py
    ├── test_init.py
    ├── test_hashing.py
    ├── test_ledger_ops.py
    ├── test_validate.py
    └── test_gate_scan.py
```

Each module has one responsibility; `cli.py` is thin glue over the others.

---

## Task 1: Project scaffold + `bw --help`

**Files:**
- Create: `pyproject.toml`, `src/bw/__init__.py`, `src/bw/cli.py`, `tests/conftest.py`

**Interfaces:**
- Produces: console script `bw` with a `main(argv)->int` entry; subcommand parsers registered in later tasks.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_cli.py
import subprocess, sys

def test_bw_help_exits_zero_and_lists_command_groups():
    result = subprocess.run([sys.executable, "-m", "bw", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    out = result.stdout
    for grp in ["init", "ledger", "validate", "hash", "gate-scan"]:
        assert grp in out
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli.py -v`
Expected: FAIL — `No module named 'bw'`.

- [ ] **Step 3: Write minimal implementation**

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "bw"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["PyYAML>=6.0"]

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-cov>=5", "ruff>=0.5"]

[project.scripts]
bw = "bw.cli:main"

[tool.setuptools.packages.find] where = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]

[tool.coverage.run] source = ["bw"]
[tool.coverage.report] fail_under = 80
```

```python
# src/bw/__init__.py
__version__ = "0.1.0"
```

```python
# src/bw/cli.py
import argparse, sys

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="bw", description="bewater decision-phase deterministic runtime")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="scaffold _bewater/")
    sub.add_parser("ledger", help="assumption ledger add/update/validate/trace/backtrack/baseline")
    sub.add_parser("validate", help="check ledger + artifacts (invariants, refs, dual-sided, acyclic)")
    sub.add_parser("hash", help="content-hash an artifact; refresh dependency hashes")
    sub.add_parser("gate-scan", help="compute gate evidence pass/fail (G1)")
    return p

def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    print(f"bw: '{args.cmd}' not yet implemented")  # replaced task-by-task
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

```python
# tests/conftest.py
import pytest, yaml, os
from pathlib import Path

@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    (tmp_path / "_bewater" / "state").mkdir(parents=True)
    (tmp_path / "_bewater" / "artifacts").mkdir()
    (tmp_path / "_bewater" / "knowledge-base").mkdir()
    (tmp_path / "_bewater" / "state" / "assumption-ledger.yaml").write_text(
        yaml.safe_dump({"project": "t", "last_baselined_at": None, "baseline": None, "assumptions": []})
    )
    return tmp_path
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pip install -e '.[dev]' && pytest tests/test_cli.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml src/bw tests/conftest.py
git commit -m "feat(bw): scaffold package and bw --help"
```

---

## Task 2: Paths + YAML IO

**Files:** Create `src/bw/paths.py`, `src/bw/io.py`; Test `tests/test_io.py`.

**Interfaces:**
- Consumes: `_bewater/` layout from Task 1's `tmp_project`.
- Produces: `paths.find_project_root(start) -> Path`; `paths.ledger_path(root) -> Path`; `io.load_ledger(root) -> Ledger`; `io.save_ledger(root, ledger)`; `io.read_artifact(path) -> (ArtifactMeta, body:str)`; `io.write_artifact(path, meta, body)`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_io.py
from pathlib import Path
from bw import io, paths

def test_find_project_root_locates_bewater_dir(tmp_project):
    sub = tmp_project / "artifacts" / "discover"
    sub.mkdir(parents=True)
    assert paths.find_project_root(sub) == tmp_project

def test_round_trip_ledger(tmp_project):
    led = io.load_ledger(tmp_project)
    assert led.assumptions == []
    led.project = "renamed"
    io.save_ledger(tmp_project, led)
    assert io.load_ledger(tmp_project).project == "renamed"

def test_round_trip_artifact_frontmatter(tmp_project):
    p = tmp_project / "artifacts" / "immersion" / "charter.md"
    p.parent.mkdir(parents=True)
    meta, _ = io.read_artifact_dummy()  # helper below
    io.write_artifact(p, meta, "body text")
    m2, body2 = io.read_artifact(p)
    assert body2 == "body text"
    assert m2.artifact_id == meta.artifact_id
```

- [ ] **Step 2: Run → FAIL** (`ModuleNotFoundError: bw.paths`).

- [ ] **Step 3: Implement**

```python
# src/bw/paths.py
from pathlib import Path
STATE_DIR = "_bewater"
def find_project_root(start: Path) -> Path:
    p = Path(start).resolve()
    for cand in [p, *p.parents]:
        if (cand / STATE_DIR).is_dir():
            return cand
    raise FileNotFoundError(f"no _bewater/ found at or above {start}")
def ledger_path(root: Path) -> Path: return root / STATE_DIR / "state" / "assumption-ledger.yaml"
def artifacts_dir(root: Path) -> Path: return root / STATE_DIR / "artifacts"
def gates_dir(root: Path) -> Path: return root / STATE_DIR / "state" / "gates"
```

```python
# src/bw/io.py
import yaml
from pathlib import Path
from . import schema
from .paths import ledger_path

def load_ledger(root: Path) -> "schema.Ledger":
    data = yaml.safe_load(ledger_path(root).read_text()) or {}
    return schema.Ledger.from_dict(data)

def save_ledger(root: Path, ledger: "schema.Ledger") -> None:
    ledger_path(root).write_text(yaml.safe_dump(ledger.to_dict(), sort_keys=False, allow_unicode=True))

def read_artifact(path: Path) -> tuple["schema.ArtifactMeta", str]:
    text = Path(path).read_text()
    if not text.startswith("---\n"): return schema.ArtifactMeta.empty(), text
    end = text.index("\n---\n", 4)
    fm = yaml.safe_load(text[4:end])
    body = text[end+5:]
    return schema.ArtifactMeta.from_dict(fm or {}), body

def write_artifact(path: Path, meta: "schema.ArtifactMeta", body: str) -> None:
    fm = yaml.safe_dump(meta.to_dict(), sort_keys=False, allow_unicode=True)
    Path(path).write_text(f"---\n{fm}---\n{body}")
```

(`read_artifact_dummy` is a test helper creating a valid `ArtifactMeta`; define it in conftest or inline — it's test-only.)

- [ ] **Step 4: Run → PASS.**  Step 5: Commit `feat(bw): paths and YAML IO`.

---

## Task 3: Schema dataclasses + field validation

**Files:** Create `src/bw/schema.py`, `src/bw/errors.py`; Test `tests/test_schema.py`.

**Interfaces:**
- Produces: enums (`Layer`, `Impact`[low/medium/high], `EvidenceLevel`[L1..L6], `ValidationStatus`, `AssumptionStatus`[active/killed/merged], `ArtifactKind`, `ArtifactStatus`, `GateExit`); dataclasses `Assumption`, `Ledger`, `ArtifactMeta`, `GateRecord`; `Assumption.is_achilles_heel` computed property; `from_dict`/`to_dict` round-trip.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_schema.py
import pytest
from bw import schema
from bw.errors import ValidationError

def test_achilles_heel_is_high_high():
    a = schema.Assumption(id="A-1", statement="x", layer="concept", category="consumer",
                          impact="high", uncertainty="high", evidence_level="L3",
                          validation_status="open", status="active", evidence_ref="",
                          derived_from=[], affects=[], branch="sol-01")
    assert a.is_achilles_heel is True

def test_invariant_achilles_validated_needs_L4():
    a = schema.Assumption(id="A-1", statement="x", layer="concept", category="consumer",
                          impact="high", uncertainty="high", evidence_level="L3",
                          validation_status="validated", status="active", evidence_ref="kb/x",
                          derived_from=[], affects=[], branch="sol-01")
    with pytest.raises(ValidationError):
        a.check_invariants()   # achilles validated but L3 < L4

def test_assumption_round_trip():
    a = schema.Assumption(id="A-1", statement="x", layer="root", category="consumer",
                          impact="low", uncertainty="medium", evidence_level="L1",
                          validation_status="open", status="active", evidence_ref="",
                          derived_from=[], affects=[], branch="sol-01")
    a2 = schema.Assumption.from_dict(a.to_dict())
    assert a2 == a
```

- [ ] **Step 2: Run → FAIL.**

- [ ] **Step 3: Implement** — `schema.py` defines the enums and dataclasses; `Assumption.is_achilles_heel` = `impact=="high" and uncertainty=="high"`; `check_invariants()` raises `ValidationError` for: (1) `is_achilles_heel` != high×high; (2) achilles + validated + evidence_level<L4; (3) (falsified → backtrack is enforced in ledger_ops, not here — but `check_invariants` returns the falsified flag). `from_dict`/`to_dict` round-trip all fields. `errors.py` defines `ValidationError(Exception)`.

- [ ] **Step 4: Run → PASS.**  Step 5: Commit `feat(bw): schema dataclasses and invariants`.

---

## Task 4: `bw init` — scaffold `_bewater/`

**Files:** Modify `src/bw/cli.py` (wire `init`); Create impl in `src/bw/init.py`; Test `tests/test_init.py`.

**Interfaces:**
- Produces: `bw init [project]` creates `_bewater/{config.yaml,state/assumption-ledger.yaml,state/gates,artifacts/<stages>,knowledge-base}`; idempotent (no-op if ledger exists unless `--force`).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_init.py
from bw import cli
from pathlib import Path

def test_init_creates_scaffold(tmp_path):
    rc = cli.main(["init", str(tmp_path / "proj")])
    assert rc == 0
    root = tmp_path / "proj"
    assert (root / "_bewater" / "state" / "assumption-ledger.yaml").exists()
    for stage in ["immersion","discover","define","ideate","shape","handoff"]:
        assert (root / "_bewater" / "artifacts" / stage).is_dir()

def test_init_is_idempotent(tmp_path):
    root = tmp_path / "proj"
    cli.main(["init", str(root)])
    rc = cli.main(["init", str(root)])  # second run
    assert rc == 0
```

- [ ] **Step 2: Run → FAIL** (`not yet implemented`).

- [ ] **Step 3: Implement** `src/bw/init.py` `scaffold(root, force=False)` that `mkdir -p`s the tree and writes an empty ledger `{"project": root.name, "last_baselined_at": null, "baseline": null, "assumptions": []}` only if absent (unless `force`). Wire `cli.py` `init` subparser to call it.

- [ ] **Step 4: Run → PASS.**  Step 5: Commit `feat(bw): init scaffolds _bewater/`.

---

## Task 5: `bw hash` — content hash + stale detection

**Files:** Create `src/bw/hashing.py`; wire `hash` in `cli.py`; Test `tests/test_hashing.py`.

**Interfaces:**
- Consumes: `io.read_artifact`/`write_artifact` (Task 2).
- Produces: `hashing.content_hash(body:str)->str` (sha256 of body, excluding nothing in body but the CLI sets `meta.hash`); `hashing.refresh_deps(root, artifact_path)` rewrites every artifact whose `last_validated_against` references this id to `{id, hash}`. Detects stale by comparing stored `hash` in a dependent's `last_validated_against` against the upstream's current `hash`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_hashing.py
from bw import hashing, io, schema
from pathlib import Path

def _write(root, rel, aid, body, deps=None):
    p = root / rel; p.parent.mkdir(parents=True)
    meta = schema.ArtifactMeta(artifact_id=aid, kind="insights", stage="discover",
        status="final", hash="", locked=False, validated_by="", validated_at="",
        signoffs=[], dual_sided=None, derived_from=[], last_validated_against=deps or [], created_at="d", updated_at="d")
    io.write_artifact(p, meta, body); return p

def test_hash_stable_and_detects_edit(tmp_project):
    p = _write(tmp_project, "artifacts/discover/insights.md", "INS-1", "original body")
    hashing.hash_artifact(p)
    h1 = io.read_artifact(p)[0].hash
    assert h1 and h1 == hashing.content_hash("original body")
    io.write_artifact(p, io.read_artifact(p)[0], "edited body")
    assert io.read_artifact(p)[0].hash != hashing.content_hash("edited body")  # stale until re-hash

def test_refresh_deps_updates_dependents(tmp_project):
    upstream = _write(tmp_project, "artifacts/discover/insights.md", "INS-1", "ubody")
    hashing.hash_artifact(upstream)
    dep = _write(tmp_project, "artifacts/discover/hyp.md", "HYP-1", "hbody",
                 deps=[{"id":"INS-1","hash":"old"}])
    hashing.refresh_deps(tmp_project, upstream)
    deps2 = io.read_artifact(dep)[0].last_validated_against
    assert deps2[0]["hash"] == io.read_artifact(upstream)[0].hash
    assert hashing.is_stale(tmp_project, dep) is False
```

- [ ] **Step 2: Run → FAIL.**

- [ ] **Step 3: Implement** `hashing.py`: `content_hash(body)=hashlib.sha256(body.encode()).hexdigest()`; `hash_artifact(path)` reads meta, sets `meta.hash=content_hash(body)`, writes back; `refresh_deps(root, path)` scans all artifacts, for each entry in `last_validated_against` matching this artifact's id, sets its `hash` to current; `is_stale(root, dep_path)` returns True if any `last_validated_against[].hash` != the referenced artifact's current `hash`.

- [ ] **Step 4: Run → PASS.**  Step 5: Commit `feat(bw): hash and stale detection`.

---

## Task 6: `bw ledger add|update|validate` — write path + 3 invariants

**Files:** Create `src/bw/ledger_ops.py` (add/update/validate); wire `ledger` subcommands; Test `tests/test_ledger_ops.py`.

**Interfaces:**
- Consumes: `schema`, `io.load_ledger/save_ledger`.
- Produces: `ledger_ops.add(root, fields)->Assumption` (assigns `A-NNN` = max+1, defaults validation_status=open/evidence_level=L1/status=active, calls `check_invariants`, persists); `ledger_ops.update(root, id, changes)` (re-applies invariants, recomputes achilles on impact/uncertainty change); `ledger_ops.validate_one(root, id)->list[str]` (returns invariant violations).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_ledger_ops.py
import pytest
from bw import ledger_ops
from bw.errors import ValidationError

def _f(**over):
    base = dict(statement="s", layer="concept", category="consumer", impact="high",
                uncertainty="high", evidence_level="L3", validation_status="open",
                evidence_ref="", derived_from=[], affects=[], branch="sol-01")
    base.update(over); return base

def test_add_assigns_sequential_id_and_persists(tmp_project):
    a = ledger_ops.add(tmp_project, _f())
    assert a.id == "A-001"
    assert ledger_ops.add(tmp_project, _f()).id == "A-002"

def test_add_rejects_invariant_violation(tmp_project):
    # achilles + validated + L3 < L4
    with pytest.raises(ValidationError):
        ledger_ops.add(tmp_project, _f(validation_status="validated"))

def test_update_recomputes_achilles_on_impact_change(tmp_project):
    a = ledger_ops.add(tmp_project, _f(impact="low"))   # not achilles
    assert a.is_achilles_heel is False
    a2 = ledger_ops.update(tmp_project, a.id, {"impact":"high"})
    assert a2.is_achilles_heel is True
```

- [ ] **Step 2: Run → FAIL.**

- [ ] **Step 3: Implement** `ledger_ops.add/update/validate_one`. `add`: build `Assumption`, assign id, `check_invariants()` (raises on violation), append, save. `update`: load, apply changes, `is_achilles_heel` is a computed property so it auto-recomputes, `check_invariants()`, save. `validate_one`: return list of invariant violations without raising.

- [ ] **Step 4: Run → PASS.**  Step 5: Commit `feat(bw): ledger add/update/validate + invariants`.

---

## Task 7: `bw ledger trace` — lineage + cycle/dangling detection

**Files:** Extend `src/bw/ledger_ops.py` (`trace`); Test `tests/test_ledger_ops.py`.

**Interfaces:**
- Produces: `ledger_ops.trace(root, id, direction="upstream"|"downstream")->list[str]`; raises `ValidationError("dangling reference: <id>")` on unresolved id; raises `ValidationError("lineage cycle: ...")` on cycle.

- [ ] **Step 1: Write the failing test**

```python
def test_trace_upstream_and_downstream(tmp_project):
    ledger_ops.add(tmp_project, _f(id_override=None, statement="root", layer="root", derived_from=[]))
    # A-001 root; add A-002 derived_from A-001; A-003 derived_from A-002
    a2 = ledger_ops.add(tmp_project, _f(statement="mid", layer="strategy", derived_from=["A-001"]))
    a3 = ledger_ops.add(tmp_project, _f(statement="leaf", layer="concept", derived_from=["A-002"]))
    assert ledger_ops.trace(tmp_project, "A-003", "upstream") == ["A-002", "A-001"]
    assert ledger_ops.trace(tmp_project, "A-001", "downstream") == ["A-002", "A-003"]

def test_trace_detects_dangling(tmp_project):
    ledger_ops.add(tmp_project, _f(derived_from=["NOPE"]))
    with pytest.raises(ValidationError):
        ledger_ops.trace(tmp_project, "A-001", "upstream")

def test_trace_detects_cycle(tmp_project):
    ledger_ops.add(tmp_project, _f(statement="a", derived_from=["A-002"]))
    ledger_ops.add_raw(tmp_project, _f(id_override="A-002", statement="b", derived_from=["A-001"]))  # bypass for test setup
    with pytest.raises(ValidationError):
        ledger_ops.trace(tmp_project, "A-001", "upstream")
```

- [ ] **Step 2: Run → FAIL.**

- [ ] **Step 3: Implement** `trace` as a graph walk over `derived_from` (upstream) / `affects`+reverse-derived (downstream) with a visited set → raise on revisit (cycle) or unresolved id (dangling). (`add_raw` is a test helper that writes without invariant checks — add to a test fixture, not production.)

- [ ] **Step 4: Run → PASS.**  Step 5: Commit `feat(bw): ledger trace with cycle/dangling detection`.

---

## Task 8: `bw ledger baseline` + `bw ledger backtrack`

**Files:** Extend `src/bw/ledger_ops.py` (`baseline`, `backtrack`); Test `tests/test_ledger_ops.py`.

**Interfaces:**
- Produces: `ledger_ops.baseline(root, label="G2")->dict` (snapshot `{assumption_id: <fields used by boundary check>}` + all artifact `{id: hash}` → writes `ledger.last_baselined_at=label`, `ledger.baseline=snapshot`); `ledger_ops.backtrack(root, falsified_id)->BacktrackResult(depth_target, type, affected_ids, must_repass_gate)`.

- [ ] **Step 1: Write the failing test**

```python
def test_backtrack_depth_by_layer(tmp_project):
    ledger_ops.add(tmp_project, _f(statement="root", layer="root", derived_from=[]))
    ledger_ops.add(tmp_project, _f(statement="con", layer="concept", derived_from=["A-001"]))
    # falsify the concept-level one -> small loop
    ledger_ops.update(tmp_project, "A-002", {"validation_status":"falsified"})
    r = ledger_ops.backtrack(tmp_project, "A-002")
    assert r.loop_type == "small" and r.depth_target == "reframe"
    # falsify the root one -> large loop to Discover
    ledger_ops.update(tmp_project, "A-001", {"validation_status":"falsified"})
    r = ledger_ops.backtrack(tmp_project, "A-001")
    assert r.loop_type == "large" and r.depth_target == "Discover"

def test_backtrack_upgrades_to_large_if_baseline_touched(tmp_project):
    ledger_ops.add(tmp_project, _f(statement="root", layer="concept", derived_from=[]))
    ledger_ops.baseline(tmp_project, "G2")
    ledger_ops.update(tmp_project, "A-001", {"validation_status":"falsified"})
    r = ledger_ops.backtrack(tmp_project, "A-001")
    assert r.must_repass_gate == "G2"   # touched baseline -> re-pass original gate

def test_backtrack_marks_downstream_stale(tmp_project):
    ledger_ops.add(tmp_project, _f(statement="root", layer="root", derived_from=[]))
    ledger_ops.add(tmp_project, _f(statement="con", layer="concept", affects=["A-001"]))
    ledger_ops.update(tmp_project, "A-001", {"validation_status":"falsified"})
    r = ledger_ops.backtrack(tmp_project, "A-001")
    assert "A-002" in r.affected_ids
```

- [ ] **Step 2: Run → FAIL.**

- [ ] **Step 3: Implement** `backtrack`: read `falsified_id.layer` → map `feature|concept→small/reframe`, `opportunity|strategy→large/Define`, `root→large/Discover`; walk downstream `affects` for `affected_ids`; if any affected is in `ledger.baseline` (when set) → `must_repass_gate=last_baselined_at`, loop_type="large". `baseline`: snapshot current assumption ids + every artifact's `{id:hash}` into `ledger.baseline`.

- [ ] **Step 4: Run → PASS.**  Step 5: Commit `feat(bw): ledger baseline and backtrack routing`.

---

## Task 9: `bw validate` — system-wide check

**Files:** Create `src/bw/validate.py`; wire `validate` in `cli.py`; Test `tests/test_validate.py`.

**Interfaces:**
- Consumes: `ledger_ops.validate_one`, `trace` (cycle/dangling), `schema` (dual-sided kinds).
- Produces: `validate.validate_all(root)->list[Issue]` where `Issue=(scope, kind, message)`; kinds: `invariant-violation`, `dangling-ref`, `cycle`, `single-sided`, `missing-final`. Exit code: 0 if no issues else 1; prints issues.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_validate.py
from bw import validate, ledger_ops, io, schema
from pathlib import Path

def test_validate_passes_clean(tmp_project):
    ledger_ops.add(tmp_project, dict(statement="s", layer="concept", category="consumer",
        impact="low", uncertainty="low", evidence_level="L1", validation_status="open",
        evidence_ref="", derived_from=[], affects=[], branch="sol-01"))
    assert validate.validate_all(tmp_project) == []

def test_validate_flags_single_sided(tmp_project):
    p = tmp_project/"artifacts/define/strategy.md"; p.parent.mkdir(parents=True)
    meta = schema.ArtifactMeta(artifact_id="S-1", kind="solution", stage="shape", status="final",
        hash="x", locked=False, validated_by="", validated_at="", signoffs=[],
        dual_sided={"money":{"commercial_value_proposition":"","leverageable_assets":""},
                    "magic":{"consumer_value_proposition":"c","consumer_target":"t"},"tension":""},
        derived_from=[], last_validated_against=[], created_at="d", updated_at="d")
    io.write_artifact(p, meta, "body")
    issues = validate.validate_all(tmp_project)
    assert any(i.kind=="single-sided" for i in issues)

def test_validate_flags_dangling(tmp_project):
    ledger_ops.add(tmp_project, dict(statement="s", layer="concept", category="consumer",
        impact="low", uncertainty="low", evidence_level="L1", validation_status="open",
        evidence_ref="", derived_from=["GONE"], affects=[], branch="sol-01"))
    issues = validate.validate_all(tmp_project)
    assert any(i.kind=="dangling-ref" for i in issues)
```

- [ ] **Step 2: Run → FAIL.**

- [ ] **Step 3: Implement** `validate_all`: iterate assumptions → `validate_one` (invariant-violation); build id-set of assumptions+artifacts → check every `derived_from`/`affects` resolves (dangling-ref); run `trace` on each to surface cycles; iterate artifacts with kind in {charter,directional-hypothesis,concept,solution} → dual-sided four elements non-empty (single-sided); report artifacts referenced by a gate/gate-scan but `status!=final` (missing-final). Return issues.

- [ ] **Step 4: Run → PASS.**  Step 5: Commit `feat(bw): system-wide validate`.

---

## Task 10: `bw gate-scan G1`

**Files:** Create `src/bw/gate_scan.py`; wire `gate-scan` in `cli.py`; Test `tests/test_gate_scan.py`.

**Interfaces:**
- Consumes: `io`, `schema`, `validate`.
- Produces: `gate_scan.scan(root, gate="G1", subject=None)->GateScanResult(criteria:list[Criterion(name, passed:bool, blocking:bool, note)], exit_allowed:list[str])`. `exit_allowed` excludes `go` if any blocking criterion fails. Scans only the subject's active lineage (assumptions with `status=="active"` on the subject solution's `branch`); killed/merged excluded.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_gate_scan.py
from bw import gate_scan, io, schema

def _mk(root, rel, kind, stage, status="final", dual=None, locked=False, signoffs=None):
    p = root/rel; p.parent.mkdir(parents=True)
    meta = schema.ArtifactMeta(artifact_id=rel.stem, kind=kind, stage=stage, status=status,
        hash="x", locked=locked, validated_by="", validated_at="", signoffs=signoffs or [],
        dual_sided=dual, derived_from=[], last_validated_against=[], created_at="d", updated_at="d")
    io.write_artifact(p, meta, "body")

def test_g1_blocks_when_thin(tmp_project):
    r = gate_scan.scan(tmp_project, "G1", subject=None)
    assert "go" not in r.exit_allowed
    assert any(c.name=="missing-artifact" and c.blocking for c in r.criteria)

def test_g1_passes_when_complete(tmp_project):
    ds = {"money":{"commercial_value_proposition":"m","leverageable_assets":"l"},
          "magic":{"consumer_value_proposition":"c","consumer_target":"t"},"tension":""}
    _mk(tmp_project,"artifacts/immersion/charter.md","charter","immersion",dual=ds)
    _mk(tmp_project,"artifacts/discover/insights.md","insights","discover",
        signoffs=[{"who":"u","role":"lead","what":"F/P/E/T","at":"d"}])
    for i in (1,2):
        _mk(tmp_project,f"artifacts/discover/hyp{i}.md","directional-hypothesis","discover",dual=ds)
    _mk(tmp_project,"artifacts/define/strategy.md","strategy","define",locked=True)
    _mk(tmp_project,"artifacts/define/oa.md","opportunity-area","define")
    from bw import ledger_ops
    ledger_ops.add(tmp_project, dict(statement="ach", layer="concept", category="consumer",
        impact="high", uncertainty="high", evidence_level="L1", validation_status="open",
        evidence_ref="", derived_from=[], affects=[], branch="sol-01"))
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    assert "go" in r.exit_allowed, [c.name for c in r.criteria if not c.passed]

def test_g1_excludes_killed_assumptions(tmp_project):
    from bw import ledger_ops
    a = ledger_ops.add(tmp_project, dict(statement="k", layer="concept", category="consumer",
        impact="high", uncertainty="high", evidence_level="L1", validation_status="open",
        evidence_ref="", derived_from=[], affects=[], branch="sol-01"))
    ledger_ops.update(tmp_project, a.id, {"status":"killed"})
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    assert not any("killed" in (c.note or "") for c in r.criteria)  # killed not counted
```

- [ ] **Step 2: Run → FAIL.**

- [ ] **Step 3: Implement** `gate_scan.scan` G1 criteria (mechanical subset — blade/non-overlap are flagged `note="requires human judgment"`, non-blocking):
  - `charter`: exists, status final, dual-sided complete → else `missing-artifact`/`single-sided`.
  - `directional-hypotheses`: count 2–5, each dual-sided → else `gate-criteria-incomplete`.
  - `insights`: each carries a signoff `what=="F/P/E/T"` → else `gate-criteria-incomplete`.
  - `strategy`: exists, `locked==True` → else `gate-criteria-incomplete`.
  - `opportunity-areas`: count 2–4 → else `gate-criteria-incomplete`.
  - `ledger`: ≥1 `is_achilles_heel` on active lineage (quadrant identified) → else `gate-criteria-incomplete`.
  - `exit_allowed`: if any blocking → `["conditional-go","recycle","pivot","kill"]`; else all five incl. `go`.
  Subject scope: filter assumptions to `branch==subject` and `status=="active"`.

- [ ] **Step 4: Run → PASS.**  Step 5: Commit `feat(bw): gate-scan G1`.

---

## Task 11: Coverage gate + install + smoke

**Files:** `.gitignore` (add `src/bw.egg-info/`, `build/`, `dist/`); verify only.

**Interfaces:**
- Produces: `pytest --cov=bw --cov-fail-under=80` green; `bw` on PATH after `pip install -e .`; a recorded smoke run.

- [ ] **Step 1: Write the failing test** (a smoke test that the installed CLI works end-to-end on a temp project)

```python
# tests/test_smoke.py
import subprocess, sys
def test_end_to_end_init_add_validate(tmp_path):
    subprocess.run([sys.executable,"-m","bw","init",str(tmp_path/"p")], check=True)
    subprocess.run([sys.executable,"-m","bw","ledger","add",str(tmp_path/"p"),
        "--statement","s","--layer","concept","--category","consumer",
        "--impact","high","--uncertainty","high","--branch","sol-01"], check=True)
    r = subprocess.run([sys.executable,"-m","bw","validate",str(tmp_path/"p")], capture_output=True, text=True)
    assert r.returncode == 0
```

- [ ] **Step 2: Run → FAIL** (CLI flags not wired — wire `ledger add` / `validate` argparse in `cli.py` to call the ops with parsed args; this is the glue task).

- [ ] **Step 3: Implement** the argparse glue in `cli.py` for all subcommands (each calls the function from Tasks 4–10, prints a result table, returns 0/1). Run coverage.

Run: `pytest --cov=bw --cov-report=term-missing`
Expected: ≥80%; fix uncovered branches by adding tests (not by deleting tests).

- [ ] **Step 4: Run → PASS** (`bw` on PATH after `pip install -e .`, smoke green, cov ≥80%).

- [ ] **Step 5: Commit**

```bash
git add src/bw/cli.py tests/test_smoke.py .gitignore
git commit -m "feat(bw): wire CLI subcommands, smoke test, 80% coverage gate"
```

---

## Self-Review (run after writing, before handoff)

- **Spec coverage:** spec §4 CLI ops — `init`(T4) ✓ `ledger`(T6-8) ✓ `validate`(T9) ✓ `gate-scan`(T10) ✓ `hash`(T5) ✓. §5.1 3 invariants — T3/T6 ✓. §5.2 dual-sided/hash/signoffs/locked/last_validated_against — T3/T5/T9/T10 ✓. §5.3 gate record (write path) — deferred to Plan B (skills write the record via a thin `bw gate record` add; acceptable since G1 decision record is produced at gate-execution time, not runtime). §5.4 active-lineage/killed — T10 ✓. §7 G1 criteria — T10 ✓. §8 backtrack depth/baseline-boundary — T8 ✓. §13 unit tests ≥80% + edge cases (duplicate-id, dangling, cycle, stale, killed) — T6/T7/T8/T9/T10 ✓. **Gap:** duplicate-id detection — add a one-line assertion in `add` (Task 6) that `id` not already present; add a test. (Implementer: add `test_add_rejects_duplicate_id` to Task 6.)
- **Placeholder scan:** none — each step has real test code or a concrete implement instruction with named functions matching the Interfaces block.
- **Type consistency:** `Assumption.is_achilles_heel` (property, T3) used in T6/T8/T10 ✓. `last_validated_against` is `list[{id,hash}]` in T2/T5/T9 ✓. `BacktrackResult(loop_type, depth_target, affected_ids, must_repass_gate)` defined in T8, fields match tests ✓. `GateScanResult(criteria, exit_allowed)` and `Criterion(name, passed, blocking, note)` defined in T10 ✓.

---

## Execution Handoff

**Plan A complete and saved to `docs/superpowers/plans/2026-07-28-bw-runtime-phase1.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — execute tasks in this session via executing-plans, batch with checkpoints.

**Which approach?** (Plan B — the 13 Phase-1 skills built on this CLI — is written once Plan A lands, so skills call a verified `bw`.)
