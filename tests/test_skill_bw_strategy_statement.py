from __future__ import annotations
from pathlib import Path
from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_strategy_statement_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-strategy-statement"))
    validate_skill_evals(REPO / "evals", "bw-strategy-statement")


def test_strategy_statement_is_knife_not_summary():
    text = (skill_dir(REPO, "bw-strategy-statement") / "references" / "strategy-statement.md").read_text()
    for token in ["knife", "summary", "kind: strategy", "locked"]:
        assert token in text, f"strategy-statement missing {token}"
