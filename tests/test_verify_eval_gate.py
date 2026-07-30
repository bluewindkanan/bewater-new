"""TDD for the §11.3 eval result-gate in verify.py (skips cleanly before results exist)."""
from __future__ import annotations
from pathlib import Path
import json
import verify


def test_check_eval_results_skips_when_no_results():
    ok, detail = verify.check_eval_results()
    # no results stored yet anywhere -> skip, not fail
    assert ok is True
    assert any("deferred" in str(d) or "not yet" in str(d) for d in detail) or detail == []


def test_check_eval_results_fails_on_green_with_untriggered_red_requirement(tmp_path, monkeypatch):
    # fabricate a RED result that wrongly passed (verdict green) -> gate must fail
    fake_evals = tmp_path / "evals"
    skill = fake_evals / "bw-start" / "red"; skill.mkdir(parents=True)
    (skill / "BWST-R1-r1.json").write_text(json.dumps({
        "scenario_id": "BWST-R1", "target_skill": "bw-start", "mode": "red", "repetition": 1,
        "verdict": "green", "fresh_context_id": "c", "cwd": "", "temp_home": "",
        "project_local_skills": [], "global_skills": [], "model": "", "transcript_path": "",
        "checks": [], "forbidden_triggered": [], "reviewer": None}))
    monkeypatch.setattr(verify, "EVALS", fake_evals)
    monkeypatch.setattr(verify, "list_eval_scenarios", lambda root: [("bw-start", "red", "BWST-R1", 1)],
                       raising=False)
    ok, detail = verify.check_eval_results()
    assert ok is False and any("red" in str(d).lower() for d in detail)


def test_check_eval_results_passes_red_with_needs_review_and_reviewer(tmp_path, monkeypatch):
    # RED result with needs-review + non-null reviewer -> gate PASSES
    fake_evals = tmp_path / "evals"
    skill = fake_evals / "bw-start" / "red"; skill.mkdir(parents=True)
    (skill / "BWST-R1-r1.json").write_text(json.dumps({
        "scenario_id": "BWST-R1", "target_skill": "bw-start", "mode": "red", "repetition": 1,
        "verdict": "needs-review", "fresh_context_id": "c", "cwd": "", "temp_home": "",
        "project_local_skills": [], "global_skills": [], "model": "", "transcript_path": "",
        "checks": [], "forbidden_triggered": [], "reviewer": "human-reviewer"}))
    monkeypatch.setattr(verify, "EVALS", fake_evals)
    monkeypatch.setattr(verify, "list_eval_scenarios", lambda root: [("bw-start", "red", "BWST-R1", 1)],
                       raising=False)
    ok, detail = verify.check_eval_results()
    assert ok is True


def test_check_eval_results_passes_green_with_needs_review_and_reviewer(tmp_path, monkeypatch):
    # GREEN result with needs-review + non-null reviewer -> gate PASSES
    fake_evals = tmp_path / "evals"
    skill = fake_evals / "bw-start" / "scenarios"; skill.mkdir(parents=True)
    (skill / "BWST-S1-r1.json").write_text(json.dumps({
        "scenario_id": "BWST-S1", "target_skill": "bw-start", "mode": "green", "repetition": 1,
        "verdict": "needs-review", "fresh_context_id": "c", "cwd": "", "temp_home": "",
        "project_local_skills": [], "global_skills": [], "model": "", "transcript_path": "",
        "checks": [], "forbidden_triggered": [], "reviewer": "human-reviewer"}))
    monkeypatch.setattr(verify, "EVALS", fake_evals)
    monkeypatch.setattr(verify, "list_eval_scenarios", lambda root: [("bw-start", "scenarios", "BWST-S1", 1)],
                       raising=False)
    ok, detail = verify.check_eval_results()
    assert ok is True


def test_check_eval_results_fails_on_needs_review_without_reviewer(tmp_path, monkeypatch):
    # needs-review result with null reviewer -> gate FAILS
    fake_evals = tmp_path / "evals"
    skill = fake_evals / "bw-start" / "scenarios"; skill.mkdir(parents=True)
    (skill / "BWST-S1-r1.json").write_text(json.dumps({
        "scenario_id": "BWST-S1", "target_skill": "bw-start", "mode": "green", "repetition": 1,
        "verdict": "needs-review", "fresh_context_id": "c", "cwd": "", "temp_home": "",
        "project_local_skills": [], "global_skills": [], "model": "", "transcript_path": "",
        "checks": [], "forbidden_triggered": [], "reviewer": None}))
    monkeypatch.setattr(verify, "EVALS", fake_evals)
    monkeypatch.setattr(verify, "list_eval_scenarios", lambda root: [("bw-start", "scenarios", "BWST-S1", 1)],
                       raising=False)
    ok, detail = verify.check_eval_results()
    assert ok is False
    assert any("reviewer" in str(d).lower() for d in detail)


def test_check_eval_results_fails_on_green_with_verdict_red(tmp_path, monkeypatch):
    # GREEN result with verdict red -> gate FAILS
    fake_evals = tmp_path / "evals"
    skill = fake_evals / "bw-start" / "scenarios"; skill.mkdir(parents=True)
    (skill / "BWST-S1-r1.json").write_text(json.dumps({
        "scenario_id": "BWST-S1", "target_skill": "bw-start", "mode": "green", "repetition": 1,
        "verdict": "red", "fresh_context_id": "c", "cwd": "", "temp_home": "",
        "project_local_skills": [], "global_skills": [], "model": "", "transcript_path": "",
        "checks": [], "forbidden_triggered": [], "reviewer": None}))
    monkeypatch.setattr(verify, "EVALS", fake_evals)
    monkeypatch.setattr(verify, "list_eval_scenarios", lambda root: [("bw-start", "scenarios", "BWST-S1", 1)],
                       raising=False)
    ok, detail = verify.check_eval_results()
    assert ok is False
    assert any("red" in str(d).lower() for d in detail)
