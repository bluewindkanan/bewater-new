from __future__ import annotations

import yaml

from bw import io, schema, validate


def _supported_assumption() -> schema.Assumption:
    return schema.Assumption(
        id="A-001",
        statement="Observed behavior supports the claim.",
        layer="root",
        category="consumer",
        impact="low",
        uncertainty="low",
        evidence_level="L4",
        validation_status="supported",
        status="active",
        evidence_refs=["evidence:E-001@1"],
        branch_id="BR-001",
    )


def _save_assumption(root) -> None:
    ledger = io.load_ledger(root)
    assumption = _supported_assumption()
    ledger.assumptions[assumption.id] = assumption
    io.save_ledger(root, ledger)


def _save_evidence(root, *, revision=1, validity="active", branch_id="BR-001") -> None:
    (root / "_bewater" / "evidence.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "revision": 1,
                "branch_id": branch_id,
                "next_evidence_id": 2,
                "evidence": [
                    {
                        "id": "E-001",
                        "record_revision": revision,
                        "validity": validity,
                    }
                ],
            },
            sort_keys=False,
        )
    )


def test_supported_assumption_requires_resolvable_machine_evidence(tmp_project):
    _save_assumption(tmp_project)
    knowledge_dir = tmp_project / "_bewater-output" / "knowledge"
    knowledge_dir.mkdir()
    (knowledge_dir / "K-001-claim.md").write_text("# Supporting workpaper\n")

    issues = validate.validate_all(tmp_project)

    assert any(issue.kind == "evidence-ref" and issue.scope == "A-001" for issue in issues)


def test_current_active_evidence_satisfies_supported_assumption(tmp_project):
    _save_assumption(tmp_project)
    _save_evidence(tmp_project)

    issues = validate.validate_all(tmp_project)

    assert not any(issue.kind == "evidence-ref" for issue in issues)


def test_stale_invalidated_or_cross_branch_evidence_fails_closed(tmp_project):
    _save_assumption(tmp_project)
    for revision, validity, branch_id in [
        (2, "active", "BR-001"),
        (1, "invalidated", "BR-001"),
        (1, "active", "BR-002"),
    ]:
        _save_evidence(
            tmp_project,
            revision=revision,
            validity=validity,
            branch_id=branch_id,
        )
        issues = validate.validate_all(tmp_project)
        assert any(issue.kind == "evidence-ref" for issue in issues)
