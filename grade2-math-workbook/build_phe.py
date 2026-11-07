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
NAMES = {1: "My Body & Physical Literacy", 2: "Fundamental Movement Skills", 3: "Ways to Be Active Every Day", 4: "How My Body Feels When I Move",
         5: "Healthy Eating & Energy", 6: "Healthy Habits & Preventing Illness", 7: "Feelings & Who I Am", 8: "Friends, Fair Play & Leadership",
         9: "Staying Safe & Getting Help", 10: "Healthy Living Together"}
LEVEL = {1: "Starter", 2: "Starter", 3: "Starter", 4: "Building", 5: "Building", 6: "Building", 7: "Stretch", 8: "Stretch", 9: "Stretch", 10: "Challenge"}
FOCUS = {1: "Physical literacy", 2: "Fundamental movement skills", 3: "Daily activity, 60-90 min", 4: "Exertion & effects of activity", 5: "Healthy eating choices",
         6: "Illness prevention practices", 7: "Emotions & self-identity", 8: "Safety, fair play, leadership", 9: "Safety strategies & support", 10: "Components of healthy living"}
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
    elif t == "exert":
        labels = ["cold", "getting warmer", "warm", "getting hot", "very hot"]
        sp = (w - 40) / 5
        for i in range(5):
            cx = x + 20 + sp * (i + .5)
            draw_icon(c, f"exert{i + 1}", cx, yt - 34, 46)
            c.setFillColor(black)
            c.setFont("Helvetica-Bold", 9.5)
            c.drawCentredString(cx, yt - 74, labels[i])
    else:
        _old_diagram(c, x, yt, w, h, data, **kw)


B.DRAW["diagram"] = d_diagram

BS.LESSON.clear()
BS.LESSON.update({
    1: dict(goal="I can name body parts and how moving helps my whole body.", vocab=["eye", "ear", "nose", "hand", "foot", "heart", "lungs", "run"],
            learn=["Moving every day helps all of our well-being.", "Learning different activities builds physical literacy.", "Each body part has a job."],
            ex=("pic", ("What do you use to see?", ["eye", "ear", "hand"]), "A"),
            tryit=[("pic", ("What do you use to kick?", ["hand", "foot", "ear"]), "B"), ("word", ("lungs", "What body part is this?  (heart / lungs / nose)"), "lungs")]),
    2: dict(goal="I can name movement skills: on the spot, travelling and with a ball.", vocab=["balance", "twist", "lift", "roll", "gallop", "bounce", "kick", "strike"],
            learn=["On the spot: balance, bend, twist, lift.", "Travelling: roll, jump, hop, run, gallop.", "With a ball: bounce, throw, catch, kick, strike."],
            ex=("word", ("gallop", "Which kind of move?  (travelling / with a ball)"), "travelling"),
            tryit=[("word", ("twist", "Which kind of move?  (on the spot / travelling)"), "on the spot"), ("pic", ("Which one is striking?", ["run", "strike", "balance"]), "B")]),
    3: dict(goal="I can name ways to be active and aim for 60 to 90 minutes a day.", vocab=["skiprope", "swim", "bike", "yoga", "hulahoop", "dance", "gymnastics", "tag"],
            learn=["Get 60 to 90 minutes of active play every day.", "Be active alone, with a partner, to music, or in games.", "Be active at school, at home and in your community."],
            ex=("word", ("swim", "Which kind of activity?  (alone or with a partner / rhythm / game with rules)"), "alone or with a partner"),
            tryit=[("word", ("tag", "Which kind of activity?  (rhythm / game with rules)"), "game with rules"), ("word", ("playground", "Where can you be active?  (at school / at home)"), "at school")]),
    4: dict(goal="I can tell how my body feels when I move, using the 1 to 5 scale.", vocab=["sweat", "breath_hard", "glass", "muscle", "happy", "exert1", "exert3", "exert5"],
            learn=["Active play makes us breathe harder, sweat and feel thirsty.", "Our muscles work and we feel good.", "Use the scale: 1 cold, 3 warm, 5 very hot."],
            ex=("pic", ("Which shows sweating?", ["sleep", "sweat", "glass"]), "B"),
            tryit=[("pic", ("Which number feels very hot?", ["exert1", "exert3", "exert5"]), "C"), ("pic", ("Which shows feeling thirsty?", ["glass", "happy", "muscle"]), "A")]),
    5: dict(goal="I can make healthy food choices and try a variety of foods.", vocab=["apple", "carrot", "broccoli", "bread", "rice", "egg", "salmon", "water"],
            learn=["Foods give us energy to grow, play and learn.", "Try a variety of foods.", "Make water your drink of choice."],
            ex=("word", ("apple", "Everyday or sometimes?  (everyday / sometimes)"), "everyday"),
            tryit=[("word", ("candy", "Everyday or sometimes?  (everyday / sometimes)"), "sometimes"), ("pic", ("Which drink is best every day?", ["juice", "water", "cake"]), "B")]),
    6: dict(goal="I can use healthy habits to stop germs and stay healthy.", vocab=["soap", "tap", "towel", "cough", "tissue", "sick", "bed", "house"],
            learn=["Wash your hands with soap and water.", "Cover your mouth when you cough.", "Rest and stay home when you are sick."],
            ex=("pic", ("What do you do when you cough?", ["cough", "ball", "kite"]), "A"),
            tryit=[("pic", ("Where do you stay when you are sick?", ["park", "house", "playground"]), "B"), ("word", ("soap", "Wash hands with soap?  (yes / no)"), "yes")]),
    7: dict(goal="I can name my feelings, manage them, and be proud of who I am.", vocab=["happy", "sad", "angry", "worried", "proud", "hug", "talk", "lungs"],
            learn=["All feelings are OK. We can manage them.", "Be proud of what you can do.", "Our body, feelings and thoughts are connected."],
            ex=("pic", ("Which face is sad?", ["happy", "sad", "angry"]), "B"),
            tryit=[("pic", ("What helps when you feel angry?", ["lungs", "kite", "tap"]), "A"), ("pic", ("You learned to ride a bike. How do you feel?", ["sad", "proud", "angry"]), "B")]),
    8: dict(goal="I can show fair play, kindness, listening and leadership.", vocab=["say_goodgame", "turns", "sharing", "include", "team", "coach", "ear", "talk"],
            learn=["Take turns, share and include everyone.", "Listen and use kind words.", "Leaders help others play safely and fairly."],
            ex=("pic", ("Which shows taking turns?", ["sharing", "turns", "team"]), "B"),
            tryit=[("pic", ("Who helps a team?", ["coach", "ball", "tap"]), "A"), ("pic", ("Which is a kind thing to say?", ["say_cant", "say_goodgame", "say_go"]), "B")]),
    9: dict(goal="I can stay safe and know who to ask for help.", vocab=["mom", "teacher", "doctor", "say_stop", "say_no", "phone", "medicine", "cleaner"],
            learn=["Trusted adults can help you.", "Use a strong voice: \u201cNo!\u201d \u201cStop!\u201d Then tell a trusted adult.", "Ask a trusted adult about medicine and cleaning sprays."],
            ex=("pic", ("Which is a strong voice for an unsafe moment?", ["say_hello", "say_stop", "say_thanks"]), "B"),
            tryit=[("pic", ("Who is a trusted adult you can ask?", ["teacher", "ball", "kite"]), "A"), ("pic", ("Which should only a trusted adult give you?", ["apple", "medicine", "milk"]), "B")]),
    10: dict(goal="I can put healthy living together: move, eat well, rest, stay clean and safe.", vocab=["run", "apple", "soap", "bed", "happy", "hug", "helmet", "water"],
             learn=["Healthy living: move, eat well, rest, stay clean.", "Feelings, friends and safety matter too.", "You can make healthy choices every day!"],
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
    c.drawCentredString(W / 2, 22, "Follows the BC Grade 2 Physical and Health Education curriculum. Not affiliated with Kumon.")
    b.page(footer=False)


def guide(b):
    c = b.c
    b.rec["guide"] = c.getPageNumber()
    b.banner("A Note for Parents & Teachers", "How to use this book")
    blocks = [
        ("A picture-first book, and a move-it book",
         ["Every question uses <b>pictures</b>. Read short questions aloud at first, then let your child lead.",
          "After each lesson, <b>do the moves for real</b>: run, jump, balance, throw and catch, wash hands the right way.",
          "Aim for <b>60 to 90 minutes of moderate to vigorous activity a day</b>. Count it together on the Unit 3 sheets.",
          "Ask your school or your local First Nations or Indigenous community about <b>traditional Aboriginal games</b> and try some together."]),
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
    b.box(M, b.y, W - 2 * M, 150, CREAM, Color(.9, .8, .5))
    q = Paragraph("<b>Follows the BC Grade 2 PHE curriculum.</b> The Big Ideas are: (1) daily moderate-to-vigorous activity benefits all aspects of our well-being; "
                  "(2) learning to move in different activities builds physical literacy; (3) healthy personal practices and safety strategies protect ourselves and others; "
                  "(4) good communication and managing emotions help healthy relationships; (5) our physical, emotional and mental health are interconnected. "
                  "Content covered: fundamental movement skills (on the spot, travelling, with objects), types of activity (individual and dual, rhythmic, games), monitoring exertion "
                  "(1\u20135 scale), effects of activity on the body, healthy eating, illness prevention, support and health information, safety strategies, medicine and poison safety, "
                  "emotions and self-identity. Check your own curriculum for exact wording. Kumon\u2019s own pages do not match its levels to school grades. Levels rise from "
                  "<b>Starter</b> (Units 1\u20133) to <b>Building</b> (4\u20136), <b>Stretch</b> (7\u20139) and <b>Challenge</b> (10).", SMALL)
    _, hh = q.wrap(W - 2 * M - 20, 1000)
    q.drawOn(c, M + 10, b.y - 8 - hh)
    b.page()


SKILLS = ["Name body parts and how they help me move", "Name moving skills: on the spot, travelling, with a ball", "Name ways to be active (60 to 90 minutes a day)",
          "Tell how my body feels when I move (1\u20135 scale)", "Make healthy food choices and try new foods", "Use healthy habits to stop germs",
          "Name feelings, manage them and be proud of who I am", "Show fair play, kindness and leadership", "Stay safe and know who to ask for help", "Put healthy living together"]


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
