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
