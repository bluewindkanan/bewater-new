from __future__ import annotations

import re
from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_insight_craft_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-insight-craft"))
    validate_skill_evals(REPO / "evals", "bw-insight-craft")


def test_generation_has_ladder_and_methods():
    text = (skill_dir(REPO, "bw-insight-craft") / "references" / "insight-generation.md").read_text()
    for token in ["Accepted Belief", "Pearl", "Code", "Force"]:
        assert token in text, f"insight-generation missing {token}"


def test_fpet_lists_four_standards():
    text = (skill_dir(REPO, "bw-insight-craft") / "references" / "fpet-judgment.md").read_text()
    for token in ["Fresh", "Potent", "Energizing", "Truth"]:
        assert token in text, f"fpet-judgment missing {token}"


def test_fpet_expansion_does_not_drift():
    # F/P/E/T canonically expands to Fresh/Potent/Energizing/Truth. A prior drift
    # to Foundational/Proven/Exclusive/Translational silently changed signoff
    # semantics, so guard the canonical expansion across the whole skill.
    text = "\n".join(
        path.read_text()
        for path in sorted(skill_dir(REPO, "bw-insight-craft").rglob("*.md"))
    )
    for token in ["Foundational", "Proven", "Exclusive", "Translational"]:
        assert token not in text, f"drifted F/P/E/T expansion {token!r} must not appear in insight-craft"


def test_fpet_downgrade_requires_observable_fact():
    # A failed F/P/E/T candidate is a Fact only when directly observed; otherwise
    # it stays a candidate belief or explanatory hypothesis. The reference must
    # match the SKILL body and must not state an unconditional downgrade.
    text = (skill_dir(REPO, "bw-insight-craft") / "references" / "fpet-judgment.md").read_text()
    assert "explanatory hypothesis" in text.lower()
    assert "downgraded back to a fact" not in text.lower()


def test_insight_craft_is_a_define_capability_and_stops_at_insights():
    text = "\n".join(
        path.read_text().lower()
        for path in sorted(skill_dir(REPO, "bw-insight-craft").rglob("*.md"))
    )
    for token in [
        "kind: insights",
        "stage: define",
        "does not create directional hypotheses",
        "explanatory hypothesis",
        "not a directional hypothesis",
        "define capability",
    ]:
        assert token in text, f"Insight craft boundary missing {token!r}"


def test_signoff_question_must_express_every_candidate():
    # A host structured-question tool caps visible options (4 in Claude Code). Candidates
    # can outnumber that cap; option-per-candidate then silently drops a candidate from
    # the human's signoff decision. The surface must adapt, never the candidate set.
    text = re.sub(
        r"\s+", " ", (skill_dir(REPO, "bw-insight-craft") / "SKILL.md").read_text()
    ).lower()
    for token in [
        "every candidate",
        "option limit",
        "never silently drop",
        "free-form",
    ]:
        assert token in text, f"signoff surface contract missing {token!r}"


def test_insight_craft_consumes_research_ingredients_and_owns_generation():
    # Research hands Insight Ingredients to Insight Craft. Insight Craft performs the
    # creative/evaluative transformation into Insight candidates and keeps F/P/E/T and
    # the human signature. Research labels (tension, reframe candidate) are ingredients,
    # not pre-approved Insights.
    text = "\n".join(
        path.read_text().lower()
        for path in sorted(skill_dir(REPO, "bw-insight-craft").rglob("*.md"))
    )
    for token in [
        "insight ingredients",
        "patterns",
        "tensions",
        "anomalies",
        "challenged accepted beliefs",
        "reframe candidates",
        "strategic relevance",
        "accepted beliefs",
        "research supplies",
        "owns insight generation",
        "f/p/e/t",
        "not pre-approved insights",
    ]:
        assert token in text, f"Insight-craft ingredient contract missing {token!r}"
