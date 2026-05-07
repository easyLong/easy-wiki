---
type: workflow
title: "Domain To Project Implementation Workflow"
created: 2026-05-03
updated: 2026-05-06
tags: [implementation, workflow, project]
---

# Domain To Project Implementation Workflow

## Purpose

Use this workflow when the wiki has enough domain understanding to begin a real project, but the project still needs controlled scope.

This workflow bridges:

```text
domain knowledge -> project plan -> MVP artifact -> validation -> wiki update
```

## Preconditions

- [[requirement-intake-workflow]] has been completed or drafted.
- The domain has at least an overview and expert map.
- Critical platform constraints are known enough to avoid obvious dead ends.
- The first project output can be described in one sentence.

## 1. Project Framing

Write:

- Problem.
- Target user.
- First output.
- Success criteria.
- Constraints.
- Non-goals.

If these are unclear, stay in requirement intake.

## 2. Expert Binding

Select only the expert roles needed for this project.

Do not load every possible role. Use the smallest expert set that protects the current risk.

## 3. MVP Definition

Define the smallest artifact that proves the key assumption.

For software, the MVP should include:

- One primary user flow.
- One visible output.
- One test path.
- One deploy or preview path.
- One review checklist.

## 4. Architecture Boundary

Decide:

- Runtime/platform.
- Language/framework.
- Local folder structure.
- External services.
- Data storage.
- Build and preview method.

Put durable choices in the project decision log.

## 5. Implementation Plan

Use [[implementation-plan-template]].

Every step should produce or change a concrete file.

## 6. Validation

Use [[mvp-validation-template]].

Validation must check:

- Does the core flow work?
- Is the result acceptable to the target user?
- Which assumption is still unproven?
- What should be built next?

## 7. Wiki Feedback

After validation, update:

- Project working notes.
- Project postmortem.
- Domain overview or framework if needed.
- Source pages if new evidence was used.
- Workflow/templates if the process changed.

## Links

- [[requirement-intake-workflow]]
- [[project-start-workflow]]
