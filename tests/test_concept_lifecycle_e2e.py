from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
import yaml
from test_concept_lifecycle import _concept, _opportunity, _pool, _portfolio, _seeds
from test_solution_contract import _assumption, _ledger, _solution

from bw import gate_scan, io, paths, schema, validate
from bw.solution_contract import render_solution_body
from bwkit import integrity

FIXTURE = Path(__file__).parent / "fixtures" / "idea-concept-solution"


def test_fixture_has_three_oas_one_pool_one_portfolio_and_two_solutions():
    data = yaml.safe_load((FIXTURE / "topology.yaml").read_text())

    assert data["opportunity"]["opportunity_area_ids"] == ["OA-001", "OA-002", "OA-003"]
    assert data["idea_pool"]["artifact_id"] == "ART-011"
    assert data["idea_pool"]["recommendation_revision"] < data["idea_pool"]["confirmation_revision"]
    assert {len(seed_ids) for seed_ids in data["idea_pool"]["groups"].values()} == {10}
    assert len({seed_id for ids in data["idea_pool"]["groups"].values() for seed_id in ids}) == 30

    concepts = data["concept_portfolio"]["concepts"]
    confirmed = set(data["idea_pool"]["confirmed_seed_ids"])
    assert {concept["source_seed_id"] for concept in concepts.values()} == confirmed
    assert len(concepts) == len(confirmed) == 15
    assert 2 <= len(data["concept_portfolio"]["selected_concept_ids"]) <= 4

    assert len(data["solutions"]) == 2
    assert {solution["path"] for solution in data["solutions"]} == {"linear-refine", "hybridize"}
    assert all(solution["unvalidated_revision"] < solution["validated_revision"] for solution in data["solutions"])
    assert data["g2"]["decision"] is None


def test_fixture_revision_chains_pass_schema_agnostic_integrity():
    payload = json.loads((FIXTURE / "integrity-input.json").read_text())
    result = integrity.check_artifacts(payload["records"])
    assert result["ok"] is True, result["errors"]
    assert result["heads"] == {
        "ART-010": 1,
        "ART-011": 2,
        "ART-012": 2,
        "ART-020": 2,
        "ART-021": 2,
    }


def _write_raw(root, meta, frontmatter, body):
    p = paths.output_dir(root) / f"{meta.artifact_id}-r{meta.revision}-{meta.kind.value}.md"
    canonical = meta.to_dict()
    canonical.update(frontmatter)
    p.write_text(f"---\n{yaml.safe_dump(canonical, sort_keys=False)}---\n{body}")


def _canonical_lifecycle():
    opportunity = deepcopy(_opportunity())
    opportunity[1]["opportunity_areas"].append(
        {
            "id": "OA-003",
            "name": "Third",
            "audience": "People",
            "opportunity": "Need three",
            "consumer_value": "Value",
            "commercial_value": "Growth",
            "source_insight_refs": ["artifact:ART-004@1"],
        }
    )

    pool_r1 = deepcopy(_pool(revision=1))
    for group in pool_r1[1]["opportunity_areas"]:
        group["shortlist"]["confirmed"] = []
    pool_r1[1]["decisions"] = []
    third_seeds = _seeds(21)
    third_ids = [seed["id"] for seed in third_seeds]
    pool_r1[1]["opportunity_areas"].append(
        {
            "opportunity_area_id": "OA-003",
            "seeds": third_seeds,
            "review": {"status": "ready", "iterations": 1, "findings": []},
            "shortlist": {
                "recommended_cuts": [
                    {
                        "seed_id": seed_id,
                        "reason": "weak-distinctiveness",
                        "rationale": f"{seed_id} repeats a stronger mechanism.",
                    }
                    for seed_id in third_ids[5:]
                ],
                "confirmed": [],
            },
        }
    )

    pool_r2 = deepcopy(_pool(revision=2))
    pool_r2[1]["opportunity_areas"].append(
        {
            "opportunity_area_id": "OA-003",
            "seeds": _seeds(21),
            "review": {"status": "ready", "iterations": 1, "findings": []},
            "shortlist": {
                "recommended_cuts": [
                    {
                        "seed_id": seed_id,
                        "reason": "weak-distinctiveness",
                        "rationale": f"{seed_id} repeats a stronger mechanism.",
                    }
                    for seed_id in third_ids[5:]
                ],
                "confirmed": third_ids[:5],
            },
        }
    )
    pool_r2[1]["decisions"].append(
        {
            "type": "confirm-shortlist",
            "opportunity_area_id": "OA-003",
            "seed_ids": third_ids[:5],
            "decided_by": {"type": "human", "name": "Accountable human", "role": "innovation lead"},
        }
    )

    source_rows = [
        *[(f"CS-{number:03d}", "OA-001") for number in range(1, 6)],
        *[(f"CS-{number:03d}", "OA-002") for number in range(11, 16)],
        *[(f"CS-{number:03d}", "OA-003") for number in range(21, 26)],
    ]
    portfolio_concepts = [
        _concept(f"CI-{index:03d}", seed_id, area_id)
        for index, (seed_id, area_id) in enumerate(source_rows, 1)
    ]
    for index, concept in enumerate(portfolio_concepts, 1):
        concept["assumption_refs"] = [f"assumption:A-{index:03d}@1"]

    portfolio_r1 = deepcopy(_portfolio(revision=1))
    portfolio_r1[1]["idea_pool_ref"] = "artifact:ART-011@2"
    portfolio_r1[1]["concepts"] = deepcopy(portfolio_concepts)
    portfolio_r1[1]["review"]["reviewed_concept_ids"] = [
        concept["id"] for concept in portfolio_r1[1]["concepts"]
    ]
    portfolio_r1[1]["decisions"] = []
    portfolio_r1[1]["exit"] = {"selected_concept_ids": []}

    portfolio_r2 = deepcopy(_portfolio(revision=2))
    portfolio_r2[1]["idea_pool_ref"] = "artifact:ART-011@2"
    portfolio_r2[1]["concepts"] = deepcopy(portfolio_concepts)
    selected_ids = ["CI-001", "CI-006", "CI-011"]
    for concept in portfolio_r2[1]["concepts"]:
        if concept["id"] in selected_ids:
            concept["decision"] = "selected"
    portfolio_r2[1]["review"]["reviewed_concept_ids"] = [
        concept["id"] for concept in portfolio_r2[1]["concepts"]
    ]
    portfolio_r2[1]["decisions"] = [
        {
            "type": "select",
            "concept_ids": selected_ids,
            "decided_by": {"name": "Accountable human", "role": "innovation lead"},
        }
    ]
    portfolio_r2[1]["exit"] = {"selected_concept_ids": selected_ids}

    artifacts = [opportunity, pool_r1, pool_r2, portfolio_r1, portfolio_r2]
    solutions = []
    for artifact_id, path, concept_ids, concept_assumptions, solution_assumption in (
        ("ART-020", "linear-refine", ["CI-001"], ["A-001"], "A-016"),
        ("ART-021", "hybridize", ["CI-006", "CI-011"], ["A-006", "A-011"], "A-017"),
    ):
        meta_r1, fm_r1 = deepcopy(_solution(validation_status="unvalidated"))
        meta_r1.artifact_id = artifact_id
        fm_r1["artifact_id"] = artifact_id
        fm_r1["source_concepts"]["path"] = path
        fm_r1["source_concepts"]["concept_ids"] = concept_ids
        fm_r1["definition"]["dimensions"]["branding"] = ""
        fm_r1["content_gaps"] = [
            {"field_path": "definition.dimensions.branding", "reason": "Brand research is pending."}
        ]
        fm_r1["validation"]["achilles_assumption_refs"] = [
            *[f"assumption:{assumption_id}@1" for assumption_id in concept_assumptions],
        ]
        solutions.append((meta_r1, fm_r1, render_solution_body(fm_r1)))

        meta_r2, fm_r2 = deepcopy(_solution(validation_status="validated"))
        meta_r2.artifact_id = artifact_id
        meta_r2.revision = 2
        meta_r2.signoffs[0]["artifact_revision"] = 2
        fm_r2["artifact_id"] = artifact_id
        fm_r2["revision"] = 2
        fm_r2["source_concepts"]["path"] = path
        fm_r2["source_concepts"]["concept_ids"] = concept_ids
        fm_r2["validation"]["achilles_assumption_refs"] = [
            *[f"assumption:{assumption_id}@1" for assumption_id in concept_assumptions],
            f"assumption:{solution_assumption}@1",
        ]
        solutions.append((meta_r2, fm_r2, render_solution_body(fm_r2)))

    concept_assumptions = [
        _assumption(
            f"A-{index:03d}",
            layer="concept",
            source_concept_id=f"CI-{index:03d}",
            derived_from=["artifact:ART-012@1"],
        )
        for index in range(1, 16)
    ]
    ledger = _ledger(
        *concept_assumptions,
        _assumption("A-016", layer="solution", derived_from=["artifact:ART-020@2"]),
        _assumption("A-017", layer="solution", derived_from=["artifact:ART-021@2"]),
    )
    return [*artifacts, *solutions], ledger


def _materialize_canonical(root, artifacts=None, ledger=None):
    if artifacts is None or ledger is None:
        artifacts, ledger = _canonical_lifecycle()
    evidence_records = []
    for index, assumption in enumerate(ledger.assumptions.values(), 1):
        if assumption.validation_status != schema.AssumptionValidationStatus.supported:
            continue
        evidence_id = f"E-{index:03d}"
        assumption.evidence_refs = [f"evidence:{evidence_id}@1"]
        evidence_records.append(
            {"id": evidence_id, "record_revision": 1, "validity": "active"}
        )
    io.save_ledger(root, ledger)
    if evidence_records:
        (root / "_bewater" / "evidence.yaml").write_text(
            yaml.safe_dump(
                {
                    "schema_version": 1,
                    "revision": 1,
                    "branch_id": "BR-001",
                    "next_evidence_id": len(evidence_records) + 1,
                    "evidence": evidence_records,
                },
                sort_keys=False,
            )
        )
    for entry in artifacts:
        if len(entry) == 2:
            meta, frontmatter = entry
            body = f"{meta.kind.value} {meta.artifact_id}@{meta.revision}"
        else:
            meta, frontmatter, body = entry
        _write_raw(root, meta, frontmatter, body)

    narrative = schema.ArtifactMeta(
        artifact_id="ART-022",
        kind="investment-narrative",
        stage="shape",
        revision=1,
        document_status="final",
        validation_status="unvalidated",
        branch_id="BR-001",
    )
    _write_raw(root, narrative, {}, "Complete six-part investment narrative")
    return artifacts, ledger


def test_fresh_canonical_fixture_validates_and_g2_stops_for_human(tmp_project):
    _materialize_canonical(tmp_project)

    issues = validate.validate_all(tmp_project)
    assert issues == []

    result = gate_scan.scan(tmp_project, "G2", subject="BR-001")
    criteria = {criterion.name: criterion for criterion in result.criteria}
    assert criteria["solutions"].passed
    assert criteria["solution-readiness"].passed
    assert criteria["investment-narrative"].passed
    assert "go" in result.exit_allowed
    assert not hasattr(result, "exit")


@pytest.mark.parametrize(
    "case",
    ["malformed", "stale", "missing", "extra", "wrong-layer", "wrong-source", "wrong-portfolio"],
)
def test_concept_assumption_refs_are_an_exact_pinned_local_set(tmp_project, case):
    artifacts, ledger = _canonical_lifecycle()
    portfolio = next(entry for entry in artifacts if entry[0].artifact_id == "ART-012" and entry[0].revision == 2)
    refs = portfolio[1]["concepts"][0]["assumption_refs"]
    if case == "malformed":
        refs[:] = ["A-001"]
    elif case == "stale":
        refs[:] = ["assumption:A-001@2"]
    elif case == "missing":
        refs.clear()
    elif case == "extra":
        refs.append("assumption:A-999@1")
    elif case == "wrong-layer":
        ledger.assumptions["A-001"].layer = schema.Layer.root
    elif case == "wrong-source":
        ledger.assumptions["A-001"].source_concept_id = "CI-002"
    else:
        ledger.assumptions["A-001"].derived_from = ["artifact:ART-099@1"]

    _materialize_canonical(tmp_project, artifacts, ledger)
    assert any(issue.kind == "concept-assumption-lineage" for issue in validate.validate_all(tmp_project))
