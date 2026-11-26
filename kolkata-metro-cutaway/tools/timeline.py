"""Narration starts + Hindi subtitle cues -> timeline.json (the one file the picture, the mix and the subtitles read)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, '..')
L = json.load(open(os.path.join(P, 'voice', 'lines.json'))); D = json.load(open(os.path.join(P, 'voice', 'dur.json')))
GAP = {'v1': 1.0, 'v2': 1.0, 'v3': 1.0, 'v4': 1.0, 'v5': 1.1, 'v6': 1.0}
START = {}; t = 0.8
for l in L:
    START[l['id']] = round(t, 3); t += D[l['id']] + GAP.get(l['id'], 0)
END = round(START['v7'] + D['v7'] + 2.4, 2)
subs = []
import re
for l in L:
    t0 = START[l['id']]; dur = D[l['id']]
    parts = [p.strip() for p in re.findall(r'[^।!?,]+[।!?,]?', l['text']) if p.strip()]
    # merge short fragments so each cue is readable (>= 22 chars) and at most about 60 chars
    cues = []; cur = ''
    for p in parts:
        if cur and len(cur) + len(p) > 58: cues.append(cur); cur = p
        else: cur = (cur + ' ' + p).strip()
        if len(cur) >= 22 and cur[-1] in '।!?': cues.append(cur); cur = ''
    if cur: cues.append(cur)
    tot = sum(len(c) for c in cues); a = t0
    for c in cues:
        w = dur * len(c) / tot; subs.append({'id': l['id'], 't0': round(a - 0.03, 3), 't1': round(a + w + 0.12, 3), 'hi': c}); a += w
for i in range(len(subs) - 1):
    if subs[i]['t1'] > subs[i + 1]['t0'] - 0.03: subs[i]['t1'] = round(subs[i + 1]['t0'] - 0.03, 3)
json.dump({'end': END, 'vo': START, 'dur': D, 'subs': subs}, open(os.path.join(P, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
print(START, END)
for s in subs: print(f"{s['t0']:6.2f}-{s['t1']:6.2f}  {s['hi']}")
