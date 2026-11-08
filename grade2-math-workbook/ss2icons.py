"""A few extra icons for the Social Studies workbook (leaders, globe...)."""
import math
from sticons import ICONS, LBL, R, C, E, Pg, L, O, A, T, G, P

ICONS.update({
    "mayor": [G(0, 0, .95, P("blue", "skin2", "black", extra=[A(-6, -1, 6, 9, 200, 140, "gold", 2), C(0, 0, 1.8, "gold")]))],
    "townhall": [R(-17, -14, 34, 22, "cream"), Pg([(-19, 8), (0, 16), (19, 8)], "grey"), R(-13, -14, 4, 22, "white"), R(-2, -14, 4, 22, "white"), R(9, -14, 4, 22, "white"),
                 L(0, 16, 0, 22, "dgrey", 1.2), R(0, 19, 7, 3, "red")],
    "vote": [R(-12, -14, 24, 18, "blue"), R(-6, 4, 12, 2.5, "dgrey"), Pg([(-5, 15), (5, 15), (5, 6), (-5, 6)], "white"), L(-3, 12, 3, 12, "grey", .8), L(-3, 9, 3, 9, "grey", .8)],
    "globe": [C(0, 0, 15, "blue"), Pg([(-8, 6), (-3, 10), (0, 4), (-4, -2), (-9, 0)], "green"), Pg([(3, 3), (9, 6), (11, -3), (5, -9), (2, -3)], "green"), O(0, 0, 15, "dgrey", 1.2)],
    "drum": [E(-13, 4, 13, 12, "tan"), R(-13, -9, 26, 14, "brown"), E(-13, -13, 13, -5, "brown"), L(-6, 8, -2, -9, "tan", 1), L(2, 8, 6, -9, "tan", 1), L(-14, 16, -4, 8, "grey", 1.5), L(14, 16, 4, 8, "grey", 1.5)],
})
LBL.update({"mayor": "mayor", "townhall": "town hall", "vote": "voting", "globe": "the world", "drum": "drum"})
