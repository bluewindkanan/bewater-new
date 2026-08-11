from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_solution_shape_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-solution-shape"))
    validate_skill_evals(REPO / "evals", "bw-solution-shape")


def test_solution_template_matches_spec_frontmatter():
    text = (skill_dir(REPO, "bw-solution-shape") / "references" / "solution-template.md").read_text()
    for token in ["kind: solution", "stage: shape", "source_concepts:",
                  "portfolio_ref:", "concept_ids:", "path:", "definition:",
                  "how_it_works:", "how_to_implement:", "how_it_makes_money:",
                  "validation:", "content_gaps:", "applicability_exceptions:"]:
        assert token in text, f"solution-template missing {token}"


def test_solution_template_uses_exact_runtime_field_names():
    text = (skill_dir(REPO, "bw-solution-shape") / "references" / "solution-template.md").read_text()
    for token in [
        "product_or_service_design:",
        "step:",
        "action:",
        "evidence_refs:",
        "design_refs:",
        "owner:",
        "pilot_and_rollout:",
        "adoption_retention_frequency_assumptions:",
        "development_and_operating_costs:",
        "assumption:",
        "source:",
        "sensitivity:",
        "consumer_desire:",
        "commercial_value:",
        "feasibility_and_implementation:",
        "claim:",
    ]:
        assert token in text, f"solution-template missing canonical field {token}"
    for legacy in [
        "action_or_state_change:",
        "design_or_prototype_refs:",
        "accountable_role:",
        "pilot_and_rollout_logic:",
        "financial_assumptions:",
    ]:
        assert legacy not in text, f"solution-template retains superseded field {legacy}"


def test_solution_skill_enforces_maturity_and_authority_boundaries():
    text = (skill_dir(REPO, "bw-solution-shape") / "SKILL.md").read_text()
    for token in ["Focused", "Detailed", "Persuasive", "L4", "linear-refine",
                  "hybridize", "content_gaps", "applicability_exceptions"]:
        assert token in text, f"bw-solution-shape missing {token}"
    assert "invent" in text
    assert "stop" in text.lower() and "human" in text.lower()
