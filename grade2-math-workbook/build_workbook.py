#!/usr/bin/env python3
"""Builds Grade2_Math_Mastery_Workbook.pdf (lessons, daily sheets, answer key)."""
import math
import random
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, black, white
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

import generators as G
from generators import MINUS, TIMES

W, H = letter
M = 40
NAVY = Color(.11, .24, .45)
TEAL = Color(.0, .55, .55)
ORANGE = Color(.95, .55, .1)
LIGHT = Color(.92, .96, .99)
CREAM = Color(1, .97, .86)
MINT = Color(.90, .97, .95)
GREY = Color(.45, .45, .45)
SOFT = Color(.80, .80, .80)
BLUE = Color(.25, .5, .85)

BOOK_TITLE = "Grade 2 Math Mastery Workbook"
TOP_LABEL = {"vert", "seq", "clock", "frac", "groups", "word"}
OUT = sys.argv[1] if len(sys.argv) > 1 else "Grade2_Math_Mastery_Workbook.pdf"

BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=11, leading=15)
SMALL = ParagraphStyle("small", fontName="Helvetica", fontSize=9.5, leading=12.5)
BUL = ParagraphStyle("bul", parent=BODY, leftIndent=14, bulletIndent=2, spaceAfter=4)

UNIT_NAMES = {1: "Counting & Comparing to 100", 2: "Adding Within 20", 3: "Subtracting Within 20",
              4: "Two-Digit Add & Subtract", 5: "Regrouping: Carry & Borrow", 6: "Place Value to 1000",
              7: "Skip Counting & Multiplying", 8: "Telling Time & Counting Money",
              9: "Shapes, Measuring & Fractions", 10: "Word Problems & Challenges"}
UNIT_CC = {1: "2.NBT.2, 2.NBT.3, 2.NBT.4", 2: "2.OA.2", 3: "2.OA.2", 4: "2.NBT.5",
           5: "2.NBT.5, 2.NBT.6", 6: "2.NBT.1, 2.NBT.3, 2.NBT.4, 2.NBT.7, 2.NBT.8",
           7: "2.OA.3, 2.OA.4, 2.NBT.2", 8: "2.MD.7, 2.MD.8", 9: "2.G.1, 2.G.3, 2.MD.1, 2.MD.4, 2.MD.10",
           10: "2.OA.1, 2.MD.5"}
UNIT_LEVEL = {1: "Starter", 2: "Starter", 3: "Starter", 4: "Building", 5: "Building", 6: "Building",
              7: "Stretch", 8: "Stretch", 9: "Stretch", 10: "Challenge"}


# ================================================================ cell drawers
def fit_text(c, text, x, y, maxw, size=13, font="Helvetica"):
    while stringWidth(text, font, size) > maxw and size > 8:
        size -= .5
    c.setFont(font, size)
    c.drawString(x, y, text)


def d_eq(c, x, yt, w, h, data, **_):
    c.setFillColor(black)
    fit_text(c, data, x + 22, yt - h + 11, w - 28, 13)


def d_vert(c, x, yt, w, h, data, **_):
    nums, op = data
    c.setFillColor(black)
    c.setFont("Helvetica", 16)
    mw = max(stringWidth(str(n), "Helvetica", 16) for n in nums)
    xr = x + w / 2 + mw / 2 + 4
    y = yt - 22
    for i, n in enumerate(nums):
        c.drawRightString(xr, y, str(n))
        if i == len(nums) - 1:
            c.drawString(xr - mw - 15, y, "+" if op == "+" else MINUS)
        y -= 20
    c.setLineWidth(1)
    c.line(xr - mw - 18, y + 14, xr + 4, y + 14)


def d_seq(c, x, yt, w, h, data, **_):
    n = len(data)
    bw = min(46, (w - 30) / n)
    x0 = x + 26
    for i, v in enumerate(data):
        bx = x0 + i * bw
        c.setLineWidth(1)
        c.setStrokeColor(black)
        if v is None:
            c.setFillColor(CREAM)
            c.rect(bx + 2, yt - h + 4, bw - 4, h - 8, fill=1, stroke=1)
        else:
            c.setFillColor(white)
            c.rect(bx + 2, yt - h + 4, bw - 4, h - 8, fill=1, stroke=1)
            c.setFillColor(black)
            c.setFont("Helvetica", 14)
            c.drawCentredString(bx + bw / 2, yt - h + 12, str(v))


def d_cmp(c, x, yt, w, h, data, **_):
    a, b = data
    cx = x + w / 2 + 6
    cy = yt - h / 2 - 2
    c.setFillColor(black)
    c.setFont("Helvetica", 14)
    c.drawRightString(cx - 17, cy - 5, str(a))
    c.setLineWidth(1)
    c.circle(cx, cy, 11, stroke=1, fill=0)
    c.drawString(cx + 17, cy - 5, str(b))


def d_word(c, x, yt, w, h, data, **_):
    c.setFillColor(black)
    lines = simpleSplit(data, "Helvetica", 11.5, w - 28)
    y = yt - 13
    c.setFont("Helvetica", 11.5)
    for ln in lines:
        c.drawString(x + 22, y, ln)
        y -= 14
    c.setFont("Helvetica", 10.5)
    c.setFillColor(GREY)
    c.drawString(x + 22, yt - h + 12, "Number sentence: ________________________")
    c.drawString(x + 22 + 270, yt - h + 12, "Answer: ______________")


def _clock(c, cx, cy, r, hh, mm, nums=True):
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.setLineWidth(1.5)
    c.circle(cx, cy, r, fill=1, stroke=1)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", max(6, r * .22))
    for i in range(1, 13):
        a = math.radians(90 - i * 30)
        c.drawCentredString(cx + (r - r * .2) * math.cos(a), cy + (r - r * .2) * math.sin(a) - r * .08, str(i))
    for i in range(60):
        a = math.radians(90 - i * 6)
        L = r * .05 if i % 5 else r * .09
        c.setLineWidth(.5)
        c.line(cx + (r - L) * math.cos(a), cy + (r - L) * math.sin(a), cx + r * math.cos(a), cy + r * math.sin(a))
    am = math.radians(90 - mm * 6)
    ah = math.radians(90 - ((hh % 12) * 30 + mm * .5))
    c.setLineWidth(2.5)
    c.line(cx, cy, cx + r * .48 * math.cos(ah), cy + r * .48 * math.sin(ah))
    c.setLineWidth(1.5)
    c.line(cx, cy, cx + r * .72 * math.cos(am), cy + r * .72 * math.sin(am))
    c.circle(cx, cy, 2, fill=1)


def d_clock(c, x, yt, w, h, data, **_):
    hh, mm = data
    _clock(c, x + w / 2, yt - 8 - 36, 36, hh, mm)
    c.setFillColor(black)
    c.setFont("Helvetica", 12)
    c.drawCentredString(x + w / 2, yt - h + 6, "Time: ______ : ______")


def d_frac(c, x, yt, w, h, data, **_):
    parts, shaded = data
    bw, bh = 108, 26
    bx, by = x + (w - bw) / 2, yt - 14 - bh
    for i in range(parts):
        c.setFillColor(Color(1, .8, .45) if i < shaded else white)
        c.rect(bx + i * bw / parts, by, bw / parts, bh, fill=1, stroke=1)
    c.setFillColor(black)
    c.setFont("Helvetica", 12)
    c.drawCentredString(x + w / 2, yt - h + 6, "Shaded: ______ / ______")


def d_groups(c, x, yt, w, h, data, **_):
    g, p = data
    gw, gh = 38, 32
    x0 = x + 22
    for i in range(g):
        bx = x0 + i * (gw + 8)
        c.setFillColor(LIGHT)
        c.roundRect(bx, yt - 14 - gh, gw, gh, 5, fill=1, stroke=1)
        c.setFillColor(BLUE)
        for k in range(p):
            col, row = k % 3, k // 3
            c.circle(bx + 9 + col * 10, yt - 14 - gh + 22 - row * 12, 3.2, fill=1, stroke=0)
    c.setFillColor(black)
    c.setFont("Helvetica", 11.5)
    c.drawString(x + 22, yt - h + 12, "____ groups of ____ = ____")


DRAW = {"eq": d_eq, "vert": d_vert, "seq": d_seq, "cmp": d_cmp, "word": d_word,
        "clock": d_clock, "frac": d_frac, "groups": d_groups}


# ==================================================================== art
def dots(c, x, y, n, r=4, color=BLUE, per=6, gap=11):
    c.setFillColor(color)
    for i in range(n):
        c.circle(x + (i % per) * gap, y - (i // per) * gap, r, fill=1, stroke=0)


def tenframe(c, x, y, filled, color, s=14):
    for i in range(10):
        cx, cy = x + (i % 5) * s, y - (i // 5) * s
        c.setFillColor(white)
        c.rect(cx, cy, s, s, fill=1, stroke=1)
        if i < filled:
            c.setFillColor(color)
            c.circle(cx + s / 2, cy + s / 2, s * .35, fill=1, stroke=0)


def rod(c, x, y, hgt=48):
    c.setFillColor(Color(.6, .85, .7))
    c.rect(x, y, 8, hgt, fill=1, stroke=1)
    for i in range(1, 10):
        c.setLineWidth(.3)
        c.line(x, y + i * hgt / 10, x + 8, y + i * hgt / 10)
    c.setLineWidth(1)


def cube(c, x, y, s=8):
    c.setFillColor(Color(.98, .85, .5))
    c.rect(x, y, s, s, fill=1, stroke=1)


def flat(c, x, y, s=44):
    c.setFillColor(Color(.75, .85, .98))
    c.rect(x, y, s, s, fill=1, stroke=1)
    c.setLineWidth(.3)
    for i in range(1, 10):
        c.line(x + i * s / 10, y, x + i * s / 10, y + s)
        c.line(x, y + i * s / 10, x + s, y + i * s / 10)
    c.setLineWidth(1)


def polygon(c, cx, cy, r, n, label):
    c.setFillColor(LIGHT)
    p = c.beginPath()
    for i in range(n):
        a = math.radians(90 + i * 360 / n)
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        p.moveTo(px, py) if i == 0 else p.lineTo(px, py)
    p.close()
    c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(black)
    c.setFont("Helvetica", 8)
    c.drawCentredString(cx, cy - r - 11, label)


def art1(c, x, y, w, h):
    s = min(w, h - 14) / 10
    c.setFont("Helvetica", s * .38)
    for r in range(10):
        for k in range(10):
            c.setFillColor(LIGHT if (r + k) % 2 else white)
            c.rect(x + k * s, y + h - 14 - (r + 1) * s, s, s, fill=1, stroke=0)
            c.setFillColor(black)
            c.drawCentredString(x + k * s + s / 2, y + h - 14 - (r + 1) * s + s * .3, str(r * 10 + k + 1))
    c.setStrokeColor(SOFT)
    c.rect(x, y + h - 14 - 10 * s, 10 * s, 10 * s, fill=0)
    c.setStrokeColor(black)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(x + 5 * s, y + h - 9, "A hundred chart")


def art2(c, x, y, w, h):
    tenframe(c, x + 6, y + h - 40, 8, BLUE)
    tenframe(c, x + 6 + 82, y + h - 40, 5, ORANGE)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 36, y + h - 76, "8")
    c.drawString(x + 76, y + h - 76, "+")
    c.drawString(x + 112, y + h - 76, "5")
    c.setFont("Helvetica", 9.5)
    c.drawString(x + 10, y + h - 100, "Move 2 to fill the ten-frame:")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 10, y + h - 116, "10 + 3 = 13")


def art3(c, x, y, w, h):
    dots(c, x + 12, y + h - 25, 12, 7, BLUE, per=6, gap=22)
    c.setStrokeColor(Color(.8, .1, .1))
    c.setLineWidth(2)
    for i in range(7, 12):
        cx, cy = x + 12 + (i % 6) * 22, y + h - 25 - (i // 6) * 22
        c.line(cx - 7, cy - 7, cx + 7, cy + 7)
        c.line(cx - 7, cy + 7, cx + 7, cy - 7)
    c.setStrokeColor(black)
    c.setLineWidth(1)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 12, y + h - 95, f"12 {MINUS} 5 = 7")
    c.setFont("Helvetica", 9.5)
    c.drawString(x + 12, y + h - 112, "Cross out 5. Count what is left.")


def art4(c, x, y, w, h):
    for i in range(4):
        rod(c, x + 14 + i * 14, y + h - 80)
    for i in range(3):
        cube(c, x + 90 + i * 12, y + h - 80)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 14, y + h - 102, "43 = 4 tens + 3 ones")
    c.setFont("Helvetica", 9.5)
    c.drawString(x + 14, y + h - 118, "tens column | ones column")


def art5(c, x, y, w, h):
    rod(c, x + 20, y + h - 90, 60)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x + 40, y + h - 62, "=")
    for i in range(10):
        cube(c, x + 62 + (i % 5) * 12, y + h - 40 - (i // 5) * 14 - 12)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 14, y + h - 108, "1 ten = 10 ones")
    c.setFont("Helvetica", 9.5)
    c.drawString(x + 14, y + h - 123, "Borrow a ten, get 10 ones!")


def art6(c, x, y, w, h):
    c.setFont("Helvetica-Bold", 9.5)
    for i in range(2):
        flat(c, x + 8 + i * 50, y + h - 62, 44)
    for i in range(4):
        rod(c, x + 112 + i * 11, y + h - 62, 44)
    for i in range(5):
        cube(c, x + 112 + i * 10, y + h - 85)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(x + 4, y + h - 104, "245 = 2 hundreds, 4 tens, 5 ones")


def art7(c, x, y, w, h):
    for i in range(3):
        bx = x + 10 + i * 52
        c.setFillColor(LIGHT)
        c.roundRect(bx, y + h - 70, 46, 46, 6, fill=1, stroke=1)
        dots(c, bx + 11, y + h - 36, 4, 4.5, BLUE, per=2, gap=22)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 10, y + h - 92, f"3 groups of 4 = 3 {TIMES} 4 = 12")


def art8(c, x, y, w, h):
    _clock(c, x + 50, y + h - 56, 44, 4, 15)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 105, y + h - 30, "4:15")
    c.setFont("Helvetica", 9.5)
    for i, t in enumerate(["penny 1¢", "nickel 5¢", "dime 10¢", "quarter 25¢"]):
        c.drawString(x + 105, y + h - 50 - i * 14, t)
    c.drawString(x + 8, y + h - 118, "5 min per number on the clock")


def art9(c, x, y, w, h):
    for i, (n, nm) in enumerate([(3, "3 sides"), (4, "4 sides"), (5, "5 sides"), (6, "6 sides")]):
        polygon(c, x + 20 + i * 38, y + h - 30, 15, n, nm)
    bx, by = x + 12, y + h - 92
    for i in range(4):
        c.setFillColor(Color(1, .8, .45) if i < 3 else white)
        c.rect(bx + i * 30, by, 30, 24, fill=1, stroke=1)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(bx, by - 15, "3/4 shaded")


def art10(c, x, y, w, h):
    c.setFillColor(LIGHT)
    c.rect(x + 10, y + h - 50, 80, 28, fill=1, stroke=1)
    c.setFillColor(CREAM)
    c.rect(x + 90, y + h - 50, 50, 28, fill=1, stroke=1)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(x + 50, y + h - 41, "8")
    c.drawCentredString(x + 115, y + h - 41, "5")
    c.line(x + 10, y + h - 60, x + 140, y + h - 60)
    c.drawCentredString(x + 75, y + h - 76, "?")
    c.setFont("Helvetica", 9.5)
    c.drawString(x + 10, y + h - 98, "Bar model: 8 and 5 join to make ?")
    c.drawString(x + 10, y + h - 112, "8 + 5 = 13")


ART = {1: art1, 2: art2, 3: art3, 4: art4, 5: art5, 6: art6, 7: art7, 8: art8, 9: art9, 10: art10}

# ================================================================== lessons
LESSONS = {
    1: dict(goal="I can count to 100, fill in missing numbers, and tell which number is bigger.",
            learn=["Numbers go up by <b>1</b> each step: 23, 24, 25. Going backwards, they go down by 1.",
                   "To compare, look at the <b>tens</b> first. 47 is bigger than 39 because 4 tens is more than 3 tens.",
                   "If the tens match, compare the <b>ones</b>: 52 &lt; 58.",
                   "The symbol <b>&lt;</b> or <b>&gt;</b> opens its mouth toward the <b>bigger</b> number."],
            ex=[("Next number", ["~What comes after 29?", "29 + 1", "= 30"]),
                ("Compare", ["~47 and 39", "~Tens: 4 > 3", "47 > 39"]),
                ("Missing", ["61, 62, __, 64", "~Count up by 1", "= 63"])],
            tip="Use the hundred chart to count: moving right adds 1, moving down adds 10.",
            tryit=[("seq", [([5, 6, None, 8, 9, None, 11, 12], "7, 10")], 1, 36),
                   ("cmp", [((34, 29), ">"), ((51, 58), "<"), ((60, 60), "="), ((17, 71), "<")], 4, 36)]),
    2: dict(goal="I can add two numbers that make up to 20.",
            learn=["Addition means <b>putting groups together</b>. The answer is called the <b>sum</b>.",
                   "<b>Count on:</b> start with the bigger number. 8 + 3 → say 8, then 9, 10, 11.",
                   "<b>Make a ten:</b> 8 + 5 → 8 + 2 = 10, then 10 + 3 = 13.",
                   "<b>Doubles:</b> 6 + 6 = 12. Learn these by heart!",
                   "Order does not matter: 3 + 9 = 9 + 3."],
            ex=[("Count on", ["8 + 3", "~8 ... 9, 10, 11", "= 11"]),
                ("Make a ten", ["9 + 6", "~9 + 1 = 10", "10 + 5 = 15"]),
                ("Doubles", ["7 + 7", "~7 and 7 are twins", "= 14"])],
            tip="Fast facts are like muscles. A few minutes every day make them strong!",
            tryit=[("eq", [("6 + 4 = ____", "10"), ("9 + 5 = ____", "14"), ("8 + 8 = ____", "16"),
                           ("7 + ____ = 12", "5")], 2, 30)]),
    3: dict(goal="I can subtract numbers within 20.",
            learn=["Subtraction means <b>taking away</b> or finding <b>how many more</b>. The answer is the <b>difference</b>.",
                   "<b>Count back:</b> 9 – 3 → say 8, 7, 6.",
                   "<b>Think addition:</b> 13 – 5 = ? What plus 5 makes 13? It is 8!",
                   "<b>Go back to ten:</b> 14 – 6 → 14 – 4 = 10, then 10 – 2 = 8.",
                   "A <b>fact family</b> uses the same 3 numbers: 5 + 8 = 13, 8 + 5 = 13, 13 – 5 = 8, 13 – 8 = 5."],
            ex=[("Count back", ["9 – 3", "~8, 7, 6", "= 6"]),
                ("Think addition", ["13 – 5", "~5 + 8 = 13", "= 8"]),
                ("Back to ten", ["14 – 6", "~14 – 4 = 10", "10 – 2 = 8"])],
            tip="If you know your addition facts, you already know your subtraction facts!",
            tryit=[("eq", [(f"9 {MINUS} 4 = ____", "5"), (f"15 {MINUS} 6 = ____", "9"),
                           (f"12 {MINUS} 7 = ____", "5"), (f"17 {MINUS} 9 = ____", "8")], 2, 30)]),
    4: dict(goal="I can add and subtract two-digit numbers when no regrouping is needed.",
            learn=["Write the numbers so <b>ones line up under ones</b> and <b>tens under tens</b>.",
                   "Always start with the <b>ones</b> column, then do the <b>tens</b> column.",
                   "A two-digit number has tens and ones: 43 = 4 tens + 3 ones.",
                   "Adding tens is like adding small numbers: 40 + 30 = 4 tens + 3 tens = 7 tens = 70."],
            ex=[("Add", ["  32", "+ 45", "----", "  77"]),
                ("Subtract", ["  68", "– 35", "----", "  33"]),
                ("Tens only", ["50 + 30", "~5 tens + 3 tens", "= 80"])],
            tip="Check your answer: add to check subtracting. 33 + 35 = 68 ✓",
            tryit=[("vert", [(([24, 15], "+"), "39"), (([53, 21], "+"), "74"),
                             (([76, 42], "-"), "34"), (([89, 63], "-"), "26")], 4, 78)]),
    5: dict(goal="I can add and subtract when I need to carry or borrow a ten.",
            learn=["<b>Carry:</b> if the ones add to 10 or more, make a ten and carry it to the tens column.",
                   "<b>Borrow:</b> if the top ones are too small, take 1 ten from the tens and make it 10 ones.",
                   "1 ten = 10 ones. Nothing is lost; the ten just changes into ones.",
                   "Always check the <b>ones column first</b> and ask: do I need to carry or borrow?"],
            ex=[("Carry", ["   1", "  38", "+ 27", "----", "  65"]),
                ("Borrow", ["  52", "– 27", "----", "  25", "~12 – 7 = 5, 4 – 2 = 2"]),
                ("Why?", ["~8 + 7 = 15 ones", "~15 ones = 1 ten + 5 ones", "~So write 5, carry 1"])],
            tip="After you borrow, the tens digit is 1 smaller. Cross it out and write the new number!",
            tryit=[("vert", [(([47, 36], "+"), "83"), (([29, 45], "+"), "74"),
                             (([63, 28], "-"), "35"), (([81, 7], "-"), "74")], 4, 78)]),
    6: dict(goal="I can read, write and compare numbers up to 1000.",
            learn=["A 3-digit number has <b>hundreds, tens and ones</b>.",
                   "Expanded form: 345 = 300 + 40 + 5.",
                   "<b>10 more/less</b> changes the tens digit. <b>100 more/less</b> changes the hundreds digit.",
                   "Compare: look at the <b>hundreds</b> first, then tens, then ones."],
            ex=[("Break apart", ["~Number: 245", "2 hundreds", "4 tens, 5 ones"]),
                ("100 more", ["345 + 100", "~hundreds go up 1", "= 445"]),
                ("Compare", ["~456 and 478", "~Hundreds: same", "~Tens: 5 < 7 → 456 < 478"])],
            tip="A zero keeps a place: 305 has 3 hundreds, 0 tens, 5 ones.",
            tryit=[("eq", [("526 = ____ hundreds ____ tens ____ ones", "5, 2, 6"),
                           ("700 + 30 + 4 = ____", "734"), ("10 more than 360 = ____", "370"),
                           ("100 less than 842 = ____", "742")], 1, 30)]),
    7: dict(goal="I can skip count and use equal groups to multiply.",
            learn=["<b>Skip counting</b> means jumping by the same number: by 2s: 2, 4, 6, 8; by 5s: 5, 10, 15; by 10s: 10, 20, 30.",
                   "<b>Equal groups:</b> 3 groups of 4 is 4 + 4 + 4 = 12. We write 3 × 4 = 12.",
                   "<b>Even</b> numbers end in 0, 2, 4, 6, 8. <b>Odd</b> numbers end in 1, 3, 5, 7, 9.",
                   "The × sign is read “times” or “groups of”."],
            ex=[("Count by 5s", ["5, 10, __, 20", "~jump 5 each time", "= 15"]),
                ("Equal groups", ["3 × 4", "4 + 4 + 4", "= 12"]),
                ("Even or odd", ["~Is 17 even or odd?", "~It ends in 7", "= odd"])],
            tip="Tap your desk as you skip count. Your fingers help you remember!",
            tryit=[("seq", [([10, 20, None, 40, None, 60, 70], "30, 50")], 1, 36),
                   ("eq", [(f"2 {TIMES} 5 = ____", "10"), (f"5 {TIMES} 3 = ____", "15"),
                           (f"10 {TIMES} 4 = ____", "40"), ("Is 16 odd or even?  ____", "even")], 2, 30)]),
    8: dict(goal="I can tell time to 5 minutes and count coins.",
            learn=["The <b>short hand</b> shows the hour. The <b>long hand</b> shows the minutes.",
                   "Long hand on 12 = o’clock. On 3 = 15 minutes. On 6 = 30 minutes. On 9 = 45 minutes.",
                   "Each number on the clock is <b>5 minutes</b>. Count by 5s around the clock.",
                   "Coins: penny 1¢, nickel 5¢, dime 10¢, quarter 25¢. 100¢ = $1.",
                   "Count money by starting with the <b>biggest coin</b>."],
            ex=[("Time", ["~Short hand just past 4", "~Long hand on 3", "= 4:15"]),
                ("Time", ["~Short hand between 7 and 8", "~Long hand on 6", "= 7:30"]),
                ("Money", ["1 quarter, 1 dime", "25, 35, 36, 37", "= 37¢ (2 pennies)"])],
            tip="Say the hour first, then the minutes: “four fifteen”.",
            tryit=[("clock", [((9, 0), "9:00"), ((2, 30), "2:30"), ((6, 45), "6:45")], 3, 104),
                   ("eq", [("2 dimes, 1 nickel = ____¢", "25"), ("1 quarter, 2 dimes = ____¢", "45")], 1, 30)]),
    9: dict(goal="I can name shapes, measure lengths, and write simple fractions.",
            learn=["Shapes have <b>sides</b> (straight edges) and <b>corners</b>. A triangle has 3, a square 4, a pentagon 5, a hexagon 6.",
                   "Length: <b>12 inches = 1 foot</b>. <b>100 centimeters = 1 meter</b>. Line the ruler up at 0!",
                   "A <b>fraction</b> names equal parts of a whole. Halves = 2 equal parts, thirds = 3, fourths = 4.",
                   "In 3/4, the bottom number (4) is the equal parts and the top number (3) is the parts we count."],
            ex=[("Shapes", ["~A hexagon has", "6 sides", "6 corners"]),
                ("Measure", ["~Pencil 7 in.", "~Crayon 3 in.", "7 – 3 = 4 in."]),
                ("Half of", ["~Half of 12", "12 shared by 2", "= 6"])],
            tip="Equal means the same size. Parts that are not equal are not halves!",
            tryit=[("eq", [("A pentagon has ____ sides.", "5"), ("Half of 8 = ____", "4"),
                           ("12 inches = ____ foot", "1")], 1, 30),
                   ("frac", [((4, 1), "1/4"), ((3, 2), "2/3")], 2, 66)]),
    10: dict(goal="I can solve word problems by choosing add, subtract or multiply.",
             learn=["<b>Read</b> the problem twice. <b>Circle</b> the numbers. <b>Underline</b> the question.",
                    "<b>Join / in all / together</b> → add (+). <b>Left / take away / how many more</b> → subtract (–).",
                    "<b>Each / groups of / bags with</b> → multiply (×).",
                    "Write a <b>number sentence</b>, solve it, and write the answer.",
                    "<b>Check:</b> does your answer make sense?"],
             ex=[("Add", ["~5 red, 7 blue.", "~How many in all?", "5 + 7 = 12"]),
                 ("Subtract", ["~15 cookies, 6 eaten.", "~How many left?", "15 – 6 = 9"]),
                 ("Multiply", ["~4 bags, 5 in each.", "~How many in all?", "4 × 5 = 20"])],
             tip="Two-step problems: do the first step, write the answer, then do the second step.",
             tryit=[("word", [("Mia has 9 shells. Leo gives Mia 6 more. How many shells does Mia have now?", "15")], 1, 70),
                    ("word", [("There are 3 boxes with 4 pencils in each box. How many pencils in all?", "12")], 1, 70)]),
}


# =============================================================== the book
class Book:
    def __init__(self, path, pages):
        self.c = canvas.Canvas(path, pagesize=letter)
        self.c.setTitle(BOOK_TITLE)
        self.c.setAuthor(BOOK_TITLE)
        self.known = pages
        self.rec = {}
        self.y = 0
        self.answers = []       # (label, [(qn, ans)])
        self.foot = True
        self.begin()

    def begin(self):
        self.y = H - M

    def page(self, key=None, footer=True):
        """finish current page, begin the next"""
        self.foot_draw()
        self.c.showPage()
        self.foot = footer
        self.begin()
        if key:
            self.rec[key] = self.c.getPageNumber()

    def foot_draw(self):
        if not self.foot:
            return
        c = self.c
        c.setFont("Helvetica", 8.5)
        c.setFillColor(GREY)
        c.drawCentredString(W / 2, 22, f"{BOOK_TITLE}   •   page {c.getPageNumber()}")

    # ---------- primitives
    def banner(self, text, sub=""):
        c = self.c
        c.setFillColor(NAVY)
        c.roundRect(M, self.y - 44, W - 2 * M, 44, 8, fill=1, stroke=0)
        c.setFillColor(white)
        size = 17
        room = W - 2 * M - 28 - (stringWidth(sub, "Helvetica", 10) + 14 if sub else 0)
        while stringWidth(text, "Helvetica-Bold", size) > room and size > 9:
            size -= .5
        c.setFont("Helvetica-Bold", size)
        c.drawString(M + 14, self.y - 28, text)
        if sub:
            c.setFont("Helvetica", 10)
            c.drawRightString(W - M - 14, self.y - 28, sub)
        self.y -= 44 + 12

    def para(self, html, x, width, style=BODY, gap=0):
        p = Paragraph(html, style)
        _, h = p.wrap(width, 10000)
        p.drawOn(self.c, x, self.y - h)
        self.y -= h + gap
        return h

    def box(self, x, ytop, w, h, fill=LIGHT, stroke=SOFT):
        self.c.setFillColor(fill)
        self.c.setStrokeColor(stroke)
        self.c.roundRect(x, ytop - h, w, h, 8, fill=1, stroke=1)
        self.c.setStrokeColor(black)

    def fresh_page_if_needed(self, need, cont_title=None):
        if self.y - need < 52:
            self.page()
            if cont_title:
                self.c.setFillColor(NAVY)
                self.c.setFont("Helvetica-Bold", 11)
                self.c.drawString(M, self.y - 10, cont_title + "  (continued)")
                self.y -= 26

    # ---------- sections of questions
    def sections(self, sections, qn, store, cont_title):
        c = self.c
        for s in sections:
            n = len(s["cells"])
            cols, h = s["cols"], s["h"]
            rows = math.ceil(n / cols)
            head_h = 24 if s["head"] else 4
            self.fresh_page_if_needed(head_h + h, cont_title)
            if s["head"]:
                c.setFillColor(TEAL)
                c.setFont("Helvetica-Bold", 11.5)
                c.drawString(M, self.y - 14, s["head"])
                self.y -= head_h
            else:
                self.y -= head_h
            cw = (W - 2 * M) / cols
            for r in range(rows):
                self.fresh_page_if_needed(h, cont_title)
                for k in range(cols):
                    i = r * cols + k
                    if i >= n:
                        break
                    data, ans = s["cells"][i]
                    x = M + k * cw
                    DRAW[s["kind"]](c, x, self.y, cw, h, data)
                    if ans is None:
                        continue
                    qn += 1
                    c.setFillColor(GREY)
                    c.setFont("Helvetica-Bold", 9)
                    c.drawString(x + 2, self.y - 12 if s["kind"] in TOP_LABEL
                                 else self.y - h + 11, f"{qn})")
                    store.append((qn, ans))
                self.y -= h
            self.y -= 6
        return qn

    # ---------- a daily practice sheet
    def sheet(self, sh, label, letter=""):
        c = self.c
        total = sum(len(s["cells"]) for s in sh["sections"])
        title = f"{label}: {sh['title']}" if label else sh["title"]
        self.banner(title, ("Daily Practice \u2022 Sheet " + letter) if letter else ("Daily Practice" if sh["unit"] else "Assessment"))
        c.setFillColor(black)
        c.setFont("Helvetica", 10.5)
        c.drawString(M, self.y - 4, "Name: ______________________    Date: ____________    Time: ______ min    "
                                    f"Score: ______ / {total}")
        self.y -= 20
        lines = simpleSplit(sh["instr"], "Helvetica-Bold", 10.5, W - 2 * M - 20)
        lines2 = simpleSplit(sh["example"], "Helvetica-Oblique", 10, W - 2 * M - 20)
        bh = 12 * len(lines) + 12 * len(lines2) + 12
        self.box(M, self.y, W - 2 * M, bh, CREAM, Color(.9, .8, .5))
        yy = self.y - 15
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 10.5)
        for ln in lines:
            c.drawString(M + 10, yy, ln)
            yy -= 12
        c.setFont("Helvetica-Oblique", 10)
        for ln in lines2:
            c.drawString(M + 10, yy, ln)
            yy -= 12
        self.y -= bh + 6
        store = []
        self.sections(sh["sections"], 0, store, title)
        self.answers.append((title + (" \u2022 Sheet " + letter if letter else ""), store))
        self.page()

    # ---------- a lesson page
    def lesson(self, u):
        L = LESSONS[u]
        c = self.c
        self.banner(f"Unit {u} Lesson: {UNIT_NAMES[u]}", UNIT_LEVEL[u])
        # goal
        gh = 26
        self.box(M, self.y, W - 2 * M, gh, MINT, Color(.6, .85, .8))
        c.setFillColor(TEAL)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(M + 10, self.y - 17, "My goal:")
        c.setFillColor(black)
        c.setFont("Helvetica", 11)
        c.drawString(M + 66, self.y - 17, L["goal"][:110])
        self.y -= gh + 10
        # learn + art
        top = self.y
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(M, self.y - 12, "Learn")
        self.y -= 20
        sx = self.y
        for t in L["learn"]:
            self.para(t, M + 6, 335, BUL)
            # bullet
            c.setFillColor(ORANGE)
        # bullets drawn after
        used = sx - self.y
        # redraw bullets simply
        yb = sx
        for t in L["learn"]:
            p = Paragraph(t, BUL)
            _, hh = p.wrap(335, 10000)
            c.setFillColor(ORANGE)
            c.circle(M + 4, yb - 8, 2.5, fill=1, stroke=0)
            yb -= hh + 0
        ah = 150
        self.box(M + 360, top, W - 2 * M - 360, ah)
        ART[u](c, M + 366, top - ah, W - 2 * M - 372, ah)
        self.y = min(self.y, top - ah) - 12
        # examples
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(M, self.y - 12, "Examples")
        self.y -= 20
        ew = (W - 2 * M - 20) / 3
        eh = 112
        for i, (ttl, lines) in enumerate(L["ex"]):
            x = M + i * (ew + 10)
            self.box(x, self.y, ew, eh, white, Color(.6, .7, .85))
            c.setFillColor(ORANGE)
            c.setFont("Helvetica-Bold", 10.5)
            c.drawString(x + 8, self.y - 15, f"Example {i + 1}: {ttl}")
            yy = self.y - 33
            for ln in lines:
                if ln.startswith("~"):
                    c.setFillColor(GREY)
                    c.setFont("Helvetica", 9)
                    for part in simpleSplit(ln[1:], "Helvetica", 9, ew - 16):
                        c.drawString(x + 8, yy, part)
                        yy -= 12
                else:
                    c.setFillColor(black)
                    c.setFont("Courier-Bold", 13)
                    c.drawString(x + 8, yy, ln)
                    yy -= 15
        self.y -= eh + 12
        # try it
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(M, self.y - 12, "Try it yourself!  (answers are in the back)")
        self.y -= 22
        store = []
        qn = 0
        for kind, cells, cols, h in L["tryit"]:
            sec = G.sec("", kind, cells, cols, h)
            qn = self.sections([sec], qn, store, f"Unit {u} Lesson")
        self.answers.append((f"Unit {u} Lesson: Try it", store))
        # tip
        th = 30
        if self.y - th > 40:
            self.box(M, self.y - 4, W - 2 * M, th, CREAM, Color(.9, .8, .5))
            c.setFillColor(ORANGE)
            c.setFont("Helvetica-Bold", 10.5)
            c.drawString(M + 10, self.y - 24, "Remember:")
            c.setFillColor(black)
            c.setFont("Helvetica", 10)
            c.drawString(M + 80, self.y - 24, L["tip"][:105])
        self.page()


# ============================================================ front/back matter
def cover(b):
    c = b.c
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # decorative number circles
    rnd = random.Random(7)
    cols = [ORANGE, TEAL, BLUE, Color(.95, .75, .2), Color(.85, .35, .45)]
    for i, ch in enumerate("1234567890+–×=?"):
        x, y = 60 + (i % 7) * 82, 110 + (i // 7) * 90 + rnd.randint(-8, 8)
        c.setFillColor(cols[i % len(cols)])
        c.circle(x, y, 28, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(x, y - 9, ch)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(W / 2, H - 170, "Grade 2")
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(W / 2, H - 222, "Math Mastery")
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(W / 2, H - 274, "Workbook")
    c.setFillColor(Color(1, .85, .5))
    c.setFont("Helvetica", 17)
    c.drawCentredString(W / 2, H - 316, "From first steps to big challenges – one small step a day")
    c.setFillColor(white)
    c.setFont("Helvetica", 13)
    for i, t in enumerate(["10 units  •  10 lessons  •  100 daily practice sheets",
                           "2 check-ups  •  full answer key  •  progress tracker  •  certificate"]):
        c.drawCentredString(W / 2, H - 358 - i * 20, t)
    c.setFillColor(white)
    c.roundRect(W / 2 - 150, H - 470, 300, 56, 10, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(W / 2 - 138, H - 448, "This workbook belongs to:")
    c.setLineWidth(1)
    c.line(W / 2 - 138, H - 462, W / 2 + 138, H - 462)
    c.setFillColor(Color(.8, .85, .95))
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(W / 2, 22, "Aligned to Common Core Grade 2 math. Inspired by small-step, mastery-based learning; "
                                  "not affiliated with or endorsed by Kumon.")
    b.page(footer=False)


def guide(b):
    c = b.c
    b.rec["guide"] = c.getPageNumber()
    b.banner("A Note for Parents & Teachers", "How to use this book")
    blocks = [
        ("The method (what we learned from Kumon-style programs)",
         ["<b>Tiny steps.</b> Each sheet is only slightly harder than the last, so a child almost always succeeds.",
          "<b>Repetition to mastery.</b> Ten short sheets per skill (two a day) build speed and accuracy before the next topic.",
          "<b>Self-learning.</b> Each unit starts with a one-page lesson with worked examples a child can read and copy.",
          "<b>Correct every mistake.</b> Check together with the answer key and let your child fix each wrong answer until the sheet is 100%.",
          "<b>Short and daily.</b> Ten to fifteen minutes every day beats one long session a week."]),
        ("The weekly rhythm (about 12 weeks, 5 days a week, 10\u201315 minutes)",
         ["<b>Lesson day:</b> read the lesson together, study the examples, do “Try it yourself”.",
          "<b>Days 1–4:</b> two practice sheets a day (<b>Sheet A</b>, then <b>Sheet B</b> with new problems on the same skill). Write the time at the top.",
          "<b>Day 5:</b> review sheet with mixed questions and word problems.",
          "<b>Goal:</b> 90% or better in about 10 minutes. Below 80%? Repeat the sheet tomorrow (print a spare copy first).",
          "Take the Check-Up after Unit 5 and the Final Test at the end."]),
        ("Tips that make it fun",
         ["Stay close for the first few minutes, then let your child work alone.",
          "Praise effort and improvement, not just the score. Stop before frustration builds.",
          "Use real life: count stairs, tell time from the kitchen clock, pay with real coins.",
          "Colour in the tracker after each sheet – children love seeing progress."])]
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
    b.box(M, b.y, W - 2 * M, 50, CREAM, Color(.9, .8, .5))
    q = Paragraph("<b>About the levels:</b> Kumon’s own pages do not match its levels to school grades, so this book follows "
                  "the Common Core Grade 2 standards (listed per unit on the next page) and rises from "
                  "<b>Starter</b> (Units 1–3) to <b>Building</b> (4–6), <b>Stretch</b> (7–9) and <b>Challenge</b> (10).", SMALL)
    _, hh = q.wrap(W - 2 * M - 20, 1000)
    q.drawOn(c, M + 10, b.y - 8 - hh)
    b.page()


def contents(b, pages):
    c = b.c
    b.rec["contents"] = c.getPageNumber()
    b.banner("Contents & Learning Path", "Basic → High level")
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(GREY)
    c.drawString(M, b.y - 4, "Unit / topic")
    c.drawString(M + 285, b.y - 4, "Level")
    c.drawString(M + 345, b.y - 4, "Common Core")
    c.drawRightString(W - M, b.y - 4, "Page")
    b.y -= 14
    rows = []
    for u in range(1, 11):
        rows.append((f"Unit {u}: {UNIT_NAMES[u]}", UNIT_LEVEL[u], UNIT_CC[u], pages.get(f"u{u}", "")))
        if u == 5:
            rows.append(("Check-Up: Units 1–5", "", "", pages.get("checkup", "")))
    rows += [("Final Test: Units 1–10", "", "", pages.get("final", "")),
             ("Certificate of Achievement", "", "", pages.get("cert", "")),
             ("Answer Key", "", "", pages.get("answers", ""))]
    for i, (t, lv, cc, pg) in enumerate(rows):
        rh = 31 if cc else 25
        if i % 2 == 0:
            c.setFillColor(LIGHT)
            c.rect(M, b.y - rh, W - 2 * M, rh, fill=1, stroke=0)
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(M + 6, b.y - 18, t)
        c.setFont("Helvetica", 10)
        c.setFillColor(ORANGE)
        c.drawString(M + 285, b.y - 18, lv)
        c.setFillColor(GREY)
        c.setFont("Helvetica", 7.5)
        if cc:
            for j, part in enumerate(simpleSplit(cc, "Helvetica", 7.5, 150)[:2]):
                c.drawString(M + 345, b.y - 14 - j * 9, part)
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(W - M - 6, b.y - 18, str(pg))
        b.y -= rh
    b.y -= 10
    c.setFillColor(GREY)
    c.setFont("Helvetica", 8.5)
    c.drawString(M, b.y - 8, "Each unit = 1 lesson page + 5 daily practice sheets (Days 1–4 build up, Day 5 reviews).")
    b.page()


def tracker(b, skills=None):
    c = b.c
    b.banner("My Progress Tracker", "Colour a circle when both sheets are done")
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(GREY)
    c.drawString(M, b.y - 4, "Unit")
    heads = ["Lesson", "Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
    for i, hd in enumerate(heads):
        c.drawCentredString(M + 215 + i * 44, b.y - 4, hd)
    c.drawString(M + 215 + 6 * 44 - 14, b.y - 4, "Best score")
    b.y -= 14
    for u in range(1, 11):
        rh = 34
        if u % 2:
            c.setFillColor(LIGHT)
            c.rect(M, b.y - rh, W - 2 * M, rh, fill=1, stroke=0)
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(M + 6, b.y - 21, f"{u}. {UNIT_NAMES[u]}"[:44])
        for i in range(6):
            c.setStrokeColor(NAVY)
            c.setFillColor(white)
            c.circle(M + 215 + i * 44, b.y - 17, 9, fill=1, stroke=1)
        c.setFillColor(black)
        c.line(M + 215 + 6 * 44 - 14, b.y - 25, W - M - 6, b.y - 25)
        b.y -= rh
        if u == 5:
            c.setFillColor(CREAM)
            c.rect(M, b.y - 26, W - 2 * M, 26, fill=1, stroke=0)
            c.setFillColor(black)
            c.setFont("Helvetica-Bold", 10.5)
            c.drawString(M + 6, b.y - 17, "Check-Up (Units 1–5)")
            c.circle(M + 215, b.y - 13, 9, fill=0, stroke=1)
            c.line(M + 215 + 6 * 44 - 14, b.y - 21, W - M - 6, b.y - 21)
            b.y -= 26
    c.setFillColor(CREAM)
    c.rect(M, b.y - 26, W - 2 * M, 26, fill=1, stroke=0)
    c.setFillColor(black)
    c.drawString(M + 6, b.y - 17, "Final Test (Units 1–10)")
    c.circle(M + 215, b.y - 13, 9, fill=0, stroke=1)
    c.line(M + 215 + 6 * 44 - 14, b.y - 21, W - M - 6, b.y - 21)
    b.y -= 40
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 12.5)
    c.drawString(M, b.y - 8, "I can… (tick when you are confident)")
    b.y -= 24
    skills = skills or ["Count to 100 and say which number is bigger", "Add and subtract facts within 20 quickly",
              "Add and subtract two-digit numbers (with carrying and borrowing)", "Read and compare numbers up to 1000",
              "Skip count by 2s, 5s, 10s and 100s", "Multiply with equal groups (2s, 5s, 10s)",
              "Tell time to 5 minutes and count coins", "Name shapes, measure lengths, and write fractions",
              "Solve one-step and two-step word problems"]
    for i, s in enumerate(skills):
        x = M + (i % 2) * 270
        if i % 2 == 0 and i:
            b.y -= 20
        c.setStrokeColor(NAVY)
        c.rect(x, b.y - 12, 11, 11, fill=0)
        c.setFillColor(black)
        c.setFont("Helvetica", 9)
        c.drawString(x + 17, b.y - 10, s[:60])
    b.page()


def certificate(b):
    c = b.c
    b.rec["cert"] = c.getPageNumber()
    c.setStrokeColor(ORANGE)
    c.setLineWidth(6)
    c.rect(M, M + 120, W - 2 * M, H - 2 * M - 240)
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.5)
    c.rect(M + 12, M + 132, W - 2 * M - 24, H - 2 * M - 264)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(W / 2, H - 230, "Certificate of Achievement")
    c.setFillColor(ORANGE)
    c.setFont("Helvetica", 16)
    c.drawCentredString(W / 2, H - 275, "This certificate is proudly presented to")
    c.setStrokeColor(black)
    c.setLineWidth(1)
    c.line(W / 2 - 180, H - 335, W / 2 + 180, H - 335)
    c.setFillColor(black)
    c.setFont("Helvetica", 15)
    c.drawCentredString(W / 2, H - 385, "for completing all 10 units of the")
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(NAVY)
    c.drawCentredString(W / 2, H - 420, BOOK_TITLE)
    c.setFillColor(ORANGE)
    for i in range(5):
        p = c.beginPath()
        cx, cy = W / 2 - 80 + i * 40, H - 475
        for k in range(10):
            a = math.radians(90 + k * 36)
            r = 14 if k % 2 == 0 else 6
            px, py = cx + r * math.cos(a), cy + r * math.sin(a)
            p.moveTo(px, py) if k == 0 else p.lineTo(px, py)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(black)
    c.setFont("Helvetica", 12)
    c.drawString(W / 2 - 220, H - 560, "Date: ________________")
    c.drawString(W / 2 + 30, H - 560, "Signed: ________________")
    b.page(footer=False)


def answer_key(b):
    c = b.c
    b.rec["answers"] = c.getPageNumber()
    b.banner("Answer Key", "Check together • fix every mistake")
    first = True
    for label, items in b.answers:
        text = "  \u2022  ".join(f"{q}) {a}" for q, a in items)
        lines = simpleSplit(text, "Helvetica", 9.5, W - 2 * M - 16)
        need = 20 + 12.5 * len(lines)
        if b.y - need < 50:
            b.page()
            c.setFillColor(NAVY)
            c.setFont("Helvetica-Bold", 11)
            c.drawString(M, b.y - 10, "Answer Key (continued)")
            b.y -= 26
        c.setFillColor(LIGHT)
        c.rect(M, b.y - 16, W - 2 * M, 16, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(M + 6, b.y - 12, label)
        b.y -= 16 + 4
        c.setFillColor(black)
        c.setFont("Helvetica", 9.5)
        for ln in lines:
            c.drawString(M + 8, b.y - 10, ln)
            b.y -= 12.5
        b.y -= 6
    b.foot_draw()
    c.showPage()


def build(path, pages):
    b = Book(path, pages)
    cover(b)
    guide(b)
    contents(b, pages)
    tracker(b)
    for u in range(1, 11):
        b.rec[f"u{u}"] = b.c.getPageNumber()
        b.lesson(u)
        A, B = G.unit_sheets(u, 0), G.unit_sheets(u, 1)
        for sa, sb in zip(A, B):
            b.sheet(sa, f"Unit {u} • Day {sa['day']}", "A")
            b.sheet(sb, f"Unit {u} • Day {sb['day']}", "B")
        if u == 5:
            b.rec["checkup"] = b.c.getPageNumber()
            b.sheet(G.checkup_a(), "")
    b.rec["final"] = b.c.getPageNumber()
    b.sheet(G.final_test(), "")
    certificate(b)
    answer_key(b)
    b.c.save()
    return b.rec


if __name__ == "__main__":
    rec = build(OUT, {})
    rec = build(OUT, rec)   # second pass fills in contents page numbers
    print("pages:", rec)
