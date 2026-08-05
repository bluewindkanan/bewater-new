from __future__ import annotations

from pathlib import Path

import yaml

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_discover_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-discover"))
    validate_skill_evals(REPO / "evals", "bw-discover")


def test_discover_routes_to_research_and_insight():
    text = (skill_dir(REPO, "bw-discover") / "references" / "stage.md").read_text()
    assert "bw-discovery-research" in text
    assert "bw-insight-craft" in text
    assert "bw-4c-research" not in text


def test_discover_exits_with_signed_insights_not_directional_hypotheses():
    text = "\n".join(
        path.read_text().lower()
        for path in sorted(skill_dir(REPO, "bw-discover").rglob("*.md"))
    )
    for token in ["insight portfolio", "f/p/e/t", "does not produce directional hypotheses"]:
        assert token in text, f"Discover output boundary missing {token!r}"


def test_discover_consumes_charter_and_assumptions_not_assessment_as_fact():
    root = skill_dir(REPO, "bw-discover")
    text = "\n".join(path.read_text() for path in root.rglob("*.md")).lower()
    for token in [
        "current charter revision",
        "active root assumptions",
        "formal discover inputs",
        "initial assessment",
        "candidate beliefs",
        "not as facts",
        "bw-project-charter",
    ]:
        assert token in text, f"Discover contract missing {token!r}"
    assert "separate discover brief" not in text


def test_discover_formal_input_is_charter_revision_and_active_root_assumptions():
    text = (skill_dir(REPO, "bw-discover") / "SKILL.md").read_text()
    for token in ["current charter revision", "active root assumptions", "initial-assessment"]:
        assert token in text, f"Discover missing formal-input rule: {token}"
    assert "Fact" in text and "candidate" in text


def test_discover_routes_missing_formal_inputs_back_to_charter():
    text = (skill_dir(REPO, "bw-discover") / "references" / "stage.md").read_text()
    assert "missing" in text
    assert "bw-project-charter" in text
    assert "does not create a Discover Brief" in text


def test_discover_reads_only_snapshot_matching_assessment_as_advisory():
    text = "\n".join(
        path.read_text().lower()
        for path in sorted(skill_dir(REPO, "bw-discover").rglob("*.md"))
    )
    for token in [
        "exactly matches",
        "same branch",
        "candidate insights",
        "candidate judgments to validate",
        "core conflict / tension",
        "priority challenge",
        "most promising direction",
        "candidate research path",
        "key risks",
        "disconfirming questions",
        "advisory reference",
    ]:
        assert token in text, f"Discover assessment protocol missing {token}"


def test_discover_ignores_mismatched_assessment_without_blocking():
    text = (skill_dir(REPO, "bw-discover") / "SKILL.md").read_text().lower()
    for token in [
        "stale",
        "cross-branch",
        "snapshot mismatch",
        "ignore",
        "advisory gap",
        "does not block discover",
    ]:
        assert token in text, f"Discover advisory-gap contract missing {token}"
    for promoted in ["fact", "evidence", "accepted belief", "f/p/e/t insight"]:
        assert promoted in text


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
