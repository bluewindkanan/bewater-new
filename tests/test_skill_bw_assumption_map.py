from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_assumption_map_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-assumption-map"))
    validate_skill_evals(REPO / "evals", "bw-assumption-map")


def test_assumption_map_has_axes_and_achilles():
    text = (skill_dir(REPO, "bw-assumption-map") / "references" / "assumption-map.md").read_text()
    for token in ["impact", "uncertainty", "Achilles", "category"]:
        assert token in text, f"assumption-map missing {token}"


def test_assumption_map_owns_complete_g1_inventory_after_research_projection():
    text = "\n".join(
        path.read_text().lower()
        for path in sorted(skill_dir(REPO, "bw-assumption-map").rglob("*.md"))
    )
    for token in ["research-derived", "charter-derived", "complete", "g1 inventory", "zero"]:
        assert token in text, f"assumption-map boundary missing {token!r}"
