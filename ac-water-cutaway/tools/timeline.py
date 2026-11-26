"""Narration starts + subtitle cues -> timeline.json (the one file the picture, the mix and the subtitles read)."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, '..')
START = {'v1': 0.8, 'v2': 5.4, 'v3': 14.5, 'v4': 22.8, 'v5': 34.4, 'v6': 39.3, 'v7': 50.4, 'v8': 60.9}
W = json.load(open(os.path.join(P, 'voice', 'words.json'))); D = json.load(open(os.path.join(P, 'voice', 'dur.json')))
subs = []
for vid, t0 in START.items():
    words = W[vid]; cur = []
    def flush():
        global cur
        if not cur: return
        txt = ' '.join(w[0] for w in cur).replace('Legion airs', 'Legionnaires'); a = t0 + max(0, cur[0][1]); b = t0 + cur[-1][2]
        subs.append({'id': vid, 't0': round(a - 0.05, 3), 't1': round(max(b + 0.5, a + 1.8), 3), 'en': txt}); cur = []
    for w in words:
        cur.append(w); n = sum(len(x[0]) + 1 for x in cur)
        if w[0][-1] in '.?!' or (w[0][-1] == ',' and n > 62): flush()
    flush()
for i in range(len(subs) - 1):                 # never overlap the next cue
    if subs[i]['t1'] > subs[i + 1]['t0'] - 0.03: subs[i]['t1'] = round(subs[i + 1]['t0'] - 0.03, 3)
TEXT = ["That clear water dripping from your air conditioner? Don't drink it.", "It is condensation.",
 "Warm, humid room air touches the cold coil, the moisture turns into drops, and they run into a pan and out the pipe.",
 "The same coil also pulls moisture out of your air, so the room gets dry,", "and dry air can irritate your skin, eyes and throat.",
 "In a closed bedroom, many room air conditioners just recirculate the air, so carbon dioxide builds up overnight.",
 "Studies link that to less deep sleep.", "Let some fresh air in.",
 "Now the catch. On its way out, the water touches the coil, the pan and the pipe.",
 "Germs can build up there, including, in some systems, the bacteria behind Legionnaires disease.",
 "Parts can also add metals like copper, and lead from solder.", "So drain it, or water your plants. Don't drink it.", "Like, share and subscribe for more explainers."]
assert len(TEXT) == len(subs), (len(TEXT), len(subs))
for s_, t_ in zip(subs, TEXT): s_['en'] = t_
json.dump({'end': 65.0, 'vo': START, 'dur': D, 'subs': subs}, open(os.path.join(P, 'timeline.json'), 'w'), indent=1)
for s in subs: print(f"{s['t0']:6.2f}-{s['t1']:6.2f}  {s['en']}")
