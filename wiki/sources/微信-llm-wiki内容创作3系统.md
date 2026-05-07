---
type: source
title: "WeChat Case Study - LLM Wiki 内容创作3.0系统"
source_id: wechat-uSNIibUFNVnZg1JSoeqtHg
raw_original_path: raw/微信-llm-wiki内容创作3系统-原文.md
source_url: "https://mp.weixin.qq.com/s/uSNIibUFNVnZg1JSoeqtHg"
date_added: 2026-05-03
status: compiled-source
review_status: reviewed
promotion_status: promoted
tags: [llm-wiki, content-production, knowledge-architecture, zh]
---

# WeChat Case Study - LLM Wiki 内容创作3.0系统

## Summary

This WeChat article is a practical implementation case for an LLM Wiki-powered content production system. The author describes moving from an automated writing pipeline to a stronger knowledge-compilation system where raw materials are turned into reusable wiki pages, concepts, methods, indexes, and logs.

## Main System Pattern

The article's core pattern is:

```text
raw sources
  -> LLM compilation
  -> wiki summaries / concepts / methods / indexes
  -> content production workflows
  -> regular health checks
```

The useful distinction is between:

- runtime retrieval: finding and assembling knowledge only when writing.
- compile-time wiki: processing knowledge before it is needed, then keeping it maintained.

## Implementation Ideas Worth Borrowing

### 1. Compilation Should Be More Than Summary

The article argues that plain summarization can compress information without resolving tension between sources. Its practical improvement is a staged compilation process that forces the LLM to question and compare source material instead of only extracting notes.

Borrow for this repo:

- Add explicit compile stages to ingest.
- Separate "what the source says" from "how it changes the framework."
- Track contradictions and differences between sources.

### 2. Source Utilization Matters

The author reports that many collected materials were never referenced after ingestion. This maps directly to a risk in this repo: `raw/` can become a warehouse unless the wiki tracks how sources are used.

Borrow for this repo:

- Add `source_usage` or backlinks from wiki summaries to raw source ids.
- Add lint checks for sources with no wiki source page.
- Add lint checks for wiki source pages that do not feed concepts, experts, domains, or workflows.

### 3. Health Checks Need Concrete Dimensions

The article uses health checks around consistency, completeness, isolated pages, and cross-directory rule conflicts.

Borrow for this repo:

- Extend `wiki_lint` beyond broken links.
- Add consistency checks for duplicate concept definitions.
- Add completeness checks for required frontmatter and required sections.
- Add orphan/island checks.
- Add cross-domain or cross-project rule conflict checks.

### 4. Instruction Files Are Part Of The System

The article treats instruction files such as `CLAUDE.md` as operational infrastructure, not casual notes.

Borrow for this repo:

- Keep `AGENTS.md` as the canonical maintenance policy.
- Consider domain-specific agent rules when a domain becomes large.
- Add output-channel style guides only when content production becomes a real project.

### 5. Compiled Knowledge Can Become A Product

The article's strongest commercial insight is that the valuable asset is not the raw material but the compiled, maintained knowledge structure.

Borrow for this repo:

- Keep raw evidence private and traceable.
- Make compiled domain frameworks and expert systems reusable.
- Treat project postmortems as material that improves the knowledge asset.

## Differences From This Repository

The article focuses on content production and multi-account publishing. This repository is currently broader and more infrastructure-oriented:

- `wiki/` is treated as a database.
- `services/wiki-service/` is the future MCP/API access layer.
- `wiki/domains/` and `wiki/projects/` separate reusable knowledge from concrete work.
- `raw/` stores complete readable original files only.

## Recommended Changes

- Add a formal compile pipeline page.
- Add stronger lint categories.
- Track source usage.
- Add domain-specific style guides only after the first real content or short-drama project exists.

## Sources

- Raw original: `raw/微信-llm-wiki内容创作3系统-原文.md`

