---
type: decision-index
updated: 2026-05-03
---

# Decision Index

## Purpose

This page tracks durable decisions that shape the wiki itself or long-running domains.

Project-specific decisions should live inside `wiki/projects/<project-slug>/`.

## Decisions

- 2026-05-03: Add long-term domain and project layers to separate durable knowledge from concrete execution.
- 2026-05-03: Treat `wiki/` as the markdown database and `services/wiki-service/` as the future MCP/API access layer. External clients should use page ids and service calls instead of hard-coded file paths.

## Links

- [[domain-index]]
- [[project-index]]
