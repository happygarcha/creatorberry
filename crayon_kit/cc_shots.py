"""Shot templates: one call = one finished shot, framed for 16:9 or 9:16 (whatever animlib.set_format chose).
Each takes `sh` = the shot's entry from timeline.json ({start, end, lines:[{t0, t1, words}]}) so text and mouth
flaps land on the voice. Anything a template can't do: build the shot by hand with cc_kit + scene()."""
from animlib import *
from cc_kit import *


def V(): return W() < H()
def span(sh): return sh['start'], sh['end'], sh['end'] - sh['start']
def line(sh, i=0): return sh['lines'][i] if sh.get('lines') else {'t0': 0, 't1': sh['end'] - sh['start'], 'words': []}
CUES = []   # (sfx name, GLOBAL time, gain) collected by the templates; mix them in the sound step


def cue(name, t, gain=1.0): CUES.append([name, round(t, 3), gain])


def wt(sh, word):
    """Local time of the first word starting with `word` (any line of the shot), for syncing a reveal to the VO."""
    for ln in sh.get('lines', []):
        for w, t0, t1 in ln['words']:
            if w.lower().strip('.,!?:;"\'$').startswith(word.lower()): return t0
    return line(sh)['t0']
def head_y(feet, s): return feet - 196 * s          # head centre of a person() at scale s
def feet_for(head, s): return head + 196 * s         # feet y that puts the head centre at `head`


def t_card(sh, text_, title=False, z=1):
    """Black card. title=True: chapter title, hard cut, no typing. Otherwise the narration line types on with the voice."""
    st, en, d = span(sh)
    if title: return scene(st, en, chapter(text_), z=z)
    ln = line(sh)
    size = 44 if not V() else 54
    return scene(st, en, card(text_, size, kf=typewrite(ln['t0'], max(ln['t0'] + .3, ln['t1'] - .1))), z=z)


def t_spot(sh, who, s=None, label=None):
    """Character introduction: dark stage, light cone, the character fades up; optional typed name label + arrow."""
    st, en, d = span(sh)
    s = s or (1.5 if not V() else 1.9)
    cx, fy = W() / 2, H() * (.8 if not V() else .66)
    o = stage(cx, fy) + G(person(cx, fy, s, **who), fade(0, .35))
    cue('boom', st, .45)
    if label:
        lx, ly = (cx + 300, H() * .28) if not V() else (cx, H() * .18)
        o += label_arrow(lx, ly, label, (cx + 60, head_y(fy, s) - 20), 38 if not V() else 46, kf=type_cps(.4, label, 18))
    return scene(st, en, frame_svg(o, 'spotlight intro'), cam=push(d, 1.06))


def t_place(sh, setting, caption=None, reveal=True):
    """Establishing shot: pull-out reveal from 1.45x + typed place/date caption ('Pune, 2014.')."""
    st, en, d = span(sh)
    o = setting + (place_caption(caption, 40 if not V() else 52, kf=type_cps(.3, caption, 16)) if caption else '')
    return scene(st, en, frame_svg(o, caption or 'establishing'), cam=pull(d, 1.45, dur=min(2.6, d)) if reveal else push(d, 1.05))


def office(wall=CREAM_WALL, night=False, seed=2):
    """The default interior: wall, wood panelling, window (city), bookshelf, curtain."""
    if not V():
        return (room(wall, WOOD, H() * .76, wainscot=H() * .52) + bookshelf(30, 90, 190, 330, seed) +
                window(W() * .56, 60, 300, 220, 'night' if night else 'city') + curtain(W() - 190, 30, 160, 470))
    return (room(wall, WOOD, H() * .7, wainscot=H() * .46) + window(60, 110, 300, 250, 'night' if night else 'city') +
            bookshelf(W() - 220, 120, 190, 420, seed))


def t_desk(sh, who, bg=None, text_=None, voiced=True, plaque_txt=None, props='', s=None):
    """Medium shot of one character behind a desk (the workhorse of business stories)."""
    st, en, d = span(sh)
    bg = bg if bg is not None else office()
    s = s or (1.55 if not V() else 2.0)
    cx = W() / 2 if V() else W() * .42
    hy = H() * (.42 if not V() else .44)
    fy = feet_for(hy, s)
    dy = hy + 150 * s / 1.55
    ln = line(sh)
    o = [bg, chair_back(cx, dy + 10, w=150 * s, h=dy + 10 - (hy + 6 * s)),
         person(cx, fy, s, talk=(ln['t0'], ln['t1']) if (text_ and voiced) else None, **who),
         desk(cx, dy, (600 if not V() else 640), 400), papers(cx - 210, dy + 14, 6, 110), papers(cx + 210, dy + 14, 5, 110), props]
    if plaque_txt: o.append(plaque(cx, dy + 14, plaque_txt, size=22 if not V() else 28))
    if text_: o.append(_line(sh, text_, voiced, (cx, hy), s))
    return scene(st, en, frame_svg(''.join(o), 'desk shot'), cam=push(d, 1.05), cam_o=(cx, hy))


def _line(sh, text_, voiced, head, s, side=1):
    """Voiced -> white text + tick near the head, appears when the line starts. Unvoiced -> bubble pops on the line start."""
    ln = line(sh)
    hx, hy = head
    big = 40 if not V() else 52
    if voiced:
        if V(): x, y = W() / 2, hy - 44 * s - 150
        else: x, y = hx + side * (60 * s + tw(text_, big) / 2), hy - 44 * s - 30
        return say(x, max(60, y), text_, big, to=(hx + side * 30 * s, hy - 40 * s), kf=appear(ln['t0']))
    x = W() / 2 if V() else hx + side * (40 * s + tw(text_, 34) / 2)
    y = max(70, hy - 44 * s - (130 if V() else 90))
    cue('pop', sh['start'] + max(0, ln['t0'] - .05), .6)
    return bubble(x, y, text_, tail=(hx + side * 10 * s, hy - 48 * s), size=36 if not V() else 46, kf=pop(max(0, ln['t0'] - .05)))


def t_two(sh, a, b, speaker='a', text_=None, voiced=True, bg=None, sa=None, sb=None):
    """Two-shot: a (left) and b (right) facing each other; one of them says/bubbles the line."""
    st, en, d = span(sh)
    bg = bg if bg is not None else office()
    sa, sb = sa or (1.5 if not V() else 1.7), sb or (1.5 if not V() else 1.7)
    gy = H() * (.9 if not V() else .8)                      # both stand on the same floor line
    ha, hb = gy - 196 * sa, gy - 196 * sb
    xa, xb = (W() * .3, W() * .7) if not V() else (W() * .28, W() * .74)
    ln = line(sh)
    ta = dict(a); tb = dict(b)
    if text_ and voiced: (ta if speaker == 'a' else tb)['talk'] = (ln['t0'], ln['t1'])
    ta.setdefault('look', 5); tb.setdefault('look', -5)
    o = [bg, person(xa, feet_for(ha, sa), sa, **ta), person(xb, feet_for(hb, sb), sb, **tb)]
    if text_:
        hx, hy, s, side = (xa, ha, sa, 1) if speaker == 'a' else (xb, hb, sb, -1)
        o.append(_line(sh, text_, voiced, (hx, hy), s, side))
    return scene(st, en, frame_svg(''.join(o), 'two-shot'), cam=pan(d, 40 if not V() else 24, s=1.06))


def t_close(sh, who, text_=None, voiced=True, bg=None, s=None, side=1):
    """Close-up on a face (reactions, the key line). Mouth flaps while a voiced line plays."""
    st, en, d = span(sh)
    s = s or (2.4 if not V() else 3.0)
    hx, hy = (W() * .4, H() * .55) if not V() else (W() / 2, H() * .52)
    ln = line(sh)
    w = dict(who)
    if text_ and voiced: w['talk'] = (ln['t0'], ln['t1'])
    o = [bg if bg is not None else office(), person(hx, feet_for(hy, s), s, **w)]
    if text_: o.append(_line(sh, text_, voiced, (hx, hy), s, side))
    return scene(st, en, frame_svg(''.join(o), 'close-up'), cam=push(d, 1.06), cam_o=(hx, hy))


def t_ots(sh, front, back, text_=None, voiced=True, bg=None):
    """Over-the-shoulder: `back` (seen from behind) big in the near corner, `front` speaking to them."""
    st, en, d = span(sh)
    sf_, hy = (1.9 if not V() else 2.5), H() * (.42 if not V() else .46)
    fx = W() * .62 if not V() else W() * .58
    ln = line(sh)
    f = dict(front)
    if text_ and voiced: f['talk'] = (ln['t0'], ln['t1'])
    o = [bg if bg is not None else office(), person(fx, feet_for(hy, sf_), sf_, **f),
         person(W() * .14 if not V() else W() * .06, H() * (1.45 if not V() else 1.42), 2.4 if not V() else 3.0, back=True, **back)]
    if text_: o.append(_line(sh, text_, voiced, (fx, hy), sf_, 1 if not V() else -1))
    return scene(st, en, frame_svg(''.join(o), 'over the shoulder'), cam=push(d, 1.05))


def t_compare(sh, left, right, label=None, w_left=None, w_right=None, label_col=RED):
    """Infographic: [left box] -> [right box] + caps label on the blue-grey backdrop. Each pops on its word.
    left/right = (text, fill, word_to_sync)."""
    st, en, d = span(sh)
    cx, cy = W() / 2, H() / 2
    (lt, lf, lw), (rt, rf, rw) = left, right
    t1, t2 = wt(sh, lw), wt(sh, rw)
    cue('pop', st + t1, .6); cue('ding', st + t2, .6)
    if not V(): a, b = (cx - 300, cy - 30), (cx + 240, cy - 30)
    else: a, b = (cx, cy - 260), (cx, cy + 120)
    arr = arrow(a[0] + 110, a[1], b[0] - 170, b[1], RED, 40) if not V() else arrow(a[0], a[1] + 80, b[0], b[1] - 80, RED, 40)
    o = [info_bg(), G(price_box(*a, lt, fill=lf, size=56), pop(t1), a), G(arr, wipe(t2 - .25, .35)), G(price_box(*b, rt, fill=rf, size=56), pop(t2), b)]
    if label: o.append(G(caps(cx, cy + (120 if not V() else 300), label, 64, label_col), pop(t2 + .45), (cx, cy + 120)))
    return scene(st, en, frame_svg(''.join(o), 'comparison'), cam=push(d, 1.05))


def t_stat(sh, big, small='', bg=None, word=None, col=GREEN):
    """Big number on a white card over a scene (or the blue-grey backdrop): '$22 BILLION / COMBINED VALUE'."""
    st, en, d = span(sh)
    t = wt(sh, word) if word else .2
    cue('ding', st + t, .6)
    o = (bg if bg is not None else info_bg()) + G(stat_card(W() / 2, H() * (.62 if not V() else .55), big, small, col, size=72 if not V() else 64), pop(t), (W() / 2, H() * .6))
    return scene(st, en, frame_svg(o, big), cam=push(d, 1.04))


def t_news(sh, headline, sub='', word=None, photo=''):
    """Newspaper close-up; the sub-line gets a marker swipe on `word`."""
    st, en, d = span(sh)
    cx, cy = W() / 2, H() / 2
    nw, nh = (min(900, W() - 60), 560) if not V() else (W() - 120, 760)
    ws = headline.split()
    hl = headline if not V() or len(headline) < 16 else ' '.join(ws[:(len(ws) + 1) // 2]) + '\n' + ' '.join(ws[(len(ws) + 1) // 2:])
    sy = cy - nh / 2 + 140 + 48 * hl.count('\n')
    o = [fill_bg('#4A3324'), newspaper(cx, cy, nw, nh, hl, sub, photo, rot=-2)]
    cue('paper', st, .8)
    if sub: o.append(G(f'<g transform="rotate(-2 {cx} {cy})"><rect x="{cx - tw(sub, 22) / 2 - 14}" y="{sy - 17}" width="{tw(sub, 22) + 28}" height="34" fill="#6FA8E0" opacity=".55"/></g>',
                       wipe((wt(sh, word) if word else .4) - .3, .5)))
    return scene(st, en, frame_svg(''.join(o), headline), cam=push(d, 1.12), cam_o=(cx, sy))


def t_panels(sh, roles, wall='#DCD2BE', phone=True):
    """Row (16:9) or 2x2 grid (9:16) of panels sliding in one per beat; roles = [(plaque, person_kwargs)].
    Classic 'everyone is calling' / 'every department said no' beat."""
    st, en, d = span(sh)
    n = len(roles)
    o = [fill_bg('#000')]
    for i, (lab, kw) in enumerate(roles):
        if not V(): x0, y0, pw, ph = i * W() / n, 0, W() / n, H()
        else: x0, y0, pw, ph = (i % 2) * W() / 2, (i // 2) * H() / 2, W() / 2, H() / 2
        ps = 2.0 if not V() else 1.6
        k = dict(kw); k.setdefault('arms', 'phone' if phone else 'down'); k.setdefault('skin', 'white')
        inner = (person(x0 + pw / 2, y0 + ph * .42 + 196 * ps, ps, **k)
                 + f'<rect x="{x0}" y="{y0 + ph * .8}" width="{pw}" height="{ph * .2 + 2}" fill="{WOOD}" stroke="{INK}" stroke-width="3"/>'
                 + (phone_old(x0 + pw * .2, y0 + ph * .84, .7) if phone else '') + plaque(x0 + pw * .6, y0 + ph * .84 + 6, lab, size=22))
        t = -.05 + i * min(.6, d / (n + 1))
        keys = ([[0, {'tx': 60 if not V() else 0, 'ty': 0 if not V() else 40, 'o': 0}]] if i else []) + \
               [[t, {'tx': 60 if not V() else 0, 'ty': 0 if not V() else 40, 'o': 0}], [t + .03, {'o': 1}], [t + .3, {'tx': 0, 'ty': 0}, 'o']]
        o.append(G(panel(x0, y0, pw, ph, inner, wall), keys)); cue('whoosh', st + max(0, t), .35)
    if phone: cue('phone', st + .2, .4)
    return scene(st, en, frame_svg(''.join(o), 'panels'))


def t_logo(sh, name, icon='spark', sub=None, montage=None):
    """'This is <Company>.' Wordmark over sunburst rays; montage=[svg, ...] strobes backgrounds every 0.12 s first."""
    st, en, d = span(sh)
    cx, cy = W() / 2, H() / 2
    if montage:
        lay = []
        for i, b in enumerate(montage):
            keys, t, k = [[-.01, {'o': 1 if i == 0 else 0}]], 0.0, 0
            while t < d - .9:
                keys.append([round(t, 3), {'o': 1 if k % len(montage) == i else 0}, 'h']); t += .12; k += 1
            keys.append([round(t, 3), {'o': 1 if i == 0 else 0}, 'h'])
            lay.append(G(b, keys))
        bg = ''.join(lay) + f'<rect width="{W()}" height="{H()}" fill="#000" opacity=".25"/>'
        cue('whoosh', st, .5)
    else:
        bg = rays_bg()
    return scene(st, en, frame_svg(bg + wordmark(cx, cy, name, icon, '#FFFFFF', 84 if not V() else 64, sub), name), cam=push(d, 1.05))
