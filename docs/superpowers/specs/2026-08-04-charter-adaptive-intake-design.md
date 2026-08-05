# Adaptive Charter Intake and Automatic Drafting

**Date:** 2026-08-04

## Purpose

Improve the Immersion experience so BeWater reaches a faithful user intent quickly while reducing
typing effort. The Charter capability should adapt each question to the available context, use a
host-native structured-choice dialog whenever it can safely do so, self-review a completed Charter,
and automatically persist it. The Initial Assessment remains a separate fresh-context evaluation and
automatically persists its report without a user confirmation or a second self-review phase.

This design borrows the interaction principles of `superpowers:brainstorming`: one question at a
time, multiple choice when useful, open-ended input when choices would be misleading, no fixed
question count, and no unnecessary follow-up after the intent is clear.

## Goals

- Obtain the user's actual intent with the fewest low-value questions.
- Prefer low-effort structured choices without turning model guesses into facts.
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

### Question selection

The Charter capability maintains its existing coverage checklist in working context only. On every
turn it identifies the unanswered item with the highest information gain, smart-skips information
already established by the user's input, and asks exactly one question.

The capability then selects an interaction modality based on the information shape rather than a
fixed number of free-form or structured turns.

| Condition | Interaction |
|---|---|
| The intent, experience, named facts, or constraints are open-ended; candidate answers would lead or distort the user. | Free-form input. |
| The current context supports two or three credible, mutually distinguishable candidates. | Host-native structured-choice dialog. |
| The next issue is a scope, priority, trade-off, correction, or other bounded decision. | Host-native structured-choice dialog. |
| The user does not know, or Discover should determine the answer. | Offer `Uncertain`; persist the result as an explicit Unknown when appropriate. |
| No candidate accurately represents the user. | Offer `None are accurate — I want to add context`, which opens a free-form response. |
| The coverage and usefulness thresholds are met. | Stop interviewing and draft the Charter. |

The first interaction is not inherently free-form. A rich initial prompt may already cover most of
the Charter, while an ambiguous first prompt may require an open question. Candidate options must
be grounded in stated context; they are prompts for correction or selection, not user facts or
evidence. Only a user's selection or free-form addition may be recorded as L1 input.

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
root assumptions. It then runs an in-context self-review before any project-state mutation:

1. Scan for placeholders, omitted required sections, contradictions, scope drift, and ambiguous
   language.
2. Verify that original user intent and structured interpretation remain distinct; that quoted
   language is not invented; and that no model-generated candidate is represented as a user fact.
3. Verify Magic, Money, leverageable assets, boundaries, success signals, and
   Known/Believed/Unknown/Tension are coherent and complete enough for the context.
4. Verify each root assumption is `layer: root`, falsifiable, uncertain, linked to an evidence need
   and disconfirming signal, and remains `L1`/`untested`.
5. Revise automatically when the existing context resolves the issue.

Explicit Unknowns are valid and do not block drafting. If the review finds a material ambiguity that
could change the user's intended proposition, the capability returns to adaptive intake and asks one
new highest-information-gain question. It must not fabricate an answer or persist until that
ambiguity is resolved or legitimately classified as Unknown.

No review artifact, review state, or separate reviewer is created. The former complete-draft
confirmation checkpoint is removed: once the self-review passes, the Charter and assumptions are
written automatically through the existing lock/CAS transaction. The committed Charter remains
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

- Do not persist interview state, modal choices, a review report, or a new workflow artifact.
- Continue to use the existing transactional `bwkit plan apply` path for all state mutation.
- Preserve immutable artifact revisions, CAS checks, exact lineage snapshots, and integrity checks.
- Preserve the formal Discover input definition: current Charter plus at least three active root
  assumptions. A matching Assessment remains advisory only.
- Do not treat self-review completion, automatic persistence, or a recommended option as a human
  signoff, validation result, gate exit, or authorization to advance the stage.

## Testing Strategy

Implement test-first and maintain at least 80% coverage for changed executable behavior.

### Structural tests

- Assert the adaptive modality contract, one-question limit, smart-skip behavior, choice escape
  hatches, structured-tool preference, and prose fallback.
- Assert the Charter self-review checklist, automatic repair behavior, removal of the complete-draft
  confirmation gate, and automatic CAS persistence after review.
- Assert that Assessment has no newly introduced self-review or confirmation gate while retaining
  its independent context boundary and pre-write contract checks.
- Reassert all methodology boundaries: draft/unvalidated Charter, L1/untested assumptions, advisory
  Assessment, no AI stage decision, and no direct project-state writes.

### Behavioral evaluations

- Ambiguous intent selects one free-form, high-information question.
- Rich initial context smart-skips redundant questions.
- A grounded scope or priority question invokes the native structured-choice tool.
- `Uncertain` becomes an Unknown; the custom escape hatch opens free-form input.
- An unavailable dialog tool produces a prose fallback and waits; it does not auto-select.
- Charter self-review repairs resolvable problems, asks one follow-up for material ambiguity, and
  automatically persists a passing Charter without requesting confirmation.
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
