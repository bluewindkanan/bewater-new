# BeWater Realization — Global Design and Change-Driven Build

- **Date**: 2026-08-21
- **Status**: Draft for written-spec review
- **Scope**: Post-G2 Design and Build architecture, with extension points for later realization stages
- **Supersedes after approval**: `docs/superpowers/plans/2026-08-20-bx-realization-openspec-core-gsd-views.md`

## 0. Decision Summary

BeWater becomes an end-to-end product methodology. G2 remains the investment decision boundary,
but it is no longer the toolkit boundary. A formal G2 Go hands a validated Solution into a new
Realization segment:

```text
Concept -> Solution -> G2 Baseline -> Realization Handoff
        -> Design Baseline -> Change-driven Build -> verified product increments
```

The first Realization implementation covers Design and Build. It establishes contracts that later
Launch, Grow, G3, and G4 work can consume without defining those later workflows prematurely.

The design combines four proven ideas without installing three overlapping operating systems:

1. **GSD global planning** contributes project questioning, requirements, feature slicing, roadmap,
   and current-state views.
2. **OpenSpec core** contributes current specs plus proposal, delta specs, technical design, tasks,
   apply, verify, and archive.
3. **Feature Workflow practices** contribute independent user-value slices, parent/child roll-up,
   explicit dependencies, blocking, and acceptance scenarios.
4. **Requirements-management practice** contributes baselines, typed bidirectional traceability,
   impact analysis, suspect links, and separate lifecycle and verification status.

BeWater does not depend on the GSD or OpenSpec CLI. Deterministic operations are reimplemented as
native `python -m bw ...` commands. Agent judgment remains in skills. The OpenSpec core workflow is
adapted rather than simplified away.

## 1. Goals and Non-goals

### 1.1 Goals

1. Start product realization directly from a validated Solution and its G2 baseline.
2. Create a coherent global product design before detailed implementation begins.
3. Preserve enough flexibility for detailed design to emerge change by change during Build.
4. Trace every implemented behavior back to an approved requirement and ultimately to the
   validated Solution.
5. Allow Build discoveries to revise Design safely without rewriting historical baselines.
6. Keep routers thin, capabilities focused, and deterministic state changes inside the BeWater CLI.
7. Remove runtime dependence on upstream GSD and OpenSpec installations.

### 1.2 Non-goals

- Port the complete GSD command set, workflow engine, hooks, or Git conventions.
- Port every OpenSpec skill, profile, telemetry, onboarding, or bulk-operation feature.
- Use directory renames, Git branches, or worktrees as canonical requirement state.
- Complete a feature merely because its task checkboxes are checked.
- Let Build silently broaden the G2-approved product boundary.
- Define detailed Launch, Grow, G3, or G4 behavior in this design.
- Replace BeWater's existing evidence, gate, baseline, or backtrack governance.

## 2. Constitutional Boundaries

### 2.1 Human and machine authority

- Skills may draft, recommend, classify impact, and prepare actions.
- The accountable human approves Design Baselines, requirement changes, scope changes, and Change
  proposals.
- The CLI validates, writes, indexes, merges, archives, computes impact, and reconciles views. It
  never chooses a product or gate decision.
- Routers navigate and invoke one selected capability. They do not produce capability artifacts
  inline.

### 2.2 Baseline authority

Three truth layers coexist because they answer different questions:

| Truth | Question answered | Mutation rule |
|---|---|---|
| G2 Baseline | Why and within what validated Solution boundary should this exist? | Immutable; material changes use `bw-backtrack` and re-pass G2 |
| Design Baseline | What global product structure and delivery plan did humans approve? | Immutable snapshot; later approved design revisions create a successor baseline |
| Current Specs | What behavior is the product currently required to provide? | Updated only by archiving an approved, verified Change |

An active Change is proposed future truth. It never becomes current truth merely because code was
written.

### 2.3 Global design versus change design

Design is intentionally progressive:

- **Global Design** defines product capabilities, experience flows, system boundaries, cross-cutting
  constraints, non-functional requirements, feature slices, dependencies, and roadmap outcomes.
- **Change Design** defines the implementation-specific technical decisions necessary for one
  bounded Change.

Global Design must be sufficient to coordinate the whole product, but it must not attempt to
pre-design every implementation detail. Change Design must conform to the active Design Baseline or
trigger a governed design revision.

## 3. Skill Architecture

### 3.1 Routing map

```text
G2 Go
  -> bw-design (router)
       -> bw-project-design initialize
       -> bw-project-design revise
  -> approved Design Baseline
  -> bw-build (router)
       -> bw-change-propose
       -> bw-change-apply
       -> bw-change-verify
       -> bw-change-archive
       -> bw-project-design revise  [design gap]
       -> bw-backtrack              [validated boundary impact]
```

### 3.2 Router contracts

#### `bw-design`

`bw-design` is a router. It reads the G2 handoff, Design state, open design revisions, and active
baseline. It then reports status and invokes exactly one selected capability:

- no Design exists -> `bw-project-design initialize`;
- an approved Build discovery requires global revision -> `bw-project-design revise`;
- a draft awaits human review -> present review/resume options;
- an active Design Baseline exists -> route to `bw-build` when requested.

It does not write Project, Requirements, Feature Map, Roadmap, Architecture, or Specs itself.

#### `bw-build`

`bw-build` is a router. It reads the active Design Baseline, feature readiness, dependencies, active
Changes, verification state, and suspect links. It routes the user to one of the four Change
capabilities, Design revision, or baseline-aware backtracking.

When several features or Changes are eligible, it presents the choices and stops. When the user
names an eligible target and the next action is deterministic, it may invoke the matching capability
directly. It never writes proposal, code, verification evidence, or archive state inline.

### 3.3 Design capability

#### `bw-project-design`

This capability is the BeWater equivalent of GSD's project initialization, but its intake is a
validated G2 handoff rather than an untested idea.

It has two modes:

- **initialize**: question the team about delivery constraints and implementation decisions, then
  draft the first global product design;
- **revise**: assess an approved Design Gap, draft the smallest coherent revision, and show its
  impact before any baseline or current spec changes.

It produces drafts and stops for the accountable human. A native CLI operation creates a Design
Baseline only after explicit approval.

### 3.4 OpenSpec-derived Change capabilities

BeWater keeps four OpenSpec core capabilities. Their reasoning and artifact depth should remain
close to upstream behavior; naming, inputs, governance, and runtime operations become BeWater-native.

| Skill | Responsibility | Stop condition |
|---|---|---|
| `bw-change-propose` | Create or resume a Change; draft proposal, delta specs, change design, and tasks; analyze trace and baseline impact | Apply-ready artifacts validated and human approval requested |
| `bw-change-apply` | Implement approved tasks against the Change context; keep task progress and implementation evidence current | Tasks complete, blocked, or a Design Gap is detected |
| `bw-change-verify` | Verify implementation against delta requirements, scenarios, design, tasks, tests, and global constraints | Verification report produced; never archive automatically |
| `bw-change-archive` | Require approval and passing verification; merge deltas into current specs; archive atomically; reconcile requirements, features, roadmap, and traceability | Archive committed or failed without partial state |

OpenSpec's separate explore, new, continue, fast-forward, sync, onboarding, and bulk-archive skills do
not become first-class BeWater skills:

- exploration is covered by `bw-brainstorm`;
- creation, continuation, and apply-ready artifact generation are modes of `bw-change-propose`;
- spec synchronization is a deterministic `bw change sync` operation used by archive;
- onboarding is covered by `bw-project-design`;
- bulk archive is deferred until real usage justifies it.

## 4. Shape-to-Design Handoff

### 4.1 Handoff chain

There is no direct Concept-to-Build handoff. A Concept is an option; a complete validated Solution is
the execution contract.

```text
Concept Portfolio
  -> selected complete Solution
  -> G2 decision
  -> immutable G2 Baseline
  -> portable Realization Handoff v2
  -> global Design draft
  -> human-approved Design Baseline
```

### 4.2 Realization Handoff v2

The current handoff schema is too thin for global planning. Version 2 must be portable and contain:

| Section | Required content |
|---|---|
| Lineage | Concept Portfolio refs, selected Concept refs, complete Solution refs, G2 decision, and G2 Baseline |
| Intent | target users, jobs/outcomes, value logic, business logic, and core mechanism |
| Fixed boundary | G2-confirmed invariants, explicit scope, out-of-scope, and assumptions that would require backtracking if falsified |
| Flex zone | implementation choices and observations that Design or Build may refine without re-passing G2 |
| Evidence | key experiments, success criteria, evidence refs, known limitations, and open observations |
| Delivery seeds | candidate capabilities, dependencies, risks, resource envelope, constraints, and milestone hypotheses |
| Materialization | copies of every required source artifact plus exact ref, revision, digest, and originating project identity |

Path-only references are insufficient. A handoff copied to another delivery repository must remain
understandable and verifiable without access to the original working tree.

### 4.3 Compatibility

The native CLI may read Handoff v1 only to produce a migration report. Initialization requires a v2
handoff or an explicit, reviewed enrichment step; it must not invent missing G2 intent or scope.

## 5. Global Product Design

### 5.1 Outputs

`bw-project-design initialize` drafts the following coherent set:

| Artifact | Purpose |
|---|---|
| `PROJECT.md` | product intent, G2 boundary, users, constraints, success outcomes, and non-goals |
| `REQUIREMENTS.md` | human-readable requirement catalog grouped by capability and release intent |
| `FEATURE-MAP.md` | independent user-value slices, parent/child relations, dependencies, and requirement coverage |
| `ROADMAP.md` | outcome-oriented phases, entry/exit conditions, dependencies, and target features |
| `ARCHITECTURE.md` | system boundaries, key flows, interfaces, data ownership, cross-cutting constraints, and ADR refs |
| `STATE.md` | current milestone, active feature/Change, blockers, decisions pending, and next safe actions |
| `TRACEABILITY.md` | generated end-to-end coverage, gaps, suspect links, and verification summary |
| current specs | normative capability behavior expressed as requirements and acceptance scenarios |

The Markdown views are optimized for humans. Stable identity, typed links, statuses, digests, and
baseline membership are stored as structured state and rendered into the views. Humans do not
maintain duplicate status tables by hand.

### 5.2 Design Baseline

After human approval, the CLI creates an immutable Design Baseline containing exact revisions and
digests of:

- the source G2 Baseline and Realization Handoff;
- all global Design artifacts;
- capabilities, requirements, features, and typed links;
- current specs;
- the approved roadmap and architecture decisions;
- unresolved observations and accepted delivery risks.

The baseline records approval but does not imply that every implementation detail is known. A
successor baseline supersedes it; historical Changes remain traceable to the baseline under which
they were proposed.

## 6. Requirements and Feature Management

### 6.1 Model

The model is a typed graph with useful hierarchy, not a single backlog tree:

```text
Validated Solution
  -> Product Capability
       -> Requirement
            -> Acceptance Scenario / Test Evidence

Feature --delivers----------> Requirement
        --scheduled_in------> Roadmap Phase
        --implemented_by----> Change
        --depends_on--------> Feature / Capability
```

Core stable identities are:

- `CAP-NNN`: product capability;
- `REQ-NNN`: normative requirement;
- `FEAT-NNN`: independently valuable delivery slice;
- `CHG-NNN`: one governed spec and implementation change;
- `DB-NNN`: one immutable, human-approved Design Baseline;
- stable scenario IDs scoped to their requirement;
- existing BeWater artifact, evidence, decision, and baseline refs for upstream lineage.

### 6.2 Typed links

At minimum, the graph supports:

- `derived_from`;
- `decomposes_to`;
- `delivers` / `satisfies`;
- `implemented_by`;
- `verified_by`;
- `depends_on`;
- `affects` as a computed reverse view;
- `scheduled_in`;
- `released_in` when release support is later added.

The trace target is:

```text
Concept -> Solution -> G2 Baseline -> Design Baseline -> Capability
        -> Requirement -> Feature -> Change -> Task -> Commit/PR
        -> Test Evidence -> Release
```

### 6.3 Independent status dimensions

A single status field cannot represent delivery truth. Each managed item uses separate dimensions:

```yaml
lifecycle_status: proposed | approved | planned | active | completed | deferred | removed
verification_status: unverified | partial | passed | failed
change_status: clean | changed | suspect
release_status: unreleased | candidate | released
```

Completion rules are explicit:

- a task is complete when its defined work and evidence are complete;
- a Change is implementation-complete when all tasks finish, but remains unverified until
  `bw-change-verify` passes;
- a Feature is complete only when every required scenario is verified, all delivering Changes are
  archived, dependencies are satisfied, and no required link is suspect;
- a Roadmap phase completes only when its outcome and required Feature rules pass.

### 6.4 Feature slicing and queueing

Features are split by independently demonstrable user value, not by technical layers. Parent
Features may roll up child status but cannot hide incomplete children. Dependencies are explicit;
blocked Features remain visible with reason, owner or decision authority, and unblock condition.

Git branches, worktrees, directory names, and queue order are operational aids, never canonical
requirement state.

### 6.5 Suspect links and impact

When an upstream artifact changes, the runtime walks typed links and marks affected downstream links
`suspect`. A suspect link means “review required,” not “invalid.” Reconciliation clears it only after
the responsible capability records one of:

- still valid against the new revision;
- updated to conform;
- deferred or removed with approval;
- routed to `bw-backtrack`.

This preserves bidirectional traceability without hand-maintaining reverse references.

## 7. Change-Driven Build

### 7.1 Standard flow

```text
bw-build selects an eligible Feature or Requirement set
  -> bw-change-propose
       proposal.md
       specs/**/spec.md delta
       design.md
       tasks.md
       impact report
  -> human approval
  -> bw-change-apply
  -> bw-change-verify
  -> human archive approval
  -> bw-change-archive
       merge deltas into current specs
       archive Change
       reconcile graph and human views
```

One Change may deliver several tightly coupled requirements. One Feature may require several
Changes. Those links are explicit; neither entity is forced to masquerade as the other.

### 7.2 Proposal requirements

An apply-ready Change contains:

- motivation, user-visible outcome, scope, non-goals, and affected Features/Requirements;
- ADDED, MODIFIED, and REMOVED requirement deltas with acceptance scenarios;
- technical design appropriate to the Change's complexity;
- ordered tasks with verification expectations;
- dependency and baseline impact analysis;
- links to the active Design Baseline and current spec revisions.

Refactors with no normative behavior change may use an explicit no-spec-delta declaration, but still
require proposal, design as appropriate, tasks, impact analysis, and verification. The validator
rejects an omitted delta with no declaration.

### 7.3 Atomic archive

Archive is a transaction. Validation, spec merge, archive move, graph reconciliation, and generated
view updates either all succeed or leave current truth unchanged. Archive refuses when:

- verification has not passed;
- the proposal lacks required human approval;
- current specs or the Design Baseline changed incompatibly since proposal;
- required links remain suspect;
- merge validation fails.

## 8. Design Gaps Discovered During Build

Build is expected to discover missing detail. It is not allowed to conceal a product-design change
inside implementation.

### 8.1 Classification

| Discovery | Route | Effect |
|---|---|---|
| Implementation detail with no externally observable behavior, requirement, architecture boundary, or roadmap impact | Update the active Change's `design.md` and `tasks.md`, then revalidate | No global Design revision |
| Incomplete design for an approved requirement within the current Solution boundary | Pause apply; invoke `bw-project-design revise` | Smallest global Design revision; update the Change after approval |
| New Feature or Requirement within the current Solution boundary | Pause or split the Change; invoke `bw-project-design revise` | Add requirement/feature, update roadmap/spec draft, analyze downstream impact |
| Change to target user, promised value, business logic, core mechanism, evidence conclusion, or G2-fixed scope | Invoke `bw-backtrack` | Reassess from the owning upstream artifact and re-pass affected gate |

### 8.2 Revision flow

```text
bw-change-apply detects Design Gap
  -> record and pause the affected task
  -> bw-build classifies impact with trace evidence
  -> bw-project-design revise drafts the smallest coherent revision
  -> impact and suspect-link report
  -> accountable human approves, rejects, or routes upstream
  -> create successor Design Baseline when global design changed
  -> update or split the original Change
  -> revalidate and resume
```

Design documents therefore evolve, but approved baselines never mutate. Minor related revisions may
be accumulated into a successor baseline at an approved milestone; a Change may not resume against
an unapproved draft revision.

## 9. Native BeWater CLI

### 9.1 Principle

There is no `gsd` or `openspec` executable dependency. Upstream CLIs are behavioral references and
possible test oracles only. The BeWater CLI owns deterministic realization operations so installed
skills use one state, one lock protocol, one validation model, and one recovery path.

### 9.2 Command surface

The intended surface is:

```text
python -m bw design init <project>
python -m bw design status <project> [--json]
python -m bw design validate <project> [--strict]
python -m bw design baseline <project> --approval-ref <ref>
python -m bw design impact <project> <artifact-or-node>

python -m bw requirement list/show/trace/impact/reconcile ...
python -m bw feature list/status/next/block/unblock ...

python -m bw change new <change> [--feature <id>] [--requirement <id> ...]
python -m bw change list
python -m bw change status <change> [--json]
python -m bw change instructions <change> <artifact> --json
python -m bw change validate <change> --strict
python -m bw change sync <change> --check|--apply
python -m bw change archive <change> --approval-ref <ref>

python -m bw realization status
python -m bw realization trace <id>
python -m bw realization reconcile [--check|--apply]
```

Exact flags may be refined in the implementation plan, but the responsibility split is fixed:

- skills decide what should be proposed and explain judgment;
- CLI commands perform deterministic reads, validation, writes, merges, indexing, and status
  computation;
- `--json` provides stable machine context to skills;
- mutating commands use the existing BeWater lock, revision, diff, backup, and recovery conventions.

### 9.3 Internal modules

The runtime should be decomposed by responsibility rather than placed in `cli.py`:

- realization entity schemas and serialization;
- typed graph and impact traversal;
- Design baseline operations;
- Change artifact graph and validation;
- delta parsing and current-spec merge;
- requirements, feature, and roadmap reconciliation;
- thin CLI parsing and output adapters.

The implementation plan will choose exact module names after comparing these boundaries with the
current `src/bw` patterns.

## 10. Storage and Views

### 10.1 Canonical machine state

Structured realization state lives under `_bewater/` and is changed only through native runtime
operations. It contains stable entities, typed links, current revisions, approvals, baselines,
digests, and reconciliation metadata.

The storage contract is:

```text
_bewater/realization/
  manifest.yaml                 # schema version, next IDs, active Design Baseline, active milestone
  capabilities/CAP-NNN.yaml
  requirements/REQ-NNN.yaml
  features/FEAT-NNN.yaml
  links.yaml                    # canonical forward typed links; reverse impact is computed
  baselines/DB-NNN.yaml         # immutable Design Baseline records
  actions/                      # resumable multi-file operations
```

Partitioning entities by identity prevents one unreviewable monolithic ledger. `manifest.yaml` is a
small index and pointer record, not a duplicate entity store.

### 10.2 Human and normative artifacts

Human-readable global Design, current specs, active Changes, archived Changes, and generated views
live under a dedicated Realization area in `_bewater-output/`. This preserves BeWater's control-state
versus output-artifact boundary while keeping an OpenSpec-like `specs/` and `changes/` shape.

```text
_bewater-output/realization/
  design/
    PROJECT.md
    REQUIREMENTS.md
    FEATURE-MAP.md
    ROADMAP.md
    ARCHITECTURE.md
    STATE.md
    TRACEABILITY.md
  specs/<capability-slug>/spec.md
  changes/CHG-NNN-<slug>/
    proposal.md
    specs/<capability-slug>/spec.md
    design.md
    tasks.md
    verification.md
  changes/archive/YYYY-MM-DD-CHG-NNN-<slug>/
  baselines/DB-NNN/             # materialized immutable snapshot for review and portability
```

These invariants apply:

- current specs and active Changes are separate;
- archived Changes are immutable;
- generated planning/status views are reproducible from structured state and normative artifacts;
- all artifacts remain portable with stable refs and digests;
- skills do not hand-edit `_bewater/` state.

## 11. Failure Handling and Recovery

- Every mutating command acquires the project lock and checks expected revisions.
- Higher schema versions fail closed.
- Interrupted multi-file operations record a resumable action plan.
- Validation errors show the exact artifact, rule, and safe next action.
- Apply stops on a Design Gap instead of marking the task complete.
- Verify failure returns the Change to active or blocked state; it never auto-completes or archives.
- Archive conflict leaves current specs and planning state unchanged.
- Reconcile defaults to check/report unless `--apply` is explicitly requested.
- Baseline-impact ambiguity routes to human review; it is never treated as in-boundary by default.

## 12. Verification Strategy

Implementation follows TDD. New runtime code has at least 80% line coverage, while critical state
transitions receive direct branch and failure-path tests.

### 12.1 Runtime tests

- schema validation and forward-version rejection;
- typed-link integrity, reverse impact, cycles, and suspect propagation;
- Design Baseline creation and immutability;
- Change lifecycle and approval preconditions;
- ADDED/MODIFIED/REMOVED delta parsing and merge behavior;
- no-spec-delta refactor declaration;
- atomic archive rollback and resumable failure;
- feature completion and roadmap roll-up rules;
- deterministic view reconciliation and drift detection;
- Handoff v2 digest and materialization verification.

### 12.2 Skill evals

- `bw-design` and `bw-build` remain routers and do not produce capability artifacts inline;
- `bw-project-design` consumes G2 truth without reopening settled Shape decisions;
- `bw-change-propose` produces the full apply-ready artifact graph;
- `bw-change-apply` stops on a Design Gap;
- `bw-change-verify` does not archive or accept warnings as success;
- `bw-change-archive` requires explicit approval and passing verification;
- G2-boundary changes route to `bw-backtrack`.

### 12.3 End-to-end fixtures

At least one realistic fixture runs:

```text
G2 Go -> Handoff v2 -> Project Design -> Design Baseline
      -> Change propose -> apply -> verify -> archive
      -> current specs + feature/roadmap/trace reconciliation
```

A second path injects an in-boundary Design Gap; a third injects a G2-boundary change. Tests assert
the first creates a successor Design Baseline and the second routes to backtracking without corrupting
Build state.

## 13. Delivery Decomposition

This architecture is implemented as a sequence of separately reviewable plans:

1. **Contract and scope foundation**: update methodology scope and routing; define Handoff v2,
   realization schemas, IDs, links, statuses, and storage contract.
2. **Global Design**: implement Handoff enrichment, `bw-design`, `bw-project-design`, Design CLI,
   planning views, current spec seed, and Design Baseline.
3. **Change core**: adapt the four OpenSpec core skills and implement Change CLI, validation, delta
   parsing, apply context, verify contract, and atomic archive.
4. **Reconciliation and Build routing**: implement requirements/feature graph operations,
   `bw-build`, suspect links, completion roll-ups, generated views, and Design Gap routing.
5. **Hardening**: deployment, migrations, end-to-end fixtures, evals, documentation, and removal of
   any temporary upstream CLI test dependency.

Each implementation plan must pass its own approval gate. No plan may weaken the contracts in this
spec merely to reduce the first delivery slice.

## 14. Acceptance Criteria

This design is realized when:

1. A formal G2 Go can initialize a portable global Design without GSD or OpenSpec installed.
2. The human can trace every planned Feature and normative Requirement to its Solution and baseline.
3. `bw-project-design` creates a reviewable global plan and an approved immutable Design Baseline.
4. `bw-build` can route a Feature through propose, apply, verify, and archive using BeWater-native
   OpenSpec-derived skills.
5. Archiving updates current specs and all planning views atomically.
6. Feature completion requires verified scenarios and archived Changes, not only completed tasks.
7. An in-boundary design discovery creates a governed Design revision and successor baseline.
8. A discovery that changes G2-fixed intent or scope routes to `bw-backtrack`.
9. Typed traceability and suspect-link impact analysis work across Design and Build.
10. New deterministic runtime code meets the 80% coverage floor and all end-to-end fixtures pass.
