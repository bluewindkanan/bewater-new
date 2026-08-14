# Research Plan

The Research Plan is the branch's one living `kind: research` planning artifact. It iterates through
adaptive Sprints using the same artifact ID and `supersedes_ref`. Older revisions preserve history;
do not duplicate every prior Sprint in the current revision.

Revision 1 has exactly four core sections: Research Objective, Learning Plan, Next Sprint, and
Research Progress. Sprint Decision and Insight Ingredients and Insight Readiness
appear only after execution; omit a section rather than add an empty placeholder. An internal Orient pass may be part of initialization, but persist it as a
separate meaningful delta only when it changes the agenda, priorities, boundary, or lens map.

## Artifact layout

The living research artifact is organized around adaptive Sprints. Each revision persists the stable
sections below; the execution-only sections appear only after a Sprint has actually run.

1. **Research Objective** — the current Charter revision, innovation challenge, research boundary,
   strategic uncertainties, and the future
   strategic choices the research may inform without implying such a choice already exists.
2. **Learning Plan** — stable learning intent and optional projected assumption refs.
3. **Next Sprint** — bounded research missions for the next Sprint only.
4. **Research Progress** — the authoritative answer state and exact question-to-Knowledge index.
5. **Sprint Decision — after execution only** — what was learned, contradicted,
   reframed, deepened, or dropped; new questions and remaining gaps; and the next transition with
   rationale.
6. **Insight Ingredients and Insight Readiness — after execution only** — evidence-backed patterns, tensions, anomalies,
   challenged Accepted Beliefs, reframe candidates, and strategic relevance, plus the Insight
   Readiness assessment that decides whether to hand off.
Remaining uncertainty is not a separate state section. `Research Progress.remaining_gap` owns it.

### Learning Plan

Use stable artifact-local IDs such as `LP-001`. Every row has `id`, `learning_objective`,
`starting_state` (`known`, `think-known`, `unknown`, or `assumption`), `starting_view`,
`decision_relevance`, `lens`, `priority`, and optional `ledger_ref`. The Learning Plan owns learning
intent, not current answer state. Do not duplicate `answer_status` in the Learning Plan.

### Next Sprint

Fully plan only the next Sprint. Each mission uses a stable ID such as `RM-001`, one or more Learning Plan refs,
the evidence needed, smallest suitable method/source bundle, exclusions, dependencies,
owner, bounded budget, stop condition, expected output, and limitation.

### Research Progress

Initialize one row per Learning Plan item. Each row contains `learning_ref`, `answer_status`
(`not-researched`, `partial`, `answered`, `dropped`, or `gap-accepted`), exact `knowledge_refs`,
`current_answer` (initially `Not researched`), and `remaining_gap`. `answered` and `partial` require
at least one complete Knowledge workpaper on the same branch. `RM-NNN` is an activity identifier and
is never a Knowledge or Evidence ref. Assessment-derived candidates remain unknown until independent
Knowledge supports an answer.

### Research Objective

The Research Objective fixes what the research is about for this revision. Record the exact Charter
revision, the innovation challenge, the research
boundary, and the strategic uncertainties. Derive `innovation challenge` from the Charter's
**Challenge**, `research boundary` from **Scope + Constraints**, and `strategic uncertainties` from
**Unknown + Tensions** (per the charter-template mapping; the Charter does not pre-name these). List
the future strategic choices the research may inform
without claiming a strategy decision already exists; the Research Objective orients research toward a decision
edge, it does not assume the decision has been made.

### Orientation and learning coverage

The Learning Plan is the working backlog of this research. Seed it from Charter Unknowns,
starting beliefs, and a broad orientation scan — plus, when a matching Assessment exists, its
`What to Inspect Next` as candidate seed items, never as evidence; treat hypotheses as
prioritization inputs, never as the outer boundary of research. Record, for each open question, its
priority, dependencies, and evidence need. Map the Consumer, Company, Category, and Channel lenses
plus any challenge-specific extended lens that is material here, and keep them as a blind-spot map,
not four tasks. Record accepted gaps and why each is acceptable, including what strategic
consequence the gap may carry. Add newly discovered questions and material lenses as Sprints proceed.

### Sprint Decision — after execution only

Replace a collection-only debrief with a synthesis that records what changed in belief and
understanding:

- **learned** — new evidence-backed findings;
- **contradicted** — prior belief or evidence overturned;
- **belief changed** — which Accepted Belief or candidate belief shifted, and how;
- **reframed** — where the question itself was restructured;
- **deepened** — where confidence or detail increased without changing the frame;
- **dropped** — questions or hypotheses that no longer earn research effort;
- **new questions** — questions this Sprint surfaced;
- **remaining gaps** — material gaps that survive and what each may change.

Then record the Plan Delta (which priorities, agenda items, lens map, boundary, or Method Bundles
changed for the next Sprint) and choose the Sprint Decision from `continue`, `deepen`, `redirect`,
`synthesize`, or `stop`, with a rationale and stop rule based on marginal strategic learning rather
than on a fixed Sprint count. `redirect` is chosen when evidence moves the question to a different
frame. The synthesis is the decision edge for another Sprint; it is not a human Gate.

### Insight Ingredients and Insight Readiness

**Insight Ingredients** are the evidence-backed handoff inputs surfaced by research: patterns,
tensions, anomalies, challenged Accepted Beliefs, reframe candidates, and strategic relevance, each
with its limitations. They are candidates only; Research does not create a final Insight, does not
sign F/P/E/T, does not compose a directional hypothesis, and does not choose a Gate exit.

**Insight Readiness** is a Coordinator judgment that the handoff input is ready for `bw-define`.
Research may move to synthesize only when:

- critical strategic uncertainties are evidenced or retained as explicit material gaps;
- 4C and any challenge-specific extended lens have been checked for strategy-changing blind spots;
- important supporting and disconfirming evidence have both been considered;
- contradictions and plausible alternative explanations remain visible;
- the Sprint Synthesis identifies evidence-backed Insight Ingredients, or explicitly explains why
  no meaningful tension or reframe emerged;
- continuing immediately is unlikely to add enough strategic learning value to justify another
  Sprint, given current access and constraints;
- remaining uncertainty is carried forward with its possible strategic consequence.

Insight Readiness is not a human Gate, not a score, not a fact quota, not a framework quota, and not
permission to sign F/P/E/T. One wave's local missions completing is not, by itself, Insight
Readiness.

Record surviving high-value gaps only in `Research Progress.remaining_gap`, including what each
may change and a future research path when known. A short cross-objective gap summary may travel
with Insight Ingredients into `bw-define`; it does not own or duplicate the underlying state.

## Stable versus transient state

Only durable, validity-relevant content is persisted in the living research artifact. Transient
execution detail stays out of the artifact.

**Stable — persist:**

- Research Objective;
- Learning Plan;
- Next Sprint research design;
- Research Progress;
- exact Knowledge references;
- meaningful method limitations (only when they affect what the evidence can support or explain a
  fallback);
- Sprint Decision and its next-plan delta;
- Insight Ingredients;
- Research Progress remaining gaps.

**Transient — do not persist:**

- scratch issue trees and alternative decompositions;
- queries attempted, except when needed to explain a material gap;
- routine connector selection;
- worker count and topology;
- intermediate Research Packets after normalized fan-in;
- unused Toolkit candidates;
- framework selection deliberation;
- duplicate source material already normalized into evidence.

## Research Mission contract

Each selected mission carries enough information to schedule and evaluate it:

| Field | Meaning |
|---|---|
| mission objective | Decision-relevant outcome |
| decision relevance | What judgment this can change |
| questions | Learning questions this mission answers |
| evidence need | Evidence required before method selection |
| source scope | Where the mission may look |
| exclusions | What the mission must not cover |
| dependencies | Missions this mission depends on |
| parallelizable | Whether independent execution is possible |
| priority | Relative importance among missions |
| search budget | Bounded calls/time/coverage |
| stop condition | Evidence or diminishing-return threshold |
| expected output | Research Packet |
| limitation | What this mission cannot establish |

`parallelizable: true` is necessary but not sufficient: missions sharing a dependency, dense
context, or substantially overlapping source space remain sequential or are merged by the
Coordinator.

## Execution selection

The Coordinator chooses the internal execution strategy automatically, without asking the user for
a research mode or worker count. Execution is automatic and internal:

| Condition | Internal execution |
|---|---|
| One bounded question or dense shared context | One researcher; sequential refinement |
| Independent queries inside one mission | Query-level parallelism |
| 2-4 missions with distinct questions and source spaces | Mission-level parallelism |
| One mission depends on another | Dependency-ordered waves |
| High-risk synthesis or conflicting evidence | Add a contradiction/citation verification pass |
| Concurrency unavailable | Sequential fallback |

Two-to-four workers is a per-wave concurrency limit, not a research-scope limit. Build
dependency-ordered waves, mark independent missions eligible for bounded parallel execution, and
fall back to sequential execution whenever worker concurrency is unavailable.

## Research Packet

Workers return a structured, uncommitted packet instead of a narrative report. Packets are
transient coordination payloads — not BeWater artifacts, evidence files, or ledger records. Each
packet carries its mission ID plus findings, contradictions, unanswered questions,
queries attempted, and stop reason. Each finding is an atomic claim with a source reference,
source title, source date, source location, source family, independence key, evidence form,
support, and limitation.

## Evidence fan-in

The Coordinator — the single writer — normalizes every Research Packet from the current dependency
wave, then deduplicates findings by underlying origin rather than page count, resolves citation
locations, checks claim-to-source support, searches for disconfirming evidence where important
claims remain one-sided, and preserves contradictions and alternative explanations. Workers are
read-only: they never write project state, never allocate evidence or artifact IDs, and never
commit; one Coordinator commit writes all state. Duplicate findings are merged without losing
limitations.

## Fan-in quality audit

Before any state write, the Coordinator checks:

1. every persisted claim is decision-relevant and an atomic claim;
2. every claim resolves to an exact source reference and, when available, a source location;
3. repeated pages from one report, study, or dataset count as one independent source family;
4. source authority, recency, directness, and known bias fit the claim being made;
5. supporting and disconfirming evidence are both preserved;
6. contradictions are visible and are not resolved by silently selecting the favorable source;
7. inference does not exceed what the evidence form can establish;
8. duplicate findings are merged without losing limitations;
9. high-priority gaps and unanswered questions remain explicit;
10. the Sprint stop reason follows its stop condition or a documented budget constraint.

The audit repairs the uncommitted synthesis when possible. It creates
no artifact, review state, signoff, score, or gate, and adds no checklist result or user approval
step. It does not block Research on missing interviews.

## Plan self-review

Run one in-context self-review after drafting or changing the Research Objective, Learning Plan,
Next Sprint research design, or Research Progress, and before persistence or execution. Use the
same four checks as the brainstorming self-review, adapted to research:

1. **Placeholder scan** — remove temporary or incomplete placeholders, incomplete required
   sections, and vague mission fields.
2. **Internal consistency** — align the mission and decision with formal inputs, risk priorities,
   4C coverage, evidence need, method, expected output, limitation, and stop condition.
3. **Scope check** — keep the next Sprint bounded and compatible with available time, authority,
   access, owner, and dependency; do not turn Discover into a fixed research programme.
4. **Ambiguity check** — make the evidence need, expected output, limitation, owner/dependency, and
   stop condition unambiguous. Define evidence need before method, and never call an analysis
   framework evidence.

Also confirm that an Initial Assessment, self-report, or model inference remains a candidate rather
than a Fact. Automatically repair a problem when the current context resolves it. Explicit Unknowns
are valid when the Plan names a research path. If an unresolved ambiguity would change the mission,
decision, priority, scope, authority, or resource commitment, ask one question and stop before
writing or executing; do not persist or execute. The review creates no artifact, review state,
signoff, or human gate.

Research is flow, not waterfall. Research over public sources and supplied context may be sufficient
for Discover, but its limitations and unresolved validation needs remain visible. Do not wait for
every possible fact; do not hide an evidence gap by calling it resolved. The toolkit is a seed
library, not a whitelist: an ad-hoc method records why selected, what it cannot prove, and is not
automatically promoted.
