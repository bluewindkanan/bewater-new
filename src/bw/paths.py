"""Project-root discovery and well-known path helpers for the _bewater/ layout."""
from __future__ import annotations

from pathlib import Path

STATE_DIR = "_bewater"
OUTPUT_DIR = "_bewater-output"


def find_project_root(start: Path) -> Path:
    """Walk up from `start` until a directory containing `_bewater/` is found."""
    p = Path(start).resolve()
    for cand in [p, *p.parents]:
        if (cand / STATE_DIR).is_dir():
            return cand
    raise FileNotFoundError(f"no _bewater/ found at or above {start}")


def ledger_path(root: Path) -> Path:
    return root / STATE_DIR / "ledger.yaml"


def records_dir(root: Path) -> Path:
    return root / STATE_DIR / "records"


def output_dir(root: Path) -> Path:
    return root / OUTPUT_DIR


def artifacts_dir(root: Path) -> Path:
    return output_dir(root) / "artifacts"


def sources_dir(root: Path) -> Path:
    return output_dir(root) / "sources"


def knowledge_dir(root: Path) -> Path:
    return output_dir(root) / "knowledge"


def iter_workflow_documents(root: Path):
    """Yield Markdown workflow documents from canonical and migration locations."""
    root = Path(root)
    output = output_dir(root)
    seen: set[Path] = set()

    canonical = artifacts_dir(root)
    if canonical.is_dir():
        for path in sorted(canonical.rglob("*.md")):
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield path

    if output.is_dir():
        for path in sorted(output.glob("*.md")):
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield path

    legacy_archive = output / "archive"
    if legacy_archive.is_dir():
        for path in sorted(legacy_archive.rglob("*.md")):
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield path
