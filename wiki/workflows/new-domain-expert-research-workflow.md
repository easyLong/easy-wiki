---
type: workflow
title: "New Domain Expert Research Workflow"
tags: [workflow, expert-research, knowledge-bootstrap]
---

# New Domain Expert Research Workflow

## Purpose

Use this workflow when starting an unfamiliar domain. The goal is to avoid jumping directly into execution. First build a map of expert perspectives, ingest high-quality expert sources, synthesize frameworks, then plan and execute with those frameworks.

## Operating Sequence

```text
domain framing
  -> expert decomposition
  -> source search by expert role
  -> source ingest
  -> framework synthesis
  -> workflow and template creation
  -> execution plan
  -> actual work
  -> postmortem and wiki update
```

## 1. Domain Framing

Define the target:

- What are we trying to do?
- What counts as a good result?
- What is the user's current skill level?
- What constraints exist: budget, tools, timeline, platform, risk?
- What outputs must be created?

Output page:

- `wiki/domains/<domain>/<domain>-domain-overview.md`

## 2. Expert Decomposition

Break the domain into expert roles. Each role should protect a different quality dimension.

Good expert roles have:

- A clear responsibility.
- A distinct failure mode.
- A concrete artifact they produce.
- Review questions that can judge work.

Output page:

- `wiki/domains/<domain>/<domain>-expert-map.md`

## 3. Source Search By Expert Role

Search one role at a time. Prioritize:

- Official documentation.
- Expert interviews.
- Classic books or lectures.
- Professional guilds, academies, or institutions.
- Case studies and postmortems.
- Tool-specific official guides.

Avoid using low-quality listicles as primary sources.

Output pages:

- `raw/articles/<domain>-expert-research-<date>.md`
- `wiki/sources/<source-name>.md`

## 4. Source Ingest

For each source, create a source page with:

- Summary.
- Expert role coverage.
- Core claims.
- Useful frameworks.
- Implications for the domain.
- Links to pages that should be updated.

## 5. Framework Synthesis

Compile source ideas into durable pages:

- Expert pages.
- Concept pages.
- Comparison pages.
- Workflow pages.
- Template pages.

This is the main LLM Wiki step. Do not leave knowledge only in source summaries.

## 6. Execution Planning

Only after expert pages and workflows exist, create an action plan.

The plan should include:

- Steps.
- Required artifacts.
- Responsible expert lens.
- Decision checkpoints.
- Quality checks.
- Open questions.

Output page:

- `wiki/projects/<project>/<project>-action-plan.md`

## 7. Actual Work

Execute through artifacts, not vague conversation. For each work session:

- Read `wiki/index.md`.
- Read the relevant domain and expert pages.
- Produce or update concrete files.
- Log decisions.
- If a new insight appears, update the relevant wiki page.

## 8. Postmortem

After execution, write:

- What worked.
- What failed.
- Which expert framework was useful.
- Which source idea needs revision.
- What template should change.

Output page:

- `wiki/projects/<project>/<project>-postmortem.md`

## Prompt To Use

```text
I want to start a new domain: <domain>.
Use the New Domain Expert Research Workflow.
First decompose the required expert roles.
Then search high-quality sources role by role.
Ingest each source into the wiki.
Synthesize expert pages, concept pages, workflows, and templates.
Only then create an execution plan and start actual work.
```

## Links

- [[llm-wiki-pattern]]
- [[expert-role-system]]
- [[ai-short-drama-expert-map]]
