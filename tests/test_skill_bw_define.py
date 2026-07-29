from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_define_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-define"))
    validate_skill_evals(REPO / "evals", "bw-define")


def test_define_routes_to_strategy_capabilities_and_gate():
    text = (skill_dir(REPO, "bw-define") / "references" / "stage.md").read_text()
    for name in ["bw-strategy-statement", "bw-opportunity-area",
                 "bw-assumption-map", "bw-strategy-gate"]:
        assert name in text, f"define stage.md missing {name}"
