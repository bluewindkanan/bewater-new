from __future__ import annotations

import csv
from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]
SKILL = "bw-discovery-research"

TOOLKIT_FIELDS = [
    "id",
    "layer",
    "learning_intent",
    "lens_fit",
    "use_when",
    "avoid_when",
    "evidence_or_output",
    "complements",
    "key_limitation",
    "execution_need",
]
TOOLKIT_LAYERS = {
    "collection_method",
    "analysis_framework",
    "validation_method",
    "synthesis_method",
}
TOOLKIT_LENSES = {
    "Consumer",
    "Company",
    "Category",
    "Channel",
    "Technology",
    "Regulation",
    "Economics",
    "Ecosystem",
    "Future",
}
LEARNING_INTENTS = {
    "explore",
    "describe",
    "compare",
    "explain",
    "size",
    "forecast",
    "validate",
    "reframe",
}


def _skill_text() -> str:
    root = skill_dir(REPO, SKILL)
    return "\n".join(path.read_text() for path in sorted(root.rglob("*.md"))).lower()


def _workflow_text() -> str:
    return " ".join((skill_dir(REPO, SKILL) / "SKILL.md").read_text().lower().split())


def _plan_text() -> str:
    return (skill_dir(REPO, SKILL) / "references" / "discover-plan.md").read_text().lower()


def _framework_text() -> str:
    return (skill_dir(REPO, SKILL) / "references" / "4c-framework.md").read_text().lower()


def _toolkit_rows() -> list[dict[str, str]]:
    path = skill_dir(REPO, SKILL) / "references" / "research-toolkit.csv"
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def test_bw_discovery_research_is_well_formed():
    validate_skill(skill_dir(REPO, SKILL))
    validate_skill_evals(REPO / "evals", SKILL)


def test_discovery_research_starts_from_charter_challenge_and_strategic_uncertainty():
    text = _skill_text()
    for token in [
        "kind: research",
        "innovation challenge",
        "research boundary",
        "strategic uncertainties",
        "future strategic choice",
        "current charter revision",
        "active root assumptions",
        "same artifact id",
        "supersedes_ref",
        "derived_from",
        "never claim that a strategy decision already exists",
    ]:
        assert token in text, f"Research entry contract missing {token!r}"
    for forbidden in [
        "primary research stage",
        "secondary research stage",
        "strategy decision as a formal input",
    ]:
        assert forbidden not in text, f"Discovery research retains forbidden entry wording: {forbidden!r}"


def test_discovery_research_runs_an_adaptive_multi_sprint_loop():
    text = _skill_text()
    for token in [
        "orient",
        "living learning agenda",
        "latest research sprint",
        "sprint synthesis",
        "plan delta",
        "continue",
        "deepen",
        "redirect",
        "synthesize",
        "stop",
        "new questions",
        "contradiction",
        "belief change",
        "reframe",
        "remaining uncertainty",
    ]:
        assert token in text, f"Adaptive Sprint loop missing {token!r}"


def test_discovery_research_treats_sprint_as_a_loop_not_a_quota():
    text = _skill_text()
    for token in [
        "no fixed sprint count",
        "one wave's local missions is not, by itself, insight readiness",
    ]:
        assert token in text, f"Sprint-quota contract missing {token!r}"


def test_discovery_research_distinguishes_stable_artifact_state_from_transient_execution_detail():
    text = _skill_text()
    plan = _plan_text()
    for token in [
        "research frame",
        "living learning agenda",
        "evidence references",
        "method limitations",
        "sprint synthesis",
        "insight ingredients",
        "remaining uncertainty",
    ]:
        assert token in text, f"Stable artifact contract missing {token!r}"
    for transient in [
        "worker count and topology",
        "routine connector",
        "unused toolkit",
        "transient",
    ]:
        assert transient in plan, f"Transient execution contract missing {transient!r}"


def test_4c_framework_keeps_base_lenses_and_adds_conditional_extended_lenses():
    text = _framework_text()
    for token in [
        "consumer",
        "company",
        "category",
        "channel",
        "technology",
        "regulation",
        "economics",
        "ecosystem",
        "future",
        "blind spot",
        "coverage compass",
        "a lens never implies a task, report chapter, method, or worker",
    ]:
        assert token in text, f"4C framework lens contract missing {token!r}"


def test_discovery_research_reference_set_and_selective_toolkit_loading():
    root = skill_dir(REPO, SKILL)
    references = root / "references"
    markdown_refs = {path.name for path in references.glob("*.md")}
    assert markdown_refs == {"4c-framework.md", "discover-plan.md", "method-bundles.md"}
    assert (references / "research-toolkit.csv").is_file()

    text = _skill_text()
    for token in [
        "seed library",
        "not a whitelist",
        "load the toolkit selectively",
        "ad-hoc method",
        "why selected",
        "what it cannot prove",
        "not automatically",
    ]:
        assert token in text, f"Open-world toolkit contract missing {token!r}"


def test_research_toolkit_csv_uses_the_layered_schema():
    path = skill_dir(REPO, SKILL) / "references" / "research-toolkit.csv"
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == TOOLKIT_FIELDS
        rows = list(reader)

    assert len(rows) >= 1
    assert len({row["id"] for row in rows}) == len(rows)
    assert {row["layer"] for row in rows} == TOOLKIT_LAYERS

    all_intents: set[str] = set()
    for row in rows:
        assert all(row[field].strip() for field in TOOLKIT_FIELDS), row
        assert row["layer"] in TOOLKIT_LAYERS
        intents = {part.strip() for part in row["learning_intent"].split("|") if part.strip()}
        assert intents, row
        assert intents <= LEARNING_INTENTS, row
        all_intents |= intents
        lenses = {part.strip() for part in row["lens_fit"].split("|") if part.strip()}
        assert lenses, row
        assert lenses <= TOOLKIT_LENSES, row
    assert all_intents == LEARNING_INTENTS


def test_research_toolkit_covers_the_layered_method_families_without_hardcoding_connectors():
    rows = _toolkit_rows()
    corpus = "\n".join(" ".join(row.values()).lower() for row in rows)
    for token in [
        # collection
        "desk", "internal", "interview", "observation", "expert", "usability",
        "behavioral", "survey", "patent", "regulatory", "social",
        # analysis
        "sizing", "segmentation", "competitive", "five forces", "value chain",
        "profit pool", "ecosystem", "jtbd", "journey", "pricing", "unit economics",
        "trend", "weak signal", "scenario", "analogy", "causal",
        # validation
        "triangulation", "disconfirming", "contradiction", "sensitivity",
        "alternative explanation", "transferability",
        # synthesis
        "pattern", "anomaly", "accepted belief", "belief shift", "tension",
        "reframe", "collision", "strategic relevance",
    ]:
        assert token in corpus, f"Toolkit is missing planned coverage for {token!r}"
    for forbidden in ["browser", "spreadsheet", "web search"]:
        assert forbidden not in corpus, f"Toolkit hardcodes an execution connector: {forbidden!r}"


def test_discovery_research_composes_smallest_complementary_method_bundles():
    text = _skill_text()
    for token in [
        "method bundle",
        "evidence need before method selection",
        "smallest complementary",
        "reject redundant",
        "do not require exactly one method from every layer",
        "execution_need against tools available in the current host",
        "no method registry hardcodes a connector name",
    ]:
        assert token in text, f"Method Bundle contract missing {token!r}"


def test_discovery_research_persists_reviewed_plan_before_execution():
    workflow = _workflow_text()
    markers = [
        "orient pass",
        "draft or update the research frame",
        "in-context self-review",
        "persist a reviewed research revision",
        "execute only the reviewed",
    ]
    positions = []
    cursor = 0
    for marker in markers:
        position = workflow.find(marker, cursor)
        assert position >= 0, f"Discovery workflow missing or mis-ordered {marker!r}"
        positions.append(position)
        cursor = position + len(marker)
    assert positions == sorted(positions)


def test_discovery_research_self_review_uses_brainstorming_checks_without_gate_output():
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
        assert token in text, f"Discovery self-review contract missing {token!r}"


def test_discovery_research_orchestrates_bounded_concurrency_as_a_per_wave_limit():
    text = _skill_text()
    for token in [
        "automatic and internal",
        "query-level parallelism",
        "mission-level parallelism",
        "dependency-ordered waves",
        "sequential fallback",
        "2-4 workers",
        "per-wave concurrency limit",
        "not a research-scope limit",
    ]:
        assert token in text, f"Concurrency contract missing {token!r}"


def test_discovery_research_defines_packets_and_single_writer_fan_in():
    text = _skill_text()
    for token in [
        "research packet",
        "transient",
        "uncommitted",
        "atomic claim",
        "source reference",
        "source title",
        "source date",
        "source location",
        "source family",
        "independence key",
        "evidence form",
        "support",
        "limitation",
        "contradictions",
        "unanswered questions",
        "queries attempted",
        "stop reason",
        "underlying origin",
        "claim-to-source",
        "never write project state",
        "never allocate",
        "single writer",
        "one coordinator commit",
    ]:
        assert token in text, f"Research packet contract missing {token!r}"


def test_discovery_research_fan_in_quality_audit_creates_no_gate_output():
    text = _skill_text()
    for token in [
        "decision-relevant",
        "atomic claim",
        "exact source reference",
        "source location",
        "independent source family",
        "authority",
        "recency",
        "directness",
        "bias",
        "supporting and disconfirming",
        "contradictions",
        "favorable source",
        "does not exceed",
        "without losing limitations",
        "unanswered questions",
        "stop reason",
        "stop condition",
        "no artifact, review state, signoff, score, or gate",
    ]:
        assert token in text, f"Fan-in quality audit contract missing {token!r}"


def test_shared_evidence_schema_is_source_neutral_and_backward_compatible():
    schema = (REPO / "src" / "skills" / "_bw-shared" / "ledger-schema.md").read_text().lower()
    for token in [
        "source_type",
        "source_ref",
        "source_title",
        "source_date",
        "source_location",
        "source_family",
        "independence_key",
        "evidence_form",
        "claim",
        "support",
        "limitation",
        "related_assumptions",
    ]:
        assert token in schema, f"shared evidence schema missing {token!r}"
    assert "does not require `evidence_origin`" in schema
    assert "historical entries" in schema and "not rewritten" in schema


def test_discovery_research_is_ai_executed_with_optional_user_context():
    text = _skill_text()
    for token in [
        "ai-executed research",
        "user-provided",
        "optional context",
        "never wait",
        "source reference",
        "evidence form",
        "limitation",
    ]:
        assert token in text, f"Discovery evidence strategy missing {token!r}"

    for forbidden in [
        "research_mode",
        "secondary_only",
        "secondary_first",
        "primary trigger",
        "evidence_origin",
        "primary | secondary",
    ]:
        assert forbidden not in text, f"Discovery research retains an obsolete mode: {forbidden!r}"


def test_discovery_research_does_not_require_a_three_facts_per_4c_quota():
    text = _skill_text()
    for forbidden in ["≥3", ">=3", "at least three sourced facts", "three sourced facts"]:
        assert forbidden not in text, f"Discovery research retains a mechanical fact quota: {forbidden!r}"
    assert "coverage compass" in text


def test_discover_plan_artifact_uses_the_adaptive_sprint_layout():
    text = _plan_text()
    for token in [
        "research frame",
        "living learning agenda",
        "latest research sprint — after execution only",
        "sprint synthesis and plan delta — after execution only",
        "insight ingredients",
        "insight readiness",
        "remaining uncertainty",
        "revision 1 contains a reviewed research frame",
        "omit a section rather than add an empty placeholder",
    ]:
        assert token in text, f"Discover Plan layout missing {token!r}"


def test_discover_plan_sprint_synthesis_captures_belief_change_and_reframe():
    text = _plan_text()
    for token in [
        "learned",
        "contradicted",
        "belief changed",
        "reframed",
        "deepened",
        "dropped",
        "new questions",
        "remaining gaps",
        "redirect",
    ]:
        assert token in text, f"Sprint synthesis contract missing {token!r}"


def test_discover_plan_states_insight_readiness_conditions_without_a_gate():
    text = _plan_text()
    for token in [
        "insight readiness",
        "not a human gate",
        "not a score",
        "not a fact quota",
        "framework quota",
        "permission to sign f/p/e/t",
        "remaining uncertainty",
    ]:
        assert token in text, f"Insight Readiness contract missing {token!r}"


def test_discovery_research_surfaces_insight_ingredients_without_signing_an_insight():
    text = _skill_text()
    for token in [
        "insight ingredients",
        "patterns",
        "tensions",
        "anomalies",
        "challenged accepted beliefs",
        "reframe candidates",
        "strategic relevance",
        "limitations",
        "do not create a final insight",
        "do not sign f/p/e/t",
        "do not compose a directional hypothesis",
        "do not choose a gate exit",
    ]:
        assert token in text, f"Insight ingredient boundary missing {token!r}"
