"""Initialize and inspect the canonical BeWater project state."""
from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path


class ProjectInitError(RuntimeError):
    """Base error for project initialization failures."""


class InvalidProjectState(ProjectInitError):
    """Raised when initialization would overwrite incomplete or unsupported state."""


_STATE_FILES = {
    "config.yaml": (
        "schema_version",
        "revision",
        "updated_at",
        "updated_by",
        "next_ids",
        "project",
        "decision_authority",
        "active_branch",
        "active_execution_handoff",
        "branches",
    ),
    "ledger.yaml": (
        "schema_version",
        "revision",
        "next_id",
        "updated_at",
        "updated_by",
        "assumptions",
    ),
    "conditions.yaml": (
        "schema_version",
        "revision",
        "next_id",
        "updated_at",
        "updated_by",
        "conditions",
    ),
}


def _has_top_level_key(text: str, key: str) -> bool:
    return re.search(rf"(?m)^{re.escape(key)}\s*:", text) is not None


def _valid_state_file(path: Path, required_keys: tuple[str, ...]) -> bool:
    if not path.is_file():
        return False
    try:
        text = path.read_text()
    except (OSError, UnicodeError):
        return False
    schema = re.search(r"(?m)^schema_version\s*:\s*(\d+)\s*(?:#.*)?$", text)
    revision = re.search(r"(?m)^revision\s*:\s*[1-9]\d*\s*(?:#.*)?$", text)
    return (
        schema is not None
        and int(schema.group(1)) == 1
        and revision is not None
        and all(_has_top_level_key(text, key) for key in required_keys)
    )


def _fresh_bewater_directory(bewater: Path) -> bool:
    if not bewater.exists():
        return True
    if not bewater.is_dir():
        return False
    return all(child.name == "bwkit" and child.is_dir() for child in bewater.iterdir())


def inspect_state(root: str | Path) -> str:
    """Classify a project root as ``fresh``, ``valid``, or ``invalid``."""
    root = Path(root)
    bewater = root / "_bewater"
    output = root / "_bewater-output"
    try:
        if _fresh_bewater_directory(bewater) and not output.exists():
            return "fresh"

        if not output.is_dir() or not (bewater / "records").is_dir():
            return "invalid"
        if not all(
            _valid_state_file(bewater / filename, required_keys)
            for filename, required_keys in _STATE_FILES.items()
        ):
            return "invalid"
        return "valid"
    except OSError as exc:
        raise ProjectInitError(f"failed to inspect BeWater project at {root}: {exc}") from exc


def _timestamp() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _config_text(updated_at: str) -> str:
    return f'''schema_version: 1
revision: 1
updated_at: "{updated_at}"
updated_by: bwkit-init
next_ids:
  branch: 2
  artifact: 1
  experiment: 1
  decision: 1
  baseline: 1
  backtrack: 1
  action: 1
  evidence: 1
project:
  name: ""
  success_criteria: []
decision_authority:
  G1:
    level: product-owner
    accountable_person: null
    accountable_role: null
  G2:
    level: investment-decision
    accountable_person: null
    accountable_role: null
active_branch: BR-001
active_execution_handoff: null
branches:
  BR-001:
    status: active
    current_stage: immersion
    parent_ids: []
    merged_into: null
    gate_due_at:
      G1: null
      G2: null
    inherited_assumption_refs: []
    excluded_assumption_refs: []
    inherited_condition_ids: []
    needs_rebase_refs: []
    active_baselines:
      G1: null
      G2: null
'''


def _ledger_text(updated_at: str) -> str:
    return f'''schema_version: 1
revision: 1
next_id: 1
updated_at: "{updated_at}"
updated_by: bwkit-init
assumptions: {{}}
'''


def _conditions_text(updated_at: str) -> str:
    return f'''schema_version: 1
revision: 1
next_id: 1
updated_at: "{updated_at}"
updated_by: bwkit-init
conditions: {{}}
'''


def _rollback(created_files: list[Path], created_dirs: list[Path]) -> None:
    for path in reversed(created_files):
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass
    for path in reversed(created_dirs):
        try:
            path.rmdir()
        except OSError:
            pass


def initialize_project(root: str | Path) -> str:
    """Create canonical state for a fresh root without overwriting existing state."""
    root = Path(root)
    state = inspect_state(root)
    if state == "valid":
        return "already-initialized"
    if state == "invalid":
        raise InvalidProjectState(f"invalid BeWater project state at {root}")

    bewater = root / "_bewater"
    created_dirs: list[Path] = []
    created_files: list[Path] = []
    try:
        if not root.exists():
            root.mkdir(parents=True)
            created_dirs.append(root)
        if not bewater.exists():
            bewater.mkdir()
            created_dirs.append(bewater)

        records = bewater / "records"
        records.mkdir()
        created_dirs.append(records)
        output = root / "_bewater-output"
        output.mkdir()
        created_dirs.append(output)

        updated_at = _timestamp()
        state_files = (
            (bewater / "config.yaml", _config_text(updated_at)),
            (bewater / "ledger.yaml", _ledger_text(updated_at)),
            (bewater / "conditions.yaml", _conditions_text(updated_at)),
        )
        for path, text in state_files:
            stream = path.open("x")
            created_files.append(path)
            with stream:
                stream.write(text)
    except OSError as exc:
        _rollback(created_files, created_dirs)
        raise ProjectInitError(f"failed to initialize BeWater project at {root}: {exc}") from exc
    return "initialized"
