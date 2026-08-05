from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_directional_hypothesis_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-directional-hypothesis"))
    validate_skill_evals(REPO / "evals", "bw-directional-hypothesis")


def test_hypothesis_template_has_by_we_resulting():
    text = (skill_dir(REPO, "bw-directional-hypothesis") / "references" / "hypothesis-template.md").read_text()
    for token in ["By", "We can", "Resulting in", "kind: directional-hypothesis", "stage: define"]:
        assert token in text, f"hypothesis-template missing {token}"


def test_directional_hypothesis_uses_signed_insights_as_define_inputs():
    root = skill_dir(REPO, "bw-directional-hypothesis")
    text = "\n".join(path.read_text().lower() for path in sorted(root.rglob("*.md")))
    for token in ["signed insight", "derived_from", "stage: define"]:
        assert token in text, f"Directional hypothesis contract missing {token!r}"
