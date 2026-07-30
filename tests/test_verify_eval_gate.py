"""TDD for the §11.3 eval result-gate in verify.py (skips cleanly before results exist)."""
from __future__ import annotations
from pathlib import Path
import json
import verify


def test_check_eval_results_skips_when_no_results(tmp_path, monkeypatch):
    # Point at an empty tmp_path so the gate sees zero results → deferred skip.
    # Must use monkeypatch because the real repo may contain pilot results.
    monkeypatch.setattr(verify, "EVALS", tmp_path / "evals")
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
    # GREEN result with needs-review + non-null reviewer -> gate PASSES.
    # GREEN results live in evals/{skill}/green/ (manifest bucket 'scenarios'
    # maps to result dir 'green' per spec §11.1 / pilot F2).
    fake_evals = tmp_path / "evals"
    skill = fake_evals / "bw-start" / "green"; skill.mkdir(parents=True)
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
    skill = fake_evals / "bw-start" / "green"; skill.mkdir(parents=True)
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
    skill = fake_evals / "bw-start" / "green"; skill.mkdir(parents=True)
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


def test_check_eval_results_finds_green_result_in_green_dir(tmp_path, monkeypatch):
    # Pilot gap F2: GREEN results are written to evals/{skill}/green/ (manifest
    # bucket 'scenarios' -> result dir 'green'). The gate MUST find them there and
    # NOT look in evals/{skill}/scenarios/ (the manifest bucket).
    fake_evals = tmp_path / "evals"
    green = fake_evals / "bw-start" / "green"; green.mkdir(parents=True)
    (green / "BWST-S1-r1.json").write_text(json.dumps({
        "scenario_id": "BWST-S1", "target_skill": "bw-start", "mode": "green", "repetition": 1,
        "verdict": "green", "fresh_context_id": "c", "cwd": "", "temp_home": "",
        "project_local_skills": [], "global_skills": [], "model": "", "transcript_path": "",
        "checks": [{"id": "c", "verdict": "pass"}], "forbidden_triggered": [], "reviewer": None}))
    # Do NOT put anything in scenarios/ — if the gate looked there it would
    # report a missing-result failure instead of passing.
    monkeypatch.setattr(verify, "EVALS", fake_evals)
    monkeypatch.setattr(verify, "list_eval_scenarios",
                       lambda root: [("bw-start", "scenarios", "BWST-S1", 1)], raising=False)
    ok, detail = verify.check_eval_results()
    assert ok is True, detail
    # And there must be no scenarios/ dir at all.
    assert not (fake_evals / "bw-start" / "scenarios").exists()


def test_check_eval_results_skips_skills_without_results(tmp_path, monkeypatch):
    # Pilot gap F3: a partial pilot run (results for ONE skill, not others) must
    # NOT fail on the skills lacking results. Scenarios with NO result files are
    # not-yet-run -> SKIPPED, while the skill that DOES have results is still
    # enforced (here, a bad RED-verdict-green on bw-start still fails).
    fake_evals = tmp_path / "evals"
    red = fake_evals / "bw-start" / "red"; red.mkdir(parents=True)
    (red / "BWST-R1-r1.json").write_text(json.dumps({
        "scenario_id": "BWST-R1", "target_skill": "bw-start", "mode": "red", "repetition": 1,
        "verdict": "green", "fresh_context_id": "c", "cwd": "", "temp_home": "",
        "project_local_skills": [], "global_skills": [], "model": "", "transcript_path": "",
        "checks": [], "forbidden_triggered": [], "reviewer": None}))
    monkeypatch.setattr(verify, "EVALS", fake_evals)
    monkeypatch.setattr(verify, "list_eval_scenarios", lambda root: [
        ("bw-start", "red", "BWST-R1", 1),       # has a result -> enforced
        ("bw-start", "scenarios", "BWST-G1", 1), # no result file -> skipped
        ("bw-ideate", "scenarios", "BWID-G1", 1),# no result file -> skipped
        ("bw-define", "red", "BWDF-R1", 1),      # no result file -> skipped
    ], raising=False)
    ok, detail = verify.check_eval_results()
    # The single enforced failure is the RED-with-green on bw-start.
    assert ok is False
    assert any("BWST-R1" in str(d) for d in detail)
    # None of the not-yet-run skills/scenarios are reported as failures.
    joined = " ".join(str(d) for d in detail)
    assert "BWST-G1" not in joined
    assert "BWID-G1" not in joined
    assert "BWDF-R1" not in joined


def test_check_eval_results_partial_run_all_clean_passes(tmp_path, monkeypatch):
    # F3 positive case: results present for one clean skill (GREEN green), the
    # other skills have no results yet -> gate PASSES overall (skips the rest).
    fake_evals = tmp_path / "evals"
    green = fake_evals / "bw-start" / "green"; green.mkdir(parents=True)
    (green / "BWST-G1-r1.json").write_text(json.dumps({
        "scenario_id": "BWST-G1", "target_skill": "bw-start", "mode": "green", "repetition": 1,
        "verdict": "green", "fresh_context_id": "c", "cwd": "", "temp_home": "",
        "project_local_skills": [], "global_skills": [], "model": "", "transcript_path": "",
        "checks": [{"id": "c", "verdict": "pass"}], "forbidden_triggered": [], "reviewer": None}))
    monkeypatch.setattr(verify, "EVALS", fake_evals)
    monkeypatch.setattr(verify, "list_eval_scenarios", lambda root: [
        ("bw-start", "scenarios", "BWST-G1", 1),
        ("bw-ideate", "scenarios", "BWID-G1", 1),
    ], raising=False)
    ok, detail = verify.check_eval_results()
    assert ok is True, detail

