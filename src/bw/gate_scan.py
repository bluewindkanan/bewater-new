"""Strategy-gate evidence scoring (machine half).

``scan`` reads the ledger + artifacts and scores each gate criterion
pass/fail WITHOUT taking the decision. The human-facing gate skill (Plan B)
calls this, presents the result and the allowed exits, and stops.

Criteria are data-driven so later gates can be added by registering another
scorer set. This module never re-validates invariants (that is
``validate.validate_all``'s job); it only scores gate evidence.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from . import evidence, io, paths, schema
from .signoffs import has_fpet_signoff
from .solution_contract import solution_issues

# Reuse the validate module's notion of "dual-sided complete" so the gate and
# the system validator agree on what counts as single-sided. Imported lazily
# to avoid an import cycle at module load.
from .validate import _DUAL_SIDED_KINDS, _single_sided_violations  # noqa: F401  (re-exported intent)


# --- result types ---------------------------------------------------------

@dataclass(frozen=True)
class Criterion:
    """One scored gate criterion.

    ``passed`` is the mechanical pass/fail. ``blocking`` is True when a fail
    withholds the ``go`` exit. ``note`` carries human-judgment flags or scope
    detail (e.g. "requires human judgment", "scored across all active ...").
    """
    name: str
    passed: bool
    blocking: bool
    note: str | None = None


@dataclass(frozen=True)
class GateScanResult:
    criteria: list[Criterion] = field(default_factory=list)
    exit_allowed: list[str] = field(default_factory=list)


_ALL_EXITS = ["go", "conditional-go", "recycle", "pivot", "kill"]
_BLOCKED_EXITS = ["conditional-go", "recycle", "pivot", "kill"]

_HYP_MIN, _HYP_MAX = 2, 5
_OA_MIN, _OA_MAX = 2, 4


# --- artifact loading -----------------------------------------------------

def _load_artifacts(root: Path) -> list[schema.ArtifactMeta]:
    """Return every readable artifact meta under ``_bewater-output/``.

    Malformed frontmatter is skipped (the validator reports it; the gate
    only scores what it can read). De-duplicated by resolved path.
    """
    out: list[schema.ArtifactMeta] = []
    for p in paths.iter_workflow_documents(root):
        try:
            meta, _ = io.read_artifact(p)
        except (FileNotFoundError, ValueError):
            continue
        if meta.artifact_id:
            out.append(meta)
    return out


def _load_structured_artifacts(root: Path) -> list[tuple[schema.ArtifactMeta, dict, str]]:
    out: list[tuple[schema.ArtifactMeta, dict, str]] = []
    for p in paths.iter_workflow_documents(root):
        try:
            meta, body = io.read_artifact(p)
            frontmatter = io.read_frontmatter(p)
        except (FileNotFoundError, KeyError, TypeError, ValueError):
            continue
        if meta.artifact_id:
            out.append((meta, frontmatter, body))
    return out


def _is_dual_complete(meta: schema.ArtifactMeta) -> bool:
    """True iff ``meta`` is a dual-sided kind with all four elements filled."""
    if meta.kind not in _DUAL_SIDED_KINDS:
        return True
    return not _single_sided_violations(meta)


# --- G1 criterion scorers -------------------------------------------------
# Each scorer returns a ``Criterion``. They are pure functions of the loaded
# artifacts + active assumptions, so adding a criterion is a matter of
# appending a scorer to ``_G1_SCORERS``.

def _score_charter(arts, _active) -> Criterion:
    charters = [m for m in arts if m.kind == schema.ArtifactKind.charter]
    if not charters:
        # name is the failure code per the gate contract.
        return Criterion("missing-artifact", False, True, "charter not found")
    m = charters[0]
    if m.document_status != schema.ArtifactDocumentStatus.final:
        return Criterion("charter", False, True, "charter not final")
    if not _is_dual_complete(m):
        return Criterion("single-sided", False, True, "charter dual-sided incomplete")
    return Criterion("charter", True, True, None)


def _score_directional_hypotheses(arts, _active) -> Criterion:
    hyps = [m for m in arts if m.kind == schema.ArtifactKind.directional_hypothesis]
    if not (_HYP_MIN <= len(hyps) <= _HYP_MAX):
        return Criterion(
            "directional-hypotheses", False, True,
            f"gate-criteria-incomplete: expected {_HYP_MIN}-{_HYP_MAX}, found {len(hyps)}",
        )
    if any(not _is_dual_complete(h) for h in hyps):
        return Criterion("directional-hypotheses", False, True, "single-sided")
    return Criterion("directional-hypotheses", True, True, None)


def _score_insights(arts, _active) -> Criterion:
    insights = [m for m in arts if m.kind == schema.ArtifactKind.insights]
    if not insights:
        return Criterion("insights", False, True, "gate-criteria-incomplete: no insights artifact")
    # Each insights artifact must carry an F/P/E/T signoff (brief: "each").
    all_signed = all(has_fpet_signoff(m) for m in insights)
    if not all_signed:
        return Criterion("insights", False, True, "gate-criteria-incomplete: missing F/P/E/T signoff on one or more insights")
    return Criterion("insights", True, True, None)


def _score_strategy(arts, _active) -> Criterion:
    strat = [m for m in arts if m.kind == schema.ArtifactKind.strategy]
    if not strat or not strat[0].locked:
        return Criterion("strategy", False, True, "gate-criteria-incomplete: strategy not locked")
    # "Is the statement a blade?" is human judgment — flag, do not block.
    return Criterion("strategy", True, False, "requires human judgment")


def _score_opportunity_areas(arts, _active) -> Criterion:
    oas = [m for m in arts if m.kind == schema.ArtifactKind.opportunity]
    if not (_OA_MIN <= len(oas) <= _OA_MAX):
        return Criterion(
            "opportunity-areas", False, True,
            f"gate-criteria-incomplete: expected {_OA_MIN}-{_OA_MAX}, found {len(oas)}",
        )
    # Non-overlap is human judgment — flag, do not block.
    return Criterion("opportunity-areas", True, False, "requires human judgment")


def _score_achilles_quadrant(arts, active) -> Criterion:
    has_achilles = any(a.is_achilles_heel for a in active)
    if not has_achilles:
        return Criterion(
            "achilles-quadrant", False, True, "gate-criteria-incomplete: no achilles-heel on active lineage"
        )
    return Criterion("achilles-quadrant", True, True, None)


def _score_l4_obligations(_arts, active) -> Criterion:
    """L4+ behavioral evidence is a hard gate criterion."""
    open_l4 = [a for a in active if a.is_achilles_heel and a.l4_obligation_open]
    if open_l4:
        ids = ", ".join(a.id for a in open_l4)
        return Criterion(
            "l4-obligations",
            False,
            True,
            f"methodology-deviation: {len(open_l4)} Achilles with open L4 obligations: {ids}",
        )
    return Criterion("l4-obligations", True, False, None)


_G1_SCORERS = [
    _score_charter,
    _score_directional_hypotheses,
    _score_insights,
    _score_strategy,
    _score_opportunity_areas,
    _score_achilles_quadrant,
    _score_l4_obligations,
]


# --- G2 criterion scorers -------------------------------------------------

StructuredArtifact = tuple[schema.ArtifactMeta, dict, str]


def _current_artifact_heads(
    artifacts: list[StructuredArtifact],
    kind: schema.ArtifactKind,
    subject: str | None,
) -> list[StructuredArtifact]:
    by_id: dict[str, StructuredArtifact] = {}
    for entry in artifacts:
        meta = entry[0]
        if meta.kind != kind:
            continue
        if subject is not None and meta.branch_id != subject:
            continue
        current = by_id.get(meta.artifact_id)
        if current is None or meta.revision > current[0].revision:
            by_id[meta.artifact_id] = entry
    return list(by_id.values())


def _g2_solution_heads(
    artifacts: list[StructuredArtifact],
    subject: str | None,
) -> list[StructuredArtifact]:
    heads = _current_artifact_heads(artifacts, schema.ArtifactKind.solution, subject)
    return [
        entry
        for entry in heads
        if entry[0].document_status == schema.ArtifactDocumentStatus.final
        and entry[0].validation_status == schema.ArtifactValidationStatus.validated
    ]


def _score_g2_solutions(
    artifacts: list[StructuredArtifact],
    ledger: schema.Ledger,
    _active: list[schema.Assumption],
    subject: str | None,
) -> Criterion:
    solutions = _g2_solution_heads(artifacts, subject)
    if not (1 <= len(solutions) <= 2):
        return Criterion(
            "solutions",
            False,
            True,
            f"gate-criteria-incomplete: expected 1-2 complete validated Solutions, found {len(solutions)}",
        )
    blocking_issues = [
        issue
        for issue in solution_issues(artifacts, ledger)
        if issue.scope in {entry[0].artifact_id for entry in solutions}
    ]
    if blocking_issues:
        kinds = ", ".join(sorted({issue.kind for issue in blocking_issues}))
        return Criterion("solutions", False, True, f"gate-criteria-incomplete: {kinds}")
    return Criterion("solutions", True, True, None)


def _score_g2_solution_readiness(
    artifacts: list[StructuredArtifact],
    ledger: schema.Ledger,
    _active: list[schema.Assumption],
    subject: str | None,
) -> Criterion:
    solutions = _g2_solution_heads(artifacts, subject)
    if not solutions:
        return Criterion("solution-readiness", False, True, "gate-criteria-incomplete: no validated Solutions")
    issues = [
        issue
        for issue in solution_issues(artifacts, ledger)
        if issue.scope in {entry[0].artifact_id for entry in solutions}
    ]
    if issues:
        kinds = ", ".join(sorted({issue.kind for issue in issues}))
        return Criterion("solution-readiness", False, True, f"gate-criteria-incomplete: {kinds}")
    return Criterion("solution-readiness", True, False, "requires human judgment")


def _score_g2_l4_obligations(
    _artifacts: list[StructuredArtifact],
    _ledger: schema.Ledger,
    active: list[schema.Assumption],
    _subject: str | None,
) -> Criterion:
    return _score_l4_obligations([], active)


def _score_g2_investment_narrative(
    artifacts: list[StructuredArtifact],
    _ledger: schema.Ledger,
    _active: list[schema.Assumption],
    subject: str | None,
) -> Criterion:
    narratives = _current_artifact_heads(artifacts, schema.ArtifactKind.investment_narrative, subject)
    complete = [
        entry
        for entry in narratives
        if entry[0].document_status == schema.ArtifactDocumentStatus.final
        and str(entry[2]).strip()
    ]
    if not complete:
        return Criterion(
            "investment-narrative",
            False,
            True,
            "gate-criteria-incomplete: investment-narrative not found",
        )
    return Criterion("investment-narrative", True, False, "requires human judgment")


_G2_SCORERS = [
    _score_g2_solutions,
    _score_g2_solution_readiness,
    _score_g2_l4_obligations,
    _score_g2_investment_narrative,
]


# --- entry point ----------------------------------------------------------

def _active_assumptions(root: Path, subject: str | None) -> tuple[list, str | None]:
    """Return (active assumptions on the subject lineage, scope note).

    ``subject`` filters to ``branch == subject AND status == active``;
    killed/merged are excluded everywhere. ``None`` keeps all active
    assumptions and annotates the quadrant note accordingly.
    """
    ledger = io.load_ledger(root)
    if subject is None:
        active = [a for a in ledger.assumptions.values() if a.status == schema.AssumptionStatus.active]
        return active, "scored across all active assumptions"
    active = [
        a for a in ledger.assumptions.values()
        if a.branch_id == subject and a.status == schema.AssumptionStatus.active
    ]
    return active, None


def _annotate_scope(criteria: list[Criterion], note: str | None) -> None:
    """Attach the subject-scope note to the achilles-quadrant criterion."""
    if not note:
        return
    for i, c in enumerate(criteria):
        if c.name == "achilles-quadrant":
            criteria[i] = Criterion(c.name, c.passed, c.blocking, note)
            return


def _enforce_machine_evidence(
    root: Path,
    criteria: list[Criterion],
    active: list[schema.Assumption],
) -> None:
    unresolved = [
        assumption
        for assumption in active
        if assumption.validation_status == schema.AssumptionValidationStatus.supported
        and not evidence.assumption_refs_resolve(root, assumption)
    ]
    if not unresolved:
        return
    ids = ", ".join(assumption.id for assumption in unresolved)
    replacement = Criterion(
        "l4-obligations",
        False,
        True,
        f"methodology-deviation: unresolved current machine Evidence for {ids}",
    )
    for index, criterion in enumerate(criteria):
        if criterion.name == "l4-obligations":
            criteria[index] = replacement
            return
    criteria.append(replacement)


def scan(root: Path, gate: str = "G1", subject: str | None = None) -> GateScanResult:
    """Score gate ``gate`` for project ``root``; return criteria + allowed exits.

    ``subject`` scopes assumption scoring to the given solution branch's
    ACTIVE lineage (killed/merged excluded). ``go`` is withheld when any
    blocking criterion fails.
    """
    active, scope_note = _active_assumptions(root, subject)

    if gate == "G1":
        arts = _load_artifacts(root)
        criteria = [scorer(arts, active) for scorer in _G1_SCORERS]
        _annotate_scope(criteria, scope_note)
    elif gate == "G2":
        artifacts = _load_structured_artifacts(root)
        ledger = io.load_ledger(root)
        criteria = [scorer(artifacts, ledger, active, subject) for scorer in _G2_SCORERS]
    else:
        raise NotImplementedError(f"scan: gate {gate!r} not implemented")

    _enforce_machine_evidence(root, criteria, active)
    any_blocking_failed = any(not c.passed and c.blocking for c in criteria)
    exit_allowed = list(_BLOCKED_EXITS) if any_blocking_failed else list(_ALL_EXITS)
    return GateScanResult(criteria=criteria, exit_allowed=exit_allowed)
