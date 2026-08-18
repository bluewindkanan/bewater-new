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


def _cuts(seed_ids: list[str], *, keep: int = 5):
    return [
        {
            "seed_id": seed_id,
            "reason": "weak-distinctiveness",
            "rationale": f"{seed_id} repeats a stronger intervention mechanism.",
        }
        for seed_id in seed_ids[keep:]
    ]


def _pool(*, artifact_id: str = "ART-011", revision: int = 1, opportunity_revision: int = 1):
    groups = []
    for area_id, start in (("OA-001", 1), ("OA-002", 11)):
        seeds = _seeds(start)
        seed_ids = [seed["id"] for seed in seeds]
        groups.append(
            {
                "opportunity_area_id": area_id,
                "seeds": seeds,
                "review": {"status": "ready", "iterations": 1, "findings": []},
                "shortlist": {
                    "recommended_cuts": _cuts(seed_ids),
                    "confirmed": seed_ids[:5],
                },
            }
        )
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
                "decided_by": {
                    "type": "human",
                    "name": "Accountable human",
                    "role": "innovation lead",
                },
            }
            for group in groups
        ],
    }
    return _meta(artifact_id, "idea-pool", revision=revision), fm


def _legacy_pool(*, revision: int = 1):
    meta, fm = _pool(revision=revision)
    for group in fm["opportunity_areas"]:
        confirmed = group["shortlist"]["confirmed"][:2]
        group.pop("review")
        group["shortlist"] = {
            "recommended": list(confirmed),
            "confirmed": list(confirmed),
        }
    for decision, group in zip(fm["decisions"], fm["opportunity_areas"]):
        decision["seed_ids"] = list(group["shortlist"]["confirmed"])
    return meta, fm


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
        "evaluation": {
            "hard": {"lineage": True, "mechanism": True},
            "soft": {"comprehension": "strong"},
            "revision_attempts": 1,
            "recommended_action": "refine",
        },
        "assumption_refs": ["assumption:A-001@1"],
        "decision": decision,
        "merge_into": None,
    }


def _portfolio(*, artifact_id: str = "ART-012", revision: int = 1):
    source_rows = [
        *[(f"CS-{number:03d}", "OA-001") for number in range(1, 6)],
        *[(f"CS-{number:03d}", "OA-002") for number in range(11, 16)],
    ]
    concepts = [
        _concept(f"CI-{index:03d}", seed_id, area_id, decision="selected" if index <= 2 else None)
        for index, (seed_id, area_id) in enumerate(source_rows, 1)
    ]
    decisions = [
        {
            "type": "select",
            "concept_ids": ["CI-001", "CI-002"],
            "decided_by": {
                "type": "human",
                "name": "Accountable human",
                "role": "innovation lead",
            },
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
        "review": {
            "status": "ready",
            "iterations": 1,
            "reviewed_concept_ids": [concept["id"] for concept in concepts],
            "portfolio_findings": [],
        },
        "concepts": concepts,
        "decisions": decisions,
        "exit": {"selected_concept_ids": ["CI-001", "CI-002"]},
    }
    return _meta(artifact_id, "concept-portfolio", revision=revision), fm


def _legacy_portfolio(*, revision: int = 1):
    meta, fm = _portfolio(revision=revision)
    fm.pop("review")
    fm["concepts"] = [
        _concept("CI-001", "CS-001", "OA-001", decision="selected"),
        _concept("CI-002", "CS-011", "OA-002", decision="selected"),
    ]
    fm["decisions"][0]["concept_ids"] = ["CI-001", "CI-002"]
    fm["exit"]["selected_concept_ids"] = ["CI-001", "CI-002"]
    return meta, fm


@pytest.fixture
def valid_lifecycle():
    return [_opportunity(), _pool(), _portfolio()]


def _kinds(artifacts):
    return {issue.kind for issue in concept_issues(artifacts)}


def _sync_confirmation(pool: dict, area_index: int) -> None:
    group = pool["opportunity_areas"][area_index]
    decision = next(
        decision
        for decision in pool["decisions"]
        if decision["opportunity_area_id"] == group["opportunity_area_id"]
    )
    decision["seed_ids"] = list(group["shortlist"]["confirmed"])


def test_valid_lifecycle_uses_new_canonical_names(valid_lifecycle):
    assert concept_issues(valid_lifecycle) == []


def test_legacy_shortlist_and_portfolio_are_grandfathered():
    assert concept_issues([_opportunity(), _legacy_pool(), _legacy_portfolio()]) == []


def test_legacy_portfolio_allows_merge_suggestion_before_human_decision():
    portfolio = _legacy_portfolio()
    suggestion = _concept("CI-003", "CS-002", "OA-001")
    suggestion["merge_into"] = "CI-001"
    portfolio[1]["concepts"].append(suggestion)
    assert concept_issues([_opportunity(), _legacy_pool(), portfolio]) == []


def test_legacy_pool_keeps_the_old_soft_ceiling_behavior():
    opportunity = _opportunity()
    pool = _legacy_pool()
    pool[1]["opportunity_areas"][0]["seeds"] = _seeds(1, count=16)
    assert "seed-count" not in _kinds([opportunity, pool])


def test_second_idea_pool_chain_is_rejected_even_with_different_snapshot(valid_lifecycle):
    second_meta, second = _pool(artifact_id="ART-099", opportunity_revision=2)
    assert "pool-chain-duplicate" in _kinds([*valid_lifecycle, (second_meta, second)])


def test_changed_snapshot_is_a_revision_of_the_same_idea_pool_chain(valid_lifecycle):
    artifacts = [*valid_lifecycle, _opportunity(revision=2), _pool(revision=2, opportunity_revision=2)]
    assert "pool-chain-duplicate" not in _kinds(artifacts)
    assert "pool-snapshot-revision" not in _kinds(artifacts)


@pytest.mark.parametrize(("count", "valid"), [(9, False), (10, True), (15, True), (16, False)])
def test_seed_count_is_ten_to_fifteen_per_opportunity_area(valid_lifecycle, count, valid):
    artifacts = deepcopy(valid_lifecycle)
    group = artifacts[1][1]["opportunity_areas"][0]
    group["seeds"] = _seeds(1, count=count)
    ids = [seed["id"] for seed in group["seeds"]]
    group["shortlist"]["recommended_cuts"] = _cuts(ids, keep=min(5, count))
    group["shortlist"]["confirmed"] = ids[: min(5, count)]
    _sync_confirmation(artifacts[1][1], 0)
    assert ("seed-count" not in _kinds(artifacts)) is valid


def test_seed_ids_are_unique_pool_wide(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[1][1]["opportunity_areas"][1]["seeds"][0]["id"] = "CS-001"
    assert "seed-duplicate" in _kinds(artifacts)


@pytest.mark.parametrize(("remaining", "valid"), [(4, False), (5, True), (8, True), (9, False)])
def test_recommended_cut_complement_must_leave_five_to_eight(valid_lifecycle, remaining, valid):
    artifacts = deepcopy(valid_lifecycle)
    group = artifacts[1][1]["opportunity_areas"][0]
    ids = [seed["id"] for seed in group["seeds"]]
    group["shortlist"]["recommended_cuts"] = _cuts(ids, keep=remaining)
    assert ("recommended-remaining-count" not in _kinds(artifacts)) is valid


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        (lambda cuts: cuts.append(deepcopy(cuts[0])), "recommended-cut-duplicate"),
        (lambda cuts: cuts[0].update(seed_id="CS-999"), "recommended-cut-source-unresolved"),
        (lambda cuts: cuts[0].update(reason="popular"), "recommended-cut-reason"),
        (lambda cuts: cuts[0].update(rationale=" "), "recommended-cut-rationale"),
        (lambda cuts: cuts.__setitem__(0, "CS-006"), "recommended-cut-shape"),
    ],
)
def test_recommended_cuts_are_strict_structured_records(valid_lifecycle, mutation, expected):
    artifacts = deepcopy(valid_lifecycle)
    cuts = artifacts[1][1]["opportunity_areas"][0]["shortlist"]["recommended_cuts"]
    mutation(cuts)
    assert expected in _kinds(artifacts)


def test_new_shortlist_cannot_mix_legacy_recommended_field(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[1][1]["opportunity_areas"][0]["shortlist"]["recommended"] = ["CS-001"]
    assert "shortlist-contract-mixed" in _kinds(artifacts)


@pytest.mark.parametrize(("count", "valid"), [(4, False), (5, True), (8, True), (9, False)])
def test_confirmed_shortlist_must_contain_five_to_eight_unique_seeds(valid_lifecycle, count, valid):
    artifacts = deepcopy(valid_lifecycle)
    group = artifacts[1][1]["opportunity_areas"][0]
    group["shortlist"]["confirmed"] = [seed["id"] for seed in group["seeds"][:count]]
    _sync_confirmation(artifacts[1][1], 0)
    assert ("confirmed-count" not in _kinds(artifacts)) is valid


def test_duplicate_confirmed_seed_is_rejected_even_when_decision_matches(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    confirmed = artifacts[1][1]["opportunity_areas"][0]["shortlist"]["confirmed"]
    confirmed[-1] = confirmed[0]
    _sync_confirmation(artifacts[1][1], 0)
    assert "confirmed-duplicate" in _kinds(artifacts)


def test_confirmed_seed_must_resolve_inside_its_own_oa(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[1][1]["opportunity_areas"][0]["shortlist"]["confirmed"][-1] = "CS-011"
    _sync_confirmation(artifacts[1][1], 0)
    assert "shortlist-source-unresolved" in _kinds(artifacts)


def test_malformed_confirmed_entry_reports_issues_without_crashing(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[1][1]["opportunity_areas"][0]["shortlist"]["confirmed"][-1] = {"id": "CS-005"}
    _sync_confirmation(artifacts[1][1], 0)
    assert "shortlist-source-unresolved" in _kinds(artifacts)


@pytest.mark.parametrize("actor_type", [None, "ai", "reviewer"])
def test_confirmed_shortlist_requires_matching_human_decision(valid_lifecycle, actor_type):
    artifacts = deepcopy(valid_lifecycle)
    if actor_type is None:
        artifacts[1][1]["decisions"] = []
    else:
        artifacts[1][1]["decisions"][0]["decided_by"] = {
            "type": actor_type,
            "name": "Independent reviewer",
            "role": "reviewer",
        }
    assert "shortlist-confirmation-authority" in _kinds(artifacts)


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        (lambda review: review.update(status="approved"), "pool-review-invalid"),
        (lambda review: review.update(iterations=3), "pool-review-invalid"),
        (lambda review: review.update(findings="none"), "pool-review-invalid"),
    ],
)
def test_new_pool_review_has_bounded_structured_contract(valid_lifecycle, mutation, expected):
    artifacts = deepcopy(valid_lifecycle)
    mutation(artifacts[1][1]["opportunity_areas"][0]["review"])
    assert expected in _kinds(artifacts)


def test_needs_revision_pool_review_cannot_carry_human_confirmation():
    opportunity = _opportunity()
    pool = deepcopy(_pool())
    pool[1]["opportunity_areas"][0]["review"]["status"] = "needs-revision"
    assert "pool-review-not-ready" in _kinds([opportunity, pool])


def test_needs_revision_pool_review_is_valid_while_confirmation_is_empty():
    opportunity = _opportunity()
    pool = deepcopy(_pool())
    group = pool[1]["opportunity_areas"][0]
    group["review"]["status"] = "needs-revision"
    group["shortlist"]["confirmed"] = []
    pool[1]["decisions"] = [
        decision
        for decision in pool[1]["decisions"]
        if decision["opportunity_area_id"] != group["opportunity_area_id"]
    ]
    assert "pool-review-not-ready" not in _kinds([opportunity, pool])


def test_concept_development_waits_for_every_oa_confirmation(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[1][1]["opportunity_areas"][1]["shortlist"]["confirmed"] = []
    artifacts[1][1]["decisions"] = artifacts[1][1]["decisions"][:1]
    assert "pool-confirmation-incomplete" in _kinds(artifacts)


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        (lambda fm: fm.update(idea_pool_ref="artifact:ART-011@99"), "concept-source-unresolved"),
        (lambda fm: fm["concepts"][0].update(source_seed_id="CS-999"), "concept-source-unresolved"),
        (lambda fm: fm.update(opportunity_ref="artifact:ART-010@2"), "concept-opportunity-mismatch"),
        (lambda fm: fm["concepts"][0].update(opportunity_area_id="OA-002"), "concept-oa-mismatch"),
    ],
)
def test_concept_lineage_resolves_exact_revisions_and_local_ids(valid_lifecycle, mutation, expected):
    artifacts = deepcopy(valid_lifecycle)
    mutation(artifacts[2][1])
    assert expected in _kinds(artifacts)


def test_every_confirmed_seed_has_exactly_one_root_concept(valid_lifecycle):
    missing = deepcopy(valid_lifecycle)
    missing[2][1]["concepts"].pop()
    missing[2][1]["review"]["reviewed_concept_ids"].pop()
    assert "initial-concept-missing" in _kinds(missing)

    duplicate = deepcopy(valid_lifecycle)
    duplicate[2][1]["concepts"][-1]["source_seed_id"] = "CS-001"
    assert "initial-concept-duplicate" in _kinds(duplicate)

    extra = deepcopy(valid_lifecycle)
    extra_concept = _concept("CI-011", "CS-006", "OA-001")
    extra[2][1]["concepts"].append(extra_concept)
    extra[2][1]["review"]["reviewed_concept_ids"].append("CI-011")
    assert "initial-concept-extra" in _kinds(extra)


def test_parented_concept_is_not_counted_as_an_initial_one_to_one_development(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    child = _concept("CI-011", "CS-001", "OA-001")
    child["parent_ids"] = ["CI-001"]
    artifacts[2][1]["concepts"].append(child)
    artifacts[2][1]["review"]["reviewed_concept_ids"].append("CI-011")
    assert not {"initial-concept-missing", "initial-concept-duplicate", "initial-concept-extra"} & _kinds(artifacts)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda concept: concept.pop("parent_ids"),
        lambda concept: concept.update(parent_ids="CI-001"),
    ],
)
def test_strict_concept_parent_ids_must_be_a_list(valid_lifecycle, mutation):
    artifacts = deepcopy(valid_lifecycle)
    mutation(artifacts[2][1]["concepts"][0])
    assert "concept-parent-ids" in _kinds(artifacts)


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        (lambda review: review.update(status="approved"), "concept-review-invalid"),
        (lambda review: review.update(iterations=3), "concept-review-invalid"),
        (lambda review: review.update(portfolio_findings="none"), "concept-review-invalid"),
        (lambda review: review["reviewed_concept_ids"].pop(), "concept-review-coverage"),
        (lambda review: review["reviewed_concept_ids"].append("CI-999"), "concept-review-coverage"),
        (lambda review: review["reviewed_concept_ids"].append("CI-001"), "concept-review-coverage"),
    ],
)
def test_concept_review_is_bounded_and_covers_current_candidates(valid_lifecycle, mutation, expected):
    artifacts = deepcopy(valid_lifecycle)
    mutation(artifacts[2][1]["review"])
    assert expected in _kinds(artifacts)


def test_ready_review_requires_nonempty_hard_and_soft_evaluation(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[2][1]["concepts"][0]["evaluation"]["soft"] = {}
    assert "concept-review-invalid" in _kinds(artifacts)


def test_terminal_history_is_excluded_from_review_coverage(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    portfolio = artifacts[2][1]
    portfolio["concepts"][-1]["decision"] = "killed"
    portfolio["decisions"].append(
        {
            "type": "kill",
            "concept_ids": [portfolio["concepts"][-1]["id"]],
            "decided_by": {"type": "human", "name": "Accountable human", "role": "innovation lead"},
        }
    )
    portfolio["review"]["reviewed_concept_ids"].pop()
    assert "concept-review-coverage" not in _kinds(artifacts)


def test_review_needs_revision_blocks_human_terminal_decision(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[2][1]["review"]["status"] = "needs-revision"
    assert "concept-review-not-ready" in _kinds(artifacts)


@pytest.mark.parametrize(
    "forbidden_key",
    ["confirmed", "decision", "merge_into", "selected_concept_ids", "exit"],
)
def test_reviewer_payload_cannot_contain_human_only_fields(valid_lifecycle, forbidden_key):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[2][1]["review"][forbidden_key] = []
    assert "review-authority" in _kinds(artifacts)


def test_merge_into_requires_matching_human_owned_merge(valid_lifecycle):
    artifacts = deepcopy(valid_lifecycle)
    artifacts[2][1]["concepts"][2]["merge_into"] = "CI-001"
    assert "concept-decision-ownership" in _kinds(artifacts)


def test_opportunity_area_content_may_evolve_without_reassigning_identity(valid_lifecycle):
    opportunity_r2 = deepcopy(_opportunity(revision=2))
    opportunity_r2[1]["opportunity_areas"][0]["name"] = "Sharper name"
    opportunity_r2[1]["opportunity_areas"][0]["opportunity"] = "A sharper opportunity"
    assert "opportunity-id-reassigned" not in _kinds([*valid_lifecycle, opportunity_r2])


def test_seed_id_is_never_reassigned_or_reused_across_history(valid_lifecycle):
    pool_r2 = deepcopy(_pool(revision=2))
    pool_r2[1]["opportunity_areas"][0]["seeds"][0]["idea"] = "A different possibility."
    assert "seed-id-reassigned" in _kinds([*valid_lifecycle, pool_r2])


def test_removed_seed_id_cannot_be_reused_later():
    pool_r1 = _legacy_pool(revision=1)
    pool_r2 = deepcopy(_legacy_pool(revision=2))
    pool_r3 = deepcopy(_legacy_pool(revision=3))
    pool_r2[1]["opportunity_areas"][0]["seeds"] = pool_r2[1]["opportunity_areas"][0]["seeds"][1:]
    pool_r2[1]["opportunity_areas"][0]["shortlist"] = {"recommended": [], "confirmed": []}
    pool_r2[1]["decisions"] = pool_r2[1]["decisions"][1:]
    assert "seed-id-reassigned" in _kinds([_opportunity(), pool_r1, pool_r2, pool_r3])


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
    portfolio["concepts"][0].update(decision="merged", merge_into="CI-011")
    portfolio["concepts"][1].update(decision="merged", merge_into="CI-011")
    target = _concept("CI-011", "CS-001", "OA-001")
    target["parent_ids"] = ["CI-001"]
    portfolio["concepts"].append(target)
    portfolio["review"]["reviewed_concept_ids"] = [
        concept["id"]
        for concept in portfolio["concepts"]
        if concept.get("decision") not in {"merged", "killed"}
    ]
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
