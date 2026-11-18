"""Assemble zz.html (page + art + data + animation). Output page is rendered by tools/engine/render.py (Chromium, deterministic renderAt(t))."""
import os, sys, json, re, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import zz_art, zz_sets
from cc_kit import INK

LINE_T = {'n1a': .5, 'n1b': 4.5, 'r1': 11.3, 'm1': 17.3, 'n2': 23.6, 'm2': 36.4, 'r2': 45.4, 'n3': 47.9, 'g1': 55.0}
WHO_LABEL = {'NARRATOR': None, 'REED': 'REED:', 'MORGAN': 'MORGAN:', 'LILY': "GIRL'S VOICE:"}
WHO_COL = {'REED': '#F2C14E', 'MORGAN': '#7FC8F8', 'LILY': '#F29BB0'}
script = json.load(open(os.path.join(HERE, 'script.json')))
dur = json.load(open(os.path.join(HERE, 'audio', 'durations.json')))


def env(wavp):
    x, sr = sf.read(wavp); x = np.abs(x if x.ndim == 1 else x.mean(1)); n = int(len(x) / sr * 30) + 1
    e = np.array([np.sqrt(np.mean(x[int(i / 30 * sr):int((i + 1) / 30 * sr) + 1] ** 2)) for i in range(n)])
    k = np.convolve(e, np.ones(3) / 3, 'same'); k = k / (np.percentile(k, 95) + 1e-9)
    return [round(float(v), 3) for v in np.clip(k, 0, 1.2)]


lines, caps = [], []
for l in script:
    t0 = LINE_T[l['id']]; d = dur[l['id']]
    lines.append({'id': l['id'], 'who': l['who'], 't0': t0, 'dur': d, 'env': env(os.path.join(HERE, 'audio', l['id'] + '.wav'))})
    txt = l['text']; sents = [s.strip() for s in re.findall(r'[^.?!]+[.?!…]*', txt) if s.strip()]
    tot = sum(len(s) for s in sents); c = 0.0
    for s in sents:
        a = t0 + d * (c / tot); c += len(s); b = t0 + d * (c / tot)
        disp = s.upper().replace('…', '...')
        if l['who'] == 'LILY': disp = '"' + disp + '"'
        elif l['who'] in ('REED', 'MORGAN'): disp = '"' + disp + '"'
        caps.append({'t0': round(a - .05, 3), 't1': round(b + .45 if s is sents[-1] else b + .02, 3), 'text': disp, 'label': WHO_LABEL[l['who']] or '', 'col': WHO_COL.get(l['who'], '#fff'), 'who': l['who']})
for i in range(len(caps) - 1):      # no overlaps
    if caps[i]['t1'] > caps[i + 1]['t0']: caps[i]['t1'] = round(caps[i + 1]['t0'] - .001, 3)
json.dump(caps, open(os.path.join(HERE, 'subtitles', 'caps.json'), 'w'), indent=1)

io = zz_sets.interior_objects()
Zdata = {'chars': zz_art.char_defs(), 'lines': lines, 'caps': caps,
         'art': {'basement': zz_sets.basement(), 'interior': zz_sets.interior(), 'iobj': io, 'shelf': zz_sets.shelf(), 'bolt': zz_sets.bolt(),
                 'flash': zz_sets.flashlight(), 'wrench': zz_sets.wrench(), 'rec': zz_sets.recorder()}}
fonts = ''
FR = os.path.abspath(os.path.join(HERE, '..', 'assets', 'fonts'))
fonts = (f"@font-face{{font-family:'Patrick Hand SC';src:url(file://{FR}/node_modules/@fontsource/patrick-hand-sc/files/patrick-hand-sc-latin-400-normal.woff2)}}")
js = open(os.path.join(HERE, 'zz_anim.js')).read()
patch = lambda id, cx, cy, rx, ry: f'<ellipse id="{id}" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000" opacity="0" filter="url(#bl3)"/>'
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{fonts}
html,body{{margin:0;background:#000}} #stage{{position:relative;width:1280px;height:720px;overflow:hidden;background:#05070b}}
svg{{display:block}} .cap{{font-family:'Patrick Hand SC',cursive;paint-order:stroke;stroke:#000;stroke-width:7;stroke-linejoin:round}}</style></head>
<body data-fw="1280" data-fh="720"><div id="stage"><svg id="sv" xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<defs>
<filter id="bl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="bl2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="bl3" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="22"/></filter>
<mask id="dm" maskUnits="userSpaceOnUse" x="-900" y="-400" width="5600" height="1500"><rect x="-900" y="-400" width="5600" height="1500" fill="#fff"/>
<polygon id="mb1" fill="#000" filter="url(#bl)"/><polygon id="mb2" fill="#000" filter="url(#bl)"/>
{patch('p_desk', 3765, 500, 150, 90)}{patch('p_gear', 3560, 400, 120, 100)}{patch('p_box', 3380, 480, 110, 100)}{patch('p_hand', 3722, 450, 70, 50)}{patch('p_rec', 3850, 436, 60, 70)}</mask>
<clipPath id="bclip"><polygon id="cb1"/><polygon id="cb2"/></clipPath>
</defs>
<g id="cam"><g id="world"></g></g>
<g id="capsg"></g>
<rect id="xblack" x="0" y="0" width="1280" height="720" fill="#000" opacity="0"/>
<rect id="blackout" x="0" y="0" width="1280" height="720" fill="#000" opacity="1"/>
</svg></div>
<script>window.ZZ={json.dumps(Zdata)};</script><script>{js}</script></body></html>'''
open(os.path.join(HERE, 'zz.html'), 'w').write(html)
print('zz.html', len(html) // 1024, 'KB; caps', len(caps))
