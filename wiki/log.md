---
type: log
updated: 2026-05-03
---

# Log

## [2026-05-02] structure | Initialize Easy Wiki

Created the initial LLM Wiki structure:

- `AGENTS.md`
- `raw/`
- `wiki/`
- `wiki/index.md`
- `wiki/log.md`

Initialized the first knowledge domain: [[ai-short-drama|AI Short Drama]].

## [2026-05-02] source | Karpathy LLM Wiki

Registered root file `llm-wiki.md` as the seed reference and created [[karpathy-llm-wiki|Karpathy - LLM Wiki]] plus [[llm-wiki-pattern|LLM Wiki Pattern]] and [[llm-wiki-vs-rag|LLM Wiki vs RAG]].

## [2026-05-02] topic | AI Short Drama Chinese Wiki

Added Chinese entry pages for AI short drama:

- [[ai-short-drama-cn|AI 短剧知识地图]]
- [[ai-short-drama-expert-system-cn|AI 短剧专家系统]]
- [[ai-short-drama-implementation-cn|AI 短剧实施手册]]

## [2026-05-02] ingest | AI Short Drama Expert Research Batch 1

Searched and registered the first external expert-source batch for AI short drama production. Created:

- `raw/articles/expert-research-2026-05-02.md`
- [[pixar-storytelling-film-grammar]]
- [[walter-murch-rule-of-six]]
- [[youtube-audience-retention]]
- [[randy-thom-designing-for-sound]]
- [[dga-directing-craft]]
- [[ai-video-prompting-guides]]

Next action: propagate the strongest source ideas into expert pages and templates.

## [2026-05-02] synthesize | Expert Pages Updated From Research Batch 1

Propagated source ideas into:

- [[storyboard-expert]]
- [[editing-expert]]
- [[sound-expert]]
- [[director-expert]]
- [[prompt-expert]]
- [[script-expert]]
- [[cinematography-expert]]
- [[continuity-expert]]

Key synthesis:

- Pixar/Khan reinforces storyboard/storyreel iteration and visual grammar.
- Murch gives editing priority: emotion and story before spatial continuity.
- YouTube retention reports become post-release pacing diagnostics.
- Randy Thom moves sound design earlier into story and scene planning.
- DGA interviews reinforce director ownership of motivation, staging, and whole-story coherence.
- Sora/Runway guides reinforce shot-level prompting with camera, motion, lighting, and temporal progression.

## [2026-05-02] workflow | New Domain Expert Research Workflow

Added [[new-domain-expert-research-workflow]] to formalize the user's preferred process:

1. Decompose a new domain into expert roles.
2. Search expert sources role by role.
3. Ingest sources into the wiki.
4. Synthesize expert frameworks and templates.
5. Plan execution.
6. Start actual work.
7. Postmortem and update the wiki.

Added [[ai-short-drama-expert-map]] as the AI short drama-specific expert decomposition and search map.

## [2026-05-03] structure | Add Domain And Project Layers

Added long-term structure for durable knowledge and concrete execution:

- [[domain-index]]
- [[ai-short-drama-domain-overview]]
- [[ai-short-drama-domain-sources]]
- [[ai-short-drama-domain-framework]]
- [[ai-short-drama-domain-workflows]]
- [[ai-short-drama-domain-projects]]
- [[ai-short-drama-domain-open-questions]]
- [[project-index]]
- [[project-start-workflow]]
- [[decision-index]]
- [[postmortem-index]]

Added project templates:

- [[project-overview-template]]
- [[project-brief-template]]
- [[project-action-plan-template]]
- [[project-decisions-template]]
- [[project-working-notes-template]]
- [[project-postmortem-template]]

## [2026-05-03] architecture | Wiki Database And MCP/API Access Layer

Adjusted the repository architecture around the user's long-term direction:

- `wiki/` is the markdown knowledge database.
- `services/wiki-service/` is the future MCP/API access layer.
- External services should use page ids and service calls instead of hard-coded file paths.
- Added `docs/core-knowledge-architecture.md`.
- Added service contract docs under `services/wiki-service/`.
- Added a minimal read-only HTTP API implementation:
  - `services/wiki-service/wiki_core.py`
  - `services/wiki-service/api_server.py`
- Moved AI short drama topic pages, domain-specific workflows, and domain-specific templates under `wiki/domains/ai-short-drama/`.
- Removed empty legacy `wiki/topics/` and `wiki/templates/` directories.
- Runtime verification was not completed because Python is not installed in the current shell environment.

## [2026-05-03] architecture | Function Boundaries

Added `docs/function-boundaries.md` to clarify current responsibilities, non-goals, boundary risks, and maturity state.

Updated `AGENTS.md` to remove `topic` as an active top-level page type. Existing `type: topic` pages are now treated as domain entry pages under domain folders.

## [2026-05-03] raw | Source Packet Upgrade

Upgraded the raw evidence layer from a link-only registry toward source packets:

- Added `raw/sources/README.md`.
- Added `raw/sources/_templates/source-packet-template.md`.
- Added first-pass source packets, later migrated to `raw/sources/<source-id>/`.
- Split the first expert research batch into 10 raw source packets.

Current status: these packets are still partly `link-only` / `needs-capture`, but each source now has explicit metadata, acquisition status, rights notes, role coverage, and a related wiki source page. Future ingest should add local originals, transcripts, user notes, or mark sources as restricted.

## [2026-05-03] raw | Download Core Expert Source Files

Downloaded public HTML snapshots for sources that allowed direct capture:

- `raw/sources/pixar-in-a-box/captures/original.html`
- `raw/sources/walter-murch-rule-of-six/captures/original.html`
- `raw/sources/walter-murch-rule-of-six/captures/supporting-original.html`
- `raw/sources/randy-thom-designing-for-sound/captures/original.html`

Capture was blocked or incomplete for several sources and recorded accurately:

- Pixar/Khan storytelling: JavaScript shell only, marked `needs-capture`.
- YouTube audience retention: timeout, marked `needs-capture`.
- DGA interview: Incapsula challenge, marked `restricted`.
- OpenAI Sora help: JavaScript/refresh page, marked `needs-capture`.
- OpenAI video generation API: Cloudflare challenge, marked `needs-capture`.
- Runway guides: Cloudflare challenge, marked `restricted`.

## [2026-05-03] raw | Redesign Source Storage

Redesigned `raw/` from batch-owned source folders to source-centric packets:

- `raw/sources/<source-id>/source.md`
- `raw/sources/<source-id>/captures/`
- `raw/sources/<source-id>/assets/`
- `raw/sources/<source-id>/notes/`

Moved research batch files and capture logs into `raw/batches/`. Batches now index source ids instead of owning source folders.
