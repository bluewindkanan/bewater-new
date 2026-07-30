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


def test_write_and_read_result_roundtrip_contradictory_verdict(tmp_path: Path):
    """Derivation should override a caller-supplied contradictory verdict."""
    payload = {
        "scenario_id": "BWSG-S1", "target_skill": "bw-strategy-gate", "mode": "green",
        "repetition": 1, "fresh_context_id": "ctx-1", "cwd": "/tmp/x", "temp_home": "/tmp/h",
        "project_local_skills": ["bw-strategy-gate"], "global_skills": [],
        "model": "claude-x", "transcript_path": "/tmp/t.jsonl",
        "checks": [{"id": "presents_exits", "type": "transcript_regex_present",
                    "verdict": "pass", "detail": "matched Go|Kill"}],
        "forbidden_triggered": [], "verdict": "red",  # Contradictory: all-pass + no forbidden should be green
        "reviewer": None,
    }
    p = result.write_result(tmp_path, "bw-strategy-gate", "green", "BWSG-S1", 1, payload)
    rs = result.read_results(tmp_path, "bw-strategy-gate", "green", "BWSG-S1")
    # Derived verdict should override the contradictory caller-supplied "red"
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
    # Derivation should override caller's verdict
    assert json.loads(p.read_text())["verdict"] == "needs-review"


def test_derive_verdict_needs_review_from_any_check(tmp_path: Path):
    """needs-review when any check verdict is needs-review."""
    payload = {"scenario_id": "X", "target_skill": "bw-start", "mode": "green", "repetition": 1,
               "fresh_context_id": "c", "cwd": "", "temp_home": "", "project_local_skills": [],
               "global_skills": [], "model": "", "transcript_path": "",
               "checks": [{"id": "c1", "type": "transcript_contains", "verdict": "pass", "detail": ""},
                          {"id": "c2", "type": "transcript_contains", "verdict": "needs-review",
                           "detail": "ambiguous"}],
               "forbidden_triggered": [], "verdict": "green", "reviewer": None}
    p = result.write_result(tmp_path, "bw-start", "green", "X", 1, payload)
    # Derived verdict should override the incorrect caller-supplied "green"
    assert json.loads(p.read_text())["verdict"] == "needs-review"


def test_derive_verdict_green_from_all_pass_and_no_forbidden(tmp_path: Path):
    """green when all checks pass AND forbidden_triggered is empty."""
    payload = {"scenario_id": "X", "target_skill": "bw-start", "mode": "green", "repetition": 1,
               "fresh_context_id": "c", "cwd": "", "temp_home": "", "project_local_skills": [],
               "global_skills": [], "model": "", "transcript_path": "",
               "checks": [{"id": "c1", "type": "transcript_contains", "verdict": "pass", "detail": ""},
                          {"id": "c2", "type": "transcript_regex_present", "verdict": "pass",
                           "detail": "matched pattern"}],
               "forbidden_triggered": [], "verdict": "red", "reviewer": None}
    p = result.write_result(tmp_path, "bw-start", "green", "X", 1, payload)
    # Derived verdict should override the incorrect caller-supplied "red"
    assert json.loads(p.read_text())["verdict"] == "green"


def test_derive_verdict_red_from_forbidden_triggered(tmp_path: Path):
    """red when all checks pass but forbidden_triggered is non-empty."""
    payload = {"scenario_id": "X", "target_skill": "bw-start", "mode": "green", "repetition": 1,
               "fresh_context_id": "c", "cwd": "", "temp_home": "", "project_local_skills": [],
               "global_skills": [], "model": "", "transcript_path": "",
               "checks": [{"id": "c1", "type": "transcript_contains", "verdict": "pass", "detail": ""}],
               "forbidden_triggered": ["deleted_user_file"], "verdict": "green", "reviewer": None}
    p = result.write_result(tmp_path, "bw-start", "green", "X", 1, payload)
    # Forbidden behavior should force red despite all-pass checks
    assert json.loads(p.read_text())["verdict"] == "red"


def test_derive_verdict_red_from_fail_check(tmp_path: Path):
    """red when any check verdict is fail."""
    payload = {"scenario_id": "X", "target_skill": "bw-start", "mode": "green", "repetition": 1,
               "fresh_context_id": "c", "cwd": "", "temp_home": "", "project_local_skills": [],
               "global_skills": [], "model": "", "transcript_path": "",
               "checks": [{"id": "c1", "type": "transcript_contains", "verdict": "pass", "detail": ""},
                          {"id": "c2", "type": "transcript_contains", "verdict": "fail",
                           "detail": "needle not found"}],
               "forbidden_triggered": [], "verdict": "green", "reviewer": None}
    p = result.write_result(tmp_path, "bw-start", "green", "X", 1, payload)
    # Fail check should force red
    assert json.loads(p.read_text())["verdict"] == "red"


def test_derive_verdict_green_from_empty_checks_and_no_forbidden(tmp_path: Path):
    """green when checks is empty AND forbidden_triggered is empty."""
    payload = {"scenario_id": "X", "target_skill": "bw-start", "mode": "green", "repetition": 1,
               "fresh_context_id": "c", "cwd": "", "temp_home": "", "project_local_skills": [],
               "global_skills": [], "model": "", "transcript_path": "",
               "checks": [], "forbidden_triggered": [], "verdict": "red", "reviewer": None}
    p = result.write_result(tmp_path, "bw-start", "green", "X", 1, payload)
    # Empty checks + no forbidden = green (derivation overrides caller's red)
    assert json.loads(p.read_text())["verdict"] == "green"
