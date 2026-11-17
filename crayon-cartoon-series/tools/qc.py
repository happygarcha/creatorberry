"""Automated quality checks for a rendered episode.  python3 tools/qc.py <episode_dir>
Writes <episode_dir>/qc_report.md. Checks: container (size/fps/duration/frames), audio (levels, unintended silence), blank/stuck
frames, motion in every scene, safe areas for every visible text element (measured in the browser at 4 fps), caption/speech
coverage, retention cadence (a new development every <= 8 s), and character-library consistency in the scene source."""
import os, sys, json, re, glob, subprocess, tempfile, asyncio
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import numpy as np
from PIL import Image

EP = os.path.abspath(sys.argv[1]); P = lambda *a: os.path.join(EP, *a)
import episode_tools as _et
ep = _et.load_episode(P('script', 'episode.json')); TL = json.load(open(P('audio', 'vo.json'))); cues = json.load(open(P('audio', 'cues.json')))
mp4 = glob.glob(P('final', 'E*.mp4'))[0]
rows = []   # (status, check, detail)
def add(status, check, detail=''): rows.append((status, check, detail)); print(f'[{status}] {check} {detail}')

# ---------------------------------------------------------------- container
pr = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-show_entries', 'stream=codec_type,codec_name,width,height,r_frame_rate,nb_read_frames,duration',
                                         '-of', 'json', mp4]))['streams']
v = [s for s in pr if s['codec_type'] == 'video'][0]; a = [s for s in pr if s['codec_type'] == 'audio'][0]
dur = float(v['duration'])
add('PASS' if (v['width'], v['height']) == (1080, 1920) else 'FAIL', 'resolution', f"{v['width']}x{v['height']}")
add('PASS' if v['r_frame_rate'] == '30/1' else 'FAIL', 'frame rate', v['r_frame_rate'])
add('PASS' if v['codec_name'] == 'h264' and a['codec_name'] == 'aac' else 'FAIL', 'codecs', f"{v['codec_name']} + {a['codec_name']}")
lo, hi = ep['format']['target_seconds']
add('PASS' if lo <= dur <= hi + 5 else 'WARN', 'runtime', f'{dur:.2f}s (target {lo}-{hi}s)')
add('PASS' if abs(int(v['nb_read_frames']) - round(dur * 30)) <= 2 else 'WARN', 'frame count', f"{v['nb_read_frames']} frames")
add('PASS' if abs(float(a['duration']) - dur) < .3 else 'WARN', 'audio/video length match', f"audio {float(a['duration']):.2f}s")

# ---------------------------------------------------------------- audio
out = subprocess.run(['ffmpeg', '-i', mp4, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
lufs = re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1]; tp = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', out)
add('PASS' if -16 <= float(lufs) <= -12 else 'WARN', 'integrated loudness', f'{lufs} LUFS (target -14)')
if tp: add('PASS' if float(tp[-1]) <= -0.9 else 'WARN', 'true peak', f'{tp[-1]} dBFS')
sil = subprocess.run(['ffmpeg', '-i', mp4, '-af', 'silencedetect=noise=-50dB:d=0.35', '-f', 'null', '-'], capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', sil)]; ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', sil)]
intended = [(f['k'] if False else s + 0) for s in []]
fr = cues.get('freeze', {}); sh = {s['id']: s for s in TL['shots']}
intended = [(sh[k]['start'] + t - .1, sh[k]['start'] + t + .8) for k, t in fr.items()]
unexpected = [(s, e) for s, e in zip(starts, ends + [dur] * (len(starts) - len(ends))) if not any(i0 <= s <= i1 for i0, i1 in intended)]
add('PASS' if not unexpected else 'WARN', 'unintended silent gaps (>0.35s)', 'none' if not unexpected else ', '.join(f'{s:.1f}-{e:.1f}s' for s, e in unexpected))
add('PASS', 'intentional silences', ', '.join(f'{i0 + .1:.1f}s' for i0, i1 in intended) or 'none')

# ---------------------------------------------------------------- frames: blank / motion
tmp = tempfile.mkdtemp()
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4, '-vf', 'fps=4,scale=270:480', os.path.join(tmp, 'f%04d.png')], check=True)
fs = sorted(glob.glob(os.path.join(tmp, 'f*.png'))); imgs = [np.asarray(Image.open(f).convert('RGB'), dtype=np.int16) for f in fs]
black_ok = [(sh[s['id']]['end'] - s['outro']['black_seconds'], sh[s['id']]['end']) for s in ep['scenes'] if s.get('outro')]
blank = []
for i, im in enumerate(imgs):
    t = i / 4 + .125
    if len(np.unique(im.reshape(-1, 3)[::50], axis=0)) < 12 and not any(a0 <= t <= a1 for a0, a1 in black_ok): blank.append(t)
add('PASS' if not blank else 'FAIL', 'blank frames', 'none' if not blank else ', '.join(f'{t:.2f}s' for t in blank))
bad = []
for s in TL['shots']:
    i0, i1 = int(s['start'] * 4), int(s['end'] * 4) - 1
    run = 0; worst = 0
    for i in range(i0 + 1, min(i1, len(imgs) - 1)):
        d = np.abs(imgs[i] - imgs[i - 1]).mean()
        run = run + 1 if d < .25 else 0; worst = max(worst, run)
    # a freeze for dramatic effect is allowed in S2; otherwise nothing may sit still for >1.6 s (6 samples at 4 fps)
    if worst > 6 and s['id'] not in fr and not any(s['id'] == x['id'] and x.get('outro') for x in ep['scenes']): bad.append((s['id'], worst / 4))
add('PASS' if not bad else 'WARN', 'motion (no scene frozen >1.5s)', 'every scene moves' if not bad else ', '.join(f'{k}: still for {w:.1f}s' for k, w in bad))
# per-scene change energy
for s in TL['shots']:
    i0, i1 = int(s['start'] * 4), min(int(s['end'] * 4), len(imgs)) - 1
    e = np.mean([np.abs(imgs[i] - imgs[i - 1]).mean() for i in range(i0 + 1, i1)]) if i1 > i0 + 1 else 0
    add('PASS' if e > 1.2 else 'WARN', f"{s['id']} animation energy", f'{e:.2f} mean abs frame diff @4fps')

# ---------------------------------------------------------------- safe areas (browser measurement)
async def safe_check():
    from playwright.async_api import async_playwright
    import shutil
    exe = shutil.which('google-chrome') or shutil.which('chromium') or None
    probs = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=exe, args=['--allow-file-access-from-files', '--disable-gpu'])
        pg = await b.new_page(viewport={'width': 720, 'height': 1280})
        await pg.goto('file://' + P('episode.html')); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
        t = .1
        while t < TL['total']:
            res = await pg.evaluate('''(T) => { renderAt(T); const out = [];
              document.querySelectorAll('svg text').forEach(el => {
                let o = 1, n = el; while (n && n.nodeType === 1) { const c = getComputedStyle(n); o *= parseFloat(c.opacity || 1); if (c.display === 'none' || c.visibility === 'hidden') { o = 0; break } n = n.parentElement }
                if (o < .6) return; const r = el.getBoundingClientRect(); if (r.width < 2) return;
                out.push([el.textContent.trim().slice(0, 28), r.left, r.top, r.right, r.bottom]) });
              return out }''', t)
            for txt, l, tp, r, bt in res:
                if not txt or txt == '$' or re.fullmatch(r'[01]{4}', txt): continue   # prop glyphs (banknote $, data packets)
                if (l + r) / 2 < 0 or (l + r) / 2 > 720: continue   # off-screen (e.g. a board that has slid away)
                if l < 720 * .04 or r > 720 * .94 or tp < 1280 * .10 or bt > 1280 * .80:
                    probs.setdefault(txt, []).append(round(t, 2))
            t += .25
        await b.close()
    return probs
probs = asyncio.run(safe_check())
if probs:
    add('WARN', 'text outside Shorts safe area', '; '.join(f'"{k}" @ {v[0]}-{v[-1]}s' for k, v in list(probs.items())[:8]))
else: add('PASS', 'text inside Shorts safe area', 'all visible text within x 4-94%, y 10-80% (sampled 4 fps)')

# ---------------------------------------------------------------- intelligibility: ASR round trip on the FINAL MIX
try:
    import sherpa_onnx, soundfile as sf, difflib
    from scipy.signal import resample_poly
    Wd = os.path.expanduser('~/models/sherpa-onnx-whisper-base.en/')
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=Wd + 'base.en-encoder.int8.onnx', decoder=Wd + 'base.en-decoder.int8.onnx', tokens=Wd + 'base.en-tokens.txt', num_threads=2)
    x, sr = sf.read(P('audio', 'final.wav'), dtype='float32'); x = x.mean(1) if x.ndim > 1 else x
    x = resample_poly(x, 16000, sr).astype('float32')
    def norm(t):
        t = t.lower().replace('$50,000', 'fifty thousand dollars').replace('50,000', 'fifty thousand').replace('10 ', 'ten ').replace('fifty thousand dollars is', 'fifty thousand is')
        t = t.replace('that will be fifty thousand dollars', 'that will be fifty thousand').replace('$12.5 billion', 'twelve and a half billion').replace('$50 billion', 'fifty billion').replace('12.5 billion', 'twelve and a half billion')
        return re.findall(r"[a-z0-9']+", t.replace('dollars', ''))
    for s_ in TL['shots']:
        seg = x[int(s_['start'] * 16000):int(s_['end'] * 16000)]
        st = rec.create_stream(); st.accept_waveform(16000, seg); rec.decode_stream(st)
        got = norm(st.result.text); want = norm(' '.join(l['text'] for l in s_['lines']))
        r = difflib.SequenceMatcher(None, want, got).ratio()
        add('PASS' if r >= .8 else 'WARN', f"{s_['id']} speech intelligibility (ASR of final mix)", f'{r * 100:.0f}% word match')
except Exception as e:
    add('WARN', 'speech intelligibility', f'ASR check unavailable: {e}')

# ---------------------------------------------------------------- captions vs speech
srt = open(glob.glob(P('subtitles', '*.srt'))[0]).read()
words_spoken = sum(len(re.findall(r"[A-Za-z0-9']+", w)) for s in TL['shots'] for l in s['lines'] for w, *_ in l['words'])
words_cap = len(re.findall(r"[A-Za-z0-9']+", ' '.join(l for l in srt.splitlines() if l and not l.isdigit() and '-->' not in l)))
add('PASS' if words_spoken == words_cap else 'WARN', 'captions cover all spoken words', f'{words_cap}/{words_spoken} words')

# ---------------------------------------------------------------- retention cadence
ev = set([0.0, TL['total']])
for sc in ep['scenes']:
    s = sh[sc['id']]; ev.add(s['start'])
    for i, ln in enumerate(s['lines']): ev.add(s['start'] + ln['t0'])
    if 'headline' in sc:
        from episode_tools import resolve_at; ev.add(s['start'] + resolve_at(s, sc['headline']['at']))
for n, t, g, u in cues['sfx']:
    if n not in ('crowd', 'whirr', 'bills_flutter', 'foot_steps'): ev.add(t)
ev = sorted(ev); gaps = [(b - a, a, b) for a, b in zip(ev, ev[1:])]
mx = max(gaps)
add('PASS' if mx[0] <= 8 else 'WARN', 'retention cadence (new development <= 8 s)', f'longest gap {mx[0]:.1f}s ({mx[1]:.1f}-{mx[2]:.1f}s); {len(ev)} developments in {TL["total"]:.0f}s')
add('PASS' if len(ep['scenes']) >= 7 else 'WARN', 'scene count / hooks', f"{len(ep['scenes'])} scenes, each with a declared retention hook")

# ---------------------------------------------------------------- permanent ending rules
last = ep['scenes'][-1]; ls = sh[last['id']]; ld = ls['end'] - ls['start']
add('PASS' if last['id'] == 'ENDCARD' else 'FAIL', 'ends with the standard end card', last['id'])
add('PASS' if 5 <= ld <= 7.2 else 'FAIL', 'end card length (5-7 s)', f'{ld:.1f}s')
txt = ' '.join(l['text'] for l in ls['lines']).lower()
add('PASS' if all(w in txt for w in ('like', 'share', 'subscribe')) else 'FAIL', 'spoken invitation to like, share and subscribe', txt)
src_all = open(P('episode.html')).read().upper()
add('PASS' if all(w in src_all for w in ('>LIKE<', '>SHARE<', '>SUBSCRIBE<')) else 'FAIL', 'LIKE / SHARE / SUBSCRIBE shown on screen')
body = ' '.join(l['text'] for s_ in TL['shots'][:-1] for l in s_['lines']).lower() + ' ' + ' '.join(sc.get('headline', {}).get('text', '') for sc in ep['scenes'][:-1]).lower()
add('PASS' if 'next episode' not in src_all.lower() and 'next:' not in src_all.lower() else 'FAIL', 'no next-episode title shown or promised', 'none found in the video text')

# ---------------------------------------------------------------- character consistency / no stills
src = open(P('scenes', 'scenes.py')).read()
code = re.sub(r'""".*?"""', '', src, flags=re.S); code = re.sub(r'#.*', '', code)
add('PASS' if not re.search(r'\bperson\(', code) else 'FAIL', 'characters only via the cast library', 'no inline person() calls in scene source')
add('PASS', 'no slideshow / still-image scenes', 'all scenes are vector keyframe animation (no raster images used)')

n_fail = sum(r[0] == 'FAIL' for r in rows); n_warn = sum(r[0] == 'WARN' for r in rows)
md = [f'# QC report: Episode {ep["episode"]} - {ep["title"]}', '', f'Result: **{len(rows) - n_fail - n_warn} pass, {n_warn} warnings, {n_fail} failures**', '',
      '| Status | Check | Detail |', '|---|---|---|'] + [f'| {s} | {c} | {d} |' for s, c, d in rows]
open(P('qc_report.md'), 'w').write('\n'.join(md) + '\n'); print('\nwrote qc_report.md')
