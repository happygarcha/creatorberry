"""Extra drawn icons for the Physical & Health Education workbook (poses, body, food, hygiene...).
Importing this module adds them to sticons.ICONS / LBL."""
import math
from sticons import ICONS, LBL, R, C, E, Pg, L, O, A, T, G, P


def fig(head, neck, hip, arms, legs, shirt="blue", skin="skin", pants="pants", extra=(), before=()):
    pr = list(before)
    for a, b, c_ in legs:
        pr += [L(*a, *b, pants, 3.4), L(*b, *c_, pants, 3.4), C(c_[0], c_[1], 2.3, "black")]
    pr.append(L(*hip, *neck, shirt, 6.5))
    for a, b, c_ in arms:
        pr += [L(*a, *b, skin, 2.7), L(*b, *c_, skin, 2.7)]
    hx, hy = head
    pr += [C(hx, hy, 5.6, skin), E(hx - 5.8, hy + .5, hx + 5.8, hy + 6.6, "brown"), C(hx - 2, hy + .4, .9, "black"), C(hx + 2, hy + .4, .9, "black"),
           A(hx - 2.8, hy - 4, hx + 2.8, hy + 1.2, 200, 140, "black", .8)]
    return pr + list(extra)


BALL = lambda x, y, col="red": [C(x, y, 3.4, col)]
POSES = {
    "run": fig((4, 16), (2, 9), (-1, -3), [((2, 8), (8, 5), (12, 10)), ((2, 8), (-4, 5), (-8, 1))],
               [((-1, -3), (6, -8), (9, -17)), ((-1, -3), (-6, -10), (-13, -13))], shirt="red"),
    "jump": fig((0, 16), (0, 9), (0, -2), [((0, 8), (-7, 13), (-9, 20)), ((0, 8), (7, 13), (9, 20))],
                [((0, -2), (-6, -9), (-3, -14)), ((0, -2), (6, -9), (3, -14))], shirt="orange"),
    "hop": fig((0, 16), (0, 9), (0, -3), [((0, 8), (-8, 6), (-13, 9)), ((0, 8), (8, 6), (13, 9))],
               [((0, -3), (0, -10), (0, -17)), ((0, -3), (7, -7), (4, -13))], shirt="green"),
    "walk": fig((1, 16), (0, 9), (0, -3), [((0, 8), (4, 3), (5, -2)), ((0, 8), (-4, 3), (-5, -2))],
                [((0, -3), (4, -10), (5, -17)), ((0, -3), (-3, -10), (-5, -17))], shirt="purple"),
    "balance": fig((0, 16), (0, 9), (0, -3), [((0, 8), (-8, 9), (-15, 9)), ((0, 8), (8, 9), (15, 9))],
                   [((0, -3), (0, -10), (0, -17)), ((0, -3), (8, -5), (13, -4))], shirt="blue"),
    "stretch": fig((0, 16), (0, 9), (0, -3), [((0, 8), (-3, 15), (-3, 21)), ((0, 8), (3, 15), (3, 21))],
                   [((0, -3), (-3, -10), (-4, -17)), ((0, -3), (3, -10), (4, -17))], shirt="pink"),
    "bend": fig((8, 2), (4, 5), (-3, -3), [((4, 5), (7, -3), (9, -11)), ((4, 5), (9, -2), (12, -10))],
                [((-3, -3), (-3, -10), (-3, -17)), ((-3, -3), (-1, -10), (-1, -17))], shirt="green"),
    "throw": fig((0, 15), (0, 8), (0, -4), [((0, 7), (7, 11), (12, 16)), ((0, 7), (-6, 8), (-11, 9))],
                 [((0, -4), (5, -10), (8, -17)), ((0, -4), (-5, -10), (-8, -17))], shirt="orange", extra=BALL(13, 18)),
    "catch": fig((0, 16), (0, 9), (0, -3), [((0, 8), (6, 7), (12, 8)), ((0, 8), (6, 6), (12, 6))],
                 [((0, -3), (-3, -10), (-4, -17)), ((0, -3), (3, -10), (4, -17))], shirt="blue", extra=BALL(15, 7)),
    "kick": fig((-2, 16), (-2, 9), (-2, -3), [((-2, 8), (-8, 6), (-12, 9)), ((-2, 8), (4, 6), (7, 10))],
                [((-2, -3), (-2, -10), (-2, -17)), ((-2, -3), (6, -4), (12, -10))], shirt="red", extra=[C(17, -14, 3.6, "white"), O(17, -14, 3.6, "black", .8)]),
    "bounce": fig((-2, 16), (-2, 9), (-2, -3), [((-2, 8), (4, 2), (8, -6)), ((-2, 8), (-7, 5), (-10, 3))],
                  [((-2, -3), (-5, -10), (-6, -17)), ((-2, -3), (1, -10), (2, -17))], shirt="purple", extra=BALL(9, -12, "orange")),
    "swim": [R(-20, -18, 40, 22, "lblue")] + fig((11, 1), (6, 0), (-8, -3), [((6, 0), (12, 6), (17, 9)), ((6, 0), (0, 5), (-4, 8))],
                                                  [((-8, -3), (-14, -1), (-19, -4)), ((-8, -3), (-14, -6), (-19, -8))], shirt="red") +
            [A(-20, -6, -12, 0, 0, 180, "blue", 1.2), A(-8, -8, 0, -2, 0, 180, "blue", 1.2), A(6, -8, 16, -2, 0, 180, "blue", 1.2)],
    "dance": fig((2, 16), (0, 9), (0, -3), [((0, 8), (-8, 13), (-11, 19)), ((0, 8), (7, 6), (12, 9))],
                 [((0, -3), (-5, -10), (-8, -17)), ((0, -3), (4, -9), (8, -13))], shirt="pink",
                 extra=[C(-15, 12, 1.5, "yellow"), C(16, 15, 1.5, "yellow"), C(14, 1, 1.5, "orange")]),
    "skiprope": fig((0, 16), (0, 9), (0, -3), [((0, 8), (-7, 2), (-10, -2)), ((0, 8), (7, 2), (10, -2))],
                    [((0, -3), (-2, -10), (-2, -14)), ((0, -3), (2, -10), (2, -14))], shirt="green",
                    extra=[A(-11, -22, 11, 10, 180, 180, "red", 1.8), L(-10, -2, -11, -6, "red", 1.5)]),
    "sit_tv": fig((-3, 10), (-3, 4), (-4, -5), [((-3, 3), (2, -1), (7, -2)), ((-3, 3), (1, 0), (6, -1))],
                  [((-4, -5), (4, -5), (5, -14)), ((-4, -5), (3, -7), (4, -15))], shirt="blue",
                  extra=[R(11, -3, 9, 9, "black"), R(12, -2, 7, 7, "lblue")], before=[R(-10, -9, 9, 3, "brown"), R(-10, -9, 2, 16, "brown")]),
    "sleep": [R(-19, -13, 38, 8, "blue"), R(-19, -17, 3, 14, "brown"), R(-19, -5, 38, 3, "lblue")] +
             [L(-6, -2, 12, -2, "green", 6), C(-11, -1, 5.4, "skin"), E(-16.5, 0, -5.5, 5, "brown"), T(10, 8, "z", 9, "dgrey"), T(15, 13, "Z", 11, "dgrey")],
}
ICONS.update(POSES)

_ear_in = A(-5, -7, 5, 7, 40, 240, "skin3", 1.3)
ICONS.update({
    "eye": [E(-14, -8, 14, 8, "white"), C(0, 0, 6, "blue"), C(0, 0, 3, "black"), C(2, 2, 1, "white")],
    "ear": [E(-9, -14, 9, 14, "skin"), _ear_in, A(-3, -3, 3, 3, 60, 240, "skin3", 1.2)],
    "nose": [Pg([(0, 12), (-9, -8), (9, -8)], "skin"), C(-4, -8, 1.6, "brown"), C(4, -8, 1.6, "brown")],
    "hand": [R(-8, -12, 16, 15, "skin")] + [R(x, 3, 3.4, 12, "skin") for x in (-8, -3.7, .6, 4.6)] + [Pg([(-8, -4), (-14, 4), (-11, 7), (-8, 2)], "skin")],
    "foot": [Pg([(-6, 14), (4, 14), (6, -4), (14, -8), (14, -15), (-8, -15), (-8, -2)], "skin")] + [C(x, -12, 1.6, "skin2") for x in (7, 10, 13)],
    "heart": [C(-5.5, 5, 6.5, "red"), C(5.5, 5, 6.5, "red"), Pg([(-11, 2), (11, 2), (0, -14)], "red"), A(-8, 3, -2, 9, 120, 60, "white", 1.4)],
    "lungs": [E(-17, -12, -2, 12, "pink"), E(2, -12, 17, 12, "pink"), R(-1.5, 2, 3, 15, "grey"), L(0, 4, -6, -2, "grey", 1.4), L(0, 4, 6, -2, "grey", 1.4)],
    "carrot": [Pg([(-5, 10), (5, 10), (0, -17)], "orange"), E(-6, 9, 0, 19, "green"), E(0, 9, 6, 19, "green"), L(-2, 4, 2, 4, "red", 1), L(-1.5, -4, 1.5, -4, "red", 1)],
    "broccoli": [R(-3, -16, 6, 14, "green"), C(-7, 2, 6, "dgreen"), C(7, 2, 6, "dgreen"), C(0, 9, 7, "dgreen"), C(0, 3, 6, "green")],
    "banana": [Pg([(-15, 5), (-7, -8), (8, -10), (16, -3), (13, 0), (6, -4), (-3, -3), (-10, 7)], "yellow"), C(-15, 6, 1.6, "brown")],
    "orange": [C(0, -1, 12, "orange"), E(0, 9, 9, 15, "green"), L(0, 10, 0, 12, "brown", 1.4)],
    "rice": [Pg([(-14, 0), (14, 0), (10, -12), (-10, -12)], "blue"), E(-12, -1, 12, 11, "white"), L(-4, 4, -2, 6, "grey", .8), L(3, 5, 5, 3, "grey", .8)],
    "egg": [E(-14, -9, 14, 9, "white"), C(0, 0, 5.5, "yellow")],
    "beans": [E(-14, -3, -2, 7, "brown"), E(-2, -9, 11, 1, "red"), E(-9, 5, 3, 15, "red"), E(3, 4, 14, 13, "brown")],
    "juice": [R(-8, -12, 16, 22, "orange"), R(-8, 0, 16, 8, "yellow"), L(2, 10, 6, 17, "red", 2), C(-2, 4, 2.5, "orange")],
    "chips": [Pg([(-10, -14), (10, -14), (12, 12), (-12, 12)], "red"), T(0, -2, "CHIPS", 6, "white"), L(-12, 12, 12, 12, "yellow", 2)],
    "donut": [O(0, 0, 11, "pink", 7), O(0, 0, 11, "orange", 1)] + [L(x, y, x + 2, y + 1, c, 1.6) for x, y, c in ((-9, 6, "blue"), (4, 12, "yellow"), (9, -2, "green"), (-4, -11, "red"))],
    "soap": [R(-7, -14, 14, 18, "lblue"), R(-2, 4, 4, 6, "grey"), R(-2, 10, 9, 3, "grey"), O(11, -4, 3.2, "blue", 1), O(14, 3, 2.2, "blue", 1)],
    "towel": [R(-14, -12, 28, 24, "blue"), R(-14, -4, 28, 3, "white"), R(-14, 3, 28, 3, "white")],
    "tap": [R(-15, 4, 22, 7, "grey"), R(2, -3, 7, 14, "grey"), R(-15, -4, 6, 12, "grey"), E(-5, 11, 5, 16, "dgrey"), C(-12, -9, 2.4, "blue"), C(-12, -15, 1.6, "blue")],
    "germ": [C(0, 0, 8, "green")] + [L(8 * math.cos(math.radians(a)), 8 * math.sin(math.radians(a)), 14 * math.cos(math.radians(a)), 14 * math.sin(math.radians(a)), "dgreen", 1.8) for a in range(0, 360, 45)] + [C(-3, 2, 1.4, "black"), C(3, 2, 1.4, "black"), A(-3, -4, 3, 1, 200, 140, "black", .8)],
    "tissue": [R(-12, -12, 24, 13, "lblue"), Pg([(-6, 1), (-3, 12), (2, 7), (5, 13), (7, 1)], "white")],
    "sunhat": [E(-17, -4, 17, 3, "yellow"), E(-9, -2, 9, 14, "yellow"), R(-9, 2, 18, 3, "red")],
    "sunscreen": [R(-6, -14, 12, 24, "yellow"), R(-4, 10, 8, 4, "white"), T(0, -2, "SUN", 6, "red"), C(0, -9, 2, "orange")],
    "talk": [E(-16, -8, 16, 12, "white"), Pg([(-9, -7), (-13, -16), (-3, -8)], "white"), C(-6, 2, 1.8, "dgrey"), C(0, 2, 1.8, "dgrey"), C(6, 2, 1.8, "dgrey")],
    "hug": [G(-6, -2, .72, P("orange", "skin", "brown")), G(6, -2, .72, P("blue", "skin3", "black")), C(-1, 1, 3, "red"), C(2, 1, 3, "red"), Pg([(-3.5, 0), (4.5, 0), (.5, -5)], "red")],
    "crayon": [Pg([(-3, -14), (3, -14), (3, 6), (0, 13), (-3, 6)], "red"), R(-3, -4, 6, 5, "white"), R(7, -12, 12, 16, "white"), L(9, -4, 17, -4, "blue", 1)],
    "music": [C(-5, -9, 4.2, "black"), C(7, -12, 4.2, "black"), L(-1, -9, -1, 12, "black", 2), L(11, -12, 11, 9, "black", 2), Pg([(-1, 12), (11, 9), (11, 5), (-1, 8)], "black")],
    "rope": [A(-14, -18, 14, 12, 180, 180, "red", 2.2), R(-17, -4, 5, 9, "brown"), R(12, -4, 5, 9, "brown")],
    "skates": [Pg([(-10, 14), (2, 14), (2, 0), (14, -2), (14, -10), (-10, -10)], "white"), R(-12, -13, 28, 3, "silver"), L(-10, -10, -10, -13, "dgrey", 1.6), L(14, -10, 14, -13, "dgrey", 1.6)],
    "ski": [Pg([(-18, -13), (18, -7), (18, -5), (-18, -11)], "red"), Pg([(-18, -2), (18, 4), (18, 6), (-18, 0)], "blue"), L(-10, 16, -4, -10, "grey", 1.6), L(10, 16, 4, -2, "grey", 1.6)],
    "sled": [R(-14, -8, 28, 5, "red"), A(-18, -8, -8, 6, 90, 120, "brown", 2.2), L(-14, 1, -14, -5, "brown", 1.4), L(14, 1, 14, -5, "brown", 1.4), L(-16, 0, 16, 9, "tan", 1.2)],
    "mittens": [E(-15, -11, -2, 9, "red"), E(-1, -11, 13, 9, "red"), C(-16, 0, 3.2, "red"), C(14, 0, 3.2, "red"), R(-15, -14, 13, 5, "white"), R(-1, -14, 14, 5, "white")],
    "toque": [E(-12, -6, 12, 15, "blue"), R(-13, -9, 26, 6, "white"), C(0, 16, 4, "white")],
    "snowboots": [Pg([(-10, 13), (2, 13), (2, -1), (14, -3), (14, -13), (-10, -13)], "blue"), R(-10, 9, 12, 5, "white")],
    "kite": [Pg([(0, 16), (10, 4), (0, -8), (-10, 4)], "red"), L(0, 16, 0, -8, "white", 1), L(-10, 4, 10, 4, "white", 1), L(0, -8, -4, -14, "brown", 1.2), C(-4, -14, 1.8, "blue"), C(-7, -18, 1.8, "yellow")],
    "whistle": [E(-12, -7, 6, 5, "silver"), R(4, -3, 12, 5, "silver"), C(-4, -1, 2.4, "dgrey"), L(-12, 3, -16, 12, "grey", 1)],
    "coach": [G(0, 0, .95, P("red", "skin2", "black", hat="cap", extra=[C(3, 3, 1.6, "silver"), L(3, 3, 1, 7, "grey", .8)]))],
    "turns": [G(-11, -2, .62, P("orange", "skin", "brown")), G(11, -2, .62, P("blue", "skin3", "black")), T(-11, 17, "1", 9, "red"), T(11, 17, "2", 9, "red")],
    "include": [G(-9, 4, .5, P("orange", "skin", "brown")), G(9, 4, .5, P("blue", "skin3", "black")), G(-9, -9, .5, P("green", "skin2", "black")), G(9, -9, .5, P("purple", "skin", "brown")), O(0, -2, 17, "grey", 1)],
    "team": [G(-12, -2, .6, P("red", "skin", "brown")), G(12, -2, .6, P("red", "skin3", "black")), G(0, 2, .6, P("red", "skin2", "black")), C(0, -14, 3.4, "orange")],
    "moon": [Pg([(12 * math.cos(math.radians(a)), 12 * math.sin(math.radians(a))) for a in range(70, 291, 20)] +
                [(6 + 10 * math.cos(math.radians(b)), 10 * math.sin(math.radians(b))) for b in range(250, 109, -20)], "yellow"), C(10, 10, 1.4, "yellow"), C(14, 3, 1, "yellow")],
})


def _bubble(name, text, size):
    ICONS[name] = [E(-19, -9, 19, 14, "white"), Pg([(-10, -7), (-14, -16), (-3, -9)], "white"), T(0, -1.5, text, size, "black")]


for _n, _t, _s in (("say_goodgame", "Good game!", 6.6), ("say_nicetry", "Nice try!", 7.5), ("say_play", "Can I play?", 6.6), ("say_cant", "You can't play!", 5.4),
                   ("breath_easy", "La la la!", 7.5), ("breath_talk", "Hello!", 8), ("breath_hard", "Huff, puff!", 6.8)):
    _bubble(_n, _t, _s)


def _faceplus(kind):
    base = [C(0, 0, 16, "yellow"), O(0, 0, 16, "orange", 1.2)]
    if kind == "worried":
        return base + [C(-5.5, 3, 2, "black"), C(5.5, 3, 2, "black"), L(-9, 8, -3, 10.5, "black", 1.6), L(9, 8, 3, 10.5, "black", 1.6), A(-6, -10, 6, -2, 30, 120, "black", 1.4)]
    return base + [C(-5.5, 4, 2, "black"), C(5.5, 4, 2, "black"), A(-8, -10, 8, 3, 200, 140, "black", 1.6), C(-10, -3, 2.6, "pink"), C(10, -3, 2.6, "pink"),
                   Pg([(0, 20), (1.6, 17), (5, 17), (2.4, 15), (3.4, 12), (0, 14), (-3.4, 12), (-2.4, 15), (-5, 17), (-1.6, 17)], "gold")]


ICONS["worried"] = _faceplus("worried")
ICONS["proud"] = _faceplus("proud")

LBL.update({
    "run": "running", "jump": "jumping", "hop": "hopping", "walk": "walking", "balance": "balancing", "stretch": "stretching", "bend": "bending",
    "throw": "throwing", "catch": "catching", "kick": "kicking", "bounce": "bouncing", "swim": "swimming", "dance": "dancing",
    "skiprope": "skipping rope", "sit_tv": "watching TV", "sleep": "sleeping", "eye": "eye", "ear": "ear", "nose": "nose", "hand": "hand",
    "foot": "foot", "heart": "heart", "lungs": "lungs", "carrot": "carrot", "broccoli": "broccoli", "banana": "banana", "orange": "orange",
    "rice": "rice", "egg": "egg", "beans": "beans", "juice": "juice box", "chips": "chips", "donut": "donut", "soap": "soap", "towel": "towel",
    "tap": "tap", "germ": "germ", "tissue": "tissue", "sunhat": "sun hat", "sunscreen": "sunscreen", "talk": "talk to someone", "hug": "hug",
    "crayon": "draw", "music": "music", "rope": "skipping rope", "skates": "skates", "ski": "skis", "sled": "sled", "mittens": "mittens",
    "toque": "warm hat", "snowboots": "snow boots", "kite": "kite", "whistle": "whistle", "coach": "coach", "turns": "taking turns",
    "include": "including everyone", "team": "team", "moon": "moon", "worried": "worried", "proud": "proud",
    "say_goodgame": "Good game!", "say_nicetry": "Nice try!", "say_play": "Can I play?", "say_cant": "You can't play!",
    "breath_easy": "La la la!", "breath_talk": "Hello!", "breath_hard": "Huff, puff!", "salmon": "salmon", "cake": "cake"})
