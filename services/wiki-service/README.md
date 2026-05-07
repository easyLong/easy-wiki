# Wiki Service

This directory defines the current access layer for the core knowledge base.

The service should expose the markdown wiki through:

- MCP tools for AI agents.
- HTTP API for applications and automation.

The service owns path resolution, search, link parsing, and write policy. Consumers should use page ids and API calls rather than hard-coded file paths.

## Repository Boundary

```text
wiki/                  database
services/wiki-service/ access layer contract and implementation
```

## Minimal Capabilities

- List pages.
- Read page by id.
- Search pages.
- Get backlinks.
- Get page links.
- Lint links and run wiki health checks.
- Track raw/source usage.
- Compile raw source files into source-page drafts.
- Scan `raw/` for uncompiled originals and batch-compile them.
- Append log entries through service operations.
- Create projects from templates.

The current implementation includes HTTP API support for listing, reading, searching, link inspection, linting, health checks, source usage reports, source compilation drafts, project creation, and log appends.

The current implementation also includes a basic MCP stdio server for initialization, tool listing, and tool calls against the same `wiki_core.py` logic.

Compiled source drafts now include lifecycle tracking such as `review_status`, `promotion_status`, `compiled_at`, and `compile_version`.

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
GET http://127.0.0.1:8765/healthcheck
GET http://127.0.0.1:8765/sources/usage
POST http://127.0.0.1:8765/compile-source
POST http://127.0.0.1:8765/compile-missing-sources
POST http://127.0.0.1:8765/projects
POST http://127.0.0.1:8765/log
```

Runtime verification passed with Python 3.14.3 in the current shell environment.

## Run The MCP Server

Requires Python 3.

From the repository root:

```powershell
python services/wiki-service/mcp_server.py
```

The MCP server currently supports:

- `initialize`
- `notifications/initialized`
- `ping`
- `tools/list`
- `tools/call`

Implemented tools:

- `wiki_list_pages`
- `wiki_read_page`
- `wiki_search`
- `wiki_get_links`
- `wiki_lint`
- `wiki_healthcheck`
- `wiki_source_usage`
- `wiki_append_log`
- `wiki_create_project`
- `wiki_compile_source`
- `wiki_compile_missing_sources`
- `wiki_ingest_source`

## Scan Raw Batch

To scan `raw/` for files that do not yet have `wiki/sources/` pages:

```powershell
python services/wiki-service/scan_raw.py
```

Dry-run output reports `would_write_count` and `would_write_source_ids`, so previewed files are separated from true skips.

To actually write the missing compiled drafts:

```powershell
python services/wiki-service/scan_raw.py --apply
```

When raw files begin with lines such as `Source URL:`, `Publisher:`, `Expert:`, or `Published:`, the compiler now keeps that metadata separate from the article body so summaries and extracted claims stay cleaner.

## Run The Tests

From the repository root:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

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
