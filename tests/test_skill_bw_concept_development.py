# tests/test_skill_bw_concept_development.py
from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_concept_development_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-concept-development"))
    validate_skill_evals(REPO / "evals", "bw-concept-development")


def test_concept_portfolio_template_has_lifecycle_fields():
    text = (skill_dir(REPO, "bw-concept-development") / "references"
            / "concept-portfolio-template.md").read_text()
    for token in ["kind: concept-portfolio", "concepts:", "CI-001", "source_seed_id:",
                  "opportunity_area_id:", "idea_pool_ref:", "parent_ids:",
                  "selected_concept_ids", "recycle-to-OA"]:
        assert token in text, f"concept-portfolio-template missing {token}"


def test_concept_development_cites_lifecycle_contract():
    text = (skill_dir(REPO, "bw-concept-development") / "SKILL.md").read_text()
    assert "idea-concept-solution-lifecycle.md" in text
    assert "recycle-to-OA" in text
    assert "bw-backtrack" in text
    assert "confirmed" in text.lower()
    assert "stop" in text.lower() and "human" in text.lower()
