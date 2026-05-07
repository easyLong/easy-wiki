---
type: workflow
title: "Requirement Intake Workflow"
created: 2026-05-03
updated: 2026-05-03
tags: [workflow, requirements, intake]
---

# Requirement Intake Workflow

## Purpose

All work starts with requirement intake.

Do not search, plan, archive sources, create projects, or implement until the user's goal is clear enough to choose the right workflow.

Requirement intake is the human deliberation phase. The agent should help the user repeatedly clarify and sharpen the requirement until the user confirms a named version. After that, expert workflows can run normally.

## Trigger

Use this workflow before:

- Starting a new domain.
- Starting a project.
- Searching sources.
- Ingesting sources.
- Writing code.
- Creating templates or expert pages.
- Making architecture changes.

## Intake Questions

Clarify only what is needed to proceed.

Core questions:

- What are we trying to achieve?
- What concrete output should exist after this step?
- Is this exploration, planning, research, implementation, review, or maintenance?
- Who is the user/audience?
- What constraints exist: platform, tools, budget, timeline, language, quality bar, risk?
- What should not be done?
- What decisions are already fixed?
- What is still unknown?

## Human Deliberation Gate

For any new product, game, app, workflow, or version plan, requirement intake is not complete until the user confirms a named requirement version.

Do this before expert research, deep planning, or implementation:

1. Write a requirement version, such as `v0 需求理解`.
2. List what is included.
3. List what is excluded.
4. List default assumptions.
5. List unresolved decisions.
6. Ask the user to challenge, revise, or confirm this version.
7. If the user changes anything, update the requirement version and ask again.

Do not silently treat agent assumptions as confirmed.

Once the user confirms the requirement version, downstream work can follow expert workflows without asking for confirmation at every small step. Ask again only when:

- New information changes the confirmed requirement.
- A major tradeoff appears.
- A choice belongs to the user, such as product direction, monetization, publishing, or visual style.
- The user explicitly asks to revisit requirements.

Example confirmation prompt:

```text
这是我理解的 v0 版本：
- ...

请推敲一下：这个版本是否可以进入专家流程？
如果不可以，请指出要改的地方。
```

## Requirement Clarity Levels

### Level 0: Unclear

The request is ambiguous or missing the target output.

Action:

- Ask focused questions.
- Do not search or implement yet.

### Level 1: Exploratory

The user wants to understand or start an unfamiliar area.

Action:

- Use [[new-domain-expert-research-workflow]].
- Explore and plan before searching.

### Level 2: Research Ready

The target is clear enough to search, but not enough to execute.

Action:

- Create or update the domain source map.
- Search by expert role.
- Classify source candidates.
- Remind the user before archiving strong sources into `raw/`.

### Level 3: Execution Ready

The target output, constraints, and success criteria are clear.

Action:

- Confirm the named requirement version with the user first.
- Use [[project-start-workflow]] when it is concrete project work.
- Create or update project artifacts.
- Execute through files, not only chat.

After confirmation:

- Continue through expert research, planning, implementation, and validation.
- Do not ask for confirmation on every internal workflow step.
- Escalate only when a downstream decision changes requirement scope or needs user ownership.

### Level 4: Maintenance Ready

The user is asking to update, lint, clean, or refactor the existing wiki.

Action:

- Read `wiki/index.md`.
- Read the relevant policy/workflow pages.
- Make scoped changes.
- Update `wiki/index.md` and `wiki/log.md` when needed.

## Output

Before moving on, state the interpreted requirement:

```text
Requirement understood:
- Goal:
- Output:
- Current mode:
- Constraints:
- Requirement version:
- Confirmation status:
- Next workflow:
```

For small obvious maintenance requests, this can be a one-sentence internal check. For new domains or ambiguous tasks, make it explicit in the response.

## Links

- [[new-domain-expert-research-workflow]]
- [[project-start-workflow]]
- [[source-compile-workflow]]
