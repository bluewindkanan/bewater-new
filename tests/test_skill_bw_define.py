from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_define_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-define"))
    validate_skill_evals(REPO / "evals", "bw-define")


def test_define_routes_to_strategy_capabilities_and_gate():
    text = (skill_dir(REPO, "bw-define") / "references" / "stage.md").read_text()
    for name in ["bw-directional-hypothesis", "bw-strategy-statement", "bw-opportunity-area",
                 "bw-assumption-map", "bw-strategy-gate"]:
        assert name in text, f"define stage.md missing {name}"


def test_define_starts_with_directional_hypotheses_from_signed_insights():
    text = "\n".join(
        path.read_text().lower()
        for path in sorted(skill_dir(REPO, "bw-define").rglob("*.md"))
    )
    for token in ["begins", "bw-directional-hypothesis", "signed insight"]:
        assert token in text, f"Define directional-hypothesis boundary missing {token!r}"
