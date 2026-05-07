# Governance Layer

## Purpose

The governance layer defines how external apps and agents should reliably use Easy Wiki knowledge assets.

Easy Wiki stores expert thinking, workflows, templates, and source-backed knowledge. Governance does not replace those assets and does not execute domain work. It checks whether each execution step has the right evidence, wiki knowledge, upstream artifacts, and trace requirements.

In short:

```text
wiki provides knowledge
governance defines reliable use
apps perform domain execution
```

## Current Minimal Layer

The first implemented slice lives under:

```text
services/governance/
```

It includes:

- core artifact schema
- step contract schema
- governance decision schema
- trace record schema
- input resolution
- trace record construction
- core policy examples

This is intentionally smaller than a workflow engine. The workflow still belongs to the app or agent. Governance answers whether a step is allowed to proceed with its selected inputs and what trace evidence the output should keep.

## Relationship To Existing Layers

```text
raw/                    original evidence
wiki/                   knowledge assets
services/wiki-service/  access layer for raw/wiki
services/governance/    governance layer for reliable use
external apps/agents    concrete execution
```

`wiki-service` answers:

- What pages exist?
- What does this page say?
- How do I search, read, lint, or write wiki records?

`governance` answers:

- Does this step need source, derived artifacts, wiki experts, workflows, templates, or all of them?
- Is summary-only input allowed?
- Is the selected input granularity sufficient?
- Does the output need provenance?
- Which source artifacts and spans should the output trace back to?

## Core Objects

### Artifact

An artifact is anything an execution step can consume or produce:

- raw/source evidence
- wiki expert page
- workflow page
- template page
- structured IR
- summary
- plan
- generated output
- QA report

Key fields:

- `id`
- `type`
- `content`
- `domain`
- `schema_ref`
- `granularity`
- `provenance`
- `quality`
- `freshness`
- `tags`
- `relations`

### Step Contract

A step contract defines what one execution step requires before it runs.

Key fields:

- `step_id`
- `goal`
- `output_type`
- `primary_input_types`
- `secondary_input_types`
- `must_read_source`
- `requires_granularity`
- `detail_loss_tolerance`
- `provenance_requirement`
- `selection_policy`
- `validation_rules`

### Governance Decision

A decision reports whether the step can proceed.

It contains:

- `allowed`
- `status`
- `selected_inputs`
- `missing_requirements`
- `warnings`

### Trace Record

A trace record ties an output back to the inputs and source evidence that produced it.

It contains:

- `output_id`
- `step_id`
- `input_artifact_ids`
- `source_artifact_ids`
- `source_spans`
- `derivation_note`
- `created_at`

## Current Strategies

The minimal resolver supports:

- `source_only`
- `derived_only`
- `source_plus_derived`
- `derived_with_source_fallback`
- `multi_evidence_merge`
- `human_confirmed_only`

These strategies are generic. Domain-specific meaning belongs in contracts and adapters, not in the governance core.

## Design Rule

Each execution step must decide its own input contract. A step should not blindly consume the previous step's output.

Some steps may use only derived artifacts. Some must go back to original source evidence. Some need source, derived artifacts, and wiki expert knowledge together.

The governance layer exists to make that choice explicit, testable, and traceable.

## First Consumer

`C:\Code\easy-wiki-studio` should become the first consumer.

The studio should keep short-drama-specific contracts and adapters in its own project, then call `services/governance/` to resolve inputs for steps such as:

- script IR building
- shot planning
- prompt compiling
- coverage checking

The governance core should not learn short-drama concepts directly.
