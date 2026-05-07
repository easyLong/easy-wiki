from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


SOURCE_TYPES = {"source", "raw-source", "original", "evidence"}
SUMMARY_TYPES = {"summary", "digest", "abstract"}

DEFAULT_GRANULARITY_RANK = {
    "collection": 0,
    "document": 1,
    "section": 2,
    "paragraph": 3,
    "line": 4,
    "span": 5,
    "unit": 5,
    "entity": 6,
}


@dataclass
class Artifact:
    id: str
    type: str
    content: Any = None
    domain: str = ""
    schema_ref: str = ""
    granularity: str = "document"
    provenance: dict[str, Any] = field(default_factory=dict)
    quality: dict[str, Any] = field(default_factory=dict)
    freshness: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    relations: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class StepContract:
    step_id: str
    name: str
    goal: str
    output_type: str
    primary_input_types: list[str] = field(default_factory=list)
    secondary_input_types: list[str] = field(default_factory=list)
    must_read_source: bool = False
    requires_granularity: str = "document"
    detail_loss_tolerance: str = "medium"
    provenance_requirement: str = "input-artifacts"
    selection_policy: dict[str, Any] = field(default_factory=lambda: {"strategy": "source_plus_derived"})
    validation_rules: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> StepContract:
        return cls(
            step_id=str(payload["step_id"]),
            name=str(payload.get("name", payload["step_id"])),
            goal=str(payload.get("goal", "")),
            output_type=str(payload.get("output_type", "")),
            primary_input_types=[str(item) for item in payload.get("primary_input_types", [])],
            secondary_input_types=[str(item) for item in payload.get("secondary_input_types", [])],
            must_read_source=bool(payload.get("must_read_source", False)),
            requires_granularity=str(payload.get("requires_granularity", "document")),
            detail_loss_tolerance=str(payload.get("detail_loss_tolerance", "medium")),
            provenance_requirement=str(payload.get("provenance_requirement", "input-artifacts")),
            selection_policy=dict(payload.get("selection_policy", {"strategy": "source_plus_derived"})),
            validation_rules=list(payload.get("validation_rules", [])),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class GovernanceDecision:
    allowed: bool
    status: str
    step_id: str
    selected_inputs: list[Artifact] = field(default_factory=list)
    missing_requirements: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["selected_inputs"] = [artifact.to_dict() for artifact in self.selected_inputs]
        return payload


@dataclass
class TraceRecord:
    output_id: str
    step_id: str
    input_artifact_ids: list[str]
    source_artifact_ids: list[str]
    source_spans: list[dict[str, Any]] = field(default_factory=list)
    derivation_note: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ArtifactRegistry:
    def __init__(self, artifacts: list[Artifact] | None = None) -> None:
        self._artifacts: dict[str, Artifact] = {}
        for artifact in artifacts or []:
            self.add(artifact)

    def add(self, artifact: Artifact) -> None:
        if not artifact.id:
            raise ValueError("artifact id is required")
        self._artifacts[artifact.id] = artifact

    def get(self, artifact_id: str) -> Artifact | None:
        return self._artifacts.get(artifact_id)

    def list(self) -> list[Artifact]:
        return list(self._artifacts.values())

    def by_type(self, artifact_types: list[str]) -> list[Artifact]:
        wanted = set(artifact_types)
        return [artifact for artifact in self.list() if artifact.type in wanted]


def resolve_inputs(
    contract: StepContract,
    registry: ArtifactRegistry,
    granularity_rank: dict[str, int] | None = None,
) -> GovernanceDecision:
    rank = granularity_rank or DEFAULT_GRANULARITY_RANK
    strategy = str(contract.selection_policy.get("strategy", "source_plus_derived"))
    selected = _select_by_strategy(contract, registry, strategy)

    missing = _validate_selection(contract, selected, rank)
    warnings = _build_warnings(contract, selected, rank)
    allowed = not missing
    status = "allowed" if allowed else "blocked"
    return GovernanceDecision(
        allowed=allowed,
        status=status,
        step_id=contract.step_id,
        selected_inputs=selected,
        missing_requirements=missing,
        warnings=warnings,
    )


def build_trace_record(
    output_id: str,
    step_id: str,
    selected_inputs: list[Artifact],
    derivation_note: str = "",
) -> TraceRecord:
    source_artifacts = [artifact for artifact in selected_inputs if _is_source_artifact(artifact)]
    source_spans: list[dict[str, Any]] = []
    for artifact in source_artifacts:
        spans = artifact.provenance.get("source_spans", [])
        if isinstance(spans, list):
            source_spans.extend(dict(span, artifact_id=artifact.id) for span in spans if isinstance(span, dict))

    return TraceRecord(
        output_id=output_id,
        step_id=step_id,
        input_artifact_ids=[artifact.id for artifact in selected_inputs],
        source_artifact_ids=[artifact.id for artifact in source_artifacts],
        source_spans=source_spans,
        derivation_note=derivation_note,
    )


def _select_by_strategy(
    contract: StepContract,
    registry: ArtifactRegistry,
    strategy: str,
) -> list[Artifact]:
    primary = registry.by_type(contract.primary_input_types)
    secondary = registry.by_type(contract.secondary_input_types)
    sources = [artifact for artifact in registry.list() if _is_source_artifact(artifact)]

    if strategy == "source_only":
        return _dedupe_artifacts(sources)
    if strategy == "derived_only":
        return _dedupe_artifacts(primary + secondary)
    if strategy == "derived_with_source_fallback":
        selected = primary + secondary
        if contract.must_read_source or not selected:
            selected += sources
        return _dedupe_artifacts(selected)
    if strategy == "multi_evidence_merge":
        return _dedupe_artifacts(primary + secondary + sources)
    if strategy == "human_confirmed_only":
        selected = primary + secondary + sources
        return _dedupe_artifacts(
            [artifact for artifact in selected if artifact.quality.get("human_confirmed") is True]
        )
    return _dedupe_artifacts(primary + secondary + sources)


def _validate_selection(
    contract: StepContract,
    selected: list[Artifact],
    granularity_rank: dict[str, int],
) -> list[str]:
    missing: list[str] = []
    selected_types = {artifact.type for artifact in selected}

    if contract.primary_input_types and not selected_types.intersection(contract.primary_input_types):
        missing.append(f"missing primary input types: {', '.join(contract.primary_input_types)}")

    if contract.must_read_source and not any(_is_source_artifact(artifact) for artifact in selected):
        missing.append("source input is required")

    if contract.detail_loss_tolerance == "low" and selected and all(
        artifact.type in SUMMARY_TYPES for artifact in selected
    ):
        missing.append("low detail-loss steps cannot use summary-only inputs")

    if contract.requires_granularity:
        if not any(_granularity_satisfies(artifact.granularity, contract.requires_granularity, granularity_rank) for artifact in selected):
            missing.append(f"requires granularity at least: {contract.requires_granularity}")

    if contract.provenance_requirement != "none" and not any(
        artifact.provenance for artifact in selected
    ):
        missing.append("provenance is required")

    return missing


def _build_warnings(
    contract: StepContract,
    selected: list[Artifact],
    granularity_rank: dict[str, int],
) -> list[str]:
    warnings: list[str] = []
    if not selected:
        warnings.append("no inputs selected")
        return warnings

    if contract.secondary_input_types:
        selected_types = {artifact.type for artifact in selected}
        missing_secondary = [
            artifact_type
            for artifact_type in contract.secondary_input_types
            if artifact_type not in selected_types
        ]
        if missing_secondary:
            warnings.append(f"missing optional secondary inputs: {', '.join(missing_secondary)}")

    coarse_primary_inputs = [
        artifact.id
        for artifact in selected
        if artifact.type in set(contract.primary_input_types)
        if not _granularity_satisfies(artifact.granularity, contract.requires_granularity, granularity_rank)
    ]
    if coarse_primary_inputs:
        warnings.append(f"coarser-than-required primary inputs selected: {', '.join(coarse_primary_inputs)}")

    return warnings


def _granularity_satisfies(
    actual: str,
    required: str,
    granularity_rank: dict[str, int],
) -> bool:
    if not required:
        return True
    if actual == required:
        return True
    return granularity_rank.get(actual, -1) >= granularity_rank.get(required, 999)


def _is_source_artifact(artifact: Artifact) -> bool:
    return artifact.type in SOURCE_TYPES or "source" in artifact.tags


def _dedupe_artifacts(artifacts: list[Artifact]) -> list[Artifact]:
    seen: set[str] = set()
    result: list[Artifact] = []
    for artifact in artifacts:
        if artifact.id in seen:
            continue
        seen.add(artifact.id)
        result.append(artifact)
    return result
