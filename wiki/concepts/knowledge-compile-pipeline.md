---
type: concept
title: "Knowledge Compile Pipeline"
created: 2026-05-03
updated: 2026-05-03
tags: [llm-wiki, ingest, knowledge-architecture]
---

# Knowledge Compile Pipeline

## Definition

A knowledge compile pipeline is the controlled process that turns raw sources into durable, linked, reusable wiki knowledge.

It is stronger than summarization. A summary says what a source contains. A compile pipeline decides how the source changes the knowledge system.

## Default Pipeline

```text
capture
  -> source summary
  -> claim extraction
  -> challenge / contradiction check
  -> compare with existing wiki
  -> update concepts, experts, domains, workflows
  -> update source usage and links
  -> log changes
```

In the access layer, the service operation for this is `POST /compile-source`.

## Stages

### 1. Capture

If a complete original source file is available, store it under `raw/`.

Record:

- URL or file origin.
- Source metadata in `wiki/sources/`.
- Capture failures in `docs/capture-attempts/`.
- Rights and handling notes in the wiki source page.

### 2. Source Summary

Create a wiki source page under `wiki/sources/`.

Separate:

- What the source says.
- What is useful for the current domain.
- Which pages should be updated.

### 3. Claim Extraction

Extract concrete claims, frameworks, workflows, and examples.

Avoid vague takeaways.

### 4. Challenge

Ask:

- What might be wrong?
- What assumptions does the source make?
- What does it ignore?
- Does it conflict with existing pages?

### 5. Benchmark Against Existing Wiki

Compare source claims with existing concepts, experts, workflows, and domain pages.

The result should be one of:

- Adds new idea.
- Refines existing idea.
- Contradicts existing idea.
- Provides evidence for existing idea.
- Is not useful enough to promote.

### 6. Update Durable Pages

Update only pages that actually change:

- `wiki/concepts/`
- `wiki/experts/`
- `wiki/domains/`
- `wiki/workflows/`
- `wiki/projects/` when project-specific.

### 7. Log And Usage Tracking

Update:

- `wiki/index.md`
- `wiki/log.md`
- source links and usage notes.

Service checks:

- `GET /sources/usage`
- `GET /healthcheck`

## Borrowed From

- [[karpathy-llm-wiki资料]]
- [[微信-llm-wiki内容创作3系统]]

## Links

- [[llm-wiki-pattern]]
- [[source-compile-workflow]]
- [[new-domain-expert-research-workflow]]

