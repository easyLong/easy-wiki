---
type: comparison
tags: [llm, rag, knowledge-management]
---

# LLM Wiki vs RAG

| Dimension | LLM Wiki | RAG |
|---|---|---|
| Knowledge form | Maintained Markdown pages | Retrieved source chunks |
| Timing | Knowledge is compiled during ingest and maintenance | Knowledge is assembled at query time |
| Persistence | Answers and synthesis can become pages | Answers usually stay in chat history |
| Human role | Curate sources, guide questions, review synthesis | Upload files and ask questions |
| LLM role | Wiki maintainer and analyst | Retriever and answer generator |
| Best fit | Long-running research, production systems, evolving domains | Direct Q&A over a known document set |

## Practical Rule

Use RAG when the user needs fast lookup over documents. Use an LLM Wiki when the user is building durable understanding over time.

## Links

- [[llm-wiki-pattern]]
- [[karpathy-llm-wiki资料]]
