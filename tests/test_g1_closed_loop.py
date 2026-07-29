"""Deterministic G1 closed-loop test: a real G1 Go action plan applied via bwkit.
Exercises the gate's state mechanics end-to-end (baseline created, branch advanced,
idempotent re-run) without an LLM in the loop."""
from __future__ import annotations

from pathlib import Path

from bwkit import applier

CONFIG_R4 = """schema_version: 1
revision: 4
active_branch: BR-001
branches:
  BR-001:
    status: active
    current_stage: define
    active_baselines: {G1: null, G2: null}
"""

BASELINE = """schema_version: 1
baseline_id: B-001
gate: G1
decision_id: D-001
branch_id: BR-001
"""


def _scaffold(tmp_path: Path) -> Path:
    bw = tmp_path / "_bewater"
    bw.mkdir()
    (bw / "records").mkdir()
    (bw / "config.yaml").write_text(CONFIG_R4)
    return tmp_path


def _go_plan():
    advanced = CONFIG_R4.replace("revision: 4", "revision: 5").replace(
        "current_stage: define", "current_stage: ideate").replace(
        "active_baselines: {G1: null", "active_baselines: {G1: B-001")
    return {"action_id": "ACT-001", "owner": "bw-strategy-gate", "steps": [
        {"step_id": "s1", "op": "write_new",
         "path": "_bewater/records/B-001-baseline.yaml", "new_text": BASELINE},
        {"step_id": "s2", "op": "cas_commit", "path": "_bewater/config.yaml",
         "expected_revision": 4, "new_text": advanced},
    ]}


def test_g1_go_creates_baseline_and_advances_branch(tmp_path):
    root = _scaffold(tmp_path)
    r = applier.apply_plan(root, _go_plan())
    assert r["action_status"] == "applied"
    cfg = (root / "_bewater/config.yaml").read_text()
    assert "revision: 5" in cfg
    assert "current_stage: ideate" in cfg
    assert "B-001" in cfg.split("active_baselines")[1]
    assert (root / "_bewater/records/B-001-baseline.yaml").read_text() == BASELINE


def test_g1_go_plan_is_idempotent_on_rerun(tmp_path):
    root = _scaffold(tmp_path)
    applier.apply_plan(root, _go_plan())
    r2 = applier.apply_plan(root, _go_plan())
    assert r2["action_status"] == "applied"
    assert all(res["status"] == "skipped" for res in r2["results"])
