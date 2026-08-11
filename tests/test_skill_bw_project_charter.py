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


def test_project_charter_uses_explore_then_converge_intake():
    root = skill_dir(REPO, "bw-project-charter")
    text = (root / "SKILL.md").read_text().lower()
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
    ]:
        assert token in text, f"project-charter missing {token}"
    assert text.index("explore") < text.index("converge")


def test_project_charter_explore_is_a_consultative_open_dialogue():
    text = (skill_dir(REPO, "bw-project-charter") / "SKILL.md").read_text().lower()
    explore = text[text.index("**explore"):text.index("**converge")]

    for token in [
        "clear",
        "focused",
        "natural",
        "most worth thinking about",
        "advance shared understanding",
        "next thought",
        "necessary context",
        "question complexity",
        "internal reasoning",
        "expression",
    ]:
        assert token in explore, f"Explore must state the positive consultative principle: {token}"
    assert "one open question" in explore
    assert "agent-interpretation" in explore
    assert "do not offer options" in explore


def test_project_charter_converges_with_context_grounded_recommendations():
    text = (skill_dir(REPO, "bw-project-charter") / "SKILL.md").read_text().lower()
    for token in [
        "recommend",
        "stated context",
        "trade-off",
        "scope",
        "priority",
        "unknown",
        "other",
        "user-selected",
        "user-stated",
        "agent-interpretation",
        "never evidence",
    ]:
        assert token in text, f"project-charter choice/stop contract missing {token}"
    assert "never silently upgraded" in text


def test_project_charter_converge_recommendations_illuminate_tradeoffs():
    text = (skill_dir(REPO, "bw-project-charter") / "SKILL.md").read_text().lower()
    converge = text[text.index("**converge"):text.index("## charter draft")]
    for token in [
        "optimizes",
        "sacrifices",
        "would change this recommendation",
        "credible alternative",
        "uncertain",
        "other",
    ]:
        assert token in converge, f"Converge must help users think through {token}"


def test_project_charter_runs_layered_review_and_intent_calibration_before_persistence():
    root = skill_dir(REPO, "bw-project-charter")
    text = "\n".join(
        (root / name).read_text().lower()
        for name in [
            "SKILL.md",
            "references/charter-template.md",
            "references/self-review-contract.md",
        ]
    )
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
        "disconfirming signal",
        "re-run l0 and l1",
        "persist",
        "3–5",
        "bwkit lock",
        "cas",
        "draft",
        "unvalidated",
    ]:
        assert token in text, f"project-charter self-review contract missing {token}"
    quality = (root / "SKILL.md").read_text().lower()
    assert (
        quality.index("l0 is deterministic")
        < quality.index("l1 is the")
        < quality.index("intent calibration before persistence")
        < quality.index("## persistence")
    )


def test_project_charter_l2_is_final_intent_calibration_then_auto_persistence():
    root = skill_dir(REPO, "bw-project-charter")
    skill = (root / "SKILL.md").read_text().lower()
    review = (root / "references" / "self-review-contract.md").read_text().lower()
    persistence = (root / "references" / "persistence-plan.md").read_text().lower()

    l2 = review[review.index("## l2"):review.index("## l3")]
    for token in ["final unified intent calibration", "not a signoff", "not an approval"]:
        assert token in l2, f"L2 must be calibration rather than {token}"

    final_loop = skill[skill.index("intent calibration before persistence"):skill.index("## persistence")]
    assert "final l0/l1" in final_loop
    assert "persist immediately" in final_loop
    assert "no user confirmation" in final_loop
    assert skill.index("intent calibration before persistence") < skill.index("## persistence")
    assert "user confirmation" not in persistence


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
    artifact.write_text("""---
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
    consumer_value_proposition: {statement: Useful value, evidence_refs: []}
    consumer_target: {statement: A person in context, evidence_refs: []}
  money:
    commercial_value_proposition: {statement: Viable exchange, evidence_refs: []}
    leverageable_assets: {statement: Existing capability, evidence_refs: []}
  tension: {statement: Value and cost balance}
  balance_choice: Learn first
derived_from: []
signoffs: []
stale_reason: null
---

### Original intent

An original intent.

### Structured interpretation

A structured interpretation.

### Money + Magic

A balanced proposition.

### Intent trace

| Claim | Source | Basis |
|---|---|---|
| The user has a goal | user-stated | intake turn 1 |

### Current knowledge state

| Type | Content |
|---|---|
| **Known** | A reported observation. |

### Discover handoff

#### Core exploration question

What must we learn?

#### Beliefs to challenge

A candidate belief.

#### Root assumption research map

| Assumption | 4C | Why it matters | Evidence needed | Disconfirming signal |
|---|---|---|---|---|
| A-001 | Consumer | It matters | Observe use | No repeat use |
| A-002 | Company | It matters | Test capability | Cannot deliver |
| A-003 | Channel | It matters | Observe access | No access route |

#### Starting 4C questions

A starting question.

#### Research boundary

Research these assumptions first.
""")
    ledger.write_text("""schema_version: 1
revision: 3
next_id: 4
assumptions:
  A-001:
    record_revision: 1
    statement: Adoption depends on value
    branch_id: BR-001
    layer: root
    category: consumer
    side: both
    impact: high
    uncertainty: high
    evidence_level: L1
    validation_status: untested
    status: active
    derived_from: [artifact:ART-001@1]
  A-002:
    record_revision: 1
    statement: Delivery depends on capability
    branch_id: BR-001
    layer: root
    category: commercial
    side: both
    impact: high
    uncertainty: high
    evidence_level: L1
    validation_status: untested
    status: active
    derived_from: [artifact:ART-001@1]
  A-003:
    record_revision: 1
    statement: Access depends on channel
    branch_id: BR-001
    layer: root
    category: distribution
    side: both
    impact: high
    uncertainty: high
    evidence_level: L1
    validation_status: untested
    status: active
    derived_from: [artifact:ART-001@1]
""")
    config.write_text("revision: 3\n")
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--action-id", "project-charter:ART-001@1",
            "--owner", "bw-project-charter",
            "--artifact-path", "_bewater-output/ART-001-r1-charter.md",
            "--artifact-file", str(artifact),
            "--ledger-file", str(ledger),
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
        "exploration-before-convergence",
        "recommendation-provenance",
        "intent-mirror-correction",
        "causal-chain-gap",
    } <= names


def test_charter_text_choice_fallback_eval_supplies_its_credible_candidates():
    text = (
        REPO / "evals" / "bw-project-charter" / "scenarios" / "tool-unavailable.yaml"
    ).read_text().lower()
    assert "use the installed bw-project-charter skill" in text
    assert "one city deeply" in text
    assert "three cities shallowly" in text
    assert "uncertain" in text
    assert "other" in text


def test_charter_evals_cover_exploration_convergence_and_review_contracts():
    scenarios = REPO / "evals" / "bw-project-charter" / "scenarios"
    expected = {
        "exploration-before-convergence": ["open", "recommended", "structured"],
        "recommendation-provenance": ["recommendation", "user-selected", "trade-off"],
        "intent-mirror-correction": ["intent calibration", "correction", "persist"],
        "causal-chain-gap": ["channel", "p0", "research question"],
    }
    for name, tokens in expected.items():
        text = (scenarios / f"{name}.yaml").read_text().lower()
        for token in tokens:
            assert token in text, f"{name} must cover {token}"
