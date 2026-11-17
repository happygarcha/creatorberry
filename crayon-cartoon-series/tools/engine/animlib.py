"""Keyframe presets, camera moves, shot wrapper and page assembly. Times are seconds LOCAL to the shot.
Call set_format('16:9') or set_format('9:16') before building anything."""
import json, os

FW, FH = 1280, 720   # logical canvas; render.py captures at 1.5x -> 1920x1080 or 1080x1920


def set_format(fmt):
    global FW, FH
    FW, FH = (1280, 720) if fmt == '16:9' else (720, 1280)
    return FW, FH


def J(k): return json.dumps(k, separators=(',', ':')).replace("'", '&#39;')


def A(html, keys, o=None, wb=None):
    """Full-frame HTML wrapper with a keyframe track; children use frame coordinates."""
    at = f" data-kf='{J(keys)}'" + (f' data-o="{o[0]} {o[1]}"' if o else '') + (f' data-wb="{" ".join(map(str, wb))}"' if wb else '')
    return f'<div class="a"{at} style="position:absolute;left:0;top:0;width:{FW}px;height:{FH}px;pointer-events:none">{html}</div>'


def G(inner, keys, o=None):
    """SVG <g> with a keyframe track (origin in viewBox px)."""
    return f"<g data-kf='{J(keys)}'" + (f' data-o="{o[0]} {o[1]}"' if o else '') + f'>{inner}</g>'


# ---- element presets
def pop(t, d=.28, s0=.6): return [[t, {'o': 0, 's': s0}], [t + .04, {'o': 1}], [t + d, {'s': 1}, 'b']]
def appear(t): return [[t - .001, {'o': 0}], [t, {'o': 1}, 'h']]          # hard on (dialogue lines, labels)
def vanish(t): return [[t - .001, {'o': 1}], [t, {'o': 0}, 'h']]
def fade(t, d=.25): return [[t, {'o': 0}], [t + d, {'o': 1}]]
def fout(t, d=.2): return [[t, {'o': 1}], [t + d, {'o': 0}]]
def wipe(t, d=.35): return [[t, {'wipe': 0}], [t + d, {'wipe': 1}, 'o']]
def slide(t, dx=0, dy=0, d=.32): return [[t, {'tx': dx, 'ty': dy, 'o': 0}], [t + .03, {'o': 1}], [t + d, {'tx': 0, 'ty': 0}, 'o']]
def draw(t, d=.4): return [[t, {'draw': 0}], [t + d, {'draw': 1}, 'o']]
def typewrite(t0, t1): return [[t0, {'chars': 0}], [t1, {'chars': 1}, 'l']]
def type_cps(t0, text, cps=22): return typewrite(t0, t0 + max(.15, len(text) / cps))
def count(t0, t1, v0, v1, e='o'): return [[t0, {'count': v0}], [t1, {'count': v1}, e]]
def slam(t, s0=1.8): return [[t, {'o': 0, 's': s0}], [t + .12, {'o': 1, 's': .95}, 'i'], [t + .22, {'s': 1}, 'o']]
def shake(t, amp=6, d=.24):
    return [[t, {'tx': 0}]] + [[t + d * (i + 1) / 5, {'tx': v}, 'l'] for i, v in enumerate([amp, -amp * .8, amp * .5, -amp * .3, 0])]
def bob(t0, t1, amp=4, period=.5, p='ty'):
    k, t, up = [[t0, {p: 0}]], t0, True
    while t < t1:
        t += period / 2; k.append([round(t, 3), {p: -amp if up else 0}, 'io']); up = not up
    return k
def wiggle(t0, t1, amp=4, period=.3, p='r'):
    k, t, s = [[t0, {p: 0}]], t0, 1
    while t < t1:
        t += period / 2; k.append([round(t, 3), {p: amp * s}, 'io']); s = -s
    return k + [[t + period / 2, {p: 0}, 'io']]
def flicker(t0, t1, period=.24, on_first=True):
    """Alternate visibility (mouth flap: give the open mouth flicker(), the closed mouth flicker(on_first=False))."""
    k, t, on = [[t0 - .001, {'o': 0 if on_first else 1}]], t0, on_first
    while t < t1:
        k.append([round(t, 3), {'o': 1 if on else 0}, 'h']); t += period / 2; on = not on
    return k + [[round(t1, 3), {'o': 0 if on_first else 1}, 'h']]


# ---- camera presets (apply to the shot via scene(cam=...))
def push(d, s1=1.07, s0=1.0, tx1=0, ty1=0): return [[0, {'s': s0, 'tx': 0, 'ty': 0}], [d, {'s': s1, 'tx': tx1, 'ty': ty1}, 'l']]
def pull(d, s0=1.4, s1=1.0, dur=None, tx0=0, ty0=0):
    """Reveal: start tight, ease out to the wide frame, then hold."""
    dur = dur or min(d, 3.2)
    return [[0, {'s': s0, 'tx': tx0, 'ty': ty0}], [dur, {'s': s1, 'tx': 0, 'ty': 0}, 'io']]
def pan(d, dx, dy=0, s=1.12): return [[0, {'s': s, 'tx': dx / 2, 'ty': dy / 2}], [d, {'s': s, 'tx': -dx / 2, 'ty': -dy / 2}, 'l']]
def punch(t, s1=1.7, d=.7, hold=None, back=.7, base=1.0):
    """Fast push to a detail (set the shot's cam origin on the detail), hold, optionally return."""
    k = [[0, {'s': base}], [t, {'s': base}], [t + d, {'s': s1}, 'o']]
    if hold is not None: k += [[t + d + hold, {'s': s1}], [t + d + hold + back, {'s': base}, 'io']]
    return k


def scene(start, end, inner, bg='#000', cam=None, cam_o=None, z=1, xin=0, xout=0):
    """One shot. start/end are GLOBAL seconds; every key inside is LOCAL to start. xin/xout = fade from/to black."""
    x = (f' data-xin="{xin}"' if xin else '') + (f' data-xout="{xout}"' if xout else '')
    o = cam_o or (FW / 2, FH / 2)
    c = (f"<div data-kf='{J(cam)}' data-o=\"{o[0]} {o[1]}\" style=\"position:absolute;inset:0\">" if cam
         else '<div style="position:absolute;inset:0">')
    return (f'<div data-start="{start:.3f}" data-end="{end:.3f}"{x} style="position:absolute;left:0;top:0;width:{FW}px;height:{FH}px;'
            f'overflow:hidden;display:none;z-index:{z};background:{bg}">{c}{inner}</div></div>')


def page(scenes, head='', bg='#000'):
    rt = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runtime.js')).read()
    return (f'<!doctype html><html><head><meta charset="utf-8">{head}<style>html,body{{margin:0;background:{bg}}}'
            f'#stage{{position:relative;width:{FW}px;height:{FH}px;overflow:hidden}}</style></head><body data-fw="{FW}" data-fh="{FH}">'
            f'<div id="stage">{"".join(scenes)}</div><script>window.__FW={FW};window.__FH={FH};</script><script>{rt}</script></body></html>')


def local_fonts(root, specs):
    """@font-face CSS from npm @fontsource packages: npm i --prefix <root> @fontsource/<pkg>.
    specs = [(family, pkg, weight, style)]."""
    css = ''.join(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};"
                  f"src:url(file://{root}/node_modules/@fontsource/{pkg}/files/{pkg}-latin-{w}-{st}.woff2)}}" for fam, pkg, w, st in specs)
    return f'<style>{css}</style>'
