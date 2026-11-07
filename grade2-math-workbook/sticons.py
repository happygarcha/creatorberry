"""A small library of drawn kid-friendly icons (pure vector, no image files).

Each icon is a list of primitives in a -20..20 box:
  ("r", x, y, w, h, color)   rectangle        ("c", x, y, r, color)         circle
  ("e", x1, y1, x2, y2, col) ellipse          ("p", [(x, y), ...], color)    polygon
  ("l", x1, y1, x2, y2, color, width)  line   ("o", x, y, r, color, width)   outlined circle
  ("a", x1, y1, x2, y2, start, extent, color, width)  arc
  ("t", x, y, text, size, color)  centred text
  ("g", x, y, scale, prims, rot)  a transformed group of primitives
"""
import math
from reportlab.lib.colors import Color

COL = dict(red=(.86, .22, .22), blue=(.25, .5, .86), green=(.35, .7, .35), dgreen=(.15, .45, .25),
           yellow=(1, .85, .25), orange=(.96, .55, .15), brown=(.55, .38, .22), grey=(.62, .64, .68),
           dgrey=(.4, .42, .46), white=(1, 1, 1), black=(.15, .15, .18), skin=(1, .85, .7),
           skin2=(.87, .65, .45), skin3=(.56, .37, .25), pink=(1, .72, .82), purple=(.6, .45, .82),
           lblue=(.78, .9, 1), cream=(1, .95, .82), tan=(.9, .75, .5), pants=(.25, .3, .55),
           lred=(1, .65, .55), lgreen=(.78, .92, .66), sky=(.7, .88, 1), gold=(.95, .78, .2), silver=(.8, .82, .86))


def _c(name):
    return Color(*COL[name])


R = lambda x, y, w, h, c: ("r", x, y, w, h, c)
C = lambda x, y, r, c: ("c", x, y, r, c)
E = lambda x1, y1, x2, y2, c: ("e", x1, y1, x2, y2, c)
Pg = lambda pts, c: ("p", pts, c)
L = lambda x1, y1, x2, y2, c="black", w=1.5: ("l", x1, y1, x2, y2, c, w)
O = lambda x, y, r, c="black", w=1.5: ("o", x, y, r, c, w)
A = lambda x1, y1, x2, y2, s, e, c="black", w=1.2: ("a", x1, y1, x2, y2, s, e, c, w)
T = lambda x, y, s, size=8, c="black": ("t", x, y, s, size, c)
G = lambda x, y, sc, prims, rot=0: ("g", x, y, sc, prims, rot)


def _prims(c, prims):
    for p in prims:
        k = p[0]
        if k in ("r", "c", "e", "p"):
            c.setFillColor(_c(p[-1]))
            c.setStrokeColor(Color(.25, .27, .32))
            c.setLineWidth(.6)
            if k == "r":
                c.rect(p[1], p[2], p[3], p[4], fill=1, stroke=1)
            elif k == "c":
                c.circle(p[1], p[2], p[3], fill=1, stroke=1)
            elif k == "e":
                c.ellipse(p[1], p[2], p[3], p[4], fill=1, stroke=1)
            else:
                path = c.beginPath()
                for i, (x, y) in enumerate(p[1]):
                    path.moveTo(x, y) if i == 0 else path.lineTo(x, y)
                path.close()
                c.drawPath(path, fill=1, stroke=1)
        elif k == "l":
            c.setStrokeColor(_c(p[5]))
            c.setLineWidth(p[6])
            c.line(p[1], p[2], p[3], p[4])
        elif k == "o":
            c.setStrokeColor(_c(p[4]))
            c.setLineWidth(p[5])
            c.circle(p[1], p[2], p[3], fill=0, stroke=1)
        elif k == "a":
            c.setStrokeColor(_c(p[7]))
            c.setLineWidth(p[8])
            c.arc(p[1], p[2], p[3], p[4], p[5], p[6])
        elif k == "t":
            c.setFillColor(_c(p[5]))
            c.setFont("Helvetica-Bold", p[4])
            c.drawCentredString(p[1], p[2], p[3])
        elif k == "g":
            c.saveState()
            c.translate(p[1], p[2])
            if p[5]:
                c.rotate(p[5])
            c.scale(p[3], p[3])
            _prims(c, p[4])
            c.restoreState()


def draw_icon(c, key, cx, cy, size=40):
    c.saveState()
    c.translate(cx, cy)
    k = size / 40.0
    c.scale(k, k)
    _prims(c, ICONS[key])
    c.restoreState()
    c.setStrokeColor(Color(0, 0, 0))
    c.setLineWidth(1)


# ------------------------------------------------------------------ people
def P(shirt="blue", skin="skin", hair="brown", hat=None, glasses=False, extra=None, pants="pants"):
    pr = [R(-5, -18, 4, 12, pants), R(1, -18, 4, 12, pants),
          L(-6, 4, -11, -5, skin, 2.6), L(6, 4, 11, -5, skin, 2.6),
          Pg([(-6, 7), (6, 7), (7, -6), (-7, -6)], shirt), C(0, 12, 6.2, skin),
          E(-6.4, 13, 6.4, 19.4, hair), C(-2.3, 11.5, .9, "black"), C(2.3, 11.5, .9, "black"),
          A(-3, 7.5, 3, 12, 200, 140, "black", .8)]
    if glasses:
        pr += [O(-2.8, 11.5, 2.3, "black", .7), O(2.8, 11.5, 2.3, "black", .7)]
    hats = {"fire": [Pg([(-7, 15), (-6, 20), (0, 23), (6, 20), (7, 15)], "red"), R(-8.5, 14, 17, 2, "red")],
            "police": [R(-6.5, 15, 13, 4.5, "blue"), R(-8.5, 14, 17, 2, "black"), C(0, 17, 1.3, "yellow")],
            "hard": [E(-7, 14, 7, 23, "yellow"), R(-8.5, 14, 17, 2, "yellow")],
            "chef": [R(-5, 15, 10, 5, "white"), C(-3, 21, 3.8, "white"), C(3, 21, 3.8, "white"), C(0, 22.5, 3.8, "white")],
            "straw": [E(-11, 14, 11, 18, "yellow"), E(-5, 15.5, 5, 23, "yellow")],
            "cap": [R(-6.5, 15, 13, 4, "blue"), R(3, 14, 8, 2, "blue")]}
    if hat:
        pr += hats[hat]
    return pr + (extra or [])


def kid(shirt, skin="skin", hair="brown", sc=.8, **kw):
    return [G(0, -3, sc, P(shirt, skin, hair, **kw))]


ICONS = {}
ICONS.update({
    "mom": [G(0, 0, .92, P("pink", "skin", "brown", extra=[Pg([(-7, -6), (7, -6), (9, -13), (-9, -13)], "pink")], pants="pink"))],
    "dad": [G(0, 0, .95, P("green", "skin2", "black"))],
    "girl": [G(0, -4, .78, P("purple", "skin3", "black", extra=[C(-7, 15, 2.4, "red"), C(7, 15, 2.4, "red")]))],
    "boy": [G(0, -4, .78, P("orange", "skin", "brown"))],
    "grandma": [G(0, 0, .9, P("lblue", "skin", "silver", glasses=True, extra=[C(0, 21.5, 3, "silver")]))],
    "grandpa": [G(0, 0, .92, P("green", "skin2", "silver", glasses=True))],
    "baby": [E(-8, -16, 8, -1, "pink"), C(0, 4, 9.5, "skin"), C(-3.5, 5, 1, "black"), C(3.5, 5, 1, "black"),
             A(-3.5, 0, 3.5, 5, 200, 140, "black", .9), E(-3, 12, 3, 16, "brown"), C(-9, -8, 2.5, "skin"), C(9, -8, 2.5, "skin")],
    "doctor": [G(0, 0, .95, P("white", "skin2", "black", extra=[R(-1, -1, 2, 7, "red"), R(-3.5, 1.5, 7, 2, "red")]))],
    "teacher": [G(0, 0, .95, P("purple", "skin", "brown", glasses=True, extra=[R(8, -8, 7, 9, "yellow"), L(9, -4, 14, -4, "brown", .8)]))],
    "firefighter": [G(0, 0, .95, P("orange", "skin3", "black", hat="fire", extra=[L(-6, 0, 6, 0, "yellow", 1.5)]))],
    "police": [G(0, 0, .95, P("blue", "skin", "brown", hat="police", extra=[C(3, 2, 1.4, "yellow")]))],
    "mail": [G(0, 0, .95, P("blue", "skin2", "black", hat="cap", extra=[R(7, -9, 9, 7, "white"), L(7, -2, 11.5, -6, "grey", .7), L(16, -2, 11.5, -6, "grey", .7)]))],
    "builder": [G(0, 0, .95, P("orange", "skin", "brown", hat="hard", extra=[R(8, -3, 3, 8, "brown"), R(5, 3, 9, 4, "grey")]))],
    "farmer": [G(0, 0, .95, P("green", "skin3", "black", hat="straw", pants="blue"))],
    "cook": [G(0, 0, .95, P("white", "skin", "brown", hat="chef"))],
    "family": [G(-11, -2, .62, P("pink", "skin", "brown", pants="pink")), G(11, -2, .62, P("green", "skin2", "black")),
               G(0, -8, .5, P("purple", "skin3", "black"))],
    "sharing": [G(-11, -2, .62, P("orange", "skin", "brown")), G(11, -2, .62, P("blue", "skin3", "black")), C(0, -6, 5, "red"), C(0, -6, 2, "yellow")],
})


def face(kind):
    base = [C(0, 0, 16, "yellow" if kind != "angry" else "lred"), O(0, 0, 16, "orange", 1.2)]
    if kind == "happy":
        return base + [C(-5.5, 4, 2, "black"), C(5.5, 4, 2, "black"), A(-8, -10, 8, 3, 200, 140, "black", 1.6)]
    if kind == "sad":
        return base + [C(-5.5, 4, 2, "black"), C(5.5, 4, 2, "black"), A(-6, -13, 6, -4, 20, 140, "black", 1.6), E(5, -2, 8, 3, "lblue")]
    if kind == "angry":
        return base + [C(-5.5, 3, 2, "black"), C(5.5, 3, 2, "black"), L(-9, 9, -3, 6, "black", 1.8), L(9, 9, 3, 6, "black", 1.8),
                       A(-6, -12, 6, -4, 20, 140, "black", 1.6)]
    if kind == "surprised":
        return base + [C(-5.5, 4, 3, "white"), C(5.5, 4, 3, "white"), C(-5.5, 4, 1.2, "black"), C(5.5, 4, 1.2, "black"), C(0, -7, 3.5, "black")]
    return base + [L(-9, 4, -3, 4, "black", 1.6), L(3, 4, 9, 4, "black", 1.6), L(-3, -7, 3, -7, "black", 1.6), T(13, 12, "z", 8, "dgrey")]


for _k in ("happy", "sad", "angry", "surprised", "tired"):
    ICONS[_k] = face(_k)

# ------------------------------------------------------------------ places
ICONS.update({
    "house": [R(-14, -14, 28, 16, "cream"), Pg([(-17, 2), (0, 17), (17, 2)], "red"), R(-3, -14, 7, 11, "brown"),
              R(6, -9, 6, 6, "lblue"), R(-12, -9, 6, 6, "lblue")],
    "apartment": [R(-11, -18, 22, 36, "orange")] + [R(x, y, 5, 5, "lblue") for x in (-8, 3) for y in (10, 2, -6)] + [R(-3, -18, 6, 8, "brown")],
    "tent": [Pg([(-17, -14), (0, 15), (17, -14)], "orange"), Pg([(-4, -14), (0, -2), (4, -14)], "brown")],
    "houseboat": [R(-20, -18, 40, 5, "lblue"), Pg([(-18, -8), (18, -8), (13, -16), (-13, -16)], "blue"), R(-9, -8, 18, 10, "cream"),
                  Pg([(-11, 2), (0, 11), (11, 2)], "red"), R(-2, -6, 4, 6, "brown")],
    "school": [R(-16, -14, 32, 22, "red"), R(-4, 8, 8, 7, "red"), Pg([(-5, 15), (0, 20), (5, 15)], "grey"), R(-3, -14, 6, 10, "brown"),
               R(-13, -6, 6, 6, "lblue"), R(7, -6, 6, 6, "lblue")],
    "hospital": [R(-16, -14, 32, 28, "white"), R(-2, 0, 4, 12, "red"), R(-6, 4, 12, 4, "red"), R(-3, -14, 6, 9, "lblue"),
                 R(-13, -8, 6, 5, "lblue"), R(7, -8, 6, 5, "lblue")],
    "firehall": [R(-16, -14, 32, 24, "red"), R(-9, -14, 18, 16, "white"), L(-9, -8, 9, -8, "grey", 1), L(-9, -3, 9, -3, "grey", 1),
                 Pg([(-18, 10), (0, 18), (18, 10)], "grey")],
    "library": [R(-16, -14, 32, 22, "brown"), Pg([(-18, 8), (0, 18), (18, 8)], "tan"), R(-9, -6, 8, 10, "blue"), R(1, -6, 8, 10, "green"),
                L(-5, -6, -5, 4, "white", 1), L(5, -6, 5, 4, "white", 1), R(-3, -14, 6, 5, "cream")],
    "store": [R(-15, -14, 30, 20, "cream"), R(-16, 6, 8, 6, "red"), R(-8, 6, 8, 6, "white"), R(0, 6, 8, 6, "red"), R(8, 6, 8, 6, "white"),
              R(-3, -14, 8, 12, "brown"), R(-12, -8, 7, 7, "lblue")],
    "bank": [Pg([(-18, 6), (0, 17), (18, 6)], "grey"), R(-16, -14, 32, 4, "grey"), R(-13, -10, 5, 16, "cream"), R(-2.5, -10, 5, 16, "cream"),
             R(8, -10, 5, 16, "cream"), R(-16, 6, 32, 3, "grey")],
    "postoffice": [R(-16, -14, 32, 24, "blue"), R(-9, -4, 18, 11, "white"), L(-9, 7, 0, 1, "grey", 1), L(9, 7, 0, 1, "grey", 1), R(-3, -14, 6, 6, "brown")],
    "park": [R(-20, -18, 40, 5, "green"), R(-3, -13, 5, 12, "brown"), C(0, 6, 10, "green"), R(8, -9, 10, 3, "brown"), L(9, -13, 9, -9), L(17, -13, 17, -9)],
    "playground": [R(-20, -18, 40, 4, "green"), Pg([(-13, -14), (-13, 12), (-7, 12), (12, -14)], "orange"), L(-13, 12, -3, 12, "red", 2), L(-13, -2, -7, -2, "brown", 1.5)],
    "barn": [R(-16, -14, 32, 22, "red"), Pg([(-18, 8), (-9, 16), (9, 16), (18, 8)], "red"), R(-6, -14, 12, 14, "white"), L(-6, -14, 6, 0, "red", 1), L(6, -14, -6, 0, "red", 1)],
})

# ------------------------------------------------------------------ nature
ICONS.update({
    "tree": [R(-3, -18, 6, 14, "brown"), C(0, 5, 12, "green"), C(-8, -1, 8, "green"), C(8, -1, 8, "green")],
    "cedar": [R(-2, -18, 4, 6, "brown"), Pg([(-14, -12), (0, 0), (14, -12)], "dgreen"), Pg([(-11, -4), (0, 8), (11, -4)], "dgreen"), Pg([(-8, 4), (0, 18), (8, 4)], "dgreen")],
    "mountain": [Pg([(-20, -14), (-4, 14), (12, -14)], "grey"), Pg([(0, -14), (10, 6), (20, -14)], "dgrey"), Pg([(-7, 8), (-4, 14), (-1, 8)], "white")],
    "river": [R(-20, -14, 40, 28, "green"), Pg([(-4, -14), (4, -14), (8, 0), (2, 14), (-6, 14), (0, 0)], "blue")],
    "lake": [R(-20, -14, 40, 28, "green"), E(-15, -9, 15, 9, "blue"), A(-8, -4, 2, 2, 200, 120, "white", 1)],
    "ocean": [R(-20, -14, 40, 28, "blue"), A(-16, -2, -6, 6, 0, 180, "white", 1.2), A(-4, -8, 6, 0, 0, 180, "white", 1.2), A(8, -2, 18, 6, 0, 180, "white", 1.2), C(12, 10, 5, "yellow")],
    "island": [R(-20, -14, 40, 28, "blue"), E(-13, -9, 13, 1, "yellow"), R(-1, -2, 2.5, 11, "brown"), C(0, 11, 5, "green"), C(-5, 8, 3.5, "green"), C(5, 8, 3.5, "green")],
    "forest": [G(-9, -2, .6, [R(-3, -18, 6, 14, "brown"), C(0, 5, 12, "green")]), G(9, -2, .6, [R(-3, -18, 6, 14, "brown"), C(0, 5, 12, "green")]),
               G(0, 2, .75, [R(-2, -18, 4, 6, "brown"), Pg([(-14, -12), (0, 0), (14, -12)], "dgreen"), Pg([(-8, 4), (0, 18), (8, 4)], "dgreen")])],
    "bridge": [R(-20, -18, 40, 10, "lblue"), R(-20, 2, 40, 4, "grey"), R(-14, -10, 3, 12, "dgrey"), R(11, -10, 3, 12, "dgrey"),
               A(-13, -2, 13, 20, 0, 180, "dgrey", 1.5), L(-6, 6, -6, 11, "dgrey", 1), L(0, 6, 0, 12, "dgrey", 1), L(6, 6, 6, 11, "dgrey", 1)],
    "sun": [C(0, 0, 9, "yellow")] + [L(11 * math.cos(math.radians(a)), 11 * math.sin(math.radians(a)), 17 * math.cos(math.radians(a)), 17 * math.sin(math.radians(a)), "orange", 2) for a in range(0, 360, 45)],
    "snowflake": [C(0, 0, 17, "lblue")] + [L(0, 0, 13 * math.cos(math.radians(a)), 13 * math.sin(math.radians(a)), "white", 2.2) for a in range(0, 360, 60)] + [C(0, 0, 2, "white")],
    "flower": [L(0, -17, 0, 2, "green", 2.5), E(-9, -10, 0, -6, "green")] + [C(7 * math.cos(math.radians(a)), 8 + 7 * math.sin(math.radians(a)), 4.6, "pink") for a in range(0, 360, 72)] + [C(0, 8, 3.5, "yellow")],
    "dogwood": [C(0, 0, 3.5, "yellow")] + [E(-4 + 0, 3, 4, 17, "white")] + [G(0, 0, 1, [E(-4, 3, 4, 17, "white")], a) for a in (90, 180, 270)],
})

# --------------------------------------------------------------- transport
ICONS.update({
    "car": [R(-16, -8, 32, 10, "red"), Pg([(-9, 2), (-5, 10), (5, 10), (10, 2)], "red"), Pg([(-7, 2), (-4, 8), (0, 8), (0, 2)], "lblue"),
            Pg([(2, 2), (2, 8), (5, 8), (8, 2)], "lblue"), C(-9, -8, 4, "black"), C(9, -8, 4, "black")],
    "bus": [R(-18, -10, 36, 20, "yellow")] + [R(x, 0, 7, 6, "lblue") for x in (-15, -6, 3, 12)] + [R(-18, -4, 36, 2, "orange"), C(-10, -10, 4, "black"), C(10, -10, 4, "black")],
    "bike": [O(-10, -8, 7, "black", 1.6), O(10, -8, 7, "black", 1.6), L(-10, -8, -2, 2, "red", 1.6), L(-2, 2, 10, -8, "red", 1.6),
             L(-10, -8, 2, -8, "red", 1.6), L(-2, 2, 4, 2, "red", 1.6), L(4, 2, 10, -8, "red", 1.6), L(-5, 5, 0, 5, "black", 2.2), L(9, 4, 12, 4, "black", 2)],
    "truck": [R(-18, -8, 22, 16, "orange"), R(4, -8, 14, 10, "red"), R(8, -2, 7, 6, "lblue"), C(-10, -10, 4, "black"), C(10, -10, 4, "black")],
    "train": [R(-16, -4, 22, 14, "blue"), R(6, -4, 12, 8, "red"), R(12, 4, 4, 8, "black"), R(-14, 4, 6, 6, "lblue"), C(-10, -8, 4, "black"), C(2, -8, 4, "black"), C(12, -8, 4, "black"), L(-20, -13, 20, -13, "dgrey", 1.5)],
    "plane": [E(-18, -3, 18, 4, "white"), Pg([(-2, 3), (-12, 15), (-8, 15), (4, 3)], "grey"), Pg([(-2, -2), (-12, -14), (-8, -14), (4, -2)], "grey"), Pg([(-18, 1), (-20, 9), (-14, 2)], "grey"), C(10, 1, 1.2, "lblue"), C(5, 1, 1.2, "lblue")],
    "ferry": [R(-20, -18, 40, 4, "lblue"), Pg([(-18, -4), (18, -4), (12, -14), (-12, -14)], "blue"), R(-10, -4, 20, 8, "white"), R(-6, 4, 12, 6, "white"), R(-2, 10, 4, 6, "red")],
    "canoe": [R(-20, -18, 40, 8, "lblue"), Pg([(-18, -4), (18, -4), (12, -11), (-12, -11)], "brown"), L(-4, 10, 4, -9, "tan", 2), E(-8, 8, -2, 14, "tan")],
    "horsecart": [R(-4, -4, 18, 8, "brown"), O(0, -8, 6, "brown", 1.8), O(11, -8, 6, "brown", 1.8), E(-20, -4, -6, 8, "brown"), R(-19, -14, 2.5, 10, "brown"),
                  R(-9, -14, 2.5, 10, "brown"), Pg([(-8, 6), (-6, 16), (-2, 14), (-5, 4)], "brown"), L(-6, 3, -4, 0, "black", 1)],
    "tractor": [R(-4, -3, 14, 12, "green"), R(-16, 0, 12, 8, "green"), R(2, 9, 5, 6, "dgrey"), C(-10, -8, 6, "black"), C(8, -6, 4, "black")],
})

# ----------------------------------------------------------- communication
ICONS.update({
    "letter": [R(-16, -10, 32, 20, "white"), L(-16, 10, 0, -2, "grey", 1.2), L(16, 10, 0, -2, "grey", 1.2), R(8, 2, 6, 6, "red")],
    "phone": [R(-7, -16, 14, 32, "black"), R(-5, -12, 10, 22, "lblue"), C(0, -14, 1.5, "white")],
    "computer": [R(-14, -6, 28, 18, "grey"), R(-12, -4, 24, 14, "lblue"), R(-18, -12, 36, 4, "grey")],
    "tv": [R(-16, -10, 32, 22, "black"), R(-13, -7, 26, 16, "lblue"), L(-6, 12, -10, 18), L(6, 12, 10, 18)],
    "typewriter": [R(-15, -10, 30, 12, "dgrey"), R(-10, 2, 20, 12, "white")] + [C(x, -5, 1.6, "white") for x in (-10, -5, 0, 5, 10)],
    "candle": [R(-4, -14, 8, 18, "cream"), L(0, 4, 0, 8, "black", 1), E(-3, 8, 3, 17, "orange")],
    "lamp": [Pg([(-10, 4), (10, 4), (5, 15), (-5, 15)], "yellow"), R(-1, -10, 2, 14, "grey"), R(-7, -14, 14, 4, "grey")],
    "stop": [Pg([(15 * math.cos(math.radians(22.5 + 45 * k)), 15 * math.sin(math.radians(22.5 + 45 * k))) for k in range(8)], "red"), T(0, -2.5, "STOP", 7, "white")],
    "trafficlight": [R(-7, -17, 14, 34, "black"), C(0, 9, 4.2, "red"), C(0, 0, 4.2, "yellow"), C(0, -9, 4.2, "green")],
    "crosswalk": [R(-20, -14, 40, 28, "dgrey")] + [R(x, -14, 5, 28, "white") for x in (-16, -8, 0, 8, 16)],
    "helmet": [E(-14, -4, 14, 16, "red"), R(-16, -8, 32, 5, "red"), R(-6, -3, 12, 2, "white"), L(-12, -8, -12, -14, "grey", 1.5), L(12, -8, 12, -14, "grey", 1.5)],
    "lifejacket": [Pg([(-12, 14), (-4, 14), (0, 8), (4, 14), (12, 14), (10, -14), (-10, -14)], "orange"), L(-10, -2, 10, -2, "yellow", 2.5), L(0, 8, 0, -14, "yellow", 1.5)],
    "umbrella": [Pg([(-16, 2), (-12, 12), (-4, 18), (4, 18), (12, 12), (16, 2), (8, 6), (0, 2), (-8, 6)], "red"), L(0, 2, 0, -14, "black", 1.6), A(-4, -18, 4, -10, 180, 180, "black", 1.6)],
    "bin_recycle": [R(-9, -14, 18, 20, "blue"), R(-11, 6, 22, 3, "blue"), Pg([(0, 3), (-5, -5), (5, -5)], "white")],
    "bin_trash": [R(-9, -14, 18, 20, "dgrey"), R(-11, 6, 22, 3, "dgrey"), L(-4, 2, -4, -10, "grey", 1.2), L(0, 2, 0, -10, "grey", 1.2), L(4, 2, 4, -10, "grey", 1.2)],
})

# ------------------------------------------------------------------- things
ICONS.update({
    "apple": [C(0, -2, 12, "red"), R(-1, 8, 2, 6, "brown"), E(2, 10, 11, 16, "green")],
    "bread": [E(-15, -8, 15, 10, "orange"), L(-7, -6, -5, 7, "tan", 1.4), L(0, -7, 0, 8, "tan", 1.4), L(7, -6, 5, 7, "tan", 1.4)],
    "milk": [R(-8, -15, 16, 22, "white"), Pg([(-8, 7), (0, 16), (8, 7)], "lblue"), R(-8, -6, 16, 9, "blue")],
    "water": [Pg([(0, 16), (-10, -2), (10, -2)], "blue"), C(0, -4, 10, "blue"), A(-5, -8, 5, 2, 200, 100, "white", 1.4)],
    "shirt": [Pg([(-8, 14), (-18, 6), (-14, 0), (-8, 4), (-8, -14), (8, -14), (8, 4), (14, 0), (18, 6), (8, 14), (3, 10), (-3, 10)], "blue")],
    "coat": [Pg([(-8, 14), (-18, 6), (-16, -8), (-8, -4), (-8, -16), (8, -16), (8, -4), (16, -8), (18, 6), (8, 14), (3, 10), (-3, 10)], "purple"), L(0, 10, 0, -16, "white", 1.2), C(-3, 0, 1, "white"), C(-3, -7, 1, "white")],
    "shoe": [Pg([(-16, -8), (-16, 4), (-6, 4), (-4, -2), (16, -4), (16, -8)], "brown"), R(-16, -10, 32, 3, "black")],
    "bed": [R(-18, -10, 36, 8, "blue"), R(-18, -14, 4, 16, "brown"), R(14, -14, 4, 10, "brown"), E(-14, -2, -4, 6, "white")],
    "ball": [C(0, 0, 13, "white")] + [Pg([(0, 0), (13 * math.cos(math.radians(a)), 13 * math.sin(math.radians(a))), (13 * math.cos(math.radians(a + 30)), 13 * math.sin(math.radians(a + 30))), (13 * math.cos(math.radians(a + 60)), 13 * math.sin(math.radians(a + 60)))], ["red", "yellow", "blue", "green", "orange", "purple"][i]) for i, a in enumerate(range(0, 360, 60))] + [O(0, 0, 13, "dgrey", 1)],
    "teddy": [C(0, -4, 10, "brown"), C(0, 10, 7, "brown"), C(-6, 15, 3, "brown"), C(6, 15, 3, "brown"), C(0, 8, 3, "cream"), C(-2, 11, 1, "black"), C(2, 11, 1, "black")],
    "game": [R(-16, -6, 32, 14, "dgrey"), C(-8, 1, 3.5, "black"), C(8, 4, 2, "red"), C(12, 0, 2, "blue"), L(-8, -2, -8, 5, "white", 1.2)],
    "candy": [L(0, -16, 0, 0, "white", 2.5), C(0, 6, 10, "pink"), C(0, 6, 6, "white"), C(0, 6, 2.5, "pink")],
    "book": [R(-12, -14, 24, 28, "blue"), R(-9, -11, 18, 22, "white"), L(-6, 4, 6, 4, "grey", 1), L(-6, 0, 6, 0, "grey", 1), L(-6, -4, 3, -4, "grey", 1)],
    "toothbrush": [R(-2, -17, 4, 22, "blue"), R(-3.5, 5, 7, 11, "white"), L(-2, 8, 2, 8, "lblue", 1), L(-2, 12, 2, 12, "lblue", 1)],
    "backpack": [R(-10, -14, 20, 26, "green"), R(-7, -14, 14, 10, "dgreen"), A(-6, 6, 6, 18, 0, 180, "dgreen", 2)],
    "stove": [R(-14, -14, 28, 26, "grey"), R(-11, -2, 22, 12, "black"), C(-5, 4, 3, "red"), C(5, 4, 3, "red"), R(-11, -12, 22, 8, "white")],
    "tub": [Pg([(-18, -2), (18, -2), (14, -12), (-14, -12)], "white"), L(-18, -2, 18, -2, "grey", 2.5), C(-8, 6, 3, "lblue"), C(2, 10, 3, "lblue"), R(-12, -16, 3, 4, "grey"), R(9, -16, 3, 4, "grey")],
    "sofa": [R(-14, -4, 28, 12, "purple"), R(-18, -6, 6, 12, "purple"), R(12, -6, 6, 12, "purple"), R(-14, 6, 28, 9, "purple"), R(-14, -12, 3, 6, "brown"), R(11, -12, 3, 6, "brown")],
    "fridge": [R(-9, -17, 18, 34, "white"), L(-9, 2, 9, 2, "grey", 1.2), R(5, 6, 2, 7, "grey"), R(5, -8, 2, 7, "grey")],
    "stethoscope": [A(-8, -2, 8, 14, 180, 180, "dgrey", 2.2), L(-8, 6, -8, 14, "dgrey", 2.2), L(8, 6, 8, 14, "dgrey", 2.2), L(0, -2, 0, -10, "dgrey", 2.2), C(0, -13, 4.5, "silver")],
    "hose": [O(0, 0, 10, "red", 4), O(0, 0, 5, "red", 3), R(10, -14, 8, 6, "yellow"), L(14, -8, 14, 8, "lblue", 2)],
    "chalkboard": [R(-17, -10, 34, 24, "dgreen"), R(-19, -12, 38, 3, "brown"), L(-12, 6, -2, 6, "white", 1.5), L(-12, 0, 6, 0, "white", 1.5), C(10, 6, 2, "white")],
    "pot": [R(-12, -10, 24, 18, "dgrey"), R(-16, 4, 5, 3, "dgrey"), R(11, 4, 5, 3, "dgrey"), E(-12, 5, 12, 11, "grey"), A(-5, 12, 5, 18, 0, 180, "grey", 1.5)],
    "badge": [Pg([(0, 16), (13, 10), (11, -6), (0, -16), (-11, -6), (-13, 10)], "gold"), C(0, 0, 5, "yellow")],
    "scissors": [O(-6, -10, 5, "red", 2), O(6, -10, 5, "red", 2), L(-6, -6, 6, 15, "grey", 2), L(6, -6, -6, 15, "grey", 2)],
    "hammer": [R(-2, -16, 4, 24, "brown"), R(-10, 6, 20, 8, "grey")],
    "jar": [R(-10, -14, 20, 22, "lblue"), R(-11, 8, 22, 4, "grey")] + [C(x, y, 3.5, "gold") for x, y in ((-4, -10), (4, -10), (0, -4))],
    "cart": [Pg([(-18, 14), (-12, 14), (-8, -4), (14, -4), (16, 8), (-9, 8)], "grey"), C(-6, -12, 3, "black"), C(10, -12, 3, "black")],
    "cookie": [C(0, 0, 11, "tan"), C(-4, 4, 1.6, "brown"), C(4, 3, 1.6, "brown"), C(0, -4, 1.6, "brown"), C(-5, -3, 1.4, "brown"), C(6, -4, 1.4, "brown")],
})
ICONS["coin_loonie"] = [C(0, 0, 13, "gold"), O(0, 0, 13, "orange", 1.5), T(0, -3.5, "$1", 11, "dgrey")]
ICONS["coin_toonie"] = [C(0, 0, 14, "silver"), C(0, 0, 9, "gold"), T(0, -3.5, "$2", 11, "dgrey")]
ICONS["coin_quarter"] = [C(0, 0, 13, "silver"), O(0, 0, 13, "dgrey", 1), T(0, -2.5, "25¢", 9.5, "dgrey")]
ICONS["coin_dime"] = [C(0, 0, 10, "silver"), O(0, 0, 10, "dgrey", 1), T(0, -2.5, "10¢", 8.5, "dgrey")]
ICONS["coin_nickel"] = [C(0, 0, 12, "silver"), O(0, 0, 12, "dgrey", 1), T(0, -2.5, "5¢", 10, "dgrey")]

# ---------------------------------------------------- celebration / Canada
_leaf_half = [(0, 18), (3, 10), (7, 12), (7, 5), (14, 7), (11, 0), (15, -3), (8, -5), (9, -10), (2, -8), (1, -17)]
_leaf = _leaf_half + [(-x, y) for x, y in reversed(_leaf_half)]
ICONS.update({
    "maple": [Pg(_leaf, "red")],
    "leaf_fall": [Pg(_leaf, "orange")],
    "flag_canada": [R(-20, -11, 40, 22, "white"), R(-20, -11, 9, 22, "red"), R(11, -11, 9, 22, "red"), G(0, -1, .46, [Pg(_leaf, "red")])],
    "flag_blue": [R(-20, -11, 40, 22, "blue"), R(-20, -3, 40, 6, "white")],
    "flag_green": [R(-20, -11, 40, 22, "green"), C(0, 0, 6, "yellow")],
    "cake": [R(-14, -12, 28, 12, "pink"), R(-14, 0, 28, 6, "cream"), R(-8, 6, 2.5, 7, "yellow"), R(-1, 6, 2.5, 7, "yellow"), R(6, 6, 2.5, 7, "yellow"),
             E(-8.5, 13, -4.5, 17, "orange"), E(-1.5, 13, 2.5, 17, "orange"), E(5.5, 13, 9.5, 17, "orange")],
    "gift": [R(-12, -12, 24, 18, "red"), R(-2, -12, 4, 18, "yellow"), R(-14, 6, 28, 5, "red"), C(-5, 14, 4, "yellow"), C(5, 14, 4, "yellow")],
    "fireworks": [C(0, 0, 1.5, "yellow")] + [L(3 * math.cos(math.radians(a)), 3 * math.sin(math.radians(a)), 15 * math.cos(math.radians(a)), 15 * math.sin(math.radians(a)), ["red", "orange", "yellow", "blue", "purple"][i % 5], 2) for i, a in enumerate(range(0, 360, 30))],
    "balloon": [E(-9, -2, 9, 18, "red"), Pg([(-2, -2), (2, -2), (0, -5)], "red"), L(0, -5, 0, -18, "grey", 1.2)],
    "pumpkin": [E(-15, -11, 15, 9, "orange"), E(-8, -11, 8, 9, "lred"), R(-1.5, 8, 3, 6, "green")],
    "lantern": [E(-10, -9, 10, 11, "red"), R(-4, 11, 8, 3, "yellow"), R(-4, -12, 8, 3, "yellow"), L(0, 14, 0, 19, "grey", 1.2), L(0, -12, 0, -18, "yellow", 2)],
    "salmon": [E(-17, -7, 11, 7, "orange"), Pg([(10, 0), (20, 8), (20, -8)], "orange"), C(-11, 2, 1.4, "black"), L(-2, -6, -2, 6, "red", 1)],
})
for _n, _t in (("say_thanks", "Thank you!"), ("say_please", "Please"), ("say_sorry", "I'm sorry"), ("say_go", "Go away!"), ("say_give", "Give me!"), ("say_hello", "Hello!")):
    ICONS[_n] = [E(-19, -9, 19, 14, "white"), Pg([(-10, -7), (-14, -16), (-3, -9)], "white"), T(0, -1.5, _t, 6.4 if len(_t) > 8 else 7.5, "black")]
for _n, _r in (("arrow_up", 0), ("arrow_left", 90), ("arrow_down", 180), ("arrow_right", 270)):
    ICONS[_n] = [G(0, 0, 1, [Pg([(0, 17), (11, 3), (4, 3), (4, -15), (-4, -15), (-4, 3), (-11, 3)], "blue")], _r)]

LBL = {"mom": "mom", "dad": "dad", "girl": "girl", "boy": "boy", "grandma": "grandma", "grandpa": "grandpa", "baby": "baby",
       "doctor": "doctor", "teacher": "teacher", "firefighter": "firefighter", "police": "police officer", "mail": "mail carrier",
       "builder": "builder", "farmer": "farmer", "cook": "cook", "family": "family", "sharing": "sharing",
       "happy": "happy", "sad": "sad", "angry": "angry", "surprised": "surprised", "tired": "sleepy",
       "house": "house", "apartment": "apartment", "tent": "tent", "houseboat": "houseboat", "school": "school",
       "hospital": "hospital", "firehall": "fire hall", "library": "library", "store": "store", "bank": "bank",
       "postoffice": "post office", "park": "park", "playground": "playground", "barn": "farm barn",
       "tree": "tree", "cedar": "cedar tree", "mountain": "mountain", "river": "river", "lake": "lake", "ocean": "ocean",
       "island": "island", "forest": "forest", "bridge": "bridge", "sun": "sun", "snowflake": "snowflake", "flower": "flower",
       "dogwood": "dogwood flower", "car": "car", "bus": "bus", "bike": "bike", "truck": "truck", "train": "train",
       "plane": "airplane", "ferry": "ferry", "canoe": "canoe", "horsecart": "horse cart", "tractor": "tractor",
       "letter": "letter", "phone": "phone", "computer": "computer", "tv": "TV", "typewriter": "typewriter",
       "candle": "candle", "lamp": "lamp", "stop": "stop sign", "trafficlight": "traffic light", "crosswalk": "crosswalk",
       "helmet": "helmet", "lifejacket": "life jacket", "umbrella": "umbrella", "bin_recycle": "recycling bin",
       "bin_trash": "garbage can", "apple": "apple", "bread": "bread", "milk": "milk", "water": "water", "shirt": "shirt",
       "coat": "coat", "shoe": "shoe", "bed": "bed", "ball": "ball", "teddy": "teddy bear", "game": "video game",
       "candy": "candy", "book": "book", "toothbrush": "toothbrush", "backpack": "backpack", "stove": "stove",
       "tub": "bathtub", "sofa": "sofa", "fridge": "fridge", "stethoscope": "stethoscope", "hose": "fire hose",
       "chalkboard": "chalkboard", "pot": "pot", "badge": "badge", "scissors": "scissors", "hammer": "hammer",
       "jar": "savings jar", "cart": "shopping cart", "cookie": "cookie", "maple": "maple leaf", "leaf_fall": "autumn leaf",
       "flag_canada": "Canadian flag", "cake": "cake", "gift": "gift", "fireworks": "fireworks", "balloon": "balloon",
       "pumpkin": "pumpkin", "lantern": "lantern", "salmon": "salmon", "canoe": "canoe",
       "coin_loonie": "loonie", "coin_toonie": "toonie", "coin_quarter": "quarter", "coin_dime": "dime", "coin_nickel": "nickel",
       "arrow_up": "up", "arrow_down": "down", "arrow_left": "left", "arrow_right": "right"}
