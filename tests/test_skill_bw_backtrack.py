# tests/test_skill_bw_backtrack.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_backtrack_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-backtrack"))
    validate_skill_evals(REPO / "evals", "bw-backtrack")


def test_backtrack_references_cover_record_lineage_loopsize():
    refs = skill_dir(REPO, "bw-backtrack") / "references"
    bt = (refs / "backtrack-record-template.md").read_text()
    lin = (refs / "lineage.md").read_text()
    loop = (refs / "loop-size.md").read_text()
    for token in ["backtrack_id", "loop_type", "affected_refs", "baseline_refs",
                  "gates_to_rerun", "target_stage", "action_plan"]:
        assert token in bt, f"backtrack-record missing {token}"
    for token in ["transitive_dependents", "derived_from", "evidence_refs",
                  "branch inheritance", "baseline membership"]:
        assert token in lin, f"lineage missing {token}"
    for token in ["small", "large", "active_baselines"]:
        assert token in loop, f"loop-size missing {token}"
