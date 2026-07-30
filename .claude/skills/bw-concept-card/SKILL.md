---
name: bw-concept-card
description: Use when the user wants to generate, complete, evaluate, or converge bewater concept cards.
---

# bw-concept-card

A **capability** for concept exploration (bewater-core §9.7). You diverge many concepts,
fill cards, run the 8 criteria + scoring matrix, and present candidates — you stop before
the human's convergence choices (healthy anxiety, altitude, kill/proceed) (spec §4, §8.2).

## Workflow

1. For each opportunity area, brainstorm 10–15 concepts ("how might we" + strong names).
2. Fill the 8-field concept card per `references/concept-card-template.md`; run the 8
   criteria and the Money∩Magic scoring matrix; cut "only interesting" ones.
3. Write concept artifacts (`_bewater-output/ART-xxx-rN-concept.md`, `kind: concept`,
   §5.4) via bwkit (§5.7). Concept revisions are append-only; the integrity check
   (`bwkit check integrity`) validates the chain.
4. Present 2–4 candidates + your scoring, name the human decision authority, and **stop**.
   Healthy anxiety, altitude, and kill/proceed are non-delegable human judgments.
