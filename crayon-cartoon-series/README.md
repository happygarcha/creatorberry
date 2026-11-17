# Explained Like You're 5: animated cartoon series (production system)

A code-driven 2D cartoon pipeline for vertical YouTube Shorts (1080x1920, 30 fps, H.264 + AAC). Everything is vector SVG animated by
keyframes, rendered frame by frame with headless Chromium and encoded with FFmpeg. No paid services, no stock footage, no still-image
zooms. Voices are local text-to-speech; music and sound effects are synthesised.

**Episode 1, "Why Can't We Just Print More Money?"** is finished: `episodes/episode-01/final/E01_Why_Can_t_We_Just_Print_More_Money.mp4`
(60.2 s). See `episodes/episode-01/qc_report.md` and `QC_MANUAL_NOTES.md` for what was checked and what the limits are.

## Permanent ending rules (applied automatically to every episode)

1. Finish the educational explanation first, then a memorable final joke or reaction (the episode's last scene).
2. The standard animated end card is appended automatically: `templates/end_card.json` + `tools/end_card.py` (final 6 s, mustard background,
   all three characters; Guy presses LIKE, Friend points at SHARE, Banker presses the red SUBSCRIBE button, the bell rings, everyone reacts; narrator:
   "Like, share, and subscribe for more crazy explanations!"). Episodes never list it in `episode.json`; `episode_tools.with_end_card()` adds it.
3. A next-episode teaser is optional, must never replace the card, and Episode 1 has none.
4. Text stays inside the Shorts safe areas; QC fails an episode that does not end with the end card, whose end card is not 5-7 s, whose narration lacks
   like/share/subscribe, or that shows a next-episode title.

## Layout

```
assets/
  characters/   cast.py (locked model sheet, 11 poses, 12 expressions), voices.json, model_sheet_*.png
  backgrounds/  bg.py (muted red / mustard / dusty blue / cream flat backgrounds)
  props/        props.py (wallet, coin, bread, printer, bakery, price tag, vault, money stacks, flying banknotes...)
  audio/        sfx_lib.py (31 synthesised effects) + rendered previews in sfx/
  fonts/        handwriting fonts (Caveat, Caveat Brush, Patrick Hand SC; SIL Open Font Licence)
tools/
  engine/       the SVG keyframe engine (animlib, runtime.js, cc_kit, render.py, TTS timeline, music)
  episode_tools.py   script/timeline plumbing, SFX resolution, captions + SRT, motion presets, Shorts safe areas
  make_episode.py    the pipeline (script, tts, build, stills, render, audio, mux, all)
  end_card.py        the standard animated end card (library, used by every episode)
  qc.py              automated quality checks -> qc_report.md
  make_model_sheet.py, make_thumbnail.py, contact.py, scene_sheet.py
episodes/episode-01/
  script/        episode.json (structured scene definitions) + E01_script_with_timestamps.md
  scenes/        scenes.py (the scene animation source)
  audio/         vo.wav (dialogue), final.wav (full mix), vo.json (timeline), cues.json
  subtitles/     E01_Why_Can_t_We_Just_Print_More_Money.srt
  final/         the MP4, PRIMARY_THUMBNAIL, contact sheet, YOUTUBE_UPLOAD_SHEET.md
templates/       episode_template.json, scenes_template.py, season1_roadmap.json
```

## Requirements

Python 3.11+, `playwright` (Chromium), `numpy scipy soundfile pillow sherpa-onnx`, FFmpeg, and the Kokoro TTS + Whisper models in `~/models`
(downloaded from the sherpa-onnx GitHub releases; see the `crayon-story-video` skill setup section).

## Render an episode

```bash
python3 tools/make_episode.py episodes/episode-01 all        # script, tts, build, render, audio, mux, qc
python3 tools/make_episode.py episodes/episode-01 render S3  # re-render ONE scene, then:
python3 tools/make_episode.py episodes/episode-01 mux
python3 tools/make_episode.py episodes/episode-01 stills scenes   # begin/middle/end stills of every scene
```

Dialogue is spoken first and the animation is locked to the voice timeline, so changing a line automatically retimes captions, lip sync,
sound effects and scene length.

## Make the next episode

1. Fact-check the topic first (the roadmap is in `templates/season1_roadmap.json`; every episode starts as `research_pending`).
2. Create `episodes/episode-02/script/` and `episodes/episode-02/scenes/`; copy `templates/episode_template.json` to
   `script/episode.json` and `templates/scenes_template.py` to `scenes/scenes.py`.
3. Do NOT add an end card: it is appended automatically. In `episode.json` define each scene: id, minimum length, background, music mood, characters, dialogue (`who`, `text`, `emph` for yellow caption words,
   optional `pre` lead-in silence and `say` pronunciation override), on-screen headline, and SFX anchored to words (`"at": "word:fifty"`),
   lines (`"line:1:end"`) or seconds. Keep the 7-beat retention map (the last beat is the conclusion and final joke).
4. In `scenes.py` write one `sN(c)` per scene using only `cast.char()/acting()`, `bg.flat()`, `props.*`, `headline()`, `bill_storm()`, `jitter()` etc.
   New props go into `assets/props/props.py`, new sound effects into `assets/audio/sfx_lib.py` so every later episode can use them.
5. `python3 tools/make_episode.py episodes/episode-02 all`, then `python3 tools/make_thumbnail.py episodes/episode-02 "LINE|LINE|LINE"`.

The template has been run through the whole pipeline end to end (it renders; the QC correctly flags that a one-scene stub is too short).

## Character rules

Characters exist only in `assets/characters/cast.py` (Everyday Guy, Banker, Friend; the Narrator is voice-only). Scenes call `char()` or `acting()`, and the
QC fails the build if scene source calls the engine's `person()` directly, so a character cannot drift between scenes. Voices are fixed in `voices.json`.

## Shorts safe areas

Canvas 720x1280 (rendered at 1.5x). Text lives in x 4-94% and y 10-80%; captions sit at 71.5% height; characters stand at 62%. The QC measures every
visible text element at 4 fps in the browser and reports anything outside those bounds.

## Licences

Original code and drawings; synthesised music and effects; fonts are SIL OFL (via npm `@fontsource`). The TTS model licence (Kokoro) should be checked
for your intended use before monetising; I did not verify it in this session.
