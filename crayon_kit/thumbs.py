"""Thumbnails for the 2008 crisis Reel. python3 thumbs.py 9:16|16:9 -> thumbs_<fmt>.html (3 designs, stills at 1,3,5 s)
  python3 render.py $PWD/thumbs_916.html th916 --stills 1,3,5"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from animlib import set_format, page, scene, G
fmt = sys.argv[1]
set_format(fmt)
from cc_kit import *
from cc_shots import *
Vt = W() < H()
BANKER = dict(skin='white', suit='grey', hat='top', hat_col='#1D1E21', moustache='black')
HOME = dict(skin='tan', suit='blue', hair='curly', hair_col='dark', tie=None, lapels=False)
MASCOT = dict(skin='tan', suit=('#8B5A3C', '#6F452C'), shirt='#F7F7F5', tie=None, lapels=False, hair='side', hair_col='black', moustache='black')
cx, cy = W() / 2, H() / 2
YEL = '#F7D35C'

def sc(i, inner, label): return scene(i * 2, i * 2 + 2, frame_svg(inner, label))

S = []
# A: newspaper + shocked mascot + huge year
nw, nh = (W() - 140, 520) if Vt else (700, 400)
A = [fill_bg('#C0392F'), burst(cx, cy, W() * (.8 if Vt else .5), '#D95A4E', 18)]
if Vt:
    A += [newspaper(cx, H() * .3, nw, nh, 'GIANT BANK\nCOLLAPSES', 'September 15, 2008', rot=-4),
          caps(cx, H() * .6, '2008', 170, YEL), caps(cx, H() * .68, 'THE CRASH', 90, '#FFFFFF'),
          person(cx, H() * 1.0, 1.3, expr='shocked', arms='up', **MASCOT)]
else:
    A += [newspaper(cx - 330, cy, nw, nh, 'GIANT BANK\nCOLLAPSES', 'September 15, 2008', rot=-4),
          caps(cx + 280, cy - 170, '2008', 200, YEL), caps(cx + 280, cy - 60, 'THE CRASH', 100, '#FFFFFF'),
          person(cx + 300, H() * 1.02, 1.5, expr='shocked', arms='up', **MASCOT)]
S.append(sc(0, ''.join(A), 'A'))
# B: big mascot face, question text
B = [fill_bg(YEL), burst(cx if Vt else cx + 380, H() * (.64 if Vt else .5), W() * (.55 if Vt else .26), '#F2BE2E', 16)]
if Vt:
    B += [caps(cx, H() * .12, 'WHAT REALLY', 92, INK), caps(cx, H() * .2, 'CAUSED THE', 92, INK), caps(cx, H() * .29, '2008 CRASH?', 100, '#C0392F'),
          caps(cx, H() * .36, "EXPLAINED LIKE YOU'RE 5", 50, INK),
          person(cx, feet_for(H() * .68, 3.0), 3.0, expr='surprised', **MASCOT)]
else:
    B += [caps(cx - 330, cy - 120, 'WHAT REALLY', 112, INK), caps(cx - 330, cy - 10, 'CAUSED THE', 112, INK), caps(cx - 330, cy + 110, '2008 CRASH?', 124, '#C0392F'),
          caps(cx - 330, cy + 230, "EXPLAINED LIKE YOU'RE 5", 44, INK),
          person(cx + 380, feet_for(cy - 20, 2.6), 2.6, expr='surprised', **MASCOT)]
S.append(sc(1, ''.join(B), 'B'))
# C: banker + homeowner, "No problem."
C = [info_bg()]
if Vt:
    C += [person(W() * .27, H() * .86, 1.9, expr='smug', arms='present', **BANKER), person(W() * .76, H() * .86, 1.9, expr='happy', **HOME),
          caps(cx, H() * .1, 'NO JOB?', 110, INK), caps(cx, H() * .19, 'NO SAVINGS?', 110, INK), caps(cx, H() * .30, 'NO PROBLEM.', 112, '#C0392F')]
else:
    C += [person(W() * .09, H() * 1.04, 1.4, expr='smug', arms='present', **BANKER), person(W() * .91, H() * 1.04, 1.4, expr='happy', **HOME),
          caps(cx, cy - 130, 'NO JOB? NO SAVINGS?', 100, INK), caps(cx, cy + 20, 'NO PROBLEM.', 140, '#C0392F')]
S.append(sc(2, ''.join(C), 'C'))
out = os.path.join(HERE, 'thumbs_' + fmt.replace(':', '') + '.html')
open(out, 'w').write(page(S, fonts_head(os.path.expanduser('~/fonts'))))
print('wrote', out)
