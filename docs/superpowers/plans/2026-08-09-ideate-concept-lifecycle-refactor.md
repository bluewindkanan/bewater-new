# BeWater Ideate Concept Lifecycle Refactor

## Objective

Replace the current one-shot `bw-concept-card` flow with an explicit Ideate lifecycle:

```text
Opportunity Area
  -> 10-15 Concept Seeds per OA
  -> Concept Portfolio with formal candidate items
  -> bounded candidate evaluation/revision loop
  -> same portfolio revision with 2-4 Selected Concepts
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

Both artifacts are owned by Ideate. The portfolio is an Ideate-to-Shape handoff, not a Shape
artifact.

1. `concept-seed-pool`: one append-only artifact per OA; contains 10-15 stable seed item IDs,
   one-line mechanisms, and source references.
2. `concept-portfolio`: one append-only artifact for the Ideate working set; contains the formal
   candidate Concept Items, their card fields, evaluation, assumptions, iteration history, and the
   final human-selected 2-4 subset.

Shape consumes the portfolio and produces `solution` artifacts. It does not reselect concepts.

`document_status` and `validation_status` retain their existing meanings. Do not add a third
authoritative status axis. Seed shortlist decisions are authoritative in the seed-pool revision;
`selected`, `killed`, and `merged` decisions are authoritative in the concept-portfolio decision
records. In-flight Concept Item state (`developed`, `evaluated`, `needs-revision`) is derived from
the latest portfolio revision's item evaluation and iteration fields. A renderer may show the
derived state, but no writer may persist a conflicting lifecycle status in frontmatter.

### Concept lifecycle

```text
seeded -> shortlisted -> developed -> evaluated
                              ^          |
                              |          v
                       needs-revision <-+
                              |
                selected / killed / merged
                               |
                 recommend recycle-to-OA
                               |
                        bw-backtrack (stop)
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

`recycle-to-OA` is a recommendation and a stop condition, never a lifecycle terminal state. The
capability hands it to `bw-backtrack` with the exact trigger and proposed route. A concept-local
reframe is a small Ideate/Shape loop; changing the OA boundary is a large loop that returns to
Define + G1 recertification. Ideate never edits a G1-baselined OA implicitly.

### Human decision surface

The user is not asked to complete eight fields or eight separate choices.

1. Seed checkpoint: review each OA's pool, clusters, and recommended shortlist.
2. Concept checkpoint: review a batch comparison and decide `select / revise / merge / kill`.

Altitude and healthy anxiety are shown as batch columns and require one human judgment per final
candidate. The capability stops before recording those choices and resumes to write the next
portfolio revision after the decision.

### Lineage and evidence

Each Concept Item carries exact references to its OA, locked strategy, source insights, and relevant
evidence. Concept-level assumptions are created in the ledger with `layer: concept`, `derived_from`
pointing to the exact portfolio revision, and a validated `source_concept_id`. Evidence at Ideate may
remain L1-L3; L4+ behavioral evidence belongs to Shape/G2. A Concept Item records the exact seed-pool
artifact revision plus `source_seed_id`; the lifecycle validator resolves the item ID against the
pool. This preserves exact provenance without extending the global typed-ref grammar or every shared
resolver.

### Contract Clarifications

- Add `concept-seed-pool` and `concept-portfolio` to `ArtifactKind`; remove top-level `concept` as
  an artifact kind. Formal Concepts are nested `concept_item` records inside the portfolio.
- Remove top-level `concept` from the dual-sided artifact set and validate Money/Magic fields on each
  Concept Item inside `concept-portfolio`.
- Treat item IDs as pool-local (`CS-001`, `CS-002`, ...), allocated inside the pool artifact rather
  than in `config.next_ids`. IDs are never reused within an OA pool's revision chain.
- Integrate lifecycle invariants into `bw.validate.validate_all`, the single health-check path used
  by gates and resume. Do not create a second schema-aware validation command. Generic integrity and
  impact helpers remain reusable where they already apply.
- Add parser/schema tests for the new enum values, status derivation, source-seed resolution, and
  old typed references without fragments. No global `#item:` parser change is in scope.

## Implementation Plan

### Phase 1: Contracts and deterministic validation

- Add a shared `concept-lifecycle` contract covering artifact kinds, item IDs, statuses, actions,
  hard/soft criteria, decision ownership, Concept Item structure, and pool/item references.
- Add `concept-seed-pool` and `concept-portfolio` templates. The portfolio template contains the
  nested formal Concept Item schema and its decision record; there is no standalone concept file.
- Extend `src/bw/schema.py` with the two new artifact kinds and update the kind-specific validation
  sets; do not add a new global status axis.
- Add concept lifecycle checks to `src/bw/validate.py::validate_all`: seed counts, source-seed
  resolution, derived in-flight state, portfolio decision ownership, legal revision references,
  per-OA minimums, and the 2-4 portfolio exit.
- Add deterministic schema/validator tests before changing skills. A separate lifecycle CLI is not
  needed; `bw validate` remains the single health-check entry point.

### Phase 2: Seed capability

- Create `src/skills/bw-concept-seed/SKILL.md` and references.
- Generate 10-15 seeds per OA with stable IDs; capture one-line mechanism, intended audience,
  source insight refs, and initial strategy-filter result.
- Cluster near-duplicates and expose all seeds plus recommendations; never hide AI-rejected seeds.
- Treat 10 as the hard minimum and 15 as a soft ceiling. Above 15, emit a warning and ask whether
  the additional divergence is justified; never silently truncate the pool.
- Stop at a capability continuation checkpoint (not a gate, signoff, or baseline) and require the
  human to confirm the development shortlist.

### Phase 3: Concept development capability

- Create `src/skills/bw-concept-development/SKILL.md` and references.
- Consume only confirmed seed IDs.
- Create or revise Concept Items inside the single `concept-portfolio` artifact, fill the eight
  fields, run anchored criteria/scoring, attach evidence and concept assumptions, and emit a bounded
  revision proposal.
- Preserve every portfolio revision, Concept Item revision, and parent relation for refine, pivot,
  split, and merge. A merge creates a new Concept Item and records both parent IDs; it does not
  mutate the parent items in place.
- Present a batch convergence view and stop before human decisions.
- After the decision, write the next `concept-portfolio` revision with the selected Concept Item IDs
  and explicit kill/merge records.

### Phase 4: Router and downstream contracts

- Update `bw-ideate` to report seed counts, shortlist status, concept lifecycle states, revision
  blockers, and portfolio readiness; route to the correct capability mode.
- Remove `bw-concept-card` from source/deployment and route maps.
- Update `bw-resume` and `bw-resume/references/routing.md` to inspect the latest seed-pool and
  concept/portfolio heads, surface pending human decisions, and route back to `bw-ideate` without
  inventing a new recovery owner.
- Update the project `CLAUDE.md` routing table and installer manifests to replace
  `bw-concept-card` with the two capabilities.
- Update `bw-shape` to require an Ideate `concept-portfolio` containing 2-4 selected concepts.
- Update `bw-solution-shape` to preserve portfolio revision + Concept Item IDs and record the selected
  concept-to-solution path.
- Update `bw-assumption-map` and `bw-backtrack` for concept-layer assumptions and portfolio-item
  impact. A concept revision reframe updates the portfolio; a changed OA still routes through the
  baseline-aware large loop.

### Phase 5: Methodology and evaluation coverage

- Update `bewater-core.md` and the English skill references to define the linear macro-flow plus
  bounded intra-stage loops.
- Unify all methodology references to one quantity contract: 10-15 seeds per OA, 3-5 developed
  concepts per OA as a working shortlist, and 2-4 selected concepts globally. Remove the conflicting
  "20-30 total", "3-5 then 5", and other legacy counts from the core and quick-start sections.
- Replace keyword-only tests with structural tests for artifacts, lifecycle transitions, lineage,
  human-decision boundaries, resume routing, and Shape handoff. Explicitly remove/rewrite
  `tests/test_skill_bw_concept_card.py`, `tests/test_skill_bw_ideate.py`, and `evals/bw-concept-card/`;
  add `evals/bw-concept-seed/` and `evals/bw-concept-development/`.
- Add behavioral evals for duplicate seeds, missing evidence, failed hard criteria, repeated
  revision, merge/pivot lineage, OA abandonment, AI premature kill, and user overload.
- Run a fresh end-to-end fixture from OA through concept portfolio and Shape input.

## Acceptance Criteria

- Every OA has a persisted 10-15 item seed pool with stable IDs.
- Seed IDs are pool-local, stable across revisions, and allocated without changing global
  `config.next_ids`.
- The system never silently removes seeds or records human convergence decisions.
- The portfolio has an append-only revision chain; every Concept Item has a stable ID, item revision,
  and exact Insight/Evidence/OA/Seed lineage.
- `selected`, `killed`, and `merged` resolve only from concept-portfolio decisions; no conflicting
  lifecycle frontmatter is accepted.
- A failed hard criterion produces a bounded revision action, not an automatic selection.
- Two failed revision proposals produce an explicit `recycle-to-OA` choice.
- `recycle-to-OA` stops and routes through `bw-backtrack`; it never edits an OA or bypasses G1.
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
| New artifact kinds break shared runtime paths | Enum/schema tests, `validate_all` integration tests, and explicit no-fragment parser coverage |
| Resume loses a pending seed/concept decision | `bw-resume` derives pending work from artifact heads and routes to `bw-ideate` |

## Verification Order

1. `pytest` for lifecycle and artifact validators.
2. Structural skill and eval-manifest tests.
3. Fresh-context green/red behavioral evals.
4. End-to-end fixture: three OAs, seed pools, revisions, merge/pivot, 2-4 portfolio, Shape handoff.
5. Integrity and impact scans over the generated artifact graph.
