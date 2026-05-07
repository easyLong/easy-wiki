---
type: workflow
title: "New Domain Expert Research Workflow"
tags: [workflow, expert-research, knowledge-bootstrap]
---

# New Domain Expert Research Workflow

## Purpose

Use this workflow when starting an unfamiliar domain. The goal is to avoid jumping directly into execution. First build a map of expert perspectives, ingest high-quality expert sources, synthesize frameworks, then plan and execute with those frameworks.

This workflow must run after [[requirement-intake-workflow]]. Requirement intake is the precondition for exploration, planning, and search.

## Operating Sequence

```text
exploration
  -> research plan
  -> domain framing
  -> expert decomposition
  -> source search by expert role
  -> source candidate review
  -> archive reminder
  -> source ingest / raw archive
  -> framework synthesis
  -> workflow and template creation
  -> execution plan
  -> actual work
  -> postmortem and wiki update
```

## 1. Exploration

Before searching, clarify the problem.

Ask:

- What does the user want to make or learn?
- Is this a one-off task, a reusable domain, or a product direction?
- What does success look like?
- What is the minimum useful output?
- What does the user already know?
- What constraints exist: platform, budget, tools, timeline, risk, language?

Output:

- A short exploration note inside the domain overview.
- Open questions that should guide search.

Do not jump directly to source collection before this is clear.

## 2. Research Plan

Plan the search before searching.

Define:

- Expert roles to investigate.
- Source types needed for each role.
- Search order.
- Evidence quality bar.
- Which sources would be strong enough for `raw/`.
- Which sources should remain link-only.

Output page:

- `wiki/domains/<domain>/<domain>-domain-sources.md`

## 3. Domain Framing

Define the target:

- What are we trying to do?
- What counts as a good result?
- What is the user's current skill level?
- What constraints exist: budget, tools, timeline, platform, risk?
- What outputs must be created?

Output page:

- `wiki/domains/<domain>/<domain>-domain-overview.md`

## 4. Expert Decomposition

Break the domain into expert roles. Each role should protect a different quality dimension.

Good expert roles have:

- A clear responsibility.
- A distinct failure mode.
- A concrete artifact they produce.
- Review questions that can judge work.

Output page:

- `wiki/domains/<domain>/<domain>-expert-map.md`

## 5. Source Search By Expert Role

Search one role at a time. Prioritize:

- Official documentation.
- Expert interviews.
- Classic books or lectures.
- Professional guilds, academies, or institutions.
- Case studies and postmortems.
- Tool-specific official guides.

Avoid using low-quality listicles as primary sources.

Output pages:

- `wiki/sources/<source-name>.md`

At this stage, do not automatically put search results into `raw/`.

## 6. Source Candidate Review

Every found source should first be classified.

Use these fields on the source page:

```yaml
acquisition_status: link-only | candidate-for-raw | local-copy | restricted
source_quality: official-doc | official-index | primary-article | expert-interview | book-landing-page | secondary | weak
evidence_strength: strong | medium | weak
archive_recommendation: archive | do-not-archive | ask-user
```

Archive only when the source has:

- Actual body content, not just a landing page or index.
- Medium or strong evidence for the current domain.
- Clear provenance.
- Reuse value for future synthesis, planning, or implementation.

Weak sources remain in `wiki/sources/` as link records.

## 7. Archive Reminder

When a source looks important enough to preserve, explicitly remind the user before archiving:

```text
I found a strong source: <title>.
It looks worth preserving in raw because <reason>.
Should I archive the readable original into raw/ and compile it?
```

If the user already asked to fully ingest/archive sources, proceed under the raw entry criteria.

## 8. Source Ingest

For each source, create a source page with:

- Summary.
- Expert role coverage.
- Core claims.
- Useful frameworks.
- Implications for the domain.
- Links to pages that should be updated.

If the source is approved for archive, use [[source-compile-workflow]] after placing the qualified original into `raw/`.

## 9. Framework Synthesis

Compile source ideas into durable pages:

- Expert pages.
- Concept pages.
- Comparison pages.
- Workflow pages.
- Template pages.

This is the main LLM Wiki step. Do not leave knowledge only in source summaries.

## 10. Execution Planning

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

## 11. Actual Work

Execute through artifacts, not vague conversation. For each work session:

- Read `wiki/index.md`.
- Read the relevant domain and expert pages.
- Produce or update concrete files.
- Log decisions.
- If a new insight appears, update the relevant wiki page.

## 12. Postmortem

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
Classify sources before archiving.
When you find an important source worth preserving, remind me and ask whether to archive it into raw/.
Ingest useful sources into the wiki.
Synthesize expert pages, concept pages, workflows, and templates.
Only then create an execution plan and start actual work.
```

## Links

- [[llm-wiki-pattern]]
- [[expert-role-system]]
- [[ai-short-drama-expert-map]]

