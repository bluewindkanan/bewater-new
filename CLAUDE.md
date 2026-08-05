# BeWater

Innovation methodology toolkit. Pipeline: Immersion → Discover → Define → G1 → Ideate → Shape → G2 → handoff.

## Skill Routing

```
FIRST ACTION     → bw-immersion
RESUME / global  → bw-resume       (read-only status and recovery routing)
immersion        → bw-immersion    → bw-project-charter, bw-initial-assessment
discover         → bw-discover     → bw-discovery-research, bw-insight-craft
define           → bw-define       → bw-directional-hypothesis, bw-strategy-statement,
                                     bw-opportunity-area, bw-assumption-map
G1 (strategy)    → bw-strategy-gate
ideate           → bw-ideate       → bw-concept-card
shape            → bw-shape        → bw-solution-shape, bw-experiment, bw-investment-narrative
G2 (investment)  → bw-concept-gate
backtrack        → bw-backtrack    (falsified assumption or artifact change)
```

**Router** = navigate only. **Capability** = produce artifacts, stop before human decision. **Gate** = present exits, never choose.

Skills are authored under `src/skills/` and deployed under `.claude/skills/`. Shared deployed
contracts live under `.claude/skills/_bw-shared/`. Deployment initializes BeWater project state;
the first workflow action is Immersion, while `bw-resume` may be used at any time afterward.

## Commands

```bash
python -m bwkit lock acquire
python -m bwkit cas commit <path> --expected <rev>
python -m bwkit plan apply <root> < plan.json
python -m bwkit check integrity
echo '{"edges":[...], "roots":[...]}' | python -m bwkit scan impact
```

## Design Principles

- **Minimal by default**: every element must justify its existence. One responsibility per phase/role/artifact. If one sentence suffices, don't write two. If one skill can do it, don't create two.
- **English-first**: BeWater methodology design resources and documents — skill content (SKILL.md), references, templates, and design specs — are written in full English; other languages derive from English, never the reverse. User-facing project artifacts (Charter, Assessment, etc.) preserve the user's own language.

## Rules

- Never choose a gate exit. Never sign F/P/E/T. Never write `_bewater/` state by hand.
- L4+ behavioral evidence is a hard gate criterion — L1-L3 self-report + human insistence ≠ Go.
- Capabilities produce drafts and stop. Gates assemble evidence and stop. Human decides.
- **Superpowers policy:** only the local `brainstorming` skill is permitted. Do not invoke,
  recommend, or hand off to any other `superpowers:*` skill, including `writing-plans`,
  `executing-plans`, `subagent-driven-development`, or `using-superpowers`.
