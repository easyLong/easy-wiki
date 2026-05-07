# Raw Sources

Place original source materials here. The LLM may read these files but should not modify original evidence.

`raw/` is the evidence layer. It should be stronger than a link list.

Recommended folders:

- `inbox/` - temporary drop zone for files before classification.
- `sources/` - durable source packets, one folder per source id.
- `batches/` - research batch manifests and capture result logs.
- `projects/` - raw project inputs and generated media references.
- `assets/` - shared raw assets that are not tied to one source packet.
- `_templates/` - raw-layer templates.

## Preferred Source Packet Structure

Use `raw/sources/` for durable source packets:

```text
raw/sources/<source-id>/
  source.md       canonical metadata, acquisition status, rights note
  captures/       raw downloaded pages, snapshots, blocked-capture pages
  assets/         images, PDFs, screenshots, transcripts, tables
  notes/          raw reading notes and extraction notes
```

At minimum, each source should have a `source.md`. A link-only packet is acceptable for initial research, but it should be treated as weak evidence until a local file, transcript, user note, or permitted snapshot is added.

Research batches should not contain source packets. They should only point to source ids:

```text
raw/batches/<batch-id>.md
```

## Acquisition Status

Use one of:

- `provided-file`
- `local-copy`
- `link-only`
- `needs-capture`
- `restricted`

The root `llm-wiki.md` is currently kept in place because it is open in the user's IDE. It is registered in the wiki as a reference source.
