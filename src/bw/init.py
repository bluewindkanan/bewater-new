"""`bw init` — scaffold the `_bewater/` project tree.

Creates the canonical directory layout and an empty assumption ledger.
Idempotent: re-running on an existing tree is a no-op (the ledger is only
written if absent, unless `force` is set).
"""
from __future__ import annotations

from pathlib import Path

from . import io, schema
from .paths import artifacts_dir, ledger_path

# Per-stage artifact subdirs (new in T4 — no existing path helper covers them).
STAGE_ARTIFACT_DIRS = ("immersion", "discover", "define", "ideate", "shape", "handoff")

_BEWATER = "_bewater"


def _empty_ledger(root: Path) -> schema.Ledger:
    return schema.Ledger(project=root.name, last_baselined_at=None, baseline=None)


def scaffold(root: Path, force: bool = False) -> None:
    """Create the `_bewater/` tree under `root` and an empty ledger.

    Directories are created unconditionally (mkdir -p semantics). The ledger is
    written only when it does not already exist, unless `force` rewrites it.
    Returns None; success is the absence of an exception.
    """
    root = Path(root)

    (root / _BEWATER / "state" / "gates").mkdir(parents=True, exist_ok=True)
    (root / _BEWATER / "knowledge-base").mkdir(parents=True, exist_ok=True)
    # Touch the canonical artifact dirs and per-stage subdirs.
    artifacts_dir(root).mkdir(parents=True, exist_ok=True)
    for stage in STAGE_ARTIFACT_DIRS:
        (artifacts_dir(root) / stage).mkdir(parents=True, exist_ok=True)

    if force or not ledger_path(root).exists():
        io.save_ledger(root, _empty_ledger(root))
