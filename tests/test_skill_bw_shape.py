# tests/test_skill_bw_shape.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_shape_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-shape"))
    validate_skill_evals(REPO / "evals", "bw-shape")


def test_shape_routes_to_the_three_capabilities_and_gate():
    text = (skill_dir(REPO, "bw-shape") / "references" / "stage.md").read_text()
    for cap in ("bw-experiment", "bw-solution-shape", "bw-investment-narrative", "bw-concept-gate"):
        assert cap in text, f"stage.md missing {cap}"
    assert "shape" in text.lower()
