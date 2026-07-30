# tests/test_skill_bw_ideate.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_ideate_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-ideate"))
    validate_skill_evals(REPO / "evals", "bw-ideate")


def test_ideate_routes_to_concept_card():
    text = (skill_dir(REPO, "bw-ideate") / "references" / "stage.md").read_text()
    assert "bw-concept-card" in text
    assert "ideate" in text.lower()
