from __future__ import annotations

import csv
from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]
SKILL = "bw-discovery-research"
TOOLKIT_FIELDS = [
    "id",
    "type",
    "4c_fit",
    "use_when",
    "avoid_when",
    "evidence_output",
    "key_limitation",
    "execution_need",
]
VALID_4CS = {"Consumer", "Company", "Category", "Channel"}
VALID_TOOLKIT_TYPES = {"collection_method", "analysis_framework"}


def _skill_text() -> str:
    root = skill_dir(REPO, SKILL)
    return "\n".join(path.read_text() for path in sorted(root.rglob("*.md"))).lower()


def _toolkit_rows() -> list[dict[str, str]]:
    path = skill_dir(REPO, SKILL) / "references" / "research-toolkit.csv"
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def _workflow_text() -> str:
    return " ".join((skill_dir(REPO, SKILL) / "SKILL.md").read_text().lower().split())


def test_bw_discovery_research_is_well_formed():
    validate_skill(skill_dir(REPO, SKILL))
    validate_skill_evals(REPO / "evals", SKILL)


def test_discovery_research_embeds_a_living_discover_plan_in_research_artifact():
    text = _skill_text()
    for token in [
        "kind: research",
        "discover plan",
        "discovery mission",
        "decision",
        "risk priorit",
        "4c coverage",
        "learning question",
        "evidence need",
        "research mission",
        "stop rule",
        "same artifact id",
        "supersedes_ref",
        "current charter revision",
        "active root assumptions",
    ]:
        assert token in text, f"Discovery research contract missing {token!r}"


def test_discovery_research_uses_iterative_sprints_not_primary_then_secondary_stages():
    text = _skill_text()
    for token in [
        "research sprint",
        "research debrief",
        "learned",
        "unresolved",
        "deepen",
        "drop",
        "new questions",
        "continue",
        "synthesize",
        "edge",
    ]:
        assert token in text, f"Discovery sprint loop missing {token!r}"
    assert "primary research stage" not in text
    assert "secondary research stage" not in text


def test_discovery_research_reviews_and_persists_a_plan_before_each_sprint_loop():
    workflow = _workflow_text()
    markers = [
        "4. draft or update the current discover plan",
        "6. run the in-context plan self-review",
        "7. when the plan is new or materially changed, persist",
        "8. execute only the reviewed research missions",
        "its research sprint debrief",
        "updated current discover plan",
    ]

    positions = []
    cursor = 0
    for marker in markers:
        position = workflow.find(marker, cursor)
        assert position >= 0, f"Discovery workflow missing {marker!r}"
        positions.append(position)
        cursor = position + len(marker)

    assert positions == sorted(positions)
    assert "self-review the updated plan before this revision is written" in workflow


def test_discovery_research_self_review_has_brainstorming_checks_without_review_output():
    text = _skill_text()
    for token in [
            "same four checks as the brainstorming self-review",
        "placeholder scan",
        "incomplete required",
        "vague mission",
        "internal consistency",
        "scope check",
        "ambiguity check",
        "automatically repair",
        "ask one question and stop",
        "do not persist or execute",
        "review creates no artifact, review state, signoff, or human gate",
    ]:
        assert token in text, f"Discovery Plan self-review contract missing {token!r}"


def test_discovery_research_separates_plan_from_latest_sprint_and_debrief_in_one_chain():
    text = _skill_text()
    for token in [
        "current discover plan — required sections",
        "latest research sprint — after execution only",
        "research sprint debrief and plan delta — after execution only",
        "revision 1 contains a reviewed current discover plan",
        "do not create empty sprint or debrief sections",
        "omit them rather than adding empty placeholders",
        "same artifact id",
        "supersedes_ref",
        "derived_from",
    ]:
        assert token in text, f"Discovery research artifact-layout contract missing {token!r}"


def test_discovery_research_allows_secondary_only_and_keeps_evidence_provenance():
    text = _skill_text()
    for token in [
        "secondary_only",
        "secondary_first",
        "mixed",
        "primary trigger",
        "evidence limitations",
        "evidence_origin",
        "primary | secondary",
        "evidence_form",
        "behavior",
        "self-report",
        "expert-judgment",
        "market-data",
        "document",
    ]:
        assert token in text, f"Discovery evidence strategy missing {token!r}"
    assert "primary_required" not in text


def test_discovery_research_does_not_require_a_three_facts_per_4c_quota():
    text = _skill_text()
    for forbidden in ["≥3", ">=3", "at least three sourced facts", "three sourced facts"]:
        assert forbidden not in text, f"Discovery research retains a mechanical fact quota: {forbidden!r}"
    assert "coverage compass" in text


def test_discovery_research_uses_a_compact_open_world_toolkit_index():
    root = skill_dir(REPO, SKILL)
    references = root / "references"
    markdown_refs = {path.name for path in references.glob("*.md")}
    assert markdown_refs == {"4c-framework.md", "discover-plan.md"}
    assert (references / "research-toolkit.csv").is_file()

    text = _skill_text()
    for token in [
        "seed library",
        "not a whitelist",
        "ad-hoc method",
        "why selected",
        "what it cannot prove",
        "not automatically",
    ]:
        assert token in text, f"Open-world toolkit contract missing {token!r}"


def test_research_toolkit_csv_has_a_small_typed_schema():
    path = skill_dir(REPO, SKILL) / "references" / "research-toolkit.csv"
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == TOOLKIT_FIELDS
        rows = list(reader)

    assert 1 <= len(rows) <= 20
    assert len({row["id"] for row in rows}) == len(rows)
    assert {row["type"] for row in rows} == VALID_TOOLKIT_TYPES
    for row in rows:
        assert all(row[field].strip() for field in TOOLKIT_FIELDS), row
        assert {part.strip() for part in row["4c_fit"].split("|")} <= VALID_4CS


def test_research_toolkit_covers_collection_and_analysis_without_hardcoding_connectors():
    rows = _toolkit_rows()
    corpus = "\n".join(" ".join(row.values()).lower() for row in rows)
    for token in [
        "desk", "internal", "interview", "observation", "expert", "usability",
        "behavior", "aeiou", "jtbd", "journey", "competitive", "five forces",
        "value chain", "ecosystem", "analog",
    ]:
        assert token in corpus, f"Toolkit is missing planned coverage for {token!r}"
    for forbidden in ["browser", "spreadsheet", "web search"]:
        assert forbidden not in corpus, f"Toolkit hardcodes an execution connector: {forbidden!r}"
