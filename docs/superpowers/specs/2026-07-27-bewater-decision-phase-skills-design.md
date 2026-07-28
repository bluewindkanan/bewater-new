# BeWater Decision-Phase Skill Toolkit — Design Spec

- **Date**: 2026-07-27 · **Status**: v3 (for review) · **Authority**: `bewater-methodology/bewater-core.md` v1.3 (read-only)
- **v2 → v3 change**: **dropped the deterministic `bw` CLI runtime.** It was over-built for a tool meant to be "类似 bmad / 尽可能简洁". BMAD (the reference) ships NO methodology runtime — only skills + an installer; execution = host AI + human. bewater follows that. The runtime's enforcement (gates, dual-sided, achilles L4+, refs) moves to **skill checklists presented to the human at the gate**. The human is the block (bewater is human-converge anyway).
- **Plan A archived**: `src/bw/` + `tests/` (commits `264654a..ff3c7ac`) stay in git history as a reference implementation; **not shipped**. Removed from the working tree as the first step of the new plan.

---

## 0. Goal

A Claude Code **skill toolkit** (BMAD-shaped) that turns bewater's decision phase into an interactive flow. No runtime, no Python, no install friction — just markdown skills + a tiny installer. The host AI (Claude Code) executes the skills; the human converges at every gate.

> Decision phase = manage *uncertainty* (assumption ledger, evidence levels, gates, backtrack). bewater's distinctive value. This toolkit makes the flow executable; it does NOT machine-guarantee enforcement — that's the human's job at the gates, by design.

---

## 1. Scope

**In:** decision phase — Immersion → Discover → Define → Ideate → Shape + `strategy-gate` (G1) + `concept-gate` (G2). Skills + installer + per-project `_bewater/` (config+state) + `_bewater-output/` (documents). G2 → execution handoff (doc only).

**Out (YAGNI):** execution phase; any deterministic runtime/CLI (no `bw` state engine — that was v2, archived); multi-platform mirroring (Claude Code only); persona/agent model (stage-organized skills); machine-enforced invariants (enforcement is via skill checklists + human, not code).

---

## 2. Architecture (BMAD-shaped)

```
bewater-new/                         ← tool repo
├── bewater-methodology/bewater-core.md   ← read-only authority
├── skills/bw-*/SKILL.md             ← the methodology content (English)
│   └── references/                  ← shared, lazy-loaded (templates, gate-criteria, ledger-schema, workshop)
├── install.sh                       ← ~30-line symlink/copy installer → ~/.claude/skills/
├── plugin/.claude-plugin/           ← (later) native Claude plugin manifest
└── docs/                            ← this spec + plan

<product-project>/                   ← per project (bw-start creates these)
├── _bewater/                        ← centralized config + state (control center; gates/routers consult it)
│   ├── config.yaml                  (project name, success criteria, current_stage, decision-makers)
│   └── state/assumption-ledger.yaml (living source of truth)
└── _bewater-output/                 ← document outputs (deliverables, produced stage by stage)
    ├── artifacts/<stage>/*.md       (charter/insights/.../solution/narrative; frontmatter informational)
    ├── gates/<gate>-<date>.md       (gate decision records)
    └── knowledge-base/              (raw research)
```

No `src/`, no package, no venv. Skills are installed once **globally** via `install.sh` → `~/.claude/skills/` (or a plugin); `_bewater/` (config+state) and `_bewater-output/` (documents) are per project.

---

## 3. Design Principles

1. **Skills are the whole tool.** No runtime underneath. Each skill is self-contained markdown the host AI executes.
2. **Enforcement = checklist + human, not code.** Mechanical checks (dual-sided non-empty, achilles heel L4+, ref integrity, gate criteria) live as checklists the gate/capability skill presents to the human. The human is the block (§8 human-converge). Trade-off accepted: best-effort, not machine-guaranteed — same as BMAD.
3. **Atomic capabilities, stage routers.** Stage skills are thin routers; each capability is one §9 template, independently invocable, composable.
4. **Gates present evidence, never decide.** A gate skill reads ledger + artifacts, surfaces the evidence checklist, presents the 5 exits, and **stops**. The human picks the exit.
5. **Single source = the methodology.** `bewater-core.md` is the authority; skills reference §-numbers and the shared `references/` instead of restating.

---

## 4. Skill Catalog (19)

Frontmatter = `name` + `description` only (standard). `description` is trigger-only ("Use when …"), no workflow summary (per `writing-skills` SDO). Taxonomy (`layer`/`stage`) lives in a `catalog.yaml`, not frontmatter.

| layer | skill | trigger-style description (draft) |
|---|---|---|
| entry | `bw-start` | Use when starting a bewater decision-phase project, or resuming one and unsure which stage/action is next. |
| stage | `bw-immersion` | Use when navigating bewater Immersion — aligning proposition and seeding first assumptions. |
| stage | `bw-discover` | Use when navigating bewater Discover — 4C research, insights, or directional hypotheses. |
| stage | `bw-define` | Use when navigating bewater Define — strategy statement, opportunity areas, or requesting the strategy gate. |
| stage | `bw-ideate` | Use when navigating bewater Ideate — generating and converging concept cards. |
| stage | `bw-shape` | Use when navigating bewater Shape — assumption map, experiments, solution, or requesting the concept gate. |
| gate | `bw-strategy-gate` | Use when bewater Define outputs are in place and a human must decide if the direction is worth exploration resources (G1). |
| gate | `bw-concept-gate` | Use when bewater Shape outputs are in place and a human must decide if the concept is validated enough to invest build resources (G2). |
| capability | `bw-project-charter` | Use when drafting/revising the bewater project charter and seeding first assumptions. |
| capability | `bw-4c-research` | Use when planning/running bewater 4C research and the living learning plan. |
| capability | `bw-insight-craft` | Use when synthesizing raw bewater research into insights and judging them against F/P/E/T. |
| capability | `bw-directional-hypothesis` | Use when composing bewater directional hypotheses (By/We can/Resulting in). |
| capability | `bw-strategy-statement` | Use when writing the bewater innovation strategy + its statement (the choice-cutting blade). |
| capability | `bw-opportunity-area` | Use when carving bewater opportunity areas (2–4, non-overlapping). |
| capability | `bw-concept-card` | Use when generating, filling, and scoring bewater concept cards. |
| capability | `bw-assumption-map` | Use when classifying bewater assumptions, ranking impact×uncertainty, flagging achilles heels (initial inventory OR deep Shape map). |
| capability | `bw-experiment-design` | Use when designing a bewater experiment for an achilles heel, with kill/proceed criteria fixed before running. |
| capability | `bw-investment-narrative` | Use when drafting the bewater investment narrative (6 parts + Solutions 3-segment + per-assumption evidence disclosure). |
| capability | `bw-solution-shape` | Use when shaping a selected concept into the validated bewater solution artifact (dual-sided solution + business case). |

**Folded into references (not skills):** ledger read/write (a `references/ledger-schema.md` documents the YAML + update rules — any skill edits it directly, no single-writer skill); dual-sided check (a section in `references/gate-criteria.md` every capability references); workshop ops (two-worlds switch, creative meeting in `references/workshop.md`).

**Capability → human-converge endpoint (non-delegable stop):** every capability that converges ends "present candidates + state the decision + stop." (charter→lock proposition; insights→which pass F/P/E/T; strategy→pick+lock; concept-card→which advance; assumption-map→which to test first; experiment→kill/proceed; etc.)

---

## 5. State Format (informational; skills read/write directly)

**Config** `_bewater/config.yaml` — `project` name, success criteria, `current_stage`, decision-makers, output paths. Written by `bw-start`; updated as the project advances.

**Ledger** `_bewater/state/assumption-ledger.yaml` — fields per `bewater-core.md` §7.2/§9.8: `id, statement, layer(root|strategy|opportunity|concept|feature), category, impact, uncertainty, evidence_level(L1-L6), validation_status, status(active|killed|merged), evidence_ref, derived_from[], affects[], branch, updated_at`. `is_achilles_heel = impact=high AND uncertainty=high` (derived; the skill computes it when presenting, not stored). **No machine invariants** — the gate checklist asks the human to confirm "achilles heels validated ⟹ evidence ≥ L4" (§7.2).

**Artifacts** `_bewater-output/artifacts/<stage>/*.md` — markdown body + YAML frontmatter: `artifact_id, kind, stage, status(draft|final|superseded), dual_sided{money,magic,tension}, derived_from[], signoffs[]`. Frontmatter is **informational** (skills read it to present evidence; no validator rejects writes). `status: final` + non-empty body = completion evidence the gate checklist looks for.

**Gate records** `_bewater-output/gates/<gate>-<date>.md` — `gate, position, subject, decision_maker, exit(go|conditional-go|recycle|pivot|kill), evidence-checklist-result, conditions[]`. The gate skill writes this AFTER the human picks the exit.

---

## 6. Gate Mechanics (human-decide; skill surfaces evidence)

```
1. Gate skill reads ledger + artifact frontmatter.
2. Presents the evidence checklist (G1/G2 criteria from references/gate-criteria.md, which mirrors bewater-core.md §6.1):
   - for each criterion, surface the relevant items (e.g. "achilles heels on this solution's lineage: A-001 (L4 ✓), A-003 (L3 ✗)") so the human can see pass/fail at a glance.
3. Presents the 5 exits.
4. STOPS. Waits for the human. Never picks an exit.
5. On the human's choice: writes the gate record; performs the exit's action.
```

`go` is withheld in the skill's *presentation* when criteria are visibly unmet (the skill says "evidence incomplete — conditional-go/recycle/pivot/kill"), but the human can overrule (it's their call). This is the trade-off vs v2's machine-guaranteed block — accepted.

**Backtrack** (§6.2): when an assumption is falsified, the relevant capability/gate skill reads its `layer`, recommends the backtrack target (feature|concept→reframe; opportunity|strategy→Define; root→Discover), and surfaces downstream `affects` artifacts to re-check. Routed by the skill, confirmed by the human.

---

## 7. Installer

MVP: `install.sh` (~30 lines bash) symlinks `skills/bw-*` into `~/.claude/skills/` (the Claude Code personal skills path). Idempotent. Later: a proper `.claude-plugin/marketplace.json` for native plugin install. **This is the only code in the toolkit.**

---

## 8. Build, Phasing, Verification

**Phasing (behavioral TDD per `writing-skills` — RED-GREEN-REFACTOR per skill; no batch):**
- **Phase 1 (MVP closed loop):** Immersion → Discover → Define → `bw-strategy-gate` — `bw-start`, 3 routers (immersion/discover/define), `bw-project-charter`, `bw-4c-research`, `bw-insight-craft`, `bw-directional-hypothesis`, `bw-strategy-statement`, `bw-opportunity-area`, `bw-assumption-map`, `bw-strategy-gate` + `install.sh` + references.
- **Phase 2:** `bw-ideate`, `bw-shape`, `bw-concept-card`, `bw-experiment-design`, `bw-investment-narrative`, `bw-solution-shape`, `bw-concept-gate`.

**Verification (behavioral, per skill):**
- Routing evals: correct skill triggers; adjacent skills disambiguated.
- Human-converge stress test: under "just pick one" pressure, the capability still stops + presents candidates; the gate still waits for a human exit.
- G1/G2 E2E on a real proposition: gate surfaces the right evidence; human picks; record written.
- Clean-install smoke test: `install.sh` → fresh project → a `bw-*` skill activates.
- (No unit tests — there's no code except `install.sh`, which gets a one-shot smoke test.)

---

## 9. Why no runtime (the decision)

- **BMAD (the chosen reference) has no methodology runtime** — only skills + an installer; host AI + human execute. bewater "类似 bmad" ⇒ same shape.
- bewater is **human-converge** — a human decides at every gate. The runtime's machine-guaranteed block was redundant with the human block; it pre-computed evidence the skill can surface just as well.
- The runtime added a Python package + venv + tests + install friction on top of a markdown-methodology tool — the same over-scope that stalled `bewater-n`.
- What's lost: deterministic guarantee of invariant enforcement. What's kept: the methodology's full rigor, surfaced to the human via checklists. Net simpler, faithful to "类似 bmad". If a specific gate ever proves to need machine guarantees, add a ~20-line script for just that — YAGNI now.
