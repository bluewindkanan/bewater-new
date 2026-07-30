# tests/test_gate_criteria_g2.py
from __future__ import annotations
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GC = REPO / ".claude" / "skills" / "_bw-shared" / "gate-criteria.md"


def test_g2_block_is_authored():
    text = GC.read_text()
    # the G2 criteria list (spec §6.3)
    for token in ["1-2 validated solutions", "Achilles", "L4", "six-part",
                  "financial assumption", "impossible not to invest"]:
        assert token in text, f"gate-criteria missing G2 token {token}"


def test_phase2_kind_specific_readiness_is_filled():
    text = GC.read_text()
    for token in ["concept portfolio", "solution:", "investment narrative:"]:
        assert token in text, f"gate-criteria missing Phase-2 kind readiness {token}"
