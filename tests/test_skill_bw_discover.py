from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_discover_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-discover"))
    validate_skill_evals(REPO / "evals", "bw-discover")


def test_discover_routes_to_research_and_insight():
    text = (skill_dir(REPO, "bw-discover") / "references" / "stage.md").read_text()
    assert "bw-4c-research" in text
    assert "bw-insight-craft" in text
