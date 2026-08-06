# Discover Plan

The Discover Plan is the forward-looking planning section of the branch's living `research`
artifact. Revision 1 contains a reviewed Current Discover Plan. A Research Sprint first uses that
snapshot, then writes the next append-only revision of the same artifact ID using `supersedes_ref`.
That next revision carries the updated Current Discover Plan, Latest Research Sprint, and Research
Sprint Debrief. Older revisions preserve history; do not duplicate every prior Sprint in the
current revision.

## Artifact layout

### Current Discover Plan — required sections

1. **Discovery mission and decision** — the core exploration question, provisional proposition,
   research boundary, and the decision this research must inform.
2. **Formal inputs and priorities** — exact Charter and active root-assumption revisions; the
   assumptions, risk priorities, and beliefs to challenge in priority order.
3. **4C coverage map** — the four learning questions, priority, coverage status, and accepted gaps.
   4C is a coverage compass; it never implies four workers.
4. **Evidence strategy** — constraints and decision-relevant evidence targets; source scope and
   desired source-family diversity; any user-provided documents available now as optional context;
   known source limitations and accepted gaps; verification approach and stop conditions. Missing
   interview or internal material is an evidence limitation or a future research path, never a
   reason to block the current ai-executed research Sprint. Each new evidence record is appended as
   an entry in `_bewater/evidence.yaml` under the shared source-neutral contract; each claim
   records its source reference, source location when available, source family, independence key,
   evidence form (behavior, self-report, expert-judgment, market-data, or document), support, and
   limitation.
5. **Research missions** — for each mission: mission objective, decision relevance, questions,
   evidence need, source scope, exclusions, dependencies, `parallelizable`, priority, bounded
   search budget, stop condition, expected output, and limitation. Evidence need precedes
   method/framework selection; an analysis framework is not evidence.

### Latest Research Sprint — after execution only

Record the reviewed mission, work actually executed, evidence references, deviations from the
Plan, and limitations. Revision 1 has no Latest Research Sprint or Research Sprint Debrief section:
omit them rather than adding empty placeholders.

### Research Sprint Debrief and Plan Delta — after execution only

Record **learned**, **unresolved**, **deepen**, **drop**, and **new questions**. Then choose
`continue`, `deepen`, `synthesize`, or `stop` with a reason and stop rule based on marginal
learning. The Research Debrief records the Plan Delta: which priorities, 4C gaps, evidence
strategy, or missions changed for the next Sprint. It is the decision edge for another Sprint, not
a human Gate.

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
a research mode or worker count:

| Condition | Internal execution |
|---|---|
| One bounded question or dense shared context | One researcher; sequential refinement |
| Independent queries inside one mission | Query-level parallelism |
| 2–4 missions with distinct questions and source spaces | Mission-level parallelism |
| One mission depends on another | Dependency-ordered waves |
| High-risk synthesis or conflicting evidence | Add a contradiction/citation verification pass |
| Concurrency unavailable | Sequential fallback |

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

1. every persisted claim is decision-relevant and atomic;
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
no artifact, review state, signoff, score, or Gate, and adds no checklist result or user approval
step. It does not block Research on missing interviews.

## Plan self-review

Run one in-context self-review after drafting or changing the Current Discover Plan and before
persistence or execution. Use the same four checks as the brainstorming self-review, adapted to
research:

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
writing or executing. The self-review itself produces no artifact, state, signoff, checklist result,
or user confirmation.

Research is flow, not waterfall. Research over public sources and supplied context may be sufficient
for Discover, but its limitations and unresolved validation needs remain visible. Do not wait for
every possible fact; do not hide an evidence gap by calling it resolved. The toolkit is a seed
library, not a whitelist: an ad-hoc method records why selected, what it cannot prove, and is not
automatically promoted.
