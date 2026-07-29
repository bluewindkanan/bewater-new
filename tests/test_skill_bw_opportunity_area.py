from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_opportunity_area_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-opportunity-area"))
    validate_skill_evals(REPO / "evals", "bw-opportunity-area")


def test_opportunity_areas_template_has_bounds():
    text = (skill_dir(REPO, "bw-opportunity-area") / "references" / "opportunity-areas.md").read_text()
    for token in ["2", "4", "non-overlapping", "kind: opportunity"]:
        assert token in text, f"opportunity-areas missing {token}"
