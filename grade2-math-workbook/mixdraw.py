"""Extra question types for the 'mixed' workbooks: word bank box and matching columns."""
from reportlab.lib.colors import Color, black
from reportlab.lib.utils import simpleSplit
import build_workbook as B
from build_workbook import NAVY, ORANGE, SOFT, CREAM, GREY


def d_bank(c, x, yt, w, h, data, **_):
    words = list(data)
    c.setFillColor(CREAM)
    c.setStrokeColor(Color(.9, .8, .5))
    c.roundRect(x + 4, yt - h + 4, w - 8, h - 6, 8, fill=1, stroke=1)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + 14, yt - 15, "Word bank:")
    c.setFillColor(black)
    lines = simpleSplit("   •   ".join(words), "Helvetica-Bold", 11, w - 110)
    c.setFont("Helvetica-Bold", 11)
    for i, ln in enumerate(lines[:2]):
        c.drawString(x + 86, yt - 15 - i * 14, ln)
    c.setStrokeColor(black)


def d_match(c, x, yt, w, h, data, **_):
    left, right = data["left"], data["right"]
    c.setFillColor(black)
    for i, (l_, r_) in enumerate(zip(left, right)):
        yy = yt - 20 - i * 24
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x + 22, yy, f"{i + 1})")
        c.setFont("Helvetica", 11.5)
        c.drawString(x + 44, yy, l_)
        c.setFillColor(NAVY)
        c.drawString(x + 196, yy, "____")
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x + 280, yy, "abcd"[i] + ")")
        c.setFont("Helvetica", 11.5)
        c.drawString(x + 298, yy, r_)


B.DRAW.update({"bank": d_bank, "match": d_match})
B.TOP_LABEL.update({"match"})
