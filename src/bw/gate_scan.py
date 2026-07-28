"""Strategy-gate evidence scoring (machine half).

``scan`` reads the ledger + artifacts and scores each gate criterion
pass/fail WITHOUT taking the decision. The human-facing gate skill (Plan B)
calls this, presents the result and the allowed exits, and stops.

Only G1 is implemented here. Criteria are data-driven so G2 (and later
gates) can be added by extending ``_GATE_CRITERIA`` / registering a new
``_scan_<gate>`` function — this module never re-validates invariants
(that is ``validate.validate_all``'s job); it only scores G1 evidence.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from . import io, paths, schema

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
    """Return every readable artifact meta under ``_bewater/artifacts/``.

    Malformed frontmatter is skipped (the validator reports it; the gate
    only scores what it can read). De-duplicated by resolved path.
    """
    art_dir = paths.artifacts_dir(root)
    if not art_dir.is_dir():
        return []
    out: list[schema.ArtifactMeta] = []
    seen: set[Path] = set()
    for p in sorted(art_dir.rglob("*.md")):
        rp = p.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        try:
            meta, _ = io.read_artifact(p)
        except (FileNotFoundError, ValueError):
            continue
        if meta.artifact_id:
            out.append(meta)
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
    if m.status != schema.ArtifactStatus.final:
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
    all_signed = all(
        any((s.get("what") if isinstance(s, dict) else None) == "F/P/E/T"
            for s in (m.signoffs or []))
        for m in insights
    )
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
    oas = [m for m in arts if m.kind == schema.ArtifactKind.opportunity_area]
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


_G1_SCORERS = [
    _score_charter,
    _score_directional_hypotheses,
    _score_insights,
    _score_strategy,
    _score_opportunity_areas,
    _score_achilles_quadrant,
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
        active = [a for a in ledger.assumptions if a.status == schema.AssumptionStatus.active]
        return active, "scored across all active assumptions"
    active = [
        a for a in ledger.assumptions
        if a.branch == subject and a.status == schema.AssumptionStatus.active
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


def scan(root: Path, gate: str = "G1", subject: str | None = None) -> GateScanResult:
    """Score gate ``gate`` for project ``root``; return criteria + allowed exits.

    ``subject`` scopes assumption scoring to the given solution branch's
    ACTIVE lineage (killed/merged excluded). ``go`` is withheld when any
    blocking criterion fails. Only ``G1`` is implemented.
    """
    if gate != "G1":
        raise NotImplementedError(f"scan: gate {gate!r} not implemented (only G1)")

    arts = _load_artifacts(root)
    active, scope_note = _active_assumptions(root, subject)

    criteria = [scorer(arts, active) for scorer in _G1_SCORERS]
    _annotate_scope(criteria, scope_note)

    any_blocking_failed = any(not c.passed and c.blocking for c in criteria)
    exit_allowed = list(_BLOCKED_EXITS) if any_blocking_failed else list(_ALL_EXITS)
    return GateScanResult(criteria=criteria, exit_allowed=exit_allowed)
