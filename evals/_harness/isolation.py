"""Eval isolation primitives: repo-external temp product cwd + temp HOME with controlled skill set (§11.1 step 2/4)."""
from __future__ import annotations

import os
import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Literal


@contextmanager
def Sandbox(
    repo: Path,
    product_root: Path,
    home_root: Path,
    target_skill: str,
    dependency_skills: list[str],
    mode: Literal["green", "red"],
):
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

    Yields:
        Sandbox object with attributes:
            product_cwd: Path to temp product working directory
            temp_home: Path to temp HOME directory
            env: dict with HOME overridden, ANTHROPIC_API_KEY passed through, etc.
            installed_skills: list of skill names that were copied
    """
    # Use the caller-supplied directories directly
    product_cwd = product_root
    temp_home = home_root

    product_cwd.mkdir(parents=True, exist_ok=True)
    temp_home.mkdir(parents=True, exist_ok=True)

    # Create .claude/skills directory in product cwd
    skills_dir = product_cwd / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    # Copy skills from repo
    repo_skills = repo / ".claude" / "skills"
    installed_skills = []

    # Always copy dependency skills
    for skill in dependency_skills:
        src = repo_skills / skill
        if src.exists():
            dst = skills_dir / skill
            shutil.copytree(src, dst)
            installed_skills.append(skill)

    # For GREEN mode, also copy the target skill
    if mode == "green":
        src = repo_skills / target_skill
        if src.exists():
            dst = skills_dir / target_skill
            shutil.copytree(src, dst)
            installed_skills.append(target_skill)

    # Build environment dict with HOME overridden
    env = dict(os.environ)
    env["HOME"] = str(temp_home)

    class SandboxResult:
        def __init__(self):
            self.product_cwd = product_cwd
            self.temp_home = temp_home
            self.env = env
            self.installed_skills = installed_skills

    try:
        yield SandboxResult()
    finally:
        # Cleanup: remove product_cwd and temp_home
        if product_cwd.exists():
            shutil.rmtree(product_cwd)
        if temp_home.exists():
            shutil.rmtree(temp_home)
