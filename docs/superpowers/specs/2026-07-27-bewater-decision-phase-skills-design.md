# BeWater Decision-Phase Skill Toolkit — Design Spec

- **Date**: 2026-07-27
- **Revised**: 2026-07-29
- **Status**: v5.1 (final)
- **Authority**: bewater-methodology/bewater-core.md v1.3 (read-only)
- **Supersedes**: this document's v3
- **Superseded implementation plan**: docs/superpowers/plans/2026-07-28-bw-runtime-phase1.md — retained only as a legacy behavioral oracle; do not execute it

> **v5.1 changelog (2026-07-29, design finalization):** G1 — the `bwkit` helper ships with skills: source at `src/bwkit/`, deployed by the installer into `_bw-shared/bwkit/` (§2.1, §9, §12.2, §12.5). G2 — condition edits bump in-place `record_revision` under a stable ID (§5.6). G3 — `supersedes_ref` self-revision vs cross-entity replacement semantics disambiguated (§5.1). G4 — baselines and gate decisions clarified as cross-file versioned + in-file immutable (§5.1). G5 — Phase 0 authoritative schemas live under `_bw-shared/` (§10.2). G6 — `scripts/verify` is Python under the 80% floor (§11.3). H1 — bwkit is refactored to a standard-library-only, text-level revision CAS: it never parses YAML; the caller parses/mutates/serializes/bumps and bwkit enforces the CAS + backup + atomic write (§12.5).

## 0. Decision Summary

The product remains a Claude Code skill toolkit. The MVP does **not** ship a general-purpose bewater runtime, CLI, package, or plugin.

v4 keeps that simplification but restores the governance semantics that make bewater distinct:

- a human owns convergence and resource decisions, while methodology evidence requirements remain binding;
- G1/G2 are explicit state transitions with five exits and recoverable actions;
- a G2 Go creates an immutable validated baseline and an execution handoff;
- assumptions, artifacts, gate decisions, experiments, branches, and backtracks have stable IDs and traceable lineage;
- skills edit project state directly under a single-writer, revision-checked protocol;
- every installed skill is self-contained, and the installer is fail-closed and behaviorally tested.

The existing src/bw and tests implementation is a **legacy prototype and behavioral oracle**, not a shipped dependency. It is also the implementation source for the narrow helpers introduced in §12. It remains in the working tree until the skill-only G1/G2 loop passes acceptance. Deletion, if still desirable, requires separate user approval and a separate change.

---

## 1. Goal and Scope

### 1.1 Goal

Turn bewater's decision phase into an interactive, auditable flow:

    Immersion → Discover → Define → G1 → Ideate → Shape → G2 → execution handoff

The toolkit helps a team manage uncertainty through:

- dual-sided Money + Magic reasoning;
- an assumption ledger and evidence levels;
- Achilles Heel prioritization;
- human convergence;
- event-driven gates with deadline fallback;
- branching, experiments, baselines, and governed backtracking.

### 1.2 In scope

- 19 Claude Code project skills under .claude/skills/bw-*/SKILL.md, self-contained by default (§3.10);
- skill-local references under each .claude/skills/bw-*/references/ directory, plus shared references under .claude/skills/_bw-shared/ when extracted (§2.3);
- narrow runtime helpers under _bewater/ as required by §12, with no authority over gate outcomes;
- a Bash installer for personal Claude Code skills;
- per-product-project control state under _bewater/;
- human-readable deliverables under _bewater-output/;
- behavioral evals for every skill;
- installer and state-transition verification.

### 1.3 Out of scope

- execution-phase skills after the G2 handoff;
- a general state engine or bw CLI;
- machine-selected gate exits;
- automatic scoring as a substitute for accountable human judgment;
- multi-host skill packaging;
- a Claude plugin manifest;
- deletion of the legacy runtime in the same change.

### 1.4 Product boundary

The host AI executes the workflow; the accountable human makes non-delegable choices. Skills must not silently weaken methodology rules to satisfy a requested outcome. Direct edits outside the skills cannot be made perfectly safe without a runtime; the toolkit detects and surfaces inconsistencies rather than claiming a machine guarantee it does not provide.

---

## 2. Architecture

### 2.1 Tool repository

    bewater-new/
    ├── bewater-methodology/
    │   └── bewater-core.md
    ├── src/
    │   ├── bw/                          # legacy oracle + helper source (§0, §12)
    │   └── bwkit/                       # narrow helper package source (§12.2, §12.5)
    ├── .claude/
    │   └── skills/
    │       ├── bw-*/
    │       │   ├── SKILL.md
    │       │   └── references/
    │       │       └── <only-the-files-this-skill-uses>.md
    │       └── _bw-shared/              # shared references extracted per §2.3
    ├── evals/
    │   └── <skill>/
    │       ├── scenarios/
    │       ├── red/
    │       └── green/
    ├── tests/
    │   └── installer/
    ├── scripts/
    │   └── verify
    ├── install.sh
    └── docs/

There is no catalog.yaml in the MVP. The catalog in §4 is the authoring taxonomy; no runtime consumer needs a second manifest. The .claude/skills location makes every source skill directly invocable while experimenting in the tool repository.

### 2.2 Product project

    <product-project>/
    ├── _bewater/
    │   ├── config.yaml
    │   ├── ledger.yaml
    │   ├── conditions.yaml
    │   ├── .backup-ledger-r11.yaml
    │   └── records/
    │       ├── D-001-gate.md
    │       ├── B-001-baseline.yaml
    │       └── BT-001-backtrack.md
    └── _bewater-output/
        ├── ART-001-r1-project-charter.md
        ├── ART-002-r3-solution.md
        ├── EXP-001-r2-experiment.md
        ├── E-001-r1-evidence.md
        └── execution-handoff.md

The product project has only two top-level bewater directories and one shallow records directory. Artifact, experiment, evidence, and handoff files are flat; branch, kind, and lineage live in frontmatter rather than directory nesting. Control state is canonical under _bewater. Gate reports may be rendered for humans, but _bewater-output is never a second source of gate truth.

### 2.3 Installed skill

Each source and installed skill directory contains everything it references:

    <skills-destination>/bw-start/
    ├── SKILL.md
    ├── references/
    │   ├── templates.md
    │   ├── gate-criteria.md
    │   ├── ledger-schema.md
    │   └── workshop.md
    └── .bewater-managed

A skill may contain only the reference files it actually uses; every directly referenced file normally lives inside that skill directory. This keeps source skills directly runnable and installed skills portable.

**Shared references are deliberate, not forbidden.** When a reference is copied across three or more skills, or when its drift risk is high (for example ledger-schema, gate-criteria, or the bewater glossary), it is extracted to .claude/skills/_bw-shared/ with a stable contract_id and contract_version. The installer deploys a shared reference together with every skill that depends on it. Inside a single skill, reference copies stay byte-identical; across skills a shared copy need only match by contract_id and contract_version. Validation rejects parent-relative escapes and drift between contract copies.

Every standard reference declares contract_id, contract_version, and source_sections. A skill may cite bewater-core.md as authority text, but the operational schemas and the bewater glossary it depends on must be available inside the skill or its declared shared references; invoking a skill must not require ad-hoc reading outside those locations.

---

## 3. Design Principles

1. **Skills are the product; runtime is minimized, not forbidden.** The MVP ships markdown skills plus an installer, not a general methodology runtime. A narrow helper is added only when an operation meets the no-runtime tests in §12.
2. **Human convergence does not redefine evidence.** Humans choose strategy, concepts, Kill/Proceed, and gate exits. They cannot convert incomplete G2 evidence into a methodology-compliant Go.
3. **Gates present and record decisions; they never make them.** A gate skill assembles evidence, resolves authority, presents permitted exits, stops for the accountable human, and then applies the selected action.
4. **Document presence is not validation.** A non-empty final document proves only that a document exists. Kind-specific readiness, evidence, current revision signoff, and gate criteria determine readiness.
5. **Atomic capabilities; thin routers.** Capability skills do work. Stage skills only orient, resume, report stage status, and route “what next?” requests.
6. **Stable identity and explicit lineage.** IDs survive file renames. Forward derived_from references are canonical; reverse impact is derived by scanning rather than hand-maintaining affects.
7. **State changes are reviewable and recoverable.** Every write checks revision, preserves unknown fields, shows a diff, and makes multi-file gate actions resumable.
8. **Baselines govern loop size.** Any change touching a gate-confirmed baseline is a large loop and must return to the original gate.
9. **The methodology is authoritative.** Skills cite the relevant bewater-core.md sections and their skill-local references rather than inventing weaker local rules.
10. **Skills are self-contained and MECE by default; shared resources are deliberate.** Each skill carries its own references, and skill responsibilities are mutually exclusive and collectively exhaustive. A reference copied across three or more skills, or one whose drift risk is high, is extracted to .claude/skills/_bw-shared/ with a stable contract_id (§2.3) rather than duplicated blindly.

---

## 4. Skill Catalog and Routing

All SKILL.md files use Claude-native frontmatter with name and description only. Descriptions state triggers, not workflow summaries.

| Layer | Skill | Trigger contract |
|---|---|---|
| entry | bw-start | Use when the user wants to start a bewater decision-phase project, resume without a known stage, or reconcile ambiguous or pending project state. |
| router | bw-immersion | Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Immersion. |
| router | bw-discover | Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Discover. |
| router | bw-define | Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Define. |
| router | bw-ideate | Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Ideate. |
| router | bw-shape | Use when the user explicitly asks to navigate, resume, check status, or choose the next action in bewater Shape. |
| gate | bw-strategy-gate | Use when the user asks for G1 readiness or a strategy-gate decision after Define. |
| gate | bw-concept-gate | Use when the user asks for G2 readiness or a concept-gate investment decision after Shape. |
| capability | bw-project-charter | Use when the user wants to draft or revise a bewater project charter or seed root assumptions. |
| capability | bw-4c-research | Use when the user wants to plan, run, or synthesize bewater 4C research or a learning plan. |
| capability | bw-insight-craft | Use when the user wants to turn research into insights or judge insight candidates against F/P/E/T. |
| capability | bw-directional-hypothesis | Use when the user wants to compose or refine By / We can / Resulting in hypotheses. |
| capability | bw-strategy-statement | Use when the user wants to create, select, revise, or lock a choice-cutting innovation strategy. |
| capability | bw-opportunity-area | Use when the user wants to define or revise 2–4 non-overlapping bewater opportunity areas. |
| capability | bw-concept-card | Use when the user wants to generate, complete, evaluate, or converge bewater concept cards. |
| capability | bw-assumption-map | Use when the user wants to map or revise assumptions, risk ordering, or Achilles Heel obligations. |
| capability | bw-experiment | Use when the user wants to design a bewater experiment or record its result and Kill/Proceed decision. |
| capability | bw-investment-narrative | Use when the user wants to draft or revise the six-part narrative or evidence-linked financial case. |
| capability | bw-solution-shape | Use when the user wants to shape or revise selected concepts into validated dual-sided solutions. |

**Layer responsibilities.** Capability skills produce iterable artifacts (charters, insights, strategies, concepts, experiments, solutions). Router skills only orient, resume, report status, and route "what next?" — they never produce artifacts. Gate skills are constrained adjudicators: they perform real state work (writing immutable decisions, baselines, handoffs, backtracks) but only as the gate contract (§6) permits, and they never choose an exit or emit a free-form artifact.

Routing precedence:

1. A direct, specific work request triggers the matching capability or gate.
2. A new project, global/cross-stage status, unspecified “resume”, pending recoverable action, or ambiguous branch triggers bw-start.
3. A request that explicitly names one stage and resolves to one branch triggers that stage's router.
4. A router must not perform a capability workflow inline; it presents the relevant capability choices and stops for selection when the next action is ambiguous.
5. If several branches are active and the request does not identify one, bw-start asks the human to choose before writing state.
6. bw-start and every router scan open conditions and active-baseline validity before recommending downstream work.

Every convergent capability ends by presenting candidates, naming the required human decision and decision authority, and stopping. The AI may recommend with reasons but may not record a human choice before receiving it.

---

## 5. State Contract

The detailed field definitions and examples live in each consuming skill's own {skill-dir}/references/ledger-schema.md. This section defines the behavior that skills and evals must preserve.

**Schema versioning.** Every revisioned file carries schema_version. A skill or helper declares the schema_version it supports and fails closed on a higher version rather than guessing its layout. A schema bump migrates canonical mutable files (config, ledger, conditions) under the §5.7 protocol; when a record layout changes, it writes new revisions instead of rewriting history, and superseded files keep their original schema_version for audit. Migrations are versioned, tested scripts run once per file, recording from/to versions in change_history.

### 5.1 IDs and typed references

IDs are stable and never reused:

- branches: BR-001;
- assumptions: A-001;
- artifacts: ART-001;
- experiments: EXP-001;
- decisions: D-001;
- baselines: B-001;
- backtracks: BT-001;
- actions: ACT-001;
- conditions: C-001;
- evidence items: E-001.

Canonical references are typed:

- artifact:ART-001@3;
- assumption:A-001@4;
- experiment:EXP-001@2;
- gate:D-001;
- baseline:B-001;
- evidence:E-001@1.

Mutable artifacts, assumptions, experiments, and evidence references include a record revision. Gate references identify the immutable decision core; baseline references identify immutable snapshot files. Reverse dependencies are computed from derived_from; the schema has no manually maintained affects field.

**Next-ID ownership.** Each entity's next identifier lives with its canonical file: assumptions in ledger.yaml (§5.3), conditions in conditions.yaml (§5.6), and branch, artifact, experiment, decision, baseline, backtrack, action, and evidence in config.next_ids (§5.2). A writer allocates an ID only from that entity's canonical source while holding the §5.7 lock.

**supersedes_ref.** `supersedes_ref` is the single field name for "the typed reference this record replaces," used on every versioned record — assumption, artifact, evidence, decision, and baseline — and its value is a typed reference such as `artifact:ART-001@2` or `gate:D-001`. The field carries two distinct semantics, disambiguated by comparing the record's own ID/type against the referenced ID/type: (a) **self-revision** — a new revision of the same entity points at its immediate predecessor (`artifact:ART-001@3` supersedes `artifact:ART-001@2`; an assumption bumps `record_revision` and points at its prior snapshot); (b) **cross-entity replacement** — a new entity records that it replaces a different entity's revision (a branch-local `assumption:A-002` whose `supersedes_ref` is `assumption:A-001@4`, per §8.1). Versioning models differ by entity: assumptions, conditions, and the config/ledger/conditions envelopes revise in place by bumping a revision field inside one file; artifacts and evidence are append-only, writing a new file per revision; baselines and gate decisions are cross-file versioned and in-file immutable, where a successor (`B-002`, a new attempt's `D-002`) supersedes the prior file rather than bumping a revision inside it (§6.5, §6.6). The action_plan subfield `supersedes_handoff_ref` is the one named exception: it points to the gate decision whose execution handoff a Go action replaces, since a handoff has no ID of its own.

### 5.2 Config

_bewater/config.yaml contains project-level settings and branch navigation:

    schema_version: 1
    revision: 4
    updated_at: 2026-07-28T12:00:00Z
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
      name: Example
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

Branch status is active, merged, killed, pivoted, or deviated. There is no single global current_stage; the displayed project stage is derived from the active branch or branches.

A gate cannot record a decision when its single accountable person is missing or ambiguous. The skill may still render a readiness report.

### 5.3 Assumption ledger

_bewater/ledger.yaml has a revisioned envelope:

    schema_version: 1
    revision: 12
    next_id: 18
    updated_at: 2026-07-28T12:00:00Z
    updated_by: bw-assumption-map
    assumptions:
      A-001:
        record_revision: 1
        statement: Example assumption
        branch_id: BR-001
        layer: concept
        category: consumer
        side: magic
        impact: high
        uncertainty: high
        evidence_level: L2
        validation_status: testing
        status: active
        evidence_refs: []
        derived_from: []
        supersedes_ref: null
        risk_history: []
        l4_obligation_status: open
        history: []

Required semantics:

- layer is root, strategy, opportunity, concept, or feature;
- category is consumer, commercial, technical, distribution, or regulatory;
- side is money, magic, or both;
- validation_status is untested, testing, supported, falsified, or inconclusive;
- status is active, killed, or merged;
- evidence level is L1–L6 and must point to evidence, not merely be asserted;
- core assumption portfolios must cover both Money and Magic;
- is_achilles_heel is derived from current impact=high and uncertainty=high.

An Achilles Heel creates a durable L4 obligation. Once an assumption has been high-impact and high-uncertainty, lowering either field does not erase that obligation. l4_obligation_status remains open until either:

- the assumption has a validation conclusion backed by L4+ evidence, making it satisfied; or
- evidence-backed reclassification or falsification is explicitly signed off by a human, making it not-required.

risk_history records the prior classification, evidence reference, human signoff, and timestamp. Gate reports show both current Achilles Heels and all open historical L4 obligations.

Every assumption update increments record_revision and stores the complete prior record in history. A versioned assumption reference resolves either the current record or that immutable historical snapshot; skills never rewrite or prune referenced history.

### 5.4 Artifact contract

Every artifact has YAML frontmatter:

    schema_version: 1
    artifact_id: ART-001
    revision: 3
    supersedes_ref: artifact:ART-001@2
    kind: solution
    stage: shape
    branch_id: BR-001
    document_status: final
    validation_status: validated
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
    derived_from: []
    signoffs: []
    stale_reason: null

document_status is draft, final, or superseded. validation_status is unvalidated, in-review, validated, or invalidated.

A substantive edit increments revision. Signoffs include person, role, scope, artifact_revision, and signed_at; a signoff for an older revision cannot satisfy a current gate. When an upstream typed reference is revised, falsified, or invalidated, dependent artifacts become stale until reviewed and must state stale_reason.

Artifact files are append-only revisions in the flat output directory: ART-001-r3-solution.md supersedes ART-001-r2-solution.md through supersedes_ref. A substantive edit, stale mark, or invalidation always writes a new revision and never replaces an older file. Versioned artifact and experiment references resolve directly by ID and revision; the current revision is the chain head not superseded by another file.

The resolver requires exactly one file for each type/ID/revision and exactly one head per revision chain. A duplicate revision, missing predecessor, cycle, or two heads is state corruption: skills stop before routing or writing and show the conflicting files.

Kind-specific readiness is defined in each consuming skill's own {skill-dir}/references/gate-criteria.md, including:

- insight: F/P/E/T decisions signed at the current revision;
- directional hypothesis: complete By / We can / Resulting in structure and Money + Magic coverage;
- strategy: human-selected, locked, and passes the “knife, not summary” test;
- opportunity portfolio: 2–4 non-overlapping areas that can each spawn concepts;
- concept portfolio: strategy-filtered, with human healthy-anxiety and altitude decisions;
- solution: validated status, dual-sided solution, business case, and traceable evidence;
- investment narrative: six parts complete, financial assumptions sourced with logic.

final plus a non-empty body is only document-presence evidence. It never implies the readiness conditions above.

**Revision retention and archival.** Append-only revisions are never deleted — they satisfy audit. To keep the flat output directory navigable as a project grows, a project may archive superseded revisions into _bewater-output/archive/ without renaming them or altering supersedes_ref; the resolver searches the output directory and archive/ together. Head resolution may use a derived head-index maintained by the §12 scanner instead of scanning every file. Archival is triggered explicitly by the human through a helper, never automatically during a gate or write.

### 5.5 Evidence contract

Each evidence:E-xxx@n reference resolves to the immutable flat wrapper _bewater-output/{evidence-id}-r{revision}-evidence.md. Its frontmatter contains evidence_id, revision, supersedes_ref, effect_on_prior, validity, correction_reason, source_type, captured_at, content_sha256, source_path_or_user_provided_url, and related assumption or experiment references. A wrapper may point to a large or binary attachment stored beside it.

Corrections create the next immutable revision. validity is active or invalidated; effect_on_prior is supplements, supersedes, or invalidates, and invalidation requires a reason and human acknowledgement. A superseded or invalid evidence revision triggers a scan of every assumption and artifact evidence_refs edge, creation of new stale/invalidated dependent revisions, and Gate/baseline impact analysis. Evidence therefore participates in lineage even though it is not stored in derived_from.

An evidence level is valid only when its evidence_refs resolve and the evidence type supports that level. A user-provided URL is preserved exactly; skills do not invent or repair external URLs.

### 5.6 Condition registry

_bewater/conditions.yaml is the canonical current-state projection for Conditional Go conditions:

    schema_version: 1
    revision: 1
    next_id: 2
    updated_at: 2026-07-28T12:00:00Z
    updated_by: bw-strategy-gate
    conditions:
      C-001:
        record_revision: 1
        origin_decision_id: D-001
        branch_id: BR-001
        statement: ""
        owner: ""
        due_at: null
        status: open
        required_evidence: ""
        evidence_refs: []
        resolution_ref: null
        resolved_at: null
        resolved_by: null
        waiver_rationale: null
        close_reason: null
        close_authority: null

Status is open, satisfied, waived, cancelled, or superseded. A resolution updates this registry under the direct-write protocol, retains the origin decision ID, and bumps the condition's in-place `record_revision` together with the conditions.yaml envelope `revision`. A condition keeps its stable C-NNN ID across every status and field change — satisfied, waived, cancelled, and superseded are state transitions on the same record, never a new condition ID; the registry is append-history within one file, not append-only new files. cancelled and superseded require close_reason and close_authority. A new gate attempt reads the registry rather than inferring condition state from an old transcript. Open lineage conditions remain visible across attempts; waived hard G2 evidence still does not qualify for Go.

### 5.7 Direct-write protocol

Because the MVP has no state runtime, every state-writing skill follows the same protocol:

1. Announce the target files and obtain the human choice required by the capability.
2. Require one active bewater writer/session per project. A narrow helper (§12) acquires `_bewater/.bw-lock` by compare-and-set; if another session holds it, stop and coordinate without writing.
3. Read config, ledger, the condition registry, affected records, and pending gate/backtrack actions immediately before editing.
4. Capture the current revision and create a flat rotating backup named _bewater/.backup-{source}-{revision}-{timestamp}; retain the five most recent verified backups per mutable canonical file.
5. Modify only the intended records; preserve unknown fields and unrelated records.
6. Re-read before replacement. If the revision changed, stop without writing and request a manual merge; when inside an action plan, mark the affected step failed and the action manual-repair.
7. Increment every affected file and record revision, or create a new immutable record. Config, ledger, condition registry, artifacts, evidence wrappers, gate operational state, and backtrack operational state are all revisioned.
8. Show the exact diff and ask for correction when the change includes a human judgment.
9. Re-read the written state and verify IDs, references, schema version, and revision.

This protocol provides conflict detection and recovery discipline, backed by the narrow helpers in §12 for the operations that require deterministic enforcement. It is not a transactional guarantee against arbitrary external edits.

---

## 6. Gate Contract

### 6.1 Trigger and authority

Gates are event-driven when evidence is ready, with a deadline fallback from the active branch's gate_due_at. At the deadline, the gate runs even if evidence is incomplete; incompleteness is displayed as decision evidence and does not become an automatic Go.

- G1 requires one product-owner-level accountable decision maker.
- G2 requires one investment-decision-level accountable decision maker.

If the accountable person is missing, ambiguous, or below the configured authority level, the skill produces a readiness report and stops without a decision record.

### 6.2 Gate flow

1. Resolve branch, subject references, accountable person, trigger, and input revisions.
2. Reconcile pending or manual-repair prior gate and backtrack actions.
3. Evaluate every criterion as pass, fail, or unknown and cite its evidence.
4. Separate structural, hard-evidence, and human-judgment criteria.
5. Display open conditions from the registry, current Achilles Heels, and historical L4 obligations.
6. Present only methodology-permitted exits and the exact action for each.
7. Stop for the accountable human.
8. Preallocate every ID and write the complete decision plus action plan with action_status: pending before changing any other state.
9. Apply each ordered action step idempotently, recording applied, skipped, or failed after every attempted write.
10. Verify resulting state, show the diff, then mark action_status: applied; conflicts enter manual-repair rather than remaining silently pending.

The gate skill never chooses an exit.

### 6.3 Readiness

G1 criteria mirror bewater-core.md §6.1:

- insights have current-revision human F/P/E/T signoff;
- 2–5 directional hypotheses are closed and dual-sided;
- the strategy statement is selected, locked, and choice-cutting;
- 2–4 opportunity areas are non-overlapping and generative;
- the assumption ledger has an initial inventory and identifies the Achilles Heel quadrant;
- the Money + Magic initial judgment is explicitly made.

G1 intentionally tolerates high uncertainty. It requires a coherent direction and visible risks, not L4 validation.

G2 criteria mirror bewater-core.md §5.2.2, §6.1, and §7.2:

- the subject contains 1–2 solutions at validated status;
- every current Achilles Heel and open historical L4 obligation has a conclusion supported by L4+ behavioral evidence;
- self-reported intent alone cannot satisfy the L4 requirement;
- every financial assumption cites its source and reasoning;
- the six-part investment narrative is complete and dual-sided;
- the accountable human resolves the “make it impossible not to invest” judgment;
- the exact input revisions are ready to become a validated baseline.

All required G2 criteria must pass for Go. Human judgment resolves qualitative criteria; it does not relabel L1–L3 evidence as L4 or waive a missing required artifact.

### 6.4 Five exits and actions

| Exit | Availability | State action |
|---|---|---|
| Go | Every required criterion passes and authority is resolved. For G2, the project handoff slot is empty or the decision explicitly supersedes the active handoff. | Create an immutable gate baseline. G1 advances the branch to Ideate. G2 advances it to handoff-ready and writes the execution handoff. |
| Conditional Go | A bounded, remediable gap has explicit conditions; never used to treat a failed G2 hard-evidence criterion as validated. | Mark the current gate conditional. G1 advances to Ideate. G2 enters a constrained closeout-directed state under an explicit allowed_work and resource_envelope — only the design/validation work needed to close the conditions, not full execution. Do not create a validated baseline or a real execution handoff (only a provisional one). Unrestricted resource release and the next gate stay blocked until mandatory closeout converts it to a new Go. |
| Recycle | More work is needed without changing the governing direction. | Create a backtrack record, set the branch to the named earlier stage, and retain all evidence. |
| Pivot | The direction or solution premise must materially change. | Check active baselines first, then create a successor branch. Route feature/concept change to Ideate or Shape local reframe when no baseline is touched; opportunity/strategy change to Define plus G1; root change to Discover plus G1. Invalidate only the dependent downstream decisions. |
| Kill | The branch should receive no further resources. | Invalidate prior active gate decisions, clear active baseline pointers, archive/remove this branch's active handoff projection, close branch conditions with authority and reason, then mark the branch killed last. Preserve all artifacts, assumptions, experiments, and evidence. |

Conditional Go creates condition-registry entries before applying any allowed work. Every router and gate reads the current registry projection. Once all conditions close, the branch enters mandatory current-gate closeout: the gate skill re-evaluates every criterion against current revisions, stops for the same authority level, and records a new Go decision that supersedes the Conditional Go. That Go creates the required baseline and, for G2, the full execution handoff. Until closeout is applied, the next gate remains ineligible. A waiver records authority and rationale but cannot waive a G2 L4 obligation into a Go.

### 6.5 Decision record

The canonical record path is:

    _bewater/records/<decision-id>-gate.md

It contains:

    schema_version
    revision
    decision_id
    attempt
    gate
    branch_id
    subject_refs[]
    decision_maker{person, role, authority_level}
    trigger{kind, due_at}
    input_revisions{ledger, artifacts[]}
    checklist_results[]
    exit
    condition_ids[]
    action_plan:
      action_id
      expected_revisions
      target_stage
      allowed_work[]
      resource_envelope
      successor_branch_id
      baseline_id
      supersedes_handoff_ref
      ordered_steps[]{step_id, operation, target_ref, status}
      action_status: pending | applied | aborted | manual-repair
      conflict_refs[]
      resolution{mode, authority, rationale, followup_action_id}
    supersedes_ref
    decided_at
    validity: active | superseded | invalidated
    methodology_deviation
    change_history[]

subject_refs is a list because G2 may assess 1–2 solutions. New attempts create new records and supersede older attempts; records are never overwritten by date. The decision core through exit is immutable after the accountable human decides. Only revisioned operational fields—action step status, action_status, validity, and change_history—may change.

Step status is pending, applied, skipped, or failed. The action plan fixes all IDs and expected input revisions before its first external write. If applying the action is interrupted, bw-start compares intended and actual state and asks the human to resume or resolve the remaining steps. An already-applied step is verified and skipped; recovery must not allocate replacement IDs or duplicate baselines, branches, conditions, or handoff projections.

When safe roll-forward is impossible, the accountable human selects compensation, invalidation, or manual repair. The record captures conflict refs, authority, rationale, and any follow-up action. aborted is terminal and invalidates the unapplied decision; manual-repair is non-terminal but blocks further state-changing skills until explicitly resolved.

**Resolving manual-repair.** Resolution is never automatic. The accountable human reconciles actual state with the intended plan; a re-run of the §12 integrity check (or bw-start's reconciliation) then verifies every ordered step as applied or intentionally skipped. On success the action moves to applied; if the human abandons it, it moves to aborted. Either transition is recorded in change_history with authority, rationale, and the evidence used, and only then do state-changing skills unblock.

### 6.6 Baselines and G2 execution handoff

Every Go creates _bewater/records/<baseline-id>-baseline.yaml. The file is immutable by protocol and includes:

- baseline ID, gate, decision ID, branch ID, creation time, and a supersedes_ref to the prior baseline;
- exact gate input references and revisions;
- dependency on any upstream active baseline;
- the gate checklist result.

A G1 baseline freezes the signed insights, locked strategy, opportunity portfolio, initial assumption portfolio, and Money + Magic judgment.

A G2 baseline additionally includes:

- exact solution and investment narrative artifact references and revisions;
- a frozen snapshot of in-scope assumptions, validation conclusions, evidence levels, and evidence references;
- open assumptions that remain observations rather than gate blockers;
- the strategy and opportunity lineage.

A baseline file is never edited. The branch's active_baselines pointer defines the current baseline for each gate. Revalidation creates a new decision and baseline, records supersedes_ref, and atomically switches that pointer through the gate action plan; older files remain auditable.

The same G2 Go writes:

    _bewater-output/execution-handoff.md

The handoff contains:

- branch ID, status, source G2 decision, and baseline reference;
- every validated solution in the G2 subject_refs list;
- the investment narrative and financial case;
- open assumptions to monitor during execution;
- the immutable baseline reference;
- the G2 decision and exact source revisions.

The MVP permits parallel discovery and concept branches but only one active execution handoff per project. config.active_execution_handoff points directly to the source gate:D-xxx decision, whose record identifies the branch; no separate handoff ID or manifest exists. Before replacing the current handoff, a G2 decision must explicitly name the gate decision it supersedes, and the skill moves that file to _bewater-output/execution-handoff-{prior-decision-id}-archived.md.

The handoff is derived output and can be regenerated from canonical state. A G2 Conditional Go may create _bewater-output/provisional-handoff-{decision-id}.md containing its condition IDs and resource envelope, but it has no baseline reference, never occupies active_execution_handoff, and must not be presented as validated. If a normal execution handoff's G2 decision or baseline is invalidated, the backtrack action archives it as invalidated, removes the current execution-handoff.md projection, and clears the config pointer before any further routing.

### 6.7 Requested methodology deviation

If a human insists on “Go” while a required hard criterion fails:

- the skill explains the failed criterion and offers Conditional Go, Recycle, Pivot, or Kill;
- it does not record exit: go, create a validated baseline, or produce the G2 execution handoff;
- if the human proceeds outside the method, the decision record captures methodology_deviation with requested action, rationale, acknowledgement, and time;
- the branch becomes deviated, and the bewater workflow makes no claim that G2 passed.

This preserves human authority over organizational action without falsifying methodology evidence.

---

## 7. Experiment Lifecycle

bw-experiment has two explicit modes.

### 7.1 Design

The skill creates or revises the flat, append-only artifact _bewater-output/{experiment-id}-r{revision}-experiment.md, linked to one or more assumptions. Before execution, the accountable human approves:

- target assumption references;
- method and target evidence level;
- metric and baseline;
- Proceed threshold;
- Kill threshold;
- treatment of inconclusive results;
- owner, timebox, and evidence capture path.

Kill/Proceed criteria are fixed before observing results. An experiment intended to close an Achilles Heel must target L4+ behavioral evidence.

### 7.2 Record result

The skill records:

- observed result and metric values;
- raw evidence references;
- achieved evidence level and why;
- conclusion: supported, falsified, or inconclusive;
- proposed ledger changes;
- the human decision: proceed, kill, or retest;
- artifact and ledger revisions changed by the result.

The human makes the Kill/Proceed decision. The skill updates the assumption only after that decision and shows the diff. A falsified assumption initiates the backtrack analysis in §8; it cannot be treated as a local note with no lineage impact.

---

## 8. Branching, Lineage, and Backtracking

### 8.1 Branches

All assumptions, artifacts, experiments, gate decisions, baselines, and backtracks carry branch_id.

- A fork creates a new stable branch ID and parent_ids.
- A merge retains all parent IDs and marks source branches merged with merged_into.
- A kill or pivot never deletes evidence.
- When more than one branch is active, state-changing skills require an explicit active branch.
- Gate subjects can include artifacts from a merged lineage only when that lineage is explicit.

At fork or pivot time, the human confirms a pinned inherited_assumption_refs set. A branch's effective assumption portfolio is deterministic:

1. start with those inherited assumption revisions;
2. remove only refs listed in excluded_assumption_refs;
3. replace an inherited ref when a branch-local assumption explicitly names it in supersedes_ref;
4. add the latest active branch-local assumption revisions.

An exclusion requires rationale, evidence, and human signoff. It cannot erase an open L4 obligation without the resolution required by §5.3. Later changes to a parent and the parent's killed or pivoted status do not silently change the child's pinned portfolio.

A later revision of the same inherited assumption identity that falsifies or materially reclassifies it creates a needs_rebase_refs blocker on every descendant using an older revision. The pinned snapshot remains reproducible, but no gate may proceed until the child accepts the new revision or records an evidence-backed, human-signed superseding assumption or exclusion.

Effective obligations consist of branch-owned open conditions plus inherited_condition_ids. A normal fork carries applicable open conditions and unaffected active baseline pointers. Invalidating a carried baseline marks every branch pointing to it needs-rebase and clears those pointers through the same recoverable action. A pivot action explicitly carries or closes each condition and clears every baseline affected by its route. A merge unions open conditions, resolves conflicts, and clears baseline pointers by default; retaining a common baseline requires an explicit accountable decision that both parent inputs are identical.

A merge must resolve conflicting assumption revisions, exclusions, evidence conclusions, needs-rebase blockers, and open L4 obligations before creating the merged branch view. Gates evaluate the resulting effective portfolio and obligations, not every ancestor indiscriminately and not only branch-local rows.

### 8.2 Lineage

Canonical dependency edges are derived_from and evidence_refs; both pin mutable upstream record revisions. Branch inheritance and baseline membership are additional governance edges. Skills compute downstream impact by scanning all four rather than relying on a manually maintained reverse affects list.

When an upstream assumption is falsified or an artifact revision changes, the skill:

1. finds all transitive dependents;
2. appends new invalidated or stale revisions for affected artifacts;
3. lists affected gate decisions and baselines;
4. proposes the required backtrack depth;
5. stops for the accountable human to confirm the route.

### 8.3 Backtrack decision

Before using the assumption layer heuristic, the skill checks the branch's active_baselines pointers.

- If the change touches a baseline item, it is a large loop and the original gate must be rerun.
- If no baseline is touched, feature/concept failures may remain a local reframe.
- Opportunity/strategy failures route to Define and require G1 recertification.
- Root-premise failures route to Discover and require G1 recertification.

The canonical backtrack record contains:

    schema_version
    revision
    backtrack_id
    branch_id
    trigger_ref
    affected_refs[]
    baseline_refs[]
    loop_type: small | large
    target_stage
    gates_to_rerun[]
    decision_maker
    decided_at
    status: planned | active | resolved
    action_plan:
      action_id
      expected_revisions
      ordered_steps[]{step_id, operation, target_ref, status}
      action_status: pending | applied | aborted | manual-repair
      conflict_refs[]
      resolution{mode, authority, rationale, followup_action_id}
    change_history[]

The complete action plan is written before any affected state changes. A large-loop plan orders invalidation of gate decisions, clearing affected active-baseline pointers, archiving any active execution handoff, appending stale artifact revisions, and changing branch stage before scheduling gate reruns. bw-start reconciles pending or manual-repair backtracks with the same idempotent recovery rules as gate actions. status becomes resolved only after every required ordered step verifies as applied or intentionally skipped.

Skills recommend the route with evidence; the accountable human confirms it. A branch cannot silently edit a confirmed baseline and continue as a small loop.

---

## 9. Installer Contract

install.sh is shipped code and follows these behaviors:

- project-local experiments discover .claude/skills/bw-* from the repository and invoke them by skill name; no install step is required;
- global installation reads only the self-contained directories under .claude/skills/;
- default release mode is --copy;
- --link is available for repository development;
- --dest overrides the default destination for tests and nonstandard setups;
- the default destination is $HOME/.claude/skills;
- each already self-contained source skill is copied or linked as one unit;
- shared references (§2.3) and the shared `bwkit/` helper package (§12.2) are deployed into `<dest>/_bw-shared/` together with every skill that depends on them, each tracked by contract_id/version (references) or package version (bwkit), under the same managed-marker and idempotent-update rules;
- every target contains a managed marker identifying bewater and its source version;
- repeated installs update only managed targets and are idempotent;
- an unrelated existing file, directory, or symlink causes a fail-closed error;
- a broken managed link can be repaired;
- updates stage content before replacing a managed target;
- --uninstall removes only targets with a valid bewater managed marker.

In --link mode, the target directory contains managed links for SKILL.md, each reference, and the bwkit package rather than relying on source-relative paths. In --copy mode, the installed skill and its deployed bwkit remain usable after the source repository moves or is deleted.

The installer must not touch a real user skill directory during tests.

---

## 10. Authoring and Phasing

### 10.1 Skill authoring

Skills are authored as Claude Code skills using superpowers:writing-skills:

- write a failing behavioral scenario first;
- implement the minimum skill content that changes the observed behavior;
- rerun the same scenario;
- close loopholes found under pressure;
- refactor without weakening the scenario;
- validate and commit one skill before starting the next.

No agents/openai.yaml or plugin-specific metadata is added. Skill-local references hold schemas and reusable criteria; each SKILL.md stays focused on triggers and behavior.

### 10.2 Phase 0 — transition safety

- add an in-file SUPERSEDED banner to the old runtime plan so it visibly matches the authority declaration at the top of this spec;
- treat src/bw and its tests as a non-shipped oracle for state and gate cases;
- do not delete legacy files;
- create the authoritative reference schemas under .claude/skills/_bw-shared/ — ledger-schema, gate-criteria, and the bewater glossary, i.e. the high-drift shared references of §2.3 — so Phase 1 skills cite or copy them per contract; also create the eval harness and the installer test harness.

### 10.3 Phase 1 — G1 closed loop

Build and verify:

- bw-start;
- bw-immersion, bw-discover, bw-define;
- bw-project-charter, bw-4c-research, bw-insight-craft;
- bw-directional-hypothesis, bw-strategy-statement, bw-opportunity-area;
- bw-assumption-map;
- bw-strategy-gate;
- skill-local references and installer.

Acceptance: a fresh project can reach every G1 exit, resume after interruption, preserve branch/ledger integrity, and never record Go when G1 required evidence or authority is unresolved.

### 10.4 Phase 2 — G2 closed loop

Build and verify:

- bw-ideate, bw-shape;
- bw-concept-card, bw-experiment;
- bw-investment-narrative, bw-solution-shape;
- bw-concept-gate;
- baseline, handoff, and backtrack flows.

Acceptance: a project can reach every G2 exit; G2 Go requires all hard evidence, creates one immutable baseline and one traceable handoff, and a later falsification routes through the correct baseline-aware loop.

### 10.5 Phase 3 — legacy disposition

Only after Phase 2 acceptance:

1. compare skill-only behavior with the legacy oracle;
2. document any intentionally accepted loss of guarantee;
3. request explicit user approval for legacy deletion;
4. perform cleanup in a separate commit.

**Oracle mapping.** The comparison is structured by module, since src/bw is also the helper source (§12.3) and the eval judge (§11.1):

| src/bw module | New-design role | Compare on |
|---|---|---|
| paths.py | path conventions (§2.2) | _bewater / _bewater-output layout |
| init.py | project bootstrap | _bewater skeleton, default config/ledger |
| io.py | direct-write protocol + helper (§5.7, §12) | backup, reread, revision increment |
| hashing.py | CAS + lock helper (§12) | content hash, compare-and-set |
| ledger_ops.py | action-plan applier (§12) | ID allocation, atomic action steps |
| gate_scan.py | lineage/impact scanner (§12) | transitive closure, stale marking |
| validate.py | integrity check (§12) | duplicate head, cycle, schema/ref drift |
| schema.py | skill-local ledger-schema.md | field set, enums, required semantics |
| cli.py | not shipped; oracle driver only | scenario orchestration |
| errors.py | failure modes | corruption/conflict classification |

Any divergence is recorded as an intentionally accepted loss of guarantee before deletion is requested.

**Known drift (2026-07-29).** The mapping above is largely aspirational: `src/bw` targets the pre-v5 layout (`_bewater/state/assumption-ledger.yaml`, list-shaped assumptions, no `revision` / config / conditions). Only `hashing.content_hash` is safely reusable; `io` / `schema` / `ledger_ops` / `gate_scan` / `validate` bind the old schema and are bypassed by bwkit (§12.5). The oracle comparison therefore checks behavioral shape, not byte-level schema parity.

---

## 11. Verification and Acceptance

### 11.1 Behavioral TDD

Each skill has at least three pressure scenarios. Behavior-shaping rules, especially human convergence and hard gate evidence, are repeated at least five times with varied wording.

For each skill:

1. define scenario inputs, required behaviors, forbidden behaviors, and assertion ownership;
2. run RED in a fresh context, isolated temporary HOME, and repository-external temporary product cwd where the target skill is absent from both project and global skill locations;
3. preserve the failing control result under evals/{skill}/red/;
4. copy only the target skill into the temporary product's .claude/skills as the experimental variable while keeping cwd, model, prompt, dependency skills, global skills, and fixtures fixed;
5. run GREEN in a new fresh context and store it under evals/{skill}/green/;
6. add adjacent positive and negative routing cases;
7. refactor and rerun before moving to the next skill.

Each scenario manifest records scenario_id, target_skill, prompt, fixture refs, installed dependency skills, required assertions, forbidden behaviors, and repetition count. Each run result records mode, fresh-context ID, cwd, temporary HOME, project-local skill set, global skill set, model/version/config, transcript ref, per-assertion result, verdict, and reviewer when semantic judgment is manual.

A RED control must fail at least one target behavior or the scenario is invalid. GREEN must pass every required assertion and trigger no forbidden behavior. Safety-critical gate scenarios must pass 5/5 fresh-context repetitions. All deterministic installer and verification-script tests must pass.

**Eval cost control.** Coverage is tiered so cost tracks risk. Deterministic behaviors — ID allocation, revision conflict, backup/reread, versioned-ref and contract checks — are asserted by automated tests and the §12 helpers, not by fresh-context LLM runs. Behavioral scenarios (routing, convergence, gate-evidence judgment) use fresh-context LLM eval; only safety-critical gate scenarios require 5/5 repetitions, the rest use 3. Where an assertion would otherwise need a human reviewer, the legacy src/bw oracle (validate, gate_scan) acts as the deterministic judge for mechanical behaviors, reserving human review for genuinely semantic judgments and avoiding LLM-judging-LLM circularity.

### 11.2 Required scenario matrix

| Area | Required scenarios |
|---|---|
| Routing | Direct capability request bypasses routers; global/unspecified resume uses bw-start; explicit single-stage resume uses that router; adjacent skills do not steal each other's triggers; multiple active branches require selection. |
| Human convergence | “Just choose for me” pressure still produces candidates, recommendation, named authority, and a stop before recording the choice. |
| State writes | Stable ID allocation; unknown-field preservation; revision conflict across every mutable record; flat backup and reread; versioned refs; evidence correction propagation; duplicate/forked revision-chain failure; stale lineage propagation. |
| Experiments | Design before result; missing precommitted threshold; supported/falsified/inconclusive outcomes; human Kill/Proceed; ledger and backtrack update. |
| Gate authority | Missing, ambiguous, and insufficient decision maker; evidence-ready trigger; expired timebox with incomplete evidence. |
| Gate exits | Go, Conditional Go, mandatory Conditional closeout, Recycle, Pivot, and Kill for both gates; condition inheritance/closure; complete preallocated action plan; interruption after every step; applied, aborted, and manual-repair recovery. |
| G2 hard rule | L1–L3 self-report plus human insistence on Go never yields Go, baseline, or execution handoff. |
| Baseline/backtrack | G1 and G2 snapshots; active/superseded pointers; exact-revision handoff; local failure outside baseline; failure touching baseline; pending backtrack recovery; original-gate recertification. |
| Branches | Forked assumptions/conditions/baselines; descendant needs-rebase after parent falsification; merge conflict resolution and baseline clearing; pivot; Kill cleanup; parallel active branches; one active project handoff; and a G2 subject containing two solutions. |
| Local discovery and installer | From the tool-repository cwd, invoke a project skill by skill name such as /bw-start without installing and verify local references are readable; then test fresh copy, repeated copy, unrelated target conflict, broken managed link, repository path with spaces, unwritable destination, --copy/--link/--dest, reference accessibility, and managed uninstall. |

### 11.3 Automated verification

scripts/verify (implemented in Python, under the 80% coverage floor below) may orchestrate authoring-time checks without becoming a shipped methodology runtime. It verifies:

- all 19 skills exist and have valid name/description-only frontmatter whose description starts with “Use when” and contains triggers rather than procedural steps;
- every skill-local reference exists in source and installed layouts, no reference escapes its skill directory, contract metadata is present, and duplicate contract ID/version copies are byte-identical;
- no catalog or plugin manifest is required;
- schemas and sample state parse;
- no placeholders such as TODO/TBD remain in shipped skills;
- installer behavior passes in an isolated temporary HOME/destination;
- project-local discovery works from the tool-repository cwd without global installation;
- product fixtures use only flat files plus the single _bewater/records directory;
- every scenario has the required repetitions and complete result fields;
- every RED control demonstrates a target-behavior failure;
- every GREEN result passes required assertions and forbidden-behavior checks;
- manually judged assertions include reviewer identity and verdict.

Any Python authoring utility has at least 80% test coverage. Bash installer behavior is covered by the full scenario matrix rather than a one-shot smoke test.

---

## 12. Runtime Minimization

The MVP ships markdown skills plus an installer, not a general methodology runtime. Runtime minimization is a guiding principle, not a ban: a narrow helper is added when an operation needs deterministic enforcement that direct skill editing cannot reliably provide.

### 12.1 When a helper is required

Add a narrow helper when any of these holds:

- **A1 — determinism.** Correctness depends on a deterministic mechanism (compare-and-set, atomic write, hash check, transitive closure) and direct skill editing fails it repeatedly in evals.
- **A2 — cross-session coordination.** The operation needs state visible across sessions (single-writer lock, action-plan application progress) that plain files cannot express reliably.
- **A3 — scaling.** Cost degrades linearly with state size (for example full lineage/impact scans) until the skill is unusable.

### 12.2 Helper contract

Every helper has a narrow contract, tests, and **no authority to choose or relax a gate outcome**. Gate exits remain human decisions. Helper state lives directly under `_bewater/` (for example `_bewater/.bw-lock`); `_bewater/` is the runtime state root, so no `runtime/` subdirectory is added. Action-plan progress is not a separate file: it is the `action_plan.action_status` and `ordered_steps[].status` already defined in §6.5 and §8.3.

**Helper code location and distribution.** Helper source lives at `src/bwkit/` in the tool repository, where it is installed editable (`pip install -e`) for authoring and eval. Because bwkit is shared by every P0 gate and backtrack skill, it is distributed like a shared reference (§2.3): the installer (§9) deploys the `bwkit/` package into `<dest>/_bw-shared/bwkit/` alongside the shared references, with a bewater managed marker and package version. An installed skill locates bwkit relative to its own directory (`../_bw-shared/bwkit/`) and invokes it as `python <shared>/bwkit/__main__.py <args>` (equivalently `PYTHONPATH=<shared> python -m bwkit <args>`). bwkit is standard-library-only (§12.5), so no PyYAML and no product-project Python dependency is required — only a Python 3 interpreter.

### 12.3 Current helper set

The operations below already meet A1–A3 and are built first, reusing the legacy `src/bw` implementation as a starting point rather than rewriting it:

| Helper | Reuses | Resolves |
|---|---|---|
| Single-writer lock + revision CAS | src/bw io, hashing | §5.7 single-writer enforcement and TOCTOU |
| Action-plan atomic applier (preallocate IDs, idempotent, resumable) | src/bw ledger_ops | §6.5 and §8.3 recoverable gate/backtrack actions |
| Lineage/impact scanner (transitive closure, stale marking) | src/bw gate_scan | §8.2 scan correctness and scaling |
| Integrity check (duplicate head, cycle, two-head detection) | src/bw validate | §5.4 corruption detection |

The first two are P0 for the closed loop; the latter two follow. A helper not in this set is added only when a new operation meets A1–A3.

### 12.4 What stays out of the runtime

Governance stays visible in skills, schemas, decision records, and human-readable diffs. The single-writer and direct-edit limitations are accepted explicitly. The legacy implementation is retained as an oracle until the skill-only closed loop passes acceptance (§10.5); it is also the source for the helpers above, so the two roles share one codebase rather than drifting apart.

The accepted trade-off is less machine enforcement in exchange for a smaller, inspectable toolkit. The non-negotiable outcome is that minimization must not erase bewater's evidence discipline, baselines, lineage, or accountable human decisions.

### 12.5 Helper spec: single-writer lock + revision CAS (`bwkit/cas`)

The first P0 helper (§12.3). Authored as a schema-agnostic, **YAML-agnostic, standard-library-only** primitive: it operates on any revisioned text file under `_bewater/` and never parses YAML or binds to ledger/config/conditions business fields. It reuses only `bw.hashing.content_hash`; the rest of legacy `src/bw` is bypassed because it targets the pre-v5 layout (§10.5 drift).

**Lock** — `_bewater/.bw-lock`:

- `acquire_lock(root, owner, ttl_seconds=3600) -> dict` creates the lockfile atomically (`O_CREAT | O_EXCL`). On success it writes `{owner, pid, acquired_at}` and returns it. If the file already exists, it reads the holder; if the holder is stale (pid dead via `os.kill(pid, 0)`, or age > ttl) it preempts atomically (temp + `os.replace`), otherwise it raises `LockError("locked by {holder}")`.
- `release_lock(root, owner)` is a no-op when unlocked; unlinks only when `owner` matches; raises `LockError` on mismatch.
- `lock_status(root) -> dict | None` reads the lock or returns None.

**Revision CAS (text-level, standard-library-only)**:

bwkit never parses YAML. The caller — the skill, or the AI editing under the skill's direction — parses, mutates, serializes, and bumps the revision field; bwkit enforces only the deterministic mechanism: read the current revision, check it, back up, and atomically write the caller's new text. bwkit therefore depends on the Python standard library alone (`hashlib`, `os`, `re`); no PyYAML, no product-project install.

- `read_revision(path) -> int` regex-extracts the top-level integer `revision` field; `FileNotFoundError` if the file is absent, `KeyError` if the field is missing or non-integer.
- `commit(path, new_text, expected_revision, *, keep_backups=5) -> {revision, hash}`:
  1. read the current file and `read_revision` it;
  2. require `current == expected_revision`, else raise `CasConflict` (no write, no backup);
  3. require the top-level `revision` in `new_text` equals `expected_revision + 1`, else raise `BadRevisionBump` (catches a caller that forgot to bump);
  4. write a rotated backup `_bewater/.backup-{stem}-{old_rev}-{time_ns}`, keeping the newest `keep_backups`;
  5. atomic-write `new_text` via temp file + `os.replace`;
  6. return `{revision: expected_revision + 1, hash: content_hash(new_text)}`.
- Field preservation is the caller's responsibility: bwkit writes `new_text` verbatim, so unknown fields survive exactly as the caller serialized them; no temp file is left behind.

**Errors**: `LockError` (contention / owner mismatch), `CasConflict` (current revision ≠ expected), `BadRevisionBump` (new_text top-level revision ≠ expected + 1).

**CLI surface** (entry `bwkit/__main__.py`): `lock acquire --owner`, `lock release --owner`, `lock status`, `cas show <path>`, `cas bump <path> --expected <rev> --set key=val`. In the tool repository it runs as `python -m bwkit <args>` under the editable install. In an installed product project, skills invoke the same surface through the deployed `_bw-shared/bwkit/` (§12.2): `python <shared>/bwkit/__main__.py <args>`.

**Non-goals**: not cross-host / not a distributed lock; does not parse or mutate YAML, does not validate business schema, and does not preserve fields (all the caller's job); holds no gate authority (§12.2); action-plan progress lives in the decision record (§6.5), not here; depends only on the Python standard library.

**Maps to §5.7**: acquire = step 2 (single writer); `commit`'s backup + rotation = step 4; CAS check = step 6; the caller bumps the revision in `new_text` and `commit` atomic-writes it = step 7; `read_revision` supports the step 3/6 re-reads.

**Acceptance**: test matrix — lock (acquire / release / status / stale-preempt / wrong-owner / unlocked-noop); CAS (read / missing-file / commit-with-bump / conflict-no-write / bad-bump-rejected / backup-old-content / keep-N / verbatim-write / no-temp-residue); coverage ≥80% (§11.3). Field preservation is asserted at the skill and `scripts/verify` layer, not here.
