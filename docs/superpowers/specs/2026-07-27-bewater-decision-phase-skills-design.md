# BeWater Decision-Phase Skill Toolkit — Design Spec

- **Date**: 2026-07-27 (revised 2026-07-28 after external review)
- **Status**: Draft v2 (for review)
- **Authority**: `bewater-methodology/bewater-core.md` v1.3 (read-only source of truth for the methodology)
- **Prior art**: `bewater-methodology-bmad-rosy-perlis.md` (4-layer design) — architecture borrowed and trimmed; `bewater-n/` (python substrate) — cautionary tale of over-scoped runtime (stalled)

---

## 0. Goal

A Claude Code skill toolkit that turns bewater's **decision phase** into an interactive, executable flow, backed by a **minimal deterministic runtime** so the parts that must be reliable (invariants, gate evidence, stale/baseline, lineage) actually are.

> Decision phase = manage *uncertainty* (assumption ledger, evidence levels, gates, backtrack). This is what bewater is distinctive for and what existing tools (bmad, spec-kit, coding agents) do not provide.

**Two tiers, not one.** The kit is split along the seam `writing-skills` L59 draws:
- **Deterministic runtime** (`bw` CLI) — owns file state; enforces everything mechanical (invariants, referential integrity, dual-sided non-empty, gate pass/fail, content hashing). Skills do **not** edit state directly.
- **Skills** (markdown) — the agent-facing interaction layer; judgment calls, diverge work, and "stop for human" convergence. They call the CLI for any state touch.

This split is what makes the closed loop real. Prompt instructions alone cannot enforce single-writer, reject-illegal-write, or machine-scan (review P0-1, verified against `writing-skills` L59). But the runtime stays minimal (§4) — database-grade machinery (locks, CAS, journals, concurrency) is deliberately out, because this is single-user Claude Code and `bewater-n` already proved the heavy version stalls.

---

## 1. Scope

**In scope**
- Decision phase: Immersion → Discover → Define → Ideate → Shape + `strategy-gate` (G1) + `concept-gate` (G2).
- Minimal `bw` runtime: `init`, `ledger`, `validate`, `gate-scan`, `hash`.
- State layer: assumption ledger, 3 invariants, lineage, backtrack, content-hash stale/baseline.
- Money + Magic dual-sided enforcement (as a `validate` check).
- Gates: machine verification via `gate-scan` + 5-exit **human** decision.
- G2 → execution handoff (handoff doc only).

**Out of scope (YAGNI)**
- Execution phase (Design / Build / Launch / Grow).
- `dist/` packaging (`build-runtime.js` / `install.sh`); only a dev-install symlink + smoke test (§11).
- Multi-platform byte-identical mirrors. **Claude Code only.**
- Persona / agent model. Stage-organized skills; human-converge non-delegable.
- **Heavy runtime**: file locks, atomic rename, CAS revisions, action journal, concurrency detection, interrupt recovery. Single-user, single-session — these solve non-problems.
- **Full branch/merge semantics**: `branch_id` / selected-killed-merged parallel state machines. Ideate converges before Shape; one active solution path is the norm.
- **Full gate FSM**: pending→decided→applied, supersedes chains, input snapshots. UUID + tracked conditions is enough.

---

## 2. Design Principles

1. **Mechanical → CLI, judgment → skill** (`writing-skills` L59). Anything regex/validatable (invariants, dual-sided, gate criteria, stale) is a CLI op. Skills hold only judgment and interaction.
2. **Atomic capabilities, stage routers.** Stage skills are thin routers. Each capability is one §9 template, independently invocable, composable.
3. **Single writer.** The ledger and gate records are written only via `bw` ops; skills never hand-edit the YAML. Invariants are enforced at the CLI boundary.
4. **Gates: machine-verify, human-decide.** A gate runs `bw gate-scan`, reports pass/fail, presents 5 exits, and **stops**. Never auto-decides.
5. **Human-converge is non-delegable** (§8). Every capability that converges ends "present candidates + stop".
6. **Lineage + hash everywhere.** Every artifact carries `derived_from` and a content `hash`; `last_validated_against` stores `{id, hash}` so in-place upstream edits are detectable.
7. **Lean.** 20 skills + 4-op CLI. Workshop ops are a reference, not skills.

---

## 3. Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│ DETERMINISTIC RUNTIME (not skills)                                │
│   bw  init | ledger | validate | gate-scan | hash   ← owns state │
│   enforces: 3 invariants, referential integrity, dual-sided,      │
│              gate pass/fail, content hash, lineage cycle check     │
├──────────────────────────────────────────────────────────────────┤
│ SKILLS — interaction layer (call bw, never edit state directly)   │
│                                                                   │
│   entry      bw-start                                             │
│   stage      bw-immersion / bw-discover / bw-define /             │
│   router     bw-ideate / bw-shape   (scan → route; carry nothing) │
│   gate       bw-strategy-gate (G1) / bw-concept-gate (G2)         │
│   capability bw-project-charter / bw-4c-research /                │
│              bw-insight-craft / bw-directional-hypothesis /        │
│              bw-strategy-statement / bw-opportunity-area /         │
│              bw-concept-card / bw-assumption-map /                 │
│              bw-experiment-design / bw-investment-narrative /      │
│              bw-solution-shape            (11, one §9 template ea) │
│   state      bw-ledger   (agent's interface to bw ledger ops)     │
└──────────────────────────────────────────────────────────────────┘
```

Taxonomy (`layer`, `stage`, gate `position`) lives in **`catalog.yaml`**, NOT in SKILL.md frontmatter — frontmatter stays standard `name` + `description` only (per `agentskills.io` spec; verified `writing-skills` L96). This avoids generator/validator conflicts (review P0-4) and decouples taxonomy from skill files.

---

## 4. The `bw` Runtime (minimal, 5 command groups)

Language: **Python 3, stdlib only** (zero deps; matches `bewater-n` prior art; strong for schema/validation unit tests). Overridable at plan time.

| command group | what it does | enforces / computes |
|---|---|---|
| `bw init [project]` | scaffold `_bewater/` (config, empty ledger, artifact dirs, knowledge-base) | idempotent |
| `bw ledger <add\|update\|validate\|baseline\|trace\|backtrack>` | the **only** mutation path for the assumption ledger | enforces 3 invariants on every write; `baseline` snapshots `{id:hash}` → `last_baselined_at`; `backtrack` routes by `layer` |
| `bw validate [--kind dual-sided\|invariants\|refs]` | check ledger + artifacts | 3 invariants; referential integrity (`derived_from`/`affects`/`subject_refs` resolve); dual-sided 4 elements non-empty for kinds {charter, directional-hypothesis, concept, solution}; lineage acyclic |
| `bw gate-scan G1\|G2 [--subject <artifact_id>]` | compute evidence pass/fail for a gate | scans **only the subject solution's active lineage**; reports per-criterion pass/fail + blocking reasons |
| `bw hash <path>` | content-hash an artifact; record in frontmatter `hash`; refresh `last_validated_against` deps | enables stale detection + immutable baseline snapshot |

`bw-ledger` (skill) is the agent's interface to add/update/validate assumptions; it shells out to a ledger sub-op (`bw ledger add\|update\|validate\|baseline\|trace\|backtrack`) — the CLI does the write and enforces invariants; the skill never edits YAML by hand.

**No** locks, atomic-rename, CAS, journal, or concurrency handling. Single-user, single-session.

---

## 5. State Schemas (field-level)

### 5.1 Assumption Ledger — `_bewater/state/assumption-ledger.yaml`

```yaml
project: <name>
last_baselined_at: null           # G2 id on concept-gate exit=go
baseline: null                    # immutable {artifact_id: hash, assumption_id: hash} snapshot at baseline
assumptions:
  - id: A-001
    statement: "..."
    layer: concept                # root | strategy | opportunity | concept | feature
    category: consumer            # consumer | commercial | technical | distribution | regulatory
    impact: high                  # low | medium | high
    uncertainty: high             # low | medium | high
    is_achilles_heel: true        # ⟺ impact=high && uncertainty=high
    evidence_level: L3            # L1..L6
    validation_status: open       # open | testing | validated | falsified | superseded
    status: active                # active | killed | merged   (killed/merged evidence stays, not blocking)
    evidence_ref: knowledge-base/<path>
    derived_from: [C-002]
    affects: [S-001, A-004]
    branch: sol-01                # the solution lineage this belongs to (see §5.4)
    updated_at: 2026-07-28
```

**3 invariants** (enforced by `bw validate --kind invariants`, reject write on violation):
1. `is_achilles_heel` ⟺ `impact=high && uncertainty=high`.
2. `is_achilles_heel=true && validation_status=validated` ⟹ `evidence_level >= L4`.
3. `validation_status: falsified` ⟹ `bw ledger backtrack` invoked (route by `layer`).

### 5.2 Artifact Frontmatter — all `artifacts/**/*.md`

```yaml
---
artifact_id: <unique-id>
kind: strategy                   # charter | directional-hypothesis | strategy | opportunity-area
                                 #   | concept | solution | investment-narrative | research | insights
stage: define                    # immersion | discover | define | ideate | shape
status: draft                    # draft | final | superseded
hash: <sha256>                   # set by `bw hash`; detects in-place edits
locked: false                    # strategy lock (G1 criterion)
validated_by: ""                 # human who validated (solution, G2 criterion)
validated_at: ""                 # ISO date
signoffs:                        # human non-delegable judgments (review P1-7)
  - {who: <name>, role: <role>, what: "F/P/E/T", at: "2026-07-28"}
dual_sided:                      # required when kind ∈ {charter, directional-hypothesis, concept, solution}
  money:  {commercial_value_proposition: ..., leverageable_assets: ...}
  magic:  {consumer_value_proposition: ..., consumer_target: ...}   # situation & desire, not "solves a problem"
  tension: ...
derived_from: [<artifact-id>]
last_validated_against:          # {id, hash} pairs — mismatch ⟹ stale (review P1-5)
  - {id: C-002, hash: <sha256>}
created_at: 2026-07-28
updated_at: 2026-07-28
---
```

`kind: strategy` is the **innovation strategy** artifact (the set of choices); the **strategy statement** is its `statement` field — the choice-cutting blade handle (methodology §9.5; review P2). Produced by `bw-strategy-statement`.

**Gate rules (machine-scan via `bw validate`):** `status: final` + non-empty body is the only completion evidence. `draft` is resumable input. dual-sided four elements non-empty for the kinds above. `hash` mismatch on a dependency ⟹ stale ⟹ blocking.

### 5.3 Gate Decision Record — `_bewater/state/gates/<gate>-<uuid>.md`

```yaml
---
gate: G2                         # G1 | G2
attempt_id: <uuid>               # not date — survives same-day re-review (review P1-8)
position: shape→design
subject_refs: [sol-01]           # which solution(s) adjudicated; scan only their lineage (review P1-6)
decision_date: 2026-07-28
decision_maker: <name>           # single accountable human (non-delegable, §8.2)
exit: go                         # go | conditional-go | recycle | pivot | kill
conditions: []                   # for conditional-go: [{id, requirement, owner, status: open|closed}]
---
## Evidence check (bw gate-scan output, pass/fail per criterion)
## Five-exit selection (human)
## Decision actions
```

### 5.4 Branching (light)

`branch` on an assumption = the solution lineage it belongs to (`sol-01`). `bw gate-scan --subject sol-01` walks only `sol-01`'s `derived_from`/`affects` chain. Killed (`status: killed`) assumptions stay in the ledger with their evidence (serve other branches, §7.3) but are excluded from active-lineage scans. **No** `branch_id`/merge parallel state machine — that's YAGNI (review P1-6, trimmed).

---

## 6. Skill Catalog (20)

Frontmatter = `name` + `description` only. `description` is trigger-only ("Use when …"), no workflow summary (`writing-skills` L99-102/L150 — review P2). Drafts below; finalized via SDO + micro-testing during implementation.

| layer | skill | description (trigger-style draft) |
|---|---|---|
| entry | `bw-start` | Use when starting a bewater decision-phase project, or resuming one and unsure which stage/action is next. |
| stage | `bw-immersion` | Use when navigating bewater Immersion — aligning proposition and seeding first assumptions before research. |
| stage | `bw-discover` | Use when navigating bewater Discover — deciding whether to run 4C research, synthesize insights, or write directional hypotheses. |
| stage | `bw-define` | Use when navigating bewater Define — strategy statement, opportunity areas, or requesting the strategy gate. |
| stage | `bw-ideate` | Use when navigating bewater Ideate — generating and converging concept cards toward the few worth shaping. |
| stage | `bw-shape` | Use when navigating bewater Shape — assumption map, experiments, solution, or requesting the concept gate. |
| gate | `bw-strategy-gate` | Use when bewater Define outputs are in place and a human must decide if the direction is worth exploration resources (G1). |
| gate | `bw-concept-gate` | Use when bewater Shape outputs are in place and a human must decide if the concept is validated enough to invest build resources (G2). |
| capability | `bw-project-charter` | Use when drafting/revising the bewater project charter and seeding first assumptions into the ledger. |
| capability | `bw-4c-research` | Use when planning/running bewater 4C research and the living learning plan. |
| capability | `bw-insight-craft` | Use when synthesizing raw bewater research into insights and judging them against F/P/E/T. |
| capability | `bw-directional-hypothesis` | Use when composing bewater directional hypotheses (By/We can/Resulting in) from confirmed insights. |
| capability | `bw-strategy-statement` | Use when writing the bewater innovation strategy + its statement (the choice-cutting blade that can kill candidate options). |
| capability | `bw-opportunity-area` | Use when carving bewater opportunity areas (2–4, non-overlapping) from a locked strategy. |
| capability | `bw-concept-card` | Use when generating, filling, and scoring bewater concept cards to converge on the few worth shaping. |
| capability | `bw-assumption-map` | Use when classifying bewater assumptions, ranking impact×uncertainty, flagging achilles heels — for an initial inventory (pre-G1) **or** a deep Shape map. (cross-stage) |
| capability | `bw-experiment-design` | Use when designing a bewater experiment for an achilles heel, with kill/proceed criteria fixed before running. |
| capability | `bw-investment-narrative` | Use when drafting the bewater investment narrative (6 parts + Solutions 3-segment + per-assumption evidence disclosure). |
| capability | `bw-solution-shape` | Use when shaping a selected concept into the validated bewater solution artifact (dual-sided solution + business case) that the concept gate adjudicates. |
| state | `bw-ledger` | Use when adding/updating/validating a bewater assumption, tracing dependents, or routing a backtrack after a falsification. |

### Capability → human-converge endpoint (non-delegable stop)

| capability | AI diverges | human converges |
|---|---|---|
| bw-project-charter | charter + seed assumptions | lock proposition + success criteria |
| bw-4c-research | desk research + interview guides | real interviews (共情) |
| bw-insight-craft | insight candidates | which pass F/P/E/T |
| bw-directional-hypothesis | hypothesis candidates | confirm |
| bw-strategy-statement | strategy + statement candidates | pick + lock the strategy |
| bw-opportunity-area | OA options | select/edit |
| bw-concept-card | scored concepts | which advance |
| bw-assumption-map | achilles ranking | which to test first |
| bw-experiment-design | experiment designs | kill/proceed after results |
| bw-investment-narrative | narrative draft | review (kill/proceed is at the gate) |
| bw-solution-shape | solution draft | confirm dual-sided solution |

---

## 7. Gate Mechanics

```
1. bw gate-scan <G1|G2> --subject <solution_id>   → pass/fail per criterion (only active lineage)
2. Any blocking reason non-empty → present ONLY conditional-go / recycle / pivot / kill + reason. No go.
3. Evidence complete → present all 5 exits.
4. STOP. Wait for the human decision_maker. Absent → stop, do not auto-decide.
5. On exit: write decision record (UUID); perform decision actions.
```

**Five exits:** `go` · `conditional-go` · `recycle` · `pivot` · `kill`.
**Blocking reasons (canonical):** `missing-artifact` · `achilles-heel-under-evidenced` · `unbacked-financial-assumption` · `single-sided` · `stale-artifact` · `gate-criteria-incomplete`.

### `bw-strategy-gate` (G1, judgment) — criteria
- [ ] insights human-signed F/P/E/T (`signoffs`)
- [ ] directional hypotheses: 2–5, dual-sided complete
- [ ] strategy artifact: `locked: true`, statement passes "is a blade, not a summary"
- [ ] opportunity areas: 2–4, non-overlapping
- [ ] ledger: initial inventory done, achilles quadrant identified
- [ ] Money + Magic dual-sided preliminary pass

### `bw-concept-gate` (G2, burden-of-proof, heaviest) — criteria
- [ ] solution artifact `status: final`, `validated_by/at` set, dual-sided complete
- [ ] all `is_achilles_heel=true` on `sol-01` lineage: `validated` AND `evidence_level >= L4`
- [ ] every financial-case assumption has non-empty `evidence_ref`
- [ ] investment narrative: 6 sections present
- [ ] **Decision actions on `go`:** `bw ledger baseline` (snapshot `{id:hash}` → `last_baselined_at` + `baseline`); produce execution handoff (§9).

---

## 8. Backtrack (in `bw ledger backtrack`)

Triggered by `validation_status: falsified`, a gate exit of `recycle`/`pivot`, or a human-reported failed validation.

```
Step 1 — depth from falsified.layer:
   feature | concept      → small loop (current stage reframe, no gate)
   opportunity | strategy → large loop (back to Define, re-pass G1)
   root                    → large loop (back to Discover, re-pass G1)
Step 2 — trace downstream affects chain; mark each artifact stale (hash mismatch).
Step 3 — if any stale artifact is in the post-G2 `baseline` snapshot → large loop, re-pass original gate.
Step 4 — route to target stage router with the stale-artifact list.
```

`回溯深度 = 假设错的深度` (§6.2). Baseline boundary is now computable because `baseline` stores hashes (review P1-5).

---

## 9. Human-Converge Rule

Every capability SKILL.md ends its converge step with the fixed pattern:
> "Present candidates as a table/list. State the decision the human must make. Stop. Do not pick on the human's behalf."

Defense against anti-pattern #13 (AI over-converging). Non-negotiable; present in every converging capability (table in §6).

---

## 10. G2 → Execution Handoff

On `bw-concept-gate` exit = `go`, produce `_bewater/artifacts/handoff/execution-handoff.md`: validated solution + investment narrative + open assumptions + baselined ledger snapshot. Recommend an execution tool (superpowers / spec-kit / coding agent). **No execution-phase skills.**

---

## 11. Build, Install, Phasing

### Dev-install (minimal; full packaging deferred)
Skills ship in the tool repo's `.claude/skills/bw-*/`. For use in a product project elsewhere, **symlink** (or copy) them into `~/.claude/skills/` (the Claude Code personal skills path, verified `writing-skills` L12; review P0-3):
```bash
ln -s "$PWD/.claude/skills/bw-"* ~/.claude/skills/
```
Plus a clean-project smoke test (§13) proving a skill activates outside the tool repo.

### Phasing (TDD within each — see §12; no batch)
**Phase 1 — MVP closed loop: Immersion → Discover → Define → `strategy-gate` (13 skills + CLI)**
`bw-start`, `bw-ledger`, `bw-immersion`, `bw-discover`, `bw-define`, `bw-project-charter`, `bw-4c-research`, `bw-insight-craft`, `bw-directional-hypothesis`, `bw-strategy-statement`, `bw-opportunity-area`, `bw-assumption-map` (cross-stage), `bw-strategy-gate` — and the `bw` CLI ops needed for G1 (`init`, `validate`, `hash`, `gate-scan G1`).

**Phase 2 — Concept stage: Ideate + Shape + `concept-gate` (7 skills + CLI `gate-scan G2`, `baseline`)**
`bw-ideate`, `bw-shape`, `bw-concept-card`, `bw-experiment-design`, `bw-investment-narrative`, `bw-solution-shape`, `bw-concept-gate`.

Total: 20 skills + minimal `bw` CLI.

---

## 12. Implementation Method

- **TDD throughout** (`writing-sk` L10/L374; no batch L614; user CLAUDE.md "默认 TDD / 80%+"). Two test types:
  - **`bw` CLI → unit tests, ≥80% coverage.** Covers: schema validation, 3 invariants, referential integrity, dual-sided check, `gate-scan` pass/fail for both gates, hashing/stale detection, duplicate-id, dangling references, lineage cycles, killed-branch exclusion. (Defer concurrency/interrupt-recovery — no concurrency.)
  - **SKILL.md → behavioral evals per skill** (RED-GREEN-REFACTOR with subagent pressure scenarios). Discipline skills (`bw-strategy-gate`, `bw-concept-gate`, every converging capability's "stop for human") get combined-pressure scenarios verifying the agent does not auto-converge. Routing evals verify the right skill triggers and adjacent skills don't collide (review P2).
- **Each SKILL.md generated by `skill-creator`** from this spec's per-skill row (name + trigger description) — not hand-written. Descriptions then SDO-tuned + micro-tested (`writing-skills` SDO section).
- **Shared references** live in a `bw-references/` skill dir (canonical path), lazy-loaded: `templates.md` (§9 field templates), `gate-criteria.md` (G1/G2 checklists), `workshop.md` (two-worlds switch + creative meeting). Other skills reference by skill name, not `@path`.
- **`catalog.yaml`** at tool root records each skill's `layer`/`stage`/gate-`position`/dependencies — the taxonomy source (kept out of frontmatter).
- **Language:** skills, references, schemas, CLI, README in **English**. `bewater-core.md` stays Chinese (read-only authority).

---

## 13. Verification

**Unit (CLI):** every `bw` op has failing-test-first unit tests; ≥80% coverage; edge cases from §12 (duplicate-id, dangling refs, cycles, stale, killed-branch).

**Behavioral (skills, per-skill RED-GREEN-REFACTOR):**
- Routing evals: correct skill triggers on a cue; adjacent skills disambiguated.
- Human-converge stress test: under combined pressure (speed / "just pick one" / authority), the capability still stops and presents candidates; the gate still waits for a human exit.
- G1/G2 E2E: gate blocks when evidence thin (no `go` offered); presents 5 exits when complete; conditional-go conditions tracked.

**End-to-end on one real proposition:**
1. `bw-start` → `bw-immersion` → `bw-project-charter`: charter + ≥3 seed assumptions.
2. `bw-discover` → 4C + insights + directional-hypotheses.
3. `bw-define` → strategy + opportunity-areas.
4. `bw-strategy-gate`: blocks when thin; 5 exits when complete.
5. Inject a falsified assumption → `bw ledger backtrack` routes to correct depth, marks downstream stale.
6. Inject a single-sided artifact → `bw validate` blocks it.

**Clean-install smoke test:** symlink skills into `~/.claude/skills/`, open a fresh product project, confirm a `bw-*` skill activates and can read `_bewater/`.

**Pass bar:** gates block correctly; falsification propagates to correct depth; single-sided caught; every converge action performed by the human; skills work from a clean project via dev-install.

---

## 14. Key Decisions & Trade-offs

1. **Two-tier (deterministic CLI + skills), not prompt-only.** Mechanical enforcement must be automated (`writing-skills` L59); prompt can't enforce single-writer/invariants/gate-scan (review P0-1, verified). The CLI is the engine; skills are interaction.
2. **Minimal CLI, not a runtime.** Only `init`/`ledger`/`validate`/`gate-scan`/`hash`. Locks/CAS/journal/concurrency deliberately out — single-user; `bewater-n` proved the heavy version stalls.
3. **Atomic capabilities, stage routers** (user's call). ~20 skills vs ~9 monolithic; buys composability + clean routing.
4. **`catalog.yaml` over frontmatter taxonomy.** SKILL.md frontmatter stays `name`+`description` (standard); avoids generator/validator conflicts (review P0-4); generator-agnostic.
5. **Content-hash stale/baseline.** `last_validated_against` stores `{id, hash}`; baseline snapshots hashes — makes backtrack boundary computable (review P1-5).
6. **Light branching.** `branch` + `status: killed`; gate scans active lineage only; killed evidence preserved. Full branch/merge deferred (YAGNI; review P1-6 trimmed).
7. **Gate = machine-verify + 5-exit human; UUID + tracked conditions.** No full FSM (review P1-8 trimmed).
8. **Dual-sided is a `validate` check, not a skill.** Mechanical → CLI; trims a skill, raises reliability.
9. **`bw-solution-shape` added.** G2 needs a solution producer (review P0-2).
10. **`bw-assumption-map` cross-stage, in Phase 1.** G1 needs the inventory/quadrant producer (review P1-9).
11. **Machine-readable gate fields.** `signoffs`/`locked`/`validated_by,at`/required sections/financial-assumption refs make gate criteria checkable (review P1-7).
12. **English skills, Chinese methodology; Claude-only; dev-install not full packaging.**
13. **MVP reaches a real gate (G1).** Smallest slice exercising every mechanism including the human gate decision and backtrack.
