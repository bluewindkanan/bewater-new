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

1. Walk the cognitive ladder (`references/insight-generation.md`): Facts → Accepted Beliefs →
   Insights. Accepted Beliefs are the target insights challenge; explanatory hypotheses may support
   interpretation but are not directional-hypothesis artifacts.
2. Generate candidates with the 13 lenses and the Pearl/Code/Force methods.
3. Judge each candidate against F/P/E/T (`references/fpet-judgment.md`); reclassify a failing
   candidate as a Fact only when it is directly observed, otherwise retain it as a candidate belief
   or explanatory hypothesis.
4. Write insight artifacts (`_bewater-output/ART-xxx-rN-insights.md`, `kind: insights`,
   `stage: define`).
5. Use `AskUserQuestion` to present each insight candidate with your F/P/E/T judgment and request
   the human's signature. For each insight, show: the insight statement, your F/P/E/T assessment
   (Fresh, Potent, Energizing, Truth — each with yes/no and reasoning), and ask
   the human to sign or reject. Present candidates one at a time or in a small batch; do not
   request signature on all candidates at once without individual review. Name the human decision
   authority and **stop**. Current-revision human F/P/E/T signoff is a G1 readiness requirement —
   the human signs, not you (`../_bw-shared/gate-criteria.md`). This capability does not create directional hypotheses.
