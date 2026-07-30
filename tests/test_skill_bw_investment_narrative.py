# tests/test_skill_bw_investment_narrative.py
from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_investment_narrative_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-investment-narrative"))
    validate_skill_evals(REPO / "evals", "bw-investment-narrative")


def test_narrative_template_has_six_parts_and_sourced_financials():
    text = (skill_dir(REPO, "bw-investment-narrative") / "references" / "investment-narrative-template.md").read_text()
    for part in ["Brief", "Opportunity", "Solution", "Why big", "Financial Case", "Roadmap"]:
        assert part in text, f"narrative-template missing part {part}"
    for token in ["kind: investment-narrative", "source", "CAC", "retention"]:
        assert token in text, f"narrative-template missing {token}"
