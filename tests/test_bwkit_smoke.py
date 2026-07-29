"""End-to-end subprocess smoke for bwkit (spec §12.5 acceptance)."""
from __future__ import annotations

import re
import subprocess
import sys


def test_python_m_bwkit_help():
    r = subprocess.run([sys.executable, "-m", "bwkit", "--help"], capture_output=True, text=True)
    assert r.returncode == 0
    assert "lock" in r.stdout and "cas" in r.stdout


def test_end_to_end_lock_and_commit(tmp_path):
    bw = tmp_path / "_bewater"
    bw.mkdir()
    (bw / "ledger.yaml").write_text("schema_version: 1\nrevision: 3\nnext_id: 4\nassumptions: {}\n")
    p = bw / "ledger.yaml"

    acquire = subprocess.run(
        [sys.executable, "-m", "bwkit", "lock", "acquire", str(tmp_path), "--owner", "smoke"],
        capture_output=True, text=True)
    assert acquire.returncode == 0, acquire.stderr

    new = re.sub(r"(?m)^revision:\s*\d+", "revision: 4", p.read_text(), count=1)
    commit = subprocess.run(
        [sys.executable, "-m", "bwkit", "cas", "commit", str(p), "--expected", "3"],
        input=new, text=True, capture_output=True)
    assert commit.returncode == 0, commit.stderr
    assert "revision: 4" in p.read_text()
