"""Reel Part 3 (9:16): what happened to the homeowners after 2008.
  python3 reel_homeowners.py script -> script3.json ; python3 timeline.py tts script3.json vo3
  python3 reel_homeowners.py build -> reel3.html + cues3.json ; render.py ... ; reel_homeowners.py sound -> final3.wav
Facts (via web research; see notes in the delivery message):
- ~5.8 million households received a first notice of default 2007-2010 (NBER paper); foreclosure starts peaked in 2009 (Chicago Fed Letter).
- US home prices fell more than 25% from the peak by late 2008 (UCLA Anderson brief); 'underwater' = owing more than the home is worth.
- HAMP modifications began April 2009; nearly 1.4 million permanent HAMP modifications through March 2014 (Treasury housing scorecards).
- Case-Shiller showed home values back to mid-2004 levels in early 2014 (Treasury/HUD Feb 2014 scorecard)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from animlib import set_format, page, scene, G
cmd = sys.argv[1]
set_format('9:16')
from cc_kit import *
from cc_shots import *
SCRIPT = {"voices": {"N": 16, "banker": 11, "home": 18, "host": 17}, "gap": [0.3, 0.6], "shots": [
    {"id": "hook", "vo": [{"text": "The banks got a bailout. So what did the homeowners get?"}]},
    {"id": "stat", "vo": [{"text": "Between 2007 and 2010, about five point eight million households got a default notice."}]},
    {"id": "fall", "vo": [{"text": "At the same time, home prices fell more than 25 percent from their peak."}]},
    {"id": "own", "vo": [{"text": "I owe more than my house is worth?!", "who": "home"}]},
    {"id": "under", "vo": [{"text": "Yes. That's called being underwater.", "who": "banker"}]},
    {"id": "peak", "vo": [{"text": "Foreclosures peaked in 2009."}]},
    {"id": "aside", "vo": [{"text": "Banks first. Homeowners later.", "who": "host"}]},
    {"id": "hamp", "vo": [{"text": "In 2009, the government launched a program to help homeowners lower their payments."}]},
    {"id": "mods", "vo": [{"text": "By 2014, it had permanently changed about one point four million loans."}]},
    {"id": "back", "vo": [{"text": "And it took until 2014 for home values to climb back to where they were in 2004."}]},
    {"id": "card", "vo": [{"text": "Banks were rescued in weeks. Homeowners recovered over years."}]},
    {"id": "cta", "vo": [{"text": "Follow for more money stories.", "who": "host"}], "tail": .6},
]}
if cmd == 'script':
    json.dump(SCRIPT, open(os.path.join(HERE, 'script3.json'), 'w'), indent=1); sys.exit(print('wrote script3.json'))
if cmd == 'sound':
    from sfx_cc import *
    c = json.load(open(os.path.join(HERE, 'cues3.json')))
    n = int(c['total'] * SR) + SR
    f = np.zeros((n, 2))
    for name, t, gain in c['fx']: place(f, fx(name), t, gain)
    mix(os.path.join(HERE, 'vo3.wav'), f, bed(c['total'] + 1, c['music'], c['dips'])[:n], os.path.join(HERE, 'final3.wav'))
    sys.exit(print('wrote final3.wav'))
TL = json.load(open(os.path.join(HERE, 'vo3.json')))
sh = {s['id']: s for s in TL['shots']}
BANKER = dict(skin='white', suit='grey', hat='top', hat_col='#1D1E21', moustache='black')
HOME = dict(skin='tan', suit='blue', hair='curly', hair_col='dark', tie=None, lapels=False)
MASCOT = dict(skin='tan', suit=('#8B5A3C', '#6F452C'), shirt='#F7F7F5', tie=None, lapels=False, hair='side', hair_col='black', moustache='black')
S = []
S.append(t_close(sh['hook'], dict(HOME, expr='worried'), 'What did the\nhomeowners get?', voiced=False))
S.append(t_stat(sh['stat'], '5.8 MILLION', 'DEFAULT NOTICES, 2007-2010', word='five', col=RED))
S.append(t_compare(sh['fall'], ('HOME PRICES', '#5E6B78', 'prices'), ('DOWN 25%+', RED, 'twenty'), 'FROM THE PEAK', label_col=INK))
S.append(t_close(sh['own'], dict(HOME, expr='shocked'), 'I owe more than my\nhouse is worth?!'))
S.append(t_ots(sh['under'], dict(BANKER, expr='smug'), dict(HOME), "Yes. That's called\nbeing underwater."))
S.append(t_stat(sh['peak'], 'FORECLOSURES', 'PEAKED IN 2009', word='peaked', col=RED, bg=fill_bg('#3A3D44')))
S.append(t_close(sh['aside'], dict(MASCOT, expr='smug'), 'Banks first.\nHomeowners later.', bg=info_bg()))
S.append(t_news(sh['hamp'], 'GOVERNMENT LAUNCHES HOMEOWNER HELP PLAN', '2009', word='launched'))
S.append(t_stat(sh['mods'], '1.4 MILLION', 'LOANS PERMANENTLY MODIFIED BY 2014', word='one', col=GREEN))
S.append(t_compare(sh['back'], ('HOME VALUES, 2014', GREEN, 'climb'), ('= HOME VALUES, 2004', '#5E6B78', 'were'), 'TEN YEARS BACK', label_col=INK))
S.append(t_card(sh['card'], 'Banks were rescued in weeks.\nHomeowners recovered\nover years.'))
S.append(t_close(sh['cta'], dict(MASCOT, expr='grin'), 'Follow for more\nmoney stories.', bg=info_bg()))
out = os.path.join(HERE, 'reel3.html')
open(out, 'w').write(page(S, fonts_head(os.path.expanduser('~/fonts'))))
tot = TL['total']
json.dump({'total': tot, 'fx': CUES,
           'music': [[0, sh['hamp']['start'], 'tense'], [sh['hamp']['start'], sh['card']['start'], 'warm'], [sh['card']['start'], tot, 'mystery']],
           'dips': [[sh['card']['start'], sh['card']['end'], .4]]}, open(os.path.join(HERE, 'cues3.json'), 'w'), indent=1)
print(f'wrote {out}  total {tot:.2f}s  shots {len(S)}')
