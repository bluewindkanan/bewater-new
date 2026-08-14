from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
VALIDATOR = REPO / "src/skills/bw-discovery-research/scripts/validate_knowledge_workpaper.py"


def _module():
    spec = importlib.util.spec_from_file_location("knowledge_validator", VALIDATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _research(*, revision: int = 1, knowledge_ref: str | None = None) -> str:
    refs = "[]" if knowledge_ref is None else f"[{knowledge_ref}]"
    status = "not-researched" if knowledge_ref is None else "answered"
    return f"""---
schema_version: 1
artifact_id: ART-003
revision: {revision}
kind: research
stage: discover
branch_id: BR-001
---

## Learning Plan
```yaml
- id: LP-001
```

## Research Progress
```yaml
- learning_ref: LP-001
  answer_status: {status}
  knowledge_refs: {refs}
  current_answer: Pending
  remaining_gap: Explicit gap
```
"""


def _workpaper(
    *, revision: int = 1, source_refs: str = "[]", knowledge_refs: str = "[]",
    evidence_refs: str = "[]", branch_id: str = "BR-001",
    research_ref: str = "artifact:ART-003@1", status: str = "complete",
    method: str = "Desk research",
) -> str:
    return f"""---
schema_version: 1
knowledge_id: K-001
revision: {revision}
branch_id: {branch_id}
title: Repeat use
research_ref: {research_ref}
learning_refs: [LP-001]
source_refs: {source_refs}
knowledge_refs: {knowledge_refs}
evidence_refs: {evidence_refs}
status: {status}
---

# Repeat use

## Question or hypothesis
Do people return?

## Method and scope
{method}

## Sources used
The sources listed in frontmatter.

## Summary
Observed behavior is consistent across two cohorts.

## Conclusion
Repeat use is likely. Confidence: medium.

## Limitations and new questions
The sample is small and excludes new users.
"""


def _project(tmp_path: Path) -> tuple[Path, Path, Path]:
    knowledge = tmp_path / "_bewater-output/knowledge"
    sources = tmp_path / "_bewater-output/sources"
    artifacts = tmp_path / "_bewater-output/artifacts"
    knowledge.mkdir(parents=True)
    sources.mkdir()
    artifacts.mkdir()
    research = artifacts / "ART-003-r1-research.md"
    research.write_text(_research())
    workpaper = knowledge / "K-001-repeat-use.md"
    workpaper.write_text(_workpaper())
    return workpaper, research, sources


def test_accepts_working_and_complete_workpapers(tmp_path: Path):
    workpaper, research, _ = _project(tmp_path)
    validator = _module()
    assert validator.validate_workpaper(workpaper, tmp_path, research_files=[research]) == []
    workpaper.write_text(_workpaper(status="working"))
    assert validator.validate_workpaper(workpaper, tmp_path, research_files=[research]) == []


def test_checks_stable_identity_revision_and_duplicate_ids(tmp_path: Path):
    workpaper, research, _ = _project(tmp_path)
    validator = _module()
    fanout = workpaper.with_name("K-001-r2-repeat-use.md")
    fanout.write_text(_workpaper(revision=2))
    errors = validator.validate_workpaper(fanout, tmp_path, research_files=[research])
    assert any("stable" in error.lower() or "rN" in error for error in errors)
    assert any("duplicate" in error.lower() for error in errors)
    workpaper.write_text(_workpaper(revision=0))
    assert any("positive" in error.lower() for error in validator.validate_workpaper(workpaper, tmp_path, research_files=[research]))


def test_checks_research_learning_and_branch_but_not_new_research_head(tmp_path: Path):
    workpaper, research, _ = _project(tmp_path)
    newer = research.with_name("ART-003-r2-research.md")
    newer.write_text(_research(revision=2, knowledge_ref="knowledge:K-001@1"))
    validator = _module()
    assert validator.validate_workpaper(workpaper, tmp_path, research_files=[research, newer]) == []
    workpaper.write_text(_workpaper(branch_id="BR-002"))
    assert any("branch" in error.lower() for error in validator.validate_workpaper(workpaper, tmp_path, research_files=[research]))
    workpaper.write_text(_workpaper(research_ref="artifact:ART-003@9"))
    assert any("research_ref" in error for error in validator.validate_workpaper(workpaper, tmp_path, research_files=[research]))

    research.write_text(_research() + "\n## Unrelated rows\n```yaml\n- id: LP-999\n```\n")
    workpaper.write_text(_workpaper().replace("[LP-001]", "[LP-999]"))
    assert any("learning_refs" in error for error in validator.validate_workpaper(workpaper, tmp_path, research_files=[research]))


def test_hashes_local_source_bytes_without_parsing_binary(tmp_path: Path):
    workpaper, research, sources = _project(tmp_path)
    binary = sources / "interviews.docx"
    payload = b"PK\x03\x04\x00\xffnot-text"
    binary.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    workpaper.write_text(_workpaper(source_refs=f"[{{path: _bewater-output/sources/interviews.docx, sha256: {digest}}}]"))
    validator = _module()
    assert validator.validate_workpaper(workpaper, tmp_path, research_files=[research]) == []
    binary.write_bytes(payload + b"changed")
    assert any("SHA-256" in error for error in validator.validate_workpaper(workpaper, tmp_path, research_files=[research]))
    workpaper.write_text(_workpaper(source_refs=f"[{{path: ../outside.pdf, sha256: {digest}}}]"))
    assert any("sources" in error.lower() for error in validator.validate_workpaper(workpaper, tmp_path, research_files=[research]))


def test_accepts_exact_url_and_rejects_malformed_source_entry(tmp_path: Path):
    workpaper, research, _ = _project(tmp_path)
    workpaper.write_text(_workpaper(source_refs="[{url: 'https://example.test/report?a=1&b=2'}]"))
    validator = _module()
    assert validator.validate_workpaper(workpaper, tmp_path, research_files=[research]) == []
    workpaper.write_text(_workpaper(source_refs="[{url: example.test/report}]"))
    assert any("URL" in error for error in validator.validate_workpaper(workpaper, tmp_path, research_files=[research]))


def test_synthesis_requires_exact_current_knowledge_closure(tmp_path: Path):
    workpaper, research, _ = _project(tmp_path)
    input_path = workpaper.with_name("K-002-input.md")
    input_path.write_text(_workpaper().replace("K-001", "K-002"))
    workpaper.write_text(_workpaper(knowledge_refs="[knowledge:K-002@1]", method="synthesis"))
    validator = _module()
    assert validator.validate_workpaper(workpaper, tmp_path, research_files=[research]) == []
    input_path.write_text(_workpaper(revision=2).replace("K-001", "K-002"))
    assert any("current" in error.lower() for error in validator.validate_workpaper(workpaper, tmp_path, research_files=[research]))
    workpaper.write_text(_workpaper(knowledge_refs="[K-002@2]", method="synthesis"))
    assert any("exact" in error.lower() for error in validator.validate_workpaper(workpaper, tmp_path, research_files=[research]))


def test_required_content_and_evidence_ref_validation(tmp_path: Path):
    workpaper, research, _ = _project(tmp_path)
    validator = _module()
    workpaper.write_text(_workpaper().replace("Repeat use is likely. Confidence: medium.", ""))
    assert any("Conclusion" in error for error in validator.validate_workpaper(workpaper, tmp_path, research_files=[research]))
    workpaper.write_text(_workpaper().replace("## Limitations and new questions", "## New questions"))
    assert any("Limitations" in error for error in validator.validate_workpaper(workpaper, tmp_path, research_files=[research]))
    workpaper.write_text(_workpaper(evidence_refs="[RM-001]"))
    assert any("Evidence" in error for error in validator.validate_workpaper(workpaper, tmp_path, research_files=[research]))
