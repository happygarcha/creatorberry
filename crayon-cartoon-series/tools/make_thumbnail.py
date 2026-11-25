"""make_thumbnail.py <episode_dir> "LINE 1|LINE 2|LINE 3" [bg=red] [char=GUY] [pose=shocked] -> <episode_dir>/final/PRIMARY_THUMBNAIL_1080x1920.png
One primary thumbnail per video: big hand-lettered hook on a library background with the lead character reacting."""
import os, sys, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools')); sys.path.insert(0, os.path.join(ROOT, 'tools', 'engine'))
import animlib
animlib.set_format('9:16')
from episode_tools import *
import cast, bg as BG, props
from cc_kit import fill_bg, frame_svg, cash
import cc_kit
ep_dir = os.path.abspath(sys.argv[1]); lines = sys.argv[2].split('|')
bgname = sys.argv[3] if len(sys.argv) > 3 else 'red'; ch = sys.argv[4] if len(sys.argv) > 4 else 'GUY'; pose = sys.argv[5] if len(sys.argv) > 5 else 'shocked'
cx = W() / 2
o = BG.flat(bgname, floor=False) + cc_kit.burst(cx, H() * .66, W() * .6, '#F7D35C', 16)
import random; r = random.Random(7)
decor = sys.argv[6] if len(sys.argv) > 6 else 'cash'
for i in range(16 if decor == 'cash' else (7 if decor == 'envelopes' else 5)):
    if decor == 'envelopes': o += props.envelope(r.uniform(60, W() - 60), r.uniform(H() * .40, H() * .64), r.uniform(.9, 1.5)) if False else ''
    if decor == 'node': o += props.ocean_node(r.uniform(80, W() - 80), r.uniform(H() * .46, H() * .6), r.uniform(.45, .8), 200) if i < 3 else ''
    elif decor == 'planes': o += props.plane(r.uniform(80, W() - 80), r.uniform(H() * .42, H() * .62), r.uniform(.45, .7), flip=bool(i % 2))
    elif decor == 'envelopes': o += props.envelope(r.uniform(60, W() - 60), r.uniform(H() * .42, H() * .66), r.uniform(.9, 1.5)) + props.spinner(0, 0, 1) * 0
    else: o += cash(r.uniform(40, W() - 40), r.uniform(H() * .08, H() * .6), r.uniform(.7, 1.1), r.uniform(-60, 60))
sizes = [118, 150, 118]
for i, ln in enumerate(lines):
    o += caps(cx, S(.13) + i * 118, ln, sizes[min(i, 2)] if len(lines) > 1 else 130, '#FFFFFF' if i != 1 else YELLOW, stroke='#161616', sw=14, rot=-3)
o += cast.char(ch, cx, S(.93), 2.9, pose)
html = page([scene(0, 2, frame_svg(o, 'thumbnail'))], animlib.local_fonts(FONTS, cc_kit.FONT_SPECS))
open('/tmp/_thumb.html', 'w').write(html)
subprocess.run(['python3', os.path.join(ROOT, 'tools', 'engine', 'render.py'), '/tmp/_thumb.html', '/tmp/_thumb', '--stills', '1'], check=True)
os.makedirs(os.path.join(ep_dir, 'final'), exist_ok=True)
import glob; os.replace(glob.glob('/tmp/_thumb_*.png')[0], os.path.join(ep_dir, 'final', 'PRIMARY_THUMBNAIL_1080x1920.png')); print('thumbnail written')
