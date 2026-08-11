# Adaptive Charter Intake and Automatic Drafting

**Date:** 2026-08-04

## Purpose

Improve the Immersion experience so BeWater first develops a faithful shared understanding with the
user, then reduces effort by recommending bounded decisions. The Charter capability should use an
explicit Explore → Converge interaction, a consultative Explore dialogue, provenance-labelled
interpretation, a staged draft-quality loop, and automatic persistence. The Initial Assessment remains
a separate fresh-context evaluation and automatically persists its report without a user confirmation
or a second self-review phase.

This design borrows the interaction principles of `superpowers:brainstorming`: one question at a
time, open-ended exploration where context is still forming, and choices where a bounded decision
can help the user think and respond with less effort.

## Goals

- Obtain the user's actual intent with the fewest low-value questions.
- Elicit grounding context through useful reflection before using recommendations to converge bounded
  decisions.
- Prefer low-effort structured choices without turning model guesses or user selections into facts.
- Automatically persist a complete, reviewed Charter; do not require a final user confirmation.
- Preserve Assessment isolation and automatic persistence.
- Keep every human-controlled workflow decision explicit; the AI must never choose on the user's
  behalf.
- Preserve append-only artifacts, CAS-protected writes, evidence levels, and stage ownership.

## Non-goals

- Build a BeWater-owned dialog UI or a new persisted interview state machine.
- Add a second, independent reviewer for either artifact.
- Convert Assessment conclusions into validation, Evidence, a Gate result, or a stage decision.
- Change the formal Discover inputs, stage-transition ownership, or the Assessment's advisory
  status.

## Interaction Architecture

### Explore → Converge question selection

The Charter capability maintains its existing coverage checklist in working context only. On every
turn it identifies the unanswered item with the highest information gain, smart-skips information
already established by the user's input, and asks exactly one question.

The capability begins in **Explore**. It must collect, or explicitly mark Unknown, four grounding
anchors: trigger / why now; a specific person and situation; current behavior or alternative; and
desired change. Explore questions are free-form only and seek concrete recent events, observed
behavior, workarounds, constraints, and outcomes. Each reply uses clear, focused, natural language to
surface the one point most worth thinking about and invite the next thought with one open question.
The capability keeps its reasoning internal and lets the question's complexity determine the necessary
context for shared understanding. Any implication, tension, ambiguity, or assumption is labelled
`agent-interpretation`. A rich initial prompt can establish anchors and move directly to Converge.

Only after those anchors are available does the capability enter **Converge**. Converge uses
recommendations to resolve bounded framing, scope, priority, trade-off, Magic–Money balance, success
signals, and corrections. A recommendation must cite stated context and its material trade-off,
explain what it optimizes and sacrifices, name a credible alternative, and state what unknown would
change the recommendation. It may never supply a customer behavior, willingness to pay, market fact,
or unstated resource or constraint. The capability still asks exactly one question per turn.

| Condition | Interaction |
|---|---|
| Explore anchor is missing. | Free-form input; no recommendation or structured choice. |
| Converge has two or three credible, mutually distinguishable candidates grounded in stated context. | Host-native structured-choice dialog, with a stated recommendation basis and trade-off where one is recommended. |
| The next Converge issue is a scope, priority, trade-off, correction, or other bounded decision. | Host-native structured-choice dialog. |
| The user does not know, or Discover should determine the answer. | Offer `Uncertain`; persist the result as an explicit Unknown when appropriate. |
| No candidate accurately represents the user. | Offer `None are accurate — I want to add context`, which opens a free-form response. |
| The coverage and usefulness thresholds are met. | Stop interviewing and draft the Charter. |

Candidate options must be grounded in stated context; they are prompts for correction or selection,
not user facts or evidence. Track each high-impact claim as `user-stated`, `user-selected`,
`agent-interpretation`, or `unknown`. A selection can be L1 user input, but never becomes a
user-stated claim, a Fact, or validation merely because it was selected.

### Structured-choice transport

When the host provides a native structured-question tool (for example, `AskUserQuestion`,
`request_user_input`, or an equivalent), the capability must use it so the user receives a dialog
rather than having to type a letter or option text.

If the tool is unavailable or fails in an interactive host, render the same single question and
options as prose and stop for a reply. The fallback must include `Uncertain` and the free-form
escape hatch when applicable. It must never silently select a recommendation. In headless runs the
capability stops after presenting the question; evaluations supply a later scripted response rather
than simulating a human selection.

## Charter Drafting and Quality Loop

When intent coverage is sufficient, the capability creates the complete Charter and three to five
root assumptions. It then runs a staged quality loop before any project-state mutation:

1. **L0 deterministic validation:** reject missing sections, placeholders, invalid provenance,
   incomplete dual-sided fields, malformed root-assumption records, missing evidence needs or
   disconfirming signals, and any forbidden signoff/state change.
2. **L1 same-context semantic audit:** use the claim trace to check frontmatter/body consistency,
   scope drift, knowledge-state classification, invented quotations, source-labelled fidelity,
   causal-chain coverage (need, value, commercial, channel, technical/regulatory), and whether P0
   Unknowns have a root-assumption or explicit Discover-question exit. L1 is draft lint, not proof
   of user intent or external reality.
3. Revise automatically when existing context resolves the issue, then re-run L0 and L1.
4. Run a final unified intent calibration: show a compact 4–7-row source-labelled intent mirror and
   ask: `Which point is least accurate, or most needs to be in your own words?` Apply any correction
   and re-run L0 and L1. This is an open correction chance, not full-document confirmation, signoff,
   approval, validation, or a Gate.
5. If the user declines calibration or is fatigued, retain the source labels and explicit Unknowns;
   do not recast them as user facts. After the final L0/L1 pass, persist immediately without asking
   for save confirmation.

Explicit Unknowns are valid and do not block drafting. If the L1 audit finds a material ambiguity
that could change the user's intended proposition, the capability returns to adaptive intake and asks
one new highest-information-gain question. It must not fabricate an answer or persist until that
ambiguity is resolved or legitimately classified as Unknown.

No review artifact, review state, or separate reviewer is created. The former complete-draft
confirmation checkpoint is removed: once L0/L1 pass and any required calibration is handled, the
Charter and assumptions are written automatically through the existing lock/CAS transaction. The
committed Charter remains
`document_status: draft` and `validation_status: unvalidated`; root assumptions remain
`evidence_level: L1` and `validation_status: untested`.

## Assessment Handoff and Automatic Persistence

After the Charter transaction succeeds, the caller delegates to `bw-initial-assessment` in a fresh
context, passing only:

- the current branch;
- the exact typed Charter revision; and
- the complete exact active root-assumption revision snapshot.

The Assessment must not read the interview or any earlier Assessment body. It performs its research
and creates its source-bounded report as today, then persists it automatically without a user
confirmation. This design does not add a second self-review phase to Assessment. Its existing
deterministic pre-write report-contract checks (headings, trace labels, sources, word budget, and
lineage) remain write-safety requirements rather than a user-visible quality-review workflow.

Assessment success returns the committed revision and research boundary. Assessment remains advisory
and must not change the stage, validate assumptions, create Evidence, or choose whether to enter
Discover.

If research yields no credible sources or the research tool fails, no Assessment artifact is
created. The caller reports the concrete reason and presents the genuine human next action through
the structured-choice transport: retry Assessment, continue without an Assessment, or remain in
Immersion. A later request to enter Discover, revise the Charter, or pause must likewise be shown as
a human choice by the appropriate router; routers still do not write stage state or select an exit.

## Data and Safety Invariants

- Do not persist interview state, modal choices, a review report, or a new workflow artifact; retain
  the compact claim-level provenance only in the Charter body.
- Continue to use the existing transactional `bwkit plan apply` path for all state mutation.
- Preserve immutable artifact revisions, CAS checks, exact lineage snapshots, and integrity checks.
- Preserve the formal Discover input definition: current Charter plus at least three active root
  assumptions. A matching Assessment remains advisory only.
- Do not treat self-review completion, automatic persistence, or a recommended option as a human
  signoff, validation result, gate exit, or authorization to advance the stage.

## Testing Strategy

Implement test-first and maintain at least 80% coverage for changed executable behavior.

### Structural tests

- Assert the Explore-before-Converge contract, grounding-anchor requirement, one-question limit,
  smart-skip behavior, recommendation provenance, choice escape hatches, structured-tool preference,
  and prose fallback.
- Assert the advisory Explore cadence, inspiration-oriented Converge recommendations, L0 validation,
  L1 semantic-audit contract, final unified L2 intent calibration, automatic repair and rerun
  behavior, removal of the complete-draft and save-confirmation gates, and automatic CAS persistence
  after review.
- Assert that Assessment has no newly introduced self-review or confirmation gate while retaining
  its independent context boundary and pre-write contract checks.
- Reassert all methodology boundaries: draft/unvalidated Charter, L1/untested assumptions, advisory
  Assessment, no AI stage decision, and no direct project-state writes.

### Behavioral evaluations

- Ambiguous intent receives a mirror, a tentative observation, and one free-form, high-information
  Explore question.
- Rich initial context smart-skips redundant questions and may enter Converge directly.
- A grounded scope or priority question invokes the native structured-choice tool only in Converge,
  explaining what each recommended direction optimizes, sacrifices, and could change.
- `Uncertain` becomes an Unknown; the custom escape hatch opens free-form input.
- An unavailable dialog tool produces a prose fallback and waits; it does not auto-select.
- Charter L1 repairs resolvable problems, catches claim/provenance or causal-chain gaps, asks one
  follow-up for material ambiguity, and automatically persists a passing Charter without requesting
  full-document confirmation.
- A successful Assessment automatically persists in a fresh context; an unavailable or source-empty
  Assessment does not write and exposes the three next-action choices.
- Run a live interactive check where a structured-choice tool exists; keep headless evaluations on
  the documented prose/scripted-response path.

## Expected Change Surface

- `src/skills/bw-project-charter/SKILL.md` and, if necessary, its references: adaptive modality,
  self-review, and automatic persistence contracts.
- `src/skills/bw-initial-assessment/SKILL.md`: clarify automatic persistence and preserve the
  distinction between deterministic report validation and a self-review phase.
- Charter and Assessment structural tests and behavioral scenario manifests.
- Installed/deployed skill copies only through the repository's existing installation workflow; no
  manual edits to generated project state.
