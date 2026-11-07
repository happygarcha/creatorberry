#!/usr/bin/env python3
"""Builds Grade2_Science_Mastery_Workbook.pdf using the shared layout engine."""
import math
import sys
from reportlab.platypus import Paragraph
from reportlab.lib.colors import Color, black, white

import build_workbook as B
import build_english as BE          # reuses the qline / write / passage drawers
import science_generators as S
from build_workbook import (W, H, M, NAVY, TEAL, ORANGE, LIGHT, CREAM, MINT, GREY, SOFT, BLUE, BUL, SMALL)

OUT = sys.argv[1] if len(sys.argv) > 1 else "Grade2_Science_Mastery_Workbook.pdf"
TITLE = "Grade 2 Science Mastery Workbook"
GREEN = Color(.3, .65, .3)
BROWN = Color(.6, .42, .25)
SKY = Color(.75, .9, 1)

B.BOOK_TITLE = TITLE
B.STD_LABEL = "BC Science theme"
NAMES = {1: "Being a Scientist: Senses & Tools", 2: "Living Things & Plants", 3: "Animals & Their Habitats",
         4: "Life Cycles", 5: "Matter: Solids, Liquids & Gases", 6: "Changing Matter & the 3 Rs",
         7: "Water & the Water Cycle", 8: "Forces & Motion", 9: "Energy: Light, Sound & Heat",
         10: "Weather, Seasons & Earth"}
LEVEL = {1: "Starter", 2: "Starter", 3: "Starter", 4: "Building", 5: "Building", 6: "Building",
         7: "Stretch", 8: "Stretch", 9: "Stretch", 10: "Challenge"}
THEME = {1: "Questioning & observing", 2: "Living things & their needs", 3: "Animals & habitats", 4: "Life cycles",
         5: "Matter & materials", 6: "Matter can change", 7: "Water & the water cycle", 8: "Forces & motion",
         9: "Light, sound & heat", 10: "Weather, seasons & Earth"}
for d, src in ((B.UNIT_NAMES, NAMES), (B.UNIT_LEVEL, LEVEL), (B.UNIT_CC, THEME)):
    d.clear()
    d.update(src)
B.TOP_LABEL.update({"qline", "write", "passage", "diagram"})


# ----------------------------------------------------------------- drawings
def _label(c, x, y, s, size=8, color=black, bold=True):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    c.drawString(x, y, s)


def _tag(c, x, y, letter):
    c.setFillColor(white)
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.2)
    c.circle(x, y, 8, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(x, y - 3.5, letter)
    c.setStrokeColor(black)
    c.setLineWidth(1)


def plant(c, cx, gy, sc=1.0, names=False):
    c.saveState()
    c.translate(cx, gy)
    c.scale(sc, sc)
    c.setFillColor(BROWN)
    c.rect(-80, -45, 160, 45, fill=1, stroke=0)
    c.setStrokeColor(Color(.45, .3, .15))
    c.setLineWidth(2)
    for dx, dy in [(0, -35), (-14, -30), (14, -30), (-26, -22), (26, -22)]:
        c.line(0, 0, dx, dy)
    c.setStrokeColor(GREEN)
    c.setLineWidth(5)
    c.line(0, 0, 0, 92)
    c.setFillColor(GREEN)
    c.setStrokeColor(Color(.15, .45, .15))
    c.setLineWidth(1)
    c.ellipse(-40, 38, -3, 56, fill=1)
    c.ellipse(3, 52, 40, 70, fill=1)
    c.setFillColor(Color(1, .85, .2))
    for k in range(6):
        a = math.radians(k * 60)
        c.circle(9 * math.cos(a), 104 + 9 * math.sin(a), 6, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.circle(0, 104, 5, fill=1, stroke=0)
    c.setStrokeColor(black)
    if names:
        for (tx, ty, s_, lx, ly) in [(30, 112, "flower", 12, 108), (46, 54, "leaves", 40, 60), (-62, 22, "stem", -4, 22), (22, -30, "roots", 8, -30)]:
            c.setFillColor(black)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(tx, ty, s_) if tx > -20 else c.drawString(tx, ty, s_)
    else:
        for (tx, ty, L, lx, ly) in [(34, 112, "A", 12, 108), (58, 56, "B", 40, 62), (-30, 24, "C", -3, 24), (46, -24, "D", 20, -26)]:
            c.setLineWidth(1)
            c.line(tx - 7, ty - 3, lx, ly)
            _tag(c, tx, ty, L)
    c.restoreState()


def wcycle(c, cx, y, w, h, names=False, fs=9):
    x = cx - 150
    c.setFillColor(SKY)
    c.rect(x, y, 300, h, fill=1, stroke=0)
    c.setFillColor(Color(.3, .55, .9))
    c.rect(x, y, 300, 34, fill=1, stroke=0)
    c.setFillColor(Color(.45, .75, .4))
    c.rect(x, y + 34, 70, 16, fill=1, stroke=0)
    # sun
    sx, sy = x + 48, y + h - 36
    c.setFillColor(Color(1, .85, .2))
    c.setStrokeColor(Color(1, .7, .1))
    for k in range(12):
        a = math.radians(k * 30)
        c.line(sx + 18 * math.cos(a), sy + 18 * math.sin(a), sx + 27 * math.cos(a), sy + 27 * math.sin(a))
    c.circle(sx, sy, 15, fill=1, stroke=0)
    # cloud
    kx, ky = x + 215, y + h - 40
    c.setFillColor(white)
    for dx, dy, r in [(-22, 0, 14), (0, 8, 18), (22, 0, 14), (0, -4, 16)]:
        c.circle(kx + dx, ky + dy, r, fill=1, stroke=0)
    # rain
    c.setStrokeColor(Color(.2, .4, .9))
    c.setLineWidth(1.5)
    for dx in (-20, -6, 8, 22):
        c.line(kx + dx, ky - 24, kx + dx - 3, ky - 40)
        c.line(kx + dx - 3, ky - 48, kx + dx - 6, ky - 62)
    # evaporation arrows
    c.setStrokeColor(Color(.9, .4, .1))
    c.setLineWidth(2)
    for dx in (120, 150):
        c.line(x + dx, y + 38, x + dx, y + h - 70)
        p = c.beginPath()
        p.moveTo(x + dx - 5, y + h - 78)
        p.lineTo(x + dx + 5, y + h - 78)
        p.lineTo(x + dx, y + h - 66)
        p.close()
        c.setFillColor(Color(.9, .4, .1))
        c.drawPath(p, fill=1, stroke=0)
    c.setStrokeColor(black)
    c.setLineWidth(1)
    if names:
        _label(c, sx + 18, sy - 36, "Sun", fs)
        _label(c, kx - 20, ky + 28, "cloud", fs)
        _label(c, kx + 24, ky - 50, "rain", fs)
        _label(c, x + 100, y + 12, "lake / ocean", fs, white)
        _label(c, x + 160, y + 80, "vapour rises", fs - 1, Color(.6, .25, .05))
    else:
        _tag(c, sx + 32, sy - 22, "A")
        _tag(c, kx - 34, ky + 18, "B")
        _tag(c, kx + 34, ky - 38, "C")
        _tag(c, x + 200, y + 17, "D")


def d_diagram(c, x, yt, w, h, data, **_):
    cx = x + w / 2
    if data == "plant":
        plant(c, cx, yt - 120, 1.0)
    else:
        wcycle(c, cx, yt - h + 4, w, h - 8)


B.DRAW["diagram"] = d_diagram


# ----------------------------------------------------------------- lesson art
def art1(c, x, y, w, h):
    rows = [("eyes", "see", Color(.3, .6, .9)), ("ears", "hear", ORANGE), ("nose", "smell", GREEN), ("tongue", "taste", Color(.85, .35, .45)),
            ("skin", "touch", Color(.6, .45, .8))]
    for i, (o, a, col) in enumerate(rows):
        yy = y + h - 30 - i * 24
        c.setFillColor(col)
        c.circle(x + 20, yy + 4, 9, fill=1, stroke=0)
        _label(c, x + 36, yy, o, 11)
        _label(c, x + 90, yy, "to " + a, 11, GREY, False)
    _label(c, x + 8, y + h - 12, "The five senses", 9, GREY, False)


def art2(c, x, y, w, h):
    plant(c, x + w / 2, y + h - 100, 0.82, names=True)


def art3(c, x, y, w, h):
    rows = [("mammal", "fur"), ("bird", "feathers"), ("fish", "scales"), ("reptile", "dry scales"), ("amphibian", "moist skin"), ("insect", "6 legs")]
    for i, (a, b) in enumerate(rows):
        yy = y + h - 24 - i * 21
        c.setFillColor(LIGHT if i % 2 == 0 else white)
        c.rect(x + 4, yy - 5, w - 8, 18, fill=1, stroke=0)
        _label(c, x + 10, yy, a, 10)
        _label(c, x + 84, yy, b, 10, ORANGE)


def _arrow(c, x1, y1, x2, y2, col=NAVY, wd=1.6):
    c.setStrokeColor(col)
    c.setFillColor(col)
    c.setLineWidth(wd)
    c.line(x1, y1, x2, y2)
    a = math.atan2(y2 - y1, x2 - x1)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - 7 * math.cos(a - .4), y2 - 7 * math.sin(a - .4))
    p.lineTo(x2 - 7 * math.cos(a + .4), y2 - 7 * math.sin(a + .4))
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setStrokeColor(black)
    c.setLineWidth(1)


def art4(c, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2 + 8
    pts = [(cx, cy + 46, "egg"), (cx + 56, cy, "caterpillar"), (cx, cy - 46, "chrysalis"), (cx - 56, cy, "butterfly")]
    for i in range(4):
        a, b = pts[i], pts[(i + 1) % 4]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy)
        _arrow(c, a[0] + dx / d * 22, a[1] + dy / d * 22, b[0] - dx / d * 22, b[1] - dy / d * 22, ORANGE)
    for px, py, s_ in pts:
        c.setFillColor(LIGHT)
        c.setStrokeColor(NAVY)
        c.circle(px, py, 21, fill=1, stroke=1)
        _label(c, px - c.stringWidth(s_, "Helvetica-Bold", 7) / 2, py - 2.5, s_, 7)
    _label(c, x + 6, y + 4, "A butterfly life cycle", 9, GREY, False)


def art5(c, x, y, w, h):
    bw = 48
    for i, (nm, kind) in enumerate([("solid", "s"), ("liquid", "l"), ("gas", "g")]):
        bx = x + 6 + i * (bw + 6)
        c.setFillColor(white)
        c.rect(bx, y + 50, bw, bw + 6, fill=1, stroke=1)
        c.setFillColor(BLUE)
        if kind == "s":
            for r in range(4):
                for k in range(4):
                    c.circle(bx + 8 + k * 11, y + 58 + r * 12, 4.5, fill=1, stroke=0)
        elif kind == "l":
            pts = [(10, 10), (22, 12), (36, 9), (44, 14), (14, 24), (28, 22), (40, 26), (8, 36), (22, 34), (34, 38), (46, 32)]
            for px, py in pts:
                c.circle(bx + min(px, 42), y + 52 + py - 2, 4.5, fill=1, stroke=0)
            c.setFillColor(Color(.6, .8, 1))
        else:
            for px, py in [(10, 12), (38, 44), (24, 30), (40, 10), (8, 46), (30, 52)]:
                c.circle(bx + px, y + 54 + py, 4.5, fill=1, stroke=0)
        _label(c, bx + bw / 2 - c.stringWidth(nm, "Helvetica-Bold", 10) / 2, y + 34, nm, 10)
    _label(c, x + 6, y + 14, "Solid: tight, keeps its shape", 8, GREY, False)
    _label(c, x + 6, y + 4, "Gas: spreads out everywhere", 8, GREY, False)


def art6(c, x, y, w, h):
    for i, (nm, col) in enumerate([("ice", Color(.8, .92, 1)), ("water", Color(.6, .8, 1)), ("steam", Color(.92, .92, .92))]):
        bx = x + 6 + i * 56
        c.setFillColor(col)
        c.roundRect(bx, y + h - 60, 46, 28, 6, fill=1, stroke=1)
        _label(c, bx + 23 - c.stringWidth(nm, "Helvetica-Bold", 10) / 2, y + h - 50, nm, 10)
    _arrow(c, x + 52, y + h - 40, x + 62, y + h - 40, ORANGE)
    _arrow(c, x + 108, y + h - 40, x + 118, y + h - 40, ORANGE)
    _label(c, x + 8, y + h - 78, "melting", 9, ORANGE)
    _label(c, x + 64, y + h - 78, "evaporating", 9, ORANGE)
    _arrow(c, x + 120, y + h - 96, x + 60, y + h - 96, BLUE)
    _arrow(c, x + 60, y + h - 110, x + 8, y + h - 110, BLUE)
    _label(c, x + 64, y + h - 124, "condensing", 9, BLUE)
    _label(c, x + 8, y + h - 138, "freezing", 9, BLUE)


def art7(c, x, y, w, h):
    c.saveState()
    c.translate(x + 2, y + 8)
    c.scale(0.56, 0.56)
    wcycle(c, 150, 0, 300, 250, names=True, fs=15)
    c.restoreState()


def art8(c, x, y, w, h):
    c.setFillColor(Color(.85, .2, .2))
    c.rect(x + 14, y + h - 50, 60, 26, fill=1, stroke=1)
    c.setFillColor(BLUE)
    c.rect(x + 74, y + h - 50, 60, 26, fill=1, stroke=1)
    _label(c, x + 40, y + h - 42, "N", 14, white)
    _label(c, x + 100, y + h - 42, "S", 14, white)
    _arrow(c, x + 14, y + h - 80, x + 74, y + h - 80, ORANGE, 3)
    _label(c, x + 20, y + h - 96, "push", 10, ORANGE)
    _arrow(c, x + 134, y + h - 112, x + 74, y + h - 112, GREEN, 3)
    _label(c, x + 90, y + h - 128, "pull", 10, GREEN)


def art9(c, x, y, w, h):
    sx, sy = x + 32, y + h - 42
    c.setStrokeColor(Color(1, .7, .1))
    c.setLineWidth(1.5)
    for k in range(12):
        a = math.radians(k * 30)
        c.line(sx + 18 * math.cos(a), sy + 18 * math.sin(a), sx + 28 * math.cos(a), sy + 28 * math.sin(a))
    c.setFillColor(Color(1, .85, .2))
    c.circle(sx, sy, 14, fill=1, stroke=0)
    _label(c, x + 8, y + h - 90, "light + heat", 10, ORANGE)
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.6)
    for r in (10, 18, 26):
        c.arc(x + 100 - r, y + h - 40 - r, x + 100 + r, y + h - 40 + r, -40, 80)
    c.setFillColor(BLUE)
    c.circle(x + 98, y + h - 40, 3, fill=1, stroke=0)
    c.setStrokeColor(black)
    c.setLineWidth(1)
    _label(c, x + 92, y + h - 90, "sound", 10, BLUE)
    _label(c, x + 8, y + h - 120, "Sound is made by vibrations.", 9, GREY, False)


def art10(c, x, y, w, h):
    cx, cy, r = x + w / 2, y + h / 2 - 4, 52
    for i, (nm, col) in enumerate([("spring", Color(.6, .85, .5)), ("summer", Color(1, .9, .4)), ("fall", Color(.95, .6, .25)), ("winter", Color(.78, .9, 1))]):
        c.setFillColor(col)
        c.wedge(cx - r, cy - r, cx + r, cy + r, 90 - i * 90, -90, fill=1, stroke=1)
        a = math.radians(90 - i * 90 - 45)
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(cx + 30 * math.cos(a), cy + 30 * math.sin(a) - 3, nm)
    _label(c, x + 8, y + h - 12, "A year has four seasons", 9, GREY, False)


B.ART.clear()
B.ART.update({1: art1, 2: art2, 3: art3, 4: art4, 5: art5, 6: art6, 7: art7, 8: art8, 9: art9, 10: art10})

# ------------------------------------------------------------------- lessons
B.LESSONS.clear()
B.LESSONS.update({
    1: dict(goal="I can use my senses and simple tools to observe, measure and ask questions.",
            learn=["Scientists <b>observe</b> with their <b>senses</b>: eyes, ears, nose, tongue and skin. Never taste unknown things!",
                   "An <b>observation</b> is what you see, hear, smell or feel. An <b>opinion</b> is what you think.",
                   "Tools help us: <b>ruler</b> (length), <b>thermometer</b> (temperature), <b>balance</b> (mass), <b>measuring cup</b> (volume), <b>magnifying glass</b> (tiny things).",
                   "A <b>fair test</b> changes only one thing. Record what you find."],
            ex=[("Sense", ["~Hear a bell", "~Which body part?", "= ears"]), ("Observation", ["~The leaf is green.", "= observation", "~(you can see it)"]),
                ("Tool", ["~How long is a pencil?", "~Which tool?", "= ruler"])],
            tip="Look closely, ask “What if…?”, and write down what you see.",
            tryit=[("eq", [("You smell a flower with your ____.  (nose / ears)", "nose"), ("Which tool measures how hot the air is?  (thermometer / ruler)", "thermometer"),
                           ("Rocks are boring.  Observation or opinion?  ____", "opinion")], 1, 30)]),
    2: dict(goal="I can tell living from non-living things and name the parts of a plant.",
            learn=["<b>Living things</b> grow, need food, water and air, and can have young. A <b>non-living</b> thing (like a rock) does not.",
                   "Plants need <b>sunlight, water, air and soil</b> to grow.",
                   "<b>Roots</b> take in water. The <b>stem</b> holds the plant up. <b>Leaves</b> make food from sunlight. <b>Flowers</b> make seeds.",
                   "A <b>seed</b> can grow into a new plant."],
            ex=[("Living?", ["~A tree", "~grows and needs water", "= living"]), ("Plant parts", ["~Which part takes", "~in water?", "= roots"]),
                ("Food from plants", ["~A carrot is a", "= root"])],
            tip="Ask: does it grow, need food and air, and have babies?",
            tryit=[("eq", [("Is a bird living or non-living?  ____", "living"), ("Which part of a plant makes seeds?  (flower / roots)", "flower"),
                           ("Plants need sunlight, air, soil and ____.  (water / candy)", "water")], 1, 30)]),
    3: dict(goal="I can sort animals into groups and tell where they live and what they eat.",
            learn=["Animal groups: <b>mammals</b> (fur), <b>birds</b> (feathers), <b>fish</b> (scales), <b>reptiles</b> (dry scales), <b>amphibians</b> (moist skin), <b>insects</b> (6 legs).",
                   "A <b>habitat</b> is where an animal lives: land, water, or both.",
                   "<b>Herbivores</b> eat plants, <b>carnivores</b> eat animals, <b>omnivores</b> eat both.",
                   "An <b>adaptation</b> is a body part or behaviour that helps an animal survive."],
            ex=[("Group", ["~A salmon", "~scales, lives in water", "= fish"]), ("Diet", ["~A cow eats grass.", "= herbivore"]),
                ("Adaptation", ["~Webbed feet help", "~a duck to ____", "= swim"])],
            tip="Salmon, orcas and bears all live in BC. Which groups are they in?",
            tryit=[("eq", [("A dog is a ____.  (mammal / fish)", "mammal"), ("A frog is covered with ____.  (moist skin / fur)", "moist skin"),
                           ("A lion eats other animals. It is a ____.  (carnivore / herbivore)", "carnivore")], 1, 30)]),
    4: dict(goal="I can put life cycles in order and name the stages.",
            learn=["A <b>life cycle</b> shows how a living thing is born, grows, has young, and dies.",
                   "Butterfly: <b>egg, caterpillar, chrysalis, butterfly</b>. Frog: <b>egg, tadpole, froglet, frog</b>.",
                   "Plants: <b>seed, sprout, young plant, adult plant</b> (which makes new seeds).",
                   "Pacific salmon: <b>egg, alevin, fry, adult</b>. Adults return to the river to lay eggs.",
                   "Baby animals have names: puppy, kitten, calf, foal, lamb."],
            ex=[("Next stage", ["~Frog: egg, then", "= tadpole"]), ("Baby name", ["~A baby cow", "= calf"]),
                ("In order", ["egg, caterpillar,", "chrysalis,", "butterfly"])],
            tip="Say the stages in order, then check them off.",
            tryit=[("eq", [("In the butterfly life cycle, what comes just after the egg?  (caterpillar / chrysalis)", "caterpillar"),
                           ("A baby sheep is called a ____.  (lamb / foal)", "lamb"), ("A hen lays ____.  (eggs / seeds)", "eggs")], 1, 30)]),
    5: dict(goal="I can sort matter into solids, liquids and gases and describe materials.",
            learn=["<b>Matter</b> is anything that takes up space and has mass.",
                   "A <b>solid</b> keeps its shape. A <b>liquid</b> takes the shape of its container. A <b>gas</b> spreads out to fill its space.",
                   "<b>Properties</b> describe matter: hard, soft, rough, smooth, shiny, stretchy, waterproof.",
                   "Things are made of <b>materials</b>: metal, wood, glass, plastic, cloth, rubber, paper."],
            ex=[("State", ["~Milk", "~pours, takes the", "~shape of the cup: liquid"]), ("Float?", ["~A cork", "= floats"]),
                ("Material", ["~A window is", "~made of glass", "= transparent"])],
            tip="Squeeze it, pour it, spread it: which state is it?",
            tryit=[("eq", [("Is air a solid, a liquid, or a gas?  ____", "gas"), ("Will a coin float or sink?  ____", "sink"),
                           ("A raincoat is ____.  (waterproof / stretchy)", "waterproof")], 1, 30)]),
    6: dict(goal="I can describe how matter changes and sort waste into the right bins.",
            learn=["<b>Melting</b>: solid to liquid (heat). <b>Freezing</b>: liquid to solid (cold). <b>Evaporating</b>: liquid to gas. <b>Condensing</b>: gas to liquid.",
                   "Some changes can be <b>undone</b> (melting, freezing). Others cannot (baking, burning).",
                   "A <b>mixture</b> is two or more things put together. Some things <b>dissolve</b> (sugar), some do not (sand).",
                   "<b>Reduce, reuse, recycle.</b> Sort: compost (food scraps), recycle (cans, paper), garbage."],
            ex=[("Melting", ["~Ice in the sun", "= melts"]), ("Undo it?", ["~Baking a cake", "= cannot change", "back"]),
                ("Which bin?", ["~Banana peel", "= compost"])],
            tip="Heat melts, cold freezes. Can you go back? If yes, it is reversible.",
            tryit=[("eq", [("When ice gets warm, it ____.  (melts / freezes)", "melts"), ("Cooking an egg.  Can you change it back?  ____", "no"),
                           ("Which bin? a glass jar  (recycle / compost / garbage)  ____", "recycle")], 1, 30)]),
    7: dict(goal="I can describe the water cycle and say why water matters.",
            learn=["<b>All living things need water.</b> Many First Peoples teach that water is a gift to protect.",
                   "Water can be <b>ice</b> (solid), <b>water</b> (liquid) or <b>water vapour</b> (gas).",
                   "The <b>water cycle</b>: <b>evaporation</b> (Sun heats water), <b>condensation</b> (clouds form), <b>precipitation</b> (rain or snow), <b>collection</b> (rivers, lakes, ocean).",
                   "We save water by turning off the tap and keeping streams clean."],
            ex=[("Evaporation", ["~The Sun heats a puddle", "= water vapour"]), ("Precipitation", ["~Rain, snow, hail", "~falling from clouds"]),
                ("Save water", ["~Turn off the tap", "~while brushing"])],
            tip="Follow the arrows: up (evaporation), clouds (condensation), down (precipitation).",
            tryit=[("eq", [("Water vapour is a ____.  (gas / solid)", "gas"), ("Rain and snow are called ____.  (precipitation / evaporation)", "precipitation"),
                           ("Which saves water?  (turning off the tap / leaving the hose on)", "turning off the tap")], 1, 30)]),
    8: dict(goal="I can explain pushes, pulls, gravity, friction and magnets.",
            learn=["A <b>force</b> is a <b>push</b> or a <b>pull</b>. Forces can start, stop, speed up, slow down or turn an object.",
                   "A bigger force makes an object move faster or farther. Heavier objects are harder to move.",
                   "<b>Gravity</b> pulls things down toward the Earth. <b>Friction</b> slows things that rub together (rough surfaces have more).",
                   "<b>Magnets</b> pull on iron and steel. <b>Like poles push apart</b>; <b>opposite poles pull together</b>."],
            ex=[("Push or pull?", ["~Kick a ball", "= push"]), ("Gravity", ["~Drop a ball", "= it falls down"]),
                ("Magnet", ["~Iron nail", "= attracted"])],
            tip="No force, no change: an object at rest stays still until a force moves it.",
            tryit=[("eq", [("To open a drawer, you use a ____ (push / pull).", "pull"), ("Which has more friction?  (carpet / ice)", "carpet"),
                           ("Will a magnet pick up a wooden block?  ____", "no")], 1, 30)]),
    9: dict(goal="I can describe light, sound and heat and where energy comes from.",
            learn=["A <b>source of light</b> makes its own light: the Sun, a lamp, a flame. The Moon only <b>reflects</b> sunlight.",
                   "<b>Transparent</b> lets light through. <b>Translucent</b> lets some through. <b>Opaque</b> blocks light and makes a <b>shadow</b>.",
                   "<b>Sound</b> is made by <b>vibrations</b>. Sounds can be loud or quiet, high or low.",
                   "The <b>Sun</b> gives light and heat. Plants, animals and machines all use <b>energy</b>."],
            ex=[("Light source", ["~The Sun", "= makes light"]), ("Opaque", ["~A wooden door", "= blocks light"]),
                ("Sound", ["~A drum is hit", "= it vibrates"])],
            tip="Hold your hand on your throat and hum. Feel the vibration!",
            tryit=[("eq", [("Is a flashlight a source of light?  ____", "yes"), ("A tiny bell makes a ____ sound.  (high / low)", "high"),
                           ("The Sun gives us light and ____.  (heat / noise)", "heat")], 1, 30)]),
    10: dict(goal="I can describe weather and seasons, and plan a fair test.",
             learn=["<b>Weather</b> is what the air outside is like: sunny, cloudy, rainy, snowy, windy, stormy.",
                    "Weather tools: <b>thermometer</b> (temperature), <b>rain gauge</b> (rain), <b>wind sock</b> (wind direction).",
                    "<b>Four seasons:</b> spring, summer, fall, winter. Earth <b>spins</b> to make day and night.",
                    "To plan a <b>fair test</b>: ask a question, predict, change one thing, keep the rest the same, record, and tell what you found."],
             ex=[("Weather tool", ["~Temperature", "= thermometer"]), ("Season", ["~Leaves change color", "= fall"]),
                 ("Fair test", ["~Change one thing,", "~keep the rest", "~the same"])],
             tip="Keep a weather chart for one week. What do you notice?",
             tryit=[("eq", [("A wind sock shows which way the ____ blows.  (wind / rain)", "wind"), ("The season after winter is ____.  (spring / fall)", "spring"),
                            ("The Sun appears to rise in the ____.  (east / west)", "east")], 1, 30)]),
})


# ------------------------------------------------------------- front matter
def cover(b):
    c = b.c
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    cols = [ORANGE, TEAL, BLUE, Color(.95, .75, .2), Color(.85, .35, .45)]
    for i, ch in enumerate(["Sun", "Ice", "Air", "Bug", "Sea", "Leaf", "Rock", "Moon", "Seed", "Rain", "Heat", "Star", "Push", "Pull"]):
        x, y = 60 + (i % 7) * 82, 110 + (i // 7) * 92
        c.setFillColor(cols[i % len(cols)])
        c.circle(x, y, 29, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(x, y - 5, ch)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(W / 2, H - 170, "Grade 2")
    c.drawCentredString(W / 2, H - 222, "Science Mastery")
    c.drawCentredString(W / 2, H - 274, "Workbook")
    c.setFillColor(Color(1, .85, .5))
    c.setFont("Helvetica", 17)
    c.drawCentredString(W / 2, H - 316, "Observe, ask, test and discover – one small step a day")
    c.setFillColor(white)
    c.setFont("Helvetica", 13)
    for i, t in enumerate(["10 units  •  10 lessons  •  100 daily practice sheets",
                           "2 check-ups  •  full answer key  •  progress tracker  •  certificate"]):
        c.drawCentredString(W / 2, H - 358 - i * 20, t)
    c.roundRect(W / 2 - 150, H - 470, 300, 56, 10, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(W / 2 - 138, H - 448, "This workbook belongs to:")
    c.setLineWidth(1)
    c.line(W / 2 - 138, H - 462, W / 2 + 138, H - 462)
    c.setFillColor(Color(.8, .85, .95))
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(W / 2, 22, "Themes follow the Grade 2 science topics (life cycles, matter, water, forces, energy). "
                                  "Inspired by small-step learning; not affiliated with or endorsed by Kumon.")
    b.page(footer=False)


def guide(b):
    c = b.c
    b.rec["guide"] = c.getPageNumber()
    b.banner("A Note for Parents & Teachers", "How to use this book")
    blocks = [
        ("The method (small steps, repeated until mastered)",
         ["<b>Tiny steps.</b> Each sheet is only a little harder than the last, so a child almost always succeeds.",
          "<b>Learn, then practise.</b> Each unit opens with a one-page lesson with pictures and worked examples.",
          "<b>Ten short sheets per topic</b> (two a day: Sheet A, then Sheet B with new questions) build vocabulary and understanding.",
          "<b>Correct every mistake.</b> Check with the answer key and talk about why an answer is right."]),
        ("The weekly rhythm (about 12 weeks, 5 days a week, 10–15 minutes)",
         ["<b>Lesson day:</b> read the lesson together and do “Try it yourself”.",
          "<b>Days 1–4:</b> two practice sheets a day. Write the time at the top of each sheet.",
          "<b>Day 5:</b> a reading investigation plus mixed review. In Unit 10 it is an investigation-planning challenge.",
          "<b>Goal:</b> 90% or better. Below 80%? Repeat the sheet tomorrow (print a spare copy first).",
          "Take the Check-Up after Unit 5 and the Final Test at the end."]),
        ("Make it real",
         ["Science is learned by doing. Try one simple experiment a week: sink or float, melting ice, a bean in a cup, a magnet hunt.",
          "Keep a science notebook. Draw what you see and write one sentence.",
          "Go outside: look for animals, plants, weather and seasons near you.",
          "Always follow safety rules. Never taste or smell unknown things, and ask an adult before heating anything."])]
    for head, items in blocks:
        c.setFillColor(TEAL)
        c.setFont("Helvetica-Bold", 12.5)
        c.drawString(M, b.y - 12, head)
        b.y -= 22
        for it in items:
            p = Paragraph(it, BUL)
            _, hh = p.wrap(W - 2 * M - 14, 10000)
            c.setFillColor(ORANGE)
            c.circle(M + 4, b.y - 8, 2.5, fill=1, stroke=0)
            p.drawOn(c, M + 6, b.y - hh)
            b.y -= hh + 1
        b.y -= 8
    b.box(M, b.y, W - 2 * M, 62, CREAM, Color(.9, .8, .5))
    q = Paragraph("<b>About the levels:</b> Kumon’s own pages do not match its levels to school grades, so the topics here follow the main "
                  "Grade 2 science themes (life cycles, matter and how it changes, water, forces, energy). They are <b>not</b> a line-by-line copy of "
                  "any provincial document: please check your own curriculum for exact wording. Levels rise from <b>Starter</b> (Units 1–3) to "
                  "<b>Building</b> (4–6), <b>Stretch</b> (7–9) and <b>Challenge</b> (10).", SMALL)
    _, hh = q.wrap(W - 2 * M - 20, 1000)
    q.drawOn(c, M + 10, b.y - 8 - hh)
    b.page()


SKILLS = ["Use my senses and tools to observe and measure", "Tell living from non-living things; name plant parts",
          "Sort animals into groups and name their habitats", "Put life cycles in order",
          "Sort matter into solids, liquids and gases", "Explain how matter changes; sort waste",
          "Describe the water cycle", "Explain pushes, pulls, gravity and magnets",
          "Describe light, sound and heat", "Describe weather and seasons; plan a fair test"]


def build(path, pages):
    b = B.Book(path, pages)
    cover(b)
    guide(b)
    B.contents(b, pages)
    B.tracker(b, SKILLS)
    for u in range(1, 11):
        b.rec[f"u{u}"] = b.c.getPageNumber()
        b.lesson(u)
        A, Bs = S.unit_sheets(u, 0), S.unit_sheets(u, 1)
        for sa, sb in zip(A, Bs):
            b.sheet(sa, f"Unit {u} • Day {sa['day']}", "A")
            b.sheet(sb, f"Unit {u} • Day {sb['day']}", "B")
        if u == 5:
            b.rec["checkup"] = b.c.getPageNumber()
            b.sheet(S._longfix(S.checkup_a()), "")
    b.rec["final"] = b.c.getPageNumber()
    b.sheet(S._longfix(S.final_test()), "")
    B.certificate(b)
    B.answer_key(b)
    b.c.save()
    return b.rec


if __name__ == "__main__":
    rec = build(OUT, {})
    rec = build(OUT, rec)
    print("pages:", rec)
