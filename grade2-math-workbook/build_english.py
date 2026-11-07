#!/usr/bin/env python3
"""Builds Grade2_English_Mastery_Workbook.pdf using the same layout engine as the math book."""
import sys
from reportlab.lib.utils import simpleSplit
from reportlab.platypus import Paragraph
from reportlab.lib.colors import Color, black, white

import build_workbook as B
import english_generators as E
from build_workbook import (W, H, M, NAVY, TEAL, ORANGE, LIGHT, CREAM, MINT, GREY, SOFT, BLUE, BUL, SMALL)

OUT = sys.argv[1] if len(sys.argv) > 1 else "Grade2_English_Mastery_Workbook.pdf"
TITLE = "Grade 2 English Mastery Workbook"

# ------------------------------------------------------------ course data
B.BOOK_TITLE = TITLE
NAMES = {1: "Alphabet, Vowels & ABC Order", 2: "Short & Long Vowels", 3: "Blends, Digraphs & Word Families",
         4: "Nouns, Verbs & Plurals", 5: "Sentences & Punctuation", 6: "Opposites, Synonyms & Compounds",
         7: "Past Tense, Contractions & Endings", 8: "Reading Stories & Comprehension",
         9: "Adjectives, Homophones & Meaning", 10: "Writing & Challenges"}
LEVEL = {1: "Starter", 2: "Starter", 3: "Starter", 4: "Building", 5: "Building", 6: "Building",
         7: "Stretch", 8: "Stretch", 9: "Stretch", 10: "Challenge"}
CC = {1: "RF.2.3, L.2.2", 2: "RF.2.3", 3: "RF.2.3, RF.2.4", 4: "L.2.1, L.2.2", 5: "L.2.1, L.2.2",
      6: "L.2.4, L.2.5", 7: "L.2.1, L.2.2, L.2.4", 8: "RL.2.1, RL.2.2, RI.2.2", 9: "L.2.1, L.2.4, L.2.5",
      10: "W.2.3, W.2.5, L.2.2"}
for d, src in ((B.UNIT_NAMES, NAMES), (B.UNIT_LEVEL, LEVEL), (B.UNIT_CC, CC)):
    d.clear()
    d.update(src)
B.TOP_LABEL.update({"qline", "write", "passage"})


# ------------------------------------------------------------- drawers
def d_qline(c, x, yt, w, h, data, **_):
    c.setFillColor(black)
    c.setFont("Helvetica", 11.5)
    y = yt - 13
    for ln in simpleSplit(data, "Helvetica", 11.5, w - 30):
        c.drawString(x + 22, y, ln)
        y -= 14
    c.setStrokeColor(SOFT)
    c.setLineWidth(.8)
    c.setFillColor(GREY)
    c.setFont("Helvetica", 10)
    c.drawString(x + 22, yt - h + 10, "Answer:")
    c.line(x + 66, yt - h + 9, x + w - 12, yt - h + 9)
    c.setStrokeColor(black)


def d_write(c, x, yt, w, h, data, **_):
    c.setFillColor(black)
    c.setFont("Helvetica", 11.5)
    y = yt - 13
    for ln in simpleSplit(data, "Helvetica", 11.5, w - 30):
        c.drawString(x + 22, y, ln)
        y -= 14
    c.setStrokeColor(SOFT)
    c.setLineWidth(.8)
    ly = y - 12
    while ly > yt - h + 6:
        c.line(x + 22, ly, x + w - 12, ly)
        ly -= 22
    c.setStrokeColor(black)


def d_passage(c, x, yt, w, h, data, **_):
    title, text = data
    c.setFillColor(CREAM)
    c.setStrokeColor(Color(.9, .8, .5))
    c.roundRect(x, yt - h + 6, w, h - 6, 8, fill=1, stroke=1)
    c.setStrokeColor(black)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 12.5)
    c.drawString(x + 14, yt - 20, title)
    c.setFillColor(black)
    c.setFont("Helvetica", 11.5)
    y = yt - 38
    for ln in simpleSplit(text, "Helvetica", 11.5, w - 28):
        c.drawString(x + 14, y, ln)
        y -= 15


B.DRAW.update({"qline": d_qline, "write": d_write, "passage": d_passage})


# ----------------------------------------------------------------- art
def _text(c, x, y, s, font="Helvetica-Bold", size=11, color=black):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, s)


def art1(c, x, y, w, h):
    s = 17
    for i in range(26):
        L = chr(97 + i)
        r, k = divmod(i, 9)
        bx, by = x + 4 + k * s, y + h - 40 - r * (s + 6)
        c.setFillColor(Color(1, .85, .55) if L in "aeiou" else white)
        c.rect(bx, by, s, s, fill=1, stroke=1)
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(bx + s / 2, by + 4.5, L)
    _text(c, x + 4, y + h - 14, "The alphabet", "Helvetica-Oblique", 9)
    _text(c, x + 4, y + 36, "Vowels are orange: a e i o u", "Helvetica", 9.5, ORANGE)
    _text(c, x + 4, y + 20, "All other letters are consonants.", "Helvetica", 9.5, GREY)


def art2(c, x, y, w, h):
    _text(c, x + 8, y + h - 30, "short a", "Helvetica", 9.5, GREY)
    _text(c, x + 8, y + h - 52, "cap", "Courier-Bold", 20)
    _text(c, x + 70, y + h - 52, "+ e", "Courier-Bold", 16, ORANGE)
    _text(c, x + 8, y + h - 80, "long a", "Helvetica", 9.5, GREY)
    _text(c, x + 8, y + h - 102, "cape", "Courier-Bold", 20)
    _text(c, x + 8, y + h - 124, "The silent e makes", "Helvetica", 9.5, GREY)
    _text(c, x + 8, y + h - 136, "a say its name!", "Helvetica", 9.5, GREY)


def art3(c, x, y, w, h):
    items = [("sh", "ship"), ("ch", "chip"), ("th", "thin"), ("wh", "whale"), ("bl", "black"), ("st", "star")]
    for i, (a, b) in enumerate(items):
        bx, by = x + 8 + (i % 2) * 82, y + h - 56 - (i // 2) * 38
        c.setFillColor(LIGHT if i < 4 else CREAM)
        c.roundRect(bx, by, 74, 28, 6, fill=1, stroke=1)
        _text(c, bx + 8, by + 8, a, "Helvetica-Bold", 14, ORANGE)
        _text(c, bx + 34, by + 9, b, "Helvetica", 11)
    _text(c, x + 8, y + h - 14, "Digraphs (blue)   Blends (yellow)", "Helvetica-Oblique", 8.5, GREY)


def art4(c, x, y, w, h):
    for i, (hd, ws, col) in enumerate([("NOUNS", ["girl", "park", "ball", "dog"], BLUE), ("VERBS", ["run", "jump", "swim", "sing"], ORANGE)]):
        bx = x + 8 + i * 82
        c.setFillColor(col)
        c.roundRect(bx, y + h - 30, 74, 22, 5, fill=1, stroke=0)
        _text(c, bx + 10, y + h - 24, hd, "Helvetica-Bold", 11, white)
        for k, wd in enumerate(ws):
            _text(c, bx + 10, y + h - 50 - k * 18, wd, "Helvetica", 11)
    _text(c, x + 8, y + 12, "Person, place, thing  |  action", "Helvetica", 8.5, GREY)


def art5(c, x, y, w, h):
    _text(c, x + 8, y + h - 50, "The dog runs.", "Helvetica-Bold", 17)
    c.setStrokeColor(ORANGE)
    c.setLineWidth(2)
    c.line(x + 8, y + h - 54, x + 28, y + h - 54)
    c.line(x + 100, y + h - 54, x + 106, y + h - 54)
    c.setStrokeColor(black)
    c.setLineWidth(1)
    _text(c, x + 8, y + h - 74, "capital letter", "Helvetica", 9.5, ORANGE)
    _text(c, x + 88, y + h - 90, "end mark", "Helvetica", 9.5, ORANGE)
    _text(c, x + 8, y + h - 112, ".  tells    ?  asks    !  shouts", "Helvetica-Bold", 10.5)


def art6(c, x, y, w, h):
    rows = [("hot", "<>", "cold", "opposites"), ("big", "=", "large", "synonyms"), ("sun", "+", "flower", "compound")]
    for i, (a, o, b, lab) in enumerate(rows):
        yy = y + h - 36 - i * 34
        _text(c, x + 8, yy, a, "Helvetica-Bold", 13)
        _text(c, x + 62, yy, o, "Helvetica-Bold", 13, ORANGE)
        _text(c, x + 86, yy, b, "Helvetica-Bold", 13)
        _text(c, x + 8, yy - 13, lab, "Helvetica-Oblique", 9, GREY)


def art7(c, x, y, w, h):
    rows = [("walk", "walked"), ("go", "went"), ("do not", "don't"), ("un + happy", "unhappy")]
    for i, (a, b) in enumerate(rows):
        yy = y + h - 34 - i * 28
        _text(c, x + 8, yy, a, "Helvetica", 12)
        _text(c, x + 76, yy, ">", "Helvetica-Bold", 12, ORANGE)
        _text(c, x + 90, yy, b, "Helvetica-Bold", 12)
    _text(c, x + 8, y + 14, "past | irregular | contraction | prefix", "Helvetica", 8, GREY)


def art8(c, x, y, w, h):
    for i, q in enumerate(["Who?", "What?", "Where?", "When?", "Why?"]):
        cx, cy = x + 32 + (i % 3) * 52, y + h - 40 - (i // 3) * 48
        c.setFillColor([BLUE, ORANGE, TEAL, Color(.85, .35, .45), Color(.95, .75, .2)][i])
        c.circle(cx, cy, 22, fill=1, stroke=0)
        _text(c, cx - 15 if len(q) > 4 else cx - 12, cy - 4, q, "Helvetica-Bold", 10, white)
    _text(c, x + 8, y + 12, "Ask these five questions", "Helvetica-Oblique", 9, GREY)


def art9(c, x, y, w, h):
    _text(c, x + 8, y + h - 30, "see  /  sea", "Helvetica-Bold", 15)
    _text(c, x + 8, y + h - 46, "sound the same", "Helvetica", 9, GREY)
    _text(c, x + 8, y + h - 76, "the red apple", "Helvetica-Bold", 14)
    c.setStrokeColor(ORANGE)
    c.setLineWidth(2)
    c.line(x + 40, y + h - 79, x + 66, y + h - 79)
    c.setStrokeColor(black)
    c.setLineWidth(1)
    _text(c, x + 8, y + h - 94, "red = adjective", "Helvetica", 9, ORANGE)
    _text(c, x + 8, y + h - 124, "tall  taller  tallest", "Helvetica-Bold", 12)


def art10(c, x, y, w, h):
    for i, (hd, tx) in enumerate([("First", "Get an idea."), ("Next", "Write it."), ("Last", "Check it.")]):
        yy = y + h - 36 - i * 36
        c.setFillColor([LIGHT, CREAM, MINT][i])
        c.roundRect(x + 8, yy - 8, 140, 28, 6, fill=1, stroke=1)
        _text(c, x + 16, yy + 2, hd, "Helvetica-Bold", 11, ORANGE)
        _text(c, x + 62, yy + 2, tx, "Helvetica", 10.5)


B.ART.clear()
B.ART.update({1: art1, 2: art2, 3: art3, 4: art4, 5: art5, 6: art6, 7: art7, 8: art8, 9: art9, 10: art10})

# ------------------------------------------------------------- lessons
B.LESSONS.clear()
B.LESSONS.update({
    1: dict(goal="I can say the alphabet, tell vowels from consonants, and put words in ABC order.",
            learn=["There are <b>26 letters</b>. Five are <b>vowels</b>: a, e, i, o, u. The rest are <b>consonants</b>.",
                   "Each letter has a <b>capital</b> (A) and a <b>small</b> (a) form.",
                   "<b>ABC order:</b> look at the <b>first letter</b>. <i>ant</i> comes before <i>bee</i>.",
                   "If the first letters match, look at the <b>second letter</b>: <i>bag</i> comes before <i>bat</i>."],
            ex=[("Next letter", ["~What comes after m?", "m, n", "= n"]),
                ("ABC order", ["cat, ant, bee", "~Look at first letters", "ant bee cat"]),
                ("Same start", ["bat, bag, bed", "~Look at 2nd letters", "bag bat bed"])],
            tip="Sing the alphabet song to find a missing letter.",
            tryit=[("seq", [(["a", "b", None, "d", "e", None, "g", "h"], "c, f")], 1, 36),
                   ("eq", [("What letter comes after p?  ____", "q"), ("Is 'o' a vowel or a consonant?  ____", "vowel"),
                           ("dog, ant, cat   " + E.ARROW + "   ____ , ____ , ____", "ant, cat, dog")], 1, 30)]),
    2: dict(goal="I can read and spell short vowel words and long vowel words.",
            learn=["<b>Short vowels</b> make little sounds: a (cat), e (bed), i (pig), o (pot), u (sun).",
                   "A <b>silent e</b> at the end makes the vowel say its name: cap + e = <b>cape</b>.",
                   "Two vowels can <b>team up</b>: ai (rain), ay (play), ee (tree), ea (leaf), oa (boat).",
                   "In a vowel team, the first vowel usually says its name and the second is quiet."],
            ex=[("Short vowel", ["c_t", "~a pet that purrs", "= a (cat)"]),
                ("Silent e", ["kit + e", "~the i says its name", "= kite"]),
                ("Vowel team", ["r__n", "~water from clouds", "= ai (rain)"])],
            tip="Say the word slowly. Do you hear the vowel's name or its little sound?",
            tryit=[("eq", [("p__n   (you write with it)", "e"), ("tub + e = ____", "tube"),
                           ("b__t   (floats on water) [oa / ee]", "oa"), ("Is 'bike' long or short?  ____", "long")], 1, 30)]),
    3: dict(goal="I can use blends, digraphs and word families to read new words.",
            learn=["A <b>digraph</b> is two letters with ONE sound: <b>sh</b>ip, <b>ch</b>air, <b>th</b>in, <b>wh</b>ale, du<b>ck</b>.",
                   "A <b>blend</b> is two letters that keep their own sounds: <b>fr</b>og, <b>bl</b>ack, <b>st</b>ar.",
                   "A <b>word family</b> shares an ending: cat, bat, hat, mat all end in <b>-at</b>.",
                   "Words that <b>rhyme</b> end with the same sound."],
            ex=[("Digraph", ["__ip", "~sails on the sea", "= sh (ship)"]),
                ("Blend", ["__og", "~green, hops", "= fr (frog)"]),
                ("Word family", ["b + ack", "~onset + ending", "= back"])],
            tip="Change the first sound to make a whole family of new words.",
            tryit=[("eq", [("__ale   (a giant sea animal) [wh / sh / ch]", "wh"), ("__ab   (a sea animal with claws) [cr / fl / sp]", "cr"),
                           ("h + ill = ____", "hill"), ("Which word rhymes with cake?  (lake / lock)  ____", "lake")], 1, 30)]),
    4: dict(goal="I can find nouns and verbs and make plurals.",
            learn=["A <b>noun</b> names a person, place or thing: <i>girl, park, ball</i>.",
                   "A <b>verb</b> is an action word: <i>run, jump, swim</i>.",
                   "<b>Plural</b> means more than one. Add <b>-s</b>: cats. Add <b>-es</b> after s, x, ch, sh: boxes, dishes.",
                   "Change <b>y to ies</b>: baby, babies. Some plurals are special: child, children; foot, feet."],
            ex=[("Noun or verb?", ["~dog / run", "dog = noun", "run = verb"]),
                ("Add -es", ["one box", "two ____", "= boxes"]),
                ("y to ies", ["one baby", "two ____", "= babies"])],
            tip="If you can do it (run, jump, eat), it is a verb.",
            tryit=[("eq", [("Is 'teacher' a noun or a verb?  ____", "noun"), ("Is 'dance' a noun or a verb?  ____", "verb"),
                           ("one dish, two ____", "dishes"), ("one city, two ____", "cities")], 2, 30)]),
    5: dict(goal="I can write complete sentences with capital letters and end marks.",
            learn=["A <b>sentence</b> tells a whole idea: who or what, and what happens. <i>The dog runs.</i>",
                   "Start with a <b>capital letter</b>. Names, days, months, places and <b>I</b> are capitalized too.",
                   "End with <b>.</b> (telling), <b>?</b> (asking) or <b>!</b> (excited).",
                   "Words must be in the right <b>order</b> to make sense."],
            ex=[("Sentence?", ["~In the park", "~no who or what", "= not a sentence"]),
                ("End mark", ["Where is my hat", "~it asks", "= ?"]),
                ("Capitals", ["mia lives in paris.", "~names, places", "Mia, Paris"])],
            tip="Read your sentence aloud. Does it sound finished?",
            tryit=[("eq", [("The dog barks   Complete sentence?  ____", "yes"), ("Under the table   Complete sentence?  ____", "no"),
                           ("What is your name ____", "?"), ("Wow, that is great ____", "!")], 1, 30)]),
    6: dict(goal="I can use opposites, synonyms and compound words.",
            learn=["<b>Opposites</b> (antonyms) mean the reverse: hot and cold, up and down.",
                   "<b>Synonyms</b> mean almost the same: big and large, glad and happy.",
                   "A <b>compound word</b> is two small words joined: sun + flower = <b>sunflower</b>.",
                   "Knowing word pairs helps you read and write with more exciting words."],
            ex=[("Opposite", ["hot", "~the reverse", "= cold"]),
                ("Synonym", ["big", "~means the same", "= large"]),
                ("Compound", ["rain + bow", "~two words join", "= rainbow"])],
            tip="Try swapping a word for its synonym to make your writing more interesting.",
            tryit=[("eq", [("The opposite of 'up' is ____   (down / left)", "down"), ("Which word means the same as 'glad'?  (happy / sad)  ____", "happy"),
                           ("tooth + brush = ____", "toothbrush"), ("foot + ____ = football", "ball")], 1, 30)]),
    7: dict(goal="I can use past tense, contractions, prefixes and suffixes.",
            learn=["<b>Past tense</b> tells what already happened. Most verbs add <b>-ed</b>: walk, walked.",
                   "Spelling changes: bake, <b>baked</b> (drop e); hop, <b>hopped</b> (double); cry, <b>cried</b> (y to i).",
                   "<b>Irregular</b> verbs change: go, <b>went</b>; run, <b>ran</b>; eat, <b>ate</b>.",
                   "A <b>contraction</b> joins two words: do not = <b>don't</b>. The apostrophe replaces letters.",
                   "<b>un-</b> means not (unhappy). <b>re-</b> means again (rewrite). <b>-ful</b> means full of (careful)."],
            ex=[("Past tense", ["jump", "~add -ed", "= jumped"]),
                ("Irregular", ["go", "~special change", "= went"]),
                ("Contraction", ["do not", "~apostrophe", "= don't"])],
            tip="Say it aloud: “I goed” does not sound right. “I went” does.",
            tryit=[("eq", [("clap " + E.ARROW + " ____ (past)", "clapped"), ("eat " + E.ARROW + " ____ (past)", "ate"),
                           ("I am = ____", "I'm"), ("re + write = ____", "rewrite")], 2, 30)]),
    8: dict(goal="I can read a story and answer who, what, where, when and why questions.",
            learn=["<b>Read</b> the whole passage once. Then read it again slowly.",
                   "Ask: <b>Who</b> is it about? <b>What</b> happens? <b>Where</b> and <b>when</b>? <b>Why</b> does it happen?",
                   "Go back to the text to <b>find the answer</b>. Underline it.",
                   "The <b>main idea</b> is what the whole passage is mostly about."],
            ex=[("Who?", ["~Pip is a cat.", "~Who is the story", "= Pip"]),
                ("Where?", ["~Pip naps in the sun.", "~Where does Pip nap?", "= in the sun"]),
                ("Why?", ["~Pip is tired.", "~Why does Pip nap?", "= she is tired"])],
            tip="Answer in a full sentence when you can: “Pip naps in the sun.”",
            tryit=[("passage", [(("Pip the Cat", "Pip is a little cat. She naps in the warm sun. When she wakes up, she chases a bug."), None)], 1, 82),
                   ("qline", [("Where does Pip nap?", "in the warm sun"), ("What does Pip chase?", "a bug")], 1, 46)]),
    9: dict(goal="I can use adjectives, homophones and context clues to understand words.",
            learn=["An <b>adjective</b> describes a noun: <i>red</i> apple, <i>tiny</i> ant, <i>loud</i> drum.",
                   "Add <b>-er</b> to compare two things and <b>-est</b> for three or more: tall, taller, tallest.",
                   "<b>Homophones</b> sound the same but are spelled differently: see/sea, no/know, to/too/two.",
                   "Some words have <b>more than one meaning</b>. Use the sentence to decide.",
                   "<b>Context clues</b> are nearby words that help you figure out a new word."],
            ex=[("Adjective", ["the red apple", "~which word describes?", "= red"]),
                ("Homophone", ["I ___ a bird.", "~see or sea?", "= see"]),
                ("Context", ["~The enormous elephant was as big as a house.", "= very big"])],
            tip="If two words sound alike, read the whole sentence to see which spelling fits.",
            tryit=[("eq", [("the shiny coin   Adjective: ____", "shiny"), ("Please ____ your name. (write / right)", "write"),
                           ("hot:  one is hot, two is ____, three is the ____", "hotter, hottest")], 1, 30)]),
    10: dict(goal="I can write sentences and a short paragraph, and fix my mistakes.",
             learn=["<b>Plan:</b> think of your idea first. Say your sentences out loud.",
                    "<b>Write:</b> start each sentence with a capital letter and end it with . ? or !.",
                    "Use <b>sequence words</b>: First, Next, Then, Last. Add describing words to tell more.",
                    "<b>Check:</b> read it again. Fix spelling, capitals and end marks."],
             ex=[("Sequence", ["~First, I woke up.", "~Then I ate.", "~Last, I went to school."]),
                 ("Add details", ["~I have a dog.", "~I have a fluffy", "~brown dog named Max."]),
                 ("Fix it", ["i like pizza", "~capital + end mark", "I like pizza."])],
             tip="Good writers always read their work twice before they say “done”.",
             tryit=[("write", [("Write one sentence about your favorite food.", "Answers vary. Check: capital letter, end mark, complete idea.")], 1, 70),
                    ("qline", [("Fix the sentence:  we goed to the park", "We went to the park.")], 1, 46)]),
})


# -------------------------------------------------------- front matter
def cover(b):
    c = b.c
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    cols = [ORANGE, TEAL, BLUE, Color(.95, .75, .2), Color(.85, .35, .45)]
    for i, ch in enumerate("AaBbCcDdEeFfGg"):
        x, y = 60 + (i % 7) * 82, 110 + (i // 7) * 92
        c.setFillColor(cols[i % len(cols)])
        c.circle(x, y, 28, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(x, y - 10, ch)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(W / 2, H - 170, "Grade 2")
    c.drawCentredString(W / 2, H - 222, "English Mastery")
    c.drawCentredString(W / 2, H - 274, "Workbook")
    c.setFillColor(Color(1, .85, .5))
    c.setFont("Helvetica", 17)
    c.drawCentredString(W / 2, H - 316, "From letters and sounds to stories and writing")
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
    c.drawCentredString(W / 2, 22, "Aligned to Common Core Grade 2 English Language Arts. Inspired by small-step, "
                                  "mastery-based learning; not affiliated with or endorsed by Kumon.")
    b.page(footer=False)


def guide(b):
    c = b.c
    b.rec["guide"] = c.getPageNumber()
    b.banner("A Note for Parents & Teachers", "How to use this book")
    blocks = [
        ("The method (small steps, repeated until mastered)",
         ["<b>Tiny steps.</b> Each sheet is only a little harder than the last, so a child almost always succeeds.",
          "<b>Sounds first, then words, sentences, stories.</b> Units 1–3 build phonics, Units 4–7 build grammar and word skills, Units 8–10 build reading and writing.",
          "<b>Ten short sheets per skill.</b> Two sheets a day (Sheet A, then Sheet B with new words on the same skill) build accuracy and fluency.",
          "<b>Correct every mistake.</b> Check with the answer key and let your child fix each wrong answer.",
          "<b>Read aloud daily.</b> Add 10 minutes of reading together every day. It makes every unit stronger."]),
        ("The weekly rhythm (about 12 weeks, 5 days a week, 10–15 minutes)",
         ["<b>Lesson day:</b> read the lesson together, study the examples, do “Try it yourself”.",
          "<b>Days 1–4:</b> two practice sheets a day. Write the time at the top of each sheet.",
          "<b>Day 5:</b> mixed review sheets. In Unit 10, Day 5 is a writing challenge.",
          "<b>Goal:</b> 90% or better. Below 80%? Repeat the sheet tomorrow (print a spare copy first).",
          "Take the Check-Up after Unit 5 and the Final Test at the end."]),
        ("About open-ended answers",
         ["Reading and writing questions often have more than one good answer. The answer key gives a <b>sample</b>; accept any answer that makes sense and is a complete sentence.",
          "For writing, use the checklist: capital letters, end marks, complete sentences, and neat spelling.",
          "Praise effort first. Stop before frustration builds."])]
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
    q = Paragraph("<b>About the levels:</b> Kumon’s own pages do not match its levels to school grades, so this book follows the "
                  "Common Core Grade 2 English standards (listed per unit on the next page) and rises from <b>Starter</b> (Units 1–3) to "
                  "<b>Building</b> (4–6), <b>Stretch</b> (7–9) and <b>Challenge</b> (10).", SMALL)
    _, hh = q.wrap(W - 2 * M - 20, 1000)
    q.drawOn(c, M + 10, b.y - 8 - hh)
    b.page()


SKILLS = ["Say the alphabet and put words in ABC order", "Read and spell short and long vowel words",
          "Use blends, digraphs and word families", "Tell nouns from verbs and make plurals",
          "Write complete sentences with capitals and end marks", "Use opposites, synonyms and compound words",
          "Use past tense, contractions, prefixes and suffixes", "Read a story and answer questions",
          "Use adjectives, homophones and context clues", "Write a short paragraph and fix mistakes"]


def build(path, pages):
    b = B.Book(path, pages)
    cover(b)
    guide(b)
    B.contents(b, pages)
    B.tracker(b, SKILLS)
    for u in range(1, 11):
        b.rec[f"u{u}"] = b.c.getPageNumber()
        b.lesson(u)
        A, Bs = E.unit_sheets(u, 0), E.unit_sheets(u, 1)
        for sa, sb in zip(A, Bs):
            b.sheet(sa, f"Unit {u} • Day {sa['day']}", "A")
            b.sheet(sb, f"Unit {u} • Day {sb['day']}", "B")
        if u == 5:
            b.rec["checkup"] = b.c.getPageNumber()
            b.sheet(E.checkup_a(), "")
    b.rec["final"] = b.c.getPageNumber()
    b.sheet(E.final_test(), "")
    B.certificate(b)
    B.answer_key(b)
    b.c.save()
    return b.rec


if __name__ == "__main__":
    rec = build(OUT, {})
    rec = build(OUT, rec)
    print("pages:", rec)
