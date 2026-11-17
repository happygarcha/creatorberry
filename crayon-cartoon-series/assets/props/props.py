"""Reusable cartoon props (SVG strings). Anchor = base-centre unless stated. Wrap in animlib.G(..., keys, o=(x, y)) to animate.
Palette matches the engine: thick INK outlines, flat fills."""
import os, sys, math, random
ENGINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'engine')
if ENGINE not in sys.path: sys.path.insert(0, ENGINE)
import animlib
from animlib import G
from cc_kit import (INK, RED, GREEN, GOLD, BLUE, WOOD, WOOD_D, CAPS, SCRIPT, caps, text, g, cash, money_bag, burst, tw)

LW = 4
MUSTARD, DUSTY, CREAM, MUTED_RED = '#E0B24A', '#7C9AB5', '#F3E3BC', '#B8524A'
STEEL, STEEL_D = '#A9B4BC', '#7F8B94'


def wallet(x, y, s=1.0, empty=True):
    """Open brown wallet (anchor = centre). Flip it with rot=180 via G keys to shake the coin out."""
    inner = (f'<rect x="-60" y="-42" width="120" height="84" rx="12" fill="#8A5A3A" stroke="{INK}" stroke-width="{LW}"/>'
             f'<rect x="-52" y="-34" width="104" height="68" rx="8" fill="#6A432A" stroke="{INK}" stroke-width="2.4"/>'
             f'<path d="M-48 -8 H48" stroke="{INK}" stroke-width="2.4" stroke-dasharray="6 5" opacity=".6"/>'
             f'<rect x="38" y="-14" width="26" height="28" rx="6" fill="#D8A43A" stroke="{INK}" stroke-width="3"/>')
    return g(x, y, s, inner)


def coin(x, y, s=1.0):
    return g(x, y, s, f'<circle r="20" fill="#E8B83A" stroke="{INK}" stroke-width="3.4"/><circle r="13" fill="none" stroke="#B88A1E" stroke-width="2.4"/>'
                      + text(0, 1, '$', 22, CAPS, '#8C6414'))


def bread(x, y, s=1.0, col='#D9A05B'):
    """Loaf, anchor = bottom centre."""
    return g(x, y, s, f'<path d="M-44 0 C-56 -4 -54 -34 -30 -42 C-10 -50 10 -50 30 -42 C54 -34 56 -4 44 0 Z" fill="{col}" stroke="{INK}" stroke-width="3.4" stroke-linejoin="round"/>'
                      f'<path d="M-24 -38 L-14 -12 M-4 -42 L6 -14 M16 -40 L26 -14" stroke="{INK}" stroke-width="2.6" stroke-linecap="round" fill="none"/>'
                      f'<ellipse cx="22" cy="-30" rx="14" ry="5" fill="#EAC283" opacity=".7"/>')


def crumb(x, y, s=1.0):
    return g(x, y, s, f'<circle r="5" fill="#D9A05B" stroke="{INK}" stroke-width="2"/>')


def price_tag(x, y, text1, s=1.0, text2=None, flip_t=None, col='#F7F7F5', size=34):
    """Hanging price tag (anchor = top of the string). With text2 + flip_t the tag flips from text1 to text2 at local time flip_t."""
    def face(t):
        return (f'<path d="M-46 10 L-30 -6 H30 L46 10 V54 H-46 Z" fill="{col}" stroke="{INK}" stroke-width="3.4" stroke-linejoin="round"/>'
                f'<circle cx="0" cy="8" r="4" fill="{INK}"/>' + caps(0, 34, t, size))
    base = f'<path d="M0 -60 L0 4" stroke="{INK}" stroke-width="3"/>'
    if text2 is None or flip_t is None:
        return g(x, y, s, base + face(text1))
    f1 = G(face(text1), [[0, {'sx': 1}], [flip_t - .12, {'sx': 1}], [flip_t, {'sx': 0}, 'i'], [flip_t + .01, {'o': 0}]], (0, 30))
    f2 = G(face(text2), [[0, {'o': 0}], [flip_t, {'o': 0, 'sx': 0}], [flip_t + .01, {'o': 1, 'sx': 0}], [flip_t + .16, {'sx': 1}, 'b']], (0, 30))
    return g(x, y, s, base + f1 + f2)


def printer(x, y, s=1.0, spin=None, press=None, label='MONEY\nPRINTER'):
    """Giant comic money-printing machine (anchor = base centre, ~300 wide x 330 tall at s=1).
    spin=(t0, t1) rotates the gears; press=t pushes the red button down at that local time.
    Wrap in G(...) with shake() keys to make it rattle."""
    gear = lambda cx, cy, r: (f'<g transform="translate({cx} {cy})"><circle r="{r}" fill="{STEEL_D}" stroke="{INK}" stroke-width="3.4"/>'
                              + ''.join(f'<rect x="{-r * .16}" y="{-r - 9}" width="{r * .32}" height="14" fill="{STEEL_D}" stroke="{INK}" stroke-width="2.4" transform="rotate({a})"/>' for a in range(0, 360, 45))
                              + f'<circle r="{r * .34}" fill="#5F6A72" stroke="{INK}" stroke-width="2.6"/></g>')
    gears = gear(-86, -150, 34) + gear(-20, -118, 26)
    if spin:
        gears = (G(gear(-86, -150, 34), [[0, {'r': 0}], [spin[0], {'r': 0}], [spin[1], {'r': 1440}, 'l']], (-86, -150)) +
                 G(gear(-20, -118, 26), [[0, {'r': 0}], [spin[0], {'r': 0}], [spin[1], {'r': -1800}, 'l']], (-20, -118)))
    btn = f'<rect x="-8" y="-4" width="64" height="18" rx="6" fill="#8A1F1A" stroke="{INK}" stroke-width="3"/><circle cx="24" cy="-14" r="26" fill="#E0382C" stroke="{INK}" stroke-width="3.6"/><ellipse cx="14" cy="-24" rx="10" ry="6" fill="#F58A80" opacity=".7"/>'
    if press is not None:
        btn = G(btn, [[0, {'ty': 0}], [press, {'ty': 0}], [press + .06, {'ty': 12}, 'o'], [press + .5, {'ty': 12}], [press + .6, {'ty': 0}, 'o']], (24, -14))
    body = (f'<rect x="-150" y="-230" width="300" height="230" rx="22" fill="{STEEL}" stroke="{INK}" stroke-width="{LW}"/>'
            f'<rect x="-150" y="-230" width="300" height="46" rx="22" fill="#8E9BA4" stroke="{INK}" stroke-width="{LW}"/>'
            f'<rect x="-120" y="-90" width="240" height="30" rx="10" fill="#2B2F36" stroke="{INK}" stroke-width="3.4"/>'     # output slot
            f'<rect x="-110" y="-72" width="220" height="10" fill="#14161A"/>'
            + caps(40, -150, label, 30, '#2B2F36')
            + f'<path d="M-150 -40 H150" stroke="{INK}" stroke-width="3" opacity=".5"/>')
    legs = f'<rect x="-120" y="0" width="40" height="22" rx="6" fill="{STEEL_D}" stroke="{INK}" stroke-width="3"/><rect x="80" y="0" width="40" height="22" rx="6" fill="{STEEL_D}" stroke="{INK}" stroke-width="3"/>'
    top = f'<g transform="translate(70 -248)">{btn}</g>'
    return g(x, y, s, legs + body + gears + top)


def bill_burst(x0, y0, n, t0, targets, seed=1, size=(.8, 1.1), fall=True, dur=(.9, 1.5), spin=720, hold=True):
    """n banknotes fly from (x0, y0) to random `targets` boxes [(xmin, xmax, ymin, ymax)] with spin and a gravity-ish arc.
    Keys are LOCAL to the scene. If hold=False they fade out at the end. Returns SVG."""
    rnd = random.Random(seed); out = []
    for i in range(n):
        tx = rnd.uniform(*targets[0][:2]); ty = rnd.uniform(*targets[0][2:])
        d = rnd.uniform(*dur); ts = t0 + i * (0.5 / max(1, n)) * rnd.uniform(.6, 1.4)
        mid_t = ts + d * .45
        keys = [[0, {'o': 0}], [ts, {'o': 0, 'tx': 0, 'ty': 0, 'r': 0}], [ts + .02, {'o': 1}],
                [mid_t, {'tx': (tx - x0) * .6, 'ty': min(ty - y0, 0) - rnd.uniform(60, 180) if fall else ty - y0, 'r': spin * .5}, 'o'],
                [ts + d, {'tx': tx - x0, 'ty': ty - y0, 'r': spin * rnd.choice([-1, 1]) * rnd.uniform(.7, 1.2)}, 'i']]
        if not hold: keys.append([ts + d + .25, {'o': 0}])
        out.append(G(cash(x0, y0, rnd.uniform(*size)), keys, (x0, y0)))
    return ''.join(out)


def bakery(w, floor_y, counter_h=190, wall=None):
    """Bakery interior: back wall details, shelves with loaves, BAKERY sign, counter. Returns (back, counter_front) so a
    character can stand BETWEEN them (back first, then the baker, then counter_front)."""
    cx = w / 2
    back = (f'<rect x="{cx - 150}" y="{floor_y - 560}" width="300" height="72" rx="8" fill="#E8D8A8" stroke="{INK}" stroke-width="{LW}"/>'
            + caps(cx, floor_y - 524, 'BAKERY', 54, '#8A1F1A')
            + f'<rect x="46" y="{floor_y - 398}" width="{w - 92}" height="14" fill="{WOOD}" stroke="{INK}" stroke-width="3"/>'
            + ''.join(bread(80 + k * (w - 160) / 5.0 + 20, floor_y - 398, .62) for k in range(6)))
    front = (f'<rect x="20" y="{floor_y - counter_h}" width="{w - 40}" height="{counter_h}" fill="{WOOD}" stroke="{INK}" stroke-width="{LW}"/>'
             f'<rect x="10" y="{floor_y - counter_h - 16}" width="{w - 20}" height="22" rx="4" fill="#8A5A3A" stroke="{INK}" stroke-width="{LW}"/>'
             + ''.join(f'<rect x="{50 + k * (w - 100) / 3}" y="{floor_y - counter_h + 26}" width="{(w - 100) / 3 - 20}" height="{counter_h - 56}" rx="6" fill="{WOOD_D}" stroke="{INK}" stroke-width="2.6" opacity=".9"/>' for k in range(3)))
    return back, front


def door(x, y, w=150, h=300, col='#8A5A3A', bell=True):
    """Shop door (anchor = bottom left), a bell on a spring above it that can be animated."""
    return (f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{col}" stroke="{INK}" stroke-width="{LW}"/>'
            f'<rect x="{x + 16}" y="{y - h + 24}" width="{w - 32}" height="{h * .45}" fill="#BFDDEA" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{x + w - 22}" cy="{y - h * .45}" r="7" fill="{GOLD}" stroke="{INK}" stroke-width="2.6"/>')


def bell(x, y, s=1.0):
    return g(x, y, s, f'<path d="M-14 0 C-14 -22 14 -22 14 0 Z" fill="{GOLD}" stroke="{INK}" stroke-width="3"/><circle cy="4" r="4" fill="{INK}"/>')


def vault(x, y, s=1.0, open_t=None, open_d=1.6, light=True):
    """Round steel vault door (anchor = base centre, ~300 wide). open_t = local time it starts swinging open; golden light behind it."""
    door_svg = (f'<circle r="140" fill="{STEEL}" stroke="{INK}" stroke-width="{LW + 1}"/>'
                f'<circle r="112" fill="{STEEL_D}" stroke="{INK}" stroke-width="3.4"/>'
                f'<circle r="26" fill="#6F7A82" stroke="{INK}" stroke-width="3.4"/>'
                + ''.join(f'<rect x="-9" y="-104" width="18" height="78" rx="6" fill="#C9D2D8" stroke="{INK}" stroke-width="3" transform="rotate({a})"/>' for a in range(0, 360, 60))
                + ''.join(f'<circle cx="{118 * math.cos(math.radians(a)):.0f}" cy="{118 * math.sin(math.radians(a)):.0f}" r="6" fill="#5F6A72" stroke="{INK}" stroke-width="2.4"/>' for a in range(15, 360, 30)))
    frame = f'<circle r="156" fill="#4E5860" stroke="{INK}" stroke-width="{LW + 1}"/>'
    glow = (f'<circle r="140" fill="#FFE066"/>' + ''.join(f'<path d="M0 0 L{200 * math.cos(math.radians(a)):.0f} {200 * math.sin(math.radians(a)):.0f} L{200 * math.cos(math.radians(a + 9)):.0f} {200 * math.sin(math.radians(a + 9)):.0f} Z" fill="#FFF3B0" opacity=".8"/>' for a in range(0, 360, 30)))
    if open_t is None:
        return g(x, y - 160, s, frame + door_svg)
    dr = G(door_svg, [[0, {'sx': 1, 'tx': 0}], [open_t, {'sx': 1, 'tx': 0}], [open_t + open_d, {'sx': .12, 'tx': -120}, 'io']], (-140, 0))
    wheel = G('', [])
    lit = G(glow, [[0, {'o': 0}], [open_t, {'o': 0}], [open_t + .5, {'o': 1}]]) if light else ''
    return g(x, y - 160, s, frame + lit + dr)


def money_stack(x, y, n=5, w=110, kf=None):
    """Stack of banknotes (anchor = bottom centre)."""
    o = ''.join(f'<rect x="{x - w / 2}" y="{y - (k + 1) * 14}" width="{w}" height="16" rx="3" fill="#7FBF6A" stroke="{INK}" stroke-width="2.8"/>' for k in range(n))
    return animlib.G(o, kf, (x, y)) if kf else o


def thought_dollar(x, y, s=1.0):
    return g(x, y, s, text(0, 0, '$$$', 40, CAPS, GREEN))


# ---------------------------------------------------------------- travel / tech props (Episode 2)
def plane(x, y, s=1.0, flip=False, body='#F7F7F5', accent='#C0392F'):
    """Side-view cartoon airliner (anchor = centre of fuselage, ~260 wide)."""
    inner = (f'<path d="M-130 -6 C-130 -26 -90 -34 -40 -34 L90 -34 C130 -34 150 -14 150 0 C150 14 130 22 90 22 L-60 22 C-110 22 -130 12 -130 -6 Z" fill="{body}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>'
             f'<path d="M-130 -6 L-150 -62 L-112 -58 L-86 -30 Z" fill="{accent}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>'
             f'<path d="M-20 -2 L36 -2 L-30 56 L-62 56 Z" fill="#C9D2D8" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>'
             + ''.join(f'<circle cx="{cx}" cy="-12" r="7" fill="#9FD3F0" stroke="{INK}" stroke-width="2.6"/>' for cx in range(-70, 100, 28))
             + f'<path d="M110 -26 C130 -26 142 -14 148 -4 L106 -4 Z" fill="#9FD3F0" stroke="{INK}" stroke-width="3"/>'
             + f'<path d="M-124 6 H146" stroke="{accent}" stroke-width="6"/>')
    return g(x, y, s, inner, flip=flip)


def router(x, y, s=1.0, face='worried', lights=True, sweat=False):
    """A boxy network router with antennas and a face (anchor = base centre, ~150 wide)."""
    eyes = {'worried': ('M-30 -78 L-14 -84 M14 -84 L30 -78', 'M-14 -34 Q0 -46 14 -34'), 'shocked': ('M-30 -86 L-14 -82 M14 -82 L30 -86', ''), 'smug': ('', 'M-14 -40 Q0 -28 14 -40')}[face]
    inner = (f'<path d="M-50 -110 L-60 -170 M50 -110 L60 -170" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><circle cx="-60" cy="-172" r="8" fill="{RED}" stroke="{INK}" stroke-width="3"/><circle cx="60" cy="-172" r="8" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
             f'<rect x="-84" y="-112" width="168" height="112" rx="14" fill="#5C6B78" stroke="{INK}" stroke-width="{LW}"/>'
             f'<rect x="-84" y="-112" width="168" height="26" rx="14" fill="#47535E" stroke="{INK}" stroke-width="{LW}"/>'
             f'<circle cx="-24" cy="-62" r="12" fill="#F7F7F5" stroke="{INK}" stroke-width="3"/><circle cx="24" cy="-62" r="12" fill="#F7F7F5" stroke="{INK}" stroke-width="3"/>'
             f'<circle cx="-24" cy="-62" r="5" fill="{INK}"/><circle cx="24" cy="-62" r="5" fill="{INK}"/>'
             f'<path d="{eyes[0]}" stroke="{INK}" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
             + (f'<path d="{eyes[1]}" stroke="{INK}" stroke-width="3.4" fill="none" stroke-linecap="round"/>' if eyes[1] else f'<ellipse cx="0" cy="-30" rx="12" ry="14" fill="{INK}"/>')
             + (''.join(f'<circle cx="{-60 + k * 16}" cy="-14" r="4" fill="{c}" stroke="{INK}" stroke-width="2"/>' for k, c in enumerate(('#6FE06F', '#F7D35C', '#6FE06F', '#E0382C', '#6FE06F', '#F7D35C', '#E0382C', '#6FE06F'))) if lights else '')
             + (f'<path d="M70 -96 q-6 12 0 18 q6 -6 0 -18 Z" fill="#9FD3F0" stroke="{INK}" stroke-width="2.4"/>' if sweat else ''))
    return g(x, y, s, inner)


def radar_screen(x, y, w=300, h=230, glitch=None):
    """CRT-style radar screen (anchor = top-left). glitch=t makes it break up (static bars + red ERROR) from local time t."""
    cx, cy = x + w / 2, y + h / 2; r = min(w, h) / 2 - 18
    base = (f'<rect x="{x - 12}" y="{y - 12}" width="{w + 24}" height="{h + 24}" rx="20" fill="#2D3036" stroke="{INK}" stroke-width="{LW}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#0E2A1A" stroke="{INK}" stroke-width="3"/>'
            + ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r * k}" fill="none" stroke="#2F8A55" stroke-width="2"/>' for k in (.33, .66, 1))
            + f'<path d="M{cx - r} {cy} H{cx + r} M{cx} {cy - r} V{cy + r}" stroke="#2F8A55" stroke-width="2"/>')
    sweep = G(f'<path d="M{cx} {cy} L{cx + r} {cy} A{r} {r} 0 0 0 {cx + r * .87:.0f} {cy - r * .5:.0f} Z" fill="#6FE06F" opacity=".55"/>', [[0, {'r': 0}], [8, {'r': 2880}, 'l']], (cx, cy))
    blips = ''.join(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="5" fill="#C8FFD8"/>' for dx, dy in ((-40, -30), (50, 20), (20, -55), (-60, 40)))
    out = base + sweep + blips
    if glitch is not None:
        bars = ''.join(f'<rect x="{x}" y="{y + 18 + k * 34}" width="{w}" height="{10 + (k % 3) * 6}" fill="#C8FFD8" opacity=".75"/>' for k in range(6))
        out += G(bars, [[0, {'o': 0}], [glitch - .001, {'o': 0}], [glitch, {'o': 1}, 'h'], [glitch + .12, {'o': 0}, 'h'], [glitch + .2, {'o': 1}, 'h'], [glitch + .32, {'o': .4}, 'h'], [glitch + .4, {'o': 1}, 'h']], (cx, cy))
        out += G(f'<rect x="{x + 40}" y="{cy - 28}" width="{w - 80}" height="56" rx="8" fill="{RED}" stroke="{INK}" stroke-width="4"/>' + caps(cx, cy + 2, 'SIGNAL LOST', 34, '#FFFFFF'),
                 [[0, {'o': 0}], [glitch + .35, {'o': 0}], [glitch + .36, {'o': 1}, 'h']], (cx, cy))
    return out


def flight_board(x, y, w, rows, flip_ts, label_from='ON TIME', label_to='GROUNDED', to_col=RED):
    """Departures board (anchor = top-left). rows = [city names]; each row flips from label_from to label_to at flip_ts[i] (local s)."""
    h = 70 + 62 * len(rows)
    o = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#1F2A35" stroke="{INK}" stroke-width="{LW}"/>'
         + caps(x + w / 2, y + 34, 'DEPARTURES', 34, '#F7D35C'))
    for i, c in enumerate(rows):
        ry = y + 62 + i * 62
        o += f'<rect x="{x + 14}" y="{ry}" width="{w - 28}" height="50" rx="6" fill="#2E3C4A"/>' + caps(x + 28, ry + 27, c, 30, '#FFFFFF', 'start')
        a = G(f'<rect x="{x + w - 188}" y="{ry + 6}" width="168" height="38" rx="5" fill="#2F8A55"/>' + caps(x + w - 104, ry + 26, label_from, 24, '#FFFFFF'),
              [[0, {'sy': 1}], [flip_ts[i] - .1, {'sy': 1}], [flip_ts[i], {'sy': 0}, 'i'], [flip_ts[i] + .01, {'o': 0}]], (x + w - 104, ry + 25))
        b = G(f'<rect x="{x + w - 188}" y="{ry + 6}" width="168" height="38" rx="5" fill="{to_col}"/>' + caps(x + w - 104, ry + 26, label_to, 24, '#FFFFFF'),
              [[0, {'o': 0}], [flip_ts[i], {'o': 0, 'sy': 0}], [flip_ts[i] + .01, {'o': 1, 'sy': 0}], [flip_ts[i] + .16, {'sy': 1}, 'b']], (x + w - 104, ry + 25))
        o += a + b
    return o


def suitcase(x, y, s=1.0, col='#C0392F'):
    return g(x, y, s, f'<rect x="-34" y="-62" width="68" height="62" rx="8" fill="{col}" stroke="{INK}" stroke-width="{LW}"/>'
                      f'<path d="M-14 -62 V-76 H14 V-62" fill="none" stroke="{INK}" stroke-width="5"/><path d="M-34 -30 H34" stroke="{INK}" stroke-width="3" opacity=".5"/>'
                      f'<circle cx="-22" cy="4" r="5" fill="{INK}"/><circle cx="22" cy="4" r="5" fill="{INK}"/>')


def stop_sign(x, y, s=1.0, text_='STOP'):
    pts = ' '.join(f'{40 * math.cos(math.radians(22.5 + 45 * k)):.1f},{40 * math.sin(math.radians(22.5 + 45 * k)):.1f}' for k in range(8))
    return g(x, y, s, f'<rect x="-4" y="30" width="8" height="70" fill="#8A5A3A" stroke="{INK}" stroke-width="3"/><polygon points="{pts}" fill="{RED}" stroke="{INK}" stroke-width="4"/>' + caps(0, 2, text_, 22, '#FFFFFF'))


def cloud_shape(x, y, s=1.0):
    return g(x, y, s, f'<path d="M-60 0 C-80 0 -80 -30 -54 -30 C-52 -56 -10 -60 0 -38 C20 -58 62 -44 56 -20 C84 -22 86 4 60 4 Z" fill="#F7F7F5" stroke="{INK}" stroke-width="3.4" stroke-linejoin="round"/>')


# ---------------------------------------------------------------- IT / outage props (Episode 3)
def envelope(x, y, s=1.0, col='#F7F7F5'):
    return g(x, y, s, f'<rect x="-34" y="-24" width="68" height="48" rx="6" fill="{col}" stroke="{INK}" stroke-width="3.6"/><path d="M-34 -20 L0 6 L34 -20" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linejoin="round"/>')


def server_unit(x, y, w=120, h=46, state='ok', label=None):
    """One rack server (anchor = top-left). state ok=green LEDs, down=dark with red X."""
    led = '#6FE06F' if state == 'ok' else '#E0382C'
    body = '#5C6B78' if state == 'ok' else '#3A3F45'
    o = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{body}" stroke="{INK}" stroke-width="4"/>'
         + ''.join(f'<circle cx="{x + 16 + k * 14}" cy="{y + h / 2}" r="4.5" fill="{led}" stroke="{INK}" stroke-width="1.6"/>' for k in range(3))
         + f'<rect x="{x + w - 54}" y="{y + 12}" width="40" height="{h - 24}" rx="3" fill="#2B2F36"/>')
    if state != 'ok': o += f'<path d="M{x + w - 44} {y + 14} L{x + w - 24} {y + h - 14} M{x + w - 24} {y + 14} L{x + w - 44} {y + h - 14}" stroke="#E0382C" stroke-width="4" stroke-linecap="round"/>'
    if label: o += caps(x + w / 2, y + h + 22, label, 22, INK)
    return o


def bug(x, y, s=1.0, asleep=True):
    """Cute software bug (anchor = base centre)."""
    eyes = (f'<path d="M-14 -34 Q-8 -28 -2 -34 M6 -34 Q12 -28 18 -34" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>' if asleep
            else f'<circle cx="-8" cy="-34" r="5" fill="{INK}"/><circle cx="12" cy="-34" r="5" fill="{INK}"/>')
    return g(x, y, s, f'<path d="M-30 0 C-34 -40 -16 -58 2 -58 C20 -58 38 -40 34 0 Z" fill="#7BC96F" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>'
                      f'<path d="M-8 -64 L-16 -82 M14 -64 L22 -82" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>'
                      f'<path d="M-30 -14 L-48 -8 M-30 -28 L-50 -26 M34 -14 L52 -8 M34 -28 L54 -26" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>'
                      f'<circle cx="-12" cy="-12" r="5" fill="#2F6A2A"/><circle cx="16" cy="-14" r="5" fill="#2F6A2A"/>' + eyes
                      + (f'<path d="M-12 -22 Q2 -16 16 -22" fill="none" stroke="{INK}" stroke-width="3"/>'))


def gateway_door(x, y, w=170, h=230, label='FRONT DOOR'):
    """Big double door that all traffic goes through (anchor = bottom-centre)."""
    return (f'<rect x="{x - w / 2}" y="{y - h}" width="{w}" height="{h}" rx="12" fill="#6B452E" stroke="{INK}" stroke-width="{LW}"/>'
            f'<path d="M{x} {y - h} V{y}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="{x - w / 2 + 14}" y="{y - h + 18}" width="{w / 2 - 22}" height="{h * .38}" rx="6" fill="#8A5A3A" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x + 8}" y="{y - h + 18}" width="{w / 2 - 22}" height="{h * .38}" rx="6" fill="#8A5A3A" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{x - 12}" cy="{y - h * .38}" r="6" fill="{GOLD}" stroke="{INK}" stroke-width="2.6"/><circle cx="{x + 12}" cy="{y - h * .38}" r="6" fill="{GOLD}" stroke="{INK}" stroke-width="2.6"/>'
            + f'<rect x="{x - w / 2 - 10}" y="{y - h - 56}" width="{w + 20}" height="46" rx="8" fill="#E8D8A8" stroke="{INK}" stroke-width="3.6"/>' + caps(x, y - h - 32, label, 28, '#8A1F1A'))


def spinner(x, y, r=40, col='#4DA3FF'):
    """Loading spinner (rotates continuously)."""
    return G(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#C9D2D8" stroke-width="10"/><path d="M{x} {y - r} A{r} {r} 0 0 1 {x + r} {y}" fill="none" stroke="{col}" stroke-width="10" stroke-linecap="round"/>',
             [[0, {'r': 0}], [3, {'r': 1080}, 'l']], (x, y))
