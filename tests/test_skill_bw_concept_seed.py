# tests/test_skill_bw_concept_seed.py
from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_concept_seed_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-concept-seed"))
    validate_skill_evals(REPO / "evals", "bw-concept-seed")


def test_idea_pool_template_has_lifecycle_fields():
    text = (skill_dir(REPO, "bw-concept-seed") / "references"
            / "idea-pool-template.md").read_text()
    for token in ["kind: idea-pool", "input_snapshot:", "opportunity_areas:",
                  "opportunity_area_id: OA-001", "CS-001", "idea:",
                  "review:", "status: ready", "recommended_cuts:",
                  "reason:", "rationale:", "confirmed:", "strategy_filter:"]:
        assert token in text, f"idea-pool-template missing {token}"


def test_concept_seed_cites_lifecycle_contract():
    text = (skill_dir(REPO, "bw-concept-seed") / "SKILL.md").read_text()
    assert "idea-concept-solution-lifecycle.md" in text
    assert "10" in text and "15" in text
    assert "one" in text.lower() and "branch" in text.lower()
    assert "stop" in text.lower() and "confirm" in text.lower()


def test_concept_seed_enforces_the_per_oa_hard_funnel_and_lightweight_review():
    text = (skill_dir(REPO, "bw-concept-seed") / "SKILL.md").read_text().lower()
    for token in [
        "10–15", "hard range", "5–8", "recommended_cuts", "rationale",
        "lightweight", "batch", "needs-revision", "never hide",
    ]:
        assert token in text, f"concept seed contract missing {token}"
    assert "soft ceiling" not in text
