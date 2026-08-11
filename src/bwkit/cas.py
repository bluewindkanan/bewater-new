"""bwkit/cas — single-writer lock + text-level revision CAS (stdlib-only).

Schema-agnostic and YAML-agnostic. See design spec §12.5. This module never
imports yaml and never imports from the legacy bw package.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path

LOCKNAME = ".bw-lock"
BACKUP_PREFIX = ".backup-"


class LockError(Exception):
    """Lock contention or owner mismatch."""


class CasConflict(Exception):
    """Current revision != expected_revision (no write performed)."""


class BadRevisionBump(Exception):
    """new_text top-level revision != expected_revision + 1."""


def content_hash(body: str) -> str:
    return hashlib.sha256(body.encode()).hexdigest()


def lock_path(root) -> Path:
    return Path(root) / "_bewater" / LOCKNAME


def acquire_lock(root, owner, ttl_seconds: int = 3600) -> dict:
    root = Path(root)
    state_dir = root / "_bewater"
    if not state_dir.is_dir():
        raise LockError("no _bewater/ directory; run 'bwkit init' first")
    path = lock_path(root)
    info = {"owner": owner, "pid": os.getpid(), "acquired_at": time.time()}
    try:
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError:
        holder = _read_lock(path)
        if holder is not None and not _is_stale(holder, ttl_seconds):
            raise LockError(f"locked by {holder.get('owner')}")
        tmp = path.with_name(f"{LOCKNAME}.tmp-{os.getpid()}")
        tmp.write_text(json.dumps(info))
        os.replace(tmp, path)  # atomic preempt of stale lock
        holder = _read_lock(path)
        if holder is None or holder.get("owner") != owner or holder.get("pid") != os.getpid():
            raise LockError("lost race after preempt")
        return info
    try:
        os.write(fd, json.dumps(info).encode())
    finally:
        os.close(fd)
    return info


def release_lock(root, owner) -> None:
    path = lock_path(Path(root))
    holder = _read_lock(path)
    if holder is None:
        return  # unlocked: no-op
    if holder.get("owner") != owner:
        raise LockError(f"lock held by {holder.get('owner')}, not {owner}")
    path.unlink()


def lock_status(root):
    return _read_lock(lock_path(Path(root)))


def _read_lock(path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, ValueError):
        return None


def _is_stale(holder: dict, ttl_seconds: int) -> bool:
    pid = holder.get("pid")
    if not isinstance(pid, int):
        return True
    try:
        os.kill(pid, 0)
        running = True
    except ProcessLookupError:
        running = False
    except PermissionError:
        running = True
    if running:
        return (time.time() - holder.get("acquired_at", 0.0)) > ttl_seconds
    return True


_REVISION_RE = re.compile(r"(?m)^revision:\s*(\d+)\s*$")


def read_revision(path) -> int:
    text = Path(path).read_text()  # FileNotFoundError if absent
    m = _REVISION_RE.search(text)
    if not m:
        raise KeyError(f"no top-level 'revision:' field in {path}")
    return int(m.group(1))


def commit(path, new_text: str, expected_revision: int, *, keep_backups: int = 5) -> dict:
    path = Path(path)
    current = read_revision(path)  # FileNotFoundError propagates if missing
    if current != expected_revision:
        raise CasConflict(f"current revision {current} != expected {expected_revision}")
    m = _REVISION_RE.search(new_text)
    got = int(m.group(1)) if m else None
    if got != expected_revision + 1:
        raise BadRevisionBump(
            f"new_text revision must be {expected_revision + 1} (got {got})")
    _rotate_backup(path, keep_backups)
    tmp = path.with_name(f".tmp-{path.name}-{os.getpid()}")
    tmp.write_text(new_text)
    os.replace(tmp, path)  # atomic
    return {"revision": expected_revision + 1, "hash": content_hash(new_text)}


def _backup_sort_key(path: Path) -> tuple[int, int]:
    """Numeric sort key ``(revision, timestamp)`` for backup filenames.

    Backups are ``.backup-{stem}-{old_rev}-{time_ns}``; sorting the filename
    lexicographically mis-orders revisions past 9 (``'10' < '5'``). Sort by the
    trailing numeric revision and timestamp so the most recent backups survive
    rotation.
    """
    try:
        *_, rev, stamp = path.name.split("-")
        return (int(rev) if rev != "x" else -1, int(stamp))
    except (ValueError, TypeError):
        return (-1, 0)


def _rotate_backup(path: Path, keep_backups: int) -> None:
    parent = path.parent
    old_text = path.read_text()
    old_rev_m = _REVISION_RE.search(old_text)
    old_rev = old_rev_m.group(1) if old_rev_m else "x"
    backup = parent / f"{BACKUP_PREFIX}{path.stem}-{old_rev}-{time.time_ns()}"
    backup.write_text(old_text)
    backups = sorted(parent.glob(f"{BACKUP_PREFIX}{path.stem}-*"),
                     key=_backup_sort_key)
    extras = backups if keep_backups == 0 else backups[:-keep_backups]
    for extra in extras:
        extra.unlink()
