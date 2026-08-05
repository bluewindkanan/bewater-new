---
name: bw-project-charter
description: Use when the user wants to frame or revise a BeWater project Charter and seed its active root assumptions before Discover.
---

# bw-project-charter

An Immersion **capability** that turns the user's current intent into a context-rich,
answer-light Charter and 3–5 falsifiable root assumptions. It produces draft, unvalidated inputs;
it does not validate the premise, make a Gate decision, or choose whether to continue.

## Adaptive interview

1. Read the active branch and current Charter and ledger heads. Preserve distinctive user wording;
   a rich initial prompt may already cover most of the intent, so do not force a first free-form
   question.
2. Maintain this coverage checklist internally; do not create an intake artifact or interview state
   machine:
   - why now and the triggering event;
   - the specific person, situation, desire, and current behavior;
   - alternatives, workarounds, and their cost;
   - the provisional proposition and hoped-for behavior change;
   - Magic, Money, and leverageable assets;
   - in-scope and out-of-scope boundaries, constraints, and success signals;
   - Known, Believed, Unknown, and Tension.
3. For the single unanswered item with the highest information gain, select the least-cost input
   mode. Ask one question at a time and smart-skip anything answered by the conversation or current
   confirmed inputs. There is no fixed question limit: stop by coverage and usefulness, not by count.
   - Use free-form input when the answer is open or high-dimensional, or when answer choices would induce
     the user's intent, distort named facts, or conceal an important constraint.
   - Use a host-native structured choice when the context supports 2–3 credible candidates, or for
     a genuine scope, priority, trade-off, correction, or when the user is stuck. Candidates must be
     grounded in the conversation; do not invent facts or present a candidate as evidence.
   - Every structured choice includes “Uncertain” and an Other path: “None are accurate — I want to
     add context.” Other opens a free-form input. A candidate is L1 only after the user selects it
     or supplies it in free-form input.
   - Prefer the host's structured-question tool so the user receives a dialog. If native selection is unavailable
     or fails in an interactive host, use a text-choice fallback that repeats the credible candidates plus Uncertain and Other.
     Use a fixed four-option fallback whenever there are two credible candidates: 1) first candidate, 2) second candidate,
     3) Uncertain, 4) Other: “None are accurate — I want to add context.” Never render a fallback with only candidates.
     There is no substitute for Uncertain and Other: “reply A or B” alone is not a valid fallback. Stop for a reply and do not choose for the user.
     In headless runs, stop after presenting the question and accept a later scripted answer.
4. Stop asking about a field when it is clear, the user explicitly does not know, or Discover should investigate it.
   Unknown is a valid result. If the user shows fatigue or asks for a version now,
   draft with explicit Unknowns rather than forcing template completion.

## Charter draft and self-review

1. When coverage is sufficient, build the complete Charter with `references/charter-template.md`
   and draft 3–5 uncertain, falsifiable `layer: root` assumptions with
   `references/root-assumptions.md`.
2. Before any project-state mutation, run one in-context self-review. Check missing fields,
   internal contradictions, scope drift, ambiguous wording, fidelity to the user's intent,
   fabricated facts or quotations, Magic and Money completeness, the knowledge-state split, and
   root-assumption falsifiability plus disconfirming signals.
3. Automatically revise any issue the existing context resolves. Explicit Unknowns do not block
   drafting. If a material ambiguity could change the user intent, return to the interview and ask
   one new highest-information-gain question; do not invent an answer or persist it as fact.
4. The self-review produces no artifact or workflow state. Once it passes, persist without user confirmation;
   this is expression drafting, not validation, signoff, or a decision to continue.

## Persistence

- Before writing anything, require that the Charter self-review passes. Do not persist a partial
  interview or a draft with unresolved material ambiguity.
- After self-review, acquire `bwkit lock` and use CAS to append the Charter r1 or next revision and
  persist the 3–5 active root assumptions. Allocate IDs from canonical counters; never overwrite an
  artifact revision or write `_bewater/` state by hand.
- Perform that write only through the transaction in `references/persistence-plan.md`. The **only
  allowed project-state mutation path** is `PYTHONPATH=_bewater python3 -m bwkit plan apply .`.
  Never use Edit or Write on project state. Never use shell redirection, a heredoc, or a
  general-purpose script to create or change `_bewater/` or `_bewater-output/` files directly.
- Keep the Charter `document_status: draft` and `validation_status: unvalidated`. Keep user-provided
  assumptions at `evidence_level: L1` and `validation_status: untested`.
- Capture the committed exact typed Charter revision and the exact active root-assumption revision
  snapshot. Do not write a signoff or change `current_stage` as part of automatic drafting.

## Assessment handoff

After the Charter and assumptions commit succeeds, use `bw-initial-assessment` as a separate
capability:

- When isolated delegation is available, start a fresh-context agent and pass only the current branch,
  the exact typed Charter revision, and the exact active root-assumption revision snapshot.
- The delegated agent runs `bw-initial-assessment`. It must not author the Assessment inline or pass
  the interview, chat transcript, or an older Assessment.
- When isolated delegation is unavailable, stop and route to `bw-initial-assessment`. Do not degrade
  to writing the report in the Charter context.

## Later stage transition

Automatic Charter drafting does not equal a decision to continue. Only a later, separate, explicit user
decision may authorize the CAS update from `current_stage: immersion` to `current_stage: discover`.
The Assessment is advisory rather than a hard prerequisite for that explicit transition. A refusal
or deferral leaves the branch in Immersion.

## Boundaries

- The Charter is exploration context, not a formal Insight, validation result, Gate, or investment
  conclusion.
- The user's proposed `how` remains a provisional solution hypothesis.
- Magic is empathy for the person's situation and desire, not willingness to pay.
- Do not create a Discover Brief, Evidence wrapper, score, readiness label, or additional workflow
  state.
