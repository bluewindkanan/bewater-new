---
name: bw-initial-assessment
description: Use when a confirmed BeWater Charter and its active root assumptions need a fresh, source-bounded preliminary assessment before Discover.
---

# bw-initial-assessment

An **independent capability** that uses light external research to produce a compact professional
judgment from confirmed Immersion inputs. It is preliminary and advisory: it is not validation, a
formal Insight, a Gate, or an investment decision.

## Fresh-context input boundary

Run in a fresh context. The caller supplies only:

1. the current branch;
2. the exact typed Charter revision, such as `artifact:ART-001@1`;
3. the exact active root-assumption revision snapshot, such as
   `assumption:A-001@1`, `assumption:A-002@1`, and `assumption:A-003@1`.

On direct invocation, resolve that same snapshot from current project state before research. Require
one unique Charter head, at least three active root assumptions on the same branch, and exact typed
revisions. Do not read the original interview, chat transcript, or any prior Assessment body. Prior
Assessment metadata may be inspected only to establish identity, lineage, revision, and
idempotency; do not inherit its judgments.

If the inputs are missing, ambiguous, multi-head, cross-branch, or no longer current, stop and route
the Charter gap to `bw-project-charter`. Do not reconstruct intent from conversation history.

## Idempotency and reassessment

- Find an existing `initial-assessment` head for the branch by metadata. A matching Assessment has
  a `derived_from` set that exactly equals the current Charter revision plus the complete active
  root-assumption snapshot.
- If a matching Assessment exists and the user did not request explicit reassessment, reuse it and
  do not research or write another revision.
- A first Assessment receives a new ART ID from `config.next_ids.artifact`. Explicit reassessment,
  or assessment after an input change, uses the same artifact ID and appends the next revision with
  `supersedes_ref` pointing to the previous Assessment revision.
- A Charter or input-assumption revision change makes an older Assessment stale by snapshot
  mismatch. Do not edit or mark the old append-only file in place.

## Lightweight external research

1. Search for 3–5 credible public sources. Prefer primary research, official data, regulatory
   material, and authoritative industry sources. Preserve exact source titles and URLs returned by
   the research tool; never invent or repair a citation.
2. Cite sourced statements in the body only as **External signal**. Do not create an Evidence
   wrapper or third artifact, and do not change the ledger's `evidence_level: L1` or
   `validation_status: untested`.
3. Model knowledge must not be presented as an external fact. Unsourced reasoning is allowed only
   when labeled **Assessment inference**.
4. If sources conflict, preserve the conflict and turn it into a risk and Discover question. Do not
   select the favorable source as truth.

Source availability controls the outcome:

- With 3–5 credible sources, generate the normal report.
- With only 1–2 credible sources, generate a visibly source-sparse report and narrow every
  conclusion to the available material.
- With zero credible sources, when the search tool is unavailable, or when search fails, do not
  create an Assessment. Preserve the Charter and report a concrete retry reason.

## Judgment and report contract

Use `references/initial-assessment-template.md` and target 1–2 screens. The top supports a
60-second read; the remainder supplies traceability. Every key judgment distinguishes:

1. **Charter basis**;
2. **External signal**;
3. **Assessment inference**;
4. **Implication**;
5. **What would change this view**.

The report may state a clear preliminary judgment, Candidate Insight, or directional hypothesis.
It must not score the project, apply red/yellow/green or another readiness label, decide whether it
is worth investing, or decide whether the user should enter Discover.

Before any write, perform a **pre-write content audit** on the complete draft. Require all eight required headings,
a compact five-label trace for every key judgment, 2–3 Candidate Insights, at most three risks each
with a disconfirming signal, an explicit research boundary with only the
sources actually retrieved. If any check fails, revise the uncommitted draft. Do not acquire the write lock or
commit until the content audit passes.

This audit is a deterministic report-contract check, not a second quality-review phase. The
Assessment does not run a brainstorming-style self-review and does not request user confirmation.
After the pre-write content audit passes, automatically commit the report through the transactional
write path below.

## Concurrent-safe write

Use the project-local runtime as `PYTHONPATH=_bewater python3 -m bwkit ...` when `bwkit` is not
already importable. Do not scan outside the project for another runtime or reuse a runtime from a
different sandbox, checkout, or temporary directory.
Treat `references/write-plan.md` as the complete runtime interface; do not inspect `_bewater/bwkit` source.

1. Research without holding the project lock.
2. Immediately before writing, acquire `bwkit lock`, re-read the Charter head and active root-assumption snapshot,
   and compare them with the captured inputs.
3. If either changed, discard the uncommitted report, release the lock, capture the new inputs, and
   automatically rerun once.
4. If either changes again before the second write, fail closed, report concurrent modification,
   and write nothing stale.
5. When inputs still match, use the single transaction in `references/write-plan.md`, with
   `derived_from` pinned to every exact input revision and the artifact counter protected by CAS.
   Run the available revision-chain integrity
   check and fail closed on duplicate revisions, missing predecessors, cycles, or multiple heads.

Stop after the integrity check passes and report the committed revision plus research boundary.
Once integrity returns `ok`, release the write lock if it is still held, then make no further tool call:
do not list or re-read the artifact and do not add a redundant post-commit filesystem audit.

## Mutation boundary

This capability writes only the new append-only Assessment revision and the canonical artifact-ID
counter when first allocating its ID. It does not modify the Charter, does not change assumption
validation, does not change current_stage, and does not write a signoff. No Evidence wrapper is
created. There is no score and no readiness label. It creates no Gate record or extra workflow
artifact, and it must not decide whether to invest.

The **only allowed project-state mutation path** is
`PYTHONPATH=_bewater python3 -m bwkit plan apply .` with the plan defined in
`references/write-plan.md`. Never use Edit or Write on project state. Never use shell redirection,
a heredoc, or a general-purpose script to create or change `_bewater/` or `_bewater-output/` files directly.
