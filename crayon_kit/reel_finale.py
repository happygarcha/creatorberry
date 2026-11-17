"""Reel Part 4, the finale (9:16): what changed after 2008.
  python3 reel_finale.py script -> script4.json ; timeline.py tts script4.json vo4 ; reel_finale.py build ; render ; reel_finale.py sound
Facts (via web research): Fed cut target to 0-0.25% on Dec 16, 2008; Dodd-Frank signed July 21, 2010 and created four agencies
(CFPB, FSOC, OFR, FIO); Fed emergency lending only through programs broadly available, not to a single firm (Federal Reserve History);
partial rollback in 2018 (Economic Growth, Regulatory Relief, and Consumer Protection Act)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from animlib import set_format, page, scene, G
cmd = sys.argv[1]
set_format('9:16')
from cc_kit import *
from cc_shots import *
SCRIPT = {"voices": {"N": 16, "banker": 11, "home": 18, "host": 17}, "gap": [0.3, 0.6], "shots": [
    {"id": "hook", "vo": [{"text": "How do you stop another 2008? You change the rules."}]},
    {"id": "fed", "vo": [{"text": "First, in December 2008, the Fed cut interest rates to almost zero."}]},
    {"id": "qe", "vo": [{"text": "Then it started buying bonds to push borrowing costs even lower. It's called quantitative easing."}]},
    {"id": "law", "vo": [{"text": "In July 2010, Congress passed a giant law called Dodd Frank.", "say": "In July twenty ten, Congress passed a giant law called Dod Frank."}]},
    {"id": "agencies", "vo": [{"text": "It created four new watchdog groups, including one to protect people who borrow money."}]},
    {"id": "ask", "vo": [{"text": "Can the Fed just rescue my bank?", "who": "banker"}]},
    {"id": "rule", "vo": [{"text": "Not anymore. Emergency help can't go to just one firm."}]},
    {"id": "aside", "vo": [{"text": "Of course, some of it was rolled back.", "who": "host"}]},
    {"id": "ease", "vo": [{"text": "In 2018, Congress loosened parts of the law."}]},
    {"id": "card", "vo": [{"text": "Safer? People still argue."}]},
    {"id": "cta", "vo": [{"text": "That's the full story of 2008. Follow for more money stories.", "who": "host"}], "tail": .6},
]}
if cmd == 'script':
    json.dump(SCRIPT, open(os.path.join(HERE, 'script4.json'), 'w'), indent=1); sys.exit(print('wrote script4.json'))
if cmd == 'sound':
    from sfx_cc import *
    c = json.load(open(os.path.join(HERE, 'cues4.json')))
    n = int(c['total'] * SR) + SR
    f = np.zeros((n, 2))
    for name, t, gain in c['fx']: place(f, fx(name), t, gain)
    mix(os.path.join(HERE, 'vo4.wav'), f, bed(c['total'] + 1, c['music'], c['dips'])[:n], os.path.join(HERE, 'final4.wav'))
    sys.exit(print('wrote final4.wav'))
TL = json.load(open(os.path.join(HERE, 'vo4.json')))
sh = {s['id']: s for s in TL['shots']}
BANKER = dict(skin='white', suit='grey', hat='top', hat_col='#1D1E21', moustache='black')
MASCOT = dict(skin='tan', suit=('#8B5A3C', '#6F452C'), shirt='#F7F7F5', tie=None, lapels=False, hair='side', hair_col='black', moustache='black')
S = []
S.append(t_news(sh['hook'], 'NEW WALL STREET RULES', 'July 21, 2010', word='rules'))
S.append(t_stat(sh['fed'], '0 - 0.25%', 'FED TARGET RATE, DEC 2008', word='almost', col=RED))
S.append(t_compare(sh['qe'], ('THE FED', '#5E6B78', 'buying'), ('BUYS BONDS', GREEN, 'lower'), 'QUANTITATIVE EASING', label_col=INK))
S.append(t_news(sh['law'], 'DODD-FRANK SIGNED INTO LAW', 'July 2010', word='law'))
S.append(t_panels(sh['agencies'], [('CFPB', dict(suit='navy', expr='happy')), ('FSOC', dict(suit='grey', expr='smug')),
                                   ('OFR', dict(suit='brown', expr='happy')), ('FIO', dict(suit='teal', expr='smug'))], phone=False))
S.append(t_close(sh['ask'], dict(BANKER, expr='worried'), 'Can the Fed just\nrescue my bank?'))
S.append(t_close(sh['rule'], dict(MASCOT, expr='smug'), "Not anymore. Help can't\ngo to just one firm.", voiced=False, bg=info_bg()))
S.append(t_close(sh['aside'], dict(MASCOT, expr='smug'), 'Of course, some of it\nwas rolled back.', bg=info_bg()))
S.append(t_news(sh['ease'], 'CONGRESS EASES SOME RULES', '2018', word='loosened'))
S.append(t_card(sh['card'], 'Safer?\nPeople still argue.'))
S.append(t_close(sh['cta'], dict(MASCOT, expr='grin'), "That's the full story\nof 2008. Follow for more\nmoney stories.", bg=info_bg()))
out = os.path.join(HERE, 'reel4.html')
open(out, 'w').write(page(S, fonts_head(os.path.expanduser('~/fonts'))))
tot = TL['total']
json.dump({'total': tot, 'fx': CUES,
           'music': [[0, sh['law']['start'], 'tense'], [sh['law']['start'], sh['card']['start'], 'warm'], [sh['card']['start'], tot, 'triumph']],
           'dips': [[sh['card']['start'], sh['card']['end'], .4]]}, open(os.path.join(HERE, 'cues4.json'), 'w'), indent=1)
print(f'wrote {out}  total {tot:.2f}s  shots {len(S)}')
