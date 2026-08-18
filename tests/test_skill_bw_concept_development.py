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
                  "review:", "reviewed_concept_ids:", "portfolio_findings:",
                  "selected_concept_ids", "recycle-to-OA"]:
        assert token in text, f"concept-portfolio-template missing {token}"


def test_concept_development_cites_lifecycle_contract():
    text = (skill_dir(REPO, "bw-concept-development") / "SKILL.md").read_text()
    assert "idea-concept-solution-lifecycle.md" in text
    assert "recycle-to-OA" in text
    assert "bw-backtrack" in text
    assert "confirmed" in text.lower()
    assert "stop" in text.lower() and "human" in text.lower()


def test_concept_development_separates_production_from_independent_review():
    root = skill_dir(REPO, "bw-concept-development")
    text = (root / "SKILL.md").read_text().lower()
    review = (root / "references" / "concept-review-contract.md").read_text().lower()
    for token in [
        "fresh-context", "independent reviewer", "cannot mutate", "at most two",
        "needs-revision", "reviewed_concept_ids", "human-only",
        "concept-review-contract.md",
    ]:
        assert token in text, f"concept development missing {token}"
    for token in [
        "contract_id", "review payload", "evaluation.hard", "evaluation.soft",
        "recommended_action", "decision", "merge_into", "exit.selected_concept_ids",
    ]:
        assert token in review, f"concept review contract missing {token}"


def test_concept_development_is_one_to_one_from_each_valid_oa_shortlist():
    text = (skill_dir(REPO, "bw-concept-development") / "SKILL.md").read_text().lower()
    for token in ["exactly one initial concept", "5–8", "same oa", "review.status: ready"]:
        assert token in text, f"concept development funnel missing {token}"
