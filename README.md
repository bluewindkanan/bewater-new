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

Immersion separates two capabilities: `bw-project-charter` adaptively collects intent, self-reviews,
and automatically persists the Charter plus root assumptions; `bw-initial-assessment` then runs in
fresh context against those exact revisions and automatically adds a source-bounded advisory report.
The report is not a formal Discover input or Gate.
