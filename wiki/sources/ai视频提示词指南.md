---
type: source
title: "AI Video Prompting Guides"
date_added: 2026-05-02
status: compiled-source
review_status: reviewed
promotion_status: promoted
tags: [ai-video, prompting, sora, runway]
---

# AI Video Prompting Guides

## Summary

Official Sora and Runway guides converge on the same operational idea: video prompts work better when they specify subject, setting, action, camera, motion, lighting, pacing, and audio intent in clear, direct language.

## Useful Ideas

- Sora guidance suggests optional prompt details such as subject and setting, camera and motion, look and pacing, and audio intent.
- OpenAI's API guide recommends describing shot type, subject, action, setting, lighting, camera, and motion.
- Runway recommends clear positive phrasing and a structure such as camera movement, establishing scene, and details.
- Image-to-video prompting should focus on motion, camera work, and temporal progression because the image already provides subject, composition, lighting, and style.

## Implications For AI Short Drama

- Prompt from [[shot-list-template|shot list]] rows, not from whole-scene summaries.
- Keep casts small and timing clear for dialogue-heavy shots.
- Put stable identity and continuity constraints in reusable character/location blocks.
- Use shot-specific prompt fields for action, camera, emotion, and motion.

## Links

- [[prompt-expert]]
- [[shot-unit]]
- [[continuity-bible]]
- [[storyboard-expert]]

## Sources

- https://help.openai.com/en/articles/12460853
- https://platform.openai.com/docs/guides/video-generation/
- https://help.runwayml.com/hc/en-us/articles/30586818553107-Gen-3-Alpha-Prompting-Guide
- https://help.runwayml.com/hc/en-us/articles/48324313115155
