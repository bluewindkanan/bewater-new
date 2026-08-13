# Discover stage

Discover uses 4C-directed exploration and field methods to conduct research and gather evidence. It
outputs research evidence (candidate Facts, beliefs, documented gaps); insights are crafted in the
following Define stage.

## Formal inputs

The selected branch's current Charter revision is the only formal prerequisite and formal Discover
input. It supplies the project definition and explicit Unknowns from which Research Planning starts.

An Initial Assessment is a user-facing checkpoint, not a Discover input. Discover must not consume
it as Evidence and may read a matching Assessment's `What to Inspect Next` only as candidate seed
questions, never as Facts or Evidence. Whether the Assessment is missing,
current, or stale does not block Discover and does not seed Research as Evidence, the Knowledge Base,
assumptions, or Evidence.

## Capabilities to route to

- **bw-discovery-research** — initialize and iterate the Research Plan, then run Consumer, Company,
  Category, and Channel Research Sprints. A missing or stale Research Plan routes to **Research
  Planning**; a current plan routes to its next Research Sprint.

If the Charter is missing, route back to `bw-immersion`; this stage does not create a
Discover Brief. When assumptions are absent, do not route back; Research Planning may legitimately
project zero assumptions. Keep Fact, Evidence, Accepted Belief, and research evidence distinct.

## Exit criteria

Research evidence is complete with 4C coverage documented and visible gaps acknowledged. Hand the
research evidence to Define, where insights are crafted and directional hypotheses are composed.
