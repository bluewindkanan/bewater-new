# Charter Interview: Rules to Principles

**Date:** 2026-08-17

**Supersedes:** the Adaptive-interview section of
`2026-08-04-charter-adaptive-intake-design.md` (interaction architecture, coverage checklist,
mode-gating mechanics, and fallback arithmetic). The Explore → Converge vocabulary, provenance
contract, L0/L1/L2 quality loop, persistence path, and Assessment design of that document remain in
force.

## Motivation

Across several real Immersion runs, two symptoms appeared: the interview ran long, and questions
crossed the Charter boundary — probing a concrete tool's parameters and other details that no
Charter field depends on. The diagnosis is not a missing rule. The Adaptive interview section of
`bw-immersion/SKILL.md` had accreted into a program: an eight-item coverage checklist, a
one-question-at-a-time hard rule, mode gating on grounding anchors, and fallback-option arithmetic.
The skill said HOW in increasing detail and never said WHY or WHAT FOR, so the model optimized
coverage completion rather than question value.

Adding more rules — round budgets, a filter for categories of questions — would further constrain
judgment and still not prevent the next failure mode, which nobody has named yet.

## The dividing line

**Judgment-shaped behavior is specified as principles; completeness and integrity are specified as
rules.** This is now a toolkit-level design principle (`CLAUDE.md`: Principles over rules).

- Principles: what to ask, how to probe, when to stop. Few, testable, each explaining what it
  protects so the model can generalize to unnamed failure modes.
- Rules: state, evidence, and gate integrity — provenance labels, L0/L1/L2, the single persistence
  path, Uncertain/Other escape routes, gate boundaries. These are not judgment calls and stay
  procedural.

## The three principles

The ~50 lines of interview procedure collapse into three principles in `SKILL.md`. Each is
independently testable and none can be satisfied by mechanically completing a checklist:

1. **Earn its place.** Ask only what would materially change a Charter field. A publicly checkable
   fact or a downstream implementation detail is not an interview question: record the user's
   impression as Believed or an explicit Unknown, and let Discover investigate. The user's
   experience of a tool is Charter material; the tool's specifications are not.
2. **Respect attention.** Start from what the user already gave; invite one rich account when the
   opening is thin; then one question at a time — the highest-information-gain one. Unknown is a
   valid answer; fatigue or a request to draft now is a stop signal.
3. **Ground before framing.** No structured question, recommendation, or candidate may supply
   grounding facts (Explore); after grounding, a structured choice is a thinking aid that explains
   its trade-offs (Converge) and never recommends the user's real behavior, willingness to pay, or
   market facts.

Explore / Converge survive as mode names inside principle 3 because eval scenarios and the review
rubric depend on them.

## What stayed as rules

- Provenance (`user-stated` / `user-selected` / `agent-interpretation` / `unknown`; never silently
  upgraded) — unchanged.
- Uncertain/Other escape routes and host-native structured choice preference — kept, with the
  four-option fallback arithmetic removed (candidates + Uncertain + Other is the requirement; the
  count arithmetic was the habit, not the contract).
- L0/L1 self-review, L2 intent calibration, the single `bwkit plan apply` persistence path, and all
  gate/Assessment boundaries — untouched.

## Enforcement

- `tests/test_skill_bw_immersion.py` pins the three principle names plus the public-fact boundary
  phrasing, alongside the existing interview tokens.
- New eval scenario `evals/bw-immersion/scenarios/public-fact-boundary.yaml` (BWCHA-S15) replicates
  the observed failure: the user names a concrete editing tool, and the skill must ask about the
  user's experience of it, not its specifications.
- `evals/bw-immersion/review-rubric.md` folds the relevance criterion (ask only what only the user
  knows) into the Explore dimension and adds the public-fact reject condition.
