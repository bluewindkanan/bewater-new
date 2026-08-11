from __future__ import annotations

import subprocess
import sys
import importlib.util
from pathlib import Path

import pytest
import yaml


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "src" / "skills" / "bw-project-charter" / "scripts"
VALIDATOR = SCRIPTS / "validate_draft.py"
EMITTER = SCRIPTS / "emit_write_plan.py"


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

### Original intent

- **User's own words:** A problem worth exploring.
- **Trigger / why now:** A recent event.
- **Desired change:** A better outcome.

### Structured interpretation

The team has a provisional proposition.

### Money + Magic

The proposition balances value and viability.

### Intent trace

| Claim | Source | Basis |
|---|---|---|
| The user wants a better outcome | {intent_source} | intake turn 1 |

### Current knowledge state

| Type | Content |
|---|---|
| **Known** | The user reported the recent event. |
| **Believed** | The proposition may help. |
| **Unknown** | Whether people will adopt it. |
| **Tensions** | Speed and cost may conflict. |

### Discover handoff

#### Core exploration question

What must we learn before trusting the proposition?

#### Beliefs to challenge

The proposition is a candidate belief.

#### Root assumption research map

| Assumption | 4C | Why it matters | Evidence needed | Disconfirming signal |
|---|---|---|---|---|
| A-001 | Consumer | Adoption matters | Observe repeated use | People do not return |
| A-002 | Company | Delivery matters | Test capability | Capability cannot deliver |
| A-003 | Channel | Access matters | Observe access | No viable access route |

#### Starting 4C questions

- **Consumer:** What does the person do now?

#### Research boundary

Discover tests these assumptions first.
"""


def _ledger() -> str:
    assumptions = {
        f"A-00{index}": {
            "record_revision": 1,
            "statement": f"Assumption {index}",
            "branch_id": "BR-001",
            "layer": "root",
            "category": category,
            "side": "both",
            "impact": "high",
            "uncertainty": "high",
            "evidence_level": "L1",
            "validation_status": "untested",
            "status": "active",
            "evidence_refs": [],
            "derived_from": ["artifact:ART-001@1"],
            "supersedes_ref": None,
            "risk_history": [],
            "l4_obligation_status": "open",
            "history": [],
        }
        for index, category in enumerate(("consumer", "commercial", "distribution"), start=1)
    }
    return yaml.safe_dump(
        {"schema_version": 1, "revision": 2, "next_id": 4, "assumptions": assumptions},
        sort_keys=False,
    )


def _run_validator(charter: Path, ledger: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--artifact-file", str(charter), "--ledger-file", str(ledger)],
        capture_output=True,
        text=True,
    )


def test_validator_accepts_a_complete_draft_with_provenance_and_root_map(tmp_path: Path):
    charter = tmp_path / "charter.md"
    ledger = tmp_path / "ledger.yaml"
    charter.write_text(_charter())
    ledger.write_text(_ledger())

    result = _run_validator(charter, ledger)

    assert result.returncode == 0, result.stderr
    assert result.stdout == ""
    assert VALIDATE_DRAFT.validate_files(charter, ledger) == []


def test_validator_accepts_template_provenance_and_basis_column_names(tmp_path: Path):
    charter = tmp_path / "charter.md"
    ledger = tmp_path / "ledger.yaml"
    charter.write_text(
        _charter().replace(
            "| Claim | Source | Basis |\n|---|---|---|\n| The user has a goal | user-stated | intake turn 1 |",
            "| Claim | Provenance | Basis / exact user context | Calibration status |\n"
            "|---|---|---|---|\n"
            "| The user has a goal | user-stated | intake turn 1 | unchanged |",
        )
    )
    ledger.write_text(_ledger())

    result = _run_validator(charter, ledger)

    assert result.returncode == 0, result.stderr
    assert VALIDATE_DRAFT.validate_files(charter, ledger) == []


def test_validator_rejects_invalid_provenance_and_incomplete_root_map(tmp_path: Path):
    charter = tmp_path / "charter.md"
    ledger = tmp_path / "ledger.yaml"
    charter.write_text(_charter(intent_source="claimed-by-agent").replace("Observe repeated use", "..."))
    ledger.write_text(_ledger())

    result = _run_validator(charter, ledger)

    assert result.returncode == 1
    assert "intent trace source" in result.stderr.lower()
    assert "evidence needed" in result.stderr.lower()
    assert len(VALIDATE_DRAFT.validate_files(charter, ledger)) >= 2


def test_validator_rejects_non_root_or_non_l1_assumption(tmp_path: Path):
    charter = tmp_path / "charter.md"
    ledger = tmp_path / "ledger.yaml"
    charter.write_text(_charter())
    data = yaml.safe_load(_ledger())
    data["assumptions"]["A-001"]["evidence_level"] = "L2"
    ledger.write_text(yaml.safe_dump(data, sort_keys=False))

    result = _run_validator(charter, ledger)

    assert result.returncode == 1
    assert "evidence_level must be l1" in result.stderr.lower()
    assert any("evidence_level must be L1" in error for error in VALIDATE_DRAFT.validate_files(charter, ledger))


def test_validator_rejects_root_assumption_without_exact_charter_lineage(tmp_path: Path):
    charter = tmp_path / "charter.md"
    ledger = tmp_path / "ledger.yaml"
    charter.write_text(_charter())
    data = yaml.safe_load(_ledger())
    data["assumptions"]["A-001"]["derived_from"] = ["artifact:ART-001@2"]
    ledger.write_text(yaml.safe_dump(data, sort_keys=False))

    result = _run_validator(charter, ledger)

    assert result.returncode == 1
    assert "derived_from must include artifact:art-001@1" in result.stderr.lower()
    assert any("derived_from must include artifact:ART-001@1" in error for error in VALIDATE_DRAFT.validate_files(charter, ledger))


def test_emitter_fails_closed_without_writing_a_plan_for_invalid_draft(tmp_path: Path):
    charter = tmp_path / "charter.md"
    ledger = tmp_path / "ledger.yaml"
    config = tmp_path / "config.yaml"
    charter.write_text(_charter(intent_source="agent guess"))
    ledger.write_text(_ledger())
    config.write_text("schema_version: 1\nrevision: 3\n")

    result = subprocess.run(
        [
            sys.executable, str(EMITTER),
            "--action-id", "project-charter:ART-001@1",
            "--owner", "bw-project-charter",
            "--artifact-path", "_bewater-output/ART-001-r1-charter.md",
            "--artifact-file", str(charter),
            "--ledger-file", str(ledger),
            "--cas-step", "ledger", "_bewater/ledger.yaml", "2", str(ledger),
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


def test_validator_helpers_report_incomplete_document_and_ledger(tmp_path: Path):
    frontmatter_errors = VALIDATE_DRAFT._validate_frontmatter({"dual_sided": {"magic": "bad"}})
    body_errors = VALIDATE_DRAFT._validate_body("### Original intent\n\nTODO")
    missing_ledger, missing_errors = VALIDATE_DRAFT._load_ledger(tmp_path / "missing.yaml")
    malformed = tmp_path / "malformed.yaml"
    malformed.write_text(": bad yaml")
    _, malformed_errors = VALIDATE_DRAFT._load_ledger(malformed)
    incomplete = tmp_path / "incomplete.yaml"
    incomplete.write_text("schema_version: 1\n")
    _, incomplete_errors = VALIDATE_DRAFT._load_ledger(incomplete)

    assert missing_ledger is None
    assert any("schema_version" in error for error in frontmatter_errors)
    assert any("dual_sided.money" in error for error in frontmatter_errors)
    assert any("missing required heading" in error for error in body_errors)
    assert any("placeholder" in error for error in body_errors)
    assert any("does not exist" in error for error in missing_errors)
    assert any("cannot be parsed" in error for error in malformed_errors)
    assert any("assumptions mapping" in error for error in incomplete_errors)


def test_intent_trace_and_root_map_helpers_reject_structural_gaps():
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
    ledger = yaml.safe_load(_ledger())
    ledger["assumptions"] = {"A-001": ledger["assumptions"]["A-001"]}
    ledger["assumptions"]["A-001"]["statement"] = ""
    ledger["assumptions"]["A-001"]["record_revision"] = 0
    root_errors = VALIDATE_DRAFT._validate_root_assumptions(
        "#### Root assumption research map\n\n| Assumption | Evidence needed | Disconfirming signal |\n"
        "|---|---|---|\n| A-999 | Observe | Reject |",
        ledger,
        "BR-001",
        "ART-001",
        1,
    )

    assert any("Markdown table" in error for error in no_trace)
    assert any("Claim" in error for error in wrong_columns)
    assert any("at least one claim" in error for error in empty_rows)
    assert any("claim must be non-empty" in error.lower() for error in empty_claim)
    assert any("3–5 active" in error for error in root_errors)
    assert any("statement must be non-empty" in error for error in root_errors)
    assert any("record_revision" in error for error in root_errors)
    assert any("missing A-001" in error for error in root_errors)


def test_validator_main_returns_status_and_reports_errors(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    charter = tmp_path / "charter.md"
    ledger = tmp_path / "ledger.yaml"
    charter.write_text(_charter())
    ledger.write_text(_ledger())

    assert VALIDATE_DRAFT.main(["--artifact-file", str(charter), "--ledger-file", str(ledger)]) == 0
    charter.write_text("missing frontmatter")
    assert VALIDATE_DRAFT.main(["--artifact-file", str(charter), "--ledger-file", str(ledger)]) == 1
    assert "ERROR: Charter must begin" in capsys.readouterr().err
