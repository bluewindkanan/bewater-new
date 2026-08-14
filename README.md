# bw — bewater decision-phase runtime

Deterministic runtime for the bewater decision phase (assumption ledger,
artifact hashing, gate-scan, system-wide validate). Source lives in `src/bw/`,
tests in `tests/`.

## Setup & tests

Create the project venv, install editable with dev extras, and run the suite:

```
python -m venv .venv && .venv/bin/pip install -e '.[dev]' && .venv/bin/python -m pytest
```

The `bw` console script is added to PATH only after the editable install inside
the venv (`.venv/bin/bw`); without it, invoke the runtime via
`.venv/bin/python -m bw`.

## BeWater workflow

Installing BeWater initializes the project state and deploys the skills from `src/skills/` to
`.claude/skills/`. The first workflow action is **Immersion** through `bw-immersion`; there is no
separate start step. Invoke `bw-resume` at any time to read global or cross-stage status, recover
orientation after an interruption, resolve branch ambiguity, or route pending recovery work.

Immersion is a single entry point, `bw-immersion`: it adaptively collects intent, self-reviews, and
automatically persists the Charter, then runs a fresh-context, source-bounded preliminary Assessment
against that exact Charter revision and delivers a compact advisory conclusion. Charter alone is the
formal Discover input. The report is not an input to Research, the Knowledge Base, assumptions, or
Evidence, and is not a Gate.

## Project and output layout

One repository or working directory contains one BeWater project. The first Charter transaction
sets the repository's non-empty `project.name`; unrelated project intent starts in another
repository or working directory rather than replacing the current Charter or state.

Canonical and supporting outputs use three shallow directories:

```text
_bewater-output/
├── artifacts/   # immutable ART-NNN-rN and EXP-NNN-rN workflow revisions
├── knowledge/   # living K-NNN research workpapers, revised in place through CAS
└── sources/     # byte-preserved referenced research material; never written by bwkit

docs/presentations/  # optional user-controlled readouts, outside methodology state
```

Research Artifacts pin exact `knowledge:K-NNN@n` revisions. `_bewater/evidence.yaml` remains the
machine contract for decision-critical claims and Gates; a Knowledge workpaper or an `RM-NNN`
mission is not Evidence.
