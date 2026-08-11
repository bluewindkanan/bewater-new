# tests/test_gate_criteria_g2.py
from __future__ import annotations
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GC = REPO / "src" / "skills" / "_bw-shared" / "gate-criteria.md"


def test_g2_block_is_authored():
    text = GC.read_text()
    for token in ["1-2 complete validated Solutions", "five canonical blocks",
                  "content_gaps", "Focused", "Detailed", "Persuasive",
                  "Achilles", "L4", "six-part", "financial assumption",
                  "impossible not to invest"]:
        assert token in text, f"gate-criteria missing G2 token {token}"


def test_phase2_kind_specific_readiness_is_filled():
    text = GC.read_text()
    for token in ["concept portfolio", "solution:", "investment narrative:"]:
        assert token in text, f"gate-criteria missing Phase-2 kind readiness {token}"


def test_g1_counts_one_opportunity_portfolio_head():
    text = GC.read_text()
    for token in ["one current `kind: opportunity` Portfolio", "opportunity_areas[]", "2–4", "OA-NNN"]:
        assert token in text, f"gate-criteria missing Opportunity Portfolio rule {token}"


def test_gate_contract_never_chooses_an_exit():
    text = GC.read_text()
    assert "It never chooses\nan exit." in text
