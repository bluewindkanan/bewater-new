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


def write_result(eval_root: Path, skill: str, mode: str, scenario_id: str, rep: int, payload: dict) -> Path:
    """Write a result record to evals/{skill}/{mode}/{scenario_id}-r{rep}.json."""
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
