import pytest
from pathlib import Path

from bw import validate, ledger_ops, io, schema, paths


# --- helpers ---

def _add(root, **over):
    base = dict(statement="s", layer="concept", category="consumer", impact="low",
                uncertainty="low", evidence_level="L1", validation_status="open",
                evidence_ref="", derived_from=[], affects=[], branch="sol-01")
    base.update(over)
    return ledger_ops.add(root, base)


def _full_dual_sided():
    return {
        "money": {"commercial_value_proposition": "cvp", "leverageable_assets": "assets"},
        "magic": {"consumer_value_proposition": "cvp2", "consumer_target": "target"},
        "tension": "",
    }


def _write_artifact(root, artifact_id, kind, status="final", dual_sided=None,
                    derived_from=None, path_name="art.md"):
    meta = schema.ArtifactMeta(
        artifact_id=artifact_id, kind=kind, stage="shape", status=status,
        hash="x", locked=False, validated_by="", validated_at="", signoffs=[],
        dual_sided=dual_sided, derived_from=derived_from or [],
        last_validated_against=[], created_at="d", updated_at="d")
    p = paths.artifacts_dir(root) / "define" / path_name
    p.parent.mkdir(parents=True, exist_ok=True)
    io.write_artifact(p, meta, "body")
    return p


# --- clean ---

def _add_raw(root, aid, **over):
    """Write an assumption directly, bypassing add()'s id/invariant guards.
    Lets cycle tests build lineage the production write path forbids."""
    fields = dict(statement="s", layer="concept", category="consumer", impact="low",
                  uncertainty="low", evidence_level="L1", validation_status="open",
                  status="active", evidence_ref="", derived_from=[], affects=[],
                  branch="sol-01")
    fields.update(over)
    fields["id"] = aid
    assumption = schema.Assumption.from_dict(fields)
    ledger = io.load_ledger(root)
    ledger.assumptions.append(assumption)
    io.save_ledger(root, ledger)
    return assumption


def test_validate_passes_clean(tmp_project):
    _add(tmp_project)
    assert validate.validate_all(tmp_project) == []


def test_validate_returns_list_of_issues(tmp_project):
    _add(tmp_project, derived_from=["GONE"])
    issues = validate.validate_all(tmp_project)
    assert isinstance(issues, list)
    for i in issues:
        assert hasattr(i, "scope") and hasattr(i, "kind") and hasattr(i, "message")


# --- invariant violations ---

def test_validate_flags_invariant_violation(tmp_project):
    # achilles + validated + L3 < L4, written directly to bypass add's guard.
    bad = schema.Assumption(
        id="A-001", statement="s", layer="concept", category="consumer",
        impact="high", uncertainty="high", evidence_level="L3",
        validation_status="validated", status="active", evidence_ref="",
    )
    ledger = io.load_ledger(tmp_project)
    ledger.assumptions.append(bad)
    io.save_ledger(tmp_project, ledger)

    issues = validate.validate_all(tmp_project)
    inv = [i for i in issues if i.kind == "invariant-violation"]
    assert len(inv) == 1
    assert inv[0].scope == "A-001"
    assert "l4" in inv[0].message.lower() or "achilles" in inv[0].message.lower()


# --- dangling refs ---

def test_validate_flags_dangling_ref_in_derived_from(tmp_project):
    _add(tmp_project, derived_from=["GONE"])
    issues = validate.validate_all(tmp_project)
    assert any(i.kind == "dangling-ref" and i.scope == "A-001" for i in issues)
    assert "GONE" in [i.message for i in issues if i.kind == "dangling-ref"][0]


def test_validate_flags_dangling_ref_in_affects(tmp_project):
    _add(tmp_project, affects=["GHOST"])
    issues = validate.validate_all(tmp_project)
    assert any(i.kind == "dangling-ref" for i in issues)


def test_validate_ref_resolves_to_artifact_id(tmp_project):
    # derived_from pointing at an existing artifact_id is NOT a dangling ref.
    _write_artifact(tmp_project, "ART-9", "solution")
    _add(tmp_project, derived_from=["ART-9"])
    issues = validate.validate_all(tmp_project)
    assert not any(i.kind == "dangling-ref" for i in issues)


# --- cycles ---

def test_validate_flags_cycle(tmp_project):
    _add_raw(tmp_project, "A-001", statement="a", derived_from=["A-002"])
    _add_raw(tmp_project, "A-002", statement="b", derived_from=["A-001"])
    issues = validate.validate_all(tmp_project)
    cyc = [i for i in issues if i.kind == "cycle"]
    assert len(cyc) >= 1


def test_validate_cycle_dedup(tmp_project):
    # Two assumptions in the same cycle should yield ONE cycle issue, not N.
    _add_raw(tmp_project, "A-001", statement="a", derived_from=["A-002"])
    _add_raw(tmp_project, "A-002", statement="b", derived_from=["A-001"])
    cyc = [i for i in validate.validate_all(tmp_project) if i.kind == "cycle"]
    assert len(cyc) == 1


# --- single-sided ---

@pytest.mark.parametrize("kind", ["charter", "directional-hypothesis", "concept", "solution"])
def test_validate_flags_single_sided(tmp_project, kind):
    dual = _full_dual_sided()
    dual["money"]["commercial_value_proposition"] = ""  # one empty
    _write_artifact(tmp_project, "ART-1", kind, dual_sided=dual)
    issues = validate.validate_all(tmp_project)
    assert any(i.kind == "single-sided" and i.scope == "ART-1" for i in issues)


def test_validate_single_sided_reports_each_empty_element(tmp_project):
    dual = _full_dual_sided()
    dual["money"]["commercial_value_proposition"] = ""
    dual["magic"]["consumer_target"] = ""
    _write_artifact(tmp_project, "ART-1", "solution", dual_sided=dual)
    issues = [i for i in validate.validate_all(tmp_project)
              if i.kind == "single-sided" and i.scope == "ART-1"]
    assert len(issues) == 2


def test_validate_full_dual_sided_is_clean(tmp_project):
    _write_artifact(tmp_project, "ART-1", "solution", dual_sided=_full_dual_sided())
    issues = validate.validate_all(tmp_project)
    assert not any(i.kind == "single-sided" for i in issues)


def test_validate_non_dual_sided_kind_not_checked(tmp_project):
    # research/insights/etc don't need dual_sided; absent block is fine.
    _write_artifact(tmp_project, "ART-1", "research", dual_sided=None)
    issues = validate.validate_all(tmp_project)
    assert not any(i.kind == "single-sided" for i in issues)


# --- missing-final ---

def test_validate_flags_missing_final_dependency(tmp_project):
    # A-final depends on B-draft: B is referenced but not final.
    _write_artifact(tmp_project, "A", "solution", status="final",
                    derived_from=["B"], path_name="a.md")
    _write_artifact(tmp_project, "B", "solution", status="draft",
                    derived_from=[], path_name="b.md")
    issues = validate.validate_all(tmp_project)
    assert any(i.kind == "missing-final" and i.scope == "B" for i in issues)


def test_validate_final_dependency_clean(tmp_project):
    _write_artifact(tmp_project, "A", "solution", status="final",
                    derived_from=["B"], path_name="a.md")
    _write_artifact(tmp_project, "B", "solution", status="final",
                    derived_from=[], path_name="b.md")
    issues = validate.validate_all(tmp_project)
    assert not any(i.kind == "missing-final" for i in issues)


# --- malformed frontmatter ---

def test_validate_catches_malformed_frontmatter(tmp_project):
    p = paths.artifacts_dir(tmp_project) / "define" / "broken.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("---\nartifact_id: ART-X\nkind: solution\nno closing fence\n")
    issues = validate.validate_all(tmp_project)
    assert any(i.kind == "malformed-frontmatter" for i in issues)
    # crucially: it did not crash


def test_validate_malformed_frontmatter_does_not_abort_rest(tmp_project):
    # A malformed artifact should not stop validation of the ledger.
    p = paths.artifacts_dir(tmp_project) / "define" / "broken.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("---\nartifact_id: ART-X\nkind: solution\nno closing fence\n")
    _add(tmp_project, derived_from=["GONE"])  # separate dangling-ref issue
    issues = validate.validate_all(tmp_project)
    kinds = {i.kind for i in issues}
    assert "malformed-frontmatter" in kinds
    assert "dangling-ref" in kinds
