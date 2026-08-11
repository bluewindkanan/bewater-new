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

1. Read the current Charter revision and the complete active root-assumption revision snapshot, the
   innovation challenge, the research boundary, and the strategic uncertainties. Derive the strategic
   uncertainties and the future strategic choice relevance from these inputs. If either formal input
   is missing or ambiguous, route back to `bw-project-charter`; never invent a Discover Brief.
2. Find the branch's current research artifact. If none exists, start revision 1 with
   `references/discover-plan.md`; otherwise read its Research Frame, Living Learning Agenda, Latest
   Research Sprint, Sprint Synthesis, and remaining uncertainty. Any user-provided documents
   available now are optional context inputs; they become evidence only when a source-bounded claim is
   extracted and recorded. Preserve the same artifact ID, the `supersedes_ref` chain, and the exact
   `derived_from` Charter and active-assumption revisions.

### 2. Orient

3. Run an Orient pass when initializing or when the topic materially changes. Use the 4C coverage
   compass plus any challenge-specific extended lens (`references/4c-framework.md`) to surface blind
   spots, and broaden the Living Learning Agenda beyond the existing assumptions when evidence
   warrants. Do not persist a separate Orient artifact; fold orientation into the Research Frame and
   the Living Learning Agenda.

### 3. Plan the next Sprint

4. Draft or update the Research Frame and Living Learning Agenda before selecting work for the next
   Sprint, following `references/discover-plan.md`. Select the highest-learning-value questions for
   the next Sprint. For each, derive the evidence need before method selection and compose the
   smallest complementary **Method Bundle** from the layered Toolkit (`references/research-toolkit.csv`,
   `references/method-bundles.md`). Load the Toolkit selectively per question; it is a seed library,
   not a whitelist, and is never injected wholesale. Select the smallest complementary set, reject
   redundant frameworks that reuse the same evidence to make the same inference, and do not require
   exactly one method from every layer. The Coordinator resolves each method's `execution_need`
   against tools available in the current host; no method registry hardcodes a connector name.
5. Run the in-context self-review (`references/discover-plan.md`) after every Frame or Agenda draft or
   revision and before either persistence or execution. Repair issues the current context resolves
   inline; the review creates no artifact, review state, signoff, or human Gate. If a material
   ambiguity would change the mission, decision, priority, scope, authority, or resource commitment,
   ask one question and stop; do not persist or execute.
6. When the Frame or Agenda is new or materially changed, persist a reviewed research revision after
   the self-review passes. For a new artifact, this is revision 1 and contains the Research Frame and
   Living Learning Agenda only; do not create empty Sprint sections.

### 4. Execute, synthesize, and re-plan

7. Execute only the reviewed research missions available within the user's authority and the current
   environment. Execution is automatic and internal — never ask the user for a research mode or worker
   count. Build mission dependencies, merge overlapping missions, mark independent missions eligible
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
   quality audit. One Coordinator commit writes the normalized evidence plus the next research
   revision.
9. After every meaningful Sprint, run the Sprint Synthesis. Record learned, contradicted, belief
   changed, reframed, deepened, dropped, new questions, and remaining gaps; propagate new questions,
   contradictions, belief changes, reframes, and remaining uncertainty into the next Sprint. Then
   choose `continue`, `deepen`, `redirect`, `synthesize`, or `stop` based on marginal strategic
   learning. There is no fixed Sprint count: a narrow, well-evidenced question may reach Insight
   Readiness after one Sprint, while a broad or conflicting topic must continue.

### 5. Insight Readiness and handoff

10. Insight Readiness is a topic-level Coordinator judgment about the handoff input;
    completing one wave's local missions is not, by itself, Insight Readiness. When readiness is met
    (`references/discover-plan.md`), surface **Insight Ingredients** — evidence-backed patterns,
    tensions, anomalies, challenged Accepted Beliefs, reframe candidates, strategic relevance, and
    limitations — plus remaining uncertainty to `bw-define` (the Define router will direct to
    `bw-insight-craft`).
11. Do not create a final Insight. Do not sign F/P/E/T. Do not compose a directional hypothesis. Do
    not form a strategy. Do not choose a Gate exit. Initial Assessment content and self-report remain
    candidate beliefs until research supports them.
