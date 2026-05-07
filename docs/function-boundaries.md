# Function Boundaries

## Summary

Easy Wiki has five main responsibilities:

1. preserve qualified original evidence in `raw/`
2. maintain durable knowledge in `wiki/`
3. expose controlled access through `services/wiki-service/`
4. govern execution input and trace contracts through `services/governance/`
5. guide maintenance through `docs/` and `AGENTS.md`

It is not a general product shell, not a media pipeline, and not a full CMS.

## Boundary Map

### `raw/`

Owns:

- qualified complete readable original source files
- long-term evidence storage

Does not own:

- notes
- metadata cards
- capture logs
- failed capture artifacts
- compiled summaries
- durable synthesis

Boundary rule:

`raw/` stores evidence only.

### `wiki/`

Owns:

- source-page drafts
- durable concepts
- expert role pages
- domain knowledge
- project artifacts
- decisions
- postmortems
- index and log

Does not own:

- runtime APIs
- transport concerns
- application code
- binary media serving

Boundary rule:

`wiki/` is the markdown database, not the service runtime.

### `wiki/domains/`

Owns:

- reusable domain structure
- domain frameworks
- domain source maps
- domain workflows
- domain open questions
- domain-level project tracking

Does not own:

- one-off project execution notes
- service-layer logic

Boundary rule:

Domain pages should remain reusable beyond a single project.

### `wiki/projects/`

Owns:

- briefs
- plans
- decisions
- working notes
- reviews
- postmortems

Does not own:

- general truth for the whole wiki
- reusable domain frameworks unless promoted back out

Boundary rule:

Project knowledge is local until deliberately promoted.

### `wiki/experts/`

Owns:

- reusable role lenses
- review perspectives
- expert-style evaluation questions

Does not own:

- biographies
- project-local logs
- transport or service code

Boundary rule:

Expert pages are role abstractions, not case-specific documents.

### `services/wiki-service/`

Owns:

- page listing and reading
- search
- wikilink and backlink resolution
- lint and health reporting
- source usage reporting
- source compile operations
- batch scan operations
- project creation operations
- controlled log append operations
- HTTP API transport
- MCP stdio transport

Does not own:

- domain-specific knowledge
- source truth itself
- unrestricted wiki edits
- automatic durable synthesis decisions

Boundary rule:

The service layer stays generic and policy-aware.

### `services/governance/`

Owns:

- execution artifact schema
- step contract schema
- input resolution policy
- trace record construction
- reusable governance policy examples

Does not own:

- page storage or path resolution
- HTTP or MCP access to wiki pages
- domain-specific execution logic
- short-drama, research, or coding business rules
- the final generated artifacts themselves

Boundary rule:

The governance layer defines how apps should use evidence and wiki knowledge reliably; apps still perform the domain work.

## Current Capability Boundary

### Strong Enough Today

- repository structure and scope
- evidence vs synthesis split
- query and page inspection
- link resolution
- health and usage diagnostics
- source draft compilation
- basic batch compile detection
- project scaffolding
- basic HTTP and MCP access
- minimal governance layer for input resolution and trace records

### Intentionally Limited Today

- write surface area
- durable knowledge promotion
- conflict resolution between sources
- automation depth
- compile intelligence

### Not Yet Mature

- test coverage
- modularity inside the service core
- lifecycle tracking for source drafts
- watch-mode or queue-based ingest
- stronger transport-contract validation
- richer governance modules such as output, coverage, write, and version governance

## Current Non-Goals

Easy Wiki is not currently responsible for:

- hosting a public frontend
- storing large media assets
- running model inference
- managing users or auth
- being a production CMS
- replacing an editor like Obsidian
- being a vector database service
- solving multi-user merge coordination at the service level

Those can exist around the wiki later, but they should not distort the current core.

## Boundary Risks

### Risk 1: The Wiki Becomes A Dumping Ground

Symptoms:

- lots of raw files
- many source pages
- little durable synthesis

Mitigation:

- keep `source_usage` and `healthcheck` in the loop
- require promotion from source pages into reusable pages
- review project postmortems for reusable lessons

### Risk 2: External Consumers Couple To Paths

Symptoms:

- apps depend on `wiki/.../...md`
- refactors become dangerous

Mitigation:

- use page ids
- route reads and writes through the service layer

### Risk 3: Service Layer Starts Encoding Domain Logic

Symptoms:

- AI short drama rules appear in transport or storage code
- service behavior changes per domain

Mitigation:

- keep domain knowledge in markdown pages
- let workflows read wiki pages instead of hard-coding domain logic

### Risk 4: Compile Drafts Accumulate Without Review

Symptoms:

- many `compiled-draft` pages
- weak traceability into domain/expert/concept pages

Mitigation:

- add source lifecycle states
- add promotion tracking
- create a review queue for source drafts

### Risk 5: The Service Core Becomes Too Monolithic

Symptoms:

- one file change affects parsing, health, compile, and write behavior
- harder testing

Mitigation:

- split `wiki_core.py` by responsibility
- add fixture-driven tests before deeper refactors

## Recommended Boundary Improvements

1. Refactor the service core into smaller modules.
2. Add tests for parse, search, health, compile, HTTP, and MCP behaviors.
3. Introduce a source-draft lifecycle and promotion tracking.
4. Keep write operations narrow until tests and lifecycle semantics are stronger.
5. Add optional watch-mode ingest only after the core loop is stable.

## Bottom Line

The current boundaries are directionally good.

The main job now is not to expand the system sideways. It is to make the existing boundaries easier to enforce, easier to test, and harder to blur by accident.
