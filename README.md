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
