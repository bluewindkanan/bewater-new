"""Content hashing and stale-dependency detection for artifacts.

The hash is of the BODY only: frontmatter fields (updated_at, etc.) are
excluded so re-saving metadata does not churn the hash. This makes stale
detection computable: a dependent's recorded `last_validated_against[].hash`
is compared against the upstream artifact's current `meta.hash`.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from . import io, paths


def content_hash(body: str) -> str:
    return hashlib.sha256(body.encode()).hexdigest()


def hash_artifact(path: Path) -> str:
    meta, body = io.read_artifact(Path(path))
    meta.hash = content_hash(body)
    io.write_artifact(Path(path), meta, body)
    return meta.hash


def _iter_artifact_files(root: Path):
    seen: set[Path] = set()
    primary = paths.output_dir(root)
    roots = [primary, root] if primary != root else [primary]
    for base in roots:
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.md")):
            rp = p.resolve()
            if rp in seen:
                continue
            seen.add(rp)
            yield p


def _load_index(root: Path) -> dict[str, str]:
    """Map artifact_id -> current meta.hash for every artifact under root."""
    index: dict[str, str] = {}
    for p in _iter_artifact_files(root):
        try:
            meta, _ = io.read_artifact(p)
        except (FileNotFoundError, ValueError):
            continue
        if meta.artifact_id:
            index[meta.artifact_id] = meta.hash
    return index


def refresh_deps(root: Path, artifact_path: Path) -> None:
    target_meta, _ = io.read_artifact(Path(artifact_path))
    target_id = target_meta.artifact_id
    new_hash = target_meta.hash
    for p in _iter_artifact_files(root):
        meta, body = io.read_artifact(p)
        changed = False
        for entry in meta.last_validated_against:
            if entry.get("id") == target_id and entry.get("hash") != new_hash:
                entry["hash"] = new_hash
                changed = True
        if changed:
            io.write_artifact(p, meta, body)


def is_stale(root: Path, dep_path: Path) -> bool:
    dep_meta, _ = io.read_artifact(Path(dep_path))
    if not dep_meta.last_validated_against:
        return False
    index = _load_index(root)
    for entry in dep_meta.last_validated_against:
        rid = entry.get("id")
        if rid not in index:
            return True
        if entry.get("hash") != index[rid]:
            return True
    return False
