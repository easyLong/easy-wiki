---
type: workflow
title: "Source Compile Workflow"
created: 2026-05-03
updated: 2026-05-03
tags: [workflow, ingest, llm-wiki]
---

# Source Compile Workflow

## Purpose

Turn one readable raw original into durable wiki knowledge without leaving it as an isolated source summary.

## Trigger

Use this workflow when a new file is added under `raw/`.

## Service Operation

Call the access layer:

```text
POST /compile-source
```

Example body:

```json
{
  "source_path": "raw/example.md",
  "domain": "ai-short-drama-domain-overview",
  "apply": true
}
```

The service creates a source-page draft when no source page exists yet.

## Compile Stages

1. Read the raw original.
2. Create or identify the `wiki/sources/` page.
3. Produce a summary draft.
4. Extract concrete claims.
5. Ask challenge questions.
6. Benchmark against existing wiki pages.
7. Suggest durable pages to update.
8. Update `wiki/index.md` and `wiki/log.md` when a new source page is created.

## Promotion Rule

The service may draft source pages, but durable synthesis still requires an LLM maintainer to update:

- `wiki/concepts/`
- `wiki/experts/`
- `wiki/domains/`
- `wiki/workflows/`
- `wiki/projects/` when project-specific

Do not promote claims mechanically. Review assumptions, conflicts, and domain fit first.

## Health Check

After promotion, run:

```text
GET /healthcheck
GET /sources/usage
```

The source should no longer appear as unused. It should feed at least one durable page through a wikilink or backlink.

## Links

- [[knowledge-compile-pipeline]]
- [[new-domain-expert-research-workflow]]
- [[llm-wiki-pattern]]
