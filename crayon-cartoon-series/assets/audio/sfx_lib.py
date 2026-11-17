"""Sound-effect library: every effect is synthesised with numpy (no third-party samples, so no licence issues).
`python3 sfx_lib.py` renders all effects to assets/audio/sfx/<name>.wav so they can be auditioned or replaced by real samples
(a real <name>.wav in $SFX_DIR wins, see engine/sfx_cc.py). `make(name)` returns a mono float array at 48 kHz."""
import os, sys
ENGINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'engine')
if ENGINE not in sys.path: sys.path.insert(0, ENGINE)
from sfx_cc import *          # SR, noise, filt, env, sine, tick, click, thud, whoosh, chime, pop, paper, ding, coins, crowd, phone, tone ...


def _fit(x, n): return np.pad(x, (0, max(0, n - len(x))))[:n]


def _sum(*xs):
    n = max(len(x) for x in xs); return sum(_fit(x, n) for x in xs)


def _pad(parts, total):
    out = np.zeros(int(total * SR))
    for t, x, g in parts:
        s = int(t * SR); x = x[:max(0, len(out) - s)]; out[s:s + len(x)] += g * x
    return out


def squeak():                      # empty-wallet squeak: two rising/falling chirps
    n = int(.34 * SR); t = np.arange(n) / SR
    f = 900 + 900 * np.sin(np.pi * np.clip(t / .16, 0, 1)) * (t < .16) + (t >= .17) * (1500 - 2500 * (t - .17))
    return .3 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, np.minimum(t / .01, (.34 - t) / .06))


def coin_bounce():                 # a coin dropping and bouncing with shrinking gaps
    out = np.zeros(int(1.4 * SR)); t = 0.0; gap = .32; g = .5
    while gap > .05:
        x = chime(3100 - 400 * (gap < .15), g, .35); s = int(t * SR); out[s:s + len(x)] += x[:len(out) - s]
        t += gap; gap *= .62; g *= .72
    return out


def record_scratch():
    d = .55; n = int(d * SR); t = np.arange(n) / SR
    x = filt(noise(d), [600, 6000], 'band') * (np.sin(2 * np.pi * 14 * t) > -.3) * np.exp(-t / .3)
    sweep = np.sin(2 * np.pi * np.cumsum(400 + 1800 * (1 - t / d)) / SR) * np.exp(-t / .25)
    return .45 * (.8 * x + .4 * sweep) * np.minimum(1, (d - t) / .05)


def button_click(): return .6 * _sum(click(1), .5 * thud(120, .5, .05)[:int(.2 * SR)])


def whirr(d=3.0):                  # mechanical printing: motor hum + stutter
    n = int(d * SR); t = np.arange(n) / SR
    motor = np.sin(2 * np.pi * (70 + 20 * np.sin(2 * np.pi * 3 * t)) * t) * .5 + filt(noise(d), [200, 1800], 'band') * (.5 + .5 * (np.sin(2 * np.pi * 22 * t) > 0))
    return .3 * motor * np.minimum(1, np.minimum(t / .1, (d - t) / .2))


def register_ding(): return _sum(chime(1568, .35, 1.0), .5 * chime(2093, .3, .9))


def doorbell():
    return _sum(chime(1760, .3, .9), np.pad(chime(1319, .3, .9), (int(.14 * SR), 0)))


def tag_flip(): return _sum(.35 * (filt(noise(.12), [1500, 8000], 'band') * env(int(.12 * SR), .001, .05)), .25 * click(1))


def sting(f=220, d=1.0):           # dramatic orchestral-style stab (stacked detuned saws, low-passed)
    n = int(d * SR); t = np.arange(n) / SR
    x = sum(np.sign(np.sin(2 * np.pi * f * m * t)) * a for m, a in ((1, 1), (1.5, .7), (2.0, .6), (2.52, .5)))
    return .3 * filt(x, 1800, 'low') * np.exp(-t / .45) * np.minimum(1, t / .005)


def thud_big(): return thud(50, .9, .3)


def whistle_up(d=1.4):
    n = int(d * SR); t = np.arange(n) / SR
    return .22 * np.sin(2 * np.pi * np.cumsum(500 + 2200 * (t / d) ** 1.5) / SR) * np.minimum(1, np.minimum(t / .05, (d - t) / .1))


def sad_trombone():
    notes = [(233, .55), (220, .55), (208, .55), (196, 1.2)]
    parts = []; t = 0
    for f, d in notes:
        n = int(d * SR); tt = np.arange(n) / SR
        vib = 1 + (.012 * np.sin(2 * np.pi * 5.5 * tt) if f == 196 else 0) + (-.06 * tt if f == 196 else 0)
        x = sum(a * np.sin(2 * np.pi * f * vib * m * tt) for m, a in ((1, 1), (2, .5), (3, .3), (4, .15)))
        parts.append((t, .22 * filt(x, 1800, 'low') * np.minimum(1, np.minimum(tt / .04, (d - tt) / .08)), 1)); t += d * .95
    return _pad(parts, t + .3)


def alarm(d=2.0):
    n = int(d * SR); t = np.arange(n) / SR
    f = np.where((t % .5) < .25, 880, 660)
    return .2 * np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.minimum(1, np.minimum(t / .02, (d - t) / .1))


def scream(d=1.1):                 # cartoon scream: voiced sawtooth sweeping up then wobbling, formant filtered
    n = int(d * SR); t = np.arange(n) / SR
    f = 600 + 500 * np.minimum(1, t / .3) + 30 * np.sin(2 * np.pi * 9 * t)
    saw = ((np.cumsum(f) / SR) % 1) * 2 - 1
    x = filt(saw, [700, 1400], 'band') + .6 * filt(saw, [2200, 3200], 'band')
    return .45 * x * np.minimum(1, np.minimum(t / .03, (d - t) / .2))


def rattle(d=1.6):
    n = int(d * SR); t = np.arange(n) / SR
    x = filt(noise(d), [150, 1500], 'band') * (np.sin(2 * np.pi * 38 * t) > 0) + .6 * np.sin(2 * np.pi * 96 * t)
    return .3 * x * np.minimum(1, np.minimum(t / .05, (d - t) / .15))


def crash():
    d = 1.2; n = int(d * SR); t = np.arange(n) / SR
    return .55 * (filt(noise(d), 4000, 'low') * np.exp(-t / .35) + .5 * _fit(thud(55, 1, .3), n))


def vault_unlock():
    parts = []
    for k, t in enumerate((0, .28, .55, .95)):
        parts.append((t, _sum(tick(1400 + 350 * k, .05, 1.2) * .7, thud(90, .4, .05)[:int(.2 * SR)] * .6), 1))
    parts.append((1.25, .35 * filt(noise(.6), [100, 600], 'band') * np.minimum(1, np.arange(int(.6 * SR)) / (.2 * SR)), 1))
    return _pad(parts, 1.9)


def creak(d=1.7):
    n = int(d * SR); t = np.arange(n) / SR
    f = 180 + 120 * np.sin(2 * np.pi * 1.4 * t) + 60 * np.sin(2 * np.pi * 7 * t)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .5 + filt(noise(d), [800, 2500], 'band') * .4
    return .22 * filt(x, [150, 2500], 'band') * np.minimum(1, np.minimum(t / .2, (d - t) / .3))


def suspense_sting(d=1.6):
    n = int(d * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 110 * t) + np.sin(2 * np.pi * 116.5 * t) + .6 * np.sin(2 * np.pi * 164.8 * t * (1 + .03 * t))
    return .28 * x * np.minimum(1, np.minimum(t / .2, (d - t) / .6)) + .35 * _fit(thud(45, .6, .5), n)


def cartoon_bell(): return chime(1046, .3, 1.2)
def boing():
    n = int(.5 * SR); t = np.arange(n) / SR
    return .35 * np.sin(2 * np.pi * np.cumsum(300 + 500 * np.sin(2 * np.pi * 7 * t) * np.exp(-t / .2)) / SR) * np.exp(-t / .25)
def gasp():
    n = int(.4 * SR); t = np.arange(n) / SR
    return .3 * filt(noise(.4), [1200, 4500], 'band') * np.sin(np.pi * t / .4) ** 2
def bills_flutter(d=1.2):
    n = int(d * SR); t = np.arange(n) / SR
    return .25 * filt(noise(d), [2000, 9000], 'band') * (np.sin(2 * np.pi * 26 * t) > .1) * np.exp(-t / 1.0)
def foot_steps(n=6, gap=.22):
    return _pad([(k * gap, thud(160, .35, .04)[:int(.15 * SR)], 1) for k in range(n)], n * gap + .2)
def silence(d=.5): return np.zeros(int(d * SR))
def giggle():
    parts = [(k * .13, .3 * np.sin(2 * np.pi * (520 + 40 * (k % 2)) * np.arange(int(.09 * SR)) / SR) * np.hanning(int(.09 * SR)), 1) for k in range(6)]
    return _pad(parts, 1.0)

def unplug_zap():                  # plug yanked: crackle + tiny pop
    d = .45; n = int(d * SR); t = np.arange(n) / SR
    crackle = filt(noise(d), [2500, 9000], 'band') * (np.sin(2 * np.pi * 90 * t) > .2) * np.exp(-t / .12)
    return .5 * crackle + .3 * _fit(pop(.5), n)


def power_down(d=1.1):             # falling sweep as the machine stops
    n = int(d * SR); t = np.arange(n) / SR
    return .3 * np.sin(2 * np.pi * np.cumsum(520 * np.exp(-3.2 * t / d) + 40) / SR) * np.minimum(1, (d - t) / .2) * np.minimum(1, t / .01)


def jet_flyby(d=2.6):
    n = int(d * SR); t = np.arange(n) / SR
    env_ = np.sin(np.pi * t / d) ** 2
    return .35 * filt(noise(d), [200, 2400], 'band') * env_ * (1 + .2 * np.sin(2 * np.pi * 45 * t))


def error_beep(d=.9):
    out = np.zeros(int(d * SR))
    for k in range(3):
        x = .25 * np.sin(2 * np.pi * 880 * np.arange(int(.18 * SR)) / SR) * np.hanning(int(.18 * SR)); s0 = int(k * .27 * SR); out[s0:s0 + len(x)] += x
    return out


def stamp(): return _sum(thud(70, .8, .1), .4 * click(1))


REGISTRY = {
    'phone': lambda: phone(.2, 1.6),
    'jet_flyby': jet_flyby, 'error_beep': error_beep, 'stamp': stamp,
    'unplug_zap': unplug_zap, 'power_down': power_down,
    'squeak': squeak, 'coin_bounce': coin_bounce, 'record_scratch': record_scratch, 'button_click': button_click, 'whirr': whirr,
    'register_ding': register_ding, 'doorbell': doorbell, 'tag_flip': tag_flip, 'sting': sting, 'thud': lambda: thud(60, .7, .15),
    'thud_big': thud_big, 'crowd': lambda: crowd(2.5, .22), 'pop': lambda: pop(.5), 'cartoon_bell': cartoon_bell, 'whistle_up': whistle_up,
    'sad_trombone': sad_trombone, 'alarm': alarm, 'scream': scream, 'rattle': rattle, 'crash': crash, 'vault_unlock': vault_unlock,
    'creak': creak, 'suspense_sting': suspense_sting, 'boing': boing, 'gasp': gasp, 'bills_flutter': bills_flutter,
    'foot_steps': foot_steps, 'whoosh': lambda: whoosh(.4, .35), 'paper': paper, 'giggle': giggle, 'silence': silence,
}


def make(name, **kw):
    x = REGISTRY[name](**kw) if kw else REGISTRY[name]()
    return np.asarray(x, dtype=float)


if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sfx')
    os.makedirs(out, exist_ok=True)
    for k in REGISTRY:
        x = make(k); pk = np.max(np.abs(x)) or 1
        sf.write(os.path.join(out, k + '.wav'), (x / max(1, pk) * .9).astype('float32'), SR)
    print('wrote', len(REGISTRY), 'effects to', out)
