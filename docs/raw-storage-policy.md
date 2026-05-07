# Raw Storage Policy

## Rule

`raw/` stores qualified complete readable original source files only.

`raw/` is not a download cache. A source enters `raw/` only when it is strong enough to serve as durable evidence.

Current shape:

```text
raw/
  <stable-source-id>.<ext>
```

## Allowed In raw

- Complete original article text converted to readable Markdown.
- Complete plain-text transcript file.
- Complete downloaded PDF.
- Complete user-provided document.
- Complete source media file, when appropriate and intentionally stored.

## Entry Criteria

A file should enter `raw/` only if it satisfies all of these:

- It contains the actual source body, not only a landing page, index page, navigation page, or promotional shell.
- It is useful enough to support future synthesis, decisions, or implementation.
- Its provenance can be recorded in `wiki/sources/`.
- Its quality is at least medium evidence for the current task.

Weak sources should stay as `wiki/sources/` link records until a stronger original is captured.

When research finds a strong source, the agent should remind the user before archiving unless the user has already requested full ingest.

## Not Allowed In raw

- Source metadata cards.
- Reading notes.
- Summaries.
- Capture logs.
- Failed capture pages.
- Bot challenge pages.
- JavaScript shells that do not contain the article body.
- HTML snapshots or webpage wrappers.
- Temporary inbox files.
- Landing pages that do not contain the source body.
- Documentation index pages without the specific chapter content needed.
- Secondary articles that are not strong enough to preserve as durable evidence.

## Where Other Things Go

- Source metadata and summaries: `wiki/sources/`
- Synthesized knowledge: `wiki/concepts/`, `wiki/experts/`, `wiki/domains/`
- Failed capture diagnostics: sibling archive such as `C:\Code\easy-wiki-capture-attempts`
- HTML snapshots kept only for debugging: sibling archive such as `C:\Code\easy-wiki-capture-attempts`
- Architecture and policy: `docs/`

## Naming

Use stable, readable filenames:

```text
raw/karpathy-llm-wiki-原文.md
raw/微信-llm-wiki内容创作3系统-原文.md
raw/walter-murch-六法则-原文.md
```

If a source cannot be captured as a complete original, do not put a placeholder in `raw/`.
If the only available local capture is HTML, convert the article body to readable Markdown before placing it in `raw/`.

