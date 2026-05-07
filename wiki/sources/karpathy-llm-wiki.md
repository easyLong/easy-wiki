---
type: source
title: "LLM Wiki"
author: "Andrej Karpathy"
source_path: "../../llm-wiki.md"
date_added: 2026-05-02
tags: [llm, wiki, knowledge-management]
---

# Karpathy - LLM Wiki

## Summary

Karpathy proposes a pattern for building personal or team knowledge bases where an LLM incrementally maintains a persistent Markdown wiki. Instead of retrieving raw document chunks at query time, the LLM reads sources, extracts durable knowledge, updates linked pages, records contradictions, and keeps an evolving synthesis current.

## Core Claims

- The wiki is a persistent compounding artifact, not a temporary answer.
- Raw sources should remain immutable.
- The LLM owns the generated wiki layer: summaries, pages, cross-links, index, and log.
- A schema file such as `AGENTS.md` or `CLAUDE.md` turns the LLM from a generic chatbot into a disciplined wiki maintainer.
- Valuable query answers should be filed back into the wiki.
- Periodic linting keeps the knowledge base healthy as it grows.

## Implications For This Repository

- `raw/` stores source evidence.
- `wiki/` stores maintained knowledge.
- `AGENTS.md` defines workflow rules.
- `wiki/index.md` acts as the first retrieval layer.
- `wiki/log.md` records the evolution of the knowledge base.

## Links

- Related concept: [[llm-wiki-pattern]]
- Comparison: [[llm-wiki-vs-rag]]
- Current domain: [[ai-short-drama]]

## Sources

- `llm-wiki.md`
