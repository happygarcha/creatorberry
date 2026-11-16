#!/usr/bin/env bash
# Full rebuild: bake .blend -> render frames (CPU Cycles) -> audio -> mux -> validate.
# Requires: pip install bpy (Blender 5.x as a Python module), numpy, pillow, ffmpeg.
set -euo pipefail
cd "$(dirname "$0")/.."
PCT=${PCT:-100}          # % of 1080x1920 (100 = native)
SAMPLES=${SAMPLES:-8}
python3 -I scripts/build_episode.py blend/LittleWonderWorld_E01.blend
python3 -I scripts/render_frames.py blend/LittleWonderWorld_E01.blend renders 0 899 1 --res "$PCT" --samples "$SAMPLES"
python3 -I scripts/make_audio.py audio/E01_mix.wav
ffmpeg -y -framerate 30 -i renders/f%04d.png -i audio/E01_mix.wav -vf "scale=1080:1920:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset slow -crf 17 -r 30 -c:a aac -b:a 192k -t 30 -movflags +faststart output/LittleWonderWorld_E01_Final.mp4
ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=width,height,r_frame_rate,nb_read_frames,duration -of default=nw=1 output/LittleWonderWorld_E01_Final.mp4
