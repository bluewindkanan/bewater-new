# Loop-size classification (spec §8.3)

Before any assumption-layer heuristic, inspect the branch's `active_baselines` pointers.

- **Large loop** — the change touches a baseline item (an assumption/record frozen in an active
  baseline, or a baseline itself). The original gate must rerun. `loop_type: large`,
  `gates_to_rerun: [gate:D-xxx]`.
- **Small loop** — no baseline is touched. A feature/concept failure may still be a local reframe
  (Ideate/Shape). `loop_type: small`.

Change-depth routing (§8.3): root premise → Discover + G1 recertify; opportunity/strategy → Define +
G1; feature/concept (no baseline touched) → Ideate/Shape local reframe. A branch cannot silently
edit a confirmed baseline and continue as a small loop.
