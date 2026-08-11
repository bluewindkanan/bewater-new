"""Shared signoff predicates for gate and validation checks."""
from __future__ import annotations

from typing import Any

from . import schema

_FPET_COMPONENTS = {"fresh", "potent", "energizing", "truth"}


def has_fpet_signoff(meta: schema.ArtifactMeta) -> bool:
    signoffs = meta.signoffs or []
    if any(
        isinstance(signoff, dict)
        and str(signoff.get("what", "")).strip().upper() == "F/P/E/T"
        for signoff in signoffs
    ):
        return True
    if any(
        isinstance(signoff, dict)
        and str(signoff.get("type", "")).strip().lower() == "fpet"
        for signoff in signoffs
    ):
        return True
    return _signed_components(signoffs) == _FPET_COMPONENTS


def _signed_components(signoffs: list[Any]) -> set[str]:
    out: set[str] = set()
    for signoff in signoffs:
        if not isinstance(signoff, dict):
            continue
        what = str(signoff.get("what", "")).strip().lower()
        if what in _FPET_COMPONENTS:
            out.add(what)
    return out
