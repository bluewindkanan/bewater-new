"""Shared helpers for installer tests (Phase 1 install.sh). Not shipped."""
from __future__ import annotations

import json
from pathlib import Path

MARKER = ".bewater-managed"


def write_managed_marker(target, *, version, source="bewater"):
    (Path(target) / MARKER).write_text(
        json.dumps({"managed_by": source, "version": version}))


def has_managed_marker(target) -> bool:
    return (Path(target) / MARKER).exists()
