---
type: index
updated: 2026-05-07
---

# Wiki Index

## Scope

This repository is now intentionally narrowed to the `easy-wiki` core:

- The markdown wiki database under `wiki/`
- The evidence store under `raw/`
- The access layer under `services/wiki-service/`
- The seed knowledge area for AI short drama

Non-core app experiments have been moved to `C:\Code\easy-wiki-apps`.
Non-core domain expansion assets have been moved to `C:\Code\easy-wiki-domain-expansion`.

## Access Layer

- Overall architecture: `docs/overall-architecture.md`
- Architecture: `docs/core-knowledge-architecture.md`
- Function boundaries: `docs/function-boundaries.md`
- Governance layer: `docs/governance-layer.md`
- Raw storage policy: `docs/raw-storage-policy.md`
- Service contract: `services/wiki-service/README.md`
- Governance service: `services/governance/README.md`
- Storage contract: `services/wiki-service/storage-contract.md`
- HTTP API: `services/wiki-service/api-spec.md`
- MCP tools: `services/wiki-service/mcp-tools.md`
- Write policy: `services/wiki-service/write-policy.md`

External services should use MCP/API through `services/wiki-service/`. Direct file paths are internal implementation details.

## Primary Entry Points

- [[ai-short-drama-cn|AI 短剧知识地图]] - 中文总入口。
- [[ai-short-drama-expert-system-cn|AI 短剧专家系统]] - 专家协作方法。
- [[ai-short-drama-implementation-cn|AI 短剧实施手册]] - 从创意到成片的落地步骤。
- [[ai-short-drama-expert-map|AI Short Drama Expert Map]] - 角色拆分与执行顺序。

## Long-Term Structure

- [[domain-index|Domain Index]] - Long-lived knowledge areas.
- [[project-index|Project Index]] - Project status inside the core repo.
- [[decision-index|Decision Index]] - Durable wiki/domain decisions.
- [[postmortem-index|Postmortem Index]] - Lessons learned from completed work.

## Domains

- [[ai-short-drama-domain-overview|AI Short Drama Domain]] - Durable knowledge area for AI-assisted short drama production.
- [[ai-short-drama|AI Short Drama]] - Legacy topic-style entry for AI short drama production concepts.
- [[ai-short-drama-domain-sources|AI Short Drama Domain Sources]] - Source map for AI short drama expert research.
- [[ai-short-drama-domain-framework|AI Short Drama Domain Framework]] - Reusable production framework and decision hierarchy.
- [[ai-short-drama-domain-workflows|AI Short Drama Domain Workflows]] - Domain-specific workflow map.
- [[ai-short-drama-domain-projects|AI Short Drama Domain Projects]] - AI short drama project tracker.
- [[ai-short-drama-domain-open-questions|AI Short Drama Domain Open Questions]] - Research and method questions.

## Sources

- [[karpathy-llm-wiki资料|Karpathy - LLM Wiki]] - Persistent wiki maintenance pattern.
- [[微信-llm-wiki内容创作3系统|WeChat Case Study - LLM Wiki 内容创作3.0系统]] - Practical LLM wiki operating example.
- [[pixar故事与电影语法|Pixar / Khan Academy - The Art of Storytelling]] - Story, visual language, and film grammar.
- [[walter-murch-六法则|Walter Murch - Rule of Six]] - Editing decision hierarchy.
- [[youtube观众留存|YouTube Help - Audience Retention]] - Official retention signals for intros, spikes, and dips.
- [[randy-thom-为声音设计电影|Randy Thom - Designing A Movie For Sound]] - Sound as story design craft.
- [[dga导演创作访谈|DGA Interviews - Directing Craft]] - Directing ideas on prep, staging, and motivation.
- [[ai视频提示词指南|AI Video Prompting Guides]] - Sora and Runway prompt guidance.

## Concepts

- [[llm-wiki-pattern|LLM Wiki Pattern]] - Persistent knowledge base maintained by an LLM.
- [[knowledge-compile-pipeline|Knowledge Compile Pipeline]] - Staged process for turning raw sources into durable wiki knowledge.
- [[ai-short-drama-pipeline|AI Short Drama Pipeline]] - End-to-end production pipeline from premise to delivery.
- [[expert-role-system|Expert Role System]] - Multi-role thinking model for production decisions.
- [[shot-unit|Shot Unit]] - The minimum controllable unit for script, image, video, edit, and QA.
- [[continuity-bible|Continuity Bible]] - Control document for character, world, style, and story consistency.

## Experts

- [[script-expert|Script Expert]] - Designs hooks, conflict, beats, and payoffs.
- [[storyboard-expert|Storyboard Expert]] - Converts scenes into shots with visual intent and continuity.
- [[director-expert|Director Expert]] - Owns performance, staging, tone, and unified interpretation.
- [[cinematography-expert|Cinematography Expert]] - Controls composition, lens logic, lighting, and camera movement.
- [[editing-expert|Editing Expert]] - Shapes rhythm, retention, transitions, and emotional timing.
- [[sound-expert|Sound Expert]] - Designs dialogue clarity, music, ambience, and audio cues.
- [[continuity-expert|Continuity Expert]] - Protects character, prop, costume, location, and timeline consistency.
- [[prompt-expert|Prompt Expert]] - Translates creative intent into repeatable AI generation prompts.

## Workflows

- [[requirement-intake-workflow|Requirement Intake Workflow]] - Universal entry gate before search or execution.
- [[new-domain-expert-research-workflow|New Domain Expert Research Workflow]] - Bootstrap flow for unfamiliar domains.
- [[source-compile-workflow|Source Compile Workflow]] - Raw-to-source compilation workflow.
- [[project-start-workflow|Project Start Workflow]] - Project setup inside an existing domain.
- [[domain-to-project-implementation-workflow|Domain To Project Implementation Workflow]] - Domain understanding to MVP execution.
- [[ai-short-drama-production-workflow|AI Short Drama Production Workflow]] - Shot-centered AI short drama workflow.

## Templates

- [[scene-card-template|Scene Card Template]] - Reusable scene planning format.
- [[shot-list-template|Shot List Template]] - Reusable shot-level production table.
- [[review-checklist-template|Review Checklist Template]] - QA checklist for generated scenes and edits.
- [[project-overview-template|Project Overview Template]] - Reusable project overview format.
- [[project-brief-template|Project Brief Template]] - Reusable project brief format.
- [[project-action-plan-template|Project Action Plan Template]] - Reusable execution plan format.
- [[project-decisions-template|Project Decisions Template]] - Reusable decision log format.
- [[project-working-notes-template|Project Working Notes Template]] - Reusable working notes format.
- [[project-postmortem-template|Project Postmortem Template]] - Reusable project postmortem format.
- [[source-candidate-template|Source Candidate Template]] - Source quality and archive decision template.
- [[implementation-plan-template|Implementation Plan Template]] - Reusable plan for scoped implementation.
- [[mvp-validation-template|MVP Validation Template]] - Reusable validation format for MVP assumptions.

## Comparisons

- [[llm-wiki-vs-rag|LLM Wiki vs RAG]] - Persistent wiki maintenance versus query-time retrieval.
