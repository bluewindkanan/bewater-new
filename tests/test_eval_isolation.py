"""TDD for eval isolation: repo-external cwd + temp HOME + controlled skill set (§11.1 step 2/4)."""
from __future__ import annotations
from pathlib import Path
from evals._harness import isolation

REPO = Path(__file__).resolve().parents[1]


def test_green_sandbox_copies_target_skill_and_deps(tmp_path):
    prod_root = tmp_path / "prod"
    home_root = tmp_path / "home"
    prod_root.mkdir()
    home_root.mkdir()

    with isolation.Sandbox(repo=REPO, product_root=prod_root,
                           home_root=home_root, target_skill="bw-start",
                           dependency_skills=["bw-immersion"], mode="green") as sb:
        sb_prod_cwd = sb.product_cwd  # Save the mkdtemp subdir path
        sb_temp_home = sb.temp_home    # Save the mkdtemp subdir path

        skills_dir = sb.product_cwd / ".claude" / "skills"
        assert (skills_dir / "bw-start" / "SKILL.md").exists()       # target present (GREEN)
        assert (skills_dir / "bw-immersion" / "SKILL.md").exists()   # dependency present
        assert sb.temp_home.exists()
        assert sb.env["HOME"] == str(sb.temp_home)
        # GREEN: installed_skills contains target + deps
        assert "bw-start" in sb.installed_skills
        assert "bw-immersion" in sb.installed_skills

    # Cleanup: mkdtemp SUBDIRS are removed, parent roots remain
    assert not sb_prod_cwd.exists()  # mkdtemp prod subdir cleaned up
    assert not sb_temp_home.exists()  # mkdtemp home subdir cleaned up
    assert prod_root.exists()  # parent root may remain
    assert home_root.exists()  # parent root may remain


def test_red_sandbox_omits_target_keeps_deps(tmp_path):
    with isolation.Sandbox(repo=REPO, product_root=tmp_path / "prod",
                           home_root=tmp_path / "home", target_skill="bw-start",
                           dependency_skills=["bw-immersion"], mode="red") as sb:
        skills_dir = sb.product_cwd / ".claude" / "skills"
        assert not (skills_dir / "bw-start").exists()                # target absent (RED)
        assert (skills_dir / "bw-immersion" / "SKILL.md").exists()   # dependency still present
        # RED: installed_skills contains deps but NOT target
        assert "bw-start" not in sb.installed_skills
        assert "bw-immersion" in sb.installed_skills


def test_product_cwd_is_outside_repo(tmp_path):
    with isolation.Sandbox(repo=REPO, product_root=tmp_path / "prod",
                           home_root=tmp_path / "home", target_skill="bw-start",
                           dependency_skills=[], mode="green") as sb:
        assert REPO not in sb.product_cwd.parents


def test_sandbox_preserves_codex_home_while_isolating_home(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", "/auth-home")

    with isolation.Sandbox(repo=REPO, product_root=tmp_path / "prod",
                           home_root=tmp_path / "home", target_skill="bw-start",
                           dependency_skills=[], mode="red") as sb:
        assert sb.env["HOME"] == str(sb.temp_home)
        assert sb.env["CODEX_HOME"] == "/auth-home/.codex"
