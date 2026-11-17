import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from animlib import set_format, page, scene
set_format('9:16')
from cc_kit import *
from cc_shots import *
HOME = dict(skin='tan', suit='blue', hair='curly', hair_col='dark', tie=None, lapels=False)
cx = W() / 2
o = [fill_bg('#2F3D5C'), burst(cx, H() * .7, W() * .55, '#3A4B70', 16),
     caps(cx, H() * .12, 'BANKS:', 110, '#FFFFFF'), caps(cx, H() * .22, 'SAVED', 150, '#5CC26B'),
     caps(cx, H() * .33, 'HOMEOWNERS:', 100, '#FFFFFF'), caps(cx, H() * .43, '???', 170, '#F7D35C'),
     person(cx, feet_for(H() * .76, 2.6), 2.6, expr='worried', **HOME)]
open(os.path.join(HERE, 'thumb_homeowners.html'), 'w').write(page([scene(0, 2, frame_svg(''.join(o), 'thumb'))], fonts_head(os.path.expanduser('~/fonts'))))
