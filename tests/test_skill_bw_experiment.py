# tests/test_skill_bw_experiment.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_experiment_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-experiment"))
    validate_skill_evals(REPO / "evals", "bw-experiment")


def test_experiment_template_has_design_record_and_thresholds():
    text = (skill_dir(REPO, "bw-experiment") / "references" / "experiment-template.md").read_text()
    for token in ["kind: experiment", "Design", "Record result", "Kill threshold",
                  "Proceed threshold", "L4", "evidence:E-"]:
        assert token in text, f"experiment-template missing {token}"
