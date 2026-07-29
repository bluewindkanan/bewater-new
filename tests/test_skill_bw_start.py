from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_start_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-start"))
    validate_skill_evals(REPO / "evals", "bw-start")


def test_state_bootstrap_carries_v5_scaffold():
    text = (skill_dir(REPO, "bw-start") / "references" / "state-bootstrap.md").read_text()
    for token in ["schema_version: 1", "next_ids:", "branch:", "artifact:", "decision:",
                  "active_branch: BR-001", "current_stage: immersion", "decision_authority:",
                  "assumptions: {}", "conditions: {}"]:
        assert token in text, f"state-bootstrap missing {token}"


def test_routing_cites_precedence_and_reconcile():
    text = (skill_dir(REPO, "bw-start") / "references" / "routing.md").read_text()
    for token in ["open condition", "active-baseline", "direct-write", "bwkit"]:
        assert token.lower() in text.lower(), f"routing missing {token}"
