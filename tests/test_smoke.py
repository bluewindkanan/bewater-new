"""End-to-end smoke test: the installed `bw` CLI works on a temp project.

Drives the entry point via `python -m bw` (the same path `bw` on PATH wraps),
so a green run proves the installed/editable package is importable and the
argparse glue for every subcommand group is wired.
"""
import subprocess
import sys


def _bw(*args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "bw", *args],
        capture_output=True,
        text=True,
    )


def test_end_to_end_init_add_validate(tmp_path):
    project = tmp_path / "p"

    r = _bw("init", str(project))
    assert r.returncode == 0, r.stderr
    assert (project / "_bewater").is_dir()

    r = _bw(
        "ledger", "add", str(project),
        "--statement", "s",
        "--layer", "concept",
        "--category", "consumer",
        "--impact", "high",
        "--uncertainty", "high",
        "--branch", "sol-01",
    )
    assert r.returncode == 0, r.stderr
    assert "A-001" in r.stdout

    r = _bw("validate", str(project))
    assert r.returncode == 0, (r.stdout, r.stderr)
