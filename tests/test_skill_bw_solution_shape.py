from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_solution_shape_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-solution-shape"))
    validate_skill_evals(REPO / "evals", "bw-solution-shape")


def test_solution_template_matches_spec_frontmatter():
    text = (skill_dir(REPO, "bw-solution-shape") / "references" / "solution-template.md").read_text()
    for token in ["kind: solution", "stage: shape", "validation_status: validated",
                  "consumer_value_proposition", "commercial_value_proposition",
                  "leverageable_assets", "tension", "balance_choice"]:
        assert token in text, f"solution-template missing {token}"
