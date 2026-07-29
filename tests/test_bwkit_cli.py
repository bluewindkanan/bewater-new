"""CLI wiring for bwkit — drive main([...]) directly (spec §12.5 CLI surface)."""
from __future__ import annotations

import io
import re
from pathlib import Path

import pytest
import yaml

from bwkit import cas, cli


@pytest.fixture
def v5_root(tmp_path: Path) -> Path:
    (tmp_path / "_bewater").mkdir()
    (tmp_path / "_bewater" / "ledger.yaml").write_text(yaml.safe_dump(
        {"schema_version": 1, "revision": 3, "next_id": 4, "assumptions": {}}))
    return tmp_path


def test_help_lists_subcommands(capsys):
    with pytest.raises(SystemExit) as exc:
        cli.main(["--help"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    for token in ["lock", "cas"]:
        assert token in out


def test_lock_acquire_then_status(v5_root, capsys):
    assert cli.main(["lock", "acquire", str(v5_root), "--owner", "s1"]) == 0
    assert cli.main(["lock", "status", str(v5_root)]) == 0
    assert "s1" in capsys.readouterr().out


def test_lock_release(v5_root):
    cli.main(["lock", "acquire", str(v5_root), "--owner", "s1"])
    assert cli.main(["lock", "release", str(v5_root), "--owner", "s1"]) == 0
    assert cas.lock_status(v5_root) is None


def test_cas_show_prints_revision_and_hash(v5_root, capsys):
    p = v5_root / "_bewater" / "ledger.yaml"
    assert cli.main(["cas", "show", str(p)]) == 0
    out = capsys.readouterr().out
    assert "revision=3" in out
    assert "hash=" in out


def test_cas_commit_reads_new_text_from_stdin(v5_root):
    p = v5_root / "_bewater" / "ledger.yaml"
    new = re.sub(r"(?m)^revision:\s*\d+", "revision: 4", p.read_text(), count=1)
    rc = cli.main(["cas", "commit", str(p), "--expected", "3"], _stdin=io.StringIO(new))
    assert rc == 0
    assert yaml.safe_load(p.read_text())["revision"] == 4


def test_cas_commit_conflict_returns_nonzero(v5_root):
    p = v5_root / "_bewater" / "ledger.yaml"
    data = yaml.safe_load(p.read_text())
    data["revision"] = 4
    p.write_text(yaml.safe_dump(data))
    new = re.sub(r"(?m)^revision:\s*\d+", "revision: 5", p.read_text(), count=1)
    rc = cli.main(["cas", "commit", str(p), "--expected", "3"], _stdin=io.StringIO(new))
    assert rc == 1
