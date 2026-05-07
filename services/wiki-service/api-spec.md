# HTTP API Spec

## Principles

- Clients use page ids, not file paths.
- Responses include page metadata and resolved paths for observability.
- Writes go through explicit operations that update `wiki/log.md`.

## Read Endpoints

### `GET /health`

Returns service health.

### `GET /pages`

Query params:

- `type`
- `tag`
- `domain`
- `project`

Returns catalog records.

### `GET /pages/{id}`

Returns:

```json
{
  "id": "script-expert",
  "path": "wiki/experts/script-expert.md",
  "frontmatter": {},
  "content": "...",
  "links": [],
  "backlinks": []
}
```

### `GET /search?q=<query>`

Returns ranked page matches.

Minimum implementation can use filename, title, tags, headings, and body text search.

Later implementation can add BM25/vector hybrid search.

### `GET /pages/{id}/links`

Returns outbound links and backlinks.

### `GET /lint`

Returns:

- Broken links.
- Duplicate page ids.
- Missing frontmatter.
- Pages missing from `wiki/index.md`.

### `GET /healthcheck`

Returns the stronger weekly wiki health report:

- Basic lint results.
- Pages missing from `wiki/index.md`.
- Orphan pages.
- Pages missing required sections.
- Raw files with no `wiki/sources/` page.
- Source pages pointing to missing raw files.
- Source pages that do not feed any durable page.
- Source drafts pending review or promotion.
- Durable pages that have no explicit source context.

### `GET /sources/usage`

Returns raw/source usage mapping:

```json
{
  "raw_files": ["raw/example.md"],
  "raw_files_missing_source_page": [],
  "source_pages_missing_raw_file": [],
  "source_pages_without_usage": [],
  "source_pages_without_durable_usage": [],
  "source_pages_pending_review": [],
  "source_pages_not_promoted": [],
  "durable_pages_without_source_context": [],
  "closure_counts": {},
  "sources": []
}
```

Durable usage means a durable page links back to the source page. Candidate links inside a source draft do not count as promotion.

### `GET /sources/promotion-candidates`

Returns source drafts that need review, promotion, or durable usage.

```json
{
  "candidate_count": 1,
  "candidates": [
    {
      "source_id": "example-source",
      "review_status": "pending-review",
      "promotion_status": "not-promoted",
      "durable_usage_pages": [],
      "suggested_targets": [],
      "reason": "source draft still needs human review; promotion_status is not promoted; no durable page currently uses this source",
      "priority": 18
    }
  ]
}
```

## Write Endpoints

### `POST /log`

Append a log entry.

### `POST /pages`

Create a new page under an allowed area.

### `PATCH /pages/{id}`

Update a page through a controlled write operation.

### `POST /compile-source`

Compile a readable raw original into a source-page draft.

Request:

```json
{
  "source_path": "raw/example.md",
  "title": "Example Source",
  "domain": "ai-short-drama-domain-overview",
  "apply": true
}
```

Behavior:

- Reads only files under `raw/`.
- Creates `wiki/sources/<source-id>.md` only when no source page exists.
- Separates top-of-file source metadata from article body when possible, then generates the summary draft, condensed takeaways, extracted claims, challenge notes, benchmark/transfer notes, promotion candidates, suggested links, and next actions from the body.
- Adds lifecycle tracking fields such as `review_status`, `promotion_status`, `compiled_at`, and `compile_version` to newly written source drafts.
- Updates `wiki/index.md` and appends `wiki/log.md` when `apply` is true and a new source page is created.

### `POST /ingest`

Alias for `POST /compile-source`.

### `POST /compile-missing-sources`

Scan `raw/` for files that do not yet have source pages and compile them in batch.

Request:

```json
{
  "domain": "ai-short-drama-domain-overview",
  "apply": true,
  "limit": 10
}
```

Behavior:

- Finds raw files missing `wiki/sources/` pages.
- Runs the same compile logic as `POST /compile-source` for each pending file.
- When `apply` is false, returns a dry-run report with `would_write_count` and `would_write_source_ids`.
- When `apply` is true, writes missing source drafts and updates `wiki/index.md` and `wiki/log.md`.

### `POST /scan-raw`

Alias for `POST /compile-missing-sources`.

### `POST /maintain-sources`

Run one source maintenance pass.

Request:

```json
{
  "domain": "cross-border-ecommerce-domain-overview",
  "apply": true,
  "limit": 10
}
```

Behavior:

- Compiles raw files that do not yet have source pages.
- Reports source closure counts.
- Reports promotion candidates that still need durable-page updates.
- Returns a health summary and next actions.

This endpoint automates `raw -> wiki/sources`. Durable promotion remains a maintainer/agent step because it changes synthesized knowledge pages.

### `POST /projects`

Create a project from templates.

Request:

```json
{
  "slug": "short-drama-001",
  "domain": "ai-short-drama-domain-overview",
  "title": "Short Drama 001"
}
```

### `POST /ingest`

Register or ingest a source.

Request:

```json
{
  "source_path": "raw/example.md",
  "domain": "ai-short-drama-domain-overview"
}
```

## Future Endpoints

- `POST /domains`
- `POST /research/expert-batch`
- `POST /synthesize`
- `POST /postmortems`

