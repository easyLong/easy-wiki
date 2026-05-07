# Easy Wiki Agent Rules

This repository is an LLM-maintained markdown wiki inspired by Karpathy's LLM Wiki pattern.

## Layers

- `raw/` contains source materials. Treat these files as read-only evidence.
- `wiki/` is the markdown knowledge database. The agent may create and update these files when maintaining the repository directly.
- `services/wiki-service/` defines the MCP/API access layer for external agents and applications.
- `docs/` contains architecture documents that describe the system outside the wiki database.
- `AGENTS.md` defines the operating rules for future sessions.

The root `llm-wiki.md` is the original Karpathy reference downloaded by the user. Do not edit it unless explicitly asked.

## Wiki Conventions

- Use Markdown files with YAML frontmatter.
- Prefer stable ASCII filenames.
- Use Obsidian-style links: `[[page-name]]` or `[[page-name|display text]]`.
- Keep claims traceable through a `Sources` section when they come from a specific source.
- When creating or materially changing wiki pages, update `wiki/index.md`.
- Append an entry to `wiki/log.md` after ingest, query filing, lint, or structural changes.
- Treat filenames without `.md` as page ids.
- Page paths are allowed to change. External consumers should use page ids through MCP/API instead of hard-coding paths.

## Access Model

This repository should be treated as:

```text
raw/                 evidence store
wiki/                markdown database
services/wiki-service/  access layer
```

Direct file editing is acceptable for repository maintenance sessions. External services, product code, and other agents should use the access layer defined in `services/wiki-service/`.

The access layer is responsible for:

- Page id to file path resolution.
- Listing pages.
- Reading pages.
- Searching pages.
- Parsing wikilinks and backlinks.
- Linting links and metadata.
- Creating projects.
- Appending logs.
- Enforcing write policy.

## Page Types

- `source`: summary of one raw/reference source.
- `concept`: reusable idea or framework.
- `expert`: role-specific thinking model for AI short drama production.
- `workflow`: repeatable operating procedure.
- `template`: reusable production artifact.
- `comparison`: structured comparison.
- `domain`: long-lived knowledge area that can support many projects.
- `project`: concrete execution space for one piece of work.
- `decision`: durable choice that affects a project, domain, or the wiki.
- `postmortem`: lessons learned after execution.

Legacy pages with `type: topic` may exist inside a domain folder. Treat them as domain entry pages, not as a separate top-level topic layer.

## Long-Term Structure

- `wiki/domains/` contains durable domain knowledge and domain-specific indexes.
- `wiki/projects/` contains concrete execution work and project templates.
- `wiki/decisions/` contains durable wiki/domain decisions.
- `wiki/postmortems/` contains cross-project lesson indexes and summaries.
- `wiki/workflows/` contains cross-domain workflows only.
- Domain-specific workflows and templates should live under the relevant domain folder.

Use domain pages for reusable knowledge. Use project pages for concrete work. Feed project lessons back into domain, expert, workflow, and template pages.

## Ingest Workflow

When the user asks to ingest a source:

1. Read the source.
2. Create or update a source-centric raw source packet under `raw/sources/<source-id>/` unless a packet already exists.
3. Record acquisition status: `provided-file`, `local-copy`, `link-only`, `needs-capture`, or `restricted`.
4. Create or update a `wiki/sources/` summary page.
5. Extract relevant entities, concepts, tools, workflows, and open questions.
6. Update existing domain/concept/expert pages when the source changes the synthesis.
7. Create new pages only when they will be reused.
8. Add cross-links.
9. Update `wiki/index.md`.
10. Append to `wiki/log.md`.

Do not treat a bare URL as strong evidence. A URL can start the ingest process, but the raw layer should record whether a local copy, source file, transcript, note, or restricted-link-only packet exists.

Raw source packets use this structure:

```text
raw/sources/<source-id>/
  source.md
  captures/
  assets/
  notes/
```

Research batches belong in `raw/batches/` and should reference source ids. Do not nest source packets under batch folders.

## Query Workflow

When answering questions from the wiki:

1. Read `wiki/index.md` first.
2. Read the most relevant pages.
3. Check source pages or raw files when factual grounding matters.
4. Answer directly.
5. If the answer has durable value, file it back into `wiki/` as a new page or update an existing page.

## Lint Workflow

When asked to lint the wiki, check for:

- Missing index entries.
- Broken or stale cross-links.
- Duplicate concepts.
- Orphan pages that should be linked.
- Claims without source context.
- Production templates that no longer match workflows.
- Topic pages that need synthesis updates.

## AI Short Drama Focus

This wiki currently focuses on AI-assisted short drama production, especially:

- Script and dramatic structure.
- Storyboarding and shot design.
- Directing, visual continuity, and character consistency.
- Editing rhythm and retention.
- Sound, music, and delivery.
- Prompting, asset control, and production QA.

Treat the expert pages as reusable thinking models. They are not named real-world authorities; they are role lenses for planning and reviewing AI short drama work.

## New Domain Bootstrap Workflow

When the user starts something unfamiliar, use [[new-domain-expert-research-workflow]] as the default approach:

1. Frame the domain and success criteria.
2. Decompose the domain into expert roles.
3. Search high-quality sources one expert role at a time.
4. Ingest sources into `wiki/sources/`.
5. Compile durable ideas into expert, concept, workflow, and template pages.
6. Create an execution plan only after the expert framework exists.
7. Start actual work through concrete artifacts.
8. Write a postmortem and update the wiki.

Do not jump directly to advice when the user is asking to learn or start a new field from scratch.

## Project Workflow

When the user starts actual work inside an existing domain, use [[project-start-workflow]]:

1. Read `wiki/index.md`.
2. Read the relevant domain overview.
3. Create a project folder under `wiki/projects/<project-slug>/`.
4. Create project overview, brief, action plan, decisions, working notes, review, and postmortem files.
5. Bind only the expert pages needed for that project.
6. Execute by updating project artifacts.
7. At the end, write a postmortem and propagate lessons back to durable wiki pages.
