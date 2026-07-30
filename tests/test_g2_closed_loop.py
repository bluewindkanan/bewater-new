"""Deterministic G2 closed-loop test: a real G2 Go action plan applied via bwkit. Exercises the
gate's state mechanics end-to-end (G2 baseline + execution handoff created, branch advanced to
handoff-ready, active_execution_handoff set, idempotent re-run) without an LLM in the loop."""
from __future__ import annotations

from pathlib import Path

from bwkit import applier

CONFIG_R5 = """schema_version: 1
revision: 5
active_branch: BR-001
active_execution_handoff: null
branches:
  BR-001:
    status: active
    current_stage: shape
    active_baselines: {G1: B-001, G2: null}
"""

BASELINE = """schema_version: 1
baseline_id: B-002
gate: G2
decision_id: D-002
branch_id: BR-001
"""

HANDOFF = """---
schema_version: 1
branch_id: BR-001
status: active
source_g2_decision: gate:D-002
baseline_ref: baseline:B-002
validated_solutions: []
investment_narrative_ref: artifact:ART-008@1
---
G2 execution handoff body.
"""


def _scaffold(tmp_path: Path) -> Path:
    bw = tmp_path / "_bewater"
    bw.mkdir()
    (bw / "records").mkdir()
    out = tmp_path / "_bewater-output"
    out.mkdir()
    (bw / "config.yaml").write_text(CONFIG_R5)
    return tmp_path


def _go_plan():
    advanced = (CONFIG_R5
                .replace("revision: 5", "revision: 6")
                .replace("current_stage: shape", "current_stage: handoff-ready")
                .replace("active_baselines: {G1: B-001, G2: null}",
                         "active_baselines: {G1: B-001, G2: B-002}")
                .replace("active_execution_handoff: null",
                         "active_execution_handoff: gate:D-002"))
    return {"action_id": "ACT-002", "owner": "bw-concept-gate", "steps": [
        {"step_id": "s1", "op": "write_new",
         "path": "_bewater/records/B-002-baseline.yaml", "new_text": BASELINE},
        {"step_id": "s2", "op": "write_new",
         "path": "_bewater-output/execution-handoff.md", "new_text": HANDOFF},
        {"step_id": "s3", "op": "cas_commit", "path": "_bewater/config.yaml",
         "expected_revision": 5, "new_text": advanced},
    ]}


def test_g2_go_creates_baseline_handoff_and_advances(tmp_path):
    root = _scaffold(tmp_path)
    r = applier.apply_plan(root, _go_plan())
    assert r["action_status"] == "applied"
    cfg = (root / "_bewater/config.yaml").read_text()
    assert "revision: 6" in cfg
    assert "current_stage: handoff-ready" in cfg
    assert "G2: B-002" in cfg
    assert "active_execution_handoff: gate:D-002" in cfg
    assert (root / "_bewater/records/B-002-baseline.yaml").read_text() == BASELINE
    assert (root / "_bewater-output/execution-handoff.md").read_text() == HANDOFF


def test_g2_go_plan_is_idempotent_on_rerun(tmp_path):
    root = _scaffold(tmp_path)
    applier.apply_plan(root, _go_plan())
    r2 = applier.apply_plan(root, _go_plan())
    assert r2["action_status"] == "applied"
    assert all(res["status"] == "skipped" for res in r2["results"])
