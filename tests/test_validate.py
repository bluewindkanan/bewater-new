import pytest
from pathlib import Path

from bw import validate, ledger_ops, io, schema, paths


# --- helpers ---

def _add(root, **over):
    base = dict(statement="s", layer="root", category="consumer", impact="low",
                uncertainty="low", evidence_level="L1", validation_status="untested",
                evidence_refs=[], derived_from=[], affects=[], branch_id="BR-001")
    base.update(over)
    return ledger_ops.add(root, base)


def _full_dual_sided():
    return {
        "money": {"commercial_value_proposition": "cvp", "leverageable_assets": "assets"},
        "magic": {"consumer_value_proposition": "cvp2", "consumer_target": "target"},
        "tension": "",
    }


def _write_artifact(root, artifact_id, kind, status="final", dual_sided=None,
                    derived_from=None, path_name="art.md", signoffs=None):
    meta = schema.ArtifactMeta(
        artifact_id=artifact_id, kind=kind, stage="shape", revision=1,
        document_status=status, validation_status="unvalidated",
        locked=False, signoffs=signoffs or [],
        dual_sided=dual_sided or None, derived_from=derived_from or [],
        last_validated_against=[], created_at="d", updated_at="d")
    p = paths.output_dir(root) / path_name
    p.parent.mkdir(parents=True, exist_ok=True)
    io.write_artifact(p, meta, "body")
    return p


def _add_raw(root, aid, **over):
    """Write an assumption directly, bypassing add()'s id/invariant guards."""
    fields = dict(statement="s", layer="root", category="consumer", impact="low",
                  uncertainty="low", evidence_level="L1", validation_status="untested",
                  status="active", evidence_refs=[], derived_from=[], affects=[],
                  branch_id="BR-001")
    fields.update(over)
    fields["id"] = aid
    assumption = schema.Assumption.from_dict(fields)
    ledger = io.load_ledger(root)
    ledger.assumptions[aid] = assumption
    io.save_ledger(root, ledger)
    return assumption


# --- clean ---

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
    bad = schema.Assumption(
        id="A-001", statement="s", layer="concept", category="consumer",
        impact="high", uncertainty="high", evidence_level="L3",
        validation_status="supported", status="active", evidence_refs=[],
    )
    ledger = io.load_ledger(tmp_project)
    ledger.assumptions[bad.id] = bad
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


def test_validate_rejects_bare_artifact_id_ref(tmp_project):
    _write_artifact(tmp_project, "ART-9", "research")
    _add(tmp_project, derived_from=["ART-9"])
    issues = validate.validate_all(tmp_project)
    assert any(i.kind == "dangling-ref" for i in issues)


def test_validate_exact_artifact_revision_ref_resolves(tmp_project):
    _write_artifact(tmp_project, "ART-9", "research")
    _add(tmp_project, derived_from=["artifact:ART-9@1"])
    issues = validate.validate_all(tmp_project)
    assert not any(i.kind == "dangling-ref" for i in issues)


@pytest.mark.parametrize("ref", ["artifact:ART-9@2", "artifact:ART-404@1"])
def test_validate_rejects_stale_or_missing_artifact_revision_ref(tmp_project, ref):
    _write_artifact(tmp_project, "ART-9", "research")
    _add(tmp_project, derived_from=[ref])
    assert any(i.kind == "dangling-ref" for i in validate.validate_all(tmp_project))


def test_validate_rejects_bare_assumption_ref(tmp_project):
    _add_raw(tmp_project, "A-001")
    _add_raw(tmp_project, "A-002", derived_from=["A-001"])
    assert any(i.kind == "dangling-ref" for i in validate.validate_all(tmp_project))


def _write_lineage_subject(root, artifact_id, kind, **extra):
    meta = schema.ArtifactMeta(
        artifact_id=artifact_id,
        kind=kind,
        stage="ideate" if kind == "concept-portfolio" else "shape",
        revision=1,
        document_status="final",
        validation_status="unvalidated",
        branch_id="BR-001",
        extra=extra,
    )
    p = paths.output_dir(root) / f"{artifact_id}-r1-{kind}.md"
    io.write_artifact(p, meta, "subject")


@pytest.mark.parametrize(
    "overrides",
    [
        {"source_concept_id": None, "derived_from": ["artifact:ART-012@1"]},
        {"source_concept_id": "CI-001", "derived_from": []},
        {"source_concept_id": "CI-001", "derived_from": ["artifact:ART-099@1"]},
    ],
)
def test_validate_concept_assumption_requires_exact_portfolio_and_local_concept(tmp_project, overrides):
    _write_lineage_subject(
        tmp_project,
        "ART-012",
        "concept-portfolio",
        concepts=[{"id": "CI-001"}],
        exit={"selected_concept_ids": ["CI-001"]},
    )
    _add_raw(tmp_project, "A-001", layer="concept", **overrides)
    assert any(issue.kind == "assumption-lineage" for issue in validate.validate_all(tmp_project))


@pytest.mark.parametrize("derived_from", [[], ["artifact:ART-099@1"]])
def test_validate_solution_assumption_requires_exact_solution_revision(tmp_project, derived_from):
    _write_lineage_subject(tmp_project, "ART-020", "solution")
    _add_raw(tmp_project, "A-001", layer="solution", derived_from=derived_from)
    assert any(issue.kind == "assumption-lineage" for issue in validate.validate_all(tmp_project))


# --- cycles ---

def test_validate_flags_cycle(tmp_project):
    _add_raw(tmp_project, "A-001", statement="a", derived_from=["assumption:A-002@1"])
    _add_raw(tmp_project, "A-002", statement="b", derived_from=["assumption:A-001@1"])
    issues = validate.validate_all(tmp_project)
    cyc = [i for i in issues if i.kind == "cycle"]
    assert len(cyc) >= 1


def test_validate_cycle_dedup(tmp_project):
    _add_raw(tmp_project, "A-001", statement="a", derived_from=["assumption:A-002@1"])
    _add_raw(tmp_project, "A-002", statement="b", derived_from=["assumption:A-001@1"])
    cyc = [i for i in validate.validate_all(tmp_project) if i.kind == "cycle"]
    assert len(cyc) == 1


def test_validate_flags_affects_only_cycle(tmp_project):
    _add_raw(tmp_project, "A-001", statement="a", affects=["assumption:A-002@1"])
    _add_raw(tmp_project, "A-002", statement="b", affects=["assumption:A-001@1"])
    issues = validate.validate_all(tmp_project)
    cyc = [i for i in issues if i.kind == "cycle"]
    assert len(cyc) == 1


# --- single-sided ---

@pytest.mark.parametrize("kind", ["charter", "directional-hypothesis"])
def test_validate_flags_single_sided(tmp_project, kind):
    dual = _full_dual_sided()
    dual["money"]["commercial_value_proposition"] = ""
    _write_artifact(tmp_project, "ART-1", kind, dual_sided=dual)
    issues = validate.validate_all(tmp_project)
    assert any(i.kind == "single-sided" and i.scope == "ART-1" for i in issues)


def test_validate_single_sided_reports_each_empty_element(tmp_project):
    dual = _full_dual_sided()
    dual["money"]["commercial_value_proposition"] = ""
    dual["magic"]["consumer_target"] = ""
    _write_artifact(tmp_project, "ART-1", "directional-hypothesis", dual_sided=dual)
    issues = [i for i in validate.validate_all(tmp_project)
              if i.kind == "single-sided" and i.scope == "ART-1"]
    assert len(issues) == 2


def test_validate_full_dual_sided_is_clean(tmp_project):
    _write_artifact(tmp_project, "ART-1", "charter", dual_sided=_full_dual_sided())
    issues = validate.validate_all(tmp_project)
    assert not any(i.kind == "single-sided" for i in issues)


def test_validate_non_dual_sided_kind_not_checked(tmp_project):
    _write_artifact(tmp_project, "ART-1", "research", dual_sided=None)
    issues = validate.validate_all(tmp_project)
    assert not any(i.kind == "single-sided" for i in issues)


# --- F/P/E/T signoff ---

def test_validate_final_insights_require_fpet_signoff(tmp_project):
    _write_artifact(tmp_project, "ART-1", "insights", signoffs=[])
    issues = validate.validate_all(tmp_project)
    assert any(i.kind == "fpet-signoff" and i.scope == "ART-1" for i in issues)


def test_validate_accepts_structured_fpet_signoff(tmp_project):
    _write_artifact(tmp_project, "ART-1", "insights", signoffs=[{"type": "fpet"}])
    issues = validate.validate_all(tmp_project)
    assert not any(i.kind == "fpet-signoff" for i in issues)


# --- missing-final ---

def test_validate_flags_missing_final_dependency(tmp_project):
    _write_artifact(tmp_project, "A", "solution", status="final",
                    derived_from=["artifact:B@1"], path_name="a.md")
    _write_artifact(tmp_project, "B", "solution", status="draft",
                    derived_from=[], path_name="b.md")
    issues = validate.validate_all(tmp_project)
    assert any(i.kind == "missing-final" and i.scope == "B" for i in issues)


def test_validate_final_dependency_clean(tmp_project):
    _write_artifact(tmp_project, "A", "solution", status="final",
                    derived_from=["artifact:B@1"], path_name="a.md")
    _write_artifact(tmp_project, "B", "solution", status="final",
                    derived_from=[], path_name="b.md")
    issues = validate.validate_all(tmp_project)
    assert not any(i.kind == "missing-final" for i in issues)


# --- malformed frontmatter ---

def test_validate_catches_malformed_frontmatter(tmp_project):
    p = paths.output_dir(tmp_project) / "broken.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("---\nartifact_id: ART-X\nkind: solution\nno closing fence\n")
    issues = validate.validate_all(tmp_project)
    assert any(i.kind == "malformed-frontmatter" for i in issues)


def test_validate_malformed_frontmatter_does_not_abort_rest(tmp_project):
    p = paths.output_dir(tmp_project) / "broken.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("---\nartifact_id: ART-X\nkind: solution\nno closing fence\n")
    _add(tmp_project, derived_from=["GONE"])
    issues = validate.validate_all(tmp_project)
    kinds = {i.kind for i in issues}
    assert "malformed-frontmatter" in kinds
    assert "dangling-ref" in kinds


# --- concept lifecycle (validate_all wiring) ---

def test_validate_flags_seed_pool_underfilled_from_file(tmp_project):
    seeds = "".join(
        f"      - id: CS-{i:03d}\n        idea: Raw possibility {i}.\n        source_insight_refs: [artifact:ART-004@1]\n"
        for i in range(1, 6)
    )
    fm = ("artifact_id: ART-008\nrevision: 1\nkind: idea-pool\nstage: ideate\n"
          "branch_id: BR-001\ndocument_status: draft\nvalidation_status: unvalidated\n"
          "input_snapshot:\n  strategy_ref: artifact:ART-006@1\n  opportunity_ref: artifact:ART-007@1\n"
          "opportunity_areas:\n  - opportunity_area_id: OA-001\n    seeds:\n" + seeds +
          "    shortlist:\n      recommended: []\n      confirmed: []\n")
    p = paths.output_dir(tmp_project) / "ART-008-r1-idea-pool.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"---\n{fm}---\nbody\n")
    issues = validate.validate_all(tmp_project)
    assert any(i.kind == "seed-count" and i.scope == "ART-008" for i in issues)


def test_validate_idea_pool_is_not_a_top_level_dual_sided_kind(tmp_project):
    dual = _full_dual_sided()
    dual["money"]["commercial_value_proposition"] = ""
    meta = schema.ArtifactMeta(
        artifact_id="ART-1", kind="idea-pool", stage="ideate", revision=1,
        document_status="final", validation_status="unvalidated", dual_sided=dual,
        derived_from=[], last_validated_against=[],
        created_at="d", updated_at="d")
    p = paths.output_dir(tmp_project) / "pool.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    io.write_artifact(p, meta, "body")
    issues = validate.validate_all(tmp_project)
    assert not any(i.kind == "single-sided" for i in issues)
