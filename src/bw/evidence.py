"""Resolution helpers for canonical machine Evidence records."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from .paths import STATE_DIR


_EVIDENCE_REF = re.compile(r"^evidence:(E-\d{3})@([1-9]\d*)$")


def load_envelope(root: Path) -> dict:
    path = Path(root) / STATE_DIR / "evidence.yaml"
    if not path.is_file():
        return {}
    try:
        data = yaml.safe_load(path.read_text()) or {}
    except (OSError, UnicodeError, yaml.YAMLError):
        return {}
    return data if isinstance(data, dict) else {}


def ref_resolves(root: Path, ref: str, *, branch_id: str = "") -> bool:
    """Return whether an exact ref identifies the active Evidence head."""
    match = _EVIDENCE_REF.fullmatch(str(ref))
    if match is None:
        return False
    envelope = load_envelope(root)
    envelope_branch = str(envelope.get("branch_id") or "")
    if branch_id and envelope_branch and branch_id != envelope_branch:
        return False
    records = envelope.get("evidence")
    if not isinstance(records, list):
        return False
    evidence_id, revision_text = match.groups()
    revision = int(revision_text)
    for record in records:
        if not isinstance(record, dict) or record.get("id") != evidence_id:
            continue
        record_branch = str(record.get("branch_id") or envelope_branch)
        try:
            record_revision = int(record.get("record_revision", 0))
        except (TypeError, ValueError):
            return False
        return (
            record_revision == revision
            and record.get("validity", "active") == "active"
            and (not branch_id or not record_branch or record_branch == branch_id)
        )
    return False


def assumption_refs_resolve(root: Path, assumption) -> bool:
    """Return whether an assumption has at least one current active Evidence ref."""
    return any(
        ref_resolves(root, ref, branch_id=assumption.branch_id)
        for ref in assumption.evidence_refs
    )
