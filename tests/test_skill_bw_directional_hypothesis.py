from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_directional_hypothesis_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-directional-hypothesis"))
    validate_skill_evals(REPO / "evals", "bw-directional-hypothesis")


def test_hypothesis_template_has_by_we_resulting():
    text = (skill_dir(REPO, "bw-directional-hypothesis") / "references" / "hypothesis-template.md").read_text()
    for token in ["By", "We can", "Resulting in", "kind: hypothesis"]:
        assert token in text, f"hypothesis-template missing {token}"
