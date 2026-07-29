from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SHARED = REPO / ".claude" / "skills" / "_bw-shared"


def _frontmatter(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


@pytest.mark.parametrize("name", ["ledger-schema.md", "gate-criteria.md", "glossary.md"])
def test_shared_reference_exists_with_contract_frontmatter(name):
    text = (SHARED / name).read_text()
    fm = _frontmatter(text)
    assert "contract_id:" in fm
    assert "contract_version:" in fm
    assert "source_sections:" in fm


def test_ledger_schema_covers_core_fields_and_enums():
    text = (SHARED / "ledger-schema.md").read_text()
    for token in ["record_revision", "supersedes_ref", "BR-001", "A-001",
                  "achilles", "L1", "L4", "schema_version"]:
        assert token in text, f"ledger-schema missing {token}"


def test_gate_criteria_covers_g1_readiness():
    text = (SHARED / "gate-criteria.md").read_text()
    for token in ["G1", "directional", "strategy", "opportunity", "Achilles", "Money", "Magic"]:
        assert token in text, f"gate-criteria missing {token}"
