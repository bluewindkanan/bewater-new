---
name: bw-directional-hypothesis
description: Use when the user wants to compose or refine By / We can / Resulting in hypotheses.
---

# bw-directional-hypothesis

A **Define capability** that composes or refines directional hypotheses from current-revision,
human-signed insights. You produce candidates and stop before the human chooses which to close.

## Workflow

1. Confirm the selected branch is in Define and the source Insight Portfolio carries current-revision
   human F/P/E/T signoff. If either is absent, route back to `bw-insight-craft`.
2. Collide insights into candidate hypotheses using `references/hypothesis-template.md`
   — each has **By**[means] / **We can**[consumer value = Magic] / **Resulting in**[business
   outcome = Money], each backed by ≥1 insight from each relevant C (no lopsided 4C).
3. Write hypothesis artifacts (`_bewater-output/ART-xxx-rN-directional-hypothesis.md`,
   `kind: directional-hypothesis`, `stage: define`) via bwkit, with `derived_from` pinned to the
   signed insight revisions.
4. Present 2–5 candidates, name the human decision authority, and **stop**. Closing a hypothesis
   for the remaining Define work is a human choice.
