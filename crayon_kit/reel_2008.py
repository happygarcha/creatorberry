"""Reel (9:16, ~60 s): the 2008 financial crisis, explained like you're 5.
  python3 reel_2008.py script
  python3 timeline.py tts script.json vo
  python3 reel_2008.py build            # -> reel.html + cues.json
  python3 render.py $PWD/reel.html reel_v.mp4 0 <total>
  python3 reel_2008.py sound            # -> final.wav
Facts used (Federal Reserve History / St. Louis Fed): subprime mortgage credit expansion; Lehman filed for
Chapter 11 on Sept 15, 2008, the largest in US history, with more than $600 billion of debt."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from animlib import set_format, page, scene, G
cmd = sys.argv[1]
set_format('9:16')
from cc_kit import *
from cc_shots import *

SCRIPT = {"voices": {"N": 16, "banker": 11, "home": 18}, "gap": [0.3, 0.6], "shots": [
    {"id": "hook", "vo": [{"text": "In 2008, a giant bank collapsed."}]},
    {"id": "stat", "vo": [{"text": "It owed over $600 billion."}]},
    {"id": "spot", "vo": [{"text": "So how did ordinary home loans bring down the world?"}]},
    {"id": "place", "vo": [{"text": "It started in America, around 2003."}], "min": 2.2},
    {"id": "lend", "vo": [{"text": "Banks gave mortgages to almost anyone."}]},
    {"id": "bank", "vo": [{"text": "No job? No savings? No problem.", "who": "banker"}]},
    {"id": "home", "vo": [{"text": "Great! I'll take the big house.", "who": "home"}]},
    {"id": "bundle", "vo": [{"text": "Then the banks bundled those loans, and sold them as safe investments."}]},
    {"id": "fall", "vo": [{"text": "But house prices fell, and people stopped paying."}]},
    {"id": "panic", "vo": [{"text": "Nobody knew who held the bad loans, so nobody would lend to anybody."}], "tail": .3},
    {"id": "lehman", "vo": [{"text": "On September 15, Lehman Brothers went bankrupt. The largest bankruptcy in American history.", "say": "On September fifteenth, Lee man Brothers went bankrupt. The largest bankruptcy in American history."}]},
    {"id": "card", "vo": [{"text": "It was a very big problem."}]},
    {"id": "cta", "vo": [{"text": "Follow for part two: the bailout."}], "tail": .6},
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
# Cast (model sheet): fixed looks reused in every shot
BANKER = dict(skin='white', suit='grey', hat='top', hat_col='#1D1E21', moustache='black')
HOME = dict(skin='tan', suit='blue', hair='curly', hair_col='dark', tie=None, lapels=False)

S = []
S.append(t_news(sh['hook'], 'GIANT BANK COLLAPSES', 'September 15, 2008', word='collapsed'))
S.append(t_stat(sh['stat'], '$600 BILLION', 'OWED', word='600', col=RED))
S.append(t_spot(sh['spot'], dict(BANKER, expr='smug', arms='hold'), label='THE BANKER'))
d = sh['place']['end'] - sh['place']['start']
gy = H() * .7
walkers = G(extra(W() * .25, gy, 1.2, 'white', 'brown', walk=(0, d)), [[0, {'tx': -40}], [d, {'tx': 120}, 'l']])
S.append(t_place(sh['place'], street('#B9AE9B', '#E9C79A', seed=3) + walkers, 'America, 2003.'))
S.append(t_two(sh['lend'], dict(BANKER, expr='grin', arms='present'), dict(HOME, expr='happy'), 'a', 'Sign here!', voiced=False))
S.append(t_ots(sh['bank'], dict(BANKER, expr='smug'), dict(HOME), 'No job? No savings?\nNo problem.'))
S.append(t_close(sh['home'], dict(HOME, expr='happy'), "Great! I'll take\nthe big house."))
S.append(t_compare(sh['bundle'], ('RISKY LOANS', '#5E6B78', 'loans'), ('"SAFE" BONDS', GREEN, 'safe'), 'RATED AAA'))
S.append(t_close(sh['fall'], dict(HOME, expr='worried'), "I can't pay.", voiced=False))
S.append(t_panels(sh['panic'], [('BANK A', dict(suit='navy', expr='worried')), ('BANK B', dict(suit='brown', hat='fedora', expr='shocked')),
                                ('BANK C', dict(suit='black', hat='top', expr='worried')), ('BANK D', dict(suit='grey', expr='shocked'))]))
S.append(t_news(sh['lehman'], 'LEHMAN BROTHERS FILES FOR BANKRUPTCY', 'largest in American history', word='largest'))
S.append(t_card(sh['card'], 'It was a very\nbig problem.'))
S.append(t_stat(sh['cta'], 'PART 2', 'THE BAILOUT', word='part', col=GREEN))

out = os.path.join(HERE, 'reel.html')
open(out, 'w').write(page(S, fonts_head(os.path.expanduser('~/fonts'))))
tot = TL['total']
json.dump({'total': tot, 'fx': CUES,
           'music': [[0, sh['place']['start'], 'mystery'], [sh['place']['start'], sh['bundle']['start'], 'warm'],
                     [sh['bundle']['start'], sh['card']['start'], 'tense'], [sh['card']['start'], tot, 'mystery']],
           'dips': [[sh['card']['start'], sh['card']['end'], .4]]},
          open(os.path.join(HERE, 'cues.json'), 'w'), indent=1)
print(f'wrote {out}  total {tot:.2f}s  shots {len(S)}')
