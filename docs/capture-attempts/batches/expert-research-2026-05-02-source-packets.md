# Expert Research Batch - 2026-05-02

This batch records the first AI short drama expert research pass. Source packets now live in `raw/sources/<source-id>/`; this file is only a batch manifest.

The first capture pass downloaded local HTML for sources that allowed direct capture. Some sources are still `needs-capture` or `restricted` because direct download returned a JavaScript shell, timeout, or bot challenge instead of article content. Future ingest passes should either:

- Save permitted local copies as `original.*`.
- Add user-provided PDFs, transcripts, or notes.
- Mark sources as `restricted` when full local capture is not appropriate.

## Packets

- `pixar-khan-storytelling` - needs-capture; current file is a JS shell.
- `pixar-in-a-box` - local-copy.
- `walter-murch-rule-of-six` - local-copy, including supporting page.
- `youtube-audience-retention` - needs-capture; direct download timed out.
- `randy-thom-designing-for-sound` - local-copy.
- `dga-dan-attias-interview` - restricted; direct capture blocked.
- `openai-sora-help` - needs-capture; direct capture returned JS/refresh page.
- `openai-video-generation-api` - needs-capture; direct capture returned Cloudflare challenge.
- `runway-gen3-prompting` - restricted; direct capture blocked.
- `runway-image-to-video-prompting` - restricted; direct capture blocked.
