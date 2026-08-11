---
name: bw-directional-hypothesis
description: Use when the user wants to compose or refine By / We can / Resulting in hypotheses.
---

# bw-directional-hypothesis

A **Define capability** that composes or refines directional hypotheses from current-revision,
human-signed insights. You produce candidates and stop before the human chooses which to close.

## Workflow

1. Confirm the selected branch is in Define and that insights exist. If insights are missing or lack
   current-revision human F/P/E/T signoff, route to `bw-define` (the router will direct to
   `bw-insight-craft`).
2. Collide insights into candidate hypotheses using `references/hypothesis-template.md`
   — each has **By**[means] / **We can**[consumer value = Magic] / **Resulting in**[business
   outcome = Money], each backed by ≥1 insight from each relevant C (no lopsided 4C).
3. Write one hypothesis artifact (`_bewater-output/ART-xxx-rN-directional-hypothesis.md`,
   `kind: directional-hypothesis`, `stage: define`) via bwkit, with `derived_from` pinned to the
   signed insight revisions. The single artifact contains all 2–5 candidates.
4. Present all candidates in the artifact body with their numbers and dual-sided coverage
   (Magic/Money/Tension). Name the human decision authority and **stop**. Closing a hypothesis
   for the remaining Define work is a human choice — the human selects which candidate(s) to close.
