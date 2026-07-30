import pytest

from bw import io, paths
from bw.schema import ArtifactKind, ArtifactMeta, ArtifactStatus


def test_find_project_root_locates_bewater_dir(tmp_project):
    sub = tmp_project / "_bewater-output" / "discover"
    sub.mkdir(parents=True)
    assert paths.find_project_root(sub) == tmp_project


def test_find_project_root_raises_when_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        paths.find_project_root(tmp_path)


def test_paths_layout(tmp_project):
    assert paths.ledger_path(tmp_project) == tmp_project / "_bewater" / "ledger.yaml"
    assert paths.records_dir(tmp_project) == tmp_project / "_bewater" / "records"
    assert paths.output_dir(tmp_project) == tmp_project / "_bewater-output"


def test_round_trip_ledger(tmp_project):
    led = io.load_ledger(tmp_project)
    assert led.assumptions == {}
    led.revision = 5
    io.save_ledger(tmp_project, led)
    assert io.load_ledger(tmp_project).revision == 5


def test_round_trip_artifact_frontmatter(tmp_project):
    p = tmp_project / "_bewater-output" / "charter.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    meta, _ = io.read_artifact_dummy()
    io.write_artifact(p, meta, "body text")
    m2, body2 = io.read_artifact(p)
    assert body2 == "body text"
    assert m2.artifact_id == meta.artifact_id


def test_read_artifact_no_frontmatter(tmp_path):
    p = tmp_path / "plain.md"
    p.write_text("just body, no frontmatter")
    meta, body = io.read_artifact(p)
    assert body == "just body, no frontmatter"
    assert meta.artifact_id == ""


def test_read_artifact_missing_closing_fence_raises(tmp_path):
    p = tmp_path / "broken.md"
    p.write_text("---\nartifact_id: ART-1\nkind: charter\nbody that never closes\n")
    with pytest.raises(ValueError):
        io.read_artifact(p)


def read_artifact_dummy() -> tuple[ArtifactMeta, str]:
    """Test-only helper: build a valid ArtifactMeta for round-trip checks."""
    meta = ArtifactMeta(
        artifact_id="A-charter-0001",
        kind=ArtifactKind.charter,
        stage="immersion",
        status=ArtifactStatus.draft,
        hash="abc123",
    )
    return meta, ""


io.read_artifact_dummy = read_artifact_dummy
