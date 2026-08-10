# Shape stage

Shape consumes the Ideate `concept-portfolio` handoff — exactly 2–4 selected
Concept Items (`exit.selected_concept_ids`, each `decision: selected` with hard
criteria passing) — and turns them into 1–2 validated, dual-sided solutions with
business cases and investment narratives, resolving every Achilles Heel with L4+
behavioral evidence. Judgment: a solution must be focused / detailed /
persuasive — "make it impossible not to invest."

Shape does not reselect concepts. If the portfolio is missing, holds fewer than
2 or more than 4 selected concepts, or a selected concept's hard criteria have
not passed, route back to **bw-ideate** (a small Ideate/Shape loop) rather than
inventing or trimming the selection.

## Capabilities to route to

- **bw-solution-shape** — shape selected concepts into validated dual-sided
  solutions (`kind: solution`, five concept→solution paths), preserving the
  portfolio revision and each Concept Item id along the concept→solution path.
- **bw-experiment** — design an experiment or record its result + the human
  Kill/Proceed decision. Achilles-Heel experiments must target L4+ behavioral
  evidence.
- **bw-investment-narrative** — draft/revise the six-part dual-sided narrative +
  sourced financial case.

## Convergence into G2 (no gate here)

Shape hands **1–2 validated solutions + the investment narrative + L4 evidence +
sourced financial assumptions** to **bw-concept-gate** (G2). Use
`../_bw-shared/gate-criteria.md` as the filter. A falsified assumption surfaces
through bw-backtrack, never as a local note.
