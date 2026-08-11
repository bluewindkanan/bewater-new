"""YAML IO for the ledger and frontmatter artifacts.

Returns schema types (Ledger, ArtifactMeta) defined in bw.schema.
"""
from __future__ import annotations

from pathlib import Path

import yaml

from . import schema
from .paths import ledger_path


def load_ledger(root: Path) -> schema.Ledger:
    data = yaml.safe_load(ledger_path(root).read_text()) or {}
    return schema.Ledger.from_dict(data)


def save_ledger(root: Path, ledger: schema.Ledger) -> None:
    ledger_path(root).write_text(
        yaml.safe_dump(ledger.to_dict(), sort_keys=False, allow_unicode=True)
    )


def read_artifact(path: Path) -> tuple[schema.ArtifactMeta, str]:
    path = Path(path)
    text = path.read_text()
    if not text.startswith("---\n"):
        return schema.ArtifactMeta.empty(), text
    try:
        end = text.index("\n---\n", 4)
    except ValueError as exc:
        raise ValueError(f"malformed artifact: missing closing fence in {path}") from exc
    fm = yaml.safe_load(text[4:end])
    body = text[end + 5 :]
    return schema.ArtifactMeta.from_dict(fm or {}), body


def read_frontmatter(path: Path) -> dict:
    """Return the raw parsed frontmatter dict of an artifact ({} if none).

    Unlike :func:`read_artifact`, this preserves every frontmatter key (e.g. the
    lifecycle ``opportunity_areas`` / ``concepts`` / Solution blocks) so callers that need
    artifact-specific structured fields can read them directly.
    """
    path = Path(path)
    text = path.read_text()
    if not text.startswith("---\n"):
        return {}
    try:
        end = text.index("\n---\n", 4)
    except ValueError as exc:
        raise ValueError(f"malformed artifact: missing closing fence in {path}") from exc
    fm = yaml.safe_load(text[4:end])
    return fm if isinstance(fm, dict) else {}


def write_artifact(path: Path, meta: schema.ArtifactMeta, body: str) -> None:
    fm = yaml.safe_dump(meta.to_dict(), sort_keys=False, allow_unicode=True)
    Path(path).write_text(f"---\n{fm}---\n{body}")
