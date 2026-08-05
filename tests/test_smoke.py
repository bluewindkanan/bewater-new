"""End-to-end smoke test: the installed CLIs work on a temp project.

Drives the entry points via ``python -m bwkit`` and ``python -m bw`` (the same
paths the installed commands wrap), so a green run proves both packages are
importable and their argparse glue works together.
"""
import subprocess
import sys


def _bw(*args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "bw", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def _bwkit(*args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "bwkit", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_end_to_end_deployment_init_add_validate(tmp_path):
    project = tmp_path / "p"

    r = _bwkit("init", str(project))
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
