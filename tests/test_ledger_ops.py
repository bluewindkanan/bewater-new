import pytest
from bw import ledger_ops
from bw.errors import ValidationError


def _f(**over):
    base = dict(statement="s", layer="concept", category="consumer", impact="high",
                uncertainty="high", evidence_level="L3", validation_status="open",
                evidence_ref="", derived_from=[], affects=[], branch="sol-01")
    base.update(over); return base


def test_add_assigns_sequential_id_and_persists(tmp_project):
    a = ledger_ops.add(tmp_project, _f())
    assert a.id == "A-001"
    assert ledger_ops.add(tmp_project, _f()).id == "A-002"


def test_add_rejects_invariant_violation(tmp_project):
    # achilles + validated + L3 < L4
    with pytest.raises(ValidationError):
        ledger_ops.add(tmp_project, _f(validation_status="validated"))


def test_update_recomputes_achilles_on_impact_change(tmp_project):
    a = ledger_ops.add(tmp_project, _f(impact="low"))   # not achilles
    assert a.is_achilles_heel is False
    a2 = ledger_ops.update(tmp_project, a.id, {"impact": "high"})
    assert a2.is_achilles_heel is True


def test_add_applies_defaults_when_omitted(tmp_project):
    minimal = dict(statement="s", layer="concept", category="consumer",
                   impact="high", uncertainty="high")
    a = ledger_ops.add(tmp_project, minimal)
    assert a.validation_status.value == "open"
    assert a.evidence_level.value == "L1"
    assert a.status.value == "active"
    assert a.derived_from == []
    assert a.affects == []
    assert a.id == "A-001"


def test_add_persists_to_disk(tmp_project):
    from bw import io
    a = ledger_ops.add(tmp_project, _f(statement="persisted"))
    reloaded = io.load_ledger(tmp_project).assumptions
    assert reloaded[-1].id == a.id
    assert reloaded[-1].statement == "persisted"


def test_add_generates_unique_ids(tmp_project):
    ids = {ledger_ops.add(tmp_project, _f()).id for _ in range(5)}
    assert ids == {"A-001", "A-002", "A-003", "A-004", "A-005"}


def test_add_rejects_explicit_colliding_id(tmp_project):
    ledger_ops.add(tmp_project, _f())
    with pytest.raises(ValidationError):
        ledger_ops.add(tmp_project, _f(id="A-001"))


def test_add_accepts_explicit_non_colliding_id(tmp_project):
    a = ledger_ops.add(tmp_project, _f(id="A-042"))
    assert a.id == "A-042"
    # next auto id should look past the explicit one? No — spec: NNN = max suffix + 1.
    # Explicit id does not rebase the counter (counter tracks actual stored max).
    b = ledger_ops.add(tmp_project, _f())
    assert b.id == "A-043"


def test_update_applies_changes_and_persists(tmp_project):
    from bw import io
    a = ledger_ops.add(tmp_project, _f())
    a2 = ledger_ops.update(tmp_project, a.id, {"statement": "changed", "impact": "low"})
    assert a2.statement == "changed"
    assert a2.impact.value == "low"
    reloaded = io.load_ledger(tmp_project).assumptions
    assert reloaded[0].statement == "changed"
    assert reloaded[0].impact.value == "low"


def test_update_rejects_invariant_violation(tmp_project):
    a = ledger_ops.add(tmp_project, _f())  # achilles, open, L3 — ok
    with pytest.raises(ValidationError):
        ledger_ops.update(tmp_project, a.id, {"validation_status": "validated"})


def test_update_rejects_unknown_id(tmp_project):
    ledger_ops.add(tmp_project, _f())
    with pytest.raises(KeyError):
        ledger_ops.update(tmp_project, "A-999", {"statement": "x"})


def test_update_rejects_colliding_id_change(tmp_project):
    ledger_ops.add(tmp_project, _f())              # A-001
    b = ledger_ops.add(tmp_project, _f())          # A-002
    with pytest.raises(ValidationError):
        ledger_ops.update(tmp_project, b.id, {"id": "A-001"})


def test_validate_one_returns_violations_without_raising(tmp_project):
    # achilles + validated + L3 < L4 — write it directly to bypass add's guard.
    from bw import io, schema
    bad = schema.Assumption(
        id="A-001", statement="s", layer="concept", category="consumer",
        impact="high", uncertainty="high", evidence_level="L3",
        validation_status="validated", status="active", evidence_ref="",
    )
    ledger = io.load_ledger(tmp_project)
    ledger.assumptions.append(bad)
    io.save_ledger(tmp_project, ledger)

    violations = ledger_ops.validate_one(tmp_project, "A-001")
    assert isinstance(violations, list)
    assert len(violations) == 1
    assert "achilles" in violations[0].lower() or "l4" in violations[0].lower()


def test_validate_one_clean_returns_empty(tmp_project):
    a = ledger_ops.add(tmp_project, _f(evidence_level="L5", validation_status="validated"))
    assert ledger_ops.validate_one(tmp_project, a.id) == []


def test_validate_one_unknown_id(tmp_project):
    with pytest.raises(KeyError):
        ledger_ops.validate_one(tmp_project, "A-999")


def add_raw(root, fields, id_override):
    """TEST-ONLY helper: write an assumption directly, bypassing add()'s
    auto-id assignment and invariant checks. Lets tests build cycles and
    explicit-id graphs that the production write path forbids."""
    from bw import io, schema
    payload = _f()
    payload.update(fields)
    payload["id"] = id_override
    for key, default in (
        ("validation_status", "open"), ("evidence_level", "L1"), ("status", "active"),
        ("derived_from", []), ("affects", []),
    ):
        payload.setdefault(key, default)
    assumption = schema.Assumption.from_dict(payload)
    ledger = io.load_ledger(root)
    ledger.assumptions.append(assumption)
    io.save_ledger(root, ledger)
    return assumption


def test_trace_upstream_and_downstream(tmp_project):
    ledger_ops.add(tmp_project, _f(id_override=None, statement="root", layer="root", derived_from=[]))
    # A-001 root; add A-002 derived_from A-001; A-003 derived_from A-002
    ledger_ops.add(tmp_project, _f(statement="mid", layer="strategy", derived_from=["A-001"]))
    ledger_ops.add(tmp_project, _f(statement="leaf", layer="concept", derived_from=["A-002"]))
    assert ledger_ops.trace(tmp_project, "A-003", "upstream") == ["A-002", "A-001"]
    assert ledger_ops.trace(tmp_project, "A-001", "downstream") == ["A-002", "A-003"]


def test_trace_detects_dangling(tmp_project):
    ledger_ops.add(tmp_project, _f(derived_from=["NOPE"]))
    with pytest.raises(ValidationError):
        ledger_ops.trace(tmp_project, "A-001", "upstream")


def test_trace_detects_cycle(tmp_project):
    ledger_ops.add(tmp_project, _f(statement="a", derived_from=["A-002"]))
    add_raw(tmp_project, _f(id_override="A-002", statement="b", derived_from=["A-001"]),
            id_override="A-002")  # bypass for test setup
    with pytest.raises(ValidationError):
        ledger_ops.trace(tmp_project, "A-001", "upstream")


def test_trace_downstream_via_affects(tmp_project):
    # downstream must follow `affects` in addition to reverse-derived_from.
    ledger_ops.add(tmp_project, _f(statement="a"))                  # A-001
    ledger_ops.add(tmp_project, _f(statement="b", affects=["A-003"]))  # A-002 affects A-003
    ledger_ops.add(tmp_project, _f(statement="c"))                  # A-003
    assert ledger_ops.trace(tmp_project, "A-002", "downstream") == ["A-003"]


def test_trace_unknown_start_id_raises(tmp_project):
    with pytest.raises(KeyError):
        ledger_ops.trace(tmp_project, "A-999", "upstream")


def test_trace_empty_when_no_neighbors(tmp_project):
    ledger_ops.add(tmp_project, _f())  # A-001, isolated
    assert ledger_ops.trace(tmp_project, "A-001", "upstream") == []
    assert ledger_ops.trace(tmp_project, "A-001", "downstream") == []


def test_trace_default_direction_is_upstream(tmp_project):
    ledger_ops.add(tmp_project, _f(statement="root", layer="root", derived_from=[]))
    ledger_ops.add(tmp_project, _f(statement="mid", derived_from=["A-001"]))
    assert ledger_ops.trace(tmp_project, "A-002") == ["A-001"]


# --- Task 8: baseline + backtrack ---

def test_backtrack_depth_by_layer(tmp_project):
    ledger_ops.add(tmp_project, _f(statement="root", layer="root", derived_from=[]))
    ledger_ops.add(tmp_project, _f(statement="con", layer="concept", derived_from=["A-001"]))
    # falsify the concept-level one -> small loop
    ledger_ops.update(tmp_project, "A-002", {"validation_status": "falsified"})
    r = ledger_ops.backtrack(tmp_project, "A-002")
    assert r.loop_type == "small" and r.depth_target == "reframe"
    # falsify the root one -> large loop to Discover
    ledger_ops.update(tmp_project, "A-001", {"validation_status": "falsified"})
    r = ledger_ops.backtrack(tmp_project, "A-001")
    assert r.loop_type == "large" and r.depth_target == "Discover"


def test_backtrack_upgrades_to_large_if_baseline_touched(tmp_project):
    ledger_ops.add(tmp_project, _f(statement="root", layer="concept", derived_from=[]))
    ledger_ops.baseline(tmp_project, "G2")
    ledger_ops.update(tmp_project, "A-001", {"validation_status": "falsified"})
    r = ledger_ops.backtrack(tmp_project, "A-001")
    assert r.must_repass_gate == "G2"   # touched baseline -> re-pass original gate


def test_backtrack_marks_downstream_stale(tmp_project):
    # A-002 is downstream of A-001 (derived_from A-001), so falsifying A-001
    # marks A-002 stale. (affects is a forward/downstream edge per T7; to put
    # A-002 below A-001 we use derived_from, matching test_backtrack_depth_by_layer.)
    ledger_ops.add(tmp_project, _f(statement="root", layer="root", derived_from=[]))
    ledger_ops.add(tmp_project, _f(statement="con", layer="concept", derived_from=["A-001"]))
    ledger_ops.update(tmp_project, "A-001", {"validation_status": "falsified"})
    r = ledger_ops.backtrack(tmp_project, "A-001")
    assert "A-002" in r.affected_ids


def test_baseline_snapshots_assumptions_and_artifacts(tmp_project):
    from bw import io, paths
    a = ledger_ops.add(tmp_project, _f(statement="root", layer="concept"))
    # create one artifact with a known hash
    art_dir = paths.artifacts_dir(tmp_project) / "immersion"
    art_dir.mkdir(parents=True)
    meta_body = (
        "---\n"
        "artifact_id: ART-1\nkind: charter\nstage: immersion\nstatus: draft\n"
        "hash: abc123\nlocked: false\nsignoffs: []\nderived_from: []\n"
        "last_validated_against: []\n"
        "---\n"
        "body text"
    )
    (art_dir / "charter.md").write_text(meta_body)

    snap = ledger_ops.baseline(tmp_project, "G2")
    assert "assumptions" in snap and "artifacts" in snap
    assert a.id in snap["assumptions"]
    # assumption content_hash is a sha256 hex (64 chars)
    assert len(snap["assumptions"][a.id]) == 64
    assert snap["artifacts"]["ART-1"] == "abc123"
    # persisted on the ledger
    ledger = io.load_ledger(tmp_project)
    assert ledger.last_baselined_at == "G2"
    assert ledger.baseline == snap


def test_backtrack_large_loop_for_strategy_and_opportunity(tmp_project):
    ledger_ops.add(tmp_project, _f(statement="s", layer="strategy", derived_from=[]))
    r = ledger_ops.backtrack(tmp_project, "A-001")
    assert r.loop_type == "large" and r.depth_target == "Define"
    ledger_ops.add(tmp_project, _f(statement="o", layer="opportunity", derived_from=[]))
    r = ledger_ops.backtrack(tmp_project, "A-002")
    assert r.loop_type == "large" and r.depth_target == "Define"


def test_backtrack_no_baseline_means_no_repass_gate(tmp_project):
    ledger_ops.add(tmp_project, _f(statement="root", layer="root", derived_from=[]))
    r = ledger_ops.backtrack(tmp_project, "A-001")
    assert r.must_repass_gate is None


def test_backtrack_upgrades_when_downstream_in_baseline(tmp_project):
    # falsified id is NOT in baseline, but a downstream affected id IS.
    ledger_ops.add(tmp_project, _f(statement="root", layer="root", derived_from=[]))
    ledger_ops.add(tmp_project, _f(statement="con", layer="concept", derived_from=["A-001"]))
    ledger_ops.baseline(tmp_project, "G2")   # both A-001, A-002 snapshotted
    ledger_ops.update(tmp_project, "A-001", {"validation_status": "falsified"})
    r = ledger_ops.backtrack(tmp_project, "A-001")
    assert "A-002" in r.affected_ids
    assert r.must_repass_gate == "G2"
    assert r.loop_type == "large"


def test_backtrack_unknown_id_raises(tmp_project):
    with pytest.raises(KeyError):
        ledger_ops.backtrack(tmp_project, "A-999")
