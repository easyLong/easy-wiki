---
type: index
updated: 2026-05-03
---

# Wiki Index

## Access Layer

- Architecture: `docs/core-knowledge-architecture.md`
- Function boundaries: `docs/function-boundaries.md`
- Service contract: `services/wiki-service/README.md`
- Storage contract: `services/wiki-service/storage-contract.md`
- HTTP API: `services/wiki-service/api-spec.md`
- MCP tools: `services/wiki-service/mcp-tools.md`
- Write policy: `services/wiki-service/write-policy.md`

External services should use MCP/API through `services/wiki-service/`. Direct file paths are internal implementation details.

## Primary Domain Entry Points

- [[ai-short-drama-cn|AI 短剧知识地图]] - 面向 AI 短剧制作的中文总入口，包含流程、专家系统和可执行产物。
- [[ai-short-drama-expert-system-cn|AI 短剧专家系统]] - 分镜、导演、剪辑、声音、连续性、提示词等专家的协作方法。
- [[ai-short-drama-implementation-cn|AI 短剧实施手册]] - 从创意到成片的落地步骤和检查点。
- [[ai-short-drama-expert-map|AI Short Drama Expert Map]] - AI 短剧的专家拆分、搜索顺序和执行角色图。

## Long-Term Structure

- [[domain-index|Domain Index]] - Long-lived knowledge areas.
- [[project-index|Project Index]] - Concrete execution projects.
- [[decision-index|Decision Index]] - Durable wiki/domain decisions.
- [[postmortem-index|Postmortem Index]] - Lessons learned from completed work.

## Domains

- [[ai-short-drama-domain-overview|AI Short Drama Domain]] - Durable knowledge area for AI-assisted short drama production.
- [[ai-short-drama-domain-sources|AI Short Drama Domain Sources]] - Source map for AI short drama expert research.
- [[ai-short-drama-domain-framework|AI Short Drama Domain Framework]] - Reusable production framework and decision hierarchy.
- [[ai-short-drama-domain-workflows|AI Short Drama Domain Workflows]] - Domain-specific workflow map.
- [[ai-short-drama-domain-projects|AI Short Drama Domain Projects]] - AI short drama project tracker.
- [[ai-short-drama-domain-open-questions|AI Short Drama Domain Open Questions]] - Research and method questions.

## Sources

- [[karpathy-llm-wiki|Karpathy - LLM Wiki]] - Source summary of the LLM-maintained persistent wiki pattern.
- [[pixar-storytelling-film-grammar|Pixar / Khan Academy - The Art of Storytelling]] - Story, visual language, film grammar, storyboarding, feedback, and storyreels.
- [[walter-murch-rule-of-six|Walter Murch - Rule of Six]] - Editing hierarchy for choosing cuts.
- [[youtube-audience-retention|YouTube Help - Audience Retention]] - Official retention signals for intros, spikes, dips, and top moments.
- [[randy-thom-designing-for-sound|Randy Thom - Designing A Movie For Sound]] - Sound as a story-design craft from script through post.
- [[dga-directing-craft|DGA Interviews - Directing Craft]] - Directing ideas on motivation, staging, prep, and holding the whole story.
- [[ai-video-prompting-guides|AI Video Prompting Guides]] - Sora and Runway guidance for video prompts.

## Concepts

- [[llm-wiki-pattern|LLM Wiki Pattern]] - Persistent knowledge base maintained by an LLM.
- [[ai-short-drama-pipeline|AI Short Drama Pipeline]] - End-to-end production pipeline from premise to delivery.
- [[expert-role-system|Expert Role System]] - A multi-role thinking model for production decisions.
- [[shot-unit|Shot Unit]] - The minimum controllable unit for script, image, video, edit, and QA.
- [[continuity-bible|Continuity Bible]] - A control document for character, world, style, and story consistency.

## Experts

- [[script-expert|Script Expert]] - Designs hooks, conflict, beats, and emotional payoffs.
- [[storyboard-expert|Storyboard Expert]] - Converts scenes into shots with visual intent and continuity.
- [[director-expert|Director Expert]] - Owns performance, staging, tone, and unified interpretation.
- [[cinematography-expert|Cinematography Expert]] - Controls composition, lens logic, lighting, and camera movement.
- [[editing-expert|Editing Expert]] - Shapes rhythm, retention, transitions, and emotional timing.
- [[sound-expert|Sound Expert]] - Designs dialogue clarity, music, ambience, and audio cues.
- [[continuity-expert|Continuity Expert]] - Protects character, prop, costume, location, and timeline consistency.
- [[prompt-expert|Prompt Expert]] - Translates creative intent into repeatable AI generation prompts.

## Workflows

- [[new-domain-expert-research-workflow|New Domain Expert Research Workflow]] - Workflow for starting an unfamiliar domain by decomposing experts, ingesting sources, synthesizing frameworks, and then executing.
- [[project-start-workflow|Project Start Workflow]] - Workflow for starting concrete execution inside an existing domain.

## Templates

### AI Short Drama Domain Templates

- [[scene-card-template|Scene Card Template]] - Reusable scene planning format.
- [[shot-list-template|Shot List Template]] - Reusable shot-level production table.
- [[review-checklist-template|Review Checklist Template]] - QA checklist for generated scenes and edits.

### Project Templates

- [[project-overview-template|Project Overview Template]] - Reusable project overview format.
- [[project-brief-template|Project Brief Template]] - Reusable project brief format.
- [[project-action-plan-template|Project Action Plan Template]] - Reusable execution plan format.
- [[project-decisions-template|Project Decisions Template]] - Reusable decision log format.
- [[project-working-notes-template|Project Working Notes Template]] - Reusable working notes format.
- [[project-postmortem-template|Project Postmortem Template]] - Reusable project postmortem format.

## Comparisons

- [[llm-wiki-vs-rag|LLM Wiki vs RAG]] - Comparison of persistent wiki maintenance and query-time retrieval.
