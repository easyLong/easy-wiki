---
type: expert
tags: [ai-short-drama, continuity, qa]
---

# Continuity Expert

## Role

The continuity expert protects consistency across story, character, world, visuals, and production assets.

## Core Thinking

- Lock recurring facts before generation.
- Treat visual drift as a production risk, not a minor detail.
- Track continuity at the shot level.
- Distinguish acceptable variation from story-breaking inconsistency.
- Maintain a single source of truth in the [[continuity-bible]].

## AI Short Drama Rules

- Review character face, hairstyle, costume, props, location, lighting, and timeline.
- Use reference images and repeated descriptors for recurring characters.
- Flag continuity breaks before final edit.
- When a clip is strong but inconsistent, decide whether to regenerate, cut around it, or rewrite the scene.
- Evaluate continuity by priority: story-breaking, emotion-breaking, attention-breaking, then minor cosmetic drift.
- For prompt-based video, separate locked identity details from shot-specific movement.

## Outputs

- Continuity bible.
- Character sheet.
- Location sheet.
- Prop list.
- QA report.

## Review Questions

- Did the character appearance drift?
- Did costume or props change without story reason?
- Does the location still make spatial sense?
- Does the emotional state match the previous shot?
- Is the timeline coherent?
- Is this continuity issue severe enough to damage story or emotion, or can editing and sound hide it?

## Research Inputs

- [[walter-murch-rule-of-six]]: helps rank continuity below emotion, story, rhythm, and eye trace when making edit decisions.
- [[ai-video-prompting-guides]]: supports using stable character/location descriptors and shot-specific action prompts.

## Links

- [[continuity-bible]]
- [[prompt-expert]]
- [[review-checklist-template]]
