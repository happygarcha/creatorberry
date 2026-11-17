"""Worked example, ~36 s, 16:9 or 9:16 from the same script:
logo montage -> newspaper -> spotlight intro -> chapter card -> place reveal -> silent bubble gag ->
voiced skit (close-up + over-the-shoulder) -> typed card -> comparison infographic -> phone panels.
  python3 cc_example.py script            # writes script.json
  python3 timeline.py tts script.json vo  # scratch voices -> vo.wav + vo.json (the timing)
  python3 cc_example.py build 16:9        # or 9:16 -> example.html + cues.json
  python3 render.py $PWD/example.html ex.mp4 0 <total printed by build>
  python3 cc_example.py sound             # final.wav (VO + bed + SFX, -14 LUFS)
  ffmpeg -i ex.mp4 -i final.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest example.mp4"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from animlib import set_format, page, scene, G
cmd = sys.argv[1]
set_format(sys.argv[2] if len(sys.argv) > 2 else '16:9')
from cc_kit import *
from cc_shots import *

SCRIPT = {"voices": {"N": 16, "kid": 18, "dad": 11}, "gap": [0.35, 0.75], "shots": [
    {"id": "hook", "vo": [{"text": "This is Nova Labs."}], "tail": .4},
    {"id": "news", "vo": [{"text": "Next month, it goes public at a $2 trillion valuation."}]},
    {"id": "spot", "vo": [{"text": "But ten years ago, it was one kid with a laptop."}]},
    {"id": "chap", "min": 2.0},
    {"id": "city", "vo": [{"text": "Pune, 2014."}], "min": 2.6},
    {"id": "home", "vo": [{"text": "His father had exactly one plan for him."}, {"text": "Engineering."}]},
    {"id": "kid", "vo": [{"text": "I'm going to build a robot that does my homework.", "who": "kid"}]},
    {"id": "dad", "vo": [{"text": "Then it can also do the dishes.", "who": "dad"}]},
    {"id": "card", "vo": [{"text": "It did neither."}]},
    {"id": "info", "vo": [{"text": "His first server cost $50."}, {"text": "Today, the company is worth two trillion."}]},
    {"id": "phones", "vo": [{"text": "And suddenly, everybody wanted to talk to him."}], "tail": 1.0},
]}
if cmd == 'script':
    json.dump(SCRIPT, open(os.path.join(HERE, 'script.json'), 'w'), indent=1); sys.exit(print('wrote script.json'))

if cmd == 'sound':
    from sfx_cc import *
    c = json.load(open(os.path.join(HERE, 'cues.json')))
    n = int(c['total'] * SR) + SR
    f = np.zeros((n, 2))
    for name, t, gain in c['fx']: place(f, fx(name), t, gain)
    mix(os.path.join(HERE, 'vo.wav'), f, bed(c['total'] + 1, c['music'], c['dips'])[:n], os.path.join(HERE, 'final.wav'))
    sys.exit(print('wrote final.wav'))

TL = json.load(open(os.path.join(HERE, 'vo.json')))
sh = {s['id']: s for s in TL['shots']}
# The cast: fixed looks, reused in every shot (model sheet)
KID = dict(skin='brown', suit='blue', hair='swoop', hair_col='black', tie=None, lapels=False)
DAD = dict(skin='brown', suit='grey', hair='bald', hair_col='black', moustache='black', glasses=True)
FOUNDER = dict(skin='brown', suit='hoodie', hair='swoop', hair_col='black', tie=None, lapels=False)
WIDE = W() > H()

S = []
cx, cy, R = W() / 2, H() / 2, min(W(), H())
S.append(t_logo(sh['hook'], 'NOVA LABS', 'spark', montage=[globe(cx, cy, R * .36), fill_bg('#2B2F36') + server_racks(cx - 280, H() * .9, 5, H() * .7),
                                                            street(seed=5), fill_bg('#5A3C2A') + bookshelf(-20, -20, W() + 40, H() + 40, 9)]))
S.append(t_news(sh['news'], 'NOVA LABS GOING PUBLIC', 'targeting a $2 trillion valuation', word='$2'))
S.append(t_spot(sh['spot'], dict(FOUNDER, expr='determined', arms='hold', extras=laptop(0, -84, .55, back=True))))
S.append(t_card(sh['chap'], 'The Making of a Founder', title=True))
d = sh['city']['end'] - sh['city']['start']
gy = H() * (.95 if WIDE else .7)
walkers = (G(extra(W() * .2, gy, .9, 'white', 'brown', walk=(0, d)), [[0, {'tx': -80}], [d, {'tx': 120}, 'l']]) +
           G(extra(W() * .78, gy + 10, 1.0, 'white', 'navy', hat='fedora', flip=True, walk=(.2, d)), [[0, {'tx': 60}], [d, {'tx': -140}, 'l']]))
S.append(t_place(sh['city'], street('#B9AE9B', '#E9C79A', seed=11) + walkers, 'Pune, 2014.'))
S.append(t_two(sh['home'], dict(DAD, expr='smug', arms='point_r'), dict(KID, expr='worried'), 'a', 'Engineering.\nFinal answer.', voiced=False, sb=1.1 if WIDE else 1.25))
S.append(t_close(sh['kid'], dict(KID, expr='happy'), "I'm going to build a robot\nthat does my homework." if WIDE else "I'm going to build\na robot that does\nmy homework."))
S.append(t_ots(sh['dad'], dict(DAD, expr='smug'), dict(KID), 'Then it can also do the dishes.' if WIDE else 'Then it can also\ndo the dishes.'))
S.append(t_card(sh['card'], 'It did neither.'))
S.append(t_compare(sh['info'], ('$50', '#5E6B78', '$50'), ('$2 TRILLION', GREEN, 'two'), '40 BILLION X'))
S.append(t_panels(sh['phones'], [('INVESTOR', dict(suit='navy', expr='grin')), ('REPORTER', dict(suit='brown', hat='fedora', expr='surprised')),
                                 ('BANKER', dict(suit='black', hat='top', expr='grin')), ('RIVAL CEO', dict(suit='grey', expr='surprised'))]))

out = os.path.join(HERE, 'example.html')
open(out, 'w').write(page(S, fonts_head(os.path.expanduser('~/fonts'))))
tot = TL['total']
json.dump({'total': tot, 'fx': CUES, 'music': [[0, sh['chap']['start'], 'mystery'], [sh['chap']['end'], tot, 'warm']],
           'dips': [[sh['chap']['start'], sh['chap']['end'], .25], [sh['card']['start'], sh['card']['end'], .4]]},
          open(os.path.join(HERE, 'cues.json'), 'w'), indent=1)
print(f'wrote {out}  total {tot:.2f}s  shots {len(S)}')
