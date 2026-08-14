---
name: bw-opportunity-area
description: Use when the user wants to define or revise 2–4 non-overlapping bewater opportunity areas.
---

# bw-opportunity-area

A **capability** that defines one Opportunity Portfolio revision chain. You propose two to four
non-overlapping areas that can each spawn Concepts, then stop before human confirmation.

## Workflow

1. Use the four organizing tactics in `references/opportunity-areas.md` (consumer archetype /
   business pillar / consumer need / journey stage) to cut 2–4 areas from the locked strategy.
2. Write or revise one opportunity-portfolio artifact
   (`_bewater-output/artifacts/ART-xxx-rN-opportunity.md`, `kind: opportunity`). Store the areas in canonical
   `opportunity_areas[]` with stable, artifact-local `OA-NNN` IDs; never reuse an ID across the
   chain. Flag overlaps. Body headings are only a rendering and never authoritative lineage.
3. Present the portfolio, name the human decision authority, and **stop**. The portfolio
   feeds Ideate; the human confirms the boundaries. G1 counts the 2–4 structured entries in the
   current Portfolio head, not separate Opportunity files.
