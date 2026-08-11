"""Validation for Opportunity -> Idea Pool -> Concept Portfolio lineage.

Item identifiers are local to their owning append-only artifact chain.  The
module resolves exact artifact revisions and never accepts legacy lifecycle
names or fragment-style global references.
"""
from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterable
from typing import Any

from . import schema

Issue = schema.Issue
Artifact = tuple[schema.ArtifactMeta, dict]

_POOL = schema.ArtifactKind.idea_pool
_PORTFOLIO = schema.ArtifactKind.concept_portfolio
_OPPORTUNITY = schema.ArtifactKind.opportunity
_TERMINAL_DECISIONS = {"selected": "select", "killed": "kill", "merged": "merge"}
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
        if len(seeds) < 10:
            issues.append(Issue(meta.artifact_id, "seed-count", f"{area_id} has {len(seeds)} seeds (minimum 10)"))

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
        for key in ("recommended", "confirmed"):
            values = shortlist.get(key)
            if not isinstance(values, list):
                issues.append(Issue(meta.artifact_id, "shortlist-missing", f"{area_id} shortlist.{key} must be a list"))
                continue
            for seed_id in values:
                if not isinstance(seed_id, str) or seed_id not in local_ids:
                    issues.append(Issue(meta.artifact_id, "shortlist-source-unresolved", f"{key} seed {seed_id!r} is not in {area_id}"))
        confirmed = shortlist.get("confirmed")
        if (
            isinstance(confirmed, list)
            and confirmed
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
        issues.extend(_concept_decision_issues(meta.artifact_id, concept_id, concept, decisions))

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
        if seed_id not in shortlist.get("confirmed", []):
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
    expected = set(confirmed)
    return any(
        isinstance(decision, dict)
        and decision.get("type") == "confirm-shortlist"
        and decision.get("opportunity_area_id") == area_id
        and isinstance(decision.get("seed_ids"), list)
        and all(isinstance(seed_id, str) for seed_id in decision["seed_ids"])
        and set(decision["seed_ids"]) == expected
        and _is_human_actor(decision.get("decided_by"))
        for decision in decisions
    )


def _is_human_actor(actor: Any) -> bool:
    if not isinstance(actor, dict):
        return False
    actor_type = str(actor.get("type", actor.get("authority", "human"))).lower()
    if actor_type in {"ai", "agent", "system", "assistant"}:
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
) -> list[Issue]:
    decision = concept.get("decision")
    issues: list[Issue] = []
    if decision in _TERMINAL_DECISIONS and _TERMINAL_DECISIONS[decision] not in decisions.get(concept_id, set()):
        issues.append(Issue(artifact_id, "concept-decision-ownership", f"{concept_id} {decision} has no human decision"))
    hard = (concept.get("evaluation") or {}).get("hard")
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
