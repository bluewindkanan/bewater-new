from __future__ import annotations

from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_project_charter_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-project-charter"))
    validate_skill_evals(REPO / "evals", "bw-project-charter")


def test_charter_template_has_dual_sided_four_fields():
    text = (skill_dir(REPO, "bw-project-charter") / "references" / "charter-template.md").read_text()
    for token in ["dual_sided", "consumer_value_proposition", "consumer_target",
                  "commercial_value_proposition", "leverageable_assets", "artifact_id"]:
        assert token in text, f"charter-template missing {token}"


def test_root_assumptions_reference_layer_root():
    text = (skill_dir(REPO, "bw-project-charter") / "references" / "root-assumptions.md").read_text()
    assert "layer: root" in text
    assert "record_revision" in text
