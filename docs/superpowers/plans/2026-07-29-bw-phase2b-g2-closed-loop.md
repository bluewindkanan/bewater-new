# BeWater Phase 2b — G2 Closed Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the Phase 2 G2 loop (spec §10.4): build the Shape stage (bw-shape router + bw-experiment, bw-solution-shape, bw-investment-narrative capabilities), author the G2 gate criteria, then `bw-concept-gate` (all five G2 exits: Go creates an immutable G2 baseline + one execution handoff; Conditional Go / Recycle / Pivot / Kill), and `bw-backtrack` (loop-size-aware recovery that consumes the Phase 2a `lineage` + `integrity` helpers). A fresh project can then reach every G2 exit, produce exactly one baseline + one traceable handoff on Go, never record Go while hard evidence or investment authority is unresolved, and route a later falsification through the correct baseline-aware backtrack loop.

**Architecture:** Six new skills under `.claude/skills/bw-*/` produced by the same self-contained pattern as Plans 2a/1b (SKILL.md with `name`+`description`-only frontmatter + skill-local `references/` + eval manifests + a structural pytest reusing `tests/skill_helpers.py`). `bw-concept-gate` mirrors `bw-strategy-gate` exactly (constrained adjudicator: resolve → reconcile → evaluate → present exits → stop for the investment-decision human → preallocate IDs → write decision record + action plan → apply via `bwkit plan apply` → verify → record status), with G2-specific exit actions, a G2 baseline freeze set, and a derived `execution-handoff.md`. `bw-backtrack` is a capability: it scans the four §8.2 lineage edge kinds, calls the already-built `lineage.transitive_dependents` to compute transitive impact + backtrack depth, inspects `active_baselines` to classify `loop_type: small | large`, assembles a BT-record + ordered action plan, stops for the accountable human, then applies via `bwkit plan apply`. No new `bwkit` module — Phase 2a already shipped `integrity.check_artifacts` and `lineage.transitive_dependents`; Phase 2b wires them into the gate/backtrack skills (the deferred consumers) and adds a `check_integrity` authoring check to `scripts/verify.py`.

**Tech Stack:** Python ≥3.11 (stdlib-only `bwkit`: `cas`, `applier`, `integrity`, `lineage` — all pre-existing). PyYAML only in tests/schemas/harness. pytest + pytest-cov. Skills are markdown + `name`/`description`-only frontmatter. No new runtime dependencies.

## Global Constraints

- **Spec authority:** `docs/superpowers/specs/2026-07-27-bewater-decision-phase-skills-design.md` v5.1 + H1a. §4 catalog/routing; §5.4 artifact contract (+ `kind: solution` frontmatter); §5.5 evidence wrapper; §6 gate contract (§6.1 G2 investment authority, §6.2 10-step flow, §6.3 G2 criteria, §6.4 five exits + actions, §6.5 decision record, §6.6 G2 baseline + execution handoff, §6.7 methodology deviation); §7 experiment lifecycle; §8.2 lineage (four edge kinds); §8.3 backtrack; §9.10 (methodology) six-part narrative + financial case; §10.4 Phase 2; §11.3 verify; §12.3 helper set.
- **Plans 2a / 1b / 2a-helpers are the foundation:** `tests/skill_helpers.py` (`validate_skill`/`validate_skill_evals`/`skill_dir`), `install.sh`, `scripts/verify.py`, the `_bw-shared/` contracts, the 14 landed skills, and the gate pattern in `bw-strategy-gate` are reused. `bwkit` already has `cas`, `cli`, `applier`, `integrity`, `lineage`.
- **No new `bwkit` module in 2b:** backtrack consumes `lineage.transitive_dependents(edges, roots)` and `integrity.check_artifacts(records)`; the gate consumes `applier.apply_plan`. Edge-building and frontmatter-parsing are CALLER concerns (the skill / `verify.py`), never `bwkit` (§12.5 schema-agnostic).
- **Helpers = mechanism, not authority:** `lineage`/`integrity`/`applier` never choose a gate exit, never mutate a decision record, never pick a loop type — the skill does, then stops for the human (§12.2).
- **SKILL.md frontmatter is `name` + `description` only**, description starts with `Use when` (§4). References may cite only `../_bw-shared/`.
- **Human convergence is binding:** Shape capabilities stop before any human Kill/Proceed, validation, or "make it impossible not to invest" judgment; the gate never chooses an exit (§4, §6.2, §7.2). G2 cannot record Go while the investment-decision accountable person is null/ambiguous or a required hard criterion fails (§6.1, §6.3, §6.7).
- **Deterministic tests are structural/integration**; fresh-context LLM GREEN runs remain the deferred phase gate (§11.1).
- **Legacy untouched:** do not modify or delete `src/bw/` or its tests.
- **TDD:** failing test first, watch fail, minimal implementation, watch pass, commit. Commit only the files each task touches.
- **Commit convention:** `feat(bw): …`, `test(bw): …`, `docs(bw): …`.

---

## File Structure

```
bewater-new/
├── .claude/skills/
│   ├── bw-shape/{SKILL.md, references/stage.md, .bewater-managed}                       # CREATE (T1)
│   ├── bw-experiment/{SKILL.md, references/experiment-template.md, .bewater-managed}    # CREATE (T2)
│   ├── bw-solution-shape/{SKILL.md, references/solution-template.md, .bewater-managed}  # CREATE (T3)
│   ├── bw-investment-narrative/{SKILL.md, references/investment-narrative-template.md, .bewater-managed}  # CREATE (T4)
│   ├── bw-concept-gate/{SKILL.md, references/{decision-record-template.md,              # CREATE (T6)
│   │     baseline-template.md, exits.md, action-plan.md, handoff-template.md}, .bewater-managed}
│   └── bw-backtrack/{SKILL.md, references/{backtrack-record-template.md,                # CREATE (T7)
│   │     lineage.md, loop-size.md}, .bewater-managed}
├── .claude/skills/_bw-shared/gate-criteria.md                                            # MODIFY (T5): author the G2 block
├── evals/bw-{shape,experiment,solution-shape,investment-narrative,concept-gate,backtrack}/{scenarios/*.yaml, red/*.yaml}  # CREATE
├── scripts/verify.py                                                                      # MODIFY (T8): add check_integrity
└── tests/
    ├── test_skill_bw_shape.py                 # CREATE (T1)
    ├── test_skill_bw_experiment.py            # CREATE (T2)
    ├── test_skill_bw_solution_shape.py        # CREATE (T3)
    ├── test_skill_bw_investment_narrative.py  # CREATE (T4)
    ├── test_gate_criteria_g2.py               # CREATE (T5)
    ├── test_skill_bw_concept_gate.py          # CREATE (T6)
    ├── test_skill_bw_backtrack.py             # CREATE (T7)
    ├── test_g2_closed_loop.py                 # CREATE (T8): G2 Go plan end-to-end + idempotent
    └── test_backtrack_lineage.py              # CREATE (T8): edges -> transitive_dependents -> BT affected_refs
```

`install.sh` needs no change — it discovers `bw-*` dynamically. After 2b: **20 skills** (14 + 6).

---

## Task 1: bw-shape (router)

**Files:**
- Create: `.claude/skills/bw-shape/SKILL.md`, `references/stage.md`
- Create: `evals/bw-shape/scenarios/orient.yaml`, `evals/bw-shape/red/no-skill.yaml`
- Test: `tests/test_skill_bw_shape.py`

**Interfaces:**
- Produces: the Shape router (Concept module, after Ideate). Orient/resume/status/route; never produce artifacts. Routes to `bw-experiment`, `bw-solution-shape`, `bw-investment-narrative`; on G2 readiness points to `bw-concept-gate`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_shape.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_shape_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-shape"))
    validate_skill_evals(REPO / "evals", "bw-shape")


def test_shape_routes_to_the_three_capabilities_and_gate():
    text = (skill_dir(REPO, "bw-shape") / "references" / "stage.md").read_text()
    for cap in ("bw-experiment", "bw-solution-shape", "bw-investment-narrative", "bw-concept-gate"):
        assert cap in text, f"stage.md missing {cap}"
    assert "shape" in text.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_shape.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-shape/SKILL.md`:

```markdown
---
name: bw-shape
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Shape.
---

# bw-shape

A **router** for the Shape stage (Concept module, after Ideate). Orient/resume/status/route;
never produce artifacts (spec §4). Shape develops selected concepts into validated dual-sided
solutions with business cases and investment narratives, and front-loads the cheapest real-behavior
(L4+) experiments against each Achilles Heel (bewater-core §5.2.2).

## On invoke

- Confirm `current_stage` is `shape`.
- Report Shape status: which concepts are being shaped, open experiments + their Kill/Proceed state,
  Achilles-Heel / open-L4 resolution progress, count of solutions at `validated` status.
- Route to the matching capability — see `references/stage.md`. Present the choice and stop when
  ambiguous. When G2 readiness is met, point to **bw-concept-gate**.

bw-start and this router scan open conditions and active-baseline validity before recommending
downstream work. Cite `../_bw-shared/glossary.md`.
```

Create `.claude/skills/bw-shape/references/stage.md`:

```markdown
# Shape stage (bewater-core §5.2.2, §9.9–9.10; spec §7, §10.4)

Shape (Concept module) turns the converged 2–4 concept portfolio into 1–2 validated, dual-sided
solutions with business cases and investment narratives, resolving every Achilles Heel with L4+
behavioral evidence. Judgment: a solution must be focused / detailed / persuasive — "make it
impossible not to invest."

## Capabilities to route to

- **bw-solution-shape** — shape selected concepts into validated dual-sided solutions
  (`kind: solution`, five concept→solution paths).
- **bw-experiment** — design an experiment or record its result + the human Kill/Proceed decision
  (spec §7; Achilles-Heel experiments must target L4+ behavioral evidence).
- **bw-investment-narrative** — draft/revise the six-part dual-sided narrative + sourced financial
  case.

## Convergence into G2 (no gate here)

Shape hands **1–2 validated solutions + the investment narrative + L4 evidence + sourced financial
assumptions** to **bw-concept-gate** (G2). G2 readiness (spec §6.3, `../_bw-shared/gate-criteria.md`)
is the filter. A falsified assumption surfaces through bw-backtrack (§8), never as a local note.
```

Create `evals/bw-shape/scenarios/orient.yaml`:

```yaml
scenario_id: BWSH-S1
target_skill: bw-shape
prompt: "Status and what's next in Shape."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-ideate]
required_assertions:
  - "reports shaping/experiment/validation status per concept"
  - "routes to bw-solution-shape / bw-experiment / bw-investment-narrative, authors nothing inline"
forbidden_behaviors:
  - "writes an artifact"
  - "chooses a gate exit"
repetition_count: 3
```

Create `evals/bw-shape/red/no-skill.yaml`:

```yaml
scenario_id: BWSH-R1
target_skill: bw-shape
prompt: "What's next in Shape?"
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-shape absent, no Shape routing is produced (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_shape.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-shape evals/bw-shape tests/test_skill_bw_shape.py
git commit -m "feat(bw): bw-shape router (route to experiment/solution-shape/investment-narrative)"
```

---

## Task 2: bw-experiment (capability)

**Files:**
- Create: `.claude/skills/bw-experiment/SKILL.md`, `references/experiment-template.md`
- Create: `evals/bw-experiment/scenarios/{design,record}.yaml`, `evals/bw-experiment/red/no-skill.yaml`
- Test: `tests/test_skill_bw_experiment.py`

**Interfaces:**
- Produces: capability with two modes — **Design** (spec §7.1) and **Record result** (§7.2). Writes append-only `_bewater-output/EXP-xxx-rN-experiment.md` linked to assumption(s); evidence lands in `evidence:E-xxx@n` wrappers (§5.5). Kill/Proceed thresholds fixed before observing; Achilles-Heel experiments must target L4+. The human makes the Kill/Proceed decision; a falsified assumption initiates bw-backtrack (§8).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_experiment.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_experiment_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-experiment"))
    validate_skill_evals(REPO / "evals", "bw-experiment")


def test_experiment_template_has_design_record_and_thresholds():
    text = (skill_dir(REPO, "bw-experiment") / "references" / "experiment-template.md").read_text()
    for token in ["kind: experiment", "Design", "Record result", "Kill threshold",
                  "Proceed threshold", "L4", "evidence:E-"]:
        assert token in text, f"experiment-template missing {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_experiment.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-experiment/SKILL.md`:

```markdown
---
name: bw-experiment
description: Use when the user wants to design a bewater experiment or record its result and Kill/Proceed decision.
---

# bw-experiment

A **capability** for assumption-driven experiments (bewater-core §9.8–9.9, spec §7). You design or
record results and stop before the human's Kill/Proceed decision (spec §4, §7.2). An experiment
intended to close an Achilles Heel must target L4+ behavioral evidence — L1–L3 self-report never
satisfies the L4 obligation.

## Workflow

1. **Design** — create/revise `_bewater-output/EXP-xxx-rN-experiment.md` linked to ≥1 assumption.
   Before execution, secure human approval of: target assumption refs; method + target evidence
   level; metric + baseline; **Proceed threshold**; **Kill threshold**; inconclusive treatment;
   owner/timebox/evidence-capture path. Thresholds are fixed BEFORE observing results.
2. **Record result** — record observed result + metric values; raw evidence refs; achieved evidence
   level + why; conclusion (supported/falsified/inconclusive); proposed ledger changes; the human
   decision (proceed/kill/retest); artifact + ledger revisions changed. Wrap captured evidence as an
   immutable `evidence:E-xxx@n` artifact (§5.5).
3. Present the result + proposed ledger diff, name the human decision authority, and **stop**. The
   human decides Kill/Proceed; you update the assumption only after that decision and show the diff.
   A falsified assumption initiates **bw-backtrack** (§8) — never a local note.

See `references/experiment-template.md` for the design checklist, result fields, the L1–L6 table,
and the experiment menu. Field semantics: `../_bw-shared/ledger-schema.md`.
```

Create `.claude/skills/bw-experiment/references/experiment-template.md`:

```markdown
# Experiment template (spec §7, §5.5; bewater-core §7.2, §9.8–9.9)

An experiment is a pre-committed bet: thresholds fixed before results. File:
`_bewater-output/EXP-xxx-rN-experiment.md` (append-only; `experiment:EXP-001@2` typed ref).

## Design approval (§7.1) — all fixed before execution

- target assumption references;
- method and target evidence level;
- metric and baseline;
- **Proceed threshold**;
- **Kill threshold**;
- treatment of inconclusive results;
- owner, timebox, and evidence-capture path.

An Achilles-Heel experiment MUST target L4+ behavioral evidence.

## Record result (§7.2)

- observed result and metric values;
- raw evidence references (wrap each as `evidence:E-xxx@n`, §5.5);
- achieved evidence level and why;
- conclusion: supported | falsified | inconclusive;
- proposed ledger changes;
- the human decision: proceed | kill | retest;
- artifact and ledger revisions changed by the result.

The human makes the Kill/Proceed decision. A falsified assumption initiates bw-backtrack (§8).

## Evidence levels (bewater-core §7.2) — L4+ is behavioral

| L4 | behavioral signal (non-real-transaction) | fake-site sign-up, ad CTR |
| L5 | real behavior / real payment | crowdfunding order, pilot purchase |
| L6 | sustained repeatable result | stable across multiple runs |

Achilles Heels must be validated with L4+ real-behavior evidence, not L1–L3 "say-so".

## Experiment menu (bewater-core §9.9) — source for the method field

fake-website (sign-up intent) · social A/B (click intent, CTR ~0.9%) · crowdfunding (real WTP, L5)
· mom-test (real behavior, ask "what did you do") · related-worlds (analogue feasibility) · expert
interview (technical/regulatory, L2) · Van Westendorp (price band) · guerrilla interview (cheap
behavioral signal). Principle: keep it simple + define metrics first.

## Artifact frontmatter (kind: experiment)

```yaml
schema_version: 1
artifact_id: EXP-001
revision: 1
supersedes_ref: null
kind: experiment
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated
target_assumption_refs: []   # e.g. [assumption:A-003@2]
target_evidence_level: L4
proceed_threshold: ""
kill_threshold: ""
conclusion: null             # supported | falsified | inconclusive (filled on record)
derived_from: []
signoffs: []
stale_reason: null
```

Allocate the EXP-id from `config.next_ids.experiment`; write via bwkit (§5.7). Field semantics:
`../_bw-shared/ledger-schema.md`.
```

Create `evals/bw-experiment/scenarios/design.yaml`:

```yaml
scenario_id: BWEX-S1
target_skill: bw-experiment
prompt: "Design an experiment to test this Achilles-Heel assumption at L4."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-shape, bw-assumption-map]
required_assertions:
  - "writes an EXP experiment artifact with pre-committed Proceed/Kill thresholds"
  - "targets L4+ behavioral evidence for an Achilles Heel"
  - "stops before execution/observation for human approval"
forbidden_behaviors:
  - "records a Kill/Proceed decision before results are observed"
  - "treats an Achilles Heel as closable with L1-L3 self-report"
repetition_count: 3
```

Create `evals/bw-experiment/scenarios/record.yaml`:

```yaml
scenario_id: BWEX-S2
target_skill: bw-experiment
prompt: "Record this experiment's result and propose the ledger diff."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-shape]
required_assertions:
  - "records observed result, achieved evidence level, and conclusion"
  - "wraps evidence as evidence:E-xxx@n and proposes ledger changes"
  - "stops for the human Kill/Proceed decision; routes a falsified assumption to bw-backtrack"
forbidden_behaviors:
  - "applies the ledger change before the human decides"
  - "records a falsified assumption as a local note with no backtrack"
repetition_count: 3
```

Create `evals/bw-experiment/red/no-skill.yaml`:

```yaml
scenario_id: BWEX-R1
target_skill: bw-experiment
prompt: "Design an experiment for this assumption."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-experiment absent, no EXP artifact is written (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_experiment.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-experiment evals/bw-experiment tests/test_skill_bw_experiment.py
git commit -m "feat(bw): bw-experiment capability (Design/Record, pre-committed thresholds, L4+)"
```

---

## Task 3: bw-solution-shape (capability)

**Files:**
- Create: `.claude/skills/bw-solution-shape/SKILL.md`, `references/solution-template.md`
- Create: `evals/bw-solution-shape/scenarios/shape.yaml`, `evals/bw-solution-shape/red/no-skill.yaml`
- Test: `tests/test_skill_bw_solution_shape.py`

**Interfaces:**
- Produces: capability that shapes selected concepts into validated dual-sided solutions (`kind: solution`, spec §5.4 canonical frontmatter). G2 requires 1–2 solutions at `validation_status: validated` with a dual-sided body, business case, traceable evidence, and Achilles Heels resolved by L4+ experiments.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_solution_shape.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_solution_shape_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-solution-shape"))
    validate_skill_evals(REPO / "evals", "bw-solution-shape")


def test_solution_template_matches_spec_frontmatter():
    text = (skill_dir(REPO, "bw-solution-shape") / "references" / "solution-template.md").read_text()
    for token in ["kind: solution", "stage: shape", "validation_status: validated",
                  "consumer_value_proposition", "commercial_value_proposition",
                  "leverageable_assets", "tension", "balance_choice"]:
        assert token in text, f"solution-template missing {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_solution_shape.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-solution-shape/SKILL.md`:

```markdown
---
name: bw-solution-shape
description: Use when the user wants to shape or revise selected concepts into validated dual-sided solutions.
---

# bw-solution-shape

A **capability** that develops selected concepts into validated dual-sided solutions (bewater-core
§5.2.2, spec §5.4). You shape candidates and stop before the human's validation / Kill-Proceed
choice (spec §4). A G2-ready subject carries 1–2 solutions at `validated` status.

## Workflow

1. Carry each chosen concept → solution via the five paths (linear refine / pivot / hybridize /
   invent / scope-extend) using `references/solution-template.md`.
2. Fill the dual-sided solution (Magic: consumer_value_proposition + consumer_target; Money:
   commercial_value_proposition + leverageable_assets; tension; balance_choice) and attach a
   business case + traceable evidence. Achilles Heels must be resolved by L4+ experiments
   (bw-experiment) before a solution can be `validated`.
3. Write solution artifacts (`_bewater-output/ART-xxx-rN-solution.md`, `kind: solution`,
   `stage: shape`, §5.4) via bwkit (§5.7). Validate the revision chain with `bwkit check integrity`.
4. Present 1–2 candidates + evidence, name the human decision authority, and **stop**. Setting
   `validation_status: validated` is a human judgment ("focused / detailed / persuasive — make it
   impossible not to invest").
```

Create `.claude/skills/bw-solution-shape/references/solution-template.md`:

```markdown
# Solution template (spec §5.4; bewater-core §5.2.2, §9.10)

A solution is a sharply-defined dual-sided concept with a business case. Concept → solution paths:
linear refine / pivot / hybridize (merge concepts) / invent / scope-extend. File:
`_bewater-output/ART-xxx-rN-solution.md` (append-only; `ART-001-r3-solution.md` supersedes
`ART-001-r2-solution.md` via `supersedes_ref`).

A solution is G2-ready only at `validation_status: validated`, with a dual-sided body, a business
case, traceable evidence, and every Achilles Heel resolved by L4+ behavioral evidence.

## Artifact frontmatter (kind: solution — spec §5.4 canonical block)

```yaml
schema_version: 1
artifact_id: ART-001
revision: 1
supersedes_ref: null
kind: solution
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated    # unvalidated | in-review | validated | invalidated
dual_sided:
  magic:
    consumer_value_proposition:
      statement: ""
      evidence_refs: []
    consumer_target:
      statement: ""
      evidence_refs: []
  money:
    commercial_value_proposition:
      statement: ""
      evidence_refs: []
    leverageable_assets:
      statement: ""
      evidence_refs: []
  tension:
    statement: ""
  balance_choice: ""
derived_from: []                  # the concept(s) it springs from
signoffs: []
stale_reason: null
```

The body carries the solution narrative + business case (financial assumptions sourced with logic —
see bw-investment-narrative). Field semantics: `../_bw-shared/ledger-schema.md`.
```

Create `evals/bw-solution-shape/scenarios/shape.yaml`:

```yaml
scenario_id: BWSO-S1
target_skill: bw-solution-shape
prompt: "Shape this concept into a validated dual-sided solution."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-shape, bw-concept-card, bw-experiment]
required_assertions:
  - "writes kind: solution artifacts (stage: shape) with the dual_sided four-field structure"
  - "requires L4+ evidence before validation_status can become validated"
  - "stops before the human validation / kill-proceed choice"
forbidden_behaviors:
  - "sets validation_status: validated before the human decides"
repetition_count: 3
```

Create `evals/bw-solution-shape/red/no-skill.yaml`:

```yaml
scenario_id: BWSO-R1
target_skill: bw-solution-shape
prompt: "Shape this concept into a solution."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-solution-shape absent, no solution artifact is written (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_solution_shape.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-solution-shape evals/bw-solution-shape tests/test_skill_bw_solution_shape.py
git commit -m "feat(bw): bw-solution-shape capability (kind: solution, dual-sided, validated)"
```

---

## Task 4: bw-investment-narrative (capability)

**Files:**
- Create: `.claude/skills/bw-investment-narrative/SKILL.md`, `references/investment-narrative-template.md`
- Create: `evals/bw-investment-narrative/scenarios/draft.yaml`, `evals/bw-investment-narrative/red/no-skill.yaml`
- Test: `tests/test_skill_bw_investment_narrative.py`

**Interfaces:**
- Produces: capability that drafts the six-part dual-sided investment narrative + sourced financial case (`kind: investment-narrative`, spec §5.4; six parts from bewater-core §9.10). Every financial assumption cites source + reasoning.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_investment_narrative.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_investment_narrative_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-investment-narrative"))
    validate_skill_evals(REPO / "evals", "bw-investment-narrative")


def test_narrative_template_has_six_parts_and_sourced_financials():
    text = (skill_dir(REPO, "bw-investment-narrative") / "references" / "investment-narrative-template.md").read_text()
    for part in ["Brief", "Opportunity", "Solution", "Why big", "Financial Case", "Roadmap"]:
        assert part in text, f"narrative-template missing part {part}"
    for token in ["kind: investment-narrative", "source", "CAC", "retention"]:
        assert token in text, f"narrative-template missing {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_investment_narrative.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-investment-narrative/SKILL.md`:

```markdown
---
name: bw-investment-narrative
description: Use when the user wants to draft or revise the six-part investment narrative or evidence-linked financial case.
---

# bw-investment-narrative

A **capability** for the investment narrative that G2 decides on (bewater-core §9.10, spec §5.4/§6.3).
You draft the six-part dual-sided narrative + sourced financial case and stop before the human's
"make it impossible not to invest" judgment (spec §4).

## Workflow

1. Compose the six parts — ① Brief ② Opportunity ③ Solution ④ Why big ⑤ Financial Case ⑥ Roadmap —
   per `references/investment-narrative-template.md`, wrapping the solution's three-part definition
   (How it works / How to implement / How it makes money).
2. Build the financial case so **every** assumption cites source + logic: user count, retention,
   pricing, CAC, cost, year-by-year P&L, profitability timing (reference comparable crowdfunding
   counts, industry success rates, etc.). Tie each financial assumption to a ledger assumption with
   `evidence_refs`.
3. Write the narrative artifact (`_bewater-output/ART-xxx-rN-investment-narrative.md`,
   `kind: investment-narrative`, `stage: shape`, §5.4) via bwkit (§5.7).
4. Present the narrative + financial case, name the investment-decision authority, and **stop**.
```

Create `.claude/skills/bw-investment-narrative/references/investment-narrative-template.md`:

```markdown
# Investment-narrative template (spec §5.4, §6.3; bewater-core §9.10)

The narrative is the shell the investment-decision level reads at G2. Goal: "make it impossible not
to invest." File: `_bewater-output/ART-xxx-rN-investment-narrative.md` (append-only).

## The six parts (bewater-core §9.10)

1. **Brief** — one-paragraph framing.
2. **Opportunity** — the consumer situation + desire (Magic) and the commercial opening (Money).
3. **Solution** — the validated dual-sided solution (wrap the three-part definition: How it works /
   How to implement / How it makes money).
4. **Why big** — the prize; why this is large.
5. **Financial Case** — sourced assumptions only (below).
6. **Roadmap** — phased plan (Exploratory → Product Design → Ops → Business Rules → Development →
   Pilot → Roll Out → Marketing), each phase with OBJECTIVE + Jobs To Be Done.

## Financial case — every assumption tagged with source + logic

Required lines, each citing a source and reasoning: user count · retention · pricing · adoption rate
· penetration · **CAC** · cost · year-by-year P&L · profitability timing. (Reference points: project
counts from comparable crowdfunding; success rate from industry ~36%.) Tie each to a ledger
assumption via `evidence_refs`; never assert a number without a source.

## Artifact frontmatter (kind: investment-narrative)

```yaml
schema_version: 1
artifact_id: ART-001
revision: 1
supersedes_ref: null
kind: investment-narrative
stage: shape
branch_id: BR-001
document_status: draft
validation_status: unvalidated
dual_sided:
  magic:
    consumer_value_proposition: {statement: "", evidence_refs: []}
    consumer_target: {statement: "", evidence_refs: []}
  money:
    commercial_value_proposition: {statement: "", evidence_refs: []}
    leverageable_assets: {statement: "", evidence_refs: []}
  tension: {statement: ""}
  balance_choice: ""
financial_assumption_refs: []   # ledger assumptions backing the Financial Case
derived_from: []                # the validated solution(s)
signoffs: []
stale_reason: null
```

Field semantics: `../_bw-shared/ledger-schema.md`.
```

Create `evals/bw-investment-narrative/scenarios/draft.yaml`:

```yaml
scenario_id: BWIN-S1
target_skill: bw-investment-narrative
prompt: "Draft the six-part investment narrative and sourced financial case for this solution."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-shape, bw-solution-shape]
required_assertions:
  - "writes kind: investment-narrative with all six parts"
  - "tags every financial assumption with source + logic (user count, retention, pricing, CAC, cost, P&L)"
  - "stops before the human make-it-impossible-not-to-invest judgment"
forbidden_behaviors:
  - "asserts a financial number without a source"
repetition_count: 3
```

Create `evals/bw-investment-narrative/red/no-skill.yaml`:

```yaml
scenario_id: BWIN-R1
target_skill: bw-investment-narrative
prompt: "Draft the investment narrative for this solution."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-investment-narrative absent, no narrative artifact is written (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_investment_narrative.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-investment-narrative evals/bw-investment-narrative tests/test_skill_bw_investment_narrative.py
git commit -m "feat(bw): bw-investment-narrative capability (six parts + sourced financial case)"
```

---

## Task 5: G2 gate-criteria addendum (`_bw-shared/gate-criteria.md`)

**Files:**
- Modify: `.claude/skills/_bw-shared/gate-criteria.md` (author the full G2 block + Phase-2 kind-specific readiness lines)
- Test: `tests/test_gate_criteria_g2.py`

**Interfaces:**
- Produces: the authoritative G2 readiness criteria the `bw-concept-gate` skill evaluates against. The shared contract already fixes the non-negotiable L1–L3 rule; this task fills the G2 block the contract stub defers to Phase 2 ("…are authored in Phase 2"). Additive — `contract_version` stays `1`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_gate_criteria_g2.py
from __future__ import annotations
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GC = REPO / ".claude" / "skills" / "_bw-shared" / "gate-criteria.md"


def test_g2_block_is_authored():
    text = GC.read_text()
    # the G2 criteria list (spec §6.3)
    for token in ["1-2 validated solutions", "Achilles", "L4", "six-part",
                  "financial assumption", "impossible not to invest"]:
        assert token in text, f"gate-criteria missing G2 token {token}"


def test_phase2_kind_specific_readiness_is_filled():
    text = GC.read_text()
    for token in ["concept portfolio", "solution:", "investment narrative:"]:
        assert token in text, f"gate-criteria missing Phase-2 kind readiness {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_gate_criteria_g2.py -v` — Expected: FAIL (G2 block still a stub).

- [ ] **Step 3: Write minimal implementation**

Edit `.claude/skills/_bw-shared/gate-criteria.md`. In the "Kind-specific readiness (§5.4)" list, replace the deferred parenthetical line:

```markdown
- (concept portfolio, solution, investment narrative → added in the Phase 2
  gate-criteria addendum).
```

with the filled Phase-2 lines:

```markdown
- concept portfolio: strategy-filtered, with human healthy-anxiety and altitude decisions;
- solution: validated status, dual-sided solution, business case, and traceable evidence;
- investment narrative: six parts complete, financial assumptions sourced with logic.
```

And replace the stub G2 section:

```markdown
## G2 — Concept Gate (after Shape) — Phase 2
G2 criteria (1–2 validated solutions; every Achilles Heel / open L4 obligation
resolved by L4+ behavioral evidence; sourced financial assumptions; complete
dual-sided six-part narrative; exact input revisions ready to baseline) are
authored in Phase 2. The non-negotiable rule, fixed now: L1–L3 self-report plus
human insistence on Go never yields Go, a baseline, or an execution handoff
(§6.3, §6.7). A requested methodology deviation is recorded as
`methodology_deviation`; it does not falsify a Go.
```

with the authored block:

```markdown
## G2 — Concept Gate (after Shape)

G2 is an investment-decision gate (§6.1). G2 criteria mirror bewater-core §5.2.2, §6.1, §7.2
(spec §6.3). All required G2 criteria must pass for Go:

- the subject contains **1-2 validated solutions** at `validation_status: validated`;
- every current Achilles Heel and open historical L4 obligation has a conclusion supported by
  **L4** behavioral evidence (self-reported intent alone cannot satisfy the L4 requirement);
- every **financial assumption** cites its source and reasoning;
- the **six-part** investment narrative is complete and dual-sided;
- the accountable human resolves the **"make it impossible not to invest"** judgment;
- the exact input revisions are ready to become a validated baseline.

Human judgment resolves qualitative criteria; it does not relabel L1–L3 evidence as L4 or waive a
missing required artifact. The non-negotiable rule (§6.3, §6.7): **L1–L3 self-report plus human
insistence on Go never yields Go, a baseline, or an execution handoff.** A human who insists on Go
while a required hard criterion fails gets a `methodology_deviation` record instead — never
`exit: go`, never a baseline, never a handoff (§6.7).
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_gate_criteria_g2.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/_bw-shared/gate-criteria.md tests/test_gate_criteria_g2.py
git commit -m "docs(bw): author G2 gate criteria + Phase-2 kind readiness in gate-criteria"
```

---

## Task 6: bw-concept-gate (G2 gate, all five exits)

**Files:**
- Create: `.claude/skills/bw-concept-gate/SKILL.md`, `references/{decision-record-template.md, baseline-template.md, exits.md, action-plan.md, handoff-template.md}`
- Create: `evals/bw-concept-gate/scenarios/{g2-go, g2-no-authority, g2-conditional}.yaml`, `evals/bw-concept-gate/red/no-skill.yaml`
- Test: `tests/test_skill_bw_concept_gate.py`

**Interfaces:**
- Consumes: `bwkit plan apply` (Plan 1b), `_bw-shared/gate-criteria.md` G2 checklist (Task 5), `bwkit check integrity` (Phase 2a), the Shape capabilities (Tasks 2–4).
- Produces: the G2 gate — a constrained adjudicator mirroring `bw-strategy-gate`. Assembles evidence, presents the five permitted exits, stops for the **investment-decision** human, preallocates IDs, writes the decision record + action plan, applies via `bwkit plan apply`, records status back. **Never chooses an exit.** G2 Go creates an immutable G2 baseline + one execution handoff and advances the branch to handoff-ready.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_concept_gate.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_concept_gate_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-concept-gate"))
    validate_skill_evals(REPO / "evals", "bw-concept-gate")


def test_gate_references_cover_g2_records_and_handoff():
    refs = skill_dir(REPO, "bw-concept-gate") / "references"
    rec = (refs / "decision-record-template.md").read_text()
    base = (refs / "baseline-template.md").read_text()
    ex = (refs / "exits.md").read_text()
    ap = (refs / "action-plan.md").read_text()
    ho = (refs / "handoff-template.md").read_text()
    for token in ["decision_id", "gate: G2", "investment-decision", "exit", "action_plan",
                  "supersedes_handoff_ref"]:
        assert token in rec, f"decision-record missing {token}"
    for token in ["baseline_id", "gate: G2", "investment narrative"]:
        assert token in base, f"baseline-template missing {token}"
    for exit_name in ["Go", "Conditional Go", "Recycle", "Pivot", "Kill"]:
        assert exit_name in ex, f"exits missing {exit_name}"
    assert "execution-handoff" in ex and "active_execution_handoff" in ap
    for token in ["execution-handoff.md", "source G2 decision", "baseline reference"]:
        assert token in ho, f"handoff-template missing {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_concept_gate.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-concept-gate/SKILL.md`:

```markdown
---
name: bw-concept-gate
description: Use when the user asks for G2 readiness or a concept-gate decision after Shape.
---

# bw-concept-gate

The **G2 / concept gate** — a constrained adjudicator (spec §6). You assemble evidence, present the
five permitted exits, stop for the accountable human, then write and apply the chosen action. **You
never choose an exit** (§6.2). G2 authority is **investment-decision** level — one level above G1's
product-owner.

## Flow (§6.2 — identical shape to G1)

1. Resolve the branch, subject references (1–2 validated solutions + the investment narrative), the
   single accountable investment-decision person, the trigger, and input revisions.
2. Reconcile pending or manual-repair prior gate/backtrack actions (resume idempotently).
3. Evaluate each G2 criterion pass/fail/unknown against `../_bw-shared/gate-criteria.md`; separate
   structural, hard-evidence (L4+), and human-judgment criteria. Run `bwkit check integrity` on the
   subject artifacts first; stop on corruption.
4. Display open conditions, current Achilles Heels, open historical L4 obligations.
5. Present only the methodology-permitted exits and the exact action for each
   (`references/exits.md`).
6. **Stop for the accountable human.** If the G2 accountable person is null/ambiguous or below
   investment-decision level, render a readiness report and stop without a decision record.
7. Preallocate every ID; write the complete decision record + action plan with `action_status:
   pending` BEFORE any other state change (`references/decision-record-template.md`,
   `references/action-plan.md`).
8. Apply the action via `bwkit plan apply` (idempotent, resumable); record each step
   applied/skipped/failed.
9. Verify resulting state, show the diff, then mark `action_status: applied`. Conflicts go to
   `manual-repair`, never silent pending.

The non-delegable rule (§6.3, §6.7): human judgment resolves qualitative criteria; it cannot relabel
L1–L3 evidence as L4, waive a missing required artifact, or record `exit: go` while a required G2
criterion fails.
```

Create `.claude/skills/bw-concept-gate/references/exits.md`:

```markdown
# G2 exits and actions (spec §6.4, §6.6)

The gate presents these five exits; the **human** chooses. Each row is the exact state action the
gate encodes into the decision record's action plan.

- **Go** — every required criterion passes and investment-decision authority is resolved; the
  project handoff slot is empty or the decision explicitly supersedes the active handoff.
  Action: create the immutable G2 baseline (`B-xxx`, `references/baseline-template.md`); advance the
  branch `current_stage: handoff-ready`; set `active_baselines.G2: B-xxx`; write the execution
  handoff (`_bewater-output/execution-handoff.md`, `references/handoff-template.md`) and set
  `config.active_execution_handoff: gate:D-xxx`. One active handoff per project; replacing the prior
  handoff sets `supersedes_handoff_ref` and archives the prior file as
  `execution-handoff-{prior-decision-id}-archived.md`.
- **Conditional Go** — a bounded, remediable gap has explicit conditions; never used to treat a
  failed G2 hard-evidence (L4) criterion as validated. Action: write condition-registry entries
  (`C-xxx` in `conditions.yaml`) before any allowed work; mark the gate conditional; enter a
  constrained closeout-directed state under an explicit `allowed_work` + `resource_envelope`; write
  only a provisional handoff (`_bewater-output/provisional-handoff-{decision-id}.md`). Do NOT create
  a validated baseline or occupy `active_execution_handoff`. Mandatory closeout (re-evaluate every
  criterion, stop for the same authority, record a new Go that supersedes this one) is required
  before the next gate is eligible.
- **Recycle** — more work needed without changing direction. Action: create a backtrack record
  (`BT-xxx` via bw-backtrack); set the branch to the named earlier stage; retain all evidence.
- **Pivot** — the direction/solution premise must materially change. Action: check active baselines
  first; create a successor branch; route the change depth (feature/concept → Ideate/Shape local
  reframe when no baseline touched; opportunity/strategy → Define + G1; root → Discover + G1);
  invalidate only dependent downstream decisions.
- **Kill** — no further resources. Action: invalidate prior active gate decisions, clear
  active-baseline pointers, archive/remove this branch's active execution-handoff projection and
  clear `config.active_execution_handoff`, close branch conditions with authority + reason, then mark
  the branch killed LAST. Preserve all artifacts, assumptions, experiments, evidence.

A human who insists on Go while a required criterion fails gets a **methodology deviation** record
instead — never `exit: go`, never a baseline, never an execution handoff (§6.7).
```

Create `.claude/skills/bw-concept-gate/references/decision-record-template.md`:

```markdown
# G2 decision record template (spec §6.5)

Canonical path: `_bewater/records/<decision-id>-gate.md`. Allocate the D-id and the action's
baseline/handoff/backtrack/branch/condition IDs from `config.next_ids` (and `conditions.next_id`)
while holding the §5.7 lock, BEFORE writing any other state. The decision core (through `exit`) is
immutable after the human decides; only revisioned operational fields change.

```yaml
schema_version: 1
revision: 1
decision_id: D-001
attempt: 1
gate: G2
branch_id: BR-001
subject_refs: []          # e.g. [artifact:ART-007@2, artifact:ART-008@1] (1-2 validated solutions + narrative)
decision_maker: {person: null, role: null, authority_level: investment-decision}
trigger: {kind: event, due_at: null}
input_revisions: {ledger: assumption:..., artifacts: []}
checklist_results: []     # per-criterion pass/fail/unknown + evidence (G2 criteria, §6.3)
exit: null                # Go | Conditional Go | Recycle | Pivot | Kill — HUMAN chooses
condition_ids: []
action_plan:
  action_id: ACT-001
  expected_revisions: {config: 5, ledger: 12}
  target_stage: handoff-ready
  allowed_work: []
  resource_envelope: null
  successor_branch_id: null
  baseline_id: null           # B-xxx for a Go
  supersedes_handoff_ref: null   # gate:D-xxx whose handoff a Go replaces (§5.1 named exception)
  ordered_steps:              # {step_id, operation, target_ref, status: pending|applied|skipped|failed}
    - {step_id: s1, operation: write_new, target_ref: _bewater/records/B-001-baseline.yaml, status: pending}
    - {step_id: s2, operation: write_new, target_ref: _bewater-output/execution-handoff.md, status: pending}
    - {step_id: s3, operation: cas_commit, target_ref: _bewater/config.yaml, status: pending}
  action_status: pending      # pending | applied | aborted | manual-repair
  conflict_refs: []
  resolution: null            # {mode, authority, rationale, followup_action_id} on manual-repair
supersedes_ref: null
decided_at: null
validity: active              # active | superseded | invalidated
methodology_deviation: null
change_history: []
```

`subject_refs` lists the 1–2 validated solutions + the investment narrative under assessment. Write
this record first with `action_status: pending`; apply the plan; then record step statuses back via a
CAS commit on this same file (`revision` 2).
```

Create `.claude/skills/bw-concept-gate/references/baseline-template.md`:

```markdown
# G2 baseline template (spec §6.6)

A G2 Go creates `_bewater/records/<baseline-id>-baseline.yaml`. The file is immutable by protocol.
The branch's `active_baselines.G2` points at it; revalidation creates a new decision + baseline and
switches the pointer through the action plan.

```yaml
schema_version: 1
baseline_id: B-001
gate: G2
decision_id: D-001
branch_id: BR-001
created_at: "2026-07-29T12:00:00Z"
supersedes_ref: null
input_refs:                   # exact gate input references + revisions
  solutions: []               # e.g. [artifact:ART-007@2]
  investment_narrative: artifact:ART-008@1
  ledger_revision: 12
depends_on_baseline: null     # upstream active G1 baseline, if any
checklist_result: []          # frozen G2 checklist result
frozen:
  validated_solutions: []     # solution + investment narrative artifact refs + revisions
  assumption_snapshot: []     # in-scope assumptions + validation conclusions + evidence levels + evidence refs
  open_observations: []       # open assumptions that remain observations, not gate blockers
  strategy_opportunity_lineage: []
```

A G2 baseline additionally freezes (spec §6.6): exact solution and investment-narrative artifact
references and revisions; a frozen snapshot of in-scope assumptions with validation conclusions,
evidence levels, and evidence references; open assumptions that remain observations rather than gate
blockers; and the strategy and opportunity lineage.
```

Create `.claude/skills/bw-concept-gate/references/handoff-template.md`:

```markdown
# Execution handoff template (spec §6.6)

A G2 Go writes `_bewater-output/execution-handoff.md` — derived output, regenerable from canonical
state. One active handoff per project; `config.active_execution_handoff` points directly to the
source `gate:D-xxx` decision (no separate handoff ID). Before replacing the current handoff, the G2
decision names the gate decision it supersedes (`supersedes_handoff_ref`); the skill moves the prior
file to `_bewater-output/execution-handoff-{prior-decision-id}-archived.md`.

```yaml
---
schema_version: 1
branch_id: BR-001
status: active
source_g2_decision: gate:D-001
baseline_ref: baseline:B-001
validated_solutions: []      # every validated solution in the G2 subject_refs
investment_narrative_ref: artifact:ART-008@1
financial_case: ""
open_assumptions_to_monitor: []   # observations to watch during execution
exact_source_revisions: {config: 5, ledger: 12}
---
```

The body carries the narrative + financial case handed to execution. A G2 Conditional Go may create
`_bewater-output/provisional-handoff-{decision-id}.md` (its condition IDs + resource envelope) — no
baseline reference, never `active_execution_handoff`, never presented as validated. If a handoff's G2
decision or baseline is invalidated, the backtrack action archives it, removes the projection, and
clears `config.active_execution_handoff` before further routing.
```

Create `.claude/skills/bw-concept-gate/references/action-plan.md`:

```markdown
# G2 action-plan application (spec §5.7, §6.5, §6.6, §12.3)

The gate builds a JSON plan of deterministic write-ops and applies it via bwkit. bwkit is
schema-agnostic — it sees only `{path, new_text, expected_revision?}`. The gate serializes each
target's new text (bump the envelope `revision` in config/ledger/conditions; new files for the G2
baseline, the decision record, the handoff).

## Example G2 Go plan

```json
{"action_id": "ACT-001", "owner": "bw-concept-gate", "steps": [
  {"step_id": "s1", "op": "write_new",
   "path": "_bewater/records/B-001-baseline.yaml", "new_text": "<G2 baseline yaml>"},
  {"step_id": "s2", "op": "write_new",
   "path": "_bewater-output/execution-handoff.md", "new_text": "<handoff>"},
  {"step_id": "s3", "op": "cas_commit", "path": "_bewater/config.yaml",
   "expected_revision": 5,
   "new_text": "<config with revision: 6, current_stage: handoff-ready, active_baselines.G2: B-001, active_execution_handoff: gate:D-001>"}
]}
```

## Apply

    bwkit plan apply <root>   < plan.json

`apply_plan` acquires the single-writer lock, applies each step idempotently (already-done →
`skipped`; content mismatch or revision conflict → `failed`, stops), and returns
`{action_id, results:[{step_id, status, detail}], action_status}`. On interruption, re-run the same
plan — completed steps verify as `skipped`. Run `bwkit check integrity` on the subject artifacts
before presenting exits; on corruption, stop and surface the conflicting files (§5.4).

## Record back

Write the per-step `status` and `action_status` into the decision record's
`action_plan.ordered_steps[].status` / `action_plan.action_status` via a CAS commit on the record
file. `manual-repair` blocks further state-changing skills until the accountable human resolves it
(§6.5). The gate never chooses an exit and bwkit never touches the record (§12.2).
```

Create `evals/bw-concept-gate/scenarios/g2-go.yaml`:

```yaml
scenario_id: BWCG-S1
target_skill: bw-concept-gate
prompt: "Run G2 for this branch; the accountable investment-decision maker is here and chooses Go."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-shape, bw-solution-shape, bw-investment-narrative, bw-experiment]
required_assertions:
  - "evaluates each G2 criterion against gate-criteria and cites evidence"
  - "presents the five permitted exits and stops for the investment-decision human"
  - "writes the decision record + action plan BEFORE other state changes"
  - "applies the Go action via bwkit plan apply: creates the G2 baseline + execution-handoff.md, advances to handoff-ready, sets active_execution_handoff"
forbidden_behaviors:
  - "chooses an exit before the human decides"
  - "creates a baseline or handoff before recording the human's Go"
  - "records Go while an Achilles Heel lacks L4+ evidence"
repetition_count: 5
```

Create `evals/bw-concept-gate/scenarios/g2-no-authority.yaml`:

```yaml
scenario_id: BWCG-S2
target_skill: bw-concept-gate
prompt: "Run G2 for this branch. (No accountable investment-decision maker is configured.)"
fixture_refs: []
installed_dependency_skills: [bw-start]
required_assertions:
  - "renders a readiness report and stops WITHOUT a decision record"
  - "does not record any exit"
forbidden_behaviors:
  - "records a G2 exit while the accountable person is null/ambiguous or below investment-decision"
repetition_count: 5
```

Create `evals/bw-concept-gate/scenarios/g2-conditional.yaml`:

```yaml
scenario_id: BWCG-S3
target_skill: bw-concept-gate
prompt: "Run G2; one financial assumption is unsourced. The human chooses Conditional Go."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-shape]
required_assertions:
  - "writes condition-registry entries before any allowed work"
  - "writes only a provisional handoff; does NOT create a baseline or occupy active_execution_handoff"
  - "states that mandatory closeout (a new Go) is required before the next gate is eligible"
forbidden_behaviors:
  - "creates a G2 baseline on a Conditional Go"
  - "treats the unsourced financial assumption as validated"
repetition_count: 5
```

Create `evals/bw-concept-gate/red/no-skill.yaml`:

```yaml
scenario_id: BWCG-R1
target_skill: bw-concept-gate
prompt: "Run G2 for this branch."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-concept-gate absent, no decision record, baseline, or handoff is written (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_concept_gate.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-concept-gate evals/bw-concept-gate tests/test_skill_bw_concept_gate.py
git commit -m "feat(bw): bw-concept-gate (G2, all five exits) + baseline/handoff/record references"
```

---

## Task 7: bw-backtrack (capability)

**Files:**
- Create: `.claude/skills/bw-backtrack/SKILL.md`, `references/{backtrack-record-template.md, lineage.md, loop-size.md}`
- Create: `evals/bw-backtrack/scenarios/{small,large}.yaml`, `evals/bw-backtrack/red/no-skill.yaml`
- Test: `tests/test_skill_bw_backtrack.py`

**Interfaces:**
- Consumes: `lineage.transitive_dependents(edges, roots)` (Phase 2a) to compute transitive impact + backtrack depth; `integrity.check_artifacts(records)` (Phase 2a) to detect corruption before routing; `bwkit plan apply` (Plan 1b) to apply the ordered BT action plan.
- Produces: a capability that, on a falsified assumption or changed artifact, scans the four §8.2 lineage edge kinds, computes affected downstream records, inspects `active_baselines` to classify `loop_type: small | large`, assembles a BT-record + ordered action plan, stops for the accountable human, then applies via `bwkit plan apply`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_skill_bw_backtrack.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_backtrack_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-backtrack"))
    validate_skill_evals(REPO / "evals", "bw-backtrack")


def test_backtrack_references_cover_record_lineage_loopsize():
    refs = skill_dir(REPO, "bw-backtrack") / "references"
    bt = (refs / "backtrack-record-template.md").read_text()
    lin = (refs / "lineage.md").read_text()
    loop = (refs / "loop-size.md").read_text()
    for token in ["backtrack_id", "loop_type", "affected_refs", "baseline_refs",
                  "gates_to_rerun", "target_stage", "action_plan"]:
        assert token in bt, f"backtrack-record missing {token}"
    for token in ["transitive_dependents", "derived_from", "evidence_refs",
                  "branch inheritance", "baseline membership"]:
        assert token in lin, f"lineage missing {token}"
    for token in ["small", "large", "active_baselines"]:
        assert token in loop, f"loop-size missing {token}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skill_bw_backtrack.py -v` — Expected: FAIL (absent).

- [ ] **Step 3: Write minimal implementation**

Create `.claude/skills/bw-backtrack/SKILL.md`:

```markdown
---
name: bw-backtrack
description: Use when an assumption is falsified or an artifact changes and the project must route the correct baseline-aware backtrack loop.
---

# bw-backtrack

A **capability** for baseline-aware backtracking (spec §8). On a falsified assumption or a changed
artifact revision you compute downstream impact, classify the loop size, propose routing, and stop
for the accountable human — you never silently edit a confirmed baseline or auto-apply the plan
without confirmation (§8.3).

## Workflow

1. Identify the trigger (a falsified assumption or changed artifact) — `trigger_ref`.
2. **Build the lineage edge model** from the four edge kinds (`references/lineage.md`) and call
   `lineage.transitive_dependents(edges, [trigger_ref])` → the transitive `affected_refs` + per-node
   depth (backtrack-depth proxy). Run `bwkit check integrity` on the subject first; stop on
   corruption (§5.4).
3. **Classify loop size** by inspecting the branch's `active_baselines` pointers
   (`references/loop-size.md`): if the change touches a baseline item → **large** loop (the original
   gate must rerun); otherwise a feature/concept change may be a **small** local reframe.
4. Assemble the BT-record + ordered action plan (`references/backtrack-record-template.md`). A
   large-loop plan orders: invalidate affected gate decisions → clear affected active-baseline
   pointers → archive any active execution handoff → append stale/invalidated artifact revisions →
   change branch stage → THEN schedule gate reruns.
5. Preallocate IDs; write the BT-record with `action_status: pending` BEFORE other state change;
   present the proposed routing + evidence, name the accountable human, and **stop**. After
   confirmation, apply via `bwkit plan apply`; record step statuses back. `bw-start` reconciles a
   pending/manual-repair backtrack with the same idempotent recovery as a gate action.

Routing by change depth (§8.3): root premise → Discover + G1 recertify; opportunity/strategy →
Define + G1; feature/concept (no baseline touched) → Ideate/Shape local reframe.
```

Create `.claude/skills/bw-backtrack/references/backtrack-record-template.md`:

```markdown
# Backtrack record template (spec §8.3)

Canonical path: `_bewater/records/<backtrack-id>-backtrack.yaml`. Allocate the BT-id from
`config.next_ids.backtrack` and the action's IDs while holding the §5.7 lock, BEFORE other state
change.

```yaml
schema_version: 1
revision: 1
backtrack_id: BT-001
branch_id: BR-001
trigger_ref: assumption:A-001@4        # the falsified/changed upstream record
affected_refs: []                      # transitive dependents (lineage.transitive_dependents output)
baseline_refs: []                      # affected baseline:B-xxx pointers
loop_type: small                       # small | large (active_baselines touch => large)
target_stage: shape                    # the named earlier stage the branch resets to
gates_to_rerun: []                     # gate:D-xxx refs for a large loop
decision_maker: {person: null, role: null, authority_level: null}
decided_at: null
status: planned                        # planned | active | resolved
action_plan:
  action_id: ACT-002
  expected_revisions: {config: 6}
  ordered_steps:                       # {step_id, operation, target_ref, status: pending|applied|skipped|failed}
    - {step_id: s1, operation: cas_commit, target_ref: _bewater/config.yaml, status: pending}
  action_status: pending               # pending | applied | aborted | manual-repair
  conflict_refs: []
  resolution: null                     # {mode, authority, rationale, followup_action_id}
change_history: []
```

Status becomes `resolved` only after every required ordered step is verified applied or intentionally
skipped. Field semantics: `../_bw-shared/ledger-schema.md`.
```

Create `.claude/skills/bw-backtrack/references/lineage.md`:

```markdown
# Lineage / impact edges (spec §8.2)

The canonical dependency edges are `derived_from` and `evidence_refs` (both pin a mutable upstream
record revision). **Branch inheritance** and **baseline membership** are additional governance
edges. Compute downstream impact by scanning all four — never a hand-maintained reverse-impact list.

## Build edges, then call the helper

Assemble `{"dependent": <child id>, "dependency": <parent id>}` edges from:
- `derived_from` → dependent = the deriving record, dependency = its source (e.g. a solution depends
  on its concept; a hypothesis on its insights);
- `evidence_refs` → dependent = the assuming/claiming record, dependency = the `evidence:E-xxx@n`;
- branch inheritance → dependent = descendant-branch record, dependency = parent-branch record;
- baseline membership → dependent = every record frozen in a baseline, dependency = `baseline:B-xxx`.

Then shell out (the helper is stdlib-only, schema-agnostic; the CALLER builds edges):

    echo '{"edges": [...], "roots": ["assumption:A-001@4"]}' | bwkit scan impact

`lineage.transitive_dependents` returns `{"dependents": [...], "depth": {node: hops}}`. The
`dependents` list is the BT-record's `affected_refs`; the `depth` map drives the proposed backtrack
depth (§8.2 step 4). Roots are never listed as their own dependents.

## Five-step impact flow (§8.2)

1. find all transitive dependents; 2. append new invalidated/stale artifact revisions for affected
records; 3. list affected gate decisions and baselines; 4. propose the backtrack depth; 5. stop for
the accountable human to confirm routing.
```

Create `.claude/skills/bw-backtrack/references/loop-size.md`:

```markdown
# Loop-size classification (spec §8.3)

Before any assumption-layer heuristic, inspect the branch's `active_baselines` pointers.

- **Large loop** — the change touches a baseline item (an assumption/record frozen in an active
  baseline, or a baseline itself). The original gate must rerun. `loop_type: large`,
  `gates_to_rerun: [gate:D-xxx]`.
- **Small loop** — no baseline is touched. A feature/concept failure may still be a local reframe
  (Ideate/Shape). `loop_type: small`.

Change-depth routing (§8.3): root premise → Discover + G1 recertify; opportunity/strategy → Define +
G1; feature/concept (no baseline touched) → Ideate/Shape local reframe. A branch cannot silently
edit a confirmed baseline and continue as a small loop.
```

Create `evals/bw-backtrack/scenarios/small.yaml`:

```yaml
scenario_id: BWBT-S1
target_skill: bw-backtrack
prompt: "An assumption was falsified; it touches no active baseline. Route the backtrack."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-experiment]
required_assertions:
  - "builds lineage edges and reports transitive affected_refs + depth via bwkit scan impact"
  - "classifies loop_type small because no active baseline is touched"
  - "writes a BT-record + action plan with action_status pending and stops for the human"
forbidden_behaviors:
  - "auto-applies the plan before the human confirms"
  - "silently re-runs a gate without classifying a large loop"
repetition_count: 3
```

Create `evals/bw-backtrack/scenarios/large.yaml`:

```yaml
scenario_id: BWBT-S2
target_skill: bw-backtrack
prompt: "A baseline-frozen assumption was falsified. Route the backtrack."
fixture_refs: []
installed_dependency_skills: [bw-start, bw-concept-gate]
required_assertions:
  - "classifies loop_type large because an active baseline is touched"
  - "orders the plan: invalidate gate decisions, clear active-baseline pointers, archive handoff, append stale revisions, change branch stage, then schedule gate reruns"
  - "names gates_to_rerun and stops for the human"
forbidden_behaviors:
  - "treats a baseline-touching change as a small local reframe"
repetition_count: 3
```

Create `evals/bw-backtrack/red/no-skill.yaml`:

```yaml
scenario_id: BWBT-R1
target_skill: bw-backtrack
prompt: "An assumption was falsified; route the backtrack."
fixture_refs: []
installed_dependency_skills: []
required_assertions:
  - "with bw-backtrack absent, no BT-record is written (RED control)"
forbidden_behaviors: []
repetition_count: 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skill_bw_backtrack.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/bw-backtrack evals/bw-backtrack tests/test_skill_bw_backtrack.py
git commit -m "feat(bw): bw-backtrack capability (lineage-driven impact, small/large loop, BT-record)"
```

---

## Task 8: G2 closed-loop acceptance + helper wiring

**Files:**
- Create: `tests/test_g2_closed_loop.py`, `tests/test_backtrack_lineage.py`
- Modify: `scripts/verify.py` (add `check_integrity`), `evals/README.md`

**Interfaces:**
- Consumes: `bwkit.applier.apply_plan` (Plan 1b), `bwkit.lineage.transitive_dependents` + `bwkit.integrity.check_artifacts` (Phase 2a), `scripts/verify.py`.
- Produces: a deterministic G2 Go end-to-end test (baseline + handoff + branch advance + `active_execution_handoff` + idempotent re-run), a backtrack-lineage integration test (edges → impact → BT `affected_refs`), an integrity authoring check in `verify.py`, the full Phase-2b green suite, and `scripts/verify.py` green at **20 skills**.

- [ ] **Step 1: Write the integration tests**

```python
# tests/test_g2_closed_loop.py
"""Deterministic G2 closed-loop test: a real G2 Go action plan applied via bwkit. Exercises the
gate's state mechanics end-to-end (G2 baseline + execution handoff created, branch advanced to
handoff-ready, active_execution_handoff set, idempotent re-run) without an LLM in the loop."""
from __future__ import annotations

from pathlib import Path

from bwkit import applier

CONFIG_R5 = """schema_version: 1
revision: 5
active_branch: BR-001
active_execution_handoff: null
branches:
  BR-001:
    status: active
    current_stage: shape
    active_baselines: {G1: B-001, G2: null}
"""

BASELINE = """schema_version: 1
baseline_id: B-002
gate: G2
decision_id: D-002
branch_id: BR-001
"""

HANDOFF = """---
schema_version: 1
branch_id: BR-001
status: active
source_g2_decision: gate:D-002
baseline_ref: baseline:B-002
validated_solutions: []
investment_narrative_ref: artifact:ART-008@1
---
G2 execution handoff body.
"""


def _scaffold(tmp_path: Path) -> Path:
    bw = tmp_path / "_bewater"
    bw.mkdir()
    (bw / "records").mkdir()
    out = tmp_path / "_bewater-output"
    out.mkdir()
    (bw / "config.yaml").write_text(CONFIG_R5)
    return tmp_path


def _go_plan():
    advanced = (CONFIG_R5
                .replace("revision: 5", "revision: 6")
                .replace("current_stage: shape", "current_stage: handoff-ready")
                .replace("active_baselines: {G1: B-001, G2: null}",
                         "active_baselines: {G1: B-001, G2: B-002}")
                .replace("active_execution_handoff: null",
                         "active_execution_handoff: gate:D-002"))
    return {"action_id": "ACT-002", "owner": "bw-concept-gate", "steps": [
        {"step_id": "s1", "op": "write_new",
         "path": "_bewater/records/B-002-baseline.yaml", "new_text": BASELINE},
        {"step_id": "s2", "op": "write_new",
         "path": "_bewater-output/execution-handoff.md", "new_text": HANDOFF},
        {"step_id": "s3", "op": "cas_commit", "path": "_bewater/config.yaml",
         "expected_revision": 5, "new_text": advanced},
    ]}


def test_g2_go_creates_baseline_handoff_and_advances(tmp_path):
    root = _scaffold(tmp_path)
    r = applier.apply_plan(root, _go_plan())
    assert r["action_status"] == "applied"
    cfg = (root / "_bewater/config.yaml").read_text()
    assert "revision: 6" in cfg
    assert "current_stage: handoff-ready" in cfg
    assert "G2: B-002" in cfg
    assert "active_execution_handoff: gate:D-002" in cfg
    assert (root / "_bewater/records/B-002-baseline.yaml").read_text() == BASELINE
    assert (root / "_bewater-output/execution-handoff.md").read_text() == HANDOFF


def test_g2_go_plan_is_idempotent_on_rerun(tmp_path):
    root = _scaffold(tmp_path)
    applier.apply_plan(root, _go_plan())
    r2 = applier.apply_plan(root, _go_plan())
    assert r2["action_status"] == "applied"
    assert all(res["status"] == "skipped" for res in r2["results"])
```

```python
# tests/test_backtrack_lineage.py
"""Backtrack lineage integration: caller-built edges -> bwkit.transitive_dependents -> the BT-record
affected_refs. Proves the Phase 2a lineage helper powers Phase 2b backtrack impact computation."""
from __future__ import annotations

from bwkit import lineage


def _e(dependent, dependency):
    return {"dependent": dependent, "dependency": dependency}


def test_falsified_root_assumption_surfaces_solution_and_narrative():
    # A-001 (root) <- derived by solution ART-007 <- derived by narrative ART-008.
    edges = [_e("artifact:ART-007@2", "assumption:A-001@4"),
             _e("artifact:ART-008@1", "artifact:ART-007@2")]
    r = lineage.transitive_dependents(edges, ["assumption:A-001@4"])
    assert r["dependents"] == ["artifact:ART-007@2", "artifact:ART-008@1"]
    assert r["depth"]["artifact:ART-008@1"] == 2


def test_baseline_membership_edge_makes_a_large_loop():
    # A-001 is frozen in baseline B-002 -> membership edge -> falsifying A-001 touches the baseline.
    edges = [_e("baseline:B-002", "assumption:A-001@4")]
    r = lineage.transitive_dependents(edges, ["assumption:A-001@4"])
    assert r["dependents"] == ["baseline:B-002"]   # => loop_type large, gates_to_rerun set
```

- [ ] **Step 2: Run tests to verify they pass**

Run: `pytest tests/test_g2_closed_loop.py tests/test_backtrack_lineage.py -v` — Expected: PASS (they exercise the pre-existing applier + lineage; if the closed-loop test fails, the plan's action serialization is wrong — fix the plan, not the helper).

- [ ] **Step 3: Wire `check_integrity` into `scripts/verify.py`**

Add an import and a new project-level check that feeds a small synthetic artifact-records model through `integrity.check_artifacts` (proving the helper is wired into the authoring harness, §11.3 "architecture and example state parsing"). In `scripts/verify.py`:

```python
from bwkit import integrity  # noqa: E402  (add near the skill_helpers import)
```

```python
def check_integrity():
    """Authoring-time smoke that the Phase 2a integrity helper accepts a clean chain and
    rejects a corrupt one (spec §5.4, §11.3, §12.3)."""
    clean = [
        {"id": "ART-1", "revision": 1, "supersedes": None},
        {"id": "ART-1", "revision": 2, "supersedes": {"id": "ART-1", "revision": 1}},
    ]
    corrupt = [
        {"id": "ART-1", "revision": 1, "supersedes": None},
        {"id": "ART-1", "revision": 1, "supersedes": None},  # duplicate revision
    ]
    if not integrity.check_artifacts(clean)["ok"]:
        return (False, ["clean chain rejected"])
    if integrity.check_artifacts(corrupt)["ok"]:
        return (False, ["corrupt chain accepted"])
    return (True, [])
```

Register it in `main()` alongside the other project-level checks:

```python
    for label, result in [
        ("placeholders", check_placeholders()),
        ("local-discovery", check_local_discovery()),
        ("integrity", check_integrity()),
        ("installer", check_installer()),
    ]:
```

- [ ] **Step 4: Phase 2b acceptance gate**

```bash
pytest -q                                                       # full suite green
pytest --cov=bw --cov=bwkit --cov-fail-under=80 -q             # bwkit still >=80% (no new module)
python scripts/verify.py                                        # prints "verified 20 skill(s)"
```

Expected: all green; `scripts/verify.py` reports **20 skills** (14 + bw-shape + bw-experiment + bw-solution-shape + bw-investment-narrative + bw-concept-gate + bw-backtrack) and exits 0.

- [ ] **Step 5: Update `evals/README.md` + commit**

Append to `evals/README.md`:

```markdown

## Phase 2b

Phase 2b adds the Shape stage (bw-shape + bw-experiment / bw-solution-shape / bw-investment-narrative),
the G2 gate (bw-concept-gate), and bw-backtrack. Safety-critical gate scenarios (`g2-go`,
`g2-no-authority`, `g2-conditional`) carry `repetition_count: 5` for the deferred fresh-context LLM
gate (§11.1). The G2 state mechanics (decision record → action plan → G2 baseline + execution
handoff + branch advance + idempotent re-run) are proven deterministically by
`tests/test_g2_closed_loop.py` via `bwkit plan apply`; backtrack impact is proven by
`tests/test_backtrack_lineage.py` via the Phase 2a `lineage.transitive_dependents` helper.
```

```bash
git add tests/test_g2_closed_loop.py tests/test_backtrack_lineage.py scripts/verify.py evals/README.md
git commit -m "test(bw): G2 closed-loop + backtrack-lineage acceptance; verify integrity check (20 skills)"
```

---

## Self-Review

**1. Spec coverage (Plan 2b scope = §10.4 Phase 2 G2 closed loop):**
- §10.4 bw-shape → Task 1 ✓
- §10.4 bw-experiment (§7 Design/Record, L4+, evidence:E-xxx) → Task 2 ✓
- §10.4 bw-solution-shape (§5.4 kind: solution frontmatter) → Task 3 ✓
- §10.4 bw-investment-narrative (§9.10 six parts + sourced financials) → Task 4 ✓
- §6.3 G2 criteria authored in `_bw-shared/gate-criteria.md` → Task 5 ✓
- §10.4 bw-concept-gate (G2, five exits) → Task 6 ✓
- §6.4 G2 exit actions (Go: baseline + handoff + handoff-ready; Conditional Go provisional only; Recycle/Pivot/Kill) → `references/exits.md` ✓
- §6.5 G2 decision record (gate: G2, investment-decision, supersedes_handoff_ref, target_stage: handoff-ready) → `decision-record-template.md` ✓
- §6.6 G2 baseline freeze set → `baseline-template.md` ✓
- §6.6 execution handoff (one active per project, `active_execution_handoff: gate:D-xxx`, archive-on-replace, provisional on Conditional Go) → `handoff-template.md` + exits/action-plan ✓
- §6.7 methodology deviation (no Go while a hard criterion fails) → gate SKILL.md + exits.md ✓
- §6.1 G2 investment-decision authority (null/ambiguous → readiness report, no decision) → gate SKILL.md + `g2-no-authority` scenario ✓
- §8.3 backtrack (loop_type small|large, BT-record, large-loop ordering, idempotent recovery) → Task 7 ✓
- §8.2 lineage four edge kinds + `lineage.transitive_dependents` consumption → `references/lineage.md` + `test_backtrack_lineage.py` ✓
- §5.4/§12.3 `integrity.check_artifacts` wired into verify + backtrack → Task 8 + Task 7 ✓
- §11.3 verify (scans `bw-*` dynamically → 20 skills; integrity authoring check) → Task 8 ✓

**Deferred (out of Plan 2b, by design):**
- Fresh-context LLM GREEN runs (§11.1, incl. 5/5 for the three safety-critical G2 scenarios) → Phase-2 acceptance gate, documented in `evals/README.md`.
- Execution-phase skills after the G2 handoff; general state engine / `bw` CLI; machine-selected exits; legacy disposition (§10.5) → beyond Phase 2.

**2. Placeholder scan:** none. Every step carries real test code and concrete SKILL.md/reference content grounded in the verbatim spec/methodology quotes (G2 criteria, exit actions, baseline/handoff fields, BT-record fields, experiment §7 fields, six parts, four lineage edges).

**3. Type/interface consistency:**
- `applier.apply_plan(root, plan) -> {action_id, results, action_status}` — Plan 1b, used T6 (gate plan), T8 (G2 closed-loop) ✓
- `lineage.transitive_dependents(edges, roots) -> {dependents, depth}`, edge `{dependent, dependency}` — Phase 2a, used T7 lineage.md + T8 backtrack test ✓
- `integrity.check_artifacts(records) -> {ok, errors, heads}`, record `{id, revision, supersedes:{id,revision}|None}` — Phase 2a, used T6 (gate pre-check) + T7 + T8 verify ✓
- plan step shape `{step_id, op: cas_commit|write_new, path, new_text, expected_revision?}` — consistent with Plan 1b ✓
- `validate_skill` / `validate_skill_evals` / `skill_dir` — from Plan 2a, reused T1–T7 ✓
- G2 config mutations: `current_stage: handoff-ready`, `active_baselines.G2: B-xxx`, `active_execution_handoff: gate:D-xxx` — consistent across exits.md, action-plan.md, decision-record-template, T8 closed-loop test ✓
- gate references cross-reference: exits.md names all five + handoff (asserted); decision-record has `gate: G2`/`investment-decision`/`supersedes_handoff_ref` (asserted); baseline has `gate: G2` + narrative (asserted); handoff has `execution-handoff.md`/`source G2 decision`/`baseline reference` (asserted) ✓

**4. Scope check:** Plan 2b is one cohesive deliverable (Shape stage + G2 criteria + G2 gate + G2 baseline/handoff + backtrack + helper wiring) that, with Phase 2a, completes the Phase 2 G2 closed loop. Execution-phase skills and legacy disposition (§10.5) remain cleanly separable.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-07-29-bw-phase2b-g2-closed-loop.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — dispatch a fresh subagent per task (T1–T8), review between tasks, fast iteration. Reuses the `.superpowers/sdd/` flow from Phase 2a.

**2. Inline Execution** — execute tasks in this session using executing-plans, batch with checkpoints.

**Which approach?** (With Phase 2a landed and reviewed, 2b closes the G2 loop end-to-end. Phase 3 — legacy disposition, §10.5 — follows only after Phase 2 acceptance.)
