from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "src" / "skills" / "bw-immersion" / "scripts"
VALIDATOR = SCRIPTS / "validate_draft.py"
EMITTER = SCRIPTS / "emit_charter_plan.py"


def _load_validator_module():
    spec = importlib.util.spec_from_file_location("charter_validate_draft", VALIDATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATE_DRAFT = _load_validator_module()


def _charter(intent_source: str = "user-stated") -> str:
    return f"""---
schema_version: 1
artifact_id: ART-001
revision: 1
supersedes_ref: null
kind: charter
stage: immersion
branch_id: BR-001
document_status: draft
validation_status: unvalidated
dual_sided:
  magic:
    consumer_value_proposition: {{statement: A useful outcome, evidence_refs: []}}
    consumer_target: {{statement: A person in a situation, evidence_refs: []}}
  money:
    commercial_value_proposition: {{statement: A viable exchange, evidence_refs: []}}
    leverageable_assets: {{statement: An existing capability, evidence_refs: []}}
  tension: {{statement: Value and cost must balance}}
  balance_choice: Protect early learning
derived_from: []
signoffs: []
stale_reason: null
---

### Intent trace

| Claim | Provenance | Basis / exact user context | Calibration status |
|---|---|---|---|
| The user wants a better outcome | {intent_source} | intake turn 1 | unchanged |

### Original intent

- **User's own words:** A problem worth exploring.
- **Trigger / why now:** A recent event.
- **Desired change:** A better outcome.

### Project definition

- **Challenge:** Current behavior creates avoidable friction.
- **Intent and outcome:** Improve the person's outcome without assuming a solution.
- **Scope:** One situation is in scope; adjacent situations are out of scope.
- **Constraints:** Time and access are limited.
- **Success definition:** A concrete behavior and business signal improve.

### Money + Magic

The proposition balances value and viability.

### Current knowledge state

| Type | Content |
|---|---|
| **Known** | The user reported the recent event. |
| **Believed** | The proposition may help. |
| **Unknown** | Whether people will adopt it. |
| **Tensions** | Speed and cost may conflict. |
"""


def _run_validator(charter: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--artifact-file", str(charter)],
        capture_output=True,
        text=True,
    )


def test_validator_accepts_project_definition_without_ledger(tmp_path: Path):
    charter = tmp_path / "charter.md"
    charter.write_text(_charter())

    result = _run_validator(charter)

    assert result.returncode == 0, result.stderr
    assert result.stdout == ""
    assert VALIDATE_DRAFT.validate_files(charter) == []


def test_validator_rejects_invalid_provenance_and_missing_unknowns(tmp_path: Path):
    charter = tmp_path / "charter.md"
    charter.write_text(
        _charter(intent_source="claimed-by-agent").replace(
            "| **Unknown** | Whether people will adopt it. |\n", ""
        )
    )

    result = _run_validator(charter)

    assert result.returncode == 1
    assert "intent trace source" in result.stderr.lower()
    assert "unknown" in result.stderr.lower()
    assert len(VALIDATE_DRAFT.validate_files(charter)) >= 2


def test_validator_rejects_missing_project_definition_field(tmp_path: Path):
    charter = tmp_path / "charter.md"
    charter.write_text(_charter().replace("- **Constraints:** Time and access are limited.\n", ""))

    result = _run_validator(charter)

    assert result.returncode == 1
    assert "constraints" in result.stderr.lower()


def test_emitter_outputs_charter_and_counter_without_ledger(tmp_path: Path):
    charter = tmp_path / "charter.md"
    config = tmp_path / "config.yaml"
    charter.write_text(_charter())
    config.write_text("revision: 3\nproject:\n  name: Test project\n")

    result = subprocess.run(
        [
            sys.executable,
            str(EMITTER),
            "--action-id", "charter:ART-001@1",
            "--owner", "bw-immersion",
            "--artifact-path", "_bewater-output/artifacts/ART-001-r1-charter.md",
            "--artifact-file", str(charter),
            "--cas-step", "artifact-counter", "_bewater/config.yaml", "2", str(config),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert [step["op"] for step in plan["steps"]] == ["write_new", "cas_commit"]
    assert all(step["path"] != "_bewater/ledger.yaml" for step in plan["steps"])


def test_emitter_rejects_ledger_cas_step(tmp_path: Path):
    charter = tmp_path / "charter.md"
    ledger = tmp_path / "ledger.yaml"
    charter.write_text(_charter())
    ledger.write_text("schema_version: 1\nrevision: 2\nassumptions: {{}}\n")

    result = subprocess.run(
        [
            sys.executable,
            str(EMITTER),
            "--action-id", "charter:ART-001@1",
            "--owner", "bw-immersion",
            "--artifact-path", "_bewater-output/ART-001-r1-charter.md",
            "--artifact-file", str(charter),
            "--cas-step", "ledger", "_bewater/ledger.yaml", "1", str(ledger),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert result.stdout == ""
    assert "ledger" in result.stderr.lower()


def test_emitter_fails_closed_for_invalid_draft(tmp_path: Path):
    charter = tmp_path / "charter.md"
    config = tmp_path / "config.yaml"
    charter.write_text(_charter(intent_source="agent guess"))
    config.write_text("revision: 3\n")

    result = subprocess.run(
        [
            sys.executable, str(EMITTER),
            "--action-id", "charter:ART-001@1",
            "--owner", "bw-immersion",
            "--artifact-path", "_bewater-output/ART-001-r1-charter.md",
            "--artifact-file", str(charter),
            "--cas-step", "artifact-counter", "_bewater/config.yaml", "2", str(config),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert result.stdout == ""
    assert "draft validation failed" in result.stderr.lower()


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("not frontmatter", "complete YAML frontmatter"),
        ("---\n: invalid\n---\nbody", "invalid YAML"),
        ("---\n- list\n---\nbody", "must be a YAML mapping"),
    ],
)
def test_frontmatter_parser_rejects_malformed_inputs(text: str, expected: str):
    _, _, errors = VALIDATE_DRAFT._frontmatter(text)

    assert any(expected in error for error in errors)


def test_validator_helpers_report_incomplete_document():
    frontmatter_errors = VALIDATE_DRAFT._validate_frontmatter({"dual_sided": {"magic": "bad"}})
    body_errors = VALIDATE_DRAFT._validate_body("### Original intent\n\nTODO")

    assert any("schema_version" in error for error in frontmatter_errors)
    assert any("dual_sided.money" in error for error in frontmatter_errors)
    assert any("missing required heading" in error for error in body_errors)
    assert any("placeholder" in error for error in body_errors)


def test_intent_trace_helper_rejects_structural_gaps():
    no_trace = VALIDATE_DRAFT._validate_intent_trace("### Intent trace\n\nNo table")
    wrong_columns = VALIDATE_DRAFT._validate_intent_trace(
        "### Intent trace\n\n| What | Source | Basis |\n|---|---|---|\n| x | user-stated | turn 1 |"
    )
    empty_rows = VALIDATE_DRAFT._validate_intent_trace(
        "### Intent trace\n\n| Claim | Source | Basis |\n|---|---|---|\n| incomplete | row |"
    )
    empty_claim = VALIDATE_DRAFT._validate_intent_trace(
        "### Intent trace\n\n| Claim | Source | Basis |\n|---|---|---|\n| - | user-stated | turn 1 |"
    )

    assert any("Markdown table" in error for error in no_trace)
    assert any("Claim" in error for error in wrong_columns)
    assert any("at least one claim" in error for error in empty_rows)
    assert any("claim must be non-empty" in error.lower() for error in empty_claim)


def test_validator_main_returns_status_and_reports_errors(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    charter = tmp_path / "charter.md"
    charter.write_text(_charter())

    assert VALIDATE_DRAFT.main(["--artifact-file", str(charter)]) == 0
    charter.write_text("missing frontmatter")
    assert VALIDATE_DRAFT.main(["--artifact-file", str(charter)]) == 1
    assert "ERROR: Charter must begin" in capsys.readouterr().err
