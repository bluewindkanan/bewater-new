---
name: bw-investment-narrative
description: Use when the user wants to draft or revise the six-part investment narrative or evidence-linked financial case.
---

# bw-investment-narrative

A **capability** for the investment narrative that G2 decides on. You draft the six-part dual-sided
narrative and sourced financial case, then stop before the human's investment judgment.

## Workflow

1. Compose the six parts — ① Brief ② Opportunity ③ Solution ④ Why big ⑤ Financial Case ⑥ Roadmap —
   per `references/investment-narrative-template.md`, wrapping the solution's three-part definition
   (How it works / How to implement / How it makes money).
2. Build the financial case so **every** assumption cites source + logic: user count, retention,
   pricing, CAC, cost, year-by-year P&L, profitability timing (reference comparable crowdfunding
   counts, industry success rates, etc.). Tie each financial assumption to a ledger assumption with
   `evidence_refs`.
3. Write the narrative artifact (`_bewater-output/ART-xxx-rN-investment-narrative.md`,
   `kind: investment-narrative`, `stage: shape`) via bwkit.
4. Present the narrative + financial case, name the investment-decision authority, and **stop**.
