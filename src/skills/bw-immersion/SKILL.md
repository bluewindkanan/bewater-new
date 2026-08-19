---
name: bw-immersion
description: Use when the user wants to initialize a BeWater project, or produce or revise its Immersion Charter and preliminary Assessment.
---

# bw-immersion

An Immersion **capability** and the single project-start entry point. It confirms project state,
produces a context-rich, answer-light Charter, delegates a fresh-context preliminary Assessment,
delivers a compact summary, and stops for the human's next-step decision. It drafts and persists
project definitions; it does not validate the premise, make a Gate decision, or choose whether to
continue.

## Stage contract

The formal Discover input is the selected branch's current Charter revision only — in shorthand,
**Charter alone** is sufficient. The Initial Assessment is advisory: it is current only when it is on
the same branch and its `derived_from` exactly matches the exact typed Charter revision. Missing,
stale, or failed advice does not remove an otherwise complete formal input and does not become a hard
gate. Charter confirmation and Assessment completion do not equal a decision to continue.

## Main flow

Run the five steps in order. Stop whenever a human decision or an incomplete state requires it.

### 1. Confirm / initialize project state

Confirm the selected active branch has `current_stage: immersion`. If project state is missing or
incomplete, report the gap and stop — do not fabricate state. The deployment step (`install.sh`) is
responsible for real state initialization; this capability never writes `_bewater/` state by hand and
never manufactures a missing Charter, Assessment, or branch.

Enforce the **one repository, one project** boundary before interviewing or drafting. Read
`project.name` and the current Charter head. A repository with an existing Charter is already bound:
intent within that project must **resume or revise** the existing Charter and must never allocate a
fresh replacement. If the user presents an unrelated project, report the mismatch, write nothing,
and direct them to a **new repository or working directory**. This is a semantic capability judgment
grounded in the Charter and conversation, never a text-similarity score. Never delete or reset the
existing Charter. Never delete or reset the existing Ledger. Never delete or reset the existing
Conditions. Never delete or reset the existing Evidence. Never delete or reset the existing Artifact.

### 2. Produce the Charter

Turn the user's current intent into a context-rich, answer-light Charter draft, self-review it, and
automatically persist it. This produces a draft, unvalidated project definition; it does not validate
the premise or choose whether to continue.

For the first Charter only, derive a concise project name from the calibrated intent, preserve it in
the candidate config as non-empty `project.name`, and commit that config in the same transactional
plan as the Charter. Later Charter revisions retain the established project binding.

**Adaptive interview.** Read the active branch and current Charter head. Preserve distinctive user
wording. The Charter template defines what you are filling — use it as a guide, never as a
questionnaire. Three principles govern every question; when a principle and a habit conflict, the
principle wins.

- **Earn its place.** Ask only what would materially change a Charter field. A publicly checkable
  fact (tool capability or specs, market price, technology state) or a downstream implementation
  detail is not an interview question: record the user's impression as Believed or leave an explicit
  Unknown, and let Discover investigate it. The user's trigger, situation, current behavior and its
  cost, desire, constraints, boundaries, and success definition are the interview's subject — the
  user's experience of a tool is Charter material; the tool's specifications are not. Capture the
  provisional solution hypothesis at behavior level (who does what differently), never at
  implementation detail.
- **Respect attention.** Start from what the user already gave and smart-skip established context;
  when the opening is thin, first invite one rich account — trigger, person and situation, current
  workaround and its cost, hoped-for change, idea — before probing. Then ask one question at a time:
  the one highest-information-gain question whose answer most changes the draft. Unknown is always a
  valid answer, and the user's fatigue or a request to draft now is a stop signal, not an obstacle.
- **Ground before framing.** The interview runs in two modes with opposite question defaults. In
  **Explore — clarify together**, until the conversation holds grounding anchors for trigger / why
  now, a specific person and situation, current behavior or alternative (or an explicit Unknown),
  and desired change, use free-form questions only, do not use a structured question,
  recommendation, or candidate to supply grounding facts, and label a surfaced insight
  `agent-interpretation` — a frame offered before grounding leads the user. Re-check the anchors
  after each user answer; the moment the last one holds, switch to Converge yourself — an interview
  that stays free-form after grounding is stalled, not thorough. In **Converge — recommend bounded
  decisions**, every genuinely bounded framing, scope, priority, trade-off, or success-signal
  question is asked as a structured choice, never as a free-form question — it is a thinking aid,
  so explain what it optimizes, sacrifices, the credible alternative, and what would change it;
  free-form remains only for a genuinely open matter, flagged as open. It must not recommend the
  user's real behavior, willingness to pay, market facts, or unstated resources.

- Every structured choice includes `Uncertain` and an Other path (`None are accurate — I want to add
  context.`) that opens a free-form input. Prefer the host's structured-question tool so the user
  receives a dialog; if it is unavailable or fails in an interactive host, use a text-choice fallback
  that repeats the candidates plus Uncertain and Other — never candidates alone. In headless runs,
  stop after presenting the question and accept a later scripted answer. When the host supplies Other
  automatically, offer two credible candidates plus `Uncertain` and use the host Other path; do not
  replace either escape route with an AI recommendation.
- Record provenance for every high-impact claim: `user-stated` for the user's own free-form statement,
  `user-selected` for an AI candidate the user chose, `agent-interpretation` for a faithful synthesis,
  and `unknown` for an acknowledged gap. `user-selected` is L1 input but is never silently upgraded to
  `user-stated`, a Fact, or validated evidence.

**Charter draft and self-review.** Coverage is not sufficient while a bounded decision that would
change a Charter field — scope boundary, primary success signal, priority among competing outcomes,
a hard trade-off — is still unresolved: offer it once as a structured choice or record it as an
explicit Unknown, never resolve it silently in the draft. When coverage is sufficient, build the
complete Charter with
`references/charter-template.md` as a project definition: challenge, intent and outcome, scope,
constraints, success definition, Money/Magic framing, and explicit Unknowns. Before any project-state
mutation, run the staged quality loop in `references/self-review-contract.md`. L0 is deterministic
draft validation; L1 is the same-context semantic audit checking claim provenance, frontmatter/body
consistency, scope drift, knowledge-state classification, and coherence. L1 is draft lint, not
independent verification of intent or real-world facts. Revise any L0/L1 issue the existing context
resolves and re-run L0 and L1. Explicit Unknowns do not block drafting. If a material ambiguity could
change the user intent, return to the interview and ask one new highest-information-gain question; do
not invent an answer or persist it as fact. Run final unified intent calibration (L2) before
persistence: show a compact
source-labelled 4–7 claim mirror and ask which point is least accurate. This is an open correction
opportunity, not a signoff, approval, Gate, or decision.

**Persistence.** Once the final L0/L1 loop passes, persist immediately with no user confirmation.
Acquire `bwkit lock` and use CAS to append the Charter r1 or next revision, allocating IDs from
canonical counters. Perform that write only through the transaction in
`references/persistence-plan.md` — the **only allowed project-state mutation path** is
`PYTHONPATH=_bewater python3 -m bwkit plan apply .`. Never use Edit or Write on project state, shell
redirection, a heredoc, or a general-purpose script on `_bewater/` or `_bewater-output/` files. Keep
`document_status: draft` and `validation_status: unvalidated`, capture the committed exact typed
Charter revision, and write no signoff, no assumption-ledger mutation, and no `current_stage` change.

### 3. Produce the Assessment (fresh-context delegation)

After the Charter commit succeeds, produce a preliminary Assessment by **delegating to a fresh-context
sub-agent**. Do not author the Assessment inline in the Charter context.

**Delegation boundary.** When isolated delegation is available, start a fresh-context agent and pass
only:

1. the current branch;
2. the exact typed Charter revision, such as `artifact:ART-001@1`;
3. a pointer to this SKILL.md's Assessment step plus `references/initial-assessment-template.md` and
   `references/write-plan.md`.

Do not pass the interview, the chat transcript, or any prior Assessment body. When isolated
delegation is unavailable, stop and surface that the Assessment could not be produced; do not degrade
to writing the report in the Charter context.

**Fresh-context input boundary.** The sub-agent runs in a fresh context and resolves the exact Charter
revision from current project state before research. It requires one unique Charter head on the same
branch and an exact typed revision. It must not read assumptions, the original interview, the chat
transcript, or any prior Assessment body. Prior Assessment metadata may be inspected only to establish
identity, lineage, revision, and idempotency; do not inherit its judgments. If the inputs are missing,
ambiguous, multi-head, cross-branch, or no longer current, stop and route the Charter gap back to the
Charter flow in step 2 (do not reconstruct intent from conversation history).

**Idempotency and reassessment.** Find an existing `initial-assessment` head for the branch by
metadata: a matching Assessment is on the same branch and its `derived_from` contains exactly one
entry — the exact Charter revision only. If a matching Assessment exists and the user did not request
explicit reassessment, reuse it and do not research or write another revision. A first Assessment
receives a new ART ID from `config.next_ids.artifact`; explicit reassessment or assessment after an
input change reuses the same artifact ID and appends the next revision with `supersedes_ref`. A
Charter revision change makes an older Assessment stale; never edit the old append-only file in place.

**Lightweight external research.** Search for credible public sources — primary research, official
data, regulatory material, and authoritative industry sources — with no fixed count target.
Preserve exact source titles and URLs returned by the research tool; never invent or repair a
citation. Cite sourced statements only as **External signal**; do not create an Evidence wrapper or
change `evidence_level: L1` / `validation_status: untested`. Model knowledge must not be presented
as an external fact; unsourced reasoning is allowed only when labeled **Assessment inference**. If
sources conflict, preserve the conflict and turn it into a risk and Discover question. Source
availability controls the outcome: sufficient credible sources yield the normal report; only 1–2
yield a visibly source-sparse report narrowing every conclusion; zero credible sources, an
unavailable search tool, or a failed search produce no Assessment — preserve the Charter and report
a concrete retry reason.

**Judgment and report contract.** Use `references/initial-assessment-template.md` and target 1–2
screens. The top supports a 60-second read; the remainder supplies traceability. Every key judgment
distinguishes **Charter basis**, **External signal**, **Assessment inference**, **Implication**, and
**What would change this view**. The report may state a clear preliminary judgment; it must not produce
Candidate Insights, a Most Promising Direction, a Discover Mission, or a directional hypothesis, and
must not score the project, apply a readiness label, decide whether to invest, or decide whether the
user should enter Discover. Before any write, perform a **pre-write content audit** on the complete
draft: all five required headings, a compact five-label trace for every key judgment, a
direction-level kill signal in the conclusion, at most three pre-mortem risks each with a
disconfirming signal, an inspect-next checklist whose items are actionable, and an explicit research
boundary with only the sources actually retrieved. This is a deterministic report-contract check, not a second quality-review phase;
the Assessment does not run a brainstorming-style self-review and does not request user confirmation.
After the audit passes, automatically commit.

**Concurrent-safe write.** Use the project-local runtime as `PYTHONPATH=_bewater python3 -m bwkit ...`
and treat `references/write-plan.md` as the complete runtime interface; do not inspect `_bewater/bwkit`
source. Research without holding the lock. Immediately before writing, acquire `bwkit lock`, re-read
the Charter head, and compare branch and exact revision with the captured input; if changed, discard
the uncommitted report, release the lock, capture the new input, and automatically rerun once. If it
changes again before the second write, fail closed, report concurrent modification, and write nothing
stale. When inputs still match, use the single transaction in `references/write-plan.md`, with
`derived_from` pinned to the exact Charter revision only and the artifact counter protected by CAS.
Run the revision-chain integrity check and fail closed on duplicate revisions, missing predecessors,
cycles, or multiple heads. Stop after the integrity check passes, report the committed revision plus
research boundary, and make no further tool call.

**Mutation boundary.** This step writes only the new append-only Assessment revision and the canonical
artifact-ID counter when first allocating its ID. It does not modify the Charter, change assumption
validation, change `current_stage`, or write a signoff. It creates no Evidence wrapper, does not create
Evidence, and does not create or update assumptions. The Assessment is not an input to Research, not an
input to the Knowledge Base, and must not be consumed by Discover as Evidence. Discover may read a
matching Assessment's `What to Inspect Next` only as candidate seed questions for research planning,
each independently source-verified before promotion; `Material Risks` and the Assessment's judgments
stay advisory and do not flow into Research. There is no score and no readiness
label; it creates no Gate record and must not decide whether to invest. The **only allowed
project-state mutation path** is `PYTHONPATH=_bewater python3 -m bwkit plan apply .` with the plan in
`references/write-plan.md`.

### 4. Output the summary (inline, not persisted)

After both the Charter and the Assessment step complete (or the Assessment step fails on zero sources),
deliver one compact summary as inline session output. It is not a new artifact, ArtifactKind, signoff,
or state field. Include:

- **Charter summary:** challenge; intent and outcome; scope; success signal; key Unknowns.
- **Assessment conclusion:** overall preliminary conclusion; top risks; what to inspect next.

If the Assessment failed on zero sources or an unavailable search tool, state the missing Assessment
and preserve its concrete retry reason rather than omitting or manufacturing it. This is the
assessment conclusion handed to the human before the Discover decision; it is advisory and never a
Gate, score, or readiness label.

### 5. Next-step selection

Present a native structured selection for the next action and stop for the human's separate decision.
Never choose the next action, change `current_stage`, or record the decision on the user's behalf. With
a current matching Assessment, offer **Enter Discover**, **Revise Charter**, or **Pause in Immersion**.
With a missing, stale, or failed Assessment, offer **Retry Assessment**, **Continue without
Assessment**, or **Pause in Immersion**. Continuing is available only when the formal Discover input
(Charter alone) is complete. When native structured selection is unavailable or fails in an
interactive host, present equivalent text options and stop; in headless use, stop after presenting the
options for a later scripted response. Automatic Charter and Assessment drafting do not equal a
decision to continue; only a later, separate, explicit user decision may authorize the CAS update from
`current_stage: immersion` to `current_stage: discover`.

## Boundaries

- The Charter is exploration context, not a formal Insight, validation result, Gate, or investment
  conclusion.
- The user's proposed `how` remains a provisional solution hypothesis; Magic is empathy for the
  person's situation and desire, not willingness to pay.
- The Assessment is advisory auxiliary material, not validation, a formal Insight, a Gate, an
  investment decision, or a downstream research input.
- Do not create a Discover Brief, Evidence wrapper, score, readiness label, or additional workflow
  state.
- Do not design research, select methods, create Evidence, or create or update assumptions. Discover
  owns Research Planning and the first selective root-assumption projection.
