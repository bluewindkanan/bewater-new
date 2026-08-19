from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def _root() -> Path:
    return skill_dir(REPO, "bw-immersion")


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower()


def _skill_text() -> str:
    return _normalize((_root() / "SKILL.md").read_text())


def _all_text() -> str:
    return _normalize("\n".join(path.read_text() for path in sorted(_root().rglob("*.md"))))


def _valid_charter() -> str:
    return """---
schema_version: 1
artifact_id: ART-001
revision: 1
supersedes_ref: null
kind: charter
stage: immersion
branch_id: BR-001
document_status: draft
validation_status: unvalidated
dual_sided:
  magic:
    consumer_value_proposition: {statement: Useful matching, evidence_refs: []}
    consumer_target: {statement: Freelance chefs, evidence_refs: []}
  money:
    commercial_value_proposition: {statement: Booking fee, evidence_refs: []}
    leverageable_assets: {statement: Kitchen network, evidence_refs: []}
  tension: {statement: Trust versus speed}
  balance_choice: Start in one city
derived_from: []
signoffs: []
stale_reason: null
---
# Charter

### Original intent
Help freelance chefs book compliant kitchens.

### Project definition
**Challenge:** Chefs cannot find compliant space quickly.
**Intent and outcome:** Make booking reliable.
**Scope:** One city.
**Constraints:** Existing kitchen network.
**Success definition:** Completed compliant bookings.

### Money + Magic
Create chef value while sustaining the network.

### Intent trace
| Claim | Provenance | Basis |
|---|---|---|
| Start in one city | user-stated | User selected the first-cycle boundary. |

### Current knowledge state
| Type | Content |
|---|---|
| **Unknown** | Will chefs pay? |
"""


def test_bw_immersion_is_well_formed():
    validate_skill(_root())
    validate_skill_evals(REPO / "evals", "bw-immersion")


def test_immersion_is_a_capability_not_a_router():
    text = _skill_text()
    assert "capability" in text
    assert "never produce artifacts" not in text
    assert "read-only" not in text


def test_immersion_confirms_project_state_without_fabricating_it():
    text = _skill_text()
    for token in [
        "current_stage: immersion",
        "confirm",
        "install.sh",
        "never writes `_bewater/` state by hand",
    ]:
        assert token in text, f"immersion missing state-confirmation token {token!r}"


def test_immersion_runs_the_adaptive_charter_interview():
    text = _skill_text()
    for token in [
        "explore",
        "converge",
        "grounding anchors",
        "trigger",
        "specific person",
        "current behavior",
        "desired change",
        "one question at a time",
        "highest-information-gain",
        "smart-skip",
        "free-form questions only",
        "do not use a structured question",
        "recommendation",
        "earn its place",
        "respect attention",
        "ground before framing",
        "publicly checkable",
        "not an interview question",
        "switch to converge yourself",
        "stalled, not thorough",
        "never as a free-form question",
    ]:
        assert token in text, f"immersion charter interview missing {token}"
    assert text.index("explore") < text.index("converge")


def test_immersion_records_provenance_and_never_upgrades_selection():
    text = _skill_text()
    for token in [
        "user-stated",
        "user-selected",
        "agent-interpretation",
        "unknown",
        "never silently upgraded",
    ]:
        assert token in text, f"immersion provenance contract missing {token}"


def test_immersion_runs_layered_review_and_intent_calibration_before_persistence():
    text = _all_text()
    for token in [
        "l0",
        "deterministic",
        "l1",
        "same-context",
        "intent calibration",
        "high-impact",
        "intent trace",
        "frontmatter",
        "contradictions",
        "scope drift",
        "claim provenance",
        "re-run l0 and l1",
        "persist",
        "bwkit lock",
        "cas",
        "draft",
        "unvalidated",
    ]:
        assert token in text, f"immersion self-review contract missing {token}"
    quality = _skill_text()
    assert (
        quality.index("l0 is deterministic")
        < quality.index("l1 is the")
        < quality.index("intent calibration")
        < quality.index("**persistence.**")
    )


def test_immersion_l2_is_final_intent_calibration_then_auto_persistence():
    root = _root()
    skill = (root / "SKILL.md").read_text().lower()
    review = (root / "references" / "self-review-contract.md").read_text().lower()
    persistence = (root / "references" / "persistence-plan.md").read_text().lower()

    l2 = review[review.index("## l2"):review.index("## l3")]
    for token in ["final unified intent calibration", "not a signoff", "not an approval"]:
        assert token in l2, f"L2 must be calibration rather than {token}"

    assert "persist immediately" in skill
    assert "no user confirmation" in skill
    assert skill.index("intent calibration") < skill.index("**persistence.**")
    assert "user confirmation" not in persistence


def test_immersion_persists_charter_through_one_transactional_plan():
    root = _root()
    text = (root / "SKILL.md").read_text().lower()
    plan = (root / "references" / "persistence-plan.md").read_text().lower()
    for token in [
        "only allowed project-state mutation path",
        "pythonpath=_bewater python3 -m bwkit plan apply",
        "write_new",
        "cas_commit",
        "never use edit",
        "never use shell redirection",
    ]:
        assert token in text + "\n" + plan
    assert "charter step must precede" in plan
    assert "emit_charter_plan.py" in plan
    assert "--owner bw-immersion" in plan
    assert "charter:art-001@1" in plan


def test_immersion_protects_the_repository_project_binding():
    text = _skill_text()
    for token in [
        "one repository",
        "project.name",
        "existing charter",
        "resume or revise",
        "unrelated project",
        "new repository or working directory",
        "write nothing",
    ]:
        assert token in text, f"immersion project-binding contract missing {token!r}"
    for protected in ["charter", "ledger", "conditions", "evidence", "artifact"]:
        assert f"never delete or reset the existing {protected}" in text


def test_first_charter_plan_binds_non_empty_project_name(tmp_path: Path):
    script = _root() / "scripts" / "emit_charter_plan.py"
    artifact = tmp_path / "charter.md"
    config = tmp_path / "config.yaml"
    artifact.write_text(_valid_charter())
    config.write_text("revision: 2\nproject:\n  name: Kitchen Match\n")

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--action-id", "charter:ART-001@1",
            "--owner", "bw-immersion",
            "--artifact-path", "_bewater-output/artifacts/ART-001-r1-charter.md",
            "--artifact-file", str(artifact),
            "--cas-step", "artifact-counter", "_bewater/config.yaml", "1", str(config),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    plan = json.loads(result.stdout)
    assert [step["path"] for step in plan["steps"]] == [
        "_bewater-output/artifacts/ART-001-r1-charter.md",
        "_bewater/config.yaml",
    ]
    assert "name: Kitchen Match" in plan["steps"][1]["new_text"]


def test_first_charter_plan_rejects_blank_project_name_without_emitting_plan(tmp_path: Path):
    script = _root() / "scripts" / "emit_charter_plan.py"
    artifact = tmp_path / "charter.md"
    config = tmp_path / "config.yaml"
    artifact.write_text(_valid_charter())
    config.write_text('revision: 2\nproject:\n  name: ""\n')

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--action-id", "charter:ART-001@1",
            "--owner", "bw-immersion",
            "--artifact-path", "_bewater-output/artifacts/ART-001-r1-charter.md",
            "--artifact-file", str(artifact),
            "--cas-step", "artifact-counter", "_bewater/config.yaml", "1", str(config),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert result.stdout == ""
    assert "project.name" in result.stderr


def test_charter_plan_rejects_legacy_flat_artifact_path(tmp_path: Path):
    script = _root() / "scripts" / "emit_charter_plan.py"
    artifact = tmp_path / "charter.md"
    config = tmp_path / "config.yaml"
    artifact.write_text(_valid_charter())
    config.write_text("revision: 2\nproject:\n  name: Kitchen Match\n")

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--action-id", "charter:ART-001@1",
            "--owner", "bw-immersion",
            "--artifact-path", "_bewater-output/ART-001-r1-charter.md",
            "--artifact-file", str(artifact),
            "--cas-step", "artifact-counter", "_bewater/config.yaml", "1", str(config),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert result.stdout == ""
    assert "_bewater-output/artifacts/" in result.stderr


def test_immersion_delegates_assessment_to_fresh_context():
    text = _skill_text()
    for token in [
        "fresh-context",
        "sub-agent",
        "current branch",
        "exact typed charter revision",
        "do not author the assessment inline",
    ]:
        assert token in text, f"immersion assessment delegation missing {token}"
    assert "interview" in text
    assert "chat transcript" in text


def test_immersion_assessment_is_advisory_and_never_blocks_discover():
    text = _all_text()
    for token in [
        "advisory",
        "charter alone",
        "does not become a hard gate",
        "do not equal a decision to continue",
    ]:
        assert token in text, f"immersion advisory contract missing {token}"


def test_immersion_assessment_research_contract_and_failure_safety():
    text = _skill_text()
    for token in [
        "no fixed count target",
        "external signal",
        "assessment inference",
        "pre-write content audit",
        "direction-level kill signal",
        "concurrent-safe write",
        "integrity",
        "zero credible sources",
        "retry reason",
    ]:
        assert token in text, f"immersion assessment contract missing {token}"


def test_immersion_assessment_lineage_is_exact_charter_only():
    text = _all_text()
    for token in [
        "kind: initial-assessment",
        "derived_from",
        "artifact:art-001@1",
        "supersedes_ref",
        "same branch",
        "exact charter revision only",
        "append-only",
    ]:
        assert token in text, f"immersion assessment lineage missing {token}"


def test_immersion_outputs_a_compact_summary_after_both_artifacts():
    text = _skill_text()
    for token in [
        "summary",
        "challenge",
        "intent and outcome",
        "scope",
        "success signal",
        "key unknowns",
        "overall preliminary conclusion",
        "top risks",
        "what to inspect next",
    ]:
        assert token in text, f"immersion summary missing {token}"
    assert "not a new artifact" in text
    assert "retry reason" in text


def test_immersion_presents_structured_next_step_and_never_decides():
    text = _skill_text()
    for token in [
        "native structured selection",
        "enter discover",
        "revise charter",
        "pause in immersion",
        "retry assessment",
        "continue without assessment",
        "never choose",
        "current_stage",
    ]:
        assert token in text, f"immersion next-step contract missing {token}"


def test_immersion_boundaries_keep_charter_and_assessment_unevidenced():
    text = _all_text()
    for token in [
        "do not create a discover brief",
        "do not design research",
        "not a formal insight",
        "not an input to research",
        "must not be consumed by discover",
        "candidate seed",
        "what to inspect next",
        "no score",
        "no readiness label",
    ]:
        assert token in text, f"immersion boundary missing {token}"


def test_charter_template_has_dual_sided_four_fields():
    text = (_root() / "references" / "charter-template.md").read_text()
    for token in ["dual_sided", "consumer_value_proposition", "consumer_target",
                  "commercial_value_proposition", "leverageable_assets", "artifact_id"]:
        assert token in text, f"charter-template missing {token}"


def test_assessment_template_is_compact_and_has_all_report_sections():
    text = (_root() / "references" / "initial-assessment-template.md").read_text().lower()
    for token in [
        "60-second read",
        "1–2 screens",
        "overall preliminary conclusion",
        "professional perspectives",
        "magic",
        "money",
        "innovation",
        "material risks & unknowns",
        "what to inspect next",
        "research boundary & sources",
        "charter basis",
        "external signal",
        "assessment inference",
        "implication",
        "what would change this view",
    ]:
        assert token in text, f"initial-assessment template missing {token}"
    assert "at most three" in text
    assert "every key judgment must include all five labels" in text
    assert "not established in current sources" in text
    assert "compact trace" in text


def test_assessment_plan_emitter_only_serializes_ordered_plan(tmp_path: Path):
    script = _root() / "scripts" / "emit_assessment_plan.py"
    artifact = tmp_path / "artifact.md"
    config = tmp_path / "config.yaml"
    artifact.write_text("artifact body\n")
    config.write_text("revision: 3\n")
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--action-id", "assessment:ART-002@1",
            "--owner", "bw-immersion",
            "--artifact-path", "_bewater-output/artifacts/ART-002-r1-initial-assessment.md",
            "--artifact-file", str(artifact),
            "--cas-step", "artifact-counter", "_bewater/config.yaml", "2", str(config),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    plan = json.loads(result.stdout)
    assert [step["op"] for step in plan["steps"]] == ["write_new", "cas_commit"]
    assert plan["steps"][1]["expected_revision"] == 2


def test_assessment_integrity_emitter_serializes_records():
    script = _root() / "scripts" / "emit_integrity_payload.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--record", "ART-001", "1", "null",
            "--record", "ART-002", "2", "1",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(result.stdout) == {
        "records": [
            {"id": "ART-001", "revision": 1, "supersedes": None},
            {"id": "ART-002", "revision": 2, "supersedes": 1},
        ]
    }


def test_immersion_eval_matrix_covers_charter_and_assessment_paths():
    scenarios = REPO / "evals" / "bw-immersion" / "scenarios"
    names = {path.stem for path in scenarios.glob("*.yaml")}
    assert {
        "draft",
        "rich-input",
        "ambiguous-input",
        "stuck",
        "scope-tradeoff",
        "fatigue",
        "tool-unavailable",
        "review-revision",
        "exploration-before-convergence",
        "recommendation-provenance",
        "intent-mirror-correction",
        "causal-chain-gap",
        "public-fact-boundary",
    } <= names
    assert {
        "assess",
        "sparse-sources",
        "conflicting-sources",
        "zero-sources",
        "tool-failure",
        "reuse",
        "reassess",
        "charter-chat-conflict",
        "concurrent-change",
        "automatic-commit",
        "unrelated-project",
    } <= names
    assert (REPO / "evals" / "bw-immersion" / "live" / "real-search.yaml").is_file()


def test_immersion_charter_flow_text_fallback_eval_supplies_credible_candidates():
    text = (
        REPO / "evals" / "bw-immersion" / "scenarios" / "tool-unavailable.yaml"
    ).read_text().lower()
    assert "use the installed bw-immersion skill" in text
    assert "one city deeply" in text
    assert "three cities shallowly" in text
    assert "uncertain" in text
    assert "other" in text
