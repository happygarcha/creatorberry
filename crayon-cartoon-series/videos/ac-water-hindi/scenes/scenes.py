"""Hindi 60 s video: why you should not drink AC water. Scenes use Devanagari text (Kalam via unicode-range) and Hindi word anchors."""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from episode_tools import *
import cast, props, bg
from cast import acting, char
from cc_kit import cash, burst, fill_bg, text, caps, SCRIPT_B, INK, mark
from animlib import bob, wiggle, flicker, push, pull, pan, fade, draw

FY = S(FLOOR)
RED_, GREEN_, BLUE_ = '#C0392F', '#3F9A50', '#4DA3FF'


class C:
    def __init__(s, sc, sh, cue): s.sc, s.sh, s.cue = sc, sh, cue; s.d = sh['end'] - sh['start']
    def w(s, word, which='start'): return word_time(s.sh, word, which)
    def talk(s, who, i=0): return talks_of(s.sh, who, s.sc)[i]
    def mouth(s, who, i=0): return mouth_windows(s.sh, who, s.sc, i)


def note_text(c, t0=0.0, y=None):
    """Sources are NEVER drawn on the video (permanent user rule): they live only in the upload description. Kept as a no-op so scenes stay unchanged."""
    return ''


def over_of(c, size=58):
    return headline(c.sc['headline']['text'], resolve_at(c.sh, c.sc['headline']['at']), size)


def label_box(x, y, w, h, txt, fill='#FFFFFF', col=INK, size=26):
    return f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{INK}" stroke-width="4"/>' + caps(x, y + 2, txt, size, col)


def tag(x, y, txt, t, w=330, fill='#FFFFFF', size=24):
    return G(label_box(x, y, w, 62, txt, fill, INK, size), pop(t), (x, y))


def dots_progress(part):
    return ''.join(f'<circle cx="{300 + k * 40}" cy="{S(.255)}" r="9" fill="{"#FFD54A" if k < part else "#FFFFFF"}" fill-opacity="{1 if k < part else .35}" stroke="{INK}" stroke-width="3"/>' for k in range(4))


def sparkle_field(c, n=26, seed=3, y0=0.0, y1=1.0, col='#FFFFFF', r=(1.5, 3.5)):
    rnd = random.Random(seed); o = ''
    for i in range(n):
        x, y = rnd.uniform(0, W()), rnd.uniform(S(y0), S(y1))
        o += G(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(*r):.1f}" fill="{col}" opacity=".55"/>', bob(0, c.d, rnd.uniform(5, 14), rnd.uniform(2.5, 5), 'ty'))
    return o


# ------------------------------------------------------------------ S1: hook
def s1(c):
    d = c.d; tg = c.talk('GUY'); t_dr, t_do = c.w('टपकता'), c.w('मत')
    wall = props.grad_bg('#F3E6C8', '#D8C08A') + f'<rect x="-100" y="{FY}" width="{W() + 200}" height="{H() - FY + 100}" fill="#B98F5A"/><path d="M-100 {FY} H{W() + 100}" stroke="{INK}" stroke-width="5"/>'
    sun = props.glow(560, S(.2), 260, '#FFF2B8', .7)
    unit = props.outdoor_unit(560, FY - 190, 1.35, spin=(0, d))
    hose = f'<path d="M488 {FY - 250} C440 {FY - 240} 380 {FY - 210} 340 {FY - 150} L338 {FY - 90}" fill="none" stroke="#F4F4F0" stroke-width="16" stroke-linecap="round"/><path d="M488 {FY - 250} C440 {FY - 240} 380 {FY - 210} 340 {FY - 150} L338 {FY - 90}" fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="1 0" opacity=".25"/>'
    stool = f'<rect x="270" y="{FY - 70}" width="140" height="16" rx="6" fill="#C0392F" stroke="{INK}" stroke-width="5"/><path d="M286 {FY - 54} L276 {FY + 10} M394 {FY - 54} L404 {FY + 10}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    drops = ''.join(G(props.droplet(338, FY - 84, .8), [[0, {'o': 0}], [t_dr + k * .7 - .001, {'o': 0, 'ty': 0}], [t_dr + k * .7, {'o': 1, 'ty': 0}], [t_dr + k * .7 + .5, {'ty': 74}, 'i'], [t_dr + k * .7 + .52, {'o': 0}]]) for k in range(10))
    gl = props.glass(340, FY - 70, 1.3, .35)
    stamp = G(f'<g transform="translate(360 {S(.60)}) rotate(-8)"><rect x="-300" y="-58" width="600" height="116" rx="12" fill="#FFFFFF" fill-opacity=".92" stroke="{RED_}" stroke-width="10"/>' + text(0, 18, 'पीना मना है', 84, SCRIPT_B, RED_) + '</g>', slam(t_do), (360, S(.60)))
    guy = acting('GUY', 120, FY + 20, 1.5, [(0, dict(pose='standing', expr='happy')), (tg[0] - .05, dict(pose='shocked', expr='worried', talk=c.mouth('GUY')))], t_end=d)
    world = wall + sun + unit + hose + stool + gl + drops + guy + stamp + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.08}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S2: where it comes from (AC cutaway)
def s2(c):
    d = c.d; tf = c.talk('FRIEND'); t_w, t_dr, t_co = c.w('गर्म'), c.w('बूंदें'), c.w('कंडेंसेशन')
    bgd = props.grad_bg('#4E7FA8', '#25435E') + sparkle_field(c, 22, 5, 0.0, .6)
    cx, cy, w, h = 360, S(.34), 560, 300
    shell = f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="30" fill="#EEF3F6" stroke="{INK}" stroke-width="7"/><rect x="{cx - w / 2 + 24}" y="{cy - h / 2 + 24}" width="{w - 48}" height="{h - 70}" rx="20" fill="#16283A" stroke="{INK}" stroke-width="5"/>'
    # evaporator coil (cold, blue zig-zag) + glow
    zig = 'M' + ' L'.join(f'{cx - 200 + k * 40} {cy - 20 + (36 if k % 2 else -36)}' for k in range(11))
    coil = props.glow(cx, cy, 190, '#66C7FF', .35) + f'<path d="{zig}" fill="none" stroke="#7FD3FF" stroke-width="12" stroke-linejoin="round" stroke-linecap="round"/><path d="{zig}" fill="none" stroke="#FFFFFF" stroke-width="3" opacity=".6"/>'
    arrows = ''.join(G(f'<path d="M0 0 q16 -16 32 0 t32 0" fill="none" stroke="#FF9B4A" stroke-width="7" stroke-linecap="round"/><path d="M64 0 l-12 -10 m12 10 l-12 10" stroke="#FF9B4A" stroke-width="6" stroke-linecap="round"/>', [[0, {'o': 0}], [t_w + k * .5 - .001, {'o': 0, 'tx': -50, 'ty': 0}], [t_w + k * .5, {'o': 1}], [t_w + k * .5 + 1.4, {'tx': 80, 'o': 0}, 'o']]) for k in range(8))
    arrows = ''.join(f'<g transform="translate({cx - 270} {cy - 80 + j * 50})">{G(f"<g>{arrows}</g>", [[0, {"o": 1}]])}</g>' for j in range(1)) if False else ''.join(f'<g transform="translate({cx - 250} {cy - 70 + j * 70})">' + G(f'<path d="M0 0 q16 -16 32 0 t32 0" fill="none" stroke="#FF9B4A" stroke-width="7" stroke-linecap="round"/><path d="M64 0 l-12 -10 m12 10 l-12 10" stroke="#FF9B4A" stroke-width="6" stroke-linecap="round"/>', [[0, {'o': 0}], [t_w + j * .5 - .001, {'o': 0, 'tx': -40}], [t_w + j * .5, {'o': 1}], [t_w + j * .5 + 1.6, {'tx': 120}, 'l'], [t_w + j * .5 + 1.7, {'o': 0}]]) + '</g>' for j in range(3))
    drops = ''.join(G(props.droplet(cx - 160 + (k % 6) * 62, cy + 36 + (k // 6) * 8, .8), [[0, {'o': 0}], [t_dr + k * .2 - .001, {'o': 0, 'ty': 0}], [t_dr + k * .2, {'o': 1}], [t_dr + k * .2 + 1.6, {'ty': 78, 'o': 1}, 'i'], [t_dr + k * .2 + 1.65, {'o': 0}]]) for k in range(12))
    pan_ = f'<path d="M{cx - 230} {cy + 118} H{cx + 230} L{cx + 200} {cy + 140} H{cx - 200} Z" fill="#9AA6AE" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    pipe = f'<path d="M{cx + 210} {cy + 128} H{cx + 260} Q{cx + 300} {cy + 128} {cx + 300} {cy + 170} V{cy + 300}" fill="none" stroke="#F4F4F0" stroke-width="16" stroke-linecap="round"/>'
    flow = G(props.droplet(cx + 300, cy + 190, .8), [[0, {'o': 0}], [t_co, {'o': 0}], [t_co + .01, {'o': 1, 'ty': 0}], [t_co + 1.2, {'ty': 100, 'o': 0}, 'i']]) + G(props.droplet(cx + 300, cy + 190, .8), [[0, {'o': 0}], [t_co + 1.2, {'o': 0}], [t_co + 1.21, {'o': 1, 'ty': 0}], [t_co + 2.4, {'ty': 100, 'o': 0}, 'i']])
    labels = tag(160, S(.50), 'गर्म, नम हवा', t_w, 270, '#FFD9B0', 26) + tag(570, S(.50), 'ठंडे कॉइल', t_dr - .8, 230, '#CFEFFF', 26) + tag(360, S(.565), 'कंडेंसेशन', t_co, 300, '#FFF2B0', 28)
    friend = acting('FRIEND', 110, FY + 200, .9, [(0, dict(pose='standing', expr='neutral')), (tf[0] - .05, dict(pose='laughing', expr='grin', talk=c.mouth('FRIEND')))], t_end=d)
    glass_ = G(props.glass(600, FY + 200, 1.2, .5), wiggle(tf[0], d, 3, .5, 'r'), (600, FY + 200)) + G(''.join(f'<path d="M{572 + k * 14} {FY + 94 + k * 3} v14" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity=".8"/>' for k in range(5)), pop(tf[0]))
    world = bgd + shell + coil + arrows + drops + pan_ + pipe + flow + labels + friend + glass_ + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.05}, 'l']], (W() / 2, S(.5)), over_of(c) + dots_progress(1)


# ------------------------------------------------------------------ S3: dry air
def s3(c):
    d = c.d; tg = (c.w('आँखें'), 0); t_m, t_dry, t_th = c.w('नमी'), c.w('सूखा'), c.w('त्वचा')
    bgd = props.grad_bg('#304A66', '#16212E') + sparkle_field(c, 20, 8, 0.0, .55)
    ac = props.split_ac(360, S(.27), 430)
    pull_ = ''.join(G(props.droplet(120 + k * 60, S(.50), .7), [[0, {'o': 0}], [t_m + k * .35 - .001, {'o': 0, 'ty': 0, 'tx': 0}], [t_m + k * .35, {'o': 1}], [t_m + k * .35 + 1.4, {'ty': -150, 'tx': (360 - (120 + k * 60)) * .5, 'o': 0}, 'io']]) for k in range(8))
    gk = [[0, {'r': 50}], [t_dry - .2, {'r': 50}], [t_dry + 2.4, {'r': -62}, 'io'], [t_dry + 2.7, {'r': -66}, 'o']]
    gg = G(props.gauge(360, S(.60), 112, label='नमी', keys=gk), pop(t_m - .4), (360, S(.60)))
    z1 = tag(160, S(.455), 'बहुत सूखा', t_dry + 1.6, 200, '#F7B5AD', 26) + tag(560, S(.455), 'ठीक: 30-50%', t_th, 230, '#CDEBC5', 24)
    guy = acting('GUY', 130, FY + 140, 1.0, [(0, dict(pose='standing', expr='neutral')), (t_dry + 1.2, dict(pose='confused', expr='worried')), (tg[0] - .05, dict(pose='shocked', expr='worried', talk=c.mouth('GUY')))], t_end=d)
    world = bgd + ac + pull_ + gg + z1 + guy + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.04}, 'l']], (W() / 2, S(.5)), over_of(c) + dots_progress(2)


# ------------------------------------------------------------------ S4: the big mistake (sealed bedroom, CO2)
def s4(c):
    d = c.d; tf = (c.w('ताज़ी'), 0); t_m, t_c, t_dp, t_fr = c.w('तीन'), c.w('कार्बन'), c.w('कार्बन'), c.w('ताज़ी')
    bgd = props.grad_bg('#1B2744', '#0E1424') + props.glow(120, S(.40), 150, '#FFC773', .55) + sparkle_field(c, 24, 4, 0, .5)
    moon = f'<circle cx="560" cy="{S(.30)}" r="44" fill="#FFF6D6" stroke="{INK}" stroke-width="4"/><circle cx="574" cy="{S(.30) - 6}" r="36" fill="#1B2744"/>'
    win = f'<rect x="470" y="{S(.24)}" width="190" height="230" rx="8" fill="#223A66" stroke="{INK}" stroke-width="7"/><path d="M565 {S(.24)} V{S(.24) + 230} M470 {S(.24) + 115} H660" stroke="{INK}" stroke-width="5"/>' + moon.replace('cx="560"', 'cx="530"').replace('cx="574"', 'cx="544"') + f'<rect x="470" y="{S(.24) + 230}" width="190" height="14" fill="#8A5A3A" stroke="{INK}" stroke-width="4"/>'
    lamp = f'<rect x="96" y="{S(.34)}" width="48" height="56" rx="10" fill="#FFD27A" stroke="{INK}" stroke-width="4"/><path d="M120 {S(.34) + 56} V{S(.34) + 100}" stroke="{INK}" stroke-width="6"/>'
    ac = props.split_ac(250, S(.20), 330, .9)
    floor = f'<rect x="-100" y="{FY + 20}" width="{W() + 200}" height="{H()}" fill="#2B1F26"/><path d="M-100 {FY + 20} H{W() + 100}" stroke="{INK}" stroke-width="5"/>'
    bed_ = props.bed(330, FY + 90, 540, 1.0)
    sleeper = f'<circle cx="150" cy="{FY - 70}" r="36" fill="#F3CDA1" stroke="{INK}" stroke-width="5"/><path d="M132 {FY - 72} q8 6 16 0 M158 {FY - 72} q8 6 16 0" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/><path d="M118 {FY - 92} q30 -34 68 -4 l-6 20 q-30 -22 -62 -4 Z" fill="#2B2420" stroke="{INK}" stroke-width="4"/>'
    z = ''.join(G(text(210 + k * 28, FY - 130 - k * 36, 'Z', 38 - k * 6, SCRIPT_B, '#FFFFFF'), bob(0, d, 6, 2.2 + k * .3, 'ty')) for k in range(3))
    rnd = random.Random(6); co2s = ''
    for k in range(40):
        t0 = t_c + k * .22; x = rnd.uniform(90, 640); y0 = rnd.uniform(FY - 120, FY - 20); y1 = y0 - rnd.uniform(150, 420)
        co2s += G(props.co2(x, y0, .8), [[0, {'o': 0}], [t0 - .001, {'o': 0, 'ty': 0}], [t0, {'o': 1}], [t0 + 3.2, {'ty': y1 - y0, 'tx': rnd.uniform(-30, 30)}, 'o']])
    gk = [[0, {'r': -60}], [t_c, {'r': -60}], [t_c + 7, {'r': 60}, 'io']]
    meter = G(props.gauge(560, S(.56), 70, label='कार्बन', keys=gk), pop(t_c - .3), (560, S(.56)))
    tags = tag(200, S(.50), 'बंद कमरा', t_m + .3, 220, '#F7B5AD', 26)
    air = ''.join(f'<g transform="translate(600 {S(.30) + 40 + k * 50})">' + G('<path d="M0 0 q18 -14 36 0 t36 0" fill="none" stroke="#7CF0B5" stroke-width="7" stroke-linecap="round"/><path d="M72 0 l-12 -10 m12 10 l-12 10" stroke="#7CF0B5" stroke-width="6" stroke-linecap="round"/>', [[0, {'o': 0}], [t_fr + k * .45 - .001, {'o': 0, 'tx': 0}], [t_fr + k * .45, {'o': 1}], [t_fr + k * .45 + 1.6, {'tx': -150, 'ty': 30, 'o': 0}, 'o']]) + '</g>' for k in range(4))
    fresh = tag(550, S(.455), 'ताज़ी हवा', t_fr, 230, '#CDEBC5', 26)
    friend = acting('FRIEND', 90, FY - 40, .8, [(0, dict(pose='standing', expr='neutral')), (tf[0] - .05, dict(pose='pointing', expr='happy', talk=c.mouth('FRIEND')))], t_end=d)
    world = bgd + win + lamp + ac + floor + bed_ + sleeper + z + co2s + meter + tags + air + fresh + friend + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.04}, 'l']], (W() / 2, S(.5)), over_of(c) + dots_progress(3)


def glass_lbl(c, t):
    return label_box(360, S(.62), 340, 56, 'ताज़ा पानी लगभग शुद्ध', '#FFFFFF', INK, 22)


# ------------------------------------------------------------------ S5: can you drink it? (germs and metals)
def s5(c):
    d = c.d; tf = c.talk('FRIEND'); t_ge, t_le, t_co, t_lead, t_no = c.w('कीटाणु'), c.w('लेजियोनेयर्स'), c.w('धातुएँ'), c.w('धातुएँ'), c.w('मत')
    bgd = props.grad_bg('#4E7FA8', '#20405A') + sparkle_field(c, 20, 2, 0, .6)
    pan_ = (f'<path d="M80 {S(.40)} H640 L600 {S(.44)} H120 Z" fill="#9AA6AE" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><path d="M110 {S(.40)} H610 L585 {S(.43)} H135 Z" fill="#6FC3F0" fill-opacity=".85"/>'
            + caps(360, S(.465), 'ड्रेन पैन', 26, '#FFFFFF'))
    pipe = f'<path d="M600 {S(.42)} H650 Q690 {S(.42)} 690 {S(.46)} V{S(.62)}" fill="none" stroke="#F4F4F0" stroke-width="18" stroke-linecap="round"/>'
    coil = f'<path d="M120 {S(.33)} h40 l20 -40 l40 80 l40 -80 l40 80 l40 -80 l40 80 l40 -40 h40" fill="none" stroke="#7FD3FF" stroke-width="12" stroke-linejoin="round" stroke-linecap="round"/>' + caps(360, S(.275), 'कॉइल', 26, '#FFFFFF')
    rnd = random.Random(9); germs = ''
    for k in range(9):
        x = rnd.uniform(140, 580); y = S(.36) + rnd.uniform(-10, 60)
        germs += G(props.germ(x, y, rnd.uniform(.7, 1.1)), merge(pop(t_ge + k * .22), wiggle(t_ge + k * .22, d, 8, rnd.uniform(.5, 1.0), 'r'), bob(t_ge, d, 6, 1.4, 'ty')), (x, y))
    t1 = tag(190, S(.50), 'लेजियोनेयर्स का खतरा', t_le, 330, '#F7B5AD', 24) + tag(560, S(.50), 'धातुएँ', t_co, 170, '#F5C890', 26) + tag(560, S(.56), 'तांबा, सीसा', t_lead, 220, '#E8B7B0', 24)
    gl = props.glass(210, S(.80), 1.5, .6)
    xx = G(f'<path d="M150 {S(.80) - 220} L290 {S(.80) - 20} M290 {S(.80) - 220} L150 {S(.80) - 20}" stroke="{RED_}" stroke-width="18" stroke-linecap="round"/>', slam(t_no), (220, S(.76)))
    plant = G(props.potted_plant(560, FY + 60, 1.6), pop(tf[0]), (560, FY + 60))
    can = G(f'<path d="M440 {FY - 10} h60 l-6 40 h-48 Z" fill="#6FB0E0" stroke="{INK}" stroke-width="4"/><path d="M500 {FY - 2} l50 -20" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>', merge(pop(tf[0]), wiggle(tf[0], d, 8, .8, 'r')), (470, FY))
    friend = acting('FRIEND', 390, FY + 70, .95, [(0, dict(pose='standing', expr='worried')), (tf[0] - .05, dict(pose='laughing', expr='grin', talk=c.mouth('FRIEND')))], t_end=d)
    t_di, t_pc, t_pa, t_pi = c.w('कॉइल'), c.w('कॉइल'), c.w('पैन'), c.w('पाइप')
    world = bgd + G(coil, pop(t_pc), (360, S(.33))) + G(pan_, pop(t_pa), (360, S(.42))) + G(pipe, pop(t_pi), (650, S(.5))) + germs + t1 + gl + xx + plant + friend + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.04}, 'l']], (W() / 2, S(.5)), over_of(c) + dots_progress(4)


# ------------------------------------------------------------------ S6: conclusion + final joke
def s6(c):
    d = c.d; tb = c.talk('BANKER'); tg = c.talk('GUY'); t1 = c.w('नाली'); t2 = c.talk('BANKER')[0]; t3 = c.talk('GUY')[0]
    bgd = props.grad_bg('#F8EBCB', '#E2C892') + props.glow(360, S(.45), 360, '#FFFFFF', .5)
    def item(y, txt, t):
        return G(f'<rect x="40" y="{y - 40}" width="640" height="80" rx="16" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>' + mark(92, y, True, 1.2) + caps(134, y + 2, txt, 26, INK, 'start'), pop(t), (360, y))
    board = item(S(.30), 'एसी का पानी: नाली में, पीने को नहीं', t1) + item(S(.375), 'कमरा ज़्यादा सूखा न होने दें', t1 + 2.2) + item(S(.45), 'ताज़ी हवा आने दें', t1 + 3.6)
    fy = FY + 90
    banker = acting('BANKER', 150, fy, .85, [(0, dict(pose='standing', expr='smug')), (tb[0] - .05, dict(pose='talking', expr='grin', talk=c.mouth('BANKER')))], t_end=d)
    gl = G(props.glass(260, fy, 1.0, .6), pop(tb[0] - .2), (260, fy))
    guy = acting('GUY', 560, fy, .85, [(0, dict(pose='standing', expr='happy')), (tg[0] - .05, dict(pose='pointing', expr='worried', talk=c.mouth('GUY')))], t_end=d)
    germ = G(props.germ(300, fy - 190, 1.0), merge(pop(tg[0]), wiggle(tg[0], d, 10, .5, 'r')), (300, fy - 190))
    world = bgd + board + banker + gl + guy + germ + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.03}, 'l']], (W() / 2, S(.5)), over_of(c)


BUILDERS = {'S1': s1, 'S2': s2, 'S3': s3, 'S4': s4, 'S5': s5, 'S6': s6}
