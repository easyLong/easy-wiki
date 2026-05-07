# Write Policy

## Default Principle

The service protects the wiki as a long-term database. Writes must be explicit, logged, and scoped.

## Areas

### `raw/`

Default: read-only.

Allowed:

- Add new source files.
- Add source registry files.
- Add source packets under `raw/sources/`.
- Add batch manifests under `raw/batches/`.
- Add local originals, snapshots, notes, transcripts, and assets when permitted.

Disallowed:

- Rewrite source evidence.
- Delete source evidence without explicit approval.

Required for source packets:

- `source.md` metadata file.
- Acquisition status.
- Rights or handling note.
- Stable `source_id`.
- Source files stored under `raw/sources/<source-id>/`, not under batch folders.

### `wiki/sources/`

Default: append/create.

Allowed:

- Create source summaries.
- Add implications and links.

### `wiki/domains/`

Default: controlled update.

Allowed:

- Update frameworks after source synthesis or project postmortems.
- Add open questions.
- Add domain project links.

### `wiki/experts/`

Default: controlled update.

Allowed:

- Add research inputs.
- Refine role rules.
- Add review questions.

### `wiki/projects/`

Default: normal write area for execution.

Allowed:

- Create project folders.
- Update project artifacts.
- Record decisions and postmortems.

### `wiki/index.md`

Default: service-managed.

Update after:

- New durable page.
- New source.
- New domain.
- New project.

### `wiki/log.md`

Default: append-only.

Append after:

- Ingest.
- Domain bootstrap.
- Project creation.
- Synthesis.
- Lint.
- Structural change.

## Destructive Operations

Delete or move operations must:

- Preserve useful content when possible.
- Update links and indexes.
- Add a log entry.
- Prefer moving within `wiki/` over deletion.
