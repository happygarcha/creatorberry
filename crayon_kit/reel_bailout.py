"""Reel Part 2 (9:16): the 2008 bailout, explained like you're 5.
  python3 reel_bailout.py script            -> script2.json
  python3 timeline.py tts script2.json vo2
  python3 reel_bailout.py build             -> reel2.html + cues2.json
  python3 render.py $PWD/reel2.html reel2_v.mp4 0 <total>
  python3 reel_bailout.py sound             -> final2.wav
Facts (sources: NPR/ABC/CNN market coverage 2008-09-29; Congressional Research Service R41427; Yale New Bagehot):
House rejected the plan 228-205 on Sept 29, 2008; the Dow closed down 777.68 points (largest one-day point drop at the time);
Congress passed the Emergency Economic Stabilization Act on Oct 3, 2008, authorizing up to $700 billion (TARP);
the Treasury bought ownership stakes in banks; most banks later repaid."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from animlib import set_format, page, scene, G
cmd = sys.argv[1]
set_format('9:16')
from cc_kit import *
from cc_shots import *

SCRIPT = {"voices": {"N": 16, "banker": 11, "home": 18, "host": 17}, "gap": [0.3, 0.6], "shots": [
    {"id": "hook", "vo": [{"text": "After the crash, America had a choice: let the banks fail, or save them."}]},
    {"id": "stat", "vo": [{"text": "The plan: up to $700 billion."}]},
    {"id": "place", "vo": [{"text": "First, it had to pass Congress."}], "min": 2.0},
    {"id": "vote", "vo": [{"text": "On September 29, 2008, the House voted no. Two hundred twenty eight to two hundred five."}]},
    {"id": "dow", "vo": [{"text": "The stock market panicked, and fell nearly 800 points in one day. A record at the time."}]},
    {"id": "aside", "vo": [{"text": "Plot twist: they said no first.", "who": "host"}]},
    {"id": "law", "vo": [{"text": "Days later, Congress changed its mind. The bailout became law on October 3."}]},
    {"id": "ask", "vo": [{"text": "We need seven hundred billion. Please.", "who": "banker"}]},
    {"id": "tax", "vo": [{"text": "With my money?!", "who": "home"}]},
    {"id": "swap", "vo": [{"text": "The government put money into banks, and got ownership shares in return."}]},
    {"id": "back", "vo": [{"text": "Most of that money was paid back."}]},
    {"id": "card", "vo": [{"text": "Was it fair? People still argue."}]},
    {"id": "cta", "vo": [{"text": "Follow for more money stories.", "who": "host"}], "tail": .6},
]}
if cmd == 'script':
    json.dump(SCRIPT, open(os.path.join(HERE, 'script2.json'), 'w'), indent=1); sys.exit(print('wrote script2.json'))

if cmd == 'sound':
    from sfx_cc import *
    c = json.load(open(os.path.join(HERE, 'cues2.json')))
    n = int(c['total'] * SR) + SR
    f = np.zeros((n, 2))
    for name, t, gain in c['fx']: place(f, fx(name), t, gain)
    mix(os.path.join(HERE, 'vo2.wav'), f, bed(c['total'] + 1, c['music'], c['dips'])[:n], os.path.join(HERE, 'final2.wav'))
    sys.exit(print('wrote final2.wav'))

TL = json.load(open(os.path.join(HERE, 'vo2.json')))
sh = {s['id']: s for s in TL['shots']}
BANKER = dict(skin='white', suit='grey', hat='top', hat_col='#1D1E21', moustache='black')
HOME = dict(skin='tan', suit='blue', hair='curly', hair_col='dark', tie=None, lapels=False)
MASCOT = dict(skin='tan', suit=('#8B5A3C', '#6F452C'), shirt='#F7F7F5', tie=None, lapels=False, hair='side', hair_col='black', moustache='black')

S = []
S.append(t_news(sh['hook'], 'GOVERNMENT BAILS OUT BANKS', 'October 3, 2008', word='save'))
S.append(t_stat(sh['stat'], '$700 BILLION', 'BAILOUT PLAN', word='700', col=RED))
d = sh['place']['end'] - sh['place']['start']
S.append(t_place(sh['place'], street('#B9AE9B', '#E9C79A', seed=7), 'Washington, 2008.'))
S.append(t_stat(sh['vote'], 'NO: 228 TO 205', 'HOUSE VOTE, SEPT 29', word='two', col=RED))
S.append(t_stat(sh['dow'], 'DOW: -777', 'BIGGEST ONE-DAY POINT DROP AT THE TIME', word='fell', col=RED, bg=fill_bg('#3A3D44')))
S.append(t_close(sh['aside'], dict(MASCOT, expr='smug'), 'Plot twist:\nthey said no first.', bg=info_bg()))
S.append(t_news(sh['law'], 'BAILOUT SIGNED INTO LAW', 'October 3, 2008', word='law'))
S.append(t_ots(sh['ask'], dict(BANKER, expr='worried'), dict(HOME), 'We need seven hundred\nbillion. Please.'))
S.append(t_close(sh['tax'], dict(HOME, expr='shocked'), 'With my money?!'))
S.append(t_compare(sh['swap'], ('TAXPAYER MONEY', GREEN, 'money'), ('BANK SHARES', '#5E6B78', 'shares'), 'OWNERSHIP STAKE', label_col=INK))
S.append(t_stat(sh['back'], 'MOST REPAID', 'BANKS PAID IT BACK', word='paid', col=GREEN))
S.append(t_card(sh['card'], 'Was it fair?\nPeople still argue.'))
S.append(t_close(sh['cta'], dict(MASCOT, expr='grin'), 'Follow for more\nmoney stories.', bg=info_bg()))

out = os.path.join(HERE, 'reel2.html')
open(out, 'w').write(page(S, fonts_head(os.path.expanduser('~/fonts'))))
tot = TL['total']
json.dump({'total': tot, 'fx': CUES,
           'music': [[0, sh['place']['start'], 'tense'], [sh['place']['start'], sh['law']['start'], 'mystery'],
                     [sh['law']['start'], sh['card']['start'], 'warm'], [sh['card']['start'], tot, 'mystery']],
           'dips': [[sh['card']['start'], sh['card']['end'], .4]]},
          open(os.path.join(HERE, 'cues2.json'), 'w'), indent=1)
print(f'wrote {out}  total {tot:.2f}s  shots {len(S)}')
