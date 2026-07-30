# tests/test_skill_bw_concept_gate.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_concept_gate_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-concept-gate"))
    validate_skill_evals(REPO / "evals", "bw-concept-gate")


def test_gate_references_cover_g2_records_and_handoff():
    refs = skill_dir(REPO, "bw-concept-gate") / "references"
    rec = (refs / "decision-record-template.md").read_text()
    base = (refs / "baseline-template.md").read_text()
    ex = (refs / "exits.md").read_text()
    ap = (refs / "action-plan.md").read_text()
    ho = (refs / "handoff-template.md").read_text()
    for token in ["decision_id", "gate: G2", "investment-decision", "exit", "action_plan",
                  "supersedes_handoff_ref"]:
        assert token in rec, f"decision-record missing {token}"
    for token in ["baseline_id", "gate: G2", "investment narrative"]:
        assert token in base, f"baseline-template missing {token}"
    for exit_name in ["Go", "Conditional Go", "Recycle", "Pivot", "Kill"]:
        assert exit_name in ex, f"exits missing {exit_name}"
    assert "execution-handoff" in ex and "active_execution_handoff" in ap
    for token in ["execution-handoff.md", "source G2 decision", "baseline reference"]:
        assert token in ho, f"handoff-template missing {token}"
