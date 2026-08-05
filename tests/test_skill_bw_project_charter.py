from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def test_bw_project_charter_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-project-charter"))
    validate_skill_evals(REPO / "evals", "bw-project-charter")


def test_charter_template_has_dual_sided_four_fields():
    text = (skill_dir(REPO, "bw-project-charter") / "references" / "charter-template.md").read_text()
    for token in ["dual_sided", "consumer_value_proposition", "consumer_target",
                  "commercial_value_proposition", "leverageable_assets", "artifact_id"]:
        assert token in text, f"charter-template missing {token}"


def test_project_charter_uses_adaptive_low_cost_intake():
    root = skill_dir(REPO, "bw-project-charter")
    text = (root / "SKILL.md").read_text().lower()
    for token in [
        "one question at a time",
        "highest information gain",
        "smart-skip",
        "free-form input",
        "host-native structured choice",
        "credible candidates",
        "do not invent facts",
        "uncertain",
        "other",
        "text-choice fallback",
        "repeats the credible candidates plus uncertain and other",
        "never render a fallback with only candidates",
        "fixed four-option fallback",
        "no substitute for uncertain and other",
        "do not choose for the user",
        "why now",
        "current behavior",
        "magic",
        "money",
        "known",
        "believed",
        "unknown",
        "tension",
    ]:
        assert token in text, f"project-charter missing {token}"
    assert "choice-based intake" not in text
    assert "four contextual questions" not in text
    assert "at most four" not in text
    assert "no fixed question limit" in text
    assert "do not offer answer choices" not in text


def test_project_charter_selects_the_input_mode_without_inducing_user_intent():
    text = (skill_dir(REPO, "bw-project-charter") / "SKILL.md").read_text().lower()
    for token in [
        "open or high-dimensional",
        "would induce",
        "scope",
        "priority",
        "trade-off",
        "user is stuck",
        "none are accurate",
        "explicitly does not know",
        "discover should investigate",
        "fatigue",
        "unknown",
        "l1 only after",
    ]:
        assert token in text, f"project-charter choice/stop contract missing {token}"
    assert "do not offer answer choices" not in text


def test_project_charter_self_reviews_revises_and_persists_without_confirmation():
    text = (skill_dir(REPO, "bw-project-charter") / "SKILL.md").read_text().lower()
    for token in [
        "self-review",
        "missing fields",
        "internal contradictions",
        "scope drift",
        "material ambiguity",
        "user intent",
        "fabricated facts",
        "automatically revise",
        "return to the interview",
        "without user confirmation",
        "3–5",
        "bwkit lock",
        "cas",
        "draft",
        "unvalidated",
    ]:
        assert token in text, f"project-charter self-review contract missing {token}"
    assert "core-understanding checkpoint" not in text
    assert "complete charter draft checkpoint" not in text
    assert "accurately expresses your current intent" not in text


def test_project_charter_persists_through_one_transactional_plan():
    root = skill_dir(REPO, "bw-project-charter")
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
    assert "explicitly confirmed" not in plan
    assert "self-review passes" in plan


def test_charter_plan_emitter_orders_artifact_before_cas_steps(tmp_path: Path):
    root = skill_dir(REPO, "bw-project-charter")
    script = root / "scripts" / "emit_write_plan.py"
    artifact = tmp_path / "charter.md"
    ledger = tmp_path / "ledger.yaml"
    config = tmp_path / "config.yaml"
    artifact.write_text("charter body\n")
    ledger.write_text("revision: 3\n")
    config.write_text("revision: 3\n")
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--action-id", "project-charter:ART-001@1",
            "--owner", "bw-project-charter",
            "--artifact-path", "_bewater-output/ART-001-r1-charter.md",
            "--artifact-file", str(artifact),
            "--cas-step", "ledger", "_bewater/ledger.yaml", "2", str(ledger),
            "--cas-step", "artifact-counter", "_bewater/config.yaml", "2", str(config),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    plan = json.loads(result.stdout)
    assert [step["op"] for step in plan["steps"]] == ["write_new", "cas_commit", "cas_commit"]


def test_project_charter_hands_assessment_to_independent_fresh_context_capability():
    root = skill_dir(REPO, "bw-project-charter")
    text = (root / "SKILL.md").read_text().lower()
    for token in [
        "bw-initial-assessment",
        "fresh-context",
        "current branch",
        "exact typed charter revision",
        "exact active root-assumption revision snapshot",
        "must not author the assessment inline",
        "stop and route",
    ]:
        assert token in text, f"project-charter assessment handoff missing {token}"
    assert not (root / "references" / "initial-assessment-template.md").exists()


def test_charter_preserves_layers_and_hands_off_to_discover():
    root = skill_dir(REPO, "bw-project-charter")
    text = (root / "references" / "charter-template.md").read_text().lower()
    for token in [
        "original intent",
        "structured interpretation",
        "known",
        "believed",
        "unknown",
        "tensions",
        "discover handoff",
        "core exploration question",
        "4c",
        "research boundary",
    ]:
        assert token in text, f"charter-template missing {token}"
    assert "discover brief" not in text
    assert "initial assessment" not in text


def test_root_assumptions_reference_layer_root():
    text = (skill_dir(REPO, "bw-project-charter") / "references" / "root-assumptions.md").read_text()
    lowered = text.lower()
    for token in [
        "3–5",
        "layer: root",
        "record_revision",
        "falsifiable",
        "disconfirming signal",
        "evidence_level: l1",
        "validation_status: untested",
    ]:
        assert token in lowered, f"root-assumptions missing {token}"


def test_charter_behavior_eval_matrix_covers_adaptive_paths():
    scenarios = REPO / "evals" / "bw-project-charter" / "scenarios"
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
    } <= names


def test_charter_text_choice_fallback_eval_supplies_its_credible_candidates():
    text = (
        REPO / "evals" / "bw-project-charter" / "scenarios" / "tool-unavailable.yaml"
    ).read_text().lower()
    assert "use the installed bw-project-charter skill" in text
    assert "one city deeply" in text
    assert "three cities shallowly" in text
