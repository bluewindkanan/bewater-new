from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml
import pytest

from bwkit import applier


REPO = Path(__file__).resolve().parents[1]
EMITTER = REPO / "src/skills/bw-discovery-research/scripts/emit_write_plan.py"


def _charter() -> str:
    return """---
schema_version: 1
artifact_id: ART-001
revision: 1
kind: charter
stage: immersion
branch_id: BR-001
derived_from: []
---
# Charter
"""


def _research(*, revision: int, knowledge_ref: str | None = None) -> str:
    refs = "[]" if knowledge_ref is None else f"[{knowledge_ref}]"
    status = "not-researched" if knowledge_ref is None else "answered"
    supersedes = "null" if revision == 1 else f"artifact:ART-003@{revision - 1}"
    return f"""---
schema_version: 1
artifact_id: ART-003
revision: {revision}
supersedes_ref: {supersedes}
kind: research
stage: discover
branch_id: BR-001
derived_from: [artifact:ART-001@1]
signoffs: []
---
## Research Objective
Learn.
## Learning Plan
```yaml
- id: LP-001
  learning_objective: Learn demand
  starting_state: assumption
  starting_view: Demand exists
  decision_relevance: Direction
  lens: Consumer
  priority: high
```
## Next Sprint
```yaml
- id: RM-001
  learning_refs: [LP-001]
  evidence_needed: Behavior
  method_source_bundle: Review
  exclusions: Intent
  dependencies: []
  owner: Coordinator
  bounded_budget: One day
  stop_condition: Saturation
  expected_output: Workpaper
  limitation: Small sample
```
## Research Progress
```yaml
- learning_ref: LP-001
  answer_status: {status}
  knowledge_refs: {refs}
  current_answer: Current answer
  remaining_gap: Explicit gap
```
"""


def _workpaper(*, revision: int, research_revision: int = 1) -> str:
    return f"""---
schema_version: 1
knowledge_id: K-001
revision: {revision}
branch_id: BR-001
title: Demand
research_ref: artifact:ART-003@{research_revision}
learning_refs: [LP-001]
source_refs: []
knowledge_refs: []
evidence_refs: []
status: complete
---
# Demand
## Question or hypothesis
Does demand exist?
## Method and scope
Desk research
## Sources used
Exact sources in frontmatter.
## Summary
Demand appears bounded.
## Conclusion
Demand exists with medium confidence.
## Limitations and new questions
Behavioral validation remains limited.
"""


def _ledger(revision: int = 1) -> str:
    return yaml.safe_dump({"schema_version": 1, "revision": revision, "next_id": 1, "assumptions": {}}, sort_keys=False)


def _setup(tmp_path: Path):
    (tmp_path / "_bewater/records").mkdir(parents=True)
    (tmp_path / "_bewater-output/artifacts").mkdir(parents=True)
    (tmp_path / "_bewater-output/knowledge").mkdir()
    (tmp_path / "_bewater-output/sources").mkdir()
    charter = tmp_path / "charter.md"
    charter.write_text(_charter())
    ledger = tmp_path / "_bewater/ledger.yaml"
    ledger.write_text(_ledger())
    research_head = tmp_path / "_bewater-output/artifacts/ART-003-r1-research.md"
    research_head.write_text(_research(revision=1))
    config_before = {"schema_version": 1, "revision": 1, "active_branch": "BR-001", "next_ids": {"knowledge": 1}}
    (tmp_path / "_bewater/config.yaml").write_text(yaml.safe_dump(config_before, sort_keys=False))
    return charter, ledger, research_head


def _emit(tmp_path: Path, candidate_dir: Path, *, revision: int = 1, new: bool = True):
    charter, ledger, research_head = _setup(tmp_path)
    candidate_dir.mkdir()
    staged_research = candidate_dir / "ART-003-r2-research.md"
    staged_research.write_text(_research(revision=2, knowledge_ref=f"knowledge:K-001@{revision}"))
    staged_k = candidate_dir / "K-001-demand.md"
    staged_k.write_text(_workpaper(revision=revision))
    config_after = candidate_dir / "config.yaml"
    config = yaml.safe_load((tmp_path / "_bewater/config.yaml").read_text())
    config["revision"] = 2
    config["next_ids"]["knowledge"] = 2
    config_after.write_text(yaml.safe_dump(config, sort_keys=False))
    command = [
        sys.executable, str(EMITTER), "--project-root", str(tmp_path),
        "--action-id", "sprint:ART-003@2", "--owner", "bw-discovery-research",
        "--artifact-path", "_bewater-output/artifacts/ART-003-r2-research.md",
        "--artifact-file", str(staged_research), "--research-head-file", str(research_head),
        "--charter-file", str(charter), "--ledger-before-file", str(ledger),
        "--ledger-file", str(ledger),
    ]
    if new:
        command += [
            "--knowledge-new", "_bewater-output/knowledge/K-001-demand.md", str(staged_k),
            "--config-before-file", str(tmp_path / "_bewater/config.yaml"),
            "--config-file", str(config_after),
        ]
    else:
        command += ["--knowledge-cas", "_bewater-output/knowledge/K-001-demand.md", str(revision - 1), str(staged_k)]
    result = subprocess.run(command, capture_output=True, text=True)
    return result


def test_allocates_k_writes_knowledge_then_research_and_config_last_resumably(tmp_path: Path):
    project = tmp_path / "project"
    result = _emit(project, tmp_path / "candidates")
    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert [step["step_id"] for step in plan["steps"]] == ["knowledge-new-K-001", "research-revision", "knowledge-counter"]
    assert all(not step["path"].startswith("_bewater-output/sources/") for step in plan["steps"])
    assert all("config-after-sprint" not in step["path"] for step in plan["steps"])
    assert applier.apply_plan(project, plan)["action_status"] == "applied"
    resumed = applier.apply_plan(project, plan)
    assert resumed["action_status"] == "applied"
    assert all(item["status"] == "skipped" for item in resumed["results"])


def test_rejects_occupied_allocation_with_different_bytes(tmp_path: Path):
    project = tmp_path / "project"
    result = _emit(project, tmp_path / "candidates")
    occupied = project / "_bewater-output/knowledge/K-001-demand.md"
    occupied.write_text("unrelated bytes")
    second = subprocess.run(result.args, capture_output=True, text=True)
    assert second.returncode == 1
    assert "occupied" in second.stderr.lower()


def test_revises_same_k_path_without_allocating_or_creating_rn_file(tmp_path: Path):
    project = tmp_path / "project"
    charter, ledger, r1 = _setup(project)
    k = project / "_bewater-output/knowledge/K-001-demand.md"
    k.write_text(_workpaper(revision=1))
    r2 = project / "_bewater-output/artifacts/ART-003-r2-research.md"
    r2.write_text(_research(revision=2, knowledge_ref="knowledge:K-001@1"))
    candidates = tmp_path / "candidates"
    candidates.mkdir()
    staged_k = candidates / "K-001-demand.md"
    staged_k.write_text(_workpaper(revision=2, research_revision=2))
    staged_r3 = candidates / "ART-003-r3-research.md"
    staged_r3.write_text(_research(revision=3, knowledge_ref="knowledge:K-001@2"))
    command = [
        sys.executable, str(EMITTER), "--project-root", str(project), "--action-id", "sprint:ART-003@3",
        "--owner", "bw-discovery-research", "--artifact-path", "_bewater-output/artifacts/ART-003-r3-research.md",
        "--artifact-file", str(staged_r3), "--research-head-file", str(r2), "--charter-file", str(charter),
        "--ledger-before-file", str(ledger), "--ledger-file", str(ledger),
        "--knowledge-cas", "_bewater-output/knowledge/K-001-demand.md", "1", str(staged_k),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert [step["op"] for step in plan["steps"]] == ["cas_commit", "write_new"]
    assert all("K-001-r2" not in step["path"] for step in plan["steps"])
    first = dict(plan)
    first["steps"] = first["steps"][:1]
    assert applier.apply_plan(project, first)["action_status"] == "applied"
    assert applier.apply_plan(project, plan)["action_status"] == "applied"
    assert r1.exists()
    assert not list((project / "_bewater-output/knowledge").glob("K-001-r*.md"))


def test_derives_current_research_head_and_rejects_supplied_historical_head(tmp_path: Path):
    result = _emit(tmp_path / "project", tmp_path / "candidates")
    stale = tmp_path / "historical.md"
    stale.write_text(_research(revision=1).replace("revision: 1", "revision: 0"))
    args = list(result.args)
    index = args.index("--research-head-file") + 1
    args[index] = str(stale)
    rejected = subprocess.run(args, capture_output=True, text=True)
    assert rejected.returncode == 1
    assert "current research head" in rejected.stderr.lower()


def test_current_knowledge_closure_merges_live_k_with_staged_replacements(tmp_path: Path):
    project = tmp_path / "project"
    result = _emit(project, tmp_path / "candidates")
    live = project / "_bewater-output/knowledge/K-002-existing.md"
    live.write_text(_workpaper(revision=1).replace("K-001", "K-002"))
    staged_research = tmp_path / "candidates/ART-003-r2-research.md"
    staged_research.write_text(
        staged_research.read_text().replace(
            "[knowledge:K-001@1]", "[knowledge:K-001@1, knowledge:K-002@1]"
        )
    )
    merged = subprocess.run(result.args, capture_output=True, text=True)
    assert merged.returncode == 0, merged.stderr


def test_generic_cas_cannot_write_config_or_sources(tmp_path: Path):
    result = _emit(tmp_path / "project", tmp_path / "candidates")
    args = list(result.args) + [
        "--cas-step", "rogue-config", "_bewater/config.yaml", "1",
        str(tmp_path / "candidates/config.yaml"),
    ]
    rejected = subprocess.run(args, capture_output=True, text=True)
    assert rejected.returncode == 1
    assert "config" in rejected.stderr.lower() and "dedicated" in rejected.stderr.lower()


def test_rejects_stale_config_against_live_project_bytes(tmp_path: Path):
    project = tmp_path / "project"
    result = _emit(project, tmp_path / "candidates")
    stale_before = tmp_path / "config-before.yaml"
    stale_before.write_bytes((project / "_bewater/config.yaml").read_bytes())
    live = yaml.safe_load((project / "_bewater/config.yaml").read_text())
    live["revision"] = 9
    (project / "_bewater/config.yaml").write_text(yaml.safe_dump(live, sort_keys=False))
    args = list(result.args)
    args[args.index("--config-before-file") + 1] = str(stale_before)
    rejected = subprocess.run(args, capture_output=True, text=True)
    assert rejected.returncode == 1 and rejected.stdout == ""
    assert "stale config" in rejected.stderr.lower()


@pytest.mark.parametrize("failure", ["missing-k", "branch", "rm-ref", "source", "missing-evidence"])
def test_invalid_transaction_emits_no_plan(tmp_path: Path, failure: str):
    project = tmp_path / "project"
    candidates = tmp_path / "candidates"
    result = _emit(project, candidates)
    research = candidates / "ART-003-r2-research.md"
    workpaper = candidates / "K-001-demand.md"
    if failure == "missing-k":
        research.write_text(research.read_text().replace("knowledge:K-001@1", "knowledge:K-999@1"))
    elif failure == "branch":
        workpaper.write_text(workpaper.read_text().replace("branch_id: BR-001", "branch_id: BR-002"))
    elif failure == "rm-ref":
        research.write_text(research.read_text().replace("knowledge:K-001@1", "RM-001"))
    elif failure == "source":
        workpaper.write_text(
            workpaper.read_text().replace(
                "source_refs: []",
                "source_refs: [{path: _bewater-output/sources/missing.pdf, sha256: " + "0" * 64 + "}]",
            )
        )
    else:
        workpaper.write_text(workpaper.read_text().replace("evidence_refs: []", "evidence_refs: [evidence:E-001@1]"))
    rejected = subprocess.run(result.args, capture_output=True, text=True)
    assert rejected.returncode == 1
    assert rejected.stdout == ""


def test_optional_evidence_and_ledger_follow_research_and_precede_config(tmp_path: Path):
    project = tmp_path / "project"
    candidates = tmp_path / "candidates"
    result = _emit(project, candidates)
    staged_ledger = candidates / "ledger.yaml"
    staged_ledger.write_text(_ledger(revision=2))
    evidence = candidates / "evidence.yaml"
    evidence.write_text(yaml.safe_dump({
        "schema_version": 1, "revision": 1, "branch_id": "BR-001", "next_evidence_id": 2,
        "evidence": [{"id": "E-001", "record_revision": 1, "claim": "Demand exists"}],
    }, sort_keys=False))
    args = list(result.args)
    ledger_index = args.index("--ledger-file") + 1
    args[ledger_index] = str(staged_ledger)
    args += [
        "--evidence-new", str(evidence),
        "--cas-step", "ledger", "_bewater/ledger.yaml", "1", str(staged_ledger),
    ]
    emitted = subprocess.run(args, capture_output=True, text=True)
    assert emitted.returncode == 0, emitted.stderr
    plan = json.loads(emitted.stdout)
    assert [step["step_id"] for step in plan["steps"]] == [
        "knowledge-new-K-001", "research-revision", "evidence-new", "ledger", "knowledge-counter"
    ]


def test_stale_live_synthesis_must_be_revised_or_removed_when_input_advances(tmp_path: Path):
    project = tmp_path / "project"
    charter, ledger, _ = _setup(project)
    k1 = project / "_bewater-output/knowledge/K-001-demand.md"
    k1.write_text(_workpaper(revision=1))
    synthesis = project / "_bewater-output/knowledge/K-002-summary.md"
    synthesis.write_text(
        _workpaper(revision=1)
        .replace("K-001", "K-002")
        .replace("knowledge_refs: []", "knowledge_refs: [knowledge:K-001@1]")
        .replace("Desk research", "synthesis")
    )
    r2 = project / "_bewater-output/artifacts/ART-003-r2-research.md"
    r2.write_text(_research(revision=2, knowledge_ref="knowledge:K-001@1"))
    candidates = tmp_path / "candidates"
    candidates.mkdir()
    staged_k = candidates / "K-001-demand.md"
    staged_k.write_text(_workpaper(revision=2, research_revision=2))
    staged_r3 = candidates / "ART-003-r3-research.md"
    staged_r3.write_text(
        _research(revision=3, knowledge_ref="knowledge:K-001@2").replace(
            "[knowledge:K-001@2]", "[knowledge:K-001@2, knowledge:K-002@1]"
        )
    )
    rejected = subprocess.run([
        sys.executable, str(EMITTER), "--project-root", str(project), "--action-id", "sprint:ART-003@3",
        "--owner", "bw-discovery-research", "--artifact-path", "_bewater-output/artifacts/ART-003-r3-research.md",
        "--artifact-file", str(staged_r3), "--research-head-file", str(r2), "--charter-file", str(charter),
        "--ledger-before-file", str(ledger), "--ledger-file", str(ledger),
        "--knowledge-cas", "_bewater-output/knowledge/K-001-demand.md", "1", str(staged_k),
    ], capture_output=True, text=True)
    assert rejected.returncode == 1 and rejected.stdout == ""
    assert "stale dependency" in rejected.stderr.lower()


def test_rejects_second_research_head_on_same_branch_even_with_different_artifact_id(tmp_path: Path):
    project = tmp_path / "project"
    result = _emit(project, tmp_path / "candidates")
    second = project / "_bewater-output/artifacts/ART-004-r1-research.md"
    second.write_text(_research(revision=1).replace("ART-003", "ART-004"))
    rejected = subprocess.run(result.args, capture_output=True, text=True)
    assert rejected.returncode == 1 and rejected.stdout == ""
    assert "multiple current research heads" in rejected.stderr.lower()


def test_rejects_duplicate_live_knowledge_id_under_another_filename(tmp_path: Path):
    project = tmp_path / "project"
    result = _emit(project, tmp_path / "candidates")
    duplicate = project / "_bewater-output/knowledge/K-001-old-title.md"
    duplicate.write_text(_workpaper(revision=1))
    rejected = subprocess.run(result.args, capture_output=True, text=True)
    assert rejected.returncode == 1 and rejected.stdout == ""
    assert "duplicate knowledge id" in rejected.stderr.lower()


def test_evidence_write_new_rejects_live_different_bytes(tmp_path: Path):
    project = tmp_path / "project"
    candidates = tmp_path / "candidates"
    result = _emit(project, candidates)
    live = project / "_bewater/evidence.yaml"
    live.write_text("schema_version: 1\nrevision: 1\nbranch_id: BR-001\nevidence: []\n")
    staged = candidates / "evidence.yaml"
    staged.write_text(yaml.safe_dump({
        "schema_version": 1, "revision": 1, "branch_id": "BR-001", "next_evidence_id": 2,
        "evidence": [{"id": "E-001", "record_revision": 1, "claim": "Demand"}],
    }, sort_keys=False))
    rejected = subprocess.run(list(result.args) + ["--evidence-new", str(staged)], capture_output=True, text=True)
    assert rejected.returncode == 1 and rejected.stdout == ""
    assert "occupied" in rejected.stderr.lower()
