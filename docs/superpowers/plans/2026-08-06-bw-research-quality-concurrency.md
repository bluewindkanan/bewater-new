# BeWater Research Quality and Adaptive Concurrency — Implementation Plan

**Goal:** Make Discover Research faster and more reliable by treating Research as one AI-executed
capability, using bounded concurrency only for independent work, and strengthening the evidence
fan-in that feeds Insight Craft. User-provided interviews, internal data, and other offline research
remain optional context inputs; the workflow does not expose primary/secondary research modes.

**Architecture:** `bw-discovery-research` remains one capability and one living Research artifact.
A Research Coordinator turns the reviewed missions into a small dependency graph, selects sequential,
query-parallel, or mission-parallel execution automatically, and gives each read-only worker a bounded
mission contract. Workers return structured Research Packets; they never write project state. The
Coordinator deduplicates sources, checks source independence and contradictory evidence, verifies
claim-to-source support, updates the Discover Plan, and performs the only state commit. If worker
concurrency is unavailable, the same contract falls back to query parallelism or sequential execution
without changing the user-facing workflow or artifact model.

**Implementation surface:** English-first Markdown skill contracts, shared evidence schema, pytest
contract tests, behavioral eval manifests, and managed skill deployment. No new Python scheduler,
runtime service, Research artifact kind, user setting, gate, or primary-research workflow.

## Global Constraints

- **One Research concept:** remove `research_mode`, Primary Trigger, and active primary/secondary
  distinctions. Research means AI-executed research over public sources and supplied context.
- **Optional context, not a blocking stage:** user-provided interview notes, internal documents,
  datasets, and observations are input material. Their absence never pauses Research or creates a
  separate workflow.
- **Adaptive concurrency:** the Coordinator chooses execution strategy from mission independence,
  dependencies, source overlap, complexity, and available tooling. The user does not configure worker
  count or choose a research mode.
- **4C is not a worker topology:** Consumer, Company, Category, and Channel remain a coverage compass.
  Never create four workers merely because there are four lenses.
- **Bounded fan-out:** use one researcher for a simple mission and at most 2–4 workers for independent
  missions. A verifier may be added for high-risk or complex work. Avoid unbounded agent spawning.
- **Read-only workers, single writer:** workers may search, read, and analyze. They never append to
  `_bewater/evidence.yaml`, allocate IDs, write Research revisions, or hold the project lock.
- **Central fan-in:** only the Coordinator normalizes Research Packets, deduplicates source families,
  resolves citation locations, records contradictions and limitations, and commits evidence plus the
  next Research revision.
- **Concurrency improves breadth, not truth:** quality controls remain mandatory whether execution is
  parallel or sequential.
- **No new human gate:** plan self-review and pre-write quality audit are in-context repairs. They create
  no artifact, state, signoff, or user approval step. A material ambiguity still asks one question and
  stops under the existing rule.
- **Backward compatibility:** do not rewrite existing Research artifacts or evidence entries. Historical
  fields may remain readable, but new Discover evidence follows the new source-neutral contract.
- **TDD and coverage:** update contract tests before implementation. Keep the repository test coverage
  at or above 80% and run targeted behavioral evals after structural tests pass.
- **Agent collaboration during implementation:** this plan changes more than three files, so execution
  must use Agent collaboration under the repository policy. Agents must own non-overlapping file sets;
  the primary agent performs the final integration and verification.
- **Dirty worktree:** preserve all existing user changes. Do not touch `_bewater/`, `_bewater-output/`,
  Charter work, or unrelated skill edits.
- **No prohibited Superpowers skills:** repository policy permits only local `brainstorming`; execute
  this plan without invoking any other `superpowers:*` skill.

## Non-Goals

- Designing or distributing surveys, interview links, panels, or participant recruiting.
- Waiting for future interviews or offline studies before Research can finish.
- Building a generic multi-agent runtime or persistent worker queue.
- Exposing `primary`, `secondary`, `online`, `deep`, or worker-count choices in the UI.
- Automatically promoting a Research finding into an Insight, F/P/E/T judgment, hypothesis, or gate exit.
- Replacing the existing Research artifact revision chain, Evidence envelope, CAS, or project lock.

## Target Contract

### Research Mission

Every selected mission carries enough information to schedule and evaluate it:

```yaml
mission:
  id: RM-01
  objective: "Decision-relevant outcome"
  decision_relevance: "What judgment this can change"
  questions: []
  evidence_need: "Evidence required before method selection"
  source_scope: []
  exclusions: []
  dependencies: []
  parallelizable: true
  priority: high
  search_budget: "Bounded calls/time/coverage"
  stop_condition: "Evidence or diminishing-return threshold"
  expected_output: "Research Packet"
  limitation: "What this mission cannot establish"
```

These are artifact-content fields, not a new runtime schema. `parallelizable: true` is necessary but
not sufficient: missions sharing a dependency, dense context, or substantially overlapping source
space remain sequential or are merged by the Coordinator.

### Research Packet

Each worker returns a structured, uncommitted packet instead of a narrative report:

```yaml
research_packet:
  mission_id: RM-01
  findings:
    - claim: "Atomic, decision-relevant statement"
      source_ref: "Exact URL, file reference, or supplied-document identifier"
      source_title: "Exact retrieved title"
      source_date: "Known date or explicit unknown"
      source_location: "Page, section, paragraph, timestamp, or explicit unknown"
      source_family: "Publisher or originating dataset/study"
      independence_key: "Underlying origin used for deduplication"
      evidence_form: "behavior | self-report | expert-judgment | market-data | document"
      support: "Exact observation or concise source-bounded paraphrase"
      limitation: "What this evidence cannot prove"
  contradictions: []
  unanswered_questions: []
  queries_attempted: []
  stop_reason: "Why this worker stopped"
```

Research Packets are transient coordination payloads. They are not BeWater artifacts, evidence files,
or ledger records.

### Execution Selection

| Condition | Internal execution |
|---|---|
| One bounded question or dense shared context | One researcher; sequential refinement |
| Independent queries inside one mission | Query/tool-call parallelism |
| 2–4 missions with distinct questions and source spaces | Bounded mission parallelism |
| One mission depends on another | Dependency-ordered waves |
| High-risk synthesis or conflicting evidence | Add a contradiction/citation verification pass |
| Concurrency unavailable | Sequential fallback using the same packets and quality audit |

### Fan-in Quality Audit

Before any state write, the Coordinator checks:

1. every persisted claim is decision-relevant and atomic;
2. every claim resolves to an exact source reference and, when available, a source location;
3. repeated pages derived from one report, study, or dataset count as one independent source family;
4. source authority, recency, directness, and known bias fit the claim being made;
5. supporting and disconfirming evidence are both preserved;
6. contradictions are visible and are not resolved by silently selecting the favorable source;
7. inference does not exceed what the evidence form can establish;
8. duplicate findings are merged without losing limitations;
9. high-priority gaps and unanswered questions remain explicit;
10. the Sprint stop reason follows its stop condition or a documented budget/tool constraint.

The audit repairs the uncommitted synthesis when possible. It does not create a score, checklist
artifact, reviewer state, or Gate.

## File Map

```text
src/skills/bw-discovery-research/
├── SKILL.md                                      # MODIFY: orchestration, fan-in, single-writer flow
└── references/discover-plan.md                  # MODIFY: mission + packet + quality contract
src/skills/_bw-shared/
└── ledger-schema.md                             # MODIFY: source-neutral atomic evidence fields
tests/
└── test_skill_bw_discovery_research.py          # MODIFY: TDD contract coverage
evals/bw-discovery-research/scenarios/
├── secondary-first.yaml                         # RENAME/MODIFY: online-research.yaml
├── iterate.yaml                                 # MODIFY: unresolved gap, no Primary Trigger
├── parallel-independent.yaml                    # CREATE: mission fan-out/fan-in behavior
├── dependent-missions.yaml                      # CREATE: dependency-ordered fallback
└── supplied-context.yaml                        # CREATE: documents as optional context
.claude/skills/bw-discovery-research/             # REDEPLOY: managed copy from src
.claude/skills/_bw-shared/ledger-schema.md        # REDEPLOY: managed shared contract
```

Existing generated GREEN/RED result JSON and transcripts are evidence of the old manifests. Do not
edit their contents manually. Regenerate targeted GREEN results after the new manifests stabilize;
remove an obsolete generated result only when its scenario ID no longer exists and Git preserves its
history.

---

## Task 1: Write the failing Research contract tests

**Files:**

- Modify: `tests/test_skill_bw_discovery_research.py`

**Purpose:** Establish the intended vocabulary, mission scheduling contract, Research Packet boundary,
quality audit, source-neutral evidence model, and single-writer behavior before changing the skill.

- [ ] **Step 1: Replace the research-mode test**

Replace `test_discovery_research_allows_secondary_only_and_keeps_evidence_provenance` with a test that
requires the active Research contract to contain:

```python
for token in [
    "ai-executed research",
    "user-provided",
    "optional context",
    "never wait",
    "source reference",
    "evidence form",
    "limitation",
]:
    assert token in text

for forbidden in [
    "research_mode",
    "secondary_only",
    "secondary_first",
    "primary trigger",
    "evidence_origin",
    "primary | secondary",
]:
    assert forbidden not in text
```

The wording may be adjusted to match the final contract, but the semantic assertions must remain.

- [ ] **Step 2: Add mission orchestration assertions**

Add a test requiring:

- mission objective and decision relevance;
- source scope and exclusions;
- dependency and `parallelizable` fields;
- bounded 2–4 worker fan-out;
- automatic execution selection rather than a user mode;
- query-level and mission-level parallelism;
- dependency-ordered and concurrency-unavailable fallback;
- explicit statement that 4C does not imply four workers.

- [ ] **Step 3: Add Research Packet and fan-in assertions**

Require the skill/reference corpus to define:

- Research Packets as transient, uncommitted worker outputs;
- atomic claim, source reference/title/date/location, source family, independence key, evidence form,
  support, limitation, contradictions, unanswered questions, queries attempted, and stop reason;
- deduplication by underlying origin rather than page count;
- contradiction search and claim-to-source verification;
- no worker writes, no worker ID allocation, and one Coordinator commit.

- [ ] **Step 4: Add shared evidence schema assertions**

Read `src/skills/_bw-shared/ledger-schema.md` directly and assert that new evidence records use
source-neutral fields such as `source_ref`, `source_location`, `source_family`, `independence_key`,
`claim`, and `limitation`. Assert that the active schema does not require `evidence_origin` and states
that historical entries are not rewritten.

- [ ] **Step 5: Add pre-write quality-audit assertions**

Require the ten fan-in checks from the Target Contract and assert that the audit creates no artifact,
review state, signoff, score, or Gate.

- [ ] **Step 6: Run the targeted test and confirm RED**

```bash
pytest tests/test_skill_bw_discovery_research.py -q
```

Expected: FAIL only on the newly introduced Research quality/concurrency requirements. Existing
well-formedness, living-plan, sprint-loop, and toolkit tests should remain green.

- [ ] **Step 7: Commit the RED tests**

```bash
git add tests/test_skill_bw_discovery_research.py
git commit -m "test(discover): specify research quality and concurrency contract"
```

---

## Task 2: Make the evidence contract source-neutral and quality-preserving

**Files:**

- Modify: `src/skills/_bw-shared/ledger-schema.md`
- Modify: `src/skills/bw-discovery-research/references/discover-plan.md`

**Purpose:** Remove the primary/secondary fork from active methodology while retaining enough
provenance to judge evidence independence and claim support.

- [ ] **Step 1: Rewrite the shared evidence entry contract**

For new Discover evidence, replace the active origin field with:

```text
source_type
source_ref
source_title
source_date
source_location
source_family
independence_key
evidence_form
claim
support
limitation
related_assumptions
```

Keep the existing identity, revision, validity, correction, and summary compatibility fields where
needed. `source_ref` accepts an exact retrieved URL, a user-supplied file reference, or another stable
document identifier. Never invent or repair a URL, title, date, or location; record an explicit unknown.

State the migration rule clearly:

- existing evidence entries remain valid and are not rewritten;
- new entries follow the new source-neutral contract;
- old extra fields may remain present but do not control Research planning or execution.

- [ ] **Step 2: Replace Evidence Strategy in `discover-plan.md`**

Remove research modes and Primary Triggers. Define Evidence Strategy as:

- constraints and decision-relevant evidence targets;
- source scope and desired source-family diversity;
- supplied context available now;
- known source limitations and accepted gaps;
- verification approach and stop conditions.

Explicitly state that missing interview/internal material is an evidence limitation or future research
path, never a reason to block the current AI-executed Research Sprint.

- [ ] **Step 3: Expand Research Mission fields**

Add the Target Contract mission fields. Preserve the rule that evidence need precedes method/tool
selection and that an analysis framework is not evidence.

- [ ] **Step 4: Define Research Packet and Evidence Fan-in sections**

Add compact sections to `discover-plan.md`; do not create a new reference file. Define packets as
transient and define the Coordinator's normalization, deduplication, contradiction preservation,
verification, and quality-audit responsibilities.

- [ ] **Step 5: Run targeted tests**

```bash
pytest tests/test_skill_bw_discovery_research.py -q
```

Expected: schema and plan-layout assertions pass; workflow assertions introduced in Task 1 may remain
RED until Task 3.

- [ ] **Step 6: Commit**

```bash
git add src/skills/_bw-shared/ledger-schema.md \
        src/skills/bw-discovery-research/references/discover-plan.md
git commit -m "feat(discover): make research evidence source-neutral"
```

---

## Task 3: Add adaptive Research orchestration to the capability

**Files:**

- Modify: `src/skills/bw-discovery-research/SKILL.md`

**Purpose:** Convert a list of missions into a portable execution protocol that gains concurrency
where useful without violating BeWater's single-writer state model.

- [ ] **Step 1: Rewrite planning language**

Remove the research-mode selection and Primary Trigger behavior. Make the default input boundary:

1. current Charter revision;
2. complete active root-assumption revision snapshot;
3. current Research revision, when one exists;
4. any user-provided documents available now as optional context.

The first two remain formal lineage inputs. Supplied documents are research inputs and become evidence
only when a source-bounded claim is extracted and recorded.

- [ ] **Step 2: Add an execution-selection step**

After Plan self-review and before execution, instruct the Coordinator to:

1. build mission dependencies;
2. merge overlapping missions;
3. mark independent missions eligible for bounded parallel execution;
4. choose sequential, query-parallel, mission-parallel, or dependency-ordered waves;
5. use no more than 2–4 workers;
6. fall back safely when worker concurrency is unavailable.

This selection is automatic and internal. Do not ask the user to choose an execution mode unless a
material resource/authority ambiguity changes scope under the existing question-and-stop rule.

- [ ] **Step 3: Define the worker boundary**

Each worker receives only the formal snapshot, relevant optional context, one bounded mission,
source/exclusion boundaries, budget, stop condition, and packet output contract. Workers may perform
parallel search/tool calls when supported. Workers must not:

- broaden their mission without returning a new question;
- treat another worker's conclusion as independent evidence;
- write project state or create BeWater artifacts;
- allocate evidence/artifact IDs;
- turn findings into Insights or gate judgments.

- [ ] **Step 4: Define fan-in and verification**

The Coordinator waits for all workers in the current dependency wave, then:

1. normalizes packets;
2. deduplicates findings and underlying source families;
3. checks claim-to-source support and source locations;
4. searches for disconfirming evidence where important claims remain one-sided;
5. preserves unresolved contradictions and alternative explanations;
6. applies the pre-write quality audit;
7. updates the Plan based on marginal learning.

For high-risk or complex synthesis, allow a read-only verifier worker. The Coordinator still owns the
final judgment and write.

- [ ] **Step 5: Make the write boundary explicit**

Research and verification run without holding the project lock. Immediately before persistence, the
Coordinator re-reads the formal input heads, acquires the existing single-writer lock, and commits the
normalized evidence plus next Research revision through the existing safe mutation path. If formal
inputs changed, discard the uncommitted synthesis and follow the repository's bounded rerun/fail-closed
concurrency behavior. Never let workers write concurrently.

- [ ] **Step 6: Preserve downstream boundaries**

Keep candidate Facts, candidate beliefs, and Accepted Beliefs as the only outputs surfaced to
`bw-insight-craft`. Do not create an Insight, sign F/P/E/T, compose a directional hypothesis, or choose
a Gate exit.

- [ ] **Step 7: Run targeted tests and confirm GREEN**

```bash
pytest tests/test_skill_bw_discovery_research.py -q
```

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add src/skills/bw-discovery-research/SKILL.md
git commit -m "feat(discover): orchestrate bounded concurrent research"
```

---

## Task 4: Replace obsolete eval behavior and add concurrency scenarios

**Files:**

- Rename/Modify: `evals/bw-discovery-research/scenarios/secondary-first.yaml` →
  `evals/bw-discovery-research/scenarios/online-research.yaml`
- Modify: `evals/bw-discovery-research/scenarios/iterate.yaml`
- Create: `evals/bw-discovery-research/scenarios/parallel-independent.yaml`
- Create: `evals/bw-discovery-research/scenarios/dependent-missions.yaml`
- Create: `evals/bw-discovery-research/scenarios/supplied-context.yaml`

**Purpose:** Test behavior rather than the mere presence of concurrency vocabulary.

- [ ] **Step 1: Replace the old mode scenario**

Keep scenario ID `BWDRES-S1` to preserve identity, but rename the file and change its assertions:

- Research proceeds using available online sources without asking the user to select a mode;
- unavailable interviews are recorded as a limitation, not a Primary Trigger or blocking task;
- formal inputs and 4C coverage remain intact;
- sources and limitations are preserved;
- no primary/secondary taxonomy appears.

- [ ] **Step 2: Update the iteration scenario**

Replace the Primary Trigger assertion with:

> preserves the unresolved conflict, searches for disconfirming evidence, and records the remaining
> evidence gap plus a future research path without inventing behavioral evidence.

Retain the marginal-learning choice among `continue`, `deepen`, `synthesize`, and `stop`.

- [ ] **Step 3: Add independent-mission concurrency scenario**

Use a prompt containing three clearly independent questions with distinct source spaces. Require the
capability to:

- select bounded mission parallelism;
- issue non-overlapping mission contracts;
- return structured packets;
- fan in and deduplicate results;
- perform one Coordinator write only;
- avoid treating 4C as four mandatory workers.

- [ ] **Step 4: Add dependent-mission scenario**

Use a prompt where market terminology must be established before competitor and user-behavior searches.
Require dependency-ordered waves rather than parallelizing all missions. This guards against
"parallelism at any cost."

- [ ] **Step 5: Add supplied-context scenario**

Provide interview notes and an internal document as fixture inputs alongside public-source questions.
Require the capability to:

- use them as optional context available now;
- preserve their exact document references and evidence form;
- distinguish document contents from model inference;
- continue online Research without creating a separate offline/primary workflow;
- never wait for additional interviews.

- [ ] **Step 6: Validate manifests structurally**

```bash
pytest tests/test_skill_bw_discovery_research.py -q
python scripts/verify.py
```

Expected: PASS. `verify.py` must discover all renamed/new manifests and report no missing RED control or
schema error.

- [ ] **Step 7: Commit**

```bash
git add evals/bw-discovery-research/scenarios tests/test_skill_bw_discovery_research.py
git commit -m "test(discover): cover adaptive research execution and fan-in"
```

---

## Task 5: Deploy the authored contracts and verify parity

**Files:**

- Regenerate: `.claude/skills/bw-discovery-research/`
- Regenerate: `.claude/skills/_bw-shared/ledger-schema.md`

**Purpose:** Keep the deployed managed skill byte-equivalent to the English-first authored source.

- [ ] **Step 1: Deploy skills only**

Use the existing managed installer. Do not initialize or mutate BeWater project state:

```bash
bash install.sh --copy --project-root . --src . --skills-only
```

If the repository's `.claude/skills/` target is not managed, stop instead of overwriting it.

- [ ] **Step 2: Check authored/deployed parity**

```bash
diff -qr src/skills/bw-discovery-research .claude/skills/bw-discovery-research
diff -q src/skills/_bw-shared/ledger-schema.md \
        .claude/skills/_bw-shared/ledger-schema.md
```

Expected: no differences except installer-managed marker files.

- [ ] **Step 3: Run installer regression tests**

```bash
pytest tests/test_installer_copy.py -q
```

Expected: PASS. Copy, link, filtered deployment, managed replacement, and unmanaged collision behavior
remain unchanged.

- [ ] **Step 4: Commit deployed copies if tracked**

```bash
git add .claude/skills/bw-discovery-research \
        .claude/skills/_bw-shared/ledger-schema.md
git commit -m "chore(discover): deploy research quality contracts"
```

If these paths are ignored/generated rather than tracked, do not force-add them.

---

## Task 6: Targeted behavioral evaluation

**Files:**

- Generated by harness: `evals/bw-discovery-research/green/*.json`
- Generated by harness: `evals/bw-discovery-research/green/transcript-*.json`

**Purpose:** Verify that a fresh-context agent applies the execution strategy rather than merely
repeating contract vocabulary.

- [ ] **Step 1: Run one smoke repetition**

```bash
python -m evals._harness run --skill bw-discovery-research --mode green --rep 1
```

Expected: every scenario completes; mechanical checks pass; semantic assertions may be
`needs-review` pending human review.

- [ ] **Step 2: Review the smoke transcripts**

Check specifically that:

- the independent scenario truly fans out non-overlapping missions;
- the dependent scenario does not fan out prematurely;
- supplied documents remain context/evidence inputs rather than a separate stage;
- workers do not write state;
- one Coordinator fan-in and one commit occur;
- citations support the claims attributed to them;
- duplicated source families are not counted as independent evidence.

If behavior is wrong, improve the smallest relevant instruction or eval assertion and rerun the smoke
before proceeding.

- [ ] **Step 3: Run the required repetitions**

```bash
python -m evals._harness run --skill bw-discovery-research --mode green
```

Expected: three repetitions per standard scenario. Fill required human reviewer identity for semantic
checks under the existing eval policy.

- [ ] **Step 4: Preserve or retire old results safely**

Regenerated `BWDRES-S1` and `BWDRES-S2` results replace old behavior evidence. Remove only generated
results whose scenario IDs no longer exist. Never hand-edit transcripts to make them pass.

- [ ] **Step 5: Commit eval evidence**

```bash
git add evals/bw-discovery-research
git commit -m "test(discover): evaluate research orchestration behavior"
```

---

## Task 7: Full regression and acceptance

**Files:** verify-only unless a directly related failure requires repair.

- [ ] **Step 1: Run the Research suite**

```bash
pytest tests/test_skill_bw_discovery_research.py -q
```

- [ ] **Step 2: Run adjacent Discover tests**

```bash
pytest tests/test_skill_bw_discover.py \
       tests/test_skill_bw_insight_craft.py \
       tests/test_installer_copy.py -q
```

This verifies router compatibility, downstream Insight boundaries, and deployment behavior.

- [ ] **Step 3: Run the full suite with coverage**

```bash
pytest -q
pytest --cov=bwkit --cov-fail-under=80 -q
```

Expected: all tests pass and measured runtime coverage remains at least 80%.

- [ ] **Step 4: Run repository integrity verification**

```bash
python scripts/verify.py
python -m bwkit check integrity
```

Expected: skill/eval verification succeeds and the current repository's BeWater state reports
`"ok": true`. These commands are read-only checks; do not repair unrelated dirty state in this task.

- [ ] **Step 5: Audit the final diff**

```bash
git diff --check
git diff --stat
git status --short
```

Confirm that the diff contains only Research methodology, shared evidence schema, Research tests/evals,
and generated managed copies/results intentionally included by this plan. Preserve unrelated user work.

## Acceptance Criteria

- The user sees one Research workflow with no primary/secondary or online/offline mode choice.
- User-provided research material is optional context and never creates a blocking stage.
- A simple or dependency-dense task remains sequential.
- Independent missions can execute with bounded concurrency, with query-level concurrency as a
  lower-cost option and sequential fallback when workers are unavailable.
- Worker outputs follow a common Research Packet contract and do not mutate project state.
- One Coordinator performs source-family deduplication, contradiction handling, citation verification,
  quality audit, Plan update, and the only commit.
- New evidence is atomic, source-neutral, location-aware, limitation-aware, and traceable to an
  underlying independent source family.
- Historical evidence and Research revisions are not rewritten.
- 4C remains a coverage compass and never implies four workers.
- Research still stops before Insight judgment, F/P/E/T signing, directional hypothesis, or Gate choice.
- Targeted structural tests, behavioral evals, adjacent Discover tests, installer tests, full pytest,
  coverage, and integrity verification all pass.

## Rollback Boundary

The implementation consists of contract documents, tests, eval manifests/results, and generated skill
copies. No state migration runs. If the new behavioral evals regress Research execution, revert the
new contract commits and redeploy the previous managed skill; existing `_bewater/evidence.yaml` and
Research artifact revisions remain untouched.

## Design Basis

- Anthropic's multi-agent research architecture supports lead-agent orchestration, bounded specialist
  fan-out, broad-to-narrow search, explicit delegation contracts, and centralized citation handling.
- OpenAI Deep Research supports plan review, source selection, iterative searching, and cited synthesis;
  manager orchestration preserves one owner for the final output.
- Stanford STORM supports perspective-guided question generation and separation of research curation
  from final synthesis.
- DeepResearch Bench separates comprehensiveness, insight, source quality, and citation correctness,
  reinforcing that more searches or citations alone do not establish quality.

These principles are adapted to BeWater's minimal artifact model and single-writer state contract;
they do not introduce a generic agent platform.

## Plan Self-Review

- **Placeholder scan:** no temporary placeholders; every task has explicit files, behavior, commands,
  and expected outcomes.
- **Consistency:** adaptive read-only concurrency and centralized single-writer persistence are used
  consistently across the mission, packet, evidence, eval, and acceptance contracts.
- **Scope:** limited to Discover Research quality and execution. Survey tooling, participant research,
  UI controls, generic orchestration infrastructure, and Insight generation are excluded.
- **Ambiguity:** concurrency thresholds, fallback behavior, worker mutation boundary, evidence migration,
  eval handling, and user-visible behavior are explicit.

## Execution Order

Execute Tasks 1–7 in order. Tasks 2 and 4 may be delegated to separate agents only after Task 1's RED
contract is committed because their file ownership is non-overlapping. Task 3 owns the central skill
workflow and should remain with the primary agent. The primary agent integrates, deploys, runs behavioral
evaluation, and performs the final regression audit.
