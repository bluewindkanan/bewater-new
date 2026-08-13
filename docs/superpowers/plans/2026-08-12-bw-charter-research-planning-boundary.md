# BeWater Charter and Research Planning Boundary — Implementation Plan

## Objective

Simplify the Immersion-to-Discover handoff without weakening G1/G2 risk controls:

- Project Charter defines the project only.
- Initial Assessment is a Charter-only readout for the user and is never a Research input.
- Discover creates one living Research Plan containing the Learning Plan and Research Design.
- The Knowledge Base is the Research Plan index plus canonical Evidence records.
- Research Planning performs the first selective root-assumption projection; Define still owns the
  complete G1 assumption inventory and Achilles review.

## F212 relationship to preserve

F212 treats Research Planning as the work that initializes the Learning Plan and Knowledge Base;
its deliverable is the Research Plan. Therefore:

    Research Plan
    ├── Research Objective
    ├── Learning Plan
    ├── Research Design
    ├── Knowledge Base Index
    └── Sprint synthesis and Insight Readiness

Reference material:

- `Frog:f212 General/F212 approach/Day 1, Intro & Insights/1.1 Intro to Discovery.pptx`
- `Frog:f212 General/F212 approach/20180808_Fahrenheit 212 tools_V1.0_Final.pptx`

## Decisions

| Area | Decision |
|---|---|
| Charter | Keep challenge, intent, outcome, scope, constraints, success definition, and explicit Unknowns. Remove research planning and ledger writes. |
| Initial Assessment | Read the exact Charter revision only. Produce a short user-facing checkpoint. Create no Evidence and supply no downstream input. |
| Research Plan | Keep one living `kind: research` artifact. Learning Plan and Research Design are sections, not separate artifacts. |
| Knowledge Base | Use `_bewater/evidence.yaml` for atomic findings and the Research Plan for question-to-evidence indexing. Add no separate database or artifact. |
| Root assumptions | During Research Planning, project only material, uncertain, falsifiable starting beliefs. Use no numeric quota and permit zero projections. |
| G1 inventory | `bw-assumption-map` remains the Define-stage owner of completing the G1 inventory and Achilles review. Existing Gate criteria remain unchanged; never create a fake assumption merely to pass them. |
| Routing | Charter is the formal prerequisite for Discover. Assessment is advisory; the user may explicitly continue without it. |
| HTML | Treat as a later read-only projection with no artifact ID, lineage, or role in Research. |

## Target flow

    bw-project-charter
      -> Charter rN
      -> no assumption-ledger mutation

    bw-initial-assessment
      -> reads Charter rN only
      -> writes Assessment rN for the user

    user chooses Enter Discover

    bw-discovery-research: Research Planning
      -> derives Research Plan from Charter rN
      -> initializes Learning Plan, Research Design, and Knowledge Base Index
      -> projects zero or more qualifying root assumptions
      -> immediately derives Achilles status and durable L4 obligations

    bw-discovery-research: Research Sprint
      -> executes the Research Design
      -> commits atomic Evidence
      -> updates the Knowledge Base, assumptions, and synthesis
      -> appends the next Research Plan revision

    Define / bw-assumption-map
      -> revisits assumptions after research and strategy formation
      -> completes the current G1 inventory contract
      -> confirms the Achilles quadrant and L4 obligations before G1

## Minimal contracts

### Learning Plan: learning intent

Use stable artifact-local IDs such as `LP-001` and only these required fields:

| Field | Purpose |
|---|---|
| `id` | Stable reference within the Research artifact chain |
| `learning_objective` | What must be learned |
| `starting_state` | `known`, `think-known`, `unknown`, or `assumption` |
| `starting_view` | Current belief or explicit Unknown |
| `decision_relevance` | What later judgment this learning may change |
| `lens` | Material 4C or challenge-specific lens |
| `priority` | Relative learning value and risk |
| `ledger_ref` | Optional exact assumption ref when projection criteria are met |

The Learning Plan owns the learning intent, not the current answer state. Initialization asks:

1. What do we know or think we know?
2. What do we not know that we want to know?
3. What might we be assuming?

### Research Design: next-Sprint execution

Fully plan only the next Sprint. Each mission needs:

- a stable local ID and one or more Learning Plan refs;
- the evidence needed and smallest suitable method/source bundle;
- exclusions, dependencies, owner, and bounded budget;
- a stop condition, expected output, and limitation.

### Knowledge Base Index: cognition state

Initialize one row for every Learning Plan item. This is the single authority for whether and how a
learning objective has been answered:

| Field | Purpose |
|---|---|
| `learning_ref` | Learning Plan item |
| `answer_status` | `not-researched`, `partial`, `answered`, `dropped`, or `gap-accepted` |
| `evidence_refs` | Exact Evidence revisions; initially empty |
| `current_answer` | Evidence-bounded synthesis; initially `Not researched` |
| `contradictions` | Unresolved conflicting evidence |
| `remaining_gap` | What is still unknown and why it matters |

Do not duplicate `answer_status` in the Learning Plan. Do not create an empty `evidence.yaml`;
create it with the first real finding.

### Assumption projection, Achilles, and lineage

Project a Learning Plan item only when it is a starting belief whose failure could materially change
direction, is uncertain, and has an observable disconfirming signal.

- Research Plan `derived_from` contains the exact Charter revision only.
- New projected root assumptions derive from the Research Plan revision that introduced them.
- Research Plan may show `ledger_ref`, but assumption refs never enter its `derived_from` list.
- `impact=high` and `uncertainty=high` immediately derives `is_achilles_heel` and opens the existing
  durable L4 obligation; Research Planning does not replace or weaken that machine.
- Define's `bw-assumption-map` reclassifies and completes the inventory before G1.
- G1/G2 Gate semantics, including current L4 hard-gate behavior, remain unchanged by this refactor.
- Initial Assessment claims never become assumptions or Evidence.

## Existing-to-target section mapping

Do not append new sections beside equivalent old ones:

| Existing Research section/contract | Target location | Rule |
|---|---|---|
| `Research Frame` | `Research Objective` | Rename and remove active-assumption snapshot from formal lineage. |
| `Living Learning Agenda` | `Learning Plan` + `Knowledge Base Index` | Intent stays in Learning Plan; answer status, accepted gaps, and Evidence refs move to the index. |
| `Research Mission contract` | `Research Design` | Reuse mission fields; do not create a second mission-planning block. |
| `Latest Research Sprint` | `Sprint Record` | Keep only what was actually executed, deviations, and validity-relevant limitations. |
| `Sprint Synthesis and Plan Delta` | `Sprint Synthesis` | Keep learned/contradicted/reframed and the next-plan delta in one section. |
| `Remaining uncertainty` | `Knowledge Base Index.remaining_gap` | Remove the separate section; use a short cross-objective summary only when needed for handoff. |
| `Insight Ingredients and Insight Readiness` | unchanged | Preserve as the Discover-to-Define handoff. |
| `Stable versus transient`, packets, fan-in, self-review | reference contract only | Keep execution instructions out of the user artifact. |

Revision 1 has four core sections: Research Objective, Learning Plan, Research Design, and Knowledge
Base Index. Sprint Record/Synthesis and Insight Readiness appear only after execution. Each section
owns one state; no old and new equivalent sections coexist.

## Migration and integrity contract

Historical records are immutable. Do not force existing projects to rerun Research Planning and do
not rewrite prior assumption revisions.

### Grandfather rule

- An existing root assumption whose current record derives from an exact Charter revision remains
  valid and active if that revision exists. It is legacy lineage, not an orphan.
- An exact `assumption:A-NNN@n` ref resolves when revision `n` is either the current record or a
  complete snapshot in that record's `history[]`. This preserves append-only artifacts that pin an
  older assumption revision after a later record update.
- Generic resolution establishes existence only. Current-head contracts such as Concept/Solution
  pin sets may still report an archived revision as stale; do not weaken those checks.
- The system-wide `bw validate` accepts these resolvable historical refs. `bwkit check integrity`
  remains schema-agnostic and unchanged.
- Generic `bw validate` continues checking only exact, resolvable lineage. The Research transaction
  validator enforces the migration boundary by comparing the staged ledger with its pre-transaction
  revision: pre-existing Charter-derived roots may retain that provenance, while every newly added
  root must derive from the exact Research Plan revision that creates it.

### No-reparent rule

Never replace a legacy root's Charter provenance with Research provenance under the same A-ID.

- Evidence, validation, risk, or status updates may bump the legacy A-ID while retaining its exact
  Charter `derived_from`; the prior record remains in `history[]`.
- If Research materially changes the belief's identity or scope, kill or merge the legacy record and
  create a distinct Research-derived root with a new A-ID.
- Do not create a new A-ID for wording-only edits or duplicate an equivalent active belief.

Do not revise old Assessment or Research artifacts merely to refresh their assumption pins. Their
exact refs continue to resolve through the archived record snapshots.

Legacy assumptions remain grandfathered indefinitely. No creation timestamp, schema flag, or
guessed project age distinguishes old from new; existence in the pre-transaction ledger plus an
unchanged provenance edge is the enforceable rule.

### Zero-projection and G1 rule

- Research Planning succeeds with zero qualifying root assumptions; zero is a legitimate result,
  not a validation error.
- A project may continue through Discover and enter Define with zero assumptions.
- Zero assumptions do not satisfy G1. `bw-assumption-map` must add or confirm real
  strategy/opportunity risks and complete the existing inventory/Achilles contract before G1.
- `no quota` applies to Research Planning projection; it does not waive a downstream Gate criterion.

## Downstream impact

| Consumer | Required change |
|---|---|
| `bw-assumption-map` | Accept Research-derived roots and grandfathered Charter roots; keep ownership of G1 inventory completion and Achilles review. |
| `bw-define` | Continue reporting inventory/Achilles readiness and route to `bw-assumption-map` when incomplete. |
| `bw-strategy-gate` and `gate-criteria.md` | No methodology change. Confirm that readiness reads ledger state rather than assuming Charter created it. |
| `bw/gate_scan.py` | No planned change. Add regression coverage proving source-artifact provenance does not alter G1 scoring. |
| G2 readers | No change: read the ledger's durable L4 obligations regardless of which capability created them. |

The current runtime's Achilles/L4 derivation stays in `schema.Assumption`; only the root creation
point and accepted legacy provenance change.

## Implementation checklist

### 1. Lock behavior with RED tests

- [ ] Charter validates and persists without `--ledger-file`, a ledger snapshot, or ledger mutation.
- [ ] Assessment identity, freshness, and lineage use branch plus exact Charter revision only.
- [ ] Immersion readiness is Charter-based; Assessment remains an explicit user checkpoint.
- [ ] Discover cannot consume Assessment content or require pre-existing assumptions.
- [ ] Research Plan contains Learning Plan, Research Design, and Knowledge Base Index.
- [ ] Learning Plan has no answer-status field; Knowledge Base Index is the status authority.
- [ ] Research Planning can project zero assumptions and still complete.
- [ ] A new high/high projection creates the existing durable L4 obligation.
- [ ] A legacy Charter-derived assumption remains valid under `bw validate` and the new validator.
- [ ] After a legacy root record update, old artifacts pinning its archived revision
      remain referentially valid; current-head pin contracts still detect stale refs where required.
- [ ] A root newly added by a Research transaction is rejected unless it derives from that exact
      Research Plan revision; grandfathered-root updates retain their Charter provenance.
- [ ] Zero assumptions can finish Research Planning and enter Define, but cannot satisfy G1.
- [ ] Existing G1/G2 Achilles and L4 outcomes are unchanged for equivalent ledger state.
- [ ] `evidence.yaml` appears only with a real source-bounded finding.
- [ ] Legacy artifact revisions remain readable and are never rewritten.

Primary tests:

- `tests/test_skill_bw_project_charter.py`
- `tests/test_charter_draft_validator.py`
- `tests/test_skill_bw_initial_assessment.py`
- `tests/test_skill_bw_immersion.py`
- `tests/test_skill_bw_discover.py`
- `tests/test_skill_bw_discovery_research.py`
- `tests/test_research_plan_validator.py` — create
- `tests/test_skill_bw_assumption_map.py`
- `tests/test_skill_bw_strategy_gate.py`
- `tests/test_gate_scan.py`
- `tests/test_validate.py`

### 2. Reduce Charter to project definition

- [ ] Remove root-assumption generation, validation, persistence, and handoff fields.
- [ ] Remove 4C questions, research methods, evidence needs, and prioritized research exits.
- [ ] Preserve user intent, provenance, Money/Magic framing, scope, constraints, success, and Unknowns.
- [ ] Remove `--ledger-file` from Charter validation/emission and update its self-review/test contract.
- [ ] Persist only the Charter artifact and its counter update through `bwkit plan apply`.

Files:

- `src/skills/bw-project-charter/SKILL.md`
- `src/skills/bw-project-charter/references/charter-template.md`
- `src/skills/bw-project-charter/references/self-review-contract.md`
- `src/skills/bw-project-charter/references/persistence-plan.md`
- `src/skills/bw-project-charter/scripts/validate_draft.py`
- `src/skills/bw-project-charter/scripts/emit_write_plan.py`
- `tests/test_charter_draft_validator.py`

Move, do not discard, the reusable projection semantics from
`src/skills/bw-project-charter/references/root-assumptions.md` into
`src/skills/bw-discovery-research/references/root-assumption-projection.md`; remove the Charter copy
only after all references point to the new owner.

### 3. Isolate Assessment and correct routing

- [ ] Match Assessment by branch and exact Charter revision; remove assumption snapshot handling.
- [ ] Limit the report to Charter restatement, external reality check, material risks/Unknowns, what
      the user should inspect, and exact sources.
- [ ] Remove required Candidate Insights, Most Promising Direction, and Discover Mission sections.
- [ ] Mark the report explicitly as non-input to Research, Knowledge Base, assumptions, and Evidence.
- [ ] Make Charter the only formal Discover input.
- [ ] Route a missing or stale Research Plan to Research Planning, not back to Charter because
      assumptions are absent.

Files:

- `src/skills/bw-initial-assessment/SKILL.md`
- `src/skills/bw-initial-assessment/references/initial-assessment-template.md`
- `src/skills/bw-initial-assessment/references/write-plan.md`
- `src/skills/bw-immersion/SKILL.md`
- `src/skills/bw-immersion/references/stage.md`
- `src/skills/bw-discover/SKILL.md`
- `src/skills/bw-discover/references/stage.md`
- `README.md`

### 4. Make Research Plan the single Discover planning artifact

- [ ] Keep the existing `research` artifact kind and append-only ART revision chain.
- [ ] Apply the existing-to-target mapping; do not leave duplicate old/new sections.
- [ ] Use local LP/RM IDs; add no global counters.
- [ ] Persist Research Plan r1 before executing the first Sprint.
- [ ] Retain adaptive Sprints, selective 4C coverage, method bundles, synthesis, and Insight
      Ingredients; keep worker topology and intermediate packets transient.
- [ ] Implement the new multi-write transaction with explicit low-freedom helpers.

Files:

- `src/skills/bw-discovery-research/SKILL.md`
- rename `src/skills/bw-discovery-research/references/discover-plan.md` to
  `src/skills/bw-discovery-research/references/research-plan.md`
- `src/skills/bw-discovery-research/references/4c-framework.md`
- `src/skills/bw-discovery-research/references/method-bundles.md`
- create `src/skills/bw-discovery-research/references/root-assumption-projection.md`
- create `src/skills/bw-discovery-research/references/persistence-plan.md`
- create `src/skills/bw-discovery-research/scripts/validate_research_plan.py`
- create `src/skills/bw-discovery-research/scripts/emit_write_plan.py`
- `src/skills/_bw-shared/ledger-schema.md` — clarify legacy/new root lineage and Evidence/index only

### 5. Preserve transactional writes and legacy lineage

- [ ] Research Planning transaction writes Research Plan and the artifact counter as one resumable
      `bwkit plan apply` plan; include a ledger CAS only when assumptions are added or existing
      records are changed.
- [ ] Sprint transaction writes the next Research Plan revision, real Evidence, and affected
      assumption revisions as one resumable plan.
- [ ] Validate LP/RM refs, Evidence refs, exact Charter lineage, ledger projection, idempotent retry,
      CAS conflict, and partial-application recovery before mutation.
- [ ] Resolve artifact-pinned assumption refs against the current record plus `history[]` in generic
      validation, while preserving contract-specific stale-head checks. Versioned
      assumption-to-assumption traversal is outside this refactor.
- [ ] Implement the grandfather and no-reparent rules exactly; do not mass-migrate projects.
- [ ] Normalize old Research sections only by appending a new Research revision.
- [ ] Treat old Assessment revisions with assumption lineage as readable but stale.

Runtime files required for historical exact-ref resolution:

- `src/bw/validate.py`
- `tests/test_validate.py`

### 6. Protect Define and Gate consumers

- [ ] Update `bw-assumption-map` references and evals for Research-derived and grandfathered roots.
- [ ] Keep Define routing to `bw-assumption-map` when G1 inventory/Achilles review is incomplete.
- [ ] Confirm G1 reads the current ledger without requiring Charter-derived roots.
- [ ] Prove equivalent ledger state produces identical G1/G2 Achilles and L4 results before and
      after this refactor.

Files:

- `src/skills/bw-assumption-map/SKILL.md`
- `src/skills/bw-assumption-map/references/assumption-map.md`
- `src/skills/bw-define/SKILL.md`
- `src/skills/bw-define/references/stage.md`
- `src/skills/bw-strategy-gate/SKILL.md`
- `src/skills/_bw-shared/gate-criteria.md` — edit only if it implies Charter-owned creation
- `src/bw/gate_scan.py` — no behavior change expected; change only if a RED provenance test proves
  hidden source coupling
- affected tests and evals for assumption-map, Define, G1, and G2

### 7. Evaluate, deploy, and verify

- [ ] Update affected structural tests and behavior evals from Charter-only fixtures.
- [ ] Add fixtures for: no assumptions, grandfathered Charter roots, new Research roots, no Achilles
      identified, and an open durable L4 obligation.
- [ ] Run targeted tests, full regression, `bw validate`, artifact-chain integrity, and coverage;
      require at least 80%.
- [ ] Test installation in a temporary initialized project first.
- [ ] Deploy authored skills through `install.sh --skills-only`; never hand-edit deployed copies.
- [ ] Confirm implementation did not modify active `_bewater/` or `_bewater-output/` state.

Because implementation spans more than three files, execute after the shared RED contract with
agents owning non-overlapping areas: Charter, Assessment/routing, Research Plan, and Define/Gates.
The primary agent owns shared contracts, transaction integration, evaluations, final regression,
and diff review.

## Verification commands

```bash
.venv/bin/python -m pytest \
  tests/test_skill_bw_project_charter.py \
  tests/test_charter_draft_validator.py \
  tests/test_skill_bw_initial_assessment.py \
  tests/test_skill_bw_immersion.py \
  tests/test_skill_bw_discover.py \
  tests/test_skill_bw_discovery_research.py \
  tests/test_research_plan_validator.py \
  tests/test_skill_bw_assumption_map.py \
  tests/test_skill_bw_strategy_gate.py \
  tests/test_gate_scan.py \
  tests/test_validate.py -q

.venv/bin/python -m pytest --cov=bw --cov=bwkit --cov-report=term-missing
.venv/bin/python -m bw validate <temporary-project-root>
```

Run `bwkit check integrity` with the temporary project's artifact-chain records on stdin; it does
not accept a project-root argument and does not validate assumption lineage.

## Acceptance criteria

- Charter alone is sufficient to enter Discover and never writes assumptions.
- Assessment depends only on Charter, remains user-facing, and is never consumed downstream.
- One Research Plan contains Learning Plan, Research Design, and a non-duplicative Knowledge Base.
- Research Planning may create zero assumptions; only qualifying beliefs are projected.
- New roots derive from Research; resolvable legacy Charter roots remain valid without forced rerun.
- High/high projection still opens the durable L4 obligation; G2 behavior is unchanged.
- Zero Research projections do not satisfy G1; Define/G1 and all L4 hard-gate behavior remain intact.
- All state mutation uses transactional `bwkit plan apply`.
- Historical state is preserved, tests pass, and measured coverage remains at least 80%.

## Non-goals

- Separate Learning Plan, Research Design, or Knowledge Base artifacts.
- A new Gate, approval record, mode selector, or worker-count prompt.
- Importing Assessment claims or citations into Research.
- A fixed number of questions, assumptions, missions, methods, sources, or Sprints.
- Mass-migrating or re-parenting active projects.
- New artifact kinds or project-state directories without a failing contract that requires them.
- HTML as canonical state or as a prerequisite for this refactor.
