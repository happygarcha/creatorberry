#!/usr/bin/env python3
"""Builds Grade2_PHE_Picture_Workbook.pdf (Physical & Health Education, picture-first)."""
import math
import sys
from reportlab.platypus import Paragraph
from reportlab.lib.colors import Color, black, white

import build_workbook as B
import build_social as BS           # reuses the picture drawers and the picture-lesson layout
import phe_generators as PG
import pheicons  # noqa: F401
import sticons as ST
from build_workbook import (W, H, M, NAVY, TEAL, ORANGE, LIGHT, CREAM, MINT, GREY, SOFT, BLUE, BUL, SMALL)
from sticons import draw_icon

OUT = sys.argv[1] if len(sys.argv) > 1 else "Grade2_PHE_Picture_Workbook.pdf"
TITLE = "Grade 2 Health & Active Living Picture Workbook"
B.BOOK_TITLE = TITLE
B.STD_LABEL = "BC PHE focus"
NAMES = {1: "My Body & How It Moves", 2: "Moving Skills", 3: "Active Play Every Day", 4: "Heart, Breathing & Resting",
         5: "Healthy Eating", 6: "Healthy Habits & Staying Clean", 7: "Feelings & Well-Being", 8: "Friends, Fair Play & Leadership",
         9: "Outdoor Fun & Staying Safe", 10: "Moving Together: Review & Challenge"}
LEVEL = {1: "Starter", 2: "Starter", 3: "Starter", 4: "Building", 5: "Building", 6: "Building", 7: "Stretch", 8: "Stretch", 9: "Stretch", 10: "Challenge"}
FOCUS = {1: "Physical literacy", 2: "Fundamental movement skills", 3: "Daily physical activity", 4: "Monitoring exertion & rest",
         5: "Healthy eating choices", 6: "Healthy personal practices", 7: "Emotional well-being", 8: "Safety, fair play, leadership",
         9: "Safe, active outdoor play", 10: "Healthy, active me"}
for d, src in ((B.UNIT_NAMES, NAMES), (B.UNIT_LEVEL, LEVEL), (B.UNIT_CC, FOCUS)):
    d.clear()
    d.update(src)
BS.NAMES.clear()
BS.NAMES.update(NAMES)
BS.LEVEL.clear()
BS.LEVEL.update(LEVEL)

_old_diagram = BS.d_diagram


def d_diagram(c, x, yt, w, h, data, **kw):
    spec = data
    t = spec["type"]
    if t == "body":
        cx = x + w / 2 - 30
        c.saveState()
        c.translate(cx, yt - 100)
        c.scale(3.7, 3.7)
        ST._prims(c, [ST.G(0, 0, .95, ST.P("blue", "skin", "brown"))])
        c.restoreState()
        for L_, (tx, ty, ax, ay) in {"A": (cx + 70, yt - 20, cx + 16, yt - 40), "B": (cx + 86, yt - 88, cx + 40, yt - 92),
                                     "C": (cx + 70, yt - 128, cx + 12, yt - 130), "D": (cx + 60, yt - 160, cx + 14, yt - 158)}.items():
            c.setStrokeColor(Color(.4, .4, .45))
            c.setLineWidth(1)
            c.line(ax, ay, tx - 9, ty)
            BS._tag(c, tx, ty, L_, r=9)
        c.setStrokeColor(black)
    elif t == "plate":
        cx, cy, r = x + w / 2, yt - 88, 76
        c.setStrokeColor(Color(.5, .5, .55))
        c.setLineWidth(2)
        c.setFillColor(white)
        c.circle(cx, cy, r + 8, fill=1, stroke=1)
        for (st, ex, col, keys, lab) in ((90, 180, Color(.72, .9, .6), ["apple", "carrot", "broccoli", "banana"], "vegetables & fruits"),
                                          (270, 90, Color(.72, .9, .6), [], ""),
                                          (0, -90, Color(1, .92, .6), ["bread", "rice"], "grains"),
                                          (-90, -90, Color(1, .75, .7), ["egg", "salmon", "beans"], "protein")):
            pass
        # half: vegetables & fruits (left), quarters on the right
        c.setFillColor(Color(.72, .9, .6))
        c.wedge(cx - r, cy - r, cx + r, cy + r, 90, 180, fill=1, stroke=1)
        c.setFillColor(Color(1, .92, .6))
        c.wedge(cx - r, cy - r, cx + r, cy + r, 0, 90, fill=1, stroke=1)
        c.setFillColor(Color(1, .75, .7))
        c.wedge(cx - r, cy - r, cx + r, cy + r, -90, 90, fill=1, stroke=1)
        for k, (ix, iy) in zip(["apple", "carrot", "broccoli", "banana"], [(-44, 26), (-22, -4), (-48, -26), (-16, 38)]):
            draw_icon(c, k, cx + ix, cy + iy, 34)
        for k, (ix, iy) in zip(["bread", "rice"], [(26, 40), (50, 22)]):
            draw_icon(c, k, cx + ix, cy + iy, 32)
        for k, (ix, iy) in zip(["egg", "salmon", "beans"], [(24, -20), (50, -22), (36, -50)]):
            draw_icon(c, k, cx + ix, cy + iy, 30)
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(cx - r - 100, cy + 4, "vegetables")
        c.drawString(cx - r - 100, cy - 8, "& fruits")
        c.drawString(cx + r + 14, cy + 40, "grains")
        c.drawString(cx + r + 14, cy - 40, "protein")
        c.setStrokeColor(black)
        c.setLineWidth(1)
    else:
        _old_diagram(c, x, yt, w, h, data, **kw)


B.DRAW["diagram"] = d_diagram

BS.LESSON.clear()
BS.LESSON.update({
    1: dict(goal="I can name body parts and how they help me move.", vocab=["eye", "ear", "nose", "hand", "foot", "heart", "lungs", "run"],
            learn=["Our bodies are made to move.", "Each body part has a job.", "Moving every day helps us grow strong."],
            ex=("pic", ("What do you use to see?", ["eye", "ear", "hand"]), "A"),
            tryit=[("pic", ("What do you use to kick?", ["hand", "foot", "ear"]), "B"), ("word", ("lungs", "What body part is this?  (heart / lungs / nose)"), "lungs")]),
    2: dict(goal="I can name moving skills: travelling, balancing and ball skills.", vocab=["run", "jump", "hop", "balance", "stretch", "throw", "catch", "kick"],
            learn=["Travelling moves go from place to place.", "Balance and stretch stay in one place.", "Throw, catch, kick and bounce are ball skills."],
            ex=("word", ("jump", "Which kind of move?  (travel / ball skill)"), "travel"),
            tryit=[("word", ("catch", "Which kind of move?  (travel / ball skill)"), "ball skill"), ("pic", ("Which one is balancing?", ["run", "balance", "kick"]), "B")]),
    3: dict(goal="I can tell active play from not active, and aim for 60 minutes a day.", vocab=["run", "swim", "dance", "skiprope", "bike", "canoe", "sit_tv", "sleep"],
            learn=["Be active about 60 minutes every day.", "Active play makes our bodies strong.", "Find fun ways to move with family and friends."],
            ex=("word", ("swim", "Active or not?  (active / not active)"), "active"),
            tryit=[("word", ("sit_tv", "Active or not?  (active / not active)"), "not active"), ("pic", ("Which is more active?", ["sleep", "dance"]), "B")]),
    4: dict(goal="I can tell how active play changes my heart and breathing.", vocab=["heart", "lungs", "run", "sleep", "bed", "water", "breath_hard", "breath_easy"],
            learn=["Hard play makes your heart beat faster.", "If you cannot talk, slow down.", "Rest and water help your body."],
            ex=("pic", ("Which makes your heart beat fastest?", ["sit_tv", "run", "sleep"]), "B"),
            tryit=[("word", ("sleep", "Does your heart beat faster or slower?  (faster / slower)"), "slower"), ("pic", ("Which pumps blood?", ["lungs", "heart", "hand"]), "B")]),
    5: dict(goal="I can make healthy food choices.", vocab=["apple", "carrot", "broccoli", "bread", "rice", "egg", "salmon", "water"],
            learn=["Eat vegetables, fruits, whole grains and protein.", "Make water your drink of choice.", "Some foods are for sometimes."],
            ex=("word", ("apple", "Everyday or sometimes?  (everyday / sometimes)"), "everyday"),
            tryit=[("word", ("candy", "Everyday or sometimes?  (everyday / sometimes)"), "sometimes"), ("pic", ("Which drink is best every day?", ["juice", "water", "cake"]), "B")]),
    6: dict(goal="I can use healthy habits to stay clean and protect others.", vocab=["soap", "tap", "towel", "toothbrush", "tissue", "germ", "sunhat", "sunscreen"],
            learn=["Wash hands with soap and water.", "Brush teeth and cover sneezes.", "Healthy habits protect you and others."],
            ex=("pic", ("What do you use to wash your hands?", ["towel", "soap", "tissue"]), "B"),
            tryit=[("pic", ("What cleans your teeth?", ["toothbrush", "tissue", "tap"]), "A"), ("word", ("soap", "Wash hands with soap?  (yes / no)"), "yes")]),
    7: dict(goal="I can name feelings and ideas that help me feel better.", vocab=["happy", "sad", "angry", "surprised", "tired", "worried", "proud", "hug"],
            learn=["All feelings are OK.", "Our feelings and our bodies are connected.", "Move, rest, breathe or talk to feel better."],
            ex=("pic", ("Which face is sad?", ["happy", "sad", "angry"]), "B"),
            tryit=[("pic", ("What helps when you feel angry?", ["lungs", "kite", "tap"]), "A"), ("pic", ("What helps when you feel sad?", ["hug", "ball", "run"]), "A")]),
    8: dict(goal="I can show fair play, kindness and leadership.", vocab=["say_goodgame", "say_nicetry", "turns", "sharing", "include", "team", "coach", "whistle"],
            learn=["Take turns and share.", "Include everyone and use kind words.", "Leaders help others play safely."],
            ex=("pic", ("Which shows taking turns?", ["sharing", "turns", "team"]), "B"),
            tryit=[("pic", ("Who helps a team?", ["coach", "ball", "tap"]), "A"), ("pic", ("Which is a kind thing to say?", ["say_cant", "say_goodgame", "say_go"]), "B")]),
    9: dict(goal="I can play outdoors safely in every season.", vocab=["ski", "sled", "canoe", "kite", "toque", "mittens", "sunhat", "lifejacket"],
            learn=["Play outside in every season.", "Dress for the weather and stay safe.", "Care for nature and water."],
            ex=("pic", ("What do you wear in the snow?", ["sunhat", "toque", "lifejacket"]), "B"),
            tryit=[("pic", ("What do you wear near deep water?", ["lifejacket", "toque", "mittens"]), "A"), ("pic", ("What do you put on in the sun?", ["mittens", "sunscreen", "toque"]), "B")]),
    10: dict(goal="I can plan a healthy, active day.", vocab=["stretch", "run", "walk", "water", "bed", "apple", "soap", "happy"],
             learn=["A healthy day: move, eat well, rest, stay clean.", "Feelings, body and friends all matter.", "You can make healthy choices!"],
             ex=("pic", ("What is a good warm-up?", ["stretch", "sit_tv", "sleep"]), "A"),
             tryit=[("pic", ("What helps you rest?", ["run", "bed", "kite"]), "B"), ("pic", ("What do you drink after play?", ["candy", "juice", "water"]), "C")]),
})


def cover(b):
    c = b.c
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    cols = [ORANGE, TEAL, BLUE, Color(.95, .75, .2), Color(.85, .35, .45)]
    for i, k in enumerate(["run", "jump", "swim", "apple", "heart", "soap", "happy", "kick", "balance", "carrot", "dance", "water", "skiprope", "ski"]):
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
    c.drawCentredString(W / 2, H - 222, "Health & Active")
    c.drawCentredString(W / 2, H - 274, "Living Workbook")
    c.setFillColor(Color(1, .85, .5))
    c.setFont("Helvetica", 17)
    c.drawCentredString(W / 2, H - 316, "Move, eat well, rest and feel good – every day")
    c.setFillColor(white)
    c.setFont("Helvetica", 13)
    for i, t in enumerate(["10 units  •  10 picture lessons  •  100 daily practice sheets",
                           "Physical & Health Education  •  full answer key  •  certificate"]):
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
    c.drawCentredString(W / 2, 22, "Themes follow Grade 2 Physical and Health Education (physical literacy, daily activity, healthy choices, safety and fair play). Not affiliated with Kumon.")
    b.page(footer=False)


def guide(b):
    c = b.c
    b.rec["guide"] = c.getPageNumber()
    b.banner("A Note for Parents & Teachers", "How to use this book")
    blocks = [
        ("A picture-first book, and a move-it book",
         ["Every question uses <b>pictures</b>. Read short questions aloud at first, then let your child lead.",
          "After each lesson, <b>do the moves for real</b>: run, jump, balance, throw and catch, wash hands the right way.",
          "Aim for about <b>60 minutes of active play a day</b>. Count it together on the Unit 3 sheets."]),
        ("The weekly rhythm (about 12 weeks, 5 days a week, 10–15 minutes)",
         ["<b>Lesson day:</b> look at the picture page, try the two questions, then move together.",
          "<b>Days 1–4:</b> two practice sheets a day (Sheet A, then Sheet B with new pictures).",
          "<b>Day 5:</b> mixed review, then a <b>Draw it!</b> box.",
          "<b>Goal:</b> 90% or better. Check with the answer key and fix mistakes together.",
          "Take the Check-Up after Unit 5 and the Final Test at the end."]),
        ("Safety first",
         ["Do active games in a safe space with an adult nearby. Match activities to your child’s health and abilities.",
          "Talk about safe choices outdoors: helmets, life jackets, sun protection and crossing streets."])]
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
    b.box(M, b.y, W - 2 * M, 108, CREAM, Color(.9, .8, .5))
    q = Paragraph("<b>About the BC curriculum:</b> The units follow the Grade 2 Physical and Health Education ideas I could confirm for BC: daily moderate-to-vigorous "
                  "activity and its benefits, learning fundamental movement skills, monitoring exertion, safety, fair play and leadership, healthy eating choices, "
                  "healthy personal practices that protect ourselves and others, and the link between physical, emotional and mental health. I could not open the "
                  "official page for exact wording, so please check it against your own curriculum. Kumon’s own pages do not match its levels to school "
                  "grades. Levels rise from <b>Starter</b> (Units 1–3) to <b>Building</b> (4–6), <b>Stretch</b> (7–9) and <b>Challenge</b> (10).", SMALL)
    _, hh = q.wrap(W - 2 * M - 20, 1000)
    q.drawOn(c, M + 10, b.y - 8 - hh)
    b.page()


SKILLS = ["Name body parts and how they help me move", "Name moving skills: travel, balance, ball skills", "Tell active play from not active (60 minutes a day)",
          "Tell how my heart and breathing change", "Make healthy food choices", "Use healthy habits to stay clean",
          "Name feelings and ways to feel better", "Show fair play, kindness and leadership", "Play outdoors safely in every season", "Plan a healthy, active day"]


def build(path, pages):
    b = B.Book(path, pages)
    cover(b)
    guide(b)
    B.contents(b, pages)
    B.tracker(b, SKILLS)
    for u in range(1, 11):
        b.rec[f"u{u}"] = b.c.getPageNumber()
        BS.lesson(b, u)
        A, Bs = PG.unit_sheets(u, 0), PG.unit_sheets(u, 1)
        for sa, sb in zip(A, Bs):
            b.sheet(sa, f"Unit {u} • Day {sa['day']}", "A")
            b.sheet(sb, f"Unit {u} • Day {sb['day']}", "B")
        if u == 5:
            b.rec["checkup"] = b.c.getPageNumber()
            b.sheet(PG.checkup_a(), "")
    b.rec["final"] = b.c.getPageNumber()
    b.sheet(PG.final_test(), "")
    B.certificate(b)
    B.answer_key(b)
    b.c.save()
    return b.rec


if __name__ == "__main__":
    rec = build(OUT, {})
    rec = build(OUT, rec)
    print("pages:", rec)
