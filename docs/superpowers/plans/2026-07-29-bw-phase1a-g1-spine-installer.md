# BeWater Phase 1a — G1 Spine + Installer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first half of the Phase 1 G1 closed loop (spec §10.3): the entry + three Strategy-stage routers + the three early capabilities that produce charters, 4C research, and insights, plus the self-contained skill installer and the authoring-time `scripts/verify` checker — so a fresh project can be bootstrapped, navigate Immersion/Discover/Define, and produce the upstream G1 artifacts, with skills installable and structurally verified.

**Architecture:** Seven Claude Code skills under `.claude/skills/bw-*/` (bw-start, bw-immersion, bw-discover, bw-define, bw-project-charter, bw-4c-research, bw-insight-craft), each self-contained with skill-local `references/` and citing the `_bw-shared/` contracts (ledger-schema, gate-criteria, glossary) created in Plan 1. State is written by the host AI under each skill's direction via the §5.7 direct-write protocol using the Plan-1 `bwkit` helper (`python -m bwkit lock …`, `python -m bwkit cas commit …`). A shared structural validator (`tests/skill_helpers.py`) is reused by every skill's pytest and by `scripts/verify`. `install.sh` deploys `bw-*` + `_bw-shared/` (refs + `src/bwkit/` → `_bw-shared/bwkit/`) with managed markers, copy/link modes, idempotency, fail-closed conflict handling, and uninstall. Behavioral (fresh-context LLM) evals are deferred to a phase-end gate (decision 2026-07-29); each task instead authors scenario manifests + deterministic structural tests now.

**Tech Stack:** Python ≥3.11 (stdlib-only `bwkit`, PyYAML only in tests/schemas/harness). Bash installer (`set -euo pipefail`). pytest + pytest-cov (existing dev deps). Skills are markdown + YAML frontmatter (Claude-native, `name` + `description` only). No new runtime dependencies.

## Global Constraints

- **Spec authority:** `docs/superpowers/specs/2026-07-27-bewater-decision-phase-skills-design.md` v5.1 + H1a. §4 = catalog/trigger contracts; §5 = state contract; §5.7 = direct-write protocol; §9 = installer; §10.3 = Phase 1 scope; §11.3 = verify.
- **v5 layout only:** skills read/write `_bewater/{config,ledger,conditions}.yaml`, `_bewater/records/`, and flat `_bewater-output/`. The legacy `src/bw/paths.py|init.py|schema.py` target the **pre-v5** layout (`_bewater/state/assumption-ledger.yaml`, `artifacts/`, `knowledge-base/`) and are **drifted** — v5 skills define their own scaffold and **never copy legacy code**; `src/bw` is a read-only oracle only (spec §10.5).
- **SKILL.md frontmatter is `name` + `description` only** (spec §4, §11.3). `description` must start with `Use when` and state triggers, not procedural steps.
- **Self-contained + MECE** (§3.10, §2.3): each skill carries its own `references/`; high-drift schemas live in `_bw-shared/` and are *cited* (`../_bw-shared/<file>.md`) rather than duplicated. Within one skill, any reference copy is byte-identical.
- **State writes go through `bwkit`** (Plan 1): acquire `_bewater/.bw-lock`; `cas commit <path> --expected <rev>` with the bumped `new_text` on stdin; never hand-edit revisioned files. Tool repo: `python -m bwkit …` (editable install). Installed product: `PYTHONPATH=<dest>/_bw-shared python -m bwkit …`.
- **Human convergence is binding** (§4): routers never produce artifacts; capabilities present candidates, name the decision authority, and **stop** before recording any human choice; no skill chooses a gate exit.
- **Deterministic tests are structural** (frontmatter shape, reference presence/contract/no-escape, no TODO, manifest validity, scaffold templates). State-write correctness rides on `bwkit` (tested in Plan 1) + the deferred LLM eval gate.
- **Legacy untouched:** do not modify or delete `src/bw/` or its tests.
- **TDD:** every task writes the failing test first, watches it fail, implements the minimum, watches it pass, commits. No batch.
- **Commit convention:** `feat(bw): …` (skills + validator), `feat(installer): …`, `feat(verify): …`. Commit only the files each task touches.
- **`scripts/verify` reconciliation:** spec §2.1/§11.3 name it `scripts/verify`; we implement it as `scripts/verify.py` (importable as `verify`, ≥80% covered per §11.3) and add `"scripts"` to the pytest `pythonpath`.

---

## File Structure

```
bewater-new/
├── .claude/skills/
│   ├── _bw-shared/{ledger-schema,gate-criteria,glossary}.md   # EXISTS (Plan 1); cited, not modified
│   ├── bw-start/{SKILL.md, references/{state-bootstrap.md, routing.md}, .bewater-managed}
│   ├── bw-immersion/{SKILL.md, references/stage.md, .bewater-managed}
│   ├── bw-discover/{SKILL.md, references/stage.md, .bewater-managed}
│   ├── bw-define/{SKILL.md, references/stage.md, .bewater-managed}
│   ├── bw-project-charter/{SKILL.md, references/{charter-template.md, root-assumptions.md}, .bewater-managed}
│   ├── bw-4c-research/{SKILL.md, references/{4c-framework.md, learning-plan.md}, .bewater-managed}
│   └── bw-insight-craft/{SKILL.md, references/{insight-generation.md, fpet-judgment.md}, .bewater-managed}
├── evals/
│   ├── _harness/                              # EXISTS (Plan 1)
│   └── bw-<skill>/{scenarios/*.yaml, red/*.yaml}   # CREATE per skill (GREEN/ runs deferred)
├── install.sh                                 # CREATE (§9): copy/link/dest/uninstall + bwkit deploy
├── scripts/
│   └── verify.py                              # CREATE (§11.3): authoring-time integrity checks
├── tests/
│   ├── skill_helpers.py                       # CREATE: validate_skill + validate_skill_evals
│   ├── test_skill_helpers.py                  # CREATE: validator TDD vs fixture skills
│   ├── test_skill_bw_start.py                 # CREATE (one per skill, T2–T8)
│   ├── test_skill_bw_immersion.py
│   ├── test_skill_bw_discover.py
│   ├── test_skill_bw_define.py
│   ├── test_skill_bw_project_charter.py
│   ├── test_skill_bw_4c_research.py
│   ├── test_skill_bw_insight_craft.py
│   ├── test_installer_copy.py                 # CREATE (T9)
│   ├── test_installer_link.py                 # CREATE (T10)
│   └── test_verify.py                         # CREATE (T11)
└── pyproject.toml                             # MODIFY (T11): pythonpath += "scripts"
```

Each skill directory is one self-contained unit (the installer deploys it wholesale). The validator and `verify` share one code path so a rule change lands in one place.

---

## Task 1: Shared skill validator (`tests/skill_helpers.py`)

**Files:**
- Create: `tests/skill_helpers.py`
- Test: `tests/test_skill_helpers.py`

**Interfaces:**
- Produces (every later skill task + `scripts/verify` rely on these exact names):
  - `SkillCheckError(Exception)`
  - `validate_skill(skill_dir: Path) -> None` — raises on bad frontmatter, escaped/missing reference, missing contract metadata, or TODO/TBD in shipped skill files.
  - `validate_skill_evals(evals_root: Path, name: str) -> None` — raises if `evals/<name>/scenarios/` or `evals/<name>/red/` lacks a loadable manifest.
  - `skill_dir(repo: Path, name: str) -> Path` — `repo / ".claude" / "skills" / name`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_helpers.py
from __future__ import annotations

from pathlib import Path

import pytest

from skill_helpers import (
    SkillCheckError,
    skill_dir,
    validate_skill,
    validate_skill_evals,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


GOOD_FM = "---\nname: bw-x\ndescription: Use when the user wants to x.\n---\n# bw-x\nbody\n"


def _good_skill(repo: Path) -> None:
    _write(skill_dir(repo, "bw-x") / "SKILL.md", GOOD_FM)
    _write(repo / "evals" / "bw-x" / "scenarios" / "s1.yaml",
           "scenario_id: S-1\ntarget_skill: bw-x\nprompt: hi\n"
           "required_assertions: [a]\nforbidden_behaviors: []\nrepetition_count: 3\n")
    _write(repo / "evals" / "bw-x" / "red" / "r1.yaml",
           "scenario_id: R-1\ntarget_skill: bw-x\nprompt: hi\n"
           "required_assertions: [a]\nforbidden_behaviors: []\nrepetition_count: 1\n")


def test_validate_skill_passes_well_formed_skill(tmp_path: Path):
    repo = tmp_path / "repo"
    _good_skill(repo)
    validate_skill(skill_dir(repo, "bw-x"))          # no raise
    validate_skill_evals(repo / "evals", "bw-x")      # no raise


def test_skill_dir_path():
    assert skill_dir(Path("/r"), "bw-start") == Path("/r/.claude/skills/bw-start")


@pytest.mark.parametrize("bad_fm", [
    "---\nname: bw-x\n---\n# x\n",                       # missing description
    "---\nname: bw-x\ndescription: Trigger here.\n---\n",  # not "Use when"
    "---\nname: bw-x\ndescription: Use when x.\nallowed-tools: Bash\n---\n",  # extra key
])
def test_validate_skill_rejects_bad_frontmatter(tmp_path: Path, bad_fm):
    repo = tmp_path / "repo"
    _write(skill_dir(repo, "bw-x") / "SKILL.md", bad_fm)
    with pytest.raises(SkillCheckError):
        validate_skill(skill_dir(repo, "bw-x"))


def test_validate_skill_rejects_escaping_reference(tmp_path: Path):
    repo = tmp_path / "repo"
    sd = skill_dir(repo, "bw-x")
    _write(sd / "SKILL.md", GOOD_FM)
    _write(sd / "references" / "escape.md", "see ../outside/other.md")
    with pytest.raises(SkillCheckError):
        validate_skill(sd)


def test_validate_skill_allows_shared_reference_citation(tmp_path: Path):
    repo = tmp_path / "repo"
    sd = skill_dir(repo, "bw-x")
    _write(sd / "SKILL.md", GOOD_FM + "cite ../_bw-shared/glossary.md\n")
    validate_skill(sd)  # no raise: sanctioned shared citation


def test_validate_skill_rejects_placeholders(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(skill_dir(repo, "bw-x") / "SKILL.md", GOOD_FM.replace("body", "TODO fill"))
    with pytest.raises(SkillCheckError):
        validate_skill(skill_dir(repo, "bw-x"))


def test_validate_skill_requires_contract_metadata_on_contract_refs(tmp_path: Path):
    repo = tmp_path / "repo"
    sd = skill_dir(repo, "bw-x")
    _write(sd / "SKILL.md", GOOD_FM)
    _write(sd / "references" / "local-ledger.md",
           "---\ncontract_id: bw-ledger\n---\n# x\n")  # version missing
    with pytest.raises(SkillCheckError):
        validate_skill(sd)


def test_validate_skill_evals_requires_scenarios_and_red(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "evals" / "bw-x" / "scenarios" / "s1.yaml",
           "scenario_id: S-1\ntarget_skill: bw-x\nprompt: hi\n"
           "required_assertions: [a]\nforbidden_behaviors: []\nrepetition_count: 3\n")
    # red/ missing
    with pytest.raises(SkillCheckError):
        validate_skill_evals(repo / "evals", "bw-x")
```

> **Note on the no-escape rule:** skills cite shared contracts from prose (e.g. "cite `../_bw-shared/ledger-schema.md`"). `validate_skill` allows `../_bw-shared/` and rejects any other parent-relative (`../`) path anywhere in the skill's markdown, since that would read files outside the self-contained skill directory (§2.3, §11.3).

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_helpers.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'skill_helpers'`.

- [ ] **Step 3: Write minimal implementation**

```python
# tests/skill_helpers.py
"""Shared structural validator for bw-* skills (spec §4, §11.3). Authoring utility;
reused by every per-skill pytest and by scripts/verify. Not shipped."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from evals._harness.loader import ManifestError, load_manifest


class SkillCheckError(Exception):
    """A skill fails a structural check."""


def skill_dir(repo: Path, name: str) -> Path:
    return Path(repo) / ".claude" / "skills" / name


_PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME|XXX)\b")


def _frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        raise SkillCheckError(f"frontmatter is not YAML: {e}") from e
    return fm if isinstance(fm, dict) else {}


def validate_skill(skill_dir: Path) -> None:
    skill_dir = Path(skill_dir)
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise SkillCheckError(f"missing SKILL.md in {skill_dir}")

    fm = _frontmatter(skill_md.read_text())
    if set(fm) != {"name", "description"}:
        raise SkillCheckError(f"frontmatter must be exactly name+description (got {sorted(fm)})")
    desc = str(fm["description"]).strip()
    if not desc.startswith("Use when"):
        raise SkillCheckError("description must start with 'Use when'")

    refs = skill_dir / "references"
    files = [skill_md, *sorted((refs).rglob("*.md"))] if refs.is_dir() else [skill_md]
    for f in files:
        text = f.read_text()
        if _PLACEHOLDER_RE.search(text):
            raise SkillCheckError(f"placeholder token in {f.name}")
        # references may cite only the sanctioned shared location (../_bw-shared/);
        # any other parent-relative path escapes the skill directory (§2.3, §11.3)
        if re.search(r"\.\./(?!_bw-shared/)", text):
            raise SkillCheckError(f"{f.name} references a path outside its skill dir")
        # a reference that declares a contract must carry full contract metadata
        cfm = _frontmatter(text)
        if "contract_id" in cfm:
            for key in ("contract_version", "source_sections"):
                if key not in cfm:
                    raise SkillCheckError(f"contract ref {f.name} missing {key}")


def validate_skill_evals(evals_root: Path, name: str) -> None:
    for sub in ("scenarios", "red"):
        bucket = Path(evals_root) / name / sub
        manifests = sorted(bucket.glob("*.yaml")) if bucket.is_dir() else []
        if not manifests:
            raise SkillCheckError(f"evals/{name}/{sub}/ has no manifests")
        for m in manifests:
            try:
                load_manifest(m)
            except ManifestError as e:
                raise SkillCheckError(f"{m}: {e}") from e
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_helpers.py -v`
Expected: PASS (all).

- [ ] **Step 5: Commit**

```bash
git add tests/skill_helpers.py tests/test_skill_helpers.py
git commit -m "feat(bw): shared skill structural validator (frontmatter/refs/evals)"
```

---

## Task 2: bw-start (entry skill)

**Files:**
- Create: `.claude/skills/bw-start/SKILL.md`
- Create: `.claude/skills/bw-start/references/state-bootstrap.md`
- Create: `.claude/skills/bw-start/references/routing.md`
- Create: `evals/bw-start/scenarios/bootstrap-new-project.yaml`, `evals/bw-start/red/no-skill.yaml`
- Test: `tests/test_skill_bw_start.py`

**Interfaces:**
- Produces: the entry skill whose references carry the canonical v5 `_bewater/` scaffold (config/ledger/conditions + `records/` + `_bewater-output/`) and the §4 routing/reconcile procedure. Later routers and capabilities cite the same `_bw-shared/` contracts bw-start cites.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_start.py
from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_start_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-start"))
    validate_skill_evals(REPO / "evals", "bw-start")


def test_state_bootstrap_carries_v5_scaffold():
    text = (skill_dir(REPO, "bw-start") / "references" / "state-bootstrap.md").read_text()
    for token in ["schema_version: 1", "next_ids:", "branch:", "artifact:", "decision:",
                  "active_branch: BR-001", "current_stage: immersion", "decision_authority:",
                  "assumptions: {}", "conditions: {}"]:
        assert token in text, f"state-bootstrap missing {token}"


def test_routing_cites_precedence_and_reconcile():
    text = (skill_dir(REPO, "bw-start") / "references" / "routing.md").read_text()
    for token in ["open condition", "active baseline", "direct-write", "bwkit"]:
        assert token.lower() in text.lower(), f"routing missing {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_start.py -v`
Expected: FAIL — `.claude/skills/bw-start/` does not exist.

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-start/SKILL.md`:

```markdown
---
name: bw-start
description: Use when the user wants to start a bewater decision-phase project, resume without a known stage, or reconcile ambiguous or pending project state.
---

# bw-start

The entry point for bewater. You orient, reconcile, report status, and route — you never produce artifacts and never choose a gate exit (spec §4).

## When invoked

1. **No `_bewater/` in cwd** → bootstrap a project. Follow `references/state-bootstrap.md` verbatim: create the v5 tree, write the default config/ledger/conditions, create branch `BR-001` at `immersion`, set `active_branch`. Write state only through the §5.7 direct-write protocol (acquire `_bewater/.bw-lock` via bwkit, then `cas commit`).
2. **`_bewater/` exists** → reconcile before recommending anything (spec §4.6, §10.5):
   - read `config.yaml` (active branch/branches, stage, decision authority), `ledger.yaml`, `conditions.yaml`;
   - scan **open conditions** and **active-baseline validity**;
   - detect pending or manual-repair gate/backtrack action plans; if found, resume the idempotent recovery rather than starting new work;
   - if several branches are active and the user did not name one, **ask the human to choose before writing state**.
3. **Global / unspecified resume / ambiguous branch** → handled here; a request that names one stage and resolves to one branch routes to that stage's router.

## Routing precedence (§4)

(a) a direct, specific work request → the matching capability or gate;
(b) new project, global status, unspecified resume, pending recoverable action, or ambiguous branch → bw-start (here);
(c) one stage named + one branch → that stage's router.

Report the current stage and the next human decision, then stop. See `references/routing.md` and cite `../_bw-shared/ledger-schema.md` and `../_bw-shared/glossary.md` for field/term authority.
```

Create `.claude/skills/bw-start/references/state-bootstrap.md`:

```markdown
# State bootstrap (authoritative v5 scaffold)

Distilled from spec §2.2, §5.2, §5.3, §5.6. When bootstrapping, create the directories
and write these files verbatim (substitute `updated_at` with the real ISO-8601 time),
each through a bwkit `cas commit` with `--expected 0`-equivalent first write (for the
initial file, write it directly, then all subsequent edits go through CAS).

## Directory layout

    _bewater/
    ├── config.yaml
    ├── ledger.yaml
    ├── conditions.yaml
    └── records/
    _bewater-output/

## config.yaml

```yaml
schema_version: 1
revision: 1
updated_at: "2026-07-28T12:00:00Z"
updated_by: bw-start
next_ids:
  branch: 2
  artifact: 1
  experiment: 1
  decision: 1
  baseline: 1
  backtrack: 1
  action: 1
  evidence: 1
project:
  name: ""
  success_criteria: []
decision_authority:
  G1:
    level: product-owner
    accountable_person: null
    accountable_role: null
  G2:
    level: investment-decision
    accountable_person: null
    accountable_role: null
active_branch: BR-001
active_execution_handoff: null
branches:
  BR-001:
    status: active
    current_stage: immersion
    parent_ids: []
    merged_into: null
    gate_due_at:
      G1: null
      G2: null
    inherited_assumption_refs: []
    excluded_assumption_refs: []
    inherited_condition_ids: []
    needs_rebase_refs: []
    active_baselines:
      G1: null
      G2: null
```

## ledger.yaml

```yaml
schema_version: 1
revision: 1
next_id: 1
updated_at: "2026-07-28T12:00:00Z"
updated_by: bw-start
assumptions: {}
```

## conditions.yaml

```yaml
schema_version: 1
revision: 1
next_id: 1
updated_at: "2026-07-28T12:00:00Z"
updated_by: bw-start
conditions: {}
```

The first real edit to any of these files bumps `revision` to 2 via `bwkit cas commit
<path> --expected 1` with the bumped text on stdin (bwkit verifies the bump and keeps a
rotating backup). Field semantics: see `../_bw-shared/ledger-schema.md`.
```

Create `.claude/skills/bw-start/references/routing.md`:

```markdown
# Routing and reconcile procedure (spec §4, §5.7, §10.5)

## Before recommending downstream work, scan

1. **Open conditions** in `conditions.yaml` — any `status: open` condition blocks the
   next gate and must be surfaced (spec §5.6).
2. **Active-baseline validity** — for the active branch, read `active_baselines.G1/G2`;
   if a referenced baseline file is missing or its source decision is `invalidated`,
   the branch is needs-rebase and no gate may proceed (spec §6.6, §8.3).
3. **Pending / manual-repair actions** — read gate and backtrack records under
   `_bewater/records/`; if any `action_plan.action_status` is `pending` or
   `manual-repair`, resume idempotent recovery (verify each ordered step applied or
   intentionally skipped) before new work.

## Direct-write protocol (every state write)

Announce target files → acquire `_bewater/.bw-lock` (`bwkit lock acquire`) → read current
revisions → mutate only intended records preserving unknown fields → `bwkit cas commit
<path> --expected <rev>` with bumped text on stdin → re-read and verify (spec §5.7).
On revision conflict, stop without writing and request a manual merge. One active
bewater writer per project.

## Decision authority

A gate cannot record a decision while its single accountable person is null or ambiguous
(spec §5.2, §6.1). Surface this during reconcile; do not invent a decision maker.

Cite `../_bw-shared/glossary.md` for terms.
```

Create `evals/bw-start/scenarios/bootstrap-new-project.yaml`:

```yaml
scenario_id: BWSTART-S1
target_skill: bw-start
prompt: "Start a bewater project for: a mobile app helping solo diners find empty restaurants."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "creates _bewater/{config,ledger,conditions}.yaml"
  - "creates branch BR-001 at immersion and sets active_branch"
  - "writes state via bwkit (lock + cas commit), not by hand"
forbidden_behaviors:
  - "chooses a gate exit"
  - "records a human decision before receiving it"
repetition_count: 3
```

Create `evals/bw-start/red/no-skill.yaml`:

```yaml
scenario_id: BWSTART-R1
target_skill: bw-start
prompt: "Start a bewater project for: X."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-start absent, no _bewater/ scaffold is created (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_start.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-start evals/bw-start tests/test_skill_bw_start.py
git commit -m "feat(bw): bw-start entry skill + v5 scaffold + routing references"
```

---

## Task 3: bw-immersion (router)

**Files:**
- Create: `.claude/skills/bw-immersion/SKILL.md`, `references/stage.md`
- Create: `evals/bw-immersion/scenarios/orient.yaml`, `evals/bw-immersion/red/no-skill.yaml`
- Test: `tests/test_skill_bw_immersion.py`

**Interfaces:**
- Produces: the Immersion router. Orients/resumes/reports status/routes; never produces artifacts. Routes Immersion work to `bw-project-charter` (charter + root assumptions).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_immersion.py
from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_immersion_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-immersion"))
    validate_skill_evals(REPO / "evals", "bw-immersion")


def test_immersion_stage_routes_to_charter():
    text = (skill_dir(REPO, "bw-immersion") / "references" / "stage.md").read_text()
    assert "bw-project-charter" in text
    assert "immersion" in text.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_immersion.py -v`
Expected: FAIL — skill absent.

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-immersion/SKILL.md`:

```markdown
---
name: bw-immersion
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Immersion.
---

# bw-immersion

A **router** for the Immersion stage (Start module). You orient, resume, report status,
and route "what next?" — you never produce artifacts (spec §4). Immersion aligns the team
on the proposition and seeds the first assumptions (bewater-core §5.0).

## On invoke

- Confirm the active branch's `current_stage` is `immersion`; if not, defer to bw-start.
- Report Immersion status: is there a project charter? are root assumptions seeded?
- Route the next action to **bw-project-charter** (draft/revise the charter, seed root
  assumptions) — see `references/stage.md`. Present the capability choice and stop when
  the next action is ambiguous.

Immersion is complete when stakeholders agree on proposition + success criteria and ≥3
initial assumptions exist (bewater-core §5.0). Hand off to Discover (`bw-discover`).
Cite `../_bw-shared/glossary.md`.
```

Create `.claude/skills/bw-immersion/references/stage.md`:

```markdown
# Immersion stage (bewater-core §5.0, §9.1)

Immersion (Start module) = align on proposition / scope / constraints, write the project
charter, and seed the first assumptions.

## Capability to route to

- **bw-project-charter** — draft or revise the charter (who/what/how/why + scope +
  constraints + success criteria) with the Money+Magic four-field dual-sided definition,
  and seed root-layer assumptions into the ledger (§9.1).

## Exit criteria (orient the user toward these)

- Stakeholders aligned on proposition and success criteria.
- ≥3 initial (seed) assumptions recorded in the ledger.

Do not produce the charter yourself — route to bw-project-charter. On completion, the
next stage is Discover (bw-discover router).
```

Create `evals/bw-immersion/scenarios/orient.yaml`:

```yaml
scenario_id: BWIMM-S1
target_skill: bw-immersion
prompt: "Where are we in bewater, and what's next?"
fixture_refs: []
installed_dependency_skills: [bw-start]
required_assertions:
  - "reports Immersion status (charter present? root assumptions?)"
  - "routes to bw-project-charter, does not author the charter inline"
forbidden_behaviors:
  - "writes an artifact"
  - "chooses a gate exit"
repetition_count: 3
```

Create `evals/bw-immersion/red/no-skill.yaml`:

```yaml
scenario_id: BWIMM-R1
target_skill: bw-immersion
prompt: "What's next in Immersion?"
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-immersion absent, no Immersion status/routing is produced (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_immersion.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-immersion evals/bw-immersion tests/test_skill_bw_immersion.py
git commit -m "feat(bw): bw-immersion router (orient/resume/route to charter)"
```

---

## Task 4: bw-discover (router)

**Files:**
- Create: `.claude/skills/bw-discover/SKILL.md`, `references/stage.md`
- Create: `evals/bw-discover/scenarios/orient.yaml`, `evals/bw-discover/red/no-skill.yaml`
- Test: `tests/test_skill_bw_discover.py`

**Interfaces:**
- Produces: the Discover router. Routes to `bw-4c-research` (4C + learning plan) and `bw-insight-craft` (facts→insights, F/P/E/T); hand-off to Define.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_discover.py
from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_discover_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-discover"))
    validate_skill_evals(REPO / "evals", "bw-discover")


def test_discover_routes_to_research_and_insight():
    text = (skill_dir(REPO, "bw-discover") / "references" / "stage.md").read_text()
    assert "bw-4c-research" in text
    assert "bw-insight-craft" in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_discover.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-discover/SKILL.md`:

```markdown
---
name: bw-discover
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Discover.
---

# bw-discover

A **router** for the Discover stage (Strategy module). Orient/resume/status/route; never
produce artifacts (spec §4). Discover turns facts into insights and closes directional
hypotheses (bewater-core §5.1.1).

## On invoke

- Confirm `current_stage` is `discover`.
- Report Discover status: 4C coverage, insight count/quality, learning-plan state.
- Route to **bw-4c-research** (plan/run/synthesize 4C + learning plan) and
  **bw-insight-craft** (facts→insights, F/P/E/T judgment). Present the choice and stop
  when ambiguous.

Discover hands directional hypotheses to Define (`bw-define`). Cite
`../_bw-shared/glossary.md` and `../_bw-shared/gate-criteria.md` (insight readiness).
```

Create `.claude/skills/bw-discover/references/stage.md`:

```markdown
# Discover stage (bewater-core §5.1.1, §3.6, §9.2, §9.3)

Discover (Strategy module) = 4C-directed exploration + field method, refining facts into
insights, closing directional hypotheses.

## Capabilities to route to

- **bw-4c-research** — plan/run/synthesize 4C research (Consumer/Company/Category/Channel,
  each ≥3 facts) and maintain the learning plan (known / not-found / to-deepen / droppable).
- **bw-insight-craft** — generate insights (cognitive 4-step ladder, 13 lenses,
  Pearl/Code/Force) and judge candidates against F/P/E/T.

## Exit criteria

- Insights pass F/P/E/T; Fact / Accepted Belief / Insight are distinguishable; 4C is not
  lopsided; ≥1 "surprising-but-plausible" insight. Hand directional hypotheses to Define.
```

Create `evals/bw-discover/scenarios/orient.yaml`:

```yaml
scenario_id: BWDISC-S1
target_skill: bw-discover
prompt: "Status check and what's next in Discover."
fixture_refs: []
installed_dependency_skills: [bw-start]
required_assertions:
  - "reports 4C coverage and insight status"
  - "routes to bw-4c-research and/or bw-insight-craft, authors nothing inline"
forbidden_behaviors:
  - "writes an artifact"
repetition_count: 3
```

Create `evals/bw-discover/red/no-skill.yaml`:

```yaml
scenario_id: BWDISC-R1
target_skill: bw-discover
prompt: "What's next in Discover?"
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-discover absent, no Discover routing is produced (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_discover.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-discover evals/bw-discover tests/test_skill_bw_discover.py
git commit -m "feat(bw): bw-discover router (route to 4c-research + insight-craft)"
```

---

## Task 5: bw-define (router)

**Files:**
- Create: `.claude/skills/bw-define/SKILL.md`, `references/stage.md`
- Create: `evals/bw-define/scenarios/orient.yaml`, `evals/bw-define/red/no-skill.yaml`
- Test: `tests/test_skill_bw_define.py`

**Interfaces:**
- Produces: the Define router. Routes to the Phase-1b capabilities (`bw-directional-hypothesis`, `bw-strategy-statement`, `bw-opportunity-area`, `bw-assumption-map`) and to the G1 gate (`bw-strategy-gate`). Those skills are built in Phase 1b; this router names them as downstream routes now.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_define.py
from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_define_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-define"))
    validate_skill_evals(REPO / "evals", "bw-define")


def test_define_routes_to_strategy_capabilities_and_gate():
    text = (skill_dir(REPO, "bw-define") / "references" / "stage.md").read_text()
    for name in ["bw-strategy-statement", "bw-opportunity-area",
                 "bw-assumption-map", "bw-strategy-gate"]:
        assert name in text, f"define stage.md missing {name}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_define.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-define/SKILL.md`:

```markdown
---
name: bw-define
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Define.
---

# bw-define

A **router** for the Define stage (Strategy module, the method's pivot). Orient/resume/
status/route; never produce artifacts (spec §4). Define turns insights into an innovation
strategy + opportunity areas and runs into the G1 gate (bewater-core §5.1.2).

## On invoke

- Confirm `current_stage` is `define`.
- Report Define status: directional hypotheses closed? strategy selected/locked? opportunity
  portfolio (2–4)? assumption initial inventory + Achilles-Heel quadrant? Money+Magic
  initial judgment?
- Route to the Define capabilities (see `references/stage.md`); when the subject is
  G1-ready or a deadline has fallen, route to **bw-strategy-gate**. Present the choice and
  stop when ambiguous.

Define completes at the G1 gate decision. Cite `../_bw-shared/gate-criteria.md` (G1
readiness) and `../_bw-shared/glossary.md`.
```

Create `.claude/skills/bw-define/references/stage.md`:

```markdown
# Define stage (bewater-core §5.1.2, §9.4–9.6, §9.8)

Define (Strategy module) = refine insights into an innovation strategy + strategy statement
+ 2–4 opportunity areas; initial assumption inventory; Money+Magic initial judgment. This is
the G1 gate's input stage.

## Capabilities to route to (Phase 1b)

- **bw-directional-hypothesis** — compose/refine By / We can / Resulting in hypotheses.
- **bw-strategy-statement** — create/select/revise/lock the choice-cutting strategy.
- **bw-opportunity-area** — define 2–4 non-overlapping opportunity areas.
- **bw-assumption-map** — initial assumption inventory + Achilles-Heel prioritization.

## Gate

- **bw-strategy-gate** — when G1-ready or the gate deadline has fallen, route here. The
  gate assembles evidence and records the human G1 decision; it never chooses an exit.

G1 readiness is in `../_bw-shared/gate-criteria.md`.
```

Create `evals/bw-define/scenarios/orient.yaml`:

```yaml
scenario_id: BWDEF-S1
target_skill: bw-define
prompt: "What's left before G1?"
fixture_refs: []
installed_dependency_skills: [bw-start]
required_assertions:
  - "reports Define readiness gaps against G1 criteria"
  - "routes to a Define capability or bw-strategy-gate, authors nothing inline"
forbidden_behaviors:
  - "writes an artifact"
  - "records a G1 exit"
repetition_count: 3
```

Create `evals/bw-define/red/no-skill.yaml`:

```yaml
scenario_id: BWDEF-R1
target_skill: bw-define
prompt: "What's next in Define?"
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-define absent, no Define routing is produced (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_define.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-define evals/bw-define tests/test_skill_bw_define.py
git commit -m "feat(bw): bw-define router (route to strategy capabilities + G1 gate)"
```

---

## Task 6: bw-project-charter (capability)

**Files:**
- Create: `.claude/skills/bw-project-charter/SKILL.md`, `references/charter-template.md`, `references/root-assumptions.md`
- Create: `evals/bw-project-charter/scenarios/draft.yaml`, `evals/bw-project-charter/red/no-skill.yaml`
- Test: `tests/test_skill_bw_project_charter.py`

**Interfaces:**
- Produces: the charter capability. Writes the charter artifact (`_bewater-output/ART-001-r1-charter.md`, append-only, §5.4) and seeds root assumptions into `ledger.yaml` (§5.3). Stops before recording any human signoff/choice.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_project_charter.py
from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_project_charter_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-project-charter"))
    validate_skill_evals(REPO / "evals", "bw-project-charter")


def test_charter_template_has_dual_sided_four_fields():
    text = (skill_dir(REPO, "bw-project-charter") / "references" / "charter-template.md").read_text()
    for token in ["dual_sided", "consumer_value_proposition", "consumer_target",
                  "commercial_value_proposition", "leverageable_assets", "artifact_id"]:
        assert token in text, f"charter-template missing {token}"


def test_root_assumptions_reference_layer_root():
    text = (skill_dir(REPO, "bw-project-charter") / "references" / "root-assumptions.md").read_text()
    assert "layer: root" in text
    assert "record_revision" in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_project_charter.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-project-charter/SKILL.md`:

```markdown
---
name: bw-project-charter
description: Use when the user wants to draft or revise a bewater project charter or seed root assumptions.
---

# bw-project-charter

A **capability** that drafts/revises the project charter and seeds root assumptions
(bewater-core §5.0, §9.1). You produce iterable artifacts and stop before any human
signoff or choice (spec §4).

## Workflow

1. Elicit proposition (who/what/how/why), scope, constraints, success criteria.
2. Draft the dual-sided charter using `references/charter-template.md` — the Money+Magic
   four fields plus the tension point (§9.1). Magic ≠ "willingness to pay"; it is empathy
   for the user's situation and desire.
3. Seed the proposition's most uncertain claims as **root-layer** assumptions in the
   ledger, per `references/root-assumptions.md`.
4. Write the charter artifact (append-only `_bewater-output/ART-001-r1-charter.md`,
   §5.4) and update the ledger (§5.7: `bwkit lock` + `cas commit`).
5. Present the charter + seeded assumptions, name the human decision authority
   (product-owner level), and **stop**. Recommend; do not record the human's choice.
```

Create `.claude/skills/bw-project-charter/references/charter-template.md`:

```markdown
# Charter artifact template (spec §5.4, §9.1)

File: `_bewater-output/ART-001-r1-charter.md` (append-only; a substantive edit writes
`ART-001-r2-charter.md` with `supersedes_ref: artifact:ART-001@1`). Allocate the ART id
from `config.next_ids.artifact` while holding the §5.7 lock.

## Frontmatter

```yaml
schema_version: 1
artifact_id: ART-001
revision: 1
supersedes_ref: null
kind: charter
stage: immersion
branch_id: BR-001
document_status: draft
validation_status: unvalidated
dual_sided:
  magic:
    consumer_value_proposition:
      statement: ""        # what value we give the user
      evidence_refs: []
    consumer_target:
      statement: ""        # who, specifically — situation and desire, not "can solve X"
      evidence_refs: []
  money:
    commercial_value_proposition:
      statement: ""        # how the business works and earns
      evidence_refs: []
    leverageable_assets:
      statement: ""        # existing assets/capabilities that build the moat
      evidence_refs: []
  tension:
    statement: ""          # where Magic and Money constrain / reinforce each other
  balance_choice: ""
derived_from: []
signoffs: []
stale_reason: null
```

## Body

One-line proposition (who/what/how/why) + scope + constraints + success criteria. A non-empty
final body is only document-presence evidence — it is never readiness (spec §5.4).
```

Create `.claude/skills/bw-project-charter/references/root-assumptions.md`:

```markdown
# Seeding root assumptions (spec §5.3)

Root assumptions capture the proposition's most uncertain claims at `layer: root`. Allocate
the A-id from `ledger.next_id`. Write via `bwkit lock acquire` + `cas commit ledger.yaml
--expected <rev>` (bump the ledger envelope `revision` and the record's `record_revision`).

## Assumption record (root)

```yaml
A-001:
  record_revision: 1
  statement: ""
  branch_id: BR-001
  layer: root              # root | strategy | opportunity | concept | feature
  category: consumer       # consumer | commercial | technical | distribution | regulatory
  side: money              # money | magic | both
  impact: high             # high | medium | low
  uncertainty: high        # high | medium | low
  evidence_level: L2       # L1–L6; must point to evidence, not be asserted
  validation_status: untested   # untested | testing | supported | falsified | inconclusive
  status: active           # active | killed | merged
  evidence_refs: []
  derived_from: []
  supersedes_ref: null
  risk_history: []
  l4_obligation_status: open
  history: []
```

`is_achilles_heel` is derived (impact=high AND uncertainty=high) and raises a durable L4
obligation (§5.3). Field semantics: `../_bw-shared/ledger-schema.md`.
```

Create `evals/bw-project-charter/scenarios/draft.yaml`:

```yaml
scenario_id: BWCHA-S1
target_skill: bw-project-charter
prompt: "Draft a charter and seed root assumptions for: a service matching freelance chefs to pop-up kitchens."
fixture_refs: []
installed_dependency_skills: [bw-start]
required_assertions:
  - "writes ART charter with dual_sided four fields populated"
  - "seeds >=3 root-layer assumptions in the ledger"
  - "writes via bwkit lock + cas commit"
  - "stops before recording a human signoff"
forbidden_behaviors:
  - "records a signoff before the human gives it"
  - "overwrites an existing ART revision file in place"
repetition_count: 3
```

Create `evals/bw-project-charter/red/no-skill.yaml`:

```yaml
scenario_id: BWCHA-R1
target_skill: bw-project-charter
prompt: "Draft a charter for: X."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-project-charter absent, no charter artifact is written (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_project_charter.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-project-charter evals/bw-project-charter tests/test_skill_bw_project_charter.py
git commit -m "feat(bw): bw-project-charter capability (charter + root assumptions)"
```

---

## Task 7: bw-4c-research (capability)

**Files:**
- Create: `.claude/skills/bw-4c-research/SKILL.md`, `references/4c-framework.md`, `references/learning-plan.md`
- Create: `evals/bw-4c-research/scenarios/plan.yaml`, `evals/bw-4c-research/red/no-skill.yaml`
- Test: `tests/test_skill_bw_4c_research.py`

**Interfaces:**
- Produces: the 4C research capability. Plans/runs/synthesizes Consumer/Company/Category/Channel research and maintains the learning plan. Writes a research artifact (`kind: research`).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_4c_research.py
from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_4c_research_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-4c-research"))
    validate_skill_evals(REPO / "evals", "bw-4c-research")


def test_4c_framework_lists_four_cs():
    text = (skill_dir(REPO, "bw-4c-research") / "references" / "4c-framework.md").read_text()
    for token in ["Consumer", "Company", "Category", "Channel"]:
        assert token in text, f"4c-framework missing {token}"


def test_learning_plan_has_four_questions():
    text = (skill_dir(REPO, "bw-4c-research") / "references" / "learning-plan.md").read_text()
    for token in ["found", "not-found", "deepen", "droppable"]:
        assert token in text, f"learning-plan missing {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_4c_research.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-4c-research/SKILL.md`:

```markdown
---
name: bw-4c-research
description: Use when the user wants to plan, run, or synthesize bewater 4C research or a learning plan.
---

# bw-4c-research

A **capability** for 4C research and the learning plan (bewater-core §5.1.1, §3.6, §9.2).
You produce a research artifact and stop before human synthesis judgment (spec §4).

## Workflow

1. Stand up the 4C frame (Consumer / Company / Category / Channel) — four questions to
   answer, not four buckets; each C needs ≥3 facts (`references/4c-framework.md`).
2. Maintain the living learning plan with the four-question weekly iteration
   (`references/learning-plan.md`).
3. Record findings into a research artifact (`_bewater-output/ART-xxx-rN-research.md`,
   `kind: research`); raw material is cited, not dumped.
4. Surface candidate facts/accepted-beliefs for `bw-insight-craft`; do not yourself
   declare an insight F/P/E/T — that is human convergence.
```

Create `.claude/skills/bw-4c-research/references/4c-framework.md`:

```markdown
# 4C research framework (bewater-core §3.6, §5.1.1, §9.2)

4C is a navigation compass — four questions to answer so research is not lopsided:

| C | Question | Research type |
|---|---|---|
| **Consumer** | Who is buying, and why? | Design research (empathy) |
| **Company** | What do we already have? | Stakeholder interviews |
| **Category** | Which arena are we playing in? | Market research |
| **Channel** | What channel do we go through? | Market research |

Each C collects ≥3 facts. Method matrix (primary/secondary × 4C) and the field-method
pack (AEIOU, extreme users, projective trio, etc.) are in bewater-core §5.1.1. Discipline:
an observation is only a hypothesis until validated by interview or behavior.
```

Create `.claude/skills/bw-4c-research/references/learning-plan.md`:

```markdown
# Learning plan (bewater-core §9.2)

A living plan, iterated weekly with four questions:

- **found** — what we learned this cycle;
- **not-found** — what we still do not know (the soul of the plan);
- **to-deepen** — which signal deserves more depth next cycle;
- **droppable** — which line of inquiry to stop pursuing.

Research is flow, not waterfall: synthesize while researching, do not wait for "all facts."
Record the plan inside the research artifact's body and bump its revision when it changes.
```

Create `evals/bw-4c-research/scenarios/plan.yaml`:

```yaml
scenario_id: BW4C-S1
target_skill: bw-4c-research
prompt: "Plan 4C research for: a subscription box for home bartenders."
fixture_refs: []
installed_dependency_skills: [bw-start]
required_assertions:
  - "produces a research artifact covering all four Cs"
  - "records a four-question learning plan"
  - "does not declare insights F/P/E/T (defers to bw-insight-craft)"
forbidden_behaviors:
  - "records a human synthesis judgment"
repetition_count: 3
```

Create `evals/bw-4c-research/red/no-skill.yaml`:

```yaml
scenario_id: BW4C-R1
target_skill: bw-4c-research
prompt: "Plan 4C research for: X."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-4c-research absent, no research artifact is written (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_4c_research.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-4c-research evals/bw-4c-research tests/test_skill_bw_4c_research.py
git commit -m "feat(bw): bw-4c-research capability (4C + learning plan)"
```

---

## Task 8: bw-insight-craft (capability)

**Files:**
- Create: `.claude/skills/bw-insight-craft/SKILL.md`, `references/insight-generation.md`, `references/fpet-judgment.md`
- Create: `evals/bw-insight-craft/scenarios/craft.yaml`, `evals/bw-insight-craft/red/no-skill.yaml`
- Test: `tests/test_skill_bw_insight_craft.py`

**Interfaces:**
- Produces: the insight capability. Generates insight candidates (cognitive 4-step ladder, 13 lenses, Pearl/Code/Force) and judges them against F/P/E/T. Writes insight artifacts (`kind: insight`). Stops before human F/P/E/T signoff.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_insight_craft.py
from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_insight_craft_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-insight-craft"))
    validate_skill_evals(REPO / "evals", "bw-insight-craft")


def test_generation_has_ladder_and_methods():
    text = (skill_dir(REPO, "bw-insight-craft") / "references" / "insight-generation.md").read_text()
    for token in ["Accepted Belief", "Pearl", "Code", "Force"]:
        assert token in text, f"insight-generation missing {token}"


def test_fpet_lists_four_standards():
    text = (skill_dir(REPO, "bw-insight-craft") / "references" / "fpet-judgment.md").read_text()
    for token in ["Fresh", "Potent", "Energizing", "Truth"]:
        assert token in text, f"fpet-judgment missing {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_insight_craft.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-insight-craft/SKILL.md`:

```markdown
---
name: bw-insight-craft
description: Use when the user wants to turn research into insights or judge insight candidates against F/P/E/T.
---

# bw-insight-craft

A **capability** that turns research into insights and judges them (bewater-core §5.1.1,
§9.3). You produce insight candidates and stop before the human F/P/E/T signoff (spec §4).

## Workflow

1. Walk the cognitive four-step ladder (`references/insight-generation.md`): Facts →
   Accepted Beliefs → Insights → Hypotheses. Accepted Beliefs are the target insights
   challenge.
2. Generate candidates with the 13 lenses and the Pearl/Code/Force methods.
3. Judge each candidate against F/P/E/T (`references/fpet-judgment.md`); downgrade a
   failing candidate back to a fact.
4. Write insight artifacts (`_bewater-output/ART-xxx-rN-insight.md`, `kind: insight`).
5. Present candidates + your F/P/E/T assessment, name the human decision authority, and
   **stop**. Current-revision human F/P/E/T signoff is a G1 readiness requirement — the
   human signs, not you (`../_bw-shared/gate-criteria.md`).
```

Create `.claude/skills/bw-insight-craft/references/insight-generation.md`:

```markdown
# Insight generation (bewater-core §9.3)

## Cognitive four-step ladder

Facts (observations) → **Accepted Beliefs** (unexamined consensus — "everyone assumes") →
**Insights** (a non-obvious statement that reveals the tension behind an Accepted Belief
and opens new opportunity) → Hypotheses. Accepted Beliefs are the insight's target.

## Generation methods

- **13 lenses** — struggle / unmet aspiration / language / trend-why / cross-category
  analogy / culture / failing paradigm / unconscious behavior / category white-space /
  ritual quirk / hidden behavior / compensating behavior (each with an "Ask: …" prompt).
- **Pearl Finding** — record field surprises/metaphors/behavior without interpretation.
- **Code Cracking** — assume the pearls are true; list 3–5 explanatory hypotheses
  (motivation / culture / system / market) for the tensest pearl.
- **Force Fitting** — inductively join seemingly unrelated evidence into a new insight.

An insight is not a fact, not an accepted belief, not consensus, not a guess.
```

Create `.claude/skills/bw-insight-craft/references/fpet-judgment.md`:

```markdown
# F/P/E/T judgment (bewater-core §9.3)

Four standards every insight must pass:

- **Fresh** — non-obvious; not already common knowledge.
- **Potent** — hits a real cause; gives the business a reason to engage.
- **Energizing** — a spark for ideas; activates the room.
- **Truth** — defensible against evidence.

Signals of a strong insight: hits the cause; reveals the tension between what is and what
should be; is the spark of an idea. Signals of a weak one: mere statistics; no reason for
the business to engage; rationalizing a pre-chosen idea. A candidate that fails F/P/E/T is
downgraded back to a fact. Current-revision human F/P/E/T signoff is required for G1
readiness (`../_bw-shared/gate-criteria.md`).
```

Create `evals/bw-insight-craft/scenarios/craft.yaml`:

```yaml
scenario_id: BWINS-S1
target_skill: bw-insight-craft
prompt: "Turn these research findings into insights and judge them against F/P/E/T."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-4c-research]
required_assertions:
  - "walks Facts -> Accepted Beliefs -> Insights"
  - "writes insight artifacts with kind: insight"
  - "judges candidates against Fresh/Potent/Energizing/Truth"
  - "stops before recording the human F/P/E/T signoff"
forbidden_behaviors:
  - "records a human signoff before receiving it"
repetition_count: 3
```

Create `evals/bw-insight-craft/red/no-skill.yaml`:

```yaml
scenario_id: BWINS-R1
target_skill: bw-insight-craft
prompt: "Craft insights from these findings."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-insight-craft absent, no insight artifact is written (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_insight_craft.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-insight-craft evals/bw-insight-craft tests/test_skill_bw_insight_craft.py
git commit -m "feat(bw): bw-insight-craft capability (insight generation + F/P/E/T)"
```

---

## Task 9: install.sh — copy core + bwkit deploy

**Files:**
- Create: `install.sh`
- Test: `tests/test_installer_copy.py`

**Interfaces:**
- Consumes: `tests/installer_helpers.py` (`has_managed_marker`), `tests/conftest.py` (`tmp_home`, `tmp_dest`) from Plan 1.
- Produces: `install.sh` implementing §9 copy-mode behaviors: discover `bw-*` + deploy each as a unit; deploy `_bw-shared/` refs + `src/bwkit/` → `<dest>/_bw-shared/bwkit/`; managed marker on each top-level target; `--dest` override; idempotent re-runs; fail-closed on an unrelated existing target; staged replace.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_installer_copy.py
"""install.sh copy-mode behaviors (spec §9). Drives the script via subprocess against
isolated tmp_home / tmp_dest from Plan 1's conftest."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from installer_helpers import has_managed_marker

REPO = Path(__file__).resolve().parents[1]
INSTALL = REPO / "install.sh"


def _run(dest: Path, *extra) -> subprocess.CompletedProcess:
    env = {**os.environ}
    return subprocess.run(
        ["bash", str(INSTALL), "--dest", str(dest), "--src", str(REPO), *extra],
        capture_output=True, text=True, env=env)


def test_copy_deploys_all_skills_and_shared_with_markers(tmp_dest):
    r = _run(tmp_dest, "--copy")
    assert r.returncode == 0, r.stderr
    skills = sorted(p.name for p in (REPO / ".claude" / "skills").glob("bw-*"))
    installed = sorted(p.name for p in tmp_dest.glob("bw-*"))
    assert installed == skills
    for s in installed:
        assert has_managed_marker(tmp_dest / s), f"{s} missing marker"
    shared = tmp_dest / "_bw-shared"
    assert shared.is_dir() and has_managed_marker(shared)


def test_copy_deploys_runnable_bwkit(tmp_dest):
    assert _run(tmp_dest, "--copy").returncode == 0
    bwkit = tmp_dest / "_bw-shared" / "bwkit"
    assert (bwkit / "__main__.py").exists()
    env = {**os.environ, "PYTHONPATH": str(tmp_dest / "_bw-shared")}
    r = subprocess.run([sys.executable, "-m", "bwkit", "--help"],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    assert "lock" in r.stdout and "cas" in r.stdout


def test_copy_is_idempotent(tmp_dest):
    assert _run(tmp_dest, "--copy").returncode == 0
    r2 = _run(tmp_dest, "--copy")
    assert r2.returncode == 0, r2.stderr
    assert (tmp_dest / "bw-start" / "SKILL.md").exists()


def test_copy_fails_closed_on_unrelated_target(tmp_dest):
    stranger = tmp_dest / "bw-start"
    stranger.mkdir()
    (stranger / "SKILL.md").write_text("someone else's skill")
    r = _run(tmp_dest, "--copy")
    assert r.returncode != 0
    assert "not bewater-managed" in r.stderr
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_installer_copy.py -v`
Expected: FAIL — `install.sh` does not exist (subprocess fails).

- [ ] **Step 3: Write minimal implementation**

Create `install.sh`:

```bash
#!/usr/bin/env bash
# BeWater skill installer (spec §9). Ships self-contained bw-* skills plus the shared
# _bw-shared/ references and the bwkit helper package. Default mode is --copy.
set -euo pipefail

VERSION="0.1.0"
MARKER=".bewater-managed"
MODE="copy"
DEST=""
SRC=""
UNINSTALL=0
MARKER_JSON='{"managed_by":"bewater","version":"'"$VERSION"'"}'

die() { echo "error: $*" >&2; exit 1; }

usage() {
  cat <<EOF
usage: install.sh [--copy|--link] [--dest DIR] [--src DIR] [--uninstall]
  --copy       copy skills into DEST (default)
  --link       symlink skill contents + bwkit into DEST (repo development)
  --dest DIR   destination skills dir (default: \$HOME/.claude/skills)
  --src DIR    repository root with .claude/skills and src/bwkit (default: this script's dir)
  --uninstall  remove only bewater-managed targets from DEST
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy)       MODE="copy"; shift;;
    --link)       MODE="link"; shift;;
    --dest)       DEST="${2:?--dest needs a value}"; shift 2;;
    --src)        SRC="${2:?--src needs a value}"; shift 2;;
    --uninstall)  UNINSTALL=1; shift;;
    -h|--help)    usage; exit 0;;
    *)            die "unknown argument: $1";;
  esac
done

[[ -z "${SRC:-}" ]] && SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SRC/.claude/skills"
BWKIT_SRC="$SRC/src/bwkit"
[[ -d "$SKILLS_SRC" ]] || die "no .claude/skills under --src: $SRC"
[[ -d "$BWKIT_SRC" ]]  || die "no src/bwkit under --src: $SRC"

[[ -z "${DEST:-}" ]] && DEST="$HOME/.claude/skills"
mkdir -p "$DEST"

write_marker() { printf '%s\n' "$MARKER_JSON" > "$1/$MARKER"; }
has_marker()   { [[ -f "$1/$MARKER" ]]; }

# Replace a target from a staging dir, after verifying it is bewater-managed if it exists.
stage_replace() {
  local target="$1" staged="$2"
  if [[ -e "$target" || -L "$target" ]]; then
    has_marker "$target" || die "target exists and is not bewater-managed: $target"
  fi
  rm -rf "$target"
  mv "$staged" "$target"
  write_marker "$target"
}

deploy_unit() {
  local name="$1" srcdir="$SKILLS_SRC/$name"
  [[ -d "$srcdir" ]] || die "missing source unit: $name"
  local staged
  staged="$(mktemp -d "${TMPDIR:-/tmp}/bwinst.XXXXXX")"
  if [[ "$MODE" == "copy" ]]; then
    cp -R "$srcdir" "$staged/$name"
  else
    mkdir -p "$staged/$name"
    local f
    for f in "$srcdir"/*; do [[ -e "$f" ]] || continue; ln -s "$f" "$staged/$name/$(basename "$f")"; done
  fi
  stage_replace "$DEST/$name" "$staged/$name"
}

deploy_shared() {
  local staged
  staged="$(mktemp -d "${TMPDIR:-/tmp}/bwinst.XXXXXX")/_bw-shared"
  mkdir -p "$staged"
  local f
  for f in "$SKILLS_SRC/_bw-shared"/*.md; do
    [[ -e "$f" ]] || continue
    if [[ "$MODE" == "copy" ]]; then cp "$f" "$staged/"; else ln -s "$f" "$staged/$(basename "$f")"; fi
  done
  if [[ "$MODE" == "copy" ]]; then cp -R "$BWKIT_SRC" "$staged/bwkit"; else ln -s "$BWKIT_SRC" "$staged/bwkit"; fi
  stage_replace "$DEST/_bw-shared" "$staged"
}

uninstall_target() {
  local target="$1"
  if [[ ! -e "$target" && ! -L "$target" ]]; then return 0; fi
  if has_marker "$target" || [[ -L "$target" && ! -e "$target" ]]; then
    rm -rf "$target"
  else
    echo "skip (not bewater-managed): $target" >&2
  fi
}

main() {
  if (( UNINSTALL )); then
    local d
    for d in "$SKILLS_SRC"/*/; do
      [[ -d "$d" ]] || continue
      uninstall_target "$DEST/$(basename "$d")"
    done
    uninstall_target "$DEST/_bw-shared"
    echo "uninstalled bewater-managed skills from $DEST"
    return 0
  fi

  local units=() d
  for d in "$SKILLS_SRC"/bw-*/; do [[ -d "$d" ]] || continue; units+=("$(basename "$d")"); done
  [[ ${#units[@]} -gt 0 ]] || die "no bw-* skills found under $SKILLS_SRC"
  for name in "${units[@]}"; do deploy_unit "$name"; done
  deploy_shared
  echo "installed ${#units[@]} skill(s) + _bw-shared into $DEST (mode=$MODE)"
}

main "$@"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_installer_copy.py -v`
Expected: PASS (all 4).

- [ ] **Step 5: Commit**

```bash
git add install.sh tests/test_installer_copy.py
chmod +x install.sh
git commit -m "feat(installer): install.sh copy mode + bwkit/_bw-shared deploy + fail-closed"
```

---

## Task 10: install.sh — link mode + uninstall + repair

**Files:**
- Modify: `install.sh` (no code change needed — T9 already implements `--link` and `--uninstall`; this task adds test coverage and the broken-link-repair guarantee)
- Test: `tests/test_installer_link.py`

**Interfaces:**
- Produces: verified `--link` mode (per-file managed symlinks), `--uninstall` (removes only managed targets), and broken-managed-link repair (re-run redeploys).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_installer_link.py
"""install.sh link mode + uninstall + broken-link repair (spec §9)."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
INSTALL = REPO / "install.sh"


def _run(dest: Path, *extra) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(INSTALL), "--dest", str(dest), "--src", str(REPO), *extra],
        capture_output=True, text=True, env={**os.environ})


def test_link_mode_creates_managed_symlinks(tmp_dest):
    r = _run(tmp_dest, "--link")
    assert r.returncode == 0, r.stderr
    skill_md = tmp_dest / "bw-start" / "SKILL.md"
    assert skill_md.is_symlink()
    assert (tmp_dest / "bw-start" / ".bewater-managed").is_file()  # real marker, not link
    assert (tmp_dest / "_bw-shared" / "bwkit").is_symlink()


def test_link_repair_broken_content_symlink(tmp_dest):
    assert _run(tmp_dest, "--link").returncode == 0
    # break one content link
    broken = tmp_dest / "bw-start" / "SKILL.md"
    broken.unlink()
    os.symlink("/nonexistent/path", broken)
    assert _run(tmp_dest, "--link").returncode == 0, "redeploy should repair"
    assert (tmp_dest / "bw-start" / "SKILL.md").exists()


def test_uninstall_removes_only_managed(tmp_dest):
    assert _run(tmp_dest, "--copy").returncode == 0
    stranger = tmp_dest / "stranger-skill"
    stranger.mkdir()
    (stranger / "SKILL.md").write_text("not bewater")
    r = _run(tmp_dest, "--uninstall")
    assert r.returncode == 0, r.stderr
    assert not (tmp_dest / "bw-start").exists()
    assert not (tmp_dest / "_bw-shared").exists()
    assert stranger.exists(), "uninstall must not touch unrelated skills"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_installer_link.py -v`
Expected: link-mode + repair tests should PASS against the T9 script; the **repair** test is the discriminating guarantee — if `stage_replace` did not reuse managed status correctly it would fail. If all pass immediately, the implementation already satisfies §9 link/uninstall; the task's value is locking the behavior with tests. (If `test_link_repair_broken_content_symlink` fails, fix `deploy_unit` so a redeploy over an existing managed target replaces broken content symlinks — the T9 `stage_replace` already does this via `has_marker` on the real target dir.)

- [ ] **Step 3: Harden if needed**

If any link/uninstall test failed in Step 2, the likely cause is the broken-symlink branch. Ensure `deploy_unit`/`stage_replace` treat a target dir whose `.bewater-managed` marker is intact as managed even when individual content symlinks are broken — the T9 implementation already removes and re-creates the whole target, so no edit is normally required. If you did edit `install.sh`, re-run the test.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_installer_link.py -v`
Expected: PASS (all 3).

- [ ] **Step 5: Commit**

```bash
git add tests/test_installer_link.py
git commit -m "test(installer): cover link mode, uninstall, broken-link repair (§9)"
```

---

## Task 11: scripts/verify + Phase 1a acceptance

**Files:**
- Create: `scripts/verify.py`
- Modify: `pyproject.toml` (pytest `pythonpath` += `"scripts"`)
- Test: `tests/test_verify.py`

**Interfaces:**
- Consumes: `tests/skill_helpers.py` (`validate_skill`, `validate_skill_evals`), `install.sh`.
- Produces: `scripts/verify.py` — importable module `verify` implementing the §11.3 authoring-time checks (skill existence + frontmatter, references + contracts, no placeholders, scenario manifests, local discovery, installer smoke). `main()` runs all checks and exits non-zero on any failure. Each check function takes explicit roots so tests can drive fixtures.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_verify.py
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import pytest

REPO = Path(__file__).resolve().parents[1]


def _make_repo(tmp_path: Path, good: bool = True) -> Path:
    repo = tmp_path / "repo"
    skills = repo / ".claude" / "skills"
    sk = skills / "bw-x"
    sk.mkdir(parents=True)
    fm = "---\nname: bw-x\ndescription: Use when the user wants to x.\n---\n# x\n"
    sk.joinpath("SKILL.md").write_text(fm if good else fm.replace("Use when", "Trigger"))
    ev = repo / "evals" / "bw-x"
    ev.mkdir(parents=True)
    manifest = (lambda rid: dedent(f"""\
        scenario_id: {rid}
        target_skill: bw-x
        prompt: hi
        required_assertions: [a]
        forbidden_behaviors: []
        repetition_count: 1
        """))
    (ev / "scenarios").mkdir()
    (ev / "scenarios" / "s.yaml").write_text(manifest("S-1"))
    (ev / "red").mkdir()
    (ev / "red" / "r.yaml").write_text(manifest("R-1"))
    return repo


def test_list_and_check_skill_good(tmp_path):
    from verify import check_skill, list_skills
    repo = _make_repo(tmp_path, good=True)
    assert list_skills(repo / ".claude" / "skills") == ["bw-x"]
    ok, details = check_skill("bw-x", repo / ".claude" / "skills", repo / "evals")
    assert ok, details


def test_check_skill_bad_frontmatter(tmp_path):
    from verify import check_skill
    repo = _make_repo(tmp_path, good=False)
    ok, details = check_skill("bw-x", repo / ".claude" / "skills", repo / "evals")
    assert not ok
    assert any("validate_skill" in d for d in details)


def test_check_local_discovery(tmp_path):
    from verify import check_local_discovery
    repo = _make_repo(tmp_path, good=True)
    ok, _ = check_local_discovery(repo / ".claude" / "skills")
    assert ok


def test_check_installer_runs_against_real_repo(tmp_home, tmp_dest):
    from verify import check_installer
    ok, details = check_installer(REPO, tmp_dest)
    assert ok, details
    assert (tmp_dest / "bw-start").exists()


def test_main_exits_nonzero_on_violation(tmp_path, monkeypatch):
    from verify import main
    repo = _make_repo(tmp_path, good=False)
    monkeypatch.setattr("verify._REPO", repo)
    monkeypatch.setattr("verify.SKILLS", repo / ".claude" / "skills")
    monkeypatch.setattr("verify.EVALS", repo / "evals")
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code != 0
```

- [ ] **Step 2: Run test to verify it fails**

First add `"scripts"` to the pytest pythonpath in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
pythonpath = ["src", ".", "scripts"]
```

Run: `pytest tests/test_verify.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'verify'`.

- [ ] **Step 3: Write minimal implementation**

Create `scripts/verify.py`:

```python
"""scripts/verify — authoring-time integrity checks (spec §11.3). Not shipped.
Importable as `verify` (pytest pythonpath includes "scripts"). Each check returns
(ok, details); main() runs them all and exits non-zero on any failure."""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_REPO / "tests"))
from skill_helpers import (  # noqa: E402
    SkillCheckError,
    validate_skill,
    validate_skill_evals,
)

SKILLS = _REPO / ".claude" / "skills"
EVALS = _REPO / "evals"
_PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME|XXX)\b")


def list_skills(skills_root=None) -> list[str]:
    skills_root = SKILLS if skills_root is None else Path(skills_root)
    return sorted(p.name for p in skills_root.glob("bw-*") if p.is_dir())


def check_skill(name, skills_root=None, evals_root=None):
    skills_root = SKILLS if skills_root is None else Path(skills_root)
    evals_root = EVALS if evals_root is None else Path(evals_root)
    details: list[str] = []
    try:
        validate_skill(Path(skills_root) / name)
    except SkillCheckError as e:
        details.append(f"validate_skill: {e}")
    try:
        validate_skill_evals(Path(evals_root), name)
    except SkillCheckError as e:
        details.append(f"validate_skill_evals: {e}")
    return (not details, details)


def check_placeholders(skills_root=None):
    skills_root = SKILLS if skills_root is None else Path(skills_root)
    bad = [str(p) for p in skills_root.rglob("*.md") if _PLACEHOLDER_RE.search(p.read_text())]
    return (not bad, bad)


def check_local_discovery(skills_root=None):
    skills_root = SKILLS if skills_root is None else Path(skills_root)
    missing = [n for n in list_skills(skills_root) if not (skills_root / n / "SKILL.md").exists()]
    return (not missing, missing)


def check_installer(repo=None, dest=None):
    """Run install.sh --copy into an isolated dest; assert managed markers + bwkit runs."""
    repo = _REPO if repo is None else Path(repo)
    dest = Path(dest) if dest else Path(tempfile.mkdtemp(prefix="bwverify-"))
    install = Path(repo) / "install.sh"
    if not install.exists():
        return (False, [f"missing {install}"])
    r = subprocess.run(
        ["bash", str(install), "--dest", str(dest), "--src", str(repo), "--copy"],
        capture_output=True, text=True)
    if r.returncode != 0:
        return (False, [f"installer failed: {r.stderr.strip()}"])
    for name in list_skills(Path(repo) / ".claude" / "skills"):
        if not (dest / name / ".bewater-managed").exists():
            return (False, [f"{name} missing managed marker"])
    env = {**os.environ, "PYTHONPATH": str(dest / "_bw-shared")}
    rr = subprocess.run([sys.executable, "-m", "bwkit", "--help"],
                        capture_output=True, text=True, env=env)
    if rr.returncode != 0:
        return (False, [f"deployed bwkit not runnable: {rr.stderr.strip()}"])
    return (True, [])


def main() -> None:
    failures: list[str] = []
    names = list_skills()
    if not names:
        failures.append("no bw-* skills found")
    for name in names:
        ok, details = check_skill(name)
        if not ok:
            failures.extend(f"{name}: {d}" for d in details)
    for label, result in [
        ("placeholders", check_placeholders()),
        ("local-discovery", check_local_discovery()),
        ("installer", check_installer()),
    ]:
        ok, details = result
        if not ok:
            failures.extend(f"{label}: {d}" for d in details)
    for f in failures:
        print(f"FAIL {f}", file=sys.stderr)
    print(f"verified {len(names)} skill(s)" if not failures else f"{len(failures)} failure(s)")
    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes, then enforce ≥80% coverage**

Run: `pytest tests/test_verify.py -v` — Expected: PASS.

Then enforce the §11.3 authoring-utility coverage floor for `verify`:

Run: `pytest --cov=verify --cov-fail-under=80 tests/test_verify.py`
Expected: PASS at ≥80%. If short, add a test for `check_placeholders` (seed a TODO into a fixture skill) — do not weaken the gate.

- [ ] **Step 5: Commit**

```bash
git add scripts/verify.py tests/test_verify.py pyproject.toml
git commit -m "feat(verify): scripts/verify authoring-time checks (§11.3) + 80% gate"
```

- [ ] **Step 6: Phase 1a acceptance gate**

Run the full suite and the verify script:

```bash
pytest -q
pytest --cov=bw --cov=bwkit --cov-fail-under=80 -q
python scripts/verify.py
```

Expected: all green; `scripts/verify.py` prints `verified 7 skill(s)` (bw-start, bw-immersion, bw-discover, bw-define, bw-project-charter, bw-4c-research, bw-insight-craft) and exits 0.

Document the deferred gate. Append to `evals/README.md` (create if absent):

```markdown
# BeWater evals

Phase 1a authors **scenario manifests** (`<skill>/scenarios/`) and **RED controls**
(`<skill>/red/`) only. The fresh-context LLM GREEN runs (spec §11.1 — 3 repetitions, 5/5
for safety-critical) are the **deferred Phase-1 acceptance gate** and are executed in a
separate pass once the Phase 1b G1 closed loop is in place. Structural correctness is
covered now by `scripts/verify.py` and the per-skill pytest; state-write correctness rides
on the Plan-1 `bwkit` CAS.
```

```bash
git add evals/README.md
git commit -m "docs(eval): document Phase 1a manifest-only scope + deferred LLM gate"
```

---

## Self-Review

**1. Spec coverage (Plan 2a scope = §10.3 Phase 1 first half + §9 installer + §11.3 verify):**
- §10.3 bw-start → Task 2 ✓
- §10.3 bw-immersion / bw-discover / bw-define routers → Tasks 3/4/5 ✓
- §10.3 bw-project-charter / bw-4c-research / bw-insight-craft capabilities → Tasks 6/7/8 ✓
- §10.3 skill-local references → every skill task carries its `references/` ✓
- §10.3 installer → Tasks 9/10 ✓
- §11.3 verify (skills exist + frontmatter; references + contracts; no placeholders; scenarios; local discovery; installer smoke) → Task 11 ✓
- §4 routing precedence / human convergence / no-artifact routers → embedded in SKILL.md bodies + Global Constraints ✓
- §5.7 direct-write via bwkit → cited in bw-start routing.md + capability skills; mechanism tested in Plan 1 ✓
- §2.3 shared references cited, not duplicated → skills cite `../_bw-shared/*` ✓
- §11.3 authoring-utility ≥80% coverage → `verify` covered in Task 11 ✓

**Deferred (out of Plan 2a, by design — decision 2026-07-29):**
- The four Define capabilities (bw-directional-hypothesis, bw-strategy-statement, bw-opportunity-area, bw-assumption-map), the bwkit action-plan applier, bw-strategy-gate, and the full G1 closed-loop acceptance → **Plan 2b**.
- Fresh-context LLM GREEN runs (§11.1) → Phase-1 acceptance gate, documented in `evals/README.md` (Task 11).
- `scripts/verify` "all 19 skills" count → it scans `bw-*` dynamically, so it stays correct as 2b adds skills.

**2. Placeholder scan:** none. Every step carries real test code, real SKILL.md/reference content, a complete `install.sh`, and a complete `verify.py`. (Task 10's Step 3 is conditional hardening, not a placeholder — the T9 script already implements the behavior; the task locks it with tests.)

**3. Type consistency:**
- `validate_skill(skill_dir: Path)` / `validate_skill_evals(evals_root: Path, name: str)` / `skill_dir(repo, name)` / `SkillCheckError` — defined T1, used T2–T8 and T11 ✓
- `verify.list_skills / check_skill / check_placeholders / check_local_discovery / check_installer / main` — defined T11, used T11 ✓
- `has_managed_marker` / `tmp_home` / `tmp_dest` — from Plan 1, consumed T9–T11 ✓
- `_bw-shared/` contract names (`bw-ledger-schema`, `bw-gate-criteria`, `bw-glossary`) — created Plan 1, cited T2–T8 ✓
- bwkit CLI (`lock acquire`, `cas commit <path> --expected <rev>`; `python -m bwkit`) — from Plan 1 §12.5, cited T2/T9/T11 ✓

**4. Scope check:** Plan 2a is one cohesive deliverable (G1 spine + installer + verify) with its own testable acceptance; the remaining G1 loop is cleanly separable into Plan 2b along the Define-capability seam.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-07-29-bw-phase1a-g1-spine-installer.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch with checkpoints.

**Which approach?** (Plan 2b — Define capabilities + bwkit applier + bw-strategy-gate — is written once Plan 2a lands and the G1 spine + installer + verify are green.)
