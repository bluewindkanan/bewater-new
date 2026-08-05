---
name: bw-immersion
description: Use when the user explicitly asks to navigate, resume, check status, or choose the next action in BeWater Immersion.
---

# bw-immersion

A read-only **router** for Immersion. It reports input and advisory status, recommends exactly one
next capability when possible, and stops. It must never produce artifacts or change project state.

## On invoke

1. Confirm the selected active branch has `current_stage: immersion`; otherwise defer to
   `bw-resume`.
2. Resolve and report:
   - the unique current Charter head and its exact Charter revision;
   - the count and exact active root-assumption revision snapshot for the same branch;
   - formal Discover input readiness: a current Charter plus at least three active root assumptions;
   - Assessment state: `missing`, `failed`, `stale`, or `current`.
3. Treat an Assessment as current only when it is on the same branch and its `derived_from` exactly
   matches the exact typed Charter revision plus the complete exact active root-assumption revision
   snapshot. Existence alone is insufficient; cross-branch or snapshot-mismatched reports are stale.

## Routing

- Charter or assumptions missing or needs revision → `bw-project-charter`.
- Assessment missing, failed, or stale → `bw-initial-assessment`.
- Current Charter, at least three active root assumptions, and a matching Assessment → recommend `bw-discover`
  and stop for the user's separate decision.

When a next human action is needed, present native structured selection rather than asking the user
to type an option. With a matching Assessment, offer: Enter Discover, Revise Charter, or Pause in
Immersion. With a missing, failed, or stale Assessment, offer: Retry Assessment, Continue without Assessment,
or Pause in Immersion. The latter preserves the Assessment as advisory: continuing is
available only when the formal Discover inputs are complete.

When native structured selection is unavailable or fails in an interactive host, present equivalent text options
and stop for the user's reply. In headless use, stop after presenting the options for a
later scripted response. The router never selects on the user's behalf, changes `current_stage`, or
records the user's decision.

Default Immersion guidance waits for the matching report before recommending Discover. The
Assessment is advisory auxiliary material and not a hard gate: if the user explicitly asks to continue and the
formal Discover inputs are ready, report the advisory gap without blocking the separate stage-transition decision.
Charter confirmation does not equal a decision to continue.

The router never authors or edits the Charter, assumptions, or Assessment inline. It never changes
the stage; in other words, it never changes the stage, never records the user's decision, never changes `current_stage`, and never writes a
signoff. The human owns the explicit decision to continue.
