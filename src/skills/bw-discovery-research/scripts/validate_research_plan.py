#!/usr/bin/env python3
"""Validate a staged Research Plan and its pre/post transaction ledgers."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


CORE_SECTIONS = ("Research Objective", "Learning Plan", "Next Sprint", "Research Progress")
LP_REQUIRED_FIELDS = {
    "id", "learning_objective", "starting_state", "starting_view", "decision_relevance",
    "lens", "priority",
}
LP_FIELDS = LP_REQUIRED_FIELDS | {"ledger_ref"}
RM_FIELDS = {
    "id", "learning_refs", "evidence_needed", "method_source_bundle", "exclusions",
    "dependencies", "owner", "bounded_budget", "stop_condition", "expected_output", "limitation",
}
PROGRESS_FIELDS = {
    "learning_ref", "answer_status", "knowledge_refs", "current_answer", "remaining_gap",
}
KNOWLEDGE_REF_RE = re.compile(r"knowledge:(K-\d{3})@([1-9]\d*)\Z")


def _read_yaml(path: Path, label: str) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return None, [f"{label} cannot be read as YAML: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{label} must be a YAML mapping."]
    return data, []


def _frontmatter(text: str) -> tuple[dict[str, Any] | None, str, list[str]]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", text, re.DOTALL)
    if not match:
        return None, text, ["Research Plan must begin with YAML frontmatter."]
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, match.group(2), [f"Research Plan frontmatter is invalid YAML: {exc}"]
    if not isinstance(data, dict):
        return None, match.group(2), ["Research Plan frontmatter must be a mapping."]
    return data, match.group(2), []


def _section(body: str, heading: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$\n?(.*?)(?=^##\s+|\Z)",
        body,
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    return match.group(1) if match else ""


def _yaml_rows(body: str, heading: str) -> tuple[list[dict[str, Any]], list[str]]:
    section = _section(body, heading)
    match = re.search(r"```ya?ml\s*\n(.*?)\n```", section, re.DOTALL | re.IGNORECASE)
    if not match:
        return [], [f"{heading} must contain one YAML row list."]
    try:
        rows = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return [], [f"{heading} YAML is invalid: {exc}"]
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        return [], [f"{heading} YAML must be a list of mappings."]
    return rows, []


def _validate_rows(body: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    headings = re.findall(r"^##\s+(.+?)\s*$", body, re.MULTILINE)
    for heading in CORE_SECTIONS:
        if heading.lower() not in {item.lower() for item in headings}:
            errors.append(f"Research Plan is missing core section {heading}.")

    lp, row_errors = _yaml_rows(body, "Learning Plan")
    errors.extend(row_errors)
    rm, row_errors = _yaml_rows(body, "Next Sprint")
    errors.extend(row_errors)
    progress, row_errors = _yaml_rows(body, "Research Progress")
    errors.extend(row_errors)

    lp_ids: set[str] = set()
    for index, row in enumerate(lp, 1):
        missing = LP_REQUIRED_FIELDS - set(row)
        if missing:
            errors.append(f"Learning Plan row {index} is missing {sorted(missing)}.")
        extra = set(row) - LP_FIELDS
        if extra:
            errors.append(f"Learning Plan row {index} has forbidden fields {sorted(extra)}; answer_status belongs to Research Progress.")
        item_id = row.get("id")
        if not isinstance(item_id, str) or not re.fullmatch(r"LP-\d{3}", item_id):
            errors.append(f"Learning Plan row {index} id must match LP-NNN.")
        else:
            lp_ids.add(item_id)
        if row.get("starting_state") not in {"known", "think-known", "unknown", "assumption"}:
            errors.append(f"Learning Plan {item_id} has an invalid starting_state.")

    for index, row in enumerate(rm, 1):
        if RM_FIELDS - set(row):
            errors.append(f"Next Sprint row {index} is incomplete.")
        mission_id = row.get("id")
        if not isinstance(mission_id, str) or not re.fullmatch(r"RM-\d{3}", mission_id):
            errors.append(f"Next Sprint row {index} id must match RM-NNN.")
        refs = row.get("learning_refs")
        if not isinstance(refs, list) or not refs or not set(refs) <= lp_ids:
            errors.append(f"Next Sprint {mission_id} must reference existing Learning Plan items.")

    index_refs: list[str] = []
    progress_by_learning: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(progress, 1):
        if PROGRESS_FIELDS - set(row):
            errors.append(f"Research Progress row {index} is incomplete.")
        extra = set(row) - PROGRESS_FIELDS
        if extra:
            errors.append(f"Research Progress row {index} has forbidden fields {sorted(extra)}.")
        ref = row.get("learning_ref")
        if isinstance(ref, str):
            index_refs.append(ref)
            progress_by_learning[ref] = row
        if row.get("answer_status") not in {"not-researched", "partial", "answered", "dropped", "gap-accepted"}:
            errors.append(f"Research Progress {ref} has an invalid answer_status.")
        knowledge_refs = row.get("knowledge_refs")
        if not isinstance(knowledge_refs, list) or any(
            not KNOWLEDGE_REF_RE.fullmatch(str(knowledge_ref))
            for knowledge_ref in knowledge_refs
        ):
            errors.append(
                f"Research Progress {ref} knowledge_refs must contain exact Knowledge revisions."
            )
        if row.get("answer_status") in {"partial", "answered"} and not knowledge_refs:
            errors.append(f"Research Progress {ref} requires complete Knowledge for {row.get('answer_status')} status.")
    if len(index_refs) != len(set(index_refs)) or set(index_refs) != lp_ids:
        errors.append("Every Learning Plan item must have exactly one Research Progress row.")
    for row in lp:
        progress_row = progress_by_learning.get(str(row.get("id")), {})
        if row.get("starting_state") == "known" and not progress_row.get("knowledge_refs"):
            errors.append(
                f"Learning Plan {row.get('id')} cannot be known from Assessment text without independent Knowledge."
            )
    for forbidden in ("Source Inventory", "Full Analysis"):
        if _section(body, forbidden):
            errors.append(f"Research Plan must not contain {forbidden}; put it in a Knowledge workpaper or Source file.")
    for heading in ("Sprint Decision", "Insight Ingredients and Insight Readiness"):
        section = _section(body, heading)
        if section and not re.search(r"knowledge:K-\d{3}@[1-9]\d*", section):
            errors.append(f"{heading} must cite relevant exact Knowledge refs.")
    insight = _section(body, "Insight Ingredients and Insight Readiness")
    if insight and re.search(r"\b(?:sign(?:ed|off)?\s+F/P/E/T|pre-approve(?:d)?\s+Insight)\b", insight, re.IGNORECASE):
        errors.append("Insight Ingredients must not pre-approve an Insight or perform F/P/E/T judgment.")
    return lp, progress, errors


def _validate_frontmatter(
    frontmatter: dict[str, Any], charter: dict[str, Any]
) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    for field, expected in {"kind": "research", "stage": "discover", "signoffs": []}.items():
        if frontmatter.get(field) != expected:
            errors.append(f"Research Plan frontmatter {field} must be {expected!r}.")
    artifact_id, revision = frontmatter.get("artifact_id"), frontmatter.get("revision")
    if not isinstance(artifact_id, str) or not re.fullmatch(r"ART-\d{3}", artifact_id) or not isinstance(revision, int) or revision < 1:
        errors.append("Research Plan requires an ART-NNN artifact_id and positive revision.")
        research_ref = None
    else:
        research_ref = f"artifact:{artifact_id}@{revision}"
    charter_id, charter_revision = charter.get("artifact_id"), charter.get("revision")
    charter_ref = f"artifact:{charter_id}@{charter_revision}"
    if charter.get("kind") != "charter":
        errors.append("The lineage input must be kind: charter.")
    if charter.get("branch_id") != frontmatter.get("branch_id"):
        errors.append("Research Plan and Charter must belong to the same branch.")
    derived = frontmatter.get("derived_from")
    if derived != [charter_ref]:
        errors.append("Research Plan derived_from must contain the exact Charter revision only.")
    if isinstance(derived, list) and any(str(ref).startswith("assumption:") for ref in derived):
        errors.append("Assumption refs never enter Research Plan derived_from.")
    return research_ref, errors


def _validate_ledger(
    lp: list[dict[str, Any]], before: dict[str, Any], after: dict[str, Any], research_ref: str | None
) -> list[str]:
    errors: list[str] = []
    before_records = before.get("assumptions", {})
    after_records = after.get("assumptions", {})
    if not isinstance(before_records, dict) or not isinstance(after_records, dict):
        return ["Both ledgers must contain an assumptions mapping."]

    for assumption_id, record in after_records.items():
        if not isinstance(record, dict) or record.get("layer") != "root":
            continue
        if assumption_id not in before_records:
            if record.get("derived_from") != [research_ref]:
                errors.append(f"new root {assumption_id} must derive from exact {research_ref}.")
            if record.get("impact") == "high" and record.get("uncertainty") == "high" and record.get("l4_obligation_status") != "open":
                errors.append(f"New high/high root {assumption_id} must open the durable L4 obligation.")
        else:
            previous = before_records[assumption_id]
            if isinstance(previous, dict):
                provenance = previous.get("derived_from", [])
                is_legacy = any(re.fullmatch(r"artifact:ART-\d+@\d+", str(ref)) for ref in provenance)
                if is_legacy and record.get("derived_from") != provenance:
                    errors.append(f"grandfathered root {assumption_id} must retain its exact Charter provenance; no reparenting.")

    for row in lp:
        ref = row.get("ledger_ref")
        if ref is None:
            continue
        match = re.fullmatch(r"assumption:(A-\d+)@(\d+)", str(ref))
        record = after_records.get(match.group(1)) if match else None
        if (
            not match
            or not isinstance(record, dict)
            or record.get("record_revision") != int(match.group(2))
        ):
            errors.append(
                f"Learning Plan {row.get('id')} ledger_ref must resolve to the exact staged record revision."
            )
    return errors


def _validate_current_knowledge(
    progress: list[dict[str, Any]], branch_id: str, knowledge_files: list[Path],
    known_learning_refs: set[str],
) -> list[str]:
    errors: list[str] = []
    heads: dict[str, tuple[int, str, str]] = {}
    for path in knowledge_files:
        frontmatter, _, parse_errors = _frontmatter(path.read_text(encoding="utf-8"))
        if parse_errors or frontmatter is None:
            errors.extend(parse_errors)
            continue
        identity, revision = frontmatter.get("knowledge_id"), frontmatter.get("revision")
        if isinstance(identity, str) and isinstance(revision, int):
            heads[identity] = (revision, str(frontmatter.get("branch_id")), str(frontmatter.get("status")))
    for row in progress:
        refs = row.get("knowledge_refs")
        if not isinstance(refs, list):
            continue
        complete_count = 0
        for ref in refs:
            match = KNOWLEDGE_REF_RE.fullmatch(str(ref))
            if not match:
                continue
            head = heads.get(match.group(1))
            if head is None or head[0] != int(match.group(2)):
                errors.append(f"Research Progress Knowledge ref {ref} must match the current workpaper revision.")
            elif head[1] != branch_id:
                errors.append(f"Research Progress Knowledge ref {ref} belongs to a different branch.")
            elif head[2] == "complete":
                complete_count += 1
        if row.get("answer_status") in {"partial", "answered"} and complete_count == 0:
            errors.append(f"Research Progress {row.get('learning_ref')} requires at least one complete Knowledge workpaper.")
        if row.get("learning_ref") in known_learning_refs and complete_count == 0:
            errors.append(f"Learning Plan {row.get('learning_ref')} starting_state known requires complete Knowledge.")
    return errors


def validate_files(
    artifact_file: Path, charter_file: Path, ledger_before_file: Path, ledger_file: Path,
    *, project_root: Path | None = None, knowledge_files: list[Path] | None = None,
    resolve_knowledge: bool = True,
) -> list[str]:
    try:
        text = artifact_file.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"Research Plan cannot be read: {exc}"]
    frontmatter, body, errors = _frontmatter(text)
    try:
        charter_text = charter_file.read_text(encoding="utf-8")
    except OSError as exc:
        return errors + [f"Charter cannot be read: {exc}"]
    charter, _, charter_errors = _frontmatter(charter_text)
    errors.extend(charter_errors)
    before, before_errors = _read_yaml(ledger_before_file, "Pre-transaction ledger")
    after, after_errors = _read_yaml(ledger_file, "Staged ledger")
    errors.extend(before_errors + after_errors)
    if frontmatter is None or charter is None or before is None or after is None:
        return errors
    research_ref, fm_errors = _validate_frontmatter(frontmatter, charter)
    errors.extend(fm_errors)
    lp, progress, row_errors = _validate_rows(body)
    errors.extend(row_errors)
    errors.extend(_validate_ledger(lp, before, after, research_ref))
    if resolve_knowledge:
        files = knowledge_files
        if files is None and project_root is not None:
            files = sorted((project_root / "_bewater-output" / "knowledge").glob("K-*.md"))
        known_refs = {str(row.get("id")) for row in lp if row.get("starting_state") == "known"}
        errors.extend(
            _validate_current_knowledge(
                progress, str(frontmatter.get("branch_id")), files or [], known_refs
            )
        )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-file", type=Path, required=True)
    parser.add_argument("--charter-file", type=Path, required=True)
    parser.add_argument("--ledger-before-file", type=Path, required=True)
    parser.add_argument("--ledger-file", type=Path, required=True)
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--knowledge-file", type=Path, action="append", default=[])
    parser.add_argument("--historical", action="store_true")
    args = parser.parse_args(argv)
    errors = validate_files(
        args.artifact_file, args.charter_file, args.ledger_before_file, args.ledger_file,
        project_root=args.project_root, knowledge_files=args.knowledge_file,
        resolve_knowledge=not args.historical,
    )
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
