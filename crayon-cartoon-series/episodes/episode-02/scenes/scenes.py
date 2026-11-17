"""Episode 2 scene animation (flight-grounding explainer). Uses only the shared libraries (cast, props, backgrounds)."""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from episode_tools import *
import cast, props, bg
from cast import acting, char
from cc_kit import money_bag, cash, burst, fill_bg, text, caps, SCRIPT_B, INK, sign, mark
from animlib import bob, wiggle, flicker, push, pull, pan, fade

FY = S(FLOOR)
RED_, GREEN_ = '#C0392F', '#3F9A50'


class C:
    def __init__(s, sc, sh, cue): s.sc, s.sh, s.cue = sc, sh, cue; s.d = sh['end'] - sh['start']
    def w(s, word, which='start'): return word_time(s.sh, word, which)
    def talk(s, who, i=0): return talks_of(s.sh, who, s.sc)[i]
    def mouth(s, who, i=0): return mouth_windows(s.sh, who, s.sc, i)


def note_text(c, t0=0.0, y=348, x=None):
    n = c.sc.get('note')
    return G(caps(W() / 2 if x is None else x, y, n, 28, '#4A4A4A'), fade(t0, .4)) if n else ''


# ------------------------------------------------------------------ S1: the board flips to GROUNDED
def s1(c):
    d = c.d; sc = c.sc
    t0, t1 = c.w('FAA'), c.w('airlines')
    flips = [t0 + (t1 - t0) * i / 3 for i in range(4)]
    board = props.flight_board(190, S(.33), 500, ['NEW YORK', 'LOS ANGELES', 'CHICAGO', 'DALLAS'], flips)
    tg = c.talk('GUY'); gx = 100
    guy = acting('GUY', gx, FY + 24, 1.3, [(0, dict(pose='standing', expr='happy')), (flips[1], dict(pose='confused', expr='worried')),
                                         (tg[0] - .05, dict(pose='shocked', expr='shocked', talk=c.mouth('GUY')))], t_end=d)
    bag = G(props.suitcase(gx + 62, FY + 24 - 40, 1.2), [[0, {'ty': 0}], [tg[1] - .1, {'ty': 0}], [tg[1] + .12, {'ty': 40}, 'i'], [tg[1] + .22, {'ty': 28}, 'o'], [tg[1] + .32, {'ty': 40}, 'i']], (gx + 62, FY))
    world = bg.flat('blue') + board + guy + bag
    over = headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), 72)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.06}, 'l']], (W() / 2, S(.45)), over


# ------------------------------------------------------------------ S2: glitch + red button
def s2(c):
    d = c.d; sc = c.sc
    t_weird = c.w('weird'); t_gs = c.w('ground'); tf = c.talk('FRIEND')
    radar = props.radar_screen(150, S(.285), 300, 230, glitch=t_weird)
    friend = acting('FRIEND', 130, FY, 1.35, [(0, dict(pose='standing', expr='worried')), (t_weird - .1, dict(pose='shocked', expr='shocked', talk=c.mouth('FRIEND'))),
                                             (tf[1] + .1, dict(pose='confused', expr='worried'))], t_end=d)
    friend = G(friend, merge(bob(t_weird, tf[1], 10, .3, 'ty'), [[tf[1], {'ty': 0}]]), (130, FY))
    pedestal = (f'<rect x="370" y="{FY - 178}" width="92" height="178" rx="8" fill="#6B452E" stroke="{INK}" stroke-width="5"/>')
    t_press = max(.6, c.w('ground') - .4)
    btn = G(f'<rect x="384" y="{FY - 196}" width="64" height="16" rx="6" fill="#8A1F1A" stroke="{INK}" stroke-width="3"/><circle cx="416" cy="{FY - 208}" r="26" fill="#E0382C" stroke="{INK}" stroke-width="3.6"/>'
            f'<ellipse cx="406" cy="{FY - 218}" rx="9" ry="5" fill="#F58A80" opacity=".7"/>', [[0, {'ty': 0}], [t_press - .02, {'ty': 0}], [t_press + .06, {'ty': 13}, 'o'], [t_press + .6, {'ty': 13}], [t_press + .72, {'ty': 0}, 'o']], (416, FY - 190))
    reach = ((-44, -80), (104, -136))
    banker = acting('BANKER', 560, FY, 1.4, [(0, dict(pose='standing', expr='smug', flip=True)), (t_press - .35, dict(pose='standing', expr='determined', arms=reach, flip=True)),
                                            (t_press + .4, dict(pose='laughing', expr='grin', flip=True))], t_end=d, flip=True)
    plaque = G(props.sign(560, FY - 310, 'FAA', size=34), pop(.3), (560, FY - 310)) if hasattr(props, 'sign') else ''
    stamp = G(f'<g transform="translate(255 {S(.40)}) rotate(-8)"><rect x="-210" y="-48" width="420" height="96" rx="10" fill="#FFFFFF" fill-opacity=".85" stroke="{RED_}" stroke-width="10"/>' + text(0, 4, 'GROUND STOP', 70, SCRIPT_B, RED_) + '</g>', slam(t_gs + .3), (255, S(.40)))
    world = bg.flat('mustard') + radar + pedestal + btn + friend + banker + stamp
    h1 = headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), 70, until=t_press)
    h2 = headline('3:54 PM: STOP!', t_press + .1, 70, col='#F2A9A0')
    return world, [[0, {'s': 1.0}], [d, {'s': 1.05}, 'l']], (W() / 2, S(.5)), h1 + h2


# ------------------------------------------------------------------ S3: planes on the ground vs in the air
def s3(c):
    d = c.d; sc = c.sc
    t_no, t_al = c.w('nobody'), c.w('already')
    clouds = props.cloud_shape(120, S(.22), 1.1) + props.cloud_shape(590, S(.31), .9) + props.cloud_shape(330, S(.42), .8)
    py = FY - 62
    gp = ''
    for i, x in enumerate((150, 520)):
        gp += G(props.plane(x, py, 1.05), jitter(t_no, d - .3, 2.4, seed=4 + i, y=False), (x, py))
        gp += G(props.stop_sign(x, py - 168, 1.15), pop(t_no + i * .15), (x, py - 168))
    fly_y = S(.395)
    t_b = max(3.5, t_al - .9)
    fly = G(props.plane(0, fly_y, 1.0), merge([[0, {'tx': -300}], [.2, {'tx': -300}], [3.3, {'tx': 1020}, 'l'], [3.31, {'tx': -300}], [t_b, {'tx': -300}], [t_b + 3.0, {'tx': 1020}, 'l']],
                                              [[0, {'ty': 0}], [1.2, {'ty': -24}, 'io'], [2.4, {'ty': 18}, 'io'], [3.3, {'ty': 0}, 'io'], [t_b + 1.0, {'ty': -26}, 'io'], [t_b + 2.2, {'ty': 18}, 'io'], [t_b + 3.0, {'ty': 0}, 'io']]), (0, fly_y))
    go = G(sign(540, S(.31), 'KEEP GOING', size=32, fill='#8ED08B'), pop(t_al + .1), (540, S(.31)))
    world = bg.flat('blue') + clouds + gp + fly + go
    over = headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), 72)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.0}, 'l']], (W() / 2, S(.45)), over


# ------------------------------------------------------------------ S4: the router floods the network
def packet(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-26" y="-18" width="52" height="36" rx="6" fill="#4DA3FF" stroke="{INK}" stroke-width="3.4"/>'
            + text(0, 2, '0101', 20, CAPS, '#FFFFFF') + '</g>')


def s4(c):
    d = c.d; sc = c.sc
    t_fl = c.w('flooding'); t_cy = c.w('cyberattack'); tf = c.talk('FRIEND')
    rx, ry = 330, FY + 6
    rt = G(props.router(rx, ry, 1.55, 'worried', sweat=True), merge(jitter(t_fl - .2, d - .6, 3, seed=5)), (rx, ry))
    r = random.Random(9); pk = ''
    for i in range(34):
        ts = t_fl - .1 + r.uniform(0, 2.8)
        vx, vy = r.uniform(-360, 360), r.uniform(-640, -240)
        pk += G(packet(rx, ry - 190, r.uniform(.8, 1.2)), projectile_keys(ts, 2.4, (vx, vy), 900, r.uniform(-300, 300), ground=(FY + 26 - (ry - 190) + r.uniform(-10, 40))), (rx, ry - 190))
    radar = props.radar_screen(40, S(.285), 250, 190, glitch=t_fl + .4)
    friend = acting('FRIEND', 585, FY, 1.3, [(0, dict(pose='standing', expr='worried')), (tf[0] - .05, dict(pose='shocked', expr='shocked', talk=c.mouth('FRIEND')))], t_end=d)
    ark = G(sign(140, S(.50), 'ARKANSAS', size=34, fill='#D9A441'), pop(c.w('router') + .2), (140, S(.50)))
    clear = G(f'<rect x="90" y="{S(.395)}" width="540" height="78" rx="14" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>' + mark(140, S(.395) + 39, True, 1.3) + caps(390, S(.395) + 41, 'NO CYBERATTACK FOUND', 34, GREEN_),
              pop(t_cy), (360, S(.395) + 39))
    world = bg.flat('red') + radar + ark + pk + rt + friend + clear
    over = headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), 70)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.05}, 'l']], (W() / 2, S(.5)), over


# ------------------------------------------------------------------ S5: the domino effect
def s5(c):
    d = c.d; sc = c.sc
    t_four, t_sev = c.w('four'), c.w('seven'); tg = c.talk('GUY')
    by = S(.325)
    box = (f'<rect x="130" y="{by}" width="460" height="140" rx="18" fill="#8A1F1A" stroke="{INK}" stroke-width="6"/>'
           + count_text(325, by + 72, 88, 0, 7000, t_sev, t_sev + 1.6, 'int') + text(470, by + 74, '+', 88, CAPS, '#FFFFFF')
           + caps(360, by - 26, 'FLIGHTS CANCELLED THAT FRIDAY', 32, INK))
    clock = G(f'<rect x="40" y="{S(.53)}" width="250" height="96" rx="48" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>' + caps(165, S(.53) + 50, '4+ HOURS', 44, '#8A1F1A'), pop(t_four), (165, S(.53) + 48))
    gx = 530
    guy = acting('GUY', gx, FY + 10, 1.0, [(0, dict(pose='standing', expr='closed')), (tg[0] - .1, dict(pose='confused', expr='sad', talk=c.mouth('GUY')))], t_end=d)
    zz = G(text(gx + 64, S(.55), 'Z z z', 40, SCRIPT_B, '#4A4A4A'), merge([[0, {'o': 1, 'ty': 0}], [tg[0] - .12, {'o': 1, 'ty': -30}, 'l'], [tg[0] - .1, {'o': 0}]]), (gx + 64, S(.55)))
    bag = props.suitcase(gx - 62, FY + 10, 1.0)
    world = bg.flat('cream') + box + clock + bag + guy + zz + note_text(c, 1.0, by + 168, 250)
    over = headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), 66)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.0}, 'l']], (W() / 2, S(.45)), over


# ------------------------------------------------------------------ S6: the money angle
def s6(c):
    d = c.d; sc = c.sc
    t_a, t_b = c.w('twelve'), c.w('fifty'); tb = c.talk('BANKER')
    base = S(.605)
    bars = (f'<path d="M80 {base} H460" stroke="{INK}" stroke-width="5"/>'
            + G(f'<rect x="120" y="{base - 105}" width="130" height="105" fill="#6FBF6A" stroke="{INK}" stroke-width="5"/>', [[0, {'sy': 0}], [t_a, {'sy': 0}], [t_a + .6, {'sy': 1}, 'b']], (185, base))
            + G(f'<rect x="300" y="{base - 420}" width="130" height="340" fill="#E0382C" stroke="{INK}" stroke-width="5"/>', [[0, {'sy': 0}], [t_b, {'sy': 0}], [t_b + .8, {'sy': 1}, 'b']], (365, base))
            + G(caps(185, base - 132, '$12.5B', 44, INK), pop(t_a + .5), (185, base - 132)) + G(caps(365, base - 372, '$50B', 56, '#8A1F1A'), pop(t_b + .7), (365, base - 372))
            + caps(185, base + 34, 'APPROVED', 26, INK) + caps(365, base + 34, 'REQUESTED', 26, INK))
    bx, hy = 590, FY - 104 * 1.3
    banker = acting('BANKER', bx, FY, 1.3, [(0, dict(pose='holding', expr='smug')), (tb[0] - .1, dict(pose='holding', expr='worried', talk=c.mouth('BANKER')))], t_end=d)
    t_w = tb[0] + .1
    wal = G(props.wallet(bx, hy, .85), merge([[0, {'r': 0}], [t_w, {'r': 0}], [t_w + .28, {'r': 180}, 'b']], [[t_w, {'ty': 0}], [t_w + .28, {'ty': -8}, 'o']]), (bx, hy))
    gy = FY + 6 - (hy + 16)
    coin = G(props.coin(bx, hy + 16, 1.2), merge([[0, {'o': 0}], [t_w + .5, {'o': 0}], [t_w + .51, {'o': 1}], [t_w + 2.5, {'o': 1}]],
                                                   [[t_w + .5, {'ty': 0, 'tx': 0}], [t_w + .8, {'ty': gy, 'tx': -20}, 'i'], [t_w + 1.0, {'ty': gy - 40, 'tx': -45}, 'o'], [t_w + 1.2, {'ty': gy, 'tx': -60}, 'i']]), (bx, hy + 16))
    world = bg.flat('mustard') + bars + banker + wal + coin + note_text(c, 1.0, 348)
    over = headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), 70)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.0}, 'l']], (W() / 2, S(.45)), over


# ------------------------------------------------------------------ S7: refund, not credit (+ final joke)
def pretzel(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-30 20 C-50 -10 -20 -40 0 -14 C20 -40 50 -10 30 20 C14 34 -14 34 -30 20 Z" fill="#C98A4B" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M-14 0 L14 -2" stroke="{INK}" stroke-width="3.4"/><circle cx="-12" cy="10" r="2" fill="#FFF3D0"/><circle cx="10" cy="12" r="2" fill="#FFF3D0"/><circle cx="0" cy="-6" r="2" fill="#FFF3D0"/></g>')


def s7(c):
    d = c.d; sc = c.sc
    t_ref, t_cr = c.w('refund'), c.w('credit'); l1 = c.sh['lines'][1]; tg = c.talk('GUY')
    counter = (f'<rect x="20" y="{FY - 120}" width="680" height="{120 + 60}" fill="{props.WOOD}" stroke="{INK}" stroke-width="5"/><rect x="10" y="{FY - 136}" width="700" height="22" rx="4" fill="#8A5A3A" stroke="{INK}" stroke-width="5"/>'
               + sign(400, FY - 400, 'AIRLINE', size=40, fill='#E8D8A8'))
    agent = acting('FRIEND', 560, FY, 1.45, [(0, dict(pose='standing', expr='happy')), (t_cr - .2, dict(pose='talking', expr='smug', arms='present')), (t_ref + .5, dict(pose='confused', expr='surprised')),
                                           (l1['t0'] - .1, dict(pose='standing', expr='grin'))], t_end=d)
    voucher = G(f'<g transform="translate(420 {FY - 168})"><rect x="-70" y="-28" width="140" height="56" rx="8" fill="#F7F7F5" stroke="{INK}" stroke-width="4"/>' + caps(0, 2, 'CREDIT', 34, '#8A1F1A') + '</g>',
                merge(pop(t_cr), [[t_ref + .45, {'o': 1}], [t_ref + .46, {'o': 0}, 'h']]), (420, FY - 168))
    money = G(''.join(cash(420 + dx, FY - 150 - k * 6, .75, r) for k, (dx, r) in enumerate(((-20, -8), (14, 6), (-4, -2)))), [[0, {'o': 0}], [t_ref + .5, {'o': 0}], [t_ref + .51, {'o': 1, 's': .6}], [t_ref + .75, {'s': 1}, 'b']], (420, FY - 150))
    guy = acting('GUY', 180, FY + 36, 1.5, [(0, dict(pose='standing', expr='happy')), (t_ref - .25, dict(pose='shocked', expr='determined')), (tg[0] - .05, dict(pose='talking', expr='happy', talk=c.mouth('GUY')))], t_end=d)
    refsign = G(f'<g transform="translate(180 {FY - 360})"><rect x="-120" y="-44" width="240" height="88" rx="10" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>' + text(0, 4, 'REFUND', 62, SCRIPT_B, '#3F9A50') + f'</g><path d="M180 {FY - 316} V{FY - 300}" stroke="{INK}" stroke-width="6"/>',
                pop(t_ref - .1), (180, FY - 360))
    pret = G(pretzel(430, FY - 150, 1.0), [[0, {'o': 0}], [l1['t0'] - .6, {'o': 0}], [l1['t0'] - .59, {'o': 1, 's': .6}], [l1['t0'] - .35, {'s': 1}, 'b']], (430, FY - 150))
    world = bg.flat('cream') + counter + agent + voucher + money + pret + guy + refsign + note_text(c, 1.0, 348)
    over = headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), 64)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.05}, 'l']], (W() / 2, S(.5)), over


def g_at(svg, x, y): return f'<g transform="translate({x} {y})">{svg}</g>'


BUILDERS = {'S1': s1, 'S2': s2, 'S3': s3, 'S4': s4, 'S5': s5, 'S6': s6, 'S7': s7}
