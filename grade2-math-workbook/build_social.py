#!/usr/bin/env python3
"""Builds Grade2_SocialStudies_Picture_Workbook.pdf (picture-first, minimal reading)."""
import math
import random
import sys
from reportlab.lib.utils import simpleSplit
from reportlab.platypus import Paragraph
from reportlab.lib.colors import Color, black, white
from reportlab.pdfbase.pdfmetrics import stringWidth

import build_workbook as B
import build_english as BE          # noqa: F401  (registers qline/write/passage drawers)
import social_generators as SG
import sticons as ST
from build_workbook import (W, H, M, NAVY, TEAL, ORANGE, LIGHT, CREAM, MINT, GREY, SOFT, BLUE, BUL, SMALL)
from sticons import LBL, ICONS, draw_icon

OUT = sys.argv[1] if len(sys.argv) > 1 else "Grade2_SocialStudies_Picture_Workbook.pdf"
TITLE = "Grade 2 Social Studies Picture Workbook"
B.BOOK_TITLE = TITLE
B.STD_LABEL = "BC Social Studies theme"
NAMES = {1: "All About Me & My Family", 2: "My Home & Neighbourhood", 3: "Community Helpers", 4: "Places in Our Community",
         5: "Needs, Wants & Money", 6: "Maps & Directions", 7: "Getting Around & Staying in Touch",
         8: "Rules, Safety & Being Kind", 9: "Canada, Celebrations & Our World", 10: "Past, Present & Time"}
LEVEL = {1: "Starter", 2: "Starter", 3: "Starter", 4: "Building", 5: "Building", 6: "Building",
         7: "Stretch", 8: "Stretch", 9: "Stretch", 10: "Challenge"}
THEME = {1: "Me, family, feelings", 2: "Homes & neighbourhoods", 3: "Roles in communities", 4: "Communities meet needs",
         5: "Needs, wants, goods", 6: "Maps & places", 7: "Communities then & now", 8: "Rights & responsibilities",
         9: "Canada & world cultures", 10: "Enrichment: time & change"}
for d, src in ((B.UNIT_NAMES, NAMES), (B.UNIT_LEVEL, LEVEL), (B.UNIT_CC, THEME)):
    d.clear()
    d.update(src)
B.TOP_LABEL.update({"pic", "picp", "word", "count", "coins", "people", "diagram", "draw"})

TAGCOL = [Color(.25, .5, .85), Color(.95, .55, .15), Color(.35, .7, .35), Color(.85, .35, .45)]


# ------------------------------------------------------------------- drawers
def _tag(c, x, y, letter, r=7.5, col=NAVY):
    c.setFillColor(white)
    c.setStrokeColor(col)
    c.setLineWidth(1.2)
    c.circle(x, y, r, fill=1, stroke=1)
    c.setFillColor(col)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(x, y - 3.2, letter)
    c.setStrokeColor(black)
    c.setLineWidth(1)


def _wrap(c, text, x, y, width, size=11.5, lead=13.5, font="Helvetica", maxlines=2):
    c.setFillColor(black)
    c.setFont(font, size)
    for i, ln in enumerate(simpleSplit(text, font, size, width)[:maxlines]):
        c.drawString(x, y - i * lead, ln)


def d_pic(c, x, yt, w, h, data, hi=None, **_):
    q, opts = data
    _wrap(c, q, x + 22, yt - 13, w - 28)
    n = len(opts)
    sp = (w - 30) / n
    for i, k in enumerate(opts):
        cx = x + 22 + sp * (i + .5)
        cy = yt - h + 38
        draw_icon(c, k, cx, cy, 40)
        _tag(c, cx, yt - h + 9, "ABCD"[i])
        if hi == i:
            c.setStrokeColor(Color(.1, .65, .2))
            c.setLineWidth(2.6)
            c.circle(cx, cy, 25, fill=0, stroke=1)
            c.setStrokeColor(black)
            c.setLineWidth(1)


def d_picp(c, x, yt, w, h, data, **_):
    q, shown, opts = data
    _wrap(c, q, x + 22, yt - 13, w - 28, maxlines=1)
    for i, k in enumerate(shown):
        draw_icon(c, k, x + 34 + i * 34, yt - 40, 28)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x + 34 + len(shown) * 34 - 12, yt - 45, "?")
    n = len(opts)
    sp = (w - 30) / n
    for i, k in enumerate(opts):
        cx = x + 22 + sp * (i + .5)
        draw_icon(c, k, cx, yt - h + 42, 36)
        _tag(c, cx, yt - h + 12, "ABCD"[i])


def d_word(c, x, yt, w, h, data, **_):
    key, text = data
    draw_icon(c, key, x + 40, yt - h / 2 - 1, 44)
    lines = simpleSplit(text, "Helvetica", 11.5, w - 82)[:3]
    y = yt - h / 2 + (len(lines) - 1) * 7 - 3
    c.setFillColor(black)
    c.setFont("Helvetica", 11.5)
    for i, ln in enumerate(lines):
        c.drawString(x + 70, y - i * 14, ln)


def d_count(c, x, yt, w, h, data, **_):
    key, n, text = data
    sp = min(26, (w - 40) / max(n, 1))
    for i in range(n):
        draw_icon(c, key, x + 30 + sp * i, yt - 22, min(24, sp - 1))
    _wrap(c, text, x + 22, yt - h + 10, w - 30, size=12, maxlines=1)


def d_coins(c, x, yt, w, h, data, **_):
    keys, text = data
    for i, k in enumerate(keys):
        draw_icon(c, k, x + 40 + i * 44, yt - 26, 40)
    _wrap(c, text, x + 22, yt - h + 10, w - 30, size=12, maxlines=1)


def _person(c, spec, cx, cy, size):
    prims = [ST.G(0, 0, .95, ST.P(spec["shirt"], spec["skin"], "black", hat=spec["hat"]))]
    c.saveState()
    c.translate(cx, cy)
    c.scale(size / 40.0, size / 40.0)
    ST._prims(c, prims)
    c.restoreState()


def d_people(c, x, yt, w, h, data, **_):
    specs, text = data
    for i, s in enumerate(specs):
        _person(c, s, x + 60 + i * 56, yt - 36, 46)
    _wrap(c, text, x + 22, yt - h + 10, w - 30, size=12, maxlines=1)


def d_draw(c, x, yt, w, h, data, **_):
    prompt = data
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 22, yt - 14, prompt)
    c.setStrokeColor(SOFT)
    c.setDash(4, 3)
    c.setLineWidth(1.3)
    c.roundRect(x + 4, yt - h + 4, w - 8, h - 28, 10, fill=0, stroke=1)
    c.setDash()
    c.setStrokeColor(black)
    c.setLineWidth(1)


def d_diagram(c, x, yt, w, h, data, **_):
    spec = data
    t = spec["type"]
    if t == "map":
        rows, cols, cw, ch_ = spec["rows"], spec["cols"], 64, 50
        gx, gy = x + (w - cols * cw) / 2 - 30, yt - 16
        for ci in range(cols):
            c.setFillColor(GREY)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(gx + ci * cw + cw / 2, gy + 3, str(ci + 1))
        for r in range(rows):
            c.setFillColor(GREY)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(gx - 12, gy - r * ch_ - ch_ / 2 - 3, str(r + 1))
            for ci in range(cols):
                c.setFillColor(Color(.88, .96, .85) if (r + ci) % 2 == 0 else Color(.93, .98, .9))
                c.setStrokeColor(Color(.62, .66, .7))
                c.setLineWidth(1)
                c.rect(gx + ci * cw, gy - (r + 1) * ch_, cw, ch_, fill=1, stroke=1)
                k = spec["cells"].get((r, ci)) or spec["deco"].get((r, ci))
                if k:
                    draw_icon(c, k, gx + ci * cw + cw / 2, gy - r * ch_ - ch_ / 2, 38 if k != "tree" else 30)
        cx, cy = gx + cols * cw + 46, yt - 82
        c.setStrokeColor(black)
        c.setLineWidth(1.5)
        c.line(cx - 22, cy, cx + 22, cy)
        c.line(cx, cy - 22, cx, cy + 22)
        p = c.beginPath()
        p.moveTo(cx, cy + 26)
        p.lineTo(cx - 6, cy + 14)
        p.lineTo(cx + 6, cy + 14)
        p.close()
        c.setFillColor(Color(.85, .2, .2))
        c.drawPath(p, fill=1, stroke=0)
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(cx, cy + 30, "N")
        c.drawCentredString(cx, cy - 36, "S")
        c.drawString(cx + 25, cy - 4, "E")
        c.drawString(cx - 33, cy - 4, "W")
        c.setLineWidth(1)
    elif t == "graph":
        items = spec["items"]
        gx, base = x + (w - 300) / 2 + 26, yt - 142
        mx = 8
        for v in range(0, mx + 1):
            yy = base + v * 14
            c.setStrokeColor(Color(.85, .87, .9))
            c.setLineWidth(.6)
            c.line(gx, yy, gx + 270, yy)
            c.setFillColor(GREY)
            c.setFont("Helvetica", 8)
            c.drawRightString(gx - 5, yy - 3, str(v))
        for i, (k, n) in enumerate(items):
            bx = gx + 20 + i * 90
            c.setFillColor(TAGCOL[i % 4])
            c.setStrokeColor(Color(.3, .3, .35))
            c.rect(bx, base, 54, n * 14, fill=1, stroke=1)
            draw_icon(c, k, bx + 27, base - 18, 30)
        c.setStrokeColor(black)
        c.setLineWidth(1)
    else:
        st, nd = spec["start"], spec["days"]
        gx, gy = x + (w - 280) / 2, yt - 18
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(x + w / 2, yt - 12, spec["month"])
        for i, d in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
            c.setFillColor(ORANGE)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(gx + i * 40 + 20, gy - 12, d)
        for d in range(1, nd + 1):
            idx = st + d - 1
            r, ci = divmod(idx, 7)
            c.setFillColor(LIGHT if ci in (0, 6) else white)
            c.setStrokeColor(SOFT)
            c.setLineWidth(.8)
            c.rect(gx + ci * 40, gy - 18 - (r + 1) * 18, 40, 18, fill=1, stroke=1)
            c.setFillColor(black)
            c.setFont("Helvetica", 9)
            c.drawCentredString(gx + ci * 40 + 20, gy - 18 - (r + 1) * 18 + 5, str(d))
        c.setStrokeColor(black)


B.DRAW.update({"pic": d_pic, "picp": d_picp, "word": d_word, "count": d_count, "coins": d_coins,
               "people": d_people, "draw": d_draw, "diagram": d_diagram})

# ------------------------------------------------------------------- lessons
LESSON = {
    1: dict(goal="I can name feelings and the people in my family.", vocab=["happy", "sad", "angry", "surprised", "tired", "mom", "dad", "baby"],
            learn=["Faces show how we feel.", "Families come in many shapes and sizes.", "It is OK to talk about our feelings."],
            ex=("pic", ("Which face is sad?", ["happy", "sad", "angry"]), "B"),
            tryit=[("pic", ("Which face is angry?", ["surprised", "happy", "angry"]), "C"), ("word", ("baby", "Who is this?  (baby / dad / mom)"), "baby")]),
    2: dict(goal="I can name kinds of homes and things in my home.", vocab=["house", "apartment", "tent", "houseboat", "bed", "stove", "tub", "sofa"],
            learn=["Homes can look very different.", "Each room has things we use.", "A neighbourhood has homes and places."],
            ex=("pic", ("Which home floats on water?", ["house", "houseboat", "tent"]), "B"),
            tryit=[("pic", ("What do you use to sleep?", ["stove", "bed", "tub"]), "B"), ("word", ("stove", "Which room?  (kitchen / bedroom)"), "kitchen")]),
    3: dict(goal="I can name community helpers and what they use.", vocab=["doctor", "teacher", "firefighter", "police", "mail", "builder", "farmer", "cook"],
            learn=["Helpers do jobs for us.", "Each helper uses special tools.", "Say thank you to a helper!"],
            ex=("pic", ("Which tool does a doctor use?", ["hose", "stethoscope", "hammer"]), "B"),
            tryit=[("word", ("firefighter", "Who is this helper?  (firefighter / cook / farmer)"), "firefighter"), ("pic", ("Where does a teacher work?", ["bank", "school", "park"]), "B")]),
    4: dict(goal="I can name places in my community and what they are for.", vocab=["school", "hospital", "library", "store", "park", "bank", "postoffice", "firehall"],
            learn=["A community has many places.", "Each place gives us something we need.", "People build places to help everyone."],
            ex=("pic", ("Where do you borrow books?", ["library", "bank", "park"]), "A"),
            tryit=[("pic", ("Where do you get well?", ["store", "hospital", "bank"]), "B"), ("word", ("park", "What place is this?  (park / school / bank)"), "park")]),
    5: dict(goal="I can tell needs from wants and count coins.", vocab=["apple", "bread", "coat", "bed", "candy", "game", "teddy", "ball"],
            learn=["Needs keep us alive: food, water, shelter, clothes.", "Wants are nice to have.", "We use money to buy goods and services."],
            ex=("word", ("apple", "Need or want?  (need / want)"), "need"),
            tryit=[("word", ("candy", "Need or want?  (need / want)"), "want"), ("coins", (["coin_dime", "coin_nickel"], "How much money?  ____"), "15¢")]),
    6: dict(goal="I can read a simple map and follow directions.", vocab=["mountain", "river", "lake", "ocean", "island", "forest", "arrow_up", "arrow_right"],
            learn=["A map is a picture of a place from above.", "North is up. East is right.", "Arrows show which way to go."],
            ex=("word", ("arrow_left", "Which way?  (left / right / up)"), "left"),
            tryit=[("word", ("island", "What is this?  (island / lake / mountain)"), "island"), ("word", ("arrow_down", "Which way?  (down / up / left)"), "down")]),
    7: dict(goal="I can sort vehicles and tell old things from new things.", vocab=["car", "bus", "train", "plane", "ferry", "canoe", "horsecart", "phone"],
            learn=["Vehicles go on land, water or air.", "Long ago, people used different things.", "We can send messages in many ways."],
            ex=("word", ("bus", "Where does it travel?  (land / water / air)"), "land"),
            tryit=[("word", ("ferry", "Where does it travel?  (land / water / air)"), "water"), ("pic", ("Which is newer?", ["horsecart", "car"]), "B")]),
    8: dict(goal="I can follow safety rules and be kind.", vocab=["stop", "trafficlight", "crosswalk", "helmet", "lifejacket", "umbrella", "say_thanks", "sharing"],
            learn=["Rules keep us safe.", "Wear the right safety gear.", "Kind words and sharing help everyone."],
            ex=("pic", ("What do you wear to ride a bike?", ["umbrella", "helmet", "shoe"]), "B"),
            tryit=[("pic", ("Which says thank you?", ["say_go", "say_thanks", "say_give"]), "B"), ("pic", ("Which tells cars to stop?", ["stop", "crosswalk", "helmet"]), "A")]),
    9: dict(goal="I can name Canadian symbols and ways people celebrate.", vocab=["flag_canada", "maple", "dogwood", "cedar", "canoe", "salmon", "cake", "fireworks"],
            learn=["Canada and BC have special symbols.", "People celebrate in many ways.", "We are all different and the same."],
            ex=("pic", ("Which is the Canadian flag?", ["flag_green", "flag_canada", "flag_blue"]), "B"),
            tryit=[("pic", ("Which is for a birthday?", ["cake", "pumpkin", "hose"]), "A"), ("pic", ("Which did people paddle?", ["salmon", "cedar", "canoe"]), "C")]),
    10: dict(goal="I can tell how people and seasons change over time.", vocab=["baby", "girl", "mom", "grandma", "flower", "sun", "leaf_fall", "snowflake"],
             learn=["People grow older.", "There are four seasons.", "Things change over time."],
             ex=("pic", ("Who is the oldest?", ["baby", "grandma", "mom"]), "B"),
             tryit=[("pic", ("Which season is cold and snowy?", ["sun", "snowflake", "flower"]), "B"), ("pic", ("Who is the youngest?", ["baby", "girl", "mom"]), "A")]),
}


def lesson(b, u):
    L = LESSON[u]
    c = b.c
    b.banner(f"Unit {u} Lesson: {NAMES[u]}", LEVEL[u])
    gh = 26
    b.box(M, b.y, W - 2 * M, gh, MINT, Color(.6, .85, .8))
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M + 10, b.y - 17, "My goal:")
    c.setFillColor(black)
    c.setFont("Helvetica", 11)
    c.drawString(M + 66, b.y - 17, L["goal"][:100])
    b.y -= gh + 10
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M, b.y - 12, "Look and learn")
    b.y -= 20
    pw, ph = W - 2 * M, 176
    b.box(M, b.y, pw, ph, LIGHT, SOFT)
    cell = pw / 4
    for i, k in enumerate(L["vocab"]):
        r, col = divmod(i, 4)
        cx, cy = M + col * cell + cell / 2, b.y - 46 - r * 84
        draw_icon(c, k, cx, cy, 56)
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawCentredString(cx, cy - 42, LBL.get(k, k))
    b.y -= ph + 10
    for t in L["learn"]:
        c.setFillColor(ORANGE)
        c.circle(M + 6, b.y - 8, 3, fill=1, stroke=0)
        c.setFillColor(black)
        c.setFont("Helvetica", 12)
        c.drawString(M + 16, b.y - 12, t)
        b.y -= 20
    b.y -= 6
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M, b.y - 12, "Example")
    b.y -= 20
    kind, data, ans = L["ex"]
    cw = (W - 2 * M) / 2
    b.box(M, b.y, cw, 96, white, Color(.6, .7, .85))
    if kind == "pic":
        d_pic(c, M, b.y, cw, 92, data, hi="ABCD".index(ans))
    else:
        d_word(c, M, b.y, cw, 62, data)
    c.setFillColor(Color(.1, .55, .2))
    c.setFont("Helvetica-Bold", 12)
    c.drawString(M + cw + 14, b.y - 36, f"Answer: {ans}" if kind != "pic" else f"Answer: {ans}  (circled)")
    b.y -= 106
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M, b.y - 12, "Try it yourself!  (answers are in the back)")
    b.y -= 22
    store, qn = [], 0
    groups = []
    for kind, data, ans in L["tryit"]:
        if groups and groups[-1][0] == kind:
            groups[-1][1].append((data, ans))
        else:
            groups.append((kind, [(data, ans)]))
    for kind, cells in groups:
        h = {"pic": 92, "word": 62, "coins": 74}[kind]
        qn = b.sections([SG.sec("", kind, cells, 2, h)], qn, store, f"Unit {u} Lesson")
    b.answers.append((f"Unit {u} Lesson: Try it", store))
    b.page()


# -------------------------------------------------------------- front matter
def cover(b):
    c = b.c
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    cols = [ORANGE, TEAL, BLUE, Color(.95, .75, .2), Color(.85, .35, .45)]
    for i, k in enumerate(["house", "school", "bus", "doctor", "flag_canada", "tree", "canoe", "apple", "firefighter", "sun", "library", "family", "ferry", "maple"]):
        x, y = 60 + (i % 7) * 82, 110 + (i // 7) * 92
        c.setFillColor(white)
        c.circle(x, y, 33, fill=1, stroke=0)
        c.setStrokeColor(cols[i % len(cols)])
        c.setLineWidth(4)
        c.circle(x, y, 33, fill=0, stroke=1)
        draw_icon(c, k, x, y, 46)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(W / 2, H - 170, "Grade 2")
    c.drawCentredString(W / 2, H - 222, "Social Studies")
    c.drawCentredString(W / 2, H - 274, "Picture Workbook")
    c.setFillColor(Color(1, .85, .5))
    c.setFont("Helvetica", 17)
    c.drawCentredString(W / 2, H - 316, "Look, think and discover our community and world")
    c.setFillColor(white)
    c.setFont("Helvetica", 13)
    for i, t in enumerate(["10 units  •  10 picture lessons  •  100 daily practice sheets",
                           "maps  •  graphs  •  coins  •  calendar  •  drawing  •  full answer key  •  certificate"]):
        c.drawCentredString(W / 2, H - 358 - i * 20, t)
    c.roundRect(W / 2 - 150, H - 470, 300, 56, 10, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(W / 2 - 138, H - 448, "This workbook belongs to:")
    c.setLineWidth(1)
    c.setStrokeColor(black)
    c.line(W / 2 - 138, H - 462, W / 2 + 138, H - 462)
    c.setFillColor(Color(.8, .85, .95))
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(W / 2, 22, "Themes follow the Grade 2 social studies ideas (communities, needs and wants, Canada and the world, rights and responsibilities). "
                                  "Not affiliated with Kumon.")
    b.page(footer=False)


def guide(b):
    c = b.c
    b.rec["guide"] = c.getPageNumber()
    b.banner("A Note for Parents & Teachers", "How to use this book")
    blocks = [
        ("A picture-first book (very little reading)",
         ["Every question uses <b>pictures</b>: circle the letter under the right picture, name a picture, count, read a map or graph.",
          "Read each short question aloud at first. Then let your child lead.",
          "Talk about the pictures. Ask “What do you see? Where have you seen this?”"]),
        ("The weekly rhythm (about 12 weeks, 5 days a week, 10–15 minutes)",
         ["<b>Lesson day:</b> look at the picture page together and try the two questions.",
          "<b>Days 1–4:</b> two practice sheets a day (Sheet A, then Sheet B with new pictures).",
          "<b>Day 5:</b> mixed review, then a <b>Draw it!</b> box. Let your child draw and tell you about it.",
          "<b>Goal:</b> 90% or better. Check with the answer key and fix any mistakes together.",
          "Take the Check-Up after Unit 5 and the Final Test at the end."]),
        ("Make it real",
         ["Walk around your neighbourhood and spot the places and helpers in this book.",
          "Look at a real map. Find north, a park, and your home.",
          "Count real coins and talk about needs, wants and sharing.",
          "Talk about how your family celebrates and what makes your community special."])]
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
    b.box(M, b.y, W - 2 * M, 84, CREAM, Color(.9, .8, .5))
    q = Paragraph("<b>About the levels:</b> Kumon’s own pages do not match its levels to school grades. The units follow the main Grade 2 social studies "
                  "ideas as published for BC: how communities meet needs and wants, Canada’s diverse communities and cultures (including First Peoples), and "
                  "rights and responsibilities. Unit 10 (past, present and time) is <b>enrichment</b>. Please check your own curriculum for exact wording. "
                  "Levels rise from <b>Starter</b> (Units 1–3) to <b>Building</b> (4–6), <b>Stretch</b> (7–9) and <b>Challenge</b> (10).", SMALL)
    _, hh = q.wrap(W - 2 * M - 20, 1000)
    q.drawOn(c, M + 10, b.y - 8 - hh)
    b.page()


SKILLS = ["Name feelings and family members", "Name homes and things in my home", "Name community helpers and their tools",
          "Name places in my community", "Tell needs from wants; count coins", "Read a simple map and follow arrows",
          "Sort vehicles; tell old from new", "Follow safety rules and be kind", "Name Canadian symbols and celebrations",
          "Tell how people and seasons change"]


def build(path, pages):
    b = B.Book(path, pages)
    cover(b)
    guide(b)
    B.contents(b, pages)
    B.tracker(b, SKILLS)
    for u in range(1, 11):
        b.rec[f"u{u}"] = b.c.getPageNumber()
        lesson(b, u)
        A, Bs = SG.unit_sheets(u, 0), SG.unit_sheets(u, 1)
        for sa, sb in zip(A, Bs):
            b.sheet(sa, f"Unit {u} • Day {sa['day']}", "A")
            b.sheet(sb, f"Unit {u} • Day {sb['day']}", "B")
        if u == 5:
            b.rec["checkup"] = b.c.getPageNumber()
            b.sheet(SG.checkup_a(), "")
    b.rec["final"] = b.c.getPageNumber()
    b.sheet(SG.final_test(), "")
    B.certificate(b)
    B.answer_key(b)
    b.c.save()
    return b.rec


if __name__ == "__main__":
    rec = build(OUT, {})
    rec = build(OUT, rec)
    print("pages:", rec)
