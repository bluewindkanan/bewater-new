from pathlib import Path

from bw import paths


def _touch(root: Path, relative: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(relative)
    return path


def test_workflow_document_iterator_uses_only_supported_locations(tmp_path: Path) -> None:
    expected = {
        _touch(tmp_path, "_bewater-output/artifacts/ART-001-r1-charter.md"),
        _touch(tmp_path, "_bewater-output/artifacts/nested/EXP-001-r1-experiment.md"),
        _touch(tmp_path, "_bewater-output/ART-002-r1-research.md"),
        _touch(tmp_path, "_bewater-output/archive/ART-003-r1-insights.md"),
        _touch(tmp_path, "_bewater-output/artifacts/archive/ART-004-r1-opportunity.md"),
    }
    _touch(tmp_path, "_bewater-output/knowledge/K-001-question.md")
    _touch(tmp_path, "_bewater-output/sources/note.md")
    _touch(tmp_path, "docs/presentations/readout.md")
    _touch(tmp_path, "README.md")

    assert set(paths.iter_workflow_documents(tmp_path)) == expected


def test_legacy_flat_iteration_is_non_recursive(tmp_path: Path) -> None:
    flat = _touch(tmp_path, "_bewater-output/ART-001-r1-charter.md")
    _touch(tmp_path, "_bewater-output/random/ART-002-r1-research.md")

    assert list(paths.iter_workflow_documents(tmp_path)) == [flat]
