from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "src" / "skills" / "bw-discovery-research" / "scripts"
VALIDATOR = SCRIPTS / "validate_research_plan.py"
EMITTER = SCRIPTS / "emit_write_plan.py"


def _load_validator_module():
    spec = importlib.util.spec_from_file_location("research_plan_validator", VALIDATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _research_plan(*, ledger_ref: str | None = None) -> str:
    ledger_value = "null" if ledger_ref is None else ledger_ref
    return f"""---
schema_version: 1
artifact_id: ART-002
revision: 1
supersedes_ref: null
kind: research
stage: discover
branch_id: BR-001
document_status: draft
validation_status: unvalidated
derived_from: [artifact:ART-001@1]
signoffs: []
stale_reason: null
---

## Research Objective

Learn what could materially change the project direction.

## Learning Plan

```yaml
- id: LP-001
  learning_objective: Understand repeat use
  starting_state: assumption
  starting_view: People will return weekly
  decision_relevance: Changes whether to pursue the challenge
  lens: Consumer
  priority: high
  ledger_ref: {ledger_value}
```

## Research Design

```yaml
- id: RM-001
  learning_refs: [LP-001]
  evidence_needed: Observed repeat behavior
  method_source_bundle: Behavioral data review
  exclusions: Self-reported intent alone
  dependencies: []
  owner: Research coordinator
  bounded_budget: One working day
  stop_condition: Two independent cohorts checked
  expected_output: Repeat-use distribution
  limitation: Observational association is not causation
```

## Knowledge Base Index

```yaml
- learning_ref: LP-001
  answer_status: not-researched
  evidence_refs: []
  current_answer: Not researched
  contradictions: []
  remaining_gap: Repeat use has not been observed
```
"""


def _charter(*, branch_id: str = "BR-001", revision: int = 1) -> str:
    return f"""---
schema_version: 1
artifact_id: ART-001
revision: {revision}
kind: charter
stage: immersion
branch_id: {branch_id}
derived_from: []
---

# Project Charter
"""


def _files(tmp_path: Path, plan_text: str, before_text: str, after_text: str):
    charter = tmp_path / "charter.md"
    plan = tmp_path / "research.md"
    before = tmp_path / "before.yaml"
    after = tmp_path / "after.yaml"
    charter.write_text(_charter())
    plan.write_text(plan_text)
    before.write_text(before_text)
    after.write_text(after_text)
    return charter, plan, before, after


def _ledger(*, projected: bool = False, source: str = "artifact:ART-002@1") -> str:
    assumptions = {}
    if projected:
        assumptions["A-001"] = {
            "record_revision": 1,
            "statement": "People will return weekly",
            "branch_id": "BR-001",
            "layer": "root",
            "category": "consumer",
            "side": "magic",
            "impact": "high",
            "uncertainty": "high",
            "evidence_level": "L1",
            "validation_status": "untested",
            "status": "active",
            "evidence_refs": [],
            "derived_from": [source],
            "supersedes_ref": None,
            "risk_history": [],
            "l4_obligation_status": "open",
            "history": [],
        }
    return yaml.safe_dump(
        {"schema_version": 1, "revision": 2, "next_id": 2 if projected else 1, "assumptions": assumptions},
        sort_keys=False,
    )


def _legacy_ledgers(*, reparent: bool = False) -> tuple[str, str]:
    before = yaml.safe_load(_ledger(projected=True, source="artifact:ART-001@1"))
    after = yaml.safe_load(yaml.safe_dump(before))
    prior = dict(after["assumptions"]["A-001"])
    after["revision"] = 3
    after["assumptions"]["A-001"]["record_revision"] = 2
    after["assumptions"]["A-001"]["validation_status"] = "testing"
    after["assumptions"]["A-001"]["history"] = [prior]
    if reparent:
        after["assumptions"]["A-001"]["derived_from"] = ["artifact:ART-002@1"]
    return yaml.safe_dump(before, sort_keys=False), yaml.safe_dump(after, sort_keys=False)


def test_validator_accepts_four_core_sections_and_zero_projection(tmp_path: Path):
    charter, plan, before, after = _files(tmp_path, _research_plan(), _ledger(), _ledger())

    validator = _load_validator_module()
    assert validator.validate_files(plan, charter, before, after) == []


def test_validator_allows_omitting_optional_ledger_ref(tmp_path: Path):
    plan_text = _research_plan().replace("  ledger_ref: null\n", "")
    charter, plan, before, after = _files(tmp_path, plan_text, _ledger(), _ledger())

    assert _load_validator_module().validate_files(plan, charter, before, after) == []


def test_validator_requires_exact_charter_identity_and_branch(tmp_path: Path):
    charter, plan, before, after = _files(tmp_path, _research_plan(), _ledger(), _ledger())
    validator = _load_validator_module()

    charter.write_text(_charter(revision=2))
    errors = validator.validate_files(plan, charter, before, after)
    assert any("exact Charter revision" in error for error in errors)

    charter.write_text(_charter(branch_id="BR-002"))
    errors = validator.validate_files(plan, charter, before, after)
    assert any("same branch" in error for error in errors)


def test_validator_rejects_answer_status_in_learning_plan_and_missing_index_row(tmp_path: Path):
    plan = tmp_path / "research.md"
    before = tmp_path / "before.yaml"
    after = tmp_path / "after.yaml"
    invalid = _research_plan().replace("  ledger_ref: null", "  answer_status: partial\n  ledger_ref: null")
    invalid = invalid.replace("- learning_ref: LP-001", "- learning_ref: LP-999")
    plan.write_text(invalid)
    before.write_text(_ledger())
    after.write_text(_ledger())

    charter = tmp_path / "charter.md"
    charter.write_text(_charter())
    errors = _load_validator_module().validate_files(plan, charter, before, after)
    assert any("answer_status" in error and "Learning Plan" in error for error in errors)
    assert any("one Knowledge Base Index row" in error for error in errors)


def test_validator_requires_exact_evidence_revision_refs_in_knowledge_base(tmp_path: Path):
    invalid = _research_plan().replace("  evidence_refs: []", "  evidence_refs: [E-001]")
    charter, plan, before, after = _files(tmp_path, invalid, _ledger(), _ledger())

    errors = _load_validator_module().validate_files(plan, charter, before, after)

    assert any("exact Evidence revisions" in error for error in errors)


def test_validator_accepts_new_high_high_projection_and_checks_exact_lineage(tmp_path: Path):
    plan = tmp_path / "research.md"
    before = tmp_path / "before.yaml"
    after = tmp_path / "after.yaml"
    plan.write_text(_research_plan(ledger_ref="assumption:A-001@1"))
    before.write_text(_ledger())
    after.write_text(_ledger(projected=True))

    charter = tmp_path / "charter.md"
    charter.write_text(_charter())
    validator = _load_validator_module()
    assert validator.validate_files(plan, charter, before, after) == []

    after.write_text(_ledger(projected=True, source="artifact:ART-001@1"))
    errors = validator.validate_files(plan, charter, before, after)
    assert any("new root A-001" in error and "artifact:ART-002@1" in error for error in errors)


def test_validator_requires_ledger_ref_to_pin_exact_record_revision(tmp_path: Path):
    plan = tmp_path / "research.md"
    before = tmp_path / "before.yaml"
    after = tmp_path / "after.yaml"
    plan.write_text(_research_plan(ledger_ref="assumption:A-001@2"))
    before.write_text(_ledger())
    after.write_text(_ledger(projected=True))

    charter = tmp_path / "charter.md"
    charter.write_text(_charter())
    errors = _load_validator_module().validate_files(plan, charter, before, after)
    assert any("ledger_ref" in error and "exact staged record revision" in error for error in errors)


def test_validator_rejects_high_high_projection_without_open_l4_obligation(tmp_path: Path):
    plan = tmp_path / "research.md"
    before = tmp_path / "before.yaml"
    after = tmp_path / "after.yaml"
    plan.write_text(_research_plan(ledger_ref="assumption:A-001@1"))
    before.write_text(_ledger())
    data = yaml.safe_load(_ledger(projected=True))
    data["assumptions"]["A-001"]["l4_obligation_status"] = "satisfied"
    after.write_text(yaml.safe_dump(data, sort_keys=False))

    charter = tmp_path / "charter.md"
    charter.write_text(_charter())
    errors = _load_validator_module().validate_files(plan, charter, before, after)
    assert any("durable L4 obligation" in error for error in errors)


def test_validator_grandfathers_legacy_update_but_rejects_reparenting(tmp_path: Path):
    plan = tmp_path / "research.md"
    before = tmp_path / "before.yaml"
    after = tmp_path / "after.yaml"
    plan.write_text(_research_plan())
    before_text, after_text = _legacy_ledgers()
    before.write_text(before_text)
    after.write_text(after_text)

    charter = tmp_path / "charter.md"
    charter.write_text(_charter())
    validator = _load_validator_module()
    assert validator.validate_files(plan, charter, before, after) == []

    _, reparented = _legacy_ledgers(reparent=True)
    after.write_text(reparented)
    errors = validator.validate_files(plan, charter, before, after)
    assert any("grandfathered root A-001" in error and "must retain" in error for error in errors)


def test_emitter_omits_ledger_cas_for_zero_projection(tmp_path: Path):
    plan = tmp_path / "research.md"
    before = tmp_path / "before.yaml"
    after = tmp_path / "after.yaml"
    config = tmp_path / "config.yaml"
    plan.write_text(_research_plan())
    before.write_text(_ledger())
    after.write_text(_ledger())
    config.write_text("schema_version: 1\nrevision: 4\n")
    (tmp_path / "charter.md").write_text(_charter())

    result = subprocess.run(
        [
            sys.executable,
            str(EMITTER),
            "--action-id", "research-plan:ART-002@1",
            "--owner", "bw-discovery-research",
            "--artifact-path", "_bewater-output/ART-002-r1-research.md",
            "--artifact-file", str(plan),
            "--charter-file", str(tmp_path / "charter.md"),
            "--ledger-before-file", str(before),
            "--ledger-file", str(after),
            "--cas-step", "artifact-counter", "_bewater/config.yaml", "3", str(config),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    emitted = json.loads(result.stdout)
    assert [step["step_id"] for step in emitted["steps"]] == ["research-revision", "artifact-counter"]


def test_emitter_requires_validated_ledger_cas_when_projection_changes_ledger(tmp_path: Path):
    plan = tmp_path / "research.md"
    before = tmp_path / "before.yaml"
    after = tmp_path / "after.yaml"
    plan.write_text(_research_plan(ledger_ref="assumption:A-001@1"))
    before.write_text(_ledger())
    after.write_text(_ledger(projected=True))
    charter = tmp_path / "charter.md"
    charter.write_text(_charter())

    command = [
        sys.executable,
        str(EMITTER),
        "--action-id", "research-plan:ART-002@1",
        "--owner", "bw-discovery-research",
        "--artifact-path", "_bewater-output/ART-002-r1-research.md",
        "--artifact-file", str(plan),
        "--charter-file", str(charter),
        "--ledger-before-file", str(before),
        "--ledger-file", str(after),
    ]
    missing = subprocess.run(command, capture_output=True, text=True)
    assert missing.returncode == 1
    assert missing.stdout == ""
    assert "ledger cas" in missing.stderr.lower()

    valid = subprocess.run(
        command + ["--cas-step", "ledger", "_bewater/ledger.yaml", "1", str(after)],
        capture_output=True,
        text=True,
    )
    assert valid.returncode == 0, valid.stderr
    emitted = json.loads(valid.stdout)
    assert [step["step_id"] for step in emitted["steps"]] == ["research-revision", "ledger"]
