# Core Knowledge Architecture

## Positioning

This repository is a long-term core knowledge base.

The architecture is:

```text
raw/                 evidence store
wiki/                markdown knowledge database
services/wiki-service/  MCP/API access layer
AGENTS.md            maintenance policy for agents
```

External services should not depend on the physical layout of `wiki/`. They should call the access layer.

## Layer Responsibilities

### raw/

Stores original materials, source registries, and source packets.

Rules:

- Treat as evidence.
- Avoid modifying original sources.
- Prefer adding new source files over rewriting old ones.
- Prefer source packets under `raw/sources/` over bare link lists.
- Use `raw/sources/<source-id>/` as the durable location for each source.
- Use `raw/batches/` only for collection manifests and capture logs.
- Record acquisition status for each source.

### wiki/

Stores durable knowledge pages.

Rules:

- It is the database, not just documentation.
- Pages are identified by stable page ids, usually their filename without `.md`.
- Page paths may change.
- External consumers must not hard-code page paths.

### services/wiki-service/

Defines the access layer that makes the wiki pluggable.

Responsibilities:

- Resolve page ids to files.
- Read pages.
- Search pages.
- Parse frontmatter and wikilinks.
- Return backlinks.
- Create projects.
- Append logs.
- Enforce write policy.
- Expose MCP tools for agents and HTTP API for applications.

## Access Rule

```text
Agents maintaining the repository may edit files directly.
External agents and applications should use MCP/API.
```

## Target Runtime Shape

```text
Codex / Claude / Cursor
        |
        | MCP tools
        v
Wiki Service
        |
        v
wiki/ markdown database

Web app / automation / product service
        |
        | HTTP API
        v
Wiki Service
        |
        v
wiki/ markdown database
```

## Why This Is Loosely Coupled

- The wiki folder can be reorganized without breaking clients.
- Search, link parsing, logging, and write rules live in one place.
- Multiple agents and apps can share the same knowledge base.
- Writes can be controlled instead of allowing arbitrary file edits.

## Current State

The repository currently contains:

- The markdown database under `wiki/`.
- The access-layer contract under `services/wiki-service/`.
- A minimal read-only HTTP API implementation under `services/wiki-service/`.

The HTTP API has not been runtime-verified in the current shell environment because Python is not installed.

See [function-boundaries.md](function-boundaries.md) for current capabilities, non-goals, and boundary risks.
