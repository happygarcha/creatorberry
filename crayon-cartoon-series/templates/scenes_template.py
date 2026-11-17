"""Scene animation for a new episode. Copy to episodes/episode-NN/scenes/scenes.py.
Every sN(c) returns (world_svg, camera_keys, camera_origin, overlay_svg). Timing comes from the TTS timeline: c.w('word') = local
time of a spoken word, c.talk(who, i) = (t0, t1) of a line, c.mouth(who, i) = lip-sync windows, c.d = scene length.
Characters ONLY via cast.char()/acting() (never person()); backgrounds via bg.flat(); props via props.*"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from episode_tools import *
import cast, props, bg
from cast import acting, char
from cc_kit import money_bag, cash, burst, fill_bg
FY = S(FLOOR)


class C:
    def __init__(s, sc, sh, cue): s.sc, s.sh, s.cue = sc, sh, cue; s.d = sh['end'] - sh['start']
    def w(s, word, which='start'): return word_time(s.sh, word, which)
    def talk(s, who, i=0): return talks_of(s.sh, who, s.sc)[i]
    def mouth(s, who, i=0): return mouth_windows(s.sh, who, s.sc, i)


def s1(c):
    guy = acting('GUY', W() / 2, FY, 1.6, [(0, dict(pose='standing', expr='worried')), (c.w('keyword'), dict(pose='shocked', expr='shocked'))], t_end=c.d)
    world = bg.flat('red') + guy
    cam = [[0, {'s': 1.0}], [c.d, {'s': 1.06}, 'l']]
    over = headline(c.sc['headline']['text'], resolve_at(c.sh, c.sc['headline']['at']), 70)
    return world, cam, (W() / 2, FY - 200), over


BUILDERS = {'S1': s1}
