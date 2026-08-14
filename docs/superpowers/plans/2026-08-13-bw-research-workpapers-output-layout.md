# BeWater Research Workpapers and Output Layout — Implementation Plan

## Objective

Make Discover behave like a small consulting research workspace without introducing a separate
knowledge-graph product:

- keep one repository bound to one project;
- separate workflow artifacts, living research workpapers, referenced research materials, and
  user-controlled presentations;
- persist one readable `K-NNN` workpaper for each bounded research question or hypothesis;
- keep the Research Plan focused on learning intent, next-Sprint work, progress, and stop decisions;
- keep `_bewater/evidence.yaml` only as machine state for decision-critical claims and Gate checks;
- make every canonical Discover state write validated and resumable so a partial Sprint cannot
  masquerade as completed research.

This plan changes toolkit behavior and contracts. It does **not** choose which of the two project
topics currently mixed in the working tree should survive, and it does not rewrite the current
`_bewater/` or `_bewater-output/` state. Runtime-state recovery requires separate authorization after
the code and migration checks are complete.

## Approved decisions

| Area | Decision |
|---|---|
| Project boundary | One repository contains one BeWater project. A different project starts in a different repository or working directory. |
| Workflow document versioning | One logical `ART-NNN` Artifact or `EXP-NNN` Experiment has append-only immutable revision files. This existing Gate, signoff, lineage, and backtrack contract does not change. |
| Knowledge versioning | One `K-NNN` question has one stable Markdown file. Its frontmatter `revision` advances in place through CAS; it does not fan out into `K-NNN-rN` files. |
| Canonical research content | Workflow Artifacts and Knowledge workpapers are canonical. Files under `sources/` are referenced research materials, not workflow state. PPT/PDF in `docs/` are user-controlled and non-canonical. |
| Top-level output layout | Use three shallow directories under `_bewater-output/`: canonical `artifacts/` and `knowledge/`, plus supporting `sources/`. Presentation materials belong under `docs/` (user-controlled, non-canonical). |
| Research plan | Keep one living Research artifact containing the Learning Plan; do not create a separate Learning Plan artifact. |
| Knowledge model | Use one `K-NNN` research workpaper per bounded question or hypothesis. Lightweight: summary + conclusion, with detailed analysis optionally in `sources/`. |
| Summaries | A Sprint summary is another `K-NNN` workpaper using the same contract and `method: synthesis`; do not create separate Finding or Synthesis object models. |
| Sources | Store byte-preserved user material and process-generated supporting material under `sources/`. Host tools may read or create those files; `bwkit` never executes, parses, copies, versions, or writes them. |
| Knowledge history | Runtime validation resolves only the Knowledge revisions pinned by the current Research head. Git preserves older workpaper text; CAS backups are recovery files, not a revision store. |
| Presentation | Generated PPT/PDF readouts belong under `docs/presentations/` (outside `_bewater-output/`). They are user-controlled, non-canonical, and never become inputs to Define or Gates. The methodology does not manage them. |
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
- No methodology-controlled presentation layer — PPT/PDF generation is user-directed, not workflow-managed.
- No separation of `sources/` vs `resources/` — all research materials (original + process-generated) go in `sources/`.
- No binary-file operation or source-ingestion pipeline in `bwkit`.
- No replacement of the append-only Workflow Artifact or Experiment revision model.

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
| Output scanners treat all Markdown as workflow artifacts | `validate`, `gate_scan`, and hashing recursively inspect `_bewater-output/**/*.md`. | Restrict artifact consumers to `artifacts/` plus explicit legacy flat-artifact compatibility; exclude `knowledge/` and `sources/`. (`docs/` is outside scope.) |
| Flat workflow-document paths are embedded across skills | Writers and templates still name `_bewater-output/ART-...` and `_bewater-output/EXP-...`. | Update every managed Artifact/Experiment writer and template to use `artifacts/`, and add a repository-wide contract test so the old paths cannot return. |
| Source persistence is ambiguous | The draft groups DOCX/PDF with canonical state even though `bwkit plan apply` is text-only. | Prepare Sources outside `bwkit`; validate path and checksum before emitting the canonical Knowledge/Research action. |
| Stable Knowledge files conflict with historical pins | Replacing `K-001.md` in place removes the runtime copy of prior text. | Resolve exact Knowledge pins only for the current Research head and use Git for historical workpaper recovery; never treat CAS backups as durable history. |
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
├── artifacts/                     # canonical ART/EXP workflow documents, append-only revisions
│   ├── ART-001-r1-charter.md
│   ├── ART-002-r1-initial-assessment.md
│   ├── ART-003-rN-research.md
│   └── EXP-001-rN-experiment.md
├── sources/                       # referenced materials; never parsed or written by bwkit
│   ├── interview-notes.docx
│   ├── market-data.xlsx
│   ├── industry-report.pdf
│   └── detailed-five-forces-analysis.pdf   # process-generated intermediate work
└── knowledge/                     # canonical living workpapers; one stable file per K-NNN
    ├── K-001-smb-willingness-to-pay.md
    ├── K-002-ai-consulting-five-forces.md
    └── K-003-sprint-1-summary.md

docs/                              # user-controlled (optional git, human-consumed)
└── presentations/                 # generated PPT/PDF (methodology does not manage)
    ├── sprint-1-readout.pptx
    └── discover-readout.pdf
```

The three top-level output directories are shallow. An optional `artifacts/archive/` may hold
superseded Artifact revisions under the existing explicit archival contract; it is operational
storage, not phase grouping. `docs/` is user-controlled, and the methodology does not generate or
validate its contents. No phase, Sprint, method, or 4C subdirectories are introduced.

## Minimal contracts

### Workflow artifact

Workflow Artifacts and Experiments remain append-only `ART-NNN-rN-<kind>.md` and
`EXP-NNN-rN-experiment.md` files. One ID denotes one logical document, while each physical file is an
immutable revision snapshot linked through `supersedes_ref`. Their versioning does not change; new
revisions simply move from the flat output root to `_bewater-output/artifacts/`.

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

The default is lightweight: keep a decision-relevant summary and conclusion in the workpaper, and
put detailed supporting analysis in `sources/` only when it materially improves auditability or
reuse.

Path:

```text
_bewater-output/knowledge/K-NNN-<short-title>.md
```

Workpapers are living files. The filename stays stable while the top-level `revision` increases via
CAS. Git history preserves prior text. CAS backups support short-term write recovery only and are
never used to resolve a `knowledge:K-NNN@n` reference. No `K-NNN-rN` file fan-out is allowed.

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
  - path: _bewater-output/sources/pricing-interviews.docx
    sha256: <lowercase-hex-digest>
  - path: _bewater-output/sources/detailed-pricing-analysis.pdf
    sha256: <lowercase-hex-digest>
  - url: <exact URL returned by the research source>
knowledge_refs: []
evidence_refs: []
status: working
---
```

Required body (lightweight structure):

```markdown
# <Title>

## Question or hypothesis

## Method and scope

## Sources used
[Links to source_refs; detailed reports in sources/ can be referenced here]

## Summary
[Concise findings. Summarize material framework dimensions and point to a detailed source report
when one exists.]

## Conclusion
[The direct answer to the question, with confidence level]

## Limitations and new questions
```

**Rules:**

- `status` is `working` or `complete`.
- A complete workpaper has non-empty Summary and Conclusion sections, and names material limitations.
- A local `source_refs` entry contains a repo-relative path under `_bewater-output/sources/` plus the
  file's SHA-256. The validator reads bytes only to check existence and digest; it does not parse or
  execute the file. A URL entry preserves the exact retrieved URL. Invented or repaired URLs are
  forbidden.
- `knowledge_refs` is empty for a primary workpaper. A synthesis workpaper uses it for exact
  `knowledge:K-NNN@n` inputs and never mislabels those inputs as Source files.
- `evidence_refs` is optional in substance and may be empty. Populate it only when atomic claims are
  promoted into `_bewater/evidence.yaml` for assumptions, experiments, or Gates.
- Keep analysis in `## Summary` by default. For complex framework outputs, either summarize the
  bounded analysis inline or reference a detailed supporting report under `sources/`.
- A Sprint summary uses the same contract, cites the contributing `knowledge:K-NNN@n` refs in its
  `knowledge_refs` and Summary, and records `method: synthesis` in `## Method and scope`. It is not a
  new artifact kind.
- There is exactly one file for each `knowledge_id`. A first revision uses `write_new`; every later
  revision uses CAS against the same path. The filename remains stable even if the title changes.
- `research_ref` pins the Research revision whose approved mission caused this workpaper revision;
  `learning_refs` resolve inside that pinned plan. It is provenance, not a pointer that chases the
  newly appended Research head, which avoids a circular write dependency.
- Runtime resolution is current-head only: a Knowledge pin in the current Research head must match
  the current workpaper revision on the same branch. Historical Research revisions remain immutable
  audit snapshots and are not re-resolved against the live Knowledge head.
- The current Research head's Knowledge closure is consistent: every synthesis workpaper it cites
  must also pin the current revisions of its contributing workpapers. Revising an input workpaper
  therefore revises or removes any affected current synthesis workpaper in the same action.
- Revising a Knowledge file that the current Research head references requires a new immutable
  Research Artifact revision pinning the new Knowledge revision in the same resumable action.

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
- This resolution rule applies to the current Research Artifact head. Older Research Artifact
  revisions are checked for Artifact-chain integrity but do not force the live K file back to an old
  revision.
- `answered` and `partial` require at least one complete Knowledge workpaper.
- `not-researched`, `dropped`, and `gap-accepted` may have no Knowledge ref, but the reason or gap must
  remain explicit.
- `RM-NNN` is an activity identifier and is never valid in `knowledge_refs` or `evidence_refs`.
- Assessment text alone cannot justify `answered`, `partial`, or a `known` starting state.

### Sources

`sources/` stores research materials, both original and process-generated:

- **Original materials** (user-provided, first-hand): interview notes, industry reports, market data, financial documents, survey responses
- **Process-generated materials** (supporting work from research execution): detailed framework analyses (Five Forces full report), competitive comparison tables, and market sizing models

Design principles:

- All material copied into the repository goes in `sources/`; there is no separate `resources/`
  directory.
- Preserve the bytes and extension of the repository copy. Any required minimization or
  anonymization happens before import. Use a descriptive filename and avoid duplicates.
- Web material may stay external; record the exact URL and source location in the workpaper.
- Sensitive interview material must be minimized, anonymized when required, and used only within the
  participant's consent. This plan does not add a permissions system.
- Host tools, not `bwkit`, read, copy, or generate Source files. `bwkit plan apply` receives no Source
  step and remains text-only.
- Before emitting a Knowledge/Research action, the workpaper validator checks every local Source
  path and SHA-256. Missing or changed bytes fail closed before canonical state changes.
- Sources receive no `ART-NNN` identity, revision field, CAS operation, or Artifact parsing.
- A failed canonical transaction may leave an unreferenced Source file. It is not completed research;
  a read-only audit may report it, and no automatic cleanup occurs.
- Changing a referenced Source's bytes requires a new Knowledge revision with the new digest.

### Presentation (moved to docs/)

Presentations are **user-controlled, non-canonical materials**. They live outside `_bewater-output/`:

The following is non-binding communication guidance, not a validated methodology contract:

- Location: `docs/presentations/` (or any user-chosen path under `docs/`)
- User-generated or separately generated PPT/PDF files are derived from exact Knowledge and Artifact
  revisions.
- A Sprint readout should contain a short method/scope introduction, the main conclusions, their
  implications, limitations, and next questions.
- Record contributing `K-NNN` refs in slide notes or a source appendix.
- Presentations do **not** update the ledger, satisfy Evidence obligations, or become inputs to Define or Gates.
- A failed presentation render never rolls back already-valid Knowledge; it is safe to regenerate.
- The methodology does **not** manage, validate, or track presentation files. They are optional, user-directed outputs.

### Machine Evidence

`_bewater/evidence.yaml` remains the canonical atomic-claim store used by the assumption ledger,
experiments, and Gates. It is deliberately not mirrored as many user-facing files.

- Evidence IDs are allocated only from `evidence.yaml.next_evidence_id`.
- A Knowledge workpaper may cite exact `evidence:E-NNN@n` records.
- A claim that changes an assumption, opens/closes an L4 obligation, or supports a Gate must be
  normalized into Evidence before that state change.
- Other research details may remain source-bounded inside the workpaper.
- Removing the user-facing atomic-Evidence layer does not remove machine Evidence or relax L4.

### Discover → Define Handoff (Insight Ingredients)

After Sprint execution, the current Research Plan may contain an
`## Insight Ingredients and Insight Readiness` section. It gives Define traceable synthesis inputs
without taking over `bw-insight-craft`'s ownership of Insight generation and F/P/E/T judgment.

Minimal structure:

```markdown
## Insight Ingredients and Insight Readiness

### Direct observations
| Observation or exact quote | Context | Knowledge ref |
|---|---|---|

### Patterns, tensions, and anomalies
| Candidate synthesis | Supporting and disconfirming refs | Limitation |
|---|---|---|

### Challenged beliefs and reframe candidates
| Existing belief or frame | Challenge | Candidate reframe | Knowledge refs |
|---|---|---|---|

### Blind spots and strategic relevance
- Covered lenses:
- Material gaps and what each may change:
- Future OA or strategy judgments this research may inform:

### Insight Readiness
- Status: ready | not-ready
- Rationale:
- Knowledge refs for Define:
```

Rules:

- The section is execution-only and omitted before the first Sprint.
- Every observation and synthesis row cites exact current-head `knowledge:K-NNN@n` refs. Direct
  quotes remain exact excerpts, not reconstructed wording.
- Tensions may distinguish surface, organizational, and root levels when the evidence supports those
  levels; no fixed depth or quota is required.
- Anomalies and reframe candidates are optional. Absence is stated plainly rather than filled with a
  placeholder.
- A Fact-to-pattern reasoning chain may be included when it materially reduces Define rework, but it
  remains synthesis provenance, not an Insight candidate or F/P/E/T judgment.
- The blind-spot check covers 4C plus any challenge-specific lens and states what each material gap
  may change.
- Insight Readiness is a Coordinator handoff judgment, not a human Gate. Research does not generate
  or pre-approve Insights; `bw-insight-craft` owns that transformation.

## Target Discover flow

```text
Charter
  -> Research Plan r1
       - Learning Plan
       - Next Sprint
       - Research Progress: not researched
  -> execute one bounded mission
  -> host tools save or generate supporting files in sources/
  -> preflight local Source paths and SHA-256 values
  -> write or CAS-revise the stable K-NNN workpaper
       - question/hypothesis
       - method
       - sources
       - summary
       - conclusion
       - limitations/new questions
  -> normalize only decision-critical atomic claims into evidence.yaml
  -> append Research Plan rN in the same resumable action
       - progress references exact K revision
       - next Sprint or stop decision
       - Insight Ingredients and Insight Readiness (handoff to Define)
```

A user may create a Sprint or Discover readout under `docs/` afterward. That optional presentation
step is outside the methodology transaction.

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
5. New Research Artifacts use `ART-NNN` and append immutable revision files under `artifacts/`.
   Knowledge uses stable `K-NNN` files under `knowledge/`; their counters are independent.
6. Add `next_ids.knowledge` to config. Remove `next_ids.evidence` after compatibility migration;
   `evidence.yaml.next_evidence_id` remains authoritative.
7. Draft payloads are created in a `mktemp` directory outside `_bewater/` and `_bewater-output/`.
8. Source preparation happens before the canonical action. The validator checks local paths and
   digests, but the emitted `bwkit` plan contains no Source operation.
9. The transaction validator identifies the unique current Research head and current K files before
   `emit_write_plan.py` emits any plan. It validates only current-head Knowledge pins.
10. One resumable action orders: Knowledge `write_new` or CAS, immutable Research `write_new`,
    optional Evidence/Ledger CAS, and required config counter CAS. A retry skips byte-identical
    completed steps or reports a conflict.
11. If execution stops after the Knowledge step, the unchanged Research head prevents the partial K
    revision from masquerading as completed progress. Retrying the identical action must finish the
    Research revision; unrelated new work must fail on the head mismatch.
12. Allocating a new K ID writes the Knowledge file before advancing the config counter. An occupied
    counter value is therefore recoverable only by resuming the identical action, never by silently
    allocating the same ID to different content.

## Compatibility and migration

### New projects

`bwkit init` creates:

```text
_bewater-output/artifacts/
_bewater-output/sources/
_bewater-output/knowledge/
```

It also initializes `next_ids.knowledge: 1` and no longer initializes
`next_ids.evidence`. `docs/` is user-created when needed.

### Existing valid projects

- Readers temporarily accept workflow artifacts in both the legacy flat `_bewater-output/` root and
  the new `artifacts/` directory. Compatibility also reads recognized revisions from the legacy
  `_bewater-output/archive/` and the optional new `artifacts/archive/`.
- Writers always use the new directories.
- Artifact scanners inspect `artifacts/` recursively, the legacy flat root non-recursively, and the
  two explicit archive locations. They never recurse through the project root and explicitly ignore
  `sources/` and `knowledge/`. (`docs/` is outside scope.)
- A migration command supports a read-only `--check` mode and an explicit `--apply` mode.
- Migration moves only recognized canonical ART/EXP workflow documents into `artifacts/`; it never
  guesses that an arbitrary Markdown file is an Artifact or Experiment.
- Migration moves recognized legacy archived revisions to `artifacts/archive/` without renaming or
  changing bytes.
- Migration adds `next_ids.knowledge` and removes the redundant config Evidence counter without
  changing `evidence.yaml.next_evidence_id`.
- Existing `_bewater/evidence.yaml`, ledger records, revisions, and hashes remain unchanged.
- No existing file is converted into a Knowledge workpaper automatically.

### Current mixed workspace

The current workspace must fail migration preflight because relevant state and output paths contain
uncommitted deletions and replacements. The command reports mechanical facts without writing or
trying to infer semantic project identity:

- the bound/current Charter identity;
- tracked and working Charter/Research candidates and any duplicate IDs, revisions, or heads;
- flat artifacts eligible for layout migration;
- unresolved `RM-NNN` refs used as Evidence;
- missing or deleted Evidence state;
- stranded staged files such as `config-after-sprint1.yaml`.

The existing content indicates two project families, but that semantic conclusion remains a human
diagnosis rather than a migration heuristic. Choosing which family to preserve is a separate human
decision. No implementation task in this plan may resolve it automatically.

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

- fresh init creates exactly three shallow output directories (`artifacts/`, `sources/`, `knowledge/`);
- config contains `next_ids.knowledge: 1` and omits `next_ids.evidence`;
- a valid re-init is a byte-for-byte no-op;
- `paths.artifacts_dir`, `sources_dir`, and `knowledge_dir` resolve correctly;
- Workflow-document iteration ignores Markdown under Knowledge and Sources;
- legacy flat and archived ART/EXP revisions remain readable during migration;
- `artifacts/archive/` is optional and is not created by fresh init.

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
- a valid Experiment under `artifacts/`;
- a valid `K-NNN` Markdown workpaper under `knowledge/`;
- a Markdown source note under `sources/`;
- legacy flat Artifact and Experiment revisions;
- recognized revisions under legacy `archive/` and new `artifacts/archive/`;
- unrelated Markdown elsewhere in the project root.

Assert that validation, hashing, Gate scans, and baseline collection read only the Artifact
locations defined by the shared iterator. They never parse Knowledge, Source, presentation, or
arbitrary project Markdown as `ArtifactMeta`.

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
- Modify `tests/test_shared_schemas.py`.

Cover:

- valid working and complete workpapers;
- one stable path per `K-NNN`, positive revisions, and rejection of `K-NNN-rN` fan-out;
- exact Research and Learning refs;
- `research_ref` remains the plan revision that authorized the work and is not forced to equal the
  newly appended Research head;
- local Source path confinement, existence, SHA-256 match/mismatch, and exact external URLs;
- byte-only validation of DOCX/PDF fixtures without parsing them;
- primary workpapers with empty `knowledge_refs` and synthesis workpapers with exact current-head
  Knowledge refs;
- detection of a stale synthesis dependency after one contributing K revision advances;
- required headings;
- complete status with empty conclusion;
- missing limitations;
- malformed Evidence refs;
- branch mismatch;
- duplicate Knowledge IDs under different filenames;
- in-place revision bump and stale-CAS conflict;
- current-head resolution without consulting CAS backup files or re-resolving historical Research
  revisions.

**Implementation**

- Add `src/skills/bw-discovery-research/references/knowledge-workpaper.md`.
- Add `src/skills/bw-discovery-research/scripts/validate_knowledge_workpaper.py`.
- Modify `src/skills/_bw-shared/ledger-schema.md` once to add the `K-NNN` identity and
  `knowledge:K-NNN@n` typed ref, document the current-head resolution rule, add
  `config.next_ids.knowledge`, remove the redundant config Evidence counter, and preserve ART/EXP
  append-only versioning.
- Keep the validator deterministic and file-based. Hash local Source bytes but do not parse their
  format. Do not add a Knowledge database, global index, or Git dependency to runtime validation.

**Verify**

```bash
.venv/bin/python -m pytest tests/test_knowledge_workpaper_validator.py tests/test_shared_schemas.py
```

### Task 4 — Simplify the Research Plan around Knowledge refs

**Tests first**

- Modify `tests/test_research_plan_validator.py`.
- Modify `tests/test_skill_bw_discovery_research.py`.

Replace old expectations with:

- `Research Progress` owns answer status;
- exact `knowledge:K-NNN@n` refs in the current Research head resolve to the current complete
  workpapers on the same branch;
- historical Research revisions retain their pins as audit text and are not checked against the live
  Knowledge revision;
- `answered`/`partial` without Knowledge fails;
- `RM-NNN` in a Knowledge or Evidence field fails;
- Assessment-derived candidate questions cannot be `known` or answered without independent
  Knowledge;
- Research artifacts require `ART-NNN` identity;
- full analysis and source inventories are absent from the Research Plan;
- Sprint Decision and Insight Readiness cite relevant Knowledge refs;
- Insight Ingredients contain traceable observations and candidate synthesis but never pre-approve
  an Insight or perform F/P/E/T judgment.

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
- write one or more new stable-path workpapers and an immutable Research revision in one resumable
  action;
- revise the same workpaper paths through CAS without allocating new IDs or creating `rN` files;
- optionally create/update Evidence and Ledger in the same plan;
- omit Evidence and Ledger steps when no decision-critical claim changes;
- reject a missing Knowledge ref, invalid Source path or digest, stale config revision, stale
  Research head, branch mismatch, or `RM-NNN` masquerading as evidence;
- emit no Source step and never decode a binary Source as text;
- can resume after an already-applied identical step;
- recover the interrupted state where Knowledge advanced but the new Research revision did not;
- reject unrelated allocation when `next_ids.knowledge` points at an already-written K file with
  different bytes;
- keep the current Research head and every referenced K revision synchronized when the action
  completes;
- revise or remove an affected synthesis workpaper when one of its current Knowledge inputs advances;
- never write `config-after-sprint*.yaml` or other staged files into project state.

**Implementation**

- Modify `src/skills/bw-discovery-research/scripts/emit_write_plan.py`.
- Modify `src/skills/bw-discovery-research/references/persistence-plan.md`.
- Reuse `bwkit plan apply`; do not add a second transaction engine.
- Keep `bwkit` text-only; no applier operation is added for DOCX, PDF, or other Source files.
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

- Reuse the shared-schema update owned by Task 3; do not edit the same contract in two tasks.
- Modify only the minimum runtime/schema code needed to remove the redundant config Evidence
  counter. Do not replace `evidence.yaml` with Knowledge workpapers.

**Verify**

```bash
.venv/bin/python -m pytest tests/test_schema.py tests/test_gate_scan.py tests/test_skill_bw_assumption_map.py
```

### Task 7 — Protect the one-repository/one-project boundary

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

### Task 8 — Add explicit output-layout migration tooling

**Tests first**

- Add `tests/test_output_layout_migration.py`.

Cover:

- clean legacy flat project dry run;
- explicit apply moving canonical ART/EXP workflow documents only;
- preservation and relocation of recognized legacy archived revisions;
- idempotent second run;
- preservation of hashes, bytes, ledger, Evidence, and records;
- conflict when destination exists with different bytes;
- rejection of relevant dirty state, duplicate Artifact revisions, multiple heads, or missing Evidence
  dependencies;
- reporting tracked and working candidates without semantic topic classification;
- no write in `--check` mode or on any failed precondition.

**Implementation**

- Add a narrowly scoped `bwkit` migration module and CLI command.
- Do not run migration from the installer.
- Require an explicit apply flag and produce a human-readable inventory before writing.

**Verify**

```bash
.venv/bin/python -m pytest tests/test_output_layout_migration.py tests/test_cli_wiring.py
```

### Task 9 — Update installer, deployed skills, documentation, and evals

**Tests first**

- Modify `tests/test_installer_copy.py` and `tests/test_installer_link.py`.
- Add a contract test that scans managed source skills and rejects new Artifact or Experiment
  writer/template paths using legacy flat `_bewater-output/ART-...` or `_bewater-output/EXP-...`
  forms.
- Update Discover eval scenarios to assert Knowledge persistence and prohibit `RM-NNN` Evidence
  refs.

**Implementation**

- Update `README.md` and `CLAUDE.md` architecture diagrams.
- Update every managed Artifact- or Experiment-producing skill and template to write under
  `_bewater-output/artifacts/`; this includes Immersion, Define, Ideate, Shape, and both Gate input
  families, not only Discover.
- Update relevant Discover eval fixtures and scenarios.
- Regenerate `.claude/skills/` from `src/skills/` using the normal deployment path.
- Never copy or hand-edit the active project's `_bewater/` state during deployment.

**Verify**

```bash
.venv/bin/python -m pytest tests/test_installer_copy.py tests/test_installer_link.py tests/test_skill_bw_discovery_research.py
diff -qr src/skills .claude/skills
```

### Task 10 — Full verification and current-state audit

Run:

```bash
.venv/bin/python -m pytest --cov=bw --cov=bwkit --cov-report=term-missing
git diff --check
```

Acceptance requirements:

- all tests pass;
- combined runtime coverage remains at least 80%;
- `src/skills/` and deployed managed skill copies match;
- no new temporary or backup files are tracked;
- no current `_bewater/` or `_bewater-output/` business data was changed by the implementation test
  run;
- read-only migration audit of the current workspace reports dirty/conflicting state facts and
  performs no write;
- no `K-NNN-rN` files, binary `bwkit` plan steps, or new flat ART/EXP writer paths exist.

Stop after reporting that audit. Ask the accountable human which project family to preserve before
any real-state migration, deletion, restoration, or move.

## Acceptance scenarios

### A. Five Forces research

1. LP-005 asks whether industry structure leaves an attractive entry position.
2. RM-005 selects Five Forces plus source triangulation.
3. Host tools place local reports under `sources/`; the workpaper records each repo-relative path and
   SHA-256, while external material retains its exact URL.
4. `K-002-ai-consulting-five-forces.md` summarizes each force. It may reference a detailed report
   under `sources/`, and it includes source trail, conclusion, limitations, and new questions.
5. Research Progress references `knowledge:K-002@1` and carries only the bounded current answer.
6. Insight Ingredients expose traceable patterns, tensions, and reframe candidates from K-002 for
   Define without generating or approving an Insight.

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
5. L4/Gate behavior follows Evidence and Ledger state, not presentation summaries.

### D. Unrelated project request

1. A repository already contains a current Charter and active state.
2. The user asks to start an unrelated consulting project.
3. Immersion reports that the repository is already bound.
4. No files change.
5. The user is directed to create a separate repository or working directory.

### E. Living Knowledge revision

1. `K-001-market-demand.md` exists at revision 1 and the current Research head pins
   `knowledge:K-001@1`.
2. New source material changes the answer; host tooling prepares the Source file and its digest.
3. One action CAS-revises the same K path to revision 2 and appends a Research Artifact revision that
   pins `knowledge:K-001@2`.
4. No `K-001-r2-...md` file is created.
5. If execution stops after step 3's Knowledge CAS, validation reports a Research/Knowledge head
   mismatch until the identical action resumes.
6. The old workpaper text remains recoverable from Git, not from runtime resolution or CAS backups.

## Final design check

- Three top-level output directories: canonical `artifacts/` and `knowledge/`, plus supporting
  `sources/`. `docs/` is user-controlled.
- One logical Workflow Artifact or Experiment has immutable append-only revision files; the existing
  exact-ref, signoff, Gate, lineage, and backtrack model remains intact.
- One Research Plan with embedded Learning Plan and Insight Ingredients handoff.
- One Knowledge document type only: a lightweight living workpaper with one stable file per K ID,
  in-file revision, CAS writes, and optional detailed analysis in `sources/`.
- Current Research heads resolve current Knowledge revisions; Git owns historical Knowledge text.
- Sources may be original or process-generated. Host tools manage their bytes; `bwkit` only receives
  canonical text-state steps and never parses or writes Source files.
- Presentations are outside methodology scope; users manage them under `docs/`.
- Machine Evidence remains hidden state because Gate correctness requires it; Knowledge workpapers
  may cite Evidence but do not replace it.
- No standalone Finding, Synthesis, Source-index, or Presentation artifact models.
- Current mixed project data remains untouched until a separate human recovery decision.
