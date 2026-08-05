from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from skill_helpers import skill_dir, validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]


def _all_text() -> str:
    root = skill_dir(REPO, "bw-initial-assessment")
    return "\n".join(path.read_text() for path in sorted(root.rglob("*.md"))).lower()


def test_bw_initial_assessment_is_well_formed():
    validate_skill(skill_dir(REPO, "bw-initial-assessment"))
    validate_skill_evals(REPO / "evals", "bw-initial-assessment")


def test_assessment_is_independent_and_fresh_context_bounded():
    text = (skill_dir(REPO, "bw-initial-assessment") / "SKILL.md").read_text().lower()
    for token in [
        "independent capability",
        "fresh context",
        "current branch",
        "exact typed charter revision",
        "exact active root-assumption revision snapshot",
        "do not read the original interview",
        "chat transcript",
        "prior assessment body",
    ]:
        assert token in text, f"initial-assessment isolation contract missing {token}"


def test_assessment_uses_public_research_without_promoting_ledger_evidence():
    text = _all_text()
    for token in [
        "3–5",
        "public",
        "primary research",
        "official data",
        "regulatory",
        "authoritative industry",
        "external signal",
        "assessment inference",
        "no evidence wrapper",
        "evidence_level: l1",
        "validation_status: untested",
    ]:
        assert token in text, f"initial-assessment research contract missing {token}"
    assert "model knowledge" in text
    assert "must not be presented as an external fact" in text


def test_assessment_template_is_two_layer_and_has_all_report_sections():
    text = (skill_dir(REPO, "bw-initial-assessment") / "references" / "initial-assessment-template.md").read_text().lower()
    for token in [
        "60-second read",
        "1–2 screens",
        "overall preliminary conclusion",
        "professional perspectives",
        "magic",
        "money",
        "innovation",
        "candidate insights",
        "core conflict / tension",
        "most promising direction",
        "key risks",
        "discover mission",
        "research boundary & sources",
        "charter basis",
        "external signal",
        "assessment inference",
        "implication",
        "what would change this view",
    ]:
        assert token in text, f"initial-assessment template missing {token}"
    assert "2–3" in text
    assert "at most three" in text
    assert "every key judgment must include all five labels" in text
    assert "not established in current sources" in text
    assert "compact trace" in text


def test_assessment_lineage_revision_and_idempotency_are_exact():
    text = _all_text()
    for token in [
        "kind: initial-assessment",
        "derived_from",
        "artifact:art-001@1",
        "assumption:a-001@1",
        "supersedes_ref",
        "same artifact id",
        "matching assessment",
        "reuse",
        "explicit reassessment",
        "append-only",
        "snapshot mismatch",
        "stale",
    ]:
        assert token in text, f"initial-assessment revision contract missing {token}"


def test_assessment_research_failure_and_conflict_fail_safely():
    text = (skill_dir(REPO, "bw-initial-assessment") / "SKILL.md").read_text().lower()
    for token in [
        "1–2 credible sources",
        "sparse",
        "zero credible sources",
        "search tool is unavailable",
        "search fails",
        "do not create",
        "retry reason",
        "sources conflict",
        "discover question",
    ]:
        assert token in text, f"initial-assessment failure contract missing {token}"


def test_assessment_rechecks_snapshot_and_fails_closed_on_repeated_change():
    text = (skill_dir(REPO, "bw-initial-assessment") / "SKILL.md").read_text().lower()
    for token in [
        "re-read the charter head",
        "active root-assumption snapshot",
        "discard",
        "automatically rerun once",
        "changes again",
        "fail closed",
        "concurrent modification",
        "cas",
    ]:
        assert token in text, f"initial-assessment concurrency contract missing {token}"


def test_assessment_uses_deployed_runtime_and_stops_after_integrity():
    text = (skill_dir(REPO, "bw-initial-assessment") / "SKILL.md").read_text().lower()
    assert "pythonpath=_bewater" in text
    assert "do not scan outside the project" in text
    assert "stop after the integrity check passes" in text
    assert "make no further tool call" in text


def test_assessment_audits_report_contract_before_write():
    text = (skill_dir(REPO, "bw-initial-assessment") / "SKILL.md").read_text().lower()
    for token in [
        "pre-write content audit",
        "all eight required headings",
        "five-label trace",
        "2–3 candidate insights",
        "at most three risks",
        "do not acquire the write lock",
    ]:
        assert token in text


def test_assessment_auto_commits_without_confirmation_or_extra_self_review():
    text = (skill_dir(REPO, "bw-initial-assessment") / "SKILL.md").read_text().lower()
    for token in [
        "does not request user confirmation",
        "does not run a brainstorming-style self-review",
        "automatically commit",
        "after the pre-write content audit passes",
    ]:
        assert token in text, f"initial-assessment automatic-commit contract missing {token}"


def test_assessment_has_one_transactional_mutation_path():
    root = skill_dir(REPO, "bw-initial-assessment")
    text = (root / "SKILL.md").read_text().lower()
    plan = (root / "references" / "write-plan.md").read_text().lower()
    for token in [
        "only allowed project-state mutation path",
        "pythonpath=_bewater python3 -m bwkit plan apply",
        "write_new",
        "cas_commit",
        "never use edit",
        "never use shell redirection",
    ]:
        assert token in text + "\n" + plan
    assert "artifact step must precede" in plan


def test_assessment_plan_emitter_only_serializes_ordered_plan(tmp_path: Path):
    root = skill_dir(REPO, "bw-initial-assessment")
    script = root / "scripts" / "emit_write_plan.py"
    artifact = tmp_path / "artifact.md"
    config = tmp_path / "config.yaml"
    artifact.write_text("artifact body\n")
    config.write_text("revision: 3\n")
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--action-id", "initial-assessment:ART-002@1",
            "--owner", "bw-initial-assessment",
            "--artifact-path", "_bewater-output/ART-002-r1-initial-assessment.md",
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
    root = skill_dir(REPO, "bw-initial-assessment")
    script = root / "scripts" / "emit_integrity_payload.py"
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


def test_assessment_enforces_compact_report_budget():
    text = _all_text()
    assert "600–900 words" in text
    assert "no more than 900 words" in text
    assert "aim for 650–700 words" in text
    assert "do not inspect `_bewater/bwkit` source" in text


def test_assessment_does_not_mutate_validation_stage_or_signoff():
    text = _all_text()
    for token in [
        "does not modify the charter",
        "does not change assumption validation",
        "does not change current_stage",
        "does not write a signoff",
        "not a gate",
        "no score",
        "no readiness label",
        "must not decide whether to invest",
    ]:
        assert token in text, f"initial-assessment boundary missing {token}"


def test_assessment_eval_matrix_covers_research_and_revision_paths():
    scenarios = REPO / "evals" / "bw-initial-assessment" / "scenarios"
    names = {path.stem for path in scenarios.glob("*.yaml")}
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
    } <= names
    assert (REPO / "evals" / "bw-initial-assessment" / "live" / "real-search.yaml").is_file()
