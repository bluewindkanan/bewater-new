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
    text = Path(path).read_text()
    if not text.startswith("---\n"):
        return schema.ArtifactMeta.empty(), text
    end = text.index("\n---\n", 4)
    fm = yaml.safe_load(text[4:end])
    body = text[end + 5 :]
    return schema.ArtifactMeta.from_dict(fm or {}), body


def write_artifact(path: Path, meta: schema.ArtifactMeta, body: str) -> None:
    fm = yaml.safe_dump(meta.to_dict(), sort_keys=False, allow_unicode=True)
    Path(path).write_text(f"---\n{fm}---\n{body}")
