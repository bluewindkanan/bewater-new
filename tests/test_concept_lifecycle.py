from __future__ import annotations

from copy import deepcopy

import pytest

from bw import schema
from bw.concept_lifecycle import concept_issues


def _meta(artifact_id: str, kind: str, *, revision: int = 1, branch_id: str = "BR-001"):
    return schema.ArtifactMeta(
        artifact_id=artifact_id,
        kind=kind,
        stage="define" if kind == "opportunity" else "ideate",
        revision=revision,
        document_status="final",
        validation_status="unvalidated",
        branch_id=branch_id,
    )


def _opportunity(*, revision: int = 1):
    fm = {
        "artifact_id": "ART-010",
        "revision": revision,
        "kind": "opportunity",
        "branch_id": "BR-001",
        "opportunity_areas": [
            {
                "id": "OA-001",
                "name": "First",
                "audience": "People",
                "opportunity": "Need one",
                "consumer_value": "Value",
                "commercial_value": "Growth",
                "source_insight_refs": ["artifact:ART-004@1"],
            },
            {
                "id": "OA-002",
                "name": "Second",
                "audience": "People",
                "opportunity": "Need two",
                "consumer_value": "Value",
                "commercial_value": "Growth",
                "source_insight_refs": ["artifact:ART-004@1"],
            },
        ],
    }
    return _meta("ART-010", "opportunity", revision=revision), fm


def _seeds(start: int, *, count: int = 10):
    return [
        {
            "id": f"CS-{number:03d}",
            "idea": f"Raw possibility {number}.",
            "source_insight_refs": ["artifact:ART-004@1"],
            "cluster_id": None,
            "strategy_filter": "pass",
        }
        for number in range(start, start + count)
    ]


def _pool(*, artifact_id: str = "ART-011", revision: int = 1, opportunity_revision: int = 1):
    groups = [
        {
            "opportunity_area_id": "OA-001",
            "seeds": _seeds(1),
            "shortlist": {"recommended": ["CS-001", "CS-002"], "confirmed": ["CS-001", "CS-002"]},
        },
        {
            "opportunity_area_id": "OA-002",
            "seeds": _seeds(11),
            "shortlist": {"recommended": ["CS-011", "CS-012"], "confirmed": ["CS-011", "CS-012"]},
        },
    ]
    fm = {
        "artifact_id": artifact_id,
        "revision": revision,
        "kind": "idea-pool",
        "branch_id": "BR-001",
        "input_snapshot": {
            "strategy_ref": "artifact:ART-009@1",
            "opportunity_ref": f"artifact:ART-010@{opportunity_revision}",
        },
        "opportunity_areas": groups,
        "decisions": [
            {
                "type": "confirm-shortlist",
                "opportunity_area_id": group["opportunity_area_id"],
                "seed_ids": list(group["shortlist"]["confirmed"]),
                "decided_by": {"type": "human", "name": "Accountable human", "role": "innovation lead"},
            }
            for group in groups
            if group["shortlist"]["confirmed"]
        ],
    }
    return _meta(artifact_id, "idea-pool", revision=revision), fm


def _concept(cid: str, seed_id: str, oa_id: str, *, decision=None):
    return {
        "id": cid,
        "item_revision": 1,
        "opportunity_area_id": oa_id,
        "source_seed_id": seed_id,
        "parent_ids": [],
        "name": f"Concept {cid}",
        "pithy_description": "Useful new mechanism",
        "consumer_insight": "People need confidence.",
        "commercial_insight": "Confidence improves retention.",
        "idea_definition": "A service that makes the choice inspectable.",
        "who_its_for": "People making a first choice",
        "how_it_works": "Shows comparable evidence before commitment.",
        "what_it_replaces": "Opaque comparison",
        "why_big": "It removes a durable adoption barrier.",
        "visualization": "A three-panel walkthrough",
        "design_principles": ["Evidence before persuasion"],
        "dual_sided": {
            "money": {
                "commercial_value_proposition": {"statement": "Retention", "evidence_refs": []},
                "leverageable_assets": {"statement": "Data", "evidence_refs": []},
            },
            "magic": {
                "consumer_value_proposition": {"statement": "Confidence", "evidence_refs": []},
                "consumer_target": {"statement": "First-time buyers", "evidence_refs": []},
            },
            "tension": {"statement": "Proof without friction"},
            "balance_choice": "Progressive disclosure",
        },
        "evaluation": {"hard": {"lineage": True, "mechanism": True}},
        "assumption_refs": ["assumption:A-001@1"],
        "decision": decision,
        "merge_into": None,
    }


def _portfolio(*, artifact_id: str = "ART-012", revision: int = 1):
    concepts = [
        _concept("CI-001", "CS-001", "OA-001", decision="selected"),
        _concept("CI-002", "CS-011", "OA-002", decision="selected"),
    ]
    decisions = [
        {
            "type": "select",
            "concept_ids": ["CI-001", "CI-002"],
            "decided_by": {"name": "Accountable human", "role": "innovation lead"},
        }
    ]
    fm = {
        "artifact_id": artifact_id,
        "revision": revision,
        "kind": "concept-portfolio",
        "branch_id": "BR-001",
        "strategy_ref": "artifact:ART-009@1",
        "opportunity_ref": "artifact:ART-010@1",
        "idea_pool_ref": "artifact:ART-011@1",
        "concepts": concepts,
        "decisions": decisions,
        "exit": {"selected_concept_ids": ["CI-001", "CI-002"]},
    }
    return _meta(artifact_id, "concept-portfolio", revision=revision), fm


@pytest.fixture
def valid_lifecycle():
    return [_opportunity(), _pool(), _portfolio()]


def _kinds(artifacts):
    return {issue.kind for issue in concept_issues(artifacts)}


def test_valid_lifecycle_uses_new_canonical_names(valid_lifecycle):
    assert concept_issues(valid_lifecycle) == []


def test_second_idea_pool_chain_is_rejected_even_with_different_snapshot(valid_lifecycle):
    second_meta, second = _pool(artifact_id="ART-099", opportunity_revision=2)
    issues = concept_issues([*valid_lifecycle, (second_meta, second)])
    assert "pool-chain-duplicate" in {issue.kind for issue in issues}


def test_changed_snapshot_is_a_revision_of_the_same_idea_pool_chain(valid_lifecycle):
    opportunity_r2 = _opportunity(revision=2)
    pool_r2 = _pool(revision=2, opportunity_revision=2)
    artifacts = [*valid_lifecycle, opportunity_r2, pool_r2]
    kinds = _kinds(artifacts)
    assert "pool-chain-duplicate" not in kinds
    assert "pool-snapshot-revision" not in kinds


def test_seed_minimum_is_enforced_per_opportunity_area(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[1][1]["opportunity_areas"][1]["seeds"] = _seeds(11, count=9)
    issues = concept_issues(artifacts)
    assert any(issue.kind == "seed-count" and "OA-002" in issue.message for issue in issues)


def test_seed_ids_are_unique_pool_wide(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[1][1]["opportunity_areas"][1]["seeds"][0]["id"] = "CS-001"
    assert "seed-duplicate" in _kinds(artifacts)


def test_seed_soft_ceiling_is_not_a_structural_error(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[1][1]["opportunity_areas"][0]["seeds"] = _seeds(1, count=16)
    assert "seed-count" not in _kinds(artifacts)


@pytest.mark.parametrize(
    ("target", "bad_id", "expected_kind"),
    [("opportunity", "OA-1", "opportunity-area-id"), ("seed", "CS-1", "seed-id"), ("concept", "CI-1", "concept-id")],
)
def test_item_ids_require_three_digits(valid_lifecycle, target, bad_id, expected_kind):
    artifacts = deepcopy(valid_lifecycle)
    if target == "opportunity":
        artifacts[0][1]["opportunity_areas"][0]["id"] = bad_id
    elif target == "seed":
        artifacts[1][1]["opportunity_areas"][0]["seeds"][0]["id"] = bad_id
    else:
        artifacts[2][1]["concepts"][0]["id"] = bad_id
    assert expected_kind in _kinds(artifacts)


@pytest.mark.parametrize("change", ["reassign", "remove-and-reuse"])
def test_seed_id_is_never_reassigned_or_reused_across_history(valid_lifecycle, change):
    pool_r2 = deepcopy(_pool(revision=2))
    pool_r3 = deepcopy(_pool(revision=3))
    if change == "reassign":
        pool_r2[1]["opportunity_areas"][0]["seeds"][0]["idea"] = "A different possibility."
        artifacts = [*valid_lifecycle, pool_r2]
    else:
        pool_r2[1]["opportunity_areas"][0]["seeds"] = pool_r2[1]["opportunity_areas"][0]["seeds"][1:]
        pool_r2[1]["opportunity_areas"][0]["shortlist"] = {"recommended": [], "confirmed": []}
        artifacts = [*valid_lifecycle, pool_r2, pool_r3]
    assert "seed-id-reassigned" in _kinds(artifacts)


@pytest.mark.parametrize(
    ("mutation", "expected_kind"),
    [
        (lambda fm: fm.update(idea_pool_ref="artifact:ART-011@99"), "concept-source-unresolved"),
        (lambda fm: fm["concepts"][0].update(source_seed_id="CS-999"), "concept-source-unresolved"),
        (lambda fm: fm.update(opportunity_ref="artifact:ART-010@2"), "concept-opportunity-mismatch"),
        (lambda fm: fm["concepts"][0].update(opportunity_area_id="OA-002"), "concept-oa-mismatch"),
    ],
)
def test_concept_lineage_resolves_exact_revisions_and_local_ids(valid_lifecycle, mutation, expected_kind):
    artifacts = deepcopy(valid_lifecycle)
    mutation(artifacts[2][1])
    assert expected_kind in _kinds(artifacts)


def test_only_human_confirmed_seed_can_become_a_concept(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[1][1]["opportunity_areas"][0]["shortlist"]["confirmed"] = []
    assert "seed-not-confirmed" in _kinds(artifacts)


@pytest.mark.parametrize("actor_type", [None, "ai"])
def test_confirmed_shortlist_requires_matching_human_decision(valid_lifecycle, actor_type):
    artifacts = deepcopy(valid_lifecycle)
    if actor_type is None:
        artifacts[1][1]["decisions"] = []
    else:
        artifacts[1][1]["decisions"][0]["decided_by"] = {"type": actor_type, "name": "AI assistant"}
    assert "shortlist-confirmation-authority" in _kinds(artifacts)


def test_opportunity_area_content_may_evolve_without_reassigning_identity(valid_lifecycle):
    opportunity_r2 = deepcopy(_opportunity(revision=2))
    opportunity_r2[1]["opportunity_areas"][0]["name"] = "Sharper name"
    opportunity_r2[1]["opportunity_areas"][0]["opportunity"] = "A sharper opportunity"
    assert "opportunity-id-reassigned" not in _kinds([*valid_lifecycle, opportunity_r2])


def test_removed_opportunity_area_id_cannot_be_reused(valid_lifecycle):
    opportunity_r2 = deepcopy(_opportunity(revision=2))
    opportunity_r2[1]["opportunity_areas"] = opportunity_r2[1]["opportunity_areas"][1:]
    opportunity_r3 = deepcopy(_opportunity(revision=3))
    assert "opportunity-id-reassigned" in _kinds([*valid_lifecycle, opportunity_r2, opportunity_r3])


def test_branch_has_one_concept_portfolio_chain(valid_lifecycle):
    second_meta, second = _portfolio(artifact_id="ART-098")
    assert "portfolio-chain-duplicate" in _kinds([*valid_lifecycle, (second_meta, second)])


def test_terminal_concept_state_requires_a_human_decision(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[2][1]["decisions"] = []
    assert "concept-decision-ownership" in _kinds(artifacts)


def test_merge_target_parent_ids_include_every_merged_parent(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    portfolio = artifacts[2][1]
    portfolio["concepts"][0].update(decision="merged", merge_into="CI-003")
    portfolio["concepts"][1].update(decision="merged", merge_into="CI-003")
    target = _concept("CI-003", "CS-002", "OA-001", decision=None)
    target["parent_ids"] = ["CI-001"]
    portfolio["concepts"].append(target)
    portfolio["decisions"] = [
        {
            "type": "merge",
            "concept_ids": ["CI-001", "CI-002"],
            "decided_by": {"type": "human", "name": "Accountable human", "role": "innovation lead"},
        }
    ]
    portfolio["exit"] = {"selected_concept_ids": []}
    assert "merge-lineage" in _kinds(artifacts)


@pytest.mark.parametrize("selected", [["CI-001"], ["CI-001", "CI-002", "CI-003", "CI-004", "CI-005"]])
def test_ideate_exit_requires_two_to_four_selected_concepts(valid_lifecycle, selected):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[2][1]["exit"]["selected_concept_ids"] = selected
    assert "concept-exit-count" in _kinds(artifacts)
