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


def _run(project_root: Path, *extra) -> subprocess.CompletedProcess:
    env = {**os.environ}
    return subprocess.run(
        ["bash", str(INSTALL), "--project-root", str(project_root), "--src", str(REPO), *extra],
        capture_output=True, text=True, env=env)


def test_copy_deploys_all_skills_and_shared_with_markers(tmp_dest):
    r = _run(tmp_dest, "--copy")
    assert r.returncode == 0, r.stderr
    skills_dest = tmp_dest / ".claude" / "skills"
    skills = sorted(p.name for p in (REPO / ".claude" / "skills").glob("bw-*"))
    installed = sorted(p.name for p in skills_dest.glob("bw-*"))
    assert installed == skills
    for s in installed:
        assert has_managed_marker(skills_dest / s), f"{s} missing marker"
    shared = skills_dest / "_bw-shared"
    assert shared.is_dir() and has_managed_marker(shared)


def test_copy_deploys_runnable_bwkit(tmp_dest):
    assert _run(tmp_dest, "--copy").returncode == 0
    bwkit = tmp_dest / "_bewater" / "bwkit"
    assert (bwkit / "__main__.py").exists()
    env = {**os.environ, "PYTHONPATH": str(tmp_dest / "_bewater")}
    r = subprocess.run([sys.executable, "-m", "bwkit", "--help"],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    assert "lock" in r.stdout and "cas" in r.stdout


def test_copy_is_idempotent(tmp_dest):
    assert _run(tmp_dest, "--copy").returncode == 0
    r2 = _run(tmp_dest, "--copy")
    assert r2.returncode == 0, r2.stderr
    assert (tmp_dest / ".claude" / "skills" / "bw-start" / "SKILL.md").exists()


def test_copy_fails_closed_on_unrelated_target(tmp_dest):
    stranger = tmp_dest / ".claude" / "skills" / "bw-start"
    stranger.parent.mkdir(parents=True)
    stranger.mkdir()
    (stranger / "SKILL.md").write_text("someone else's skill")
    r = _run(tmp_dest, "--copy")
    assert r.returncode != 0
    assert "not bewater-managed" in r.stderr


def test_copy_fails_closed_on_foreign_marker(tmp_dest):
    # a foreign .bewater-managed (not bewater) must NOT authorize overwrite
    foreign = tmp_dest / ".claude" / "skills" / "bw-start"
    foreign.parent.mkdir(parents=True)
    foreign.mkdir()
    (foreign / "SKILL.md").write_text("someone else's skill")
    (foreign / ".bewater-managed").write_text('{"managed_by":"other-tool","version":"9.9"}')
    r = _run(tmp_dest, "--copy")
    assert r.returncode != 0
    assert "not bewater-managed" in r.stderr
    assert (foreign / "SKILL.md").read_text() == "someone else's skill"  # survives


def test_copy_honors_skill_destination_override(tmp_dest):
    skills_dest = tmp_dest / "custom-skills"
    r = _run(tmp_dest, "--copy", "--dest", str(skills_dest))
    assert r.returncode == 0, r.stderr
    assert (skills_dest / "bw-start" / "SKILL.md").exists()
    assert (tmp_dest / "_bewater" / "bwkit" / "__main__.py").exists()
