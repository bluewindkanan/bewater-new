"""bwkit/applier — schema-agnostic, idempotent, resumable action-plan applier (stdlib-only).
Reuses cas.commit + cas.acquire_lock. Never parses business YAML; the caller builds the
JSON plan. See design spec §12.3, §6.5, §8.3. Maps to §5.7 step 2 (lock) + step 6/7 (CAS)
+ §6.5/§8.3 ordered-step recovery."""
from __future__ import annotations

from pathlib import Path

from . import cas


class PlanError(Exception):
    """A plan is malformed."""


def apply_plan(root, plan: dict) -> dict:
    root = Path(root)
    action_id = plan.get("action_id") or "ACT-?"
    owner = plan.get("owner") or f"plan:{action_id}"
    steps = plan.get("steps")
    if not isinstance(steps, list):
        raise PlanError("plan missing 'steps' list")

    cas.acquire_lock(root, owner)  # LockError propagates -> caller coordinates
    results, action_status = [], "applied"
    try:
        for step in steps:
            res = _apply_step(root, step)
            results.append(res)
            if res["status"] == "failed":
                action_status = "failed"
                break
    finally:
        cas.release_lock(root, owner)

    return {"action_id": action_id, "results": results, "action_status": action_status}


def _apply_step(root: Path, step: dict) -> dict:
    step_id = step.get("step_id") or "?"
    op = step.get("op")
    rel = step.get("path")
    new_text = step.get("new_text")
    if op not in ("cas_commit", "write_new") or not rel or new_text is None:
        raise PlanError(f"step {step_id} malformed (need op/path/new_text)")
    path = root / rel

    if op == "write_new":
        if path.exists():
            if path.read_text(encoding="utf-8", errors="replace") == new_text:
                return {"step_id": step_id, "status": "skipped", "detail": "already present"}
            return {"step_id": step_id, "status": "failed",
                    "detail": "target exists with different content"}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_text, encoding="utf-8")
        return {"step_id": step_id, "status": "applied", "detail": "wrote new file"}

    expected = step.get("expected_revision")
    if not isinstance(expected, int):
        raise PlanError(f"step {step_id} cas_commit needs integer expected_revision")
    try:
        current = cas.read_revision(path)
    except (FileNotFoundError, KeyError) as e:
        return {"step_id": step_id, "status": "failed", "detail": f"cannot read revision: {e}"}

    if current == expected:
        try:
            r = cas.commit(path, new_text, expected)
        except (cas.CasConflict, cas.BadRevisionBump) as e:
            return {"step_id": step_id, "status": "failed", "detail": f"CAS error: {e}"}
        return {"step_id": step_id, "status": "applied", "detail": f"revision->{r['revision']}"}
    if current == expected + 1:
        if path.read_text(encoding="utf-8", errors="replace") == new_text:
            return {"step_id": step_id, "status": "skipped", "detail": "already applied"}
        return {"step_id": step_id, "status": "failed",
                "detail": f"revision {current} present with different content"}
    return {"step_id": step_id, "status": "failed",
            "detail": f"revision conflict: expected {expected}, current {current}"}
