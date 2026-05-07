# Raw Source Packets

This folder stores source packets. A source packet is stronger than a link: it records metadata, acquisition status, local files, attachments, and evidence handling notes.

## Source Packet Structure

```text
raw/sources/<source-id>/
  source.md       canonical metadata and acquisition status
  captures/       local captures, original pages, snapshots, blocked pages
  assets/         optional images, PDFs, screenshots, transcripts, tables
  notes/          optional raw reading notes and extraction notes
```

Source ids should be stable ASCII slugs. Batches should reference source ids instead of owning source folders.

## Acquisition Status

Use one of:

- `provided-file`: the user supplied a local file.
- `local-copy`: a local copy is stored in the packet.
- `link-only`: only URL metadata is stored.
- `needs-capture`: should be captured locally later.
- `restricted`: source should not be copied; keep metadata and notes only.

## Evidence Rule

`raw/` stores evidence. Do not turn it into synthesis. Synthesis belongs in `wiki/`.

For copyrighted web pages, avoid storing full text unless the user has the right to do so or the content is openly licensed. Store metadata, short notes, and links; use `source.md` to record capture status.
