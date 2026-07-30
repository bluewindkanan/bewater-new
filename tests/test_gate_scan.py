from pathlib import Path

from bw import gate_scan, io, paths, schema

_DS = {
    "money": {"commercial_value_proposition": "m", "leverageable_assets": "l"},
    "magic": {"consumer_value_proposition": "c", "consumer_target": "t"},
    "tension": "",
}


def _mk(root, rel, kind, stage, status="final", dual=None, locked=False, signoffs=None):
    rel_path = Path(rel)
    # Strip a leading "artifacts" so the file lands under _bewater-output/.
    if rel_path.parts and rel_path.parts[0] == "artifacts":
        rel_path = Path(*rel_path.parts[1:])
    p = paths.output_dir(root) / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    meta = schema.ArtifactMeta(
        artifact_id=rel_path.stem,
        kind=kind,
        stage=stage,
        status=status,
        hash="x",
        locked=locked,
        validated_by="",
        validated_at="",
        signoffs=signoffs or [],
        dual_sided=dual,
        derived_from=[],
        last_validated_against=[],
        created_at="d",
        updated_at="d",
    )
    io.write_artifact(p, meta, "body")


def _complete(root, subject=None, oas=2, hyps=2, achilles=True):
    """Build a fully-G1-complete project (every mechanical criterion green)."""
    _mk(root, "artifacts/immersion/charter.md", "charter", "immersion", dual=_DS)
    _mk(
        root,
        "artifacts/discover/insights.md",
        "insights",
        "discover",
        signoffs=[{"who": "u", "role": "lead", "what": "F/P/E/T", "at": "d"}],
    )
    for i in range(1, hyps + 1):
        _mk(
            root,
            f"artifacts/discover/hyp{i}.md",
            "directional-hypothesis",
            "discover",
            dual=_DS,
        )
    _mk(root, "artifacts/define/strategy.md", "strategy", "define", locked=True)
    for i in range(1, oas + 1):
        _mk(
            root,
            f"artifacts/define/oa{i}.md",
            "opportunity-area",
            "define",
        )
    from bw import ledger_ops

    payload = dict(
        statement="ach",
        layer="concept",
        category="consumer",
        impact="high" if achilles else "low",
        uncertainty="high" if achilles else "low",
        evidence_level="L1",
        validation_status="open",
        evidence_ref="",
        derived_from=[],
        affects=[],
        branch="sol-01",
    )
    ledger_ops.add(root, payload)
    return subject


# --- result shape ---------------------------------------------------------

def test_criterion_and_result_dataclasses():
    c = gate_scan.Criterion(name="x", passed=True, blocking=False, note=None)
    assert c.name == "x" and c.passed is True and c.blocking is False and c.note is None


# --- thin / blocked -------------------------------------------------------

def test_g1_blocks_when_thin(tmp_project):
    r = gate_scan.scan(tmp_project, "G1", subject=None)
    assert "go" not in r.exit_allowed
    assert any(
        c.name == "missing-artifact" and c.blocking and not c.passed
        for c in r.criteria
    )
    assert set(r.exit_allowed) == {"conditional-go", "recycle", "pivot", "kill"}


# --- complete -> go -------------------------------------------------------

def test_g1_passes_when_complete(tmp_project):
    subj = _complete(tmp_project, subject="sol-01")
    r = gate_scan.scan(tmp_project, "G1", subject=subj)
    assert "go" in r.exit_allowed, [c.name for c in r.criteria if not c.passed]
    assert set(r.exit_allowed) == {
        "go",
        "conditional-go",
        "recycle",
        "pivot",
        "kill",
    }
    notes = [(c.name, c.note) for c in r.criteria]
    assert any(n == "requires human judgment" for _, n in notes)


# --- charter criterion ----------------------------------------------------

def test_charter_single_sided_blocks(tmp_project):
    partial = {
        "money": {"commercial_value_proposition": "m", "leverageable_assets": "l"},
        "magic": {"consumer_value_proposition": "", "consumer_target": "t"},
    }
    _mk(tmp_project, "artifacts/immersion/charter.md", "charter", "immersion", dual=partial)
    r = gate_scan.scan(tmp_project, "G1", subject=None)
    charter = next(c for c in r.criteria if c.name == "single-sided")
    assert not charter.passed and charter.blocking
    assert "go" not in r.exit_allowed


def test_charter_not_final_blocks(tmp_project):
    _mk(
        tmp_project,
        "artifacts/immersion/charter.md",
        "charter",
        "immersion",
        status="draft",
        dual=_DS,
    )
    r = gate_scan.scan(tmp_project, "G1", subject=None)
    charter = next(c for c in r.criteria if c.name == "charter")
    assert not charter.passed and charter.blocking


# --- directional hypotheses ----------------------------------------------

def test_too_few_hypotheses_blocks(tmp_project):
    _complete(tmp_project, hyps=1)
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    hyp = next(c for c in r.criteria if c.name == "directional-hypotheses")
    assert not hyp.passed and hyp.blocking
    assert "go" not in r.exit_allowed


def test_too_many_hypotheses_blocks(tmp_project):
    _complete(tmp_project, hyps=6)
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    hyp = next(c for c in r.criteria if c.name == "directional-hypotheses")
    assert not hyp.passed and hyp.blocking


def test_hypothesis_single_sided_blocks(tmp_project):
    _mk(tmp_project, "artifacts/immersion/charter.md", "charter", "immersion", dual=_DS)
    _mk(
        tmp_project,
        "artifacts/discover/insights.md",
        "insights",
        "discover",
        signoffs=[{"who": "u", "role": "lead", "what": "F/P/E/T", "at": "d"}],
    )
    _mk(tmp_project, "artifacts/discover/hyp1.md", "directional-hypothesis", "discover", dual=_DS)
    partial = {"money": {"commercial_value_proposition": "m", "leverageable_assets": "l"},
               "magic": {"consumer_value_proposition": "", "consumer_target": "t"}}
    _mk(tmp_project, "artifacts/discover/hyp2.md", "directional-hypothesis", "discover", dual=partial)
    _mk(tmp_project, "artifacts/define/strategy.md", "strategy", "define", locked=True)
    _mk(tmp_project, "artifacts/define/oa1.md", "opportunity-area", "define")
    _mk(tmp_project, "artifacts/define/oa2.md", "opportunity-area", "define")
    from bw import ledger_ops
    ledger_ops.add(tmp_project, dict(statement="ach", layer="concept", category="consumer",
        impact="high", uncertainty="high", evidence_level="L1", validation_status="open",
        evidence_ref="", derived_from=[], affects=[], branch="sol-01"))
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    hyp = next(c for c in r.criteria if c.name == "directional-hypotheses")
    assert not hyp.passed and hyp.blocking


# --- insights / signoff ---------------------------------------------------

def test_insights_without_signoff_blocks(tmp_project):
    _complete(tmp_project, subject="sol-01")
    _mk(tmp_project, "artifacts/discover/insights.md", "insights", "discover", signoffs=[])
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    ins = next(c for c in r.criteria if c.name == "insights")
    assert not ins.passed and ins.blocking


def test_insights_mixed_signoff_blocks(tmp_project):
    _complete(tmp_project, subject="sol-01")
    _mk(tmp_project, "artifacts/discover/insights2.md", "insights", "discover", signoffs=[])
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    ins = next(c for c in r.criteria if c.name == "insights")
    assert not ins.passed and ins.blocking
    assert "go" not in r.exit_allowed


# --- strategy -------------------------------------------------------------

def test_strategy_not_locked_blocks(tmp_project):
    _complete(tmp_project, subject="sol-01")
    _mk(tmp_project, "artifacts/define/strategy.md", "strategy", "define", locked=False)
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    strat = next(c for c in r.criteria if c.name in ("strategy", "gate-criteria-incomplete"))
    assert not strat.passed and strat.blocking


def test_strategy_missing_blocks(tmp_project):
    _complete(tmp_project, subject="sol-01")
    (paths.output_dir(tmp_project) / "define" / "strategy.md").unlink(missing_ok=False)
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    strat = next(c for c in r.criteria if c.name == "strategy")
    assert not strat.passed and strat.blocking


# --- opportunity areas ----------------------------------------------------

def test_too_few_opportunity_areas_blocks(tmp_project):
    _complete(tmp_project, subject="sol-01", oas=1)
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    oa = next(c for c in r.criteria if c.name in ("opportunity-areas", "gate-criteria-incomplete"))
    assert not oa.passed and oa.blocking


def test_too_many_opportunity_areas_blocks(tmp_project):
    _complete(tmp_project, subject="sol-01", oas=5)
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    oa = next(c for c in r.criteria if c.name == "opportunity-areas")
    assert not oa.passed and oa.blocking


# --- achilles / subject scoping ------------------------------------------

def test_no_achilles_on_subject_blocks(tmp_project):
    _complete(tmp_project, subject="sol-01", achilles=False)
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    aq = next(c for c in r.criteria if c.name == "achilles-quadrant")
    assert not aq.passed and aq.blocking


def test_achilles_scoped_to_subject_branch(tmp_project):
    _mk(tmp_project, "artifacts/immersion/charter.md", "charter", "immersion", dual=_DS)
    _mk(tmp_project, "artifacts/discover/insights.md", "insights", "discover",
        signoffs=[{"who": "u", "role": "lead", "what": "F/P/E/T", "at": "d"}])
    for i in (1, 2):
        _mk(tmp_project, f"artifacts/discover/hyp{i}.md", "directional-hypothesis", "discover", dual=_DS)
    _mk(tmp_project, "artifacts/define/strategy.md", "strategy", "define", locked=True)
    _mk(tmp_project, "artifacts/define/oa1.md", "opportunity-area", "define")
    _mk(tmp_project, "artifacts/define/oa2.md", "opportunity-area", "define")
    from bw import ledger_ops
    ledger_ops.add(tmp_project, dict(statement="ach", layer="concept", category="consumer",
        impact="high", uncertainty="high", evidence_level="L1", validation_status="open",
        evidence_ref="", derived_from=[], affects=[], branch="sol-02"))
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    aq = next(c for c in r.criteria if c.name == "achilles-quadrant")
    assert not aq.passed and aq.blocking


def test_achilles_on_subject_branch_passes(tmp_project):
    _complete(tmp_project, subject="sol-01")
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    aq = next(c for c in r.criteria if c.name == "achilles-quadrant")
    assert aq.passed


def test_excludes_killed_assumptions(tmp_project):
    from bw import ledger_ops
    a = ledger_ops.add(tmp_project, dict(statement="k", layer="concept", category="consumer",
        impact="high", uncertainty="high", evidence_level="L1", validation_status="open",
        evidence_ref="", derived_from=[], affects=[], branch="sol-01"))
    ledger_ops.update(tmp_project, a.id, {"status": "killed"})
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    aq = next(c for c in r.criteria if c.name == "achilles-quadrant")
    assert not aq.passed and aq.blocking
    assert not any("killed" in (c.note or "") for c in r.criteria)


def test_excludes_merged_assumptions(tmp_project):
    from bw import ledger_ops
    a = ledger_ops.add(tmp_project, dict(statement="k", layer="concept", category="consumer",
        impact="high", uncertainty="high", evidence_level="L1", validation_status="open",
        evidence_ref="", derived_from=[], affects=[], branch="sol-01"))
    ledger_ops.update(tmp_project, a.id, {"status": "merged"})
    r = gate_scan.scan(tmp_project, "G1", subject="sol-01")
    aq = next(c for c in r.criteria if c.name == "achilles-quadrant")
    assert not aq.passed and aq.blocking


def test_subject_none_uses_all_active(tmp_project):
    _complete(tmp_project, subject=None)
    r = gate_scan.scan(tmp_project, "G1", subject=None)
    aq = next(c for c in r.criteria if c.name == "achilles-quadrant")
    assert aq.passed
    assert aq.note and "all active" in aq.note


# --- extensibility / G2 not implemented ----------------------------------

def test_unknown_gate_raises(tmp_project):
    import pytest
    with pytest.raises(NotImplementedError):
        gate_scan.scan(tmp_project, "G2", subject=None)
