## Video uploads
- For every finished video, deliver the FULL PACKAGE AT ONCE in a single reply, without being asked: the final video file, exactly ONE primary thumbnail (not a set of options),
  and the paste-ready title, description, hashtags, hidden tags and pinned comment, all written out in the reply so they can be copied. Do not split these across messages.

## Cartoon series endings (permanent rules, apply automatically; never ask again)
- Every episode: finish the educational explanation, then a memorable final joke or funny reaction, then the standard animated end card.
- The end card is appended automatically by `crayon-cartoon-series/tools/make_episode.py` (templates/end_card.json + tools/end_card.py): final ~6 s, mustard background,
  Guy / Friend / Banker, big animated LIKE, SHARE, SUBSCRIBE (+ bell) and "FOR MORE FUN EXPLANATIONS!", narrator invites viewers to like, share and subscribe.
- Same layout, colours, characters and animation style in every episode. Never a generic YouTube end-screen template or a static image.
- Do not show or promise a next-episode title in the video or its upload text. An optional teaser is allowed only in the episode body and must never replace the end card.
- Keep all text inside the YouTube Shorts safe areas. Do not rebuild approved scenes unnecessarily; re-render only what changed.

## Cartoon series audio and pacing (permanent rules, apply from the next video onward; never ask again)
- Speech must be clear and easy to follow: keep the voices at NATURAL speed 1.0 (slowing the model down sounded sloppy; do not stretch them, assets/characters/voices.json) and get the slow, easy pace from longer pauses:
  minimum 0.5 s inside a sentence and 1.0 s after a sentence. Never speed the voices up to make a video shorter, and never cut facts or script content to save time: keep ALL the researched information. The video simply runs as long as the content needs
  (YouTube Shorts allow up to 3 minutes; stay at or under 180 s, and tell the user the runtime in the delivery message).
- Background music must never mask speech: it is mixed at a lower level and ducked hard under every voice (assets/audio/mix_config.json), sound effects are ducked under the voice too.
- tools/qc.py checks the speech pace (limit 175 words per minute while speaking) and that the voice is at least 18 dB above the music while speaking; fix and re-mix if it warns.
- If a script is long, keep it and still keep a new visual development at least every 8 s; split into two parts only if it would exceed 180 s, and ask first in that case.
- Episodes 1 and 2 were rendered before these rules and keep their original faster pacing unless the user asks for a re-render.

## On-screen source credits and language (permanent rules, apply to every video; never ask again)
- NO source text on screen, ever (not in a corner, not small): sources go only into the upload description and research notes. `note_text()` in scene files is a no-op.
- The Hindi voice must sound natural: use Indic Parler-TTS (see `tools/engine/hindi_tts.py`); Piper hi_IN was rejected by the user as not good.
- Reply to the user in the language they wrote their request in. When a video is requested in Hindi, everything on screen (headline, labels, captions, source credit, end card) is Devanagari, the narration is spoken Hindi, and the upload sheet is in Hindi. Hindi tools: `tools/engine/hindi_tts.py` (Piper hi_IN voices), set `"lang": "hi"` in episode.json.
- A standalone video (no episode number) uses `videos/<slug>/` and `"slug"` in episode.json; a requested exact runtime (e.g. 60.000 s) is hit by tuning the last scene's `min`.
