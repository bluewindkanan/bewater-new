---
name: bw-discovery-research
description: Use when the user wants to initialize, run, or iterate BeWater Discover research.
---

# bw-discovery-research

A **capability** for Discover research. It initializes or advances one living `kind: research` artifact,
then stops before insight judgment, strategy choice, or human research decisions. Research is
**ai-executed research** over public sources plus any **user-provided** documents supplied as
**optional context**. Research never waits for missing interviews or internal data; their absence is
recorded as a limitation with a source reference, evidence form, and limitation, not a blocking stage.

Research starts from the Charter's innovation challenge and strategic uncertainties, not from an
already-made strategy decision. **Never claim that a strategy decision already exists;** Research
informs future strategic choices without making one. The capability owns the living research artifact
and the Sprint loop; it does not own Insight generation, strategy formation, or any Gate.

## Workflow

### 1. Entry and current state

1. Read the current Charter revision only as the formal input, including the
   innovation challenge, the research boundary, and the strategic uncertainties. Derive the strategic
   uncertainties and the future strategic choice relevance from these inputs. If either formal input
   is missing or ambiguous, route back to `bw-immersion`; never consume Initial Assessment as
   Evidence, and never invent a Discover Brief. A matching Assessment's `What to Inspect Next` may
   seed candidate Learning Plan items that research must independently source-verify. Research Plan
   `derived_from` contains the exact Charter revision only.
2. Find the branch's current research artifact. If none exists, start revision 1 with
   `references/research-plan.md`; otherwise read its Research Objective, Learning Plan, Research
   Next Sprint research design, Research Progress, Sprint Decision, and remaining gap. Any user-provided documents
   available now are optional context inputs; they become evidence only when a source-bounded claim is
   extracted and recorded. Preserve the same artifact ID, the `supersedes_ref` chain, and the exact
   Charter `derived_from` lineage.

### 2. Orient

3. Run an Orient pass when initializing or when the topic materially changes. Use the 4C coverage
   compass plus any challenge-specific extended lens (`references/4c-framework.md`) to surface blind
   spots, and broaden the Learning Plan beyond the existing starting beliefs when evidence
   warrants. Do not persist a separate Orient artifact; fold orientation into the Research Objective
   and Learning Plan.

### 3. Plan the next Sprint

4. Draft or update the Research Plan before selecting work for the next Sprint, following
   `references/research-plan.md`. Revision 1 has Research Objective, Learning Plan, Next Sprint,
   and Research Progress. Select the highest-learning-value questions for
   the next Sprint. For each, classify the question first — `question_kind` (`question` or
   `hypothesis`) plus `learning_intent` — then derive the evidence need before method selection, and
   compose the smallest complementary **Method Bundle** using the routing table in
   `references/method-map.md` as a recommended default, not a whitelist and not a menu.
   Load the Toolkit selectively per question, seeded from `references/research-toolkit.csv`; it is a
   seed library and is never injected wholesale. You may override any recommended method or framework
   with one the model knows fits better, recording why selected, what it cannot prove, and its
   limitation. Select the
   smallest complementary set, reject redundant frameworks that reuse the same evidence to make the
   same inference, and do not require exactly one method from every layer. Use the host's native
   tools (web search, browser, file read, subagents) directly; no tool registry is consulted and no
   connector name is hardcoded.
5. Run the in-context self-review (`references/research-plan.md`) after every Plan draft or
   revision and before either persistence or execution. Repair issues the current context resolves
   inline; the review creates no artifact, review state, signoff, or human Gate. If a material
   ambiguity would change the mission, decision, priority, scope, authority, or resource commitment,
   ask one question and stop; do not persist or execute.
6. When the Plan is new or materially changed, persist a reviewed research revision after the
   self-review passes and before execution using `references/persistence-plan.md`. Research Planning
   may project zero qualifying root assumptions. Project only beliefs whose failure could materially
   change direction, that are uncertain, and that name an observable disconfirming signal; follow
   `references/root-assumption-projection.md`. A projected root derives from the exact Research Plan
   revision that introduced it; assumption refs never enter Plan lineage. `impact=high` and
   `uncertainty=high` immediately open the existing durable L4 obligation.

### 4. Execute, synthesize, and re-plan

7. Execute only the reviewed research missions available within the user's authority and the current
   environment. Execution is automatic and internal — never ask the user for a research mode or worker
   count. Offline field research (live interviews, field observation, usability with real users) is
   out-of-band human work: never auto-execute it and never report it as AI-executed evidence; consume
   user-provided documents as optional context and record the absence as a limitation. Build mission
   dependencies, merge overlapping missions, mark independent missions eligible
   for bounded parallel execution, and choose sequential, query-level parallelism, mission-level
   parallelism, or dependency-ordered waves; use at most 2-4 workers and use sequential fallback
   whenever worker concurrency is unavailable. Treat 2-4 workers as a per-wave concurrency limit,
   never a total mission or topic limit; it is not a research-scope limit.
8. Workers are read-only: they never write project state, never allocate evidence or artifact IDs, and
   never commit. Each worker receives the formal snapshot, relevant optional context, one bounded
   mission, source and exclusion boundaries, budget, stop condition, and the Research Packet output
   contract. Fan in every Research Packet from the current dependency wave as the single writer:
   normalize packets, deduplicate findings by underlying origin rather than page count, check
   claim-to-source support and source locations, search for disconfirming evidence where important
   claims remain one-sided, preserve contradictions and alternative explanations, and apply the fan-in
   quality audit. The Coordinator first writes or CAS-revises one stable file per K-NNN, then appends
   the Research revision whose Research Progress pins exact `knowledge:K-NNN@n` refs. Promote only
   decision-critical atomic claims into Evidence. One Coordinator commit is one validated,
   resumable action through `bwkit plan apply`.
9. After every meaningful Sprint, run the synthesis and record a Sprint Decision. Record learned, contradicted, belief
   changed, reframed, deepened, dropped, new questions, and remaining gaps; propagate new questions,
   contradictions, belief changes, reframes, and remaining uncertainty into the next Sprint. Then
   choose `continue`, `deepen`, `redirect`, `synthesize`, or `stop` based on marginal strategic
   learning. There is no fixed Sprint count: a narrow, well-evidenced question may reach Insight
   Readiness after one Sprint, while a broad or conflicting topic must continue.

### 5. Insight Readiness and handoff

10. Insight Readiness is a topic-level Coordinator judgment about the handoff input;
    completing one wave's local missions is not, by itself, Insight Readiness. When readiness is met
    (`references/research-plan.md`), surface **Insight Ingredients** — evidence-backed patterns,
    tensions, anomalies, challenged Accepted Beliefs, reframe candidates, strategic relevance, and
    limitations — plus remaining uncertainty to `bw-define` (the Define router will direct to
    `bw-insight-craft`).
11. Do not create a final Insight. Do not sign F/P/E/T. Do not compose a directional hypothesis. Do
    not form a strategy. Do not choose a Gate exit. Initial Assessment content and self-report remain
    candidate beliefs until research supports them.

## Knowledge and persistence contract

Follow `references/knowledge-workpaper.md` and `references/persistence-plan.md`. Research Progress
owns answer status and Knowledge references; `answered` or `partial` requires a complete Knowledge
workpaper. `RM-NNN` identifies activity and never masquerades as Knowledge or Evidence. The current
Research head and its live same-branch K revisions move together. A workpaper's `research_ref`
continues to identify the approved plan revision that authorized the work and is not rewritten to
the newly appended head.

Host tools prepare material under `_bewater-output/sources/`. Before emitting canonical steps,
validate every local path and Source SHA-256 from bytes only. Never parse a binary Source as text,
never emit a Source step, and never write `config-after-sprint*.yaml` or another staged candidate
into project state. New K IDs use `config.next_ids.knowledge`; revisions CAS the same stable path.
Knowledge steps precede the immutable Research revision, optional Evidence and Ledger steps appear
only for decision-critical changes, and config CAS is last so an interrupted action can resume
without reallocating an occupied K ID.
