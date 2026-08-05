"""Eval isolation primitives: repo-external temp product cwd + temp HOME with controlled skill set (§11.1 step 2/4)."""
from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import Literal, Self

from bwkit.init import initialize_project


class Sandbox:
    """Context manager that creates an isolated evaluation environment.

    Creates a repo-external temp product cwd + temp HOME, installs the fixed
    dependency-skill set into `<product>/.claude/skills/`, and for GREEN copies
    in the target skill (RED leaves it absent).

    Args:
        repo: Path to the source repository (skills are read from here)
        product_root: Parent directory where temp product cwd will be created
        home_root: Parent directory where temp HOME will be created
        target_skill: Name of the skill being tested (e.g., "bw-resume")
        dependency_skills: List of skills that must always be present
        mode: "green" = include target skill, "red" = exclude target skill

    Attributes:
        product_cwd: Path to temp product working directory (mkdtemp subdir)
        temp_home: Path to temp HOME directory (mkdtemp subdir)
        env: dict with HOME overridden, ANTHROPIC_API_KEY passed through, etc.
        installed_skills: list of skill names that were copied
    """

    def __init__(
        self,
        repo: Path,
        product_root: Path,
        home_root: Path,
        target_skill: str,
        dependency_skills: list[str],
        mode: Literal["green", "red"],
        fixture_refs: list[str] | None = None,
    ):
        self.repo = repo
        self.product_root = product_root
        self.home_root = home_root
        self.target_skill = target_skill
        self.dependency_skills = dependency_skills
        self.mode = mode
        self.fixture_refs = list(fixture_refs or [])

        # Will be set in __enter__
        self.product_cwd: Path | None = None
        self.temp_home: Path | None = None
        self.env: dict[str, str] | None = None
        self.installed_skills: list[str] | None = None

    def __enter__(self) -> Self:
        # Create parent dirs if they don't exist
        self.product_root.mkdir(parents=True, exist_ok=True)
        self.home_root.mkdir(parents=True, exist_ok=True)

        try:
            self.product_cwd = Path(tempfile.mkdtemp(prefix="prod-", dir=str(self.product_root)))
            self.temp_home = Path(tempfile.mkdtemp(prefix="home-", dir=str(self.home_root)))

            initialize_project(self.product_cwd)
            self._apply_fixture_overlays()

            runtime_src = self.repo / "src" / "bwkit"
            runtime_dst = self.product_cwd / "_bewater" / "bwkit"
            if runtime_src.is_dir():
                shutil.copytree(runtime_src, runtime_dst, dirs_exist_ok=True)

            skills_dir = self.product_cwd / ".claude" / "skills"
            skills_dir.mkdir(parents=True, exist_ok=True)
            repo_skills = self.repo / "src" / "skills"
            self.installed_skills = []

            for skill in self.dependency_skills:
                src = repo_skills / skill
                if src.exists():
                    shutil.copytree(src, skills_dir / skill)
                    self.installed_skills.append(skill)

            if self.mode == "green":
                src = repo_skills / self.target_skill
                if src.exists():
                    shutil.copytree(src, skills_dir / self.target_skill)
                    self.installed_skills.append(self.target_skill)

            self.env = dict(os.environ)
            self.env["CODEX_HOME"] = self.env.get(
                "CODEX_HOME", str(Path(self.env["HOME"]) / ".codex")
            )
            self.env["HOME"] = str(self.temp_home)
            runtime_pythonpath = str(self.product_cwd / "_bewater")
            inherited_pythonpath = self.env.get("PYTHONPATH")
            self.env["PYTHONPATH"] = (
                runtime_pythonpath + os.pathsep + inherited_pythonpath
                if inherited_pythonpath
                else runtime_pythonpath
            )

            if self.env.get("DEEPSEEK_API_KEY"):
                self.env["ANTHROPIC_BASE_URL"] = "https://api.deepseek.com/anthropic"
                self.env["ANTHROPIC_AUTH_TOKEN"] = self.env["DEEPSEEK_API_KEY"]
                self.env.pop("ANTHROPIC_API_KEY", None)

            return self
        except Exception:
            self._cleanup()
            raise

    def _apply_fixture_overlays(self) -> None:
        repo = self.repo.resolve()
        for ref in self.fixture_refs:
            source = (repo / ref).resolve()
            try:
                source.relative_to(repo)
            except ValueError as exc:
                raise ValueError(f"fixture escapes repository: {ref}") from exc
            if not source.is_dir():
                raise FileNotFoundError(f"fixture overlay directory not found: {ref}")
            for child in source.iterdir():
                destination = self.product_cwd / child.name
                if child.is_dir():
                    shutil.copytree(child, destination, dirs_exist_ok=True)
                else:
                    shutil.copy2(child, destination)

    def _cleanup(self) -> None:
        if self.product_cwd and self.product_cwd.exists():
            shutil.rmtree(self.product_cwd)
        if self.temp_home and self.temp_home.exists():
            shutil.rmtree(self.temp_home)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._cleanup()
