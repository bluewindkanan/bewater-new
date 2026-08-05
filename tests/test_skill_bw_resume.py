from __future__ import annotations

from pathlib import Path

from skill_helpers import validate_skill, validate_skill_evals

REPO = Path(__file__).resolve().parents[1]
SKILLS = REPO / "src" / "skills"


def _resume_text() -> str:
    root = SKILLS / "bw-resume"
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(root.rglob("*.md"))
    )


def test_bw_resume_is_well_formed():
    validate_skill(SKILLS / "bw-resume")
    validate_skill_evals(REPO / "evals", "bw-resume")


def test_bw_start_is_removed_and_resume_never_bootstraps():
    assert not any(path.is_file() for path in (SKILLS / "bw-start").rglob("*"))
    text = _resume_text().lower()
    for forbidden in ["bootstrap", "create `_bewater/`", "lock acquire", "cas commit"]:
        assert forbidden not in text
    for token in ["read-only", "deployment", "incomplete", "stop"]:
        assert token in text


def test_resume_trigger_and_routing_precedence_are_explicit():
    text = _resume_text().lower()
    for token in [
        "unspecified", "global", "cross-stage", "interrupted", "ambiguous",
        "explicitly", "direct, specific", "one stage", "one branch",
    ]:
        assert token in text, f"bw-resume missing trigger or precedence token: {token}"


def test_resume_scans_state_before_routing_and_never_recovers_itself():
    text = _resume_text().lower()
    for token in [
        "config.yaml", "ledger.yaml", "conditions.yaml", "records/",
        "open conditions", "active-baseline", "pending", "manual-repair",
        "ask the human to choose", "does not execute", "does not write",
    ]:
        assert token in text, f"bw-resume missing reconcile token: {token}"


def test_resume_maps_every_stage_and_pending_owner():
    text = _resume_text()
    expected_routes = {
        "immersion": "bw-immersion",
        "discover": "bw-discover",
        "define": "bw-define",
        "ideate": "bw-ideate",
        "shape": "bw-shape",
        "G1": "bw-strategy-gate",
        "G2": "bw-concept-gate",
        "backtrack": "bw-backtrack",
    }
    for state, skill in expected_routes.items():
        assert state in text and skill in text, f"missing route {state} -> {skill}"

    lower = text.lower()
    assert "route by the action plan owner" not in lower
    for token in ["root `gate`", "`gate: g1`", "`gate: g2`", "backtrack_id", "record type", "conflict"]:
        assert token in lower, f"missing persisted recovery-owner rule: {token}"


def test_resume_covers_branch_blockers_handoff_and_fail_closed_output():
    text = _resume_text().lower()
    for token in [
        "multiple active branches", "blockers", "current branch", "current stage",
        "next human decision", "recommended skill", "active_execution_handoff",
        "handoff-ready", "unknown", "corrupt", "fail closed", "never produce artifacts",
        "never choose a gate exit",
    ]:
        assert token in text, f"bw-resume missing safety/output token: {token}"


def test_active_skill_sources_and_entry_docs_do_not_reference_bw_start():
    paths = [
        REPO / "AGENTS.md",
        REPO / "CLAUDE.md",
        REPO / "README.md",
        REPO / "src" / "bw" / "validate.py",
        *sorted(SKILLS.rglob("*.md")),
    ]
    offenders = [str(path.relative_to(REPO)) for path in paths if "bw-start" in path.read_text()]
    assert offenders == []


def test_pending_g1_eval_uses_canonical_gate_record_fixture():
    records = REPO / "evals" / "fixtures" / "bw-resume" / "pending-g1" / "_bewater" / "records"
    record = records / "D-001-gate.md"
    assert record.is_file()
    text = record.read_text()
    for token in [
        "schema_version: 1", "revision: 1", "decision_id: D-001", "attempt: 1",
        "gate: G1", "subject_refs:", "decision_maker:", "trigger:",
        "input_revisions:", "checklist_results:", "condition_ids:",
        "expected_revisions:", "target_stage: ideate", "action_status: pending",
        "supersedes_ref:", "decided_at:", "validity: active", "change_history:",
    ]:
        assert token in text, f"canonical pending G1 fixture missing {token}"
