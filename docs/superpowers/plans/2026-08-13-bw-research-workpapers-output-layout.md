# BeWater Research Workpapers and Output Layout — Implementation Plan

## Objective

Make Discover behave like a small consulting research workspace without introducing a separate
knowledge-graph product:

- keep one repository bound to one project;
- separate workflow artifacts, original sources, research workpapers, and presentations;
- persist one readable `K-NNN` workpaper for each bounded research question or hypothesis;
- keep the Research Plan focused on learning intent, next-Sprint work, progress, and stop decisions;
- keep `_bewater/evidence.yaml` only as machine state for decision-critical claims and Gate checks;
- make every Discover write validated and resumable so a partial Sprint cannot masquerade as a
  completed knowledge base.

This plan changes toolkit behavior and contracts. It does **not** choose which of the two project
topics currently mixed in the working tree should survive, and it does not rewrite the current
`_bewater/` or `_bewater-output/` state. Runtime-state recovery requires separate authorization after
the code and migration checks are complete.

## Approved decisions

| Area | Decision |
|---|---|
| Project boundary | One repository contains one BeWater project. A different project starts in a different repository or working directory. |
| Canonical research content | Markdown/YAML workpapers are canonical; PPT/PDF files are derived presentation material. |
| Top-level output layout | Use exactly four shallow directories: `artifacts/`, `sources/`, `knowledge/`, and `presentation/`. |
| Research plan | Keep one living Research artifact containing the Learning Plan; do not create a separate Learning Plan artifact. |
| Knowledge model | Use one `K-NNN` research workpaper per bounded question or hypothesis. Findings, analysis, conclusion, limitations, and new questions stay inside that document. |
| Summaries | A Sprint summary is another `K-NNN` workpaper using the same contract and `method: synthesis`; do not create separate Finding or Synthesis object models. |
| Sources | Store user-provided original files under `sources/`. A workpaper may cite a local source path or an exact external URL. Do not add a mandatory source database or source index. |
| Presentation | Store generated PPT/PDF readouts under `presentation/`. They never become canonical state and never replace their source workpapers. |
| Machine evidence | Retain `_bewater/evidence.yaml` for assumptions, L4 obligations, experiments, and Gate validation. It is not the user-facing knowledge repository. |
| Historical state | Never merge evidence or artifacts from unrelated project topics. Never silently reinterpret a historical `RM-NNN` mission ref as Evidence or Knowledge. |

## Non-goals

- No database, vector store, RDF graph, or new service.
- No separate files for atomic Findings, Themes, Clusters, or Insight Ingredients.
- No mandatory source-ingestion pipeline for downloading the web.
- No deep output tree by phase, Sprint, method, or 4C lens.
- No change to human ownership of Gate exits or F/P/E/T signoff.
- No weakening of the L4+ behavioral-evidence requirement.
- No automatic recovery of the currently dirty project state.

## Confirmed failure modes to correct

| Failure | Evidence in the current workspace | Correction |
|---|---|---|
| Two project topics share one state root | Git-tracked state describes hardso/AI hardware; current working files describe an SMB AI-transformation consulting service. | Bind an active repository to its existing Charter/project context and refuse a new unrelated project intake. |
| Research output bypassed canonical artifact allocation | Current files use `RES-001`, while the runtime and persistence contract allocate `ART-NNN`. | Require Research artifacts to use the normal `ART-NNN` counter and validator. |
| Missions were used as evidence | Current Research Plan contains `evidence_refs: [RM-001]`. | Research progress references `knowledge:K-NNN@n`; machine Evidence refs remain `evidence:E-NNN@n`. |
| Conclusions have no source trail | Numeric conclusions were written directly into the Research Plan without exact sources. | Put source refs, analysis, conclusion, and limitations in a `K-NNN` workpaper before updating Research progress. |
| Assessment claims were promoted to known facts | Assessment-derived claims appear as `starting_state: known`. | Assessment content may seed a question only; `answered`/`partial` requires a valid workpaper with independently checked sources. |
| Sprint state was only partially persisted | Research revisions exist, `_bewater/evidence.yaml` is deleted, and `config-after-sprint1.yaml` is stranded. | Validate the complete staged payload and emit one resumable `bwkit plan apply` action. Keep staged files outside project state. |
| Evidence ID has two apparent owners | `config.next_ids.evidence` coexists with `evidence.yaml.next_evidence_id`, which the shared schema calls canonical. | Remove `config.next_ids.evidence`; allocate Evidence only from `evidence.yaml.next_evidence_id`. |
| Output scanners treat all Markdown as workflow artifacts | `validate`, `gate_scan`, and hashing recursively inspect `_bewater-output/**/*.md`. | Restrict artifact consumers to `artifacts/` plus explicit legacy flat-artifact compatibility; exclude `knowledge/`, `sources/`, and `presentation/`. |
| Local verification is easy to bypass | Plain `python` is unavailable and the unconfigured `python3` lacks PyYAML. | Standardize repository verification on `.venv/bin/python` and make the transaction emitter the required validation entry point. |

## Target layout

```text
_bewater/
├── config.yaml
├── ledger.yaml
├── conditions.yaml
├── evidence.yaml                 # created only when machine Evidence exists
└── records/

_bewater-output/
├── artifacts/
│   ├── ART-001-r1-charter.md
│   ├── ART-002-r1-initial-assessment.md
│   └── ART-003-rN-research.md
├── sources/
│   ├── interview-notes.docx
│   ├── market-data.xlsx
│   └── industry-report.pdf
├── knowledge/
│   ├── K-001-smb-willingness-to-pay.md
│   ├── K-002-ai-consulting-five-forces.md
│   └── K-003-sprint-1-summary.md
└── presentation/
    ├── sprint-1-readout.pptx
    └── discover-readout.pdf
```

All four output directories are shallow. Filenames provide enough grouping; no phase or method
subdirectories are introduced in this iteration.

## Minimal contracts

### Workflow artifact

Workflow artifacts remain append-only `ART-NNN-rN-<kind>.md` files. The only path change is that new
artifacts are written under `_bewater-output/artifacts/`.

The Research Plan remains one `kind: research` artifact and owns:

1. **Research Objective** — Charter basis, boundary, and strategic uncertainties.
2. **Learning Plan** — stable `LP-NNN` questions, priority, lens, and decision relevance.
3. **Next Sprint** — bounded `RM-NNN` missions, methods, budgets, dependencies, and stop conditions.
4. **Research Progress** — answer status, exact Knowledge refs, current answer, and remaining gap.
5. **Sprint Decision** — after execution only: `continue`, `deepen`, `redirect`, `synthesize`, or
   `stop`, with rationale and marginal-learning stop rule.
6. **Insight Readiness** — after execution only: handoff readiness and the exact Knowledge refs that
   Define should read.

The Research Plan does not contain full method analyses, source inventories, or copied findings.

### Knowledge workpaper

One workpaper answers one primary research question or tests one primary hypothesis. It may use
multiple complementary methods when they serve that same question.

Path:

```text
_bewater-output/knowledge/K-NNN-<short-title>.md
```

Workpapers are living files. The filename stays stable while the top-level `revision` increases via
CAS. Git history and CAS backups preserve prior text; no `K-NNN-rN` file fan-out is required.

Minimal frontmatter:

```yaml
---
schema_version: 1
knowledge_id: K-001
revision: 1
branch_id: BR-001
title: SMB willingness to pay
research_ref: artifact:ART-003@1
learning_refs: [LP-001]
source_refs:
  - _bewater-output/sources/pricing-interviews.docx
  - https://exact-source.example/report
evidence_refs: []
status: working
---
```

Required body:

```markdown
# <Title>

## Question or hypothesis

## Method and scope

## Sources used

## Analysis

## Conclusion

## Limitations and new questions
```

Rules:

- `status` is `working` or `complete`.
- A complete workpaper has a non-empty conclusion and names material limitations.
- `source_refs` contains stable local paths or exact URLs; invented or repaired URLs are forbidden.
- `evidence_refs` is optional in substance and may be empty. Populate it only when atomic claims are
  promoted into `_bewater/evidence.yaml` for assumptions, experiments, or Gates.
- Five Forces, market sizing, competitor analysis, interview synthesis, and similar methods use the
  same workpaper structure. The method's full intermediate analysis stays in `## Analysis`.
- A Sprint summary uses the same contract, cites the contributing `knowledge:K-NNN@n` refs in its
  Sources/Analysis sections, and records `method: synthesis` in `## Method and scope`. It is not a new
  artifact kind.

### Research Progress row

Replace `evidence_refs` in the Research Plan's Knowledge Base Index with `knowledge_refs` and rename
the section to **Research Progress**:

```yaml
- learning_ref: LP-001
  answer_status: partial
  knowledge_refs:
    - knowledge:K-001@2
  current_answer: Buyers pay for bounded, measurable deliverables; subscription renewal is unknown.
  remaining_gap: China SMB price acceptance and renewal behavior remain untested.
```

Rules:

- `knowledge_refs` accepts only exact `knowledge:K-NNN@n` revisions that resolve on the same branch.
- `answered` and `partial` require at least one complete Knowledge workpaper.
- `not-researched`, `dropped`, and `gap-accepted` may have no Knowledge ref, but the reason or gap must
  remain explicit.
- `RM-NNN` is an activity identifier and is never valid in `knowledge_refs` or `evidence_refs`.
- Assessment text alone cannot justify `answered`, `partial`, or a `known` starting state.

### Sources

- User-provided originals may be copied into `_bewater-output/sources/` without conversion.
- Preserve the original extension and content. Use a descriptive filename and avoid duplicates.
- Web material may stay external; record the exact URL and source location in the workpaper.
- Sensitive interview material must be minimized, anonymized when required, and used only within the
  participant's consent. This plan does not add a permissions system.
- Sources are not parsed as workflow artifacts and receive no `ART-NNN` identity.

### Presentation

- A presentation is generated from exact Knowledge and Artifact revisions.
- Store PPT/PDF files directly under `_bewater-output/presentation/`.
- A Sprint readout should contain a short method/scope introduction, the main conclusions, their
  implications, limitations, and next questions.
- Record contributing `K-NNN` refs in slide notes or a source appendix.
- Presentations do not update the ledger, satisfy Evidence obligations, or become inputs to Define.
- A failed presentation render never rolls back already-valid Knowledge; it is safe to regenerate.

### Machine Evidence

`_bewater/evidence.yaml` remains the canonical atomic-claim store used by the assumption ledger,
experiments, and Gates. It is deliberately not mirrored as many user-facing files.

- Evidence IDs are allocated only from `evidence.yaml.next_evidence_id`.
- A Knowledge workpaper may cite exact `evidence:E-NNN@n` records.
- A claim that changes an assumption, opens/closes an L4 obligation, or supports a Gate must be
  normalized into Evidence before that state change.
- Other research details may remain source-bounded inside the workpaper.
- Removing the user-facing atomic-Evidence layer does not remove machine Evidence or relax L4.

## Target Discover flow

```text
Charter
  -> Research Plan r1
       - Learning Plan
       - Next Sprint
       - Research Progress: not researched
  -> execute one bounded mission
  -> save/cite originals in sources/
  -> write or revise K-NNN workpaper
       - question/hypothesis
       - method
       - sources
       - analysis
       - conclusion
       - limitations/new questions
  -> normalize only decision-critical atomic claims into evidence.yaml
  -> write Research Plan rN
       - progress references exact K revision
       - next Sprint or stop decision
       - Insight Readiness when met
  -> generate optional Sprint/Discover readout under presentation/
```

The Sprint terminates based on marginal strategic learning, not because no new questions exist.
New questions are triaged inside the workpaper and either enter the next Learning Plan revision,
remain a documented gap, move outside the Charter boundary, or are dropped as decision-irrelevant.

## Project-binding and write-safety rules

1. `bwkit init` remains create-only and byte-preserving when valid state already exists.
2. The first successful Charter commit must set a non-empty `config.project.name` in the same
   resumable action.
3. When a Charter already exists, `bw-immersion` resumes or revises that Charter. It never treats a
   new unrelated request as a fresh project inside the same repository.
4. If the user explicitly wants a different project, the router stops and directs them to a new
   repository or working directory. It does not delete, reset, or archive the current project.
5. New Research artifacts use `ART-NNN`; Knowledge uses `K-NNN`; their counters are independent.
6. Add `next_ids.knowledge` to config. Remove `next_ids.evidence` after a compatibility migration;
   `evidence.yaml.next_evidence_id` remains authoritative.
7. Draft payloads are created in a `mktemp` directory outside `_bewater/` and `_bewater-output/`.
8. The transaction validator runs before `emit_write_plan.py` emits any plan.
9. One resumable action writes Knowledge, the next Research revision, optional Evidence/Ledger CAS,
   and any required config counter CAS. A retry either skips identical completed steps or reports a
   conflict.
10. Presentation generation happens only after the canonical research action succeeds.

## Compatibility and migration

### New projects

`bwkit init` creates:

```text
_bewater-output/artifacts/
_bewater-output/sources/
_bewater-output/knowledge/
_bewater-output/presentation/
```

It also initializes `next_ids.knowledge: 1` and no longer initializes
`next_ids.evidence`.

### Existing valid projects

- Readers temporarily accept workflow artifacts in both the legacy flat `_bewater-output/` root and
  the new `artifacts/` directory.
- Writers always use the new directories.
- Artifact scanners explicitly ignore `sources/`, `knowledge/`, and `presentation/`.
- A migration command supports a read-only `--check` mode and an explicit `--apply` mode.
- Migration moves only recognized canonical workflow artifacts into `artifacts/`; it never guesses
  that an arbitrary Markdown file is an artifact.
- Migration adds `next_ids.knowledge` and removes the redundant config Evidence counter without
  changing `evidence.yaml.next_evidence_id`.
- Existing `_bewater/evidence.yaml`, ledger records, revisions, and hashes remain unchanged.

### Current mixed workspace

The current workspace must fail the migration preflight because it contains two incompatible project
families and uncommitted deletions/replacements. The migration command should report, without
writing:

- the bound/current Charter identity;
- competing Charter/research families detected from Git and working files;
- flat artifacts eligible for layout migration;
- unresolved `RM-NNN` refs used as Evidence;
- missing or deleted Evidence state;
- stranded staged files such as `config-after-sprint1.yaml`.

Choosing which project family to preserve is a separate human decision. No implementation task in
this plan may resolve it automatically.

## Implementation tasks

Implementation changes more than three files, so execute it with Agent collaboration as required by
the repository instructions. Keep one writer per bounded file set and integrate through the primary
agent.

### Task 1 — Lock the shallow layout with RED tests

**Tests first**

- Modify `tests/test_bwkit_init.py`.
- Modify `tests/test_io.py`.
- Add `tests/test_output_layout.py`.

Add failing tests proving:

- fresh init creates exactly the four shallow output directories;
- config contains `next_ids.knowledge: 1` and omits `next_ids.evidence`;
- a valid re-init is a byte-for-byte no-op;
- `paths.artifacts_dir`, `sources_dir`, `knowledge_dir`, and `presentation_dir` resolve correctly;
- Artifact iteration ignores Markdown under Knowledge and Sources;
- legacy flat canonical artifacts remain readable during migration.

**Implementation**

- Modify `src/bw/paths.py`.
- Modify `src/bwkit/init.py`.
- Update the deployed runtime copy only through the normal installer/redeployment flow; do not hand
  edit `_bewater/bwkit/`.

**Verify**

```bash
.venv/bin/python -m pytest tests/test_bwkit_init.py tests/test_io.py tests/test_output_layout.py
```

### Task 2 — Keep Knowledge out of Artifact scanning

**Tests first**

- Modify `tests/test_validate.py`.
- Modify `tests/test_gate_scan.py`.
- Modify `tests/test_hashing.py`.
- Modify `tests/test_ledger_ops.py` where artifact discovery is exercised.

Add failing fixtures containing:

- a valid Artifact under `artifacts/`;
- a valid `K-NNN` Markdown workpaper under `knowledge/`;
- a Markdown source note under `sources/`;
- a legacy flat Artifact.

Assert that validation, hashing, Gate scans, and baseline collection read only the two Artifact
locations and never parse Knowledge/Source Markdown as `ArtifactMeta`.

**Implementation**

- Modify `src/bw/validate.py`.
- Modify `src/bw/gate_scan.py`.
- Modify `src/bw/hashing.py`.
- Modify `src/bw/ledger_ops.py`.
- Reuse a single path iterator from `src/bw/paths.py`; do not maintain four slightly different
  recursive scanners.

**Verify**

```bash
.venv/bin/python -m pytest tests/test_validate.py tests/test_gate_scan.py tests/test_hashing.py tests/test_ledger_ops.py
```

### Task 3 — Add the one-file Knowledge workpaper contract

**Tests first**

- Add `tests/test_knowledge_workpaper_validator.py`.

Cover:

- valid working and complete workpapers;
- stable `K-NNN` IDs and positive revisions;
- exact Research and Learning refs;
- local source path resolution and exact external URLs;
- required headings;
- complete status with empty conclusion;
- missing limitations;
- malformed Evidence refs;
- branch mismatch;
- in-place revision bump and stale-CAS conflict.

**Implementation**

- Add `src/skills/bw-discovery-research/references/knowledge-workpaper.md`.
- Add `src/skills/bw-discovery-research/scripts/validate_knowledge_workpaper.py`.
- Keep the validator deterministic and file-based. Do not add a Knowledge database or global index.

**Verify**

```bash
.venv/bin/python -m pytest tests/test_knowledge_workpaper_validator.py
```

### Task 4 — Simplify the Research Plan around Knowledge refs

**Tests first**

- Modify `tests/test_research_plan_validator.py`.
- Modify `tests/test_skill_bw_discovery_research.py`.

Replace old expectations with:

- `Research Progress` owns answer status;
- exact `knowledge:K-NNN@n` refs resolve to complete workpapers on the same branch;
- `answered`/`partial` without Knowledge fails;
- `RM-NNN` in a Knowledge or Evidence field fails;
- Assessment-derived candidate questions cannot be `known` or answered without independent
  Knowledge;
- Research artifacts require `ART-NNN` identity;
- full analysis and source inventories are absent from the Research Plan;
- Sprint Decision and Insight Readiness cite the relevant Knowledge refs.

**Implementation**

- Modify `src/skills/bw-discovery-research/references/research-plan.md`.
- Modify `src/skills/bw-discovery-research/scripts/validate_research_plan.py`.
- Modify `src/skills/bw-discovery-research/SKILL.md`.
- Modify `src/skills/bw-discover/SKILL.md` and `references/stage.md` only for status terminology and
  routing; keep the router read-only.

**Verify**

```bash
.venv/bin/python -m pytest tests/test_research_plan_validator.py tests/test_skill_bw_discovery_research.py tests/test_skill_bw_discover.py
```

### Task 5 — Emit one validated, resumable Sprint action

**Tests first**

- Extend `tests/test_research_plan_validator.py` or add
  `tests/test_discovery_research_transaction.py`.
- Modify `tests/test_bwkit_applier.py` only if new generic behavior is required.

Cover transactions that:

- allocate the first `K-NNN` through config CAS;
- write a new workpaper and Research revision together;
- revise an existing workpaper through CAS without allocating a new ID;
- optionally create/update Evidence and Ledger in the same plan;
- omit Evidence and Ledger steps when no decision-critical claim changes;
- reject a missing Knowledge ref, invalid source path, stale config revision, stale Research head,
  branch mismatch, or `RM-NNN` masquerading as evidence;
- can resume after an already-applied identical step;
- never write `config-after-sprint*.yaml` or other staged files into project state.

**Implementation**

- Modify `src/skills/bw-discovery-research/scripts/emit_write_plan.py`.
- Modify `src/skills/bw-discovery-research/references/persistence-plan.md`.
- Reuse `bwkit plan apply`; do not add a second transaction engine.
- Keep temporary candidate files in a `mktemp` directory supplied to the emitter.

**Verify**

```bash
.venv/bin/python -m pytest tests/test_discovery_research_transaction.py tests/test_bwkit_applier.py
```

### Task 6 — Preserve the hidden Evidence/Gate contract

**Tests first**

- Modify `tests/test_schema.py`.
- Modify `tests/test_gate_scan.py`.
- Modify `tests/test_skill_bw_assumption_map.py` as needed.

Prove that:

- Evidence allocation uses only `evidence.yaml.next_evidence_id`;
- a Knowledge workpaper alone does not close an L4 obligation;
- decision-critical claims must resolve to exact Evidence before an assumption becomes supported;
- equivalent Evidence/Ledger state produces the same G1/G2 result before and after the layout
  change;
- a missing presentation never affects a Gate.

**Implementation**

- Modify `src/skills/_bw-shared/ledger-schema.md`.
- Modify only the minimum runtime/schema code needed to remove the redundant config Evidence
  counter. Do not replace `evidence.yaml` with Knowledge workpapers.

**Verify**

```bash
.venv/bin/python -m pytest tests/test_schema.py tests/test_gate_scan.py tests/test_skill_bw_assumption_map.py
```

### Task 7 — Add presentation-as-projection guidance

**Tests first**

- Add or modify deterministic skill-contract tests in `tests/test_skill_bw_discovery_research.py`.

Assert that the skill:

- persists Knowledge before presentation generation;
- treats presentation as optional/derived and non-blocking;
- writes it only under `presentation/`;
- cites exact Knowledge refs in notes or an appendix;
- does not read PPT/PDF as the canonical Define handoff.

**Implementation**

- Add a concise presentation section to `bw-discovery-research/SKILL.md` or a small directly linked
  reference if the main skill would become hard to scan.
- Do not create a presentation-specific BeWater artifact kind.

**Verify**

```bash
.venv/bin/python -m pytest tests/test_skill_bw_discovery_research.py
```

### Task 8 — Protect the one-repository/one-project boundary

**Tests first**

- Modify `tests/test_skill_bw_immersion.py`.
- Modify `tests/test_bwkit_init.py`.
- Add an eval scenario where an existing project receives unrelated new-project intent.

Assert that:

- existing state is preserved byte-for-byte by init;
- an existing Charter routes to resume/revise, never fresh replacement;
- the first Charter transaction sets a non-empty project name;
- unrelated project intent stops with guidance to use a new repository/directory;
- no Charter, Ledger, Conditions, Evidence, or Artifact is deleted or reset.

**Implementation**

- Modify `src/skills/bw-immersion/SKILL.md` and its persistence validator/emitter.
- Modify `src/bwkit/init.py` only where mechanical enforcement is possible.
- Keep semantic project-mismatch judgment at the capability boundary; do not invent a fragile text
  similarity score.

**Verify**

```bash
.venv/bin/python -m pytest tests/test_skill_bw_immersion.py tests/test_bwkit_init.py
```

### Task 9 — Add explicit output-layout migration tooling

**Tests first**

- Add `tests/test_output_layout_migration.py`.

Cover:

- clean legacy flat project dry run;
- explicit apply moving canonical Artifacts only;
- idempotent second run;
- preservation of hashes, bytes, ledger, Evidence, and records;
- conflict when destination exists with different bytes;
- rejection of mixed project families;
- rejection of dirty or missing Evidence dependencies;
- no write in `--check` mode or on any failed precondition.

**Implementation**

- Add a narrowly scoped `bwkit` migration module and CLI command.
- Do not run migration from the installer.
- Require an explicit apply flag and produce a human-readable inventory before writing.

**Verify**

```bash
.venv/bin/python -m pytest tests/test_output_layout_migration.py tests/test_cli_wiring.py
```

### Task 10 — Update installer, deployed skills, documentation, and evals

**Tests first**

- Modify `tests/test_installer_copy.py` and `tests/test_installer_link.py`.
- Update Discover eval scenarios to assert Knowledge persistence and prohibit `RM-NNN` Evidence
  refs.

**Implementation**

- Update `README.md` and `CLAUDE.md` architecture diagrams.
- Update relevant Discover eval fixtures and scenarios.
- Regenerate `.claude/skills/` from `src/skills/` using the normal deployment path.
- Never copy or hand-edit the active project's `_bewater/` state during deployment.

**Verify**

```bash
.venv/bin/python -m pytest tests/test_installer_copy.py tests/test_installer_link.py tests/test_skill_bw_discovery_research.py
diff -qr src/skills/bw-discovery-research .claude/skills/bw-discovery-research
```

### Task 11 — Full verification and current-state audit

Run:

```bash
.venv/bin/python -m pytest --cov=bw --cov=bwkit --cov-report=term-missing
.venv/bin/python scripts/verify.py
git diff --check
```

Acceptance requirements:

- all tests pass;
- combined runtime coverage remains at least 80%;
- `src/skills/` and deployed managed skill copies match;
- no new temporary or backup files are tracked;
- no current `_bewater/` or `_bewater-output/` business data was changed by the implementation test
  run;
- read-only migration audit of the current workspace reports the mixed-project conflict and performs
  no write.

Stop after reporting that audit. Ask the accountable human which project family to preserve before
any real-state migration, deletion, restoration, or move.

## Acceptance scenarios

### A. Five Forces research

1. LP-005 asks whether industry structure leaves an attractive entry position.
2. RM-005 selects Five Forces plus source triangulation.
3. Original reports are stored or cited under Sources.
4. `K-002-ai-consulting-five-forces.md` preserves all five forces, source trail, analysis,
   conclusion, limitations, and new questions.
5. Research Progress references `knowledge:K-002@1` and carries only the bounded current answer.
6. A Sprint readout summarizes the conclusion and cites `K-002`; it does not become the knowledge
   source.

### B. New questions after a Sprint

1. A complete workpaper produces three new questions.
2. Only a strategy-changing, currently answerable question enters the next Learning Plan.
3. A valuable but inaccessible question remains in Limitations/new questions and Research Progress
   as a gap.
4. A decision-irrelevant question is dropped with rationale.
5. Discover may still reach Insight Readiness when further immediate research has low marginal
   strategic value.

### C. Gate-critical finding

1. A workpaper concludes that a high/high assumption is contradicted.
2. The Coordinator normalizes the exact source-bounded claim into Evidence.
3. The Knowledge workpaper cites that Evidence revision.
4. The Ledger update and Research revision are emitted in the same resumable action.
5. L4/Gate behavior follows Evidence and Ledger state, not the PPT summary.

### D. Unrelated project request

1. A repository already contains a current Charter and active state.
2. The user asks to start an unrelated consulting project.
3. Immersion reports that the repository is already bound.
4. No files change.
5. The user is directed to create a separate repository or working directory.

## Final design check

- Four output directories only.
- One Research Plan with embedded Learning Plan.
- One Knowledge document type only.
- No standalone Finding, Synthesis, Source-index, or Presentation artifact models.
- Sources remain original materials.
- Presentations remain derived communication outputs.
- Machine Evidence remains hidden state because Gate correctness requires it.
- Current mixed project data remains untouched until a separate human recovery decision.
