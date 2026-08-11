"""Canonical Solution validation and deterministic Markdown projection."""
from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any

import yaml

from . import schema

Issue = schema.Issue
Artifact = tuple[schema.ArtifactMeta, dict, str]

_ALLOWED_PATHS = {"linear-refine", "pivot", "hybridize", "scope-extend"}
_TOP_LEVEL_BLOCKS = (
    "definition",
    "how_it_works",
    "how_to_implement",
    "how_it_makes_money",
    "validation",
)
_DEFINITION_FIELDS = (
    "definition.name",
    "definition.pithy_proposition",
    "definition.what_it_is",
    "definition.who_its_for",
    "definition.dual_sided.money.commercial_value_proposition",
    "definition.dual_sided.money.leverageable_assets",
    "definition.dual_sided.magic.consumer_value_proposition",
    "definition.dual_sided.magic.consumer_target",
    "definition.dual_sided.tension",
    "definition.dual_sided.balance_choice",
)
_DIMENSION_FIELDS = tuple(
    f"definition.dimensions.{name}"
    for name in (
        "path_to_market",
        "right_to_win",
        "product_or_service_platform",
        "source_of_business",
        "product_or_service_design",
        "enabling_technology",
        "reason_to_believe",
        "branding",
        "consumer_experience",
    )
)
_WORK_FIELDS = (
    "step",
    "action",
    "consumer_benefit",
    "operational_benefit",
    "strategic_rationale",
    "legal_regulatory_rationale",
    "evidence_refs",
    "design_refs",
)
_IMPLEMENT_FIELDS = (
    "phase",
    "timing",
    "objective",
    "jobs_to_be_done",
    "capabilities_and_assets",
    "owner",
    "dependencies",
    "risks",
    "open_questions",
    "pilot_and_rollout",
)
_MONEY_FIELDS = (
    "how_it_makes_money.revenue_streams",
    "how_it_makes_money.pricing_and_volume_logic",
    "how_it_makes_money.adoption_retention_frequency_assumptions",
    "how_it_makes_money.development_and_operating_costs",
    "how_it_makes_money.scenarios.base",
    "how_it_makes_money.scenarios.aggressive",
    "how_it_makes_money.sensitivity",
    "how_it_makes_money.unresolved_model_gaps",
)
_SCENARIO_FIELDS = ("revenue", "margin", "earnings", "investment", "payback")
_VALIDATION_FIELDS = (
    "validation.consumer_desire",
    "validation.commercial_value",
    "validation.feasibility_and_implementation",
    "validation.achilles_assumption_refs",
    "validation.experiment_refs",
    "validation.evidence_refs",
    "validation.invalidated_claims",
)
_ASSUMPTION_REF = re.compile(r"^assumption:(A-\d+)@(\d+)$")


def render_solution_body(frontmatter: dict) -> str:
    """Render the five canonical Solution blocks in stable Markdown."""
    name = str((frontmatter.get("definition") or {}).get("name") or "Solution")
    labels = (
        ("Definition", "definition"),
        ("How It Works", "how_it_works"),
        ("How To Implement", "how_to_implement"),
        ("How It Makes Money", "how_it_makes_money"),
        ("Validation", "validation"),
    )
    sections = [f"# {name}"]
    for label, key in labels:
        rendered = yaml.safe_dump(
            frontmatter.get(key),
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
        ).rstrip()
        sections.append(f"## {label}\n\n```yaml\n{rendered}\n```")
    return "\n\n".join(sections) + "\n"


def solution_issues(artifacts: list[Artifact], ledger: schema.Ledger) -> list[Issue]:
    """Return structural, projection, lineage, and readiness issues."""
    index = _artifact_index(artifacts)
    issues: list[Issue] = []
    for meta, frontmatter, body in artifacts:
        if meta.kind != schema.ArtifactKind.solution:
            continue
        issues.extend(_one_solution_issues(meta, frontmatter, body, index, ledger))
    return issues


def _artifact_index(artifacts: Iterable[Artifact]) -> dict[str, dict[int, tuple[schema.ArtifactMeta, dict, str]]]:
    index: dict[str, dict[int, tuple[schema.ArtifactMeta, dict, str]]] = {}
    for entry in artifacts:
        meta = entry[0]
        index.setdefault(meta.artifact_id, {})[meta.revision] = entry
    return index


def _parse_artifact_ref(ref: Any) -> tuple[str, int] | None:
    if not isinstance(ref, str) or not ref.startswith("artifact:") or "@" not in ref:
        return None
    artifact_id, _, revision = ref[len("artifact:"):].rpartition("@")
    try:
        number = int(revision)
    except (TypeError, ValueError):
        return None
    return (artifact_id, number) if artifact_id and number > 0 else None


def _resolve_artifact(
    index: dict[str, dict[int, tuple[schema.ArtifactMeta, dict, str]]],
    ref: Any,
    kind: schema.ArtifactKind,
) -> tuple[schema.ArtifactMeta, dict, str] | None:
    parsed = _parse_artifact_ref(ref)
    if parsed is None:
        return None
    artifact_id, revision = parsed
    entry = index.get(artifact_id, {}).get(revision)
    return entry if entry is not None and entry[0].kind == kind else None


def _one_solution_issues(
    meta: schema.ArtifactMeta,
    frontmatter: dict,
    body: str,
    index: dict[str, dict[int, tuple[schema.ArtifactMeta, dict, str]]],
    ledger: schema.Ledger,
) -> list[Issue]:
    issues: list[Issue] = []
    artifact_id = meta.artifact_id
    if (
        meta.validation_status == schema.ArtifactValidationStatus.validated
        and not _has_human_validation_signoff(meta)
    ):
        issues.append(Issue(
            artifact_id,
            "solution-validation-authority",
            "validated Solution requires a human validation signoff for this exact revision",
        ))
    source = frontmatter.get("source_concepts")
    portfolio: tuple[schema.ArtifactMeta, dict, str] | None = None
    concept_ids: list[str] = []
    if not isinstance(source, dict):
        issues.append(Issue(artifact_id, "solution-source-unresolved", "source_concepts must be a mapping"))
    else:
        if source.get("path") not in _ALLOWED_PATHS:
            issues.append(Issue(artifact_id, "solution-path", f"unsupported Solution path {source.get('path')!r}"))
        raw_ids = source.get("concept_ids")
        if isinstance(raw_ids, list) and raw_ids and all(isinstance(value, str) for value in raw_ids):
            concept_ids = raw_ids
        else:
            issues.append(Issue(artifact_id, "solution-source-unresolved", "source_concepts.concept_ids must be non-empty"))
        portfolio = _resolve_artifact(index, source.get("portfolio_ref"), schema.ArtifactKind.concept_portfolio)
        if portfolio is None:
            issues.append(Issue(artifact_id, "solution-source-unresolved", "source_concepts.portfolio_ref does not resolve"))
        else:
            issues.extend(_source_concept_issues(meta, portfolio[1], concept_ids, source.get("path")))

    for block in _TOP_LEVEL_BLOCKS:
        value = frontmatter.get(block)
        if not isinstance(value, (dict, list)):
            issues.append(Issue(artifact_id, "solution-required-field", f"missing canonical block {block}"))

    missing_paths = _required_missing_paths(frontmatter)
    gap_paths, exception_paths, declaration_issues = _declared_omissions(
        meta,
        frontmatter,
        missing_paths,
    )
    issues.extend(declaration_issues)
    for path in missing_paths:
        if path in exception_paths:
            continue
        if meta.validation_status != schema.ArtifactValidationStatus.validated and path in gap_paths:
            continue
        issues.append(Issue(artifact_id, "solution-content-gap", f"missing required field {path} has no exact declaration"))

    raw_content_gaps = frontmatter.get("content_gaps")
    if (
        meta.validation_status == schema.ArtifactValidationStatus.validated
        and isinstance(raw_content_gaps, list)
        and raw_content_gaps
    ):
        issues.append(Issue(artifact_id, "solution-validated-with-gaps", "validated Solution must have empty content_gaps"))

    if _normalize_body(body) != _normalize_body(render_solution_body(frontmatter)):
        issues.append(Issue(artifact_id, "solution-projection-drift", "Markdown body differs from canonical projection"))

    obligations, obligation_issues = _required_obligations(meta, frontmatter, portfolio, concept_ids, ledger)
    issues.extend(obligation_issues)

    focused, detailed, persuasive = _quality_predicates(
        frontmatter,
        missing_paths - exception_paths,
        obligations,
    )
    if meta.validation_status == schema.ArtifactValidationStatus.validated:
        if not focused:
            issues.append(Issue(artifact_id, "solution-not-focused", "validated Solution is not Focused"))
        if not detailed:
            issues.append(Issue(artifact_id, "solution-not-detailed", "validated Solution is not Detailed"))
        if not persuasive:
            issues.append(Issue(artifact_id, "solution-not-persuasive", "validated Solution is not Persuasive"))
    return issues


def _has_human_validation_signoff(meta: schema.ArtifactMeta) -> bool:
    for signoff in meta.signoffs:
        if not isinstance(signoff, dict):
            continue
        person = str(signoff.get("person", "")).strip()
        role = str(signoff.get("role", "")).strip()
        actor_type = str(signoff.get("type", signoff.get("authority", "human"))).lower()
        obvious_machine = re.search(r"\b(ai|agent|system|assistant|model|bot)\b", person.lower())
        if (
            person
            and role
            and obvious_machine is None
            and actor_type not in {"ai", "agent", "system", "assistant", "model", "bot"}
            and signoff.get("scope") == "solution-validation"
            and signoff.get("artifact_revision") == meta.revision
        ):
            return True
    return False


def _source_concept_issues(
    meta: schema.ArtifactMeta,
    portfolio: dict,
    concept_ids: list[str],
    path: Any,
) -> list[Issue]:
    issues: list[Issue] = []
    if meta.branch_id != portfolio.get("branch_id"):
        issues.append(Issue(meta.artifact_id, "solution-source-unresolved", "Solution and Concept Portfolio branches differ"))
    concepts = {
        concept.get("id"): concept
        for concept in portfolio.get("concepts", [])
        if isinstance(concept, dict) and isinstance(concept.get("id"), str)
    }
    selected = set((portfolio.get("exit") or {}).get("selected_concept_ids") or [])
    for concept_id in concept_ids:
        if concept_id not in concepts:
            issues.append(Issue(meta.artifact_id, "solution-source-unresolved", f"Concept {concept_id} does not resolve"))
        elif concept_id not in selected:
            issues.append(Issue(meta.artifact_id, "solution-concept-unselected", f"Concept {concept_id} was not selected"))
    if path == "hybridize" and len(set(concept_ids)) < 2:
        issues.append(Issue(meta.artifact_id, "solution-path", "hybridize requires at least two source Concepts"))
    if path != "hybridize" and len(set(concept_ids)) != 1:
        issues.append(Issue(meta.artifact_id, "solution-path", f"{path} requires exactly one source Concept"))
    return issues


def _declared_omissions(
    meta: schema.ArtifactMeta,
    frontmatter: dict,
    missing_paths: set[str],
) -> tuple[set[str], set[str], list[Issue]]:
    issues: list[Issue] = []
    gap_paths: set[str] = set()
    exception_paths: set[str] = set()
    for gap in frontmatter.get("content_gaps", []) if isinstance(frontmatter.get("content_gaps"), list) else []:
        path = gap.get("field_path") if isinstance(gap, dict) else None
        reason = gap.get("reason") if isinstance(gap, dict) else None
        if (
            not isinstance(path, str)
            or path not in missing_paths
            or not str(reason or "").strip()
            or _path_value(frontmatter, path) not in (None, "", [], {})
        ):
            issues.append(Issue(meta.artifact_id, "solution-content-gap", f"invalid content gap declaration for {path!r}"))
        else:
            gap_paths.add(path)
    for exception in frontmatter.get("applicability_exceptions", []) if isinstance(frontmatter.get("applicability_exceptions"), list) else []:
        path = exception.get("field_path") if isinstance(exception, dict) else None
        rationale = exception.get("rationale") if isinstance(exception, dict) else None
        cannot_waive = isinstance(path, str) and (
            path.endswith(".source") or path == "validation.achilles_assumption_refs"
        )
        if (
            not isinstance(path, str)
            or path not in missing_paths
            or cannot_waive
            or not str(rationale or "").strip()
            or _path_value(frontmatter, path) not in (None, "", [], {})
        ):
            issues.append(Issue(meta.artifact_id, "solution-applicability-exception", f"invalid applicability exception for {path!r}"))
        else:
            exception_paths.add(path)
    return gap_paths, exception_paths, issues


def _path_value(data: Any, path: str) -> Any:
    current = data
    for name, index_text in re.findall(r"([^.\[\]]+)(?:\[(\d+)\])?", path):
        if not isinstance(current, dict) or name not in current:
            return None
        current = current[name]
        if index_text:
            if not isinstance(current, list) or int(index_text) >= len(current):
                return None
            current = current[int(index_text)]
    return current


def _is_missing(value: Any, *, allow_empty: bool = False) -> bool:
    if value is None:
        return True
    if allow_empty:
        return False
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return not value
    return False


def _required_missing_paths(frontmatter: dict) -> set[str]:
    missing: set[str] = set()
    for path in (*_DEFINITION_FIELDS, *_DIMENSION_FIELDS):
        if _is_missing(_path_value(frontmatter, path)):
            missing.add(path)

    works = frontmatter.get("how_it_works")
    if not isinstance(works, list) or not works:
        missing.add("how_it_works")
    else:
        for index, step in enumerate(works):
            for field in _WORK_FIELDS:
                if _is_missing(step.get(field) if isinstance(step, dict) else None):
                    missing.add(f"how_it_works[{index}].{field}")

    phases = frontmatter.get("how_to_implement")
    if not isinstance(phases, list) or not phases:
        missing.add("how_to_implement")
    else:
        for index, phase in enumerate(phases):
            for field in _IMPLEMENT_FIELDS:
                if _is_missing(phase.get(field) if isinstance(phase, dict) else None):
                    missing.add(f"how_to_implement[{index}].{field}")

    for path in _MONEY_FIELDS:
        allow_empty = path.endswith("unresolved_model_gaps")
        if _is_missing(_path_value(frontmatter, path), allow_empty=allow_empty):
            missing.add(path)
    for scenario in ("base", "aggressive"):
        for field in _SCENARIO_FIELDS:
            path = f"how_it_makes_money.scenarios.{scenario}.{field}"
            if _is_missing(_path_value(frontmatter, path)):
                missing.add(path)
    for collection in ("adoption_retention_frequency_assumptions", "development_and_operating_costs"):
        entries = _path_value(frontmatter, f"how_it_makes_money.{collection}")
        if isinstance(entries, list):
            for index, entry in enumerate(entries):
                for field in ("assumption", "source"):
                    if _is_missing(entry.get(field) if isinstance(entry, dict) else None):
                        missing.add(f"how_it_makes_money.{collection}[{index}].{field}")

    for path in _VALIDATION_FIELDS:
        allow_empty = path.endswith("invalidated_claims")
        if _is_missing(_path_value(frontmatter, path), allow_empty=allow_empty):
            missing.add(path)
    for section in ("consumer_desire", "commercial_value", "feasibility_and_implementation"):
        for field in ("claim", "evidence_refs"):
            path = f"validation.{section}.{field}"
            if _is_missing(_path_value(frontmatter, path)):
                missing.add(path)
    return missing


def _normalize_body(body: str) -> str:
    lines = [line.rstrip() for line in str(body).replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def _required_obligations(
    meta: schema.ArtifactMeta,
    frontmatter: dict,
    portfolio: tuple[schema.ArtifactMeta, dict, str] | None,
    concept_ids: list[str],
    ledger: schema.Ledger,
) -> tuple[list[schema.Assumption], list[Issue]]:
    required: dict[str, schema.Assumption] = {}
    portfolio_ref = (frontmatter.get("source_concepts") or {}).get("portfolio_ref")
    parsed_portfolio_ref = _parse_artifact_ref(portfolio_ref)
    selected_concept_ids = set(concept_ids)
    for assumption in ledger.assumptions.values():
        if (
            assumption.status != schema.AssumptionStatus.active
            or assumption.branch_id != meta.branch_id
            or not assumption.has_durable_l4_obligation
        ):
            continue
        derived_artifacts = [
            parsed
            for ref in assumption.derived_from
            if (parsed := _parse_artifact_ref(ref)) is not None
        ]
        concept_match = (
            assumption.layer == schema.Layer.concept
            and assumption.source_concept_id in selected_concept_ids
            and parsed_portfolio_ref is not None
            and any(
                artifact_id == parsed_portfolio_ref[0]
                and revision <= parsed_portfolio_ref[1]
                for artifact_id, revision in derived_artifacts
            )
        )
        solution_match = (
            assumption.layer == schema.Layer.solution
            and any(
                artifact_id == meta.artifact_id and revision <= meta.revision
                for artifact_id, revision in derived_artifacts
            )
        )
        if concept_match or solution_match:
            required[assumption.id] = assumption

    validation = frontmatter.get("validation") if isinstance(frontmatter.get("validation"), dict) else {}
    refs = validation.get("achilles_assumption_refs") if isinstance(validation.get("achilles_assumption_refs"), list) else []
    parsed: dict[str, int] = {}
    malformed = False
    for ref in refs:
        match = _ASSUMPTION_REF.match(str(ref))
        if match is None:
            malformed = True
            continue
        parsed[match.group(1)] = int(match.group(2))

    issues: list[Issue] = []
    if malformed or set(parsed) != set(required):
        issues.append(Issue(meta.artifact_id, "solution-achilles-set", "Achilles snapshot does not equal the required Concept-plus-Solution union"))
    elif any(parsed[assumption_id] != assumption.record_revision for assumption_id, assumption in required.items()):
        issues.append(Issue(meta.artifact_id, "solution-achilles-stale", "Achilles snapshot pins a stale record revision"))

    unresolved = [
        assumption
        for assumption in required.values()
        if assumption.evidence_level < schema.EvidenceLevel.L4
        or assumption.l4_obligation_status != "closed"
        or assumption.validation_status not in {
            schema.AssumptionValidationStatus.supported,
        }
    ]
    if meta.validation_status == schema.ArtifactValidationStatus.validated and unresolved:
        issues.append(Issue(meta.artifact_id, "solution-achilles-unresolved", "validated Solution has unresolved L4 obligations"))
    return list(required.values()), issues


def _quality_predicates(
    frontmatter: dict,
    missing_paths: set[str],
    obligations: list[schema.Assumption],
) -> tuple[bool, bool, bool]:
    focused = not any(
        path.startswith("definition.") and path != "definition.dimensions.branding"
        for path in missing_paths
    )
    detailed = not any(
        path.startswith(("definition.dimensions.", "how_it_works", "how_to_implement"))
        for path in missing_paths
    )
    persuasive = not any(
        path.startswith(("how_it_makes_money", "validation"))
        for path in missing_paths
    ) and all(
        assumption.evidence_level >= schema.EvidenceLevel.L4
        and assumption.l4_obligation_status == "closed"
        and assumption.validation_status == schema.AssumptionValidationStatus.supported
        for assumption in obligations
    )
    return focused, detailed, persuasive
