---
name: bw-discovery-research
description: Use when the user wants to initialize, run, or iterate BeWater Discover research.
---

# bw-discovery-research

A **capability** for Discover research. It initializes or advances one living `kind: research` artifact,
then stops before insight judgment or human research decisions.

## Workflow

### 1. Inputs and current state

1. Read the current Charter revision and the complete active root-assumption revision snapshot. If
   either formal input is missing or ambiguous, route back to `bw-project-charter`; never invent a
   Discover Brief.
2. Find the branch's current research artifact. If none exists, start revision 1 with
   `references/discover-plan.md`; otherwise read its Current Discover Plan, outstanding evidence
   gaps, Latest Research Sprint, and Research Sprint Debrief.
3. Map the active questions across Consumer, Company, Category, and Channel using
   `references/4c-framework.md`. 4C is a coverage compass, not a research sequence or fact quota.

### 2. Plan and self-review

4. Draft or update the Current Discover Plan before selecting work for the next Sprint. Select
   `secondary_only`, `secondary_first`, or `mixed` research mode. Primary research is never
   mandatory; record a Primary Trigger when existing evidence cannot answer a high-priority question.
5. For each next research mission, derive the evidence need before selecting a collection method,
   analysis framework, and available execution tool. Consult `references/research-toolkit.csv` as a
   seed library, not a whitelist. An ad-hoc method outside the index is allowed only when the
   Discover Plan records why selected, expected evidence, what it cannot prove, key limitation, and
   execution need. An ad-hoc method is not automatically added to the toolkit.
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
   environment. For each evidence record, preserve `evidence_origin`, `evidence_form`,
   `source_type`, source reference, and limitation, and append it as an entry in
   `_bewater/evidence.yaml` (create the envelope on first write); do not write a standalone evidence
   file. An analysis framework organizes evidence; it never becomes evidence itself.
9. Write the next append-only research revision with the exact Charter and active-assumption snapshot
   in `derived_from`, the Latest Research Sprint, its Research Sprint Debrief, and the updated
   Current Discover Plan. The Debrief records the Plan Delta and chooses `continue`, `deepen`,
   `synthesize`, or `stop` based on marginal learning, not a fixed number of rounds. Self-review the
   updated Plan before this revision is written; a repaired Plan does not need a second review pass.
10. Surface only candidate Facts, candidate beliefs, and Accepted Beliefs for `bw-insight-craft`.
    Initial Assessment content and self-report remain candidates until the research supports them. Do
    not create an insight, sign F/P/E/T, compose a directional hypothesis, or choose a gate exit.
