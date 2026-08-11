---
name: bw-investment-narrative
description: Use when the user wants to draft or revise the six-part investment narrative or evidence-linked financial case.
---

# bw-investment-narrative

A **capability** for the investment narrative that G2 decides on. Wrap one or two complete,
validated Solutions in a six-part dual-sided narrative and sourced financial case, then stop before
the human's investment judgment. The narrative never compensates for missing Solution content.

## Workflow

1. Require exact refs to complete Solutions at `validation_status: validated`. Reject unresolved
   content gaps, projection drift, incomplete Achilles evidence, or missing financial provenance.
2. Compose the six parts — ① Brief ② Opportunity ③ Solution ④ Why big ⑤ Financial Case ⑥ Roadmap —
   per `references/investment-narrative-template.md`, presenting rather than recreating the
   canonical Solution blocks.
3. Build the financial case so **every** assumption cites source + logic: user count, retention,
   pricing, CAC, cost, year-by-year P&L, profitability timing (reference comparable crowdfunding
   counts, industry success rates, etc.). Tie each financial assumption to a ledger assumption with
   `evidence_refs`.
4. Write the narrative artifact (`_bewater-output/ART-xxx-rN-investment-narrative.md`,
   `kind: investment-narrative`, `stage: shape`) via bwkit.
5. Present the narrative + financial case, name the investment-decision authority, and **stop**.

Field semantics: `../_bw-shared/ledger-schema.md`; lifecycle contract:
`../_bw-shared/idea-concept-solution-lifecycle.md`.
