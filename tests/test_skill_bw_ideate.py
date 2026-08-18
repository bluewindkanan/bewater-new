# tests/test_skill_bw_ideate.py
from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_ideate_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-ideate"))
    validate_skill_evals(REPO / "evals", "bw-ideate")


def test_ideate_routes_to_lifecycle_capabilities():
    text = (skill_dir(REPO, "bw-ideate") / "references" / "stage.md").read_text()
    assert "bw-concept-seed" in text
    assert "bw-concept-development" in text
    assert "bw-concept-card" not in text
    assert "concept-portfolio" in text


def test_ideate_handoff_soft_blocks_missing_healthy_anxiety():
    text = (skill_dir(REPO, "bw-ideate") / "references" / "stage.md").read_text()
    assert "healthy anxiety" in text
    assert "soft blocker" in text
    assert "explicit human override" in text
    assert "idea-concept-solution-lifecycle.md" in text


def test_ideate_reports_both_review_checkpoints_and_hard_funnel():
    root = skill_dir(REPO, "bw-ideate")
    text = "\n".join(path.read_text() for path in sorted(root.rglob("*.md"))).lower()
    for token in [
        "10–15", "5–8", "recommended_cuts", "idea pool review",
        "independent concept review", "needs-revision", "review.status: ready",
    ]:
        assert token in text, f"ideate routing missing {token}"
