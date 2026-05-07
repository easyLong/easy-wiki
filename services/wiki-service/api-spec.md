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

## Write Endpoints

### `POST /log`

Append a log entry.

### `POST /pages`

Create a new page under an allowed area.

### `PATCH /pages/{id}`

Update a page through a controlled write operation.

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
  "source_path": "raw/articles/example.md",
  "domain": "ai-short-drama-domain-overview"
}
```

## Future Endpoints

- `POST /domains`
- `POST /research/expert-batch`
- `POST /synthesize`
- `POST /postmortems`
