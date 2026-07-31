# BeWater

Innovation methodology toolkit. Pipeline: Immersion → Discover → Define → G1 → Ideate → Shape → G2 → handoff.

## Skill Routing

```
START            → bw-start        (bootstrap or reconcile)
immersion        → bw-immersion    → bw-project-charter
discover         → bw-discover     → bw-4c-research, bw-insight-craft
define           → bw-define       → bw-directional-hypothesis, bw-strategy-statement,
                                     bw-opportunity-area, bw-assumption-map
G1 (strategy)    → bw-strategy-gate
ideate           → bw-ideate       → bw-concept-card
shape            → bw-shape        → bw-solution-shape, bw-experiment, bw-investment-narrative
G2 (investment)  → bw-concept-gate
backtrack        → bw-backtrack    (falsified assumption or artifact change)
```

**Router** = navigate only. **Capability** = produce artifacts, stop before human decision. **Gate** = present exits, never choose.

All skills under `.claude/skills/`. Shared contracts under `.claude/skills/_bw-shared/`.

## Commands

```bash
python -m bwkit lock acquire
python -m bwkit cas commit <path> --expected <rev>
python -m bwkit plan apply <root> < plan.json
python -m bwkit check integrity
echo '{"edges":[...], "roots":[...]}' | python -m bwkit scan impact
```

## Rules

- Never choose a gate exit. Never sign F/P/E/T. Never write `_bewater/` state by hand.
- L4+ behavioral evidence is a hard gate criterion — L1-L3 self-report + human insistence ≠ Go.
- Capabilities produce drafts and stop. Gates assemble evidence and stop. Human decides.
