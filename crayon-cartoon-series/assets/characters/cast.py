"""Permanent character library for the series. Every episode imports this; never redefine a look inside a scene.

Characters (fixed model sheet; same proportions because they all come from engine person()):
  GUY    the Everyday Guy  - round head, short black hair, small black moustache, brown shirt, thin black limbs.
  BANKER the Banker        - round white face, black moustache, black top hat, grey suit, red tie.
  FRIEND the Friend        - round face, curly dark-brown hair, blue shirt.
  (NARRATOR is voice-only: see voices.json)

Library
  EXPRESSIONS  neutral happy grin smug sad worried angry surprised shocked crying determined closed
  POSES        standing walking running pointing talking shocked confused laughing angry thinking holding
  char()       one figure in a fixed pose/expression
  acting()     a figure that changes pose/expression over time (stacked layers shown one at a time)
Animation of position (walk across, hop, shake) is done by wrapping the result in animlib.G(..., keys, o=(x, y))."""
import os, sys
ENGINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'engine')
if ENGINE not in sys.path: sys.path.insert(0, ENGINE)
import animlib
from animlib import G
from cc_kit import person, extra

# ---------------------------------------------------------------- model sheet (locked)
CAST = {
    'GUY':    dict(skin='tan', suit=('#8B5A3C', '#6F452C'), shirt='#F7F7F5', tie=None, lapels=False,
                   hair='side', hair_col='black', moustache='black'),
    'BANKER': dict(skin='white', suit='grey', hat='top', hat_col='#1D1E21', moustache='black'),     # default red tie
    'FRIEND': dict(skin='tan', suit='blue', hair='curly', hair_col='dark', tie=None, lapels=False),
}
EXPRESSIONS = ['neutral', 'happy', 'grin', 'smug', 'sad', 'worried', 'angry', 'surprised', 'shocked', 'crying', 'determined', 'closed']

# pose name -> person() kwargs (arms/stance/expression defaults; any can be overridden per call)
POSES = {
    'standing':  dict(arms='down', expr='neutral'),
    'walking':   dict(arms='down', expr='happy'),
    'running':   dict(arms='up', expr='shocked'),
    'pointing':  dict(arms='point_r', expr='determined'),
    'talking':   dict(arms='present', expr='happy'),
    'shocked':   dict(arms='up', expr='shocked'),
    'confused':  dict(arms='shrug', expr='worried'),
    'laughing':  dict(arms='hips', expr='grin'),
    'angry':     dict(arms='hips', expr='angry'),
    'thinking':  dict(arms='chin', expr='worried'),
    'holding':   dict(arms='hold', expr='neutral'),
}


def look(name): return dict(CAST[name])


def char(name, x, y, s=1.0, pose='standing', expr=None, talk=None, walk=None, flip=False, extras='', **kw):
    """One figure. (x, y) = feet on the ground. talk=(t0, t1) flaps the mouth; walk=(t0, t1) scissors the legs."""
    p = dict(POSES[pose]); p.update(look(name))
    if expr: p['expr'] = expr
    p.update(kw)
    return person(x, y, s, talk=talk, walk=walk, flip=flip, extras=extras, **p)


def acting(name, x, y, s, steps, t_end=None, **kw):
    """steps = [(t0, {pose=..., expr=..., talk=(a, b), walk=(a, b)}), ...] sorted by time; one layer is visible at a time.
    Position/size animation: wrap the result in G(..., keys, o=(x, y))."""
    out = []
    for i, (t0, spec) in enumerate(steps):
        t1 = steps[i + 1][0] if i + 1 < len(steps) else t_end
        spec = dict(spec); sp = dict(kw); sp.update(spec)
        pose = sp.pop('pose', 'standing')
        fig = char(name, x, y, s, pose, **sp)
        if len(steps) == 1: out.append(fig); continue
        keys = []
        if i > 0: keys += [[t0 - .001, {'o': 0}], [t0, {'o': 1}, 'h']]
        else: keys += [[0, {'o': 1}]]
        if t1 is not None: keys += [[t1 - .001, {'o': 1}], [t1, {'o': 0}, 'h']]
        out.append(G(fig, keys))
    return ''.join(out)


def crowd_member(x, y, s=1.0, suit='maroon', hat=None, expr='happy', arms='down', walk=None, flip=False, tone='white'):
    """Anonymous background figure (white face + costume cue). Not a recurring character."""
    return extra(x, y, s, tone, suit, hat=hat, expr=expr, flip=flip, arms=arms, walk=walk)
