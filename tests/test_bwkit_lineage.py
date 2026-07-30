# tests/test_bwkit_lineage.py
"""TDD for bwkit.lineage — transitive impact / dependents (spec §8.2, §12.3).
Schema-agnostic: operates on caller-built dependent->dependency edges."""
from __future__ import annotations

import io
import json

from bwkit import cli, lineage


def _e(dependent, dependency):
    return {"dependent": dependent, "dependency": dependency}


def test_chain_two_hops():
    # C depends on A; A depends on B. Falsify B -> dependents A (depth1), C (depth2).
    edges = [_e("A", "B"), _e("C", "A")]
    r = lineage.transitive_dependents(edges, ["B"])
    assert r["dependents"] == ["A", "C"]
    assert r["depth"] == {"A": 1, "C": 2}


def test_diamond_converges():
    # D->B, D->C, B->A, C->A. Falsify A -> B,C (depth1), D (depth2 via either).
    edges = [_e("B", "A"), _e("C", "A"), _e("D", "B"), _e("D", "C")]
    r = lineage.transitive_dependents(edges, ["A"])
    assert r["dependents"] == ["B", "C", "D"]
    assert r["depth"]["D"] == 2


def test_no_dependents():
    edges = [_e("A", "B")]
    r = lineage.transitive_dependents(edges, ["Z"])
    assert r["dependents"] == []
    assert r["depth"] == {}


def test_cycle_does_not_loop_forever():
    # A->B, B->A. Falsify B -> A (depth1); A's dependent B is the root, not re-listed.
    edges = [_e("A", "B"), _e("B", "A")]
    r = lineage.transitive_dependents(edges, ["B"])
    assert r["dependents"] == ["A"]
    assert r["depth"] == {"A": 1}


def test_root_not_listed_as_own_dependent():
    edges = [_e("A", "B"), _e("B", "A")]
    r = lineage.transitive_dependents(edges, ["A", "B"])
    assert "A" not in r["dependents"] and "B" not in r["dependents"]


def test_multiple_roots_union():
    edges = [_e("A", "X"), _e("B", "Y")]
    r = lineage.transitive_dependents(edges, ["X", "Y"])
    assert r["dependents"] == ["A", "B"]


def test_cli_scan_impact_reads_stdin(capsys):
    payload = json.dumps({"edges": [_e("A", "B"), _e("C", "A")], "roots": ["B"]})
    rc = cli.main(["scan", "impact"], _stdin=io.StringIO(payload))
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["dependents"] == ["A", "C"]
