from __future__ import annotations

from pathlib import Path

import yaml

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_discover_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-discover"))
    validate_skill_evals(REPO / "evals", "bw-discover")


def test_discover_routes_to_research_only():
    text = (skill_dir(REPO, "bw-discover") / "references" / "stage.md").read_text()
    assert "bw-discovery-research" in text
    assert "bw-insight-craft" not in text  # insight-craft moved to Define
    assert "bw-4c-research" not in text


def test_discover_exits_with_research_evidence_not_insights():
    text = "\n".join(
        path.read_text().lower()
        for path in sorted(skill_dir(REPO, "bw-discover").rglob("*.md"))
    )
    for token in ["research evidence", "4c coverage", "does not produce insights", "does not produce directional hypotheses"]:
        # "does not produce insights or directional hypotheses" is the phrase, so "does not produce directional hypotheses" won't match
        assert "does not produce" in text and "directional hypotheses" in text, f"Discover output boundary missing directional hypotheses boundary"


def test_discover_consumes_only_charter_and_never_assessment():
    root = skill_dir(REPO, "bw-discover")
    text = "\n".join(path.read_text() for path in root.rglob("*.md")).lower()
    for token in [
        "current charter revision",
        "formal discover inputs",
        "initial assessment",
        "must not consume",
        "candidate seed",
        "bw-immersion",
    ]:
        assert token in text, f"Discover contract missing {token!r}"
    assert "separate discover brief" not in text


def test_discover_formal_input_is_charter_revision_only():
    text = (skill_dir(REPO, "bw-discover") / "SKILL.md").read_text().lower()
    for token in ["current charter revision", "only formal prerequisite", "initial-assessment"]:
        assert token in text, f"Discover missing formal-input rule: {token}"
    assert "active root assumptions" not in text.lower()


def test_discover_routes_missing_formal_inputs_back_to_charter():
    text = (skill_dir(REPO, "bw-discover") / "references" / "stage.md").read_text()
    assert "missing" in text
    assert "bw-immersion" in text
    assert "does not create" in text.lower() and "discover brief" in text.lower()


def test_discover_does_not_read_assessment_as_evidence_even_when_current():
    text = "\n".join(
        path.read_text().lower()
        for path in sorted(skill_dir(REPO, "bw-discover").rglob("*.md"))
    )
    assert "does not read assessment content" not in text
    for token in [
        "what to inspect next",
        "candidate seed",
        "never as facts",
        "does not seed research as evidence",
    ]:
        assert token in text, f"Discover candidate-seed contract missing {token}"
    for token in ["candidate insights", "most promising direction", "advisory reference"]:
        assert token not in text


def test_discover_assessment_state_never_blocks_or_seeds_research():
    text = (skill_dir(REPO, "bw-discover") / "SKILL.md").read_text().lower()
    for token in [
        "missing, current, or stale",
        "does not block discover",
        "does not seed research as evidence",
        "candidate seed",
    ]:
        assert token in text, f"Discover advisory-gap contract missing {token}"


def test_discover_routes_missing_or_stale_research_plan_to_research_planning():
    text = "\n".join(
        path.read_text().lower()
        for path in sorted(skill_dir(REPO, "bw-discover").rglob("*.md"))
    )
    for token in [
        "research plan",
        "missing or stale",
        "research planning",
        "bw-discovery-research",
        "recommend research planning and stop",
    ]:
        assert token in text
    assert "when assumptions are absent, do not route back" in text


def test_discover_router_reports_knowledge_progress_without_writing():
    text = (skill_dir(REPO, "bw-discover") / "SKILL.md").read_text().lower()
    for token in ["read-only router", "research progress", "knowledge gaps", "exact knowledge refs"]:
        assert token in text
    assert "does not author artifacts" in text


def test_discover_eval_matrix_covers_advisory_match_states():
    scenarios = REPO / "evals" / "bw-discover" / "scenarios"
    names = {path.stem for path in scenarios.glob("*.yaml")}
    assert {
        "orient",
        "missing-assessment",
        "stale-assessment",
        "cross-branch-assessment",
    } <= names


def test_discover_stage_fixture_uses_sanctioned_branch_statuses():
    fixture = REPO / "evals" / "fixtures" / "bw-discover" / "discover-stage" / "_bewater" / "config.yaml"
    config = yaml.safe_load(fixture.read_text())
    statuses = {branch["status"] for branch in config["branches"].values()}
    assert statuses <= {"active", "merged", "killed", "pivoted", "deviated"}
