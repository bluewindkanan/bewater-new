"""Project-root discovery and well-known path helpers for the _bewater/ layout."""
from __future__ import annotations

from pathlib import Path

STATE_DIR = "_bewater"


def find_project_root(start: Path) -> Path:
    """Walk up from `start` until a directory containing `_bewater/` is found."""
    p = Path(start).resolve()
    for cand in [p, *p.parents]:
        if (cand / STATE_DIR).is_dir():
            return cand
    raise FileNotFoundError(f"no _bewater/ found at or above {start}")


def ledger_path(root: Path) -> Path:
    return root / STATE_DIR / "state" / "assumption-ledger.yaml"


def artifacts_dir(root: Path) -> Path:
    return root / STATE_DIR / "artifacts"


def gates_dir(root: Path) -> Path:
    return root / STATE_DIR / "state" / "gates"
