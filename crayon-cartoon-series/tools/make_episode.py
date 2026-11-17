"""Episode pipeline.  python3 tools/make_episode.py <episode_dir> <command> [args]
  script            episode.json -> audio/script.json (TTS script, fixed voice profiles)
  tts               voices -> audio/vo.wav + audio/vo.json (the timeline every scene is locked to)
  build             scenes.py + timeline -> episode.html, audio/cues.json, subtitles/E.srt
  stills [t,t,..]   PNG stills (or: stills scenes -> beginning/middle/end of every scene) into frames/
  render [S1 S3]    render scenes to final/scenes/<id>.mp4 (all scenes if none given); re-render one scene without touching the rest
  audio             voices + SFX + music -> audio/final.wav (-14 LUFS)
  mux               concat scene videos + audio -> final/<name>.mp4
  all               script, tts, build, render, audio, mux, qc"""
import os, sys, json, subprocess, importlib.util, shutil
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from episode_tools import *
import episode_tools as ET

EP_DIR = os.path.abspath(sys.argv[1]); cmd = sys.argv[2]; args = sys.argv[3:]
P = lambda *a: os.path.join(EP_DIR, *a)
ep = load_episode(P('script', 'episode.json'))
NAME = f"E{ep['episode']:02d}_" + ''.join(c if c.isalnum() else '_' for c in ep['title']).strip('_')
os.makedirs(P('audio'), exist_ok=True); os.makedirs(P('final', 'scenes'), exist_ok=True); os.makedirs(P('subtitles'), exist_ok=True); os.makedirs(P('frames'), exist_ok=True)
ENG = os.path.join(ROOT, 'tools', 'engine')


def run(*a, **kw):
    print('+', ' '.join(map(str, a))[:200], flush=True); return subprocess.run([str(x) for x in a], check=True, **kw)


def load_scenes():
    spec = importlib.util.spec_from_file_location('ep_scenes', P('scenes', 'scenes.py')); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def do_script():
    json.dump(build_script(ep), open(P('audio', 'script.json'), 'w'), indent=1); print('wrote audio/script.json')


def do_tts():
    run('python3', '-I', os.path.join(ENG, 'timeline.py'), 'tts', P('audio', 'script.json'), P('audio', 'vo'))


def do_build():
    animlib.set_format('9:16')
    TL = json.load(open(P('audio', 'vo.json'))); sh = {s['id']: s for s in TL['shots']}
    m = load_scenes(); scs = []; freeze = {}; black = []
    for sc in ep['scenes']:
        s = sh[sc['id']]; c = m.C(sc, s, None)
        res = m.BUILDERS[sc['id']](c)
        world, cam, cam_o, over = res
        if hasattr(c, 'freeze'): freeze[sc['id']] = c.freeze
        outro = sc.get('outro'); end = s['end'] - (outro['black_seconds'] if outro else 0)
        scs.append(scene(s['start'], end, frame_svg(world, sc['title']), cam=cam, cam_o=cam_o, z=1))
        caps_svg = caption_svg(s, sc) if sc.get('captions', True) else ''
        scs.append(scene(s['start'], end, frame_svg(over + caps_svg, 'overlay'), bg='transparent', z=5))
        if outro:
            from cc_kit import fill_bg
            t0 = end
            txt = text(W() / 2, S(.45), outro['small_text'], 54, CAPS, '#FFFFFF')
            scs.append(scene(t0, s['end'], frame_svg(fill_bg('#000') + G(txt, [[0, {'o': 0}], [.15, {'o': 0}], [.4, {'o': 1}]]), 'next episode'), z=6))
    # quick comic swipe over every scene boundary (hides the hard cut): an ink band sweeps across in 0.3 s, centred on the cut
    for i, sc in enumerate(ep['scenes'][:-1]):
        b = sh[sc['id']]['end']
        band = (f'<g transform="skewX(-12)">' + f'<rect x="-420" y="-100" width="360" height="{H() + 200}" fill="#161616"/>'
                f'<rect x="-60" y="-100" width="40" height="{H() + 200}" fill="{YELLOW}"/></g>')
        scs.append(scene(b - .16, b + .16, frame_svg(G(band, [[0, {'tx': 0}], [.32, {'tx': W() + 520}, 'l']]), 'swipe'), bg='transparent', z=9))
    html = page(scs, animlib.local_fonts(FONTS, __import__('cc_kit').FONT_SPECS))
    open(P('episode.html'), 'w').write(html)
    ev = sfx_events(ep, TL, freeze)
    ev += [['whoosh', round(sh[sc['id']]['end'] - .16, 3), .5, None] for sc in ep['scenes'][:-1]]
    music, dips = [], []
    for sc in ep['scenes']:
        s = sh[sc['id']]
        if music and music[-1][2] == sc['music']: music[-1][1] = s['end']
        else: music.append([s['start'], s['end'], sc['music']])
        if sc['id'] in freeze: dips.append([s['start'] + freeze[sc['id']] - .03, s['start'] + freeze[sc['id']] + .6, 0.0])
        if sc.get('outro'): dips.append([s['end'] - sc['outro']['black_seconds'], s['end'], .35])
    json.dump({'total': TL['total'], 'sfx': ev, 'music': music, 'dips': dips, 'freeze': freeze}, open(P('audio', 'cues.json'), 'w'), indent=1)
    open(P('subtitles', NAME + '.srt'), 'w').write(srt_text(ep, TL))
    print(f'built episode.html: total {TL["total"]:.2f}s, {len(ep["scenes"])} scenes, {len(ev)} sfx cues, srt written')
    for s in TL['shots']: print(f'  {s["id"]}: {s["start"]:6.2f} - {s["end"]:6.2f}  ({s["end"] - s["start"]:.2f}s)')


def do_stills():
    TL = json.load(open(P('audio', 'vo.json')))
    if args and args[0] != 'scenes': ts = [float(x) for x in args[0].split(',')]
    else:
        ts = []
        for s in TL['shots']:
            d = s['end'] - s['start']; ts += [s['start'] + .12, s['start'] + d * .5, s['end'] - .12]
    for f in os.listdir(P('frames')):
        if f.startswith('still_'): os.remove(P('frames', f))
    run('python3', os.path.join(ENG, 'render.py'), P('episode.html'), P('frames', 'still'), '--stills', ','.join(f'{t:.2f}' for t in ts))


def do_render():
    TL = json.load(open(P('audio', 'vo.json')))
    want = args or [s['id'] for s in TL['shots']]
    for s in TL['shots']:
        if s['id'] in want:
            run('python3', os.path.join(ENG, 'render.py'), P('episode.html'), P('final', 'scenes', s['id'] + '.mp4'), f'{s["start"]:.3f}', f'{s["end"]:.3f}')


def do_audio():
    from sfx_lib import make, SR, np, place, mix, bed
    import soundfile as sf
    c = json.load(open(P('audio', 'cues.json')))
    n = int(c['total'] * SR) + SR
    f = np.zeros((n, 2))
    for name, t, gain, until in c['sfx']:
        kw = {'d': max(.3, until - t)} if (until and name in ('whirr', 'bills_flutter')) else {}
        try: x = make(name, **kw)
        except TypeError: x = make(name)
        place(f, x, t, gain)
    mix(P('audio', 'vo.wav'), f, bed(c['total'] + 1, c['music'], c['dips'])[:n], P('audio', 'final.wav'))
    print('wrote audio/final.wav')


def do_mux():
    lst = P('final', 'scenes', 'list.txt')
    TL = json.load(open(P('audio', 'vo.json')))
    open(lst, 'w').write(''.join(f"file '{P('final', 'scenes', s['id'] + '.mp4')}'\n" for s in TL['shots']))
    out = P('final', NAME + '.mp4')
    run('ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-i', P('audio', 'final.wav'), '-map', '0:v', '-map', '1:a',
        '-vf', 'scale=1080:1920:flags=lanczos,format=yuv420p', '-r', '30', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-c:a', 'aac', '-b:a', '192k',
        '-shortest', '-movflags', '+faststart', out)
    run('ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,codec_name,width,height,r_frame_rate,duration', '-of', 'default=nw=1', out)


C = {'script': do_script, 'tts': do_tts, 'build': do_build, 'stills': do_stills, 'render': do_render, 'audio': do_audio, 'mux': do_mux}
if cmd == 'all':
    for k in ('script', 'tts', 'build', 'render', 'audio', 'mux'): C[k]()
    run('python3', os.path.join(ROOT, 'tools', 'qc.py'), EP_DIR)
else: C[cmd]()
