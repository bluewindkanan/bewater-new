from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_immersion_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-immersion"))
    validate_skill_evals(REPO / "evals", "bw-immersion")


def test_immersion_stage_routes_to_charter():
    text = (skill_dir(REPO, "bw-immersion") / "references" / "stage.md").read_text()
    assert "bw-project-charter" in text
    assert "immersion" in text.lower()
