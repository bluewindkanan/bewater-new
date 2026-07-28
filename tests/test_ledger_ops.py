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
