# Easy Wiki Overall Architecture

## 1. Positioning

Easy Wiki is a long-lived knowledge base maintained with LLM help.

Its job is not to collect links or dump notes. Its job is to turn qualified original evidence into durable, queryable, reusable knowledge that can support future agents, applications, and concrete projects.

The repository has already been narrowed back to the core path:

```text
raw/                    qualified original evidence
wiki/                   markdown knowledge database
services/wiki-service/  access layer
services/governance/    execution governance layer
docs/                   architecture and policy documents
AGENTS.md               maintenance rules for future agents
```

Non-core app experiments and non-core domain expansion have been moved out of the main repository:

```text
C:\Code\easy-wiki-apps
C:\Code\easy-wiki-domain-expansion
```

That narrowing was the right move. It gives the project a real center again.

## 2. Current Architecture Shape

The current architecture is a five-layer system:

```text
qualified evidence
    raw/

compiled knowledge
    wiki/

service access layer
    services/wiki-service/

execution governance layer
    services/governance/

maintenance policy
    AGENTS.md + docs/
```

The most important data flow is:

```text
requirement intake
  -> source discovery
  -> evidence qualification
  -> raw archive
  -> source compile draft
  -> durable wiki synthesis
  -> project execution
  -> postmortem feedback
```

The shorter architecture view is:

```text
raw evidence
  -> wiki/sources draft
  -> durable domain/expert/concept/workflow knowledge
  -> project artifacts
  -> lessons fed back into durable knowledge
```

## 3. Layer Responsibilities

### `raw/`

`raw/` is the evidence layer.

It stores qualified, readable, complete originals only.

It is intentionally narrow:

- not a download cache
- not a note folder
- not a capture-debug area
- not a place for summaries or metadata cards

The core rule is simple: `raw/` keeps evidence; interpretation happens later.

### `wiki/`

`wiki/` is the long-term markdown database.

Its main page families are:

```text
wiki/sources/       source-page drafts and source metadata
wiki/concepts/      reusable ideas and frameworks
wiki/experts/       reusable role lenses
wiki/domains/       durable domain knowledge
wiki/projects/      concrete execution artifacts
wiki/workflows/     repeatable operating procedures
wiki/decisions/     durable decisions
wiki/postmortems/   lessons learned
wiki/index.md       entry index
wiki/log.md         repository evolution log
```

`wiki/` is the knowledge database, not just a pile of markdown files.

### `services/wiki-service/`

`services/wiki-service/` is the access layer.

It exists so that external agents and applications do not depend on physical file paths.

Current implemented capabilities:

- list pages
- read pages by page id
- search pages
- parse wikilinks and backlinks
- run lint checks
- run stronger health checks
- track raw/source coverage and source usage
- compile one raw source into a source-page draft
- batch-scan `raw/` for missing source pages
- create project scaffolding
- append log entries
- expose the same core through HTTP and basic MCP stdio runtime

### `services/governance/`

`services/governance/` is the execution governance layer.

It exists so that external apps and agents do not treat expert pages, workflow pages, prior summaries, structured IR, and original evidence as interchangeable inputs.

Current minimal capabilities:

- represent inputs and outputs as artifacts
- define step input requirements as contracts
- resolve inputs by policy
- block summary-only input for low detail-loss steps
- require source evidence when a step contract says source is mandatory
- create trace records tying outputs back to inputs and source spans

It is not a workflow engine and it does not contain domain-specific business logic. Domain apps keep their own adapters and contracts, then call governance before and after execution steps.

### `docs/` and `AGENTS.md`

These define the operating contract.

They explain:

- what belongs in each layer
- what external consumers may rely on
- how ingest, compile, and project workflows should work
- which write paths are allowed

## 4. Access Model

There are two modes of use:

```text
maintenance mode:
    repo-maintaining agent edits files directly

consumer mode:
    external agent/app uses HTTP or MCP
```

Target shape:

```text
maintainer agent
        |
        | direct repo maintenance
        v
raw/ + wiki/ + docs/

external agent / app / automation
        |
        | HTTP API or MCP + governance contracts
        v
services/wiki-service/
        |
        v
wiki/ and raw/

external app / agent execution step
        |
        | input contract + artifact registry
        v
services/governance/
        |
        v
governance decision + trace record
```

This separation is one of the strongest parts of the project.

## 5. What Is Implemented Today

The current system is no longer just aspirational. A real minimal loop exists.

### Implemented and working

- repository scope narrowed back to the core wiki path
- source/durable knowledge separation
- page listing, reading, search, link parsing
- wiki lint and health reporting
- source usage tracking
- single-source compile draft
- batch compile detection for raw files missing source pages
- project scaffolding
- HTTP API runtime
- basic MCP stdio runtime
- minimal governance layer for input resolution and trace records

### Implemented but still lightweight

- search quality
- compile heuristics
- source-to-durable promotion flow
- write policy enforcement depth
- validation and test coverage

### Still mostly human workflow

- deciding whether a source is truly worth archiving
- promoting compiled source drafts into durable concept/domain/expert pages
- resolving conflicts between sources
- deciding what becomes reusable knowledge vs project-local notes

That last group is intentional. It keeps the system from becoming auto-generated sludge.

## 6. Architecture Route

The architecture route is now clearer than before. It has roughly five phases.

### Phase 1: Scope Narrowing

Already done.

Goal:

- stop the repo from trying to be too many things at once
- preserve only the core wiki loop

Result:

- lower cognitive load
- cleaner repository boundary
- fewer fake priorities

### Phase 2: Access Layer Baseline

Mostly done.

Goal:

- make the markdown database queryable through a stable interface

Result:

- HTTP API exists
- MCP stdio runtime exists
- core logic is centralized in `wiki_core.py`

### Phase 3: Compile Loop Hardening

In progress now.

Goal:

- make `raw -> wiki/sources` reliable enough for repeated use

Current improvements already in place:

- batch scan for missing source pages
- better dry-run semantics
- top-of-file metadata parsing for raw article bodies

Still needed:

- stronger compile quality
- better link suggestions
- source status lifecycle beyond `compiled-draft`

### Phase 4: Durable Knowledge Promotion

Next major architecture step.

Goal:

- turn source-page drafts into a reliable bridge toward durable knowledge

Needed additions:

- explicit review states
- promotion workflow from source pages into concepts/domains/experts/workflows
- better traceability for which durable pages were updated from which source drafts

### Phase 5: External Consumer Readiness

Later, after the core loop is stable.

Goal:

- let other tools and apps depend on Easy Wiki without coupling to file layout

Needed additions:

- tests
- clearer error contracts
- stronger write guards
- stable release discipline for the service layer

## 7. Current Strengths

The architecture already has several genuinely good qualities.

### 1. Clear evidence vs knowledge separation

This is the single best design choice in the repo.

`raw/` is evidence.
`wiki/` is synthesis.

That makes future reasoning, auditing, and backtracking much easier.

### 2. Good repository boundary after narrowing

Moving unrelated apps and non-core expansion out of the repo was healthy.

The project is easier to understand, easier to maintain, and more likely to finish useful things.

### 3. Access layer abstraction is correct

Using page ids and a service layer instead of hard-coded paths is the right long-term call.

It protects the wiki from future reorganization.

### 4. Quality-oriented maintenance checks already exist

`healthcheck` and `source_usage` are more important than they look.

They prevent the wiki from quietly becoming a dead archive full of disconnected pages.

### 5. Human review is still preserved

The system does not over-automate the most fragile step: deciding what deserves to become durable knowledge.

That restraint is a strength, not a weakness.

## 8. Current Weaknesses

The architecture is useful now, but still uneven.

### 1. Too much core logic is concentrated in `wiki_core.py`

Right now parsing, indexing, compile logic, health checks, project creation, and formatting live in one large module.

This is fine for early momentum, but it will slow the next stage.

### 2. Service contracts are only lightly enforced

The HTTP and MCP surfaces exist, but they are still thin wrappers around internal functions.

There is not yet a strong separation between:

- transport layer
- service layer
- storage logic
- compile pipeline

### 3. Compile quality is still heuristic-heavy

The current compile pass is useful for drafts, but not robust enough to be treated as a trusted knowledge transform.

Weak spots include:

- keyword quality
- claim extraction quality
- suggested link quality
- source encoding cleanup

### 4. Durable knowledge promotion is under-modeled

The architecture is strong at `raw -> source draft`, but weaker at `source draft -> reusable knowledge`.

That middle layer needs clearer workflow and state.

### 5. Automated verification is too light

There are runtime spot checks, but not enough repeatable tests.

That is manageable today, but risky once more consumers depend on the service layer.

### 6. No evented or watch-based ingest path

The system can batch-scan `raw/`, which is practical, but it does not yet support a more automatic watch mode.

That is not urgent, but it is a real usability gap.

## 9. Best Improvements To Make Next

If we prioritize well, the next improvements should strengthen the core loop instead of adding surface area.

### Priority A: Refactor the service core

Split `wiki_core.py` by responsibility, for example:

```text
wiki_core/
  parsing.py
  catalog.py
  health.py
  compile.py
  projects.py
  logging.py
```

Why it matters:

- easier testing
- clearer ownership
- lower change risk

### Priority B: Define a source draft lifecycle

Recommended states:

```text
captured
compiled-draft
reviewed
promoted
archived
```

Why it matters:

- easier queue management
- less ambiguity about what still needs human review
- better progress visibility

### Priority C: Add automated tests

Focus first on:

- page parsing
- wikilink and backlink resolution
- source usage
- healthcheck behavior
- compile output for representative raw fixtures
- HTTP and MCP smoke tests

Why it matters:

- protects the service layer as the contract hardens

### Priority D: Strengthen compile traceability

Add explicit fields or sections for:

- parsed source metadata
- compile timestamp
- compile version
- promotion targets
- review notes

Why it matters:

- easier audits
- safer iterative recompile behavior later

### Priority E: Add optional watch mode

Possible shape:

```text
raw watcher
  -> detect new file
  -> validate eligibility
  -> run compile draft
  -> append log
```

Why it matters:

- better ingest ergonomics
- less manual scanning friction

But this should come after test coverage and lifecycle modeling, not before.

## 10. Recommended Near-Term Roadmap

Here is the most sensible near-term sequence.

1. Stabilize documentation and make the current architecture truthful.
2. Refactor `wiki_core.py` into smaller modules without changing behavior.
3. Add automated tests around the current HTTP, MCP, lint, healthcheck, and compile loop.
4. Introduce source draft lifecycle fields and promotion tracking.
5. Improve compile quality using better structure extraction and cleaner heuristics.
6. Add optional watch-mode or job-style ingest automation.
7. Only after that, expand external consumers or new product surfaces.

That order keeps us on the main line.

## 11. Bottom Line

The current architecture is good in direction and still early in finish quality.

Its strongest choices are:

- separating evidence from knowledge
- separating storage from access
- separating durable knowledge from projects
- narrowing the repo back to the core

Its biggest risks are:

- too much logic in one service file
- too little test coverage
- a weakly modeled promotion step from source draft to durable knowledge

So the right strategy is not to add more breadth.
It is to harden the core loop:

```text
raw
  -> source draft
  -> durable knowledge
  -> project use
  -> postmortem feedback
```

If we make that loop solid, the rest of the system becomes much easier to grow with confidence.
