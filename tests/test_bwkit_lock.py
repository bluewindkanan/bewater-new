"""TDD for bwkit.cas single-writer lock (spec §12.5). Stdlib-only."""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
import yaml

from bwkit import cas


@pytest.fixture
def v5_root(tmp_path: Path) -> Path:
    (tmp_path / "_bewater").mkdir()
    return tmp_path


def test_content_hash_is_sha256_of_body():
    assert cas.content_hash("hello") == hashlib.sha256(b"hello").hexdigest()


def test_acquire_creates_exclusive_lockfile(v5_root):
    info = cas.acquire_lock(v5_root, owner="s1")
    assert info["owner"] == "s1"
    assert cas.lock_path(v5_root).exists()
    assert "pid" in info and "acquired_at" in info


def test_second_acquire_is_rejected(v5_root):
    cas.acquire_lock(v5_root, owner="s1")
    with pytest.raises(cas.LockError) as exc:
        cas.acquire_lock(v5_root, owner="s2")
    assert "s1" in str(exc.value)


def test_release_lets_next_session_acquire(v5_root):
    cas.acquire_lock(v5_root, owner="s1")
    cas.release_lock(v5_root, owner="s1")
    assert cas.acquire_lock(v5_root, owner="s2")["owner"] == "s2"


def test_release_wrong_owner_is_rejected(v5_root):
    cas.acquire_lock(v5_root, owner="s1")
    with pytest.raises(cas.LockError):
        cas.release_lock(v5_root, owner="s2")
    assert cas.lock_status(v5_root)["owner"] == "s1"


def test_release_when_unlocked_is_noop(v5_root):
    cas.release_lock(v5_root, owner="s1")  # must not raise


def test_lock_status_none_when_unlocked(v5_root):
    assert cas.lock_status(v5_root) is None


def test_stale_pid_dead_is_preemptable(v5_root):
    cas.acquire_lock(v5_root, owner="dead-session")
    p = cas.lock_path(v5_root)
    data = yaml.safe_load(p.read_text())
    data["pid"] = 999999  # almost certainly not running
    p.write_text(yaml.safe_dump(data))
    assert cas.acquire_lock(v5_root, owner="s2")["owner"] == "s2"


def test_stale_past_ttl_is_preemptable(v5_root):
    cas.acquire_lock(v5_root, owner="old")
    p = cas.lock_path(v5_root)
    data = yaml.safe_load(p.read_text())
    data["acquired_at"] = -1e9  # distant past -> past ttl even though pid is alive
    p.write_text(yaml.safe_dump(data))
    assert cas.acquire_lock(v5_root, owner="s2", ttl_seconds=60)["owner"] == "s2"
