---
name: bw-project-charter
description: Use when the user wants to draft or revise a bewater project charter or seed root assumptions.
---

# bw-project-charter

A **capability** that drafts/revises the project charter and seeds root assumptions
(bewater-core §5.0, §9.1). You produce iterable artifacts and stop before any human
signoff or choice (spec §4).

## Workflow

1. Elicit proposition (who/what/how/why), scope, constraints, success criteria.
2. Draft the dual-sided charter using `references/charter-template.md` — the Money+Magic
   four fields plus the tension point (§9.1). Magic ≠ "willingness to pay"; it is empathy
   for the user's situation and desire.
3. Seed the proposition's most uncertain claims as **root-layer** assumptions in the
   ledger, per `references/root-assumptions.md`.
4. Write the charter artifact (append-only `_bewater-output/ART-001-r1-charter.md`,
   §5.4) and update the ledger (§5.7: `bwkit lock` + `cas commit`).
5. Present the charter + seeded assumptions, name the human decision authority
   (product-owner level), and **stop**. Recommend; do not record the human's choice.
