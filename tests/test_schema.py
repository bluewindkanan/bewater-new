import pytest

from bw import schema
from bw.errors import ValidationError

# --- Assumption.is_achilles_heel + invariants (from brief) ---

def test_achilles_heel_is_high_high():
    a = schema.Assumption(id="A-1", statement="x", layer="concept", category="consumer",
                          impact="high", uncertainty="high", evidence_level="L3",
                          validation_status="open", status="active", evidence_ref="",
                          derived_from=[], affects=[], branch="sol-01")
    assert a.is_achilles_heel is True


def test_invariant_achilles_validated_needs_L4():
    a = schema.Assumption(id="A-1", statement="x", layer="concept", category="consumer",
                          impact="high", uncertainty="high", evidence_level="L3",
                          validation_status="validated", status="active", evidence_ref="kb/x",
                          derived_from=[], affects=[], branch="sol-01")
    with pytest.raises(ValidationError):
        a.check_invariants()


def test_assumption_round_trip():
    a = schema.Assumption(id="A-1", statement="x", layer="root", category="consumer",
                          impact="low", uncertainty="medium", evidence_level="L1",
                          validation_status="open", status="active", evidence_ref="",
                          derived_from=[], affects=[], branch="sol-01")
    a2 = schema.Assumption.from_dict(a.to_dict())
    assert a2 == a


# --- Enum coverage ---

def test_evidence_level_ordering():
    assert schema.EvidenceLevel["L3"] < schema.EvidenceLevel["L4"]
    assert schema.EvidenceLevel["L4"] < schema.EvidenceLevel["L6"]
    assert not (schema.EvidenceLevel["L5"] < schema.EvidenceLevel["L1"])


def test_enum_values():
    assert {m.name for m in schema.Layer} == {"root", "strategy", "opportunity", "concept", "feature"}
    assert {m.name for m in schema.Category} == {"consumer", "commercial", "technical", "distribution", "regulatory"}
    assert [m.value for m in schema.Impact] == ["low", "medium", "high"]
    assert [m.value for m in schema.Uncertainty] == ["low", "medium", "high"]
    assert [m.value for m in schema.EvidenceLevel] == ["L1", "L2", "L3", "L4", "L5", "L6"]
    assert [m.value for m in schema.ValidationStatus] == ["open", "testing", "validated", "falsified", "superseded"]
    assert [m.value for m in schema.AssumptionStatus] == ["active", "killed", "merged"]
    assert {m.value for m in schema.ArtifactKind} == {"charter", "directional-hypothesis", "strategy",
                                                      "opportunity-area", "concept", "solution",
                                                      "investment-narrative", "research", "insights"}
    assert [m.value for m in schema.ArtifactStatus] == ["draft", "final", "superseded"]
    assert [m.value for m in schema.GateExit] == ["go", "conditional-go", "recycle", "pivot", "kill"]


# --- Invariant branches ---

def test_achilles_validated_at_L4_ok():
    a = schema.Assumption(id="A-1", statement="x", layer="concept", category="consumer",
                          impact="high", uncertainty="high", evidence_level="L4",
                          validation_status="validated", status="active", evidence_ref="kb/x",
                          derived_from=[], affects=[], branch="sol-01")
    a.check_invariants()


def test_achilles_validated_at_L5_ok():
    a = schema.Assumption(id="A-1", statement="x", layer="concept", category="consumer",
                          impact="high", uncertainty="high", evidence_level="L5",
                          validation_status="validated", status="active", evidence_ref="kb/x",
                          derived_from=[], affects=[], branch="sol-01")
    a.check_invariants()


def test_not_achilles_validated_low_evidence_ok():
    a = schema.Assumption(id="A-1", statement="x", layer="concept", category="consumer",
                          impact="low", uncertainty="high", evidence_level="L1",
                          validation_status="validated", status="active", evidence_ref="kb/x",
                          derived_from=[], affects=[], branch="sol-01")
    a.check_invariants()


def test_is_achilles_heel_false_when_low_impact():
    a = schema.Assumption(id="A-1", statement="x", layer="concept", category="consumer",
                          impact="low", uncertainty="high", evidence_level="L1",
                          validation_status="open", status="active", evidence_ref="",
                          derived_from=[], affects=[], branch="sol-01")
    assert a.is_achilles_heel is False


def test_achilles_heel_not_in_to_dict():
    a = schema.Assumption(id="A-1", statement="x", layer="root", category="consumer",
                          impact="low", uncertainty="medium", evidence_level="L1",
                          validation_status="open", status="active", evidence_ref="",
                          derived_from=[], affects=[], branch="sol-01")
    d = a.to_dict()
    assert "is_achilles_heel" not in d


def test_from_dict_accepts_enum_objects():
    raw = {"id": "A-2", "statement": "y", "layer": schema.Layer.strategy,
           "category": schema.Category.technical, "impact": schema.Impact.high,
           "uncertainty": schema.Uncertainty.high, "evidence_level": schema.EvidenceLevel.L2,
           "validation_status": schema.ValidationStatus.open,
           "status": schema.AssumptionStatus.active, "evidence_ref": "",
           "derived_from": ["A-1"], "affects": ["A-3"], "branch": "sol-02"}
    a = schema.Assumption.from_dict(raw)
    assert a.layer == schema.Layer.strategy
    assert a.derived_from == ["A-1"]
    assert a.to_dict()["layer"] == "strategy"


# --- Ledger ---

def test_ledger_round_trip():
    a1 = schema.Assumption(id="A-1", statement="x", layer="root", category="consumer",
                           impact="low", uncertainty="medium", evidence_level="L1",
                           validation_status="open", status="active", evidence_ref="",
                           derived_from=[], affects=[], branch="sol-01")
    a2 = schema.Assumption(id="A-2", statement="y", layer="strategy", category="technical",
                           impact="high", uncertainty="high", evidence_level="L4",
                           validation_status="validated", status="active", evidence_ref="kb/y",
                           derived_from=["A-1"], affects=[], branch="sol-02")
    led = schema.Ledger(schema_version=1, revision=3, next_id=5,
                        updated_at="2026-01-01", updated_by="test",
                        assumptions={"A-1": a1, "A-2": a2})
    led2 = schema.Ledger.from_dict(led.to_dict())
    assert led2 == led
    assert led2.assumptions["A-2"].is_achilles_heel is True


def test_ledger_defaults():
    led = schema.Ledger()
    assert led.schema_version == 1
    assert led.revision == 1
    assert led.next_id == 1
    assert led.updated_at is None
    assert led.updated_by == "bw-init"
    assert led.assumptions == {}


def test_ledger_from_dict_v4_list_compat():
    """v4 list-based assumptions are converted to dict on load."""
    a1_dict = {"id": "A-1", "statement": "x", "layer": "root", "category": "consumer",
               "impact": "low", "uncertainty": "medium", "evidence_level": "L1",
               "validation_status": "open", "status": "active", "evidence_ref": "",
               "derived_from": [], "affects": [], "branch": "sol-01"}
    led = schema.Ledger.from_dict({"assumptions": [a1_dict]})
    assert isinstance(led.assumptions, dict)
    assert "A-1" in led.assumptions
    assert led.assumptions["A-1"].id == "A-1"


# --- ArtifactMeta ---

def test_artifact_meta_round_trip():
    am = schema.ArtifactMeta(
        artifact_id="charter", kind="charter", stage="charter", status="final",
        hash="abc123", locked=True, validated_by="ceo", validated_at="2026-01-01",
        signoffs=["ceo"], dual_sided={"left": "a", "right": "b"}, derived_from=[],
        last_validated_against=[{"id": "charter", "hash": "abc123"}],
        created_at="2026-01-01", updated_at="2026-01-02",
    )
    am2 = schema.ArtifactMeta.from_dict(am.to_dict())
    assert am2 == am


def test_artifact_meta_empty():
    am = schema.ArtifactMeta.empty()
    assert am.artifact_id == ""
    assert am.locked is False
    assert am.signoffs == []
    assert am.derived_from == []
    assert am.last_validated_against == []


# --- GateRecord ---

def test_gate_record_round_trip():
    gr = schema.GateRecord(
        gate="charter", attempt_id="charter/1", position=1,
        subject_refs=["charter"], decision_date="2026-01-02",
        decision_maker="ceo", exit="go", conditions=[],
    )
    gr2 = schema.GateRecord.from_dict(gr.to_dict())
    assert gr2 == gr
