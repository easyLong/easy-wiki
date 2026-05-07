---
type: workflow
title: "Project Start Workflow"
updated: 2026-05-03
tags: [projects, workflow, execution]
---

# Project Start Workflow

## Purpose

Use this workflow when moving from research into a real project. It keeps project execution connected to the long-term wiki.

This workflow must run after [[requirement-intake-workflow]]. Do not create a project until the target output, constraints, and success criteria are clear.

## 1. Confirm Requirements

State:

- Goal.
- Concrete output.
- Domain.
- Constraints.
- Success criteria.
- Non-goals.

If these are unclear, return to [[requirement-intake-workflow]].

## 2. Select Domain

Read:

- [[domain-index]]
- The relevant domain overview, such as [[ai-short-drama-domain-overview]].
- The relevant domain framework and workflows.

## 3. Create Project Folder

Create:

```text
wiki/projects/<project-slug>/
```

Use stable ASCII slugs.

## 4. Create Project Files

Start with:

- `<project-slug>-project-overview.md`
- `<project-slug>-brief.md`
- `<project-slug>-action-plan.md`
- `<project-slug>-decisions.md`
- `<project-slug>-working-notes.md`
- `<project-slug>-review.md`
- `<project-slug>-postmortem.md`

Domain-specific projects may add files such as:

- `<project-slug>-continuity-bible.md`
- `<project-slug>-beat-outline.md`
- `<project-slug>-scene-cards.md`
- `<project-slug>-shot-list.md`
- `<project-slug>-prompt-packs.md`

## 5. Bind Expert Roles

For each project, choose the relevant expert pages. Do not load every expert by default.

For AI short drama, the default set is:

- [[script-expert]]
- [[director-expert]]
- [[storyboard-expert]]
- [[continuity-expert]]
- [[prompt-expert]]
- [[editing-expert]]
- [[sound-expert]]

## 6. Create Action Plan

The action plan should list:

- Steps.
- Output files.
- Expert lens used.
- Decision checkpoints.
- Quality checks.
- Risks and unknowns.

Use [[project-action-plan-template]].

## 7. Execute Through Artifacts

During execution, update project files rather than leaving work only in chat.

Examples:

- A story decision goes into `<project-slug>-decisions.md`.
- A changed workflow insight goes into `<project-slug>-working-notes.md`.
- A production result goes into review or postmortem.

## 8. Feed Lessons Back

At the end, update:

- Relevant domain framework.
- Relevant expert pages.
- Relevant workflow pages.
- Relevant templates.
- [[project-index]]
- `wiki/log.md`

## Links

- [[project-index]]
- [[requirement-intake-workflow]]
- [[new-domain-expert-research-workflow]]
- [[project-postmortem-template]]
