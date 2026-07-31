---
name: bw-experiment
description: Use when the user wants to design a bewater experiment or record its result and Kill/Proceed decision.
---

# bw-experiment

A **capability** for assumption-driven experiments. You design or record results and stop before
the human's Kill/Proceed decision. An experiment
intended to close an Achilles Heel must target L4+ behavioral evidence — L1–L3 self-report never
satisfies the L4 obligation.

## Workflow

1. **Design** — create/revise `_bewater-output/EXP-xxx-rN-experiment.md` linked to ≥1 assumption.
   Before execution, secure human approval of: target assumption refs; method + target evidence
   level; metric + baseline; **Proceed threshold**; **Kill threshold**; inconclusive treatment;
   owner/timebox/evidence-capture path. Thresholds are fixed BEFORE observing results.
2. **Record result** — record observed result + metric values; raw evidence refs; achieved evidence
   level + why; conclusion (supported/falsified/inconclusive); proposed ledger changes; the human
   decision (proceed/kill/retest); artifact + ledger revisions changed. Wrap captured evidence as an
   immutable `evidence:E-xxx@n` artifact.
3. Present the result + proposed ledger diff, name the human decision authority, and **stop**. The
   human decides Kill/Proceed; you update the assumption only after that decision and show the diff.
   A falsified assumption initiates **bw-backtrack** — never a local note.

See `references/experiment-template.md` for the design checklist, result fields, the L1–L6 table,
and the experiment menu. Field semantics: `../_bw-shared/ledger-schema.md`.
