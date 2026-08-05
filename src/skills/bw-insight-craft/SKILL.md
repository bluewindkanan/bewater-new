---
name: bw-insight-craft
description: Use when the user wants to turn research into insights or judge insight candidates against F/P/E/T.
---

# bw-insight-craft

A **capability** that turns research into insights and judges them. You produce insight candidates
and stop before human F/P/E/T signoff.

## Workflow

1. Walk the cognitive ladder (`references/insight-generation.md`): Facts → Accepted Beliefs →
   Insights. Accepted Beliefs are the target insights challenge; explanatory hypotheses may support
   interpretation but are not directional-hypothesis artifacts.
2. Generate candidates with the 13 lenses and the Pearl/Code/Force methods.
3. Judge each candidate against F/P/E/T (`references/fpet-judgment.md`); reclassify a failing
   candidate as a Fact only when it is directly observed, otherwise retain it as a candidate belief
   or explanatory hypothesis.
4. Write insight artifacts (`_bewater-output/ART-xxx-rN-insights.md`, `kind: insights`,
   `stage: discover`).
5. Present candidates + your F/P/E/T assessment, name the human decision authority, and
   **stop**. Current-revision human F/P/E/T signoff is a G1 readiness requirement — the
   human signs, not you (`../_bw-shared/gate-criteria.md`). This capability does not create directional hypotheses.
