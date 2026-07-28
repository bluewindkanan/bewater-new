# Contributing

Tests run against the project venv. After cloning:

```bash
python3.11 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m pytest --cov=bw --cov-report=term-missing
```

`bw` is exercised as `python -m bw` (or `bw` after activating the venv). The
coverage gate is enforced at 80% (`[tool.coverage.report] fail_under = 80`).
