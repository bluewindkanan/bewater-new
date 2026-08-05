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


def test_immersion_routes_charter_and_assessment_separately():
    text = "\n".join(
        path.read_text()
        for path in sorted(skill_dir(REPO, "bw-immersion").rglob("*.md"))
    ).lower()
    assert "bw-initial-assessment" in text
    assert "never produce artifacts" in text
    assert "recommend" in text
    assert "missing or needs revision" in text
    assert "missing, failed, or stale" in text


def test_immersion_reports_the_discover_handoff_contract():
    text = "\n".join(
        path.read_text()
        for path in sorted(skill_dir(REPO, "bw-immersion").rglob("*.md"))
    ).lower()
    for token in [
        "discover handoff",
        "formal discover input",
        "charter",
        "root assumptions",
        "initial assessment",
        "auxiliary",
    ]:
        assert token in text, f"Immersion contract missing {token!r}"
    assert "charter + active root assumptions" in text


def test_immersion_recommends_without_advancing_or_recording_a_decision():
    text = (skill_dir(REPO, "bw-immersion") / "SKILL.md").read_text().lower()
    assert "recommend `bw-discover`" in text
    assert "never changes the stage" in text
    assert "never records the user's decision" in text
    assert "current_stage" in text


def test_immersion_requires_matching_snapshot_for_default_discover_recommendation():
    text = (skill_dir(REPO, "bw-immersion") / "SKILL.md").read_text().lower()
    for token in [
        "at least three active root assumptions",
        "exact charter revision",
        "exact active root-assumption revision snapshot",
        "same branch",
        "matching assessment",
        "bw-initial-assessment",
        "recommend `bw-discover`",
    ]:
        assert token in text, f"Immersion routing contract missing {token}"


def test_immersion_assessment_is_not_a_hard_discover_gate():
    text = "\n".join(
        path.read_text().lower()
        for path in sorted(skill_dir(REPO, "bw-immersion").rglob("*.md"))
    )
    assert "not a hard gate" in text
    assert "explicitly asks to continue" in text
    assert "formal discover inputs" in text
    assert "does not equal a decision to continue" in text


def test_immersion_uses_structured_choices_and_never_decides_for_the_user():
    text = "\n".join(
        path.read_text().lower()
        for path in sorted(skill_dir(REPO, "bw-immersion").rglob("*.md"))
    )
    for token in [
        "native structured selection",
        "enter discover",
        "revise charter",
        "pause in immersion",
        "retry assessment",
        "continue without assessment",
        "when native structured selection is unavailable",
        "equivalent text options",
        "never selects on the user's behalf",
    ]:
        assert token in text, f"Immersion structured-choice contract missing {token}"


def test_immersion_eval_matrix_covers_assessment_routing_states():
    scenarios = REPO / "evals" / "bw-immersion" / "scenarios"
    names = {path.stem for path in scenarios.glob("*.yaml")}
    assert {
        "orient",
        "matching-assessment",
        "stale-assessment",
        "explicit-continue",
        "assessment-success-next-action",
        "assessment-failure-next-action",
    } <= names
