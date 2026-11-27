"""Score (synthesised: vibraphone, glockenspiel, harp, pizzicato bass, bowed pad, plotter tick), foley from events.json, narration, mix -> out/mix.wav (48 kHz stereo).
Run from anywhere: python mix.py   (uses LIB for the sfx helpers)."""
import os, sys, json
import numpy as np, soundfile as sf
from scipy.signal import resample_poly
LIB = os.environ.get('LIB', '/root/lemo-opuscar'); sys.path.insert(0, os.path.join(LIB, 'core', 'audio'))
import sfx as S
SR = S.SR; HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, 'timeline.json'))); EV = json.load(open(os.path.join(HERE, 'events.json')))['ev']
DUR = float(TL['end']); N = int(DUR * SR)
T_LIKE, T_SHARE, T_SUB = TL['vo']['v7'] + 0.1, TL['vo']['v7'] + 1.0, TL['vo']['v7'] + 1.95
BEAT = 60 / 96; rng = np.random.default_rng(11)
mf = lambda m: 440 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(round(d * SR))) / SR

# ---------------- instruments (mono) ----------------
def vibes(f, d=1.6, v=1.0, hard=True):
    t = tt(d); e = np.exp(-t / (1.1 if d > .8 else d))
    x = np.sin(2 * np.pi * f * t) * e + .28 * np.sin(2 * np.pi * f * 3.98 * t) * np.exp(-t / .25) * (1 if hard else .3) + .12 * np.sin(2 * np.pi * f * 10.2 * t) * np.exp(-t / .08)
    x *= 1 + .12 * np.sin(2 * np.pi * 5.2 * t); return x * v
def glock(f, d=1.2, v=1.0):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / .15) + .15 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / .05)) * np.exp(-t / .55) * v
def pluck(f, d=1.4, v=1.0, bright=.5):
    n = int(SR / f); buf = rng.uniform(-1, 1, n) * np.hanning(n) ** .5; out = np.zeros(int(d * SR)); i = 0; prev = buf.copy()
    for k in range(0, len(out), n):
        seg = prev[:min(n, len(out) - k)]; out[k:k + len(seg)] = seg
        prev = (prev + np.roll(prev, 1)) / 2 * (0.996 - .02 * (1 - bright))
    return S.lp(out, 5000 * bright + 1500) * v * 1.4
def pizz(f, d=.7, v=1.0):
    t = tt(d); x = np.sin(2 * np.pi * f * t) * np.exp(-t / .22) + .45 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / .1) + .2 * np.sin(2 * np.pi * f * 3 * t) * np.exp(-t / .05)
    return x * v
def pad(freqs, d, v=1.0):
    t = tt(d); a = np.minimum(t / 1.4, 1) * np.minimum((d - t) / 1.2, 1)
    x = sum(np.sin(2 * np.pi * f * t + rng.random() * 6) * .5 + np.sin(2 * np.pi * f * 2.003 * t) * .2 + np.sin(2 * np.pi * f * .5 * t) * .15 for f in freqs)
    return x * a * (1 + .06 * np.sin(2 * np.pi * .23 * t)) * v / len(freqs)
def tick(v=1.0): d = .03; return S.hp(S.noise(d), 3500) * S.env_exp(d, .004) * v

# ---------------- score ----------------
mus = np.zeros((N, 2))
def put(x, at, g=1.0, pan=0.0): S.add(mus, x.astype(np.float64), at, g, pan)
C, E, G, A, D, F, B = 0, 4, 7, 9, 2, 5, 11
def n(oct, pc): return 12 * (oct + 1) + pc
bar = BEAT * 4
# plotter tick in sixteenths, quiet, only while the picture draws
for a, b, g in [(3.0, 10.0, .09), (35.3, 47.0, .08), (47.6, 58.0, .08)]:
    t0 = np.ceil(a / (BEAT / 4)) * BEAT / 4
    while t0 < b: put(tick(1), t0, g * (1.5 if int(round(t0 / (BEAT / 4))) % 4 == 0 else .8), .25 if int(t0 * 8) % 2 else -.25); t0 += BEAT / 4
# 0-10.3 hook: low pad, vibraphone notes on every other bar
put(pad([mf(n(2, C)), mf(n(3, G))], 10.4), 0.0, .35)
for k, (p_, t_) in enumerate([(E, 1.2), (G, 3.7), (A, 6.2), (G, 8.7)]): put(vibes(mf(n(5, p_)), 2.2), t_, .45, -.3 + .2 * k)
# 10.4-25: harp arpeggio, eighth notes, C - G - Am - F - C - G, bass on the bar
prog = [(C, [C, E, G]), (G, [G, B, D]), (A, [A, C, E]), (F, [F, A, C]), (C, [C, E, G]), (G, [G, B, D])]
for i in range(6):
    root, ch = prog[i]; bt = 10.4 + i * bar
    put(pizz(mf(n(2, root)), .9), bt, .6); put(pizz(mf(n(2, root)), .7), bt + 2 * BEAT, .45)
    for k in range(8): put(pluck(mf(n(4 + (k % 3 == 2), ch[k % 3])), 1.0, 1), bt + k * BEAT / 2, .26, -.4 + .1 * k % .8)
# 25.4-35: sparse, bowed pad (Am / F), slow vibraphone, a glockenspiel motif when the stopwatch runs
put(pad([mf(n(2, A)), mf(n(3, E)), mf(n(4, A))], 5.0), 25.0, .36); put(pad([mf(n(2, F)), mf(n(3, C)), mf(n(4, F))], 5.0), 30.0, .36)
for k, (p_, off) in enumerate([(E, 0), (G, 1), (A, 2), (G, 3.5)]): put(glock(mf(n(5, p_)), 1.2), 29.9 + off * BEAT, .30, .35)
for k, (p_, t_) in enumerate([(E, 26.0), (A, 28.4), (G, 32.0)]): put(vibes(mf(n(4, p_)), 2.4, 1, False), t_, .30, .3)
# 35.3-47: the machine: bass eighths climbing, a pizzicato ostinato, glockenspiel on the rings
for k in range(22): put(pizz(mf(n(2, [A, A, C, C, D, D, E, E, F, F, G][k % 11])), .5), 35.4 + k * BEAT * .5, .50 - .02 * (k % 2))
for k, p_ in enumerate([E, D, C, E, G, A]): put(glock(mf(n(6, p_)), 1.0), 40.0 + k * BEAT, .26, -.2 + .1 * k)
put(pad([mf(n(2, A)), mf(n(3, E))], 11.0), 35.3, .26)
# 47-58.5: calm F - Em - Dm - C bars, vibraphone arpeggios + pizzicato bass (the station, going down)
prog2 = [(F, [F, A, C]), (E, [E, G, B]), (D, [D, F, A]), (C, [C, E, G])]
for i in range(4):
    root, ch = prog2[i]; bt = 47.6 + i * bar * 1.1
    put(pizz(mf(n(2, root)), .9), bt, .55); put(pizz(mf(n(2, root)), .8), bt + 2 * BEAT, .4)
    for k in range(8): put(vibes(mf(n(4 + (k % 3 == 2), ch[k % 3])), 1.0, 1, True), bt + k * BEAT / 2, .22, -.3 + (k % 4) * .2)
put(pad([mf(n(3, F)), mf(n(4, A))], 10.0), 47.5, .24)
# 58.7-66.6: resolve in C, harp sweep, glockenspiel on the joke
put(pad([mf(n(2, C)), mf(n(3, G)), mf(n(4, E))], 8.0), 58.6, .40)
for k, p_ in enumerate([C, G, E, G, C, E, G, C]): put(pluck(mf(n(4 + k // 3, p_)), 1.4), 59.0 + k * .26, .30, -.5 + k * .12)
for k, p_ in enumerate([C, E, G, C]): put(glock(mf(n(5 + (k == 3), p_)), 1.4), 63.8 + k * BEAT / 2, .30, .2)
# closing card: resolve on C major, bells on like / share / subscribe
put(pad([mf(n(2, C)), mf(n(3, G)), mf(n(4, E))], 7.4), 66.6, .40)
for k, (p_, t_) in enumerate([(C, T_LIKE), (E, T_SHARE), (G, T_SUB)]): put(glock(mf(n(6, p_)), 1.6), t_, .30, -.2 + .3 * k)
put(glock(mf(n(6, C)), 3.0), T_SUB + 1.6, .30, 0)
mus = S.limit(mus[:, 0], .8)[:, None].repeat(2, 1) * 0 + mus * 1.0

# ---------------- foley from the picture events ----------------
fol = np.zeros((N, 2))
def F_(x, at, g=1.0, pan=0.0): S.add(fol, x.astype(np.float64), at, g, pan)
def L2(*a):
    m = min(len(x) for x in a); return [x[:m] for x in a]
def glide(f0, f1, d, v=1.0):
    t = tt(d); f = f0 * (f1 / f0) ** (t / d); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(t / .03, 1) * np.minimum((d - t) / .06, 1) * v
for e in EV:
    t0, ty, d, pan = e['t'], e['type'], e.get('d', .4), e.get('pan', 0); p1 = e.get('pan1', pan)
    if ty == 'swell': F_(S.lp(glide(380, 900, d, .5), 2500), t0, .10, pan)
    elif ty == 'plink':
        a_ = glide(1900, 700, .14, .6) * S.env_exp(.14, .05); b_ = S.bp(S.noise(.05), 1500, 6000) * S.env_exp(.05, .012) * .3; a_[:len(b_)] += b_; F_(a_, t0, .30, pan)
    elif ty == 'type':
        for k in range(int(d * 14)): F_(tick(1), t0 + k * d / (d * 14), .10, pan + .05 * (k % 3))
    elif ty == 'sweep': F_(S.bp(S.noise(d), 700, 2600, 2) * np.hanning(int(d * SR)), t0, .10, pan)
    elif ty == 'tick': F_(S.click(1.35, .8)[:int(.04 * SR)] * .6, t0, .14, pan)
    elif ty == 'zip': F_(S.lp(glide(420, 2200, d, .5), 4000) * np.hanning(int(d * SR)) ** .5, t0, .07, pan)
    elif ty == 'ruler':
        for k in range(14): F_(S.click(1.1 + .02 * k, .6)[:int(.03 * SR)], t0 + (k ** 1.4) * d / 14 ** 1.4, .10, pan)
    elif ty == 'barsdown': F_(S.lp(glide(1100, 420, d, .4), 3000), t0, .08, pan)
    elif ty in ('tip', 'rejoin'): F_(S.whoosh(d, .6), t0, .13, pan)
    elif ty == 'co2': F_(S.lp(S.noise(.05), 900) * S.env_exp(.05, .012) * 2, t0, .09, pan)
    elif ty == 'latch': F_(S.clack(.9, .9), t0, .26, pan)
    elif ty == 'air': F_(S.bp(S.noise(d), 300, 1600) * np.hanning(int(d * SR)), t0, .07, pan)
    elif ty == 'lift': F_(S.whoosh(d, .7), t0, .15, pan)
    elif ty == 'seat': F_(S.click(.9, .8), t0, .24 * e.get('v', .8), pan); F_(S.thump(.5, 80), t0, .10, pan)
    elif ty == 'dive': a_, b_, c_ = L2(S.rumble(d, .5), S.bp(S.noise(d), 1500, 5000), np.linspace(0, 1, int(d * SR)) ** 2); F_(a_ * .7 + b_ * c_ * .5, t0, .12, pan)
    elif ty == 'iris': F_(S.whoosh(d, .8), t0, .16, pan); F_(glide(900, 1400, .3, .5) * S.env_exp(.3, .12), t0 + .05, .08, pan)
    elif ty == 'glass': F_(S.ding(.8), t0, .18, pan)
    elif ty == 'pop': F_(S.pop(.7), t0, .15, pan)
    elif ty == 'flood': F_(S.lp(glide(300, 1100, d, .6), 3500) * np.hanning(int(d * SR)), t0, .10, pan)
    elif ty == 'drain': F_(S.lp(glide(1100, 300, d, .6), 3500) * np.hanning(int(d * SR)), t0, .10, pan)
    elif ty == 'whoosh': F_(S.whoosh(d, .7), t0, .12, pan)
    elif ty == 'train': a_, b_, h_ = L2(S.rumble(d, .6), S.bp(S.noise(d), 600, 2400), np.hanning(int(d * SR))); F_(a_ * h_ ** .5 * .8 + b_ * h_ ** 2 * .35, t0, .13, (pan + p1) / 2)
    elif ty == 'trace': F_(S.lp(glide(500, 2400, d, .5), 5000) * np.hanning(int(d * SR)) ** .6, t0, .08, pan)
# room tone (very quiet), present through the near-silences
room = np.zeros((N, 2)); r_ = S.lp(S.noise(DUR), 400) * .02; room[:, 0] = r_[:N]; room[:, 1] = S.lp(S.noise(DUR), 400)[:N] * .02

# ---------------- narration: compress, place ----------------
voice = np.zeros((N, 2))
for vid, st in TL['vo'].items():
    w, sr = sf.read(os.path.join(HERE, 'voice', vid + '.wav'))
    if w.ndim > 1: w = w.mean(1)
    w = resample_poly(w, SR, sr) if sr != SR else w
    w = S.compress(w * 1.0, thr=.22, ratio=3.2); S.add(voice, w.astype(np.float64), st, 1.0, 0.0)
voice *= .72 / max(np.abs(voice).max(), 1e-6)
# ---------------- duck + balance (voice about 10 dB above music + foley by RMS) ----------------
env = np.abs(voice[:, 0]); k = int(.12 * SR); env = np.convolve(env, np.ones(k) / k, 'same'); speak = np.clip(env / (env.max() * .12), 0, 1)
def duck_mid(x, amt):                                   # music yields 300 Hz-4 kHz while the voice speaks
    out = x.copy()
    for ch in range(2):
        lo = S.lp(x[:, ch], 300); mid = S.bp(x[:, ch], 300, 4000); hi = S.hp(x[:, ch], 4000); out[:, ch] = lo + mid * (1 - amt * speak) + hi * (1 - .5 * amt * speak)
    return out
mus_d = duck_mid(mus, .8); fol_d = fol * (1 - .35 * speak[:, None])
rms = lambda x, m: np.sqrt(np.mean(x[m] ** 2) + 1e-12)
m = speak > .5
bed = mus_d + fol_d + room
g = rms(voice, m) / rms(bed, m) / (10 ** (10 / 20))             # voice 10 dB over the bed
mix = voice + bed * g
mix = np.stack([S.limit(mix[:, 0], .92), S.limit(mix[:, 1], .92)], 1)
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
sf.write(os.path.join(HERE, 'out', 'mix.wav'), mix.astype(np.float32), SR)
print('mix ok; voice over bed (dB):', round(20 * np.log10(rms(voice, m) / rms(bed * g, m)), 1))
