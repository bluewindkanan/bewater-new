#!/usr/bin/env python3
"""Validate stable-path Knowledge workpapers without parsing Source file formats."""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml


REQUIRED_HEADINGS = (
    "Question or hypothesis",
    "Method and scope",
    "Sources used",
    "Summary",
    "Conclusion",
    "Limitations and new questions",
)
KNOWLEDGE_REF = re.compile(r"knowledge:(K-\d{3})@([1-9]\d*)\Z")
EVIDENCE_REF = re.compile(r"evidence:E-\d{3}@[1-9]\d*\Z")
RESEARCH_REF = re.compile(r"artifact:(ART-\d{3})@([1-9]\d*)\Z")


def parse_document(path: Path) -> tuple[dict[str, Any] | None, str, list[str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return None, "", [f"Knowledge workpaper cannot be read as UTF-8 Markdown: {exc}"]
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", text, re.DOTALL)
    if not match:
        return None, text, ["Knowledge workpaper must begin with YAML frontmatter."]
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, match.group(2), [f"Knowledge frontmatter is invalid YAML: {exc}"]
    if not isinstance(frontmatter, dict):
        return None, match.group(2), ["Knowledge frontmatter must be a mapping."]
    return frontmatter, match.group(2), []


def _section(body: str, heading: str) -> str | None:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$\n?(.*?)(?=^##\s+|\Z)",
        body,
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    return match.group(1).strip() if match else None


def _knowledge_heads(knowledge_dir: Path) -> tuple[dict[str, tuple[int, str, Path]], list[str]]:
    heads: dict[str, tuple[int, str, Path]] = {}
    errors: list[str] = []
    if not knowledge_dir.is_dir():
        return heads, errors
    for candidate in sorted(knowledge_dir.glob("K-*.md")):
        frontmatter, _, parse_errors = parse_document(candidate)
        if parse_errors or frontmatter is None:
            continue
        identity = frontmatter.get("knowledge_id")
        revision = frontmatter.get("revision")
        branch = frontmatter.get("branch_id")
        if not isinstance(identity, str) or not isinstance(revision, int) or revision < 1:
            continue
        if identity in heads and heads[identity][2].resolve() != candidate.resolve():
            errors.append(
                f"Duplicate Knowledge ID {identity} appears in {heads[identity][2].name} and {candidate.name}."
            )
        else:
            heads[identity] = (revision, str(branch), candidate)
    return heads, errors


def _validate_sources(entries: Any, project_root: Path) -> list[str]:
    if not isinstance(entries, list):
        return ["source_refs must be a list."]
    errors: list[str] = []
    source_root = (project_root / "_bewater-output" / "sources").resolve()
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            errors.append(f"source_refs entry {index} must be a mapping.")
            continue
        if set(entry) == {"url"}:
            url = entry["url"]
            if not isinstance(url, str) or not re.fullmatch(r"https?://\S+", url):
                errors.append(f"source_refs entry {index} URL must preserve an exact http(s) URL.")
            continue
        if set(entry) != {"path", "sha256"}:
            errors.append(f"source_refs entry {index} must contain exactly url, or path plus sha256.")
            continue
        relative = entry["path"]
        digest = entry["sha256"]
        if not isinstance(relative, str) or Path(relative).is_absolute():
            errors.append(f"source_refs entry {index} path must be repo-relative under _bewater-output/sources/.")
            continue
        target = (project_root / relative).resolve()
        try:
            target.relative_to(source_root)
        except ValueError:
            errors.append(f"source_refs entry {index} path must remain under _bewater-output/sources/.")
            continue
        if not target.is_file():
            errors.append(f"source_refs entry {index} Source file does not exist: {relative}.")
            continue
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append(f"source_refs entry {index} sha256 must be lowercase hexadecimal.")
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != digest:
            errors.append(f"source_refs entry {index} SHA-256 does not match Source bytes.")
    return errors


def _research_documents(paths: Iterable[Path]) -> dict[str, tuple[dict[str, Any], str]]:
    documents: dict[str, tuple[dict[str, Any], str]] = {}
    for path in paths:
        frontmatter, body, errors = parse_document(path)
        if errors or frontmatter is None or frontmatter.get("kind") != "research":
            continue
        identity, revision = frontmatter.get("artifact_id"), frontmatter.get("revision")
        if isinstance(identity, str) and isinstance(revision, int):
            documents[f"artifact:{identity}@{revision}"] = (frontmatter, body)
    return documents


def validate_workpaper(
    workpaper_file: Path,
    project_root: Path,
    *,
    research_files: Iterable[Path] = (),
    current_knowledge_files: Iterable[Path] = (),
) -> list[str]:
    project_root = project_root.resolve()
    frontmatter, body, errors = parse_document(workpaper_file)
    if frontmatter is None:
        return errors

    identity = frontmatter.get("knowledge_id")
    revision = frontmatter.get("revision")
    filename = workpaper_file.name
    if not isinstance(identity, str) or not re.fullmatch(r"K-\d{3}", identity):
        errors.append("knowledge_id must match K-NNN.")
    elif not re.fullmatch(rf"{re.escape(identity)}-(?!r[1-9]\d*-)[a-z0-9]+(?:-[a-z0-9]+)*\.md", filename):
        errors.append("Knowledge uses one stable K-NNN-<short-title>.md path; K-NNN-rN fan-out is forbidden.")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        errors.append("Knowledge revision must be a positive integer.")
    if frontmatter.get("status") not in {"working", "complete"}:
        errors.append("Knowledge status must be working or complete.")
    if not isinstance(frontmatter.get("title"), str) or not frontmatter["title"].strip():
        errors.append("Knowledge title must be non-empty.")

    heads, head_errors = _knowledge_heads(project_root / "_bewater-output" / "knowledge")
    for candidate in current_knowledge_files:
        staged, _, staged_errors = parse_document(candidate)
        if staged_errors or staged is None:
            errors.extend(staged_errors)
            continue
        staged_id, staged_revision = staged.get("knowledge_id"), staged.get("revision")
        if isinstance(staged_id, str) and isinstance(staged_revision, int):
            heads[staged_id] = (staged_revision, str(staged.get("branch_id")), candidate)
    errors.extend(head_errors)
    errors.extend(_validate_sources(frontmatter.get("source_refs"), project_root))

    research_ref = frontmatter.get("research_ref")
    research_match = RESEARCH_REF.fullmatch(str(research_ref))
    documents = _research_documents(research_files)
    if not research_match or research_ref not in documents:
        errors.append("research_ref must resolve to the exact Research revision that authorized the workpaper.")
    else:
        research_frontmatter, research_body = documents[research_ref]
        if research_frontmatter.get("branch_id") != frontmatter.get("branch_id"):
            errors.append("Knowledge and its authorizing Research revision must be on the same branch.")
        learning_refs = frontmatter.get("learning_refs")
        learning_section = _section(research_body, "Learning Plan") or ""
        yaml_block = re.search(r"```ya?ml\s*\n(.*?)\n```", learning_section, re.DOTALL | re.IGNORECASE)
        try:
            learning_rows = yaml.safe_load(yaml_block.group(1)) if yaml_block else []
        except yaml.YAMLError:
            learning_rows = []
        plan_learning_ids = {
            row.get("id")
            for row in learning_rows
            if isinstance(row, dict) and re.fullmatch(r"LP-\d{3}", str(row.get("id")))
        } if isinstance(learning_rows, list) else set()
        if (
            not isinstance(learning_refs, list)
            or not learning_refs
            or any(not re.fullmatch(r"LP-\d{3}", str(ref)) for ref in learning_refs)
            or not set(learning_refs) <= plan_learning_ids
        ):
            errors.append("learning_refs must resolve inside the pinned Research revision.")

    knowledge_refs = frontmatter.get("knowledge_refs")
    method = _section(body, "Method and scope") or ""
    if not isinstance(knowledge_refs, list):
        errors.append("knowledge_refs must be a list.")
    else:
        synthesis = bool(re.search(r"\bsynthesis\b", method, re.IGNORECASE))
        if knowledge_refs and not synthesis:
            errors.append("Primary workpapers must keep knowledge_refs empty; only synthesis pins Knowledge inputs.")
        if synthesis and not knowledge_refs:
            errors.append("A synthesis workpaper requires exact Knowledge inputs.")
        for ref in knowledge_refs:
            match = KNOWLEDGE_REF.fullmatch(str(ref))
            if not match:
                errors.append("knowledge_refs must contain exact knowledge:K-NNN@n revisions.")
                continue
            target = heads.get(match.group(1))
            if target is None or target[0] != int(match.group(2)):
                errors.append(f"Knowledge dependency {ref} does not match its current workpaper revision.")
            elif target[1] != frontmatter.get("branch_id"):
                errors.append(f"Knowledge dependency {ref} belongs to a different branch.")

    evidence_refs = frontmatter.get("evidence_refs")
    if not isinstance(evidence_refs, list) or any(not EVIDENCE_REF.fullmatch(str(ref)) for ref in evidence_refs):
        errors.append("evidence_refs must contain exact Evidence revisions only.")

    for heading in REQUIRED_HEADINGS:
        if _section(body, heading) is None:
            errors.append(f"Knowledge workpaper is missing required heading {heading}.")
    if frontmatter.get("status") == "complete":
        for heading in ("Summary", "Conclusion", "Limitations and new questions"):
            if not (_section(body, heading) or "").strip():
                errors.append(f"A complete workpaper requires a non-empty {heading} section.")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workpaper-file", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--research-file", type=Path, action="append", default=[])
    args = parser.parse_args(argv)
    errors = validate_workpaper(
        args.workpaper_file,
        args.project_root,
        research_files=args.research_file,
    )
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
