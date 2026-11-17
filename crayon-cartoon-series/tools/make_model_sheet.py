"""Renders the permanent model sheets (poses for each character + the expression library) to assets/characters/*.png"""
import os, sys, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'engine'))
import animlib
animlib.set_format('16:9')
from episode_tools import *
import cast
from cc_kit import fill_bg, frame_svg
import cc_kit
OUT = os.path.join(ROOT, 'assets', 'characters')
POSES = list(cast.POSES)
pages = []
def sheet(name, cells, title, sc=.78):
    o = fill_bg('#F3E3BC') + caps(640, 44, title, 40, '#161616')
    cols = 6
    for i, (label, svg) in enumerate(cells):
        r, c = divmod(i, cols); x = 120 + c * 208; y = 300 + r * 300
        o += svg(x, y, sc) + caps(x, y + 34, label.upper(), 20, '#161616')
    pages.append((name, scene(len(pages) * 2, len(pages) * 2 + 2, frame_svg(o, title))))
for ch, title in (('GUY', 'THE EVERYDAY GUY'), ('BANKER', 'THE BANKER'), ('FRIEND', 'THE FRIEND')):
    sheet(f'model_sheet_{ch.lower()}_poses', [(p, (lambda x, y, s, p=p, ch=ch: cast.char(ch, x, y, s, p))) for p in POSES], f'{title}: POSES (locked model sheet)')
sheet('model_sheet_expressions', [(e, (lambda x, y, s, e=e: cast.char('GUY', x, y, s, 'standing', expr=e))) for e in cast.EXPRESSIONS], 'EXPRESSION LIBRARY (shown on the Everyday Guy; same set for every character)')
html = page([s for _, s in pages], animlib.local_fonts(FONTS, cc_kit.FONT_SPECS))
open('/tmp/_sheets.html', 'w').write(html)
ts = ','.join(str(i * 2 + 1) for i in range(len(pages)))
subprocess.run(['python3', os.path.join(ROOT, 'tools', 'engine', 'render.py'), '/tmp/_sheets.html', '/tmp/_sheet', '--stills', ts], check=True)
for i, (n, _) in enumerate(pages): os.replace(f'/tmp/_sheet_{i * 2 + 1:07.2f}.png', os.path.join(OUT, n + '.png'))
print('wrote', [n for n, _ in pages])
