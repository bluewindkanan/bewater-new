from __future__ import annotations

import re
from pathlib import Path

import pytest

from bwkit import cli
from bwkit import init as project_init
from bwkit.init import InvalidProjectState, initialize_project, inspect_state

BUSINESS_PATHS = (
    "_bewater/config.yaml",
    "_bewater/ledger.yaml",
    "_bewater/conditions.yaml",
    "_bewater/records",
    "_bewater-output",
)


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def test_check_fresh_is_read_only(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = tmp_path / "new-project"

    assert inspect_state(root) == "fresh"
    assert cli.main(["init", str(root), "--check"]) == 0

    captured = capsys.readouterr()
    assert "fresh" in captured.out.lower()
    assert captured.err == ""
    assert not root.exists()


def test_fresh_init_writes_complete_v5_scaffold(tmp_path: Path) -> None:
    root = tmp_path / "new-project"

    assert initialize_project(root) == "initialized"

    assert all((root / relative).exists() for relative in BUSINESS_PATHS)
    assert (root / "_bewater/records").is_dir()
    assert (root / "_bewater-output").is_dir()

    config = (root / "_bewater/config.yaml").read_text()
    for field, value in {
        "branch": 2,
        "artifact": 1,
        "experiment": 1,
        "decision": 1,
        "baseline": 1,
        "backtrack": 1,
        "action": 1,
        "evidence": 1,
    }.items():
        assert re.search(rf"(?m)^  {field}: {value}$", config)
    for fragment in (
        'name: ""',
        "success_criteria: []",
        "decision_authority:",
        "G1:",
        "G2:",
        "accountable_person: null",
        "accountable_role: null",
        "active_branch: BR-001",
        "BR-001:",
        "status: active",
        "current_stage: immersion",
        "parent_ids: []",
        "merged_into: null",
        "inherited_assumption_refs: []",
        "excluded_assumption_refs: []",
        "inherited_condition_ids: []",
        "needs_rebase_refs: []",
        "active_baselines:",
    ):
        assert fragment in config

    ledger = (root / "_bewater/ledger.yaml").read_text()
    conditions = (root / "_bewater/conditions.yaml").read_text()
    for text, empty_collection in ((ledger, "assumptions: {}"), (conditions, "conditions: {}")):
        assert text.startswith("schema_version: 1\nrevision: 1\n")
        assert "next_id: 1" in text
        assert "updated_by: bwkit-init" in text
        assert empty_collection in text
        assert re.search(r'(?m)^updated_at: "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z"$', text)

    assert "updated_by: bwkit-init" in config
    assert inspect_state(root) == "valid"


def test_valid_init_is_noop_and_preserves_bytes(tmp_path: Path) -> None:
    root = tmp_path / "project"
    initialize_project(root)
    before = _snapshot(root)

    assert initialize_project(root) == "already-initialized"

    assert _snapshot(root) == before


def test_partial_state_is_invalid_and_unchanged(tmp_path: Path) -> None:
    root = tmp_path / "project"
    ledger = root / "_bewater/ledger.yaml"
    ledger.parent.mkdir(parents=True)
    ledger.write_text("do not overwrite\n")
    before = _snapshot(root)

    assert inspect_state(root) == "invalid"
    with pytest.raises(InvalidProjectState):
        initialize_project(root)

    assert _snapshot(root) == before
    assert not (root / "_bewater/config.yaml").exists()


def test_higher_schema_is_invalid(tmp_path: Path) -> None:
    root = tmp_path / "project"
    initialize_project(root)
    config = root / "_bewater/config.yaml"
    config.write_text(config.read_text().replace("schema_version: 1", "schema_version: 2", 1))

    assert inspect_state(root) == "invalid"
    with pytest.raises(InvalidProjectState, match="invalid"):
        initialize_project(root)


@pytest.mark.parametrize(
    "relative",
    [
        "_bewater/config.yaml",
        "_bewater/ledger.yaml",
        "_bewater/conditions.yaml",
    ],
)
@pytest.mark.parametrize("revision", ["0", "-1", "nope"])
def test_non_positive_or_non_numeric_revision_is_invalid(
    tmp_path: Path, relative: str, revision: str
) -> None:
    root = tmp_path / "project"
    initialize_project(root)
    path = root / relative
    path.write_text(path.read_text().replace("revision: 1", f"revision: {revision}", 1))

    assert inspect_state(root) == "invalid"


def test_deployed_bwkit_directory_does_not_prevent_fresh_init(tmp_path: Path) -> None:
    root = tmp_path / "project"
    deployed = root / "_bewater/bwkit"
    deployed.mkdir(parents=True)
    marker = deployed / "installed.txt"
    marker.write_text("keep me\n")

    assert inspect_state(root) == "fresh"
    assert initialize_project(root) == "initialized"

    assert marker.read_text() == "keep me\n"
    assert inspect_state(root) == "valid"


def test_valid_state_allows_unknown_fields_and_extra_files(tmp_path: Path) -> None:
    root = tmp_path / "project"
    initialize_project(root)
    config = root / "_bewater/config.yaml"
    config.write_text(config.read_text() + "future_field: true\n")
    (root / "_bewater/future.txt").write_text("future\n")

    assert inspect_state(root) == "valid"


@pytest.mark.parametrize("fail_at", [2, 3])
def test_failed_init_rolls_back_created_business_paths_and_preserves_bwkit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, fail_at: int
) -> None:
    root = tmp_path / "project"
    keep = root / "_bewater/bwkit/keep"
    keep.parent.mkdir(parents=True)
    keep.write_text("keep\n")
    original_open = Path.open
    opens = 0

    class PartialWriteFailure:
        def __init__(self, stream) -> None:
            self.stream = stream

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            self.stream.close()

        def write(self, text: str) -> int:
            self.stream.write(text[:10])
            self.stream.flush()
            raise OSError("disk full")

    def fail_midway(path: Path, mode: str = "r", *args, **kwargs):
        nonlocal opens
        stream = original_open(path, mode, *args, **kwargs)
        if mode == "x" and path.name in {"config.yaml", "ledger.yaml", "conditions.yaml"}:
            opens += 1
            if opens == fail_at:
                return PartialWriteFailure(stream)
        return stream

    monkeypatch.setattr(Path, "open", fail_midway)

    with pytest.raises(RuntimeError, match="failed to initialize") as exc:
        initialize_project(root)

    assert isinstance(exc.value.__cause__, OSError)
    assert keep.read_text() == "keep\n"
    assert inspect_state(root) == "fresh"
    assert not any((root / relative).exists() for relative in BUSINESS_PATHS)


def test_cli_init_reports_oserror_without_traceback(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail(_root: Path) -> str:
        raise OSError("disk unavailable")

    monkeypatch.setattr(project_init, "initialize_project", fail)

    assert cli.main(["init", str(tmp_path / "project")]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "disk unavailable" in captured.err
    assert "traceback" not in captured.err.lower()


def test_cli_init_reports_wrapped_write_failure_and_rolls_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "project"
    original_open = Path.open

    def fail_open(path: Path, mode: str = "r", *args, **kwargs):
        if mode == "x":
            raise OSError("write failed")
        return original_open(path, mode, *args, **kwargs)

    monkeypatch.setattr(Path, "open", fail_open)

    assert cli.main(["init", str(root)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "failed to initialize" in captured.err
    assert "traceback" not in captured.err.lower()
    assert not any((root / relative).exists() for relative in BUSINESS_PATHS)


def test_concurrent_config_creation_is_never_overwritten_or_rolled_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "project"
    config = root / "_bewater/config.yaml"
    original_mkdir = Path.mkdir

    def race_after_inspection(path: Path, *args, **kwargs) -> None:
        original_mkdir(path, *args, **kwargs)
        if path == root / "_bewater-output":
            config.write_text("user data\n")

    monkeypatch.setattr(Path, "mkdir", race_after_inspection)

    with pytest.raises(project_init.ProjectInitError, match="failed to initialize"):
        initialize_project(root)

    assert config.read_text() == "user data\n"


@pytest.mark.parametrize("check", [False, True])
def test_cli_init_inspection_error_is_controlled(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    check: bool,
) -> None:
    root = tmp_path / "project"
    bewater = root / "_bewater"
    bewater.mkdir(parents=True)
    original_iterdir = Path.iterdir

    def deny_access(path: Path):
        if path == bewater:
            raise PermissionError("permission denied")
        return original_iterdir(path)

    monkeypatch.setattr(Path, "iterdir", deny_access)
    argv = ["init", str(root)]
    if check:
        argv.append("--check")

    assert cli.main(argv) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "permission denied" in captured.err
    assert "traceback" not in captured.err.lower()


@pytest.mark.parametrize(
    ("relative", "anchor"),
    [
        ("_bewater/config.yaml", "next_ids:"),
        ("_bewater/config.yaml", "active_branch:"),
        ("_bewater/config.yaml", "branches:"),
        ("_bewater/ledger.yaml", "next_id:"),
        ("_bewater/ledger.yaml", "assumptions:"),
        ("_bewater/conditions.yaml", "next_id:"),
        ("_bewater/conditions.yaml", "conditions:"),
    ],
)
def test_missing_required_top_level_anchor_is_invalid(
    tmp_path: Path, relative: str, anchor: str
) -> None:
    root = tmp_path / "project"
    initialize_project(root)
    path = root / relative
    path.write_text(path.read_text().replace(anchor, f"removed_{anchor}", 1))

    assert inspect_state(root) == "invalid"


def test_cli_help_and_init_exit_codes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exc:
        cli.main(["init", "--help"])
    assert exc.value.code == 0
    assert "--check" in capsys.readouterr().out

    fresh = tmp_path / "fresh"
    assert cli.main(["init", str(fresh)]) == 0
    assert "initialized" in capsys.readouterr().out.lower()
    assert cli.main(["init", str(fresh)]) == 0
    assert "already initialized" in capsys.readouterr().out.lower()
    assert cli.main(["init", str(fresh), "--check"]) == 0
    assert "valid" in capsys.readouterr().out.lower()

    partial = tmp_path / "partial"
    (partial / "_bewater").mkdir(parents=True)
    (partial / "_bewater/config.yaml").write_text("partial\n")
    assert cli.main(["init", str(partial), "--check"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "invalid" in captured.err.lower()
