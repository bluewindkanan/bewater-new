from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SHARED = REPO / ".claude" / "skills" / "_bw-shared"
SKILLS = REPO / ".claude" / "skills"


def _frontmatter(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


@pytest.mark.parametrize("name", ["ledger-schema.md", "gate-criteria.md"])
def test_shared_reference_exists_with_contract_frontmatter(name):
    text = (SHARED / name).read_text()
    fm = _frontmatter(text)
    assert "contract_id:" in fm
    assert "contract_version:" in fm


def test_runtime_skill_docs_exclude_source_citations():
    docs = [*SHARED.glob("*.md"), *SKILLS.glob("bw-*/SKILL.md"),
            *SKILLS.glob("bw-*/references/*.md")]
    provenance = re.compile(r"\b(?:spec|bewater-core)\b|§|source_sections:")
    offenders = [str(path.relative_to(SKILLS)) for path in docs
                if provenance.search(path.read_text())]
    assert not offenders, f"runtime docs retain source citations: {offenders}"


def test_ledger_schema_covers_core_fields_and_enums():
    text = (SHARED / "ledger-schema.md").read_text()
    for token in ["record_revision", "supersedes_ref", "BR-001", "A-001",
                  "achilles", "L1", "L4", "schema_version"]:
        assert token in text, f"ledger-schema missing {token}"


def test_ledger_schema_defines_living_knowledge_identity_and_counter():
    text = (REPO / "src/skills/_bw-shared/ledger-schema.md").read_text().lower()
    assert "k-001 knowledge" in text
    assert "knowledge:k-001@1" in text
    config = text.split("## config.yaml", 1)[1].split("## ledger.yaml", 1)[0]
    assert "knowledge" in config
    assert "action,evidence" not in config
    assert "knowledge workpapers" in text and "in-place bump" in text
    assert "current research head" in text
    assert "historical research revisions" in text


def test_gate_criteria_covers_g1_readiness():
    text = (SHARED / "gate-criteria.md").read_text()
    for token in ["G1", "directional", "strategy", "opportunity", "Achilles", "Money", "Magic"]:
        assert token in text, f"gate-criteria missing {token}"
