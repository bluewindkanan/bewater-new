# BeWater Phase 2a — Ideate + Lineage/Integrity Helpers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Open Phase 2 (spec §10.4) with the Ideate stage (bw-ideate router + bw-concept-card capability) and the two remaining stdlib-only `bwkit` helpers that Phase 2b's baseline/backtrack flows depend on: an artifact revision-chain **integrity check** (§5.4) and a **lineage/impact scanner** (§8.2).

**Architecture:** Two new `bwkit` modules — `integrity.py` and `lineage.py` — each schema-agnostic and YAML-agnostic: the caller (a skill or `scripts/verify`) parses business files and hands bwkit a JSON model (records / edges), and bwkit enforces the deterministic graph algorithm (§12.5, same split as `cas`/`applier`). `integrity.check_artifacts` validates per-id revision chains (exactly one head, no cycle, no duplicate revision, no missing predecessor); `lineage.transitive_dependents` computes reverse-reachability over `dependent→dependency` edges so a falsified upstream surfaces all transitive downstream impact. The two skills reuse the Plan 2a self-contained pattern (`tests/skill_helpers.py` + eval manifests + structural pytest). Behavioral LLM evals stay deferred to the phase gate.

**Tech Stack:** Python ≥3.11 (stdlib-only `bwkit`: `json`, `collections`, `pathlib`). pytest + pytest-cov. Skills are markdown + `name`/`description`-only frontmatter. No new runtime dependencies.

## Global Constraints

- **Spec authority:** `docs/superpowers/specs/2026-07-27-bewater-decision-phase-skills-design.md` v5.1 + H1a. §5.4 artifact contract + integrity; §8.2 lineage; §9.7 concept cards; §10.4 Phase 2; §11.3 verify; §12.3 helper set.
- **Plan 2a/2b (Phase 1) is the foundation:** `tests/skill_helpers.py`, `install.sh`, `scripts/verify.py`, `_bw-shared/` contracts, and the 12 landed skills are reused. `bwkit` already has `cas`, `cli`, `applier`.
- **`bwkit` stays stdlib-only + YAML-agnostic:** `integrity.py` and `lineage.py` import only stdlib (`json`, `collections`, `pathlib`); they never import `yaml` or `bw.*`. They operate on caller-built JSON models, not business files (§12.5).
- **Helpers = mechanism, not authority:** they validate/scan; they never choose a gate exit, never mutate state, never touch a decision record (§12.2). `integrity` is read-only; `lineage` is read-only.
- **SKILL.md frontmatter is `name` + `description` only**, description starts with `Use when` (§4).
- **Human convergence is binding:** bw-concept-card presents concept candidates and stops before the human's convergence choices (healthy anxiety, altitude, kill/proceed) (§4, §8.2).
- **Deterministic tests** are structural/graph-algorithmic for the helpers and structural for the skills; fresh-context LLM GREEN runs remain the deferred phase gate.
- **Legacy untouched:** do not modify or delete `src/bw/` or its tests.
- **TDD:** failing test first, watch fail, minimal implementation, watch pass, commit. Commit only the files each task touches.
- **Commit convention:** `feat(bwkit): …`, `feat(bw): …`, `test(bw): …`.

---

## File Structure

```
bewater-new/
├── src/bwkit/
│   ├── integrity.py                      # CREATE: check_artifacts (§5.4, §12.3)
│   ├── lineage.py                        # CREATE: transitive_dependents (§8.2, §12.3)
│   └── cli.py                            # MODIFY: add `check integrity` + `scan impact`
├── .claude/skills/
│   ├── bw-ideate/{SKILL.md, references/stage.md, .bewater-managed}
│   └── bw-concept-card/{SKILL.md, references/concept-card-template.md, .bewater-managed}
├── evals/bw-ideate/{scenarios/*.yaml, red/*.yaml}        # CREATE
├── evals/bw-concept-card/{scenarios/*.yaml, red/*.yaml}  # CREATE
└── tests/
    ├── test_bwkit_integrity.py           # CREATE (T1)
    ├── test_bwkit_lineage.py             # CREATE (T2)
    ├── test_skill_bw_ideate.py           # CREATE (T3)
    └── test_skill_bw_concept_card.py     # CREATE (T4)
```

`install.sh` and `scripts/verify.py` need no changes — they discover `bw-*` dynamically (after 2a: 14 skills).

---

## Task 1: bwkit integrity check (`src/bwkit/integrity.py`)

**Files:**
- Create: `src/bwkit/integrity.py`
- Modify: `src/bwkit/cli.py` (add `check integrity`)
- Test: `tests/test_bwkit_integrity.py`

**Interfaces:**
- Produces (Phase 2b verify + the gate consume these):
  - `integrity.check_artifacts(records: list[dict]) -> dict` — `{ok: bool, errors: list[str], heads: dict[str,int]}`.
  - Record shape (caller-parsed from artifact frontmatter, §5.4): `{"file": str, "id": str (e.g. "ART-001"), "revision": int, "supersedes": {"id": str, "revision": int} | None}`. `supersedes` is the parsed self-revision predecessor (e.g. ART-001@3 supersedes ART-001@2 → `{"id":"ART-001","revision":2}`); cross-entity supersedes (different id) are ignored by this per-id check.
  - CLI `bwkit check integrity`: reads a JSON `{"records": [...]}` from stdin, prints the result JSON, exit 0 if `ok` else 1.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_bwkit_integrity.py
"""TDD for bwkit.integrity — artifact revision-chain validation (spec §5.4, §12.3).
Schema-agnostic: operates on caller-parsed {id, revision, supersedes} records."""
from __future__ import annotations

import io
import json

from bwkit import cli, integrity


def _rec(file, id, revision, supersedes=None):
    return {"file": file, "id": id, "revision": revision, "supersedes": supersedes}


def test_single_clean_chain_one_head():
    recs = [
        _rec("A-r1.md", "ART-1", 1, None),
        _rec("A-r2.md", "ART-1", 2, {"id": "ART-1", "revision": 1}),
        _rec("A-r3.md", "ART-1", 3, {"id": "ART-1", "revision": 2}),
    ]
    r = integrity.check_artifacts(recs)
    assert r["ok"] is True
    assert r["heads"] == {"ART-1": 3}


def test_independent_ids_each_have_a_head():
    recs = [
        _rec("A-r1.md", "ART-1", 1, None),
        _rec("B-r1.md", "ART-2", 1, None),
        _rec("B-r2.md", "ART-2", 2, {"id": "ART-2", "revision": 1}),
    ]
    r = integrity.check_artifacts(recs)
    assert r["ok"] is True
    assert r["heads"] == {"ART-1": 1, "ART-2": 2}


def test_duplicate_revision_is_corruption():
    recs = [
        _rec("A-r1.md", "ART-1", 1, None),
        _rec("A-r1-dup.md", "ART-1", 1, None),
    ]
    r = integrity.check_artifacts(recs)
    assert r["ok"] is False
    assert any("duplicate" in e for e in r["errors"])


def test_two_heads_is_corruption():
    recs = [
        _rec("A-r1.md", "ART-1", 1, None),
        _rec("A-r2a.md", "ART-1", 2, {"id": "ART-1", "revision": 1}),
        _rec("A-r2b.md", "ART-1", 3, {"id": "ART-1", "revision": 1}),  # second head off r1
    ]
    r = integrity.check_artifacts(recs)
    assert r["ok"] is False
    assert any("head" in e for e in r["errors"])


def test_missing_predecessor_is_corruption():
    recs = [
        _rec("A-r1.md", "ART-1", 1, None),
        _rec("A-r5.md", "ART-1", 5, {"id": "ART-1", "revision": 4}),  # r4 absent
    ]
    r = integrity.check_artifacts(recs)
    assert r["ok"] is False
    assert any("predecessor" in e for e in r["errors"])


def test_cycle_is_corruption():
    recs = [
        _rec("A-r1.md", "ART-1", 1, {"id": "ART-1", "revision": 2}),
        _rec("A-r2.md", "ART-1", 2, {"id": "ART-1", "revision": 1}),
    ]
    r = integrity.check_artifacts(recs)
    assert r["ok"] is False
    assert any("cycle" in e or "head" in e for e in r["errors"])


def test_cross_entity_supersedes_ignored_for_chain():
    # ART-2@1 supersedes ART-1@1 (cross-entity) — not this id's chain; ART-2 still has one head
    recs = [
        _rec("A-r1.md", "ART-1", 1, None),
        _rec("B-r1.md", "ART-2", 1, {"id": "ART-1", "revision": 1}),
    ]
    r = integrity.check_artifacts(recs)
    assert r["ok"] is True
    assert r["heads"] == {"ART-1": 1, "ART-2": 1}


def test_cli_check_integrity_reads_stdin(capsys):
    payload = json.dumps({"records": [
        _rec("A-r1.md", "ART-1", 1, None),
        _rec("A-r2.md", "ART-1", 2, {"id": "ART-1", "revision": 1})]})
    rc = cli.main(["check", "integrity"], _stdin=io.StringIO(payload))
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["ok"] is True and out["heads"]["ART-1"] == 2


def test_cli_check_integrity_returns_nonzero_on_corruption(capsys):
    payload = json.dumps({"records": [_rec("a", "ART-1", 1, None), _rec("b", "ART-1", 1, None)]})
    rc = cli.main(["check", "integrity"], _stdin=io.StringIO(payload))
    assert rc == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bwkit_integrity.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'bwkit.integrity'`.

- [ ] **Step 3: Write minimal implementation**

Create `src/bwkit/integrity.py`:

```python
"""bwkit/integrity — artifact revision-chain validation (stdlib-only, schema-agnostic).
Operates on caller-parsed records; never parses YAML. See spec §5.4, §12.3."""
from __future__ import annotations


def check_artifacts(records: list[dict]) -> dict:
    """Validate per-id revision chains (§5.4): exactly one file per (id, revision),
    exactly one head per id, no cycle, no missing predecessor.
    record = {"file", "id", "revision", "supersedes": {"id","revision"}|None}.
    Returns {"ok": bool, "errors": [str], "heads": {id: revision}}."""
    errors: list[str] = []
    seen: dict[tuple[str, int], str] = {}
    by_id: dict[str, dict[int, dict]] = {}

    for r in records:
        key = (r["id"], r["revision"])
        if key in seen:
            errors.append(f"duplicate revision {r['id']}@{r['revision']}: {seen[key]} and {r['file']}")
        seen[key] = r["file"]
        by_id.setdefault(r["id"], {})[r["revision"]] = r

    heads: dict[str, int] = {}
    for aid, revs in by_id.items():
        # revisions targeted as a same-id predecessor are not heads
        targeted: set[int] = set()
        for r in revs.values():
            s = r.get("supersedes")
            if s and s.get("id") == aid:
                targeted.add(s["revision"])
        head_candidates = [rev for rev in revs if rev not in targeted]
        if not head_candidates:
            errors.append(f"{aid}: no head (cycle or all superseded)")
        elif len(head_candidates) > 1:
            errors.append(f"{aid}: multiple heads {sorted(head_candidates)}")
        else:
            heads[aid] = head_candidates[0]

        # missing predecessor (same-id only)
        for r in revs.values():
            s = r.get("supersedes")
            if s and s.get("id") == aid and s["revision"] not in revs:
                errors.append(f"{aid}@{r['revision']}: missing predecessor {s['revision']}")

        # cycle detection: follow same-id supersedes chain from each revision
        for start in revs:
            chain: set[int] = set()
            cur = revs.get(start)
            while cur is not None:
                s = cur.get("supersedes")
                if not s or s.get("id") != aid:
                    break
                if s["revision"] in chain:
                    errors.append(f"{aid}: cycle through {s['revision']}")
                    break
                chain.add(s["revision"])
                cur = revs.get(s["revision"])

    return {"ok": not errors, "errors": errors, "heads": heads}
```

Extend `src/bwkit/cli.py`: register a `check` subcommand in `build_parser` (after the `plan` block):

```python
    ck = sub.add_parser("check", help="integrity checks")
    cksub = ck.add_subparsers(dest="check_cmd", required=True)
    cksub.add_parser("integrity")
```

And handle it in `main` (after the `args.cmd == "plan"` block, before `return 2`):

```python
    if args.cmd == "check":
        from . import integrity
        if args.check_cmd == "integrity":
            payload = json.loads(stdin.read())
            result = integrity.check_artifacts(payload.get("records", []))
            print(json.dumps(result))
            return 0 if result["ok"] else 1
```

- [ ] **Step 4: Run test to verify it passes, then the bwkit coverage gate**

Run: `pytest tests/test_bwkit_integrity.py -v` — Expected: PASS (all 9).

Run: `pytest --cov=bw --cov=bwkit --cov-fail-under=80 -q` — Expected: PASS (≥80%; if a branch is uncovered, e.g. the cycle-break-before-add path, add a test — do not weaken the gate).

- [ ] **Step 5: Commit**

```bash
git add src/bwkit/integrity.py src/bwkit/cli.py tests/test_bwkit_integrity.py
git commit -m "feat(bwkit): artifact revision-chain integrity check + CLI check integrity"
```

---

## Task 2: bwkit lineage/impact scanner (`src/bwkit/lineage.py`)

**Files:**
- Create: `src/bwkit/lineage.py`
- Modify: `src/bwkit/cli.py` (add `scan impact`)
- Test: `tests/test_bwkit_lineage.py`

**Interfaces:**
- Produces (Phase 2b backtrack consumes this):
  - `lineage.transitive_dependents(edges: list[dict], roots: list[str]) -> dict` — `{dependents: list[str], depth: dict[str,int]}`.
  - Edge shape (caller-built from `derived_from`/`evidence_refs`/baseline/branch edges, §8.2): `{"dependent": str, "dependency": str}` (dependent depends on dependency). `roots` = the changed/falsified node ids. Returns every node that transitively depends on a root (reverse-reachability), with BFS depth (backtrack-depth proxy). Roots themselves are not listed as dependents.
  - CLI `bwkit scan impact`: reads `{"edges": [...], "roots": [...]}` from stdin, prints the result JSON, exit 0.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_bwkit_lineage.py
"""TDD for bwkit.lineage — transitive impact / dependents (spec §8.2, §12.3).
Schema-agnostic: operates on caller-built dependent->dependency edges."""
from __future__ import annotations

import io
import json

from bwkit import cli, lineage


def _e(dependent, dependency):
    return {"dependent": dependent, "dependency": dependency}


def test_chain_two_hops():
    # C depends on A; A depends on B. Falsify B -> dependents A (depth1), C (depth2).
    edges = [_e("A", "B"), _e("C", "A")]
    r = lineage.transitive_dependents(edges, ["B"])
    assert r["dependents"] == ["A", "C"]
    assert r["depth"] == {"A": 1, "C": 2}


def test_diamond_converges():
    # D->B, D->C, B->A, C->A. Falsify A -> B,C (depth1), D (depth2 via either).
    edges = [_e("B", "A"), _e("C", "A"), _e("D", "B"), _e("D", "C")]
    r = lineage.transitive_dependents(edges, ["A"])
    assert r["dependents"] == ["B", "C", "D"]
    assert r["depth"]["D"] == 2


def test_no_dependents():
    edges = [_e("A", "B")]
    r = lineage.transitive_dependents(edges, ["Z"])
    assert r["dependents"] == []
    assert r["depth"] == {}


def test_cycle_does_not_loop_forever():
    # A->B, B->A. Falsify B -> A (depth1); A's dependent B is the root, not re-listed.
    edges = [_e("A", "B"), _e("B", "A")]
    r = lineage.transitive_dependents(edges, ["B"])
    assert r["dependents"] == ["A"]
    assert r["depth"] == {"A": 1}


def test_root_not_listed_as_own_dependent():
    edges = [_e("A", "B"), _e("B", "A")]
    r = lineage.transitive_dependents(edges, ["A", "B"])
    assert "A" not in r["dependents"] and "B" not in r["dependents"]


def test_multiple_roots_union():
    edges = [_e("A", "X"), _e("B", "Y")]
    r = lineage.transitive_dependents(edges, ["X", "Y"])
    assert r["dependents"] == ["A", "B"]


def test_cli_scan_impact_reads_stdin(capsys):
    payload = json.dumps({"edges": [_e("A", "B"), _e("C", "A")], "roots": ["B"]})
    rc = cli.main(["scan", "impact"], _stdin=io.StringIO(payload))
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["dependents"] == ["A", "C"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bwkit_lineage.py -v` — Expected: FAIL — `ModuleNotFoundError: No module named 'bwkit.lineage'`.

- [ ] **Step 3: Write minimal implementation**

Create `src/bwkit/lineage.py`:

```python
"""bwkit/lineage — transitive impact / dependents (stdlib-only, schema-agnostic).
Operates on caller-built dependent->dependency edges; never parses YAML. See spec
§8.2, §12.3. Resolves A3 (linear scan cost) by doing one reverse-BFS from the roots."""
from __future__ import annotations

from collections import deque


def transitive_dependents(edges: list[dict], roots: list[str]) -> dict:
    """Reverse-reachability from `roots` over dependent->dependency edges.
    edge = {"dependent": str, "dependency": str} (dependent depends on dependency).
    Returns {"dependents": sorted[node ids], "depth": {node: hops from nearest root}}.
    Roots are never listed as dependents."""
    rev: dict[str, list[str]] = {}
    for e in edges:
        rev.setdefault(e["dependency"], []).append(e["dependent"])

    root_set = set(roots)
    depth: dict[str, int] = {}
    dq: deque[tuple[str, int]] = deque((r, 0) for r in roots)
    while dq:
        node, d = dq.popleft()
        for dep in rev.get(node, []):
            if dep not in depth or d + 1 < depth[dep]:
                depth[dep] = d + 1
                dq.append((dep, d + 1))
    depth = {n: d for n, d in depth.items() if n not in root_set}  # roots aren't their own dependents
    return {"dependents": sorted(depth), "depth": depth}
```

Extend `src/bwkit/cli.py`: register a `scan` subcommand in `build_parser` (after the `check` block):

```python
    sc = sub.add_parser("scan", help="lineage / impact scan")
    scsub = sc.add_subparsers(dest="scan_cmd", required=True)
    scsub.add_parser("impact")
```

And handle it in `main` (after the `args.cmd == "check"` block, before `return 2`):

```python
    if args.cmd == "scan":
        from . import lineage
        if args.scan_cmd == "impact":
            payload = json.loads(stdin.read())
            result = lineage.transitive_dependents(payload.get("edges", []), payload.get("roots", []))
            print(json.dumps(result))
            return 0
```

- [ ] **Step 4: Run test to verify it passes, then the bwkit coverage gate**

Run: `pytest tests/test_bwkit_lineage.py -v` — Expected: PASS (all 7).

Run: `pytest --cov=bw --cov=bwkit --cov-fail-under=80 -q` — Expected: PASS (≥80%).

- [ ] **Step 5: Commit**

```bash
git add src/bwkit/lineage.py src/bwkit/cli.py tests/test_bwkit_lineage.py
git commit -m "feat(bwkit): lineage/impact transitive-dependents scanner + CLI scan impact"
```

---

## Task 3: bw-ideate (router)

**Files:**
- Create: `.claude/skills/bw-ideate/SKILL.md`, `references/stage.md`
- Create: `evals/bw-ideate/scenarios/orient.yaml`, `evals/bw-ideate/red/no-skill.yaml`
- Test: `tests/test_skill_bw_ideate.py`

**Interfaces:**
- Produces: the Ideate router. Routes to `bw-concept-card` (concept exploration, §9.7). Orient/resume/status/route; never produce artifacts.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_ideate.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_ideate_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-ideate"))
    validate_skill_evals(REPO / "evals", "bw-ideate")


def test_ideate_routes_to_concept_card():
    text = (skill_dir(REPO, "bw-ideate") / "references" / "stage.md").read_text()
    assert "bw-concept-card" in text
    assert "ideate" in text.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_ideate.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-ideate/SKILL.md`:

```markdown
---
name: bw-ideate
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Ideate.
---

# bw-ideate

A **router** for the Ideate stage (Concept module). Orient/resume/status/route; never
produce artifacts (spec §4). Ideate broadens each opportunity area into many early concepts
and narrows by standard (bewater-core §5.2.1).

## On invoke

- Confirm `current_stage` is `ideate`.
- Report Ideate status: concept count per opportunity area, convergence progress.
- Route to **bw-concept-card** (generate/complete/evaluate/converge concepts) — see
  `references/stage.md`. Present the choice and stop when ambiguous.

The concept convergence checkpoint (Ideate → Shape) is a lightweight self-check, not a gate:
≥3 concepts expressible in ≤5 words, ≥2 provoke healthy anxiety, all pass the strategy
filter. Hand the concept portfolio to Shape (`bw-shape`). Cite `../_bw-shared/glossary.md`.
```

Create `.claude/skills/bw-ideate/references/stage.md`:

```markdown
# Ideate stage (bewater-core §5.2.1, §9.7)

Ideate (Concept module) = broaden each opportunity area into 10–15 early concepts, then
narrow by standard to 2–4.

## Capability to route to

- **bw-concept-card** — generate concepts (brainstorm + "how might we"), fill the 8-field
  concept card, run the 8 criteria + scoring matrix, and converge.

## Convergence checkpoint (Ideate → Shape, no gate)

- ≥3 concepts expressible in ≤5 words;
- ≥2 concepts provoke healthy anxiety (human judgment);
- all concepts pass the strategy-statement filter.

Hand the concept portfolio (2–4) to Shape (bw-shape router). The locked strategy and
opportunity areas are the filters, carried from Define.
```

Create `evals/bw-ideate/scenarios/orient.yaml`:

```yaml
scenario_id: BWID-S1
target_skill: bw-ideate
prompt: "Status and what's next in Ideate."
fixture_refs: []
installed_dependency_skills: [bw-start]
required_assertions:
  - "reports concept-portfolio status per opportunity area"
  - "routes to bw-concept-card, authors nothing inline"
forbidden_behaviors:
  - "writes an artifact"
  - "chooses a gate exit"
repetition_count: 3
```

Create `evals/bw-ideate/red/no-skill.yaml`:

```yaml
scenario_id: BWID-R1
target_skill: bw-ideate
prompt: "What's next in Ideate?"
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-ideate absent, no Ideate routing is produced (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_ideate.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-ideate evals/bw-ideate tests/test_skill_bw_ideate.py
git commit -m "feat(bw): bw-ideate router (route to bw-concept-card)"
```

---

## Task 4: bw-concept-card (capability)

**Files:**
- Create: `.claude/skills/bw-concept-card/SKILL.md`, `references/concept-card-template.md`
- Create: `evals/bw-concept-card/scenarios/generate.yaml`, `evals/bw-concept-card/red/no-skill.yaml`
- Test: `tests/test_skill_bw_concept_card.py`

**Interfaces:**
- Produces: capability that generates/completes/evaluates/converges concept cards (§9.7). Writes `kind: concept` artifacts. Stops before human convergence (healthy anxiety, altitude, kill/proceed).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_concept_card.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_concept_card_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-concept-card"))
    validate_skill_evals(REPO / "evals", "bw-concept-card")


def test_concept_card_template_has_fields_and_criteria():
    text = (skill_dir(REPO, "bw-concept-card") / "references" / "concept-card-template.md").read_text()
    for token in ["kind: concept", "altitude", "healthy anxiety", "consumer_insight"]:
        assert token in text, f"concept-card-template missing {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_concept_card.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-concept-card/SKILL.md`:

```markdown
---
name: bw-concept-card
description: Use when the user wants to generate, complete, evaluate, or converge bewater concept cards.
---

# bw-concept-card

A **capability** for concept exploration (bewater-core §9.7). You diverge many concepts,
fill cards, run the 8 criteria + scoring matrix, and present candidates — you stop before
the human's convergence choices (healthy anxiety, altitude, kill/proceed) (spec §4, §8.2).

## Workflow

1. For each opportunity area, brainstorm 10–15 concepts ("how might we" + strong names).
2. Fill the 8-field concept card per `references/concept-card-template.md`; run the 8
   criteria and the Money∩Magic scoring matrix; cut "only interesting" ones.
3. Write concept artifacts (`_bewater-output/ART-xxx-rN-concept.md`, `kind: concept`,
   §5.4) via bwkit (§5.7). Concept revisions are append-only; the integrity check
   (`bwkit check integrity`) validates the chain.
4. Present 2–4 candidates + your scoring, name the human decision authority, and **stop**.
   Healthy anxiety, altitude, and kill/proceed are non-delegable human judgments.
```

Create `.claude/skills/bw-concept-card/references/concept-card-template.md`:

```markdown
# Concept card template (spec §5.4, §9.7)

Broaden, then narrow. Each concept is early, raw, provocative — "a sketch before the
drawing," allowed to be wrong.

## 8 fields

1. concept name (strong, owning name); 2. consumer_insight; 3. business insight;
4. What; 5. Who; 6. Why big; 7. one-line description (≤5 words); 8. sketch.

## 8 criteria + scoring

8 criteria: clear insight+tension / simple-new-unique solve / who-what-does-replaces-why-big
/ ≤5 words / specific enough / strong name / right visualization / design principle.
Scoring matrix: Money (strategy-fit, scale, speed, risk, ROI) ∩ Magic (unmet-need,
disruption, segmentation, repeatability, darwinism). Cut "only interesting."

## Human convergence (non-delegable)

- **altitude** — the concept's granularity; the right altitude is what best lets us
  pre-test it (human judgment).
- **healthy anxiety** — a good concept provokes an anxiety: is it big enough, bold enough,
  doable? Too safe → cut (human judgment).
- kill/proceed per concept — human.

## Artifact frontmatter (kind: concept)

```yaml
schema_version: 1
artifact_id: ART-001
revision: 1
supersedes_ref: null
kind: concept
stage: ideate
branch_id: BR-001
document_status: draft
validation_status: unvalidated
dual_sided:
  magic: {consumer_value_proposition: {statement: "", evidence_refs: []}}
  money: {commercial_value_proposition: {statement: "", evidence_refs: []}}
  tension: {statement: ""}
  balance_choice: ""
derived_from: []   # the opportunity area (+ strategy) it springs from
signoffs: []
stale_reason: null
```

Field semantics: `../_bw-shared/ledger-schema.md`.
```

Create `evals/bw-concept-card/scenarios/generate.yaml`:

```yaml
scenario_id: BWCC-S1
target_skill: bw-concept-card
prompt: "Generate and evaluate concepts for this opportunity area."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-ideate]
required_assertions:
  - "writes concept artifacts (kind: concept) with the 8 fields"
  - "runs the 8 criteria + scoring and cuts weak concepts"
  - "stops before the human's altitude/healthy-anxiety/kill-proceed choices"
forbidden_behaviors:
  - "records a kill/proceed before the human decides"
repetition_count: 3
```

Create `evals/bw-concept-card/red/no-skill.yaml`:

```yaml
scenario_id: BWCC-R1
target_skill: bw-concept-card
prompt: "Generate concepts for this opportunity area."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-concept-card absent, no concept artifact is written (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_concept_card.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-concept-card evals/bw-concept-card tests/test_skill_bw_concept_card.py
git commit -m "feat(bw): bw-concept-card capability (8 fields, 8 criteria, scoring)"
```

---

## Task 5: Phase 2a acceptance

**Files:** verify-only (no production code).

- [ ] **Step 1: Full suite + bwkit coverage + verify**

```bash
pytest -q                                                       # all green
pytest --cov=bw --cov=bwkit --cov-fail-under=80 -q             # bwkit (incl integrity+lineage) ≥80%
python scripts/verify.py                                        # prints "verified 14 skill(s)"
```

Expected: all green; `scripts/verify.py` reports **14 skills** (12 from Phase 1 + bw-ideate + bw-concept-card) and exits 0.

- [ ] **Step 2: Smoke the two new CLIs against a synthetic model**

```bash
echo '{"records":[{"file":"a","id":"ART-1","revision":1,"supersedes":null},
               {"file":"b","id":"ART-1","revision":2,"supersedes":{"id":"ART-1","revision":1}}]}' \
  | python -m bwkit check integrity
echo '{"edges":[{"dependent":"A","dependency":"B"},{"dependent":"C","dependency":"A"}],"roots":["B"]}' \
  | python -m bwkit scan impact
```

Expected: integrity prints `{"ok": true, ..., "heads": {"ART-1": 2}}` (exit 0); scan prints dependents `["A", "C"]` (exit 0).

- [ ] **Step 3: Commit (if any acceptance note)**

No code changes expected. If you added a note to `evals/README.md`, commit it; otherwise this task is verify-only and needs no commit.

---

## Self-Review

**1. Spec coverage (Plan 2a scope = §10.4 Ideate + §12.3 remaining helpers):**
- §10.4 bw-ideate → Task 3 ✓
- §10.4 bw-concept-card → Task 4 ✓
- §12.3 integrity check (duplicate head, cycle, two-head detection) → Task 1 ✓
- §12.3 lineage/impact scanner (transitive closure) → Task 2 ✓
- §5.4 integrity rules (exactly one head, no cycle, no duplicate revision, no missing predecessor) → Task 1 tests ✓
- §8.2 transitive dependents via all four edge kinds → Task 2 (caller builds edges; bwkit does reverse-BFS) ✓
- §12.5 schema-agnostic (caller parses; bwkit never parses YAML) → both helper designs ✓
- §11.3 verify (scans `bw-*` dynamically → 14 skills) → Task 5 ✓

**Deferred (out of Plan 2a, by design):**
- Shape stage (bw-shape, bw-experiment, bw-investment-narrative, bw-solution-shape), bw-concept-gate (G2), G2 baseline, execution handoff, backtrack flow → **Phase 2b**.
- Wiring `integrity.check_artifacts` / `lineage.transitive_dependents` into `scripts/verify.py` and the gate/backtrack skills → Phase 2b (the helpers are built + unit-tested now; consumers come with 2b).
- Fresh-context LLM GREEN runs → Phase-2 acceptance gate.

**2. Placeholder scan:** none. Every step carries real test code and a concrete implementation (graph algorithms for the helpers, methodology-accurate skill content).

**3. Type consistency:**
- `integrity.check_artifacts(records) -> {ok, errors, heads}` — defined T1, used T1 (CLI) ✓
- record shape `{file, id, revision, supersedes:{id,revision}|None}` — consistent across T1 tests + CLI ✓
- `lineage.transitive_dependents(edges, roots) -> {dependents, depth}` — defined T2, used T2 (CLI) ✓
- edge shape `{dependent, dependency}` — consistent across T2 tests + CLI ✓
- CLI subcommands `check integrity` / `scan impact` (stdin JSON → stdout JSON) — defined T1/T2 ✓
- `validate_skill` / `validate_skill_evals` / `skill_dir` — from Plan 2a, reused T3/T4 ✓
- `bwkit check integrity` is cited in `bw-concept-card` SKILL.md (Task 4) — matches Task 1 CLI ✓

**4. Scope check:** Plan 2a is one cohesive deliverable (Ideate stage + the two remaining helpers) that lays the foundation for Phase 2b's G2 closed loop. Phase 2b (Shape + G2 + baseline/handoff/backtrack) is cleanly separable.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-07-29-bw-phase2a-ideate-helpers.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch with checkpoints.

**Which approach?** (Phase 2b — Shape + bw-concept-gate (G2) + baseline + execution handoff + backtrack — follows, consuming these helpers.)
