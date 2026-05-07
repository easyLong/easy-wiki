# Governance Service

`services/governance/` is the execution governance layer for Easy Wiki consumers.

Easy Wiki stores reusable expert thinking, workflows, templates, and source-backed knowledge. The governance layer helps external apps and agents use those assets reliably.

The first implemented slice is intentionally small:

- core artifact, step contract, decision, and trace schemas
- input governance through `resolve_inputs`
- trace governance through `build_trace_record`
- reusable core policy examples under `policies/core/`

It does not execute domain work. It does not decide how to write a short-drama shot list, run research synthesis, or generate code. It decides whether a step has the right inputs before that work begins, and records what evidence the output used afterward.

## Boundary

```text
raw/                    original evidence
wiki/                   knowledge assets
services/wiki-service/  access to wiki/raw
services/governance/    rules for reliable use of wiki/raw/assets
external app/agent      domain execution
```

## Core Objects

- `Artifact`: any source, derived result, wiki page, rule, template, plan, output, or report that can be consumed by a step.
- `StepContract`: the input and trace requirements for one execution step.
- `GovernanceDecision`: the result of resolving inputs for a step.
- `TraceRecord`: a record of which inputs and source spans produced an output.

## Minimal Usage

```python
from governance_core import Artifact, ArtifactRegistry, StepContract, build_trace_record, resolve_inputs

registry = ArtifactRegistry([
    Artifact(
        id="script-source",
        type="source",
        granularity="line",
        provenance={"source_spans": [{"line_start": 1, "line_end": 120}]},
    ),
    Artifact(
        id="script-ir",
        type="ir",
        granularity="line",
        provenance={"derived_from": ["script-source"]},
    ),
])

contract = StepContract(
    step_id="build-shot-plan",
    name="Build Shot Plan",
    goal="Create production shots without losing source detail.",
    output_type="shot-plan",
    primary_input_types=["ir"],
    secondary_input_types=["source", "expert", "workflow"],
    must_read_source=True,
    requires_granularity="line",
    detail_loss_tolerance="low",
    provenance_requirement="source-span",
    selection_policy={"strategy": "source_plus_derived"},
)

decision = resolve_inputs(contract, registry)
if decision.allowed:
    trace = build_trace_record("shot-plan-v1", contract.step_id, decision.selected_inputs)
```

## Policy Strategies

The resolver currently supports:

- `source_only`
- `derived_only`
- `source_plus_derived`
- `derived_with_source_fallback`
- `multi_evidence_merge`
- `human_confirmed_only`

Contracts should choose a strategy declaratively. Domain apps should not hard-code step names inside the governance layer.

## First Consumer Pattern

`easy-wiki-studio` should keep short-drama-specific adapters and contracts in its own project. It can register artifacts such as script source, script IR, scene cards, expert pages, and workflow pages, then ask this governance layer which inputs each production step must use.
