"""Eval scenario manifest loader + validator. Authoring utility (not shipped,
not part of bwkit). Full jsonschema validation is deferred (no jsonschema dep);
we enforce required keys, which is enough for the scaffold."""
from __future__ import annotations

import json
from pathlib import Path

import yaml


class ManifestError(Exception):
    """A scenario manifest is missing a required field or is malformed."""


_SCHEMA = json.loads((Path(__file__).parent / "manifest_schema.json").read_text())


def load_manifest(path):
    data = yaml.safe_load(Path(path).read_text())
    if not isinstance(data, dict):
        raise ManifestError("manifest must be a mapping at the top level")
    for key in _SCHEMA["required"]:
        if key not in data:
            raise ManifestError(f"missing required field: {key}")
    return data
