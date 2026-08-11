# Loop-size classification

Before any assumption-layer heuristic, inspect the branch's `active_baselines` pointers.

- **Large loop** — the change touches a baseline item (an assumption/record frozen in an active
  baseline, or a baseline itself). The original gate must rerun. `loop_type: large`,
  `gates_to_rerun: [gate:D-xxx]`.
- **Small loop** — no baseline is touched. A Concept-local reframe returns to Ideate; a
  Solution-local or feature reframe returns to Shape. `loop_type: small`.

Change-depth routing: root premise → Discover + G1 recertify; strategy or changed OA boundary →
Define + G1; Concept (no baseline touched) → Ideate; Solution or feature (no baseline touched) →
Shape. A branch cannot silently
edit a confirmed baseline and continue as a small loop.

## Ideate concept lifecycle

A `recycle-to-OA` recommendation from bw-concept-development is a concept-local
reframe when the mechanism is wrong (small loop: revise the `concept-portfolio`
item, no gate). It becomes a **large loop** only when the opportunity-area
boundary itself is wrong — that returns to Define + G1 recertification and never
edits a G1-baselined OA implicitly. A concept-portfolio item change propagates
to its concept-layer assumptions via `source_concept_id`; a changed OA propagates
through the baseline-aware large loop. Lifecycle contract:
`../_bw-shared/idea-concept-solution-lifecycle.md`.
