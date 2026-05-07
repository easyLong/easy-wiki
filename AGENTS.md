# Easy Wiki Agent Rules

This repository is an LLM-maintained markdown wiki inspired by Karpathy's LLM Wiki pattern.

## Layers

- `raw/` contains qualified complete readable original source files only. Treat these files as read-only evidence, not as a download cache.
- `wiki/` is the markdown knowledge database. The agent may create and update these files when maintaining the repository directly.
- `services/wiki-service/` defines the MCP/API access layer for external agents and applications.
- `services/governance/` defines the generic execution governance layer for external agents and applications.
- `docs/` contains architecture documents that describe the system outside the wiki database.
- `AGENTS.md` defines the operating rules for future sessions.

The main repo is intentionally narrowed to original evidence, compiled knowledge, the access layer, and generic governance. Non-core app experiments, project-local inputs, capture diagnostics, and non-core domain expansion have been moved to sibling directories outside this repo and should not be recreated inside the main repo unless explicitly requested.

The Karpathy LLM Wiki reference belongs under `raw/` like other original evidence. Do not recreate root-level source duplicates.

## Universal Requirement Intake

All tasks start with requirement intake.

Before searching, planning, archiving sources, creating projects, writing code, or changing architecture, clarify the user's goal enough to choose the correct workflow. Use [[requirement-intake-workflow]] as the default entry gate.

Minimum clarity check:

- Goal.
- Concrete output.
- Current mode: exploration, planning, research, implementation, review, or maintenance.
- Constraints and non-goals.
- Next workflow.

For a new product, game, app, workflow, or version plan, requirement intake is a human deliberation phase. This phase may require repeated back-and-forth with the user until the requirement version is genuinely accepted.

1. Write the interpreted requirement as a named version, such as `v0 需求理解`.
2. List included scope, excluded scope, default assumptions, and open questions.
3. Ask the user to challenge, revise, or confirm this version.
4. Iterate the requirement version when the user changes, corrects, or sharpens the goal.
5. Do not move to expert research, detailed planning, or implementation until the user confirms the requirement version or explicitly asks to proceed with the stated assumptions.

After the requirement version is confirmed, downstream work can proceed through the expert workflows without repeatedly asking for confirmation at every step. Ask again only when a downstream discovery changes the confirmed requirement, introduces a major tradeoff, or requires a user-owned decision.

If the requirement is unclear, ask focused questions before proceeding. For small obvious maintenance requests, this can be a brief internal check and then execution.

## Wiki Conventions

- Use Markdown files with YAML frontmatter.
- Prefer stable ASCII filenames for service contracts, code-owned identifiers, and machine-facing files.
- For user-facing wiki pages, especially project planning pages, source/reference pages, and raw original files, prefer readable Chinese filenames when the user is working in Chinese.
- Keep machine identifiers in frontmatter, such as `project: douyin-xiyou-gacha-game`, stable even when the visible file name is Chinese.
- Use Obsidian-style links: `[[page-name]]` or `[[page-name|display text]]`.
- Keep claims traceable through a `Sources` section when they come from a specific source.
- When creating or materially changing wiki pages, update `wiki/index.md`.
- Append an entry to `wiki/log.md` after ingest, query filing, lint, or structural changes.
- Treat filenames without `.md` as page ids.
- Page paths are allowed to change. External consumers should use page ids through MCP/API instead of hard-coding paths.

## Access Model

This repository should be treated as:

```text
raw/                 readable original source file store
wiki/                markdown database
services/wiki-service/  access layer
services/governance/    generic governance layer
```

Direct file editing is acceptable for repository maintenance sessions. External services, product code, and other agents should use the access layer defined in `services/wiki-service/` and the governance layer defined in `services/governance/`.

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
- `expert`: role-specific thinking model for a domain or project.
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
2. Place a source under `raw/` only when it is a strong complete original: actual body content, useful for future synthesis, traceable, and at least medium evidence.
3. Do not put metadata, notes, blocked pages, capture logs, HTML snapshots, webpage wrappers, partial shells, landing pages, documentation indexes, or weak secondary articles in `raw/`.
4. Use [[source-compile-workflow]] or the service operation `POST /compile-source` to create a source-page draft.
5. Extract relevant entities, concepts, tools, workflows, and open questions.
6. Update existing domain/concept/expert pages when the source changes the synthesis.
7. Create new pages only when they will be reused.
8. Add cross-links.
9. Run source usage and health checks when practical.
10. Update `wiki/index.md`.
11. Append to `wiki/log.md`.

Do not treat a bare URL, blocked page, JavaScript shell, HTML wrapper, landing page, index page, or failed capture as raw evidence. Failed capture diagnostics and large HTML snapshots belong in a sibling archive such as `C:\Code\easy-wiki-capture-attempts`, not in this core repo.

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

## Seed Domain: AI Short Drama

This wiki currently contains AI-assisted short drama as the first seeded domain. Treat it as reusable compiled knowledge inside a general wiki platform, not as the only purpose of the repository.

The seed domain covers:

- Script and dramatic structure.
- Storyboarding and shot design.
- Directing, visual continuity, and character consistency.
- Editing rhythm and retention.
- Sound, music, and delivery.
- Prompting, asset control, and production QA.

Treat the expert pages as reusable thinking models. They are not named real-world authorities; they are role lenses that may be applied by domain-specific consumers such as `easy-wiki-studio`.

## Scope Control

Do not continue expanding unrelated domains or app prototypes inside this repository by default.

If the user wants to explore a new domain or build an experimental app, prefer placing that work outside the main `easy-wiki` repo unless the user explicitly says the core repo should absorb it.

## New Domain Bootstrap Workflow

When the user starts something unfamiliar, use [[new-domain-expert-research-workflow]] as the default approach:

1. Run requirement intake first.
2. Explore the user's goal, constraints, and success criteria.
3. Create a research plan before searching.
4. Decompose the domain into expert roles.
5. Search high-quality sources one expert role at a time.
6. Classify found sources by quality and evidence strength.
7. Remind the user when an important source is worth archiving into `raw/`.
8. Ingest useful source records into `wiki/sources/`.
9. Archive only qualified originals into `raw/`.
10. Compile durable ideas into expert, concept, workflow, and template pages.
11. Create an execution plan only after the expert framework exists.
12. Start actual work through concrete artifacts.
13. Write a postmortem and update the wiki.

Do not jump directly to advice when the user is asking to learn or start a new field from scratch.

## Project Workflow

When the user starts actual work inside an existing domain, use [[project-start-workflow]]:

1. Run requirement intake first.
2. Read `wiki/index.md`.
3. Read the relevant domain overview.
4. Create a project folder under `wiki/projects/<project-slug>/`.
5. Create project overview, brief, action plan, decisions, working notes, review, and postmortem files.
6. Bind only the expert pages needed for that project.
7. Execute by updating project artifacts.
8. At the end, write a postmortem and propagate lessons back to durable wiki pages.

## Domain To Project Implementation Workflow

When a new domain has enough framing to become a concrete MVP, use [[domain-to-project-implementation-workflow]].

Default sequence:

1. Confirm the project framing: problem, target user, first output, success criteria, constraints, and non-goals.
2. Bind only the expert lenses needed for the project.
3. Define the smallest MVP that proves the key assumption.
4. Set architecture boundaries: platform, language/framework, local folder, data, external services, preview/test method.
5. Use [[implementation-plan-template]] for execution.
6. Use [[mvp-validation-template]] for validation.
7. Record decisions in the project decision log.
8. Feed project lessons back into domain, source, workflow, and template pages.

If the user says "start developing" but the product idea, target user, or success criteria are unclear, create or update requirement and planning artifacts first. Do not pretend implementation is ready.

