# Wiki Service

This directory defines the access layer for the core knowledge base.

The service should expose the markdown wiki through:

- MCP tools for AI agents.
- HTTP API for applications and automation.

The service owns path resolution, search, link parsing, and write policy. Consumers should use page ids and API calls rather than hard-coded file paths.

## Repository Boundary

```text
wiki/                  database
services/wiki-service/ access layer contract and future implementation
```

## Minimal Capabilities

- List pages.
- Read page by id.
- Search pages.
- Get backlinks.
- Get page links.
- Lint links.
- Append log entries.
- Create projects from templates.

The current implementation includes read-only HTTP API support for listing, reading, searching, link inspection, and linting.

## Run The HTTP API

Requires Python 3.

From the repository root:

```powershell
python services/wiki-service/api_server.py
```

Then call:

```text
GET http://127.0.0.1:8765/health
GET http://127.0.0.1:8765/pages
GET http://127.0.0.1:8765/pages/script-expert
GET http://127.0.0.1:8765/search?q=shot%20unit
GET http://127.0.0.1:8765/pages/editing-expert/links
GET http://127.0.0.1:8765/lint
```

The current environment used during setup did not have Python installed, so runtime verification was limited to file/link checks.

## Write Policy

Default posture:

- `raw/`: read-only.
- `wiki/sources/`: append/create through ingest.
- `wiki/domains/`: controlled updates.
- `wiki/projects/`: normal project writes.
- `wiki/index.md` and `wiki/log.md`: service-managed updates.

## Documents

- [storage-contract.md](storage-contract.md)
- [api-spec.md](api-spec.md)
- [mcp-tools.md](mcp-tools.md)
- [write-policy.md](write-policy.md)
