"""Sound palette for the story-cartoon style: a soft looped music bed (~12 dB under the voice, ducked while
speaking) plus light, sparse SFX. Real samples win: put <name>.wav files in $SFX_DIR (e.g. pop.wav, whoosh.wav,
paper.wav, ding.wav, thud.wav, phone.wav, crowd.wav, coins.wav, type.wav) and fx(name) loads them instead of synthesising."""
import os
from sfx_base import *

SFX_DIR = os.environ.get('SFX_DIR', os.path.expanduser('~/sfx'))


def _load(name):
    p = os.path.join(SFX_DIR, name + '.wav')
    if not os.path.exists(p): return None
    x, sr = sf.read(p, dtype='float32')
    x = x.mean(1) if x.ndim > 1 else x
    return resample_poly(x, SR, sr) if sr != SR else x


def tone(f, d, g=.3, decay=.6, partials=((1, 1), (2, .45), (3, .18), (4, .08))):
    """Soft piano/pluck note: decaying sine partials (vectorised, fast)."""
    n = int(d * SR); t = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * m / decay) for m, a in partials)
    return g * x * np.minimum(1, t / .004)


def pop(g=.35):
    d = .12; t = np.arange(int(d * SR)) / SR
    return g * np.sin(2 * np.pi * (900 - 2600 * t) * t) * np.exp(-t / .03)


def paper(g=.25):
    d = .35; n = int(d * SR)
    return g * filt(noise(d), [1500, 7000], 'band') * np.exp(-np.arange(n) / SR / .09) * (1 + .6 * np.sin(2 * np.pi * 30 * np.arange(n) / SR))


def ding(g=.28): return chime(1318, g, 1.2)


def coins(g=.2):
    out = np.zeros(int(.6 * SR))
    for k, f in enumerate((2637, 3136, 2349, 3520)):
        x = chime(f, .5, .3); s = int(k * .06 * SR); out[s:s + len(x)] += x[:len(out) - s]
    return g * out


def phone(g=.18, d=1.2):
    n = int(d * SR); t = np.arange(n) / SR
    bell = (np.sin(2 * np.pi * 1700 * t) + np.sin(2 * np.pi * 2100 * t)) * (np.sin(2 * np.pi * 20 * t) > 0)
    return g * bell * np.where((t % .6) < .4, 1, 0)


def crowd(d=3.0, g=.12):
    n = int(d * SR); t = np.arange(n) / SR
    return g * filt(noise(d), [300, 2500], 'band') * (0.7 + .3 * np.sin(2 * np.pi * 1.3 * t) * np.sin(2 * np.pi * .7 * t)) * np.minimum(1, np.minimum(t, d - t) / .3)


def typing(nchars, cps=22, g=.06):
    d = nchars / cps + .1; out = np.zeros(int(d * SR))
    for k in range(nchars):
        if rng.random() < .15: continue
        x = tick(rng.uniform(1800, 2600), .012, 1); s = int(k / cps * SR); out[s:s + len(x)] += x[:len(out) - s]
    return g * out


def boom(g=.5): return thud(48, g, .5)


SYNTH = {'pop': pop, 'whoosh': lambda: whoosh(.4, .3), 'paper': paper, 'ding': ding, 'thud': lambda: thud(60, .6, .14),
         'coins': coins, 'phone': phone, 'crowd': crowd, 'boom': boom, 'click': lambda: click(.4)}


def fx(name, **kw):
    x = _load(name)
    return x if x is not None else SYNTH[name](**kw)


MOODS = {  # chord roots + quality per bar, tempo
    'warm': (76, [(261.6, 'M'), (196.0, 'M'), (220.0, 'm'), (174.6, 'M')]),
    'tense': (70, [(220.0, 'm'), (174.6, 'M'), (261.6, 'M'), (196.0, 'M')]),
    'mystery': (60, [(146.8, 'm'), (146.8, 'm'), (155.6, 'M'), (130.8, 'M')]),
    'triumph': (84, [(261.6, 'M'), (349.2, 'M'), (392.0, 'M'), (261.6, 'M')]),
}


def bed_loop(mood='warm', bars=4, g=.16):
    """One seamless loop of soft arpeggiated piano (bars x 4 beats)."""
    bpm, prog = MOODS[mood]
    beat = 60 / bpm; L = int(bars * 4 * beat * SR)
    out = np.zeros(L + SR * 3)
    for b in range(bars):
        root, q = prog[b % len(prog)]
        third = root * (2 ** ((4 if q == 'M' else 3) / 12)); fifth = root * 1.5
        notes = [root, fifth, root * 2, third * 2, fifth * 2, third * 2, root * 2, fifth]
        for k, f in enumerate(notes):
            s = int((b * 4 + k * .5) * beat * SR); x = tone(f, 2.2, .22 if k else .3, .9); out[s:s + len(x)] += x
        x = tone(root / 2, 3.5, .35, 1.6, ((1, 1), (2, .3))); s = int(b * 4 * beat * SR); out[s:s + len(x)] += x
    tail = out[L:L + SR * 3].copy(); out = out[:L]; out[:len(tail)] += tail[:L]   # wrap the ring-out
    return g * filt(out, 5000, 'low')


def bed(total, sections, dips=()):
    """sections = [(t0, t1, mood)]; dips = [(t0, t1, gain)] e.g. under black cards or for a dramatic silence.
    Returns (n, 2) stereo array at 48 kHz."""
    n = int(total * SR); out = np.zeros(n)
    for t0, t1, mood in sections:
        lp = bed_loop(mood); s, e = int(t0 * SR), min(n, int(t1 * SR))
        seg = np.resize(lp, e - s)
        f = min(int(.8 * SR), (e - s) // 2); ramp = np.ones(e - s); ramp[:f] = np.linspace(0, 1, f); ramp[-f:] = np.linspace(1, 0, f)
        out[s:e] += seg * ramp
    for t0, t1, gn in dips:
        s, e = int(t0 * SR), min(n, int(t1 * SR)); out[s:e] *= gn
    return np.stack([out, out], 1)
