from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import pytest

REPO = Path(__file__).resolve().parents[1]


def _make_repo(tmp_path: Path, good: bool = True) -> Path:
    repo = tmp_path / "repo"
    skills = repo / ".claude" / "skills"
    sk = skills / "bw-x"
    sk.mkdir(parents=True)
    fm = "---\nname: bw-x\ndescription: Use when the user wants to x.\n---\n# x\n"
    sk.joinpath("SKILL.md").write_text(fm if good else fm.replace("Use when", "Trigger"))
    ev = repo / "evals" / "bw-x"
    ev.mkdir(parents=True)
    manifest = (lambda rid: dedent(f"""\
        scenario_id: {rid}
        target_skill: bw-x
        prompt: hi
        required_assertions: [a]
        forbidden_behaviors: []
        repetition_count: 1
        """))
    (ev / "scenarios").mkdir()
    (ev / "scenarios" / "s.yaml").write_text(manifest("S-1"))
    (ev / "red").mkdir()
    (ev / "red" / "r.yaml").write_text(manifest("R-1"))
    return repo


def test_list_and_check_skill_good(tmp_path):
    from verify import check_skill, list_skills
    repo = _make_repo(tmp_path, good=True)
    assert list_skills(repo / ".claude" / "skills") == ["bw-x"]
    ok, details = check_skill("bw-x", repo / ".claude" / "skills", repo / "evals")
    assert ok, details


def test_check_skill_bad_frontmatter(tmp_path):
    from verify import check_skill
    repo = _make_repo(tmp_path, good=False)
    ok, details = check_skill("bw-x", repo / ".claude" / "skills", repo / "evals")
    assert not ok
    assert any("validate_skill" in d for d in details)


def test_check_local_discovery(tmp_path):
    from verify import check_local_discovery
    repo = _make_repo(tmp_path, good=True)
    ok, _ = check_local_discovery(repo / ".claude" / "skills")
    assert ok


def test_check_installer_runs_against_real_repo(tmp_home, tmp_dest):
    from verify import check_installer
    ok, details = check_installer(REPO, tmp_dest)
    assert ok, details
    assert (tmp_dest / "bw-start").exists()


def test_main_exits_nonzero_on_violation(tmp_path, monkeypatch):
    from verify import main
    repo = _make_repo(tmp_path, good=False)
    monkeypatch.setattr("verify._REPO", repo)
    monkeypatch.setattr("verify.SKILLS", repo / ".claude" / "skills")
    monkeypatch.setattr("verify.EVALS", repo / "evals")
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code != 0
