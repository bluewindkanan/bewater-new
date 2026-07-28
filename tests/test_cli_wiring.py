"""CLI wiring tests: exercise each subcommand handler via main([...]).

These drive the argparse glue directly (fast, deterministic) to cover the
branch logic — success paths, validation-issue exit codes, and the
gate-scan NotImplementedError -> exit 2 path. End-to-end subprocess coverage
lives in test_smoke.py.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from bw import cli, ledger_ops
from bw import init as init_mod


def _add(root: Path, statement="s", branch="sol-01", status="active") -> str:
    a = ledger_ops.add(root, dict(
        statement=statement, layer="concept", category="consumer",
        impact="high", uncertainty="high", evidence_level="L1",
        validation_status="open", status=status, evidence_ref="",
        derived_from=[], affects=[], branch=branch))
    return a.id


# --- ledger add / update ---

def test_ledger_add_and_update_via_cli(tmp_project, capsys):
    rc = cli.main(["ledger", "add", str(tmp_project),
                   "--statement", "s", "--layer", "concept",
                   "--category", "consumer", "--impact", "high",
                   "--uncertainty", "high", "--branch", "sol-01"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "A-001" in out

    rc = cli.main(["ledger", "update", str(tmp_project), "A-001",
                   "--set", "statement=new", "--status", "killed"])
    assert rc == 0
    assert "updated" in capsys.readouterr().out


def test_ledger_update_set_kv_parse_error(tmp_project):
    with pytest.raises(SystemExit):
        cli.main(["ledger", "update", str(tmp_project), "A-001", "--set", "noequals"])


def test_ledger_update_unknown_id(tmp_project, capsys):
    rc = cli.main(["ledger", "update", str(tmp_project), "A-999", "--statement", "x"])
    assert rc == 1
    assert "A-999" in capsys.readouterr().out


# --- ledger validate ---

def test_ledger_validate_clean_and_violating(tmp_project, capsys):
    _add(tmp_project)
    assert cli.main(["ledger", "validate", str(tmp_project), "A-001"]) == 0
    assert "OK" in capsys.readouterr().out


def test_ledger_validate_unknown_id(tmp_project, capsys):
    rc = cli.main(["ledger", "validate", str(tmp_project), "A-999"])
    assert rc == 1


# --- trace / backtrack / baseline ---

def test_ledger_trace_upstream_and_downstream(tmp_project, capsys):
    a1 = _add(tmp_project, statement="root", branch="sol-01")
    a2 = ledger_ops.add(tmp_project, dict(
        statement="child", layer="feature", category="consumer",
        impact="low", uncertainty="low", evidence_level="L1",
        validation_status="open", status="active", evidence_ref="",
        derived_from=[a1], affects=[], branch="sol-01")).id

    assert cli.main(["ledger", "trace", str(tmp_project), a2, "--direction", "upstream"]) == 0
    assert a1 in capsys.readouterr().out

    assert cli.main(["ledger", "trace", str(tmp_project), a1, "--direction", "downstream"]) == 0
    assert a2 in capsys.readouterr().out


def test_ledger_trace_no_lineage(tmp_project, capsys):
    # isolated assumption, no upstream/downstream reachable
    aid = _add(tmp_project, statement="solo", branch="sol-01")
    assert cli.main(["ledger", "trace", str(tmp_project), aid, "--direction", "upstream"]) == 0
    assert "no upstream lineage" in capsys.readouterr().out


def test_ledger_trace_dangling(tmp_project, capsys):
    _add(tmp_project)
    # craft a dangling derived_from by writing directly
    from bw import io
    ledger = io.load_ledger(tmp_project)
    ledger.assumptions[0].derived_from = ["A-999"]
    io.save_ledger(tmp_project, ledger)
    rc = cli.main(["ledger", "trace", str(tmp_project), "A-001", "--direction", "upstream"])
    assert rc == 1


def test_ledger_backtrack_small_loop(tmp_project, capsys):
    aid = _add(tmp_project)  # concept layer -> small loop
    rc = cli.main(["ledger", "backtrack", str(tmp_project), aid])
    assert rc == 0
    out = capsys.readouterr().out
    assert "small" in out
    assert "reframe" in out


def test_ledger_backtrack_unknown_id(tmp_project, capsys):
    rc = cli.main(["ledger", "backtrack", str(tmp_project), "A-999"])
    assert rc == 1


def test_ledger_baseline(tmp_project, capsys):
    _add(tmp_project)
    rc = cli.main(["ledger", "baseline", str(tmp_project), "--label", "G2"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "G2" in out
    assert "1 assumptions" in out


# --- validate (system-wide) ---

def test_validate_clean(tmp_project, capsys):
    _add(tmp_project)
    assert cli.main(["validate", str(tmp_project)]) == 0
    assert "clean" in capsys.readouterr().out


def test_validate_reports_issues(tmp_project, capsys):
    _add(tmp_project)
    # introduce a dangling ref
    from bw import io
    ledger = io.load_ledger(tmp_project)
    ledger.assumptions[0].affects = ["A-999"]
    io.save_ledger(tmp_project, ledger)
    rc = cli.main(["validate", str(tmp_project)])
    assert rc == 1
    out = capsys.readouterr().out
    assert "dangling-ref" in out


# --- gate-scan ---

def test_gate_scan_g1_blocks_thin(tmp_project, capsys):
    rc = cli.main(["gate-scan", "G1", str(tmp_project)])
    assert rc == 1  # no charter -> go withheld


def test_gate_scan_g2_not_implemented_exits_2(tmp_project, capsys):
    rc = cli.main(["gate-scan", "G2", str(tmp_project)])
    assert rc == 2
    assert "not yet implemented" in capsys.readouterr().out


# --- hash ---

def test_hash_artifact(tmp_project, tmp_path, capsys):
    art = tmp_project / "_bewater" / "artifacts" / "discover" / "x.md"
    art.parent.mkdir(parents=True, exist_ok=True)
    art.write_text("---\nartifact_id: x\nkind: research\nstage: discover\nstatus: draft\nhash: ''\n---\nbody")
    assert cli.main(["hash", str(art)]) == 0
    assert "hash=" in capsys.readouterr().out


def test_hash_stale(tmp_project, capsys):
    # dependent references an id with no current artifact -> stale
    dep = tmp_project / "_bewater" / "artifacts" / "discover" / "dep.md"
    dep.parent.mkdir(parents=True, exist_ok=True)
    dep.write_text(
        "---\n"
        "artifact_id: dep\nkind: research\nstage: discover\nstatus: draft\nhash: ''\n"
        "last_validated_against:\n  - {id: gone, hash: old}\n"
        "---\nbody"
    )
    assert cli.main(["hash", str(dep), "--stale"]) == 0
    assert "STALE" in capsys.readouterr().out


def test_hash_refresh_deps_captures_new_hash(tmp_project, capsys):
    # C1: hashing the upstream then --refresh-deps must propagate the NEW hash
    # so dependents are fresh, not stale, the instant the command returns.
    from bw import hashing, io
    arts = tmp_project / "_bewater" / "artifacts" / "discover"
    arts.mkdir(parents=True, exist_ok=True)
    upstream = arts / "insights.md"
    upstream.write_text(
        "---\nartifact_id: INS-1\nkind: research\nstage: discover\nstatus: final\nhash: ''\n---\nubody"
    )
    dep = arts / "hyp.md"
    dep.write_text(
        "---\n"
        "artifact_id: HYP-1\nkind: research\nstage: discover\nstatus: final\nhash: ''\n"
        "last_validated_against:\n  - {id: INS-1, hash: stale-old}\n"
        "---\nhbody"
    )
    rc = cli.main(["hash", str(upstream), "--refresh-deps"])
    assert rc == 0
    new_hash = io.read_artifact(upstream)[0].hash
    assert new_hash == hashing.content_hash("ubody")
    recorded = io.read_artifact(dep)[0].last_validated_against[0]["hash"]
    assert recorded == new_hash  # dependent captured the upstream's NEW hash
    assert hashing.is_stale(tmp_project, dep) is False


def test_hash_stale_and_refresh_deps_mutually_exclusive(tmp_project):
    # I2: argparse should reject --stale + --refresh-deps with exit code 2.
    art = tmp_project / "_bewater" / "artifacts" / "discover" / "x.md"
    art.parent.mkdir(parents=True, exist_ok=True)
    art.write_text("---\nartifact_id: x\nkind: research\nstage: discover\nstatus: draft\nhash: ''\n---\nbody")
    with pytest.raises(SystemExit) as exc:
        cli.main(["hash", str(art), "--stale", "--refresh-deps"])
    assert exc.value.code == 2


# --- init ---

def test_init_creates_tree(tmp_path, capsys):
    proj = tmp_path / "proj"
    assert cli.main(["init", str(proj)]) == 0
    assert (proj / "_bewater" / "state" / "assumption-ledger.yaml").exists()
    assert "_bewater/" in capsys.readouterr().out


def test_init_force_overwrites(tmp_path):
    proj = tmp_path / "proj"
    init_mod.scaffold(proj)
    lp = proj / "_bewater" / "state" / "assumption-ledger.yaml"
    lp.write_text(yaml.safe_dump({"project": "x", "assumptions": [{"id": "junk"}]}))
    cli.main(["init", str(proj), "--force"])
    data = yaml.safe_load(lp.read_text())
    assert data["assumptions"] == []
