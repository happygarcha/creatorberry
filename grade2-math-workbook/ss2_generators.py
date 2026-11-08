"""Social Studies (BC Grade 2) generators: official-content units, a mix of pictures, reading, writing and fill-in."""
import random
import ss2icons  # noqa: F401
import pheicons  # noqa: F401
import social_generators as SG
import mix
from english_generators import take, fit, ARROW, passage_sec
from generators import sec, sheet
from ss_text import BANK
from social_generators import PIC, PICF, WORD, WORDF, lw, pics, words, eqs, draw
from sticons import LBL

TITLES = {1: "What Community Means", 2: "Needs, Wants, Goods & Services", 3: "Community Leaders & Government", 4: "Maps, Directions & Symbols",
          5: "Communities Across Canada", 6: "Communities Around the World", 7: "First Peoples Communities & Cultures",
          8: "People & the Environment", 9: "Rights & Responsibilities", 10: "Change Over Time & Points of View"}
# (old picture unit, old day) used for the picture part of each new unit/day
MAP = {1: [(4, 1), (4, 2), (2, 3), (4, 4), (2, 5)], 2: [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5)], 3: [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5)],
       4: [(6, 2), (6, 3), (6, 4), (6, 3), (6, 5)], 5: [(9, 1), (2, 1), (9, 2), (9, 3), (9, 5)], 6: [(6, 1), (7, 1), (2, 1), (10, 4), (6, 5)],
       7: [(9, 4), (9, 2), (4, 1), (6, 1), (9, 5)], 8: [(8, 3), (4, 1), (4, 3), (6, 1), (8, 5)], 9: [(8, 1), (8, 2), (8, 3), (8, 4), (8, 5)],
       10: [(10, 1), (10, 2), (10, 3), (10, 4), (10, 5)]}
LEADER_PICS = [("Who leads a town or city?", "mayor", ["mayor", "ball", "kite"]), ("Where do leaders meet?", "townhall", ["townhall", "bed", "tub"]),
               ("What do people use to choose together?", "vote", ["vote", "ball", "soap"]), ("Who shares knowledge and stories?", "grandma", ["grandma", "ball", "game"]),
               ("Who keeps people safe?", "police", ["police", "game", "candy"]), ("Who puts out fires?", "firefighter", ["firefighter", "kite", "game"])]


def unit_sheets(u, variant=0):
    out = []
    for d in range(1, 6):
        ou, od = MAP[u][d - 1]
        rng = random.Random(u * 100 + d + variant * 1000)
        sh = SG.UNITS[ou](od, rng, variant)
        sh = dict(sh)
        sh["unit"], sh["day"], sh["title"] = u, d, TITLES[u]
        if u == 3 and d in (1, 5):     # leaders unit: add the leaders pictures
            sh["sections"] = [pics([PICF(rng, q, c, o) for q, c, o in take(LEADER_PICS * 2, 8, variant, f"s3p{d}")], "Leaders and helpers")] + list(sh["sections"])
        sh = mix.mixify(sh, BANK[u], u, d, variant)
        out.append(fit(sh))
    return out


def checkup_a():
    rng = random.Random(5555)
    s = [pics([PIC(rng, "Where do you borrow books?", "library", SG.PLACES), PIC(rng, "Where do you get well?", "hospital", SG.PLACES),
               PICF(rng, "Who leads a town or city?", "mayor", ["mayor", "ball", "kite"]), PICF(rng, "Where do leaders meet?", "townhall", ["townhall", "bed", "tub"])], "Community and leaders"),
         words([WORDF(rng, "apple", "need", ["need", "want"], "Need or want?"), WORDF(rng, "candy", "want", ["need", "want"], "Need or want?"),
                WORDF(rng, "bread", "good", ["good", "service"], "Good or service?"), WORDF(rng, "doctor", "service", ["good", "service"], "Good or service?")], "Needs, wants, goods, services")]
    for u in (1, 2, 3, 4, 5):
        s.append(mix.tf_sec(BANK[u], 2 if u in (1, 4) else 1, 0, f"ck{u}", "True or false?" if u == 1 else ""))
    s += mix.fill_secs(BANK[4], 3, 0, "ckf", "Fill in the blank")
    s += mix.read_secs(BANK[1], 0)
    return sheet(0, "A", "Check-Up: Units 1–5", "Show what you know! Do your best on every question.", "Aim for 90% or more before moving on to Unit 6.", s)


def final_test():
    rng = random.Random(5999)
    spec = {"type": "map", "rows": 3, "cols": 4, "cells": {(0, 0): "school", (0, 2): "park", (1, 1): "library", (1, 3): "store", (2, 0): "hospital", (2, 2): "bank"}, "deco": {(0, 3): "tree", (2, 3): "tree"}}
    s = [sec("Read the map", "diagram", [(spec, None)], 1, 176),
         eqs([("What is in row 1, column 1?  (school / bank / store)", "school"), ("What is east (right) of the library?  (park / store / bank)", "store")], ""),
         pics([PICF(rng, "Which is the Canadian flag?", "flag_canada", ["flag_canada", "flag_blue", "flag_green"]), PICF(rng, "Which did people paddle?", "canoe", ["canoe", "salmon", "cedar"]),
               PICF(rng, "Which helps the environment?", "bin_recycle", ["bin_recycle", "bin_trash", "stop"]), PICF(rng, "Which shows sharing?", "sharing", ["sharing", "ball", "game"])], "Canada, culture and care")]
    for u in (6, 7, 8, 9, 10):
        s.append(mix.tf_sec(BANK[u], 1, 1, f"ft{u}", "True or false?" if u == 6 else ""))
    s += mix.fill_secs(BANK[9], 3, 0, "ftf", "Fill in the blank")
    s += mix.read_secs(BANK[10], 1)
    return sheet(0, "F", "Final Test: Units 1–10", "You made it! Show everything you have learned.", "Aim for 90% or more. Then it's certificate time!", s)
