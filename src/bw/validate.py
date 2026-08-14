"""System-wide health check: ``validate_all(root) -> list[Issue]``.

This is the single command that scans the whole ``_bewater/`` tree (the
assumption ledger plus every artifact) and reports every problem it finds:

- ``invariant-violation``  — an assumption breaks an invariant.
- ``dangling-ref``         — a ``derived_from``/``affects`` id resolves to no
                             assumption and no artifact.
- ``cycle``                — the assumption lineage graph has a cycle.
- ``single-sided``         — a dual-sided artifact is missing one of its four
                             money/magic elements.
- ``missing-final``        — an artifact is referenced as a dependency but its
                             status is not ``final``.
- ``malformed-frontmatter``— an artifact's frontmatter has no closing fence.

An empty return value means clean. Gates (T10) and the bw-ledger/bw-resume
skills call this to decide whether state is healthy.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import evidence, io, ledger_ops, paths, schema
from .concept_lifecycle import concept_issues
from .errors import ValidationError
from .signoffs import has_fpet_signoff
from .solution_contract import solution_issues

# ``Issue`` is defined on schema so the lifecycle module can share it without a
# circular import; re-export the historic ``validate.Issue`` symbol.
Issue = schema.Issue

# Kinds whose frontmatter must carry a complete dual-sided block.
_DUAL_SIDED_KINDS = {
    schema.ArtifactKind.charter,
    schema.ArtifactKind.directional_hypothesis,
}

# The four dual-sided elements that must all be non-empty.
_DUAL_SIDED_PATHS = (
    ("money", "commercial_value_proposition"),
    ("money", "leverageable_assets"),
    ("magic", "consumer_value_proposition"),
    ("magic", "consumer_target"),
)

_ARTIFACT_REF = re.compile(r"^artifact:([^@]+)@(\d+)$")
_ASSUMPTION_REF = re.compile(r"^assumption:(A-\d{3})@([1-9]\d*)$")


def _iter_artifacts(root: Path):
    """Yield the Path of each readable ``.md`` artifact under _bewater-output/.

    Malformed files are yielded too (the caller's read surfaces a
    malformed-frontmatter Issue); only unreadable duplicates are skipped.
    """
    yield from paths.iter_workflow_documents(root)


def _single_sided_violations(meta: schema.ArtifactMeta) -> list[str]:
    """Return a message for each empty dual-sided element of ``meta``."""
    if meta.kind not in _DUAL_SIDED_KINDS:
        return []
    out: list[str] = []
    block = meta.dual_sided or {}
    for section, key in _DUAL_SIDED_PATHS:
        value = (block.get(section) or {}).get(key)
        if not value or not str(value).strip():
            out.append(f"{meta.artifact_id}: empty dual-sided element {section}.{key}")
    return out


def _reference_exists(
    ref: str,
    assumptions: dict[str, schema.Assumption],
    artifact_revisions: set[tuple[str, int]],
) -> bool:
    artifact_match = _ARTIFACT_REF.match(ref)
    if artifact_match is not None:
        return (artifact_match.group(1), int(artifact_match.group(2))) in artifact_revisions
    assumption_match = _ASSUMPTION_REF.match(ref)
    if assumption_match is not None:
        assumption = assumptions.get(assumption_match.group(1))
        if assumption is None:
            return False
        revision = int(assumption_match.group(2))
        if assumption.record_revision == revision:
            return True
        return any(
            isinstance(snapshot, dict) and snapshot.get("record_revision") == revision
            for snapshot in assumption.history
        )
    return False


def _resolved_artifact_entries(
    refs: list[str],
    artifacts_by_revision: dict[tuple[str, int], tuple[schema.ArtifactMeta, dict]],
) -> list[tuple[schema.ArtifactMeta, dict]]:
    resolved: list[tuple[schema.ArtifactMeta, dict]] = []
    for ref in refs:
        match = _ARTIFACT_REF.match(ref)
        if match is None:
            continue
        entry = artifacts_by_revision.get((match.group(1), int(match.group(2))))
        if entry is not None:
            resolved.append(entry)
    return resolved


def _derives_from_artifact_chain(
    assumption: schema.Assumption,
    artifact_id: str,
    through_revision: int,
) -> bool:
    return any(
        match is not None
        and match.group(1) == artifact_id
        and int(match.group(2)) <= through_revision
        for ref in assumption.derived_from
        for match in [_ARTIFACT_REF.match(ref)]
    )


def _concept_assumption_issues(
    structured_artifacts: list[tuple[schema.ArtifactMeta, dict, str]],
    assumptions: list[schema.Assumption],
) -> list[Issue]:
    issues: list[Issue] = []
    for meta, frontmatter, _ in structured_artifacts:
        if meta.kind != schema.ArtifactKind.concept_portfolio:
            continue
        concepts = frontmatter.get("concepts")
        if not isinstance(concepts, list):
            continue
        for concept in concepts:
            if not isinstance(concept, dict) or not isinstance(concept.get("id"), str):
                continue
            concept_id = concept["id"]
            expected = {
                assumption.id: assumption
                for assumption in assumptions
                if assumption.status == schema.AssumptionStatus.active
                and assumption.branch_id == meta.branch_id
                and assumption.layer == schema.Layer.concept
                and assumption.source_concept_id == concept_id
                and _derives_from_artifact_chain(assumption, meta.artifact_id, meta.revision)
            }
            raw_refs = concept.get("assumption_refs")
            parsed: dict[str, int] = {}
            malformed = not isinstance(raw_refs, list)
            if isinstance(raw_refs, list):
                for ref in raw_refs:
                    match = _ASSUMPTION_REF.match(str(ref))
                    if match is None or match.group(1) in parsed:
                        malformed = True
                        continue
                    parsed[match.group(1)] = int(match.group(2))

            pins_match = not malformed and set(parsed) == set(expected)
            if pins_match:
                pins_match = all(
                    parsed[assumption_id] == assumption.record_revision
                    for assumption_id, assumption in expected.items()
                )
            if not pins_match:
                issues.append(Issue(
                    scope=meta.artifact_id,
                    kind="concept-assumption-lineage",
                    message=(
                        f"{concept_id} assumption_refs must exactly pin its active Concept assumptions "
                        f"through artifact:{meta.artifact_id}@{meta.revision}"
                    ),
                ))
    return issues


def validate_all(root: Path) -> list[Issue]:
    """Scan ledger + artifacts and return every Issue found (empty = clean)."""
    issues: list[Issue] = []

    ledger = io.load_ledger(root)
    assumptions = list(ledger.assumptions.values())

    # --- 1. Invariants (single source: schema.Assumption.invariant_violations) ---
    for a in assumptions:
        for msg in a.invariant_violations():
            issues.append(Issue(scope=a.id, kind="invariant-violation", message=msg))
        if (
            a.validation_status == schema.AssumptionValidationStatus.supported
            and not evidence.assumption_refs_resolve(root, a)
        ):
            issues.append(Issue(
                scope=a.id,
                kind="evidence-ref",
                message=(
                    "supported assumption must resolve an exact current active Evidence "
                    "revision on the same branch"
                ),
            ))

    # --- 4 & 6. Artifacts: single-sided + malformed frontmatter ---
    artifact_revisions: set[tuple[str, int]] = set()
    artifacts: list[schema.ArtifactMeta] = []
    structured_artifacts: list[tuple[schema.ArtifactMeta, dict, str]] = []
    for p in _iter_artifacts(root):
        try:
            meta, body = io.read_artifact(p)
            frontmatter = io.read_frontmatter(p)
        except (KeyError, TypeError, ValueError):
            issues.append(Issue(
                scope="ledger",
                kind="malformed-frontmatter",
                message=f"malformed or non-canonical frontmatter: {p}",
            ))
            continue
        if meta.artifact_id:
            artifact_revisions.add((meta.artifact_id, meta.revision))
        artifacts.append(meta)
        structured_artifacts.append((meta, frontmatter, body))
        for msg in _single_sided_violations(meta):
            issues.append(Issue(scope=meta.artifact_id, kind="single-sided", message=msg))
        if (
            meta.kind == schema.ArtifactKind.insights
            and meta.document_status == schema.ArtifactDocumentStatus.final
            and not has_fpet_signoff(meta)
        ):
            issues.append(Issue(
                scope=meta.artifact_id,
                kind="fpet-signoff",
                message="final insights artifact requires current-revision F/P/E/T signoff",
            ))

    # --- 2. Referential integrity (derived_from/affects) ---
    assumptions_by_id = {assumption.id: assumption for assumption in assumptions}
    for a in assumptions:
        for ref in a.derived_from:
            if not _reference_exists(ref, assumptions_by_id, artifact_revisions):
                issues.append(Issue(scope=a.id, kind="dangling-ref",
                                    message=f"derived_from references unknown id {ref!r}"))
        for ref in a.affects:
            if not _reference_exists(ref, assumptions_by_id, artifact_revisions):
                issues.append(Issue(scope=a.id, kind="dangling-ref",
                                    message=f"affects references unknown id {ref!r}"))

    for meta in artifacts:
        for ref in meta.derived_from:
            if not _reference_exists(ref, assumptions_by_id, artifact_revisions):
                issues.append(Issue(
                    scope=meta.artifact_id,
                    kind="dangling-ref",
                    message=f"derived_from references unknown exact revision {ref!r}",
                ))

    artifacts_by_revision = {
        (meta.artifact_id, meta.revision): (meta, frontmatter)
        for meta, frontmatter, _ in structured_artifacts
    }
    for assumption in assumptions:
        resolved_sources = _resolved_artifact_entries(
            assumption.derived_from,
            artifacts_by_revision,
        )
        if assumption.layer == schema.Layer.concept:
            portfolios = [
                frontmatter
                for meta, frontmatter in resolved_sources
                if meta.kind == schema.ArtifactKind.concept_portfolio
            ]
            concept_id = assumption.source_concept_id
            concept_resolves = isinstance(concept_id, str) and concept_id.startswith("CI-") and any(
                any(
                    isinstance(concept, dict) and concept.get("id") == concept_id
                    for concept in (frontmatter.get("concepts") or [])
                )
                for frontmatter in portfolios
            )
            if not concept_resolves:
                issues.append(Issue(
                    scope=assumption.id,
                    kind="assumption-lineage",
                    message="concept assumption must resolve source_concept_id in an exact Concept Portfolio revision",
                ))
        elif assumption.layer == schema.Layer.solution:
            if not any(
                meta.kind == schema.ArtifactKind.solution
                for meta, _ in resolved_sources
            ):
                issues.append(Issue(
                    scope=assumption.id,
                    kind="assumption-lineage",
                    message="solution assumption must derive from an exact Solution revision",
                ))

    issues.extend(_concept_assumption_issues(structured_artifacts, assumptions))

    # --- 3. Cycles (dedup: one cycle issue per run; either direction) ---
    # Lineage must be acyclic in BOTH directions: a cycle formed solely via
    # `affects` edges (downstream) is invisible to an upstream-only walk, so we
    # trace each assumption in both directions and surface a single cycle Issue.
    cycle_seen = False
    for direction in ("upstream", "downstream"):
        for a in assumptions:
            try:
                ledger_ops.trace(root, a.id, direction)
            except ValidationError as exc:
                if str(exc).startswith("lineage cycle") and not cycle_seen:
                    issues.append(Issue(scope="ledger", kind="cycle", message=str(exc)))
                    cycle_seen = True
                # dangling references surfaced by trace are already covered above.

    # --- 5. Missing-final dependencies ---
    referenced: set[str] = set()
    for meta in artifacts:
        referenced.update(meta.derived_from)
    by_revision = {
        (meta.artifact_id, meta.revision): meta
        for meta in artifacts
        if meta.artifact_id
    }
    for dependency_ref in sorted(referenced):
        match = _ARTIFACT_REF.match(dependency_ref)
        dep = (
            by_revision.get((match.group(1), int(match.group(2))))
            if match is not None
            else None
        )
        if dep is not None and dep.document_status != schema.ArtifactDocumentStatus.final:
            issues.append(Issue(
                scope=dep.artifact_id,
                kind="missing-final",
                message=f"{dependency_ref} is referenced as a dependency but status is "
                        f"{dep.document_status.value!r}, not 'final'",
            ))

    # --- 7. Canonical Idea -> Concept -> Solution contracts ---
    issues.extend(concept_issues([(meta, frontmatter) for meta, frontmatter, _ in structured_artifacts]))
    issues.extend(solution_issues(structured_artifacts, ledger))

    return issues
