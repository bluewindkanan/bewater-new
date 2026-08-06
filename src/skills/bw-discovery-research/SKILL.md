---
name: bw-discovery-research
description: Use when the user wants to initialize, run, or iterate BeWater Discover research.
---

# bw-discovery-research

A **capability** for Discover research. It initializes or advances one living `kind: research` artifact,
then stops before insight judgment or human research decisions. Research is **ai-executed research**
over public sources plus any **user-provided** documents supplied as **optional context**. Research
never waits for missing interviews or internal data; their absence is recorded as a limitation, not a
blocking stage.

## Workflow

### 1. Inputs and current state

1. Read the current Charter revision and the complete active root-assumption revision snapshot. If
   either formal input is missing or ambiguous, route back to `bw-project-charter`; never invent a
   Discover Brief.
2. Find the branch's current research artifact. If none exists, start revision 1 with
   `references/discover-plan.md`; otherwise read its Current Discover Plan, outstanding evidence
   gaps, Latest Research Sprint, and Research Sprint Debrief. Any user-provided documents available
   now are optional context inputs; they become evidence only when a source-bounded claim is
   extracted and recorded.
3. Map the active questions across Consumer, Company, Category, and Channel using
   `references/4c-framework.md`. 4C is a coverage compass, not a research sequence or fact quota,
   and never implies four workers.

### 2. Plan and self-review

4. Draft or update the Current Discover Plan before selecting work for the next Sprint. The Evidence
   Strategy records decision-relevant evidence targets, source scope and source-family diversity,
   user-provided documents available now, known source limitations, verification approach, and stop
   conditions. Never expose a research mode or ask the user to choose one; research runs over public
   sources and any supplied context.
5. For each next research mission, derive the evidence need before selecting a collection method,
   analysis framework, and available execution tool. A mission records its mission objective,
   decision relevance, questions, source scope, exclusions, dependencies, `parallelizable` flag,
   priority, bounded search budget, stop condition, expected output, and limitation. Consult
   `references/research-toolkit.csv` as a seed library, not a whitelist. An ad-hoc method outside
   the index is allowed only when the Discover Plan records why selected, expected evidence, what it
   cannot prove, key limitation, and execution need. An ad-hoc method is not automatically added to
   the toolkit.
6. Run the in-context Plan self-review in `references/discover-plan.md` after every Plan draft or
   revision and before either persistence or execution. Repair issues that the current context
   resolves inline; the review creates no artifact, review state, signoff, or human Gate. Explicit
   Unknowns remain valid when they have a research path. If a material ambiguity would change the
   mission, decision, priority, scope, authority, or resource commitment, ask one question and stop;
   do not persist or execute.
7. When the Plan is new or materially changed, persist a new append-only research revision after
   the Plan self-review passes. For a new artifact, this is revision 1 and contains the Current
   Discover Plan only; do not create empty Sprint or Debrief sections. Preserve each reviewed Plan
   snapshot before executing it, using the same artifact ID and `supersedes_ref` chain.

### 3. Execute, debrief, and re-plan

8. Execute only the reviewed research missions available within the user's authority and the current
   environment. Select the execution strategy **automatic and internal** — never ask the user for a
   research mode or worker count. Build mission dependencies, merge overlapping missions, mark
   independent missions eligible for bounded parallel execution, and choose sequential, query-level
   parallelism, mission-level parallelism, or dependency-ordered waves; use at most 2-4 workers and
   use sequential fallback whenever worker concurrency is unavailable. Each worker receives the
   formal snapshot, relevant optional context, one bounded mission, source and exclusion boundaries,
   budget, stop condition, and the Research Packet output contract. Workers are read-only: they
   never write project state, never allocate evidence or artifact IDs, and never commit; they may
   search, read, and analyze, and may parallelize search or tool calls within their mission. Workers
   must not broaden their mission without returning a new question, treat another worker's
   conclusion as independent evidence, or turn findings into Insights or gate judgments.
9. Fan in every Research Packet from the current dependency wave as the **single writer**. Normalize
   packets, deduplicate findings by underlying origin rather than page count, check claim-to-source
   support and source locations, search for disconfirming evidence where important claims remain
   one-sided, preserve contradictions and alternative explanations, and apply the fan-in quality
   audit in `references/discover-plan.md`. A read-only verifier worker may check high-risk or complex
   synthesis; the Coordinator still owns the final judgment and write. Research and verification run
   without holding the project lock; immediately before persistence the Coordinator re-reads the
   formal input heads, acquires the existing single-writer lock, and makes one Coordinator commit of
   the normalized evidence plus the next Research revision. If the formal inputs changed, discard the
   uncommitted synthesis and follow the repository's bounded rerun or fail-closed concurrency
   behavior. Never let workers write concurrently.
10. Write the next append-only research revision with the exact Charter and active-assumption
    snapshot in `derived_from`, the Latest Research Sprint, its Research Sprint Debrief, and the
    updated Current Discover Plan. The Debrief records the Plan Delta and chooses `continue`,
    `deepen`, `synthesize`, or `stop` based on marginal learning, not a fixed number of rounds.
    Self-review the updated Plan before this revision is written; a repaired Plan does not need a
    second review pass.
11. Surface only candidate Facts, candidate beliefs, and Accepted Beliefs for `bw-insight-craft`.
    Initial Assessment content and self-report remain candidates until the research supports them. Do
    not create an insight, sign F/P/E/T, compose a directional hypothesis, or choose a gate exit.
