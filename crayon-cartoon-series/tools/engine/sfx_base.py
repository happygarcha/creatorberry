import json, subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
SR = 48000
rng = np.random.default_rng(3)
def env(n, a=.005, d=.2):
    t = np.arange(n) / SR
    return np.exp(-t / max(d, 1e-4)) * np.minimum(1, t / max(a, 1e-4))
def filt(x, f, kind, o=2): return sosfilt(butter(o, f, btype=kind, fs=SR, output='sos'), x)
def sine(f, d):
    n = int(d * SR)
    return np.sin(2 * np.pi * np.cumsum(np.broadcast_to(f, (n,))) / SR)
def noise(d): return rng.standard_normal(int(d * SR))
def tick(f=2200, d=.03, g=.3): return g * sine(f, .06) * env(int(.06 * SR), .001, d)
def click(g=.5): return g * filt(noise(.02), 2500, 'high') * env(int(.02 * SR), .0005, .004)
def thud(f=65, g=.8, d=.15):
    n = int(.35 * SR)
    return g * (sine(f * (1 + 1.5 * np.exp(-np.arange(n) / SR / .03)), .35) * env(n, .002, d) + .25 * filt(noise(.35), 400, 'low') * env(n, .001, .03))
def whoosh(d=.45, g=.4, lo=300, hi=4000):
    n, x, out = int(d * SR), noise(d), np.zeros(int(d * SR))
    for i in range(0, n, 256):
        fc = lo + (hi - lo) * np.sin(np.pi * i / n)
        out[i:i + 256] = filt(x[max(0, i - 2048):i + 256], [max(60, fc * .5), min(20000, fc * 1.5)], 'band')[-len(x[i:i + 256]):]
    return g * out * np.sin(np.pi * np.arange(n) / n) ** 1.5
def chime(f=880, g=.3, d=1.1):
    n = int(d * SR)
    return g * sum(a * sine(f * m, d) * env(n, .002, d * dd) for m, a, dd in ((1, 1, .5), (2.01, .5, .3), (3.02, .25, .2)))
def place(buf, x, t, gain=1.0, pan=0.0):
    s = int(t * SR)
    if 0 <= s < len(buf):
        x = x[:len(buf) - s]
        buf[s:s + len(x), 0] += x * gain * np.cos((pan + 1) * np.pi / 4) * 1.414
        buf[s:s + len(x), 1] += x * gain * np.sin((pan + 1) * np.pi / 4) * 1.414
def mix(vo_wav, fx, bed, out_wav, duck=.45):
    """fx/bed: (n,2) float arrays at 48 kHz. Bed is ducked under the voice; final file loudness-normalised to -14 LUFS (YouTube)."""
    n = len(fx)
    vo, vsr = sf.read(vo_wav, dtype='float32')
    vo = resample_poly(vo, SR, vsr)[:n]
    vo = np.pad(vo, (0, n - len(vo))) / (np.sqrt(np.mean(vo[np.abs(vo) > .01] ** 2)) + 1e-9) * .16
    d = 1 - duck * np.clip(filt(np.abs(vo), 8, 'low') / .05, 0, 1)
    o = np.tanh((vo[:, None] + fx * .55 + bed * d[:, None]) * 1.1) / 1.1
    sf.write(out_wav + '.tmp.wav', (o * .89 / np.max(np.abs(o))).astype(np.float32), SR)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out_wav + '.tmp.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', str(SR), out_wav], check=True)
