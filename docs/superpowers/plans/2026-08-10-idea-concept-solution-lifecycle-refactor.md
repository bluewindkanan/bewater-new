# BeWater Idea Seed → Concept → Solution Lifecycle Refactor

## Status

Implemented and deterministically verified on 2026-08-10. This plan supersedes
`docs/superpowers/plans/2026-08-09-ideate-concept-lifecycle-refactor.md`.

The active Shape-stage project was not regenerated or redeployed. Real fresh-context LLM eval runs
remain deferred until their cost is explicitly authorized.

The change is a breaking methodology contract. Backward compatibility with the current runtime,
ledger, artifact envelopes, or generated artifacts is not required. The implementation does not
migrate or rewrite the current `_bewater/` state or `_bewater-output/` artifacts. Any regeneration
of the active project must be authorized separately and performed through bwkit after the
implementation is verified. Installer deployment into the active Shape-stage project is blocked
until that authorization is recorded.

The English terms **Idea Seed**, **Concept**, and **Solution** are frozen by this plan. Behavioral eval
manifests are in scope, but real fresh-context LLM runs remain deferred until their cost is explicitly
authorized.

## Objective

Align BeWater's Ideate and Shape artifacts with the source methodology:

```text
Opportunity Portfolio
  -> one Idea Pool revision chain
     -> 10-15 raw ideas per Opportunity Area
     -> human-confirmed development shortlist
  -> one Concept Portfolio revision chain
     -> developed, researchable Concepts
     -> human-selected 2-4 Concepts
  -> 1-2 independent Solution revision chains
     -> Focused + Detailed + Persuasive
     -> How It Works + How To Implement + How It Makes Money
     -> L4+ evidence for every Achilles Heel before G2 readiness
```

Correct the current semantic imbalance:

- Seed items are too heavy and are incorrectly split across one artifact per Opportunity Area.
- Portfolio items are currently too light to qualify as developed, researchable Concepts.
- Solution artifacts are too light to represent the complete source-methodology deliverable.

## Source-Grounded Definitions

### Idea Seed

A raw possibility produced during divergence. Its required human-facing content is one sentence.
It may be wrong, incomplete, or infeasible. System metadata preserves lineage, clustering, strategy
filtering, and recommendation state without turning the Seed into a developed Concept.

### Concept

An early-stage, researchable proposition that indicates where the innovation is heading rather than
where it has landed. It is developed enough to create comprehension, credibility, appeal,
differentiation, debate, and test questions, but it is not a complete Solution.

### Solution

A sharply defined, two-sided proposition that dimensionalizes new consumer and commercial value.
It is complete enough to support an investment decision through design, operational and financial
assumptions, evidence, implementation logic, and storytelling.

A great Solution must be:

- **Focused** — one unambiguous big idea;
- **Detailed** — the audience, experience, mechanism, operating model, and implementation are clear;
- **Persuasive** — the evidence and commercial case explain why to invest and why confidence is
  warranted.

### Source precedence and BeWater adaptations

Resolve terminology conflicts in this order:

1. original F212 training decks and primary case materials;
2. English BeWater methodology contracts derived from those sources;
3. current skills, runtime enums, fixtures, and generated artifacts.

F212 materials sometimes use *Ideas Portfolio* for the stage output while calling brainstormed items
Concepts from the start. BeWater deliberately distinguishes a one-sentence **Idea Seed** from a
developed **Concept** so the raw divergence capture does not masquerade as a complete Concept Card.
`Idea Seed` is therefore a BeWater authoring distinction; `Concept` and `Solution` retain their F212
meanings.

F212 also lists New Invention as a Concept-to-Solution path. BeWater intentionally removes that direct
path: an invention outside the selected Concept boundaries returns to Ideate for human convergence.
This is a governance adaptation, not a claim that the source method lacks New Invention.

## Scope

### In scope

- Stable structured Opportunity Area IDs.
- Exactly one branch-global Idea Pool revision chain per active branch; each revision records its exact
  Ideate input snapshot.
- A `concept-portfolio` artifact with `CI-` item IDs.
- Complete canonical Solution frontmatter, deterministic Markdown rendering, and maturity validation.
- Exact Idea Seed → Concept → Solution lineage.
- Runtime readers and validators that operate on the new canonical ledger and artifact envelope.
- Assumption, experiment, backtrack, resume, Shape, and G2 integration.
- Source skills, templates, shared contracts, methodology documentation, installer manifests,
  deterministic tests, behavioral eval manifests, and an end-to-end fixture.

### Out of scope

- Automatic migration of the current live BeWater project.
- Regeneration of the active Shape-stage project without a separate human authorization.
- Hand-editing `_bewater/` control state.
- Backward-compatible aliases, migrations, or dual-read paths for superseded contracts.
- Creating separate files for individual Seeds or Concepts.
- Creating a new lifecycle status axis beside `document_status` and `validation_status`.
- Changing gate decision ownership or allowing AI to record human decisions.
- Designing the post-G2 Solution Specification used by the Design stage.
- Running real fresh-context LLM evals before cost authorization; this plan prepares and structurally
  validates their manifests.

## Contract Decisions

### Artifact topology

| Stage | Artifact kind | Cardinality | Item IDs |
|---|---|---:|---|
| Define | `opportunity` | one portfolio chain | `OA-001`, `OA-002`, ... |
| Ideate | `idea-pool` | exactly one chain per active branch | `CS-001`, `CS-002`, ... |
| Ideate | `concept-portfolio` | exactly one chain per active branch | `CI-001`, `CI-002`, ... |
| Shape | `solution` | 1-2 independent chains | top-level `ART-` IDs |

All four artifact kinds use append-only revision chains. `r1`, `r2`, and later files are revisions of
one logical artifact, not additional pools or portfolios.

### Skill topology

Retain the existing Ideate capability names and clarify their output semantics:

| Skill | Output | Responsibility |
|---|---|---|
| `bw-concept-seed` | `idea-pool` | diverge raw Idea Seeds and stop for shortlist confirmation |
| `bw-concept-development` | `concept-portfolio` | develop confirmed Idea Seeds into Concepts and stop for convergence |

Keep `bw-ideate` as a read-only router. Keep `bw-solution-shape` as the Shape capability, but make
its output contract complete.

### Opportunity Area identity

The `opportunity` artifact must expose structured `opportunity_areas[]`. Each entry has a stable,
artifact-local `OA-NNN` ID that is never reused across the artifact's revision chain.

A Seed and a Concept must reference both:

- the exact `opportunity` artifact revision; and
- the exact `OA-NNN` item ID resolved inside that revision.

Body headings such as `OA-1` are not authoritative lineage.

The existing `ArtifactKind.opportunity_area = "opportunity-area"` runtime value conflicts with the
deployed template and real artifacts, which use `kind: opportunity`. Rename the enum member and value
to `opportunity`. This is both a target-contract change and a fix for an existing runtime/deployed
schema bug. G1 must then count the 2-4 structured `opportunity_areas[]` inside the current portfolio
head, not count 2-4 separate Opportunity artifacts.

### Ideate input snapshot and Idea Pool uniqueness

The logical uniqueness key for an Idea Pool is the active `branch_id`, not an input-snapshot
hash. Its current revision records:

```yaml
branch_id: BR-001
input_snapshot:
  strategy_ref: artifact:ART-NNN@r
  opportunity_ref: artifact:ART-NNN@r
```

If either exact input reference changes, append `r2` or later to the same Idea Pool artifact chain.
Do not allocate a second Pool artifact ID. Validation rejects two distinct Pool chains on one active
branch even when their input snapshots differ, while accepting later revisions of the one chain.

### Item identity

- `CS-NNN` is unique across the single Idea Pool chain, not reset per Opportunity Area.
- `CI-NNN` is unique across the Concept Portfolio chain.
- IDs are allocated inside their owning artifact and never consume `config.next_ids`.
- IDs are never reused, including after kill, merge, split, or backtrack.

### Human authority

- AI may recommend Seed shortlists and Concept actions.
- Only the accountable human may confirm a Seed shortlist.
- Only the accountable human may record `selected`, `killed`, or `merged` Concepts.
- Only the accountable human may set a Solution to `validated` or choose a G2 exit.

## Target Artifact Contracts

### Opportunity Portfolio

Add this structured field to the current artifact envelope:

```yaml
opportunity_areas:
  - id: OA-001
    name: ""
    audience: ""
    opportunity: ""
    consumer_value: ""
    commercial_value: ""
    source_insight_refs: []
```

The Markdown body remains the human-readable rendering. Frontmatter is canonical for identity and
lineage.

### Idea Pool

Use one artifact for all Opportunity Areas:

```yaml
kind: idea-pool
stage: ideate
branch_id: BR-001
input_snapshot:
  strategy_ref: artifact:ART-NNN@r
  opportunity_ref: artifact:ART-NNN@r
opportunity_areas:
  - opportunity_area_id: OA-001
    seeds:
      - id: CS-001
        idea: ""
        source_insight_refs: []
        cluster_id: null
        strategy_filter: pass
    shortlist:
      recommended: []
      confirmed: []
decisions: []
```

Rules:

- `idea` is the only required human-facing Seed content.
- `source_insight_refs` is required lineage metadata.
- `cluster_id`, `strategy_filter`, and shortlist state are system annotations.
- Each Opportunity Area must contain 10-15 Seeds; 10 is hard minimum and 15 is soft ceiling.
- All Seeds remain visible, including duplicates, failed filters, and non-shortlisted items.
- `r1` may hold AI recommendations; the next revision records human confirmation.
- A changed input snapshot creates the next revision of this Pool chain, never a second chain.
- Pool-wide `CS-` identity is checked across revision history: an ID may persist for the same Seed but
  may never be reassigned to different content or reused after removal.

### Concept Portfolio

Use `concept-portfolio` with canonical `concepts[]`:

```yaml
kind: concept-portfolio
stage: ideate
branch_id: BR-001
strategy_ref: artifact:ART-NNN@r
opportunity_ref: artifact:ART-NNN@r
idea_pool_ref: artifact:ART-NNN@r
concepts:
  - id: CI-001
    item_revision: 1
    opportunity_area_id: OA-001
    source_seed_id: CS-001
    parent_ids: []
    name: ""
    pithy_description: ""
    consumer_insight: ""
    commercial_insight: ""
    idea_definition: ""
    who_its_for: ""
    how_it_works: ""
    what_it_replaces: ""
    why_big: ""
    visualization: ""
    design_principles: []
    dual_sided: {}
    evaluation: {}
    assumption_refs: [assumption:A-001@1]
    decision: null
    merge_into: null
decisions: []
exit:
  selected_concept_ids: []
```

Rules:

- Only human-confirmed Seeds may be developed.
- `opportunity_ref` must equal the Idea Pool snapshot's exact Opportunity revision.
- A Concept's `opportunity_area_id` must equal the OA group containing its `source_seed_id`; a
  cross-group mismatch is invalid even when both IDs exist.
- `pithy_description` expresses the big idea in five words or fewer where the language permits.
- `how_it_works` remains mechanism-level; full experience and operating flows belong to Solution.
- `dual_sided` remains the canonical Money/Magic block.
- `assumption_refs` pins ledger records as `assumption:A-NNN@record_revision`; assumptions are not
  embedded or duplicated inside the Portfolio.
- Hard criteria cover lineage, one unresolved tension, a distinct mechanism, Who/What/How/What it
  replaces/Why Big, strategy fit, useful pretest altitude, and Concept assumptions.
- Soft criteria cover comprehension, credibility, appeal, differentiation, naming, visualization,
  design principles, Money/Magic scores, altitude, and healthy anxiety.
- The bounded action set remains `refine`, `pivot`, `split`, `merge`, `kill`, and
  `recycle-to-OA`.
- A merge creates a new `CI-` item with both parents; it never mutates a parent in place.
- Ideate handoff requires 2-4 human-selected Concepts.

### Solution

Keep one top-level artifact per independent Solution candidate. Replace body-only Concept references
with structured Concept lineage:

```yaml
kind: solution
stage: shape
branch_id: BR-001
source_concepts:
  portfolio_ref: artifact:ART-NNN@r
  concept_ids: [CI-001]
  path: linear-refine
definition:
  name: ""
  pithy_proposition: ""
  what_it_is: ""
  who_its_for: ""
  dual_sided: {}
  dimensions: {}
how_it_works: []
how_to_implement: []
how_it_makes_money: {}
validation:
  consumer_desire: {}
  commercial_value: {}
  feasibility_and_implementation: {}
  achilles_assumption_refs: [assumption:A-001@2]
  experiment_refs: []
  evidence_refs: []
  invalidated_claims: []
content_gaps: []
applicability_exceptions: []
```

Allowed paths:

- `linear-refine`
- `pivot`
- `hybridize`
- `scope-extend`

Remove `invent`. A new invention outside selected Concept boundaries returns to Ideate rather than
bypassing human convergence.

The raw frontmatter is the single source of truth for all five required structured blocks. The
Markdown body is generated by one deterministic `render_solution_body(frontmatter)` projection; it
is never parsed to decide completeness. Validation compares the normalized stored body with the
renderer output and reports projection drift rather than treating body edits as canonical data.

The five blocks are four Solution content blocks plus one validation/readiness block. **Focused**,
**Detailed**, and **Persuasive** are quality predicates evaluated across those blocks; they are not
three sections.

Each Solution must contain the following structured blocks.

#### Definition and dimensions

- name and pithy proposition;
- what it is and who it is for;
- Money/Magic, tension, and balance choice;
- path to market;
- right to win;
- product or service platform;
- source of business;
- product/service design;
- enabling technology;
- reason to believe;
- branding;
- consumer experience.

#### How It Works

An end-to-end step sequence. Every step contains:

- action or state change;
- consumer benefit;
- operational benefit;
- strategic rationale;
- legal/regulatory rationale when applicable;
- evidence and design/prototype references.

#### How To Implement

A phased path containing:

- phase name and timing;
- objective;
- Jobs To Be Done;
- capabilities and assets;
- owner or accountable role where known;
- dependencies;
- risks;
- open questions;
- pilot and rollout logic.

#### How It Makes Money

- revenue streams;
- pricing and volume logic;
- adoption, retention, and frequency assumptions where relevant;
- development and operating costs;
- Base and Aggressive scenarios;
- revenue, margin, earnings, investment, and payback outputs where applicable;
- source or rationale for every financial assumption;
- sensitivity and unresolved model gaps.

#### Validation

- consumer desire;
- commercial value;
- feasibility and implementation;
- Concept- and Solution-layer assumptions;
- Achilles Heels;
- experiment and evidence references;
- unresolved gaps and invalidated claims.

Every required field must be one of:

- populated with structured content;
- represented by `content_gaps[]` with an exact field path and reason while the Solution is
  `unvalidated`; or
- represented by `applicability_exceptions[]` with an exact field path and non-empty rationale when
  the field is genuinely not applicable.

An omitted required field with no matching gap or applicability exception is invalid at every
maturity. `validation_status: validated` requires empty `content_gaps`, complete
Focused/Detailed/Persuasive predicates, a rationale for every applicability exception, and L4+
evidence for every required Achilles obligation. Applicability exceptions cannot waive lineage,
human authority, financial-assumption provenance, or the L4 hard criterion.

## Assumption and Evidence Contract

Update assumption layers to:

```text
root | strategy | opportunity | concept | solution | feature
```

- Concept assumptions carry `source_concept_id` and derive from an exact Concept Portfolio revision.
- Solution assumptions derive from an exact Solution revision.
- The ledger remains the single source of truth for assumption records; creating a Solution never
  copies or relayers a Concept assumption.
- A Solution's required Achilles set is the deterministic union of open durable L4 obligations from
  every selected source Concept and open obligations created at the Solution layer.
- `validation.achilles_assumption_refs` is a pinned, human-readable snapshot of that union. The
  validator rejects missing, extra, unresolved, or stale references instead of inventing inheritance
  state.
- Achilles references use `assumption:A-NNN@record_revision`; the validator compares both stable ID
  membership and pinned record revision.
- An obligation remains open until closed on its original ledger record by L4+ evidence or an allowed
  human signoff that cites L4+ evidence. A signoff cannot promote L1-L3 evidence or waive the hard
  criterion.
- Evidence at the Concept stage may remain L1-L3; G2 qualification still requires L4+ behavioral
  evidence for every active Achilles Heel.

Changing assumption layers ripples through `src/bw/cli.py` ledger `--layer` choices,
`src/bw/ledger_ops.py::_LAYER_LOOP`, CLI and ledger tests, backtrack documentation, and deployed
shared schemas. `concept` routes a local reframe to Ideate; `solution` routes one to Shape.

## Implementation Plan

Implementation changes more than three files, so execution must use Agent collaboration. Keep one
integration owner and divide work by non-overlapping responsibility after Phase 0 establishes the
expected failing baseline. The runtime switches directly to the new contract; no compatibility
phase or legacy-project smoke test is required.

### Phase 0 — Lock the contract with failing tests

Write tests before implementation.

1. Add schema tests for `idea-pool`, `concept-portfolio`, `OA-`, and `CI-`.
2. Add validator tests proving:
   - an active branch has exactly one Idea Pool chain;
   - a second Pool chain on the same branch is rejected even when its input snapshot differs;
   - a changed input snapshot is accepted only as a later revision of the existing chain;
   - Seed counts are enforced per Opportunity Area;
   - `CS-` IDs are globally unique and never reassigned across the Pool's revision history;
   - Concepts resolve one exact Pool revision, Seed ID, Opportunity revision, and OA ID;
   - a Concept's OA equals the OA group containing its source Seed;
   - only human-confirmed Seeds can become Concepts;
   - an active branch has exactly one Concept Portfolio chain, and upstream changes revise that chain;
   - only human decisions populate terminal Concept states;
   - Ideate exit contains 2-4 selected `CI-` IDs;
   - `invent` is rejected as a Solution path;
   - all five Solution blocks exist in canonical frontmatter;
   - unvalidated omissions require exact `content_gaps`, and not-applicable fields require rationales;
   - Markdown projection drift is detected without parsing headings for completeness;
   - Solution Achilles references equal the required Concept-plus-Solution obligation union;
   - validated Solutions have no content gaps and require L4+ evidence for every obligation;
   - G1 counts 2-4 OA entries in one current Opportunity Portfolio rather than separate files; and
   - G2 scanning evaluates complete validated Solutions and never chooses an exit.
3. Add failing end-to-end fixtures for three OAs, one Idea Pool, one Concept Portfolio, and two
   Solutions.

Primary test files:

- `tests/test_schema.py`
- `tests/test_validate.py`
- `tests/test_concept_lifecycle.py` (new)
- `tests/test_solution_contract.py` (new)
- `tests/test_concept_lifecycle_e2e.py` (new)
- `tests/test_gate_criteria_g2.py`
- `tests/test_gate_scan.py`

### Phase 1 — Shared contracts, schemas, and parsers

1. Replace `src/skills/_bw-shared/concept-lifecycle.md` with
   `src/skills/_bw-shared/idea-concept-solution-lifecycle.md`.
2. Extend the Opportunity contract with structured `opportunity_areas[]` and stable `OA-` IDs.
3. Complete the Opportunity ripple: update G1 scanning, fixtures, and tests to treat
   one Opportunity Portfolio's 2-4 entries as the criterion.
4. Update assumption-layer enums plus CLI choices, ledger backtrack routing, tests, and shared schema
   documentation for `concept` and `solution`.
5. Rewrite `src/bw/concept_lifecycle.py` for Idea Pool and Concept Portfolio validation, and add a shared
   `src/bw/solution_contract.py` for Solution completeness, rendering, and G2 predicates.
6. Keep item resolution local to owning artifacts; do not extend the global typed-reference grammar
   with fragments.
7. Wire the lifecycle and Solution checks into `src/bw/validate.py::validate_all`.
8. Remove `concept-seed-pool`, `concept_items`, one-pool-per-OA, and any non-Concept intermediate
   acceptance paths.

Exit condition: Phase 0 schema and validator tests pass without changing capability prose or live
project state.

### Phase 2 — One branch-global Idea Pool

1. Keep the `bw-concept-seed` skill name and make its output contract `idea-pool`.
2. Rewrite the skill and template around one Idea Pool with OA groups.
3. Reduce required Seed content to one idea sentence plus source lineage.
4. Allocate `CS-` IDs pool-wide and preserve them across revisions.
5. Recommend a shortlist separately inside each OA group.
6. Stop before recording confirmation; resume only after explicit human input.
7. Record exact `strategy_ref` and `opportunity_ref` under `input_snapshot`; revise the existing Pool
   chain when either changes.
8. Update structural tests and behavioral eval manifests for:
   - multiple OAs in one Pool;
   - duplicate clustering without deletion;
   - fewer than ten Seeds in one OA;
   - more than fifteen Seeds with an explicit warning;
   - AI recommendation without human confirmation;
   - attempted creation of a second Idea Pool chain, including one with a different snapshot;
   - valid snapshot change through the existing chain's next revision; and
   - historical `CS-` reassignment or reuse.

Primary files:

- `src/skills/bw-concept-seed/SKILL.md`
- `src/skills/bw-concept-seed/references/idea-pool-template.md`
- `tests/test_skill_bw_concept_seed.py`
- `evals/bw-concept-seed/`

### Phase 3 — Concept Portfolio

1. Keep the `bw-concept-development` skill name and make its output a true Concept Portfolio.
2. Rewrite `concept-portfolio-template.md` around canonical `concepts[]` and `CI-` IDs.
3. Develop only confirmed Seeds into `CI-` Concepts.
4. Implement the source-grounded Concept fields and dual-sided block.
5. Require the Concept Portfolio Opportunity revision to match its Idea Pool snapshot and each
   Concept's OA ID to match its source Seed's OA group.
6. Align assumption linkage with exact Concept Portfolio revisions and `CI-` identities.
7. Preserve bounded refinement, pivot, split, merge, kill recommendation, and recycle behavior.
8. Present one batch comparison and stop before human decisions.
9. Populate `selected_concept_ids` only after explicit human convergence.
10. Add eval manifests for missing Concept specificity, wrong altitude, weak visualization, missing design
   principles, merge lineage, user overload, AI premature kill, and revision cap.

Primary files:

- `src/skills/bw-concept-development/SKILL.md`
- `src/skills/bw-concept-development/references/concept-portfolio-template.md`
- `tests/test_skill_bw_concept_development.py`
- `evals/bw-concept-development/`

### Phase 4 — Complete Solution contract

1. Expand `bw-solution-shape` from a narrative shell to the full Solution contract.
2. Add structured `source_concepts`, allowed path validation, and reject `invent`.
3. Add Definition/Dimensions, How It Works, How To Implement, How It Makes Money, and Validation
   as five canonical frontmatter blocks.
4. Implement one deterministic Markdown renderer and report projection drift by normalized string
   comparison; never parse body headings to determine completeness.
5. Permit progressive unvalidated revisions only through exact `content_gaps[]`; require a rationale
   for every `applicability_exceptions[]` entry.
6. Resolve the Solution Achilles set as the checked union of source-Concept and Solution-layer open
   obligations, using original ledger IDs without copying records.
7. Require empty content gaps, complete Focused/Detailed/Persuasive predicates, supported financial
   assumptions, and L4+ evidence for every obligation before `validated`.
8. Update `bw-experiment` to attach results to Solution assumptions and exact Solution revisions.
9. Update `bw-investment-narrative` to wrap a complete validated Solution rather than compensate for
   missing Solution content.
10. Add behavioral eval manifests for incomplete flow, missing implementation logic, unsupported financial
   assumptions, absent scenario analysis, invalid path, unresolved Achilles, and premature
   validation.

Primary files:

- `src/skills/bw-solution-shape/SKILL.md`
- `src/skills/bw-solution-shape/references/solution-template.md`
- `src/bw/solution_contract.py`
- `src/skills/bw-experiment/`
- `src/skills/bw-investment-narrative/`
- `tests/test_skill_bw_solution_shape.py`
- `tests/test_skill_bw_experiment.py`
- `tests/test_skill_bw_investment_narrative.py`
- `evals/bw-solution-shape/`

### Phase 5 — Routing, recovery, and gates

1. Update `bw-ideate` to route between `bw-concept-seed` and `bw-concept-development`.
2. Update `bw-resume` to detect:
   - missing or unconfirmed global Idea Pool;
   - Concepts awaiting convergence;
   - a Concept Portfolio without 2-4 selected Concepts;
   - incomplete or unvalidated Solutions in Shape.
3. Update `bw-shape` to consume an exact `concept-portfolio` revision.
4. Update `bw-assumption-map` for Concept and Solution layers without copying inherited assumptions.
5. Update `src/bw/cli.py`, `src/bw/ledger_ops.py`, their tests, and `bw-backtrack` routes:
   - Concept-local reframe → Ideate;
   - Solution-local reframe → Shape;
   - changed OA boundary → Define + G1 recertification.
6. Add net-new G2 support to `src/bw/gate_scan.py`. `validate_all` and
   `src/bw/solution_contract.py` own structural and L4 predicates; the G2 scanner reuses them to
   assemble criteria and permitted exits without duplicating validation logic.
7. Update `bw-concept-gate` so G2 subjects are 1-2 complete validated Solutions plus the required
   investment narrative.
8. Preserve the rule that routers navigate, capabilities draft, gates assemble evidence, and humans
   decide.

Primary files:

- `src/skills/bw-ideate/`
- `src/skills/bw-resume/`
- `src/skills/bw-shape/`
- `src/skills/bw-assumption-map/`
- `src/skills/bw-backtrack/`
- `src/skills/bw-concept-gate/`
- `src/bw/cli.py`
- `src/bw/ledger_ops.py`
- `src/bw/gate_scan.py`
- related router and gate tests

### Phase 6 — Methodology, routing maps, and deployment

1. Update the English shared contract first.
2. Derive user-facing methodology language from that English source.
3. Update the pipeline terminology to Raw Ideas → Concepts → Solutions.
4. Define one branch-global Idea Pool, one branch-global Concept Portfolio, and 1-2 Solutions
   consistently.
5. Remove contradictory references to one Pool per OA, undeveloped Concept Items, and lightweight
   Solutions.
6. Update `CLAUDE.md`, installer manifests, copied-skill tests, and routing documentation.
7. Make the installer remove superseded managed skill copies while preserving unmanaged user files.
8. Deploy through the installer flow; do not hand-edit managed `.claude/skills/` copies and do not
   deploy into the active Shape-stage project before regeneration authorization.

Primary files:

- `bewater-methodology/bewater-core.md`
- `CLAUDE.md`
- `install.sh`
- installer manifests and tests
- source skill references under `src/skills/`

#### Existing artifacts to retain and rewrite

Retain these source, test, and eval paths. Rewrite their contracts in place rather than creating
newly named skills or parallel lifecycle implementations:

- `src/bw/concept_lifecycle.py`
- `src/skills/bw-concept-seed/`
- `src/skills/bw-concept-development/`
- `tests/test_concept_lifecycle.py`
- `tests/test_concept_lifecycle_e2e.py`
- `tests/test_skill_bw_concept_seed.py`
- `tests/test_skill_bw_concept_development.py`
- `evals/bw-concept-seed/`
- `evals/bw-concept-development/`

Replace the old shared lifecycle contract with
`src/skills/_bw-shared/idea-concept-solution-lifecycle.md`. Do not create parallel or renamed
Ideate skill directories.

Do not delete the superseded 2026-08-09 plan; it remains historical decision context. Managed
deployed copies are removed only through the installer.

Do not edit source archive files under `Frog:f212 General/`.

### Phase 7 — End-to-end and regression verification

Build a fresh temporary project fixture with:

1. one Opportunity Portfolio containing three structured OAs;
2. one Idea Pool containing 10-15 Seeds per OA;
3. an AI shortlist revision and a human-confirmed revision;
4. one Concept Portfolio with `CI-` lineage and bounded revisions;
5. a human-selected 2-4 Concept handoff;
6. two Solutions, including one hybridized Solution;
7. incomplete unvalidated Solution revisions;
8. experiments closing every Achilles Heel with L4+ evidence;
9. validated Solution revisions;
10. a G2 evidence assembly that stops for the human decision; and
11. a schema-agnostic integrity input payload for the fixture's revision chains.

Verify all negative paths: duplicate Pool on one branch, second Pool with a different snapshot,
historical Seed ID reassignment, invalid OA ID, Concept/Seed OA mismatch, Seed count failure,
unconfirmed Seed, invented Concept, AI terminal decision, invalid merge parent, body-only lineage,
missing Solution block, unlisted content gap, unjustified applicability exception, Markdown projection
drift, unsupported commercial assumption, incomplete Achilles union, unresolved obligation, and
premature G2 readiness.

## Agent Collaboration During Implementation

After Phase 0 establishes the lifecycle's failing contract tests, split implementation into three
coordinated workstreams:

| Agent | Ownership | Must not edit |
|---|---|---|
| Contract/runtime | schemas, lifecycle resolver, validator, gate scan | skill prose and eval scenarios |
| Skills/methodology | source skills, templates, routing docs, methodology | runtime Python modules |
| Tests/evals | deterministic tests, fixtures, behavioral eval manifests | production contracts without coordination |

The root integration owner resolves contract questions, runs the full suite, reviews combined diffs,
and performs the final installer verification. Agents must not edit `_bewater/` or generated project
artifacts.

## Acceptance Criteria

- Runtime schema and IO use the new canonical ledger/artifact fields without silently dropping
  record history or artifact-specific frontmatter.
- `kind: opportunity` is canonical, and G1 evaluates 2-4 OA entries inside one current Opportunity
  Portfolio.
- Exactly one current Idea Pool chain exists for each active branch.
- An Ideate input change creates the next revision of that chain, never a second chain.
- The Pool contains distinct OA groups and 10-15 visible Seeds per OA.
- Seed content is one raw idea sentence; metadata does not masquerade as developed content.
- `CS-` IDs are pool-wide, stable, and never reassigned or reused across revision history.
- The system never confirms a shortlist for the human.
- Exactly one Concept Portfolio chain represents each active branch's Ideate working set; upstream
  changes create later revisions rather than a second chain.
- Every Concept uses a `CI-` ID and resolves exact Opportunity, OA, Pool, and Seed lineage; its OA
  matches the OA group containing its source Seed.
- Concepts contain the complete researchable-proposition fields but do not contain full Solution
  implementation or commercial-case detail.
- Only human decisions populate selected, killed, and merged Concept states.
- Ideate handoff contains 2-4 selected Concepts.
- Shape produces 1-2 independent Solution chains from exact selected Concepts.
- Every Solution's canonical frontmatter contains Definition/Dimensions, How It Works, How To
  Implement, How It Makes Money, and Validation.
- The Markdown body is a deterministic projection of canonical Solution data; validator completeness
  does not depend on Markdown heading parsing.
- Every missing unvalidated field is an exact content gap, and every not-applicable field has a
  rationale; validated Solutions contain no content gaps.
- `invent` is not an allowed Shape path.
- A Solution's Achilles references exactly equal the open source-Concept plus Solution-layer
  obligation union without copied assumption records.
- A validated Solution is Focused, Detailed, Persuasive, and has L4+ evidence for every required
  Achilles obligation.
- The net-new G2 scanner consumes 1-2 complete validated Solutions, reuses Solution predicates, and
  never treats a narrative shell as ready or chooses a gate exit.
- No capability chooses a gate exit or writes a human decision.
- No implementation step hand-edits `_bewater/` state.
- Installer deployment does not regenerate or strand the active Shape-stage project without separate
  human authorization.
- New or materially changed Python behavior follows TDD and total coverage remains at least 80%.
- All deterministic tests, structural eval-manifest checks, installer tests, integrity checks, and
  end-to-end fixtures pass.
- Real fresh-context LLM eval runs remain explicitly deferred until cost authorization; manifest
  readiness is not misreported as completed behavioral execution.
- Idea Seed, Concept, and Solution terminology plus the New Invention governance adaptation remain
  frozen and documented.

## Verification Order

Run the narrowest relevant command after each TDD step, then finish with:

```bash
pytest tests/test_io.py
pytest tests/test_schema.py tests/test_concept_lifecycle.py tests/test_validate.py
pytest tests/test_solution_contract.py tests/test_gate_scan.py tests/test_gate_criteria_g2.py
pytest tests/test_cli_wiring.py tests/test_ledger_ops.py
pytest tests/test_skill_bw_concept_seed.py tests/test_skill_bw_concept_development.py
pytest tests/test_skill_bw_solution_shape.py tests/test_skill_bw_experiment.py
pytest tests/test_skill_bw_ideate.py tests/test_skill_bw_shape.py tests/test_skill_bw_resume.py
pytest tests/test_skill_bw_concept_gate.py
pytest tests/test_concept_lifecycle_e2e.py
pytest --cov=bw --cov=bwkit --cov-report=term-missing --cov-fail-under=80
python -m bwkit check integrity < tests/fixtures/idea-concept-solution/integrity-input.json
```

The fresh end-to-end fixture must be clean. The current real project is not a compatibility target
and is not included in acceptance verification.

After deterministic tests are green, structurally validate the behavioral eval manifests for
`bw-concept-seed`, `bw-concept-development`, `bw-solution-shape`, routers, backtrack, and G2. Do not start
real fresh-context LLM runs without explicit cost authorization. If authorized later, run them as a
separate recorded acceptance pass with the existing repetition and human-review rules.

## Final Review Checklist

- [x] No `TODO`, `TBD`, placeholder schema, or ambiguous cardinality remains.
- [x] The English shared contract is authoritative and other language derives from it.
- [x] Primary F212 sources, derived BeWater contracts, and BeWater-specific adaptations have an
      explicit precedence order.
- [x] Raw Idea, Concept, Solution, and Solution Specification are not conflated.
- [x] One logical artifact versus multiple append-only revisions is stated consistently.
- [x] Idea Pool uniqueness is branch-scoped; input changes revise rather than fork the Pool chain.
- [x] Every item-level reference has an owning artifact revision plus a local item ID.
- [x] Opportunity G1 cardinality counts structured OA entries, not Opportunity files.
- [x] Human decision boundaries are explicit in skills, validators, tests, and evals.
- [x] Solution completeness and Solution validation are separate checks.
- [x] Solution frontmatter is canonical, applicability/gap semantics are deterministic, and the body
      is a checked projection.
- [x] Concept Achilles obligations are referenced by Solutions without copying ledger records.
- [x] Runtime validation has been exercised against the fresh canonical fixture without mutating the
      current real project.
- [x] Fresh-context LLM execution is labeled deferred unless separately authorized and recorded.
- [x] Current live state was not mutated as part of implementation or verification.
