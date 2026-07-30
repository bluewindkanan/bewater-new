"""Eval run-result record schema and persistence (spec §11.1)."""
from __future__ import annotations

import json
from pathlib import Path


RESULT_FIELDS = [
    "scenario_id",
    "target_skill",
    "mode",
    "repetition",
    "fresh_context_id",
    "cwd",
    "temp_home",
    "project_local_skills",
    "global_skills",
    "model",
    "transcript_path",
    "checks",
    "forbidden_triggered",
    "verdict",
    "reviewer",
]


def derive_verdict(payload: dict) -> str:
    """Derive verdict from checks and forbidden_triggered (spec §11.1).

    Rules:
    - "needs-review" if any check's verdict is "needs-review"
    - "green" if every check's verdict is "pass" AND forbidden_triggered is empty
    - "red" otherwise
    """
    checks = payload.get("checks", [])
    forbidden_triggered = payload.get("forbidden_triggered", [])

    # If any check needs-review, overall verdict is needs-review
    if any(check.get("verdict") == "needs-review" for check in checks):
        return "needs-review"

    # If all checks pass AND no forbidden behaviors triggered, green
    if all(check.get("verdict") == "pass" for check in checks) and not forbidden_triggered:
        return "green"

    # Otherwise red
    return "red"


def write_result(eval_root: Path, skill: str, mode: str, scenario_id: str, rep: int, payload: dict) -> Path:
    """Write a result record to evals/{skill}/{mode}/{scenario_id}-r{rep}.json.

    The verdict is DERIVED from checks/forbidden_triggered (spec §11.1) — any
    caller-supplied verdict is ignored and replaced by the derived value.
    """
    # Derive and set verdict (do not trust caller-supplied verdict)
    payload["verdict"] = derive_verdict(payload)

    skill_dir = eval_root / "evals" / skill / mode
    skill_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{scenario_id}-r{rep}.json"
    path = skill_dir / filename
    path.write_text(json.dumps(payload, indent=2))
    return path


def read_results(eval_root: Path, skill: str, mode: str, scenario_id: str) -> list[dict]:
    """Read all result records for a given scenario."""
    skill_dir = eval_root / "evals" / skill / mode
    if not skill_dir.exists():
        return []
    results = []
    for f in skill_dir.glob(f"{scenario_id}-r*.json"):
        results.append(json.loads(f.read_text()))
    return results
