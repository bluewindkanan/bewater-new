#!/usr/bin/env python3
"""Emit one validated, resumable Discover Sprint action for bwkit plan apply."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from bw.paths import iter_workflow_documents

from validate_knowledge_workpaper import parse_document, validate_workpaper
from validate_research_plan import _frontmatter, validate_files


def _yaml(path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        errors.append(f"{label} cannot be read as YAML: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{label} must be a YAML mapping.")
        return None
    return value


def _canonical_text(path: Path, label: str, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{label} must be canonical UTF-8 text: {exc}")
        return ""


def _document_ref(frontmatter: dict[str, Any]) -> str:
    return f"artifact:{frontmatter.get('artifact_id')}@{frontmatter.get('revision')}"


def _project_research_heads(
    project_root: Path, branch_id: str
) -> tuple[list[tuple[Path, dict[str, Any]]], list[str]]:
    documents: list[tuple[Path, dict[str, Any]]] = []
    errors: list[str] = []
    for path in iter_workflow_documents(project_root):
        try:
            frontmatter, _, parse_errors = _frontmatter(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            errors.append(f"Workflow document cannot be read: {path}: {exc}")
            continue
        if parse_errors or frontmatter is None or frontmatter.get("kind") != "research":
            continue
        if frontmatter.get("branch_id") == branch_id:
            documents.append((path, frontmatter))
    superseded = {
        frontmatter.get("supersedes_ref")
        for _, frontmatter in documents
        if isinstance(frontmatter.get("supersedes_ref"), str)
    }
    heads = [item for item in documents if _document_ref(item[1]) not in superseded]
    if len(heads) > 1:
        errors.append(f"Project has multiple current Research heads on {branch_id}.")
    return heads, errors


def _validate_research_head(
    project_root: Path, staged_file: Path, supplied_head_file: Path | None
) -> list[str]:
    staged, _, errors = _frontmatter(staged_file.read_text(encoding="utf-8"))
    if staged is None:
        return errors
    revision = staged.get("revision")
    heads, head_errors = _project_research_heads(project_root, str(staged.get("branch_id")))
    errors.extend(head_errors)
    if len(heads) > 1:
        return errors
    staged_ref = _document_ref(staged)
    if not heads and revision == 1:
        if staged.get("supersedes_ref") is not None:
            errors.append("Research revision 1 must not supersede another revision.")
        return errors
    if not heads:
        errors.append("The project has no current Research head for this successor.")
        return errors
    current_path, current = heads[0]
    current_ref = _document_ref(current)
    expected_supplied_ref = current_ref
    if current_ref == staged_ref:
        if current_path.read_bytes() != staged_file.read_bytes():
            errors.append("The current Research head has the staged identity but different bytes.")
        expected_supplied_ref = str(staged.get("supersedes_ref"))
    elif (
        staged.get("artifact_id") != current.get("artifact_id")
        or not isinstance(revision, int)
        or revision != current.get("revision", 0) + 1
        or staged.get("supersedes_ref") != current_ref
    ):
        errors.append(f"Staged Research revision must advance the exact current Research head {current_ref}.")
    if supplied_head_file is not None:
        try:
            supplied, _, supplied_errors = _frontmatter(supplied_head_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            supplied, supplied_errors = None, [str(exc)]
        errors.extend(supplied_errors)
        if supplied is None or _document_ref(supplied) != expected_supplied_ref:
            errors.append(
                f"--research-head-file is not the project-derived current Research head or resumable predecessor {expected_supplied_ref}."
            )
    return errors


def _merged_knowledge_files(project_root: Path, staged: list[Path]) -> tuple[list[Path], list[str]]:
    by_id: dict[str, Path] = {}
    errors: list[str] = []
    knowledge_dir = project_root / "_bewater-output" / "knowledge"
    for path in sorted(knowledge_dir.glob("K-*.md")) if knowledge_dir.is_dir() else []:
        frontmatter, _, parse_errors = parse_document(path)
        if not parse_errors and frontmatter is not None and isinstance(frontmatter.get("knowledge_id"), str):
            by_id[frontmatter["knowledge_id"]] = path
    for path in staged:
        frontmatter, _, parse_errors = parse_document(path)
        if not parse_errors and frontmatter is not None and isinstance(frontmatter.get("knowledge_id"), str):
            existing = by_id.get(frontmatter["knowledge_id"])
            if existing is not None and existing.name != path.name:
                errors.append(
                    f"Duplicate Knowledge ID {frontmatter['knowledge_id']} uses different stable filenames: "
                    f"{existing.name} and {path.name}."
                )
            by_id[frontmatter["knowledge_id"]] = path
    return [by_id[key] for key in sorted(by_id)], errors


def _validate_evidence_closure(
    knowledge_files: list[Path], ledger_file: Path, evidence_file: Path | None, branch_id: str
) -> list[str]:
    refs: set[tuple[str, int]] = set()
    for path in [*knowledge_files, ledger_file]:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        refs.update(
            (identity, int(revision))
            for identity, revision in re.findall(r"evidence:(E-\d{3})@([1-9]\d*)", text)
        )
    if not refs:
        return []
    if evidence_file is None:
        return ["Knowledge or Ledger cites Evidence but no live or staged Evidence state exists."]
    errors: list[str] = []
    evidence = _yaml(evidence_file, "Evidence closure", errors)
    if evidence is None:
        return errors
    if evidence.get("branch_id") != branch_id:
        errors.append("Evidence closure belongs to a different branch.")
    heads = {
        record.get("id"): record.get("record_revision")
        for record in evidence.get("evidence", [])
        if isinstance(record, dict)
    } if isinstance(evidence.get("evidence"), list) else {}
    for identity, revision in sorted(refs):
        if heads.get(identity) != revision:
            errors.append(f"Evidence ref evidence:{identity}@{revision} does not resolve to the staged/live head.")
    return errors


def _validate_current_knowledge_closure(
    research_file: Path, knowledge_files: list[Path]
) -> list[str]:
    errors: list[str] = []
    by_id: dict[str, tuple[dict[str, Any], Path]] = {}
    for path in knowledge_files:
        frontmatter, _, parse_errors = parse_document(path)
        if parse_errors or frontmatter is None:
            continue
        identity = frontmatter.get("knowledge_id")
        if isinstance(identity, str):
            by_id[identity] = (frontmatter, path)
    research_frontmatter, research_body, _ = _frontmatter(research_file.read_text(encoding="utf-8"))
    branch = research_frontmatter.get("branch_id") if research_frontmatter else None
    pending = re.findall(r"knowledge:(K-\d{3})@([1-9]\d*)", research_body)
    visited: set[str] = set()
    while pending:
        identity, pinned_text = pending.pop()
        ref = f"knowledge:{identity}@{pinned_text}"
        if ref in visited:
            continue
        visited.add(ref)
        current = by_id.get(identity)
        if current is None:
            errors.append(f"Current Research Knowledge closure is missing {ref}.")
            continue
        frontmatter, _ = current
        if frontmatter.get("revision") != int(pinned_text):
            errors.append(f"Current Research Knowledge closure has stale dependency {ref}.")
            continue
        if frontmatter.get("branch_id") != branch:
            errors.append(f"Current Research Knowledge closure crosses branch at {ref}.")
        for dependency in frontmatter.get("knowledge_refs", []):
            match = re.fullmatch(r"knowledge:(K-\d{3})@([1-9]\d*)", str(dependency))
            if match:
                pending.append((match.group(1), match.group(2)))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--action-id", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--artifact-path", required=True)
    parser.add_argument("--artifact-file", type=Path, required=True)
    parser.add_argument("--research-head-file", type=Path)
    parser.add_argument("--charter-file", type=Path, required=True)
    parser.add_argument("--ledger-before-file", type=Path, required=True)
    parser.add_argument("--ledger-file", type=Path, required=True)
    parser.add_argument("--knowledge-new", nargs=2, action="append", default=[], metavar=("PATH", "FILE"))
    parser.add_argument("--knowledge-cas", nargs=3, action="append", default=[], metavar=("PATH", "REV", "FILE"))
    parser.add_argument("--config-before-file", type=Path)
    parser.add_argument("--config-file", type=Path)
    parser.add_argument("--evidence-new", type=Path)
    parser.add_argument("--evidence-cas", nargs=2, metavar=("REV", "FILE"))
    parser.add_argument("--cas-step", nargs=4, action="append", default=[])
    args = parser.parse_args(argv)

    errors: list[str] = []
    project_root = args.project_root.resolve()
    staged_knowledge = [Path(item[-1]) for item in args.knowledge_new + args.knowledge_cas]
    staged_files = [args.artifact_file, *staged_knowledge]
    if args.config_file:
        staged_files.append(args.config_file)
    if args.ledger_file.resolve() != args.ledger_before_file.resolve():
        staged_files.append(args.ledger_file)
    if args.evidence_new:
        staged_files.append(args.evidence_new)
    if args.evidence_cas:
        staged_files.append(Path(args.evidence_cas[1]))
    for staged_file in staged_files:
        try:
            staged_file.resolve().relative_to(project_root)
        except ValueError:
            continue
        errors.append(
            f"Candidate file must come from an external caller-supplied mktemp directory: {staged_file}."
        )
    research_files = [path for path in [args.research_head_file, args.artifact_file] if path is not None]

    current_knowledge, merge_errors = _merged_knowledge_files(project_root, staged_knowledge)
    errors.extend(merge_errors)
    errors.extend(_validate_research_head(project_root, args.artifact_file, args.research_head_file))
    for candidate in staged_knowledge:
        errors.extend(
            validate_workpaper(
                candidate,
                project_root,
                research_files=research_files,
                current_knowledge_files=current_knowledge,
            )
        )
    errors.extend(
        validate_files(
            args.artifact_file,
            args.charter_file,
            args.ledger_before_file,
            args.ledger_file,
            project_root=project_root,
            knowledge_files=current_knowledge,
        )
    )
    errors.extend(_validate_current_knowledge_closure(args.artifact_file, current_knowledge))

    artifact_match = re.fullmatch(r"_bewater-output/artifacts/(ART-\d{3})-r([1-9]\d*)-research\.md", args.artifact_path)
    staged_research, _, _ = _frontmatter(args.artifact_file.read_text(encoding="utf-8"))
    if not artifact_match or staged_research is None or (
        artifact_match.group(1) != staged_research.get("artifact_id")
        or int(artifact_match.group(2)) != staged_research.get("revision")
    ):
        errors.append("Research artifact path must be the matching immutable artifacts/ ART-NNN revision.")

    ledger_changed = args.ledger_before_file.read_bytes() != args.ledger_file.read_bytes()
    ledger_steps = [step for step in args.cas_step if step[1] == "_bewater/ledger.yaml"]
    if ledger_changed and (
        len(ledger_steps) != 1 or Path(ledger_steps[0][3]).resolve() != args.ledger_file.resolve()
    ):
        errors.append("A changed staged ledger requires exactly one ledger CAS using --ledger-file.")
    if not ledger_changed and ledger_steps:
        errors.append("An unchanged staged ledger must omit the ledger CAS.")
    live_ledger = project_root / "_bewater" / "ledger.yaml"
    if not live_ledger.is_file() or live_ledger.read_bytes() != args.ledger_before_file.read_bytes():
        errors.append("Pre-transaction ledger does not match the live project ledger bytes.")
    if ledger_changed and ledger_steps:
        before_ledger = _yaml(args.ledger_before_file, "Pre-transaction ledger", errors)
        after_ledger = _yaml(args.ledger_file, "Staged ledger", errors)
        if before_ledger is not None and after_ledger is not None and (
            ledger_steps[0][2] != str(before_ledger.get("revision"))
            or after_ledger.get("revision") != before_ledger.get("revision", 0) + 1
        ):
            errors.append("Ledger CAS expected revision and staged envelope must advance the live ledger by one.")

    new_ids: list[int] = []
    for target, candidate_name in args.knowledge_new:
        candidate = Path(candidate_name)
        match = re.fullmatch(r"_bewater-output/knowledge/(K-(\d{3}))-[a-z0-9]+(?:-[a-z0-9]+)*\.md", target)
        frontmatter, _, parse_errors = parse_document(candidate)
        errors.extend(parse_errors)
        if not match or frontmatter is None or frontmatter.get("knowledge_id") != match.group(1) or frontmatter.get("revision") != 1:
            errors.append("A new Knowledge step requires matching stable K-NNN path and revision 1 content.")
        else:
            new_ids.append(int(match.group(2)))
        occupied = project_root / target
        if occupied.exists() and occupied.read_bytes() != candidate.read_bytes():
            errors.append(f"Knowledge allocation target is occupied by different bytes: {target}.")

    for target, expected, candidate_name in args.knowledge_cas:
        candidate = Path(candidate_name)
        match = re.fullmatch(r"_bewater-output/knowledge/(K-\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md", target)
        frontmatter, _, parse_errors = parse_document(candidate)
        errors.extend(parse_errors)
        expected_revision = int(expected) if expected.isdigit() else None
        if (
            not match or frontmatter is None or frontmatter.get("knowledge_id") != match.group(1)
            or expected_revision is None or frontmatter.get("revision") != expected_revision + 1
        ):
            errors.append("A Knowledge CAS must revise the same stable K path by exactly one revision.")
        live = project_root / target
        if not live.is_file():
            errors.append(f"Knowledge CAS target does not exist: {target}.")
        elif live.read_bytes() != candidate.read_bytes():
            live_frontmatter, _, live_errors = parse_document(live)
            errors.extend(live_errors)
            if (
                live_frontmatter is None
                or live_frontmatter.get("knowledge_id") != (match.group(1) if match else None)
                or live_frontmatter.get("revision") != expected_revision
            ):
                errors.append(f"Knowledge CAS expected revision {expected} does not match live same-path head.")

    config_step: dict[str, Any] | None = None
    if new_ids:
        if args.config_before_file is None or args.config_file is None:
            errors.append("New Knowledge allocation requires config before/after files and config CAS.")
        else:
            before = _yaml(args.config_before_file, "Current config", errors)
            after = _yaml(args.config_file, "Staged config", errors)
            if before is not None and after is not None:
                actual_config_path = project_root / "_bewater" / "config.yaml"
                if not actual_config_path.is_file() or actual_config_path.read_bytes() not in {
                    args.config_before_file.read_bytes(), args.config_file.read_bytes()
                }:
                    errors.append("Current project config does not match the supplied before/after revision; stale config.")
                expected_id = before.get("next_ids", {}).get("knowledge")
                if sorted(new_ids) != list(range(expected_id, expected_id + len(new_ids))) if isinstance(expected_id, int) else True:
                    errors.append("New Knowledge IDs must allocate contiguously from config.next_ids.knowledge.")
                expected_after = expected_id + len(new_ids) if isinstance(expected_id, int) else None
                if after.get("next_ids", {}).get("knowledge") != expected_after or after.get("revision") != before.get("revision", 0) + 1:
                    errors.append("Staged config must advance revision and next_ids.knowledge exactly once.")
                expected_config = yaml.safe_load(yaml.safe_dump(before))
                expected_config["revision"] = before.get("revision", 0) + 1
                expected_config.setdefault("next_ids", {})["knowledge"] = expected_after
                if after != expected_config:
                    errors.append("Staged config may change only revision and next_ids.knowledge for this Sprint allocation.")
                config_step = {
                    "step_id": "knowledge-counter", "op": "cas_commit", "path": "_bewater/config.yaml",
                    "expected_revision": before.get("revision"),
                    "new_text": _canonical_text(args.config_file, "Staged config", errors),
                }
    elif args.config_before_file is not None or args.config_file is not None:
        errors.append("Knowledge revisions do not allocate IDs and must omit config counter files.")

    for _step_id, path, expected_text, text_file in args.cas_step:
        if not expected_text.isdigit():
            errors.append(f"Generic CAS expected revision must be a non-negative integer for {path}.")
        if path not in {"_bewater/ledger.yaml", "_bewater/config.yaml"}:
            errors.append(f"Generic --cas-step target is not allowed: {path}; use a dedicated canonical step.")
        if path == "_bewater/config.yaml":
            errors.append("Generic --cas-step cannot write config; use the dedicated config allocation step.")
        if path.startswith("_bewater-output/sources/") or "config-after-sprint" in path:
            errors.append("Source and staged config files are never canonical plan steps.")
        _canonical_text(Path(text_file), f"CAS candidate {path}", errors)

    if args.evidence_new and args.evidence_cas:
        errors.append("Evidence uses either write_new or CAS, never both.")
    evidence_step: dict[str, Any] | None = None
    if args.evidence_new:
        evidence = _yaml(args.evidence_new, "Staged Evidence", errors)
        if evidence is not None and (
            evidence.get("revision") != 1
            or evidence.get("branch_id") != (staged_research or {}).get("branch_id")
            or not evidence.get("evidence")
        ):
            errors.append("First Evidence write requires revision 1, same branch, and at least one record.")
        evidence_step = {
            "step_id": "evidence-new", "op": "write_new", "path": "_bewater/evidence.yaml",
            "new_text": _canonical_text(args.evidence_new, "Staged Evidence", errors),
        }
        live_evidence_path = project_root / "_bewater/evidence.yaml"
        if live_evidence_path.exists() and live_evidence_path.read_bytes() != args.evidence_new.read_bytes():
            errors.append("Evidence write_new target is occupied by different bytes.")
    elif args.evidence_cas:
        expected, evidence_name = args.evidence_cas
        expected_revision = int(expected) if expected.isdigit() else None
        evidence_file = Path(evidence_name)
        evidence = _yaml(evidence_file, "Staged Evidence", errors)
        live = project_root / "_bewater/evidence.yaml"
        if expected_revision is None or evidence is None or evidence.get("revision") != expected_revision + 1:
            errors.append("Evidence CAS must advance the envelope revision by one.")
        if not live.is_file():
            errors.append("Evidence CAS requires an existing live Evidence file.")
        elif live.read_bytes() != evidence_file.read_bytes():
            live_evidence = _yaml(live, "Live Evidence", errors)
            if live_evidence is None or live_evidence.get("revision") != expected_revision:
                errors.append("Evidence CAS expected revision does not match the live envelope.")
        if expected_revision is not None:
            evidence_step = {
                "step_id": "evidence", "op": "cas_commit", "path": "_bewater/evidence.yaml",
                "expected_revision": expected_revision,
                "new_text": _canonical_text(evidence_file, "Staged Evidence", errors),
            }

    closure_evidence_file: Path | None
    if args.evidence_new:
        closure_evidence_file = args.evidence_new
    elif args.evidence_cas:
        closure_evidence_file = Path(args.evidence_cas[1])
    else:
        live_evidence = project_root / "_bewater/evidence.yaml"
        closure_evidence_file = live_evidence if live_evidence.is_file() else None
    errors.extend(
        _validate_evidence_closure(
            current_knowledge,
            args.ledger_file,
            closure_evidence_file,
            str((staged_research or {}).get("branch_id")),
        )
    )

    if errors:
        print("Research Sprint validation failed; no write plan was emitted.", file=sys.stderr)
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    steps: list[dict[str, Any]] = []
    for target, candidate_name in args.knowledge_new:
        identity = target.split("/")[-1].split("-", 2)[:2]
        steps.append({
            "step_id": f"knowledge-new-{'-'.join(identity)}", "op": "write_new", "path": target,
            "new_text": Path(candidate_name).read_text(encoding="utf-8"),
        })
    for target, expected, candidate_name in args.knowledge_cas:
        identity = re.search(r"K-\d{3}", target).group(0)
        steps.append({
            "step_id": f"knowledge-revise-{identity}", "op": "cas_commit", "path": target,
            "expected_revision": int(expected), "new_text": Path(candidate_name).read_text(encoding="utf-8"),
        })
    steps.append({
        "step_id": "research-revision", "op": "write_new", "path": args.artifact_path,
        "new_text": args.artifact_file.read_text(encoding="utf-8"),
    })
    if evidence_step is not None:
        steps.append(evidence_step)
    for step_id, path, expected, text_file in args.cas_step:
        steps.append({
            "step_id": step_id, "op": "cas_commit", "path": path,
            "expected_revision": int(expected), "new_text": Path(text_file).read_text(encoding="utf-8"),
        })
    if config_step is not None:
        steps.append(config_step)
    print(json.dumps({"action_id": args.action_id, "owner": args.owner, "steps": steps}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
