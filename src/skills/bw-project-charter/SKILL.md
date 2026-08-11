---
name: bw-project-charter
description: Use when the user wants to frame or revise a BeWater project Charter and seed its active root assumptions before Discover.
---

# bw-project-charter

An Immersion **capability** that turns the user's current intent into a context-rich,
answer-light Charter and 3–5 falsifiable root assumptions. It produces draft, unvalidated inputs;
it does not validate the premise, make a Gate decision, or choose whether to continue.

## Adaptive interview

1. Read the active branch and current Charter and ledger heads. Preserve distinctive user wording.
2. Maintain this coverage internally:
   - why now and the triggering event;
   - the specific person, situation, desire, and current behavior;
   - alternatives, workarounds, and their cost;
   - the provisional proposition and hoped-for behavior change;
   - Magic, Money, and leverageable assets;
   - in-scope and out-of-scope boundaries, constraints, and success signals;
   - Known, Believed, Unknown, and Tension.
3. Work in two explicit interaction modes. Ask one question at a time, smart-skip established context,
   and stop when the shared understanding is useful.

   **Explore — clarify together.** Until the conversation has grounding anchors for all of
   trigger / why now, a specific person and situation, current behavior or alternative (or an explicit
   Unknown), and desired change, use free-form questions only. Be a consultant, not an intake form:
   use internal reasoning to offer the one point most worth thinking about, then ask one open question
   about a concrete event, behavior, workaround, constraint, or desired outcome. Keep the visible
   expression clear, focused, and natural; let question complexity determine the necessary context to
   advance shared understanding and the user's next thought. A useful insight may surface an
   implication, tension, ambiguity, assumption, or signal; label it `agent-interpretation`. A rich
   initial prompt can establish some or all anchors and move directly to Converge. Do not use a structured question, recommendation, or candidate framing to supply grounding facts. Do not offer options during Explore.

   **Converge — recommend bounded decisions.** After the grounding anchors are present, use a
   host-native structured choice for a genuinely bounded framing, scope, priority, trade-off,
   balance choice, success signal, or correction. A recommendation is allowed only when it cites
   stated context and explains its material trade-off. It must not recommend a user's real behavior,
   willingness to pay, market fact, or an unstated resource or constraint. Candidates are prompts
   for selection or correction, never evidence. Make the recommendation a thinking aid, not just an
   answer: explain what it **optimizes**, what it **sacrifices**, the **credible alternative**, and
   what unknown or evidence **would change this recommendation**.

   - Every structured choice includes `Uncertain` and an Other path: `None are accurate — I want to
     add context.` Other opens a free-form input. Prefer the host's structured-question tool so the
     user receives a dialog. If native selection is unavailable or fails in an interactive host, use
     a text-choice fallback that repeats the candidates plus Uncertain and Other. Use a fixed
     four-option fallback whenever there are two credible candidates: first candidate, second
     candidate, Uncertain, Other. Never render a fallback with only candidates. In headless runs,
     stop after presenting the question and accept a later scripted answer.
     When the host supplies Other automatically, offer two credible candidates plus `Uncertain` and
     use the host Other path; do not replace either escape route with an AI recommendation.
   - Record provenance for every high-impact claim: `user-stated` for the user's own free-form
     statement, `user-selected` for an AI candidate the user chose, `agent-interpretation` for a
     faithful synthesis, and `unknown` for an acknowledged gap. `user-selected` is L1 input but is
     never silently upgraded to `user-stated`, a Fact, or validated evidence.
4. Stop asking about a field when it is clear, the user explicitly does not know, or Discover should investigate it.
   Unknown is a valid result. If the user shows fatigue or asks for a version now,
   draft with explicit Unknowns rather than forcing template completion.

## Charter draft and self-review

1. When coverage is sufficient, build the complete Charter with `references/charter-template.md`
   and draft 3–5 uncertain, falsifiable `layer: root` assumptions with
   `references/root-assumptions.md`.
2. Before any project-state mutation, run the staged quality loop defined in
   `references/self-review-contract.md`. L0 is deterministic draft validation. L1 is the
   same-context semantic audit: it checks claim provenance, frontmatter/body consistency, scope
   drift, knowledge-state classification, causal-chain coverage (need, value, commercial viability,
   channel, and necessary technical/regulatory conditions), and falsifiability plus observable
   disconfirming signals. L1 is draft lint; it cannot independently verify the user's intent or
   real-world facts.
3. Automatically revise any L0/L1 issue the existing context resolves, then re-run L0 and L1.
   Explicit Unknowns do not block drafting. If a material ambiguity could change the user intent,
   return to the interview and ask one new highest-information-gain question; do not invent an
   answer or persist it as fact.
4. Run final unified intent calibration before persistence. Show a compact, source-labelled 4–7
   claim mirror and ask: `Which point is least accurate, or most needs to be in your own words?`
   This is an open correction opportunity, not a full-document confirmation, signoff, approval,
   Gate, or decision. It consolidates high-impact `user-selected` and `agent-interpretation` claims,
   while preserving `user-stated` and `unknown` claims. Apply any correction and run the final L0/L1
   loop. If the user declines or shows fatigue, preserve unresolved provenance labels and explicit
   Unknowns; do not relabel them as user facts.
5. The quality loop produces no artifact or workflow state. Once the final L0/L1 pass, persist immediately
   with no user confirmation. This is expression drafting, not validation, signoff, or a
   decision to continue.

## Persistence

- Before writing anything, require final unified intent calibration and the final L0/L1 quality loop
  to pass. Do not persist a partial interview or a draft with unresolved material ambiguity. Do not
  ask the user to approve or authorize saving after the review loop.
- After the quality loop, acquire `bwkit lock` and use CAS to append the Charter r1 or next revision
  and persist the 3–5 active root assumptions. Allocate IDs from canonical counters; never overwrite
  an artifact revision or write `_bewater/` state by hand.
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
