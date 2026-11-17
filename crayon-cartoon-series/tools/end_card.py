"""The standard animated end card (final 6-7 s of EVERY episode; appended automatically by episode_tools.with_end_card).
Mustard background, three established characters, big LIKE / SHARE / SUBSCRIBE rows, 'FOR MORE FUN EXPLANATIONS!' headline.
Guy presses LIKE, Friend points at SHARE, Banker presses the red SUBSCRIBE button, the bell rings, everyone reacts.
Timing comes from the narrator's spoken words (like / share / subscribe / crazy). No next-episode title (optional teasers belong
in the episode body and must never replace this card)."""
from episode_tools import *
import cast, bg
from cast import acting
from cc_kit import text, SCRIPT_B, INK, burst, cash
from animlib import fade, wiggle, bob


def icon_like(x, y, s=1.0, fill='#FFFFFF'):
    return (f'<g transform="translate({x} {y}) scale({s}) translate(-52 -52)"><path d="M8 46 H30 V94 H8 Z" fill="{fill}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M34 94 V48 L50 12 Q62 6 64 20 L58 40 H90 Q102 42 99 54 L92 84 Q90 94 78 94 Z" fill="{fill}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></g>')


def icon_share(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s}) translate(-52 -52)"><path d="M82 22 L26 52 L82 82" fill="none" stroke="{INK}" stroke-width="6"/>'
            + ''.join(f'<circle cx="{cx}" cy="{cy}" r="15" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>' for cx, cy in ((82, 22), (26, 52), (82, 82))) + '</g>')


def icon_bell(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 -26 C-20 -26 -27 -6 -27 12 L-34 26 H34 L27 12 C27 -6 20 -26 0 -26 Z" fill="#FFD54A" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
            f'<circle cy="34" r="7" fill="#FFD54A" stroke="{INK}" stroke-width="4"/><circle cy="-30" r="5" fill="#FFD54A" stroke="{INK}" stroke-width="3.5"/></g>')


def build(c):
    d = c.d
    tl, ts, tsub, tcr = c.w('like'), c.w('share'), c.w('subscribe'), c.w('crazy')
    t_for = c.w('for')
    R1, R2, R3 = S(.285), S(.475), S(.665)
    cxp, s = 98, .78                     # characters at the left, icons right
    ix, tx = 268, 330
    fy = lambda R: R + 100
    # --- icons + words (pop on the spoken word)
    like_w = G(icon_like(ix, R1, 1.2) + text(tx, R1 + 2, 'LIKE', 100, SCRIPT_B, '#FFFFFF', 'start', stroke=INK, sw=14), pop(tl - .05, .34, .4), (ix, R1))
    like_pressed = G(icon_like(ix, R1, 1.2, '#4DA3FF'), [[0, {'o': 0}], [tl - .001, {'o': 0}], [tl + .05, {'o': 1}]])
    like_bounce = G(like_w + like_pressed, merge([[tl, {'s': 1.0}], [tl + .06, {'s': .82}, 'o'], [tl + .26, {'s': 1.18}, 'b'], [tl + .5, {'s': 1.0}, 'io']]), (ix, R1))
    share_w = G(icon_share(ix, R2, 1.2) + text(tx, R2 + 2, 'SHARE', 100, SCRIPT_B, '#FFFFFF', 'start', stroke=INK, sw=14), pop(ts - .05, .34, .4), (ix, R2))
    share_w = G(share_w, wiggle(ts + .1, ts + 1.0, 7, .3), (ix, R2))
    pill = (f'<rect x="196" y="{R3 - 46}" width="370" height="92" rx="46" fill="#E0382C" stroke="{INK}" stroke-width="6"/>'
            + text(381, R3 + 2, 'SUBSCRIBE', 60, SCRIPT_B, '#FFFFFF'))
    pill = G(pill, merge(pop(tsub - .05, .34, .4), [[tsub + .0, {'ty': 0}], [tsub + .08, {'ty': 8}, 'o'], [tsub + .3, {'ty': 0}, 'io']]), (381, R3))
    bell = G(G(icon_bell(604, R3, 1.1), wiggle(tsub + .3, tsub + 2.2, 20, .26), (604, R3 - 22)), pop(tsub + .15, .3, .4), (604, R3))
    title = G(caps(W() / 2, S(.152), 'FOR MORE FUN', 68, INK, rot=-2) + caps(W() / 2, S(.198), 'EXPLANATIONS!', 68, '#8A1F1A', rot=-2), slam(t_for), (W() / 2, S(.175)))
    # --- characters: point/press, then react
    def hop_react(t0, amp, period, seed):
        return merge(bob(t0, d - .2, amp, period, 'ty'), [[d - .2, {'ty': 0}]])
    guy = acting('GUY', cxp, fy(R1), s, [(0, dict(pose='standing', expr='happy')), (tl - .45, dict(pose='pointing', expr='determined')),
                                         (tl + .55, dict(pose='shocked', expr='grin')), (tcr, dict(pose='laughing', expr='grin'))], t_end=d)
    friend = acting('FRIEND', cxp, fy(R2), s, [(0, dict(pose='standing', expr='happy')), (ts - .45, dict(pose='pointing', expr='happy')),
                                               (tsub + .1, dict(pose='confused', expr='surprised')), (tcr, dict(pose='shocked', expr='grin'))], t_end=d)
    banker = acting('BANKER', cxp, fy(R3), s, [(0, dict(pose='standing', expr='smug')), (tsub - .45, dict(pose='pointing', expr='determined')),
                                              (tsub + .35, dict(pose='shocked', expr='shocked')), (tcr, dict(pose='laughing', expr='grin'))], t_end=d)
    guy = G(guy, hop_react(tcr, 16, .5, 1), (cxp, fy(R1)))
    friend = G(friend, hop_react(tcr + .1, 18, .46, 2), (cxp, fy(R2)))
    banker = G(banker, merge(hop_react(tcr + .2, 14, .54, 3), wiggle(tsub + .4, tsub + 1.4, 6, .22)), (cxp, fy(R3)))
    # --- confetti banknotes on the punchline
    pops = ''.join(G(burst(x, y, 62, '#FFF3B0', 10), [[0, {'o': 0, 's': .3}], [t - .001, {'o': 0, 's': .3}], [t, {'o': 1, 's': .6}, 'h'], [t + .2, {'o': 1, 's': 1.2}, 'o'], [t + .45, {'o': 0, 's': 1.3}, 'i']], (x, y))
                   for x, y, t in ((ix, R1, tl), (ix + 20, R2, ts), (604, R3, tsub + .1)))
    world = bg.flat('mustard', floor=False) + pops + title + like_bounce + share_w + pill + bell + guy + friend + banker
    return world, [[0, {'s': 1.0}], [d, {'s': 1.0}, 'l']], (W() / 2, S(.45)), ''
