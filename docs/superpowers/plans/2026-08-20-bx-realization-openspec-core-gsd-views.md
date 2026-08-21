# BX Realization Stage — OpenSpec Core + GSD Views — Adoption Plan

Date: 2026-08-20
Status: Draft (user-approved direction; execution pending go)

## Objective

Give BeWater a Realization-stage (post-G2 execution) capability without breaking the
three constitutional principles (minimal runtime, self-contained, human-machine split):

1. **Validate the design in a lab** — GSD outer-ring documents + OpenSpec inner loop,
   composed in `~/Desktop/gsd` on a real pilot project.
2. **Distill the validated contract** into a BeWater-native `bx-*` skill family
   (init / propose / apply / archive).
3. **Retire both external runtimes.** The only new runtime code is a delta validator
   in `bwkit`. No GSD CLI, no OpenSpec CLI, no hooks.

## Decisions already made (do not re-litigate)

| Area | Decision |
|---|---|
| Role of GSD | Lab instrument + document shapes only. Its runtime (state machine, inner-loop workflows, hooks, runtime shims, transition) is NOT integrated. |
| Role of OpenSpec | Blueprint for the entire inner loop: specs/changes two-layer truth, delta format, propose→apply→archive, planning boundary. Its CLI/store/profiles/telemetry are NOT integrated. |
| new-project | Not needed after merge. BeWater Immersion→G2 replaces it: Charter = PROJECT.md, execution-handoff.md = REQUIREMENTS seed. |
| Views vs truth | In the lab, GSD docs (REQUIREMENTS/ROADMAP/STATE) are projections of OpenSpec truth (specs/ + archive history). Views are touched only at two hooks: propose (register) and archive (settle). PROJECT.md remains human-owned authority. |
| Update discipline | "GSD docs move only when a commitment changes" — propose commits to do, archive settles (or cancels). Mid-execution never writes back. |
| Intake governance | A change delta that MODIFIES a capability linked to the G2 baseline routes to `bw-backtrack`; never silently absorbed. In-boundary ideas update planning directly. |
| No bx-next router | Actions-not-phases model needs no state machine. Dropped from the earlier GSD-skeleton Route B sketch. |
| BeWater state untouched | bx skills never write `_bewater/`; they read execution-handoff and route to bw-backtrack for falsification. |

## Phase A — Lab validation (`~/Desktop/gsd`, zero changes to bewater-new)

- **A1** Install OpenSpec: `npm i -g @fission-ai/openspec && openspec init`.
  Check the generated instruction file does not clobber GSD's `.claude/CLAUDE.md`.
- **A2** Write the glue into the project's `.claude/CLAUDE.md` (~20 lines): mapping
  rules (phase N ↔ change `phase-NN-<slug>`, Success Criteria ↔ Given/When/Then
  scenarios, REQ-ID ↔ capability), the two-hook update discipline, and "GSD
  inner-loop commands are forbidden" (discuss/plan/execute/verify).
- **A3** Start a real pilot project via `/gsd-new-project` (deep questioning,
  requirements, roadmap). **Open decision:** which project. Candidates: a small
  fresh idea, or a dry-run fixture. User picks at execution time.
- **A4** Run one full change cycle end to end:
  `/opsx:propose phase-01-<slug>` → human review of proposal + delta →
  `/opsx:apply` → `/opsx:archive` → manual settle (REQ ✓ / ROADMAP strike /
  STATE advance).
- **A5** After the manual settle proves the rules, script it: `openspec-sync`
  (~30 lines; reads `openspec/changes/archive/`, edits the three GSD docs). If
  GSD's write-guard hook blocks it, route the commit via `gsd_run query commit`.
- **A6** Write findings: is the delta format expressive enough (incl. non-feature
  changes like refactors)? Is settle smooth? Is the roadmap view worth keeping?
  Any missing intake case? → feeds Phase B.

**Exit criteria:** one change archived with specs/ merged and the ledger settled;
findings list written.

## Phase B — Contract distillation (bewater-new)

- **B1** `bx-artifacts.md` — the artifact contract, in a new shared home
  `src/skills/_bx-shared/` (mirrors `_bw-shared/`): target directory layout in the
  delivery repo, delta format (ADDED / MODIFIED / REMOVED requirements +
  Given/When/Then scenarios), requirement-ledger shape, roadmap-view shape, settle
  rules, intake governance fork (in-boundary vs G2-baseline vs reject).
- **B2** Lock scope decisions: artifacts live in the delivery repo; BeWater
  canonical state untouched; ART references from execution-handoff must be
  materialized (copied) into the delivery repo, never referenced by path only.

## Phase C — bx skills + validator (TDD, coverage ≥ 80% on runtime code)

- **C1** `bwkit` delta validator (`python -m bwkit validate-delta <change-dir>` or
  equivalent), test-first, mirroring existing `src/bwkit/` validator style: delta
  section format, capability-path references exist, ≥1 scenario per requirement.
- **C2** `bx-init` — consume `execution-handoff.md` (schema_version 1): materialize
  initial `specs/` from validated solutions, roadmap seed from solution scope,
  Out-of-Scope from unselected concepts, scenarios from EXP success criteria.
  Verify ART refs; refuse non-formal-Go handoffs (provisional included).
- **C3** `bx-propose` — intake + proposal + delta + tasks; planning boundary
  adapted from `openspec-propose` ("artifacts only, stop, wait for explicit
  apply"); governance fork: MODIFIED on G2-baseline-linked capability → surface
  and route to `bw-backtrack` instead of drafting.
- **C4** `bx-apply` — execute tasks.md, atomic commits, no ledger writes, no
  scope decisions.
- **C5** `bx-archive` — merge deltas into specs/, archive the change, settle the
  ledger (REQ ✓ / roadmap strike). Absorbs GSD's transition gap.
- **C6** Deployment: extend the `src/skills → .claude/skills` deployment pipeline
  for `_bx-shared`; update project CLAUDE.md (Scope + Skill Routing table with the
  bx row and the post-G2 entry).

## Phase D — Verification

- **D1** Dry-run: Baidu AI-glasses mock execution-handoff → `bx-init` →
  `bx-propose` → `bx-archive`; assert final specs/ content and ledger states.
- **D2** `bwkit` delta-validator unit tests pass; coverage ≥ 80% on new code.
- **D3** (deferred, optional) an eval scenario exercising the intake governance
  fork.

## Non-goals

- No wave-parallel execution, no UAT conversational acceptance in v1 (GSD organs;
  revisit if a real project needs them).
- No porting of GSD CLI/hooks/state machine or OpenSpec CLI/store/profile engine.
- No changes to decision-segment skills or `_bewater/` state schema.

## Risks / open items

| Risk | Mitigation |
|---|---|
| Pilot project for Phase A not chosen | User decision at A3; keep it small — one phase is enough |
| Delta insufficient for refactor-type changes | Record in A6; decide between "no spec delta, proposal+tasks only" vs a REFACTOR marker in B1 |
| GSD write-guard blocks sync script | Use `gsd_run query commit` for the settle commit |
| Two installers both edit instruction files | Check markers before each install step (A1, A2) |
