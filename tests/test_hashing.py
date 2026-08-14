
from bw import hashing, io, schema


def _write(root, rel, aid, body, deps=None):
    p = root / rel; p.parent.mkdir(parents=True, exist_ok=True)
    meta = schema.ArtifactMeta(artifact_id=aid, kind="insights", stage="define",
        revision=1, document_status="final", validation_status="unvalidated",
        branch_id="BR-001", locked=False, signoffs=[], dual_sided=None,
        derived_from=[], last_validated_against=deps or [], created_at="d", updated_at="d",
        extra={"hash": ""})
    io.write_artifact(p, meta, body); return p


def test_content_hash_is_sha256_hex():
    assert hashing.content_hash("original body") == (
        __import__("hashlib").sha256(b"original body").hexdigest()
    )


def test_hash_stable_and_detects_edit(tmp_project):
    p = _write(tmp_project, "_bewater-output/insights.md", "INS-1", "original body")
    hashing.hash_artifact(p)
    h1 = io.read_artifact(p)[0].hash
    assert h1 and h1 == hashing.content_hash("original body")
    io.write_artifact(p, io.read_artifact(p)[0], "edited body")
    assert io.read_artifact(p)[0].hash != hashing.content_hash("edited body")


def test_refresh_deps_updates_dependents(tmp_project):
    upstream = _write(tmp_project, "_bewater-output/insights.md", "INS-1", "ubody")
    hashing.hash_artifact(upstream)
    dep = _write(tmp_project, "_bewater-output/hyp.md", "HYP-1", "hbody",
                 deps=[{"id":"INS-1","hash":"old"}])
    hashing.refresh_deps(tmp_project, upstream)
    deps2 = io.read_artifact(dep)[0].last_validated_against
    assert deps2[0]["hash"] == io.read_artifact(upstream)[0].hash
    assert hashing.is_stale(tmp_project, dep) is False


def test_is_stale_when_upstream_changed(tmp_project):
    upstream = _write(tmp_project, "_bewater-output/insights.md", "INS-1", "ubody")
    hashing.hash_artifact(upstream)
    dep = _write(tmp_project, "_bewater-output/hyp.md", "HYP-1", "hbody",
                 deps=[{"id":"INS-1","hash":"old"}])
    assert hashing.is_stale(tmp_project, dep) is True


def test_is_stale_no_deps_is_false(tmp_project):
    dep = _write(tmp_project, "_bewater-output/hyp.md", "HYP-1", "hbody", deps=[])
    assert hashing.is_stale(tmp_project, dep) is False


def test_hash_index_ignores_artifact_shaped_knowledge(tmp_project):
    _write(tmp_project, "_bewater-output/knowledge/K-001-question.md", "UPSTREAM", "body")
    dep = _write(
        tmp_project,
        "_bewater-output/artifacts/ART-002-r1-research.md",
        "DEPENDENT",
        "body",
        deps=[{"id": "UPSTREAM", "hash": ""}],
    )

    assert hashing.is_stale(tmp_project, dep) is True
