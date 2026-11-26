#!/bin/sh
# One command: Kolkata underwater metro (Line-Art Cutaway, Hindi). Needs the Lemo-Opuscar library (LIB), ffmpeg 7+ on PATH, edge-tts (pip).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
LIB=${LIB:-/root/lemo-opuscar}; export LIB
PY="$LIB/.venv/bin/python"; NAME=kolkata-underwater-metro-hindi
python3 "$HERE/tools/make_voice.py" >/dev/null
python3 "$HERE/tools/timeline.py" >/dev/null
cd "$LIB"
sh "$HERE/build_main.sh"
node core/render/events.mjs "$HERE"
node core/render/video.mjs "$HERE" --fps 24 --workers "${WORKERS:-4}" --q "jit=${JIT:-4}&ss=${SS:-1}" --out "$HERE/out/video.mp4"
"$PY" "$HERE/mix.py"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/$NAME.mp4" 24 0
echo "done: $HERE/$NAME.mp4"
