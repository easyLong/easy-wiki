# MCP Tools

## Purpose

MCP tools expose the wiki to AI agents without requiring them to know the file layout.

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

## Write Tools

### `wiki_append_log`

Append an entry to `wiki/log.md`.

### `wiki_create_page`

Create a page in an allowed area.

### `wiki_update_page`

Update an existing page with write-policy checks.

### `wiki_create_project`

Create a project folder from templates.

### `wiki_ingest_source`

Create source summary pages and update related pages.

## Workflow Tools

Future higher-level tools:

- `wiki_bootstrap_domain`
- `wiki_research_experts`
- `wiki_start_project`
- `wiki_write_postmortem`
- `wiki_synthesize_sources`

These should compose lower-level read/write tools rather than bypassing the storage contract.
