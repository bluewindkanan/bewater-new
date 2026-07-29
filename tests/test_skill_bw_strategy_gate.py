from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_strategy_gate_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-strategy-gate"))
    validate_skill_evals(REPO / "evals", "bw-strategy-gate")


def test_gate_references_cover_record_baseline_exits_plan():
    refs = skill_dir(REPO, "bw-strategy-gate") / "references"
    rec = (refs / "decision-record-template.md").read_text()
    base = (refs / "baseline-template.md").read_text()
    ex = (refs / "exits.md").read_text()
    ap = (refs / "action-plan.md").read_text()
    for token in ["decision_id", "exit", "action_plan"]:
        assert token in rec, f"decision-record missing {token}"
    for token in ["baseline_id", "gate: G1"]:
        assert token in base, f"baseline-template missing {token}"
    for exit_name in ["Go", "Conditional Go", "Recycle", "Pivot", "Kill"]:
        assert exit_name in ex, f"exits missing {exit_name}"
    assert "bwkit plan apply" in ap
