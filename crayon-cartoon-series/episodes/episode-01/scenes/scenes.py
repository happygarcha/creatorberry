"""Episode 1 scene animation. Each sN(c) returns the SVG for one scene; timing comes from the TTS timeline (c.sh) so the
animation is locked to the voices. Everything is built from the shared libraries (cast, props, backgrounds)."""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from episode_tools import *
import cast, props, bg
from cast import acting, char
from cc_kit import money_bag, cash, money_pile, burst, tw, fill_bg, text, SCRIPT_B, INK
from animlib import bob, wiggle, flicker, push, pull, pan, fade

FY = S(FLOOR)


class C:
    """Per-scene context: episode scene json, timeline shot, global cue function."""
    def __init__(s, sc, sh, cue): s.sc, s.sh, s.cue = sc, sh, cue; s.d = sh['end'] - sh['start']
    def w(s, word, which='start'): return word_time(s.sh, word, which)
    def talk(s, who, i=0): return talks_of(s.sh, who, s.sc)[i]
    def mouth(s, who, i=0): return mouth_windows(s.sh, who, s.sc, i)


def stack_keys(*lists): return merge(*lists)


# ------------------------------------------------------------------ S1
def s1(c):
    d = c.d; x = 230; s = 1.85
    t_flip, t_coin = .55, 1.3; why = c.w('why')
    guy = acting('GUY', x, FY, s, [(0, dict(pose='holding', expr='worried')), (2.7, dict(pose='holding', expr='sad', look=6)),
                                   (why - .15, dict(pose='holding', expr='worried', look=0))], t_end=d)
    hy = FY - 104 * s
    wallet = G(props.wallet(x, hy, 1.15), merge(
        [[0, {'r': 0}], [t_flip, {'r': 0}], [t_flip + .28, {'r': 180}, 'b']],
        [[.95, {'r': 172}, 'io'], [1.05, {'r': 190}], [1.15, {'r': 174}], [1.25, {'r': 187}], [1.35, {'r': 180}]],
        [[t_flip, {'ty': 0}], [t_flip + .28, {'ty': -10}, 'o'], [1.4, {'ty': -10}]]), (x, hy))
    gy = FY + 14 - (hy + 22)
    coin = G(props.coin(x, hy + 22, 1.5), merge(
        [[0, {'o': 0}], [t_coin - .001, {'o': 0}], [t_coin, {'o': 1}], [3.78, {'o': 1}], [3.8, {'o': 0}]],
        [[t_coin, {'tx': 0, 'ty': 0, 'r': 0}], [1.62, {'tx': 30, 'ty': gy, 'r': 120}, 'i'], [1.92, {'tx': 70, 'ty': gy - 80, 'r': 260}, 'o'],
         [2.2, {'tx': 120, 'ty': gy, 'r': 400}, 'i'], [2.4, {'tx': 150, 'ty': gy - 38, 'r': 500}, 'o'], [2.55, {'tx': 175, 'ty': gy, 'r': 560}, 'i'],
         [2.63, {'tx': 188, 'ty': gy - 14, 'r': 600}, 'o'], [2.7, {'tx': 198, 'ty': gy, 'r': 620}, 'i'], [3.8, {'tx': 560, 'ty': gy, 'r': 1900}, 'l']]), (x, hy + 22))
    behind = big_word('WHY?', c.w('why'), 125, S(.40), '#FFFFFF', x=425)
    cam = [[0, {'s': 1.0}], [why, {'s': 1.0}], [why + .45, {'s': 1.2}, 'o']]
    world = bg.flat('red') + behind + guy + wallet + coin
    over = headline(c.sc['headline']['text'], resolve_at(c.sh, c.sc['headline']['at']), 72)
    return world, cam, (330, S(.36)), over


# ------------------------------------------------------------------ S2
def s2(c):
    d = c.d; sc = c.sc
    t_press = .35; tf = c.w('right', 'end') + .05
    c.freeze = tf
    px, py = 460, FY + 8
    printer = G(props.printer(px, py, 1.0, spin=(.5, tf), press=t_press), jitter(.5, tf, 4, seed=2), (px, py))
    bills = bill_storm(px, py - 90, 48, .55, spread=(-330, 330), up=(-860, -420), g=720, seed=5, freeze=tf, floor=FY + 30, dur=3.4, stagger=tf - 1.2)
    reach = ((-44, -80), (129, -169))
    tb = c.talk('BANKER')
    banker = acting('BANKER', 360, FY, 1.5, [(0, dict(pose='standing', expr='smug')), (.15, dict(pose='standing', expr='smug', arms=reach)),
                                             (.75, dict(pose='talking', expr='grin', talk=c.mouth('BANKER'), arms=((-44, -80), (96, -112)))),
                                             (tb[1] + .05, dict(pose='talking', expr='smug'))], t_end=d)
    steps = [(0, dict(pose='standing', expr='happy')), (.45, dict(pose='shocked', expr='surprised'))]
    t, k = .9, 0
    while t < tf - .1:
        steps.append((round(t, 2), dict(pose='shocked' if k % 2 == 0 else 'laughing', expr='grin'))); t += .24; k += 1
    steps.append((tf, dict(pose='shocked', expr='grin')))
    steps.append((c.w('watch') - .05, dict(pose='confused', expr='worried')))
    guy = G(acting('GUY', 130, FY, 1.4, steps, t_end=d), merge(bob(.9, tf, 30, .48, 'ty'), wiggle(.9, tf, 4, .48), [[tf, {'ty': 0, 'r': 0}]]), (130, FY))
    world = bg.flat('mustard') + printer + banker + guy + bills
    cam = [[0, {'s': 1.0}], [tf, {'s': 1.05}, 'l']]
    over = headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), 72)
    return world, cam, (W() / 2, FY - 200), over


# ------------------------------------------------------------------ S3
def s3(c):
    d = c.d; sc = c.sc
    back, front = props.bakery(W(), FY)
    t_fifty = c.w('fifty'); t_gold = c.w('gold'); l2_end = c.sh['lines'][2]['t1']; t_bread = c.w('bread')
    tf1, tf2, tg = c.talk('FRIEND'), c.talk('GUY', 0), c.talk('GUY', 1)
    baker = acting('FRIEND', 560, FY, 1.5, [(0, dict(pose='standing', expr='happy')), (tf1[0] - .1, dict(pose='talking', expr='smug', talk=c.mouth('FRIEND'), arms='present')),
                                            (tf1[1] + .1, dict(pose='standing', expr='smug'))], t_end=d)
    steps = [(0, dict(pose='walking', walk=(0, 1.0), expr='happy', arms='down')), (1.0, dict(pose='standing', expr='happy', talk=c.mouth('GUY', 0))),
             (tf1[0] + .6, dict(pose='confused', expr='surprised')), (tg[0] - .05, dict(pose='shocked', expr='shocked', talk=c.mouth('GUY', 1))),
             (l2_end + .15, dict(pose='shocked', expr='crying'))]
    gx, gy = 190, FY + 36
    guy = acting('GUY', gx, gy, 1.55, steps, t_end=d)
    hop_t = l2_end + .15
    guy_g = G(guy, merge([[0, {'tx': -330}], [1.0, {'tx': 0}, 'o']], hop(hop_t + .05, 36, .34, 3)), (gx, gy))
    bag = G(money_bag(gx + 66, gy - 10, 1.45), merge([[0, {'tx': -330}], [1.0, {'tx': 0}, 'o']],
            [[l2_end - .3, {'ty': -120}], [l2_end - .3 + .0001, {'ty': -120}], [hop_t, {'ty': 0}, 'i'], [hop_t + .08, {'ty': -10}, 'o'], [hop_t + .16, {'ty': 0}, 'i']]), (gx + 66, gy))
    loaf = G(props.bread(345, FY - 190 + 2, 1.5), pop(t_bread - .3), (345, FY - 190))
    tag = G(props.price_tag(445, 500, '$5', 1.4, '$50,000', t_fifty, size=26), shake(t_fifty + .02, 5, .3), (445, 500))
    world = bg.flat('blue', floor=False) + fill_bg('#7C9AB5') + back + baker + front + loaf + tag + guy_g + bag
    cam = [[0, {'s': 1.04, 'tx': 10}], [d, {'s': 1.04, 'tx': -10}, 'l']]
    over = headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), 70)
    return world, cam, (W() / 2, FY - 150), over


# ------------------------------------------------------------------ S4
def s4(c):
    d = c.d; sc = c.sc
    t_ten, t_pay = c.w('ten'), c.w('pay'); t_problem = c.w('problem')
    base = bg.flat('cream')
    rack = (f'<rect x="372" y="300" width="330" height="170" fill="#8A5A3A" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="384" y="312" width="306" height="146" fill="#6A432A" stroke="{INK}" stroke-width="2.6"/>'
            f'<rect x="372" y="388" width="330" height="12" fill="#8A5A3A" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="372" y="468" width="330" height="12" fill="#8A5A3A" stroke="{INK}" stroke-width="3"/>')
    loaves = ''
    for i in range(10):
        row, col = divmod(i, 5)
        t = (t_problem + .6) + i * (max(.35, (t_ten - t_problem - .6)) / 9)
        loaves += G(props.bread(414 + col * 62, 388 + (0 if row == 0 else 80), .6), pop(t), (414 + col * 62, 388 + row * 80))
    counter = (f'<rect x="372" y="640" width="330" height="{FY + 40 - 640}" fill="{props.WOOD}" stroke="{INK}" stroke-width="4"/>'
               f'<rect x="362" y="626" width="350" height="20" rx="4" fill="#8A5A3A" stroke="{INK}" stroke-width="4"/>')
    tf = c.talk('FRIEND')
    baker = acting('FRIEND', 600, FY, 1.4, [(0, dict(pose='standing', expr='happy')), (tf[0] - .1, dict(pose='talking', expr='smug', talk=c.mouth('FRIEND'))),
                                            (tf[1] + .1, dict(pose='laughing', expr='smug'))], t_end=d)
    rows = [(95, FY + 46, 1.25, 'maroon', 'top'), (200, FY + 46, 1.25, 'navy', None), (305, FY + 46, 1.25, 'green', 'fedora'),
            (60, FY, 1.1, 'black', 'top'), (150, FY, 1.1, 'brown', None), (250, FY, 1.1, 'maroon', 'fedora'), (345, FY, 1.1, 'navy', 'top')]
    crowd = ''; r = random.Random(4)
    for i, (x, y, s, suit, hat) in enumerate(rows):
        t0 = .05 + i * .13; t1 = t0 + 1.0
        arr = acting_extra(x, y, s, suit, hat, t0, t1, t_pay + .05 + r.uniform(0, .12), d)
        crowd += G(arr, merge([[0, {'tx': -520}], [t0, {'tx': -520}], [t1, {'tx': 0}, 'o']], bob(t1, d, 6, .7 + .05 * i, 'ty')), (x, y))
    world = base + rack + loaves + counter + baker + crowd
    cam = [[0, {'s': 1.05, 'tx': 18}], [d, {'s': 1.05, 'tx': -18}, 'l']]
    over = headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), 62)
    return world, cam, (W() / 2, FY - 150), over


def held_note(x, y, s): return cash(x + 30 * s, y - 108 * s, .5 * s, 12)


def acting_extra(x, y, s, suit, hat, t_walk0, t_walk1, t_hands, d):
    """Wealthy bystander: walks in, holds a banknote, throws both hands (and the note) up on cue."""
    f1 = cast.crowd_member(x, y, s, suit, hat, 'happy', 'hold', walk=(t_walk0, t_walk1)) + held_note(x, y, s)
    f2 = cast.crowd_member(x, y, s, suit, hat, 'grin', 'up')
    note = cash(x, y - 285 * s, .7 * s, -8)
    return (G(f1, [[0, {'o': 1}], [t_hands - .001, {'o': 1}], [t_hands, {'o': 0}, 'h']]) +
            G(f2 + note, [[0, {'o': 0}], [t_hands - .001, {'o': 0}], [t_hands, {'o': 1}, 'h']]))


# ------------------------------------------------------------------ S5
def s5(c):
    d = c.d; sc = c.sc
    l0 = c.sh['lines'][0]; t_b = l0['t1'] + .45
    t_inf = c.w('inflation')
    # ---- board
    colL, colR = 190, 530
    stacks = ''
    for i, sx in enumerate((110, 180, 250)):
        for row in range(3):
            stacks += props.money_stack(sx, 625 - row * 72, 5, 62, kf=[[0, {'sy': 0}], [.4 + i * .3 + row * .45, {'sy': 0}], [1.0 + i * .3 + row * .45, {'sy': 1}, 'b']])
    bread_rows = ''.join(props.bread(436 + col * 56, 505 + row * 66, .5) for row in range(2) for col in range(5))
    price_y = 748
    board = (fill_bg('#E0B24A')
             + caps(colL, 352, 'MONEY', 58) + caps(colR, 352, 'BREAD', 58)
             + G(arrow_up(335, 495), [[0, {'o': 0}], [2.5, {'o': 0}], [2.6, {'o': 1}]])
             + stacks + bread_rows
             + caps(colR, 631, 'ALWAYS 10', 36, '#8A1F1A')
             + f'<rect x="196" y="{price_y - 54}" width="328" height="108" rx="16" fill="#8A1F1A" stroke="{INK}" stroke-width="5"/>'
             + count_text(360, price_y, 78, 5, 50000, 2.6, t_b - .3, 'money')
             + caps(360, price_y - 76, 'PRICE OF BREAD', 34))
    board = G(board, [[0, {'tx': 0}], [t_b, {'tx': 0}], [t_b + .35, {'tx': -780}, 'i']])
    # ---- characters
    tg, tb = c.talk('GUY'), None
    gx, bx = 190, 540
    bag = money_bag(gx + 80, FY + 4, 2.1)
    guy = acting('GUY', gx, FY, 1.5, [(0, dict(pose='standing', expr='happy')), (tg[0] - .05, dict(pose='shocked', expr='shocked', talk=c.mouth('GUY'))),
                                      (tg[1] + .05, dict(pose='confused', expr='sad'))], t_end=d)
    baker = acting('FRIEND', bx, FY, 1.5, [(0, dict(pose='standing', expr='smug', arms='present')), (tg[1] - .2, dict(pose='standing', expr='grin', arms='present'))], t_end=d)
    t_hand = t_b + .7
    crumb = G(props.crumb(bx - 60, FY - 150, 2.6), merge([[0, {'o': 0}], [t_hand - .001, {'o': 0}], [t_hand, {'o': 1}],
                                                          [t_hand, {'tx': 0, 'ty': 0}], [t_hand + .7, {'tx': -250, 'ty': 40}, 'io']]), (bx - 60, FY - 150))
    chars = G(bg.flat('mustard') + bag + guy + baker + crumb, [[0, {'o': 0}], [t_b - .001, {'o': 0}], [t_b, {'o': 1, 'tx': 780}], [t_b + .35, {'tx': 0}, 'o']])
    note = G(caps(W() / 2, 826, '(a simplified example)', 28, '#5A3A12'), [[0, {'o': 0}], [t_inf + .3, {'o': 0}], [t_inf + .4, {'o': 1}], [t_b - .001, {'o': 1}], [t_b, {'o': 0}, 'h']])
    world = fill_bg('#E0B24A') + board + chars
    cam = [[0, {'s': 1.0}], [t_b, {'s': 1.0}], [d, {'s': 1.08}, 'l']]
    over = headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), 90, until=t_b) + note
    return world, cam, (W() / 2, FY - 150), over


def arrow_up(x, y):
    return (f'<path d="M{x - 40} {y + 34} L{x} {y - 22} L{x + 40} {y + 34} H{x + 16} V{y + 66} H{x - 16} V{y + 34} Z" fill="{RED_}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')


RED_ = '#C0392F'


# ------------------------------------------------------------------ S6
def s6(c):
    d = c.d; sc = c.sc
    t_press = c.w('printing'); t_boom = t_press + .1
    l1 = c.sh['lines'][1]; t_crash = l1['t1'] + .05
    px, py = 470, FY + 22
    wheels = ''.join(f'<g transform="translate({px + wx} {py + 24})"><circle r="22" fill="#2B2F36" stroke="{INK}" stroke-width="4"/><path d="M-14 0 H14 M0 -14 V14" stroke="#7F8B94" stroke-width="4"/></g>' for wx in (-100, 100))
    entry = [[0, {'tx': 420}], [.2, {'tx': 420}], [1.1, {'tx': 0}, 'o']]
    printer = G(props.printer(px, py, 1.15, spin=(t_boom, t_crash), press=t_press) + wheels,
                merge(entry, jitter(t_boom, t_crash - .05, 9, seed=7), [[0, {'r': 0}], [t_crash, {'r': 0}], [t_crash + .35, {'r': 34, 'ty': 22}, 'i']]), (px + 150, py + 40))
    reach = ((-44, -80), (119, -186))
    tb = c.talk('BANKER')
    banker = acting('BANKER', 395, FY, 1.5, [(0, dict(pose='standing', expr='grin', arms='present', talk=c.mouth('BANKER'))), (t_press - .25, dict(pose='standing', expr='grin', arms=reach, talk=c.mouth('BANKER'))),
                                             (t_press + .4, dict(pose='confused', expr='shocked')), (t_press + 1.2, dict(pose='confused', expr='worried'))], t_end=d)
    banker = G(banker, merge(entry, [[t_press + .5, {'tx': 0}], [t_press + 1.3, {'tx': -120}, 'io']]), (395, FY))
    bills = bill_storm(px, py - 120, 70, t_boom, spread=(-470, 450), up=(-900, -300), g=1100, seed=11, floor=FY + 30, dur=2.8, stagger=.5)
    pile = G(money_pile(395, FY + 22, 240, seed=2), [[0, {'o': 0}], [t_boom + 2.2, {'o': 0}], [t_boom + 2.6, {'o': 1}]])
    # people: stand in a line at the left, then run in different directions
    tg = c.talk('GUY')
    def runner(x, y, s, steps, tx_end, ty_end, tstart, dur=1.4, who=None, **kw):
        fig = acting(who, x, y, s, steps, t_end=d) if who else steps
        keys = merge([[0, {'tx': 0, 'ty': 0}], [tstart, {'tx': 0, 'ty': 0}], [tstart + dur, {'tx': tx_end, 'ty': ty_end}, 'i']], bob(tstart, tstart + dur, 12, .26, 'ty'))
        return G(fig, keys, (x, y))
    t_run = t_press + .8
    guy = runner(120, FY + 30, 1.45, [(0, dict(pose='standing', expr='happy')), (t_press, dict(pose='shocked', expr='shocked')),
                                      (t_run, dict(pose='running', expr='shocked', walk=(t_run, d), talk=c.mouth('GUY')))], -330, 20, t_run, 1.6, who='GUY')
    friend = runner(230, FY + 10, 1.5, [(0, dict(pose='standing', expr='happy')), (t_press, dict(pose='shocked', expr='shocked')),
                                        (t_run + .1, dict(pose='running', expr='crying', walk=(t_run + .1, d)))], -500, 140, t_run + .1, 1.5, who='FRIEND')
    extras = ''
    for i, (x, y, s, suit, hat, tx, ty) in enumerate([(40, FY - 4, 1.2, 'maroon', 'top', -260, -50), (320, FY - 10, 1.2, 'navy', None, 380, 40),
                                                       (200, FY - 20, 1.1, 'green', 'fedora', -300, 90), (440, FY - 30, 1.1, 'black', 'top', 420, 60)]):
        st = t_run + .15 + i * .1
        fig = acting_extra_run(x, y, s, suit, hat, t_press, st, d)
        extras += runner(x, y, s, fig, tx, ty, st, 1.4)
    world = bg.flat('red') + printer + pile + extras + guy + friend + banker + bills
    cam = merge([[0, {'s': 1.0}]], jitter(t_boom, t_crash, 7, seed=3))
    over = headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']) + .3, 84, until=d) if False else \
        headline(sc['headline']['text'], t_boom + .6, 84)
    return world, cam, (W() / 2, FY - 150), over


def acting_extra_run(x, y, s, suit, hat, t_scream, t_run, d):
    a = cast.crowd_member(x, y, s, suit, hat, 'happy', 'hold')
    b = cast.crowd_member(x, y, s, suit, hat, 'shocked', 'up')
    r = cast.crowd_member(x, y, s, suit, hat, 'crying', 'up', walk=(t_run, d))
    return (G(a, [[0, {'o': 1}], [t_scream - .001, {'o': 1}], [t_scream, {'o': 0}, 'h']]) +
            G(b, [[0, {'o': 0}], [t_scream - .001, {'o': 0}], [t_scream, {'o': 1}, 'h'], [t_run - .001, {'o': 1}], [t_run, {'o': 0}, 'h']]) +
            G(r, [[0, {'o': 0}], [t_run - .001, {'o': 0}], [t_run, {'o': 1}, 'h']]))


# ------------------------------------------------------------------ S7
def s7(c):
    d = c.d; sc = c.sc
    black = sc['outro']['black_seconds']; d_world = d - black
    open_t = c.w('how') - .2
    vx, vy = 360, FY + 40
    v = props.vault(vx, vy, .92, open_t=open_t, open_d=max(1.2, d_world - open_t - .2))
    wheel_spin = G('', [])
    flash = G(burst(vx, vy - 160, 300, '#FFF3B0', 18), [[0, {'o': 0}], [d_world - 1.2, {'o': 0}], [d_world - 1.1, {'o': .9, 's': .2}], [d_world - .05, {'o': 1, 's': 5}, 'i']], (vx, vy - 160))
    banker = acting('BANKER', 92, FY, 1.5, [(0, dict(pose='talking', expr='smug', arms='present')), (open_t, dict(pose='shocked', expr='surprised'))], t_end=d)
    guy = acting('GUY', 575, FY, 1.45, [(0, dict(pose='pointing', expr='determined', flip=True)), (open_t, dict(pose='pointing', expr='surprised', flip=True))], t_end=d, flip=True)
    world = bg.flat('blue') + v + banker + guy + flash
    cam = [[0, {'s': 1.0}], [d_world, {'s': 1.12}, 'l']]
    over = headline(sc['headline']['text'], resolve_at(c.sh, sc['headline']['at']), 66, until=d_world)
    return world, cam, (vx, vy - 160), over


# ------------------------------------------------------------------ S8 end card
def icon_like(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s}) translate(-52 -52)"><path d="M8 46 H30 V94 H8 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M34 94 V48 L50 12 Q62 6 64 20 L58 40 H90 Q102 42 99 54 L92 84 Q90 94 78 94 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></g>')


def icon_share(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s}) translate(-52 -52)"><path d="M82 22 L26 52 L82 82" fill="none" stroke="{INK}" stroke-width="6"/>'
            + ''.join(f'<circle cx="{cx}" cy="{cy}" r="15" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>' for cx, cy in ((82, 22), (26, 52), (82, 82))) + '</g>')


def icon_bell(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 -26 C-20 -26 -27 -6 -27 12 L-34 26 H34 L27 12 C27 -6 20 -26 0 -26 Z" fill="#FFD54A" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
            f'<circle cy="34" r="7" fill="#FFD54A" stroke="{INK}" stroke-width="4"/><circle cy="-30" r="5" fill="#FFD54A" stroke="{INK}" stroke-width="3.5"/></g>')


def s8(c):
    d = c.d
    t_like, t_share, t_sub = c.w('like'), c.w('share'), c.w('subscribe')
    R1, R2, R3 = S(.255), S(.355), S(.46)
    gx, gy = 590, S(.745)
    row = lambda y, icon, label, t: G(icon(105, y, 1.25) + text(200, y + 2, label, 104, SCRIPT_B, '#FFFFFF', 'start', stroke=INK, sw=14), pop(t - .05, .34, .4), (105, y))
    like = G(row(R1, icon_like, 'LIKE', t_like), hop(t_like + .15, 24, .3, 2), (105, R1))
    share = G(row(R2, icon_share, 'SHARE', t_share), wiggle(t_share + .1, t_share + .9, 8, .3), (105, R2))
    pill = (f'<rect x="60" y="{R3 - 50}" width="430" height="100" rx="50" fill="#E0382C" stroke="{INK}" stroke-width="6"/>'
            + text(275, R3 + 2, 'SUBSCRIBE', 66, SCRIPT_B, '#FFFFFF'))
    sub = G(pill, merge(pop(t_sub - .05, .34, .4), [[t_sub + .4, {'s': 1.0}], [t_sub + .6, {'s': 1.06}, 'io'], [t_sub + .8, {'s': 1.0}, 'io'], [t_sub + 1.0, {'s': 1.06}, 'io'], [t_sub + 1.2, {'s': 1.0}, 'io']]), (275, R3))
    bell = G(G(icon_bell(560, R3, 1.25), wiggle(t_sub + .25, t_sub + 1.6, 18, .26), (560, R3 - 24)), pop(t_sub + .1, .3, .4), (560, R3))
    title = G(caps(W() / 2, S(.172), 'ENJOYED THIS?', 78, INK, rot=-2), slam(.05), (W() / 2, S(.172)))
    steps = []
    t = 0.0; k = 0
    while t < d:
        steps.append((round(t, 2), dict(pose='talking' if k % 2 == 0 else 'standing', arms='wave' if k % 2 == 0 else 'down', expr='grin', talk=c.mouth('GUY')))); t += .32; k += 1
    guy = acting('GUY', gx, gy, 1.1, steps, t_end=d)
    more = G(caps(60, S(.565), 'FOR MORE MONEY', 46, '#5A1A12', 'start') + caps(60, S(.605), 'EXPLAINED', 46, '#5A1A12', 'start')
             + caps(60, S(.665), 'NEXT: HOW DO BANKS', 36, INK, 'start') + caps(60, S(.698), 'CREATE MONEY?', 36, INK, 'start'), fade(t_sub + .6, .3))
    world = bg.flat('mustard', floor=False) + burst(gx, gy - 135, 175, '#F2BE2E', 16) + title + like + share + sub + bell + guy + more
    return world, [[0, {'s': 1.0}], [d, {'s': 1.03}, 'l']], (W() / 2, S(.4)), ''


BUILDERS = {'S1': s1, 'S2': s2, 'S3': s3, 'S4': s4, 'S5': s5, 'S6': s6, 'S7': s7, 'S8': s8}
