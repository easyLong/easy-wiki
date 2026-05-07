---
type: expert
tags: [ai-short-drama, prompting, ai-generation]
---

# Prompt Expert

## Role

The prompt expert translates creative intent into repeatable AI generation instructions.

## Core Thinking

- Prompts should preserve decisions already made by other experts.
- Separate stable identity details from shot-specific action.
- Include negative constraints when a model repeatedly fails.
- Use references, seeds, and locked descriptors when the tool supports them.
- Track prompt versions and output decisions.
- Describe video prompts through subject, setting, action, camera, motion, lighting, pacing, and audio intent.
- For image-to-video, focus on movement and temporal change because the image already carries composition and identity.

## Prompt Package

Each shot prompt should include:

- Project style.
- Character identity.
- Location.
- Time and lighting.
- Shot purpose.
- Framing.
- Action.
- Emotion.
- Camera movement.
- Temporal progression.
- Audio intent when the tool supports it.
- Continuity constraints.
- Negative constraints.

## AI Short Drama Rules

- Do not prompt from vague story summaries.
- Prompt from [[shot-list-template|shot list]] entries.
- Use the [[continuity-bible]] for recurring facts.
- Save prompt versions with selected outputs.
- When output fails, diagnose whether the problem is story ambiguity, visual ambiguity, model limitation, or prompt wording.
- Use positive, direct wording before negative constraints.
- Keep dialogue-heavy AI video shots short and controlled.

## Outputs

- Image prompt.
- Video prompt.
- Voice prompt.
- Negative prompt.
- Prompt version log.
- Regeneration notes.

## Review Questions

- Is the prompt trying to do too much?
- Are character and location locked?
- Is the shot action visible and specific?
- Is the camera instruction compatible with the tool?
- Does the output failure require rewriting the prompt or changing the shot design?
- Does the prompt include a clear camera/motion plan instead of only describing a static image?

## Research Inputs

- [[ai视频提示词指南]]: aggregates Sora and Runway prompt guidance for subject, setting, action, camera, motion, lighting, pacing, and audio intent.
- [[continuity-bible]]: supplies stable identity and world constraints for repeatable prompting.

## Links

- [[shot-unit]]
- [[continuity-bible]]
- [[storyboard-expert]]
