"""Crayon-style story cartoon kit: thick black outlines, flat cel-shaded fills, round-head bean-body cast,
grey crowds, handwritten dialogue. All drawing is SVG in the logical canvas (1280x720 or 720x1280; see animlib.set_format).
Every function returns an SVG string. (x, y) for characters/props = the point on the ground between the feet / base."""
import math, random, html as _html
import animlib

# ------------------------------------------------------------------ palette
INK = '#161616'                      # every outline
LW = 4.2                             # character outline
LW2 = 3.2                            # props / architecture
LW3 = 2.2                            # inner detail lines
SKIN = {'peach': ('#F3CDA1', '#DDAE80'), 'tan': ('#E2B184', '#C8956A'), 'brown': ('#B9805A', '#9C6744'),
        'deep': ('#7E5238', '#683F29'), 'white': ('#FFFFFF', '#D8D8D8'), 'grey': ('#9A9A9A', '#7E7E7E')}
SUIT = {'black': ('#2B2C30', '#1D1E21'), 'navy': ('#2F3D5C', '#232E47'), 'brown': ('#6E4C36', '#573A28'),
        'grey': ('#8E9196', '#74777C'), 'maroon': ('#7C2F35', '#622328'), 'olive': ('#5E6440', '#4A4F31'),
        'cream': ('#EDE6D6', '#D3CAB6'), 'blue': ('#4D6FA3', '#3C5986'), 'teal': ('#3E7C7A', '#2F6260'),
        'green': ('#5C8A4E', '#4A7140'), 'orange': ('#D9772E', '#B95F20'), 'pink': ('#C66B86', '#A85570'),
        'hoodie': ('#3A3D44', '#2A2D33'), 'labcoat': ('#F4F4F2', '#D9D9D4')}
HAIR = {'black': '#222224', 'dark': '#3A2C24', 'brown': '#6E4A30', 'auburn': '#8A3F2A', 'blonde': '#D9B062', 'grey': '#BDBDBD', 'white': '#EDEDED'}
RED, GREEN, GOLD, BLUE = '#C0392F', '#3F9A50', '#D8A43A', '#3E6FA8'
CREAM_WALL, WOOD, WOOD_D, PANEL = '#F5E2B3', '#6B452E', '#4E3121', '#5E3C29'
INFO_BG, INFO_BLOB = '#8DA1B1', '#A9BAC6'
SCRIPT = "font-family:'Caveat',cursive;font-weight:600"      # dialogue, bubbles, cards, captions
SCRIPT_B = "font-family:'Caveat Brush','Caveat',cursive"     # end card / big words
CAPS = "font-family:'Patrick Hand SC',cursive"               # signs, plaques, labels, numbers
FONT_SPECS = [('Caveat', 'caveat', 400, 'normal'), ('Caveat', 'caveat', 600, 'normal'), ('Caveat', 'caveat', 700, 'normal'),
              ('Caveat Brush', 'caveat-brush', 400, 'normal'), ('Patrick Hand SC', 'patrick-hand-sc', 400, 'normal')]
_uid = [0]


def uid(p='u'):
    _uid[0] += 1
    return f'{p}{_uid[0]}'


def esc(t): return _html.escape(str(t), quote=False)
def W(): return animlib.FW
def H(): return animlib.FH


def g(x, y, s, inner, flip=False, rot=0):
    return f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot}) scale({-s if flip else s} {s})">{inner}</g>'


def fonts_head(root):
    return animlib.local_fonts(root, FONT_SPECS)


def frame_svg(inner, label=''):
    """Full-frame SVG for one shot (no grain, no vignette: the look is clean flat vector)."""
    return (f'<svg width="{W()}" height="{H()}" viewBox="0 0 {W()} {H()}" role="img" aria-label="{esc(label)}" '
            f'style="position:absolute;left:0;top:0;width:{W()}px;height:{H()}px">{inner}</svg>')


# ------------------------------------------------------------------ text primitives
def text(x, y, t, size, fam=SCRIPT, fill=INK, anchor='middle', stroke=None, sw=0, rot=0, skew=0, extra='', lh=1.08, kf=None):
    """Multi-line text ('\n'). stroke draws an outline behind the fill (paint-order)."""
    lines = str(t).split('\n')
    st = f'{fam};font-size:{size}px;fill:{fill}' + (f';stroke:{stroke};stroke-width:{sw}px;paint-order:stroke;stroke-linejoin:round' if stroke else '') + extra
    tf = (f' transform="translate({x} {y}) rotate({rot}) skewX({skew}) translate({-x} {-y})"') if (rot or skew) else ''
    y0 = y - (len(lines) - 1) * size * lh / 2
    spans = ''.join(f'<tspan x="{x}" y="{y0 + i * size * lh:.1f}">{esc(l)}</tspan>' for i, l in enumerate(lines))
    k = f" data-kf='{animlib.J(kf)}'" if kf else ''
    return f'<text text-anchor="{anchor}" dominant-baseline="middle" style="{st}"{tf}{k}>{spans}</text>'


def wtext(x, y, t, size, anchor='middle', kf=None, fam=None):
    """White handwriting with a thin dark outline and a soft offset shadow (dialogue, captions, labels)."""
    fam = fam or SCRIPT
    sh = text(x + size * .05, y + size * .07, t, size, fam, '#000000', anchor, stroke='#000000', sw=size * .1, extra=';opacity:.45', kf=kf)
    return sh + text(x, y, t, size, fam, '#FFFFFF', anchor, stroke='#151515', sw=size * .085, kf=kf)


def tw(t, size, fam='script'):
    """Rough text width (px) for layout of bubbles and tags."""
    k = .40 if fam == 'script' else .52
    return max(len(l) for l in str(t).split('\n')) * size * k


def caps(x, y, t, size, fill=INK, anchor='middle', rot=0, **kw):
    return text(x, y, t, size, CAPS, fill, anchor, rot=rot, skew=-7, **kw)


# ------------------------------------------------------------------ characters
def _shade_clip(shape, shade_shape, base, shade):
    cid = uid('c')
    return (f'<clipPath id="{cid}">{shape}</clipPath>{shape.replace("/>", f" fill=\"{base}\"/>", 1)}'
            f'<g clip-path="url(#{cid})">{shade_shape.replace("/>", f" fill=\"{shade}\"/>", 1)}</g>'
            f'{shape.replace("/>", f" fill=\"none\" stroke=\"{INK}\" stroke-width=\"{LW}\"/>", 1)}')


BODY = 'M-27 -150 Q0 -157 27 -150 Q45 -141 44 -102 Q43 -62 30 -56 Q0 -50 -30 -56 Q-43 -62 -44 -102 Q-45 -141 -27 -150 Z'
HEAD_C, HEAD_R = -196, 44


def _arms(pose, fill):
    """Thin black arms; pose name or ((hx,hy),(hx,hy)) hand points relative to the feet."""
    P = {'down': ((-54, -76), (54, -76)), 'hips': ((-58, -98), (58, -98)), 'point_r': ((-44, -80), (104, -142)),
         'point_l': ((-104, -142), (44, -80)), 'up': ((-62, -232), (62, -232)), 'wave': ((-44, -80), (70, -228)),
         'hold': ((-22, -104), (22, -104)), 'shrug': ((-74, -150), (74, -150)), 'phone': ((-54, -76), (34, -136)),
         'chin': ((-44, -80), (14, -166)), 'present': ((-44, -80), (96, -112)), 'cross': ((22, -110), (-22, -106))}
    hands = P.get(pose, pose) if isinstance(pose, str) else pose
    o = []
    for (hx, hy), sx in zip(hands, (-34, 34)):
        mx, my = (sx + hx) / 2 + (-10 if sx < 0 else 10), (-136 + hy) / 2 + 8
        o.append(f'<path d="M{sx} -136 Q{mx:.0f} {my:.0f} {hx} {hy}" fill="none" stroke="{INK}" stroke-width="{LW - .6}" stroke-linecap="round"/>')
    return ''.join(o)


def _legs(stance):
    if stance == 'walk':
        return (f'<path d="M-8 -60 L14 0 M8 -60 L-14 0" stroke="{INK}" stroke-width="{LW - .4}" stroke-linecap="round"/>')
    if stance == 'sit':
        return (f'<path d="M-12 -60 L-12 -40 L-30 -40 M12 -60 L12 -40 L-6 -40" fill="none" stroke="{INK}" stroke-width="{LW - .4}" stroke-linecap="round"/>')
    if stance == 'none':
        return ''
    return f'<path d="M-11 -60 L-12 0 M11 -60 L12 0" stroke="{INK}" stroke-width="{LW - .4}" stroke-linecap="round"/>'


def _hair(style, col, face):
    cy, r = HEAD_C, HEAD_R
    s = f'fill="{col}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"'
    if style == 'side':      # neat side part / short
        return (f'<path d="M-45 {cy + 6} C-50 {cy - 40} -26 {cy - 58} 2 {cy - 56} C30 {cy - 56} 50 {cy - 38} 45 {cy + 4} '
                f'C40 {cy - 18} 30 {cy - 26} 14 {cy - 28} C2 {cy - 18} -20 {cy - 22} -34 {cy - 26} C-40 {cy - 18} -42 {cy - 6} -45 {cy + 6} Z" {s}/>')
    if style == 'swoop':     # fringe swept to one side (young / modern)
        return (f'<path d="M-46 {cy + 8} C-52 {cy - 44} -10 {cy - 64} 22 {cy - 52} C44 {cy - 44} 52 {cy - 20} 45 {cy + 6} '
                f'C38 {cy - 14} 24 {cy - 18} 18 {cy - 34} C4 {cy - 12} -24 {cy - 10} -40 {cy - 14} Z" {s}/>')
    if style == 'curly':
        bumps = ''.join(f'<circle cx="{r * .92 * math.cos(a):.1f}" cy="{cy - 6 + r * .9 * math.sin(a):.1f}" r="15" {s}/>'
                        for a in [math.pi * (1.0 + i / 8) for i in range(9)])
        return bumps + f'<path d="M-42 {cy - 4} C-36 {cy - 40} 36 {cy - 40} 42 {cy - 4} C24 {cy - 20} -24 {cy - 20} -42 {cy - 4} Z" fill="{col}"/>'
    if style == 'bald':      # bald top, tufts on the sides (older men)
        return (f'<path d="M-46 {cy + 10} C-52 {cy - 6} -48 {cy - 24} -38 {cy - 30} C-40 {cy - 14} -40 {cy - 2} -34 {cy + 12} Z" {s}/>'
                f'<path d="M46 {cy + 10} C52 {cy - 6} 48 {cy - 24} 38 {cy - 30} C40 {cy - 14} 40 {cy - 2} 34 {cy + 12} Z" {s}/>')
    if style == 'long':
        return (f'<path d="M-48 {cy + 44} C-56 {cy - 30} -30 {cy - 60} 0 {cy - 58} C30 {cy - 60} 56 {cy - 30} 48 {cy + 44} '
                f'L34 {cy + 44} C38 {cy + 10} 36 {cy - 14} 28 {cy - 26} C10 {cy - 20} -16 {cy - 24} -30 {cy - 20} C-38 {cy - 6} -38 {cy + 14} -34 {cy + 44} Z" {s}/>')
    if style == 'bun':
        return (f'<circle cx="0" cy="{cy - 54}" r="17" {s}/>' + _hair('side', col, face))
    if style == 'spiky':
        return (f'<path d="M-45 {cy + 2} L-50 {cy - 30} L-34 {cy - 34} L-30 {cy - 58} L-12 {cy - 44} L0 {cy - 66} L12 {cy - 46} L30 {cy - 60} '
                f'L32 {cy - 36} L50 {cy - 30} L45 {cy + 2} C30 {cy - 22} -30 {cy - 22} -45 {cy + 2} Z" {s}/>')
    if style == 'buzz':
        return f'<path d="M-44 {cy - 4} C-42 {cy - 50} 42 {cy - 50} 44 {cy - 4} C28 {cy - 24} -28 {cy - 24} -44 {cy - 4} Z" {s}/>'
    return ''


def _hat(kind, col):
    cy = HEAD_C
    s = f'stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"'
    if kind == 'top':
        return (f'<rect x="-30" y="{cy - 112}" width="60" height="78" rx="5" fill="{col}" {s}/>'
                f'<rect x="-30" y="{cy - 50}" width="60" height="12" fill="{SUIT["black"][1]}" opacity=".8"/>'
                f'<ellipse cx="0" cy="{cy - 34}" rx="54" ry="11" fill="{col}" {s}/>')
    if kind == 'fedora':
        return (f'<path d="M-34 {cy - 34} C-36 {cy - 70} -20 {cy - 76} 0 {cy - 66} C20 {cy - 76} 36 {cy - 70} 34 {cy - 34} Z" fill="{col}" {s}/>'
                f'<rect x="-34" y="{cy - 46}" width="68" height="10" fill="{INK}" opacity=".55"/>'
                f'<ellipse cx="0" cy="{cy - 34}" rx="60" ry="12" fill="{col}" {s}/>')
    if kind == 'bowler':
        return (f'<path d="M-36 {cy - 32} C-36 {cy - 84} 36 {cy - 84} 36 {cy - 32} Z" fill="{col}" {s}/>'
                f'<ellipse cx="0" cy="{cy - 32}" rx="52" ry="10" fill="{col}" {s}/>')
    if kind == 'hard':
        return (f'<path d="M-42 {cy - 22} C-42 {cy - 76} 42 {cy - 76} 42 {cy - 22} Z" fill="{col}" {s}/>'
                f'<rect x="-52" y="{cy - 26}" width="104" height="10" rx="5" fill="{col}" {s}/>')
    if kind == 'grad':
        return (f'<rect x="-30" y="{cy - 50}" width="60" height="18" fill="{col}" {s}/>'
                f'<path d="M-64 {cy - 52} L0 {cy - 74} L64 {cy - 52} L0 {cy - 34} Z" fill="{col}" {s}/>'
                f'<path d="M30 {cy - 50} L42 {cy - 20}" stroke="{GOLD}" stroke-width="4"/>')
    if kind == 'cap':
        return (f'<path d="M-44 {cy - 18} C-46 {cy - 70} 44 {cy - 70} 44 {cy - 18} Z" fill="{col}" {s}/>'
                f'<path d="M30 {cy - 22} L76 {cy - 16} L44 {cy - 8} Z" fill="{col}" {s}/>')
    return ''


def face(expr='neutral', look=0, eye_y=HEAD_C - 2, mouth_open=False, nose=None, glasses=False, moustache=None, beard=None, skin=None):
    """Dot eyes, short brows only for emotion, one-stroke mouth. look = eye offset in px (-6..6)."""
    o, ey, lx, rx = [], eye_y, -14 + look, 14 + look
    ln = f'stroke="{INK}" stroke-width="3.2" stroke-linecap="round" fill="none"'
    if expr in ('closed', 'smug_closed'):
        o.append(f'<path d="M{lx - 6} {ey} Q{lx} {ey + 4} {lx + 6} {ey} M{rx - 6} {ey} Q{rx} {ey + 4} {rx + 6} {ey}" {ln}/>')
    elif expr == 'shocked':
        o.append(f'<ellipse cx="{lx}" cy="{ey}" rx="5.5" ry="7.5" fill="{INK}"/><ellipse cx="{rx}" cy="{ey}" rx="5.5" ry="7.5" fill="{INK}"/>')
    elif expr == 'crying':
        o.append(f'<path d="M{lx - 7} {ey + 2} L{lx + 6} {ey - 2} M{rx + 7} {ey + 2} L{rx - 6} {ey - 2}" {ln}/>')
    else:
        o.append(f'<ellipse cx="{lx}" cy="{ey}" rx="3.8" ry="5.4" fill="{INK}"/><ellipse cx="{rx}" cy="{ey}" rx="3.8" ry="5.4" fill="{INK}"/>')
    brow = {'angry': f'M{lx - 9} {ey - 15} L{lx + 6} {ey - 9} M{rx + 9} {ey - 15} L{rx - 6} {ey - 9}',
            'worried': f'M{lx - 8} {ey - 9} L{lx + 6} {ey - 15} M{rx + 8} {ey - 9} L{rx - 6} {ey - 15}',
            'sad': f'M{lx - 8} {ey - 9} L{lx + 6} {ey - 14} M{rx + 8} {ey - 9} L{rx - 6} {ey - 14}',
            'surprised': f'M{lx - 7} {ey - 16} Q{lx} {ey - 20} {lx + 7} {ey - 16} M{rx - 7} {ey - 16} Q{rx} {ey - 20} {rx + 7} {ey - 16}',
            'shocked': f'M{lx - 8} {ey - 19} Q{lx} {ey - 24} {lx + 8} {ey - 19} M{rx - 8} {ey - 19} Q{rx} {ey - 24} {rx + 8} {ey - 19}',
            'smug': f'M{lx - 8} {ey - 11} L{lx + 6} {ey - 11} M{rx - 6} {ey - 16} L{rx + 8} {ey - 12}',
            'determined': f'M{lx - 9} {ey - 13} L{lx + 6} {ey - 10} M{rx + 9} {ey - 13} L{rx - 6} {ey - 10}',
            'crying': f'M{lx - 8} {ey - 10} L{lx + 6} {ey - 15} M{rx + 8} {ey - 10} L{rx - 6} {ey - 15}'}.get(expr)
    if brow: o.append(f'<path d="{brow}" {ln}/>')
    my, mx = HEAD_C + 22, look * .6
    if nose == 'big':
        o.append(f'<ellipse cx="{mx}" cy="{HEAD_C + 8}" rx="11" ry="9" fill="#9C5866" stroke="{INK}" stroke-width="2.6"/>')
        my += 6
    elif nose == 'small':
        o.append(f'<path d="M{mx - 2} {HEAD_C + 4} Q{mx + 5} {HEAD_C + 10} {mx - 2} {HEAD_C + 13}" {ln}/>')
    if mouth_open or expr in ('surprised', 'talk'):
        o.append(f'<ellipse cx="{mx}" cy="{my + 1}" rx="5.5" ry="6.5" fill="{INK}"/>')
    elif expr == 'shocked':
        o.append(f'<ellipse cx="{mx}" cy="{my + 4}" rx="9" ry="12" fill="{INK}"/>')
    elif expr == 'crying':
        o.append(f'<path d="M{mx - 14} {my + 6} Q{mx} {my - 10} {mx + 14} {my + 6} Q{mx} {my + 14} {mx - 14} {my + 6} Z" fill="{INK}"/>'
                 f'<path d="M{lx} {ey + 6} L{lx - 3} {ey + 40} M{rx} {ey + 6} L{rx + 3} {ey + 40}" stroke="#8FD0F0" stroke-width="5" stroke-linecap="round"/>')
    elif expr in ('happy', 'grin'):
        o.append(f'<path d="M{mx - 12} {my - 3} Q{mx} {my + 13} {mx + 12} {my - 3} Z" fill="{INK}"/>' if expr == 'grin'
                 else f'<path d="M{mx - 10} {my - 2} Q{mx} {my + 9} {mx + 10} {my - 2}" {ln}/>')
    elif expr in ('sad', 'worried', 'angry'):
        o.append(f'<path d="M{mx - 8} {my + 4} Q{mx} {my - 3} {mx + 8} {my + 4}" {ln}/>')
    elif expr in ('smug', 'smug_closed'):
        o.append(f'<path d="M{mx - 8} {my + 1} Q{mx + 3} {my + 5} {mx + 10} {my - 4}" {ln}/>')
    else:
        o.append(f'<path d="M{mx - 6} {my + 1} L{mx + 6} {my + 1}" {ln}/>')
    if moustache:
        o.append(f'<path d="M{mx} {my - 6} C{mx - 6} {my - 12} {mx - 22} {my - 10} {mx - 24} {my + 2} C{mx - 14} {my - 2} {mx - 6} {my - 1} {mx} {my - 4} '
                 f'C{mx + 6} {my - 1} {mx + 14} {my - 2} {mx + 24} {my + 2} C{mx + 22} {my - 10} {mx + 6} {my - 12} {mx} {my - 6} Z" fill="{moustache}" stroke="{INK}" stroke-width="2.4"/>')
    if beard:
        o.append(f'<path d="M-42 {HEAD_C + 4} C-40 {HEAD_C + 40} -18 {HEAD_C + 50} 0 {HEAD_C + 50} C18 {HEAD_C + 50} 40 {HEAD_C + 40} 42 {HEAD_C + 4} '
                 f'C34 {HEAD_C + 18} 22 {HEAD_C + 14} 14 {HEAD_C + 22} C6 {HEAD_C + 16} -6 {HEAD_C + 16} -14 {HEAD_C + 22} C-22 {HEAD_C + 14} -34 {HEAD_C + 18} -42 {HEAD_C + 4} Z" '
                 f'fill="{beard}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    if glasses:
        o.append(f'<circle cx="{lx}" cy="{ey}" r="11" fill="rgba(255,255,255,.18)" stroke="{INK}" stroke-width="3"/>'
                 f'<circle cx="{rx}" cy="{ey}" r="11" fill="rgba(255,255,255,.18)" stroke="{INK}" stroke-width="3"/><path d="M{lx + 11} {ey} H{rx - 11}" {ln}/>')
    return ''.join(o)


def person(x, y, s=1, skin='peach', suit='black', shirt='#F7F7F5', tie=RED, hair='side', hair_col='black', hat=None, hat_col=None,
           expr='neutral', look=0, arms='down', stance='stand', glasses=False, moustache=None, beard=None, nose=None, flip=False,
           lapels=True, talk=None, extras='', body=None, back=False, walk=None):
    """The cast. (x, y) = feet on the ground; unscaled height ~250 px (head r=44 is ~35% of it).
    skin: SKIN key; suit: SUIT key (or (base, shade)); hair: side|swoop|curly|bald|long|bun|spiky|buzz|none.
    talk=(t0, t1): mouth flaps between closed and open while the voiced line plays.
    back=True: seen from behind (over-the-shoulder foregrounds): no face, hair covers the head, no lapels.
    walk=(t0, t1): legs scissor while walking (move the figure with G(..., slide/tx keys) at the same time)."""
    sk, sk_sh = SKIN[skin] if isinstance(skin, str) else skin
    su, su_sh = SUIT[suit] if isinstance(suit, str) else suit
    hc = HAIR.get(hair_col, hair_col)
    o = [f'<ellipse cx="0" cy="2" rx="46" ry="9" fill="#000" opacity=".16"/>']
    if walk:
        o.append(animlib.G(_legs('walk'), animlib.flicker(walk[0], walk[1], .5)) + animlib.G(_legs('stand'), animlib.flicker(walk[0], walk[1], .5, on_first=False)))
    else:
        o.append(_legs(stance))
    body_path = body or BODY
    o.append(_shade_clip(f'<path d="{body_path}"/>', '<ellipse cx="52" cy="-100" rx="34" ry="70"/>', su, su_sh))
    if back:
        o.append(_arms(arms, su))
        o.append(_shade_clip(f'<circle cx="0" cy="{HEAD_C}" r="{HEAD_R}"/>', f'<ellipse cx="{HEAD_R * .95:.0f}" cy="{HEAD_C + 6}" rx="{HEAD_R * .62:.0f}" ry="{HEAD_R * 1.25:.0f}"/>', sk, sk_sh))
        if hair not in ('none', None, 'bald'):
            o.append(f'<path d="M-45 {HEAD_C + 14} C-50 {HEAD_C - 40} -26 {HEAD_C - 56} 0 {HEAD_C - 56} C26 {HEAD_C - 56} 50 {HEAD_C - 40} 45 {HEAD_C + 14} C30 {HEAD_C + 26} -30 {HEAD_C + 26} -45 {HEAD_C + 14} Z" '
                     f'fill="{hc}" stroke="{INK}" stroke-width="{LW}"/>')
        elif hair == 'bald':
            o.append(_hair('bald', hc, None))
        if hat: o.append(_hat(hat, hat_col or SUIT['black'][0]))
        return g(x, y, s, ''.join(o), flip)
    if lapels:
        o.append(f'<path d="M-13 -151 L0 -116 L13 -151 Z" fill="{shirt}" stroke="{INK}" stroke-width="{LW3}" stroke-linejoin="round"/>')
        if tie: o.append(f'<path d="M-4 -148 L4 -148 L6 -126 L0 -116 L-6 -126 Z" fill="{tie}" stroke="{INK}" stroke-width="2"/>')
        o.append(f'<path d="M-16 -151 L-2 -110 M16 -151 L2 -110" stroke="{INK}" stroke-width="{LW3}" fill="none"/>')
    o.append(_arms(arms, su))
    head = f'<circle cx="0" cy="{HEAD_C}" r="{HEAD_R}"/>'
    if hair == 'long': o.append(_hair('long', hc, None))
    o.append(_shade_clip(head, f'<ellipse cx="{HEAD_R * .95:.0f}" cy="{HEAD_C + 6}" rx="{HEAD_R * .62:.0f}" ry="{HEAD_R * 1.25:.0f}"/>', sk, sk_sh))
    if hair not in ('long', 'none', None): o.append(_hair(hair, hc, None))
    elif hair == 'long':
        o.append(f'<path d="M-34 {HEAD_C - 18} C-16 {HEAD_C - 26} 10 {HEAD_C - 22} 30 {HEAD_C - 28} C26 {HEAD_C - 50} -26 {HEAD_C - 52} -34 {HEAD_C - 18} Z" fill="{hc}"/>')
    mc = HAIR.get(moustache, moustache) if moustache else None
    bc = HAIR.get(beard, beard) if beard else None
    if talk:
        t0, t1 = talk
        o.append(face(expr, look, nose=nose, glasses=glasses, moustache=mc, beard=bc))
        o.append(animlib.G(f'<circle cx="{look * .6}" cy="{HEAD_C + 23 + (6 if nose == "big" else 0)}" r="9" fill="{sk}"/>'
                           f'<ellipse cx="{look * .6}" cy="{HEAD_C + 23 + (6 if nose == "big" else 0)}" rx="6" ry="7" fill="{INK}"/>', animlib.flicker(t0, t1)))
    else:
        o.append(face(expr, look, nose=nose, glasses=glasses, moustache=mc, beard=bc))
    if hat: o.append(_hat(hat, hat_col or SUIT['black'][0]))
    if arms == 'phone':   # handset + hand in front of the head
        o.append(f'<path d="M34 -136 Q62 -150 50 -170" fill="none" stroke="{INK}" stroke-width="{LW - .6}" stroke-linecap="round"/>'
                 f'<path d="M30 -228 C52 -230 58 -206 54 -176 C52 -162 40 -156 30 -160 L34 -172 C42 -174 44 -190 42 -206 C40 -214 32 -216 26 -214 Z" fill="#2B2B2E" stroke="{INK}" stroke-width="3"/>'
                 f'<circle cx="50" cy="-172" r="8" fill="{sk}" stroke="{INK}" stroke-width="2.6"/>')
    o.append(extras)
    return g(x, y, s, ''.join(o), flip)


def extra(x, y, s=1, tone='white', suit='black', hat=None, expr='neutral', flip=False, **kw):
    """Background people: white faces (named minor characters) or grey (anonymous)."""
    return person(x, y, s, skin=tone, suit=suit, hat=hat, expr=expr, flip=flip, hair=kw.pop('hair', 'none'), **kw)


def crowd(x0, x1, y, rows=3, s=1.0, seed=1, tones=('#8B8B8B', '#9C9C9C', '#777777', '#A8A8A8'), hats=.2):
    """Grey silhouette crowd (the anonymous public): overlapping heads + bodies, back rows smaller."""
    rnd = random.Random(seed)
    o = []
    for r in range(rows):
        sc = s * (0.78 + 0.11 * r)
        yy = y - (rows - 1 - r) * 34 * s
        n = int((x1 - x0) / (78 * sc)) + 1
        for i in range(n):
            cx = x0 + i * 78 * sc + rnd.uniform(-14, 14) * sc
            c = rnd.choice(tones)
            hat = ''
            if rnd.random() < hats:
                hat = f'<rect x="-22" y="-122" width="44" height="34" rx="4" fill="#5E5E5E" stroke="{INK}" stroke-width="3"/><ellipse cx="0" cy="-88" rx="38" ry="8" fill="#5E5E5E" stroke="{INK}" stroke-width="3"/>'
            o.append(g(cx, yy, sc, f'<path d="M-40 40 Q-42 -30 0 -32 Q42 -30 40 40 Z" fill="{c}" stroke="{INK}" stroke-width="3.4"/>'
                                   f'<circle cx="0" cy="-62" r="32" fill="{c}" stroke="{INK}" stroke-width="3.4"/>{hat}'))
    return ''.join(o)


def robot(x, y, s=1, body='#8C9199', emblem='#E06B3C', mark='✱', eyes='#47E2F0', expr='neutral', arms='down', name=None, flip=False):
    """A personified AI model / product: visor head with glowing eyes, chest emblem, stick limbs."""
    sh = '#6F747B'
    o = [f'<ellipse cx="0" cy="2" rx="46" ry="9" fill="#000" opacity=".16"/>', _legs('stand'), _arms(arms, body)]
    o.append(_shade_clip('<rect x="-44" y="-150" width="88" height="96" rx="26"/>', '<ellipse cx="54" cy="-100" rx="30" ry="70"/>', body, sh))
    o.append(f'<circle cx="0" cy="-104" r="17" fill="#3A3E45" stroke="{INK}" stroke-width="3"/>'
             + text(0, -103, mark, 26, "font-family:'DejaVu Sans',sans-serif;font-weight:700", emblem))
    o.append(_shade_clip('<rect x="-50" y="-246" width="100" height="88" rx="38"/>', '<ellipse cx="58" cy="-200" rx="32" ry="60"/>', body, sh))
    o.append(f'<rect x="-36" y="-226" width="72" height="42" rx="20" fill="#2B2F35" stroke="{INK}" stroke-width="3"/>')
    eh = 4 if expr == 'closed' else 9
    o.append(f'<rect x="-22" y="{-207 - eh / 2}" width="13" height="{eh}" rx="4" fill="{eyes}"/><rect x="9" y="{-207 - eh / 2}" width="13" height="{eh}" rx="4" fill="{eyes}"/>')
    if expr == 'angry':
        o.append(f'<path d="M-24 -218 L-8 -212 M24 -218 L8 -212" stroke="{eyes}" stroke-width="3"/>')
    o.append(f'<path d="M0 -246 V-262" stroke="{INK}" stroke-width="3.4"/><circle cx="0" cy="-266" r="6" fill="{emblem}" stroke="{INK}" stroke-width="2.4"/>')
    if name:
        o.append(f'<rect x="-30" y="-78" width="60" height="18" rx="3" fill="#F4F1E8" stroke="{INK}" stroke-width="2"/>' + caps(0, -69, name, 14))
    return g(x, y, s, ''.join(o), flip)


def mascot(x, y, s=1, expr='grin', arms='present', flip=False, talk=None, **kw):
    """The channel host who breaks the fourth wall (asides, sponsor reads). Re-style it to the creator; keep it constant."""
    d = dict(skin='peach', suit='brown', shirt='#F7F7F5', tie='#C0392F', hair='swoop', hair_col='dark', glasses=True)
    d.update(kw)
    return person(x, y, s, expr=expr, arms=arms, flip=flip, talk=talk, **d)


# ------------------------------------------------------------------ dialogue devices
def say(x, y, t, size=34, to=None, anchor='middle', kf=None):
    """VOICED line (the character speaks it in the VO): white handwriting with a dark outline, plus a short
    white tick pointing at the speaker's mouth (to=(x, y)). No box."""
    if anchor == 'middle':   # keep the line inside the frame
        hw = tw(t, size) / 2 + 24
        x = max(hw, min(W() - hw, x))
    o = wtext(x, y, t, size, anchor)
    if to:
        n = len(str(t).split('\n'))
        bx = x if anchor == 'middle' else (x + 20 if anchor == 'start' else x - 20)
        by = y + (n * size * 1.08) / 2 + 4 if to[1] > y else y - (n * size * 1.08) / 2 - 4
        dx, dy = to[0] - bx, to[1] - by
        L = math.hypot(dx, dy) or 1
        x0, y0 = bx + dx / L * 6, by + dy / L * 6
        x1, y1 = bx + dx / L * 24, by + dy / L * 24
        o += (f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" stroke="#1A1A1A" stroke-width="8" stroke-linecap="round"/>'
              f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" stroke="#FFFFFF" stroke-width="3.6" stroke-linecap="round"/>')
    return animlib.G(o, kf) if kf else o


def bubble(x, y, t, tail=None, size=28, w=None, kf=None, fill='#FFFFFF', shout=False):
    """UNVOICED gag line in a white box (the narrator keeps talking while we read it). Pops in."""
    lines = str(t).split('\n')
    bw = w or tw(t, size) + size * 1.3
    bh = len(lines) * size * 1.08 + size * .9
    o = ''
    if tail:
        tx, ty = tail
        bx0 = max(x - bw / 2 + 18, min(x + bw / 2 - 40, tx - 12))
        by = y + bh / 2 - 2 if ty > y else y - bh / 2 + 2
        o += f'<path d="M{bx0:.0f} {by:.0f} L{tx:.0f} {ty:.0f} L{bx0 + 24:.0f} {by:.0f} Z" fill="{fill}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    if shout:
        pts = []
        for i in range(28):
            a = 2 * math.pi * i / 28
            rr = 1.0 if i % 2 == 0 else 0.86
            pts.append(f'{x + bw / 2 * 1.12 * rr * math.cos(a):.0f},{y + bh / 2 * 1.25 * rr * math.sin(a):.0f}')
        o += f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    else:
        o += f'<rect x="{x - bw / 2:.0f}" y="{y - bh / 2:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="{size * .5:.0f}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
        if tail:  # hide the tail's base line inside the box
            tx, ty = tail
            bx0 = max(x - bw / 2 + 18, min(x + bw / 2 - 40, tx - 12))
            by = y + bh / 2 if ty > y else y - bh / 2
            o += f'<path d="M{bx0 + 2:.0f} {by:.0f} H{bx0 + 22:.0f}" stroke="{fill}" stroke-width="5"/>'
    o += text(x, y + 1, t, size, SCRIPT, INK)
    return animlib.G(o, kf if kf is not None else animlib.pop(0.0), (x, y))


def thought(cx, cy, w, h, inner='', trail=None, kf=None, t=None, size=28):
    """Thought cloud with scalloped edge; inner = SVG drawn inside (icons, a mini scene) or text t."""
    n = 14
    circ = []
    for i in range(n):
        a = 2 * math.pi * i / n
        circ.append((cx + w / 2 * .82 * math.cos(a), cy + h / 2 * .78 * math.sin(a), min(w, h) * .2))
    edge = ''.join(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r:.0f}" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>' for px, py, r in circ)
    fillc = ''.join(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r - 2.5:.0f}" fill="#FFFFFF"/>' for px, py, r in circ)
    core = f'<ellipse cx="{cx}" cy="{cy}" rx="{w * .42:.0f}" ry="{h * .4:.0f}" fill="#FFFFFF"/>'
    tr = ''
    if trail:
        tx, ty = trail
        for k, rr in ((.55, 11), (.8, 7)):
            px, py = cx + (tx - cx) * k, cy + h * .45 + (ty - cy - h * .45) * k
            tr += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rr}" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
    body = tr + edge + fillc + core + inner + (text(cx, cy, t, size, SCRIPT, INK) if t else '')
    return animlib.G(body, kf if kf is not None else animlib.pop(0.0, .3), (cx, cy))


def label_arrow(x, y, t, to, size=30, kf=None, curve=40):
    """Name/label in white handwriting with a curved arrow to the target (types on with animlib.type_cps)."""
    tx, ty = to
    sx, sy = x + (-10 if tx < x else 10), y + (size * .6 if ty > y else -size * .6)
    mx, my = (sx + tx) / 2 + (curve if tx < x else -curve), (sy + ty) / 2
    ang = math.atan2(ty - my, tx - mx)
    a1, a2 = ang + 2.6, ang - 2.6
    head = f'M{tx + 16 * math.cos(a1):.0f} {ty + 16 * math.sin(a1):.0f} L{tx} {ty} L{tx + 16 * math.cos(a2):.0f} {ty + 16 * math.sin(a2):.0f}'
    arr = f'M{sx:.0f} {sy:.0f} Q{mx:.0f} {my:.0f} {tx} {ty} {head}'
    o = (f'<path d="{arr}" fill="none" stroke="#1A1A1A" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{arr}" fill="none" stroke="#FFFFFF" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>')
    tx_kf = kf or None
    return o + wtext(x, y, t, size, 'middle', kf=tx_kf)


def place_caption(t, size=36, corner='bl', kf=None):
    """'Connecticut, 1837.' - white handwriting, bottom-left (or top-right), typed on. In 9:16 it sits above the Reels UI."""
    x, anc = (36, 'start') if corner in ('bl', 'tl') else (W() - 36, 'end')
    bottom = H() - 44 if W() > H() else H() * .74
    y = bottom if corner in ('bl', 'br') else (48 if W() > H() else H() * .12)
    return wtext(x, y, t, size, anc, kf=kf)


# ------------------------------------------------------------------ card shots (full frame)
def card(t, size=40, y=None, x=None, anchor='middle', kf=None):
    """Narration / chapter text on pure black. Give kf=animlib.type_cps(...) to type it on, or nothing for a hard cut."""
    return frame_svg(f'<rect width="{W()}" height="{H()}" fill="#000"/>' +
                     text(x if x is not None else W() / 2, y if y is not None else H() / 2, t, size, SCRIPT, '#FFFFFF', anchor, kf=kf), t)


def chapter(title, size=None):
    return card(title, size or (52 if W() > H() else 58))


def end_card(word='Subscribe'):
    return frame_svg(f'<rect width="{W()}" height="{H()}" fill="#000"/>' + text(W() / 2, H() / 2, word, 96 if W() > H() else 110, SCRIPT_B, '#FFFFFF'), word)


# ------------------------------------------------------------------ settings
def fill_bg(col): return f'<rect x="-200" y="-200" width="{W() + 400}" height="{H() + 400}" fill="{col}"/>'


def room(wall=CREAM_WALL, floor=WOOD, horizon=None, wainscot=None):
    """Interior: wall + floor (+ optional wood panelling below `wainscot` y)."""
    hz = horizon if horizon is not None else H() * .72
    o = [fill_bg(wall), f'<rect x="-200" y="{hz}" width="{W() + 400}" height="{H() - hz + 200}" fill="{floor}"/>',
         f'<path d="M-200 {hz} H{W() + 200}" stroke="{INK}" stroke-width="{LW2}"/>']
    if wainscot:
        o.append(f'<rect x="-200" y="{wainscot}" width="{W() + 400}" height="{hz - wainscot}" fill="{PANEL}" stroke="{INK}" stroke-width="{LW2}"/>')
        for xx in range(-160, W() + 200, 150):
            o.append(f'<rect x="{xx + 14}" y="{wainscot + 14}" width="122" height="{hz - wainscot - 28}" fill="none" stroke="#3E2719" stroke-width="2.4"/>')
    return ''.join(o)


def window(x, y, w, h, view='city', frame='#F4F1EA'):
    sky = {'city': '#AFC6D6', 'night': '#1F2B44', 'sky': '#A9D3EA', 'dusk': '#E9A47E'}.get(view, view)
    cid = uid('w')
    o = [f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#{cid})">', f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{sky}"/>']
    if view in ('city', 'night', 'dusk'):
        rnd = random.Random(int(x + y))
        bx = x
        while bx < x + w:
            bw, bh = rnd.uniform(.12, .22) * w, rnd.uniform(.25, .6) * h
            col = '#8CA5B8' if view == 'city' else ('#2E3C5A' if view == 'night' else '#B57A63')
            o.append(f'<rect x="{bx:.0f}" y="{y + h - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{col}"/>')
            for wy in range(int(y + h - bh + 10), int(y + h - 8), 18):
                for wx in range(int(bx + 6), int(bx + bw - 8), 14):
                    lit = '#F2D98B' if view == 'night' and rnd.random() < .4 else ('#C9D7E2' if view == 'city' else '#3A4867')
                    o.append(f'<rect x="{wx}" y="{wy}" width="6" height="8" fill="{lit}"/>')
            bx += bw + 4
    o.append(f'<path d="M{x + w * .15} {y + h} L{x + w * .55} {y} M{x + w * .3} {y + h} L{x + w * .7} {y}" stroke="#FFFFFF" stroke-width="10" opacity=".25"/></g>')
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{frame}" stroke-width="12"/>'
             f'<path d="M{x + w / 2} {y} V{y + h} M{x} {y + h / 2} H{x + w}" stroke="{frame}" stroke-width="8"/>'
             f'<rect x="{x - 6}" y="{y - 6}" width="{w + 12}" height="{h + 12}" fill="none" stroke="{INK}" stroke-width="{LW2}"/>'
             f'<rect x="{x + 6}" y="{y + 6}" width="{w - 12}" height="{h - 12}" fill="none" stroke="{INK}" stroke-width="2"/>')
    return ''.join(o)


def bookshelf(x, y, w, h, seed=2):
    rnd = random.Random(seed)
    cols = ['#9C3B32', '#2F4A6B', '#C9A24A', '#4E6B45', '#6B4A7A', '#B86A3A', '#3C3C3C', '#7A8A99']
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WOOD_D}" stroke="{INK}" stroke-width="{LW2}"/>']
    nsh = max(2, int(h / 95))
    sh = (h - 16) / nsh
    for i in range(nsh):
        sy = y + 8 + i * sh
        bx = x + 10
        while bx < x + w - 18:
            bw = rnd.uniform(12, 22); bh = sh * rnd.uniform(.62, .86)
            o.append(f'<rect x="{bx:.0f}" y="{sy + sh - bh - 6:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{rnd.choice(cols)}" stroke="{INK}" stroke-width="2"/>')
            bx += bw + rnd.uniform(0, 3)
        o.append(f'<rect x="{x}" y="{sy + sh - 6:.0f}" width="{w}" height="8" fill="{WOOD}" stroke="{INK}" stroke-width="2"/>')
    return ''.join(o)


def curtain(x, y, w, h, col='#A8343A', side='r'):
    sh = '#86262C'
    tie_y = y + h * .62
    inner = x + (w * .25 if side == 'r' else w * .75)
    o = [f'<path d="M{x} {y} H{x + w} V{y + h} H{inner} Q{inner + (w * .2 if side == "r" else -w * .2):.0f} {tie_y} {x + w / 2} {y} Z" fill="{col}" stroke="{INK}" stroke-width="{LW2}"/>']
    for k in (.3, .5, .7):
        o.append(f'<path d="M{x + w * k:.0f} {y + 10} Q{x + w * k + 8:.0f} {y + h * .5:.0f} {x + w * k:.0f} {y + h - 10}" stroke="{sh}" stroke-width="7" fill="none"/>')
    o.append(f'<rect x="{x + w * .2:.0f}" y="{tie_y - 10:.0f}" width="{w * .7:.0f}" height="22" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="2.6"/>')
    return ''.join(o)


def portrait(x, y, w, h, inner=''):
    cid = uid('pc')
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#6B4A31" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<clipPath id="{cid}"><rect x="{x + 14}" y="{y + 14}" width="{w - 28}" height="{h - 28}"/></clipPath>'
            f'<rect x="{x + 14}" y="{y + 14}" width="{w - 28}" height="{h - 28}" fill="#CFC4AE" stroke="{INK}" stroke-width="2"/>'
            f'<g clip-path="url(#{cid})">{inner}<path d="M{x + w * .25} {y + h} L{x + w * .6} {y} M{x + w * .45} {y + h} L{x + w * .8} {y}" stroke="#FFF" stroke-width="12" opacity=".22"/></g>')


def door(x, y, w, h, col='#7A5236', knob=GOLD):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<rect x="{x + w * .14}" y="{y + h * .08}" width="{w * .72}" height="{h * .36}" fill="none" stroke="{INK}" stroke-width="2.4"/>'
            f'<rect x="{x + w * .14}" y="{y + h * .52}" width="{w * .72}" height="{h * .4}" fill="none" stroke="{INK}" stroke-width="2.4"/>'
            f'<circle cx="{x + w * .84}" cy="{y + h * .5}" r="6" fill="{knob}" stroke="{INK}" stroke-width="2"/>')


def desk(cx, y, w=420, h=110, top=WOOD_D, front=WOOD):
    """Desk seen from the front; y = top surface. Put characters BEFORE the desk so it hides their legs."""
    return (f'<rect x="{cx - w / 2}" y="{y + 16}" width="{w}" height="{h}" fill="{front}" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<rect x="{cx - w / 2 - 16}" y="{y}" width="{w + 32}" height="20" rx="4" fill="{top}" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<rect x="{cx - w / 2 + 24}" y="{y + 40}" width="{w * .3}" height="{h * .45}" fill="none" stroke="{INK}" stroke-width="2.2"/>'
            f'<rect x="{cx + w / 2 - 24 - w * .3}" y="{y + 40}" width="{w * .3}" height="{h * .45}" fill="none" stroke="{INK}" stroke-width="2.2"/>')


def chair_back(cx, y, col='#3A2A22', w=130, h=190):
    return (f'<rect x="{cx - w / 2}" y="{y - h}" width="{w}" height="{h}" rx="{w * .3}" fill="{col}" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<path d="M{cx - w * .3} {y - h * .8} V{y - h * .2} M{cx} {y - h * .85} V{y - h * .2} M{cx + w * .3} {y - h * .8} V{y - h * .2}" stroke="#2A1D17" stroke-width="3"/>')


def papers(x, y, n=4, w=80, rot=0):
    o = ''.join(f'<rect x="{x + i * 1.5 - w / 2:.0f}" y="{y - i * 6:.0f}" width="{w}" height="10" fill="#FBFBF7" stroke="{INK}" stroke-width="2"/>' for i in range(n))
    return f'<g transform="rotate({rot} {x} {y})">{o}</g>'


def laptop(cx, y, s=1, screen='#9FB9C8', back=False):
    if back:
        return g(cx, y, s, f'<path d="M-70 0 L-62 -92 L62 -92 L70 0 Z" fill="#A9ADB3" stroke="{INK}" stroke-width="{LW2}"/><circle cx="0" cy="-48" r="9" fill="#C9CCD0"/>')
    return g(cx, y, s, f'<rect x="-62" y="-96" width="124" height="84" rx="6" fill="#3B3E44" stroke="{INK}" stroke-width="{LW2}"/>'
                       f'<rect x="-54" y="-88" width="108" height="68" fill="{screen}"/>'
                       f'<path d="M-80 0 L-66 -12 H66 L80 0 Z" fill="#A9ADB3" stroke="{INK}" stroke-width="{LW2}"/>')


def monitor(cx, cy, w, h, inner='', bez='#2D3036'):
    """Screen whose inner SVG is drawn in screen coordinates (0,0)-(w,h) via translate."""
    cid = uid('m')
    return (f'<rect x="{cx - 14}" y="{cy + h / 2}" width="28" height="44" fill="#5A5E66" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<rect x="{cx - 60}" y="{cy + h / 2 + 40}" width="120" height="12" rx="5" fill="#5A5E66" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<rect x="{cx - w / 2 - 14}" y="{cy - h / 2 - 14}" width="{w + 28}" height="{h + 28}" rx="10" fill="{bez}" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<clipPath id="{cid}"><rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}"/></clipPath>'
            f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" fill="#F3F4F6"/>'
            f'<g clip-path="url(#{cid})"><g transform="translate({cx - w / 2} {cy - h / 2})">{inner}</g></g>')


def chat_ui(w, h, prompt='', reply_lines=3, accent='#E06B3C'):
    """Generic chatbot screen (no real product UI)."""
    o = [f'<rect width="{w}" height="{h}" fill="#F6F5F2"/>', f'<rect width="{w}" height="{h * .12:.0f}" fill="#E9E6DF"/>',
         f'<rect x="{w * .45:.0f}" y="{h * .2:.0f}" width="{w * .5:.0f}" height="{h * .14:.0f}" rx="12" fill="#DCE6F0" stroke="{INK}" stroke-width="1.6"/>',
         text(w * .7, h * .27, prompt, max(12, h * .065), SCRIPT, INK)]
    o.append(f'<circle cx="{w * .08:.0f}" cy="{h * .46:.0f}" r="{h * .035:.0f}" fill="{accent}"/>')
    for i in range(reply_lines):
        o.append(f'<rect x="{w * .14:.0f}" y="{h * (.43 + i * .08):.0f}" width="{w * (.7 - .12 * (i == reply_lines - 1)):.0f}" height="{h * .035:.0f}" rx="4" fill="#C9C6BF"/>')
    o.append(f'<rect x="{w * .08:.0f}" y="{h * .82:.0f}" width="{w * .84:.0f}" height="{h * .1:.0f}" rx="10" fill="#FFFFFF" stroke="{INK}" stroke-width="1.6"/>')
    return ''.join(o)


def phone_old(x, y, s=1):
    return g(x, y, s, f'<ellipse cx="0" cy="0" rx="34" ry="10" fill="#2B2B2E" stroke="{INK}" stroke-width="3"/>'
                      f'<rect x="-6" y="-110" width="12" height="108" fill="#2B2B2E" stroke="{INK}" stroke-width="3"/>'
                      f'<path d="M-22 -124 Q0 -140 22 -124 L14 -110 H-14 Z" fill="#2B2B2E" stroke="{INK}" stroke-width="3"/>'
                      f'<path d="M6 -70 Q40 -74 46 -40" fill="none" stroke="{INK}" stroke-width="3"/><rect x="38" y="-46" width="16" height="28" rx="6" fill="#2B2B2E" stroke="{INK}" stroke-width="3"/>')


def smartphone(cx, cy, w=150, h=290, inner='', rot=0):
    cid = uid('sp')
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="20" fill="#2A2C31" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<clipPath id="{cid}"><rect x="{cx - w / 2 + 10}" y="{cy - h / 2 + 24}" width="{w - 20}" height="{h - 48}" rx="6"/></clipPath>'
            f'<rect x="{cx - w / 2 + 10}" y="{cy - h / 2 + 24}" width="{w - 20}" height="{h - 48}" rx="6" fill="#F4F4F2"/>'
            f'<g clip-path="url(#{cid})"><g transform="translate({cx - w / 2 + 10} {cy - h / 2 + 24})">{inner}</g></g>'
            f'<circle cx="{cx}" cy="{cy + h / 2 - 12}" r="6" fill="#4A4D54"/></g>')


def plaque(cx, y, t, w=None, size=20, fill=GOLD):
    """Desk name plate ('BANK PRESIDENT', 'CEO')."""
    w = w or tw(t, size, 'caps') + 34
    return (f'<path d="M{cx - w / 2} {y} L{cx - w / 2 + 8} {y - size - 14} H{cx + w / 2 - 8} L{cx + w / 2} {y} Z" fill="{fill}" stroke="{INK}" stroke-width="2.8" stroke-linejoin="round"/>'
            + caps(cx, y - (size + 14) / 2, t, size))


def sign(cx, cy, t, w=None, size=34, fill='#D9A441', col=INK, rot=0):
    """Wall/hanging sign plate in hand caps ('RAILROAD COMPANY')."""
    w = w or tw(t, size, 'caps') + 50
    h = size * 1.1 * len(str(t).split('\n')) + 22
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{INK}" stroke-width="{LW2}"/>'
            + caps(cx, cy + 2, t, size, col) + '</g>')


def post_sign(x, y, t, size=26, w=None):
    """Wooden sign on a post ('HUDSON RIVER', 'SAME WAY')."""
    w = w or tw(t, size, 'caps') + 36
    h = size * 1.1 * len(str(t).split('\n')) + 20
    return (f'<rect x="{x - 7}" y="{y - h - 70}" width="14" height="{h + 70}" fill="{WOOD}" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x - w / 2}" y="{y - h - 100}" width="{w}" height="{h}" rx="3" fill="#4A3324" stroke="{INK}" stroke-width="{LW2}"/>'
            + caps(x, y - h / 2 - 98, t, size, '#F2EBDD'))


def sky(top='#A9D3EA', ground=None, horizon=None):
    hz = horizon if horizon is not None else H() * .78
    o = fill_bg(top)
    if ground: o += f'<rect x="-200" y="{hz}" width="{W() + 400}" height="{H() + 200}" fill="{ground}"/><path d="M-200 {hz} H{W() + 200}" stroke="{INK}" stroke-width="{LW2}"/>'
    return o


def cloud(cx, cy, s=1):
    return g(cx, cy, s, f'<path d="M-60 10 Q-64 -14 -36 -16 Q-30 -40 -4 -34 Q14 -50 34 -30 Q62 -30 60 -2 Q66 14 46 16 H-46 Q-62 16 -60 10 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="2.6"/>')


def buildings(y, x0=-60, x1=None, seed=3, palette=('#D8CDB8', '#C9B79A', '#B9C3C9', '#E2DACB', '#A9AFA8'), hmin=.35, hmax=.75):
    """Row of flat facades with window grids standing on y."""
    x1 = x1 if x1 is not None else W() + 60
    rnd = random.Random(seed)
    o, x = [], x0
    while x < x1:
        bw, bh = rnd.uniform(110, 210), rnd.uniform(hmin, hmax) * y
        col = rnd.choice(palette)
        o.append(f'<rect x="{x:.0f}" y="{y - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{col}" stroke="{INK}" stroke-width="{LW2}"/>')
        for wy in range(int(y - bh + 18), int(y - 30), 34):
            for wx in range(int(x + 14), int(x + bw - 26), 30):
                o.append(f'<rect x="{wx}" y="{wy}" width="16" height="20" fill="#7E95A6" stroke="{INK}" stroke-width="1.8"/>')
        x += bw + rnd.uniform(-10, 6)
    return ''.join(o)


def skyline(y, col='#9FB3C2', seed=5):
    rnd = random.Random(seed)
    o, x = [], -60
    while x < W() + 60:
        bw, bh = rnd.uniform(40, 110), rnd.uniform(60, 220)
        o.append(f'<rect x="{x:.0f}" y="{y - bh:.0f}" width="{bw:.0f}" height="{bh + 2:.0f}" fill="{col}"/>')
        x += bw
    return ''.join(o)


def street(ground='#B9AE9B', sky_col='#A9D3EA', seed=3):
    hz = H() * .74
    return (sky(sky_col) + skyline(hz - 120, '#BFD0DA', seed + 1) + buildings(hz, seed=seed) +
            f'<rect x="-200" y="{hz}" width="{W() + 400}" height="{H()}" fill="{ground}"/><path d="M-200 {hz} H{W() + 200}" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<rect x="-200" y="{hz}" width="{W() + 400}" height="16" fill="#CFC6B6" stroke="{INK}" stroke-width="2.4"/>')


def stage(cx=None, floor_y=None, bg='#232326'):
    """Character-introduction spotlight: dark void, light cone from above, lit floor ellipse. Put the character at (cx, floor_y)."""
    cx = cx if cx is not None else W() / 2
    fy = floor_y if floor_y is not None else H() * .8
    gid = uid('sg')
    return (fill_bg(bg) + f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2E6C4" stop-opacity=".05"/>'
            f'<stop offset="1" stop-color="#F2E6C4" stop-opacity=".22"/></linearGradient></defs>'
            f'<path d="M{cx - 40} -40 L{cx + 40} -40 L{cx + 180} {fy} L{cx - 180} {fy} Z" fill="url(#{gid})"/>'
            f'<ellipse cx="{cx}" cy="{fy}" rx="230" ry="48" fill="#5A4E3A" opacity=".55"/><ellipse cx="{cx}" cy="{fy}" rx="185" ry="36" fill="#A08A60"/>')


def info_bg(col=INFO_BG, blob=INFO_BLOB):
    """Blue-grey explainer backdrop with a soft lighter blob (infographic shots)."""
    gid = uid('ib')
    return (fill_bg(col) + f'<defs><radialGradient id="{gid}"><stop offset="0" stop-color="{blob}"/><stop offset=".7" stop-color="{blob}" stop-opacity=".6"/>'
            f'<stop offset="1" stop-color="{blob}" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse cx="{W() / 2}" cy="{H() / 2}" rx="{W() * .46}" ry="{H() * .42}" fill="url(#{gid})"/>')


def rays_bg(col='#8DA1B1', ray='#A3B5C2', n=24):
    """Sunburst for logo/wordmark reveals and 'big moment' objects."""
    cx, cy, R = W() / 2, H() / 2, max(W(), H())
    o = [fill_bg(col)]
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + .5) / n
        o.append(f'<path d="M{cx} {cy} L{cx + R * math.cos(a0):.0f} {cy + R * math.sin(a0):.0f} L{cx + R * math.cos(a1):.0f} {cy + R * math.sin(a1):.0f} Z" fill="{ray}" opacity=".55"/>')
    return ''.join(o)


def burst(cx, cy, r=120, col='#F7D35C', n=14):
    """Spiky glow behind a 'eureka' object or a happy character."""
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        rr = r if i % 2 == 0 else r * .62
        pts.append(f'{cx + rr * math.cos(a):.0f},{cy + rr * math.sin(a):.0f}')
    return f'<polygon points="{" ".join(pts)}" fill="{col}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'


def blob(cx, cy, rx, ry=None, seed=1, n=9, jit=.32):
    """Smooth irregular closed path (continents, bushes, rocks, smoke)."""
    rnd = random.Random(seed); ry = ry or rx
    pts = [(cx + rx * (1 + rnd.uniform(-jit, jit)) * math.cos(2 * math.pi * i / n), cy + ry * (1 + rnd.uniform(-jit, jit)) * math.sin(2 * math.pi * i / n)) for i in range(n)]
    mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2) for i in range(n)]
    d = f'M{mids[-1][0]:.0f} {mids[-1][1]:.0f} ' + ' '.join(f'Q{pts[i][0]:.0f} {pts[i][1]:.0f} {mids[i][0]:.0f} {mids[i][1]:.0f}' for i in range(n)) + ' Z'
    return d


def globe(cx, cy, r, space=True):
    """Earth from space (hooks: 'one company, the whole world')."""
    rnd = random.Random(7)
    cid = uid('gl')
    o = [fill_bg('#141A2A')] if space else []
    if space:
        o += [f'<circle cx="{rnd.uniform(0, W()):.0f}" cy="{rnd.uniform(0, H()):.0f}" r="{rnd.uniform(.8, 2.2):.1f}" fill="#FFFFFF" opacity="{rnd.uniform(.4, .9):.2f}"/>' for _ in range(90)]
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 18}" fill="#5C8FC9" opacity=".18"/>')
    o.append(f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath><circle cx="{cx}" cy="{cy}" r="{r}" fill="#3E6FA8"/>')
    land = ''.join(f'<path d="{blob(cx + dx * r, cy + dy * r, k * r * .22, k * r * .3, seed=i + 3, n=11, jit=.45)}" fill="#6AA057" stroke="#2F5E2A" stroke-width="2.4"/>'
                   for i, (dx, dy, k) in enumerate(((-.55, -.35, 1.1), (-.35, .3, .9), (.25, -.45, .8), (.35, .15, 1.2), (.05, .7, .5), (-.8, .2, .5), (.75, -.1, .45))))
    o.append(f'<g clip-path="url(#{cid})">{land}<circle cx="{cx + r * .35}" cy="{cy}" r="{r}" fill="#000" opacity=".18"/></g>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="{LW2}"/>')
    return ''.join(o)


# ------------------------------------------------------------------ props: money, docs, charts, tech
def cash(x, y, s=1, rot=0):
    return g(x, y, s, f'<rect x="-44" y="-22" width="88" height="44" rx="4" fill="#7FBF6A" stroke="{INK}" stroke-width="3"/>'
                      f'<rect x="-36" y="-14" width="72" height="28" rx="3" fill="none" stroke="#3E7A34" stroke-width="2"/>'
                      + text(0, 1, '$', 26, CAPS, '#2F6A2A'), rot=rot)


def money_pile(cx, y, w=360, seed=4):
    rnd = random.Random(seed)
    return ''.join(cash(cx + rnd.uniform(-w / 2, w / 2) * (1 - k / 40), y - k * 4, rnd.uniform(.8, 1.1), rnd.uniform(-35, 35)) for k in range(36))


def money_bag(x, y, s=1, mark='$'):
    return g(x, y, s, f'<path d="M-46 -10 C-56 -60 -26 -86 -14 -96 L-22 -112 H22 L14 -96 C26 -86 56 -60 46 -10 C40 4 -40 4 -46 -10 Z" fill="#E2A65E" stroke="{INK}" stroke-width="3.4"/>'
                      f'<path d="M-18 -98 H18" stroke="{INK}" stroke-width="5"/>' + text(0, -44, mark, 44, CAPS, '#3E8E3A'))


def gold_bars(cx, y, n=6):
    o = []
    for i in range(n):
        r, c = divmod(i, 3)
        x = cx + (c - 1) * 70 + r * 35
        yy = y - r * 26
        o.append(f'<path d="M{x - 32} {yy} L{x - 24} {yy - 22} H{x + 24} L{x + 32} {yy} Z" fill="#E7B84A" stroke="{INK}" stroke-width="3"/>')
    return ''.join(o)


def document(cx, cy, w, h, title='', lines=6, rot=0, stamp=None, stamp_col=RED, sig=False, body_text=None):
    o = [f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" fill="#FBFAF6" stroke="{INK}" stroke-width="{LW2}"/>']
    if title: o.append(caps(cx, cy - h / 2 + 40, title, min(34, w / max(6, len(title)) * 1.6)))
    if body_text:
        o.append(text(cx - w / 2 + 26, cy - h / 2 + 90, body_text, 22, SCRIPT, INK, 'start', lh=1.15))
    else:
        for i in range(lines):
            yy = cy - h / 2 + 80 + i * 26
            if yy > cy + h / 2 - 50: break
            o.append(f'<path d="M{cx - w / 2 + 26} {yy} H{cx + w / 2 - 26 - (40 if i % 3 == 2 else 0)}" stroke="#555" stroke-width="2.4"/>')
    if sig: o.append(f'<path d="M{cx + w * .05} {cy + h / 2 - 40} c10 -20 20 10 30 -6 s16 14 26 -4 s14 10 30 -2" fill="none" stroke="{INK}" stroke-width="2.4"/>')
    if stamp:
        o.append(f'<g transform="rotate(-14 {cx} {cy + h * .18})"><rect x="{cx - w * .36}" y="{cy + h * .18 - 26}" width="{w * .72}" height="52" rx="6" fill="none" stroke="{stamp_col}" stroke-width="5"/>'
                 + caps(cx, cy + h * .18 + 2, stamp, 34, stamp_col) + '</g>')
    return f'<g transform="rotate({rot} {cx} {cy})">{"".join(o)}</g>'


def newspaper(cx, cy, w, h, headline, sub='', photo='', rot=0, masthead='THE DAILY LEDGER'):
    o = [f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" fill="#E9E7E1" stroke="{INK}" stroke-width="{LW2}"/>',
         caps(cx, cy - h / 2 + 30, masthead, 22), f'<path d="M{cx - w / 2 + 18} {cy - h / 2 + 48} H{cx + w / 2 - 18}" stroke="{INK}" stroke-width="2.4"/>',
         caps(cx, cy - h / 2 + 92 + headline.count('\n') * 24, headline, min(46, (w - 40) / max(8, max(len(l) for l in headline.split(chr(10)))) * 1.75))]
    py = cy - h / 2 + 140 + 48 * (headline.count('\n'))
    if sub: o.append(text(cx, py, sub, 22, SCRIPT, '#333')); py += 30
    pw, ph = w * .48, h - (py - (cy - h / 2)) - 30
    o.append(f'<rect x="{cx - w / 2 + 20}" y="{py}" width="{pw:.0f}" height="{ph:.0f}" fill="#BDBBB4" stroke="{INK}" stroke-width="2.4"/>{photo}')
    for i in range(int(ph / 18)):
        o.append(f'<path d="M{cx - w / 2 + 40 + pw} {py + 10 + i * 18} H{cx + w / 2 - 22}" stroke="#77756F" stroke-width="2.2"/>')
    return f'<g transform="rotate({rot} {cx} {cy})">{"".join(o)}</g>'


def chart(x, y, w, h, pts, col=RED, title='', board='#F8F6F0', kf_line=None):
    """Whiteboard chart; pts = values 0..1 left to right. kf_line=animlib.draw(t, d) draws the line on."""
    path = ' '.join(f'{"M" if i == 0 else "L"}{x + 30 + (w - 60) * i / (len(pts) - 1):.0f} {y + h - 30 - (h - 80) * v:.0f}' for i, v in enumerate(pts))
    line = f'<path d="{path}" fill="none" stroke="{col}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>'
    return (f'<rect x="{x - 10}" y="{y - 10}" width="{w + 20}" height="{h + 20}" fill="#6B4A31" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{board}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x + 24} {y + 40} V{y + h - 24} H{x + w - 20}" fill="none" stroke="{INK}" stroke-width="3"/>'
            + (caps(x + 26, y + 26, title, 24, INK, 'start') if title else '')
            + (animlib.G(line, kf_line) if kf_line else line))


def bars(x, y, w, h, vals, cols=None, labels=None, kf_t=None):
    """Bar chart on the current background; vals 0..1. kf_t = time the bars grow (staggered)."""
    n = len(vals)
    bw = w / (n * 1.5)
    o = [f'<path d="M{x} {y - h} V{y} H{x + w}" fill="none" stroke="{INK}" stroke-width="3.4"/>']
    for i, v in enumerate(vals):
        bx = x + bw * .5 + i * bw * 1.5
        c = (cols or [GREEN] * n)[i]
        bar = f'<rect x="{bx:.0f}" y="{y - h * v:.0f}" width="{bw:.0f}" height="{h * v:.0f}" fill="{c}" stroke="{INK}" stroke-width="3"/>'
        o.append(animlib.G(bar, [[0, {'sy': 0}], [kf_t + i * .12, {'sy': 0}], [kf_t + i * .12 + .4, {'sy': 1}, 'b']], (bx, y)) if kf_t is not None else bar)
        if labels: o.append(caps(bx + bw / 2, y + 22, labels[i], 18))
    return ''.join(o)


def price_box(cx, cy, t, fill=RED, size=44, w=None):
    w = w or tw(t, size, 'caps') + 40
    return f'<rect x="{cx - w / 2}" y="{cy - size * .9}" width="{w}" height="{size * 1.8}" fill="{fill}" stroke="{INK}" stroke-width="3"/>' + caps(cx, cy + 1, t, size, '#FFFFFF')


def stat_card(cx, cy, big, small='', col=GREEN, w=None, size=64):
    """'$22 BILLION / COMBINED VALUE' - white rounded card, big coloured hand caps."""
    w = w or max(tw(big, size, 'caps'), tw(small, 24, 'caps')) + 70
    h = size * 1.2 + (40 if small else 20)
    return (f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="14" fill="#FFFFFF" stroke="{INK}" stroke-width="3.4"/>'
            + caps(cx, cy - (12 if small else 0), big, size, col) + (caps(cx - w / 2 + 34, cy + h / 2 - 22, small, 22, INK, 'start') if small else ''))


def arrow(x0, y0, x1, y1, col=RED, w=26):
    """Chunky outlined block arrow."""
    a = math.atan2(y1 - y0, x1 - x0)
    L = math.hypot(x1 - x0, y1 - y0)
    hw, hl = w * .5, w * 1.3
    pts = [(0, -hw / 2), (L - hl, -hw / 2), (L - hl, -w * .8), (L, 0), (L - hl, w * .8), (L - hl, hw / 2), (0, hw / 2)]
    P = ' '.join(f'{x0 + px * math.cos(a) - py * math.sin(a):.0f},{y0 + px * math.sin(a) + py * math.cos(a):.0f}' for px, py in pts)
    return f'<polygon points="{P}" fill="{col}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'


def mark(x, y, ok=True, s=1):
    """Green check / red cross."""
    if ok:
        return f'<path d="M{x - 16 * s} {y} L{x - 4 * s} {y + 13 * s} L{x + 18 * s} {y - 15 * s}" fill="none" stroke="{GREEN}" stroke-width="{8 * s}" stroke-linecap="round" stroke-linejoin="round"/>'
    return f'<path d="M{x - 15 * s} {y - 15 * s} L{x + 15 * s} {y + 15 * s} M{x + 15 * s} {y - 15 * s} L{x - 15 * s} {y + 15 * s}" stroke="{RED}" stroke-width="{8 * s}" stroke-linecap="round"/>'


def calendar(cx, cy, month='MARCH 2024', circle=None, w=230, xs=0):
    """Desk calendar; circle = day index (0..27) to ring in red; xs = number of days crossed out."""
    h = w * .9
    o = [f'<path d="M{cx - w / 2} {cy + h / 2} L{cx - w / 2 + 16} {cy - h / 2} H{cx + w / 2 - 16} L{cx + w / 2} {cy + h / 2} Z" fill="#EDE6D3" stroke="{INK}" stroke-width="{LW2}"/>',
         f'<rect x="{cx - w / 2 + 16}" y="{cy - h / 2}" width="{w - 32}" height="{h * .2}" fill="{RED}" stroke="{INK}" stroke-width="{LW2}"/>',
         caps(cx, cy - h / 2 + h * .1 + 2, month, w * .09, '#FFFFFF')]
    for d in range(28):
        r, c = divmod(d, 7)
        x, y = cx - w / 2 + 34 + c * (w - 68) / 6, cy - h / 2 + h * .32 + r * h * .16
        o.append(caps(x, y, str(d + 1), w * .07))
        if d < xs: o.append(mark(x, y, False, .5))
        if circle == d: o.append(f'<ellipse cx="{x}" cy="{y}" rx="{w * .07}" ry="{w * .06}" fill="none" stroke="{RED}" stroke-width="3"/>')
    return ''.join(o)


def server_racks(x0, y, n=4, h=300, w=110, glow='#47E2F0'):
    o = []
    for i in range(n):
        x = x0 + i * (w + 16)
        o.append(f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" rx="6" fill="#3A3F48" stroke="{INK}" stroke-width="{LW2}"/>')
        for k in range(int(h / 34)):
            yy = y - h + 14 + k * 34
            o.append(f'<rect x="{x + 10}" y="{yy}" width="{w - 20}" height="22" rx="3" fill="#2A2E35" stroke="{INK}" stroke-width="1.6"/>'
                     f'<circle cx="{x + w - 22}" cy="{yy + 11}" r="3.4" fill="{glow if (i + k) % 3 else "#7CF08A"}"/>')
    return ''.join(o)


def wordmark(cx, cy, name, icon='spark', col='#FFFFFF', size=72, sub=None):
    """Generic company mark: a simple geometric icon + the name in hand caps. Never a real logo."""
    ic = {'spark': ''.join(f'<path d="M0 0 L{34 * math.cos(a):.0f} {34 * math.sin(a):.0f}" stroke="{col}" stroke-width="9" stroke-linecap="round"/>' for a in [i * math.pi / 4 for i in range(8)]),
          'ring': f'<circle r="28" fill="none" stroke="{col}" stroke-width="10"/>',
          'tri': f'<path d="M0 -32 L30 24 H-30 Z" fill="{col}"/>',
          'block': f'<rect x="-28" y="-28" width="56" height="56" rx="10" fill="{col}"/>'}.get(icon, '')
    tw_ = tw(name, size, 'caps')
    return (f'<g transform="translate({cx - tw_ / 2 - 30} {cy})">{ic}</g>' + caps(cx + 30, cy + 4, name, size, col)
            + (caps(cx, cy + size * .9, sub, size * .36, col) if sub else ''))


def jag_split(x, col='#111', w=26):
    """Lightning-shaped divider for two-sided phone calls / arguments (vertical, at x)."""
    pts = []
    y, k = -20, 0
    while y < H() + 40:
        pts.append((x + (w if k % 2 else -w), y)); y += 70; k += 1
    left = ' '.join(f'{px - 9:.0f},{py}' for px, py in pts)
    right = ' '.join(f'{px + 9:.0f},{py}' for px, py in reversed(pts))
    return f'<polygon points="{left} {right}" fill="{col}"/>'


def panel(x, y, w, h, inner, bg='#E6DCC6'):
    """Clipped comic panel (phone-call rows, split screens). inner uses frame coordinates."""
    cid = uid('p')
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'
            f'<g clip-path="url(#{cid})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>{inner}</g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-width="5"/>')
