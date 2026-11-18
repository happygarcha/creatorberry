"""Vector art for the Zapzapper Dark Files test: locked characters (Reed, Morgan), props and sets, in the series' flat 4px-outline style.
Characters are authored at unscaled size (ground y=0, height ~250) and are assembled/animated as articulated rigs by zz_anim.js."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools', 'engine'))
import cc_kit as K
from cc_kit import INK, LW, HEAD_C, HEAD_R, BODY, face, _hair, SKIN, _shade_clip

EXPRS = ['neutral', 'determined', 'worried', 'surprised', 'shocked', 'smug', 'happy']
CHARS = {
    'reed':   dict(name='Detective Daniel Reed', skin='peach', coat=('#7A5438', '#5E3F2A'), shirt='#EDEAE2', hair='side', hair_col='#2A211C', glasses=True, trousers='#1E1F26', tie='#3A3F55'),
    'morgan': dict(name='Detective Morgan', skin='tan', coat=('#56709C', '#42587F'), shirt='#EDEAE2', hair='swoop', hair_col='#1B1A1D', glasses=False, trousers='#1E1F26', tie=None),
}


def torso_art(c):
    d = CHARS[c]; su, sh = d['coat']
    o = [_shade_clip(f'<path d="{BODY}"/>', '<ellipse cx="52" cy="-100" rx="34" ry="70"/>', su, sh)]
    o.append(f'<path d="M-13 -151 L0 -116 L13 -151 Z" fill="{d["shirt"]}" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>')
    if d['tie']: o.append(f'<path d="M-4 -148 L4 -148 L6 -126 L0 -116 L-6 -126 Z" fill="{d["tie"]}" stroke="{INK}" stroke-width="2"/>')
    o.append(f'<path d="M-16 -151 L-2 -110 M16 -151 L2 -110" stroke="{INK}" stroke-width="2.2" fill="none"/>')
    # coat details: centre seam + buttons; pocket flap (the wrench handle sticks out of it)
    o.append(f'<path d="M0 -112 L0 -52" stroke="{INK}" stroke-width="2.2" fill="none"/><circle cx="-7" cy="-96" r="2.6" fill="{INK}"/><circle cx="-7" cy="-78" r="2.6" fill="{INK}"/>')
    o.append(f'<path d="M12 -92 L34 -92 L34 -78 L12 -78 Z" fill="{sh}" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>')
    return ''.join(o)


def head_art(c):
    d = CHARS[c]; sk, skh = SKIN[d['skin']]
    head = f'<circle cx="0" cy="{HEAD_C}" r="{HEAD_R}"/>'
    base = _shade_clip(head, f'<ellipse cx="{HEAD_R * .95:.0f}" cy="{HEAD_C + 6}" rx="{HEAD_R * .62:.0f}" ry="{HEAD_R * 1.25:.0f}"/>', sk, skh)
    hair = _hair(d['hair'], d['hair_col'], None)
    return base, hair


def faces(c):
    return {e: face(e, 0, glasses=False) for e in EXPRS}


def glasses_art():
    ey = HEAD_C - 2; lx, rx = -14, 14
    ln = f'stroke="{INK}" stroke-width="3.2" stroke-linecap="round" fill="none"'
    return (f'<circle cx="{lx}" cy="{ey}" r="11" fill="rgba(255,255,255,.16)" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{rx}" cy="{ey}" r="11" fill="rgba(255,255,255,.16)" stroke="{INK}" stroke-width="3"/><path d="M{lx + 11} {ey} H{rx - 11}" {ln}/>'
            f'<path d="M{lx - 11} {ey} L{lx - 20} {ey - 2} M{rx + 11} {ey} L{rx + 20} {ey - 2}" {ln}/>')


def char_defs():
    out = {}
    for c, d in CHARS.items():
        base, hair = head_art(c)
        out[c] = dict(torso=torso_art(c), headbase=base, hair=hair, faces=faces(c), glasses=glasses_art() if d['glasses'] else '',
                      skin=SKIN[d['skin']][0], coat=d['coat'][0], coat_dark=d['coat'][1], trousers=d['trousers'])
    return out


def static_svg(c, w=420, h=420):
    """Front-facing model-sheet SVG of one character (an editable asset; the animated rig uses the same parts)."""
    d = char_defs()[c]; cd = CHARS[c]
    legs = (f'<path d="M-9 -62 L-12 0 M9 -62 L12 0" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>'
            f'<path d="M-9 -62 L-12 0 M9 -62 L12 0" stroke="{d["trousers"]}" stroke-width="6.4" stroke-linecap="round"/>')
    shoes = f'<ellipse cx="-12" cy="-1" rx="11" ry="5" fill="{INK}"/><ellipse cx="12" cy="-1" rx="11" ry="5" fill="{INK}"/>'
    arms = ''.join(f'<path d="M{s * 32} -136 L{s * 40} -88 L{s * 36} -44" stroke="{INK}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
                   f'<path d="M{s * 32} -136 L{s * 40} -88 L{s * 36} -44" stroke="{d["coat"]}" stroke-width="6.4" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
                   f'<circle cx="{s * 36}" cy="-42" r="6.5" fill="{d["skin"]}" stroke="{INK}" stroke-width="2.6"/>' for s in (-1, 1))
    head = d['headbase'] + d['hair'] + d['faces']['neutral'] + d['glasses']
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-110 -270 220 290" width="{w}" height="{h}"><rect x="-110" y="-270" width="220" height="290" fill="#1d2330"/>'
            f'<ellipse cx="0" cy="2" rx="46" ry="9" fill="#000" opacity=".3"/>{legs}{shoes}<g>{d["torso"]}</g>{arms}{head}</svg>')


if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, 'assets', 'svg'), exist_ok=True)
    for c in CHARS:
        open(os.path.join(HERE, 'assets', 'svg', f'{c}_model.svg'), 'w').write(static_svg(c))
    print('ok')
