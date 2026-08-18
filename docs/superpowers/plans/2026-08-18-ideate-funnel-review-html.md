# Ideate Funnel, Review, and HTML Decision Views — Implementation Plan

## Status

Proposed 2026-08-18. Implementation must not start until the user approves this
plan.

## Goal

Implement the approved design in
`docs/superpowers/specs/2026-08-18-ideate-funnel-review-html-design.md`:

- 10–15 Idea Seeds per Opportunity Area;
- explicit recommended cuts that leave 5–8 Seeds;
- human confirmation of exactly 5–8 Seeds per OA;
- one initial full Concept per confirmed Seed;
- producer/reviewer separation for Concept evaluation;
- global human selection of 2–4 reviewed Concepts; and
- Artifact-derived Idea Pool and Concept Portfolio decision views in HTML.

## Non-negotiable boundaries

- **Artifact Markdown is the single source of truth.** HTML receives no shadow
  business model and persists no decisions.
- Do not create `ART-008@3`, `ART-009@3`, or any other active-case Artifact
  revision. Do not edit `_bewater/` state, ledger, records, IDs, or stage.
- Preserve and incrementally extend the existing uncommitted Concept SVG/HTML
  work. Do not reset, replace, or broadly format those files.
- Author source skills first and deploy managed copies through `install.sh`;
  never hand-edit `.claude/skills` or `.agents/skills`.
- Every production change starts with a failing test. Repository coverage stays
  at or above 80%.
- Fresh-context LLM evals incur external cost and are not run without separate
  authorization. This plan updates their manifests and runs deterministic
  manifest validation only.

## Current baseline and overlap

The planning baseline passes 80 targeted tests across lifecycle, skill, HTML,
and installer suites.

The worktree already contains uncommitted work from the approved Concept SVG
and HTML reader design, including `src/bwkit/html.py`,
`tests/test_bwkit_html.py`, `src/bw/concept_contract.py`, CLI/package wiring,
and overlapping Concept skill files. These are treated as existing user work.
Before implementation, record the worktree and hashes of overlapping files;
all edits are small `apply_patch` increments.

One prerequisite defect is already visible: standalone deployed `bwkit` imports
`bw.concept_contract`, but the installer deploys only `src/bwkit`. The HTML
runtime must own the pure SVG projector or otherwise remove this cross-package
dependency before active deployment.

## Compatibility decision

Compatibility is selected from the exact referenced Artifact data, not date or
filename:

- a Pool using legacy `shortlist.recommended` and no `recommended_cuts` keeps
  the legacy validator path;
- a Pool using `recommended_cuts` uses the strict new contract for every OA;
- mixing the legacy and new fields is invalid; and
- a Concept Portfolio inherits strictness from its exact `idea_pool_ref`.

This keeps the active 9/9/10-confirmed legacy case and its downstream Shape
lineage valid without regeneration. HTML labels it as legacy and never invents
missing rationales or Review results. All updated skills and templates emit
only the strict format. This presence-based grandfathering is necessary because
the approved design does not introduce a separate contract-version field.

## Agent ownership during implementation

The project requires Agent collaboration for 3+ file changes. To avoid shared
worktree collisions:

- **Contracts agent:** lifecycle tests, fixtures, and
  `src/bw/concept_lifecycle.py` only.
- **HTML agent:** existing HTML/visualization files and their tests only.
- **Skills agent:** source skills, templates, references, static skill tests,
  and eval manifests only.
- **Root agent:** integration review, installer/runtime deployment, active-state
  hash audit, full verification, and commits.

No two agents edit the same file concurrently. Root resolves any change to a
shared boundary after the owning agent finishes.

## Task 1 — Protect the existing HTML baseline and fix standalone runtime

**Files**

- Modify: `tests/test_installer_copy.py`
- Modify: `tests/test_concept_contract.py`
- Create: `src/bwkit/concept_visualization.py`
- Modify: `src/bwkit/html.py`
- Modify: `src/bw/concept_contract.py`

**RED**

Add an installer smoke test that performs a full copy install into a temporary
project, creates a minimal Concept Artifact, and runs `python -m bwkit html`
with only the deployed `_bewater` directory on `PYTHONPATH`. Confirm it fails
before the fix because `bw` is unavailable.

**GREEN**

Move the pure deterministic SVG implementation into `bwkit`, import it locally
from the HTML reader, and retain `bw.concept_contract` as a compatibility
wrapper if its approved API is still needed. Preserve current escaping,
fallback, determinism, SVG, and Concept-card behavior.

**Verify**

```bash
.venv/bin/python -m pytest -q tests/test_concept_contract.py tests/test_installer_copy.py tests/test_bwkit_html.py
```

## Task 2 — Lock the strict and legacy lifecycle contracts with RED tests

**Files**

- Modify: `tests/test_concept_lifecycle.py`
- Modify: `tests/test_validate.py`

**RED fixture**

Rebuild the valid strict helper with 10 Seeds, 5 structured recommended cuts,
5 human-confirmed Seeds, and 5 initial Concepts per OA. Add a ready Portfolio
Review covering the current active candidate set; keep only 2–4 Concepts
human-selected globally.

Keep a separate explicit legacy fixture proving the active-format
`shortlist.recommended`, missing Review, and 9+ confirmations remain readable
and validator-clean.

**RED cases**

- strict Seed counts: 9 fail, 10 pass, 15 pass, 16 fail;
- recommended remaining counts: 4 fail, 5 pass, 8 pass, 9 fail;
- confirmed counts: empty draft allowed; 4 fail, 5 pass, 8 pass, 9 fail;
- cut entries require a unique same-OA `seed_id`, an allowed reason, and a
  non-empty rationale;
- legacy/new shortlist fields cannot be mixed;
- confirmed IDs are unique, same-OA, and backed by an exact human decision;
- any incomplete OA confirmation blocks a strict Concept Portfolio;
- root Concepts (`parent_ids: []`) match confirmed Seeds exactly 1:1;
- missing, duplicate, extra, unconfirmed, and cross-OA roots fail;
- derived merge/split Concepts are excluded from the initial 1:1 count;
- Review status is `ready | needs-revision`, iterations are 1–2, and reviewed
  IDs exactly cover active non-killed/non-merged candidates;
- `needs-revision` is a valid draft but blocks terminal Concept decisions and
  a non-empty exit;
- Reviewer content cannot populate any human-only field; and
- real Markdown validation exposes the same errors through `validate_all()`.

Run the new tests and confirm they fail for the intended missing behavior.

## Task 3 — Implement deterministic lifecycle validation

**Files**

- Modify: `src/bw/concept_lifecycle.py`

**GREEN**

Add small parsing and validation helpers for:

- strict-vs-legacy Pool detection;
- closed Seed bounds;
- structured recommended cuts and complement counts;
- Review shape and readiness;
- complete human confirmations for all OAs;
- exact confirmed-to-root-Concept multiplicity; and
- active candidate coverage.

Keep existing chain uniqueness, ID history, exact-ref, merge lineage, decision
ownership, and global 2–4 exit behavior. Use stable issue kinds so routing and
tests can identify each failure. `src/bw/validate.py` already calls
`concept_issues()` and needs no new integration layer.

Do not turn subjective novelty, Magic, Money, or altitude judgment into schema
rules. Validate their structure and provenance; leave their conclusions to the
Reviewer.

**Verify**

```bash
.venv/bin/python -m pytest -q tests/test_concept_lifecycle.py tests/test_validate.py
```

## Task 4 — Update the three-OA end-to-end lifecycle

**Files**

- Modify: `tests/test_concept_lifecycle_e2e.py`
- Modify: `tests/fixtures/idea-concept-solution/topology.yaml`

**RED then GREEN**

Update the fixture to represent:

```text
3 OA × 10 Seeds
  -> 3 OA × 5 confirmed Seeds
  -> 15 initial Concepts
  -> 2–4 globally selected Concepts
```

Assert equality—not a subset—between confirmed Seed IDs and root Concept source
IDs. Generate valid Concept-layer assumptions for all initial Concepts and
retain the existing Solution and assumption-lineage checks. Do not change
Artifact revision topology unless a test proves it necessary.

**Verify**

```bash
.venv/bin/python -m pytest -q tests/test_concept_lifecycle_e2e.py
```

## Task 5 — Author the funnel and independent Reviewer behavior

**Files**

- Modify: `src/skills/_bw-shared/idea-concept-solution-lifecycle.md`
- Modify: `src/skills/bw-concept-seed/SKILL.md`
- Modify: `src/skills/bw-concept-seed/references/idea-pool-template.md`
- Modify: `src/skills/bw-concept-development/SKILL.md`
- Modify: `src/skills/bw-concept-development/references/concept-portfolio-template.md`
- Create: `src/skills/bw-concept-development/references/concept-review-contract.md`
- Modify: `src/skills/bw-ideate/SKILL.md`
- Modify: `src/skills/bw-ideate/references/stage.md`
- Modify: `src/skills/bw-resume/references/routing.md`
- Modify: `src/skills/bw-shape/SKILL.md`
- Modify: affected `tests/test_skill_bw_*.py`
- Modify/add: affected `evals/bw-concept-seed/`,
  `evals/bw-concept-development/`, and `evals/bw-ideate/` manifests

**RED**

First update static skill tests and behavioral manifests to require:

- hard 10–15 and 5–8 ranges;
- structured cuts with rationales;
- no use of new-format `shortlist.recommended`;
- exact confirmed-to-Concept development;
- a fresh independent reviewer context;
- producer prohibition from self-scoring;
- reviewer ownership of hard/soft evaluation and recommended action;
- reviewer prohibition from human-only decisions;
- a maximum of two review/revision cycles;
- fail-closed behavior when independent review cannot run; and
- resume/Shape routing that respects Review readiness.

Add RED scenarios for invalid cut contracts, shortlist counts, incomplete
confirmation, duplicate Seed development, Reviewer authority, and unavailable
Reviewer execution. Validate manifests deterministically; do not run paid LLM
repetitions in this task.

**GREEN**

Update the source skills and templates. Idea Pool review remains a lightweight
batch check inside Seed generation. Concept production delegates a read-only,
fresh-context review using the new reference contract; the Reviewer owns
evaluation fields, and the producer only revises from its structured payload.
No new public stage, router, gate, or Artifact kind is created.

Merge these edits with the existing uncommitted visualization instructions.

**Verify**

```bash
.venv/bin/python -m pytest -q tests/test_skill_bw_concept_seed.py tests/test_skill_bw_concept_development.py tests/test_skill_bw_ideate.py tests/test_skill_bw_resume.py tests/test_skill_bw_shape.py
```

## Task 6 — Project Idea Pool decision evidence from Artifact Markdown

**Files**

- Modify: `tests/test_bwkit_html.py`
- Modify: `src/bwkit/html.py`

**RED**

Add tests that parse real Markdown frontmatter and preserve
`opportunity_areas`, `review`, `decisions`, `concepts`, and `exit`. Add
source-of-truth tests proving no rationale, finding, or decision appears unless
it exists in parsed Artifact Markdown or is a deterministic count/classification.

Test the Idea view for:

- OA grouping and per-OA counts;
- every Seed remaining in the DOM;
- canonical ID, sentence, Insight refs, cluster, Strategy filter, derived
  keep/cut state, rationale, and human state;
- all/keep/cut read-only filters;
- `needs-revision` suppression of the human-decision prompt; and
- explicit legacy labels without fabricated rationale or Review data.

**GREEN**

Extend the current reader with pure projection helpers. New format reads
`recommended_cuts`; legacy format reads `recommended` only as an old
elimination list. JavaScript may toggle `hidden` and ARIA/filter counts but may
not submit, fetch, use local storage, or persist state.

**Verify**

```bash
.venv/bin/python -m pytest -q tests/test_bwkit_html.py
```

## Task 7 — Add Concept comparison, active/history views, and case journey

**Files**

- Modify: `tests/test_bwkit_html.py`
- Modify: `src/bwkit/html.py`

**RED**

Lock these projection rules:

```text
history = decision in {killed, merged} OR merge_into is non-empty
active  = every other Concept
selected = decision == selected OR ID is in exit.selected_concept_ids
```

Test an OA-grouped compact comparison before full cards, reviewer results from
`evaluation` and `review.portfolio_findings`, assumptions, Review status,
active/history counts, a closed history `<details>`, and read-only OA/action/
decision filters. Findings must never be inferred from a false hard score.

Add a generated `#case-journey` view derived only from the latest parsed
Artifact items. Make it the Artifact reader default while preserving Artifact
hash deep links, back/forward navigation, and Knowledge reader behavior. Ideate
must expose Idea Pool and Concept Portfolio counts and status. Missing stages
and legacy Review states are shown honestly, not promoted to complete.

**GREEN**

Incrementally extend the existing Concept-card renderer and routing script.
Use `evaluation.recommended_action` as canonical; support any existing top-level
legacy fixture only as a defensive fallback. Keep selected Concepts active,
move killed/merged items to history, and render the Markdown body after the
structured decision evidence.

**Verify**

```bash
.venv/bin/python -m pytest -q tests/test_bwkit_html.py tests/test_concept_contract.py
```

## Task 8 — Deploy safely and verify the complete system

**Files**

- Generated managed copies under `.claude/skills`, `.agents/skills`, and
  `_bewater/bwkit` via `install.sh` only
- Derived `_bewater-output/html/` for local verification only

**Pre-deploy**

1. Run a full copy install into a temporary project.
2. Smoke-test deployed skills, standalone `bwkit html`, and current validators.
3. Record hashes of active `_bewater/{config,ledger,conditions}.yaml`, records,
   and `_bewater-output/{artifacts,knowledge,sources}`.
4. Confirm source/deployed differences are limited to managed targets.

**Deploy**

Run the repository installer only after all source tests pass. A full install is
required to deploy both skills and standalone `bwkit`; `--skills-only` is not
sufficient. The installer must report existing project state as valid and
already initialized.

After deployment, compare the protected hash manifest byte-for-byte. Any change
to state or canonical output aborts acceptance. Regenerate HTML as a derived
projection only; do not regenerate Artifact Markdown.

**Final verification**

```bash
.venv/bin/python -m pytest -q \
  tests/test_concept_lifecycle.py \
  tests/test_concept_lifecycle_e2e.py \
  tests/test_validate.py \
  tests/test_skill_bw_concept_seed.py \
  tests/test_skill_bw_concept_development.py \
  tests/test_skill_bw_ideate.py \
  tests/test_skill_bw_resume.py \
  tests/test_skill_bw_shape.py \
  tests/test_bwkit_html.py \
  tests/test_concept_contract.py \
  tests/test_installer_copy.py \
  tests/test_eval_isolation.py

.venv/bin/python -m pytest --cov=bw --cov=bwkit --cov-report=term-missing
.venv/bin/python -m bw validate .
.venv/bin/python -m bwkit html .
```

Visually inspect the generated journey, Idea Pool, Concept comparison/cards,
filters, legacy labels, and deep links at desktop and narrow widths. The active
legacy case should remain validator-clean, display its real 9/9/10 and 30-item
history truth, classify terminal history without hiding it, and show no invented
Review conclusions.

## Commit and handoff discipline

- Commit only explicit task files; never stage unrelated dirty files.
- For already modified files, inspect the complete diff before staging. If the
  whole file cannot be attributed to the two approved HTML/Review designs,
  leave it unstaged and report it rather than absorbing user work.
- Do not commit derived `_bewater-output/html/` unless the user separately asks
  to version generated output.
- Final handoff reports tests, coverage, deployment parity, unchanged protected
  hashes, and any legacy limitations.
