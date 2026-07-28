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

An empty return value means clean. Gates (T10) and the bw-ledger/bw-start
skills call this to decide whether state is healthy.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import io, ledger_ops, paths, schema
from .errors import ValidationError

# Kinds whose frontmatter must carry a complete dual-sided block.
_DUAL_SIDED_KINDS = {
    schema.ArtifactKind.charter,
    schema.ArtifactKind.directional_hypothesis,
    schema.ArtifactKind.concept,
    schema.ArtifactKind.solution,
}

# The four dual-sided elements that must all be non-empty.
_DUAL_SIDED_PATHS = (
    ("money", "commercial_value_proposition"),
    ("money", "leverageable_assets"),
    ("magic", "consumer_value_proposition"),
    ("magic", "consumer_target"),
)


@dataclass(frozen=True)
class Issue:
    """A single problem found by :func:`validate_all`.

    ``scope`` is the artifact_id, assumption id, or the literal ``"ledger"``.
    ``kind`` is one of the module docstring's categories. ``message`` is a
    human-readable detail string.
    """
    scope: str
    kind: str
    message: str


def _iter_artifacts(root: Path):
    """Yield ``(path, ArtifactMeta)`` for every readable .md under artifacts/.

    Skips files whose frontmatter is malformed, yielding them via the caller's
    malformed-frontmatter handling instead.
    """
    art_dir = paths.artifacts_dir(root)
    if not art_dir.is_dir():
        return
    seen: set[Path] = set()
    for p in sorted(art_dir.rglob("*.md")):
        rp = p.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        yield p


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


def validate_all(root: Path) -> list[Issue]:
    """Scan ledger + artifacts and return every Issue found (empty = clean)."""
    issues: list[Issue] = []

    ledger = io.load_ledger(root)
    assumptions = ledger.assumptions

    # --- 1. Invariants (single source: schema.Assumption.invariant_violations) ---
    for a in assumptions:
        for msg in a.invariant_violations():
            issues.append(Issue(scope=a.id, kind="invariant-violation", message=msg))

    # --- 4 & 6. Artifacts: single-sided + malformed frontmatter ---
    artifact_ids: set[str] = set()
    artifacts: list[schema.ArtifactMeta] = []
    for p in _iter_artifacts(root):
        try:
            meta, _ = io.read_artifact(p)
        except ValueError:
            issues.append(Issue(
                scope="ledger",
                kind="malformed-frontmatter",
                message=f"malformed frontmatter (no closing fence): {p}",
            ))
            continue
        if meta.artifact_id:
            artifact_ids.add(meta.artifact_id)
        artifacts.append(meta)
        for msg in _single_sided_violations(meta):
            issues.append(Issue(scope=meta.artifact_id, kind="single-sided", message=msg))

    # --- 2. Referential integrity (derived_from/affects) ---
    known = {a.id for a in assumptions} | artifact_ids
    for a in assumptions:
        for ref in a.derived_from:
            if ref not in known:
                issues.append(Issue(scope=a.id, kind="dangling-ref",
                                    message=f"derived_from references unknown id {ref!r}"))
        for ref in a.affects:
            if ref not in known:
                issues.append(Issue(scope=a.id, kind="dangling-ref",
                                    message=f"affects references unknown id {ref!r}"))

    # --- 3. Cycles (dedup: one cycle issue per run) ---
    cycle_seen = False
    for a in assumptions:
        try:
            ledger_ops.trace(root, a.id, "upstream")
        except ValidationError as exc:
            if str(exc).startswith("lineage cycle"):
                if not cycle_seen:
                    issues.append(Issue(scope="ledger", kind="cycle", message=str(exc)))
                    cycle_seen = True
            # dangling references surfaced by trace are already covered above.

    # --- 5. Missing-final dependencies ---
    referenced: set[str] = set()
    for meta in artifacts:
        referenced.update(meta.derived_from)
    by_id = {m.artifact_id: m for m in artifacts if m.artifact_id}
    for dep_id in sorted(referenced):
        dep = by_id.get(dep_id)
        if dep is not None and dep.status != schema.ArtifactStatus.final:
            issues.append(Issue(
                scope=dep_id,
                kind="missing-final",
                message=f"{dep_id} is referenced as a dependency but status is "
                        f"{dep.status.value!r}, not 'final'",
            ))

    return issues
