# MCP Tools

## Purpose

MCP tools expose the wiki to AI agents without requiring them to know the file layout.

The current runtime is a stdio MCP server in `services/wiki-service/mcp_server.py`.

## Read Tools

### `wiki_list_pages`

Inputs:

```json
{
  "type": "expert",
  "tag": "ai-short-drama"
}
```

Returns catalog records.

### `wiki_read_page`

Inputs:

```json
{
  "id": "script-expert"
}
```

Returns page content, frontmatter, outbound links, and backlinks.

### `wiki_search`

Inputs:

```json
{
  "query": "AI short drama storyboard shot unit",
  "limit": 10
}
```

Returns ranked pages.

### `wiki_get_links`

Inputs:

```json
{
  "id": "editing-expert"
}
```

Returns outbound links and backlinks.

### `wiki_lint`

Inputs:

```json
{}
```

Returns broken links, duplicate ids, and missing metadata.

### `wiki_healthcheck`

Inputs:

```json
{}
```

Returns lint results plus missing index entries, orphan pages, required-section gaps, raw/source coverage, and source usage gaps.

### `wiki_source_usage`

Inputs:

```json
{}
```

Returns raw files, source pages, backlinks, and durable pages fed by each source.

## Write Tools

### `wiki_append_log`

Append an entry to `wiki/log.md`.

### `wiki_create_project`

Create a project folder from templates.

### `wiki_compile_source`

Inputs:

```json
{
  "source_path": "raw/example.md",
  "domain": "ai-short-drama-domain-overview",
  "apply": true
}
```

Creates a source-page draft from a raw original and returns challenge questions, benchmark candidates, suggested links, and next actions.
The compile step also extracts simple top-of-file source metadata such as URL, publisher, published date, expert, and role when present, and returns lifecycle tracking fields for review and promotion.

### `wiki_compile_missing_sources`

Inputs:

```json
{
  "domain": "ai-short-drama-domain-overview",
  "apply": true,
  "limit": 10
}
```

Scans `raw/` for files without source pages and compiles them in batch.
Dry-run calls report `would_write_count` and `would_write_source_ids` instead of treating preview items as skipped.

### `wiki_ingest_source`

Alias for `wiki_compile_source`.

## Not Yet Implemented

These tool names remain part of the contract direction, but they are not yet implemented in the runtime:

- `wiki_create_page`
- `wiki_update_page`

## Workflow Tools

Future higher-level tools:

- `wiki_bootstrap_domain`
- `wiki_research_experts`
- `wiki_start_project`
- `wiki_write_postmortem`
- `wiki_synthesize_sources`

These should compose lower-level read/write tools rather than bypassing the storage contract.
