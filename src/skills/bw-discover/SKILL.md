---
name: bw-discover
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in BeWater Discover.
---

# bw-discover

A **router** for Discover. It reports status and routes to research or insight craft; it does not
author artifacts. Discover turns sourced facts into candidate insights and stops at the signed
Insight Portfolio; it does not produce directional hypotheses.

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
   outstanding evidence gaps, and insight count and quality. Route to `bw-discovery-research` or
   `bw-insight-craft`, presenting the choice and stopping when ambiguous.

Assessment content never becomes a Fact, Evidence, Accepted Belief, or F/P/E/T Insight directly.
It remains a candidate until Discover research supplies the required support. Discover does not
create a Discover Brief and does not change the Assessment.

Treat all Assessment claims as candidate beliefs or hypotheses, not as Facts.

Discover hands the current-revision human-signed Insight Portfolio to Define (`bw-define`).
Directional hypotheses are composed only in Define. Cite `../_bw-shared/gate-criteria.md` for
insight readiness.
