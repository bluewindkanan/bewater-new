from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_insight_craft_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-insight-craft"))
    validate_skill_evals(REPO / "evals", "bw-insight-craft")


def test_generation_has_ladder_and_methods():
    text = (skill_dir(REPO, "bw-insight-craft") / "references" / "insight-generation.md").read_text()
    for token in ["Accepted Belief", "Pearl", "Code", "Force"]:
        assert token in text, f"insight-generation missing {token}"


def test_fpet_lists_four_standards():
    text = (skill_dir(REPO, "bw-insight-craft") / "references" / "fpet-judgment.md").read_text()
    for token in ["Fresh", "Potent", "Energizing", "Truth"]:
        assert token in text, f"fpet-judgment missing {token}"
