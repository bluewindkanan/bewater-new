---
name: bw-directional-hypothesis
description: Use when the user wants to compose or refine By / We can / Resulting in hypotheses.
---

# bw-directional-hypothesis

A **capability** that composes/refines directional hypotheses from insights
(bewater-core §9.4). You produce candidates and stop before the human picks which to
close on (spec §4).

## Workflow

1. Collide insights into candidate hypotheses using `references/hypothesis-template.md`
   — each has **By**[means] / **We can**[consumer value = Magic] / **Resulting in**[business
   outcome = Money], each backed by ≥1 insight from each relevant C (no lopsided 4C).
2. Write hypothesis artifacts (`_bewater-output/ART-xxx-rN-hypothesis.md`,
   `kind: hypothesis`, §5.4) via bwkit (§5.7).
3. Present 2–5 candidates, name the human decision authority, and **stop**. Closing a
   hypothesis to feed Define is a human choice.
