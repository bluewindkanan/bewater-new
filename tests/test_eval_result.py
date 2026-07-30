"""TDD for eval result records (spec §11.1) + manifest checks field."""
from __future__ import annotations
import json
from pathlib import Path
import yaml
from evals._harness import result, loader


def test_write_and_read_result_roundtrip(tmp_path: Path):
    payload = {
        "scenario_id": "BWSG-S1", "target_skill": "bw-strategy-gate", "mode": "green",
        "repetition": 1, "fresh_context_id": "ctx-1", "cwd": "/tmp/x", "temp_home": "/tmp/h",
        "project_local_skills": ["bw-strategy-gate"], "global_skills": [],
        "model": "claude-x", "transcript_path": "/tmp/t.jsonl",
        "checks": [{"id": "presents_exits", "type": "transcript_regex_present",
                    "verdict": "pass", "detail": "matched Go|Kill"}],
        "forbidden_triggered": [], "verdict": "green", "reviewer": None,
    }
    p = result.write_result(tmp_path, "bw-strategy-gate", "green", "BWSG-S1", 1, payload)
    assert p.name == "BWSG-S1-r1.json"
    rs = result.read_results(tmp_path, "bw-strategy-gate", "green", "BWSG-S1")
    assert len(rs) == 1 and rs[0]["verdict"] == "green"


def test_manifest_accepts_optional_checks(tmp_path: Path):
    m = tmp_path / "s.yaml"
    m.write_text(yaml.safe_dump({
        "scenario_id": "X-S1", "target_skill": "bw-start", "prompt": "p",
        "required_assertions": ["a"], "forbidden_behaviors": [], "repetition_count": 3,
        "checks": [{"id": "c1", "type": "transcript_contains", "params": {"needle": "bw-"}}],
    }))
    data = loader.load_manifest(m)            # must not raise
    assert data["checks"][0]["type"] == "transcript_contains"


def test_verdict_is_needs_review_when_any_check_needs_review(tmp_path: Path):
    payload = {"scenario_id": "X", "target_skill": "bw-start", "mode": "green", "repetition": 1,
               "fresh_context_id": "c", "cwd": "", "temp_home": "", "project_local_skills": [],
               "global_skills": [], "model": "", "transcript_path": "",
               "checks": [{"id": "sem", "type": "transcript_contains", "verdict": "needs-review",
                           "detail": ""}], "forbidden_triggered": [], "verdict": "needs-review",
               "reviewer": None}
    p = result.write_result(tmp_path, "bw-start", "green", "X", 1, payload)
    assert json.loads(p.read_text())["verdict"] == "needs-review"
