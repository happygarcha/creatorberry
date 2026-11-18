"""Mix: narration + dialogue (local Kokoro TTS, natural speed 1.0), Lily's recording FX, synthesised SFX tied to the same motion functions as the animation, ducked music bed.
Outputs audio/narration.wav, audio/dialogue.wav, audio/sfx_music.wav, audio/final_mix.wav (60.0 s, 48 kHz stereo) + audio/mix_stats.json."""
import os, sys, json, numpy as np, soundfile as sf
from scipy import signal
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
SR = 48000; TOTAL = 60.0; N = int(SR * TOTAL)
rng = np.random.default_rng(7)
LINE_T = {'n1a': .5, 'n1b': 4.5, 'r1': 11.3, 'm1': 17.3, 'n2': 23.6, 'm2': 36.4, 'r2': 45.4, 'n3': 47.9, 'g1': 55.0}
WHO = {'n1a': 'N', 'n1b': 'N', 'n2': 'N', 'n3': 'N', 'r1': 'D', 'r2': 'D', 'm1': 'D', 'm2': 'D', 'g1': 'G'}
GAIN = {'N': 1.0, 'D': 1.0, 'G': .72}

def load(p):
    x, sr = sf.read(p); x = x if x.ndim == 1 else x.mean(1)
    if sr != SR: x = signal.resample_poly(x, SR, sr)
    return x.astype(np.float64)
def norm_rms(x, db=-20.0):
    r = np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2)); return x * (10 ** (db / 20) / r)
def place(buf, x, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(x));
    if i < N and j > i: buf[i:j] += x[:j - i] * g
def bp(x, lo, hi, o=2): return signal.sosfilt(signal.butter(o, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def lp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'high', fs=SR, output='sos'), x)
def env(n, a, d, p=2.0): t = np.arange(n) / SR; return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d) ** 1
def tone(f, dur, decay): t = np.arange(int(dur * SR)) / SR; return np.sin(2 * np.pi * f * t) * np.exp(-t / decay)

# ---------------- voices
voices = {k: np.zeros(N) for k in 'NDG'}
for lid, t in LINE_T.items():
    x = norm_rms(load(f'audio/{lid}.wav'))
    if WHO[lid] == 'G':    # Lily's recorded voice: thin, band-limited, slightly degraded, with hiss
        x = bp(x, 300, 3800, 2); x = signal.resample_poly(signal.resample_poly(x, 1, 3), 3, 1)[:len(x)]
        x = np.tanh(x * 1.15) * .9 + .05 * hp(rng.standard_normal(len(x)), 2500) * (np.abs(x) > .004).astype(float) * 0 + 0
        x = norm_rms(x, -21.5) + .004 * rng.standard_normal(len(x)) * np.hanning(len(x))
    place(voices[WHO[lid]], x, t, GAIN[WHO[lid]])
sf.write('audio/narration.wav', voices['N'], SR); sf.write('audio/dialogue.wav', voices['D'] + voices['G'], SR)
vo = voices['N'] + voices['D'] + voices['G']

# ---------------- SFX
sfx = np.zeros(N)
def foot(t, who, v=1.0):
    n = int(.16 * SR); tt = np.arange(n) / SR
    thump = np.sin(2 * np.pi * (88 if who == 'R' else 112) * tt) * np.exp(-tt / .035)
    scuff = bp(rng.standard_normal(n), 700, 3800) * np.exp(-tt / .02) * .5
    place(sfx, (thump + scuff) * .55 * v * (0.8 + .4 * rng.random()), t)
def creak(t, dur=.9, f0=210, f1=330, g=.22):
    n = int(dur * SR); tt = np.arange(n) / SR; f = f0 + (f1 - f0) * np.sin(np.pi * tt / dur) ** 1.2
    ph = 2 * np.pi * np.cumsum(f + 7 * np.sin(2 * np.pi * 23 * tt)) / SR
    x = (2 * ((ph / (2 * np.pi)) % 1) - 1) * (1 + .5 * np.sin(2 * np.pi * 31 * tt))
    x = bp(x, 380, 1500, 2) * np.sin(np.pi * tt / dur) ** .8
    place(sfx, x * g, t)
def rustle(t, dur=.28, g=.12): n = int(dur * SR); x = bp(rng.standard_normal(n), 900, 5000) * np.hanning(n) * (1 + .7 * rng.random(n)); place(sfx, x, t, g)
def metal(t, f=1180, g=.3, dec=.14):
    x = tone(f, .6, dec) + .6 * tone(f * 2.31, .6, dec * .6) + .35 * tone(f * 3.9, .6, dec * .4); place(sfx, x * g, t)
def tick(t, g=.16): x = bp(rng.standard_normal(int(.02 * SR)), 2000, 7000) * np.exp(-np.arange(int(.02 * SR)) / SR / .004); place(sfx, x, t, g * 2.5); metal(t, 2300, g * .5, .03)
def scrape(t, dur, g=.3):
    n = int(dur * SR); tt = np.arange(n) / SR; gate = (np.sin(2 * np.pi * (9 + 5 * rng.random()) * tt + 3 * np.sin(2 * np.pi * 1.3 * tt)) > -.2).astype(float)
    x = bp(rng.standard_normal(n), 280, 2600) * (0.55 + .45 * gate) + lp(rng.standard_normal(n), 140) * 2.0
    place(sfx, x * np.hanning(n) ** .5 * (.6 + .4 * np.sin(np.pi * tt / dur)), t, g)
def wind(t, dur, g=.07):
    n = int(dur * SR); x = bp(rng.standard_normal(n), 180, 900) ; m = .5 + .5 * np.sin(2 * np.pi * .23 * np.arange(n) / SR + 1) + .3 * np.sin(2 * np.pi * .61 * np.arange(n) / SR); place(sfx, x * np.clip(m, .1, 1.2) * np.hanning(n) ** .3, t, g)
def hum(t, dur, g=.04):
    n = int(dur * SR); tt = np.arange(n) / SR; x = np.sin(2 * np.pi * 60 * tt) + .6 * np.sin(2 * np.pi * 120 * tt) + .3 * np.sin(2 * np.pi * 180 * tt) + .12 * bp(rng.standard_normal(n), 2000, 5000) * (1 + np.sin(2 * np.pi * 120 * tt))
    place(sfx, x * np.minimum(np.minimum(tt / 2.5, 1), (dur - tt) / .3) , t, g)
def sting(t, g=.4):
    n = int(2.4 * SR); tt = np.arange(n) / SR; x = (np.sin(2 * np.pi * 55 * tt) + .8 * np.sin(2 * np.pi * 58.3 * tt) + .6 * np.sin(2 * np.pi * 77.8 * tt) + .35 * np.sin(2 * np.pi * 220 * tt * (1 + .004 * np.sin(2 * np.pi * 5 * tt))))
    x = x * np.minimum(tt / .06, 1) * np.exp(-tt / .9) + .15 * lp(rng.standard_normal(n), 900) * np.exp(-tt / .6); place(sfx, x, t, g)
def riser(t, dur, g=.12, f0=110, f1=440):
    n = int(dur * SR); tt = np.arange(n) / SR; u = tt / dur; f = f0 * (f1 / f0) ** u
    ph = 2 * np.pi * np.cumsum(f) / SR; x = np.sin(ph) + .5 * np.sin(2.01 * ph) + .3 * np.sin(3 * ph)
    nz = bp(rng.standard_normal(n), 400, 4000) * u ** 2 * .6
    place(sfx, (x * .5 + nz) * u ** 1.6 * np.minimum((dur - tt) / .05 + 0, 1), t, g)
def static(t, dur, g=.07):
    n = int(dur * SR); tt = np.arange(n) / SR; x = hp(rng.standard_normal(n), 900) * (.35 + .65 * (rng.random(n // 480 + 2).repeat(480)[:n] > .55)); place(sfx, x * np.minimum(tt / .03, 1), t, g)
def click(t, g=.5): n = int(.012 * SR); x = (rng.standard_normal(n) * np.exp(-np.arange(n) / SR / .002)); place(sfx, bp(x, 1500, 9000), t, g * 4); metal(t + .004, 3100, .12, .02)

ev = json.load(open('audio/events.json'))
for e in ev:
    if e['k'] == 'step': foot(e['t'], e['who'], 1.0 if e['t'] < 41 else .8)
for t in (1.9, 3.3, 5.2, 6.4): creak(t, .8, 190 + 40 * rng.random(), 300 + 60 * rng.random())
creak(9.6, .5, 220, 300, .15)
wind(0, 8.6, .09); wind(8.4, 3.0, .03)
rustle(10.0, .35); rustle(10.35, .22, .09); rustle(11.1, .3, .1)                                   # crouch / turn
metal(12.4, 1180, .28); metal(12.9, 1260, .26)                                                       # fingertip taps on the bolt head
sting(16.85, .55); riser(15.2, 1.7, .05, 90, 180)
for T0 in (23.4, 25.3):                                                                              # wrench: pull from the pocket, ratchet strokes, lift, bolt drops
    rustle(T0 - .35, .18, .1); metal(T0 + .15, 1500, .12, .05)
    for k in range(4):
        base = T0 + .7 + k * (1.2 / 4) + .55 * (1.2 / 4) * 0
        for m in range(5): tick(base + m * .028, .13)
    metal(T0 + 2.4 + .3, 2100, .22, .06); metal(T0 + 2.4 + .42, 1700, .14, .05); metal(T0 + 2.4 + .52, 1500, .08, .04)
rustle(26.1, .35, .1); rustle(26.7, .3, .1); rustle(27.6, .3, .1); rustle(28.1, .26, .1)
scrape(28.35, 2.6, .34); metal(28.4, 520, .1, .25)
rustle(30.8, .4, .1); rustle(31.9, .3, .08)
click(33.55, .35); metal(33.85, 700, .18, .08)                                                       # handle turns
creak(34.3, 2.5, 150, 330, .30); creak(34.9, 1.0, 240, 380, .12)                                     # door on its hinges
riser(34.4, 6.7, .07, 90, 380)
hum(41.0, 19.0, .03)
riser(41.0, 11.0, .06, 70, 260)
rustle(50.6, .4, .12); rustle(51.4, .3, .1)                                                          # picks the recorder up
click(52.42, .55); static(52.55, 2.45, .09); static(54.95, 5.0, .008)                               # play pressed, hiss, then the voice rides on faint static
rustle(55.0, .3, .12)
sf.write('audio/sfx_only.wav', sfx, SR)

# ---------------- music bed (dark drone + sparse pulse), stops dead at 54.95
music = np.zeros(N); tt = np.arange(N) / SR
pad = np.zeros(N)
for f, a in ((55, 1.0), (82.4, .7), (110.2, .35), (164.9, .16)):
    for d in (-.6, 0, .7):
        ph = 2 * np.pi * np.cumsum(f * (1 + d * .002) + .15 * np.sin(2 * np.pi * (.09 + .03 * a) * tt)) / SR
        pad += a * (2 * ((ph / (2 * np.pi)) % 1) - 1)
pad = lp(pad, 520, 2) * (.35 + .65 * (.5 + .5 * np.sin(2 * np.pi * .07 * tt)))
lvl = np.interp(tt, [0, 7, 15, 17, 23, 34, 41, 52.4, 54.9], [.35, .45, .5, .8, .6, .9, 1.0, 1.35, 1.5])
pulse = np.zeros(N)
for k in range(int(41 / 1.6), int(54.9 / 1.6) + 1):
    t0 = 41 + (k - int(41 / 1.6)) * 1.15 * (1 - .012 * (k - int(41 / 1.6)))
    if t0 < 54.9:
        a = tone(52, .5, .12); b = tone(78, .3, .06); a[:len(b)] += .5 * b; place(pulse, a, t0, .5)
sparse = np.zeros(N)
for t0, f in ((3.0, 98), (9.0, 87.3), (19.5, 92.5), (27.5, 98), (37.0, 82.4), (44.0, 87.3)): place(sparse, tone(f, 3.0, 1.1) * np.minimum(np.arange(int(3 * SR)) / SR / .5, 1), t0, .35)
music = (pad * lvl * .55 + pulse * .6 + sparse) * .12
stop = np.clip((54.95 - tt) / .012, 0, 1); music *= stop                                                # sudden musical stop
# ---------------- ducking: music strongly, SFX lightly, driven by the voice activity
act = np.sqrt(np.maximum(signal.sosfilt(signal.butter(2, 8, 'low', fs=SR, output='sos'), vo ** 2), 0)); act = np.clip(act / (np.percentile(act, 97) + 1e-9), 0, 1)
duck_m = 1 - .94 * np.clip(np.convolve(act, np.ones(2400) / 2400, 'same') * 3, 0, 1)
duck_s = 1 - .93 * np.clip(np.convolve(act, np.ones(2400) / 2400, 'same') * 3, 0, 1)
mix = vo * 1.0 + music * duck_m + sfx * duck_s * .75
sf.write('audio/sfx_music.wav', music * duck_m + sfx * duck_s * .75, SR)
mix = np.tanh(mix * .9) / np.tanh(.9)
pk = np.max(np.abs(mix)); mix = mix / pk * .89
st = np.c_[mix, mix]; sf.write('audio/final_mix.wav', st, SR, subtype='PCM_16')
# stats: speech vs music/sfx level while speaking
spk = (np.convolve(act, np.ones(4800) / 4800, 'same') > .12)
r = lambda x: 20 * np.log10(np.sqrt(np.mean(x[spk] ** 2)) + 1e-9)
stats = {'voice_dbfs_while_speaking': round(r(vo / pk * .89), 1), 'music_dbfs_while_speaking': round(r(music * duck_m / pk * .89), 1), 'sfx_dbfs_while_speaking': round(r(sfx * duck_s * .75 / pk * .89), 1)}
stats['voice_over_music_db'] = round(stats['voice_dbfs_while_speaking'] - stats['music_dbfs_while_speaking'], 1)
stats['voice_over_music_and_sfx_db'] = round(stats['voice_dbfs_while_speaking'] - 10 * np.log10(10 ** (stats['music_dbfs_while_speaking'] / 10) + 10 ** (stats['sfx_dbfs_while_speaking'] / 10)), 1)
json.dump(stats, open('audio/mix_stats.json', 'w'), indent=1); print(stats)
