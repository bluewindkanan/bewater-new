"""Shared structural validator for bw-* skills (spec §4, §11.3). Authoring utility;
reused by every per-skill pytest and by scripts/verify. Not shipped."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from evals._harness.loader import ManifestError, load_manifest


class SkillCheckError(Exception):
    """A skill fails a structural check."""


def skill_dir(repo: Path, name: str) -> Path:
    """Return the authored skill directory, never a deployed copy."""
    return Path(repo) / "src" / "skills" / name


_PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME|XXX)\b")


def _frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        raise SkillCheckError(f"frontmatter is not YAML: {e}") from e
    return fm if isinstance(fm, dict) else {}


def validate_skill(skill_dir: Path) -> None:
    skill_dir = Path(skill_dir)
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise SkillCheckError(f"missing SKILL.md in {skill_dir}")

    fm = _frontmatter(skill_md.read_text(encoding="utf-8", errors="replace"))
    if set(fm) != {"name", "description"}:
        raise SkillCheckError(f"frontmatter must be exactly name+description (got {sorted(fm)})")
    desc = str(fm["description"]).strip()
    if not desc.startswith("Use when"):
        raise SkillCheckError("description must start with 'Use when'")

    refs = skill_dir / "references"
    files = [skill_md, *sorted(refs.rglob("*.md"))] if refs.is_dir() else [skill_md]
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        if _PLACEHOLDER_RE.search(text):
            raise SkillCheckError(f"placeholder token in {f.name}")
        # references may cite only the sanctioned shared location (../_bw-shared/);
        # any other parent-relative path escapes the skill directory (§2.3, §11.3)
        if re.search(r"\.\./(?!_bw-shared/)", text):
            raise SkillCheckError(f"{f.name} references a path outside its skill dir")
        # a reference that declares a contract must carry stable contract metadata
        cfm = _frontmatter(text)
        if "contract_id" in cfm:
            for key in ("contract_version",):
                if key not in cfm:
                    raise SkillCheckError(f"contract ref {f.name} missing {key}")


def validate_skill_evals(evals_root: Path, name: str) -> None:
    for sub in ("scenarios", "red"):
        bucket = Path(evals_root) / name / sub
        manifests = sorted(bucket.glob("*.yaml")) if bucket.is_dir() else []
        if not manifests:
            raise SkillCheckError(f"evals/{name}/{sub}/ has no manifests")
        for m in manifests:
            try:
                load_manifest(m)
            except ManifestError as e:
                raise SkillCheckError(f"{m}: {e}") from e
