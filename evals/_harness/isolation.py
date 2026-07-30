"""Eval isolation primitives: repo-external temp product cwd + temp HOME with controlled skill set (§11.1 step 2/4)."""
from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import Literal


class Sandbox:
    """Context manager that creates an isolated evaluation environment.

    Creates a repo-external temp product cwd + temp HOME, installs the fixed
    dependency-skill set into `<product>/.claude/skills/`, and for GREEN copies
    in the target skill (RED leaves it absent).

    Args:
        repo: Path to the source repository (skills are read from here)
        product_root: Parent directory where temp product cwd will be created
        home_root: Parent directory where temp HOME will be created
        target_skill: Name of the skill being tested (e.g., "bw-start")
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
    ):
        self.repo = repo
        self.product_root = product_root
        self.home_root = home_root
        self.target_skill = target_skill
        self.dependency_skills = dependency_skills
        self.mode = mode

        # Will be set in __enter__
        self.product_cwd: Path | None = None
        self.temp_home: Path | None = None
        self.env: dict[str, str] | None = None
        self.installed_skills: list[str] | None = None

    def __enter__(self) -> "Sandbox":
        # Create parent dirs if they don't exist
        self.product_root.mkdir(parents=True, exist_ok=True)
        self.home_root.mkdir(parents=True, exist_ok=True)

        # Create fresh mkdtemp subdirs under caller-supplied roots
        self.product_cwd = Path(tempfile.mkdtemp(prefix="prod-", dir=str(self.product_root)))
        self.temp_home = Path(tempfile.mkdtemp(prefix="home-", dir=str(self.home_root)))

        # Create .claude/skills directory in product cwd
        skills_dir = self.product_cwd / ".claude" / "skills"
        skills_dir.mkdir(parents=True, exist_ok=True)

        # Copy skills from repo
        repo_skills = self.repo / ".claude" / "skills"
        self.installed_skills = []

        # Always copy dependency skills
        for skill in self.dependency_skills:
            src = repo_skills / skill
            if src.exists():
                dst = skills_dir / skill
                shutil.copytree(src, dst)
                self.installed_skills.append(skill)

        # For GREEN mode, also copy the target skill
        if self.mode == "green":
            src = repo_skills / self.target_skill
            if src.exists():
                dst = skills_dir / self.target_skill
                shutil.copytree(src, dst)
                self.installed_skills.append(self.target_skill)

        # Build environment dict with HOME overridden. Codex stores its login
        # independently under CODEX_HOME, so retain that authenticated config
        # while keeping the evaluated product's HOME isolated.
        self.env = dict(os.environ)
        self.env["CODEX_HOME"] = self.env.get(
            "CODEX_HOME", str(Path(self.env["HOME"]) / ".codex")
        )
        self.env["HOME"] = str(self.temp_home)

        # If DEEPSEEK_API_KEY is present, route to DeepSeek's Anthropic-compatible
        # endpoint so headless claude resolves deepseek-* models correctly.
        # Without this, a stale ANTHROPIC_BASE_URL (e.g. ZhipuAI) causes
        # "model not found" errors for DeepSeek-named models.
        # Mirrors `cm ds` behaviour: override base URL, auth via token, unset API key.
        if self.env.get("DEEPSEEK_API_KEY"):
            self.env["ANTHROPIC_BASE_URL"] = "https://api.deepseek.com/anthropic"
            self.env["ANTHROPIC_AUTH_TOKEN"] = self.env["DEEPSEEK_API_KEY"]
            self.env.pop("ANTHROPIC_API_KEY", None)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # Cleanup: remove mkdtemp subdirs (not the parent roots)
        if self.product_cwd and self.product_cwd.exists():
            shutil.rmtree(self.product_cwd)
        if self.temp_home and self.temp_home.exists():
            shutil.rmtree(self.temp_home)
