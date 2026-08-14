# BeWater Discovery Research Insight Sprints — Implementation Plan

**Goal:** Redesign Discover Research as an adaptive, multi-Sprint intelligence loop that starts
from the Charter's innovation challenge and strategic uncertainties, combines a broad but
selectively loaded research toolkit, and hands evidence-backed Insight Ingredients to Define
without making a strategy choice or signing an Insight.

**Architecture:** Keep one living Research artifact and one source-neutral evidence store. The
artifact persists the current Research Frame, Learning Agenda, latest meaningful Sprint delta,
Insight Ingredients, and unresolved gaps. Mission decomposition, queries, worker count, and most
tool-routing details remain transient execution state. A rich layered Toolkit supplies collection,
analysis, validation, and synthesis methods; the Coordinator selects a small complementary Method
Bundle for each learning question. Research iterates through Orient, Explore, Deepen, Redirect, and
Synthesize decisions until Insight Readiness is reached. The next capability, bw-insight-craft,
still owns Insight generation and F/P/E/T judgment. Define and G1 still own strategy formation and
human choice.

## Why this change

Preserve what the current capability already does correctly: one living Discover Plan, 4C as a
coverage compass, evidence need before method selection, marginal-learning debriefs with no fixed
round count, bounded adaptive concurrency, source-family provenance, and single-writer fan-in.

This plan adds only the missing behavior: challenge-specific extended lenses; validation and
synthesis Toolkit layers; a complementary Method Bundle protocol; explicit Insight Ingredients at
the Research-to-Define boundary; a redirect Sprint transition; and an Insight Readiness contract
that prevents local mission completion from being mistaken for topic-level readiness.

The target design preserves the durable parts of professional research practice:

- start from the problem space and future choice territory, not an already-made strategy decision;
- use hypotheses to prioritize research without allowing them to define the whole search space;
- iterate as evidence reveals contradictions, reframes, and new questions;
- choose methods fit for the evidence need and state what they cannot establish;
- distinguish evidence, interpretation, Insight Ingredients, Insights, recommendations, and choices;
- optimize for better Insight inputs and strategic relevance, not mission, source, or framework count.

## Global constraints

- **No strategy decision at Discover entry:** the starting point is the current Charter, active root
  assumptions, innovation challenge, boundaries, and strategic uncertainties.
- **Research is iterative:** support multiple Sprints and meaningful re-planning. Never imply that
  one execution wave completes Discover merely because its local missions stopped.
- **No forced round count:** a narrow, well-evidenced question may reach Insight Readiness after one
  Sprint; a broad or conflicting topic must continue. Sprint is a loop contract, not a quota.
- **Rich library, sparse use:** expand the Toolkit substantially, but load and select only methods
  relevant to the current learning question.
- **Composition over framework accumulation:** more methods are useful only when they add a distinct
  evidence form, perspective, inference, challenge, or synthesis operation.
- **4C is a blind-spot lens:** Consumer, Company, Category, and Channel remain required lenses to
  check, not four tasks, four report chapters, or four workers. Add Technology, Regulation,
  Economics, Ecosystem, or Future when the challenge makes them material.
- **Transient execution detail:** queries, scratch issue trees, worker topology, and routine
  connector choices are not durable artifact content.
- **Validity-relevant transparency:** persist method selection and rationale only when they affect
  what the evidence can support, introduce a material limitation, or explain a fallback.
- **Insight boundary:** Research produces Facts, candidate beliefs, Accepted Beliefs, patterns,
  tensions, contradictions, anomalies, belief shifts, and reframe candidates. It does not create or
  sign an Insight, directional hypothesis, strategy, or Gate exit.
- **Human authority:** humans still sign F/P/E/T and choose Gate exits. Research self-review and
  Sprint re-planning add no human Gate.
- **Evidence integrity:** retain the current source-neutral, claim-level evidence contract,
  source-family deduplication, contradiction preservation, and single-writer commit.
- **English-first:** all authored skill, reference, test token, and eval design content is English.
- **TDD:** write failing structural and behavioral contracts first. Keep measured repository coverage
  at or above 80 percent.
- **Agent collaboration during implementation:** this implementation changes more than three files.
  Use agents with non-overlapping file ownership after the initial RED contract is established.
- **Dirty worktree:** preserve all existing user changes. Do not modify current BeWater project state,
  deleted outputs, Charter work, or unrelated methodology edits.
- **Superpowers policy:** do not invoke any prohibited superpowers skill. The repository permits
  only brainstorming, writing-plans, and verification-before-completion.

## Non-goals

- Producing a generic exhaustive industry report for every Discover project.
- Adding a fixed minimum number of missions, sources, frameworks, or Sprints.
- Building a Python research scheduler, persistent worker queue, or connector registry.
- Exposing worker count or research mode choices to the user.
- Requiring interviews, paid databases, field research, or internal data when unavailable.
- Automatically treating synthetic personas or model inference as primary evidence.
- Moving F/P/E/T judgment, directional hypotheses, strategy formation, or Gate choice into Research.
- Rewriting historical Research revisions or evidence records.
- Replacing the current CAS, project lock, append-only artifact chain, or evidence envelope.

## Target conceptual model

    Charter / Innovation Challenge
                  |
          Strategic Uncertainties
                  |
        Sprint 0: Orient internally
                  |
        Living Learning Agenda
                  |
        +---------------------+
        | Plan next Sprint    |
        | Select questions    |
        | Compose methods     |
        | Execute research    |
        | Synthesize delta    |
        | Challenge beliefs   |
        | Re-plan             |
        +----------+----------+
                   |
          Insight Readiness?
             no ---+--- next Sprint
             yes
              |
       Insight Ingredients
              |
       bw-insight-craft
              |
       Directional Hypothesis
              |
       Strategy Definition
              |
          Human G1 choice

## Stable versus transient state

### Persist in the living Research artifact

1. **Research Frame**
   - current Charter and active-assumption revision snapshot;
   - innovation challenge and research boundary;
   - strategic uncertainties;
   - future strategic choices the research may inform, without implying a choice exists.
2. **Living Learning Agenda**
   - current hypotheses and Accepted Beliefs to challenge;
   - open questions, priority, dependencies, and evidence needs;
   - 4C plus applicable extended-lens blind-spot map;
   - material accepted gaps and why they are acceptable.
3. **Latest meaningful Research Sprint**
   - learning questions selected;
   - validity-relevant Method Bundle and limitations;
   - work actually executed and evidence references;
   - material deviations and tool/access fallbacks.
4. **Sprint Synthesis and Plan Delta**
   - learned, contradicted, reframed, deepened, dropped, and new questions;
   - belief changes and unresolved alternative explanations;
   - next action: continue, deepen, redirect, synthesize, or stop.
5. **Insight Ingredients**
   - evidence-backed patterns, tensions, anomalies, challenged Accepted Beliefs, reframe candidates,
     strategic relevance, and limitations;
   - never final Insights or F/P/E/T judgments.
6. **Remaining uncertainty**
   - high-value gaps;
   - what each gap may change;
   - future research path when one is known.

### Keep transient

- scratch issue trees and alternative decompositions;
- queries attempted except when needed to explain a material gap;
- routine tool/connector selection;
- worker count and topology;
- intermediate worker packets after normalized fan-in;
- unused Toolkit candidates;
- framework scoring or selection deliberation;
- duplicate source material already normalized into evidence.

## Layered Toolkit target

Keep one machine-readable registry plus one compact composition reference.

### Toolkit layers

1. **Collection methods**
   - desk and document research;
   - internal document and data review;
   - company, product, and competitor audit;
   - literature, patent, standards, and regulatory search;
   - behavioral and transaction data review;
   - social, review, and discourse analysis;
   - stakeholder, expert, and consumer interviews;
   - contextual observation, diary, intercept, and survey;
   - usability, demo, experiment, and POC evidence.
2. **Analysis frameworks**
   - market sizing and triangulation;
   - segmentation and decision-unit analysis;
   - competitive benchmarking and positioning;
   - Five Forces;
   - value chain and profit pool;
   - ecosystem and channel mapping;
   - JTBD and journey analysis;
   - pricing and unit economics;
   - trend, weak-signal, and structural-versus-cyclical analysis;
   - technology maturity and capability assessment;
   - scenarios, analogies, and causal models.
3. **Validation and challenge methods**
   - source-family triangulation;
   - negative-case and disconfirming search;
   - contradiction analysis;
   - sensitivity and boundary checks;
   - alternative-explanation testing;
   - evidence-strength and transferability checks.
4. **Synthesis methods**
   - pattern and anomaly detection;
   - Accepted Belief challenge;
   - belief-shift mapping;
   - tension finding;
   - structural reframe generation;
   - cross-lens collision;
   - strategic-relevance mapping.

### Registry schema

Replace the current small typed schema with fields equivalent to:

    id
    layer
    learning_intent
    lens_fit
    use_when
    avoid_when
    evidence_or_output
    complements
    key_limitation
    execution_need

Supported learning intents include explore, describe, compare, explain, size, forecast, validate,
and reframe. The registry remains connector-neutral. The Coordinator resolves execution_need
against tools actually available in the current host.

### Method Bundle selection

For each selected learning question:

1. identify the learning intent and the future strategic choice it may influence;
2. state the evidence or inference required;
3. select the smallest complementary set of collection, analysis, challenge, and synthesis methods;
4. omit any layer that adds no value;
5. reject redundant frameworks using the same evidence to make the same inference;
6. record material limitations and unavailable-access fallbacks;
7. revise the bundle in the next Sprint when evidence changes the question.

The contract must not require exactly one method from every layer. Typical bundles are examples, not
prescriptive recipes.

## Insight Readiness

Research may choose synthesize only when:

- critical strategic uncertainties are evidenced or retained as explicit material gaps;
- 4C and any challenge-specific extended lens have been checked for strategy-changing blind spots;
- important supporting and disconfirming evidence have both been considered;
- contradictions and plausible alternative explanations remain visible;
- the Sprint synthesis identifies evidence-backed Insight Ingredients, or explicitly explains why
  no meaningful tension or reframe emerged;
- continuing immediately is unlikely to produce enough strategic learning value to justify another
  Sprint, given current access and constraints;
- remaining uncertainty is carried forward with its possible strategic consequence.

Insight Readiness is not a human Gate, score, fact quota, framework quota, or permission to sign
F/P/E/T.

## File map

### Authored Research capability

- Modify: src/skills/bw-discovery-research/SKILL.md
- Modify: src/skills/bw-discovery-research/references/4c-framework.md
- Modify: src/skills/bw-discovery-research/references/discover-plan.md
- Modify: src/skills/bw-discovery-research/references/research-toolkit.csv
- Create: src/skills/bw-discovery-research/references/method-bundles.md

### Downstream Insight boundary

- Modify: src/skills/bw-insight-craft/SKILL.md
- Modify: src/skills/bw-insight-craft/references/insight-generation.md

### Structural contracts

- Modify: tests/test_skill_bw_discovery_research.py
- Modify: tests/test_skill_bw_insight_craft.py

### Behavioral evaluations

- Modify: evals/bw-discovery-research/scenarios/online-research.yaml
- Modify: evals/bw-discovery-research/scenarios/iterate.yaml
- Modify: evals/bw-discovery-research/scenarios/parallel-independent.yaml
- Modify: evals/bw-discovery-research/scenarios/dependent-missions.yaml
- Modify: evals/bw-discovery-research/scenarios/self-review-repair.yaml
- Modify: evals/bw-discovery-research/scenarios/self-review-stop.yaml
- Modify: evals/bw-discovery-research/scenarios/supplied-context.yaml
- Create: evals/bw-discovery-research/scenarios/orient-broad-space.yaml
- Create: evals/bw-discovery-research/scenarios/multi-sprint-reframe.yaml
- Create: evals/bw-discovery-research/scenarios/method-bundle-fit.yaml
- Create: evals/bw-discovery-research/scenarios/avoid-framework-soup.yaml
- Create: evals/bw-discovery-research/scenarios/insight-readiness.yaml
- Modify: evals/bw-insight-craft/scenarios/craft.yaml
- Modify: evals/README.md

### Managed deployment

- Regenerate: .claude/skills/bw-discovery-research/
- Regenerate: .claude/skills/bw-insight-craft/

No shared ledger-schema change is expected. Add one only if implementation proves that the existing
source-neutral evidence fields cannot express required provenance; do not speculate a schema change.

---

## Task 1: Write RED contracts for the corrected Research model

**Owner:** primary agent

**Files:**

- Modify tests/test_skill_bw_discovery_research.py
- Modify tests/test_skill_bw_insight_craft.py

### Capture the dirty-worktree baseline

Before the first edit, capture repo-external copies of the current status and the in-scope diff.
Record the temporary audit-directory path in the implementation handoff. At final acceptance,
compare against this baseline so pre-existing user changes are not attributed to this plan.

    BW_RESEARCH_AUDIT_DIR=$(mktemp -d)
    git status --short > "$BW_RESEARCH_AUDIT_DIR/status.before"
    git diff --binary -- src/skills/bw-discovery-research src/skills/bw-insight-craft tests/test_skill_bw_discovery_research.py tests/test_skill_bw_insight_craft.py evals/bw-discovery-research evals/bw-insight-craft evals/README.md > "$BW_RESEARCH_AUDIT_DIR/in-scope.before.patch"

### Research entry assertions

- Require Charter, innovation challenge, research boundary, and strategic uncertainties.
- Require future strategic choice relevance without claiming a strategy decision already exists.
- Forbid wording that makes an existing strategy decision a formal Discover input.
- Preserve exact Charter and active root-assumption lineage.

### Sprint loop assertions

- Require Orient, Living Learning Agenda, Latest Research Sprint, Sprint Synthesis, and Plan Delta.
- Require continue, deepen, redirect, synthesize, and stop transitions.
- Require new questions, contradictions, belief changes, reframes, and remaining uncertainty to
  update the next Sprint.
- Assert that local mission completion is insufficient for Insight Readiness.
- Assert that no fixed Sprint count is required.

### Stable/transient boundary assertions

- Require durable Research Frame, Learning Agenda, evidence refs, meaningful method limitations,
  Sprint delta, Insight Ingredients, and remaining uncertainty.
- Require worker topology, routine connector selection, and unused Toolkit candidates to remain
  transient rather than mandatory artifact fields.

### Toolkit assertions

- Update the exact Markdown reference-set assertion to equal
  {4c-framework.md, discover-plan.md, method-bundles.md}. This is a required RED-test change, not an
  incidental implementation repair.
- Remove the one-to-twenty row cap.
- Replace VALID_TOOLKIT_TYPES with canonical TOOLKIT_LAYERS:
  collection_method, analysis_framework, validation_method, synthesis_method.
- Replace VALID_4CS and the 4c_fit assertion with canonical TOOLKIT_LENSES:
  Consumer, Company, Category, Channel, Technology, Regulation, Economics, Ecosystem, Future.
- Add canonical LEARNING_INTENTS:
  explore, describe, compare, explain, size, forecast, validate, reframe.
- Require the CSV header to replace type with layer and 4c_fit with lens_fit.
- Require coverage for the method families in the Layered Toolkit target.
- Require learning-intent, complementarity, limitation, and execution-need metadata.
- Continue forbidding hardcoded host connector names in the method registry.
- Require the Toolkit to be loaded selectively rather than injected wholesale.

### Method Bundle assertions

- Require evidence need before method selection.
- Require smallest complementary bundle, redundancy rejection, limitation, and fallback behavior.
- Require the skill text to instruct the Coordinator to resolve execution_need against tools
  available in the current host, with no hardcoded connector name. Test the instruction contract;
  do not pretend a structural test proves runtime tool selection.
- Forbid a fixed one-method-per-layer quota.

### Insight boundary assertions

- Require Research to surface Insight Ingredients.
- Define ingredients as patterns, tensions, anomalies, challenged Accepted Beliefs, reframe
  candidates, strategic relevance, and limitations.
- Require bw-insight-craft to consume the ingredients while still owning Insight generation and
  F/P/E/T judgment.
- Forbid Research from authoring an Insight, directional hypothesis, strategy, or Gate choice.

### Run RED

    .venv/bin/python -m pytest tests/test_skill_bw_discovery_research.py tests/test_skill_bw_insight_craft.py -q

Expected: failures only on newly introduced architecture, Toolkit, Sprint, and handoff requirements.

### Commit boundary

    git add tests/test_skill_bw_discovery_research.py tests/test_skill_bw_insight_craft.py
    git commit -m "test(discover): specify insight-driven research sprints"

Do not delegate implementation work until this RED contract is committed.

---

## Task 2: Expand the Toolkit and define composition

**Owner:** research-method agent

**Files:**

- Modify src/skills/bw-discovery-research/references/4c-framework.md
- Modify src/skills/bw-discovery-research/references/research-toolkit.csv
- Create src/skills/bw-discovery-research/references/method-bundles.md

### Lens contract

- Keep Consumer, Company, Category, and Channel as the canonical 4C blind-spot compass.
- Add Technology, Regulation, Economics, Ecosystem, and Future as challenge-specific extended
  lenses in this reference.
- Remove the implication that one C maps to exactly one Research type.
- State that neither a base nor extended lens implies a task, report chapter, method, or worker.
- Keep extended lenses conditional: only material lenses enter the Learning Agenda.

### Registry work

- Migrate to the layered schema.
- Add the collection, analysis, validation, and synthesis method families listed above.
- Keep descriptions compact and decision-relevant.
- For every method, state when to use it, when not to use it, its output, complementary methods,
  limitation, and execution need.
- Avoid duplicated aliases that do not change method behavior.
- Do not encode a preferred consulting firm, commercial vendor, or host connector.

### Composition work

Define the selection sequence:

    learning question
      -> learning intent
      -> desired evidence or inference
      -> smallest complementary Method Bundle
      -> available execution tools
      -> evidence and limitations
      -> Sprint synthesis

Include non-prescriptive examples for:

- broad industry orientation;
- customer behavior and unmet need;
- competitive and value-chain structure;
- market sizing and economics;
- emerging technology, regulation, and future signals;
- validating whether a cost advantage becomes customer value.

For each example, show why the methods are complementary and which tempting additions would be
redundant.

### Tests

    .venv/bin/python -m pytest tests/test_skill_bw_discovery_research.py -q

Expected: Toolkit schema and coverage tests pass; central workflow tests may remain RED.

---

## Task 3: Redesign the living Discover Plan around adaptive Sprints

**Owner:** research-plan agent

**Files:**

- Modify src/skills/bw-discovery-research/references/discover-plan.md

### Artifact layout

Replace the current plan emphasis with:

1. Current Research Frame.
2. Living Learning Agenda.
3. Latest meaningful Research Sprint.
4. Sprint Synthesis and Plan Delta.
5. Insight Ingredients and Insight Readiness.
6. Remaining uncertainty.

Revision 1 contains a reviewed Research Frame and Learning Agenda. An internal Orient pass may be
part of initialization, but persist it as a separate meaningful delta only when it changes the
agenda, priorities, boundary, or lens map. Do not create ceremonial empty Sprint sections.

### Learning Agenda

- Seed it from Charter questions, root assumptions, advisory candidate beliefs, and a broad
  orientation scan.
- Keep hypotheses as prioritization inputs, not the outer boundary of research.
- Add newly discovered questions and material lenses.
- Record why a gap is accepted and what strategic consequence it may have.

### Sprint Synthesis

Replace a collection-only debrief with:

- learned;
- contradicted;
- belief changed;
- reframed;
- deepened;
- dropped;
- new questions;
- remaining gaps;
- next transition and rationale.

### Insight Readiness

Add the readiness conditions from this plan. Make explicit that readiness is a Coordinator judgment
about the handoff input, not an Insight judgment, score, signoff, or Gate.

### Tests

    .venv/bin/python -m pytest tests/test_skill_bw_discovery_research.py -q

Expected: plan-layout, Sprint-loop, and readiness contracts pass.

---

## Task 4: Integrate the Research Coordinator workflow

**Owner:** primary agent

**Files:**

- Modify src/skills/bw-discovery-research/SKILL.md

### Entry

- Start from current Charter, active root assumptions, optional matching Assessment, current
  Research revision, and user-provided context.
- Derive strategic uncertainties and future choice relevance.
- Never claim that a strategy decision already exists.

### Orient

- Run a lightweight orientation pass when initializing or when the topic materially changes.
- Use 4C plus challenge-relevant extended lenses to discover blind spots.
- Generate a broader Learning Agenda than the existing assumption list when evidence warrants it.
- Avoid persisting a separate Orient artifact.

### Sprint planning

- Select the highest-learning-value questions for the next Sprint.
- Compose Method Bundles using the layered Toolkit.
- Treat two-to-four workers as a per-wave concurrency limit, never a total mission or topic limit.
- Preserve dependency-ordered waves and sequential fallback.

### Execute and synthesize

- Preserve read-only workers, Research Packets, source-family deduplication, contradiction search,
  citation checks, and single-writer fan-in.
- After every meaningful Sprint, synthesize belief changes, tensions, anomalies, reframes, and new
  questions before selecting the next transition.
- Re-plan from marginal strategic learning, not local task completion.

### Handoff

- When Insight Readiness is met, surface the Insight Ingredients and remaining uncertainty to
  bw-insight-craft.
- Do not create final Insights or imply that synthesis equals a strategy choice.

### Tests

    .venv/bin/python -m pytest tests/test_skill_bw_discovery_research.py tests/test_skill_bw_insight_craft.py -q

Expected: all structural contracts pass.

---

## Task 5: Strengthen the Research-to-Insight interface

**Owner:** insight-boundary agent

**Files:**

- Modify src/skills/bw-insight-craft/SKILL.md
- Modify src/skills/bw-insight-craft/references/insight-generation.md

### Input contract

Require Insight Craft to consume:

- evidence-backed Facts;
- candidate and Accepted Beliefs;
- patterns and anomalies;
- tensions and contradictions;
- belief shifts;
- reframe candidates;
- strategic relevance;
- limitations and unresolved gaps.

### Cognitive boundary

Preserve:

    Facts -> Accepted Beliefs -> Insights

Clarify that Research supplies the evidence and synthesis ingredients, while Insight Craft performs
the creative and evaluative transformation into Insight candidates. Research labels such as
reframe candidate or tension must not be treated as pre-approved Insights.

### Human authority

Retain individual F/P/E/T assessment and human signature. Do not move directional hypotheses into
Insight Craft.

### Tests

    .venv/bin/python -m pytest tests/test_skill_bw_insight_craft.py -q

Expected: pass.

---

## Task 6: Add behavioral evaluations that test Research quality

**Owner:** evaluation agent

**Files:** Research and Insight eval manifests listed in the File map.

### Scenario: broad orientation

Prompt with a Charter whose assumptions omit a material regulatory or channel uncertainty.

Require:

- an orientation scan that expands beyond existing assumptions;
- applicable extended-lens discovery;
- a Living Learning Agenda with explicit priorities;
- no exhaustive generic industry report.

### Scenario: multi-Sprint reframe

Sprint 1 should reveal evidence that changes the original question. Sprint 2 must redirect or deepen
around the new tension rather than repeat the original missions.

Require:

- persisted belief change and reframe candidate;
- new question propagation;
- distinct Plan Delta;
- no premature synthesis after Sprint 1.

### Scenario: Method Bundle fit

Use a market-sizing and cost-to-customer-value problem.

Require:

- market data and sizing triangulation;
- competitive or value-chain analysis;
- customer-value validation;
- contradiction or sensitivity check;
- explanation of what public pricing cannot prove.

Forbid JTBD, journey mapping, or other unrelated frameworks unless the prompt creates a real need.

### Scenario: avoid framework soup

Use one narrow, source-bounded verification question.

Require a minimal method choice and direct evidence path. Forbid adding multiple analysis frameworks
that do not change the inference.

### Scenario: Insight Readiness

Provide completed evidence with one unresolved but non-material gap and one important contradiction.

Require:

- contradiction preservation;
- explicit reasoning that the remaining gap does or does not block Insight Craft;
- Insight Ingredients and limitations;
- no final Insight or F/P/E/T judgment.

### Existing scenario updates

- online-research.yaml: keep online research possible without missing interviews becoming a blocker;
  add Research Frame and Learning Agenda expectations.
- supplied-context.yaml: keep supplied documents as optional context and source-bounded evidence;
  add evidence-to-ingredient lineage.
- parallel-independent.yaml and dependent-missions.yaml: preserve bounded per-wave parallelism and
  dependency ordering; forbid treating the worker cap as the total Research scope.
- iterate.yaml: assert belief change, new questions, redirect/deepen behavior, and re-planning rather
  than only marginal-learning vocabulary.
- self-review-repair.yaml: retain in-context repair, but update its target from a generic Plan draft
  to the current Learning Agenda and next Sprint.
- self-review-stop.yaml: retain the material authority/resource ambiguity stop rule and update its
  vocabulary to Method Bundle and next Sprint. Do not delete either self-review scenario.
- evals/README.md: remove stale scripts/verify.py instructions and document that per-skill pytest
  performs manifest structure validation.

### Structural validation

    .venv/bin/python -m pytest tests/test_skill_bw_discovery_research.py tests/test_skill_bw_insight_craft.py -q

Expected: manifests validate and all scenario IDs are unique.

---

## Task 7: Deploy authored skills and run targeted behavioral evaluation

**Owner:** primary agent

### Deploy skills only

    bash install.sh --copy --project-root . --src . --skills-only

Stop if the target is unmanaged. Do not initialize or mutate BeWater project state.

### Check parity

    diff -qr src/skills/bw-discovery-research .claude/skills/bw-discovery-research
    diff -qr src/skills/bw-insight-craft .claude/skills/bw-insight-craft

Expected: no authored/deployed differences except installer-managed markers.

### Codex harness preflight

The fresh-context harness resolves and launches the external codex binary. Before any behavioral
evaluation:

1. confirm the binary resolves;
2. require codex --version to return within a bounded timeout;
3. run one bounded, read-only, ephemeral authentication smoke in a temporary directory;
4. classify a missing binary, timeout, or authentication failure such as HTTP 401 as an external
   eval prerequisite failure, not a Research implementation failure.

If preflight fails, record Task 7 behavioral evaluation as external-blocked, skip the smoke and full
LLM repetitions, and continue deterministic deployment, pytest, coverage, and integrity checks.
The implementation may be reported structurally complete, but full behavioral acceptance remains
pending and the plan must not be declared fully accepted.

### Smoke evaluation after preflight passes

    .venv/bin/python -m evals._harness run --skill bw-discovery-research --mode green --rep 1
    .venv/bin/python -m evals._harness run --skill bw-insight-craft --mode green --rep 1

Review transcripts for:

- expansion beyond initial assumptions when material;
- true multi-Sprint question change;
- relevant Method Bundles rather than framework accumulation;
- clear evidence-to-ingredient lineage;
- no strategy decision or final Insight created by Research;
- one Coordinator write per wave.

Repair the smallest relevant contract or eval assertion before full repetitions.

### Full targeted evaluation

    .venv/bin/python -m evals._harness run --skill bw-discovery-research --mode green
    .venv/bin/python -m evals._harness run --skill bw-insight-craft --mode green

Never hand-edit transcripts to make an eval pass.

---

## Task 8: Full regression and acceptance

**Owner:** primary agent

### Targeted suites

    .venv/bin/python -m pytest tests/test_skill_bw_discovery_research.py tests/test_skill_bw_discover.py tests/test_skill_bw_insight_craft.py tests/test_skill_bw_define.py tests/test_installer_copy.py -q

### Full tests and coverage

    .venv/bin/python -m pytest -q
    .venv/bin/python -m pytest --cov -q

The coverage command reads source = ["bw", "bwkit"] and fail_under = 80 from pyproject.toml.

### Integrity and diff audit

    .venv/bin/python -m bwkit check integrity
    git diff --check -- src/skills/bw-discovery-research src/skills/bw-insight-craft tests/test_skill_bw_discovery_research.py tests/test_skill_bw_insight_craft.py evals/bw-discovery-research evals/bw-insight-craft evals/README.md .claude/skills/bw-discovery-research .claude/skills/bw-insight-craft
    git diff --stat -- src/skills/bw-discovery-research src/skills/bw-insight-craft tests/test_skill_bw_discovery_research.py tests/test_skill_bw_insight_craft.py evals/bw-discovery-research evals/bw-insight-craft evals/README.md .claude/skills/bw-discovery-research .claude/skills/bw-insight-craft
    git status --short -- src/skills/bw-discovery-research src/skills/bw-insight-craft tests/test_skill_bw_discovery_research.py tests/test_skill_bw_insight_craft.py evals/bw-discovery-research evals/bw-insight-craft evals/README.md .claude/skills/bw-discovery-research .claude/skills/bw-insight-craft

Compare the targeted final diff with the repo-external baseline captured in Task 1. Every new
in-scope change must map to this plan; every pre-existing user change must remain preserved. Do not
use full-worktree diff output as the acceptance signal.

## Agent collaboration sequence for implementation

After Task 1 RED is committed:

1. **research-method agent:** Task 2 only.
2. **research-plan agent:** Task 3 only.
3. **insight-boundary agent:** Task 5 only.
4. **primary agent:** Task 4 central workflow, integration, deployment, and final verification.
5. Reuse a completed agent for Task 6 eval manifests after its earlier files are integrated.

Agents must not edit overlapping files. The primary agent reviews every agent diff before integration.

## Acceptance criteria

- Research begins from the Charter's innovation challenge and strategic uncertainties, not an
  already-made strategy decision.
- The living Research artifact supports multiple meaningful Sprints and re-plans when evidence
  changes the question.
- A broad topic cannot synthesize merely because two-to-four local missions completed.
- A narrow topic is not forced through ceremonial extra Sprints.
- Two-to-four workers is clearly a per-wave concurrency limit, not a research-scope limit.
- Hypotheses prioritize work but do not prevent discovery of material unknowns.
- 4C checks blind spots and extended lenses are added when material.
- The Toolkit covers collection, analysis, validation, and synthesis best practices without loading
  the whole library into every Sprint.
- Method Bundles are complementary, fit for the evidence need, limitation-aware, and minimal for the
  question.
- More frameworks are rejected when they do not add evidence, inference, challenge, or synthesis
  value.
- Evidence remains atomic, traceable, source-family-aware, contradiction-preserving, and
  single-writer committed.
- Research hands patterns, tensions, anomalies, belief shifts, and reframe candidates to Insight
  Craft without declaring them final Insights.
- Insight Craft retains F/P/E/T evaluation and human signoff.
- Define retains directional hypotheses and strategy formation.
- Gates retain all human decisions.
- Structural tests, behavioral evals, deployment parity, full pytest, coverage, and integrity checks
  pass.

## Rollback boundary

This change affects authored skill contracts, references, tests, eval manifests/results, and managed
skill copies. It introduces no Python runtime scheduler and no state migration. If behavioral evals
show worse research quality or excessive ceremony, revert the new contract and deployed copies.
Historical Research artifacts and evidence remain readable and untouched.

## Plan self-review

- **Placeholder scan:** no TBD, TODO, empty task, or unspecified owner remains.
- **Internal consistency:** Research starts from strategic uncertainty; Insight and strategy
  boundaries remain downstream throughout.
- **Scope:** limited to Discover Research, Toolkit composition, and the Insight input interface.
- **Adaptability:** durable quality contracts are persisted; model-dependent planning and tool
  orchestration remain transient.
- **Non-redundancy:** no fixed mission, method, source, worker, or Sprint quota is introduced.
- **Testability:** every major design claim has a structural or behavioral verification path.

## Execution order

Execute Tasks 1 through 8 in order. Tasks 2, 3, and 5 may proceed in parallel only after Task 1 RED
is committed. Integrate those results before Task 4 final workflow changes. Run Task 6 after the
authored contracts stabilize, then deploy and verify through Tasks 7 and 8.
