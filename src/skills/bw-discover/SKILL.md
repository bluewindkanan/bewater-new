---
name: bw-discover
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in BeWater Discover.
---

# bw-discover

A **router** for Discover. It reports status and routes to research; it does not author artifacts.
Discover conducts 4C-directed exploration and outputs research evidence (candidate Facts, beliefs);
it does not produce insights or directional hypotheses.

## On invoke

1. Confirm `current_stage: discover` on the selected branch.
2. Read the current charter revision and active root assumptions as the formal Discover inputs. If
   either is missing, stale, or ambiguous, report the input gap and route to `bw-project-charter`.
   Never substitute an Assessment or invent a Discover Brief.
3. Look for an `initial-assessment` on the same branch whose `derived_from` exactly matches the current
   Charter revision plus the complete active root-assumption revision snapshot.
4. Read a matching report as an advisory reference and translate only:
   - **Candidate Insights** → candidate judgments to validate;
   - **Core Conflict / Tension** → the priority challenge;
   - **Most Promising Direction** → a candidate research path;
   - **Key Risks** → disconfirming questions.
5. Ignore a stale, cross-branch, or snapshot mismatch Assessment. Report a missing or ignored report
   as an advisory gap; it does not block Discover when the formal inputs are complete.
6. Report formal input revisions, advisory status, 4C coverage, Discover Plan state, research mode,
   and outstanding evidence gaps. Use `AskUserQuestion` to present the next action choice:
   `bw-discovery-research` (continue research) or, when research is at Insight Readiness,
   `bw-define` (enter Define stage to craft insights). Include a clear description of what each
   option does and the current state. Stop and wait for the user's selection; do not auto-route or
   proceed without explicit user direction.

Assessment content never becomes a Fact, Evidence, Accepted Belief, or F/P/E/T Insight directly.
It remains a candidate until Discover research supplies the required support. Discover does not
create a Discover Brief and does not change the Assessment.

Treat all Assessment claims as candidate beliefs or hypotheses, not as Facts.

Discover hands research evidence (4C coverage, documented gaps) to Define (`bw-define`), where
insights are crafted and directional hypotheses are composed. Cite `../_bw-shared/gate-criteria.md`
for G1 readiness requirements.
