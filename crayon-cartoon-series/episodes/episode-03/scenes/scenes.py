"""Episode 3 scene animation: the Microsoft 365 / Outlook outage of November 12-13, 2026. Shared libraries only."""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from episode_tools import *
import cast, props, bg
from cast import acting, char
from cc_kit import cash, burst, fill_bg, text, caps, SCRIPT_B, INK, sign, mark, chart, crowd, phone_old, globe
from animlib import bob, wiggle, flicker, push, pull, pan, fade, draw

FY = S(FLOOR)
RED_, GREEN_, BLUE_ = '#C0392F', '#3F9A50', '#4DA3FF'


class C:
    def __init__(s, sc, sh, cue): s.sc, s.sh, s.cue = sc, sh, cue; s.d = sh['end'] - sh['start']
    def w(s, word, which='start'): return word_time(s.sh, word, which)
    def talk(s, who, i=0): return talks_of(s.sh, who, s.sc)[i]
    def mouth(s, who, i=0): return mouth_windows(s.sh, who, s.sc, i)


def note_text(c, t0=0.0, y=368):
    n = c.sc.get('note')
    return G(caps(W() / 2, y, n, 22, '#4A4A4A'), fade(t0, .4)) if n else ''


def window(svg, t0, t1=None):
    """Show svg only between local times t0 and t1 (hard cuts)."""
    k = [[0, {'o': 0}], [max(0, t0 - .001), {'o': 0}], [t0, {'o': 1}, 'h']]
    if t1 is not None: k += [[t1 - .001, {'o': 1}], [t1, {'o': 0}, 'h']]
    return G(svg, k)


def label_box(x, y, w, h, txt, fill='#FFFFFF', col=INK, size=26):
    return f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{INK}" stroke-width="4"/>' + caps(x, y + 2, txt, size, col)


def over_of(c, y=None, size=68):
    sc = c.sc
    return headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), size) if y is None else headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), size, y=y)


# ------------------------------------------------------------------ S1: the spinner that never stops
def s1(c):
    d = c.d; sc = c.sc
    t_ban = c.talk('BANKER')[0] - .9; tg = c.talk('GUY'); tb = c.talk('BANKER')
    desk = (f'<rect x="30" y="{FY - 120}" width="390" height="120" fill="{props.WOOD}" stroke="{INK}" stroke-width="5"/><rect x="20" y="{FY - 136}" width="410" height="20" rx="4" fill="#8A5A3A" stroke="{INK}" stroke-width="5"/>')
    scr = (f'<rect x="90" y="{FY - 330}" width="270" height="190" rx="12" fill="#2D3036" stroke="{INK}" stroke-width="5"/><rect x="102" y="{FY - 318}" width="246" height="166" rx="6" fill="#EAF3FB"/>'
           f'<rect x="170" y="{FY - 150}" width="110" height="14" fill="#2D3036" stroke="{INK}" stroke-width="3"/>'
           f'<rect x="170" y="{FY - 300}" width="110" height="74" rx="14" fill="{BLUE_}" stroke="{INK}" stroke-width="4"/>' + text(225, FY - 262, 'O', 64, SCRIPT_B, '#FFFFFF'))
    spin = props.spinner(225, FY - 190, 22)
    envs = ''
    for i in range(7):
        t = 1.2 + i * .75
        envs += G(props.envelope(60 + (i % 4) * 90, FY - 440 - (i // 4) * 60 + (i % 2) * 20, .7), pop(t), (60 + (i % 4) * 90, FY - 440))
    guy = acting('GUY', 470, FY, 1.35, [(0, dict(pose='confused', expr='worried', look=-5)), (tg[0] - .05, dict(pose='shocked', expr='shocked', talk=c.mouth('GUY')))], t_end=d)
    banker = acting('BANKER', 610, FY, 1.35, [(0, dict(pose='walking', expr='angry', walk=(t_ban, t_ban + .9))), (tb[0] - .1, dict(pose='angry', expr='angry', talk=c.mouth('BANKER')))], t_end=d)
    banker = G(banker, [[0, {'tx': 320}], [t_ban, {'tx': 320}], [t_ban + .9, {'tx': 0}, 'o']], (610, FY))
    world = bg.flat('blue') + desk + scr + spin + envs + guy + banker
    return world, [[0, {'s': 1.0}], [d, {'s': 1.05}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S2: error reports spike
def s2(c):
    d = c.d; sc = c.sc
    t_sp, t_h = c.w('spiked'), c.w('hundred'); tf = c.talk('FRIEND')
    pts = [.04, .05, .06, .05, .08, .1, .12, .95, 1.0, .9, .85]
    board = chart(200, S(.295), 480, 250, pts, RED_, 'ERROR REPORTS', kf_line=draw(t_sp, 2.2))
    box = (f'<rect x="200" y="{S(.295) + 290}" width="480" height="100" rx="16" fill="#8A1F1A" stroke="{INK}" stroke-width="6"/>'
           + count_text(420, S(.295) + 342, 70, 0, 129000, t_h, t_h + 3.2, 'int') + text(612, S(.295) + 342, '+', 70, CAPS, '#FFFFFF'))
    ring = (G(f'<path d="M-44 -170 q-12 20 0 40 M-58 -176 q-18 28 0 52 M44 -170 q12 20 0 40 M58 -176 q18 28 0 52" fill="none" stroke="{RED_}" stroke-width="5" stroke-linecap="round"/>',
              merge(wiggle(tf[0] - 2.5, d - .2, 6, .24)) , (0, 0)))
    friend = acting('FRIEND', 95, FY, 1.25, [(0, dict(pose='standing', expr='worried')), (t_sp, dict(pose='confused', expr='shocked')), (tf[0] - .05, dict(pose='shocked', expr='shocked', talk=c.mouth('FRIEND')))], t_end=d)
    ph = G(phone_old(150, FY - 200, .8), wiggle(t_sp, d - .2, 8, .22), (150, FY - 200))
    world = bg.flat('mustard') + board + box + friend + ph + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.03}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S3: one engine, many apps
def s3(c):
    d = c.d; sc = c.sc
    hub = (360, S(.435))
    nodes = {'Outlook': (135, S(.355)), 'Teams calendar': (555, S(.355)), 'Copilot': (135, S(.54)), 'SharePoint': (555, S(.54))}
    when = {'Outlook': c.w('Outlook'), 'Teams calendar': c.w('Teams'), 'Copilot': c.w('Copilot'), 'SharePoint': c.w('SharePoint')}
    o = ''
    for name, (x, y) in nodes.items():
        o += f'<path d="M{hub[0]} {hub[1]} L{x} {y}" stroke="{INK}" stroke-width="6"/>'
    o += label_box(hub[0], hub[1], 290, 100, 'EXCHANGE ONLINE', '#FFD54A', INK, 36) + caps(hub[0], hub[1] + 74, 'the email engine', 28, INK)
    for name, (x, y) in nodes.items():
        o += label_box(x, y, 210, 74, name.upper(), '#FFFFFF', INK, 26)
        o += G(mark(x + 80, y - 42, False, 1.4), pop(when[name]), (x + 80, y - 42))
    t_chat = c.w('chat')
    o += G(label_box(360, S(.54), 250, 84, 'TEAMS CHAT + CALLS', '#CDEBC5', GREEN_, 24) + mark(360 + 112, S(.54) - 46, True, 1.4), pop(t_chat), (360, S(.54)))
    t_f = c.w('four')
    o += G(label_box(360, S(.615), 440, 66, '450 MILLION+ BUSINESS SEATS', '#F7D35C', INK, 28), pop(t_f), (360, S(.615)))
    world = bg.flat('blue', floor=False) + fill_bg('#7C9AB5') + o + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.0}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S4: not a hack
def s4(c):
    d = c.d; sc = c.sc
    t_no = c.w('no'); tg = c.talk('GUY'); tf = c.talk('FRIEND')
    shield = (f'<path d="M360 {S(.33)} L460 {S(.355)} V{S(.43)} Q460 {S(.50)} 360 {S(.535)} Q260 {S(.50)} 260 {S(.43)} V{S(.355)} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>' + mark(360, S(.43), True, 3.2))
    stamp = f'<g transform="translate(360 {S(.60)}) rotate(-6)"><rect x="-290" y="-52" width="580" height="104" rx="10" fill="#FFFFFF" fill-opacity=".9" stroke="{RED_}" stroke-width="9"/>' + text(0, 6, 'NOT A CYBERATTACK', 64, SCRIPT_B, RED_) + '</g>'
    guy = acting('GUY', 150, FY, 1.35, [(0, dict(pose='confused', expr='worried')), (tg[0] - .05, dict(pose='laughing', expr='happy', talk=c.mouth('GUY')))], t_end=d)
    friend = acting('FRIEND', 570, FY, 1.35, [(0, dict(pose='standing', expr='worried')), (tf[0] - .05, dict(pose='confused', expr='worried', talk=c.mouth('FRIEND')))], t_end=d)
    world = bg.flat('red') + G(shield, pop(t_no), (360, S(.43))) + G(stamp, slam(t_no + .3), (360, S(.60))) + guy + friend + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.04}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S5: the front door and the July fix
def s5(c):
    d = c.d; sc = c.sc
    t_j, t_sm, t_th = c.w('July'), c.w('smoothly'), c.w('three')
    door = props.gateway_door(220, FY + 6, 200, 260, 'FRONT DOOR') + caps(220, FY + 40, 'special front-door servers', 24, INK)
    flow = ''
    for i in range(10):
        t0 = .8 + i * 1.3
        flow += G(props.envelope(30, FY - 70, .8), [[0, {'o': 0}], [t0, {'o': 0, 'tx': 0}], [t0 + .02, {'o': 1}], [t0 + 1.8, {'tx': 660}, 'l'], [t0 + 1.82, {'o': 0}]], (30, FY - 70))
    cx = 555
    cal = G(f'<rect x="{cx - 115}" y="{S(.315)}" width="230" height="170" rx="12" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/><rect x="{cx - 115}" y="{S(.315)}" width="230" height="48" rx="12" fill="{RED_}" stroke="{INK}" stroke-width="5"/>'
            + caps(cx, S(.315) + 26, 'JULY', 36, '#FFFFFF') + caps(cx, S(.315) + 98, 'WINDOWS FIX', 28, INK) + caps(cx, S(.315) + 136, 'ADDED', 28, INK) + mark(cx + 96, S(.315) + 140, True, 1.3), pop(t_j), (cx, S(.315) + 85))
    ty = S(.52)
    timer = G(label_box(cx, ty, 230, 130, '', '#FFFFFF') + count_text(cx - 40, ty - 10, 70, 0, 3, t_th, t_th + 1.6, 'int') + text(cx + 22, ty - 8, '+', 70, CAPS, INK) + caps(cx, ty + 44, 'MONTHS, NO PROBLEMS', 22, GREEN_), pop(t_th - .1), (cx, ty))
    friend = acting('FRIEND', 400, FY, 1.2, [(0, dict(pose='standing', expr='happy')), (t_sm, dict(pose='laughing', expr='grin'))], t_end=d)
    world = bg.flat('cream') + flow + door + cal + timer + friend + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.0}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S6: the sleeper bug
def s6(c):
    d = c.d; sc = c.sc
    t_sl, t_lab, t_lock = c.w('sleeper'), c.w('lab'), c.w('lock'); tf = c.talk('FRIEND')
    lab = props.server_unit(70, S(.30), 190, 70, 'ok', 'LAB: WEAKER HARDWARE') + G(mark(280, S(.30) + 35, True, 1.4), pop(t_lab), (280, S(.30) + 35))
    big_ok = window(props.server_unit(400, S(.30), 270, 100, 'ok', 'NEW POWERFUL SERVER'), 0, t_lock)
    big_dn = window(props.server_unit(400, S(.30), 270, 100, 'down', 'NEW POWERFUL SERVER'), t_lock)
    rug = f'<path d="M230 {FY - 8} H490 L470 {FY + 26} H250 Z" fill="#B8524A" stroke="{INK}" stroke-width="5"/>'
    bugg = G(props.bug(360, FY, 1.5, True), pop(t_sl), (360, FY))
    zz = G(text(440, FY - 140, 'Z z z', 44, SCRIPT_B, '#4A4A4A'), merge(bob(t_sl, d - .5, 6, 1.0, 'ty')), (440, FY - 140))
    friend = acting('FRIEND', 95, FY, 1.1, [(0, dict(pose='confused', expr='worried')), (tf[0] - .05, dict(pose='shocked', expr='sad', talk=c.mouth('FRIEND')))], t_end=d)
    world = bg.flat('blue') + lab + big_ok + big_dn + bugg + rug + zz + friend + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.03}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S7: two more things piled on
def s7(c):
    d = c.d; sc = c.sc
    t_t, t_15, t_14 = c.w('Teams'), c.w('fifteen'), c.w('fourteen')
    door = props.gateway_door(450, FY + 6, 170, 220, 'FRONT DOOR')
    crowd_svg = G(crowd(40, 330, FY - 10, rows=2, s=1.0, seed=3, hats=.15) + sign(185, FY - 190, 'TEAMS TRAFFIC', size=30, fill='#B9A7E0'), merge([[0, {'tx': -420}], [t_t - .2, {'tx': -420}], [t_t + 1.6, {'tx': 90}, 'o']]), (185, FY))
    clock = G(label_box(160, S(.30), 250, 66, '15 HOURS EARLIER', '#FFFFFF', INK, 26), pop(t_15), (160, S(.30)))
    xs = [78 + k * 82 for k in range(7)]
    servers = ''
    for k, x in enumerate(xs):
        servers += props.server_unit(x - 36, S(.37), 72, 46, 'ok')
    dark = G(props.server_unit(xs[3] - 36, S(.37), 72, 46, 'down'), [[0, {'o': 0}], [t_14 - .001, {'o': 0}], [t_14, {'o': 1}, 'h']])
    cap = G(label_box(480, S(.30), 300, 66, '14% OUT OF SERVICE', '#F2A9A0', INK, 26), pop(t_14), (480, S(.30)))
    guy = acting('GUY', 610, FY, 1.1, [(0, dict(pose='standing', expr='worried')), (t_14, dict(pose='shocked', expr='shocked'))], t_end=d)
    world = bg.flat('mustard') + clock + cap + servers + dark + door + crowd_svg + guy + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.02}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S8: the domino effect
def s8(c):
    d = c.d; sc = c.sc
    t_l, t_s, t_e = c.w('locked'), c.w('safety'), c.w('eighty'); tb = c.talk('BANKER')
    n = 8; base = FY - 10
    srv = ''
    t_fall = [t_l + k * (max(1.0, (t_e - t_l - .5)) / n) for k in range(n)]
    for k in range(n):
        x = 36 + k * 60
        ok = props.server_unit(x, base - 130, 46, 130, 'ok')
        dn = props.server_unit(x, base - 130, 46, 130, 'down')
        srv += G(ok, [[0, {'o': 1}], [t_fall[k] - .001, {'o': 1}], [t_fall[k], {'o': 0}, 'h']])
        srv += G(dn, [[0, {'o': 0, 'r': 0}], [t_fall[k] - .001, {'o': 0, 'r': 0}], [t_fall[k], {'o': 1, 'r': 0}, 'h'], [t_fall[k] + .45, {'r': 14}, 'o']], (x + 46, base))
    arrows = ''
    for k in range(n - 1):
        arrows += G(props.envelope(36 + k * 60 + 55, base - 170, .6), [[0, {'o': 0}], [t_fall[k], {'o': 0}], [t_fall[k] + .05, {'o': 1}], [t_fall[k] + .6, {'o': 0}]], (36 + k * 60 + 55, base - 170))
    cnt = (f'<rect x="130" y="{S(.34)}" width="440" height="110" rx="16" fill="#8A1F1A" stroke="{INK}" stroke-width="6"/>'
           + count_text(330, S(.34) + 56, 78, 0, 80, t_e, t_e + 1.4, 'int') + text(430, S(.34) + 58, '%+', 78, CAPS, '#FFFFFF') + caps(350, S(.34) - 22, 'SERVERS STOPPED RESPONDING', 26, '#FFFFFF'))
    safety = G(label_box(360, S(.455), 600, 60, 'SAFETY NET: MOVE TRAFFIC TO HEALTHY SERVERS', '#FFFFFF', INK, 22), pop(t_s), (360, S(.455)))
    banker = acting('BANKER', 640, FY + 24, 1.3, [(0, dict(pose='standing', expr='worried')), (tb[0] - .05, dict(pose='confused', expr='shocked', talk=c.mouth('BANKER')))], t_end=d)
    world = bg.flat('red') + cnt + safety + srv + arrows + banker + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.02}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S9: slow recovery and the rollback
def s9(c):
    d = c.d; sc = c.sc
    t_sw, t_un, t_ro = c.w('swamped'), c.w('undo'), c.w('rolled'); t_as, t_eu = c.w('Asia'), c.w('Europe'); tg = c.talk('GUY')
    row = ''.join(props.server_unit(50 + k * 96, S(.40), 76, 80, 'ok') for k in range(6))
    wave = G(''.join(props.envelope(30 + k * 44, S(.40) - 50 - (k % 3) * 28, .7) for k in range(14)), [[0, {'o': 0}], [t_sw - .1, {'o': 0, 'tx': -300}], [t_sw, {'o': 1}], [t_sw + 1.6, {'tx': 360}, 'l'], [t_sw + 1.8, {'o': 0}]], (360, S(.4)))
    swamped = window(row + G(label_box(360, S(.345), 440, 64, 'RESTARTED: SWAMPED!', '#F2A9A0', INK, 34), pop(t_sw), (360, S(.345))), t_sw - .2, t_un - .3)
    undo = window(label_box(230, S(.43), 270, 120, 'UNDO', '#FFFFFF', INK, 64) + mark(470, S(.43), False, 3.0) + caps(360, S(.55), 'THE CHANGE WAS MONTHS OLD', 34, '#8A1F1A'), t_un - .1, t_ro - .2)
    groups = (G(label_box(180, S(.51), 290, 130, 'ASIA PACIFIC', '#CDEBC5', GREEN_, 34) + mark(290, S(.51) - 56, True, 1.5), pop(t_as), (180, S(.51)))
              + G(label_box(480, S(.51), 230, 130, 'EUROPE', '#CDEBC5', GREEN_, 38) + mark(570, S(.51) - 56, True, 1.5), pop(t_eu), (480, S(.51))))
    rollback = window(G(label_box(360, S(.38), 520, 88, 'CODE ROLLED BACK', '#FFD54A', INK, 44), pop(t_ro), (360, S(.38))) + groups, t_ro - .1)
    guy = acting('GUY', 650, FY + 20, .9, [(0, dict(pose='thinking', expr='worried')), (tg[0] - .05, dict(pose='talking', expr='smug', talk=c.mouth('GUY')))], t_end=d)
    power = G(f'<circle cx="480" cy="{FY - 40}" r="38" fill="#E0382C" stroke="{INK}" stroke-width="6"/><path d="M480 {FY - 66} V{FY - 38}" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/><path d="M462 {FY - 54} A22 22 0 1 0 498 {FY - 54}" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>',
              pop(tg[0] - .2), (480, FY - 40))
    world = bg.flat('blue') + swamped + wave + undo + rollback + guy + power + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.0}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S10: back to normal
def s10(c):
    d = c.d; sc = c.sc
    t_f, t_fu, t_bk = c.w('Friday'), c.w('fully'), c.w('backlog')
    ys = [S(.315), S(.405), S(.495), S(.585)]
    line = G(f'<path d="M110 {ys[0]} V{ys[3]}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>', draw(.3, 1.6), (110, S(.48)))
    def node(y, title, sub, t, col):
        return G(f'<circle cx="110" cy="{y}" r="26" fill="{col}" stroke="{INK}" stroke-width="6"/>' + caps(165, y - 18, title, 40, INK, 'start') + caps(165, y + 22, sub, 30, '#4A4A4A', 'start'), pop(t), (110, y))
    o = (node(ys[0], 'THU: OUTLOOK STOPS', 'midday Eastern', .4, '#F2A9A0') + node(ys[1], 'FRI MORNING', 'webmail normal worldwide', t_f, '#CDEBC5')
         + node(ys[2], 'FRI LATE', 'incident fully restored', t_fu, '#9AD59A') + node(ys[3], 'EMAIL BACKLOG', 'processed', t_bk, '#9AD59A'))
    guy = acting('GUY', 625, FY + 10, 1.0, [(0, dict(pose='confused', expr='worried')), (t_f, dict(pose='laughing', expr='happy'))], t_end=d)
    world = bg.flat('cream') + line + o + guy + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.0}, 'l']], (W() / 2, S(.5)), over_of(c)


# ------------------------------------------------------------------ S11: conclusion + final joke
def s11(c):
    d = c.d; sc = c.sc
    t_g, t_c, t_b = c.w('good'), c.w('check'), c.w('backup'); tb = c.talk('BANKER'); tg = c.talk('GUY')
    def item(y, txt, t):
        return G(f'<rect x="40" y="{y - 38}" width="640" height="76" rx="14" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>' + mark(90, y, True, 1.2) + caps(130, y + 2, txt, 27, INK, 'start'), pop(t), (360, y))
    board = item(S(.335), 'DELAYED EMAIL WAS NOT LOST', t_g) + item(S(.41), 'CHECK WHAT YOU SENT THU/FRI', t_c) + item(S(.485), 'KEEP A BACKUP WAY TO REACH PEOPLE', t_b)
    banker = acting('BANKER', 150, FY + 52, .8, [(0, dict(pose='standing', expr='smug')), (tb[0] - .1, dict(pose='talking', expr='grin', talk=c.mouth('BANKER')))], t_end=d)
    stack = G(''.join(props.envelope(150 + dx, FY - 60 - k * 14, .6, '#FFFFFF') for k, dx in enumerate((-8, 6, -4, 8, 0))), pop(tb[0] - .2), (150, FY - 60))
    guy = acting('GUY', 560, FY + 52, .8, [(0, dict(pose='standing', expr='happy')), (tg[0] - .1, dict(pose='shocked', expr='crying', talk=c.mouth('GUY')))], t_end=d)
    world = bg.flat('cream') + board + banker + stack + guy + note_text(c, 1.0)
    return world, [[0, {'s': 1.0}], [d, {'s': 1.0}, 'l']], (W() / 2, S(.5)), over_of(c)


BUILDERS = {'S1': s1, 'S2': s2, 'S3': s3, 'S4': s4, 'S5': s5, 'S6': s6, 'S7': s7, 'S8': s8, 'S9': s9, 'S10': s10, 'S11': s11}
