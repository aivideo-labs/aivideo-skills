---
name: text-to-script
description: Convert novels or news articles into short-drama outlines, scene scripts, and shot lists. Use when asked to decompose long text into scenes/shots, summarize story structure, or fill short-drama schema artifacts (story-outline.md, scene-script.md, shot-list.md).
---

Category: task

# Text To Script

## Overview
Turn long-form text into production-ready scene and shot structures for short video generation.

## Workflow

1. **Classify input**
   - Novel/fiction -> outline + scene script + shot list
   - News/non-fiction -> brief summary + shot list

2. **Extract core content**
   - Identify main characters, conflict, and key beats
   - For news: identify 3-8 fact points and chronological order

3. **Produce artifacts**
   - Use the templates in `references/output-templates.md`
   - Keep scenes 15-45 seconds and shots 3-8 seconds

4. **Continuity checks**
   - Ensure character names and locations are consistent
   - Avoid introducing new characters mid-flow without setup

## Output Guidance

- Use compact, declarative sentences.
- Each scene must have a clear goal and outcome.
- Each shot must indicate subject, action, and camera intent.

## References

- `references/output-templates.md` for outline/script/shot templates and example formatting.