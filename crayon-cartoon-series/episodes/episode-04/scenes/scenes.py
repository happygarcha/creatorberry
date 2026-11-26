"""Episode 4 scene animation: Panthalassa, the wave-powered AI data centers at sea. Shared libraries only (cast, props, bg)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from episode_tools import *
import cast, props, bg
from cast import acting, char
from cc_kit import cash, burst, fill_bg, text, caps, SCRIPT_B, INK, mark, money_bag
from animlib import bob, wiggle, flicker, push, pull, pan, fade, draw

FY = S(FLOOR)
RED_, GREEN_, BLUE_ = '#C0392F', '#3F9A50', '#4DA3FF'


class C:
    def __init__(s, sc, sh, cue): s.sc, s.sh, s.cue = sc, sh, cue; s.d = sh['end'] - sh['start']
    def w(s, word, which='start'): return word_time(s.sh, word, which)
    def talk(s, who, i=0): return talks_of(s.sh, who, s.sc)[i]
    def mouth(s, who, i=0): return mouth_windows(s.sh, who, s.sc, i)


def note_text(c, t0=0.0, y=None):
    """Source credit: small, low-contrast, tucked into the bottom-right corner (never in the middle of the frame)."""
    n = c.sc.get('note')
    col = '#E8EEF4' if c.sc['background'] in ('navy', 'blue', 'red') else '#3A3A3A'
    return G(caps(W() - 36, S(.792), n, 14, col, anchor='end'), [[0, {'o': 0}], [t0, {'o': 0}], [t0 + .4, {'o': .72}]]) if n else ''


def over_of(c, size=64):
    sc = c.sc
    return headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), size)


def label_box(x, y, w, h, txt, fill='#FFFFFF', col=INK, size=26):
    return f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{INK}" stroke-width="4"/>' + caps(x, y + 2, txt, size, col)


def sea(c, name='ocean', front=True, t_end=None):
    """Sky + sea band with a gently sliding wave edge. Returns (back, front) layers: front waves are drawn after the node (translucent)."""
    d = c.d
    back = bg.flat(name) + props.waves(FY - 2, 900, 12, props.SEA_TOP, wiggle(0, d, 30, 6, 'tx'), n=9)
    fr = G(props.waves(FY + 12, 900, 14, '#2F6286', wiggle(0, d, 24, 5, 'tx'), x0=-100), [[0, {'o': .55}]])
    return back, fr


def node_bob(c, x, y, s, label=None, amp=12, per=2.6, tube=300):
    return G(props.ocean_node(x, y, s, tube, label), merge(bob(0, c.d, amp, per, 'ty'), wiggle(0, c.d, 3, 5.2, 'r')), (x, y))


def tag(x, y, txt, t, w=330, fill='#FFFFFF', size=24):
    return G(label_box(x, y, w, 62, txt, fill, INK, size), pop(t), (x, y))


# ------------------------------------------------------------------ S1: hook
def s1(c):
    d = c.d; tg = c.talk('GUY')
    back, fr = sea(c)
    node = node_bob(c, 500, FY, 1.15)
    stars = G(props.satellite(560, S(.17), .55), bob(0, d, 8, 3, 'ty'), (560, S(.17)))
    pier = props.pier(-30, FY, 330)
    guy = acting('GUY', 120, FY, 1.3, [(0, dict(pose='standing', expr='worried')), (tg[0] - .05, dict(pose='shocked', expr='shocked', talk=c.mouth('GUY')))], t_end=d)
    friend = acting('FRIEND', 250, FY, 1.3, [(0, dict(pose='confused', expr='worried'))], t_end=d)
    world = back + stars + node + fr + pier + guy + friend + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.07}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S2: the problem
def s2(c):
    d = c.d; tb = c.talk('BANKER'); tf = c.talk('FRIEND')
    t_h, t_e, t_c, t_p = c.w('hungry'), c.w('electricity'), c.w('cooling'), c.w('permits')
    chip = G(props.ai_chip(360, S(.32), 1.5), merge(wiggle(t_h, d - .5, 5, .3, 'r'), pop(t_h - .3)), (360, S(.32)))
    mouth = G(f'<path d="M300 {S(.32) + 26} Q360 {S(.32) + 70} 420 {S(.32) + 26}" fill="#8A1F1A" stroke="{INK}" stroke-width="5"/>', flicker(t_h, d - .5, .5), (360, S(.32) + 40))
    boxes = tag(360, S(.44), 'ELECTRICITY', t_e, 280, '#FFF2B0') + tag(360, S(.505), 'COOLING WATER', t_c, 280, '#CFE8F7') + tag(360, S(.57), 'LAND + PERMITS', t_p, 280, '#F7D1CC')
    banker = acting('BANKER', 140, FY + 40, 1.1, [(0, dict(pose='standing', expr='worried')), (tb[0] - .05, dict(pose='confused', expr='worried', talk=c.mouth('BANKER')))], t_end=d)
    friend = acting('FRIEND', 580, FY + 40, 1.1, [(0, dict(pose='standing', expr='worried')), (tf[0] - .05, dict(pose='pointing', expr='grin', talk=c.mouth('FRIEND')))], t_end=d)
    world = bg.flat('mustard') + chip + mouth + boxes + banker + friend + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.04}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S3: who is Panthalassa
def s3(c):
    d = c.d; tf = c.talk('FRIEND'); t_pa = c.w('Panthalassa')
    cx, cy = 360, S(.40)
    ring = G(f'<circle cx="{cx}" cy="{cy}" r="190" fill="#6FA8C8" stroke="{INK}" stroke-width="7"/><circle cx="{cx}" cy="{cy}" r="158" fill="none" stroke="#9CC7DE" stroke-width="5" stroke-dasharray="14 12"/>'
             + caps(cx, cy + 172, 'THE GIANT OCEAN', 26, '#FFFFFF'), pop(t_pa), (cx, cy))
    land = G(f'<path d="M{cx - 90} {cy - 50} C{cx - 100} {cy - 110} {cx - 20} {cy - 120} {cx + 30} {cy - 90} C{cx + 100} {cy - 100} {cx + 120} {cy - 20} {cx + 80} {cy + 30} C{cx + 90} {cy + 90} {cx + 10} {cy + 100} {cx - 30} {cy + 70} C{cx - 100} {cy + 80} {cx - 120} {cy + 10} {cx - 90} {cy - 50} Z" fill="#9CCB7B" stroke="{INK}" stroke-width="6"/>'
             + caps(cx, cy, 'PANGAEA', 40, INK), pop(c.w('Pangaea') - .6), (cx, cy))
    tags = tag(190, S(.60), 'PORTLAND, OREGON', c.w('Portland'), 250, '#FFFFFF', 22) + tag(450, S(.60), 'FOUNDED 2016', c.w('founded'), 200, '#FFF2B0', 22) + tag(300, S(.655), 'PUBLIC BENEFIT COMPANY', c.w('public'), 360, '#CDEBC5', 22)
    friend = acting('FRIEND', 628, FY - 40, .8, [(0, dict(pose='standing', expr='happy')), (tf[0] - .05, dict(pose='laughing', expr='grin', talk=c.mouth('FRIEND')))], t_end=d)
    world = bg.flat('cream', floor=False) + ring + land + tags + friend + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.03}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S4: the node
def s4(c):
    d = c.d; tg = c.talk('GUY'); t_g, t_b, t_t = c.w('giant'), c.w('ball'), c.w('tube')
    back, fr = sea(c)
    nx = 380
    node = node_bob(c, nx, FY - 6, 1.25, amp=8)
    ann = (G(f'<path d="M540 {FY - 150} L{nx + 80} {FY - 100}" stroke="{INK}" stroke-width="4"/>' + label_box(580, FY - 175, 170, 60, 'AIR BALL = FLOAT', '#FFFFFF', INK, 18), pop(t_b), (580, FY - 175))
           + G(f'<path d="M140 {FY + 200} L{nx - 40} {FY + 200}" stroke="{INK}" stroke-width="4"/>' + label_box(120, FY + 200, 200, 60, 'LONG STEEL TUBE', '#FFFFFF', INK, 20), pop(t_t), (120, FY + 200)))
    dim = G(f'<path d="M610 {FY - 170} V{FY + 350}" stroke="{INK}" stroke-width="5"/><path d="M598 {FY - 170} H622 M598 {FY + 350} H622" stroke="{INK}" stroke-width="5"/>'
            + label_box(560, FY + 90, 130, 80, '', '#F7D35C') + caps(560, FY + 78, '~85 m', 34, INK) + caps(560, FY + 108, '(reported)', 20, INK), pop(t_g), (560, FY + 90))
    guy = acting('GUY', 110, FY - 4, 1.2, [(0, dict(pose='confused', expr='worried')), (tg[0] - .05, dict(pose='laughing', expr='happy', talk=c.mouth('GUY')))], t_end=d)
    world = back + node + fr + ann + dim + guy + props.pier(-30, FY - 4, 250) + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.04}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S5: waves make power
def s5(c):
    d = c.d; tf = c.talk('FRIEND'); t_l, t_s, t_e = c.w('lift'), c.w('spin'), c.w('electricity')
    back, fr = sea(c)
    nx = 380; per = 2.6
    node = node_bob(c, nx, FY - 6, 1.25, amp=14, per=per)
    # water dots moving up and down the tube (inside the bobbing node, so they ride with it)
    dots = ''.join(G(f'<circle cx="{nx + dx}" cy="{FY - 6 + 160 * 1.25}" r="6" fill="#4DA3FF" stroke="{INK}" stroke-width="2"/>', merge(bob(t_l + k * .25, d, 60, per, 'ty')), (nx, FY)) for k, dx in enumerate((-8, 6, -2)))
    tur = props.turbine(nx, FY - 6 + 280 * 1.25, 1.1, spin=(t_s - .4, d))
    bolt = G(f'<path d="M0 -60 L-26 4 H-4 L-14 62 L28 -12 H6 L24 -60 Z" fill="#FFD54A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>', merge(pop(t_e), wiggle(t_e + .4, d, 6, .5, 'r')), (0, 0))
    bolt = f'<g transform="translate(560 {S(.28)}) scale(1.6)">{bolt}</g>'
    lab = tag(560, S(.37), 'ELECTRICITY', t_e, 240, '#FFF2B0') + G(label_box(130, FY + 125, 210, 50, 'WATER UP + DOWN', '#CFE8F7', INK, 20), pop(t_l), (130, FY + 125)) + G(label_box(130, FY + 185, 210, 50, 'TURBINES SPIN', '#F7D35C', INK, 20), pop(t_s), (130, FY + 185))
    friend = acting('FRIEND', 110, FY - 4, 1.2, [(0, dict(pose='standing', expr='neutral')), (tf[0] - .05, dict(pose='laughing', expr='grin', talk=c.mouth('FRIEND')))], t_end=d)
    world = back + node + dots + tur + fr + bolt + lab + friend + props.pier(-30, FY - 4, 250) + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.03}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S6: chips, cooling, satellite, Roomba
def s6(c):
    d = c.d; tf = c.talk('FRIEND'); t_ch, t_co, t_sa, t_ro = c.w('chips'), c.w('cold'), c.w('satellite'), c.w('Roomba')
    sat = G(props.satellite(540, S(.30), .8), merge(bob(0, d, 10, 3, 'ty'), pop(t_sa - .8)), (540, S(.30)))
    beam1 = G(f'<path d="M480 {S(.33)} L230 {S(.415)}" stroke="#FFD54A" stroke-width="5" stroke-dasharray="12 10" stroke-linecap="round"/>', draw(t_sa, .8))
    house = G(f'<path d="M80 {S(.455)} H190 V{S(.52)} H80 Z" fill="#F7F7F5" stroke="{INK}" stroke-width="5"/><path d="M70 {S(.455)} L135 {S(.415)} L200 {S(.455)} Z" fill="#B8524A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>', pop(t_sa + .4), (135, S(.49)))
    back, fr = sea(c, 'navy')
    node = node_bob(c, 560, FY, .85, amp=8)
    capsule = G(f'<rect x="110" y="{FY + 20}" width="270" height="150" rx="26" fill="#DDE6EC" stroke="{INK}" stroke-width="6"/>' + props.ai_chip(245, FY + 90, .75) +
                f'<path d="M140 {FY + 135} v-20 M130 {FY + 125} h20 M340 {FY + 60} v20 M330 {FY + 70} h20" stroke="{BLUE_}" stroke-width="5" stroke-linecap="round"/>'
                + caps(245, FY + 196, 'SEALED + COOLED BY SEA', 19, '#FFFFFF'), pop(t_ch), (245, FY + 90))
    cold = G(label_box(500, FY + 150, 200, 50, 'NO FRESH WATER', '#CFE8F7', INK, 20), pop(t_co), (480, FY + 150))
    rb = G(props.roomba(240, FY + 255, 1.0), merge(pop(t_ro - .3), wiggle(t_ro, d, 14, 1.4, 'r'), bob(t_ro, d, 6, 1.0, 'tx')), (240, FY + 255)) + G(label_box(240, FY + 195, 220, 46, 'STEERS ITSELF', '#FFF2B0', INK, 20), pop(t_ro + .3), (240, FY + 195))
    friend = acting('FRIEND', 600, FY + 340, .8, [(0, dict(pose='standing', expr='worried')), (tf[0] - .05, dict(pose='shocked', expr='shocked', talk=c.mouth('FRIEND')))], t_end=d)
    world = back + sat + beam1 + house + node + fr + capsule + cold + rb + friend + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.03}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S7: the money
def s7(c):
    d = c.d; tb = c.talk('BANKER'); t_h, t_t, t_b = c.w('hundred'), c.w('total'), c.w('billion')
    box = (f'<rect x="90" y="{S(.29)}" width="540" height="170" rx="18" fill="#8A1F1A" stroke="{INK}" stroke-width="7"/>'
           + text(190, S(.29) + 112, '$', 100, CAPS, '#FFFFFF') + count_text(360, S(.29) + 112, 104, 0, 140, t_h, t_h + 2.2, 'int') + text(528, S(.29) + 112, 'M', 100, CAPS, '#FFFFFF'))
    box = G(box, pop(t_h - .2), (360, S(.29) + 85))
    thiel = G(label_box(360, S(.29) - 70, 420, 60, 'LED BY PETER THIEL (MAY 2026)', '#FFFFFF', INK, 22), pop(t_h + .2), (360, S(.29) - 70))
    total = tag(360, S(.29) + 235, 'TOTAL RAISED: ~$210M', t_t, 440, '#FFF2B0', 28)
    val = G(label_box(360, S(.29) + 320, 440, 64, 'VALUE ~ $1 BILLION (REPORTED)', '#CDEBC5', INK, 24), pop(t_b), (360, S(.29) + 320))
    banker = acting('BANKER', 150, FY + 170, .8, [(0, dict(pose='standing', expr='smug')), (tb[0] - .05, dict(pose='talking', expr='grin', talk=c.mouth('BANKER')))], t_end=d)
    bags = G(money_bag(560, FY + 170, 1.0), merge(pop(t_t), bob(t_t, d, 6, 1.2, 'ty')), (560, FY + 170))
    world = bg.flat('mustard') + thiel + box + total + val + banker + bags + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.04}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S8: where it is now
def s8(c):
    d = c.d; tg = c.talk('GUY')
    t1, t2, t3, t4, t5 = c.w('Ocean'), c.w('fifty'), c.w('factory'), c.w('Next'), c.w('planned')
    x0 = 120; ys = [S(.35), S(.41), S(.47), S(.53), S(.59)]
    line = G(f'<path d="M{x0} {ys[0]} V{ys[-1]}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>', draw(t1, 1.4), (x0, ys[0]))
    def pin(y, a, b, t, col):
        return G(f'<circle cx="{x0}" cy="{y}" r="22" fill="{col}" stroke="{INK}" stroke-width="6"/>' + caps(x0 + 50, y - 12, a, 32, INK, 'start') + caps(x0 + 50, y + 22, b, 24, '#4A4A4A', 'start'), pop(t), (x0, y))
    o = (pin(ys[0], '2021: OCEAN-1', 'first sea tests', t1, '#CFE8F7') + pin(ys[1], 'OCEAN-2', 'up to 50 kW reported', t2, '#CFE8F7') + pin(ys[2], 'NOV 2026: FACTORY', 'Vancouver, Washington', t3, '#9AD59A')
         + pin(ys[3], 'OCEAN-3 PILOTS', 'northern Pacific (planned)', t4, '#F7D35C') + pin(ys[4], '2027: COMMERCIAL', 'planned', t5, '#F7D35C'))
    fac = G(props.factory(580, S(.50), 240, .7), pop(t3), (580, S(.50)))
    guy = acting('GUY', 580, FY + 170, .8, [(0, dict(pose='standing', expr='happy')), (tg[0] - .05, dict(pose='laughing', expr='happy', talk=c.mouth('GUY')))], t_end=d)
    world = bg.flat('cream') + line + o + fac + guy + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.03}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S9: the catch
def s9(c):
    d = c.d; tg = c.talk('GUY'); tf = c.talk('FRIEND')
    t1, t2, t3, t4 = c.w('history'), c.w('audited'), c.w('Repairs'), c.w('satellite')
    def flag(y, txt, t):
        return G(f'<rect x="60" y="{y - 40}" width="600" height="80" rx="14" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/><path d="M96 {y + 24} V{y - 24} L134 {y - 12} L96 {y}" fill="#C0392F" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>' + caps(160, y + 2, txt, 25, INK, 'start'), pop(t), (360, y))
    o = flag(S(.27), 'WAVE POWER HAS BROKEN IN ROUGH SEAS BEFORE', t1) + flag(S(.34), 'NO AUDITED DATA YET: OUTPUT, UPTIME', t2) + flag(S(.41), 'REPAIRS ARE HARD FAR FROM SHORE', t3) + flag(S(.48), 'SATELLITE LINKS: SLOWER THAN CABLES', t4)
    guy = acting('GUY', 150, FY + 120, .85, [(0, dict(pose='standing', expr='worried')), (tg[0] - .05, dict(pose='confused', expr='worried', talk=c.mouth('GUY')))], t_end=d)
    friend = acting('FRIEND', 570, FY + 120, .85, [(0, dict(pose='standing', expr='worried')), (tf[0] - .05, dict(pose='shocked', expr='shocked', talk=c.mouth('FRIEND')))], t_end=d)
    world = bg.flat('red') + o + guy + friend + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.04}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S10: conclusion + final joke
def s10(c):
    d = c.d; tg = c.talk('GUY'); tf = c.talk('FRIEND'); t_g, t_gb, t_m = c.w('genius'), c.w('gamble'), c.w('Mondays')
    back, fr = sea(c)
    node = node_bob(c, 560, FY - 20, .8, amp=10)
    beam = G(f'<path d="M-170 0 H170" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
             + f'<g transform="translate(-170 0)"><path d="M0 0 L-60 90 H60 Z" fill="none" stroke="{INK}" stroke-width="4"/><rect x="-95" y="90" width="190" height="64" rx="12" fill="#CDEBC5" stroke="{INK}" stroke-width="5"/>' + caps(0, 124, 'GENIUS', 30, INK) + '</g>'
             + f'<g transform="translate(170 0)"><path d="M0 0 L-60 90 H60 Z" fill="none" stroke="{INK}" stroke-width="4"/><rect x="-95" y="90" width="190" height="64" rx="12" fill="#F7D1CC" stroke="{INK}" stroke-width="5"/>' + caps(0, 124, 'SOGGY GAMBLE', 24, INK) + '</g>',
             merge(wiggle(t_g, d - .5, 7, 2.4, 'r'), pop(t_g - .3)), (0, 0))
    scale = f'<g transform="translate(360 {S(.33)})">{beam}<path d="M0 0 V260" stroke="{INK}" stroke-width="9"/></g>'
    chatbot = G(props.ai_chip(590, FY + 140, .7, '#7FBF6A', 'AI') + caps(590, FY + 78, 'seasick...', 24, '#1F5A2A'), merge(pop(tg[0]), wiggle(t_m - .5, d, 10, .35, 'r')), (590, FY + 140))
    guy = acting('GUY', 120, FY + 100, 1.0, [(0, dict(pose='standing', expr='happy')), (tg[0] - .05, dict(pose='confused', expr='worried', talk=c.mouth('GUY')))], t_end=d)
    friend = acting('FRIEND', 300, FY + 100, 1.0, [(0, dict(pose='standing', expr='neutral')), (tf[0] - .05, dict(pose='laughing', expr='grin', talk=c.mouth('FRIEND')))], t_end=d)
    t_pr, t_ld, t_se = c.w('proves'), c.w('land'), c.w('sea')
    extra = tag(360, S(.585), 'MONTHS + YEARS, NOT DAYS', t_pr, 420, '#FFF2B0', 24) + tag(360, S(.645), 'LAND RUNS LOW ON POWER', t_ld, 420, '#F7D1CC', 24) + G(f'<path d="M520 {FY + 20} Q560 {FY - 40} 600 {FY - 10}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>' + caps(560, FY - 52, 'THE SEA!', 28, '#1F5A8A'), pop(t_se), (560, FY - 20))
    t_kn, t_wk, t_dy = c.w('know'), c.w('work'), c.w('days')
    extra += G(mark(120, S(.585), True, 1.3), pop(t_kn), (120, S(.585))) + G(mark(120, S(.645), False, 1.3), pop(t_wk), (120, S(.645))) + G(burst(600, S(.615), 50, '#F7D35C', 10), pop(t_dy), (600, S(.615)))
    world = back + node + fr + scale + extra + chatbot + guy + friend + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.04}, 'l']], (W() / 2, S(.5)), over_of(c)


BUILDERS = {'S1': s1, 'S2': s2, 'S3': s3, 'S4': s4, 'S5': s5, 'S6': s6, 'S7': s7, 'S8': s8, 'S9': s9, 'S10': s10}
