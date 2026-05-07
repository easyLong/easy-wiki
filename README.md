# Easy Wiki

[中文](README.zh-CN.md) | English

Easy Wiki is a long-lived markdown knowledge base maintained with LLM help.

Its purpose is to turn qualified original evidence into durable, reusable knowledge that can support future agents, applications, and concrete projects.

This repository is the core wiki platform. It is not the Studio app and not a media-production application by itself.

## Repository Shape

```text
raw/                    qualified original evidence
wiki/                   markdown knowledge database
services/wiki-service/  HTTP/MCP access layer
services/governance/    execution governance layer
docs/                   architecture and policy documents
AGENTS.md               operating rules for future agents
```

Sibling projects currently include:

```text
C:\Code\easy-wiki-studio
```

`easy-wiki-studio` consumes this repository's wiki, service, and governance capabilities to build short-drama production assets.

## Core Ideas

- `raw/` stores qualified complete originals only.
- `wiki/` stores compiled knowledge, expert lenses, workflows, templates, domains, projects, decisions, and postmortems.
- `services/wiki-service/` exposes the wiki through stable page ids, search, HTTP, and MCP.
- `services/governance/` helps external apps decide which source, derived artifacts, experts, workflows, and templates each execution step must use.
- External consumers should use service and governance contracts instead of hard-coding file paths.

## Run The Wiki Service

From the repository root:

```powershell
python services/wiki-service/api_server.py
```

Useful endpoints:

```text
GET  http://127.0.0.1:8765/health
GET  http://127.0.0.1:8765/pages
GET  http://127.0.0.1:8765/pages/script-expert
GET  http://127.0.0.1:8765/search?q=shot%20unit
GET  http://127.0.0.1:8765/healthcheck
POST http://127.0.0.1:8765/compile-source
POST http://127.0.0.1:8765/compile-missing-sources
POST http://127.0.0.1:8765/projects
```

## Run Tests

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## Important Documents

- [Overall architecture](docs/overall-architecture.md)
- [Function boundaries](docs/function-boundaries.md)
- [Governance layer](docs/governance-layer.md)
- [Raw storage policy](docs/raw-storage-policy.md)
- [Wiki service README](services/wiki-service/README.md)
- [Governance service README](services/governance/README.md)

## Working Rule

Easy Wiki provides knowledge and platform contracts. Domain apps perform the actual work.

For example, short-drama production lives in `easy-wiki-studio`, while the reusable expert pages, workflow pages, access layer, and governance layer live here.
