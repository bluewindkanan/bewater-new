#!/usr/bin/env python3
"""Deterministic L0 validation for a staged Charter."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ALLOWED_PROVENANCE = {
    "user-stated",
    "user-selected",
    "agent-interpretation",
    "unknown",
}
REQUIRED_HEADINGS = (
    "### Original intent",
    "### Project definition",
    "### Money + Magic",
    "### Intent trace",
    "### Current knowledge state",
)
PLACEHOLDERS = {"", "-", "...", "…", "tbd", "todo", "n/a", "none"}


def _is_text(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() not in PLACEHOLDERS


def _has_placeholder(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    lowered = value.strip().lower()
    return lowered in PLACEHOLDERS or "{{" in value or "}}" in value or "<...>" in lowered


def _frontmatter(text: str) -> tuple[dict[str, Any] | None, str, list[str]]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", text, re.DOTALL)
    if not match:
        return None, text, ["Charter must begin with a complete YAML frontmatter block."]
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, match.group(2), [f"Charter frontmatter is invalid YAML: {exc}"]
    if not isinstance(frontmatter, dict):
        return None, match.group(2), ["Charter frontmatter must be a YAML mapping."]
    return frontmatter, match.group(2), []


def _section(body: str, heading: str) -> str:
    match = re.search(
        rf"^{re.escape(heading)}\s*$\n?(.*?)(?=^#{{1,3}}\s|\Z)",
        body,
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    return match.group(1) if match else ""


def _table(section: str) -> tuple[list[str], list[list[str]]] | None:
    lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(lines) < 3:
        return None

    def cells(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    header, separator = cells(lines[0]), cells(lines[1])
    if not header or not all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in separator):
        return None
    rows = [cells(line) for line in lines[2:]]
    return header, [row for row in rows if len(row) == len(header)]


def _validate_frontmatter(frontmatter: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "schema_version": 1,
        "kind": "charter",
        "stage": "immersion",
        "document_status": "draft",
        "validation_status": "unvalidated",
    }
    for key, value in expected.items():
        if frontmatter.get(key) != value:
            errors.append(f"Frontmatter {key} must be {value!r}.")
    if not _is_text(frontmatter.get("artifact_id")):
        errors.append("Frontmatter artifact_id must be non-empty.")
    if not isinstance(frontmatter.get("revision"), int) or frontmatter["revision"] < 1:
        errors.append("Frontmatter revision must be a positive integer.")
    if not _is_text(frontmatter.get("branch_id")):
        errors.append("Frontmatter branch_id must be non-empty.")
    if frontmatter.get("signoffs") != []:
        errors.append("Charter signoffs must remain empty.")

    dual_sided = frontmatter.get("dual_sided")
    if not isinstance(dual_sided, dict):
        return errors + ["Frontmatter dual_sided must be a mapping."]
    for side, fields in {
        "magic": ("consumer_value_proposition", "consumer_target"),
        "money": ("commercial_value_proposition", "leverageable_assets"),
    }.items():
        value = dual_sided.get(side)
        if not isinstance(value, dict):
            errors.append(f"dual_sided.{side} must be a mapping.")
            continue
        for field in fields:
            record = value.get(field)
            if not isinstance(record, dict) or not _is_text(record.get("statement")):
                errors.append(f"dual_sided.{side}.{field}.statement must be non-empty.")
    tension = dual_sided.get("tension")
    if not isinstance(tension, dict) or not _is_text(tension.get("statement")):
        errors.append("dual_sided.tension.statement must be non-empty.")
    if not _is_text(dual_sided.get("balance_choice")):
        errors.append("dual_sided.balance_choice must be non-empty.")
    return errors


def _validate_body(body: str) -> list[str]:
    errors = [f"Charter body is missing required heading: {heading}" for heading in REQUIRED_HEADINGS
              if not re.search(rf"^{re.escape(heading)}\s*$", body, re.MULTILINE | re.IGNORECASE)]
    if not body.strip():
        errors.append("Charter body must be non-empty.")
    if re.search(r"\b(?:TBD|TODO)\b|\{\{|\}\}", body, re.IGNORECASE):
        errors.append("Charter body contains a placeholder.")
    project_definition = _section(body, "### Project definition")
    for field in ("Challenge", "Intent and outcome", "Scope", "Constraints", "Success definition"):
        if not re.search(rf"\*\*{re.escape(field)}:\*\*\s*\S", project_definition, re.IGNORECASE):
            errors.append(f"Project definition must include a non-empty {field} field.")
    knowledge = _section(body, "### Current knowledge state")
    if not re.search(r"\*\*Unknown\*\*", knowledge, re.IGNORECASE):
        errors.append("Current knowledge state must preserve explicit Unknowns.")
    return errors


def _validate_intent_trace(body: str) -> list[str]:
    table = _table(_section(body, "### Intent trace"))
    if table is None:
        return ["Intent trace must contain a Markdown table."]
    header, rows = table
    normalized = [column.strip().lower() for column in header]
    aliases = {
        "claim": lambda column: column == "claim",
        "source": lambda column: column in {"source", "provenance"},
        "basis": lambda column: column.startswith("basis"),
    }
    indices = {
        name: next((index for index, column in enumerate(normalized) if matches(column)), None)
        for name, matches in aliases.items()
    }
    if any(index is None for index in indices.values()):
        return ["Intent trace table must contain Claim, Provenance (or Source), and Basis columns."]
    if not rows:
        return ["Intent trace must contain at least one claim."]
    errors: list[str] = []
    for row_number, row in enumerate(rows, start=1):
        for name, index in indices.items():
            assert index is not None
            if not _is_text(row[index]):
                errors.append(f"Intent trace row {row_number} {name} must be non-empty.")
        source_index = indices["source"]
        assert source_index is not None
        if row[source_index].strip().lower() not in ALLOWED_PROVENANCE:
            errors.append(
                f"Intent trace source {row[source_index]!r} is not an allowed provenance label."
            )
    return errors


def validate_files(artifact_file: Path) -> list[str]:
    """Return deterministic L0 violations; this function never writes project state."""
    try:
        text = artifact_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [f"Charter file does not exist: {artifact_file}"]
    except OSError as exc:
        return [f"Charter cannot be read: {exc}"]

    frontmatter, body, errors = _frontmatter(text)
    if frontmatter is None:
        return errors
    errors.extend(_validate_frontmatter(frontmatter))
    errors.extend(_validate_body(body))
    errors.extend(_validate_intent_trace(body))
    return errors


def validate_project_binding(artifact_file: Path, config_file: Path | None) -> list[str]:
    """Validate that the first Charter transaction binds the repository to a project name."""
    try:
        text = artifact_file.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"Charter cannot be read for project binding: {exc}"]
    frontmatter, _, errors = _frontmatter(text)
    if frontmatter is None:
        return errors
    if frontmatter.get("revision") != 1 and config_file is None:
        return []
    if config_file is None:
        return ["The first Charter transaction must CAS-commit _bewater/config.yaml with project.name."]
    try:
        config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"Candidate config for project binding is invalid: {exc}"]
    if not isinstance(config, dict):
        return ["Candidate config for project binding must be a YAML mapping."]
    project = config.get("project")
    if not isinstance(project, dict) or not _is_text(project.get("name")):
        return ["The first Charter transaction must set a non-empty project.name."]
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a staged BeWater Charter draft.")
    parser.add_argument("--artifact-file", type=Path, required=True)
    args = parser.parse_args(argv)
    errors = validate_files(args.artifact_file)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
