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

import yaml

from . import io, paths, schema
from .errors import ValidationError

_ID_RE = re.compile(r"^A-(\d+)$")

_DEFAULTS = {
    "validation_status": "untested",
    "evidence_level": "L1",
    "status": "active",
    "evidence_refs": [],
    "derived_from": [],
    "affects": [],
}
def _existing_ids(ledger: schema.Ledger) -> set[str]:
    return set(ledger.assumptions.keys())


def _max_suffix(ledger: schema.Ledger) -> int:
    """Largest numeric suffix across all stored A-NNN ids; 0 if none."""
    hi = 0
    for aid in ledger.assumptions:
        m = _ID_RE.match(aid or "")
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
        if new_id in existing:
            raise ValidationError(f"add: generated id {new_id!r} collides")

    payload = dict(fields)
    payload["id"] = new_id
    for key, default in _DEFAULTS.items():
        payload.setdefault(key, default)

    assumption = schema.Assumption.from_dict(payload)
    assumption.check_invariants()

    ledger.assumptions[new_id] = assumption
    ledger.next_id = _max_suffix(ledger) + 1
    ledger.revision += 1
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

    if id not in ledger.assumptions:
        raise KeyError(id)

    target = ledger.assumptions[id]

    if "id" in changes and changes["id"] != id:
        new_id = changes["id"]
        if new_id in ledger.assumptions:
            raise ValidationError(f"update: id {new_id!r} already exists in ledger")

    valid_keys = set(target.to_dict())
    unknown = set(changes) - valid_keys
    if unknown:
        raise ValidationError(f"update: unknown field(s): {', '.join(sorted(unknown))}")

    previous = target.to_dict()
    previous.pop("history", None)
    merged = target.to_dict()
    merged.update(changes)
    merged["record_revision"] = target.record_revision + 1
    merged["history"] = [*target.history, previous]
    rebuilt = schema.Assumption.from_dict({k: v for k, v in merged.items() if k in valid_keys})
    rebuilt.check_invariants()

    # If id changed, delete old key and insert under new key
    if rebuilt.id != id:
        del ledger.assumptions[id]
    ledger.assumptions[rebuilt.id] = rebuilt
    ledger.revision += 1
    io.save_ledger(root, ledger)
    return rebuilt


def validate_one(root: Path, id: str) -> list[str]:
    """Return invariant-violation messages for the assumption ``id``.

    Does not raise on invariant violations (returns them instead). Raises
    ``KeyError`` if ``id`` is not in the ledger.
    """
    ledger = io.load_ledger(root)
    if id not in ledger.assumptions:
        raise KeyError(id)

    return ledger.assumptions[id].invariant_violations()


def _neighbors(node: schema.Assumption, direction: str,
               by_id: dict[str, schema.Assumption]) -> list[str]:
    """Return the ids directly reachable from ``node`` in ``direction``.

    upstream   -> follow ``derived_from`` (what this depends on).
    downstream -> follow ``affects`` AND reverse-``derived_from`` (anything
                  that lists this id in its derived_from, plus what this id
                  lists in affects).
    """
    def assumption_id(ref: str) -> str | None:
        match = re.match(r"^assumption:(A-\d{3})@([1-9]\d*)$", ref)
        if match is not None:
            assumption = by_id.get(match.group(1))
            if assumption is None or assumption.record_revision != int(match.group(2)):
                return ref
            return match.group(1)
        if re.match(
            r"^(?:artifact:[^@]+|evidence:E-\d{3}|experiment:EXP-\d{3})@[1-9]\d*$",
            ref,
        ):
            return None
        return ref

    def reverse_assumption_id(ref: str) -> str | None:
        match = re.match(r"^assumption:(A-\d{3})@[1-9]\d*$", ref)
        if match is not None:
            return match.group(1) if match.group(1) in by_id else ref
        return assumption_id(ref)

    if direction == "upstream":
        return [resolved for ref in node.derived_from if (resolved := assumption_id(ref)) is not None]
    # downstream
    out = [resolved for ref in node.affects if (resolved := assumption_id(ref)) is not None]
    for cand in by_id.values():
        upstream_ids: set[str] = set()
        for ref in cand.derived_from:
            resolved = reverse_assumption_id(ref)
            if resolved is not None and resolved not in by_id:
                raise ValidationError(f"dangling reference: {ref}")
            if resolved is not None:
                upstream_ids.add(resolved)
        if node.id in upstream_ids and cand.id not in out:
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
    by_id = dict(ledger.assumptions)
    if id not in by_id:
        raise KeyError(id)

    visited: set[str] = set()
    order: list[str] = []

    def _walk(start: str) -> None:
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
                    cycle = path[path.index(nxt):] + [nxt] if nxt in path else [nxt, nxt]
                    raise ValidationError(f"lineage cycle: {' -> '.join(cycle)}")
                if nxt in visited:
                    continue
                gray.add(nxt)
                stack.append((nxt, _neighbors(by_id[nxt], direction, by_id), 0, path + [nxt]))
            else:
                gray.discard(cur_id)
                stack.pop()

    _walk(id)
    return order


# --- Task 8: baseline + backtrack ---

_LAYER_LOOP = {
    schema.Layer.feature: ("small", "Shape"),
    schema.Layer.solution: ("small", "Shape"),
    schema.Layer.concept: ("small", "Ideate"),
    schema.Layer.opportunity: ("large", "Define"),
    schema.Layer.strategy: ("large", "Define"),
    schema.Layer.root: ("large", "Discover"),
}


@dataclass
class BacktrackResult:
    """Routing decision returned by :func:`backtrack`.

    - ``loop_type``: "small" (local stage loop) or "large" (re-pass an upstream
      stage gate).
    - ``depth_target``: the stage the flow should route to — "Ideate" / "Shape"
      for a small loop; "Discover" / "Define" for a large loop.
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


def _load_baseline_snapshot(root: Path, label: str | None = None) -> tuple[dict | None, str | None]:
    """Load a baseline snapshot from records/ directory.

    If ``label`` is given, loads that specific baseline file. Otherwise loads
    the latest (by filename sort order, which approximates creation order for
    B-{gate}-baseline.yaml naming).

    Returns (snapshot_dict, gate_label) or (None, None) if no baseline found.
    """
    rec_dir = paths.records_dir(root)
    if not rec_dir.is_dir():
        return None, None

    pattern = re.compile(r"^B-(.+)-baseline\.yaml$")
    candidates: list[tuple[str, Path]] = []
    for p in sorted(rec_dir.iterdir()):
        m = pattern.match(p.name)
        if m:
            candidates.append((m.group(1), p))

    if not candidates:
        return None, None

    if label is not None:
        for gate, p in candidates:
            if gate == label:
                data = yaml.safe_load(p.read_text()) or {}
                return data.get("snapshot"), gate
        return None, None

    def gate_sort_key(candidate: tuple[str, Path]) -> tuple[int, int, str]:
        gate_label = candidate[0]
        match = re.match(r"^G([1-9]\d*)$", gate_label)
        if match is None:
            return (1, 0, gate_label)
        return (0, int(match.group(1)), gate_label)

    gate, p = sorted(candidates, key=gate_sort_key)[-1]
    data = yaml.safe_load(p.read_text()) or {}
    return data.get("snapshot"), gate


def baseline(root: Path, label: str = "G2") -> dict:
    """Snapshot current state and write to ``records/B-{label}-baseline.yaml``.

    The snapshot has two sections::

        {assumptions: {<assumption_id>: <content_hash>},
         artifacts:    {<artifact_id>:   <meta.hash>}}

    Assumption content_hash is sha256 of the canonical JSON of
    ``Assumption.to_dict()``; artifact hash is the artifact's ``meta.hash``
    (read via ``io.read_artifact`` across ``paths.output_dir``). Persists to
    ``records/`` and returns the snapshot.
    """
    ledger = io.load_ledger(root)

    assumptions = {
        aid: _assumption_content_hash(a) for aid, a in ledger.assumptions.items() if aid
    }

    artifacts: dict[str, str] = {}
    for p in paths.iter_workflow_documents(root):
        try:
            meta, _ = io.read_artifact(p)
        except (FileNotFoundError, ValueError):
            continue
        if meta.artifact_id:
            artifacts[meta.artifact_id] = meta.hash

    snapshot = {"assumptions": assumptions, "artifacts": artifacts}

    rec_dir = paths.records_dir(root)
    rec_dir.mkdir(parents=True, exist_ok=True)
    baseline_path = rec_dir / f"B-{label}-baseline.yaml"
    baseline_path.write_text(
        yaml.safe_dump(
            {"gate": label, "snapshot": snapshot},
            sort_keys=False,
            allow_unicode=True,
        )
    )

    return snapshot


def backtrack(root: Path, falsified_id: str) -> BacktrackResult:
    """Route the flow to the right upstream stage for a falsified assumption.

    The depth of the loop is decided by the failed assumption's ``layer``:
    ``concept`` -> small loop to Ideate; ``solution|feature`` -> small loop to
    Shape; ``opportunity|strategy`` -> large loop to Define; ``root`` -> large
    loop to Discover.

    ``affected_ids`` is the downstream lineage via :func:`trace`.

    Baseline-boundary check: scans ``records/`` for the latest baseline file.
    If ``falsified_id`` or any ``affected_ids`` appears in that snapshot, the
    loop upgrades to ``large`` and ``must_repass_gate`` is set to the baseline's
    gate label so the original gate is re-passed.

    Raises ``KeyError`` if ``falsified_id`` is not in the ledger.
    """
    ledger = io.load_ledger(root)
    by_id = dict(ledger.assumptions)
    if falsified_id not in by_id:
        raise KeyError(falsified_id)

    falsified = by_id[falsified_id]
    loop_type, depth_target = _LAYER_LOOP.get(falsified.layer, ("large", "Discover"))

    affected_ids = trace(root, falsified_id, "downstream")

    must_repass_gate: str | None = None
    baseline_snapshot, baseline_gate = _load_baseline_snapshot(root)
    if baseline_snapshot:
        baseline_keys: set[str] = set()
        for section in ("assumptions", "artifacts"):
            section_map = baseline_snapshot.get(section) or {}
            baseline_keys.update(section_map.keys())
        touched = falsified_id in baseline_keys or any(
            aid in baseline_keys for aid in affected_ids
        )
        if touched:
            loop_type = "large"
            must_repass_gate = baseline_gate

    return BacktrackResult(
        loop_type=loop_type,
        depth_target=depth_target,
        affected_ids=affected_ids,
        must_repass_gate=must_repass_gate,
    )
