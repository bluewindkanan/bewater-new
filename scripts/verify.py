"""scripts/verify — authoring-time integrity checks (spec §11.3). Not shipped.
Importable as `verify` (pytest pythonpath includes "scripts"). Each check returns
(ok, details); main() runs them all and exits non-zero on any failure."""
from __future__ import annotations

import json
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
from bwkit import integrity  # noqa: E402
from evals._harness.loader import load_manifest  # noqa: E402

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


def check_integrity():
    """Authoring-time smoke that the Phase 2a integrity helper accepts a clean chain and
    rejects a corrupt one (spec §5.4, §11.3, §12.3)."""
    clean = [
        {"id": "ART-1", "revision": 1, "supersedes": None},
        {"id": "ART-1", "revision": 2, "supersedes": {"id": "ART-1", "revision": 1}},
    ]
    corrupt = [
        {"id": "ART-1", "revision": 1, "supersedes": None},
        {"id": "ART-1", "revision": 1, "supersedes": None},  # duplicate revision
    ]
    if not integrity.check_artifacts(clean)["ok"]:
        return (False, ["clean chain rejected"])
    if integrity.check_artifacts(corrupt)["ok"]:
        return (False, ["corrupt chain accepted"])
    return (True, [])


def check_installer(repo=None, dest=None):
    """Run install.sh --copy into an isolated dest; assert managed markers + bwkit runs.
    Self-created temp dirs are cleaned up; a caller-supplied dest is left intact."""
    repo = _REPO if repo is None else Path(repo)
    if dest is not None:
        return _installer_ok(repo, Path(dest))
    with tempfile.TemporaryDirectory(prefix="bwverify-") as d:
        return _installer_ok(repo, Path(d))


def list_eval_scenarios(evals_root):
    """Walk evals/*/scenarios/*.yaml + evals/*/red/*.yaml and yield scenario info.
    Yields tuples of (skill, bucket, scenario_id, repetition_count) where bucket is
    'scenarios' or 'red'."""
    evals_root = Path(evals_root)
    for skill_dir in sorted(evals_root.glob("bw-*")):
        skill = skill_dir.name
        for bucket in ["scenarios", "red"]:
            bucket_dir = skill_dir / bucket
            if not bucket_dir.exists():
                continue
            for manifest_path in sorted(bucket_dir.glob("*.yaml")):
                try:
                    manifest = load_manifest(manifest_path)
                    yield (skill, bucket, manifest["scenario_id"], manifest["repetition_count"])
                except Exception:
                    # Skip manifests that can't be loaded; will be caught by other checks
                    continue


def check_eval_results(evals_root=None):
    """For every scenario manifest under evals/*/scenarios/ + evals/*/red/, enforce:
    (a) repetition_count result records with complete §11.1 fields exist;
    (b) every RED control's aggregate verdict is 'red';
    (c) every GREEN result verdict is 'green' (all checks pass, no forbidden triggered);
    (d) any 'needs-review' result carries a non-null reviewer.
    Before results exist, returns (True, ["eval results: deferred (§11.1)"]) skip notice.
    """
    evals_root = EVALS if evals_root is None else Path(evals_root)
    details: list[str] = []

    # Collect all expected result files
    expected_results = []
    for skill, bucket, scenario_id, repetition_count in list_eval_scenarios(evals_root):
        for rep in range(1, repetition_count + 1):
            result_file = evals_root / skill / bucket / f"{scenario_id}-r{rep}.json"
            expected_results.append((skill, bucket, scenario_id, rep, result_file))

    # If no result files exist yet, skip cleanly
    if not expected_results:
        return (True, ["eval results: deferred (§11.1)"])

    # Check if any results exist at all
    any_results_exist = any(f.exists() for _, _, _, _, f in expected_results)
    if not any_results_exist:
        return (True, ["eval results: deferred (§11.1)"])

    # Validate each expected result
    for skill, bucket, scenario_id, rep, result_file in expected_results:
        if not result_file.exists():
            details.append(f"{skill}/{bucket}/{scenario_id}-r{rep}: missing result file")
            continue

        try:
            result = json.loads(result_file.read_text())
        except json.JSONDecodeError:
            details.append(f"{skill}/{bucket}/{scenario_id}-r{rep}: invalid JSON")
            continue

        # Check complete §11.1 fields
        required_fields = [
            "scenario_id", "target_skill", "mode", "repetition", "verdict",
            "fresh_context_id", "cwd", "temp_home", "project_local_skills",
            "global_skills", "model", "transcript_path", "checks",
            "forbidden_triggered", "reviewer"
        ]
        missing_fields = [f for f in required_fields if f not in result]
        if missing_fields:
            details.append(f"{skill}/{bucket}/{scenario_id}-r{rep}: missing fields {missing_fields}")
            continue

        # Validate based on bucket type
        if bucket == "red":
            # RED controls MUST have verdict 'red'
            if result.get("verdict") != "red":
                details.append(f"{skill}/{bucket}/{scenario_id}-r{rep}: RED control has verdict '{result.get('verdict')}', expected 'red'")
        else:
            # GREEN scenarios MUST have verdict 'green' (all checks pass, no forbidden triggered)
            if result.get("verdict") != "green":
                details.append(f"{skill}/{bucket}/{scenario_id}-r{rep}: GREEN scenario has verdict '{result.get('verdict')}', expected 'green'")

        # Check needs-review results have non-null reviewer
        if result.get("verdict") == "needs-review" and result.get("reviewer") is None:
            details.append(f"{skill}/{bucket}/{scenario_id}-r{rep}: needs-review verdict requires non-null reviewer")

    return (not details, details)


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
        ("integrity", check_integrity()),
        ("installer", check_installer()),
        ("eval-results", check_eval_results()),
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
