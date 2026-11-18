# Zapzapper Dark Files - 60 s test (project)
Run order: `python3 make_voices.py` (TTS per line) -> `python3 build_zz.py` (zz.html: art + rig + choreography) -> events (see make_audio) -> `python3 make_audio.py` -> render 4 chunks with `../tools/engine/render.py zz.html frames/parts/pN.mp4 t0 t1` -> `python3 finalize.py` -> `python3 qc_zz.py`.
Editable files: `zz_anim.js` (rig, IK, choreography, camera), `zz_art.py` (characters), `zz_sets.py` (sets/props), `script.json`, `make_audio.py`. SVG assets in `assets/svg/`. Zapzapper logo: not supplied, omitted.
