"""install.sh link mode + uninstall + broken-link repair (spec §9)."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
INSTALL = REPO / "install.sh"


def _run(project_root: Path, *extra) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(INSTALL), "--project-root", str(project_root), "--src", str(REPO), *extra],
        capture_output=True, text=True, env={**os.environ})


def test_link_mode_creates_managed_symlinks(tmp_dest):
    r = _run(tmp_dest, "--link")
    assert r.returncode == 0, r.stderr
    skills_dest = tmp_dest / ".claude" / "skills"
    skill_md = skills_dest / "bw-start" / "SKILL.md"
    assert skill_md.is_symlink()
    assert (skills_dest / "bw-start" / ".bewater-managed").is_file()  # real marker, not link
    bwkit = tmp_dest / "_bewater" / "bwkit"
    assert (bwkit / ".bewater-managed").is_file()
    assert (bwkit / "__main__.py").is_symlink()


def test_link_repair_broken_content_symlink(tmp_dest):
    assert _run(tmp_dest, "--link").returncode == 0
    # break one content link
    broken = tmp_dest / ".claude" / "skills" / "bw-start" / "SKILL.md"
    broken.unlink()
    os.symlink("/nonexistent/path", broken)
    assert _run(tmp_dest, "--link").returncode == 0, "redeploy should repair"
    assert (tmp_dest / ".claude" / "skills" / "bw-start" / "SKILL.md").exists()


def test_uninstall_removes_only_managed(tmp_dest):
    assert _run(tmp_dest, "--copy").returncode == 0
    skills_dest = tmp_dest / ".claude" / "skills"
    stranger = skills_dest / "stranger-skill"
    stranger.mkdir()
    (stranger / "SKILL.md").write_text("not bewater")
    r = _run(tmp_dest, "--uninstall")
    assert r.returncode == 0, r.stderr
    assert not (skills_dest / "bw-start").exists()
    assert not (skills_dest / "_bw-shared").exists()
    assert not (tmp_dest / "_bewater" / "bwkit").exists()
    assert stranger.exists(), "uninstall must not touch unrelated skills"
