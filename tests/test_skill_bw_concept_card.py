# tests/test_skill_bw_concept_card.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_concept_card_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-concept-card"))
    validate_skill_evals(REPO / "evals", "bw-concept-card")


def test_concept_card_template_has_fields_and_criteria():
    text = (skill_dir(REPO, "bw-concept-card") / "references" / "concept-card-template.md").read_text()
    for token in ["kind: concept", "altitude", "healthy anxiety", "consumer_insight"]:
        assert token in text, f"concept-card-template missing {token}"
