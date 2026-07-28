"""Assumption-ledger write path: add / update / validate_one.

This is the single write boundary for the assumption ledger. Every gate,
capability, and the bw-ledger skill (Plan B) that mutates assumptions must go
through these functions so the three invariants are enforced consistently.

- add:      build an Assumption, assign A-NNN, enforce invariants, persist.
- update:   apply changes, recompute (is_achilles_heel is derived), enforce, persist.
- validate_one: return invariant violations for one assumption WITHOUT raising.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import io, schema
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

    violations: list[str] = []
    if (
        target.is_achilles_heel
        and target.validation_status == schema.ValidationStatus.validated
        and target.evidence_level < schema.EvidenceLevel.L4
    ):
        violations.append(
            f"Assumption {target.id}: achilles heel validated below L4 "
            f"(got {target.evidence_level.value})"
        )
    return violations
