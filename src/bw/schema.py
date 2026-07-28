"""BeWater runtime schema: enums, dataclasses, and invariants.

Field names here are the contract consumed by io (Task 2) and all later tasks.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from bw.errors import ValidationError

# --- Enums ---

class Layer(str, Enum):
    root = "root"
    strategy = "strategy"
    opportunity = "opportunity"
    concept = "concept"
    feature = "feature"


class Category(str, Enum):
    consumer = "consumer"
    commercial = "commercial"
    technical = "technical"
    distribution = "distribution"
    regulatory = "regulatory"


class Impact(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Uncertainty(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


_EVIDENCE_ORDER = ("L1", "L2", "L3", "L4", "L5", "L6")


class EvidenceLevel(str, Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"
    L5 = "L5"
    L6 = "L6"

    def __lt__(self, other: Any) -> bool:
        return self._rank() < _coerce_evidence(other)._rank()

    def __le__(self, other: Any) -> bool:
        return self._rank() <= _coerce_evidence(other)._rank()

    def __gt__(self, other: Any) -> bool:
        return self._rank() > _coerce_evidence(other)._rank()

    def __ge__(self, other: Any) -> bool:
        return self._rank() >= _coerce_evidence(other)._rank()

    def _rank(self) -> int:
        return _EVIDENCE_ORDER.index(self.value)


def _coerce_evidence(value: Any) -> EvidenceLevel:
    if isinstance(value, EvidenceLevel):
        return value
    if isinstance(value, str):
        return EvidenceLevel(value)
    return NotImplemented  # type: ignore[return-value]


class ValidationStatus(str, Enum):
    open = "open"
    testing = "testing"
    validated = "validated"
    falsified = "falsified"
    superseded = "superseded"


class AssumptionStatus(str, Enum):
    active = "active"
    killed = "killed"
    merged = "merged"


class ArtifactKind(str, Enum):
    charter = "charter"
    directional_hypothesis = "directional-hypothesis"
    strategy = "strategy"
    opportunity_area = "opportunity-area"
    concept = "concept"
    solution = "solution"
    investment_narrative = "investment-narrative"
    research = "research"
    insights = "insights"


class ArtifactStatus(str, Enum):
    draft = "draft"
    final = "final"
    superseded = "superseded"


class GateExit(str, Enum):
    go = "go"
    conditional_go = "conditional-go"
    recycle = "recycle"
    pivot = "pivot"
    kill = "kill"


# --- Helpers ---

def _coerce_enum(value: Any, enum_cls: type[Enum]):
    if value is None:
        return None
    if isinstance(value, enum_cls):
        return value
    return enum_cls(value)


def _enum_value(value: Any):
    return value.value if isinstance(value, Enum) else value


# --- Assumption ---

@dataclass
class Assumption:
    id: str
    statement: str
    layer: Layer
    category: Category
    impact: Impact
    uncertainty: Uncertainty
    evidence_level: EvidenceLevel
    validation_status: ValidationStatus
    status: AssumptionStatus
    evidence_ref: str
    derived_from: list[str] = field(default_factory=list)
    affects: list[str] = field(default_factory=list)
    branch: str = ""
    updated_at: str | None = None

    def __post_init__(self) -> None:
        self.layer = _coerce_enum(self.layer, Layer)
        self.category = _coerce_enum(self.category, Category)
        self.impact = _coerce_enum(self.impact, Impact)
        self.uncertainty = _coerce_enum(self.uncertainty, Uncertainty)
        self.evidence_level = _coerce_enum(self.evidence_level, EvidenceLevel)
        self.validation_status = _coerce_enum(self.validation_status, ValidationStatus)
        self.status = _coerce_enum(self.status, AssumptionStatus)

    @property
    def is_achilles_heel(self) -> bool:
        # Invariant 1 (is_achilles_heel <==> impact x uncertainty == high x high)
        # holds BY CONSTRUCTION here: the flag is derived, never stored. Do not add
        # a stored is_achilles_heel field — it would duplicate this and re-introduce
        # a checkable invariant. `test_achilles_heel_is_high_high` is the coverage.
        return self.impact == Impact.high and self.uncertainty == Uncertainty.high

    def invariant_violations(self) -> list[str]:
        """Return this assumption's invariant-violation messages (non-raising).

        Single source of truth for the achilles/L4 predicate —
        :meth:`check_invariants`, :func:`ledger_ops.validate_one`, and
        :func:`validate.validate_all` all read from here.

        Invariant 1 (is_achilles_heel <==> high x high) is satisfied by
        construction (see the property) and is therefore not checked here.
        """
        violations: list[str] = []
        if (
            self.is_achilles_heel
            and self.validation_status == ValidationStatus.validated
            and self.evidence_level < EvidenceLevel.L4
        ):
            violations.append(
                f"Assumption {self.id}: achilles heel validated below L4 "
                f"(got {_enum_value(self.evidence_level)})"
            )
        return violations

    def check_invariants(self) -> bool:
        """Validate this assumption's invariants.

        Raises ValidationError on violation. Returns the falsified flag
        (falsified backtrack is enforced in ledger_ops, not here).
        """
        violations = self.invariant_violations()
        if violations:
            raise ValidationError(violations[0])

        return self.validation_status == ValidationStatus.falsified

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "statement": self.statement,
            "layer": _enum_value(self.layer),
            "category": _enum_value(self.category),
            "impact": _enum_value(self.impact),
            "uncertainty": _enum_value(self.uncertainty),
            "evidence_level": _enum_value(self.evidence_level),
            "validation_status": _enum_value(self.validation_status),
            "status": _enum_value(self.status),
            "evidence_ref": self.evidence_ref,
            "derived_from": list(self.derived_from),
            "affects": list(self.affects),
            "branch": self.branch,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Assumption:
        return cls(
            id=d["id"],
            statement=d["statement"],
            layer=_coerce_enum(d["layer"], Layer),
            category=_coerce_enum(d["category"], Category),
            impact=_coerce_enum(d["impact"], Impact),
            uncertainty=_coerce_enum(d["uncertainty"], Uncertainty),
            evidence_level=_coerce_enum(d["evidence_level"], EvidenceLevel),
            validation_status=_coerce_enum(d["validation_status"], ValidationStatus),
            status=_coerce_enum(d["status"], AssumptionStatus),
            evidence_ref=d.get("evidence_ref", ""),
            derived_from=list(d.get("derived_from", [])),
            affects=list(d.get("affects", [])),
            branch=d.get("branch", ""),
            updated_at=d.get("updated_at"),
        )


# --- Ledger ---

@dataclass
class Ledger:
    project: str
    last_baselined_at: str | None = None
    baseline: Any = None
    assumptions: list[Assumption] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "project": self.project,
            "last_baselined_at": self.last_baselined_at,
            "baseline": self.baseline,
            "assumptions": [a.to_dict() for a in self.assumptions],
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Ledger:
        return cls(
            project=d["project"],
            last_baselined_at=d.get("last_baselined_at"),
            baseline=d.get("baseline"),
            assumptions=[Assumption.from_dict(a) for a in d.get("assumptions", [])],
        )


# --- ArtifactMeta ---

@dataclass
class ArtifactMeta:
    artifact_id: str
    kind: ArtifactKind
    stage: str
    status: ArtifactStatus
    hash: str
    locked: bool = False
    validated_by: str | None = None
    validated_at: str | None = None
    signoffs: list[str] = field(default_factory=list)
    dual_sided: dict[str, Any] | None = None
    derived_from: list[str] = field(default_factory=list)
    last_validated_against: list[dict[str, Any]] = field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None

    def __post_init__(self) -> None:
        self.kind = _coerce_enum(self.kind, ArtifactKind)
        self.status = _coerce_enum(self.status, ArtifactStatus)

    @classmethod
    def empty(cls) -> ArtifactMeta:
        return cls(
            artifact_id="",
            kind=ArtifactKind.charter,
            stage="",
            status=ArtifactStatus.draft,
            hash="",
            locked=False,
            validated_by=None,
            validated_at=None,
            signoffs=[],
            dual_sided=None,
            derived_from=[],
            last_validated_against=[],
            created_at=None,
            updated_at=None,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "kind": _enum_value(self.kind),
            "stage": self.stage,
            "status": _enum_value(self.status),
            "hash": self.hash,
            "locked": self.locked,
            "validated_by": self.validated_by,
            "validated_at": self.validated_at,
            "signoffs": list(self.signoffs),
            "dual_sided": self.dual_sided,
            "derived_from": list(self.derived_from),
            "last_validated_against": list(self.last_validated_against),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ArtifactMeta:
        return cls(
            artifact_id=d["artifact_id"],
            kind=_coerce_enum(d["kind"], ArtifactKind),
            stage=d["stage"],
            status=_coerce_enum(d["status"], ArtifactStatus),
            hash=d["hash"],
            locked=d.get("locked", False),
            validated_by=d.get("validated_by"),
            validated_at=d.get("validated_at"),
            signoffs=list(d.get("signoffs", [])),
            dual_sided=d.get("dual_sided"),
            derived_from=list(d.get("derived_from", [])),
            last_validated_against=list(d.get("last_validated_against", [])),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
        )


# --- GateRecord ---

@dataclass
class GateRecord:
    gate: str
    attempt_id: str
    position: int
    subject_refs: list[str] = field(default_factory=list)
    decision_date: str | None = None
    decision_maker: str | None = None
    exit: GateExit | None = None
    conditions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.exit = _coerce_enum(self.exit, GateExit) if self.exit is not None else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate": self.gate,
            "attempt_id": self.attempt_id,
            "position": self.position,
            "subject_refs": list(self.subject_refs),
            "decision_date": self.decision_date,
            "decision_maker": self.decision_maker,
            "exit": _enum_value(self.exit) if self.exit is not None else None,
            "conditions": list(self.conditions),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> GateRecord:
        exit_val = d.get("exit")
        return cls(
            gate=d["gate"],
            attempt_id=d["attempt_id"],
            position=d["position"],
            subject_refs=list(d.get("subject_refs", [])),
            decision_date=d.get("decision_date"),
            decision_maker=d.get("decision_maker"),
            exit=_coerce_enum(exit_val, GateExit) if exit_val is not None else None,
            conditions=list(d.get("conditions", [])),
        )
