from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_4c_research_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-4c-research"))
    validate_skill_evals(REPO / "evals", "bw-4c-research")


def test_4c_framework_lists_four_cs():
    text = (skill_dir(REPO, "bw-4c-research") / "references" / "4c-framework.md").read_text()
    for token in ["Consumer", "Company", "Category", "Channel"]:
        assert token in text, f"4c-framework missing {token}"


def test_learning_plan_has_four_questions():
    text = (skill_dir(REPO, "bw-4c-research") / "references" / "learning-plan.md").read_text()
    for token in ["found", "not-found", "deepen", "droppable"]:
        assert token in text, f"learning-plan missing {token}"
