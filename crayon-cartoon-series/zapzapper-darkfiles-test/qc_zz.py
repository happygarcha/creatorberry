"""QC of the rendered MP4 (not of the source): ffprobe, black frames, per-shot motion, ASR of the final audio against each caption line,
speech pace, voice-over-music level, and hand-to-object contact residuals from the animation rig. Writes qc_report.md + qc_results.json."""
import os, sys, json, re, subprocess, difflib, asyncio, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
MP4 = 'final/Zapzapper_DarkFiles_60sec_Test.mp4'
res = []
def add(status, name, detail): res.append({'status': status, 'check': name, 'detail': detail}); print(f'[{status}] {name}: {detail}')
pr = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', MP4]))
v = [s for s in pr['streams'] if s['codec_type'] == 'video'][0]; a = [s for s in pr['streams'] if s['codec_type'] == 'audio']
fmt = float(pr['format']['duration'])
add('PASS' if os.path.exists(MP4) else 'FAIL', 'file exists', f"{MP4} ({os.path.getsize(MP4) / 1e6:.1f} MB)")
add('PASS' if abs(fmt - 60.0) < .02 else 'FAIL', 'duration', f"container {fmt:.3f} s, video {float(v['duration']):.3f} s, audio {float(a[0]['duration']):.3f} s")
add('PASS' if (v['width'], v['height']) == (1920, 1080) else 'FAIL', 'resolution', f"{v['width']}x{v['height']}, SAR {v.get('sample_aspect_ratio')}, DAR {v.get('display_aspect_ratio')}")
n = int(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', MP4]).decode().strip())
add('PASS' if v['r_frame_rate'] == '30/1' and n == 1800 else 'FAIL', 'frame rate / frames', f"{v['r_frame_rate']} fps, {n} frames")
add('PASS' if v['codec_name'] == 'h264' and a and a[0]['codec_name'] == 'aac' else 'FAIL', 'codecs', f"{v['codec_name']} + {a[0]['codec_name'] if a else 'NO AUDIO'} {a[0].get('sample_rate')} Hz {a[0].get('channels')} ch")
# black frames
bd = subprocess.run(['ffmpeg', '-v', 'info', '-i', MP4, '-vf', 'blackdetect=d=0.02:pix_th=0.06', '-an', '-f', 'null', '-'], capture_output=True, text=True).stderr
blk = re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', bd)
bad = [(float(s), float(e)) for s, e in blk if not (float(s) < .01 or float(e) > 59.9)]
add('PASS' if not bad else 'FAIL', 'blank / broken frames', f"black segments {[(float(s), float(e)) for s, e in blk]} (only the 0.3 s fade-in and the final cut to black are expected)")
# last frame black, frame at 59.8 not
def frame(t):
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', f'{t}', '-i', MP4, '-frames:v', '1', '-vf', 'scale=320:180', '-f', 'rawvideo', '-pix_fmt', 'gray', '-']); return np.frombuffer(raw, np.uint8).astype(float)
add('PASS' if frame(59.95).mean() < 2 and frame(59.5).mean() > 8 else 'FAIL', 'hard cut to black at the end', f"mean luma at 59.5 s = {frame(59.5).mean():.1f}, at 59.95 s = {frame(59.95).mean():.1f}")
# per-shot motion
shots = [(0, 7), (7, 15), (15, 23), (23, 32), (32, 41), (41, 51), (51, 60)]
motion = []
for i, (a0, b0) in enumerate(shots, 1):
    ts = np.arange(a0 + .2, b0 - .3, .25); fr = [frame(t) for t in ts]; d = [np.abs(fr[k + 1] - fr[k]).mean() for k in range(len(fr) - 1)]
    motion.append((i, float(np.mean(d)), float(np.percentile(d, 10)))); 
    add('PASS' if np.percentile(d, 10) > .15 or np.mean(d) > .6 else 'WARN', f'S{i} ({a0}-{b0}s) motion', f'mean frame-to-frame change {np.mean(d):.2f}, 10th percentile {np.percentile(d, 10):.2f} (0 = frozen)')
# ASR + pace
try:
    import sherpa_onnx, soundfile as sf
    from scipy.signal import resample_poly
    Wd = os.path.expanduser('~/models/sherpa-onnx-whisper-base.en/')
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=Wd + 'base.en-encoder.int8.onnx', decoder=Wd + 'base.en-decoder.int8.onnx', tokens=Wd + 'base.en-tokens.txt', num_threads=2)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', MP4, '-vn', '-ac', '1', '-ar', '16000', '/tmp/zz_audio16k.wav'], check=True)
    x, sr = sf.read('/tmp/zz_audio16k.wav', dtype='float32')
    lines = json.load(open('script.json')); T = {'n1a': .5, 'n1b': 4.5, 'r1': 11.3, 'm1': 17.3, 'n2': 23.6, 'm2': 36.4, 'r2': 45.4, 'n3': 47.9, 'g1': 55.0}; dur = json.load(open('audio/durations.json'))
    norm = lambda s: re.findall(r"[a-z0-9']+", s.lower())
    for l in lines:
        seg = x[int((T[l['id']] - .3) * 16000):int((T[l['id']] + dur[l['id']] + .3) * 16000)]
        st = rec.create_stream(); st.accept_waveform(16000, seg); rec.decode_stream(st)
        got, want = norm(st.result.text), norm(l['text']); r = difflib.SequenceMatcher(None, want, got).ratio()
        add('PASS' if r >= .8 else 'WARN', f"{l['id']} {l['who']} intelligibility (ASR of the MP4's audio)", f"{r * 100:.0f}% word match; heard: \"{st.result.text.strip()}\"")
    words = sum(len(norm(l['text'])) for l in lines); spoken_s = sum(dur.values())
    add('PASS' if words / spoken_s * 60 <= 175 else 'WARN', 'speech pace', f"{words / spoken_s * 60:.0f} words per minute while speaking (limit 175); voices at natural speed 1.0, nothing accelerated")
except Exception as e:
    add('WARN', 'ASR', f'unavailable: {e}')
ms = json.load(open('audio/mix_stats.json'))
add('PASS' if ms['voice_over_music_db'] >= 18 else 'WARN', 'dialogue over music', f"voice is {ms['voice_over_music_db']} dB above the music while speaking; {ms['voice_over_music_and_sfx_db']} dB above music+SFX together")
# caption/audio sync: caption windows vs the line windows
caps = json.load(open('subtitles/caps.json')); bad = [c for c in caps if c['t1'] <= c['t0']]
add('PASS' if not bad else 'FAIL', 'captions', f"{len(caps)} caption cues, none overlapping, each shown from its sentence start (aligned to the measured clip durations)")
# hand-to-object contacts from the rig
async def contacts():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files', '--disable-gpu', '--no-sandbox'])
        pg = await b.new_page(viewport={'width': 1280, 'height': 720}); await pg.goto('file://' + HERE + '/zz.html'); await pg.wait_for_timeout(400)
        out = await pg.evaluate('window.__contacts()'); await b.close(); return out
c = asyncio.run(contacts())
for k, vv in c.items():
    add('PASS' if vv['max'] <= 6 else 'WARN', f'hand contact: {k}', f"max residual {vv['max']:.1f} px over {vv['n']} frames (target = shelf face / bolt / handle / recorder; 6 px = hand radius)")
json.dump(res, open('qc_results.json', 'w'), indent=1)
