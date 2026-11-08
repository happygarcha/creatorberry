#!/usr/bin/env python3
"""Builds Grade2_SocialStudies_Workbook.pdf: BC Grade 2 Social Studies, a mix of pictures, reading, writing and fill-in."""
import sys
from reportlab.platypus import Paragraph
from reportlab.lib.colors import Color, black, white

import build_workbook as B
import build_social as BS           # picture drawers + picture-lesson layout
import mixdraw  # noqa: F401
import ss2icons  # noqa: F401
import pheicons  # noqa: F401
import ss2_generators as S2
from build_workbook import (W, H, M, NAVY, TEAL, ORANGE, LIGHT, CREAM, MINT, GREY, SOFT, BLUE, BUL, SMALL)
from sticons import draw_icon

OUT = sys.argv[1] if len(sys.argv) > 1 else "Grade2_SocialStudies_Workbook.pdf"
TITLE = "Grade 2 Social Studies Workbook"
B.BOOK_TITLE = TITLE
B.STD_LABEL = "BC Social Studies content"
NAMES = S2.TITLES
LEVEL = {1: "Starter", 2: "Starter", 3: "Starter", 4: "Building", 5: "Building", 6: "Building", 7: "Stretch", 8: "Stretch", 9: "Stretch", 10: "Challenge"}
FOCUS = {1: "Communities & cultures", 2: "Needs & wants met", 3: "Regional government", 4: "Maps: directions & legends", 5: "Canada's diverse regions",
         6: "Features of the world", 7: "First Peoples cultures", 8: "People & environment", 9: "Rights & responsibilities", 10: "Change & perspectives"}
for d, src in ((B.UNIT_NAMES, NAMES), (B.UNIT_LEVEL, LEVEL), (B.UNIT_CC, FOCUS)):
    d.clear()
    d.update(src)
BS.NAMES.clear()
BS.NAMES.update(NAMES)
BS.LEVEL.clear()
BS.LEVEL.update(LEVEL)

BS.LESSON.clear()
BS.LESSON.update({
    1: dict(goal="I can tell what a community is and name its places and jobs.", vocab=["school", "hospital", "library", "store", "park", "bus", "house", "apartment"],
            learn=["A community is a group of people who live, work and play in one area.", "Communities have homes, schools, jobs, services and ways to travel.", "People in a community can have different cultures."],
            ex=("pic", ("Where do you borrow books?", ["library", "bank", "park"]), "A"),
            tryit=[("pic", ("Where do you get well?", ["store", "hospital", "bank"]), "B"), ("word", ("school", "What place is this?  (park / school / bank)"), "school")]),
    2: dict(goal="I can tell needs from wants, and goods from services.", vocab=["apple", "coat", "bed", "house", "ball", "teddy", "doctor", "coin_loonie"],
            learn=["Needs are food, water, shelter, and love and friendship.", "Wants are nice to have. A good is a thing; a service is work done for you.", "Communities help people who cannot meet their needs."],
            ex=("word", ("apple", "Need or want?  (need / want)"), "need"),
            tryit=[("word", ("candy", "Need or want?  (need / want)"), "want"), ("word", ("doctor", "Good or service?  (good / service)"), "service")]),
    3: dict(goal="I can name community leaders and what they do.", vocab=["mayor", "townhall", "vote", "police", "firefighter", "grandma", "grandpa", "mail"],
            learn=["A mayor and a council help make decisions.", "Elders, chiefs and volunteers are leaders too.", "Groups can choose by voting, talking it out, or asking a leader."],
            ex=("pic", ("Who leads a town or city?", ["ball", "mayor", "kite"]), "B"),
            tryit=[("pic", ("Where do leaders meet?", ["bed", "townhall", "tub"]), "B"), ("pic", ("Who puts out fires?", ["firefighter", "kite", "game"]), "A")]),
    4: dict(goal="I can read a simple map using directions, symbols and a legend.", vocab=["arrow_up", "arrow_right", "school", "park", "hospital", "library", "tree", "store"],
            learn=["North is up, south is down, east is right, west is left.", "A symbol stands for a place. A legend tells what it means.", "You can make a map of a place you know."],
            ex=("word", ("arrow_left", "Which way?  (left / right / up)"), "left"),
            tryit=[("word", ("school", "What place is this?  (park / school / bank)"), "school"), ("word", ("arrow_down", "Which way?  (down / up / left)"), "down")]),
    5: dict(goal="I can tell how communities across Canada are different and the same.", vocab=["flag_canada", "maple", "mountain", "ocean", "barn", "apartment", "snowflake", "forest"],
            learn=["Canada has many regions and communities.", "Coast, prairie, mountain, northern and city communities live in different ways.", "All people need food, water and shelter."],
            ex=("pic", ("Which is the Canadian flag?", ["flag_green", "flag_canada", "flag_blue"]), "B"),
            tryit=[("pic", ("Which is a maple leaf?", ["maple", "flower", "tree"]), "A"), ("word", ("barn", "Where would you see this?  (on a farm / in the ocean)"), "on a farm")]),
    6: dict(goal="I can describe places around the world and how people live there.", vocab=["sun", "snowflake", "umbrella", "mountain", "island", "ocean", "tent", "houseboat"],
            learn=["The world has hot, cold, wet and dry places.", "Mountains, rivers, lakes and oceans are found all over the world.", "People build homes and dress to fit where they live."],
            ex=("pic", ("Which shows a cold place?", ["sun", "snowflake", "umbrella"]), "B"),
            tryit=[("word", ("island", "What is this?  (island / lake / mountain)"), "island"), ("pic", ("Which shows rain?", ["umbrella", "sun", "snowflake"]), "A")]),
    7: dict(goal="I can name ways First Peoples share culture and show respect.", vocab=["canoe", "salmon", "cedar", "drum", "grandma", "grandpa", "river", "forest"],
            learn=["First Peoples have lived in Canada for thousands of years.", "Elders share stories, language and knowledge.", "Many cultures teach respect for the land and water."],
            ex=("pic", ("Which did people paddle on the water?", ["salmon", "cedar", "canoe"]), "C"),
            tryit=[("pic", ("Who shares stories and knowledge?", ["grandma", "ball", "kite"]), "A"), ("pic", ("Which tall tree grows in BC forests?", ["tree", "cedar", "flower"]), "B")]),
    8: dict(goal="I can tell how people can care for the environment.", vocab=["bin_recycle", "bin_trash", "tree", "water", "lake", "forest", "flower", "cedar"],
            learn=["Reduce, reuse and recycle.", "Water is limited. Do not waste it.", "Everyone has a responsibility to care for nature."],
            ex=("pic", ("Where does a plastic bottle go?", ["bin_trash", "bin_recycle"]), "B"),
            tryit=[("pic", ("Where does a candy wrapper go?", ["bin_recycle", "bin_trash"]), "B"), ("pic", ("What do we plant to help the air?", ["bin_trash", "tree", "ball"]), "B")]),
    9: dict(goal="I can name rights and responsibilities.", vocab=["sharing", "include", "turns", "say_thanks", "hug", "globe", "school", "house"],
            learn=["Every child has rights: to be safe, to learn and to play.", "Rights come with responsibilities, like helping and sharing.", "Children around the world have the same basic rights."],
            ex=("pic", ("Which shows sharing?", ["ball", "sharing", "game"]), "B"),
            tryit=[("pic", ("Which shows including everyone?", ["include", "ball", "game"]), "A"), ("pic", ("Which shows taking turns?", ["sharing", "turns", "team"]), "B")]),
    10: dict(goal="I can tell how things change over time and tell fact from opinion.", vocab=["baby", "girl", "mom", "grandma", "horsecart", "car", "flower", "snowflake"],
             learn=["A timeline puts events in order.", "Some things change and some stay the same.", "A fact can be proven. An opinion is what someone thinks."],
             ex=("pic", ("Who is the oldest?", ["baby", "grandma", "mom"]), "B"),
             tryit=[("pic", ("Which is from long ago?", ["horsecart", "car"]), "A"), ("pic", ("Which season is cold and snowy?", ["sun", "snowflake", "flower"]), "B")]),
})


def cover(b):
    c = b.c
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    cols = [ORANGE, TEAL, BLUE, Color(.95, .75, .2), Color(.85, .35, .45)]
    for i, k in enumerate(["house", "school", "mayor", "townhall", "flag_canada", "globe", "canoe", "apple", "firefighter", "vote", "library", "family", "ferry", "maple"]):
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
    c.drawCentredString(W / 2, H - 274, "Workbook")
    c.setFillColor(Color(1, .85, .5))
    c.setFont("Helvetica", 17)
    c.drawCentredString(W / 2, H - 316, "Look, read, write and discover our community and world")
    c.setFillColor(white)
    c.setFont("Helvetica", 13)
    for i, t in enumerate(["10 units  •  10 lessons  •  100 daily practice sheets",
                           "pictures, reading, writing, maps  •  full answer key  •  certificate"]):
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
    c.drawCentredString(W / 2, 22, "Follows the BC Grade 2 Social Studies curriculum. Not affiliated with Kumon.")
    b.page(footer=False)


def guide(b):
    c = b.c
    b.rec["guide"] = c.getPageNumber()
    b.banner("A Note for Parents & Teachers", "How to use this book")
    blocks = [
        ("A balanced mix",
         ["Each sheet mixes <b>pictures</b> with <b>true/false, fill-in-the-blank (word bank), matching, short reading and writing</b>.",
          "Read short passages together at first, then let your child read and write alone.",
          "Talk about the answers. Social studies is about ideas, so there is often more than one good answer in the writing parts."]),
        ("The weekly rhythm (about 12 weeks, 5 days a week, 10–15 minutes)",
         ["<b>Lesson day:</b> look and learn, read the three key ideas, try the two questions.",
          "<b>Days 1–4:</b> two practice sheets a day (Sheet A, then Sheet B).",
          "<b>Day 5:</b> mixed review, then a <b>Draw it!</b> box and a sentence about your picture.",
          "<b>Goal:</b> 90% or better. Check with the answer key and fix mistakes together.",
          "Take the Check-Up after Unit 5 and the Final Test at the end."]),
        ("Make it real",
         ["Walk through your neighbourhood and spot places, helpers and leaders. Look at a real map.",
          "Visit a library, a town hall or a food bank. Ask an Elder or a community leader to share stories or knowledge.",
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
    b.box(M, b.y, W - 2 * M, 118, CREAM, Color(.9, .8, .5))
    q = Paragraph("<b>Follows the BC Grade 2 Social Studies curriculum.</b> Big Ideas: (1) local actions have global consequences, and global actions have local consequences; "
                  "(2) Canada is made up of many diverse regions and communities; (3) individuals have rights and responsibilities as global citizens. "
                  "Content covered: communities and cultures in Canada and around the world (including a First Peoples community), how needs and wants are met, "
                  "people and the environment, features of the environment around the world, rights and responsibilities, and the roles of regional governments. "
                  "Skills practised: maps with cardinal directions, symbols and legends; sequencing and change; fact vs opinion; and choosing responses to a problem. "
                  "Check your own curriculum for exact wording. Kumon’s own pages do not match its levels to school grades. Levels rise from "
                  "<b>Starter</b> (Units 1–3) to <b>Building</b> (4–6), <b>Stretch</b> (7–9) and <b>Challenge</b> (10).", SMALL)
    _, hh = q.wrap(W - 2 * M - 20, 1000)
    q.drawOn(c, M + 10, b.y - 8 - hh)
    b.page()


SKILLS = ["Tell what a community is and name its places and jobs", "Tell needs from wants and goods from services", "Name community leaders and what they do",
          "Read a map using directions, symbols and a legend", "Tell how communities across Canada differ", "Describe places and climates around the world",
          "Show respect for First Peoples cultures", "Tell how to care for the environment", "Name rights and responsibilities", "Tell fact from opinion and how things change"]


def build(path, pages):
    b = B.Book(path, pages)
    cover(b)
    guide(b)
    B.contents(b, pages)
    B.tracker(b, SKILLS)
    for u in range(1, 11):
        b.rec[f"u{u}"] = b.c.getPageNumber()
        BS.lesson(b, u)
        A, Bs = S2.unit_sheets(u, 0), S2.unit_sheets(u, 1)
        for sa, sb in zip(A, Bs):
            b.sheet(sa, f"Unit {u} • Day {sa['day']}", "A")
            b.sheet(sb, f"Unit {u} • Day {sb['day']}", "B")
        if u == 5:
            b.rec["checkup"] = b.c.getPageNumber()
            b.sheet(S2.checkup_a(), "")
    b.rec["final"] = b.c.getPageNumber()
    b.sheet(S2.final_test(), "")
    B.certificate(b)
    B.answer_key(b)
    b.c.save()
    return b.rec


if __name__ == "__main__":
    rec = build(OUT, {})
    rec = build(OUT, rec)
    print("pages:", rec)
