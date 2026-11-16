---
name: animate
description: Turn a one-sentence idea into a painterly cinematic short film package: story, character/location/object sheet image prompts, and one timestamped master video prompt with a style lock. Use when the user runs /animate or asks for an animated short film from an idea. Writes prompts only; never generates images or video.
---

# Animate

Input: one sentence idea (`$ARGUMENTS`). If empty, ask for one.
Output: a prompt package saved to `prompts/<slug>.md`. Never generate images or video yourself; the user does that in their own tools.

## Steps

1. **Story.** Expand the idea into a ~15 second-per-beat arc: setup, escalation, turn, resolution. One protagonist, one goal, one clock (a deadline or obstacle). Max 3 locations, 1-2 key objects. Give a title and a 3-sentence logline.

2. **Style lock.** Write one paragraph, reused verbatim in every prompt: painterly look (brush texture, palette of 4-5 named colors, lighting logic), lens/camera language, aspect ratio (default 16:9), frame rate feel, and a negative list (no text, no logos, no photoreal skin, no style drift).

3. **Reference sheets.** For each character, location and key object, write a standalone image prompt for a sheet:
   - Character: turnaround (front, 3/4, side, back), face close-up, costume details, neutral pose, plain background.
   - Location: wide establishing plate plus 2 angle variants, time of day fixed.
   - Object: clean multi-angle plate.
   Each prompt starts with the style lock and gives a stable ID (`CHAR-1`, `LOC-1`, `OBJ-1`) and fixed identifying traits (age, build, hair, clothing colors) so they can be repeated word for word later.

4. **Master video prompt.** One prompt, 10-15 seconds unless the user asks otherwise, structured as:
   - Header: style lock, reference IDs the user will attach, aspect ratio, duration.
   - Timestamped shots (`0:00-0:03`, ...), each with: camera move, subject action, environment, light, sound/ambience cue.
   - Continuity rules: same costume/props/lighting across shots, no cuts to unseen locations.
   - Negative list.

5. **Save and report.** Write everything to `prompts/<slug>.md` with sections: Story, Style Lock, Image Prompts, Master Video Prompt, Generation Checklist (generate sheets into `references/`, run clip into `renders/`, accept into `final/`). In chat, show a short summary and the file path, not the full text.

## Rules

- Keep prompts self-contained; the image/video tool sees nothing else.
- Concrete visual language over abstract mood words.
- No dialogue-dependent plot; film must read silent.
- Do not name real artists, brands or copyrighted characters.
