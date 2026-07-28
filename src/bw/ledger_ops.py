"""Assumption-ledger write path: add / update / validate_one.

This is the single write boundary for the assumption ledger. Every gate,
capability, and the bw-ledger skill (Plan B) that mutates assumptions must go
through these functions so the three invariants are enforced consistently.

- add:      build an Assumption, assign A-NNN, enforce invariants, persist.
- update:   apply changes, recompute (is_achilles_heel is derived), enforce, persist.
- validate_one: return invariant violations for one assumption WITHOUT raising.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import io, paths, schema
from .errors import ValidationError

_ID_RE = re.compile(r"^A-(\d+)$")

_DEFAULTS = {
    "validation_status": "open",
    "evidence_level": "L1",
    "status": "active",
    "derived_from": [],
    "affects": [],
}


def _existing_ids(ledger: schema.Ledger) -> set[str]:
    return {a.id for a in ledger.assumptions}


def _max_suffix(ledger: schema.Ledger) -> int:
    """Largest numeric suffix across all stored A-NNN ids; 0 if none."""
    hi = 0
    for a in ledger.assumptions:
        m = _ID_RE.match(a.id or "")
        if m:
            hi = max(hi, int(m.group(1)))
    return hi


def _next_id(ledger: schema.Ledger) -> str:
    return f"A-{_max_suffix(ledger) + 1:03d}"


def add(root: Path, fields: dict) -> schema.Assumption:
    """Append a new assumption to the ledger.

    Assigns ``A-NNN`` (max existing suffix + 1, starting at 001) unless
    ``fields`` carries an explicit non-colliding ``id``. Applies defaults,
    enforces invariants (raises ``ValidationError``), and persists.
    """
    ledger = io.load_ledger(root)
    existing = _existing_ids(ledger)

    if "id" in fields and fields["id"] is not None:
        new_id = fields["id"]
        if new_id in existing:
            raise ValidationError(f"add: id {new_id!r} already exists in ledger")
    else:
        new_id = _next_id(ledger)
        # Defensive: the generated id must never collide.
        if new_id in existing:
            raise ValidationError(f"add: generated id {new_id!r} collides")

    payload = dict(fields)
    payload["id"] = new_id
    for key, default in _DEFAULTS.items():
        payload.setdefault(key, default)

    assumption = schema.Assumption.from_dict(payload)
    assumption.check_invariants()

    ledger.assumptions.append(assumption)
    io.save_ledger(root, ledger)
    return assumption


def update(root: Path, id: str, changes: dict) -> schema.Assumption:
    """Apply ``changes`` to the assumption identified by ``id``.

    Recomputes derived state (``is_achilles_heel`` tracks impact/uncertainty
    automatically), re-enforces invariants, and persists. Raises ``KeyError``
    if ``id`` is absent or ``ValidationError`` if the change introduces a
    colliding id.
    """
    ledger = io.load_ledger(root)

    target: schema.Assumption | None = None
    for a in ledger.assumptions:
        if a.id == id:
            target = a
            break
    if target is None:
        raise KeyError(id)

    if "id" in changes and changes["id"] != id:
        new_id = changes["id"]
        if any(a.id == new_id for a in ledger.assumptions):
            raise ValidationError(f"update: id {new_id!r} already exists in ledger")

    merged = target.to_dict()
    merged.update(changes)
    # Drop keys that are not Assumption fields (defensive — keeps from_dict clean).
    valid_keys = set(target.to_dict().keys())
    rebuilt = schema.Assumption.from_dict({k: v for k, v in merged.items() if k in valid_keys})
    rebuilt.check_invariants()

    for i, a in enumerate(ledger.assumptions):
        if a.id == id:
            ledger.assumptions[i] = rebuilt
            break
    io.save_ledger(root, ledger)
    return rebuilt


def validate_one(root: Path, id: str) -> list[str]:
    """Return invariant-violation messages for the assumption ``id``.

    Does not raise on invariant violations (returns them instead). Raises
    ``KeyError`` if ``id`` is not in the ledger.
    """
    ledger = io.load_ledger(root)
    target: schema.Assumption | None = None
    for a in ledger.assumptions:
        if a.id == id:
            target = a
            break
    if target is None:
        raise KeyError(id)

    return target.invariant_violations()


def _neighbors(node: schema.Assumption, direction: str,
               by_id: dict[str, schema.Assumption]) -> list[str]:
    """Return the ids directly reachable from ``node`` in ``direction``.

    upstream   -> follow ``derived_from`` (what this depends on).
    downstream -> follow ``affects`` AND reverse-``derived_from`` (anything
                  that lists this id in its derived_from, plus what this id
                  lists in affects).
    """
    if direction == "upstream":
        return list(node.derived_from)
    # downstream
    out = list(node.affects)
    for cand in by_id.values():
        if node.id in cand.derived_from and cand.id not in out:
            out.append(cand.id)
    return out


def trace(root: Path, id: str, direction: str = "upstream") -> list[str]:
    """Return the ordered list of assumption ids reachable from ``id``.

    Iterative DFS over the lineage graph (excluding ``id`` itself).
    - upstream   follows ``derived_from``.
    - downstream follows ``affects`` and reverse-``derived_from``.

    Raises:
        ValidationError("dangling reference: <id>") if any referenced id is
            absent from the ledger.
        ValidationError("lineage cycle: ...") if the walk revisits an id.
        KeyError if ``id`` itself is not in the ledger.
    """
    if direction not in ("upstream", "downstream"):
        raise ValueError(f"trace: direction must be 'upstream' or 'downstream', got {direction!r}")

    ledger = io.load_ledger(root)
    by_id = {a.id: a for a in ledger.assumptions}
    if id not in by_id:
        raise KeyError(id)

    visited: set[str] = set()
    order: list[str] = []

    def _walk(start: str) -> None:
        # Iterative DFS that detects a real cycle via a gray (on-stack) set.
        # Stack frames: (id, neighbor_iterator, path). We recurse depth-first so
        # a true back-edge (neighbor on the current DFS path) is a cycle; a
        # node reached again after a *completed* subtree (diamond) is not.
        stack: list[tuple[str, list[str], int, list[str]]] = [
            (start, _neighbors(by_id[start], direction, by_id), 0, [start])
        ]
        gray: set[str] = {start}
        while stack:
            cur_id, neighbors, idx, path = stack[-1]
            if cur_id != id and cur_id not in visited:
                visited.add(cur_id)
                order.append(cur_id)
            if idx < len(neighbors):
                stack[-1] = (cur_id, neighbors, idx + 1, path)
                nxt = neighbors[idx]
                if nxt not in by_id:
                    raise ValidationError(f"dangling reference: {nxt}")
                if nxt in gray:
                    # Back-edge to a node on the current DFS path -> real cycle.
                    cycle = path[path.index(nxt):] + [nxt] if nxt in path else [nxt, nxt]
                    raise ValidationError(f"lineage cycle: {' -> '.join(cycle)}")
                if nxt in visited:
                    continue  # already fully explored via another branch (diamond)
                gray.add(nxt)
                stack.append((nxt, _neighbors(by_id[nxt], direction, by_id), 0, path + [nxt]))
            else:
                gray.discard(cur_id)
                stack.pop()

    _walk(id)
    return order


# --- Task 8: baseline + backtrack (回溯治理 routing) ---

# Layer -> (loop_type, depth_target). feature/concept are small loops back to
# the reframe step; opportunity/strategy are large loops back to Define; root is
# a large loop all the way back to Discover.
_LAYER_LOOP = {
    schema.Layer.feature: ("small", "reframe"),
    schema.Layer.concept: ("small", "reframe"),
    schema.Layer.opportunity: ("large", "Define"),
    schema.Layer.strategy: ("large", "Define"),
    schema.Layer.root: ("large", "Discover"),
}


@dataclass
class BacktrackResult:
    """Routing decision returned by :func:`backtrack`.

    - ``loop_type``: "small" (re-pass reframe) or "large" (re-pass an upstream
      stage gate).
    - ``depth_target``: the stage the flow should route to — "reframe" for a
      small loop; "Discover" / "Define" for a large loop.
    - ``affected_ids``: the downstream lineage of the falsified assumption
      (these artifacts become stale at read time via the hash mechanism).
    - ``must_repass_gate``: the original gate label that must be re-passed when
      the failure touches the baseline (e.g. "G2"); ``None`` otherwise.
    """
    loop_type: str
    depth_target: str
    affected_ids: list[str] = field(default_factory=list)
    must_repass_gate: str | None = None


def _assumption_content_hash(assumption: schema.Assumption) -> str:
    """sha256 of a canonical JSON of ``Assumption.to_dict()``.

    Sorting keys makes the hash stable regardless of dict insertion order.
    """
    canonical = json.dumps(assumption.to_dict(), sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode()).hexdigest()


def baseline(root: Path, label: str = "G2") -> dict:
    """Snapshot current state into ``ledger.baseline`` and stamp ``label``.

    The snapshot has two sections::

        {assumptions: {<assumption_id>: <content_hash>},
         artifacts:    {<artifact_id>:   <meta.hash>}}

    Assumption content_hash is sha256 of the canonical JSON of
    ``Assumption.to_dict()``; artifact hash is the artifact's ``meta.hash``
    (read via ``io.read_artifact`` across ``paths.artifacts_dir``). Persists via
    ``io.save_ledger`` and returns the snapshot.
    """
    ledger = io.load_ledger(root)

    assumptions = {
        a.id: _assumption_content_hash(a) for a in ledger.assumptions if a.id
    }

    artifacts: dict[str, str] = {}
    art_dir = paths.artifacts_dir(root)
    if art_dir.is_dir():
        seen: set[Path] = set()
        for p in sorted(art_dir.rglob("*.md")):
            rp = p.resolve()
            if rp in seen:
                continue
            seen.add(rp)
            try:
                meta, _ = io.read_artifact(p)
            except (FileNotFoundError, ValueError):
                continue
            if meta.artifact_id:
                artifacts[meta.artifact_id] = meta.hash

    snapshot = {"assumptions": assumptions, "artifacts": artifacts}
    ledger.baseline = snapshot
    ledger.last_baselined_at = label
    io.save_ledger(root, ledger)
    return snapshot


def backtrack(root: Path, falsified_id: str) -> BacktrackResult:
    """Route the flow to the right upstream stage for a falsified assumption.

    The depth of the loop is decided by the failed assumption's ``layer``:
    ``feature|concept`` -> small loop (``reframe``); ``opportunity|strategy`` ->
    large loop (``Define``); ``root`` -> large loop (``Discover``).

    ``affected_ids`` is the downstream lineage via :func:`trace`.

    Baseline-boundary check: if ``ledger.baseline`` is set and either
    ``falsified_id`` or any ``affected_ids`` is a key in the baseline snapshot
    (assumption or artifact section), the loop upgrades to ``large`` and
    ``must_repass_gate`` is set to ``ledger.last_baselined_at`` so the original
    gate is re-passed.

    Raises ``KeyError`` if ``falsified_id`` is not in the ledger.
    """
    ledger = io.load_ledger(root)
    by_id = {a.id: a for a in ledger.assumptions}
    if falsified_id not in by_id:
        raise KeyError(falsified_id)

    falsified = by_id[falsified_id]
    loop_type, depth_target = _LAYER_LOOP.get(falsified.layer, ("large", "Discover"))

    affected_ids = trace(root, falsified_id, "downstream")

    must_repass_gate: str | None = None
    baseline = ledger.baseline
    if baseline:
        baseline_keys: set[str] = set()
        for section in ("assumptions", "artifacts"):
            section_map = baseline.get(section) or {}
            baseline_keys.update(section_map.keys())
        touched = falsified_id in baseline_keys or any(
            aid in baseline_keys for aid in affected_ids
        )
        if touched:
            loop_type = "large"
            must_repass_gate = ledger.last_baselined_at

    return BacktrackResult(
        loop_type=loop_type,
        depth_target=depth_target,
        affected_ids=affected_ids,
        must_repass_gate=must_repass_gate,
    )
