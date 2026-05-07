# Function Boundaries

## Summary

This repository has four clear responsibilities:

1. Store original evidence in `raw/`.
2. Store durable knowledge in `wiki/`.
3. Expose the knowledge database through `services/wiki-service/`.
4. Guide maintenance through `AGENTS.md`.

It is not intended to be a full production application by itself.

## Current Functional Capabilities

### Evidence Storage

Owned by `raw/`.

Current capabilities:

- Store source registries.
- Store source packets with metadata, acquisition status, local files, assets, and notes.
- Keep durable source packets source-centric under `raw/sources/<source-id>/`.
- Keep research batch manifests under `raw/batches/`.
- Store original articles, notes, and future project inputs when available.
- Preserve evidence separately from synthesized knowledge.

Boundary:

- `raw/` should not become the main working area.
- Do not rewrite original source evidence during synthesis.
- Bare links are weak evidence. Prefer source packets with local files, transcripts, notes, or explicit `link-only` / `restricted` status.
- Do not nest source packets under batch folders. A source can belong to multiple batches or domains.

### Knowledge Database

Owned by `wiki/`.

Current capabilities:

- Store source summaries.
- Store durable concepts.
- Store expert role frameworks.
- Store domain frameworks.
- Store project templates.
- Store project indexes.
- Store decisions and postmortem indexes.
- Maintain links through Obsidian-style wikilinks.

Boundary:

- `wiki/` is not the runtime service.
- `wiki/` should not contain application code.
- External clients should not depend on wiki paths.

### Domain Knowledge

Owned by `wiki/domains/`.

Current capabilities:

- Maintain long-lived domain context.
- Group domain-specific workflows and templates.
- Track domain source maps, open questions, and project lessons.

Boundary:

- Domain pages are reusable knowledge, not one-off project execution files.
- Domain-specific content should stay under its domain folder.

### Project Execution Knowledge

Owned by `wiki/projects/`.

Current capabilities:

- Store concrete project artifacts.
- Store briefs, action plans, decisions, working notes, reviews, and postmortems.
- Feed project lessons back into domains and expert pages.

Boundary:

- Project pages are not the source of general truth unless promoted back into domain/expert/workflow/template pages.

### Expert Frameworks

Owned by `wiki/experts/`.

Current capabilities:

- Store reusable expert-role thinking models.
- Link expert roles to sources and review questions.
- Guide execution and review across projects.

Boundary:

- Expert pages are role lenses, not biographies.
- Expert pages should not become project-specific notes.

### Access Layer

Owned by `services/wiki-service/`.

Current capabilities:

- Service contract for MCP and HTTP API.
- Read-only HTTP API implementation for list/read/search/link/lint operations.
- Storage contract, API spec, MCP tool spec, and write policy.

Boundary:

- It is not yet a complete production service.
- Write endpoints and MCP runtime are specified but not fully implemented.
- It should not contain domain knowledge.

## Current Non-Goals

This repository is not currently responsible for:

- Hosting a public web application.
- Storing large binary media assets.
- Running AI model inference.
- Generating video or audio.
- Managing user authentication.
- Serving as a full CMS.
- Replacing Obsidian or an editor.
- Implementing a production vector database.
- Guaranteeing multi-user write conflict resolution.

These can be added as separate services later.

## Boundary Risks

### Risk: Wiki Becomes A Dumping Ground

Mitigation:

- Ingest sources into `wiki/sources/`.
- Promote durable ideas into domain, expert, concept, workflow, or template pages.
- Put execution details into `wiki/projects/`.

### Risk: External Clients Couple To File Paths

Mitigation:

- Use page ids through MCP/API.
- Let `services/wiki-service/` resolve paths.

### Risk: Project Lessons Do Not Feed Back

Mitigation:

- Require postmortems.
- Update domain and expert pages after project completion.

### Risk: Service Layer Grows Domain Logic

Mitigation:

- Keep service layer generic.
- Domain logic belongs in `wiki/`.
- Workflow orchestration should read wiki pages instead of hard-coding domain rules.

## Maturity State

| Area | State |
|---|---|
| Markdown knowledge database | Usable |
| AI short drama domain | Seeded |
| Expert frameworks | Seeded |
| Project layer | Structured, no active projects yet |
| Source ingest process | Manual but working |
| Raw source packets | Source-centric packet structure in place; first batch migrated |
| Link linting | Manual PowerShell check works |
| HTTP API | Read-only implementation added, not runtime-verified in this environment |
| MCP API | Specified, not implemented |
| Write API | Specified, not implemented |
| Search | Basic implementation added in Python core |

## Next Boundary Improvements

1. Install Python or choose the runtime for `services/wiki-service/`.
2. Runtime-test the HTTP API.
3. Implement MCP server using the same wiki core.
4. Add write operations only after read operations are stable.
5. Create the first real project and test project-to-domain feedback.
