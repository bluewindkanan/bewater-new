# BeWater Ideate Concept Lifecycle Refactor

## Objective

Replace the current one-shot `bw-concept-card` flow with an explicit Ideate lifecycle:

```text
Opportunity Area
  -> 10-15 Concept Seeds per OA
  -> shortlist
  -> Formal Concepts
  -> bounded evaluation/revision loop
  -> 2-4 Selected Concepts
  -> Ideate-to-Shape concept portfolio handoff
  -> 1-2 Solutions in Shape
```

This is a fresh contract. No compatibility or migration work is required for existing
`ART-008`-style artifacts.

## Design Decisions

### Skill boundaries

Keep `bw-ideate` as a thin router and replace `bw-concept-card` with two capabilities:

| Skill | Responsibility | Stops at |
|---|---|---|
| `bw-concept-seed` | Diverge per OA, preserve the seed pool, cluster/deduplicate, recommend a shortlist | Human confirmation of which seeds to develop |
| `bw-concept-development` | Develop formal concepts, evaluate, revise, pivot, split, merge, and prepare convergence | Human `select / revise / merge / kill` decision |

Do not create separate generate/evaluate/converge skills. They share one concept lifecycle and
one human decision surface.

### Artifact layers

All three artifacts are owned by Ideate. The portfolio is an Ideate-to-Shape handoff, not a
Shape artifact.

1. `concept-seed-pool`: one append-only artifact per OA; contains 10-15 stable seed item IDs,
   one-line mechanisms, and source references.
2. `concept`: one append-only artifact per developed concept; contains its own revision chain,
   card fields, evaluation, assumptions, and iteration history.
3. `concept-portfolio`: one append-only artifact per convergence event; references exact concept
   revisions and records the human-selected 2-4 concept set.

Shape consumes the portfolio and produces `solution` artifacts. It does not reselect concepts.

### Concept lifecycle

```text
seeded -> shortlisted -> developed -> evaluated
                              ^          |
                              |          v
                       needs-revision <-+
                              |
                selected / killed / merged / recycle-to-OA
```

AI may propose transitions and write evaluation evidence. Only the accountable human may record
`selected`, `killed`, or `merged`.

### Bounded iteration

Each evaluation pass reports hard failures, soft weaknesses, evidence gaps, and one recommended
action:

- `refine`: wording, altitude, or scope changes without changing the core mechanism;
- `pivot`: change the target, tension, or mechanism;
- `split`: separate two independent mechanisms in one concept;
- `merge`: combine complementary concepts and preserve both parents;
- `kill`: recommend removal;
- `recycle-to-OA`: the concept cannot pass after two revision attempts or the OA boundary is wrong.

Hard criteria are: OA/strategy/insight lineage, one clear tension, distinct mechanism, complete
Who/What/Why Big, strategy-filter pass, pre-testable altitude, and concept-level assumptions.
Soft criteria are the eight capture/quality fields, Money/Magic scores, visualization, naming, and
design principle. A concept may enter human convergence only when hard criteria pass; soft
uncertainty remains visible.

The loop has a maximum of two AI revision proposals per concept before `recycle-to-OA` is
presented. The human may explicitly request another pass, but the system must never loop silently.

### Human decision surface

The user is not asked to complete eight fields or eight separate choices.

1. Seed checkpoint: review each OA's pool, clusters, and recommended shortlist.
2. Concept checkpoint: review a batch comparison and decide `select / revise / merge / kill`.

Altitude and healthy anxiety are shown as batch columns and require one human judgment per final
candidate. The capability stops before recording those choices and resumes to write the next
portfolio revision after the decision.

### Lineage and evidence

Concepts carry exact references to their OA, locked strategy, source insights, and relevant evidence.
Concept-level assumptions are created in the ledger with `layer: concept` and `derived_from` pointing
to the exact concept revision. Evidence at Ideate may remain L1-L3; L4+ behavioral evidence belongs
to Shape/G2. Item-level seed lineage uses an explicit fragment reference in the shared contract,
for example `artifact:ART-101@2#item:CS-004`.

## Implementation Plan

### Phase 1: Contracts and deterministic validation

- Add a shared `concept-lifecycle` contract covering artifact kinds, item IDs, statuses, actions,
  hard/soft criteria, decision ownership, and item-level references.
- Add `concept-seed-pool`, `concept`, and `concept-portfolio` templates.
- Add a schema-agnostic `bwkit` lifecycle validator for counts, reference resolution, legal state
  transitions, exact revision pins, per-OA seed minimums, and the 2-4 portfolio exit.
- Add CLI wiring and deterministic unit tests before changing skills.

### Phase 2: Seed capability

- Create `src/skills/bw-concept-seed/SKILL.md` and references.
- Generate 10-15 seeds per OA with stable IDs; capture one-line mechanism, intended audience,
  source insight refs, and initial strategy-filter result.
- Cluster near-duplicates and expose all seeds plus recommendations; never hide AI-rejected seeds.
- Stop at the seed checkpoint and require the human to confirm the development shortlist.

### Phase 3: Concept development capability

- Create `src/skills/bw-concept-development/SKILL.md` and references.
- Consume only confirmed seed IDs.
- Generate one formal concept artifact per developed seed, fill the eight fields, run anchored
  criteria/scoring, attach evidence and concept assumptions, and emit a bounded revision proposal.
- Preserve every revision and parent relation for refine, pivot, split, and merge.
- Present a batch convergence view and stop before human decisions.
- After the decision, write `concept-portfolio` with exact selected concept revisions and explicit
  kill/merge records.

### Phase 4: Router and downstream contracts

- Update `bw-ideate` to report seed counts, shortlist status, concept lifecycle states, revision
  blockers, and portfolio readiness; route to the correct capability mode.
- Remove `bw-concept-card` from source/deployment and route maps.
- Update `bw-shape` to require an Ideate `concept-portfolio` containing 2-4 selected concepts.
- Update `bw-solution-shape` to preserve concept references and record the selected concept-to-
  solution path.
- Update `bw-assumption-map` and `bw-backtrack` for concept-layer assumptions and item-level impact.

### Phase 5: Methodology and evaluation coverage

- Update `bewater-core.md` and the English skill references to define the linear macro-flow plus
  bounded intra-stage loops.
- Clarify the quantity contract: 10-15 seeds per OA, 3-5 developed concepts per OA as a working
  shortlist, and 2-4 selected concepts globally.
- Replace keyword-only tests with structural tests for artifacts, lifecycle transitions, lineage,
  human-decision boundaries, and Shape handoff.
- Add behavioral evals for duplicate seeds, missing evidence, failed hard criteria, repeated
  revision, merge/pivot lineage, OA abandonment, AI premature kill, and user overload.
- Run a fresh end-to-end fixture from OA through concept portfolio and Shape input.

## Acceptance Criteria

- Every OA has a persisted 10-15 item seed pool with stable IDs.
- The system never silently removes seeds or records human convergence decisions.
- Formal concepts have independent revision chains and exact Insight/Evidence/OA lineage.
- A failed hard criterion produces a bounded revision action, not an automatic selection.
- Two failed revision proposals produce an explicit `recycle-to-OA` choice.
- The user sees two batch decision points, not eight field-level questions per concept.
- Ideate cannot hand off fewer than 2 or more than 4 selected concepts.
- Shape consumes the exact `concept-portfolio` revision and produces 1-2 solution candidates.
- A concept merge preserves both parent references; a pivot creates a new revision or child with a
  clear rationale.
- All new structural and behavioral tests pass.

## Risks and Controls

| Risk | Control |
|---|---|
| Seed volume becomes token-heavy | Keep seeds lightweight; only shortlisted seeds receive full cards |
| Loop becomes endless | Hard criteria, two-proposal cap, explicit recycle action |
| AI still performs convergence | Separate recommendations from human-owned statuses and preserve rejected items |
| Scores become decorative | Anchored scores, rationale, confidence, and hard criteria separate from soft scores |
| Shape reopens Ideate selection | Require an exact `concept-portfolio` input and route failures through bounded backtrack |

## Verification Order

1. `pytest` for lifecycle and artifact validators.
2. Structural skill and eval-manifest tests.
3. Fresh-context green/red behavioral evals.
4. End-to-end fixture: three OAs, seed pools, revisions, merge/pivot, 2-4 portfolio, Shape handoff.
5. Integrity and impact scans over the generated artifact graph.
