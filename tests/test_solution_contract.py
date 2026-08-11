from __future__ import annotations

from copy import deepcopy

import pytest

from bw import schema
from bw.solution_contract import render_solution_body, solution_issues


def _meta(artifact_id: str, kind: str, *, revision: int = 1, validation_status: str = "unvalidated"):
    return schema.ArtifactMeta(
        artifact_id=artifact_id,
        kind=kind,
        stage="shape" if kind == "solution" else "ideate",
        revision=revision,
        document_status="final",
        validation_status=validation_status,
        branch_id="BR-001",
    )


def _assumption(
    assumption_id: str,
    *,
    layer: str,
    source_concept_id: str | None = None,
    derived_from: list[str] | None = None,
    branch_id: str = "BR-001",
    record_revision: int = 1,
    evidence_level: str = "L4",
    validation_status: str = "supported",
    obligation_status: str = "closed",
):
    return schema.Assumption(
        id=assumption_id,
        statement=f"Risk {assumption_id}",
        layer=layer,
        category="consumer",
        impact="high",
        uncertainty="high",
        evidence_level=evidence_level,
        validation_status=validation_status,
        status="active",
        evidence_refs=[f"evidence:{assumption_id}"],
        branch_id=branch_id,
        record_revision=record_revision,
        source_concept_id=source_concept_id,
        derived_from=derived_from or [],
        l4_obligation_status=obligation_status,
    )


def _portfolio():
    fm = {
        "artifact_id": "ART-012",
        "revision": 2,
        "kind": "concept-portfolio",
        "branch_id": "BR-001",
        "concepts": [
            {
                "id": "CI-001",
                "assumption_refs": ["assumption:A-001@1"],
                "decision": "selected",
            },
            {
                "id": "CI-002",
                "assumption_refs": [],
                "decision": "selected",
            },
        ],
        "exit": {"selected_concept_ids": ["CI-001", "CI-002"]},
    }
    return _meta("ART-012", "concept-portfolio", revision=2), fm, "Portfolio"


def _solution(*, validation_status: str = "unvalidated"):
    fm = {
        "artifact_id": "ART-020",
        "revision": 1,
        "kind": "solution",
        "stage": "shape",
        "branch_id": "BR-001",
        "document_status": "final",
        "validation_status": validation_status,
        "source_concepts": {
            "portfolio_ref": "artifact:ART-012@2",
            "concept_ids": ["CI-001"],
            "path": "linear-refine",
        },
        "definition": {
            "name": "Visible Choice",
            "pithy_proposition": "Confidence before commitment",
            "what_it_is": "An evidence-led comparison service.",
            "who_its_for": "People making a high-consequence first purchase.",
            "dual_sided": {
                "money": {
                    "commercial_value_proposition": "Higher qualified conversion and retention.",
                    "leverageable_assets": "Existing product and service data.",
                },
                "magic": {
                    "consumer_value_proposition": "A confident, inspectable choice.",
                    "consumer_target": "First-time category buyers.",
                },
                "tension": "Proof without adding friction.",
                "balance_choice": "Progressive evidence disclosure.",
            },
            "dimensions": {
                "path_to_market": "Start with the existing direct channel.",
                "right_to_win": "Unique longitudinal outcome data.",
                "product_or_service_platform": "Decision-support service.",
                "source_of_business": "Opaque comparison journeys.",
                "product_or_service_design": "Guided evidence cards.",
                "enabling_technology": "Rules plus verified data.",
                "reason_to_believe": "Auditable sources and outcome feedback.",
                "branding": "Calm and evidence-led.",
                "consumer_experience": "Orient, compare, inspect, decide, review.",
            },
        },
        "how_it_works": [
            {
                "step": 1,
                "action": "State the intended outcome.",
                "consumer_benefit": "Relevant choices only.",
                "operational_benefit": "Better qualification.",
                "strategic_rationale": "Focuses the proposition.",
                "legal_regulatory_rationale": "Consent is explicit.",
                "evidence_refs": ["evidence:E-001"],
                "design_refs": ["prototype:P-001"],
            }
        ],
        "how_to_implement": [
            {
                "phase": "Pilot",
                "timing": "Quarter 1",
                "objective": "Test the critical journey.",
                "jobs_to_be_done": ["Verify source data", "Support the first cohort"],
                "capabilities_and_assets": ["Data operations", "Service team"],
                "owner": "Product lead",
                "dependencies": ["Source-data agreement"],
                "risks": ["Data freshness"],
                "open_questions": ["Best confidence threshold"],
                "pilot_and_rollout": "One market, then expand after the evidence threshold.",
            }
        ],
        "how_it_makes_money": {
            "revenue_streams": ["Qualified transaction fee"],
            "pricing_and_volume_logic": "Fee per completed qualified purchase.",
            "adoption_retention_frequency_assumptions": [
                {"assumption": "One qualified choice per customer per year", "source": "research:R-001"}
            ],
            "development_and_operating_costs": [
                {"assumption": "Pilot service team of three", "source": "estimate:FIN-001"}
            ],
            "scenarios": {
                "base": {"revenue": 100, "margin": 30, "earnings": 10, "investment": 50, "payback": "24 months"},
                "aggressive": {"revenue": 180, "margin": 65, "earnings": 35, "investment": 70, "payback": "18 months"},
            },
            "sensitivity": ["Conversion rate", "Service cost"],
            "unresolved_model_gaps": [],
        },
        "validation": {
            "consumer_desire": {"claim": "People prefer inspectable evidence.", "evidence_refs": ["evidence:E-001"]},
            "commercial_value": {"claim": "Qualification improves unit economics.", "evidence_refs": ["evidence:E-002"]},
            "feasibility_and_implementation": {"claim": "The pilot is operable.", "evidence_refs": ["evidence:E-003"]},
            "achilles_assumption_refs": ["assumption:A-001@1", "assumption:A-002@1"],
            "experiment_refs": ["experiment:EXP-001"],
            "evidence_refs": ["evidence:E-001", "evidence:E-002", "evidence:E-003"],
            "invalidated_claims": [],
        },
        "content_gaps": [],
        "applicability_exceptions": [],
    }
    meta = _meta("ART-020", "solution", validation_status=validation_status)
    if validation_status == "validated":
        meta.signoffs = [
            {
                "person": "Accountable human",
                "role": "investment lead",
                "type": "human",
                "scope": "solution-validation",
                "artifact_revision": meta.revision,
                "signed_at": "2026-08-10",
            }
        ]
    return meta, fm


def _ledger(*assumptions):
    return schema.Ledger(assumptions={item.id: item for item in assumptions})


def _valid_inputs(*, validation_status: str = "unvalidated"):
    portfolio = _portfolio()
    meta, fm = _solution(validation_status=validation_status)
    body = render_solution_body(fm)
    ledger = _ledger(
        _assumption(
            "A-001",
            layer="concept",
            source_concept_id="CI-001",
            derived_from=["artifact:ART-012@2"],
        ),
        _assumption("A-002", layer="solution", derived_from=["artifact:ART-020@1"]),
    )
    return [portfolio, (meta, fm, body)], ledger


def _kinds(artifacts, ledger):
    return {issue.kind for issue in solution_issues(artifacts, ledger)}


def test_complete_solution_contract_is_valid():
    artifacts, ledger = _valid_inputs()
    assert solution_issues(artifacts, ledger) == []


def test_solution_renderer_is_deterministic_and_uses_canonical_frontmatter():
    _, fm = _solution()
    rendered = render_solution_body(fm)
    assert render_solution_body(deepcopy(fm)) == rendered
    assert "Visible Choice" in rendered
    assert "How It Works" in rendered
    assert "How To Implement" in rendered
    assert "How It Makes Money" in rendered
    assert "Validation" in rendered


def test_invent_path_is_rejected():
    artifacts, ledger = _valid_inputs()
    artifacts[1][1]["source_concepts"]["path"] = "invent"
    assert "solution-path" in _kinds(artifacts, ledger)


@pytest.mark.parametrize(
    "block",
    ["definition", "how_it_works", "how_to_implement", "how_it_makes_money", "validation"],
)
def test_all_five_solution_blocks_are_canonical_frontmatter(block):
    artifacts, ledger = _valid_inputs()
    del artifacts[1][1][block]
    assert "solution-required-field" in _kinds(artifacts, ledger)


def test_unvalidated_omission_requires_an_exact_content_gap():
    artifacts, ledger = _valid_inputs()
    artifacts[1][1]["definition"]["dimensions"]["branding"] = ""
    assert "solution-content-gap" in _kinds(artifacts, ledger)

    artifacts[1][1]["content_gaps"] = [
        {"field_path": "definition.dimensions.branding", "reason": "Brand architecture research is pending."}
    ]
    assert "solution-content-gap" not in _kinds(artifacts, ledger)


def test_applicability_exception_requires_an_exact_path_and_rationale():
    artifacts, ledger = _valid_inputs()
    artifacts[1][1]["how_it_works"][0]["legal_regulatory_rationale"] = ""
    artifacts[1][1]["applicability_exceptions"] = [
        {"field_path": "how_it_works[0].legal_regulatory_rationale", "rationale": ""}
    ]
    assert "solution-applicability-exception" in _kinds(artifacts, ledger)


def test_markdown_projection_drift_is_detected_without_heading_parsing():
    artifacts, ledger = _valid_inputs()
    artifacts[1] = (artifacts[1][0], artifacts[1][1], "# Definition\n\n# How It Works\n\n# How To Implement\n\n# How It Makes Money\n\n# Validation\n")
    assert "solution-projection-drift" in _kinds(artifacts, ledger)


def test_achilles_snapshot_is_exact_concept_plus_solution_union():
    artifacts, ledger = _valid_inputs()
    artifacts[1][1]["validation"]["achilles_assumption_refs"] = ["assumption:A-002@1"]
    assert "solution-achilles-set" in _kinds(artifacts, ledger)


def test_stale_achilles_record_revision_is_rejected():
    artifacts, _ = _valid_inputs()
    ledger = _ledger(
        _assumption(
            "A-001",
            layer="concept",
            source_concept_id="CI-001",
            derived_from=["artifact:ART-012@2"],
            record_revision=2,
        ),
        _assumption("A-002", layer="solution", derived_from=["artifact:ART-020@1"]),
    )
    assert "solution-achilles-stale" in _kinds(artifacts, ledger)


def test_validated_solution_has_no_content_gaps():
    artifacts, ledger = _valid_inputs(validation_status="validated")
    artifacts[1][1]["content_gaps"] = [
        {"field_path": "definition.dimensions.branding", "reason": "Pending."}
    ]
    assert "solution-validated-with-gaps" in _kinds(artifacts, ledger)


def test_validated_solution_with_exact_human_signoff_is_valid():
    artifacts, ledger = _valid_inputs(validation_status="validated")
    assert solution_issues(artifacts, ledger) == []


def test_validated_solution_requires_l4_evidence_for_every_achilles_obligation():
    artifacts, _ = _valid_inputs(validation_status="validated")
    ledger = _ledger(
        _assumption(
            "A-001",
            layer="concept",
            source_concept_id="CI-001",
            derived_from=["artifact:ART-012@2"],
            evidence_level="L3",
            validation_status="untested",
            obligation_status="open",
        ),
        _assumption("A-002", layer="solution", derived_from=["artifact:ART-020@1"]),
    )
    kinds = _kinds(artifacts, ledger)
    assert "solution-achilles-unresolved" in kinds
    assert "solution-not-persuasive" in kinds


def test_solution_head_inherits_durable_obligations_from_earlier_chain_revisions():
    portfolio_r1 = _portfolio()
    portfolio_r1[0].revision = 1
    portfolio_r1[1]["revision"] = 1

    portfolio_r2 = _portfolio()
    solution_r1_meta, solution_r1_fm = _solution(validation_status="unvalidated")
    solution_r1_body = render_solution_body(solution_r1_fm)

    solution_r2_meta, solution_r2_fm = _solution(validation_status="validated")
    solution_r2_meta.revision = 2
    solution_r2_meta.signoffs[0]["artifact_revision"] = 2
    solution_r2_fm["revision"] = 2
    solution_r2_body = render_solution_body(solution_r2_fm)

    ledger = _ledger(
        _assumption(
            "A-001",
            layer="concept",
            source_concept_id="CI-001",
            derived_from=["artifact:ART-012@1"],
        ),
        _assumption("A-002", layer="solution", derived_from=["artifact:ART-020@1"]),
    )
    artifacts = [
        portfolio_r1,
        portfolio_r2,
        (solution_r1_meta, solution_r1_fm, solution_r1_body),
        (solution_r2_meta, solution_r2_fm, solution_r2_body),
    ]

    assert solution_issues(artifacts, ledger) == []


def test_solution_union_excludes_obligation_from_another_artifact_chain():
    artifacts, ledger = _valid_inputs()
    unrelated = _assumption("A-003", layer="solution", derived_from=["artifact:ART-999@1"])
    ledger.assumptions[unrelated.id] = unrelated

    kinds = _kinds(artifacts, ledger)
    assert "solution-achilles-set" not in kinds


def test_solution_inherits_only_obligations_for_its_source_concepts():
    artifacts, ledger = _valid_inputs()
    ledger.assumptions["A-003"] = _assumption(
        "A-003",
        layer="concept",
        source_concept_id="CI-002",
        derived_from=["artifact:ART-012@2"],
    )
    assert "solution-achilles-set" not in _kinds(artifacts, ledger)

    artifacts[1][1]["source_concepts"].update(path="hybridize", concept_ids=["CI-001", "CI-002"])
    artifacts[1][1]["validation"]["achilles_assumption_refs"].append("assumption:A-003@1")
    artifacts[1] = (artifacts[1][0], artifacts[1][1], render_solution_body(artifacts[1][1]))
    assert "solution-achilles-set" not in _kinds(artifacts, ledger)


def test_solution_union_excludes_same_ids_from_another_branch():
    artifacts, ledger = _valid_inputs()
    ledger.assumptions["A-003"] = _assumption(
        "A-003",
        layer="concept",
        source_concept_id="CI-001",
        derived_from=["artifact:ART-012@2"],
        branch_id="BR-002",
    )
    assert "solution-achilles-set" not in _kinds(artifacts, ledger)


@pytest.mark.parametrize(
    "signoffs",
    [
        [],
        [{"person": "AI assistant", "role": "agent", "type": "ai", "scope": "solution-validation", "artifact_revision": 1}],
        [{"person": "Accountable human", "role": "investment lead", "type": "human", "scope": "solution-validation", "artifact_revision": 2}],
    ],
)
def test_validated_solution_requires_exact_human_signoff(signoffs):
    artifacts, ledger = _valid_inputs(validation_status="validated")
    artifacts[1][0].signoffs = signoffs
    assert "solution-validation-authority" in _kinds(artifacts, ledger)
