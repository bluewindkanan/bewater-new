"""Backtrack lineage integration: caller-built edges -> bwkit.transitive_dependents -> the BT-record
affected_refs. Proves the Phase 2a lineage helper powers Phase 2b backtrack impact computation."""
from __future__ import annotations

from bwkit import lineage


def _e(dependent, dependency):
    return {"dependent": dependent, "dependency": dependency}


def test_falsified_root_assumption_surfaces_solution_and_narrative():
    # A-001 (root) <- derived by solution ART-007 <- derived by narrative ART-008.
    edges = [_e("artifact:ART-007@2", "assumption:A-001@4"),
             _e("artifact:ART-008@1", "artifact:ART-007@2")]
    r = lineage.transitive_dependents(edges, ["assumption:A-001@4"])
    assert r["dependents"] == ["artifact:ART-007@2", "artifact:ART-008@1"]
    assert r["depth"]["artifact:ART-008@1"] == 2


def test_baseline_membership_edge_makes_a_large_loop():
    # A-001 is frozen in baseline B-002 -> membership edge -> falsifying A-001 touches the baseline.
    edges = [_e("baseline:B-002", "assumption:A-001@4")]
    r = lineage.transitive_dependents(edges, ["assumption:A-001@4"])
    assert r["dependents"] == ["baseline:B-002"]   # => loop_type large, gates_to_rerun set
