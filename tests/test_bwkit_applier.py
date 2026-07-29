"""TDD for bwkit.applier — schema-agnostic idempotent action-plan applier (spec §12.3)."""
from __future__ import annotations

import io
import json
from pathlib import Path

import pytest

from bwkit import applier, cas, cli


@pytest.fixture
def v5_root(tmp_path: Path) -> Path:
    bw = tmp_path / "_bewater"
    bw.mkdir()
    (bw / "config.yaml").write_text("schema_version: 1\nrevision: 4\nactive_branch: BR-001\n")
    (bw / "records").mkdir()
    return tmp_path


def _plan(action_id, steps, owner="bw-strategy-gate"):
    return {"action_id": action_id, "owner": owner, "steps": steps}


def test_write_new_creates_file_then_idempotent_skip(v5_root):
    plan = _plan("ACT-1", [{"step_id": "s1", "op": "write_new",
                            "path": "_bewater/records/B-001-baseline.yaml",
                            "new_text": "baseline body\n"}])
    r = applier.apply_plan(v5_root, plan)
    assert r["action_status"] == "applied"
    assert r["results"][0]["status"] == "applied"
    assert (v5_root / "_bewater/records/B-001-baseline.yaml").read_text() == "baseline body\n"
    r2 = applier.apply_plan(v5_root, plan)
    assert r2["results"][0]["status"] == "skipped"


def test_cas_commit_bumps_then_idempotent_skip(v5_root):
    new_cfg = "schema_version: 1\nrevision: 5\nactive_branch: BR-001\n"
    plan = _plan("ACT-2", [{"step_id": "s1", "op": "cas_commit",
                            "path": "_bewater/config.yaml",
                            "expected_revision": 4, "new_text": new_cfg}])
    r = applier.apply_plan(v5_root, plan)
    assert r["results"][0]["status"] == "applied"
    assert "revision: 5" in (v5_root / "_bewater/config.yaml").read_text()
    r2 = applier.apply_plan(v5_root, plan)
    assert r2["results"][0]["status"] == "skipped"


def test_cas_commit_conflict_fails_without_write(v5_root):
    # another writer bumps config to 5 first
    (v5_root / "_bewater/config.yaml").write_text("schema_version: 1\nrevision: 5\n")
    plan = _plan("ACT-3", [{"step_id": "s1", "op": "cas_commit",
                            "path": "_bewater/config.yaml",
                            "expected_revision": 4, "new_text": "schema_version: 1\nrevision: 5\nX\n"}])
    r = applier.apply_plan(v5_root, plan)
    assert r["action_status"] == "failed"
    assert r["results"][0]["status"] == "failed"
    txt = (v5_root / "_bewater/config.yaml").read_text()
    assert "revision: 5" in txt and "X" not in txt


def test_write_new_conflict_with_different_content_fails(v5_root):
    (v5_root / "_bewater/records/B-001-baseline.yaml").write_text("something else\n")
    plan = _plan("ACT-4", [{"step_id": "s1", "op": "write_new",
                            "path": "_bewater/records/B-001-baseline.yaml",
                            "new_text": "baseline body\n"}])
    r = applier.apply_plan(v5_root, plan)
    assert r["results"][0]["status"] == "failed"


def test_failure_stops_and_keeps_prior_applied_steps(v5_root):
    plan = _plan("ACT-5", [
        {"step_id": "s1", "op": "write_new", "path": "_bewater/records/B-001-baseline.yaml",
         "new_text": "ok\n"},
        {"step_id": "s2", "op": "cas_commit", "path": "_bewater/config.yaml",
         "expected_revision": 99, "new_text": "schema_version: 1\nrevision: 100\n"},
    ])
    r = applier.apply_plan(v5_root, plan)
    assert r["action_status"] == "failed"
    assert r["results"][0]["status"] == "applied"
    assert r["results"][1]["status"] == "failed"
    assert len(r["results"]) == 2


def test_malformed_plan_raises(v5_root):
    with pytest.raises(applier.PlanError):
        applier.apply_plan(v5_root, {"action_id": "X"})
    with pytest.raises(applier.PlanError):
        applier.apply_plan(v5_root, {"action_id": "X", "steps": [
            {"step_id": "s1", "op": "cas_commit", "path": "_bewater/config.yaml"}]})


def test_lock_is_released_after_apply(v5_root):
    plan = _plan("ACT-6", [{"step_id": "s1", "op": "write_new",
                            "path": "_bewater/records/x.txt", "new_text": "x"}])
    applier.apply_plan(v5_root, plan)
    assert cas.lock_status(v5_root) is None


def test_lock_is_released_even_on_failure(v5_root):
    plan = _plan("ACT-7", [{"step_id": "s1", "op": "cas_commit",
                            "path": "_bewater/config.yaml", "expected_revision": 99,
                            "new_text": "schema_version: 1\nrevision: 100\n"}])
    applier.apply_plan(v5_root, plan)
    assert cas.lock_status(v5_root) is None


def test_cli_plan_apply_reads_stdin_prints_result(v5_root):
    new_cfg = "schema_version: 1\nrevision: 5\nactive_branch: BR-001\n"
    plan = json.dumps(_plan("ACT-8", [{"step_id": "s1", "op": "cas_commit",
                                       "path": "_bewater/config.yaml",
                                       "expected_revision": 4, "new_text": new_cfg}]))
    rc = cli.main(["plan", "apply", str(v5_root)], _stdin=io.StringIO(plan))
    assert rc == 0
    assert "revision: 5" in (v5_root / "_bewater/config.yaml").read_text()


def test_cli_plan_apply_returns_nonzero_on_failure(v5_root):
    plan = json.dumps(_plan("ACT-9", [{"step_id": "s1", "op": "cas_commit",
                                       "path": "_bewater/config.yaml",
                                       "expected_revision": 99, "new_text": "schema_version: 1\nrevision: 100\n"}]))
    rc = cli.main(["plan", "apply", str(v5_root)], _stdin=io.StringIO(plan))
    assert rc == 1
