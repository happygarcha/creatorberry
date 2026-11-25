"""Flat background library (muted red, mustard, dusty blue, cream) with a simple floor band. All SVG, all frame-sized."""
import os, sys
ENGINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'engine')
if ENGINE not in sys.path: sys.path.insert(0, ENGINE)
from cc_kit import W, H, INK, fill_bg

PALETTE = {'red': ('#B8524A', '#9A4039'), 'mustard': ('#E0B24A', '#C4962F'), 'blue': ('#7C9AB5', '#627F9B'), 'cream': ('#F3E3BC', '#D9C48F'), 'ocean': ('#8FB6CC', '#3F7899'), 'navy': ('#3C5F7D', '#2B4660')}
FLOOR_Y = .62   # fraction of the frame height where characters stand (inside the Shorts safe area)


def flat(name, floor=True, y=None):
    """Plain coloured wall + darker floor band; the floor line sits at FLOOR_Y of the frame."""
    wall, floor_c = PALETTE[name]
    y = (y if y is not None else FLOOR_Y) * H()
    o = fill_bg(wall)
    if floor:
        o += (f'<rect x="-200" y="{y - 6}" width="{W() + 400}" height="{H() - y + 16}" fill="{floor_c}"/>'
              f'<path d="M-200 {y - 6} H{W() + 200}" stroke="{INK}" stroke-width="4"/>')
    return o


def dots(name, seed=1, n=26):
    """Optional subtle texture: a few hand-drawn plus signs / dots on the wall."""
    import random
    r = random.Random(seed); wall = PALETTE[name][1]
    return ''.join(f'<circle cx="{r.uniform(0, W()):.0f}" cy="{r.uniform(0, H() * .5):.0f}" r="{r.uniform(3, 7):.1f}" fill="{wall}" opacity=".55"/>' for _ in range(n))
