import pytest

from bw import evidence, schema
from bw.errors import ValidationError

# --- Assumption.is_achilles_heel + invariants (from brief) ---

def test_achilles_heel_is_high_high():
    a = schema.Assumption(id="A-1", statement="x", layer="concept", category="consumer",
                          impact="high", uncertainty="high", evidence_level="L3",
                          validation_status="untested", status="active", evidence_refs=[],
                          derived_from=[], affects=[], branch_id="BR-001")
    assert a.is_achilles_heel is True


def test_invariant_achilles_validated_needs_L4():
    a = schema.Assumption(id="A-1", statement="x", layer="concept", category="consumer",
                          impact="high", uncertainty="high", evidence_level="L3",
                          validation_status="supported", status="active", evidence_refs=["evidence:E-001@1"],
                          derived_from=[], affects=[], branch_id="BR-001")
    with pytest.raises(ValidationError):
        a.check_invariants()


def test_assumption_round_trip():
    a = schema.Assumption(id="A-1", statement="x", layer="root", category="consumer",
                          impact="low", uncertainty="medium", evidence_level="L1",
                          validation_status="untested", status="active", evidence_refs=[],
                          derived_from=[], affects=[], branch_id="BR-001")
    a2 = schema.Assumption.from_dict(a.to_dict())
    assert a2 == a


# --- Enum coverage ---

def test_evidence_level_ordering():
    assert schema.EvidenceLevel["L3"] < schema.EvidenceLevel["L4"]
    assert schema.EvidenceLevel["L4"] < schema.EvidenceLevel["L6"]
    assert not (schema.EvidenceLevel["L5"] < schema.EvidenceLevel["L1"])


def test_enum_values():
    assert {m.name for m in schema.Layer} == {"root", "strategy", "opportunity", "concept", "solution", "feature"}
    assert {m.name for m in schema.Category} == {"consumer", "commercial", "technical", "distribution", "regulatory"}
    assert [m.value for m in schema.Impact] == ["low", "medium", "high"]
    assert [m.value for m in schema.Uncertainty] == ["low", "medium", "high"]
    assert [m.value for m in schema.EvidenceLevel] == ["L1", "L2", "L3", "L4", "L5", "L6"]
    assert [m.value for m in schema.AssumptionValidationStatus] == ["untested", "testing", "supported", "falsified", "inconclusive"]
    assert [m.value for m in schema.AssumptionStatus] == ["active", "killed", "merged"]
    assert {m.value for m in schema.ArtifactKind} == {"charter", "directional-hypothesis", "strategy-statement", "strategy",
                                                      "opportunity", "idea-pool",
                                                      "concept-portfolio", "solution",
                                                      "investment-narrative", "experiment", "research", "insights",
                                                      "initial-assessment"}
    assert [m.value for m in schema.ArtifactDocumentStatus] == ["draft", "final", "superseded"]
    assert [m.value for m in schema.ArtifactValidationStatus] == ["unvalidated", "in-review", "validated", "invalidated"]
    assert [m.value for m in schema.GateExit] == ["go", "conditional-go", "recycle", "pivot", "kill"]


def test_strategy_statement_artifact_kind_round_trips():
    meta = schema.ArtifactMeta.from_dict({
        "artifact_id": "ART-006",
        "kind": "strategy-statement",
        "stage": "define",
        "revision": 1,
        "document_status": "draft",
        "validation_status": "unvalidated",
    })
    assert meta.kind is schema.ArtifactKind.strategy_statement


# --- Invariant branches ---

def test_achilles_validated_at_L4_ok():
    a = schema.Assumption(id="A-1", statement="x", layer="concept", category="consumer",
                          impact="high", uncertainty="high", evidence_level="L4",
                          validation_status="supported", status="active", evidence_refs=["evidence:E-001@1"],
                          derived_from=[], affects=[], branch_id="BR-001")
    a.check_invariants()


def test_achilles_validated_at_L5_ok():
    a = schema.Assumption(id="A-1", statement="x", layer="concept", category="consumer",
                          impact="high", uncertainty="high", evidence_level="L5",
                          validation_status="supported", status="active", evidence_refs=["evidence:E-001@1"],
                          derived_from=[], affects=[], branch_id="BR-001")
    a.check_invariants()


def test_not_achilles_validated_low_evidence_ok():
    a = schema.Assumption(id="A-1", statement="x", layer="concept", category="consumer",
                          impact="low", uncertainty="high", evidence_level="L1",
                          validation_status="supported", status="active", evidence_refs=["evidence:E-001@1"],
                          derived_from=[], affects=[], branch_id="BR-001")
    a.check_invariants()


@pytest.mark.parametrize("evidence_refs", [[], ["evidence:E-001"], ["knowledge:K-001@1"], ["RM-001"]])
def test_supported_assumption_requires_exact_evidence_revision(evidence_refs):
    assumption = schema.Assumption(
        id="A-1",
        statement="x",
        layer="root",
        category="consumer",
        impact="low",
        uncertainty="low",
        evidence_level="L1",
        validation_status="supported",
        status="active",
        evidence_refs=evidence_refs,
        derived_from=[],
        affects=[],
        branch_id="BR-001",
    )

    with pytest.raises(ValidationError, match="exact Evidence revision"):
        assumption.check_invariants()


def test_evidence_ref_resolves_only_current_active_record_on_same_branch(tmp_path):
    state_dir = tmp_path / "_bewater"
    state_dir.mkdir()
    (state_dir / "evidence.yaml").write_text(
        """schema_version: 1
revision: 3
branch_id: BR-001
next_evidence_id: 2
evidence:
  - id: E-001
    record_revision: 2
    validity: active
"""
    )

    assert evidence.ref_resolves(tmp_path, "evidence:E-001@2", branch_id="BR-001")
    assert not evidence.ref_resolves(tmp_path, "evidence:E-001@1", branch_id="BR-001")
    assert not evidence.ref_resolves(tmp_path, "evidence:E-001@2", branch_id="BR-002")
    assert not evidence.ref_resolves(tmp_path, "knowledge:K-001@2", branch_id="BR-001")


def test_invalidated_evidence_ref_does_not_resolve(tmp_path):
    state_dir = tmp_path / "_bewater"
    state_dir.mkdir()
    (state_dir / "evidence.yaml").write_text(
        """schema_version: 1
revision: 2
branch_id: BR-001
next_evidence_id: 2
evidence:
  - id: E-001
    record_revision: 1
    validity: invalidated
"""
    )

    assert not evidence.ref_resolves(tmp_path, "evidence:E-001@1", branch_id="BR-001")


def test_malformed_evidence_state_fails_closed(tmp_path):
    state_dir = tmp_path / "_bewater"
    state_dir.mkdir()
    (state_dir / "evidence.yaml").write_text("evidence: [")

    assert not evidence.ref_resolves(tmp_path, "evidence:E-001@1", branch_id="BR-001")


def test_malformed_evidence_record_fails_closed(tmp_path):
    state_dir = tmp_path / "_bewater"
    state_dir.mkdir()
    (state_dir / "evidence.yaml").write_text(
        """branch_id: BR-001
evidence:
  - id: E-001
    record_revision: not-a-number
    validity: active
"""
    )

    assert not evidence.ref_resolves(tmp_path, "evidence:E-001@1", branch_id="BR-001")


def test_is_achilles_heel_false_when_low_impact():
    a = schema.Assumption(id="A-1", statement="x", layer="concept", category="consumer",
                          impact="low", uncertainty="high", evidence_level="L1",
                          validation_status="untested", status="active", evidence_refs=[],
                          derived_from=[], affects=[], branch_id="BR-001")
    assert a.is_achilles_heel is False


def test_achilles_heel_not_in_to_dict():
    a = schema.Assumption(id="A-1", statement="x", layer="root", category="consumer",
                          impact="low", uncertainty="medium", evidence_level="L1",
                          validation_status="untested", status="active", evidence_refs=[],
                          derived_from=[], affects=[], branch_id="BR-001")
    d = a.to_dict()
    assert "is_achilles_heel" not in d


def test_from_dict_accepts_enum_objects():
    raw = {"id": "A-2", "statement": "y", "layer": schema.Layer.strategy,
           "category": schema.Category.technical, "impact": schema.Impact.high,
           "uncertainty": schema.Uncertainty.high, "evidence_level": schema.EvidenceLevel.L2,
           "validation_status": schema.AssumptionValidationStatus.untested,
           "status": schema.AssumptionStatus.active, "evidence_refs": [],
           "derived_from": ["A-1"], "affects": ["A-3"], "branch_id": "BR-002"}
    a = schema.Assumption.from_dict(raw)
    assert a.layer == schema.Layer.strategy
    assert a.derived_from == ["A-1"]
    assert a.to_dict()["layer"] == "strategy"


# --- Ledger ---

def test_ledger_round_trip():
    a1 = schema.Assumption(id="A-1", statement="x", layer="root", category="consumer",
                           impact="low", uncertainty="medium", evidence_level="L1",
                           validation_status="untested", status="active", evidence_refs=[],
                           derived_from=[], affects=[], branch_id="BR-001")
    a2 = schema.Assumption(id="A-2", statement="y", layer="strategy", category="technical",
                           impact="high", uncertainty="high", evidence_level="L4",
                           validation_status="supported", status="active", evidence_refs=["evidence:E-001@1"],
                           derived_from=["A-1"], affects=[], branch_id="BR-002")
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


def test_ledger_rejects_superseded_list_shape():
    a1_dict = {"id": "A-1", "statement": "x", "layer": "root", "category": "consumer",
               "impact": "low", "uncertainty": "medium", "evidence_level": "L1",
               "validation_status": "untested", "status": "active", "evidence_refs": [],
               "derived_from": [], "affects": [], "branch_id": "BR-001"}
    with pytest.raises(TypeError, match="ID-keyed mapping"):
        schema.Ledger.from_dict({"assumptions": [a1_dict]})


# --- ArtifactMeta ---

def test_artifact_meta_round_trip():
    am = schema.ArtifactMeta(
        artifact_id="ART-001", kind="charter", stage="immersion", revision=1,
        document_status="final", validation_status="validated", branch_id="BR-001",
        locked=True, signoffs=[{"who": "ceo"}],
        dual_sided={"left": "a", "right": "b"}, derived_from=[],
        last_validated_against=[{"id": "charter", "hash": "abc123"}],
        created_at="2026-01-01", updated_at="2026-01-02",
        extra={"hash": "abc123"},
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


def test_assumption_schema_has_no_noncanonical_source_solution_ref():
    assumption = schema.Assumption(
        id="A-001",
        statement="Solution risk",
        layer="solution",
        category="consumer",
        impact="high",
        uncertainty="high",
        evidence_level="L4",
        validation_status="supported",
        status="active",
        evidence_refs=["evidence:E-001"],
        derived_from=["artifact:ART-020@2"],
        branch_id="BR-001",
    )
    assert "source_solution_ref" not in assumption.to_dict()


# --- GateRecord ---

def test_gate_record_round_trip():
    gr = schema.GateRecord(
        gate="charter", attempt_id="charter/1", position=1,
        subject_refs=["charter"], decision_date="2026-01-02",
        decision_maker="ceo", exit="go", conditions=[],
    )
    gr2 = schema.GateRecord.from_dict(gr.to_dict())
    assert gr2 == gr
