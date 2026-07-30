"""TDD for eval isolation: repo-external cwd + temp HOME + controlled skill set (§11.1 step 2/4)."""
from __future__ import annotations
from pathlib import Path
from evals._harness import isolation

REPO = Path(__file__).resolve().parents[1]


def test_green_sandbox_copies_target_skill_and_deps(tmp_path):
    with isolation.Sandbox(repo=REPO, product_root=tmp_path / "prod",
                           home_root=tmp_path / "home", target_skill="bw-start",
                           dependency_skills=["bw-immersion"], mode="green") as sb:
        skills_dir = sb.product_cwd / ".claude" / "skills"
        assert (skills_dir / "bw-start" / "SKILL.md").exists()       # target present (GREEN)
        assert (skills_dir / "bw-immersion" / "SKILL.md").exists()   # dependency present
        assert sb.temp_home.exists()
        assert sb.env["HOME"] == str(sb.temp_home)
    # cleaned up
    assert not (tmp_path / "prod").exists()


def test_red_sandbox_omits_target_keeps_deps(tmp_path):
    with isolation.Sandbox(repo=REPO, product_root=tmp_path / "prod",
                           home_root=tmp_path / "home", target_skill="bw-start",
                           dependency_skills=["bw-immersion"], mode="red") as sb:
        skills_dir = sb.product_cwd / ".claude" / "skills"
        assert not (skills_dir / "bw-start").exists()                # target absent (RED)
        assert (skills_dir / "bw-immersion" / "SKILL.md").exists()   # dependency still present


def test_product_cwd_is_outside_repo(tmp_path):
    with isolation.Sandbox(repo=REPO, product_root=tmp_path / "prod",
                           home_root=tmp_path / "home", target_skill="bw-start",
                           dependency_skills=[], mode="green") as sb:
        assert REPO not in sb.product_cwd.parents
