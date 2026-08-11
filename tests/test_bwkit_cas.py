"""TDD for bwkit.cas text-level revision CAS (spec §12.5, H1). Stdlib-only:
bwkit never parses YAML; the caller supplies new_text verbatim."""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from bwkit import cas


@pytest.fixture
def v5_root(tmp_path: Path) -> Path:
    bw = tmp_path / "_bewater"
    bw.mkdir()
    (bw / "ledger.yaml").write_text(yaml.safe_dump(
        {"schema_version": 1, "revision": 3, "next_id": 4, "assumptions": {}}))
    return tmp_path


def _ledger(root: Path) -> Path:
    return root / "_bewater" / "ledger.yaml"


def _bump(text: str, new_rev: int) -> str:
    return re.sub(r"(?m)^revision:\s*\d+", f"revision: {new_rev}", text, count=1)


def test_read_revision(v5_root):
    assert cas.read_revision(_ledger(v5_root)) == 3


def test_read_revision_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        cas.read_revision(tmp_path / "missing.yaml")


def test_read_revision_missing_field(tmp_path):
    (tmp_path / "x.yaml").write_text("schema_version: 1\nnotes: hi\n")
    with pytest.raises(KeyError):
        cas.read_revision(tmp_path / "x.yaml")


def test_commit_writes_and_returns_new_revision(v5_root):
    p = _ledger(v5_root)
    new = _bump(p.read_text(), 4).replace("assumptions: {}", 'assumptions: {A-001: {stmt: x}}')
    r = cas.commit(p, new, expected_revision=3)
    assert r["revision"] == 4
    assert "hash" in r and r["hash"] == cas.content_hash(new)
    data = yaml.safe_load(p.read_text())
    assert data["revision"] == 4
    assert data["assumptions"]["A-001"]["stmt"] == "x"


def test_commit_conflict_does_not_write(v5_root):
    p = _ledger(v5_root)
    data = yaml.safe_load(p.read_text())
    data["revision"] = 4  # another writer bumped first
    p.write_text(yaml.safe_dump(data))
    with pytest.raises(cas.CasConflict):
        cas.commit(p, _bump(p.read_text(), 5), expected_revision=3)
    assert yaml.safe_load(p.read_text())["revision"] == 4  # unchanged


def test_commit_rejects_missing_bump(v5_root):
    p = _ledger(v5_root)
    with pytest.raises(cas.BadRevisionBump):
        cas.commit(p, p.read_text(), expected_revision=3)  # revision still 3, not 4


def test_commit_creates_backup_of_old_content(v5_root):
    p = _ledger(v5_root)
    cas.commit(p, _bump(p.read_text(), 4), expected_revision=3)
    backups = list((v5_root / "_bewater").glob(".backup-ledger-*"))
    assert len(backups) == 1
    assert yaml.safe_load(backups[0].read_text())["revision"] == 3


def test_commit_keeps_only_n_backups(v5_root):
    p = _ledger(v5_root)
    rev = 3
    for _ in range(7):
        cas.commit(p, _bump(p.read_text(), rev + 1), expected_revision=rev)
        rev += 1
    assert len(list((v5_root / "_bewater").glob(".backup-ledger-*"))) == 5


def test_commit_keep_backups_zero_keeps_no_backups(v5_root):
    p = _ledger(v5_root)
    cas.commit(p, _bump(p.read_text(), 4), expected_revision=3, keep_backups=0)
    assert list((v5_root / "_bewater").glob(".backup-ledger-*")) == []


def test_commit_keeps_most_recent_backups_when_revision_has_two_digits(v5_root):
    """Rotation must keep the 5 most recent backups by numeric revision, not by
    lexicographic filename order (where '10' < '5')."""
    p = _ledger(v5_root)
    rev = 3
    for _ in range(12):  # commit 3 -> 15, backups for old revs 3..14
        cas.commit(p, _bump(p.read_text(), rev + 1), expected_revision=rev)
        rev += 1
    kept = sorted(
        int(b.name.split("-")[-2])
        for b in (v5_root / "_bewater").glob(".backup-ledger-*")
    )
    assert kept == [10, 11, 12, 13, 14]


def test_commit_writes_new_text_verbatim(v5_root):
    p = _ledger(v5_root)
    marker = "# VERBATIM-MARKER keep-me\n"
    new = marker + _bump(p.read_text(), 4)
    cas.commit(p, new, expected_revision=3)
    assert marker in p.read_text()


def test_commit_leaves_no_temp_file(v5_root):
    p = _ledger(v5_root)
    cas.commit(p, _bump(p.read_text(), 4), expected_revision=3)
    assert [x for x in (v5_root / "_bewater").iterdir() if x.name.startswith(".tmp-")] == []
