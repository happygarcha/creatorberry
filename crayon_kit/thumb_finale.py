import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from animlib import set_format, page, scene
set_format('9:16')
from cc_kit import *
from cc_shots import *
MASCOT = dict(skin='tan', suit=('#8B5A3C', '#6F452C'), shirt='#F7F7F5', tie=None, lapels=False, hair='side', hair_col='black', moustache='black')
cx = W() / 2
o = [fill_bg('#2E7D4F'), burst(cx, H() * .7, W() * .55, '#3C9462', 16),
     caps(cx, H() * .12, 'WHAT CHANGED', 108, '#FFFFFF'), caps(cx, H() * .23, 'AFTER', 108, '#FFFFFF'), caps(cx, H() * .35, '2008?', 190, '#F7D35C'),
     person(cx, feet_for(H() * .74, 2.8), 2.8, expr='smug', arms='present', **MASCOT)]
open(os.path.join(HERE, 'thumb_finale.html'), 'w').write(page([scene(0, 2, frame_svg(''.join(o), 'thumb'))], fonts_head(os.path.expanduser('~/fonts'))))
