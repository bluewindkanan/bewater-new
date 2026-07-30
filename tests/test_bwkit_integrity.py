"""TDD for schema-agnostic bwkit artifact-integrity checks."""
from __future__ import annotations

import io
import json

from bwkit import cli, integrity


def record(file, artifact_id, revision, supersedes=None):
    return {
        "file": file,
        "id": artifact_id,
        "revision": revision,
        "supersedes": supersedes,
    }


def ref(artifact_id, revision):
    return {"id": artifact_id, "revision": revision}


def test_clean_chain_has_latest_revision_as_head():
    result = integrity.check_artifacts([
        record("ART-1-r1.md", "ART-1", 1),
        record("ART-1-r2.md", "ART-1", 2, ref("ART-1", 1)),
        record("ART-1-r3.md", "ART-1", 3, ref("ART-1", 2)),
    ])

    assert result == {"ok": True, "errors": [], "heads": {"ART-1": 3}}


def test_independent_chains_each_report_their_head():
    result = integrity.check_artifacts([
        record("ART-1-r1.md", "ART-1", 1),
        record("ART-2-r1.md", "ART-2", 1),
        record("ART-2-r2.md", "ART-2", 2, ref("ART-2", 1)),
    ])

    assert result == {"ok": True, "errors": [], "heads": {"ART-1": 1, "ART-2": 2}}


def test_duplicate_revision_is_an_error():
    result = integrity.check_artifacts([
        record("ART-1-r1-a.md", "ART-1", 1),
        record("ART-1-r1-b.md", "ART-1", 1),
    ])

    assert result["ok"] is False
    assert any("duplicate" in error for error in result["errors"])


def test_two_unsuperseded_revisions_are_an_error():
    result = integrity.check_artifacts([
        record("ART-1-r1.md", "ART-1", 1),
        record("ART-1-r2.md", "ART-1", 2, ref("ART-1", 1)),
        record("ART-1-r3.md", "ART-1", 3, ref("ART-1", 1)),
    ])

    assert result["ok"] is False
    assert any("head" in error for error in result["errors"])


def test_missing_same_entity_predecessor_is_an_error():
    result = integrity.check_artifacts([
        record("ART-1-r1.md", "ART-1", 1),
        record("ART-1-r5.md", "ART-1", 5, ref("ART-1", 4)),
    ])

    assert result["ok"] is False
    assert any("predecessor" in error for error in result["errors"])


def test_cycle_is_an_error():
    result = integrity.check_artifacts([
        record("ART-1-r1.md", "ART-1", 1, ref("ART-1", 2)),
        record("ART-1-r2.md", "ART-1", 2, ref("ART-1", 1)),
    ])

    assert result["ok"] is False
    assert any("cycle" in error or "head" in error for error in result["errors"])


def test_cross_entity_supersedes_is_ignored():
    result = integrity.check_artifacts([
        record("ART-1-r1.md", "ART-1", 1),
        record("ART-2-r1.md", "ART-2", 1, ref("ART-1", 1)),
    ])

    assert result == {
        "ok": True,
        "errors": [],
        "heads": {"ART-1": 1, "ART-2": 1},
    }


def test_cli_integrity_reports_clean_chain(capsys):
    payload = {"records": [
        record("ART-1-r1.md", "ART-1", 1),
        record("ART-1-r2.md", "ART-1", 2, ref("ART-1", 1)),
    ]}

    assert cli.main(["check", "integrity"], _stdin=io.StringIO(json.dumps(payload))) == 0
    assert json.loads(capsys.readouterr().out) == {
        "ok": True,
        "errors": [],
        "heads": {"ART-1": 2},
    }


def test_cli_integrity_returns_nonzero_for_duplicates(capsys):
    payload = {"records": [
        record("ART-1-r1-a.md", "ART-1", 1),
        record("ART-1-r1-b.md", "ART-1", 1),
    ]}

    assert cli.main(["check", "integrity"], _stdin=io.StringIO(json.dumps(payload))) == 1
    assert json.loads(capsys.readouterr().out)["ok"] is False


def test_non_dict_supersedes_returns_clean_error_without_raising():
    # Caller passed the raw §5.4 type-reference string instead of a parsed dict.
    result = integrity.check_artifacts([
        record("ART-1-r1.md", "ART-1", 1),
        record("ART-1-r2.md", "ART-1", 2, "artifact:ART-1@1"),
    ])

    assert result["ok"] is False
    assert result["errors"]  # some clean error is reported
    assert result["heads"] == {}


def test_corrupted_chain_reports_no_head():
    result = integrity.check_artifacts([
        record("ART-1-r1.md", "ART-1", 1),
        record("ART-1-r5.md", "ART-1", 5, ref("ART-1", 4)),
    ])

    assert result["ok"] is False
    assert result["heads"] == {}


def test_supersedes_missing_revision_emits_no_rNone():
    result = integrity.check_artifacts([
        record("ART-1-r1.md", "ART-1", 1),
        record("ART-1-r2.md", "ART-1", 2, {"id": "ART-1"}),
    ])

    assert result["ok"] is False
    assert result["errors"]
    assert all("rNone" not in error for error in result["errors"])
