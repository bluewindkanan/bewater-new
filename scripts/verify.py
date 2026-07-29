"""scripts/verify — authoring-time integrity checks (spec §11.3). Not shipped.
Importable as `verify` (pytest pythonpath includes "scripts"). Each check returns
(ok, details); main() runs them all and exits non-zero on any failure."""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_REPO / "tests"))
from skill_helpers import (  # noqa: E402
    SkillCheckError,
    validate_skill,
    validate_skill_evals,
)

SKILLS = _REPO / ".claude" / "skills"
EVALS = _REPO / "evals"
_PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME|XXX)\b")


def list_skills(skills_root=None) -> list[str]:
    skills_root = SKILLS if skills_root is None else Path(skills_root)
    return sorted(p.name for p in skills_root.glob("bw-*") if p.is_dir())


def check_skill(name, skills_root=None, evals_root=None):
    skills_root = SKILLS if skills_root is None else Path(skills_root)
    evals_root = EVALS if evals_root is None else Path(evals_root)
    details: list[str] = []
    try:
        validate_skill(Path(skills_root) / name)
    except SkillCheckError as e:
        details.append(f"validate_skill: {e}")
    try:
        validate_skill_evals(Path(evals_root), name)
    except SkillCheckError as e:
        details.append(f"validate_skill_evals: {e}")
    return (not details, details)


def check_placeholders(skills_root=None):
    skills_root = SKILLS if skills_root is None else Path(skills_root)
    bad = [str(p) for p in skills_root.rglob("*.md")
           if _PLACEHOLDER_RE.search(p.read_text(encoding="utf-8", errors="replace"))]
    return (not bad, bad)


def check_local_discovery(skills_root=None):
    skills_root = SKILLS if skills_root is None else Path(skills_root)
    missing = [n for n in list_skills(skills_root) if not (skills_root / n / "SKILL.md").exists()]
    return (not missing, missing)


def _installer_ok(repo, dest):
    """Run install.sh --copy into dest; assert managed markers + deployed bwkit runs."""
    install = Path(repo) / "install.sh"
    if not install.exists():
        return (False, [f"missing {install}"])
    r = subprocess.run(
        ["bash", str(install), "--dest", str(dest), "--src", str(repo), "--copy"],
        capture_output=True, text=True)
    if r.returncode != 0:
        return (False, [f"installer failed: {r.stderr.strip()}"])
    for name in list_skills(Path(repo) / ".claude" / "skills"):
        if not (dest / name / ".bewater-managed").exists():
            return (False, [f"{name} missing managed marker"])
    if not (dest / "_bw-shared" / ".bewater-managed").exists():
        return (False, ["_bw-shared missing managed marker"])
    if not (dest / "_bw-shared" / "bwkit" / "__init__.py").exists():
        return (False, ["deployed bwkit missing __init__.py"])
    env = {**os.environ, "PYTHONPATH": str(dest / "_bw-shared")}
    rr = subprocess.run([sys.executable, "-m", "bwkit", "--help"],
                        capture_output=True, text=True, env=env)
    if rr.returncode != 0:
        return (False, [f"deployed bwkit not runnable: {rr.stderr.strip()}"])
    return (True, [])


def check_installer(repo=None, dest=None):
    """Run install.sh --copy into an isolated dest; assert managed markers + bwkit runs.
    Self-created temp dirs are cleaned up; a caller-supplied dest is left intact."""
    repo = _REPO if repo is None else Path(repo)
    if dest is not None:
        return _installer_ok(repo, Path(dest))
    with tempfile.TemporaryDirectory(prefix="bwverify-") as d:
        return _installer_ok(repo, Path(d))


def main() -> None:
    failures: list[str] = []
    names = list_skills()
    if not names:
        failures.append("no bw-* skills found")
    for name in names:
        ok, details = check_skill(name)
        if not ok:
            failures.extend(f"{name}: {d}" for d in details)
    for label, result in [
        ("placeholders", check_placeholders()),
        ("local-discovery", check_local_discovery()),
        ("installer", check_installer()),
    ]:
        ok, details = result
        if not ok:
            failures.extend(f"{label}: {d}" for d in details)
    for f in failures:
        print(f"FAIL {f}", file=sys.stderr)
    print(f"verified {len(names)} skill(s)" if not failures else f"{len(failures)} failure(s)")
    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
