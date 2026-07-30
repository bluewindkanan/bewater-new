from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def test_cli_all_mode_does_not_require_skill(monkeypatch):
    from evals._harness import __main__ as cli

    monkeypatch.setattr(sys, "argv", ["evals", "run", "--all", "--mode", "red"])
    args = cli._parse_args()

    assert args.all_skills is True
    assert args.skill is None


def test_manifest_schema_has_required_fields():
    schema = json.loads((REPO / "evals" / "_harness" / "manifest_schema.json").read_text())
    required = set(schema["required"])
    for field in ["scenario_id", "target_skill", "prompt",
                  "required_assertions", "forbidden_behaviors", "repetition_count"]:
        assert field in required


def test_loader_validates_a_good_manifest(tmp_path):
    from evals._harness.loader import load_manifest  # noqa: F401  (import works)

    m = tmp_path / "s.yaml"
    m.write_text(
        "scenario_id: S-1\ntarget_skill: bw-start\nprompt: hi\n"
        "required_assertions: [a]\nforbidden_behaviors: []\nrepetition_count: 3\n")
    data = load_manifest(m)
    assert data["scenario_id"] == "S-1"


def test_loader_rejects_missing_repetition(tmp_path):
    from evals._harness.loader import load_manifest, ManifestError

    m = tmp_path / "s.yaml"
    m.write_text(
        "scenario_id: S-1\ntarget_skill: bw-start\nprompt: hi\n"
        "required_assertions: [a]\nforbidden_behaviors: []\n")
    with pytest.raises(ManifestError):
        load_manifest(m)
