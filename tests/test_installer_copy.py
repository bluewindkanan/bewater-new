"""install.sh copy-mode behaviors (spec §9). Drives the script via subprocess against
isolated tmp_home / tmp_dest from Plan 1's conftest."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from installer_helpers import has_managed_marker

REPO = Path(__file__).resolve().parents[1]
INSTALL = REPO / "install.sh"


def _run(dest: Path, *extra) -> subprocess.CompletedProcess:
    env = {**os.environ}
    return subprocess.run(
        ["bash", str(INSTALL), "--dest", str(dest), "--src", str(REPO), *extra],
        capture_output=True, text=True, env=env)


def test_copy_deploys_all_skills_and_shared_with_markers(tmp_dest):
    r = _run(tmp_dest, "--copy")
    assert r.returncode == 0, r.stderr
    skills = sorted(p.name for p in (REPO / ".claude" / "skills").glob("bw-*"))
    installed = sorted(p.name for p in tmp_dest.glob("bw-*"))
    assert installed == skills
    for s in installed:
        assert has_managed_marker(tmp_dest / s), f"{s} missing marker"
    shared = tmp_dest / "_bw-shared"
    assert shared.is_dir() and has_managed_marker(shared)


def test_copy_deploys_runnable_bwkit(tmp_dest):
    assert _run(tmp_dest, "--copy").returncode == 0
    bwkit = tmp_dest / "_bw-shared" / "bwkit"
    assert (bwkit / "__main__.py").exists()
    env = {**os.environ, "PYTHONPATH": str(tmp_dest / "_bw-shared")}
    r = subprocess.run([sys.executable, "-m", "bwkit", "--help"],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    assert "lock" in r.stdout and "cas" in r.stdout


def test_copy_is_idempotent(tmp_dest):
    assert _run(tmp_dest, "--copy").returncode == 0
    r2 = _run(tmp_dest, "--copy")
    assert r2.returncode == 0, r2.stderr
    assert (tmp_dest / "bw-start" / "SKILL.md").exists()


def test_copy_fails_closed_on_unrelated_target(tmp_dest):
    stranger = tmp_dest / "bw-start"
    stranger.mkdir()
    (stranger / "SKILL.md").write_text("someone else's skill")
    r = _run(tmp_dest, "--copy")
    assert r.returncode != 0
    assert "not bewater-managed" in r.stderr
