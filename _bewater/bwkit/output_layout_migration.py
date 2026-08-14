"""Explicit migration from the legacy flat output layout to shallow directories."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

import yaml

from bw import evidence, io, paths

from . import integrity


class OutputLayoutMigrationError(RuntimeError):
    """Raised when output migration preflight cannot prove a safe move."""


_WORKFLOW_NAME = re.compile(
    r"^(?P<id>(?:ART|EXP)-\d{3})-r(?P<revision>[1-9]\d*)-[a-z0-9][a-z0-9-]*\.md$"
)
_SUPERSEDES = re.compile(r"^artifact:((?:ART|EXP)-\d{3})@([1-9]\d*)$")
_RM_REF = re.compile(r"^RM-\d{3}$")


def _recognized(path: Path) -> re.Match[str] | None:
    return _WORKFLOW_NAME.fullmatch(path.name)


def _legacy_candidates(root: Path) -> list[tuple[Path, Path]]:
    output = paths.output_dir(root)
    candidates: list[tuple[Path, Path]] = []
    if output.is_dir():
        for source in sorted(output.glob("*.md")):
            if _recognized(source):
                candidates.append((source, paths.artifacts_dir(root) / source.name))
    archive = output / "archive"
    if archive.is_dir():
        for source in sorted(archive.rglob("*.md")):
            if _recognized(source):
                relative = source.relative_to(archive)
                candidates.append((source, paths.artifacts_dir(root) / "archive" / relative))
    return candidates


def _all_recognized(root: Path) -> list[Path]:
    return [path for path in paths.iter_workflow_documents(root) if _recognized(path)]


def _read_record(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    match = _recognized(path)
    if match is None:
        raise OutputLayoutMigrationError(f"unrecognized workflow filename: {path}")
    try:
        frontmatter = io.read_frontmatter(path)
    except (OSError, UnicodeError, ValueError) as exc:
        raise OutputLayoutMigrationError(f"invalid workflow document {path}: {exc}") from exc
    artifact_id = match.group("id")
    revision = int(match.group("revision"))
    if frontmatter.get("artifact_id") != artifact_id or frontmatter.get("revision") != revision:
        raise OutputLayoutMigrationError(
            f"filename/frontmatter mismatch: {path} names {artifact_id}@{revision}"
        )
    supersedes = frontmatter.get("supersedes_ref")
    parsed_supersedes = None
    if supersedes is not None:
        ref_match = _SUPERSEDES.fullmatch(str(supersedes))
        parsed_supersedes = (
            {"id": ref_match.group(1), "revision": int(ref_match.group(2))}
            if ref_match is not None
            else supersedes
        )
    return (
        {
            "file": str(path),
            "id": artifact_id,
            "revision": revision,
            "supersedes": parsed_supersedes,
        },
        frontmatter,
    )


def _deduplicated_records(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    frontmatters: list[dict[str, Any]] = []
    by_revision: dict[tuple[str, int], tuple[Path, bytes]] = {}
    for path in _all_recognized(root):
        record, frontmatter = _read_record(path)
        key = (record["id"], record["revision"])
        content = path.read_bytes()
        previous = by_revision.get(key)
        if previous is not None:
            legacy_pairs = _legacy_candidates(root)
            resumable_pair = any(
                {source.resolve(), destination.resolve()} == {previous[0].resolve(), path.resolve()}
                and previous[1] == content
                for source, destination in legacy_pairs
            )
            if resumable_pair:
                continue
            raise OutputLayoutMigrationError(
                f"duplicate revision: {key[0]} r{key[1]} in {previous[0]} and {path}"
            )
        by_revision[key] = (path, content)
        records.append(record)
        frontmatters.append(frontmatter)
    return records, frontmatters


def _evidence_records(value: Any):
    if isinstance(value, dict):
        refs = value.get("evidence_refs")
        if isinstance(refs, list):
            yield str(value.get("branch_id") or ""), refs
        for item in value.values():
            yield from _evidence_records(item)
    elif isinstance(value, list):
        for item in value:
            yield from _evidence_records(item)


def _check_evidence_dependencies(root: Path, frontmatters: list[dict[str, Any]]) -> list[str]:
    unresolved: list[str] = []
    payloads: list[Any] = list(frontmatters)
    ledger_path = root / paths.STATE_DIR / "ledger.yaml"
    if ledger_path.is_file():
        try:
            payloads.append(yaml.safe_load(ledger_path.read_text()) or {})
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            raise OutputLayoutMigrationError(f"invalid ledger state: {exc}") from exc
    for payload in payloads:
        for branch_id, refs in _evidence_records(payload):
            for ref in refs:
                ref_text = str(ref)
                if _RM_REF.fullmatch(ref_text):
                    unresolved.append(f"{ref_text} is a mission ref, not Evidence")
                elif ref_text.startswith("evidence:") and not evidence.ref_resolves(
                    root, ref_text, branch_id=branch_id
                ):
                    unresolved.append(f"unresolved Evidence ref {ref_text}")
    return unresolved


def _dirty_paths(root: Path) -> list[str]:
    try:
        probe = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return []
    if probe.returncode != 0:
        return []
    status = subprocess.run(
        [
            "git", "-C", str(root), "status", "--porcelain=v1", "--untracked-files=all", "--",
            "_bewater", "_bewater-output",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if status.returncode != 0:
        raise OutputLayoutMigrationError(status.stderr.strip() or "failed to inspect git state")
    return [line for line in status.stdout.splitlines() if line.strip()]


def _tracked_candidates(root: Path) -> list[str]:
    probe = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--", "_bewater-output"],
        capture_output=True,
        text=True,
        check=False,
    )
    if probe.returncode != 0:
        return []
    return sorted(
        line for line in probe.stdout.splitlines()
        if _recognized(Path(line)) is not None
    )


def _updated_config(text: str) -> str:
    lines = text.splitlines(keepends=True)
    updated: list[str] = []
    has_knowledge = any(re.match(r"^  knowledge\s*:", line) for line in lines)
    inserted = has_knowledge
    for line in lines:
        if re.match(r"^  evidence\s*:", line):
            continue
        updated.append(line)
        if not inserted and re.match(r"^  (?:artifact|experiment|action)\s*:", line):
            updated.append("  knowledge: 1\n")
            inserted = True
    if not inserted:
        raise OutputLayoutMigrationError("config.yaml has no supported next_ids insertion point")
    return "".join(updated)


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def inspect_output_layout(root: str | Path) -> dict[str, Any]:
    """Validate migration preconditions and return a human-readable inventory."""
    root = Path(root).resolve()
    config_path = root / paths.STATE_DIR / "config.yaml"
    if not config_path.is_file():
        raise OutputLayoutMigrationError(f"missing config.yaml at {config_path}")

    candidates = _legacy_candidates(root)
    dirty = _dirty_paths(root)
    tracked_candidates = _tracked_candidates(root)
    records, frontmatters = _deduplicated_records(root)
    chain = integrity.check_artifacts(records)
    if not chain["ok"]:
        raise OutputLayoutMigrationError("; ".join(chain["errors"]))
    unresolved = _check_evidence_dependencies(root, frontmatters)
    if unresolved:
        raise OutputLayoutMigrationError("; ".join(unresolved))

    conflicts: list[str] = []
    for source, destination in candidates:
        if destination.exists() and destination.read_bytes() != source.read_bytes():
            conflicts.append(f"conflict: {source} -> {destination}")
    if conflicts:
        raise OutputLayoutMigrationError("; ".join(conflicts))

    charter_candidates = [
        _relative(root, Path(record["file"]))
        for record, frontmatter in zip(records, frontmatters)
        if frontmatter.get("kind") == "charter"
    ]
    research_candidates = [
        _relative(root, Path(record["file"]))
        for record, frontmatter in zip(records, frontmatters)
        if frontmatter.get("kind") == "research"
    ]
    try:
        config_data = yaml.safe_load(config_path.read_text()) or {}
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise OutputLayoutMigrationError(f"invalid config state: {exc}") from exc
    project = config_data.get("project") if isinstance(config_data, dict) else {}
    project_name = str(project.get("name") or "") if isinstance(project, dict) else ""
    stranded = sorted(
        _relative(root, path)
        for path in (root / paths.STATE_DIR).glob("config-after-sprint*.yaml")
    )
    inventory = {
        "eligible": [_relative(root, source) for source, _ in candidates],
        "project_name": project_name,
        "charter_candidates": charter_candidates,
        "research_candidates": research_candidates,
        "tracked_candidates": tracked_candidates,
        "heads": chain["heads"],
        "dirty": dirty,
        "evidence_state": "present" if (root / paths.STATE_DIR / "evidence.yaml").is_file() else "missing",
        "stranded_state_files": stranded,
        "applied": False,
    }
    if dirty:
        facts = ", ".join(
            dirty + tracked_candidates + charter_candidates + research_candidates + stranded
        )
        raise OutputLayoutMigrationError(f"relevant state is dirty: {facts}")
    return inventory


def migrate_output_layout(root: str | Path, *, apply: bool = False) -> dict[str, Any]:
    """Check or explicitly apply the shallow output-layout migration."""
    root = Path(root).resolve()
    inventory = inspect_output_layout(root)
    if not apply:
        return inventory

    candidates = _legacy_candidates(root)
    config_path = root / paths.STATE_DIR / "config.yaml"
    old_config = config_path.read_text()
    new_config = _updated_config(old_config)
    moved: list[tuple[Path, Path, bool]] = []
    created_dirs: list[Path] = []
    try:
        for directory in (paths.artifacts_dir(root), paths.sources_dir(root), paths.knowledge_dir(root)):
            if not directory.exists():
                directory.mkdir(parents=True)
                created_dirs.append(directory)
        for source, destination in candidates:
            if not destination.parent.exists():
                destination.parent.mkdir(parents=True)
                created_dirs.append(destination.parent)
            if destination.exists():
                source.unlink()
                moved.append((source, destination, True))
            else:
                source.rename(destination)
                moved.append((source, destination, False))
        if new_config != old_config:
            config_path.write_text(new_config)
    except OSError as exc:
        for source, destination, duplicate in reversed(moved):
            try:
                if duplicate:
                    source.write_bytes(destination.read_bytes())
                elif destination.exists():
                    destination.rename(source)
            except OSError:
                pass
        try:
            config_path.write_text(old_config)
        except OSError:
            pass
        for directory in reversed(created_dirs):
            try:
                directory.rmdir()
            except OSError:
                pass
        raise OutputLayoutMigrationError(f"migration write failed: {exc}") from exc

    inventory["applied"] = bool(candidates or new_config != old_config)
    inventory["moved"] = len(candidates)
    return inventory
