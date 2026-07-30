"""`bw init` — scaffold the `_bewater/` project tree.

Creates the canonical directory layout, an empty assumption ledger, and a
project config.  Idempotent: re-running on an existing tree is a no-op (the
ledger and config are only written if absent, unless `force` is set).
"""
from __future__ import annotations

from pathlib import Path

import yaml

from . import io, schema
from .paths import ledger_path, output_dir, records_dir

_BEWATER = "_bewater"


def _empty_ledger() -> schema.Ledger:
    return schema.Ledger()


def _default_config(root: Path) -> dict:
    return {
        "schema_version": 1,
        "revision": 1,
        "active_branch": None,
        "active_execution_handoff": None,
        "branches": {},
    }


def scaffold(root: Path, force: bool = False) -> None:
    """Create the `_bewater/` tree under `root`, an empty ledger, and config.

    Directories are created unconditionally (mkdir -p semantics). The ledger
    and config are written only when they do not already exist, unless
    ``force`` rewrites them.
    """
    root = Path(root)

    (root / _BEWATER).mkdir(parents=True, exist_ok=True)
    records_dir(root).mkdir(parents=True, exist_ok=True)
    output_dir(root).mkdir(parents=True, exist_ok=True)

    config_path = root / _BEWATER / "config.yaml"
    if force or not config_path.exists():
        config_path.write_text(
            yaml.safe_dump(_default_config(root), sort_keys=False, allow_unicode=True)
        )

    if force or not ledger_path(root).exists():
        io.save_ledger(root, _empty_ledger())
