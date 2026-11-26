"""Hindi standalone video: India's first underwater metro (Kolkata, Hooghly). Devanagari text, Hindi word anchors. No source text on screen."""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from episode_tools import *
import cast, props, bg
from cast import acting, char
from cc_kit import cash, burst, fill_bg, text, caps, SCRIPT_B, INK, mark
from animlib import bob, wiggle, flicker, push, pull, pan, fade, draw

FY = S(FLOOR)
RED_, GREEN_ = '#C0392F', '#3F9A50'
WATER, WATER_D, SOIL, SOIL_D = '#3E9BD6', '#2B78AE', '#8A6244', '#6B4A33'


class C:
    def __init__(s, sc, sh, cue): s.sc, s.sh, s.cue = sc, sh, cue; s.d = sh['end'] - sh['start']
    def w(s, word, which='start'): return word_time(s.sh, word, which)
    def talk(s, who, i=0): return talks_of(s.sh, who, s.sc)[i]
    def mouth(s, who, i=0): return mouth_windows(s.sh, who, s.sc, i)


def note_text(c, t0=0.0, y=None):
    """Sources are NEVER drawn on the video (permanent user rule): they live only in the upload description."""
    return ''


def over_of(c, size=58):
    return headline(c.sc['headline']['text'], resolve_at(c.sh, c.sc['headline']['at']), size)


def label_box(x, y, w, h, txt, fill='#FFFFFF', col=INK, size=26):
    return f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{INK}" stroke-width="4"/>' + caps(x, y + 2, txt, size, col)


def tag(x, y, txt, t, w=330, fill='#FFFFFF', size=24):
    return G(label_box(x, y, w, 62, txt, fill, INK, size), pop(t), (x, y))


def sparkle_field(c, n=22, seed=3, y0=0.0, y1=1.0, col='#FFFFFF', r=(1.5, 3.5)):
    rnd = random.Random(seed); o = ''
    for i in range(n):
        x, y = rnd.uniform(0, W()), rnd.uniform(S(y0), S(y1))
        o += G(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(*r):.1f}" fill="{col}" opacity=".55"/>', bob(0, c.d, rnd.uniform(5, 14), rnd.uniform(2.5, 5), 'ty'))
    return o


# ---------------------------------------------------------------- shared pieces
def metro_train(x, y, s=1.0, cars=3):
    """Side view metro train, nose to the right. (x, y) = centre of the first car's floor line."""
    o = ''
    for k in range(cars):
        cx = x - k * 150 * s
        o += f'<rect x="{cx - 68 * s}" y="{y - 52 * s}" width="{136 * s}" height="{54 * s}" rx="{14 * s}" fill="#F4F4F0" stroke="{INK}" stroke-width="{4 * s}"/>'
        o += f'<rect x="{cx - 68 * s}" y="{y - 14 * s}" width="{136 * s}" height="{9 * s}" fill="#2F7BC8"/>'
        o += ''.join(f'<rect x="{cx - 54 * s + j * 36 * s}" y="{y - 42 * s}" width="{26 * s}" height="{20 * s}" rx="{4 * s}" fill="#7FD3FF" stroke="{INK}" stroke-width="{2.6 * s}"/>' for j in range(3))
    o += f'<path d="M{x + 68 * s} {y - 38 * s} q{26 * s} {8 * s} {26 * s} {38 * s} h{-26 * s} Z" fill="#F4F4F0" stroke="{INK}" stroke-width="{4 * s}" stroke-linejoin="round"/>'
    o += f'<circle cx="{x + 84 * s}" cy="{y - 8 * s}" r="{5 * s}" fill="#FFE27A" stroke="{INK}" stroke-width="{2 * s}"/>'
    return o


def boat(x, y, s=1.0, col='#C0392F'):
    return (f'<path d="M{x - 60 * s} {y} H{x + 60 * s} L{x + 44 * s} {y + 26 * s} H{x - 44 * s} Z" fill="{col}" stroke="{INK}" stroke-width="{4 * s}" stroke-linejoin="round"/>'
            f'<path d="M{x} {y} V{y - 70 * s}" stroke="{INK}" stroke-width="{5 * s}"/><path d="M{x + 4 * s} {y - 68 * s} L{x + 46 * s} {y - 8 * s} H{x + 4 * s} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="{4 * s}" stroke-linejoin="round"/>')


def fish(x, y, s=1.0, col='#FF9B4A'):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{30 * s}" ry="{16 * s}" fill="{col}" stroke="{INK}" stroke-width="{3.4 * s}"/>'
            f'<path d="M{x - 28 * s} {y} l{-18 * s} {-14 * s} v{28 * s} Z" fill="{col}" stroke="{INK}" stroke-width="{3.4 * s}" stroke-linejoin="round"/>'
            f'<circle cx="{x + 14 * s}" cy="{y - 4 * s}" r="{3.4 * s}" fill="{INK}"/>')


def river_cut(c, t_train, dur=4.0, sky=('#9ED7F5', '#E9F6FF'), show_boat=True, fish_t=None):
    """Cross-section: sky, river with boats, soil with a lit tunnel and a train crossing it."""
    d = c.d; ty = S(.52)
    o = props.grad_bg(*sky)
    sun = props.glow(580, S(.10), 120, '#FFF2B8', .85)
    skyline = f'<path d="M0 {S(.255)} v-40 h40 v-60 h30 v60 h50 v-30 h40 v30 h60 v-80 h26 v80 h70 v-50 h40 v50 h60 v-34 h36 v34 h50 v-70 h30 v70 h40 V{S(.255)} Z" fill="#7FA5BE" opacity=".55"/>'
    water = props.waves(S(.27), 900, 10, WATER, [[0, {'tx': 0}], [d, {'tx': -70}, 'l']], x0=-90) + f'<rect x="-100" y="{S(.27) + 8}" width="{W() + 200}" height="{S(.14)}" fill="{WATER}"/>'
    bed = f'<path d="M-100 {S(.41)} Q 360 {S(.465)} {W() + 100} {S(.41)} V{H() + 100} H-100 Z" fill="{SOIL}" stroke="{INK}" stroke-width="5"/>'
    soil = f'<rect x="-100" y="{S(.455)}" width="{W() + 200}" height="{H()}" fill="{SOIL}"/>' + ''.join(f'<circle cx="{(k * 97) % 700 + 10}" cy="{S(.60) + (k * 53) % 380}" r="{5 + k % 4}" fill="{SOIL_D}" opacity=".6"/>' for k in range(26))
    tun = (f'<rect x="-60" y="{ty - 62}" width="{W() + 120}" height="124" rx="62" fill="{SOIL_D}" stroke="{INK}" stroke-width="6"/>'
           f'<rect x="-40" y="{ty - 48}" width="{W() + 80}" height="96" rx="48" fill="#EDEAE2" stroke="{INK}" stroke-width="4"/>'
           f'<rect x="-20" y="{ty + 30}" width="{W() + 40}" height="10" fill="#6E6A60"/>' + ''.join(f'<path d="M{x} {ty - 46} v92" stroke="#C9C5B8" stroke-width="3"/>' for x in range(-20, 760, 60)))
    tr = G(metro_train(-60, ty + 30, 1.0, 3), [[0, {'tx': 0}], [t_train, {'tx': 0}], [t_train + dur, {'tx': W() + 800}, 'l']])
    boats = ''
    if show_boat:
        boats = (G(boat(150, S(.27) - 4, 1.0), merge(bob(0, d, 6, 2.6, 'ty'), [[0, {'tx': 0}], [d, {'tx': 90}, 'l']]), (150, S(.27))) +
                 G(boat(560, S(.27) - 4, .8, '#2F7BC8'), merge(bob(0, d, 5, 3.1, 'ty'), [[0, {'tx': 0}], [d, {'tx': -80}, 'l']]), (560, S(.27))))
    fishes = ''
    if fish_t is not None:
        fishes = ''.join(G(fish(120 + k * 180, S(.34) + (k % 2) * 30, .9, ['#FF9B4A', '#FFD54A', '#FF7A7A'][k]), [[0, {'o': 0}], [fish_t + k * .3 - .001, {'o': 0, 'tx': 0}], [fish_t + k * .3, {'o': 1}], [d, {'tx': 90}, 'l']]) for k in range(3))
    return o + sun + skyline + water + bed + soil + tun + boats + fishes + tr


# ------------------------------------------------------------------ S1: hook
def s1(c):
    d = c.d; tg = c.talk('GUY'); t_r, t_m = c.w('नदी'), c.w('मेट्रो')
    world = river_cut(c, t_m - .2, 5.0)
    lab = tag(190, S(.20), 'हुगली नदी', t_r, 250, '#CFEFFF', 28) + tag(540, S(.60), 'मेट्रो ट्रेन', t_m + .8, 250, '#FFF2B0', 26)
    plat = f'<rect x="-40" y="{S(.74)}" width="{W() + 80}" height="26" rx="8" fill="#D9D3C4" stroke="{INK}" stroke-width="5"/>'
    guy = acting('GUY', 130, S(.74), 1.1, [(0, dict(pose='standing', expr='happy')), (tg[0] - .05, dict(pose='shocked', expr='worried', talk=c.mouth('GUY')))], t_end=d)
    world += lab + plat + guy
    return world, [[0, {'s': 1.0}], [d, {'s': 1.05}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S2: the route
def s2(c):
    d = c.d; tf = c.talk('FRIEND'); t_h, t_u, t_y = c.w('हावड़ा'), c.w('उद्घाटन'), c.w('यात्री')
    bgd = props.grad_bg('#2A4A6B', '#14243A') + sparkle_field(c, 24, 5, 0.0, .5)
    ly = S(.40)
    river = f'<rect x="290" y="{ly - 150}" width="140" height="300" rx="20" fill="{WATER}" stroke="{INK}" stroke-width="5"/>' + props.waves(ly - 120, 400, 6, WATER_D, [[0, {'tx': 0}], [d, {'tx': 40}, 'l']], x0=290, n=3).replace(f'V{ly - 120 + 400}', f'V{ly + 150}') + caps(360, ly - 170, 'हुगली', 26, '#FFFFFF')
    rail = f'<path d="M70 {ly} H650" stroke="#EDEAE2" stroke-width="16" stroke-linecap="round"/><path d="M70 {ly} H650" stroke="{INK}" stroke-width="4" stroke-dasharray="14 14"/>'
    st = lambda x, n: f'<circle cx="{x}" cy="{ly}" r="26" fill="#FFD54A" stroke="{INK}" stroke-width="6"/>' + caps(x, ly + 70, n, 24, '#FFFFFF')
    stations = G(st(90, 'हावड़ा मैदान'), pop(t_h), (90, ly)) + G(st(630, 'एस्प्लेनेड'), pop(t_h + .6), (630, ly))
    tr = G(metro_train(90, ly - 16, .55, 3), [[0, {'o': 0}], [t_h + 1.2, {'o': 0, 'tx': 0}], [t_h + 1.21, {'o': 1}], [t_h + 5.5, {'tx': 480}, 'io']])
    b1 = G(f'<rect x="120" y="{S(.58)}" width="480" height="96" rx="16" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>' + caps(360, S(.58) + 30, 'उद्घाटन', 24, '#C0392F') + caps(360, S(.58) + 68, '6 मार्च 2024', 34, INK), pop(t_u), (360, S(.62)))
    b2 = G(f'<rect x="120" y="{S(.675)}" width="480" height="96" rx="16" fill="#CDEBC5" stroke="{INK}" stroke-width="5"/>' + caps(360, S(.675) + 30, 'यात्रियों के लिए चालू', 24, '#1E5E2C') + caps(360, S(.675) + 68, '15 मार्च 2024', 34, INK), pop(t_y), (360, S(.72)))
    friend = acting('FRIEND', 100, S(.945), .8, [(0, dict(pose='standing', expr='neutral')), (tf[0] - .05, dict(pose='pointing', expr='happy', talk=c.mouth('FRIEND')))], t_end=d)
    world = bgd + river + rail + stations + tr + b1 + b2 + friend
    return world, [[0, {'s': 1.0}], [d, {'s': 1.04}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S3: 520 m, 45 s
def s3(c):
    d = c.d; tg = c.talk('GUY'); t_t, t_m, t_s = c.w('सुरंग'), c.w('मीटर'), c.w('सेकंड')
    world = river_cut(c, t_t + .3, 5.0, sky=('#B9E4FA', '#F3FBFF'), show_boat=False)
    ty = S(.52)
    brk = G(f'<path d="M20 {ty - 120} v-24 H700 v24 M360 {ty - 144} v-14" fill="none" stroke="{RED_}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><path d="M20 {ty - 150} l24 -14 M20 {ty - 150} l24 14 M700 {ty - 150} l-24 -14 M700 {ty - 150} l-24 14" stroke="{RED_}" stroke-width="7" stroke-linecap="round"/>', pop(t_m), (360, ty - 140))
    big = G(label_box(360, ty - 190, 330, 70, '≈ 520 मीटर', '#FFFFFF', RED_, 38), pop(t_m + .1), (360, ty - 190))
    sw = G(f'<circle cx="590" cy="{S(.72)}" r="76" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/><rect x="574" y="{S(.72) - 98}" width="32" height="18" rx="5" fill="#C9C5B8" stroke="{INK}" stroke-width="5"/>' + ''.join(f'<path d="M590 {S(.72) - 66} v10" transform="rotate({k * 30} 590 {S(.72)})" stroke="{INK}" stroke-width="4"/>' for k in range(12)), pop(t_s - 1.5), (590, S(.72)))
    hand = G(f'<path d="M590 {S(.72)} V{S(.72) - 58}" stroke="{RED_}" stroke-width="7" stroke-linecap="round"/><circle cx="590" cy="{S(.72)}" r="9" fill="{INK}"/>', [[0, {'r': 0, 'o': 0}], [t_s - 1.5, {'r': 0, 'o': 1}], [t_s + 2.8, {'r': 330}, 'l']], (590, S(.72)))
    lbl = G(label_box(590, S(.72) + 120, 220, 54, '≈ 45 सेकंड', '#FFF2B0', INK, 26), pop(t_s), (590, S(.72) + 120))
    plat = f'<rect x="-40" y="{S(.80)}" width="360" height="26" rx="8" fill="#D9D3C4" stroke="{INK}" stroke-width="5"/>'
    guy = acting('GUY', 150, S(.80), 1.0, [(0, dict(pose='standing', expr='neutral')), (tg[0] - .05, dict(pose='shocked', expr='happy', talk=c.mouth('GUY')))], t_end=d)
    world += brk + big + sw + hand + lbl + plat + guy
    return world, [[0, {'s': 1.0}], [d, {'s': 1.04}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S4: the tunnel boring machine
def s4(c):
    d = c.d; tf = c.talk('FRIEND'); t_m, t_r, t_w = c.w('मशीन'), c.w('छल्ले'), c.w('पानी')
    bgd = props.grad_bg('#6B4A33', '#3E2A1D') + ''.join(f'<circle cx="{(k * 131) % 700 + 10}" cy="{(k * 89) % 1250 + 10}" r="{5 + k % 5}" fill="#8A6244" opacity=".6"/>' for k in range(30))
    cy = S(.44)
    # finished tunnel (left) with concrete rings
    ringx = [60 + k * 46 for k in range(7)]
    rings = ''.join(G(f'<rect x="{x}" y="{cy - 112}" width="34" height="224" rx="8" fill="#B8B4A8" stroke="{INK}" stroke-width="5"/><rect x="{x + 8}" y="{cy - 90}" width="18" height="180" rx="5" fill="#EDEAE2"/>', pop(t_r + k * .22), (x + 17, cy)) for k, x in enumerate(ringx))
    body = f'<rect x="380" y="{cy - 120}" width="170" height="240" rx="22" fill="#F2B134" stroke="{INK}" stroke-width="7"/><rect x="400" y="{cy - 90}" width="60" height="70" rx="8" fill="#16283A" stroke="{INK}" stroke-width="5"/><path d="M380 {cy - 40} H550 M380 {cy + 40} H550" stroke="{INK}" stroke-width="4" opacity=".5"/>'
    spokes = ''.join(f'<path d="M0 0 L0 -104" transform="rotate({k * 45})" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><circle cx="0" cy="-104" r="10" transform="rotate({k * 45})" fill="#C9C5B8" stroke="{INK}" stroke-width="4"/>' for k in range(8))
    head = G(f'<circle cx="0" cy="0" r="116" fill="#C9C5B8" stroke="{INK}" stroke-width="7"/><circle cx="0" cy="0" r="30" fill="#F2B134" stroke="{INK}" stroke-width="6"/>' + spokes, [[0, {'r': 0}], [d, {'r': 540}, 'l']], (0, 0))
    head = f'<g transform="translate(610 {cy})">' + head + '</g>'
    # moving the whole machine forward slowly
    mach = G(body + head, [[0, {'tx': 0}], [d, {'tx': 60}, 'l']])
    rocks = ''.join(G(f'<circle cx="{700 + k * 4}" cy="{cy - 40 + k * 22}" r="{8 + k * 2}" fill="#8A6244" stroke="{INK}" stroke-width="3"/>', [[0, {'o': 0}], [t_m + k * .35 - .001, {'o': 0, 'tx': 0, 'ty': 0}], [t_m + k * .35, {'o': 1}], [t_m + k * .35 + 1.0, {'tx': 70, 'ty': 24, 'o': 0}, 'o']]) for k in range(5))
    lab = tag(520, S(.27), 'टनल बोरिंग मशीन', t_m, 340, '#FFF2B0', 26) + tag(190, S(.60), 'कंक्रीट के छल्ले', t_r, 300, '#E6E2D6', 26)
    wat = G(f'<path d="M-80 {S(.20)} H800 V{S(.255)} H-80 Z" fill="{WATER}" stroke="{INK}" stroke-width="5"/>' + caps(360, S(.228), 'ऊपर: हुगली का पानी', 26, '#FFFFFF'), pop(t_w - 1.0), (360, S(.23)))
    drops = ''.join(G(props.droplet(130 + k * 120, S(.27), .8), [[0, {'o': 0}], [t_w + k * .3 - .001, {'o': 0, 'ty': 0}], [t_w + k * .3, {'o': 1}], [t_w + k * .3 + 1.0, {'ty': 40, 'o': 0}, 'i']]) for k in range(5))
    stop = G(f'<g transform="translate(130 {S(.69)})"><rect x="-90" y="-26" width="180" height="52" rx="12" fill="#FFFFFF" stroke="{RED_}" stroke-width="6"/>' + caps(0, 2, 'पानी अंदर ✕', 26, RED_) + '</g>', slam(tf[0]), (130, S(.69)))
    friend = acting('FRIEND', 560, S(.94), .8, [(0, dict(pose='standing', expr='worried')), (tf[0] - .05, dict(pose='laughing', expr='grin', talk=c.mouth('FRIEND')))], t_end=d)
    world = bgd + wat + drops + rings + mach + rocks + lab + stop + friend
    return world, [[0, {'s': 1.0}], [d, {'s': 1.04}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S5: deepest station (about 11 floors down)
def s5(c):
    d = c.d; tb = c.talk('BANKER'); t_g, t_n, t_e = c.w('गहरा'), c.w('तैंतीस'), c.w('एस्केलेटर')
    t_ty = c.w('ग्यारह')
    bgd = props.grad_bg('#BFE6F7', '#EAF7FF')
    gy = S(.24)
    top = f'<rect x="-40" y="{gy - 6}" width="{W() + 80}" height="{H()}" fill="{SOIL}" stroke="{INK}" stroke-width="5"/>' + ''.join(f'<circle cx="{(k * 97) % 700 + 10}" cy="{gy + 40 + (k * 61) % 900}" r="{5 + k % 4}" fill="{SOIL_D}" opacity=".6"/>' for k in range(30))
    street = f'<rect x="-40" y="{gy - 50}" width="{W() + 80}" height="46" fill="#7B8791" stroke="{INK}" stroke-width="5"/>' + f'<path d="M0 {gy - 26} H720" stroke="#FFFFFF" stroke-width="5" stroke-dasharray="26 18"/>'
    fh = 62; n = 11; x0 = 190; w_ = 340
    shaft = f'<rect x="{x0}" y="{gy}" width="{w_}" height="{fh * n}" rx="10" fill="#EDEAE2" stroke="{INK}" stroke-width="6"/>'
    floors = ''.join(G(f'<rect x="{x0 + 6}" y="{gy + k * fh + 4}" width="{w_ - 12}" height="{fh - 8}" rx="6" fill="{["#CFEFFF", "#FFF2B0"][k % 2]}" stroke="{INK}" stroke-width="3"/>' + caps(x0 + w_ / 2, gy + k * fh + fh / 2 + 2, str(k + 1), 28, INK), pop(t_ty + k * .17), (x0 + w_ / 2, gy + k * fh + fh / 2)) for k in range(n))
    esc = G(f'<path d="M{x0 + 40} {gy + 8} L{x0 + w_ - 40} {gy + fh * n - 20}" stroke="{INK}" stroke-width="7" stroke-dasharray="3 14" stroke-linecap="round" opacity=".5"/>', pop(t_e - .3), (360, gy + 300))
    platform = G(f'<rect x="{x0}" y="{gy + fh * n - 20}" width="{w_}" height="36" rx="8" fill="#6E6A60" stroke="{INK}" stroke-width="5"/>' + metro_train(x0 + w_ / 2 + 70, gy + fh * n - 28, .5, 2), pop(t_g), (360, gy + fh * n))
    arrow = G(f'<path d="M110 {gy + 20} V{gy + fh * n - 4}" stroke="{RED_}" stroke-width="9" stroke-linecap="round"/><path d="M96 {gy + 40} L110 {gy + 10} L124 {gy + 40} M96 {gy + fh * n - 24} L110 {gy + fh * n + 6} L124 {gy + fh * n - 24}" fill="none" stroke="{RED_}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>' + caps(60, gy + 340, '≈33 मी', 30, RED_), pop(t_n), (110, gy + 300))
    big = G(label_box(560, gy + 120, 220, 70, '≈ 33 मीटर', '#FFFFFF', RED_, 32), pop(t_n + .1), (560, gy + 120))
    bk = acting('BANKER', 600, gy - 44, .55, [(0, dict(pose='standing', expr='smug')), (tb[0] - .05, dict(pose='talking', expr='grin', talk=c.mouth('BANKER')))], t_end=d)
    world = bgd + street + top + shaft + floors + esc + platform + arrow + big + bk
    return world, [[0, {'s': 1.0}], [d, {'s': 1.03}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S6: final joke
def s6(c):
    d = c.d; tg = c.talk('GUY'); tb = c.talk('BANKER'); t_n = c.w('नावें'); t_f = c.talk('GUY')[0]
    world = river_cut(c, t_n + .5, 5.5, sky=('#9ED7F5', '#FFF4D0'), show_boat=True, fish_t=t_f - .3)
    lab = tag(180, S(.19), 'ऊपर: नावें', t_n, 250, '#FFF2B0', 28) + tag(540, S(.60), 'नीचे: मेट्रो', t_n + .8, 250, '#CFEFFF', 28)
    plat = f'<rect x="-40" y="{S(.80)}" width="{W() + 80}" height="26" rx="8" fill="#D9D3C4" stroke="{INK}" stroke-width="5"/>'
    guy = acting('GUY', 150, S(.80), 1.0, [(0, dict(pose='standing', expr='happy')), (tg[0] - .05, dict(pose='pointing', expr='happy', talk=c.mouth('GUY')))], t_end=d)
    banker = acting('BANKER', 560, S(.80), 1.0, [(0, dict(pose='standing', expr='smug')), (tb[0] - .05, dict(pose='talking', expr='grin', talk=c.mouth('BANKER')))], t_end=d)
    tick = G(f'<g transform="translate(560 {S(.66)}) rotate(-8)"><rect x="-90" y="-30" width="180" height="60" rx="10" fill="#FFFFFF" stroke="{RED_}" stroke-width="6"/>' + caps(0, 2, 'टिकट ज़रूरी!', 28, RED_) + '</g>', slam(tb[0] + .6), (560, S(.66)))
    world += lab + plat + guy + banker + tick
    return world, [[0, {'s': 1.0}], [d, {'s': 1.03}, 'l']], (W() / 2, S(.5)), over_of(c)


BUILDERS = {'S1': s1, 'S2': s2, 'S3': s3, 'S4': s4, 'S5': s5, 'S6': s6}
