#!/bin/sh
# One command: AC water, "don't drink it" (Line-Art Cutaway, 60 s). Needs the Lemo-Opuscar library (LIB), ffmpeg 7+ on PATH, Kokoro voice tier.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
LIB=${LIB:-/root/lemo-opuscar}; export LIB
PY="$LIB/.venv/bin/python"; NAME=ac-water-dont-drink-it
cd "$LIB"
[ -f "$HERE/voice/v1.wav" ] || { "$PY" core/tts/tts.py "$HERE/voice/lines.json" "$HERE/voice"; "$PY" core/tts/asr_check.py "$HERE/voice/lines.json" "$HERE/voice"; }
python3 "$HERE/tools/timeline.py" >/dev/null
sh "$HERE/build_main.sh"
node core/render/events.mjs "$HERE"
node core/render/video.mjs "$HERE" --fps 24 --workers "${WORKERS:-4}" --q "jit=${JIT:-4}&ss=${SS:-1}" --out "$HERE/out/video.mp4"
"$PY" "$HERE/mix.py"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/$NAME.mp4" 24 0
"$PY" core/render/srt.py "$HERE/cues.json" "$HERE/subtitles_en.srt"
echo "done: $HERE/$NAME.mp4"
