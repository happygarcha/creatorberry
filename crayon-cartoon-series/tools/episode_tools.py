"""Shared helpers for every episode: script/timeline plumbing, SFX resolution, captions (SVG + SRT), motion presets and
Shorts safe-area constants. Episode scene files import this and the asset libraries; nothing here is episode specific."""
import os, sys, json, math, random
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
for p in ('tools/engine', 'assets/characters', 'assets/props', 'assets/backgrounds', 'assets/audio'):
    sys.path.insert(0, os.path.join(ROOT, p))
import animlib
from animlib import G, scene, page, pop, appear, vanish, slam, shake, flicker
from cc_kit import W, H, INK, caps, text, esc, CAPS, SCRIPT, SCRIPT_B, frame_svg

FONTS = os.path.join(ROOT, 'assets', 'fonts')
VOICES = json.load(open(os.path.join(ROOT, 'assets', 'characters', 'voices.json')))
WHO = {'NARRATOR': 'N', 'GUY': 'GUY', 'BANKER': 'BANKER', 'FRIEND': 'FRIEND'}

# ---------------------------------------------------------------- Shorts safe areas (fractions of the 720x1280 canvas)
SAFE = dict(top=.12, bottom=.76, left=.06, right=.86)     # nothing important outside; captions live in the bottom band
FLOOR = .62                                               # characters' feet
CAP_Y = .715                                              # caption centre
YELLOW = '#F7D35C'


def S(f): return f * H()


# ---------------------------------------------------------------- episode / script / timeline
def load_episode(path): return json.load(open(path))


def build_script(ep):
    voices = {WHO[k]: v['sid'] for k, v in VOICES.items() if not k.startswith('_')}
    shots = []
    for sc in ep['scenes']:
        vo = []
        for ln in sc.get('dialogue', []):
            d = {'text': ln['text'], 'who': WHO[ln['who']], 'speed': VOICES[ln['who']]['speed']}
            if 'say' in ln: d['say'] = ln['say']
            if 'pre' in ln: d['pre'] = ln['pre']
            vo.append(d)
        shots.append({'id': sc['id'], 'vo': vo, 'min': sc['min'], 'tail': sc.get('tail', .3)})
    return {'voices': voices, 'gap': ep.get('gap', [.3, .6]), 'shots': shots}


def word_time(shot, word, which='start'):
    """Local time of the first word that starts with `word` (case-insensitive, punctuation ignored)."""
    w = word.lower()
    for ln in shot.get('lines', []):
        for ww, t0, t1 in ln['words']:
            if ww.lower().strip('.,!?:;"\'$').startswith(w): return t0 if which == 'start' else t1
    raise KeyError(f'{word!r} not found in shot {shot["id"]}')


def resolve_at(shot, at, dur=None):
    """Resolve an 'at' spec to LOCAL seconds: number | 'word:x' | 'line:i:start|end' | 'end-N' | 'start+N' | 'start'."""
    if isinstance(at, (int, float)): return float(at)
    d = shot['end'] - shot['start']
    if at == 'start': return 0.0
    if at.startswith('start+'): return float(at[6:])
    if at.startswith('end-'): return d - float(at[4:])
    if at == 'end': return d
    if at.startswith('word:'):
        w, off = at[5:], 0.0
        for sg in '+-':
            if sg in w[1:]: w, o = w.rsplit(sg, 1); off = float(o) * (1 if sg == '+' else -1); break
        return word_time(shot, w) + off
    if at.startswith('line:'):
        _, i, k = at.split(':'); ln = shot['lines'][int(i)]
        return ln['t0'] if k == 'start' else ln['t1']
    raise ValueError(at)


def sfx_events(ep, TL, freeze=None):
    """-> [[name, GLOBAL t, gain, until_global_or_None]] from every scene's 'sfx' list."""
    sh = {s['id']: s for s in TL['shots']}
    ev = []
    for sc in ep['scenes']:
        s = sh[sc['id']]
        for e in sc.get('sfx', []):
            t = s['start'] + resolve_at(s, e['at'])
            until = None
            if e.get('until') == 'freeze' and freeze and sc['id'] in freeze: until = s['start'] + freeze[sc['id']]
            ev.append([e['name'], round(t, 3), e.get('gain', 1.0), until])
    return ev


def line_of(shot, who_idx):
    return shot['lines'][who_idx]


def talk_of(shot, who, ep_scene):
    """(t0, t1) LOCAL of the first line spoken by `who` in this scene (for mouth flap), or None."""
    for ln, d in zip(shot.get('lines', []), ep_scene.get('dialogue', [])):
        if d['who'] == who: return (ln['t0'], ln['t1'])
    return None


def talks_of(shot, who, ep_scene):
    return [(ln['t0'], ln['t1']) for ln, d in zip(shot.get('lines', []), ep_scene.get('dialogue', [])) if d['who'] == who]


# ---------------------------------------------------------------- captions
def _chunks(shot, ep_scene):
    """Short caption chunks [(t0, t1, [(word, emph)])] LOCAL to the shot, from the TTS word timings."""
    out = []
    for ln, d in zip(shot.get('lines', []), ep_scene.get('dialogue', [])):
        emph = {e.lower() for e in d.get('emph', [])}
        cur, n = [], 0
        for w, t0, t1 in ln['words']:
            clean = w.strip('.,!?:;"').lower()
            cur.append((w, t0, t1, clean in emph)); n += len(w) + 1
            end_punct = w[-1] in '.!?'
            if (n >= 15 and len(cur) >= 2) or len(cur) >= 4 or end_punct or n >= 22:
                out.append(cur); cur, n = [], 0
        if cur: out.append(cur)
    chunks = []
    for i, c in enumerate(out):
        t0 = c[0][1]; t1 = c[-1][2]
        nxt = out[i + 1][0][1] if i + 1 < len(out) else None
        end = t1 + .35 if nxt is None else min(t1 + .3, nxt - .001)
        chunks.append((t0, max(end, t0 + .05), [(w, e) for w, _, _, e in c]))
    return chunks


def caption_svg(shot, ep_scene, size=64):
    """Large, high-contrast ALL-CAPS captions in the bottom safe band; ALL words timed to speech; emphasised words in yellow."""
    parts = []
    for t0, t1, words in _chunks(shot, ep_scene):
        txt = ' '.join(w for w, _ in words).upper()
        lines = [words]
        if sum(len(w) + 1 for w, _ in words) > 15 and len(words) >= 2:
            half = max(1, len(words) // 2); lines = [words[:half], words[half:]]
        y0 = S(CAP_Y) - (len(lines) - 1) * size * .55
        tsp = ''
        for li, ln in enumerate(lines):
            for wi, (w, e) in enumerate(ln):
                sp = '' if wi == 0 else ' '
                fill = YELLOW if e else '#FFFFFF'
                tsp += (f'<tspan x="{W() / 2}" y="{y0 + li * size * 1.08:.1f}" fill="{fill}">{sp}{esc(w.upper())}</tspan>' if wi == 0
                        else f'<tspan fill="{fill}">{sp}{esc(w.upper())}</tspan>')
        el = (f'<text text-anchor="middle" dominant-baseline="middle" style="{SCRIPT_B};font-size:{size}px;stroke:#111;stroke-width:{size * .16}px;'
              f'paint-order:stroke;stroke-linejoin:round">{tsp}</text>')
        parts.append(G(el, [[0, {'o': 0}], [t0 - .001, {'o': 0}], [t0, {'o': 1, 's': 1}, 'h'], [t1, {'o': 1}], [t1 + .001, {'o': 0}, 'h']], (W() / 2, S(CAP_Y))))
    return ''.join(parts)


def srt_text(ep, TL):
    sh = {s['id']: s for s in TL['shots']}
    n, out = 1, []
    def ts(t):
        h, r = divmod(t, 3600); m, s = divmod(r, 60)
        return f'{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}'
    for sc in ep['scenes']:
        s = sh[sc['id']]
        for t0, t1, words in _chunks(s, sc):
            out.append(f'{n}\n{ts(s["start"] + t0)} --> {ts(s["start"] + t1)}\n{" ".join(w for w, _ in words).upper()}\n'); n += 1
    return '\n'.join(out)


# ---------------------------------------------------------------- motion presets (keyframe lists, LOCAL times)
def jitter(t0, t1, amp=5, fps=15, seed=1, y=True):
    """Violent shake: random tx/ty every 1/fps s between t0 and t1, then settle."""
    r = random.Random(seed); k = [[t0, {'tx': 0, 'ty': 0}]]
    n = max(1, int((t1 - t0) * fps))
    for i in range(1, n + 1):
        k.append([round(t0 + i / fps, 3), {'tx': r.uniform(-amp, amp), 'ty': r.uniform(-amp, amp) * .6 if y else 0}, 'l'])
    k.append([t1 + .001, {'tx': 0, 'ty': 0}, 'l'])
    return k


def hop(t0, h=40, d=.4, n=1):
    k = [[t0, {'ty': 0}]]
    for i in range(n):
        k += [[t0 + d * (i + .5), {'ty': -h}, 'o'], [t0 + d * (i + 1), {'ty': 0}, 'i']]
    return k


def merge(*lists):
    """Combine keyframe lists that animate different props of the same element into one sorted list."""
    out = {}
    for L in lists:
        for t, p, *e in L: out.setdefault(t, [t, {}, e[0] if e else 'io'])[1].update(p)
    return [out[t] for t in sorted(out)]


def projectile_keys(t0, d, v0, g, rot, freeze=None, hold=True, ground=None, y0=0, step=1 / 15):
    """Sampled ballistic motion: tx = vx*t, ty = vy*t + .5 g t^2 (px, +y down), spin 'rot' deg/s. freeze=local time to stop all motion.
    If `ground` (y offset) is given the object stops there (no bounce)."""
    vx, vy = v0; k = [[0, {'o': 0}], [max(0, t0 - .001), {'o': 0, 'tx': 0, 'ty': 0, 'r': 0}], [t0, {'o': 1}]]
    t = 0.0; end = t0 + d if freeze is None else min(t0 + d, freeze)
    while t0 + t <= end + 1e-6:
        y = vy * t + .5 * g * t * t
        if ground is not None and y > ground: y = ground
        k.append([round(t0 + t, 3), {'tx': vx * t, 'ty': y, 'r': rot * t}, 'l']); t += step
    return k


def bill_storm(x0, y0, n, t0, spread=(-300, 300), up=(-420, -160), g=900, seed=3, freeze=None, floor=None, size=(.7, 1.0), dur=2.2, stagger=.8):
    """Banknotes shot from (x0, y0) in a fountain; physics-ish. Each is a G with sampled keys; they land on `floor` (absolute y) and stay."""
    from cc_kit import cash
    r = random.Random(seed); out = []
    for i in range(n):
        ts = t0 + r.uniform(0, stagger)
        vx = r.uniform(*spread); vy = r.uniform(*up)
        grd = (floor - y0 + r.uniform(-30, 20)) if floor else None
        out.append(G(cash(x0, y0, r.uniform(*size)), projectile_keys(ts, dur, (vx, vy), g, r.uniform(-500, 500), freeze=freeze, ground=grd), (x0, y0)))
    return ''.join(out)


def count_text(x, y, size, v0, v1, t0, t1, fmt='money', fill='#FFFFFF', e='o'):
    """Animated number (runtime 'count'): <text> whose content is rewritten every frame."""
    keys = [[0, {'count': v0}], [t0, {'count': v0}], [t1, {'count': v1}, e]]
    return (f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" data-fmt="{fmt}" data-kf=\'{animlib.J(keys)}\' '
            f'style="{CAPS};font-size:{size}px;fill:{fill}">{fmt}</text>')


def headline(txt, t, size=70, y=None, col=YELLOW, rot=-3, w=None, until=None):
    """Big hand-drawn headline in the top safe band: comic burst + oversized text, slams in at local time t."""
    from cc_kit import burst, tw
    y = S(.215) if y is None else y
    lines = txt.split('\n') if '\n' in txt else None
    if lines is None:   # wrap long headlines on spaces
        ws = txt.split(); half = (len(ws) + 1) // 2
        lines = [' '.join(ws[:half]), ' '.join(ws[half:])] if len(txt) > 16 else [txt]
    body = '\n'.join(lines)
    ww = max(len(l) for l in lines) * size * .55
    sc = min(1.0, (W() * (SAFE['right'] - SAFE['left'])) / ww)
    inner = (f'<g transform="translate({W() / 2} {y}) rotate({rot}) scale({sc})">'
             f'<rect x="{-ww / 2 - 28}" y="{-size * len(lines) * .62}" width="{ww + 56}" height="{size * len(lines) * 1.24}" rx="16" fill="{col}" stroke="{INK}" stroke-width="6"/>'
             + text(0, 0, body, size, CAPS, INK, lh=1.05) + '</g>')
    keys = slam(t) + ([[until - .001, {'o': 1}], [until, {'o': 0}, 'h']] if until else [])
    return G(inner, keys, (W() / 2, y))


def big_word(txt, t, size=260, y=None, col='#FFFFFF', stroke=INK, rot=-6, x=None):
    y = S(.4) if y is None else y
    x = W() / 2 if x is None else x
    inner = text(x, y, txt, size, SCRIPT_B, col, stroke=stroke, sw=size * .09, rot=rot)
    return G(inner, slam(t, 2.4), (x, y))


def black_card(inner=''):
    from cc_kit import fill_bg
    return fill_bg('#000') + inner


def mouth_windows(shot, who, ep_scene, idx=0):
    """Lip-sync: one open-mouth window per spoken word (open for the first 70% of the word) for the idx-th line spoken by `who`."""
    k = -1
    for ln, d in zip(shot.get('lines', []), ep_scene.get('dialogue', [])):
        if d['who'] == who:
            k += 1
            if k == idx: return [(t0 + .01, t0 + .72 * (t1 - t0)) for w, t0, t1 in ln['words']]
    return None
