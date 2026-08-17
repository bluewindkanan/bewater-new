---
name: bw-insight-craft
description: Use when the user wants to turn research into insights or judge insight candidates against F/P/E/T.
---

# bw-insight-craft

A **Define capability** that turns research into insights and judges them. You produce insight
candidates and stop before human F/P/E/T signoff.

You consume **Insight Ingredients** from `bw-discovery-research` (evidence-backed Facts, candidate
and Accepted Beliefs, patterns, tensions, anomalies, challenged Accepted Beliefs, reframe
candidates, strategic relevance, limitations, and unresolved gaps) and **own insight generation** —
the creative and evaluative transformation of those ingredients into Insight candidates. Research
supplies the evidence and synthesis ingredients; it does not pre-approve Insights. Research labels
such as reframe candidate or tension are ingredients, **not pre-approved Insights**. You retain
individual **F/P/E/T** assessment and the human signature on every insight. You do not create
directional hypotheses; they stay in Define.

## Workflow

1. Confirm the selected branch has `current_stage: define`. If not, route to `bw-resume`
   (the global recovery router will read the actual stage and route correctly).
2. Walk the cognitive ladder (`references/insight-generation.md`): Facts → Accepted Beliefs →
   Insights. Accepted Beliefs are the target insights challenge; explanatory hypotheses may support
   interpretation but are not directional-hypothesis artifacts.
3. Generate candidates with the 13 lenses and the Pearl/Code/Force methods.
4. Judge each candidate against F/P/E/T (`references/fpet-judgment.md`); reclassify a failing
   candidate as a Fact only when it is directly observed, otherwise retain it as a candidate belief
   or explanatory hypothesis.
5. Write insight artifacts (`_bewater-output/artifacts/ART-xxx-rN-insights.md`, `kind: insights`,
   `stage: define`).
6. Present all insight candidates in the artifact body with their number, statement, evidence,
   and your F/P/E/T assessment. Then ask the human, in one question, which insight numbers to
   sign (e.g., "1,3,4"). Every candidate must remain selectable: use the host's structured
   question only while all candidates fit inside its option limit; when candidates outnumber
   that limit, ask in plain text — the numbered list already shown is the option list — and
   accept the free-form number list as the answer. A host tool's option cap must never
   silently drop or hide a candidate from the signoff decision. Record signoff for each
   selected insight.
   Name the human decision authority and **stop**. Current-revision human F/P/E/T signoff is a G1 readiness requirement —
   the human signs, not you (`../_bw-shared/gate-criteria.md`). This capability does not create directional hypotheses.
