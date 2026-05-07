# Write Policy

## Default Principle

The service protects the wiki as a long-term database. Writes must be explicit, logged, and scoped.

## Areas

### `raw/`

Default: read-only.

Allowed:

- Add qualified complete readable original source files under `raw/`.

Disallowed:

- Rewrite source evidence.
- Delete source evidence without explicit approval.
- Add metadata files.
- Add source cards.
- Add notes.
- Add capture logs.
- Add blocked pages or JavaScript shell pages.
- Add HTML snapshots or webpage wrappers.
- Add landing pages, documentation indexes, or weak secondary pages that are not strong enough as durable evidence.

Metadata belongs in `wiki/sources/`. Failed capture diagnostics and large HTML snapshots belong in a sibling archive such as `C:\Code\easy-wiki-capture-attempts`, not in this core repo.

### `wiki/sources/`

Default: append/create.

Allowed:

- Create source summaries.
- Create compiled source drafts from `raw/` originals.
- Add implications and links.

Current service behavior:

- `POST /compile-source` creates a source page only when one does not already exist.
- Existing source pages are not overwritten by the deterministic service operation.

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

Current service behavior:

- `POST /projects` creates a project folder and standard project files from built-in templates.
- Existing project files are skipped rather than overwritten.

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

