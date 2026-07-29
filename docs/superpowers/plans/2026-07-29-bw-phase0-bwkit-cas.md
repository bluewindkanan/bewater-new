# BeWater Phase 0 + bwkit/cas Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Phase 0 foundation (SUPERSEDED banner on the legacy plan, `_bw-shared/` authoritative reference schemas, eval harness scaffold, installer test harness scaffold) and the first P0 helper `bwkit/cas` (stdlib-only single-writer lock + text-level revision CAS), so Phase 1 skills have a deterministic, schema-agnostic foundation.

**Architecture:** `bwkit` is a standard-library-only Python package under `src/bwkit/` (distinct from legacy `src/bw/`), invoked by skills via `python -m bwkit` (tool repo) or the deployed `_bw-shared/bwkit/` (installed, Phase 1). It exposes two narrow primitives — an `O_CREAT|O_EXCL` single-writer lock with stale preemption, and a text-level revision CAS (read revision by regex, verify expected + bump, back up, atomic-write) — with **zero YAML parsing** and **no authority over gate outcomes**. Phase 0 also lands the `_bw-shared/` reference schemas and the eval/installer test-harness scaffolding. `install.sh` itself and `scripts/verify` are deferred to Phase 1 (they verify/install the 19 skills, which do not exist yet).

**Tech Stack:** Python ≥3.11. `bwkit` is **stdlib-only** (`hashlib`, `os`, `re`, `argparse`, `sys`, `json`, `time`). pytest + pytest-cov (existing dev deps). PyYAML is used only in tests, schemas, and the eval harness — never inside `src/bwkit/`. No new runtime dependencies.

## Global Constraints

- **Spec authority:** `docs/superpowers/specs/2026-07-27-bewater-decision-phase-skills-design.md` v5.1 + H1a. §12.5 is the `bwkit/cas` contract; §10.2 is the Phase 0 contract; §2.3 governs shared references.
- **`bwkit` is stdlib-only:** `hashlib`/`os`/`re`/`argparse`/`sys`/`json`/`time` only. Never `import yaml` and never `from bw import …` inside `src/bwkit/` (importing `bw.hashing` pulls `bw.io` → PyYAML). `content_hash` is **inlined** as the same `hashlib.sha256` one-liner (semantically identical to `bw.hashing.content_hash`, §12.5).
- **`bwkit` never parses YAML:** revision is read by regex on the top-level `^revision:` line; CAS writes the caller's `new_text` **verbatim**. Schema/field semantics and field preservation are the caller's responsibility (§12.5 Non-goals).
- **No gate authority:** `bwkit` never chooses or relaxes a gate exit (§12.2). It only enforces deterministic mechanism (lock, CAS, backup, atomic write).
- **Helper state root is `_bewater/`:** lock at `_bewater/.bw-lock`, backups at `_bewater/.backup-{stem}-{old_rev}-{time_ns}`. No `runtime/` subdirectory (§12.2).
- **Coverage floor:** `bwkit` ≥80%, enforced via `[tool.coverage.run] source = ["bw", "bwkit"]` (Task 1) and the gate in Task 5.
- **Legacy untouched:** do not modify or delete `src/bw/` or its tests (§10.2). They are a non-shipped oracle.
- **TDD:** every task writes the failing test first, watches it fail, writes minimal code, watches it pass, commits. No batch.
- **Naming:** package `bwkit`; console entry `python -m bwkit`; state root `_bewater/`.
- **Commit convention:** `feat(bwkit): …` / `chore(phase0): …` / `docs(phase0): …`. Commit only the files each task touches.

---

## File Structure

```
bewater-new/
├── pyproject.toml                       # MODIFY: coverage source -> ["bw", "bwkit"]
├── docs/superpowers/plans/
│   ├── 2026-07-28-bw-runtime-phase1.md  # MODIFY: prepend SUPERSEDED banner
│   └── 2026-07-29-bw-phase0-bwkit-cas.md # this plan (created by writing-plans)
├── src/bwkit/                           # CREATE / EXTEND package
│   ├── __init__.py                      # exists (docstring only); leave as-is
│   ├── cas.py                           # CREATE: content_hash, lock, revision CAS, errors
│   ├── cli.py                           # CREATE: argparse main(argv, *, _stdin) -> int
│   └── __main__.py                      # CREATE: delegates to cli.main
├── tests/
│   ├── conftest.py                      # MODIFY: add tmp_home / tmp_dest fixtures
│   ├── test_phase0_scaffold.py          # CREATE: banner + coverage config
│   ├── test_bwkit_lock.py               # CREATE: lock matrix
│   ├── test_bwkit_cas.py                # REWRITE: commit/new_text API (was cas_update/mutate)
│   ├── test_bwkit_cli.py                # CREATE: cli.main wiring
│   ├── test_bwkit_smoke.py              # CREATE: subprocess end-to-end
│   ├── test_shared_schemas.py           # CREATE: _bw-shared references + contract frontmatter
│   ├── test_eval_harness.py             # CREATE: eval manifest schema + loader
│   ├── installer_helpers.py             # CREATE: managed-marker helpers
│   └── test_installer_harness.py        # CREATE: tmp HOME/dest fixtures self-test
├── .claude/skills/_bw-shared/           # CREATE
│   ├── ledger-schema.md                 # authoritative §5 field schema
│   ├── gate-criteria.md                 # G1 readiness (§6.3); G2 stubbed for Phase 2
│   └── glossary.md                      # core terms
├── evals/                               # CREATE harness scaffold
│   ├── __init__.py
│   └── _harness/
│       ├── __init__.py
│       ├── manifest_schema.json         # scenario manifest JSON schema
│       └── loader.py                    # ManifestError + load_manifest(path)
└── (install.sh, scripts/verify)         # DEFERRED to Phase 1
```

Each module has one responsibility: `cas.py` is the deterministic primitive, `cli.py` is thin argparse glue over it. Tests mirror the module split (lock vs cas vs cli).

---

## Task 1: Setup — SUPERSEDED banner + coverage config

**Files:**
- Modify: `docs/superpowers/plans/2026-07-28-bw-runtime-phase1.md` (prepend banner)
- Modify: `pyproject.toml` (`[tool.coverage.run]` source)
- Test: `tests/test_phase0_scaffold.py`

**Interfaces:**
- Produces: `pyproject.toml` `[tool.coverage.run] source = ["bw", "bwkit"]`; the legacy plan carries a visible SUPERSEDED banner matching the spec's authority declaration (§0/§10.2).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_phase0_scaffold.py
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_old_runtime_plan_has_superseded_banner():
    plan = REPO / "docs" / "superpowers" / "plans" / "2026-07-28-bw-runtime-phase1.md"
    text = plan.read_text()
    assert "SUPERSEDED" in text
    assert "2026-07-27-bewater-decision-phase-skills-design.md" in text
    assert "do not execute" in text.lower()


def test_coverage_source_includes_bwkit():
    text = (REPO / "pyproject.toml").read_text()
    assert 'source = ["bw", "bwkit"]' in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_phase0_scaffold.py -v`
Expected: FAIL — banner absent; current source is `["bw"]`.

- [ ] **Step 3: Write minimal implementation**

In `pyproject.toml`, replace the coverage source block:

```toml
[tool.coverage.run]
source = ["bw", "bwkit"]
```

Prepend this banner to `docs/superpowers/plans/2026-07-28-bw-runtime-phase1.md` (above the existing `# bw Runtime (Phase 1) Implementation Plan` title):

```markdown
> **⚠️ SUPERSEDED — DO NOT EXECUTE.** This plan builds the abandoned general-purpose
> `bw` CLI runtime (pre-v5). The authoritative design is
> `docs/superpowers/specs/2026-07-27-bewater-decision-phase-skills-design.md` (v5.1),
> which ships markdown skills plus the narrow `bwkit` helper instead of a runtime.
> This file is retained only as a legacy behavioral oracle per spec §0 and §10.5.
> Do not implement any task below.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_phase0_scaffold.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml docs/superpowers/plans/2026-07-28-bw-runtime-phase1.md tests/test_phase0_scaffold.py
git commit -m "chore(phase0): supersede legacy runtime plan + coverage source includes bwkit"
```

---

## Task 2: bwkit/cas — `content_hash` + single-writer lock

**Files:**
- Create: `src/bwkit/cas.py`
- Test: `tests/test_bwkit_lock.py`

**Interfaces:**
- Produces (other tasks rely on these exact names/signatures):
  - `cas.content_hash(body: str) -> str`
  - `cas.lock_path(root: Path) -> Path`  → `root/_bewater/.bw-lock`
  - `cas.acquire_lock(root, owner, ttl_seconds: int = 3600) -> dict`  → `{owner, pid, acquired_at}`
  - `cas.release_lock(root, owner) -> None`
  - `cas.lock_status(root) -> dict | None`
  - `cas.LockError(Exception)`
  - (also defines `CasConflict`, `BadRevisionBump` here; raised first in Task 3)

- [ ] **Step 1: Write the failing test**

```python
# tests/test_bwkit_lock.py
"""TDD for bwkit.cas single-writer lock (spec §12.5). Stdlib-only."""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
import yaml

from bwkit import cas


@pytest.fixture
def v5_root(tmp_path: Path) -> Path:
    (tmp_path / "_bewater").mkdir()
    return tmp_path


def test_content_hash_is_sha256_of_body():
    assert cas.content_hash("hello") == hashlib.sha256(b"hello").hexdigest()


def test_acquire_creates_exclusive_lockfile(v5_root):
    info = cas.acquire_lock(v5_root, owner="s1")
    assert info["owner"] == "s1"
    assert cas.lock_path(v5_root).exists()
    assert "pid" in info and "acquired_at" in info


def test_second_acquire_is_rejected(v5_root):
    cas.acquire_lock(v5_root, owner="s1")
    with pytest.raises(cas.LockError) as exc:
        cas.acquire_lock(v5_root, owner="s2")
    assert "s1" in str(exc.value)


def test_release_lets_next_session_acquire(v5_root):
    cas.acquire_lock(v5_root, owner="s1")
    cas.release_lock(v5_root, owner="s1")
    assert cas.acquire_lock(v5_root, owner="s2")["owner"] == "s2"


def test_release_wrong_owner_is_rejected(v5_root):
    cas.acquire_lock(v5_root, owner="s1")
    with pytest.raises(cas.LockError):
        cas.release_lock(v5_root, owner="s2")
    assert cas.lock_status(v5_root)["owner"] == "s1"


def test_release_when_unlocked_is_noop(v5_root):
    cas.release_lock(v5_root, owner="s1")  # must not raise


def test_lock_status_none_when_unlocked(v5_root):
    assert cas.lock_status(v5_root) is None


def test_stale_pid_dead_is_preemptable(v5_root):
    cas.acquire_lock(v5_root, owner="dead-session")
    p = cas.lock_path(v5_root)
    data = yaml.safe_load(p.read_text())
    data["pid"] = 999999  # almost certainly not running
    p.write_text(yaml.safe_dump(data))
    assert cas.acquire_lock(v5_root, owner="s2")["owner"] == "s2"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bwkit_lock.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'bwkit.cas'`.

- [ ] **Step 3: Write minimal implementation**

```python
# src/bwkit/cas.py
"""bwkit/cas — single-writer lock + text-level revision CAS (stdlib-only).

Schema-agnostic and YAML-agnostic. See design spec §12.5. This module never
imports yaml and never imports from the legacy bw package.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path

LOCKNAME = ".bw-lock"
BACKUP_PREFIX = ".backup-"


class LockError(Exception):
    """Lock contention or owner mismatch."""


class CasConflict(Exception):
    """Current revision != expected_revision (no write performed)."""


class BadRevisionBump(Exception):
    """new_text top-level revision != expected_revision + 1."""


def content_hash(body: str) -> str:
    return hashlib.sha256(body.encode()).hexdigest()


def lock_path(root) -> Path:
    return Path(root) / "_bewater" / LOCKNAME


def acquire_lock(root, owner, ttl_seconds: int = 3600) -> dict:
    root = Path(root)
    (root / "_bewater").mkdir(parents=True, exist_ok=True)
    path = lock_path(root)
    info = {"owner": owner, "pid": os.getpid(), "acquired_at": time.time()}
    try:
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError:
        holder = _read_lock(path)
        if holder is not None and not _is_stale(holder, ttl_seconds):
            raise LockError(f"locked by {holder.get('owner')}")
        tmp = path.with_name(f"{LOCKNAME}.tmp-{os.getpid()}")
        tmp.write_text(json.dumps(info))
        os.replace(tmp, path)  # atomic preempt of stale lock
        return info
    try:
        os.write(fd, json.dumps(info).encode())
    finally:
        os.close(fd)
    return info


def release_lock(root, owner) -> None:
    path = lock_path(Path(root))
    holder = _read_lock(path)
    if holder is None:
        return  # unlocked: no-op
    if holder.get("owner") != owner:
        raise LockError(f"lock held by {holder.get('owner')}, not {owner}")
    path.unlink()


def lock_status(root):
    return _read_lock(lock_path(Path(root)))


def _read_lock(path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, ValueError):
        return None


def _is_stale(holder: dict, ttl_seconds: int) -> bool:
    pid = holder.get("pid")
    if not isinstance(pid, int):
        return True
    try:
        os.kill(pid, 0)
        running = True
    except ProcessLookupError:
        running = False
    except PermissionError:
        running = True
    if running:
        return (time.time() - holder.get("acquired_at", 0.0)) > ttl_seconds
    return True
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_bwkit_lock.py -v`
Expected: PASS (all 8).

- [ ] **Step 5: Commit**

```bash
git add src/bwkit/cas.py tests/test_bwkit_lock.py
git commit -m "feat(bwkit): stdlib-only single-writer lock with stale preemption"
```

---

## Task 3: bwkit/cas — text-level revision CAS (rewrite the old test)

**Files:**
- Modify: `src/bwkit/cas.py` (append `read_revision`, `commit`, `_rotate_backup`)
- Rewrite: `tests/test_bwkit_cas.py` (was the old `cas_update`/`mutate` design; now `commit`/`new_text`)

**Interfaces:**
- Consumes: `content_hash` (Task 2)
- Produces:
  - `cas.read_revision(path) -> int`  (`FileNotFoundError` if absent, `KeyError` if no top-level `revision:`)
  - `cas.commit(path, new_text: str, expected_revision: int, *, keep_backups: int = 5) -> {"revision": int, "hash": str}`
  - raises `cas.CasConflict`, `cas.BadRevisionBump` (defined in Task 2)

- [ ] **Step 1: Rewrite the failing test**

Replace the entire contents of `tests/test_bwkit_cas.py`:

```python
# tests/test_bwkit_cas.py
"""TDD for bwkit.cas text-level revision CAS (spec §12.5, H1). Stdlib-only:
bwkit never parses YAML; the caller supplies new_text verbatim."""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from bwkit import cas


@pytest.fixture
def v5_root(tmp_path: Path) -> Path:
    bw = tmp_path / "_bewater"
    bw.mkdir()
    (bw / "ledger.yaml").write_text(yaml.safe_dump(
        {"schema_version": 1, "revision": 3, "next_id": 4, "assumptions": {}}))
    return tmp_path


def _ledger(root: Path) -> Path:
    return root / "_bewater" / "ledger.yaml"


def _bump(text: str, new_rev: int) -> str:
    return re.sub(r"(?m)^revision:\s*\d+", f"revision: {new_rev}", text, count=1)


def test_read_revision(v5_root):
    assert cas.read_revision(_ledger(v5_root)) == 3


def test_read_revision_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        cas.read_revision(tmp_path / "missing.yaml")


def test_read_revision_missing_field(tmp_path):
    (tmp_path / "x.yaml").write_text("schema_version: 1\nnotes: hi\n")
    with pytest.raises(KeyError):
        cas.read_revision(tmp_path / "x.yaml")


def test_commit_writes_and_returns_new_revision(v5_root):
    p = _ledger(v5_root)
    new = _bump(p.read_text(), 4).replace("assumptions: {}", 'assumptions: {A-001: {stmt: x}}')
    r = cas.commit(p, new, expected_revision=3)
    assert r["revision"] == 4
    assert "hash" in r and r["hash"] == cas.content_hash(new)
    data = yaml.safe_load(p.read_text())
    assert data["revision"] == 4
    assert data["assumptions"]["A-001"]["stmt"] == "x"


def test_commit_conflict_does_not_write(v5_root):
    p = _ledger(v5_root)
    data = yaml.safe_load(p.read_text())
    data["revision"] = 4  # another writer bumped first
    p.write_text(yaml.safe_dump(data))
    with pytest.raises(cas.CasConflict):
        cas.commit(p, _bump(p.read_text(), 5), expected_revision=3)
    assert yaml.safe_load(p.read_text())["revision"] == 4  # unchanged


def test_commit_rejects_missing_bump(v5_root):
    p = _ledger(v5_root)
    with pytest.raises(cas.BadRevisionBump):
        cas.commit(p, p.read_text(), expected_revision=3)  # revision still 3, not 4


def test_commit_creates_backup_of_old_content(v5_root):
    p = _ledger(v5_root)
    cas.commit(p, _bump(p.read_text(), 4), expected_revision=3)
    backups = list((v5_root / "_bewater").glob(".backup-ledger-*"))
    assert len(backups) == 1
    assert yaml.safe_load(backups[0].read_text())["revision"] == 3


def test_commit_keeps_only_n_backups(v5_root):
    p = _ledger(v5_root)
    rev = 3
    for _ in range(7):
        cas.commit(p, _bump(p.read_text(), rev + 1), expected_revision=rev)
        rev += 1
    assert len(list((v5_root / "_bewater").glob(".backup-ledger-*"))) == 5


def test_commit_writes_new_text_verbatim(v5_root):
    p = _ledger(v5_root)
    marker = "# VERBATIM-MARKER keep-me\n"
    new = marker + _bump(p.read_text(), 4)
    cas.commit(p, new, expected_revision=3)
    assert marker in p.read_text()


def test_commit_leaves_no_temp_file(v5_root):
    p = _ledger(v5_root)
    cas.commit(p, _bump(p.read_text(), 4), expected_revision=3)
    assert [x for x in (v5_root / "_bewater").iterdir() if x.name.startswith(".tmp-")] == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bwkit_cas.py -v`
Expected: FAIL — `AttributeError: module 'bwkit.cas' has no attribute 'commit'` (and the old `cas_update` tests are gone).

- [ ] **Step 3: Write minimal implementation**

Append to `src/bwkit/cas.py`:

```python
_REVISION_RE = re.compile(r"(?m)^revision:\s*(\d+)\s*$")


def read_revision(path) -> int:
    text = Path(path).read_text()  # FileNotFoundError if absent
    m = _REVISION_RE.search(text)
    if not m:
        raise KeyError(f"no top-level 'revision:' field in {path}")
    return int(m.group(1))


def commit(path, new_text: str, expected_revision: int, *, keep_backups: int = 5) -> dict:
    path = Path(path)
    current = read_revision(path)  # FileNotFoundError propagates if missing
    if current != expected_revision:
        raise CasConflict(f"current revision {current} != expected {expected_revision}")
    m = _REVISION_RE.search(new_text)
    got = int(m.group(1)) if m else None
    if got != expected_revision + 1:
        raise BadRevisionBump(
            f"new_text revision must be {expected_revision + 1} (got {got})")
    _rotate_backup(path, keep_backups)
    tmp = path.with_name(f".tmp-{path.name}-{os.getpid()}")
    tmp.write_text(new_text)
    os.replace(tmp, path)  # atomic
    return {"revision": expected_revision + 1, "hash": content_hash(new_text)}


def _rotate_backup(path: Path, keep_backups: int) -> None:
    parent = path.parent
    old_text = path.read_text()
    old_rev_m = _REVISION_RE.search(old_text)
    old_rev = old_rev_m.group(1) if old_rev_m else "x"
    backup = parent / f"{BACKUP_PREFIX}{path.stem}-{old_rev}-{time.time_ns()}"
    backup.write_text(old_text)
    backups = sorted(parent.glob(f"{BACKUP_PREFIX}{path.stem}-*"))
    for extra in backups[:-keep_backups]:
        extra.unlink()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_bwkit_cas.py -v`
Expected: PASS (all 9).

- [ ] **Step 5: Commit**

```bash
git add src/bwkit/cas.py tests/test_bwkit_cas.py
git commit -m "feat(bwkit): text-level revision CAS (commit/read_revision); drop cas_update"
```

---

## Task 4: bwkit CLI (`__main__.py` + `cli.py`)

**Files:**
- Create: `src/bwkit/cli.py`
- Create: `src/bwkit/__main__.py`
- Test: `tests/test_bwkit_cli.py`

**Interfaces:**
- Consumes: `cas.*` (Tasks 2–3)
- Produces: `cli.main(argv=None, *, _stdin=None) -> int`; subcommands `lock acquire|release|status`, `cas show`, `cas commit`. `__main__.py` delegates to `cli.main` (mirrors `src/bw/__main__.py`).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_bwkit_cli.py
"""CLI wiring for bwkit — drive main([...]) directly (spec §12.5 CLI surface)."""
from __future__ import annotations

import io
import re
from pathlib import Path

import pytest
import yaml

from bwkit import cas, cli


@pytest.fixture
def v5_root(tmp_path: Path) -> Path:
    (tmp_path / "_bewater").mkdir()
    (tmp_path / "_bewater" / "ledger.yaml").write_text(yaml.safe_dump(
        {"schema_version": 1, "revision": 3, "next_id": 4, "assumptions": {}}))
    return tmp_path


def test_help_lists_subcommands(capsys):
    with pytest.raises(SystemExit) as exc:
        cli.main(["--help"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    for token in ["lock", "cas"]:
        assert token in out


def test_lock_acquire_then_status(v5_root, capsys):
    assert cli.main(["lock", "acquire", str(v5_root), "--owner", "s1"]) == 0
    assert cli.main(["lock", "status", str(v5_root)]) == 0
    assert "s1" in capsys.readouterr().out


def test_lock_release(v5_root):
    cli.main(["lock", "acquire", str(v5_root), "--owner", "s1"])
    assert cli.main(["lock", "release", str(v5_root), "--owner", "s1"]) == 0
    assert cas.lock_status(v5_root) is None


def test_cas_show_prints_revision_and_hash(v5_root, capsys):
    p = v5_root / "_bewater" / "ledger.yaml"
    assert cli.main(["cas", "show", str(p)]) == 0
    out = capsys.readouterr().out
    assert "revision=3" in out
    assert "hash=" in out


def test_cas_commit_reads_new_text_from_stdin(v5_root):
    p = v5_root / "_bewater" / "ledger.yaml"
    new = re.sub(r"(?m)^revision:\s*\d+", "revision: 4", p.read_text(), count=1)
    rc = cli.main(["cas", "commit", str(p), "--expected", "3"], _stdin=io.StringIO(new))
    assert rc == 0
    assert yaml.safe_load(p.read_text())["revision"] == 4


def test_cas_commit_conflict_returns_nonzero(v5_root, capsys):
    p = v5_root / "_bewater" / "ledger.yaml"
    # bump underlying file so expected=3 is stale
    data = yaml.safe_load(p.read_text()); data["revision"] = 4
    p.write_text(yaml.safe_dump(data))
    new = re.sub(r"(?m)^revision:\s*\d+", "revision: 5", p.read_text(), count=1)
    rc = cli.main(["cas", "commit", str(p), "--expected", "3"], _stdin=io.StringIO(new))
    assert rc == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bwkit_cli.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'bwkit.cli'`.

- [ ] **Step 3: Write minimal implementation**

```python
# src/bwkit/cli.py
"""argparse glue over bwkit.cas. Thin router; no business logic."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import cas


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="bwkit", description="bewater narrow helpers (lock, revision CAS)")
    sub = p.add_subparsers(dest="cmd", required=True)

    lock = sub.add_parser("lock", help="single-writer lock")
    lsub = lock.add_subparsers(dest="lock_cmd", required=True)
    a = lsub.add_parser("acquire")
    a.add_argument("root")
    a.add_argument("--owner", required=True)
    a.add_argument("--ttl", type=int, default=3600)
    rel = lsub.add_parser("release")
    rel.add_argument("root")
    rel.add_argument("--owner", required=True)
    st = lsub.add_parser("status")
    st.add_argument("root")

    c = sub.add_parser("cas", help="text-level revision CAS")
    csub = c.add_subparsers(dest="cas_cmd", required=True)
    show = csub.add_parser("show")
    show.add_argument("path")
    com = csub.add_parser("commit")
    com.add_argument("path")
    com.add_argument("--expected", type=int, required=True)
    return p


def main(argv=None, *, _stdin=None) -> int:
    args = build_parser().parse_args(argv)
    stdin = _stdin if _stdin is not None else sys.stdin

    if args.cmd == "lock":
        root = Path(args.root)
        if args.lock_cmd == "acquire":
            info = cas.acquire_lock(root, args.owner, args.ttl)
            print(f"acquired owner={info['owner']} pid={info['pid']}")
            return 0
        if args.lock_cmd == "release":
            cas.release_lock(root, args.owner)
            print("released")
            return 0
        if args.lock_cmd == "status":
            st = cas.lock_status(root)
            print("unlocked" if st is None else f"owner={st['owner']} pid={st['pid']}")
            return 0

    if args.cmd == "cas":
        path = Path(args.path)
        if args.cas_cmd == "show":
            rev = cas.read_revision(path)
            print(f"revision={rev} hash={cas.content_hash(path.read_text())}")
            return 0
        if args.cas_cmd == "commit":
            new_text = stdin.read()
            try:
                r = cas.commit(path, new_text, args.expected)
            except (cas.CasConflict, cas.BadRevisionBump) as e:
                print(f"error: {e}", file=sys.stderr)
                return 1
            print(f"committed revision={r['revision']} hash={r['hash']}")
            return 0
    return 2
```

```python
# src/bwkit/__main__.py
import sys  # pragma: no cover

from bwkit.cli import main  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())  # pragma: no cover
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_bwkit_cli.py -v`
Expected: PASS (all 6).

- [ ] **Step 5: Commit**

```bash
git add src/bwkit/cli.py src/bwkit/__main__.py tests/test_bwkit_cli.py
git commit -m "feat(bwkit): CLI surface (lock, cas show/commit from stdin)"
```

---

## Task 5: bwkit coverage gate + end-to-end smoke

**Files:**
- Test: `tests/test_bwkit_smoke.py`
- Verify only (no production code).

**Interfaces:**
- Produces: `pytest --cov=bw --cov=bwkit --cov-fail-under=80` green; `python -m bwkit` works end-to-end on a fresh temp project.

- [ ] **Step 1: Write the integration test**

```python
# tests/test_bwkit_smoke.py
"""End-to-end subprocess smoke for bwkit (spec §12.5 acceptance)."""
from __future__ import annotations

import re
import subprocess
import sys


def test_python_m_bwkit_help():
    r = subprocess.run([sys.executable, "-m", "bwkit", "--help"], capture_output=True, text=True)
    assert r.returncode == 0
    assert "lock" in r.stdout and "cas" in r.stdout


def test_end_to_end_lock_and_commit(tmp_path):
    bw = tmp_path / "_bewater"
    bw.mkdir()
    (bw / "ledger.yaml").write_text("schema_version: 1\nrevision: 3\nnext_id: 4\nassumptions: {}\n")
    p = bw / "ledger.yaml"

    acquire = subprocess.run(
        [sys.executable, "-m", "bwkit", "lock", "acquire", str(tmp_path), "--owner", "smoke"],
        capture_output=True, text=True)
    assert acquire.returncode == 0, acquire.stderr

    new = re.sub(r"(?m)^revision:\s*\d+", "revision: 4", p.read_text(), count=1)
    commit = subprocess.run(
        [sys.executable, "-m", "bwkit", "cas", "commit", str(p), "--expected", "3"],
        input=new, text=True, capture_output=True)
    assert commit.returncode == 0, commit.stderr
    assert "revision: 4" in p.read_text()
```

- [ ] **Step 2: Run the smoke test**

Run: `pytest tests/test_bwkit_smoke.py -v`
Expected: PASS (implementation from Tasks 2–4 already satisfies it).

- [ ] **Step 3: Run the coverage gate**

Run: `pytest --cov=bw --cov=bwkit --cov-report=term-missing`
Expected: bwkit ≥80%. If any line is uncovered, **add a test that exercises it** (do not delete or weaken tests). Common gaps to cover: the stale-via-ttl branch in `_is_stale` (add a test that preempts a lock whose `acquired_at` is far in the past), and the `running but past ttl` path.

Example ttl-preempt test to add to `tests/test_bwkit_lock.py` if coverage is short:

```python
def test_stale_past_ttl_is_preemptable(v5_root, monkeypatch):
    cas.acquire_lock(v5_root, owner="old")
    # force acquired_at well beyond ttl without faking pid death
    p = cas.lock_path(v5_root)
    data = yaml.safe_load(p.read_text())
    data["acquired_at"] = -1e9  # distant past
    p.write_text(yaml.safe_dump(data))
    assert cas.acquire_lock(v5_root, owner="s2", ttl_seconds=60)["owner"] == "s2"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest --cov=bw --cov=bwkit --cov-fail-under=80 -q`
Expected: PASS, bwkit ≥80%.

- [ ] **Step 5: Commit**

```bash
git add tests/test_bwkit_smoke.py tests/test_bwkit_lock.py
git commit -m "test(bwkit): end-to-end smoke + 80% coverage gate"
```

---

## Task 6: `_bw-shared/` authoritative reference schemas

**Files:**
- Create: `.claude/skills/_bw-shared/ledger-schema.md`
- Create: `.claude/skills/_bw-shared/gate-criteria.md`
- Create: `.claude/skills/_bw-shared/glossary.md`
- Test: `tests/test_shared_schemas.py`

**Interfaces:**
- Produces: three shared references (§2.3), each with `contract_id` / `contract_version` / `source_sections` frontmatter. `ledger-schema.md` encodes §5.1–5.6; `gate-criteria.md` encodes §6.3 G1 (G2 readiness marked "Phase 2"); `glossary.md` defines core terms. Phase 1 skills cite or copy these per contract.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_shared_schemas.py
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SHARED = REPO / ".claude" / "skills" / "_bw-shared"


def _frontmatter(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


@pytest.mark.parametrize("name", ["ledger-schema.md", "gate-criteria.md", "glossary.md"])
def test_shared_reference_exists_with_contract_frontmatter(name):
    text = (SHARED / name).read_text()
    fm = _frontmatter(text)
    assert "contract_id:" in fm
    assert "contract_version:" in fm
    assert "source_sections:" in fm


def test_ledger_schema_covers_core_fields_and_enums():
    text = (SHARED / "ledger-schema.md").read_text()
    for token in ["record_revision", "supersedes_ref", "BR-001", "A-001",
                  "achilles", "L1", "L4", "schema_version"]:
        assert token in text, f"ledger-schema missing {token}"


def test_gate_criteria_covers_g1_readiness():
    text = (SHARED / "gate-criteria.md").read_text()
    for token in ["G1", "directional", "strategy", "opportunity", "Achilles", "Money", "Magic"]:
        assert token in text, f"gate-criteria missing {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_shared_schemas.py -v`
Expected: FAIL — `.claude/skills/_bw-shared/` does not exist.

- [ ] **Step 3: Write the reference files**

Create `.claude/skills/_bw-shared/ledger-schema.md`:

```markdown
---
contract_id: bw-ledger-schema
contract_version: 1
source_sections: spec §5.1–5.6
---

# BeWater State Schema (authoritative)

Distilled from spec §5. Consuming skills keep a copy (byte-identical within one
skill) or cite this shared contract (§2.3).

## ID prefixes (stable, never reused)
BR- branch · A- assumption · ART- artifact · EXP- experiment · D- decision ·
B- baseline · BT- backtrack · ACT- action · C- condition · E- evidence.

## Typed references
artifact:ART-001@3 · assumption:A-001@4 · experiment:EXP-001@2 ·
evidence:E-001@1 · gate:D-001 · baseline:B-001. The `@n` pins a mutable
record revision; gate/baseline refs are immutable (no `@n`).

## supersedes_ref (two semantics)
(a) self-revision — new revision of the same entity → its predecessor
(`artifact:ART-001@3` supersedes `artifact:ART-001@2`). (b) cross-entity
replacement — a new entity replaces a different entity's revision
(branch-local `assumption:A-002` → `assumption:A-001@4`). Disambiguate by
comparing own ID/type vs the referenced ID/type. `supersedes_handoff_ref`
(action_plan) is the one named exception → the gate decision whose handoff a
Go replaces.

## Versioning models
In-place bump (one file): assumptions (`record_revision`), conditions
(`record_revision`), config/ledger/conditions envelopes (`revision`).
Append-only (new file per revision): artifacts (`ART-001-r3-…`), evidence.
Cross-file versioned, in-file immutable: baselines (`B-002` supersedes
`B-001`), gate decisions (new attempt → new `D-…`).

## config.yaml (selected)
schema_version, revision, next_ids{branch,artifact,experiment,decision,
baseline,backtrack,action,evidence}, active_branch, active_execution_handoff,
branches{BR-nn: status,current_stage,parent_ids,merged_into,gate_due_at,
inherited/excluded_assumption_refs, inherited_condition_ids, needs_rebase_refs,
active_baselines{G1,G2}}.

## ledger.yaml (assumption record)
record_revision, statement, branch_id, layer{root,strategy,opportunity,
concept,feature}, category{consumer,commercial,technical,distribution,
regulatory}, side{money,magic,both}, impact, uncertainty, evidence_level{L1–L6},
validation_status{untested,testing,supported,falsified,inconclusive},
status{active,killed,merged}, evidence_refs[], derived_from[], supersedes_ref,
risk_history[], l4_obligation_status, history[]. `is_achilles_heel` =
impact=high AND uncertainty=high (derived). An Achilles Heel raises a durable
L4 obligation that survives lowering impact/uncertainty.

## conditions.yaml (condition record)
record_revision, origin_decision_id, branch_id, statement, owner, due_at,
status{open,satisfied,waived,cancelled,superseded}, required_evidence,
evidence_refs[], resolution_ref, resolved_at/by, waiver_rationale,
close_reason, close_authority. Edits bump in-place `record_revision` under a
stable C-NNN ID (never a new ID). waived hard G2 evidence still does not
qualify for Go.

## artifact frontmatter (selected)
schema_version, artifact_id, revision, supersedes_ref, kind, stage, branch_id,
document_status{draft,final,superseded}, validation_status{unvalidated,
in-review,validated,invalidated}, dual_sided{magic,money,tension,balance_choice},
derived_from[], signoffs[{person,role,scope,artifact_revision,signed_at}],
stale_reason. final + non-empty body is document-presence only, never
readiness.

## evidence wrapper
evidence_id, revision, supersedes_ref, effect_on_prior{supplements,supersedes,
invalidates}, validity{active,invalidated}, correction_reason, source_type,
captured_at, content_sha256, source_path_or_user_provided_url. Corrections
create the next immutable revision and trigger dependent stale/invalidation.
```

Create `.claude/skills/_bw-shared/gate-criteria.md`:

```markdown
---
contract_id: bw-gate-criteria
contract_version: 1
source_sections: spec §5.4, §6.3
---

# Gate Readiness Criteria (authoritative)

A gate presents evidence and records a human decision; it never chooses an
exit (§6.2). final + non-empty body proves only that a document exists.

## G1 — Strategy Gate (after Define)
- insights carry current-revision human F/P/E/T signoff;
- 2–5 directional hypotheses closed and dual-sided (By / We can / Resulting in);
- strategy statement selected, locked, and choice-cutting;
- 2–4 opportunity areas, non-overlapping and generative;
- assumption ledger has an initial inventory and identifies the Achilles Heel quadrant;
- Money + Magic initial judgment explicitly made.

G1 tolerates high uncertainty: it requires a coherent direction and visible
risks, not L4 validation.

## Kind-specific readiness (§5.4)
- insight: F/P/E/T decisions signed at current revision;
- directional hypothesis: complete By/We can/Resulting in + Money+Magic;
- strategy: human-selected, locked, passes the "knife, not summary" test;
- opportunity portfolio: 2–4 non-overlapping, each can spawn concepts;
- (concept portfolio, solution, investment narrative → Phase 2 gate-criteria addendum).

## G2 — Concept Gate (after Shape) — Phase 2
G2 criteria (1–2 validated solutions; every Achilles Heel / open L4 obligation
resolved by L4+ behavioral evidence; sourced financial assumptions; complete
dual-sided six-part narrative; exact input revisions ready to baseline) are
authored in Phase 2. The non-negotiable rule, fixed now: L1–L3 self-report
plus human insistence on Go never yields Go, a baseline, or an execution
handoff (§6.3, §6.7).
```

Create `.claude/skills/_bw-shared/glossary.md`:

```markdown
---
contract_id: bw-glossary
contract_version: 1
source_sections: spec §0–§8
---

# BeWater Glossary (authoritative)

- **Decision phase**: Immersion → Discover → Define → G1 → Ideate → Shape → G2 → execution handoff.
- **G1 / Strategy Gate**: convergence gate after Define; product-owner authority.
- **G2 / Concept Gate**: investment gate after Shape; investment-decision authority.
- **Money + Magic**: dual-sided reasoning (commercial leverage vs consumer value).
- **Assumption ledger**: revisioned record of assumptions with evidence levels.
- **Evidence level (L1–L6)**: must point to evidence, not be asserted. L4+ = behavioral.
- **Achilles Heel**: assumption with impact=high AND uncertainty=high → durable L4 obligation.
- **Baseline**: immutable snapshot created by a Go; governs loop size (touching it = large loop).
- **Execution handoff**: derived output of a G2 Go; one active per project.
- **Conditional Go**: bounded gap with conditions; closeout required before the next gate.
- **Five exits**: Go, Conditional Go, Recycle, Pivot, Kill (§6.4).
- **Direct-write protocol**: §5.7 — announce, single-writer lock, read, backup, modify, CAS check, bump, diff, verify.
- **bwkit**: narrow stdlib-only helper (lock + revision CAS); no gate authority (§12).
- **Contract reference**: a shared file under `_bw-shared/` with contract_id/version (§2.3).
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_shared_schemas.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/_bw-shared/ tests/test_shared_schemas.py
git commit -m "docs(phase0): _bw-shared authoritative schemas (ledger, gate-criteria, glossary)"
```

---

## Task 7: eval harness scaffold

**Files:**
- Create: `evals/__init__.py`, `evals/_harness/__init__.py`
- Create: `evals/_harness/manifest_schema.json`
- Create: `evals/_harness/loader.py`
- Test: `tests/test_eval_harness.py`

**Interfaces:**
- Produces: a scenario manifest JSON schema (required fields per §11.1) and `load_manifest(path)` that raises `ManifestError` on missing required fields. Establishes the `evals/{skill}/{scenarios,red,green}/` convention for Phase 1.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_eval_harness.py
from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def test_manifest_schema_has_required_fields():
    schema = json.loads((REPO / "evals" / "_harness" / "manifest_schema.json").read_text())
    required = set(schema["required"])
    for field in ["scenario_id", "target_skill", "prompt",
                  "required_assertions", "forbidden_behaviors", "repetition_count"]:
        assert field in required


def test_loader_validates_a_good_manifest(tmp_path):
    from evals._harness.loader import load_manifest  # noqa: F401  (import works)

    m = tmp_path / "s.yaml"
    m.write_text(
        "scenario_id: S-1\ntarget_skill: bw-start\nprompt: hi\n"
        "required_assertions: [a]\nforbidden_behaviors: []\nrepetition_count: 3\n")
    data = load_manifest(m)
    assert data["scenario_id"] == "S-1"


def test_loader_rejects_missing_repetition(tmp_path):
    from evals._harness.loader import load_manifest, ManifestError

    m = tmp_path / "s.yaml"
    m.write_text(
        "scenario_id: S-1\ntarget_skill: bw-start\nprompt: hi\n"
        "required_assertions: [a]\nforbidden_behaviors: []\n")
    with pytest.raises(ManifestError):
        load_manifest(m)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_eval_harness.py -v`
Expected: FAIL — `evals/` does not exist.

- [ ] **Step 3: Write minimal implementation**

`evals/__init__.py` and `evals/_harness/__init__.py`: empty files (package markers).

`evals/_harness/manifest_schema.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "bewater eval scenario manifest",
  "type": "object",
  "required": ["scenario_id", "target_skill", "prompt", "required_assertions", "forbidden_behaviors", "repetition_count"],
  "properties": {
    "scenario_id": {"type": "string"},
    "target_skill": {"type": "string"},
    "prompt": {"type": "string"},
    "fixture_refs": {"type": "array", "items": {"type": "string"}},
    "installed_dependency_skills": {"type": "array", "items": {"type": "string"}},
    "required_assertions": {"type": "array", "items": {"type": "string"}, "minItems": 1},
    "forbidden_behaviors": {"type": "array", "items": {"type": "string"}},
    "repetition_count": {"type": "integer", "minimum": 1}
  }
}
```

`evals/_harness/loader.py`:

```python
"""Eval scenario manifest loader + validator. Authoring utility (not shipped,
not part of bwkit). Full jsonschema validation is deferred (no jsonschema dep);
we enforce required keys, which is enough for the scaffold."""
from __future__ import annotations

import json
from pathlib import Path

import yaml


class ManifestError(Exception):
    """A scenario manifest is missing a required field or is malformed."""


_SCHEMA = json.loads((Path(__file__).parent / "manifest_schema.json").read_text())


def load_manifest(path):
    data = yaml.safe_load(Path(path).read_text())
    if not isinstance(data, dict):
        raise ManifestError("manifest must be a mapping at the top level")
    for key in _SCHEMA["required"]:
        if key not in data:
            raise ManifestError(f"missing required field: {key}")
    return data
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_eval_harness.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add evals/ tests/test_eval_harness.py
git commit -m "feat(phase0): eval harness scaffold (manifest schema + loader)"
```

---

## Task 8: installer test harness scaffold

**Files:**
- Modify: `tests/conftest.py` (add `tmp_home`, `tmp_dest` fixtures)
- Create: `tests/installer_helpers.py`
- Test: `tests/test_installer_harness.py`

**Interfaces:**
- Produces: pytest fixtures `tmp_home` (isolated `HOME`, monkeypatched) and `tmp_dest` (writable skills destination), plus helpers `write_managed_marker(target, *, version)` / `has_managed_marker(target)`. These are the fixtures `install.sh` tests will use in Phase 1 (§9). `install.sh` itself is not built here.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_installer_harness.py
from __future__ import annotations

from installer_helpers import has_managed_marker, write_managed_marker


def test_tmp_home_is_isolated(tmp_home):
    assert tmp_home.is_dir()
    # a fresh HOME has no installed bewater skills
    assert not (tmp_home / ".claude" / "skills" / "bw-start").exists()


def test_tmp_dest_is_writable(tmp_dest):
    (tmp_dest / "probe").write_text("x")
    assert (tmp_dest / "probe").read_text() == "x"


def test_managed_marker_roundtrip(tmp_dest):
    target = tmp_dest / "bw-start"
    target.mkdir()
    write_managed_marker(target, version="0.1.0")
    assert has_managed_marker(target) is True

    stranger = tmp_dest / "stranger"
    stranger.mkdir()
    assert has_managed_marker(stranger) is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_installer_harness.py -v`
Expected: FAIL — `tmp_home`/`tmp_dest` fixtures undefined; `installer_helpers` not importable.

- [ ] **Step 3: Write minimal implementation**

Append to `tests/conftest.py` (below the existing `tmp_project` fixture):

```python
@pytest.fixture
def tmp_home(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    return home


@pytest.fixture
def tmp_dest(tmp_path):
    dest = tmp_path / "dest"
    dest.mkdir()
    return dest
```

Create `tests/installer_helpers.py`:

```python
"""Shared helpers for installer tests (Phase 1 install.sh). Not shipped."""
from __future__ import annotations

import json
from pathlib import Path

MARKER = ".bewater-managed"


def write_managed_marker(target, *, version, source="bewater"):
    (Path(target) / MARKER).write_text(
        json.dumps({"managed_by": source, "version": version}))


def has_managed_marker(target) -> bool:
    return (Path(target) / MARKER).exists()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_installer_harness.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/conftest.py tests/installer_helpers.py tests/test_installer_harness.py
git commit -m "test(phase0): installer test harness scaffold (tmp HOME/dest + managed-marker helpers)"
```

---

## Self-Review

**1. Spec coverage (Plan 1 scope = §10.2 Phase 0 + §12.5 bwkit/cas):**
- §10.2 SUPERSEDED banner → Task 1 ✓
- §10.2 reference schemas under `_bw-shared/` → Task 6 ✓
- §10.2 eval harness → Task 7 ✓
- §10.2 installer test harness → Task 8 ✓
- §10.2 treat `src/bw` as oracle / do not delete → Global Constraints ✓
- §12.5 single-writer lock (acquire/release/status/stale-preempt/wrong-owner/noop) → Task 2 ✓
- §12.5 revision CAS (read / missing-file / commit-with-bump / conflict-no-write / bad-bump / backup-old-content / keep-N / verbatim / no-temp-residue) → Task 3 ✓
- §12.5 CLI surface (lock acquire/release/status, cas show, cas commit from stdin) → Task 4 ✓
- §12.5 Acceptance test matrix → Tasks 2/3 ✓
- §12.5 coverage ≥80% → Task 5 ✓
- §12.2 helper state root `_bewater/`, no gate authority → Global Constraints + Tasks 2/3 ✓
- §2.3 contract_id/version on shared references → Task 6 frontmatter ✓
- pyproject coverage source includes bwkit → Task 1 ✓

**Deferred (out of Plan 1 scope, by design):** `install.sh` and the bwkit deploy-to-`_bw-shared/bwkit/` step (Phase 1, §9/§10.3 — no skills exist yet to install or invoke bwkit); `scripts/verify` (Phase 1, §11.3 — it verifies all 19 skills exist); full `jsonschema` validation in the eval loader (scaffold enforces required keys only, no new dep).

**2. Placeholder scan:** none. Every step carries real test code or a concrete implementation with named functions matching the Interfaces blocks.

**3. Type consistency:**
- `cas.content_hash(body: str) -> str` — defined T2, used T3 (`commit`) and T4 (`cas show`) ✓
- `cas.acquire_lock(root, owner, ttl_seconds=3600) -> dict` — defined T2, used T4 (CLI) ✓
- `cas.release_lock(root, owner) -> None` / `cas.lock_status(root) -> dict|None` / `cas.lock_path(root) -> Path` — T2, used T4 ✓
- `cas.read_revision(path) -> int` — defined T3, used T4 (`cas show`) ✓
- `cas.commit(path, new_text, expected_revision, *, keep_backups=5) -> {"revision","hash"}` — defined T3, used T4 (`cas commit`) ✓
- `cas.LockError` / `cas.CasConflict` / `cas.BadRevisionBump` — defined T2, raised T2/T3, caught T4 ✓
- `cli.main(argv=None, *, _stdin=None) -> int` — defined T4, used by `__main__.py` and T5 smoke ✓
- `load_manifest(path)` / `ManifestError` — defined T7, used T7 ✓
- `write_managed_marker(target, *, version)` / `has_managed_marker(target)` — defined T8, used T8 ✓

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-07-29-bw-phase0-bwkit-cas.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch with checkpoints.

**Which approach?** (Plan 2 — Phase 1 G1 skills — is written once Plan 1 lands and bwkit/cas is verified.)
