"""Original soundtrack for E01, synthesised with numpy only (no samples, no licensed material):
cheerful ukulele/bell music (original 8-bar loop), rolling, footsteps, hops, leaves, giggles, and optional
spoken lines (audio/voices/*.wav, from an open-source TTS if available).  usage: make_audio.py <out.wav>"""
import sys, os, wave, math
import numpy as np
SR = 44100; DUR = 30.0; N = int(SR * DUR)
rng = np.random.default_rng(5)
L = np.zeros(N); R = np.zeros(N)
HERE = os.path.dirname(os.path.abspath(__file__)); VOICES = os.path.join(HERE, "..", "audio", "voices")

def add(sig, t0, gain=1.0, pan=0.0):
    i0 = int(t0 * SR)
    if i0 >= N or i0 + len(sig) <= 0: return
    a = max(0, -i0); b = min(len(sig), N - i0)
    gl = gain * (1 - max(pan, 0)); gr = gain * (1 + min(pan, 0))
    L[i0 + a:i0 + b] += sig[a:b] * gl; R[i0 + a:i0 + b] += sig[a:b] * gr

def env_ad(n, a=0.005, d=0.1):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1.0) * np.exp(-t / d)

def pluck(freq, dur=0.6, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for k in range(1, 9):
        s += (1.0 / k ** (1.2 / bright)) * np.sin(2 * np.pi * freq * k * t) * np.exp(-t * (5 + 4 * k) / (dur * 1.5))
    return s * np.minimum(t / 0.003, 1) * 0.5

def bell(freq, dur=0.9):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.4 * np.sin(2 * np.pi * freq * 2.76 * t) * np.exp(-t * 8) + 0.2 * np.sin(2 * np.pi * freq * 5.4 * t) * np.exp(-t * 14)
    return s * np.exp(-t * 4.5) * np.minimum(t / 0.002, 1) * 0.35

def midi(n): return 440.0 * 2 ** ((n - 69) / 12.0)

def noise_bp(n, lo, hi):
    x = rng.standard_normal(n); X = np.fft.rfft(x); fr = np.fft.rfftfreq(n, 1 / SR)
    X *= ((fr > lo) & (fr < hi)); return np.fft.irfft(X, n)

# ------------------------------------------------------------------ music: C - Am - F - G, 120 bpm, 15 bars
BEAT = 0.5
chords = [(48, [60, 64, 67]), (45, [57, 60, 64]), (41, [57, 60, 65]), (43, [55, 59, 62])]
melody = [76, 79, 81, 79, 76, 72, 74, 76,  77, 76, 72, 69, 72, 76, 74, 72,
          72, 74, 76, 77, 79, 77, 76, 74,  74, 76, 79, 83, 81, 79, 76, 74]
for bar in range(15):
    base, ch = chords[bar % 4]; t0 = bar * 4 * BEAT
    for b in (0, 2):   # bass on 1 and 3
        add(pluck(midi(base), 0.7, 0.8) * 0.8, t0 + b * BEAT, 0.20)
    for b in range(8):  # strummed ukulele eighths
        tt = t0 + b * BEAT / 2 + (0.012 if b % 2 else 0)
        for k, nn in enumerate(ch):
            add(pluck(midi(nn + 12), 0.35, 1.2), tt + k * 0.008, 0.075 * (1.0 if b % 2 == 0 else 0.7), pan=-0.2 + 0.2 * k)
    for b in range(4):   # shaker on offbeats
        add(noise_bp(int(0.06 * SR), 5000, 12000) * env_ad(int(0.06 * SR), 0.002, 0.02), t0 + b * BEAT + BEAT / 2, 0.05)
    for i in range(8):   # bell melody
        nn = melody[(bar * 8 + i) % len(melody)]
        if (bar * 8 + i) % 5 != 3: add(bell(midi(nn)), t0 + i * BEAT / 2, 0.07, pan=0.25)

# ------------------------------------------------------------------ voices / giggles
def formant_voice(f0_start, f0_end, dur, F=(850, 1900), bw=(250, 350), vib=0.0):
    n = int(dur * SR); t = np.arange(n) / SR
    f0 = np.linspace(f0_start, f0_end, n) * (1 + vib * np.sin(2 * np.pi * 6 * t))
    ph = 2 * np.pi * np.cumsum(f0) / SR
    s = np.zeros(n)
    for k in range(1, 26):
        fk = k * f0
        amp = sum(np.exp(-0.5 * ((fk - Fc) / b) ** 2) for Fc, b in zip(F, bw)) + 0.02
        s += amp * np.sin(k * ph)
    return s * np.sin(np.pi * np.arange(n) / n) ** 0.7 * 0.18

def giggle(t0, f0, dur, gain=0.5, pan=0.0, vowel=(850, 1900)):
    t = 0.0; i = 0
    while t < dur:
        d = 0.085
        add(formant_voice(f0 * (1.05 - 0.03 * i % 0.15), f0 * 0.88, d, vowel) , t0 + t, gain * (1 - 0.35 * t / dur), pan)
        add(noise_bp(int(0.03 * SR), 3000, 8000) * env_ad(int(0.03 * SR), 0.002, 0.01), t0 + t, 0.02 * gain, pan)
        t += 0.145 + 0.01 * ((i * 7) % 3); i += 1

def voice_file(name, t0, gain=1.0, pitch=1.0, pan=0.0):
    p = os.path.join(VOICES, name)
    if not os.path.exists(p): return False
    with wave.open(p) as w:
        ch = w.getnchannels(); sr = w.getframerate(); d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    if ch > 1: d = d.reshape(-1, ch).mean(1)
    k = pitch * sr / SR; idx = np.arange(0, len(d) - 1, k); d = np.interp(idx, np.arange(len(d)), d)
    d = d / (np.abs(d).max() + 1e-9) * 0.9
    add(d, t0, gain, pan); return True

def chirp_word(t0, f0, dur, gain=0.5, pan=0.0, vowels=((700, 1700), (400, 2200)), contour=(1.0, 1.25)):
    """fallback 'voice' when no TTS lines available: expressive vowel gliding sound (not intelligible speech)"""
    n = int(dur * SR); parts = []
    for i, v in enumerate(vowels):
        parts.append(formant_voice(f0 * contour[0], f0 * contour[1] if i == len(vowels) - 1 else f0, dur / len(vowels), v))
    add(np.concatenate(parts), t0, gain, pan)

# ---- timeline (seconds = frame/30)
giggle(1.55, 480, 1.7, 0.55, 0.3, (800, 2000))      # Pip, after tap
giggle(1.75, 360, 1.5, 0.5, -0.3, (900, 1700))      # Milo
giggle(3.0, 480, 0.6, 0.35, 0.3)
if not voice_file("milo_oops.wav", 8.20, 1.0, 1.3, -0.2): chirp_word(8.2, 330, 0.55, 0.7, -0.2, ((600, 1100), (350, 2000)), (1.0, 1.3))
chirp_word(8.9, 520, 0.18, 0.4, 0.3, ((500, 1800),), (1.0, 1.2))             # Pip 'huh?'
if not voice_file("pip_whoa.wav", 20.05, 1.0, 1.65, 0.3): chirp_word(20.0, 520, 0.45, 0.7, 0.3, ((700, 1500), (500, 1300)), (1.3, 0.8))
giggle(21.3, 500, 2.4, 0.6, 0.3, (800, 2000))
if not voice_file("milo_check.wav", 22.2, 1.0, 1.3, -0.2): chirp_word(22.2, 340, 0.6, 0.6, -0.2, ((700, 1500), (450, 1900)), (1.0, 1.15))
giggle(23.3, 380, 1.2, 0.4, -0.2, (900, 1700))
if not voice_file("milo_gotit.wav", 25.3, 1.0, 1.3, -0.1): chirp_word(25.3, 350, 0.45, 0.6, -0.1, ((650, 1300), (800, 1700)), (1.0, 1.2))
giggle(26.0, 500, 1.4, 0.5, 0.3)
if not voice_file("milo_team.wav", 28.1, 1.0, 1.3, -0.3): chirp_word(28.1, 340, 0.6, 0.6, -0.3, ((500, 1700), (700, 1300)), (1.0, 1.2))
if not voice_file("both_yay.wav", 28.8, 1.0, 1.3, 0.0): chirp_word(28.9, 420, 0.5, 0.8, 0.0, ((800, 1900),), (1.0, 1.3))
chirp_word(28.9, 560, 0.5, 0.55, 0.3, ((800, 2000),), (1.0, 1.3))

# ------------------------------------------------------------------ SFX
def roll(t0, t1, g0, g1):
    n = int((t1 - t0) * SR); x = noise_bp(n, 150, 1800)
    e = np.linspace(g0, g1, n) * (0.7 + 0.3 * np.sin(2 * np.pi * 5.5 * np.arange(n) / SR))
    add(x * e, t0, 1.0, 0.0)
roll(0.5, 1.5, 0.0, 0.05); roll(1.5, 4.0, 0.05, 0.03); roll(4.0, 9.0, 0.05, 0.16); roll(9.0, 15.0, 0.16, 0.07)
roll(15.3, 18.4, 0.1, 0.1); roll(18.4, 25.0, 0.08, 0.05); roll(25.0, 25.3, 0.04, 0.0)
def thump(t0, g=0.3, lo=90, pan=0.0):
    n = int(0.09 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (lo + 40 * np.exp(-t * 60)) * t) * np.exp(-t * 45) + 0.25 * noise_bp(n, 400, 2500) * np.exp(-t * 60)
    add(s, t0, g, pan)
# Milo run (alternating feet, ~0.17 s apart), 9.6 -> 21.2 s and 23.4 -> 24.7
for tt in np.arange(9.7, 21.2, 0.173): thump(tt, 0.16, 110, -0.2)
for tt in np.arange(23.4, 24.9, 0.173): thump(tt, 0.14, 110, -0.2)
for tt in np.arange(26.7, 27.2, 0.3): thump(tt, 0.08, 110, 0.0)
# Pip hops: stance contacts every 14 frames from f=292+10
for k in range(22): thump((292 + 14 * k + 10) / 30.0, 0.26, 75, 0.2)
# bridge bounces
thump(458 / 30 + 0.2, 0.3, 160); thump(548 / 30 + 0.2, 0.25, 160)
# leaves
def leaves(t0, dur, g):
    n = int(dur * SR); x = noise_bp(n, 2000, 9000) * np.abs(noise_bp(n, 1, 25)) * 4
    add(x * np.exp(-np.arange(n) / SR * 3.0), t0, g)
leaves(600 / 30 + 0.45, 1.5, 0.35); leaves(21.3, 1.8, 0.18); leaves(23.0, 0.8, 0.12)
# ball into basket + basket lift/set-down
thump(752 / 30, 0.25, 220); thump(790 / 30, 0.12, 130); thump(803 / 30, 0.2, 130)
# high-five clap
def clap(t0, g):
    n = int(0.12 * SR); add(noise_bp(n, 1200, 6000) * np.exp(-np.arange(n) / SR * 45), t0, g)
clap(866 / 30, 0.6)
# whoosh at the cuts, subtle
for f in (120, 240, 300, 450, 600, 750, 840):
    n = int(0.25 * SR); x = noise_bp(n, 600, 3000) * np.sin(np.pi * np.arange(n) / n) ** 2
    add(x, f / 30 - 0.12, 0.05)

# ------------------------------------------------------------------ master
fade = np.ones(N); k = int(0.4 * SR); fade[-k:] = np.linspace(1, 0, k); fade[:int(0.02 * SR)] = np.linspace(0, 1, int(0.02 * SR))
L *= fade; R *= fade
pk = max(np.abs(L).max(), np.abs(R).max(), 1e-9); g = 0.89 / pk
st = np.stack([L * g, R * g], 1); pcm = (np.clip(st, -1, 1) * 32767).astype('<i2')
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("wrote", sys.argv[1], DUR, "s")
