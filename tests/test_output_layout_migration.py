from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml

from bw import io, schema
from bwkit import output_layout_migration as migration
from bwkit.init import initialize_project


def _artifact(root: Path, relative: str, artifact_id: str, revision: int = 1,
              supersedes_ref: str | None = None, evidence_refs: list[str] | None = None) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if artifact_id.startswith("EXP-"):
        frontmatter = {
            "artifact_id": artifact_id,
            "kind": "experiment",
            "stage": "shape",
            "revision": revision,
            "document_status": "final",
            "validation_status": "unvalidated",
            "branch_id": "BR-001",
            "supersedes_ref": supersedes_ref,
            "evidence_refs": evidence_refs or [],
        }
        path.write_text(f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---\nbody {artifact_id} r{revision}")
        return path
    meta = schema.ArtifactMeta(
        artifact_id=artifact_id,
        kind="research",
        stage="discover",
        revision=revision,
        document_status="final",
        validation_status="unvalidated",
        branch_id="BR-001",
        extra={"supersedes_ref": supersedes_ref, "evidence_refs": evidence_refs or []},
    )
    io.write_artifact(path, meta, f"body {artifact_id} r{revision}")
    return path


def _legacy_project(tmp_path: Path) -> Path:
    initialize_project(tmp_path)
    config = tmp_path / "_bewater/config.yaml"
    config.write_text(config.read_text().replace("  knowledge: 1\n", "  evidence: 9\n"))
    return tmp_path


def test_check_inventory_is_read_only_and_apply_moves_only_canonical_documents(tmp_path: Path) -> None:
    root = _legacy_project(tmp_path)
    artifact = _artifact(root, "_bewater-output/ART-001-r1-research.md", "ART-001")
    experiment = _artifact(root, "_bewater-output/EXP-001-r1-experiment.md", "EXP-001")
    archived = _artifact(root, "_bewater-output/archive/ART-002-r1-research.md", "ART-002")
    arbitrary = root / "_bewater-output/notes.md"
    arbitrary.write_text("keep me")
    before = {path: path.read_bytes() for path in (artifact, experiment, archived, arbitrary)}

    inventory = migration.migrate_output_layout(root, apply=False)

    assert inventory["eligible"] == [
        "_bewater-output/ART-001-r1-research.md",
        "_bewater-output/EXP-001-r1-experiment.md",
        "_bewater-output/archive/ART-002-r1-research.md",
    ]
    assert all(path.read_bytes() == content for path, content in before.items())

    result = migration.migrate_output_layout(root, apply=True)

    assert result["applied"] is True
    assert (root / "_bewater-output/artifacts/ART-001-r1-research.md").read_bytes() == before[artifact]
    assert (root / "_bewater-output/artifacts/EXP-001-r1-experiment.md").read_bytes() == before[experiment]
    assert (root / "_bewater-output/artifacts/archive/ART-002-r1-research.md").read_bytes() == before[archived]
    assert arbitrary.read_text() == "keep me"
    config = (root / "_bewater/config.yaml").read_text()
    assert "  knowledge: 1\n" in config
    assert "  evidence:" not in config


def test_apply_is_idempotent_and_preserves_state_bytes(tmp_path: Path) -> None:
    root = _legacy_project(tmp_path)
    _artifact(root, "_bewater-output/ART-001-r1-research.md", "ART-001")
    evidence = root / "_bewater/evidence.yaml"
    evidence.write_bytes(
        b"schema_version: 1\nrevision: 1\nbranch_id: BR-001\n"
        b"next_evidence_id: 1\nevidence: []\n"
    )
    protected = [
        root / "_bewater/ledger.yaml",
        evidence,
        root / "_bewater/records",
    ]
    record = protected[2] / "record.yaml"
    record.write_bytes(b"record bytes\n")
    before = {
        protected[0]: protected[0].read_bytes(),
        protected[1]: protected[1].read_bytes(),
        record: record.read_bytes(),
    }

    migration.migrate_output_layout(root, apply=True)
    second = migration.migrate_output_layout(root, apply=True)

    assert second["applied"] is False
    assert all(path.read_bytes() == content for path, content in before.items())


def test_destination_conflict_fails_without_writes(tmp_path: Path) -> None:
    root = _legacy_project(tmp_path)
    source = _artifact(root, "_bewater-output/ART-001-r1-research.md", "ART-001")
    destination = root / "_bewater-output/artifacts/ART-001-r1-research.md"
    destination.write_bytes(b"different")
    config_before = (root / "_bewater/config.yaml").read_bytes()

    with pytest.raises(migration.OutputLayoutMigrationError, match="conflict"):
        migration.migrate_output_layout(root, apply=True)

    assert source.exists() and destination.read_bytes() == b"different"
    assert (root / "_bewater/config.yaml").read_bytes() == config_before


def test_duplicate_revision_and_multiple_heads_fail_preflight(tmp_path: Path) -> None:
    duplicate = _legacy_project(tmp_path / "duplicate")
    _artifact(duplicate, "_bewater-output/ART-001-r1-a.md", "ART-001")
    _artifact(duplicate, "_bewater-output/archive/ART-001-r1-b.md", "ART-001")
    with pytest.raises(migration.OutputLayoutMigrationError, match="duplicate revision"):
        migration.migrate_output_layout(duplicate, apply=False)

    heads = _legacy_project(tmp_path / "heads")
    _artifact(heads, "_bewater-output/ART-001-r1-a.md", "ART-001", 1)
    _artifact(heads, "_bewater-output/ART-001-r2-b.md", "ART-001", 2)
    with pytest.raises(migration.OutputLayoutMigrationError, match="head"):
        migration.migrate_output_layout(heads, apply=False)


def test_missing_evidence_dependency_fails_preflight(tmp_path: Path) -> None:
    root = _legacy_project(tmp_path)
    _artifact(
        root,
        "_bewater-output/ART-001-r1-research.md",
        "ART-001",
        evidence_refs=["evidence:E-001@1"],
    )

    with pytest.raises(migration.OutputLayoutMigrationError, match="Evidence"):
        migration.migrate_output_layout(root, apply=False)


def test_relevant_git_dirty_state_fails_and_reports_candidates(tmp_path: Path) -> None:
    root = _legacy_project(tmp_path)
    charter = _artifact(root, "_bewater-output/ART-001-r1-charter.md", "ART-001")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "_bewater", "_bewater-output"], cwd=root, check=True)
    subprocess.run(
        ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "base"],
        cwd=root,
        check=True,
    )
    charter.write_text(charter.read_text() + "\nworking replacement")

    with pytest.raises(migration.OutputLayoutMigrationError, match="dirty") as exc:
        migration.migrate_output_layout(root, apply=False)

    assert "ART-001-r1-charter.md" in str(exc.value)
