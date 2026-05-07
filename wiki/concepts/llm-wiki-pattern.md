---
type: concept
tags: [knowledge-management, llm]
---

# LLM Wiki Pattern

## Definition

An LLM Wiki is a persistent, interlinked Markdown knowledge base maintained by an LLM. It sits between raw sources and user queries.

```text
raw sources -> maintained wiki -> query, analysis, production output
```

## Operating Principle

The LLM does not wait until query time to rediscover knowledge. It continuously compiles useful information into durable pages, updates existing synthesis, and creates cross-links.

## Why It Matters

For long-running research or production domains, the main cost is not reading one document. The main cost is maintaining structure: summaries, links, contradictions, reusable frameworks, and logs. This pattern delegates that maintenance work to the LLM.

## In This Wiki

The pattern is used to build an AI short drama knowledge base. Each production role has a page, and each reusable method becomes a linkable concept or workflow.

## Links

- Source: [[karpathy-llm-wiki]]
- Comparison: [[llm-wiki-vs-rag]]
- Domain: [[ai-short-drama]]
