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
    (root / "_bewater").mkdir(parents=True, exist_ok=True)
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
