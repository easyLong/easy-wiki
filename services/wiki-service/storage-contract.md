# Storage Contract

## Page Identity

Each wiki page has a stable page id.

Default page id:

```text
filename without .md
```

Example:

```text
wiki/experts/script-expert.md -> script-expert
```

The access layer resolves page ids to paths. External clients must not assume paths are stable.

## Frontmatter

Pages should use YAML frontmatter:

```yaml
---
type: expert
title: "Script Expert"
updated: 2026-05-03
tags: [ai-short-drama, script]
---
```

Recommended fields:

- `type`
- `title`
- `status`
- `created`
- `updated`
- `tags`
- `domain`
- `project`

## Links

Internal links use Obsidian-style wikilinks:

```text
[[script-expert]]
[[shot-list-template|Shot List Template]]
```

The service should parse:

- Outbound links.
- Backlinks.
- Broken links.

## Page Types

Core types:

- `source`
- `domain`
- `project`
- `expert`
- `concept`
- `workflow`
- `template`
- `decision`
- `postmortem`
- `comparison`
- `index`
- `log`

## Catalog

The service should build a runtime catalog by scanning `wiki/**/*.md`.

Catalog record:

```json
{
  "id": "script-expert",
  "path": "wiki/experts/script-expert.md",
  "type": "expert",
  "title": "Script Expert",
  "tags": ["ai-short-drama", "script"],
  "links": ["ai-short-drama", "director-expert"],
  "updated": "2026-05-03"
}
```

The catalog should be generated, not manually edited.
