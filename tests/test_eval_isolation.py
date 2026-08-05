"""TDD for eval isolation: fresh project state and controlled skill deployment."""
from __future__ import annotations

from pathlib import Path

import pytest

from evals._harness import isolation


def _write_skill(repo: Path, name: str, marker: str) -> None:
    skill_dir = repo / "src" / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(marker)


def _write_bwkit_runtime(repo: Path) -> None:
    runtime = repo / "src" / "bwkit"
    runtime.mkdir(parents=True)
    (runtime / "__init__.py").write_text("")
    (runtime / "__main__.py").write_text("print('sandbox runtime')\n")


def _assert_fresh_state(product_cwd: Path) -> None:
    bewater = product_cwd / "_bewater"
    assert (bewater / "records").is_dir()
    assert (product_cwd / "_bewater-output").is_dir()
    assert (bewater / "ledger.yaml").is_file()
    assert (bewater / "conditions.yaml").is_file()
    config = (bewater / "config.yaml").read_text()
    assert "active_branch: BR-001" in config
    assert "current_stage: immersion" in config


def test_green_sandbox_deploys_source_skills_and_initializes_state(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _write_skill(repo, "bw-resume", "source target")
    _write_skill(repo, "bw-immersion", "source dependency")
    stale = repo / ".claude" / "skills" / "bw-resume"
    stale.mkdir(parents=True)
    (stale / "SKILL.md").write_text("stale deployed target")
    prod_root = tmp_path / "prod"
    home_root = tmp_path / "home"
    prod_root.mkdir()
    home_root.mkdir()

    with isolation.Sandbox(
        repo=repo,
        product_root=prod_root,
        home_root=home_root,
        target_skill="bw-resume",
        dependency_skills=["bw-immersion"],
        mode="green",
    ) as sandbox:
        product_cwd = sandbox.product_cwd
        temp_home = sandbox.temp_home
        skills_dir = product_cwd / ".claude" / "skills"
        _assert_fresh_state(product_cwd)
        assert (skills_dir / "bw-resume" / "SKILL.md").read_text() == "source target"
        assert (skills_dir / "bw-immersion" / "SKILL.md").read_text() == "source dependency"
        assert sandbox.env["HOME"] == str(temp_home)
        assert sandbox.installed_skills == ["bw-immersion", "bw-resume"]

    assert not product_cwd.exists()
    assert not temp_home.exists()
    assert prod_root.exists()
    assert home_root.exists()


def test_red_sandbox_omits_target_but_initializes_state(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _write_skill(repo, "bw-resume", "source target")
    _write_skill(repo, "bw-immersion", "source dependency")

    with isolation.Sandbox(
        repo=repo,
        product_root=tmp_path / "prod",
        home_root=tmp_path / "home",
        target_skill="bw-resume",
        dependency_skills=["bw-immersion"],
        mode="red",
    ) as sandbox:
        skills_dir = sandbox.product_cwd / ".claude" / "skills"
        assert not (skills_dir / "bw-resume").exists()
        assert (skills_dir / "bw-immersion" / "SKILL.md").read_text() == "source dependency"
        assert sandbox.installed_skills == ["bw-immersion"]
        _assert_fresh_state(sandbox.product_cwd)


def test_sandbox_deploys_project_local_bwkit_runtime(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _write_skill(repo, "bw-resume", "source target")
    _write_bwkit_runtime(repo)

    with isolation.Sandbox(
        repo=repo,
        product_root=tmp_path / "prod",
        home_root=tmp_path / "home",
        target_skill="bw-resume",
        dependency_skills=[],
        mode="green",
    ) as sandbox:
        runtime = sandbox.product_cwd / "_bewater" / "bwkit"
        assert (runtime / "__main__.py").read_text() == "print('sandbox runtime')\n"
        assert sandbox.env["PYTHONPATH"].split(":")[0] == str(sandbox.product_cwd / "_bewater")


def test_product_cwd_is_outside_repo(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _write_skill(repo, "bw-resume", "source target")

    with isolation.Sandbox(
        repo=repo,
        product_root=tmp_path / "prod",
        home_root=tmp_path / "home",
        target_skill="bw-resume",
        dependency_skills=[],
        mode="green",
    ) as sandbox:
        assert repo not in sandbox.product_cwd.parents


def test_sandbox_preserves_codex_home_while_isolating_home(
    tmp_path: Path, monkeypatch
) -> None:
    repo = tmp_path / "repo"
    _write_skill(repo, "bw-resume", "source target")
    monkeypatch.setenv("HOME", "/auth-home")

    with isolation.Sandbox(
        repo=repo,
        product_root=tmp_path / "prod",
        home_root=tmp_path / "home",
        target_skill="bw-resume",
        dependency_skills=[],
        mode="red",
    ) as sandbox:
        assert sandbox.env["HOME"] == str(sandbox.temp_home)
        assert sandbox.env["CODEX_HOME"] == "/auth-home/.codex"


def test_sandbox_applies_repo_relative_fixture_overlay(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _write_skill(repo, "bw-resume", "source target")
    fixture = repo / "evals" / "fixtures" / "pending-g1"
    record = fixture / "_bewater" / "records" / "D-001-g1.yaml"
    record.parent.mkdir(parents=True)
    record.write_text("gate: G1\naction_plan:\n  action_status: pending\n")

    with isolation.Sandbox(
        repo=repo,
        product_root=tmp_path / "prod",
        home_root=tmp_path / "home",
        target_skill="bw-resume",
        dependency_skills=[],
        mode="green",
        fixture_refs=["evals/fixtures/pending-g1"],
    ) as sandbox:
        deployed = sandbox.product_cwd / "_bewater" / "records" / record.name
        assert deployed.read_text() == record.read_text()


def test_sandbox_enter_failure_cleans_temp_subdirectories(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "repo"
    product_root = tmp_path / "prod"
    home_root = tmp_path / "home"

    def fail_init(_root: Path) -> str:
        raise RuntimeError("init failed")

    monkeypatch.setattr(isolation, "initialize_project", fail_init)

    sandbox = isolation.Sandbox(
        repo=repo,
        product_root=product_root,
        home_root=home_root,
        target_skill="bw-resume",
        dependency_skills=[],
        mode="green",
    )
    with pytest.raises(RuntimeError, match="init failed"):
        sandbox.__enter__()

    assert product_root.is_dir() and list(product_root.iterdir()) == []
    assert home_root.is_dir() and list(home_root.iterdir()) == []
