"""Schema-agnostic artifact revision-chain integrity checks."""
from __future__ import annotations


def check_artifacts(records: list[dict]) -> dict:
    """Check artifact revision chains and return their unique heads.

    Each record supplies ``id``, ``revision``, and optionally a ``supersedes``
    mapping.  Only references to revisions of the same artifact participate in
    the chain; cross-artifact references are intentionally ignored.
    """
    errors: list[str] = []
    by_id: dict[str, dict[int, dict]] = {}

    for record in records:
        artifact_id = record["id"]
        revision = record["revision"]
        revisions = by_id.setdefault(artifact_id, {})
        if revision in revisions:
            errors.append(f"duplicate revision: {artifact_id} r{revision}")
            continue
        revisions[revision] = record

    heads: dict[str, int] = {}
    for artifact_id, revisions in by_id.items():
        predecessors: dict[int, int] = {}
        superseded: set[int] = set()
        for revision, record in revisions.items():
            target = record.get("supersedes")
            if not isinstance(target, dict) or target.get("id") != artifact_id:
                continue
            predecessor = target.get("revision")
            if predecessor is None:
                errors.append(
                    f"malformed supersedes: {artifact_id} r{revision} missing revision"
                )
                continue
            if predecessor not in revisions:
                errors.append(
                    f"missing predecessor: {artifact_id} r{revision} -> r{predecessor}"
                )
                continue
            predecessors[revision] = predecessor
            superseded.add(predecessor)

        _add_cycle_errors(artifact_id, predecessors, errors)
        artifact_heads = set(revisions) - superseded
        if len(artifact_heads) != 1:
            errors.append(
                f"invalid head count: {artifact_id} has {len(artifact_heads)} heads"
            )
        else:
            heads[artifact_id] = artifact_heads.pop()

    if errors:
        heads = {}
    return {"ok": not errors, "errors": errors, "heads": heads}


def _add_cycle_errors(
    artifact_id: str, predecessors: dict[int, int], errors: list[str]
) -> None:
    checked: set[int] = set()
    for start in predecessors:
        if start in checked:
            continue
        path: set[int] = set()
        current = start
        while current in predecessors and current not in checked:
            if current in path:
                errors.append(f"cycle: {artifact_id} r{current}")
                break
            path.add(current)
            current = predecessors[current]
        checked.update(path)
