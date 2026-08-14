---
name: bw-discover
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in BeWater Discover.
---

# bw-discover

A **read-only router** for Discover. It reports status and routes to research; it does not author artifacts.
Discover conducts 4C-directed exploration and outputs traceable Knowledge, candidate Facts, and beliefs;
it does not produce insights or directional hypotheses.

## On invoke

1. Confirm `current_stage: discover` on the selected branch.
2. Read the current Charter revision as the only formal prerequisite and the sole member of the
   formal Discover inputs. If it is missing, stale, or ambiguous, report the input gap and route to
   `bw-immersion`.
   Never substitute an `initial-assessment` or invent a Discover Brief.
3. Report Assessment status only. Discover must not consume the Initial Assessment as Evidence and may
   read a matching Assessment's `What to Inspect Next` only as candidate seed questions, never as Facts or
   Evidence. Whether it is missing, current, or stale does not block Discover
   and does not seed Research as Evidence, Research Progress, Knowledge workpapers, assumptions, or Evidence.
4. Resolve the current Research Plan for this branch and exact Charter revision. If the Research
   Plan is missing or stale, route to `bw-discovery-research` in **Research Planning** mode. The
   absence of assumptions is not an input gap and never routes back to Charter. Recommend Research Planning and stop.
5. For a current Research Plan, report the formal input revision, Assessment status, 4C coverage,
   Research Progress, next Sprint state, and outstanding Knowledge gaps. Use `AskUserQuestion` to
   present the next action choice:
   `bw-discovery-research` (continue research) or, when research is at Insight Readiness,
   `bw-define` (enter Define stage to craft insights). Include a clear description of what each
   option does and the current state. Stop and wait for the user's selection; do not auto-route or
   proceed without explicit user direction.

Assessment content is user-facing only and must not be consumed by Discover as Evidence. A matching
Assessment's `What to Inspect Next` may seed candidate research questions only, each independently
source-verified before promotion; `Material Risks` and the Assessment's judgments stay advisory and do
not flow into Research. Discover does not create a Discover Brief and does not change the Assessment.

Discover hands exact Knowledge refs, 4C coverage, and documented gaps to Define (`bw-define`), where
insights are crafted and directional hypotheses are composed. Cite `../_bw-shared/gate-criteria.md`
for G1 readiness requirements.
