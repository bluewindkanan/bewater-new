"""Canonical runtime contracts for the BeWater lifecycle.

The runtime deliberately models the current methodology only.  Artifact
frontmatter has separate document and validation states; assumption state is
not reused for either of them.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from bw.errors import ValidationError


class Layer(str, Enum):
    root = "root"
    strategy = "strategy"
    opportunity = "opportunity"
    concept = "concept"
    solution = "solution"
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

    def _rank(self) -> int:
        return _EVIDENCE_ORDER.index(self.value)

    def __lt__(self, other: Any) -> bool:
        return self._rank() < _coerce_evidence(other)._rank()

    def __le__(self, other: Any) -> bool:
        return self._rank() <= _coerce_evidence(other)._rank()

    def __gt__(self, other: Any) -> bool:
        return self._rank() > _coerce_evidence(other)._rank()

    def __ge__(self, other: Any) -> bool:
        return self._rank() >= _coerce_evidence(other)._rank()


class AssumptionValidationStatus(str, Enum):
    untested = "untested"
    testing = "testing"
    supported = "supported"
    falsified = "falsified"
    inconclusive = "inconclusive"


class AssumptionStatus(str, Enum):
    active = "active"
    killed = "killed"
    merged = "merged"


class ArtifactKind(str, Enum):
    charter = "charter"
    directional_hypothesis = "directional-hypothesis"
    strategy = "strategy"
    opportunity = "opportunity"
    idea_pool = "idea-pool"
    concept_portfolio = "concept-portfolio"
    solution = "solution"
    investment_narrative = "investment-narrative"
    research = "research"
    insights = "insights"
    initial_assessment = "initial-assessment"


class ArtifactDocumentStatus(str, Enum):
    draft = "draft"
    final = "final"
    superseded = "superseded"


class ArtifactValidationStatus(str, Enum):
    unvalidated = "unvalidated"
    in_review = "in-review"
    validated = "validated"
    invalidated = "invalidated"


class GateExit(str, Enum):
    go = "go"
    conditional_go = "conditional-go"
    recycle = "recycle"
    pivot = "pivot"
    kill = "kill"


@dataclass(frozen=True)
class Issue:
    scope: str
    kind: str
    message: str


def _coerce_enum(value: Any, enum_cls: type[Enum]):
    if isinstance(value, enum_cls):
        return value
    return enum_cls(value)


def _enum_value(value: Any) -> Any:
    return value.value if isinstance(value, Enum) else value


def _coerce_evidence(value: Any) -> EvidenceLevel:
    return _coerce_enum(value, EvidenceLevel)


@dataclass
class Assumption:
    id: str
    statement: str
    layer: Layer
    category: Category
    impact: Impact
    uncertainty: Uncertainty
    evidence_level: EvidenceLevel
    validation_status: AssumptionValidationStatus
    status: AssumptionStatus
    evidence_refs: list[str] = field(default_factory=list)
    derived_from: list[str] = field(default_factory=list)
    affects: list[str] = field(default_factory=list)
    branch_id: str = ""
    record_revision: int = 1
    source_concept_id: str | None = None
    side: str | None = None
    supersedes_ref: str | None = None
    risk_history: list[dict[str, Any]] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)
    l4_obligation_status: str = "open"
    updated_at: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.layer = _coerce_enum(self.layer, Layer)
        self.category = _coerce_enum(self.category, Category)
        self.impact = _coerce_enum(self.impact, Impact)
        self.uncertainty = _coerce_enum(self.uncertainty, Uncertainty)
        self.evidence_level = _coerce_enum(self.evidence_level, EvidenceLevel)
        self.validation_status = _coerce_enum(self.validation_status, AssumptionValidationStatus)
        self.status = _coerce_enum(self.status, AssumptionStatus)

    @property
    def is_achilles_heel(self) -> bool:
        return self.impact == Impact.high and self.uncertainty == Uncertainty.high

    @property
    def has_durable_l4_obligation(self) -> bool:
        if self.is_achilles_heel:
            return True
        return any(
            entry.get("impact") == Impact.high.value
            and entry.get("uncertainty") == Uncertainty.high.value
            for entry in [*self.risk_history, *self.history]
            if isinstance(entry, dict)
        )

    @property
    def l4_obligation_open(self) -> bool:
        return (
            self.has_durable_l4_obligation
            and self.status == AssumptionStatus.active
            and self.l4_obligation_status == "open"
        )

    def invariant_violations(self) -> list[str]:
        if self.has_durable_l4_obligation and self.validation_status == AssumptionValidationStatus.supported and self.evidence_level < EvidenceLevel.L4:
            return [f"Assumption {self.id}: achilles heel supported below L4 (got {self.evidence_level.value})"]
        return []

    def check_invariants(self) -> bool:
        violations = self.invariant_violations()
        if violations:
            raise ValidationError(violations[0])
        return self.validation_status == AssumptionValidationStatus.falsified

    def to_dict(self) -> dict[str, Any]:
        data = dict(self.extra)
        data.update({
            "id": self.id, "statement": self.statement, "layer": _enum_value(self.layer),
            "category": _enum_value(self.category), "impact": _enum_value(self.impact),
            "uncertainty": _enum_value(self.uncertainty), "evidence_level": _enum_value(self.evidence_level),
            "validation_status": _enum_value(self.validation_status), "status": _enum_value(self.status),
            "evidence_refs": list(self.evidence_refs), "derived_from": list(self.derived_from),
            "affects": list(self.affects), "branch_id": self.branch_id,
            "record_revision": self.record_revision, "source_concept_id": self.source_concept_id,
            "side": self.side,
            "supersedes_ref": self.supersedes_ref, "risk_history": list(self.risk_history),
            "history": list(self.history), "l4_obligation_status": self.l4_obligation_status,
            "updated_at": self.updated_at,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any], *, id_override: str | None = None) -> Assumption:
        known = {
            "id", "statement", "layer", "category", "impact", "uncertainty",
            "evidence_level", "validation_status", "status", "evidence_refs",
            "derived_from", "affects", "branch_id", "record_revision",
            "source_concept_id", "side", "supersedes_ref",
            "risk_history", "history", "l4_obligation_status", "updated_at",
        }
        return cls(
            id=id_override or data["id"], statement=data["statement"], layer=data["layer"],
            category=data["category"], impact=data["impact"], uncertainty=data["uncertainty"],
            evidence_level=data["evidence_level"], validation_status=data["validation_status"],
            status=data["status"], evidence_refs=list(data.get("evidence_refs", [])),
            derived_from=list(data.get("derived_from", [])), affects=list(data.get("affects", [])),
            branch_id=data.get("branch_id", ""), record_revision=data.get("record_revision", 1),
            source_concept_id=data.get("source_concept_id"), side=data.get("side"),
            supersedes_ref=data.get("supersedes_ref"),
            risk_history=list(data.get("risk_history", [])), history=list(data.get("history", [])),
            l4_obligation_status=data.get("l4_obligation_status", "open"), updated_at=data.get("updated_at"),
            extra={key: value for key, value in data.items() if key not in known},
        )


@dataclass
class Ledger:
    schema_version: int = 1
    revision: int = 1
    next_id: int = 1
    updated_at: str | None = None
    updated_by: str = "bw-init"
    assumptions: dict[str, Assumption] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version, "revision": self.revision, "next_id": self.next_id,
                "updated_at": self.updated_at, "updated_by": self.updated_by,
                "assumptions": {key: assumption.to_dict() for key, assumption in self.assumptions.items()}}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Ledger:
        raw = data.get("assumptions", {})
        if not isinstance(raw, dict):
            raise TypeError("ledger assumptions must be an ID-keyed mapping")
        assumptions: dict[str, Assumption] = {}
        for key, value in raw.items():
            if not isinstance(key, str) or not isinstance(value, dict):
                raise TypeError("ledger assumptions must contain string IDs mapped to records")
            if "id" in value and value["id"] != key:
                raise ValueError(f"ledger assumption key {key!r} conflicts with record id {value['id']!r}")
            assumptions[key] = Assumption.from_dict(value, id_override=key)
        return cls(schema_version=data.get("schema_version", 1), revision=data.get("revision", 1),
                   next_id=data.get("next_id", 1), updated_at=data.get("updated_at"),
                   updated_by=data.get("updated_by", "bw-init"), assumptions=assumptions)


@dataclass
class ArtifactMeta:
    artifact_id: str
    kind: ArtifactKind
    stage: str
    revision: int
    document_status: ArtifactDocumentStatus
    validation_status: ArtifactValidationStatus
    branch_id: str = ""
    locked: bool = False
    signoffs: list[dict[str, Any]] = field(default_factory=list)
    dual_sided: dict[str, Any] | None = None
    derived_from: list[str] = field(default_factory=list)
    last_validated_against: list[dict[str, Any]] = field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.kind = _coerce_enum(self.kind, ArtifactKind)
        self.document_status = _coerce_enum(self.document_status, ArtifactDocumentStatus)
        self.validation_status = _coerce_enum(self.validation_status, ArtifactValidationStatus)

    @property
    def hash(self) -> str:
        return str(self.extra.get("hash", ""))

    @hash.setter
    def hash(self, value: str) -> None:
        self.extra["hash"] = value

    @classmethod
    def empty(cls) -> ArtifactMeta:
        return cls("", ArtifactKind.charter, "", 1, ArtifactDocumentStatus.draft,
                   ArtifactValidationStatus.unvalidated)

    def to_dict(self) -> dict[str, Any]:
        data = dict(self.extra)
        data.update({
            "artifact_id": self.artifact_id, "kind": _enum_value(self.kind), "stage": self.stage,
            "revision": self.revision, "document_status": _enum_value(self.document_status),
            "validation_status": _enum_value(self.validation_status), "branch_id": self.branch_id,
            "locked": self.locked, "signoffs": list(self.signoffs), "dual_sided": self.dual_sided,
            "derived_from": list(self.derived_from), "last_validated_against": list(self.last_validated_against),
            "created_at": self.created_at, "updated_at": self.updated_at,
        })
        return {key: value for key, value in data.items() if value is not None}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ArtifactMeta:
        required = {"artifact_id", "kind", "stage", "revision", "document_status", "validation_status"}
        missing = sorted(key for key in required if key not in data)
        if missing:
            raise ValueError(f"artifact frontmatter missing required canonical field(s): {', '.join(missing)}")
        known = required | {"branch_id", "locked", "signoffs", "dual_sided", "derived_from",
                            "last_validated_against", "created_at", "updated_at"}
        return cls(
            artifact_id=data["artifact_id"], kind=data["kind"], stage=data["stage"], revision=data["revision"],
            document_status=data["document_status"], validation_status=data["validation_status"],
            branch_id=data.get("branch_id", ""), locked=data.get("locked", False),
            signoffs=list(data.get("signoffs", [])), dual_sided=data.get("dual_sided"),
            derived_from=list(data.get("derived_from", [])),
            last_validated_against=list(data.get("last_validated_against", [])),
            created_at=data.get("created_at"), updated_at=data.get("updated_at"),
            extra={key: value for key, value in data.items() if key not in known},
        )


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
        if self.exit is not None:
            self.exit = _coerce_enum(self.exit, GateExit)

    def to_dict(self) -> dict[str, Any]:
        return {"gate": self.gate, "attempt_id": self.attempt_id, "position": self.position,
                "subject_refs": list(self.subject_refs), "decision_date": self.decision_date,
                "decision_maker": self.decision_maker, "exit": _enum_value(self.exit),
                "conditions": list(self.conditions)}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GateRecord:
        return cls(gate=data["gate"], attempt_id=data["attempt_id"], position=data["position"],
                   subject_refs=list(data.get("subject_refs", [])), decision_date=data.get("decision_date"),
                   decision_maker=data.get("decision_maker"), exit=data.get("exit"),
                   conditions=list(data.get("conditions", [])))
