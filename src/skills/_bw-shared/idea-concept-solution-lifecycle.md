---
contract_id: bw-idea-concept-solution-lifecycle
contract_version: 2
---

# BeWater Idea Seed → Concept → Solution Lifecycle (authoritative)

This English contract is the source of truth for lifecycle terminology, artifact
topology, lineage, quality, and decision ownership. User-facing methodology text
derives from it. Shared envelope and reference semantics live in
`ledger-schema.md`.

## Frozen meanings

- **Idea Seed** — one raw possibility stated in one sentence. It may be wrong,
  incomplete, or infeasible. Lineage and filtering data are metadata, not extra
  human-facing Seed content.
- **Concept** — an early-stage, researchable proposition that creates
  comprehension, credibility, appeal, differentiation, debate, and test
  questions. It indicates where the innovation is heading, not where it has
  landed.
- **Solution** — a sharply defined, two-sided proposition complete enough for an
  investment decision through design, operational and financial assumptions,
  evidence, implementation logic, and storytelling.

Primary F212 sources and case materials take precedence over this derived
contract; this contract takes precedence over skills, runtime enums, fixtures,
and generated artifacts. BeWater deliberately distinguishes raw Idea Seeds from
developed Concepts. New Invention does not bypass convergence: work outside the
selected Concept boundaries returns to Ideate.

## Artifact topology

| Stage | Kind | Cardinality | Local item IDs |
| --- | --- | --- | --- |
| Define | `opportunity` | one portfolio revision chain | `OA-NNN` |
| Ideate | `idea-pool` | exactly one chain per active branch | `CS-NNN` |
| Ideate | `concept-portfolio` | exactly one chain per active branch | `CI-NNN` |
| Shape | `solution` | one or two independent chains | none |

All are append-only revision chains. A new file with the same `artifact_id` and
the next `revision` revises one logical artifact; it does not create another
Pool or Portfolio. Item IDs are allocated inside their owning chain, never from
`config.next_ids`, and are never reused after removal, kill, merge, split, or
backtrack.

## Opportunity Portfolio

The canonical `opportunity` frontmatter contains `opportunity_areas[]`. Every
entry has a stable artifact-local `OA-NNN` ID plus `name`, `audience`,
`opportunity`, `consumer_value`, `commercial_value`, and
`source_insight_refs`. IDs are never reused across the Portfolio's revision
history. Markdown headings are not authoritative lineage.

G1 counts two to four current `opportunity_areas[]` in this one Portfolio head;
it never counts separate Opportunity files.

## Idea Pool

The active `branch_id` is the Pool uniqueness key. Its canonical fields are:

- `input_snapshot.strategy_ref` and `input_snapshot.opportunity_ref`, both exact
  artifact revisions;
- `opportunity_areas[]`, each with `opportunity_area_id`, `seeds`, and
  `shortlist.recommended` / `shortlist.confirmed`;
- `decisions[]` for the human shortlist checkpoint.

Each OA group contains 10–15 visible Seeds. Ten is a hard minimum; above fifteen
is allowed only with an explicit warning. Each Seed contains `id`, one required
`idea` sentence, `source_insight_refs`, optional `cluster_id`, and
`strategy_filter`. Clustering and failed filters never remove Seeds.

`CS-NNN` is unique pool-wide. Across revision history an ID may persist only for
the same Seed and may never be reassigned or reused. AI may recommend a shortlist;
only the accountable human may populate `shortlist.confirmed`, in a later
revision. If either input snapshot reference changes, revise the existing Pool
chain. Never allocate a second Pool chain for that branch.

## Concept Portfolio

The Portfolio records exact `strategy_ref`, `opportunity_ref`, and
`idea_pool_ref`, plus canonical `concepts[]`, `decisions[]`, and
`exit.selected_concept_ids`.

Only a human-confirmed Seed may become a Concept. Every Concept carries:

- `id` (`CI-NNN`), `item_revision`, `opportunity_area_id`, `source_seed_id`, and
  `parent_ids`;
- `name`, `pithy_description`, `consumer_insight`, `commercial_insight`,
  `idea_definition`, `who_its_for`, `how_it_works`, `what_it_replaces`,
  `why_big`, `visualization`, and `design_principles`;
- canonical `dual_sided`, `evaluation`, and pinned `assumption_refs`;
- `decision` and `merge_into`, which remain null until a human decision.

The Portfolio's `opportunity_ref` must equal the Pool snapshot's exact
Opportunity revision. A Concept's OA must equal the OA group containing its
source Seed. `pithy_description` is five words or fewer where the language
permits. Concept `how_it_works` stays mechanism-level; complete experience,
operations, implementation, and commercial modeling belong to Solution.

All hard criteria must pass before human convergence: exact lineage, one
unresolved tension, a distinct mechanism, complete Who/What/How/What it
replaces/Why Big, strategy fit, useful pretest altitude, and Concept assumptions.
Soft criteria remain visible: comprehension, credibility, appeal,
differentiation, naming, visualization, design principles, Money/Magic scores,
altitude, and healthy anxiety. L1–L3 evidence may remain open in Ideate.

AI recommends exactly one bounded action per Concept: `refine`, `pivot`,
`split`, `merge`, `kill`, or `recycle-to-OA`. A merge creates a new `CI-NNN`
with both parents and never mutates a parent in place. AI stops after two
revision proposals unless the human explicitly requests another pass. Only the
accountable human may record `selected`, `killed`, or `merged`. The handoff to
Shape requires two to four human-selected `CI-NNN` IDs.

## Solution

Each independent Solution records `source_concepts.portfolio_ref`, one or more
selected `concept_ids`, and one path: `linear-refine`, `pivot`, `hybridize`, or
`scope-extend`. `invent` is invalid.

Canonical frontmatter contains five required blocks:

1. `definition` — name, pithy proposition, what it is, who it is for,
   Money/Magic and complete dimensions;
2. `how_it_works` — end-to-end entries with `step`, `action`, consumer,
   operational, strategic and legal/regulatory rationale, `evidence_refs`, and
   `design_refs`;
3. `how_to_implement` — phases, timing, objectives, Jobs To Be Done,
   capabilities/assets, `owner`, dependencies, risks, questions, and
   `pilot_and_rollout`;
4. `how_it_makes_money` — revenue, pricing/volume, adoption/retention/frequency,
   costs, Base/Aggressive outputs, sourced `{assumption, source}` entries,
   sensitivity list, and gaps;
5. `validation` — consumer desire, commercial value, and feasibility and
   implementation each as `{claim, evidence_refs}`, plus pinned Achilles
   assumptions, experiments, evidence, and invalidated claims.

The raw frontmatter is authoritative. One deterministic
`render_solution_body(frontmatter)` projection produces the Markdown body.
Validation compares normalized body output and reports projection drift; it
never parses headings to infer completeness.

Every required field is populated, listed by exact path in `content_gaps` while
unvalidated, or listed in `applicability_exceptions` with a non-empty rationale.
Exceptions cannot waive lineage, human authority, financial provenance, or L4+
evidence. A validated Solution has no content gaps and is Focused (one
unambiguous big idea), Detailed (audience, experience, mechanism, operating
model, and implementation are clear), and Persuasive (evidence and the
commercial case warrant investment confidence). Only the accountable human may
set `validation_status: validated`. That revision must contain a human-written
signoff `{person, role, scope: solution-validation, artifact_revision,
signed_at}`; the capability never prefills it.

## Assumptions, evidence, and backtracking

Assumption layers are `root | strategy | opportunity | concept | solution |
feature`. Concept assumptions carry `source_concept_id` and derive from an exact
Concept Portfolio revision. Solution assumptions derive from an exact Solution
revision. The ledger remains the sole assumption record; Solutions never copy
or relayer Concept assumptions.

A Solution's required Achilles set is the deterministic union of open durable
L4 obligations from all source Concepts and the Solution layer.
`validation.achilles_assumption_refs` pins the exact
`assumption:A-NNN@record_revision` set. Missing, extra, unresolved, or stale
references fail validation. An obligation closes only on its original record
with L4+ evidence or an allowed human signoff that itself cites L4+ evidence.

A Concept-local reframe returns to Ideate. A Solution-local reframe returns to
Shape. A changed OA boundary returns to Define and requires G1 recertification.
No capability silently changes a baselined boundary.

## Authority boundary

Routers read and navigate. Capabilities draft and stop before human decisions.
Gates assemble evidence, present permitted exits, and stop. No AI confirms a
Seed shortlist, records terminal Concept states, validates a Solution, or
chooses a gate exit.
