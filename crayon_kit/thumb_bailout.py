"""Primary thumbnail, Part 2 (9:16). python3 thumb_bailout.py -> thumb_bailout.html ; render.py ... --stills 1"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from animlib import set_format, page, scene
set_format('9:16')
from cc_kit import *
from cc_shots import *
MASCOT = dict(skin='tan', suit=('#8B5A3C', '#6F452C'), shirt='#F7F7F5', tie=None, lapels=False, hair='side', hair_col='black', moustache='black')
cx = W() / 2
o = [fill_bg('#F7D35C'), burst(cx, H() * .66, W() * .55, '#F2BE2E', 16),
     caps(cx, H() * .12, 'THE $700 BILLION', 82, INK), caps(cx, H() * .22, 'BAILOUT', 150, '#C0392F'),
     caps(cx, H() * .30, 'WHO PAID?', 96, INK),
     person(cx, feet_for(H() * .70, 3.0), 3.0, expr='shocked', **MASCOT)]
open(os.path.join(HERE, 'thumb_bailout.html'), 'w').write(page([scene(0, 2, frame_svg(''.join(o), 'thumb'))], fonts_head(os.path.expanduser('~/fonts'))))
