"""Validation for Opportunity -> Idea Pool -> Concept Portfolio lineage.

Item identifiers are local to their owning append-only artifact chain.  The
module resolves exact artifact revisions and never accepts legacy lifecycle
names or fragment-style global references.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from collections.abc import Iterable
from typing import Any

from . import schema

Issue = schema.Issue
Artifact = tuple[schema.ArtifactMeta, dict]

_POOL = schema.ArtifactKind.idea_pool
_PORTFOLIO = schema.ArtifactKind.concept_portfolio
_OPPORTUNITY = schema.ArtifactKind.opportunity
_TERMINAL_DECISIONS = {"selected": "select", "killed": "kill", "merged": "merge"}
_CUT_REASONS = {
    "duplicate",
    "weak-distinctiveness",
    "oa-misaligned",
    "strategy-misaligned",
    "unclear",
}
_REVIEW_STATUSES = {"ready", "needs-revision"}
_RECOMMENDED_ACTIONS = {"refine", "pivot", "split", "merge", "kill", "recycle-to-OA"}
_REVIEW_FORBIDDEN_FIELDS = {"confirmed", "decision", "merge_into", "selected_concept_ids", "exit"}
_OA_ID = re.compile(r"^OA-\d{3}$")
_SEED_ID = re.compile(r"^CS-\d{3}$")
_CONCEPT_ID = re.compile(r"^CI-\d{3}$")
_ASSUMPTION_REF = re.compile(r"^assumption:A-\d{3}@[1-9]\d*$")
_CONCEPT_REQUIRED_FIELDS = (
    "name",
    "pithy_description",
    "consumer_insight",
    "commercial_insight",
    "idea_definition",
    "who_its_for",
    "how_it_works",
    "what_it_replaces",
    "why_big",
    "visualization",
)


def concept_issues(artifacts: list[Artifact]) -> list[Issue]:
    """Return structural and lineage issues for canonical Ideate artifacts."""
    index = _index(artifacts)
    opportunities = [entry for entry in artifacts if entry[0].kind == _OPPORTUNITY]
    pools = [entry for entry in artifacts if entry[0].kind == _POOL]
    portfolios = [entry for entry in artifacts if entry[0].kind == _PORTFOLIO]

    issues: list[Issue] = []
    issues.extend(_chain_issues(pools, "pool"))
    issues.extend(_chain_issues(portfolios, "portfolio"))
    issues.extend(_opportunity_history_issues(opportunities))
    issues.extend(_pool_history_issues(pools))
    issues.extend(_portfolio_history_issues(portfolios))
    for meta, frontmatter in opportunities:
        issues.extend(_opportunity_issues(meta, frontmatter))
    for meta, frontmatter in pools:
        issues.extend(_pool_issues(meta, frontmatter, index))
    for meta, frontmatter in portfolios:
        issues.extend(_portfolio_issues(meta, frontmatter, index))
    return issues


def _index(artifacts: Iterable[Artifact]) -> dict[str, dict[int, dict]]:
    index: dict[str, dict[int, dict]] = defaultdict(dict)
    for meta, frontmatter in artifacts:
        index[meta.artifact_id][meta.revision] = frontmatter
    return index


def _parse_artifact_ref(ref: Any) -> tuple[str, int] | None:
    if not isinstance(ref, str) or not ref.startswith("artifact:") or "@" not in ref:
        return None
    artifact_id, separator, revision = ref[len("artifact:"):].rpartition("@")
    if not separator or not artifact_id:
        return None
    try:
        parsed_revision = int(revision)
    except ValueError:
        return None
    return (artifact_id, parsed_revision) if parsed_revision > 0 else None


def _resolve(
    index: dict[str, dict[int, dict]], ref: Any, kind: schema.ArtifactKind
) -> dict | None:
    parsed = _parse_artifact_ref(ref)
    if parsed is None:
        return None
    artifact_id, revision = parsed
    frontmatter = index.get(artifact_id, {}).get(revision)
    if frontmatter is None or frontmatter.get("kind") != kind.value:
        return None
    return frontmatter


def _chain_issues(items: list[Artifact], label: str) -> list[Issue]:
    by_branch: dict[str, set[str]] = defaultdict(set)
    for meta, _ in items:
        by_branch[meta.branch_id].add(meta.artifact_id)
    return [
        Issue(
            branch_id or "unknown-branch",
            f"{label}-chain-duplicate",
            f"branch {branch_id!r} has {len(artifact_ids)} {label} chains; exactly one is allowed",
        )
        for branch_id, artifact_ids in sorted(by_branch.items())
        if len(artifact_ids) > 1
    ]


def _opportunity_areas(frontmatter: dict) -> list[dict]:
    areas = frontmatter.get("opportunity_areas")
    return [area for area in areas if isinstance(area, dict)] if isinstance(areas, list) else []


def _pool_groups(frontmatter: dict) -> list[dict]:
    groups = frontmatter.get("opportunity_areas")
    return [group for group in groups if isinstance(group, dict)] if isinstance(groups, list) else []


def _is_strict_pool(frontmatter: dict) -> bool:
    return any(
        isinstance(group.get("shortlist"), dict)
        and "recommended_cuts" in group["shortlist"]
        for group in _pool_groups(frontmatter)
    )


def _seeds(frontmatter: dict):
    for group in _pool_groups(frontmatter):
        opportunity_area_id = group.get("opportunity_area_id")
        seeds = group.get("seeds")
        if not isinstance(seeds, list):
            continue
        for seed in seeds:
            if isinstance(seed, dict):
                yield opportunity_area_id, seed


def _history_identity_issues(
    items: list[Artifact],
    *,
    rows,
    issue_kind: str,
) -> list[Issue]:
    issues: list[Issue] = []
    by_artifact: dict[str, list[Artifact]] = defaultdict(list)
    for entry in items:
        by_artifact[entry[0].artifact_id].append(entry)

    for artifact_id, revisions in by_artifact.items():
        seen: dict[str, Any] = {}
        removed: set[str] = set()
        for _, frontmatter in sorted(revisions, key=lambda entry: entry[0].revision):
            current: set[str] = set()
            for item_id, fingerprint in rows(frontmatter):
                if not isinstance(item_id, str):
                    continue
                current.add(item_id)
                if item_id in seen and seen[item_id] != fingerprint:
                    issues.append(Issue(
                        artifact_id,
                        issue_kind,
                        f"{artifact_id}: {item_id} was reassigned across revisions",
                    ))
                if item_id in removed:
                    issues.append(Issue(
                        artifact_id,
                        issue_kind,
                        f"{artifact_id}: {item_id} was reused after removal",
                    ))
                seen[item_id] = fingerprint
            removed.update(set(seen) - current)
    return issues


def _opportunity_history_issues(opportunities: list[Artifact]) -> list[Issue]:
    return _history_identity_issues(
        opportunities,
        rows=lambda frontmatter: (
            (area.get("id"), area.get("id"))
            for area in _opportunity_areas(frontmatter)
        ),
        issue_kind="opportunity-id-reassigned",
    )


def _pool_history_issues(pools: list[Artifact]) -> list[Issue]:
    return _history_identity_issues(
        pools,
        rows=lambda frontmatter: (
            (seed.get("id"), (opportunity_area_id, seed.get("idea")))
            for opportunity_area_id, seed in _seeds(frontmatter)
        ),
        issue_kind="seed-id-reassigned",
    )


def _portfolio_history_issues(portfolios: list[Artifact]) -> list[Issue]:
    return _history_identity_issues(
        portfolios,
        rows=lambda frontmatter: (
            (
                concept.get("id"),
                (
                    concept.get("source_seed_id"),
                    tuple(concept.get("parent_ids") or []),
                ),
            )
            for concept in _concepts(frontmatter)
        ),
        issue_kind="concept-id-reassigned",
    )


def _opportunity_issues(meta: schema.ArtifactMeta, frontmatter: dict) -> list[Issue]:
    issues: list[Issue] = []
    areas = _opportunity_areas(frontmatter)
    if not isinstance(frontmatter.get("opportunity_areas"), list):
        return [Issue(meta.artifact_id, "opportunity-areas-missing", "opportunity_areas must be a list")]
    seen: set[str] = set()
    required = ("name", "audience", "opportunity", "consumer_value", "commercial_value")
    for area in areas:
        area_id = area.get("id")
        if not isinstance(area_id, str) or _OA_ID.fullmatch(area_id) is None:
            issues.append(Issue(meta.artifact_id, "opportunity-area-id", f"invalid OA id {area_id!r}"))
        elif area_id in seen:
            issues.append(Issue(meta.artifact_id, "opportunity-area-duplicate", f"duplicate OA id {area_id}"))
        else:
            seen.add(area_id)
        for field in required:
            if not str(area.get(field, "")).strip():
                issues.append(Issue(meta.artifact_id, "opportunity-area-field", f"{area_id or '?'} missing {field}"))
        if not isinstance(area.get("source_insight_refs"), list):
            issues.append(Issue(meta.artifact_id, "opportunity-area-source", f"{area_id or '?'} lacks source_insight_refs"))
    return issues


def _pool_issues(
    meta: schema.ArtifactMeta,
    frontmatter: dict,
    index: dict[str, dict[int, dict]],
) -> list[Issue]:
    issues: list[Issue] = []
    snapshot = frontmatter.get("input_snapshot")
    if not isinstance(snapshot, dict):
        return [Issue(meta.artifact_id, "pool-snapshot-revision", "input_snapshot must be a mapping")]

    opportunity = _resolve(index, snapshot.get("opportunity_ref"), _OPPORTUNITY)
    if opportunity is None:
        issues.append(Issue(meta.artifact_id, "opportunity-source-unresolved", "input_snapshot.opportunity_ref does not resolve"))
        opportunity_ids: set[str] = set()
    else:
        opportunity_ids = {area.get("id") for area in _opportunity_areas(opportunity)}

    if _parse_artifact_ref(snapshot.get("strategy_ref")) is None:
        issues.append(Issue(meta.artifact_id, "strategy-source-unresolved", "input_snapshot.strategy_ref is not exact"))

    strict = _is_strict_pool(frontmatter)
    seen_seed_ids: set[str] = set()
    seen_group_ids: set[str] = set()
    for group in _pool_groups(frontmatter):
        area_id = group.get("opportunity_area_id")
        if not isinstance(area_id, str) or _OA_ID.fullmatch(area_id) is None or area_id not in opportunity_ids:
            issues.append(Issue(meta.artifact_id, "opportunity-area-unresolved", f"invalid opportunity area id {area_id!r}"))
        elif area_id in seen_group_ids:
            issues.append(Issue(meta.artifact_id, "opportunity-area-duplicate", f"duplicate pool group {area_id}"))
        else:
            seen_group_ids.add(area_id)

        seeds = [seed for seed in group.get("seeds", []) if isinstance(seed, dict)] if isinstance(group.get("seeds"), list) else []
        if len(seeds) < 10 or (strict and len(seeds) > 15):
            expected = "10-15" if strict else "at least 10"
            issues.append(Issue(
                meta.artifact_id,
                "seed-count",
                f"{area_id} has {len(seeds)} seeds (expected {expected})",
            ))

        local_ids: set[str] = set()
        for seed in seeds:
            seed_id = seed.get("id")
            if not isinstance(seed_id, str) or _SEED_ID.fullmatch(seed_id) is None:
                issues.append(Issue(meta.artifact_id, "seed-id", f"invalid seed id {seed_id!r}"))
            elif seed_id in seen_seed_ids:
                issues.append(Issue(meta.artifact_id, "seed-duplicate", f"duplicate seed id {seed_id}"))
            else:
                seen_seed_ids.add(seed_id)
                local_ids.add(seed_id)
            if not str(seed.get("idea", "")).strip():
                issues.append(Issue(meta.artifact_id, "seed-idea-missing", f"{seed_id or '?'} has no idea"))
            if not isinstance(seed.get("source_insight_refs"), list):
                issues.append(Issue(meta.artifact_id, "seed-source-missing", f"{seed_id or '?'} lacks source_insight_refs"))

        shortlist = group.get("shortlist")
        if not isinstance(shortlist, dict):
            issues.append(Issue(meta.artifact_id, "shortlist-missing", f"{area_id} shortlist must be a mapping"))
            continue

        if strict:
            issues.extend(_strict_group_review_issues(meta.artifact_id, area_id, group.get("review")))
            if "recommended" in shortlist:
                issues.append(Issue(
                    meta.artifact_id,
                    "shortlist-contract-mixed",
                    f"{area_id} cannot mix recommended with recommended_cuts",
                ))
            issues.extend(_recommended_cut_issues(
                meta.artifact_id,
                area_id,
                shortlist.get("recommended_cuts"),
                local_ids,
            ))
        else:
            recommended = shortlist.get("recommended")
            if not isinstance(recommended, list):
                issues.append(Issue(
                    meta.artifact_id,
                    "shortlist-missing",
                    f"{area_id} shortlist.recommended must be a list",
                ))
            else:
                for seed_id in recommended:
                    if not isinstance(seed_id, str) or seed_id not in local_ids:
                        issues.append(Issue(
                            meta.artifact_id,
                            "shortlist-source-unresolved",
                            f"recommended seed {seed_id!r} is not in {area_id}",
                        ))

        confirmed = shortlist.get("confirmed")
        if not isinstance(confirmed, list):
            issues.append(Issue(
                meta.artifact_id,
                "shortlist-missing",
                f"{area_id} shortlist.confirmed must be a list",
            ))
            continue
        for seed_id in confirmed:
            if not isinstance(seed_id, str) or seed_id not in local_ids:
                issues.append(Issue(
                    meta.artifact_id,
                    "shortlist-source-unresolved",
                    f"confirmed seed {seed_id!r} is not in {area_id}",
                ))
        if strict and confirmed:
            if not 5 <= len(confirmed) <= 8:
                issues.append(Issue(
                    meta.artifact_id,
                    "confirmed-count",
                    f"{area_id} confirmed {len(confirmed)} seeds (expected 5-8)",
                ))
            string_confirmed = [seed_id for seed_id in confirmed if isinstance(seed_id, str)]
            if len(set(string_confirmed)) != len(string_confirmed):
                issues.append(Issue(
                    meta.artifact_id,
                    "confirmed-duplicate",
                    f"{area_id} confirmed shortlist contains duplicate IDs",
                ))
            review = group.get("review")
            if not isinstance(review, dict) or review.get("status") != "ready":
                issues.append(Issue(
                    meta.artifact_id,
                    "pool-review-not-ready",
                    f"{area_id} cannot carry confirmation before review.status ready",
                ))
        if (
            confirmed
            and not _has_human_shortlist_confirmation(frontmatter, area_id, confirmed)
        ):
            issues.append(Issue(
                meta.artifact_id,
                "shortlist-confirmation-authority",
                f"{area_id} confirmed shortlist has no matching human decision",
            ))

    if opportunity is not None and seen_group_ids != opportunity_ids:
        issues.append(Issue(meta.artifact_id, "opportunity-group-mismatch", "Idea Pool OA groups do not equal its Opportunity snapshot"))
    return issues


def _strict_group_review_issues(artifact_id: str, area_id: Any, review: Any) -> list[Issue]:
    if not isinstance(review, dict):
        return [Issue(artifact_id, "pool-review-invalid", f"{area_id} review must be a mapping")]
    status = review.get("status")
    iterations = review.get("iterations")
    findings = review.get("findings")
    if (
        status not in _REVIEW_STATUSES
        or isinstance(iterations, bool)
        or not isinstance(iterations, int)
        or not 1 <= iterations <= 2
        or not isinstance(findings, list)
    ):
        return [Issue(
            artifact_id,
            "pool-review-invalid",
            f"{area_id} review requires status, 1-2 iterations, and findings[]",
        )]
    return []


def _recommended_cut_issues(
    artifact_id: str,
    area_id: Any,
    cuts: Any,
    local_ids: set[str],
) -> list[Issue]:
    if not isinstance(cuts, list):
        return [Issue(
            artifact_id,
            "shortlist-missing",
            f"{area_id} shortlist.recommended_cuts must be a list",
        )]

    issues: list[Issue] = []
    cut_ids: list[str] = []
    for cut in cuts:
        if not isinstance(cut, dict):
            issues.append(Issue(
                artifact_id,
                "recommended-cut-shape",
                f"{area_id} recommended cut must be a mapping",
            ))
            continue
        seed_id = cut.get("seed_id")
        if not isinstance(seed_id, str) or seed_id not in local_ids:
            issues.append(Issue(
                artifact_id,
                "recommended-cut-source-unresolved",
                f"recommended cut seed {seed_id!r} is not in {area_id}",
            ))
        else:
            cut_ids.append(seed_id)
        if cut.get("reason") not in _CUT_REASONS:
            issues.append(Issue(
                artifact_id,
                "recommended-cut-reason",
                f"{area_id} cut {seed_id!r} has invalid reason",
            ))
        if not str(cut.get("rationale", "")).strip():
            issues.append(Issue(
                artifact_id,
                "recommended-cut-rationale",
                f"{area_id} cut {seed_id!r} requires a rationale",
            ))

    if len(set(cut_ids)) != len(cut_ids):
        issues.append(Issue(
            artifact_id,
            "recommended-cut-duplicate",
            f"{area_id} recommended_cuts contains duplicate Seed IDs",
        ))
    remaining = len(local_ids - set(cut_ids))
    if not 5 <= remaining <= 8:
        issues.append(Issue(
            artifact_id,
            "recommended-remaining-count",
            f"{area_id} recommended cuts leave {remaining} seeds (expected 5-8)",
        ))
    return issues


def _concepts(frontmatter: dict) -> list[dict]:
    concepts = frontmatter.get("concepts")
    return [concept for concept in concepts if isinstance(concept, dict)] if isinstance(concepts, list) else []


def _portfolio_issues(
    meta: schema.ArtifactMeta,
    frontmatter: dict,
    index: dict[str, dict[int, dict]],
) -> list[Issue]:
    issues: list[Issue] = []
    pool = _resolve(index, frontmatter.get("idea_pool_ref"), _POOL)
    if pool is None:
        return [Issue(meta.artifact_id, "concept-source-unresolved", "idea_pool_ref does not resolve")]

    snapshot = pool.get("input_snapshot") if isinstance(pool.get("input_snapshot"), dict) else {}
    if frontmatter.get("opportunity_ref") != snapshot.get("opportunity_ref"):
        issues.append(Issue(meta.artifact_id, "concept-opportunity-mismatch", "opportunity_ref differs from Idea Pool snapshot"))
    if frontmatter.get("strategy_ref") != snapshot.get("strategy_ref"):
        issues.append(Issue(meta.artifact_id, "concept-strategy-mismatch", "strategy_ref differs from Idea Pool snapshot"))
    if meta.branch_id != pool.get("branch_id"):
        issues.append(Issue(meta.artifact_id, "concept-branch-mismatch", "Concept Portfolio branch differs from Idea Pool"))

    strict = _is_strict_pool(pool)
    if strict and not _pool_confirmations_ready(pool):
        issues.append(Issue(
            meta.artifact_id,
            "pool-confirmation-incomplete",
            "Concept development requires 5-8 human-confirmed Seeds in every OA",
        ))

    concepts = _concepts(frontmatter)
    decisions = _human_decisions(frontmatter)
    concept_ids: set[str] = set()
    for concept in concepts:
        concept_id = concept.get("id")
        if not isinstance(concept_id, str) or _CONCEPT_ID.fullmatch(concept_id) is None:
            issues.append(Issue(meta.artifact_id, "concept-id", f"invalid concept id {concept_id!r}"))
            concept_id = str(concept_id or "?")
        elif concept_id in concept_ids:
            issues.append(Issue(meta.artifact_id, "concept-id-duplicate", f"duplicate concept id {concept_id}"))
        else:
            concept_ids.add(concept_id)
        issues.extend(_concept_source_issues(meta.artifact_id, concept_id, concept, pool))
        issues.extend(_concept_content_issues(meta.artifact_id, concept_id, concept))
        issues.extend(_concept_decision_issues(
            meta.artifact_id,
            concept_id,
            concept,
            decisions,
            strict=strict,
        ))

    if strict:
        issues.extend(_initial_concept_issues(meta.artifact_id, concepts, pool))
        issues.extend(_concept_review_issues(meta.artifact_id, frontmatter, concepts))

    merged_by_target: dict[str, set[str]] = defaultdict(set)
    concepts_by_id = {
        concept.get("id"): concept
        for concept in concepts
        if isinstance(concept.get("id"), str)
    }
    for concept in concepts:
        if concept.get("decision") == "merged" and concept.get("merge_into") not in concept_ids:
            issues.append(Issue(meta.artifact_id, "merge-lineage", f"{concept.get('id')} has no valid merge target"))
        elif concept.get("decision") == "merged":
            merged_by_target[str(concept.get("merge_into"))].add(str(concept.get("id")))
        parents = concept.get("parent_ids")
        if parents and (not isinstance(parents, list) or len(parents) < 1 or any(parent not in concept_ids for parent in parents)):
            issues.append(Issue(meta.artifact_id, "merge-lineage", f"{concept.get('id')} has invalid parent_ids"))
    for target_id, merged_parents in merged_by_target.items():
        target_parents = set((concepts_by_id.get(target_id) or {}).get("parent_ids") or [])
        if len(merged_parents) < 2 or not merged_parents.issubset(target_parents):
            issues.append(Issue(
                meta.artifact_id,
                "merge-lineage",
                f"{target_id} parent_ids must contain every merged parent",
            ))

    issues.extend(_exit_issues(meta.artifact_id, frontmatter, concepts))
    return issues


def _pool_confirmations_ready(pool: dict) -> bool:
    for group in _pool_groups(pool):
        review = group.get("review")
        shortlist = group.get("shortlist")
        if not isinstance(review, dict) or review.get("status") != "ready":
            return False
        if not isinstance(shortlist, dict):
            return False
        confirmed = shortlist.get("confirmed")
        if not isinstance(confirmed, list) or not 5 <= len(confirmed) <= 8:
            return False
        if not all(isinstance(seed_id, str) for seed_id in confirmed):
            return False
        if len(set(confirmed)) != len(confirmed):
            return False
        local_ids = {
            seed.get("id")
            for seed in group.get("seeds", [])
            if isinstance(seed, dict) and isinstance(seed.get("id"), str)
        }
        if any(not isinstance(seed_id, str) or seed_id not in local_ids for seed_id in confirmed):
            return False
        if not _has_human_shortlist_confirmation(
            pool,
            group.get("opportunity_area_id"),
            confirmed,
        ):
            return False
    return bool(_pool_groups(pool))


def _initial_concept_issues(artifact_id: str, concepts: list[dict], pool: dict) -> list[Issue]:
    confirmed: dict[str, str] = {}
    for group in _pool_groups(pool):
        area_id = group.get("opportunity_area_id")
        shortlist = group.get("shortlist") if isinstance(group.get("shortlist"), dict) else {}
        raw_confirmed = shortlist.get("confirmed", [])
        if not isinstance(raw_confirmed, list):
            continue
        for seed_id in raw_confirmed:
            if isinstance(seed_id, str):
                confirmed[seed_id] = str(area_id)

    issues: list[Issue] = []
    for concept in concepts:
        if not isinstance(concept.get("parent_ids"), list):
            issues.append(Issue(
                artifact_id,
                "concept-parent-ids",
                f"{concept.get('id')} parent_ids must be a list",
            ))
    roots = [concept for concept in concepts if concept.get("parent_ids") == []]
    counts = Counter(
        concept.get("source_seed_id")
        for concept in roots
        if isinstance(concept.get("source_seed_id"), str)
    )
    missing = sorted(seed_id for seed_id in confirmed if counts[seed_id] == 0)
    duplicate = sorted(seed_id for seed_id in confirmed if counts[seed_id] > 1)
    extra = sorted(seed_id for seed_id in counts if seed_id not in confirmed)
    if missing:
        issues.append(Issue(
            artifact_id,
            "initial-concept-missing",
            f"confirmed Seeds missing an initial Concept: {', '.join(missing)}",
        ))
    if duplicate:
        issues.append(Issue(
            artifact_id,
            "initial-concept-duplicate",
            f"confirmed Seeds developed more than once: {', '.join(duplicate)}",
        ))
    if extra:
        issues.append(Issue(
            artifact_id,
            "initial-concept-extra",
            f"initial Concepts develop unconfirmed Seeds: {', '.join(extra)}",
        ))
    return issues


def _concept_review_issues(artifact_id: str, frontmatter: dict, concepts: list[dict]) -> list[Issue]:
    review = frontmatter.get("review")
    if not isinstance(review, dict):
        return [Issue(
            artifact_id,
            "concept-review-invalid",
            "strict Concept Portfolio requires review metadata",
        )]

    issues: list[Issue] = []
    forbidden = sorted(_REVIEW_FORBIDDEN_FIELDS.intersection(review))
    if forbidden:
        issues.append(Issue(
            artifact_id,
            "review-authority",
            f"review payload contains human-only fields: {', '.join(forbidden)}",
        ))

    status = review.get("status")
    iterations = review.get("iterations")
    findings = review.get("portfolio_findings")
    if (
        status not in _REVIEW_STATUSES
        or isinstance(iterations, bool)
        or not isinstance(iterations, int)
        or not 1 <= iterations <= 2
        or not isinstance(findings, list)
    ):
        issues.append(Issue(
            artifact_id,
            "concept-review-invalid",
            "review requires status, 1-2 iterations, and portfolio_findings[]",
        ))

    reviewed = review.get("reviewed_concept_ids")
    active = {
        concept.get("id")
        for concept in concepts
        if isinstance(concept.get("id"), str)
        and concept.get("decision") not in {"killed", "merged"}
    }
    coverage_valid = (
        isinstance(reviewed, list)
        and all(isinstance(concept_id, str) for concept_id in reviewed)
        and len(set(reviewed)) == len(reviewed)
        and set(reviewed) == active
    )
    if not coverage_valid:
        issues.append(Issue(
            artifact_id,
            "concept-review-coverage",
            "reviewed_concept_ids must exactly cover current candidates",
        ))

    for concept in concepts:
        if concept.get("id") not in active:
            continue
        evaluation = concept.get("evaluation")
        if (
            not isinstance(evaluation, dict)
            or not isinstance(evaluation.get("hard"), dict)
            or not evaluation.get("hard")
            or not isinstance(evaluation.get("soft"), dict)
            or not evaluation.get("soft")
            or evaluation.get("recommended_action") not in _RECOMMENDED_ACTIONS
        ):
            issues.append(Issue(
                artifact_id,
                "concept-review-invalid",
                f"{concept.get('id')} lacks reviewer-owned evaluation",
            ))

    terminal_present = any(
        concept.get("decision") in _TERMINAL_DECISIONS
        for concept in concepts
    )
    exit_block = frontmatter.get("exit")
    exit_present = (
        isinstance(exit_block, dict)
        and isinstance(exit_block.get("selected_concept_ids"), list)
        and bool(exit_block["selected_concept_ids"])
    )
    if status != "ready" and (terminal_present or exit_present):
        issues.append(Issue(
            artifact_id,
            "concept-review-not-ready",
            "human Concept decisions require review.status ready",
        ))
    return issues


def _concept_source_issues(artifact_id: str, concept_id: str, concept: dict, pool: dict) -> list[Issue]:
    seed_id = concept.get("source_seed_id")
    area_id = concept.get("opportunity_area_id")
    for pool_area_id, seed in _seeds(pool):
        if seed.get("id") != seed_id:
            continue
        group = next(
            (candidate for candidate in _pool_groups(pool) if candidate.get("opportunity_area_id") == pool_area_id),
            {},
        )
        shortlist = group.get("shortlist") if isinstance(group.get("shortlist"), dict) else {}
        issues: list[Issue] = []
        if area_id != pool_area_id:
            issues.append(Issue(artifact_id, "concept-oa-mismatch", f"{concept_id} OA does not match source seed {seed_id}"))
        confirmed = shortlist.get("confirmed")
        if not isinstance(confirmed, list) or seed_id not in confirmed:
            issues.append(Issue(artifact_id, "seed-not-confirmed", f"{concept_id} develops unconfirmed seed {seed_id}"))
        return issues
    return [Issue(artifact_id, "concept-source-unresolved", f"{concept_id} source seed {seed_id!r} does not resolve")]


def _concept_content_issues(artifact_id: str, concept_id: str, concept: dict) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(concept.get("item_revision"), int) or concept.get("item_revision", 0) < 1:
        issues.append(Issue(artifact_id, "concept-item-revision", f"{concept_id} has invalid item_revision"))
    for field in _CONCEPT_REQUIRED_FIELDS:
        if not str(concept.get(field, "")).strip():
            issues.append(Issue(artifact_id, "concept-hard-field", f"{concept_id} missing {field}"))
    if not isinstance(concept.get("design_principles"), list) or not concept.get("design_principles"):
        issues.append(Issue(artifact_id, "concept-hard-field", f"{concept_id} missing design_principles"))
    assumption_refs = concept.get("assumption_refs")
    if (
        not isinstance(assumption_refs, list)
        or not assumption_refs
        or any(_ASSUMPTION_REF.fullmatch(str(ref)) is None for ref in assumption_refs)
    ):
        issues.append(Issue(artifact_id, "concept-assumption-ref", f"{concept_id} has invalid assumption_refs"))
    dual_sided = concept.get("dual_sided") if isinstance(concept.get("dual_sided"), dict) else {}
    for side, field in (
        ("money", "commercial_value_proposition"),
        ("money", "leverageable_assets"),
        ("magic", "consumer_value_proposition"),
        ("magic", "consumer_target"),
    ):
        value = (dual_sided.get(side) or {}).get(field)
        if not isinstance(value, dict) or not str(value.get("statement", "")).strip():
            issues.append(Issue(artifact_id, "concept-item-single-sided", f"{concept_id} missing {side}.{field}.statement"))
    tension = dual_sided.get("tension")
    if not isinstance(tension, dict) or not str(tension.get("statement", "")).strip():
        issues.append(Issue(artifact_id, "concept-item-single-sided", f"{concept_id} missing tension.statement"))
    if not str(dual_sided.get("balance_choice", "")).strip():
        issues.append(Issue(artifact_id, "concept-item-single-sided", f"{concept_id} missing balance_choice"))
    return issues


def _has_human_shortlist_confirmation(frontmatter: dict, area_id: Any, confirmed: list[Any]) -> bool:
    decisions = frontmatter.get("decisions")
    if not isinstance(decisions, list):
        return False
    if not all(isinstance(seed_id, str) for seed_id in confirmed):
        return False
    expected = Counter(confirmed)
    return any(
        isinstance(decision, dict)
        and decision.get("type") == "confirm-shortlist"
        and decision.get("opportunity_area_id") == area_id
        and isinstance(decision.get("seed_ids"), list)
        and all(isinstance(seed_id, str) for seed_id in decision["seed_ids"])
        and Counter(decision["seed_ids"]) == expected
        and _is_human_actor(decision.get("decided_by"))
        for decision in decisions
    )


def _is_human_actor(actor: Any) -> bool:
    if not isinstance(actor, dict):
        return False
    actor_type = str(actor.get("type", actor.get("authority", "human"))).lower()
    if actor_type in {"ai", "agent", "system", "assistant", "reviewer"}:
        return False
    person = str(actor.get("name", actor.get("person", ""))).strip()
    role = str(actor.get("role", "")).strip()
    return bool(person and role) and re.search(
        r"\b(ai|agent|system|assistant|model|bot)\b",
        person.lower(),
    ) is None


def _human_decisions(frontmatter: dict) -> dict[str, set[str]]:
    decisions: dict[str, set[str]] = defaultdict(set)
    raw_decisions = frontmatter.get("decisions")
    if not isinstance(raw_decisions, list):
        return decisions
    for decision in raw_decisions:
        if not isinstance(decision, dict) or not _is_human_actor(decision.get("decided_by")):
            continue
        for concept_id in decision.get("concept_ids", []):
            if isinstance(concept_id, str):
                decisions[concept_id].add(str(decision.get("type", "")))
    return decisions


def _concept_decision_issues(
    artifact_id: str,
    concept_id: str,
    concept: dict,
    decisions: dict[str, set[str]],
    *,
    strict: bool,
) -> list[Issue]:
    decision = concept.get("decision")
    issues: list[Issue] = []
    if decision in _TERMINAL_DECISIONS and _TERMINAL_DECISIONS[decision] not in decisions.get(concept_id, set()):
        issues.append(Issue(artifact_id, "concept-decision-ownership", f"{concept_id} {decision} has no human decision"))
    if strict and concept.get("merge_into") is not None and (
        decision != "merged" or "merge" not in decisions.get(concept_id, set())
    ):
        issues.append(Issue(
            artifact_id,
            "concept-decision-ownership",
            f"{concept_id} merge_into has no matching human merge decision",
        ))
    evaluation = concept.get("evaluation")
    hard = evaluation.get("hard") if isinstance(evaluation, dict) else None
    if decision == "selected" and (not isinstance(hard, dict) or not hard or not all(bool(value) for value in hard.values())):
        issues.append(Issue(artifact_id, "selected-before-hard-pass", f"{concept_id} selected before hard criteria pass"))
    return issues


def _exit_issues(artifact_id: str, frontmatter: dict, concepts: list[dict]) -> list[Issue]:
    exit_block = frontmatter.get("exit")
    if not isinstance(exit_block, dict):
        return []
    selected = exit_block.get("selected_concept_ids")
    if not isinstance(selected, list):
        return [Issue(artifact_id, "concept-exit-count", "selected_concept_ids must be a list")]
    if not selected:
        return []
    issues: list[Issue] = []
    if not 2 <= len(selected) <= 4:
        issues.append(Issue(artifact_id, "concept-exit-count", "Ideate handoff requires 2-4 selected concepts"))
    actual = {concept.get("id") for concept in concepts if concept.get("decision") == "selected"}
    if set(selected) != actual:
        issues.append(Issue(artifact_id, "exit-decision-mismatch", "selected_concept_ids differs from item decisions"))
    return issues
