"""Concatenate the rendered chunks, mux the mixed audio, write the SRT, and build the contact sheet FROM THE RENDERED MP4."""
import os, json, subprocess
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
OUT = 'final/Zapzapper_DarkFiles_60sec_Test.mp4'
open('frames/parts/list.txt', 'w').write(''.join(f"file 'p{i}.mp4'\n" for i in range(4)))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', 'frames/parts/list.txt', '-c', 'copy', 'frames/video_only.mp4'], check=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'frames/video_only.mp4', '-i', 'audio/final_mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p',
                '-r', '30', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-af', 'apad', '-t', '60', '-movflags', '+faststart', '-metadata', 'language=eng', OUT], check=True)
# SRT
caps = json.load(open('subtitles/caps.json'))
ts = lambda t: f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round((t % 1) * 1000)):03d}"
with open('subtitles/Zapzapper_DarkFiles_60sec_Test.srt', 'w') as f:
    for i, c in enumerate(caps, 1): f.write(f"{i}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{(c['label'] + ' ') if c['label'] else ''}{c['text']}\n\n")
# contact sheet (frames decoded from the MP4)
times = [1.0, 4.5, 6.8, 10.8, 12.8, 17.6, 25.0, 29.5, 33.9, 36.2, 39.6, 43.5, 46.6, 50.0, 52.8, 55.6, 58.3, 59.95]
cols = 3; tw, th = 640, 360; rows = (len(times) + cols - 1) // cols
sheet = Image.new('RGB', (cols * tw, rows * (th + 26)), (18, 18, 22)); d = ImageDraw.Draw(sheet)
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
except Exception: font = None
labels = {1.0: 'S1 wide: walk in, flashlights', 4.5: 'S1 narrator line', 6.8: 'S1 end', 10.8: 'S2 crouch at the bolts', 12.8: 'S2 REED asks, taps bolt', 17.6: 'S3 close-up: blue strip', 25.0: 'S4 ratchet the bolts', 29.5: 'S4 both push the shelf',
          33.9: 'S5 handle turns', 36.2: 'S5 door on its hinges', 39.6: 'S5 into the doorway', 43.5: 'S6 desk / phone gear revealed', 46.6: 'S6 REED points at recorder', 50.0: 'S6 narrator',
          52.8: 'S7 play pressed, waveform', 55.6: 'S7 girl: "Mom... it\'s me."', 58.3: 'S7 shocked exchange', 59.95: 'cut to black'}
for i, t in enumerate(times):
    p = f'frames/cs_{i}.png'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{t}', '-i', OUT, '-frames:v', '1', '-vf', f'scale={tw}:{th}', p], check=True)
    x, y = (i % cols) * tw, (i // cols) * (th + 26); sheet.paste(Image.open(p), (x, y + 26)); d.text((x + 8, y + 4), f'{t:5.2f}s  {labels[t]}', fill=(235, 235, 235), font=font)
sheet.save('final/Zapzapper_DarkFiles_60sec_ContactSheet.png'); print('done', OUT)
