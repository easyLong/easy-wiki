# Core Knowledge Architecture

## Purpose

This document describes the stable architectural core of Easy Wiki.

For the broad system story, strengths, weaknesses, and roadmap, see [overall-architecture.md](overall-architecture.md).

This file is narrower. It answers one question:

What are the core abstractions that should remain true even if the implementation is refactored?

## Core Model

Easy Wiki is built around four stable ideas:

```text
evidence
  raw/

knowledge
  wiki/

access
  services/wiki-service/

governance
  docs/ + AGENTS.md
```

Those ideas matter more than the exact file layout.

## Stable Contracts

### 1. Evidence Is Not Knowledge

`raw/` stores qualified original evidence.

It should remain:

- readable
- traceable
- minimally transformed
- separate from synthesis

`wiki/` stores the maintained knowledge graph built from that evidence.

That separation should not be collapsed later.

### 2. Page Ids Are The Interface

External consumers should use page ids, not file paths.

This allows:

- path changes without client breakage
- centralized link and search logic
- safer write-policy enforcement

### 3. The Service Layer Owns Resolution And Policy

`services/wiki-service/` is responsible for:

- page lookup
- list/read/search behavior
- wikilink/backlink resolution
- linting and health reporting
- source compile operations
- source usage reporting
- controlled write operations

External applications should not bypass this layer.

### 4. Durable Knowledge And Project Work Stay Separate

The repository keeps reusable knowledge and project-local execution artifacts apart.

That means:

- reusable knowledge belongs in domains, experts, concepts, workflows, templates, and decisions
- project-local work belongs in `wiki/projects/`
- lessons move back upward only after review

## Current Runtime Shape

The current runtime is intentionally small.

### Storage

- markdown files in `wiki/`
- markdown evidence files in `raw/`

### Service

- Python service core
- HTTP API
- basic MCP stdio runtime

### Human-in-the-loop maintenance

- direct repo maintenance by the maintainer agent
- reviewed promotion from source drafts into durable pages

## What Must Stay Generic

The service layer should remain generic.

It should understand:

- pages
- links
- metadata
- indexing
- compile operations
- write policy

It should not hard-code domain-specific logic such as:

- AI short drama review standards
- expert-specific decision trees
- domain-specific promotion rules

That logic belongs in `wiki/`, not in the runtime.

## What Is Allowed To Change

The following can change without violating the architecture:

- physical page paths
- internal Python module layout
- HTTP handler structure
- MCP transport details
- compile heuristics
- exact project template contents

The following should be treated as architectural commitments:

- evidence and synthesis stay separate
- external consumers rely on service access, not raw file paths
- durable knowledge and project execution remain distinct
- write operations stay policy-aware

## Practical Reading

The current architecture is best understood as a staged system:

```text
raw evidence
  -> compiled source draft
  -> durable knowledge page
  -> project usage
  -> postmortem feedback
```

Today the strongest part of the system is:

```text
raw evidence
  -> compiled source draft
```

The next architectural strengthening should happen here:

```text
compiled source draft
  -> durable knowledge page
```

That is the main gap between "useful tooling" and "reliable knowledge system."
