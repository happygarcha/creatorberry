"""Picture-based question generators for the Grade 2 Social Studies workbook."""
import random
from english_generators import take, fit, ARROW
from generators import sec, sheet
from sticons import LBL

# ------------------------------------------------------------------ builders
def PIC(rng, q, correct, pool, n=3):
    d = [k for k in pool if k != correct]
    opts = [correct] + rng.sample(d, min(n - 1, len(d)))
    rng.shuffle(opts)
    return (q, opts), "ABCD"[opts.index(correct)]


def PICF(rng, q, correct, options):
    opts = list(options)
    rng.shuffle(opts)
    return (q, opts), "ABCD"[opts.index(correct)]


def WORD(rng, key, correct, pool_words, q="What is this?", n=3):
    ws = [correct] + rng.sample([w for w in pool_words if w != correct], min(n - 1, len(pool_words) - 1))
    rng.shuffle(ws)
    return (key, f"{q}  ({' / '.join(ws)})"), correct


def WORDF(rng, key, correct, words, q):
    ws = list(words)
    rng.shuffle(ws)
    return (key, f"{q}  ({' / '.join(ws)})"), correct


def lw(keys):
    return [LBL[k] for k in keys]


def pics(items, head=""):
    return sec(head, "pic", items, 2, 92)


def words(items, head=""):
    return sec(head, "word", items, 2, 62)


def eqs(items, head="", cols=1):
    return sec(head, "eq", items, cols, 30)


def draw(prompt):
    return sec("Draw it!", "draw", [(prompt, None)], 1, 108)


FEELS = ["happy", "sad", "angry", "surprised", "tired"]
FEELW = {"happy": "happy", "sad": "sad", "angry": "angry", "surprised": "surprised", "tired": "sleepy"}
FAM = ["mom", "dad", "baby", "grandma", "grandpa", "girl", "boy"]
HOMES = ["house", "apartment", "tent", "houseboat"]
PLACES = ["school", "hospital", "library", "store", "park", "bank", "postoffice", "firehall"]
HELP = ["doctor", "teacher", "firefighter", "police", "mail", "builder", "farmer", "cook"]
THINGS = ["bed", "shirt", "toothbrush", "bread", "backpack", "ball", "book", "water", "umbrella", "apple"]
VEH = ["car", "bus", "bike", "truck", "train", "plane", "ferry", "canoe", "tractor"]


# ============================================================== UNIT 1
def U1(day, rng, v):
    t = "All About Me & My Family"
    inst = "Look at the pictures. Pick the best answer."
    if day == 1:
        a = [PIC(rng, f"Which face is {FEELW[f]}?", f, FEELS) for f in take(FEELS * 2, 10, v, "k1d1")]
        b = [WORD(rng, f, LBL[f], lw(FEELS), "How does this face feel?") for f in take(FEELS * 2, 6, v, "k1d1b")]
        return sheet(1, 1, t, inst, "Example: Which face is happy?  " + ARROW + "  pick the smiling face",
                     [pics(a, "Part A – Find the face"), words(b, "Part B – Name the feeling")])
    if day == 2:
        a = [WORD(rng, k, LBL[k], lw(FAM), "Who is this?") for k in take(FAM * 2, 8, v, "k1d2a")]
        b = [PIC(rng, f"Which one is the {LBL[k]}?", k, FAM) for k in take(FAM * 2, 6, v, "k1d2b")]
        return sheet(1, 2, t, inst, "Example: Who is this?  " + ARROW + "  mom", [words(a, "Part A – Who is this?"), pics(b, "Part B – Find the person")])
    if day == 3:
        R_ = [("What do you sleep in?", "bed"), ("What do you wear?", "shirt"), ("What do you brush after eating?", "toothbrush"),
              ("What do you eat for breakfast?", "bread"), ("What do you carry to school?", "backpack"), ("What do you play with?", "ball"),
              ("What do you read?", "book"), ("What do you drink?", "water"), ("What keeps you dry in rain?", "umbrella"), ("What is a healthy snack?", "apple")]
        a = [PIC(rng, q, k, THINGS) for q, k in take(R_, 8, v, "k1d3a")]
        cnt = []
        for k in take(["girl", "boy", "mom", "dad", "baby"] * 2, 4, v, "k1d3b"):
            n = rng.randint(2, 8)
            cnt.append(((k, n, f"How many {LBL[k]}s?  ____" if k not in ("baby",) else "How many babies?  ____"), n))
        return sheet(1, 3, t, inst, "Example: What do you sleep in?  " + ARROW + "  bed",
                     [pics(a, "Part A – My day"), sec("Part B – Count them", "count", cnt, 2, 62)])
    if day == 4:
        fixed = [("Who is the oldest?", "grandpa", ["baby", "girl", "grandpa"]), ("Who is the youngest?", "baby", ["mom", "baby", "dad"]),
                 ("Which is a grandma?", "grandma", ["grandma", "mom", "girl"]), ("Which is a baby?", "baby", ["baby", "boy", "dad"]),
                 ("Who is the oldest?", "grandma", ["boy", "grandma", "mom"]), ("Who is the youngest?", "boy", ["boy", "dad", "grandpa"]),
                 ("Which is a dad?", "dad", ["dad", "baby", "girl"]), ("Which is a mom?", "mom", ["boy", "mom", "grandpa"])]
        a = [PICF(rng, q, c, o) for q, c, o in take(fixed, 8, v, "k1d4a")]
        ages = {"baby": "baby", "girl": "child", "boy": "child", "mom": "grown-up", "dad": "grown-up", "grandma": "grandparent", "grandpa": "grandparent"}
        b = [WORDF(rng, k, ages[k], ["baby", "child", "grown-up", "grandparent"], "Which age?") for k in take(list(ages) * 2, 6, v, "k1d4b")]
        return sheet(1, 4, t, "Families have babies, kids, grown-ups and grandparents.", "Example: Who is the youngest?  " + ARROW + "  baby",
                     [pics(a, "Part A – Young and old"), words(b, "Part B – Which age?")])
    a = [PIC(rng, f"Which face is {FEELW[f]}?", f, FEELS) for f in take(FEELS, 3, v, "k1d5a")]
    b = [WORD(rng, k, LBL[k], lw(FAM), "Who is this?") for k in take(FAM, 3, v, "k1d5b")]
    c_ = [PIC(rng, q, k, THINGS) for q, k in take([("What do you sleep in?", "bed"), ("What do you read?", "book"), ("What do you wear?", "shirt"), ("What do you drink?", "water")], 3, v, "k1d5c")]
    return sheet(1, 5, t, "Review day! Then draw your picture.", "Example: Who is this?  " + ARROW + "  dad",
                 [pics(a + c_, "Faces and my day"), words(b, "Who is this?"), draw(["Draw your family.", "Draw something that makes you happy."][v])])


# ============================================================== UNIT 2
HOME_Q = [("Which home floats on water?", "houseboat"), ("Which home has many families inside?", "apartment"), ("Which home is easy to carry?", "tent"),
          ("Which home has a roof and a chimney?", "house"), ("Which home can you take camping?", "tent"), ("Which home is a tall building?", "apartment")]
HOME_USE = [("What do you use to sleep?", "bed"), ("What do you use to cook?", "stove"), ("What do you use to take a bath?", "tub"),
            ("What do you use to sit and rest?", "sofa"), ("What keeps food cold?", "fridge"), ("What do you use to brush your teeth?", "toothbrush"),
            ("What gives light at night?", "lamp"), ("What do you use to watch shows?", "tv")]
HOME_POOL = ["bed", "stove", "tub", "sofa", "fridge", "toothbrush", "lamp", "tv"]
ROOM = {"bed": "bedroom", "stove": "kitchen", "fridge": "kitchen", "tub": "bathroom", "sofa": "living room", "toothbrush": "bathroom", "tv": "living room"}


def U2(day, rng, v):
    t = "My Home & Neighbourhood"
    inst = "Look at the pictures. Pick the best answer."
    if day == 1:
        a = [WORD(rng, k, LBL[k], lw(HOMES), "What kind of home?") for k in take(HOMES * 3, 10, v, "k2d1a")]
        b = [PIC(rng, q, k, HOMES) for q, k in take(HOME_Q, 6, v, "k2d1b")]
        return sheet(2, 1, t, inst, "Example: What kind of home?  " + ARROW + "  tent", [words(a, "Part A – Kinds of homes"), pics(b, "Part B – Which home?")])
    if day == 2:
        a = [PIC(rng, q, k, HOME_POOL) for q, k in take(HOME_USE, 8, v, "k2d2a")]
        b = [WORDF(rng, k, r, ["bedroom", "kitchen", "bathroom", "living room"], "Which room?") for k, r in take(list(ROOM.items()), 6, v, "k2d2b")]
        return sheet(2, 2, t, inst, "Example: What do you use to sleep?  " + ARROW + "  bed", [pics(a, "Part A – Things in my home"), words(b, "Part B – Which room?")])
    if day == 3:
        a = [WORD(rng, k, LBL[k], lw(PLACES), "What place is this?") for k in take(PLACES * 2, 12, v, "k2d3")]
        return sheet(2, 3, t, "Name the places in a neighbourhood.", "Example: What place is this?  " + ARROW + "  school", [words(a, "Name the place")])
    if day == 4:
        spec = make_map(rng)
        return sheet(2, 4, t, "Read the map. Answer the questions.", "Example: Look at the row and column numbers.",
                     [sec("My neighbourhood map", "diagram", [(spec, None)], 1, 176), eqs(map_questions(rng, spec, 6, mode="place"), "Questions")])
    a = [WORD(rng, k, LBL[k], lw(HOMES), "What kind of home?") for k in take(HOMES * 2, 3, v, "k2d5a")]
    b = [PIC(rng, q, k, HOME_POOL) for q, k in take(HOME_USE, 3, v, "k2d5b")]
    c_ = [WORD(rng, k, LBL[k], lw(PLACES), "What place is this?") for k in take(PLACES, 4, v, "k2d5c")]
    return sheet(2, 5, t, "Review day! Then draw your picture.", "Example: What kind of home?  " + ARROW + "  house",
                 [words(a + c_, "Homes and places"), pics(b, "Things in my home"), draw(["Draw your home.", "Draw your street."][v])])


# ------------------------------------------------------------ maps & graphs
BUILD = ["school", "hospital", "library", "store", "park", "bank", "postoffice", "firehall", "house", "apartment"]
DIRS = {"north": (-1, 0, "north (above)"), "south": (1, 0, "south (below)"), "east": (0, 1, "east (right)"), "west": (0, -1, "west (left)")}


def make_map(rng, rows=3, cols=4, nb=6):
    cells = [(r, c) for r in range(rows) for c in range(cols)]
    rng.shuffle(cells)
    bl = rng.sample(BUILD, nb)
    return {"type": "map", "rows": rows, "cols": cols, "cells": dict(zip(cells[:nb], bl)),
            "deco": {cell: "tree" for cell in cells[nb:nb + 3]}}


def map_questions(rng, spec, n, mode="all"):
    out, tries = [], 0
    cells = spec["cells"]
    names = list(cells.values())
    while len(out) < n and tries < 200:
        tries += 1
        kind = rng.choice(["place", "dir", "dir", "count"] if mode == "all" else ["place"] if mode == "place" else ["dir"])
        if kind == "place":
            (r, c), b = rng.choice(list(cells.items()))
            o = [LBL[b]] + rng.sample([LBL[x] for x in BUILD if x != b], 2)
            rng.shuffle(o)
            qtxt = f"What is in row {r + 1}, column {c + 1}?  ({' / '.join(o)})"
            if any(q.startswith(f"What is in row {r + 1}, column {c + 1}?") for q, _ in out):
                continue
            out.append((qtxt, LBL[b]))
        elif kind == "dir":
            (r, c), b = rng.choice(list(cells.items()))
            dname = rng.choice(list(DIRS))
            dr, dc, shown = DIRS[dname]
            nb = cells.get((r + dr, c + dc))
            if not nb:
                continue
            o = [LBL[nb]] + rng.sample([LBL[x] for x in BUILD if x != nb], 2)
            rng.shuffle(o)
            qtxt = f"What is {shown} of the {LBL[b]}?  ({' / '.join(o)})"
            if any(q.startswith(f"What is {shown} of the {LBL[b]}?") for q, _ in out):
                continue
            out.append((qtxt, LBL[nb]))
        else:
            if any(q.startswith("How many buildings") for q, _ in out):
                continue
            out.append(("How many buildings are on the map?  ____", len(cells)))
    return [(q, str(a)) for q, a in out]


def make_graph(rng, keys, n=3):
    ks = rng.sample(keys, n)
    counts = rng.sample(range(1, 9), n)
    return {"type": "graph", "items": list(zip(ks, counts))}


def graph_questions(rng, spec, n):
    it = spec["items"]
    qs = []
    top = max(it, key=lambda x: x[1])
    low = min(it, key=lambda x: x[1])
    qs.append((f"Which has the most?  ({' / '.join(rng.sample([LBL[k] for k, _ in it], len(it)))})", LBL[top[0]]))
    qs.append((f"Which has the fewest?  ({' / '.join(rng.sample([LBL[k] for k, _ in it], len(it)))})", LBL[low[0]]))
    for k, c_ in it:
        qs.append((f"How many {LBL[k]}s?  ____".replace("housess", "houses"), c_))
    a, b = it[0], it[1]
    qs.append((f"How many more {LBL[a[0]]}s than {LBL[b[0]]}s?  ____ (0 if fewer)", max(a[1] - b[1], 0)))
    qs.append(("How many are there in all?  ____", sum(c_ for _, c_ in it)))
    rng.shuffle(qs)
    return [(q, str(a_)) for q, a_ in qs[:n]]


# ============================================================== UNIT 3
JOBTOOL = [("doctor", "stethoscope"), ("firefighter", "hose"), ("teacher", "chalkboard"), ("mail", "letter"), ("builder", "hammer"),
           ("farmer", "tractor"), ("cook", "pot"), ("police", "badge")]
TOOLPOOL = [b for _, b in JOBTOOL]
WORKP = [("doctor", "hospital"), ("teacher", "school"), ("firefighter", "firehall"), ("mail", "postoffice"), ("farmer", "barn"), ("builder", "house")]
NEEDH = [("You are sick.", "doctor"), ("There is a fire!", "firefighter"), ("You want to learn to read.", "teacher"), ("You need to mail a letter.", "mail"),
         ("A new house is needed.", "builder"), ("We need food from a farm.", "farmer"), ("Someone is in danger.", "police"), ("You want a hot meal.", "cook")]


def U3(day, rng, v):
    t = "Community Helpers"
    inst = "Look at the pictures. Pick the best answer."
    if day == 1:
        a = [WORD(rng, k, LBL[k], lw(HELP), "Who is this helper?") for k in take(HELP * 2, 12, v, "k3d1")]
        return sheet(3, 1, t, "Community helpers make our town a good place to live.", "Example: Who is this helper?  " + ARROW + "  doctor", [words(a, "Name the helper")])
    if day == 2:
        a = [PIC(rng, f"Which tool does a {LBL[j]} use?", tl, TOOLPOOL) for j, tl in take(JOBTOOL, 8, v, "k3d2a")]
        b = [WORD(rng, tl, LBL[j], lw(HELP), "Who uses this?") for j, tl in take(JOBTOOL, 6, v, "k3d2b")]
        return sheet(3, 2, t, inst, "Example: Which tool does a doctor use?  " + ARROW + "  stethoscope", [pics(a, "Part A – Pick the tool"), words(b, "Part B – Who uses it?")])
    if day == 3:
        a = [PIC(rng, q, j, HELP) for q, j in take(NEEDH, 8, v, "k3d3")]
        return sheet(3, 3, t, "Who can help? Pick the helper.", "Example: You are sick.  " + ARROW + "  doctor", [pics(a, "Who can help?")])
    if day == 4:
        a = [PIC(rng, f"Where does a {LBL[j]} work?", p, PLACES + ["barn", "house"]) for j, p in take(WORKP, 6, v, "k3d4a")]
        b = [WORD(rng, p, LBL[j], lw(HELP), "Who works here?") for j, p in take(WORKP, 6, v, "k3d4b")]
        return sheet(3, 4, t, inst, "Example: Where does a teacher work?  " + ARROW + "  school", [pics(a, "Part A – Where do they work?"), words(b, "Part B – Who works here?")])
    odd = []
    for _ in range(3):
        hs = rng.sample(HELP, 3)
        ob = rng.choice(["ball", "teddy", "candy", "game"])
        opts = hs + [ob]
        rng.shuffle(opts)
        odd.append((("Which is NOT a helper?", opts), "ABCD"[opts.index(ob)]))
    a = [WORD(rng, k, LBL[k], lw(HELP), "Who is this helper?") for k in take(HELP, 3, v, "k3d5a")]
    b = [PIC(rng, q, j, HELP) for q, j in take(NEEDH, 3, v, "k3d5b")]
    return sheet(3, 5, t, "Review day! Then draw your picture.", "Example: You are sick.  " + ARROW + "  doctor",
                 [words(a, "Who is this?"), pics(b + odd, "Who can help?"), draw(["Draw a community helper.", "Draw someone who helps you."][v])])


# ============================================================== UNIT 4
NATURAL = ["tree", "mountain", "river", "lake", "ocean", "forest", "flower", "cedar", "island"]
BUILT = ["house", "school", "store", "bridge", "apartment", "hospital", "library", "bank", "car", "playground"]
PLACE_Q = [("Where do you borrow books?", "library"), ("Where do you get well?", "hospital"), ("Where do you keep money safe?", "bank"),
           ("Where do you mail a letter?", "postoffice"), ("Where do fire trucks stay?", "firehall"), ("Where do you play outside?", "park"),
           ("Where do you buy food?", "store"), ("Where do you learn?", "school")]


def U4(day, rng, v):
    t = "Places in Our Community"
    inst = "Look at the pictures. Pick the best answer."
    if day == 1:
        items = [(k, "found in nature") for k in take(NATURAL, 7, v, "k4d1a")] + [(k, "made by people") for k in take(BUILT, 7, v, "k4d1b")]
        rng.shuffle(items)
        a = [WORDF(rng, k, ans, ["made by people", "found in nature"], "Nature or built?") for k, ans in items]
        return sheet(4, 1, t, "Some things grow in nature. Some things are made by people.", "Example: tree  " + ARROW + "  found in nature", [words(a, "Nature or built?")])
    if day == 2:
        a = [PIC(rng, q, p, PLACES) for q, p in take(PLACE_Q, 8, v, "k4d2")]
        return sheet(4, 2, t, inst, "Example: Where do you borrow books?  " + ARROW + "  library", [pics(a, "Where do you go?")])
    if day == 3:
        spec = make_graph(rng, ["house", "tree", "store", "car", "school", "park"], 3)
        return sheet(4, 3, t, "Count the pictures on the graph. Answer the questions.", "Example: The tallest bar has the most.",
                     [sec("Things in our neighbourhood", "diagram", [(spec, None)], 1, 176), eqs(graph_questions(rng, spec, 6), "Questions")])
    if day == 4:
        PQ = [("Which place helps us learn?", "school"), ("Which place helps us get well?", "hospital"), ("Which place keeps money safe?", "bank"),
              ("Which place helps put out fires?", "firehall"), ("Which place has books to borrow?", "library"), ("Which place has swings and slides?", "playground"),
              ("Which place sends our mail?", "postoffice"), ("Which place sells food?", "store")]
        a = [PIC(rng, q, p, PLACES + ["playground"]) for q, p in take(PQ, 8, v, "k4d4")]
        return sheet(4, 4, t, "Each place gives our community something we need.", "Example: Which place helps us learn?  " + ARROW + "  school", [pics(a, "Which place?")])
    a = [PIC(rng, q, p, PLACES) for q, p in take(PLACE_Q, 4, v, "k4d5a")]
    items = [(k, "found in nature") for k in take(NATURAL, 3, v, "k4d5b")] + [(k, "made by people") for k in take(BUILT, 3, v, "k4d5c")]
    rng.shuffle(items)
    b = [WORDF(rng, k, ans, ["made by people", "found in nature"], "Nature or built?") for k, ans in items]
    return sheet(4, 5, t, "Review day! Then draw your picture.", "Example: school  " + ARROW + "  made by people",
                 [pics(a, "Where do you go?"), words(b, "Nature or built?"), draw(["Draw your favourite place.", "Draw a place in your town."][v])])


# ============================================================== UNIT 5
NEEDS = ["apple", "bread", "water", "milk", "coat", "bed", "house", "shoe"]
WANTS = ["ball", "teddy", "game", "candy", "tv", "bike", "cookie"]
GOODS = ["bread", "shirt", "ball", "book", "shoe", "apple"]
SERVICES = ["doctor", "teacher", "firefighter", "mail", "cook", "police", "scissors"]
COINC = {"coin_nickel": 5, "coin_dime": 10, "coin_quarter": 25}
LBL["scissors"] = "haircut"


def coins_q(rng, keys, n):
    out = []
    for _ in range(n):
        k = rng.randint(2, 4)
        cs = [rng.choice(keys) for _ in range(k)]
        tot = sum(COINC[c] for c in cs)
        if tot > 95:
            continue
        out.append(((cs, "How much money?  ____"), f"{tot}¢"))
    return out


def dollars_q(rng, n):
    out = []
    for _ in range(n):
        cs = [rng.choice(["coin_loonie", "coin_toonie"]) for _ in range(rng.randint(2, 4))]
        tot = sum(1 if c == "coin_loonie" else 2 for c in cs)
        out.append(((cs, "How much money?  ____"), f"${tot}"))
    return out


def U5(day, rng, v):
    t = "Needs, Wants & Money"
    inst = "Look at the pictures. Pick the best answer."
    if day == 1:
        items = [(k, "need") for k in take(NEEDS, 8, v, "k5d1a")] + [(k, "want") for k in take(WANTS, 7, v, "k5d1b")]
        rng.shuffle(items)
        a = [WORDF(rng, k, ans, ["need", "want"], "Need or want?") for k, ans in items]
        return sheet(5, 1, t, "A need keeps us alive and healthy. A want is nice to have.", "Example: apple  " + ARROW + "  need     candy  " + ARROW + "  want", [words(a, "Need or want?")])
    if day == 2:
        items = [(k, "good") for k in take(GOODS, 6, v, "k5d2a")] + [(k, "service") for k in take(SERVICES, 7, v, "k5d2b")]
        rng.shuffle(items)
        a = [WORDF(rng, k, ans, ["good", "service"], "Good or service?") for k, ans in items]
        return sheet(5, 2, t, "A good is a thing you can buy. A service is work someone does for you.", "Example: bread  " + ARROW + "  good     doctor  " + ARROW + "  service", [words(a, "Good or service?")])
    if day == 3:
        names = {"coin_loonie": "loonie", "coin_toonie": "toonie", "coin_quarter": "quarter", "coin_dime": "dime", "coin_nickel": "nickel"}
        coinkeys = list(names)
        a = [PIC(rng, f"Which is a {names[k]}?", k, coinkeys) for k in take(coinkeys * 2, 4, v, "k5d3a")]
        return sheet(5, 3, t, "Count the coins. A nickel is 5¢, a dime is 10¢, a quarter is 25¢, a loonie is $1, a toonie is $2.",
                     "Example: dime + nickel = 15¢",
                     [pics(a, "Part A – Find the coin"), sec("Part B – Count the cents", "coins", coins_q(rng, list(COINC), 6), 2, 74),
                      sec("Part C – Count the dollars", "coins", dollars_q(rng, 4), 2, 74)])
    if day == 4:
        fixed = [("Which shows saving money?", "jar", ["jar", "cart", "sharing"]), ("Which shows spending money?", "cart", ["jar", "cart", "gift"]),
                 ("Which shows sharing?", "sharing", ["jar", "cart", "sharing"]), ("Which one saves money for later?", "jar", ["jar", "candy", "ball"]),
                 ("Which one is for buying things?", "cart", ["cart", "bed", "tree"]), ("Which one is giving?", "gift", ["gift", "jar", "cart"])]
        a = [PICF(rng, q, c, o) for q, c, o in take(fixed, 6, v, "k5d4a")]
        w = [WORDF(rng, k, ans, ["save", "spend", "share"], "Save, spend or share?") for k, ans in
             take([("jar", "save"), ("cart", "spend"), ("sharing", "share"), ("gift", "share"), ("coin_loonie", "save"), ("store", "spend")], 6, v, "k5d4b")]
        sh = []
        for _ in range(4):
            f = rng.choice([2, 3, 4])
            n = f * rng.randint(2, 4)
            sh.append((("cookie", n, f"Share with {f} friends. Each gets ____"), n // f))
        return sheet(5, 4, t, "Money can be saved, spent or shared. Share things fairly!", "Example: 6 cookies for 3 friends  " + ARROW + "  2 each",
                     [pics(a, "Part A – Save, spend, share"), words(w, "Part B – Which one?"), sec("Part C – Share fairly", "count", sh, 2, 62)])
    items = [(k, "need") for k in take(NEEDS, 3, v, "k5d5a")] + [(k, "want") for k in take(WANTS, 3, v, "k5d5b")]
    rng.shuffle(items)
    a = [WORDF(rng, k, ans, ["need", "want"], "Need or want?") for k, ans in items]
    g = [WORDF(rng, k, "good" if k in GOODS else "service", ["good", "service"], "Good or service?") for k in take(GOODS[:3] + SERVICES[:3], 4, v, "k5d5c")]
    return sheet(5, 5, t, "Review day! Then draw your picture.", "Example: apple  " + ARROW + "  need",
                 [words(a + g, "Needs, wants, goods, services"), sec("Count the cents", "coins", coins_q(rng, list(COINC), 2), 2, 74),
                  draw(["Draw something you need.", "Draw something you want."][v])])


# ============================================================== UNIT 6
LAND = ["mountain", "river", "lake", "ocean", "island", "forest"]


def U6(day, rng, v):
    t = "Maps & Directions"
    inst = "Look at the pictures. Pick the best answer."
    if day == 1:
        a = [WORD(rng, k, LBL[k], lw(LAND), "What is this?") for k in take(LAND * 3, 14, v, "k6d1")]
        return sheet(6, 1, t, "Maps show mountains, rivers, lakes, oceans, islands and forests.", "Example: What is this?  " + ARROW + "  mountain", [words(a, "Land and water")])
    if day == 2:
        spec = make_map(rng)
        return sheet(6, 2, t, "North is up, south is down, east is right, west is left.", "Example: What is east (right) of the school?",
                     [sec("Neighbourhood map", "diagram", [(spec, None)], 1, 176), eqs(map_questions(rng, spec, 7, mode="dir"), "Which direction?")])
    if day == 3:
        spec = make_map(rng)
        return sheet(6, 3, t, "Use the row and column numbers to find places.", "Example: Row 2, column 3 is the box in the middle row, third from the left.",
                     [sec("Neighbourhood map", "diagram", [(spec, None)], 1, 176), eqs(map_questions(rng, spec, 7, mode="all"), "Read the map")])
    if day == 4:
        a = [WORDF(rng, f"arrow_{d}", d, ["up", "down", "left", "right"], "Which way does the arrow point?") for d in take(["up", "down", "left", "right"] * 3, 10, v, "k6d4")]
        return sheet(6, 4, t, "Arrows show directions.", "Example: an arrow pointing up  " + ARROW + "  up", [words(a, "Which way?")])
    spec = make_map(rng)
    a = [WORD(rng, k, LBL[k], lw(LAND), "What is this?") for k in take(LAND, 3, v, "k6d5a")]
    b = [WORDF(rng, f"arrow_{d}", d, ["up", "down", "left", "right"], "Which way?") for d in take(["up", "down", "left", "right"], 3, v, "k6d5b")]
    return sheet(6, 5, t, "Review day! Read the map, then draw your picture.", "Example: What is this?  " + ARROW + "  ocean",
                 [sec("Neighbourhood map", "diagram", [(spec, None)], 1, 176), eqs(map_questions(rng, spec, 3), "Read the map"), words(a + b, "Land, water and arrows")])


# ============================================================== UNIT 7
VEH_Q = [("Which carries many kids to school?", "bus"), ("Which flies in the sky?", "plane"), ("Which crosses the water in BC?", "ferry"),
         ("Which runs on tracks?", "train"), ("Which one do you pedal?", "bike"), ("Which carries heavy loads?", "truck"),
         ("Which one do you paddle?", "canoe"), ("Which is a small family vehicle?", "car"), ("Which helps on a farm?", "tractor")]
WHERE = {"car": "land", "bus": "land", "bike": "land", "truck": "land", "train": "land", "tractor": "land", "ferry": "water", "canoe": "water", "plane": "air"}
OLDNEW = [("horsecart", "car"), ("candle", "lamp"), ("typewriter", "computer"), ("letter", "phone")]
OLD = ["horsecart", "candle", "typewriter"]
NEW = ["car", "lamp", "computer", "phone", "bus", "plane", "tv"]
COMM_Q = [("What do you use to watch a show?", "tv"), ("What do you use to send a note on paper?", "letter"), ("What do you use to call a friend?", "phone"),
          ("What do you use to type and search?", "computer"), ("What gives light in a room?", "lamp")]


def U7(day, rng, v):
    t = "Getting Around & Staying in Touch"
    inst = "Look at the pictures. Pick the best answer."
    if day == 1:
        a = [WORDF(rng, k, WHERE[k], ["land", "water", "air"], "Where does it travel?") for k in take(list(WHERE) * 2, 14, v, "k7d1")]
        return sheet(7, 1, t, "Vehicles travel on land, on water or in the air.", "Example: bus  " + ARROW + "  land", [words(a, "Land, water or air?")])
    if day == 2:
        a = [PIC(rng, q, k, VEH) for q, k in take(VEH_Q, 9, v, "k7d2")]
        return sheet(7, 2, t, inst, "Example: Which flies in the sky?  " + ARROW + "  airplane", [pics(a, "Which vehicle?")])
    if day == 3:
        a = []
        for old, new in take(OLDNEW * 2, 8, v, "k7d3"):
            if rng.random() < .5:
                a.append(PICF(rng, "Which is newer?", new, [old, new]))
            else:
                a.append(PICF(rng, "Which is from long ago?", old, [old, new]))
        w = [WORDF(rng, k, "long ago" if k in OLD else "today", ["long ago", "today"], "Long ago or today?") for k in take(OLD + ["car", "phone", "computer", "lamp"], 8, v, "k7d3b")]
        return sheet(7, 3, t, "Things change over time. Some things are old and some are new.", "Example: Which is newer?  " + ARROW + "  pick the car, not the horse cart",
                     [pics(a, "Part A – Old or new?"), words(w, "Part B – Long ago or today?")])
    if day == 4:
        a = [PIC(rng, q, k, ["tv", "letter", "phone", "computer", "lamp"]) for q, k in take(COMM_Q, 5, v, "k7d4a")]
        sg = [WORD(rng, k, LBL[k], ["stop sign", "traffic light", "crosswalk"], "What is this?") for k in take(["stop", "trafficlight", "crosswalk"] * 3, 6, v, "k7d4b")]
        return sheet(7, 4, t, "We talk to each other in many ways. Signs help us travel safely.", "Example: What do you use to call a friend?  " + ARROW + "  phone",
                     [pics(a, "Part A – Staying in touch"), words(sg, "Part B – Road signs")])
    a = [WORDF(rng, k, WHERE[k], ["land", "water", "air"], "Where does it travel?") for k in take(list(WHERE), 4, v, "k7d5a")]
    b = [PIC(rng, q, k, VEH) for q, k in take(VEH_Q, 3, v, "k7d5b")]
    c_ = []
    for old, new in take(OLDNEW, 2, v, "k7d5c"):
        c_.append(PICF(rng, "Which is newer?", new, [old, new]))
    return sheet(7, 5, t, "Review day! Then draw your picture.", "Example: ferry  " + ARROW + "  water",
                 [words(a, "Land, water or air?"), pics(b + c_, "Vehicles and old/new"), draw(["Draw how you get to school.", "Draw a vehicle you like."][v])])


# ============================================================== UNIT 8
SIGN_Q = [("Which tells cars to stop?", "stop"), ("Which has red, yellow and green lights?", "trafficlight"), ("Where do you cross the street?", "crosswalk")]
GEAR_Q = [("What do you wear to ride a bike?", "helmet"), ("What do you wear in a boat?", "lifejacket"), ("What keeps you dry in the rain?", "umbrella"),
          ("What do you wear when it is cold?", "coat"), ("What protects your head?", "helmet"), ("What do you wear on your feet?", "shoe")]
GEAR_POOL = ["helmet", "lifejacket", "umbrella", "coat", "shoe", "shirt"]
SAY = [("Which says thank you?", "say_thanks"), ("Which is a kind way to ask?", "say_please"), ("Which says sorry?", "say_sorry"),
       ("Which is a kind way to say hi?", "say_hello")]
SAYP = ["say_thanks", "say_please", "say_sorry", "say_go", "say_give", "say_hello"]


def U8(day, rng, v):
    t = "Rules, Safety & Being Kind"
    inst = "Look at the pictures. Pick the best answer."
    if day == 1:
        sp = ["stop", "trafficlight", "crosswalk", "helmet", "umbrella", "lifejacket"]
        a = [PIC(rng, q, k, sp) for q, k in take(SIGN_Q * 3, 6, v, "k8d1a")]
        b = [WORD(rng, k, LBL[k], ["stop sign", "traffic light", "crosswalk"], "What is this?") for k in take(["stop", "trafficlight", "crosswalk"] * 3, 6, v, "k8d1b")]
        return sheet(8, 1, t, "Rules and signs keep us safe.", "Example: Which tells cars to stop?  " + ARROW + "  stop sign", [pics(a, "Part A – Which one?"), words(b, "Part B – Name the sign")])
    if day == 2:
        a = [PIC(rng, q, k, GEAR_POOL) for q, k in take(GEAR_Q * 2, 8, v, "k8d2")]
        return sheet(8, 2, t, "Wear the right gear to stay safe.", "Example: What do you wear to ride a bike?  " + ARROW + "  helmet", [pics(a, "Safety gear")])
    if day == 3:
        a = [PIC(rng, q, k, SAYP) for q, k in take(SAY * 2, 6, v, "k8d3a")]
        bn = [("Where does a plastic bottle go?", "bin_recycle"), ("Where does a candy wrapper go?", "bin_trash"), ("Where does a paper go?", "bin_recycle"), ("Where does a broken toy go?", "bin_trash")]
        b = [PICF(rng, q, c, ["bin_recycle", "bin_trash"]) for q, c in take(bn, 4, v, "k8d3b")]
        return sheet(8, 3, t, "Kind words and caring for the Earth make our community better.", "Example: Which says thank you?  " + ARROW + "  “Thank you!”",
                     [pics(a, "Part A – Kind words"), pics(b, "Part B – Which bin?")])
    if day == 4:
        fixed = [("Which shows sharing?", "sharing", ["sharing", "ball", "game"]), ("Which shows a kind gift?", "gift", ["gift", "game", "candy"]), ("Which shows a family together?", "family", ["family", "house", "car"])]
        a = [PICF(rng, q, c, o) for q, c, o in take(fixed * 2, 6, v, "k8d4a")]
        sh = []
        for _ in range(6):
            f = rng.choice([2, 3, 4])
            n = f * rng.randint(2, 4)
            k = rng.choice(["cookie", "apple", "ball"])
            sh.append(((k, n, f"Share with {f} friends. Each gets ____"), n // f))
        return sheet(8, 4, t, "Being fair means sharing so everyone gets the same.", "Example: 6 apples for 3 friends  " + ARROW + "  2 each",
                     [pics(a, "Part A – Sharing and caring"), sec("Part B – Share fairly", "count", sh, 2, 62)])
    a = [PIC(rng, q, k, GEAR_POOL) for q, k in take(GEAR_Q, 3, v, "k8d5a")]
    b = [PIC(rng, q, k, SAYP) for q, k in take(SAY, 2, v, "k8d5b")]
    c_ = [PIC(rng, q, k, ["stop", "trafficlight", "crosswalk", "helmet"]) for q, k in take(SIGN_Q, 2, v, "k8d5c")]
    return sheet(8, 5, t, "Review day! Then draw your picture.", "Example: Which says thank you?  " + ARROW + "  “Thank you!”",
                 [pics(a + b + c_, "Safety and kindness"), draw(["Draw a time you were kind.", "Draw a safety rule."][v])])


# ============================================================== UNIT 9
CEL_Q = [("Which is for a birthday?", "cake"), ("Which lights up the night sky?", "fireworks"), ("Which is a present to give?", "gift"),
         ("Which is a fall harvest?", "pumpkin"), ("Which is a red lantern?", "lantern"), ("Which floats at a party?", "balloon")]
CEL_POOL = ["cake", "fireworks", "gift", "pumpkin", "lantern", "balloon"]
FP_Q = [("Which did people paddle on the water?", "canoe"), ("Which fish swims up BC rivers?", "salmon"), ("Which tall tree grows in BC forests?", "cedar"),
        ("Where do salmon swim?", "river"), ("Which is a big body of salt water?", "ocean"), ("Which has snow on top?", "mountain"), ("Which place has many trees?", "forest")]
FP_POOL = ["canoe", "salmon", "cedar", "river", "ocean", "mountain", "forest"]
NEED_ALL = [("Which do all people need to drink?", "water"), ("Which do all people need to eat?", "apple"), ("Where do people sleep?", "bed"),
            ("Which keeps people warm?", "coat"), ("Where do people live?", "house"), ("Who do we love and care for?", "family")]
SHIRTS = ["red", "blue", "green", "orange", "purple", "pink"]


def people_q(rng, n):
    out = []
    for _ in range(n):
        specs = []
        for _ in range(5):
            specs.append({"shirt": rng.choice(["red", "blue", "green", "orange"]), "skin": rng.choice(["skin", "skin2", "skin3"]),
                          "hat": rng.choice([None, None, "cap", "straw", "hard"])})
        if rng.random() < .5:
            col = rng.choice(["red", "blue", "green", "orange"])
            ans = sum(1 for s in specs if s["shirt"] == col)
            out.append(((specs, f"How many people wear a {col} shirt?  ____"), ans))
        else:
            ans = sum(1 for s in specs if s["hat"])
            out.append(((specs, "How many people wear a hat?  ____"), ans))
    return out


def U9(day, rng, v):
    t = "Canada, Celebrations & Our World"
    inst = "Look at the pictures. Pick the best answer."
    if day == 1:
        a = [PICF(rng, "Which is the Canadian flag?", "flag_canada", ["flag_canada", "flag_blue", "flag_green"]),
             PICF(rng, "Which is a maple leaf?", "maple", ["maple", "flower", "tree"]),
             PICF(rng, "Which flower is a symbol of BC?", "dogwood", ["dogwood", "flower", "sun"]),
             PICF(rng, "Which tree is a symbol of BC?", "cedar", ["cedar", "tree", "flower"]),
             PICF(rng, "Which flag is from Canada?", "flag_canada", ["flag_green", "flag_canada", "flag_blue"]),
             PICF(rng, "Which is the red maple leaf?", "maple", ["maple", "cedar", "apple"])]
        b = [WORDF(rng, k, LBL[k], [LBL[k], "apple", "ball"], "What is this?") for k in ["flag_canada", "maple", "dogwood", "cedar"]]
        rng.shuffle(a)
        return sheet(9, 1, t, "Canada and BC have special symbols.", "Example: Which is the Canadian flag?  " + ARROW + "  red and white with a maple leaf",
                     [pics(a[:6], "Part A – Symbols"), words(b, "Part B – Name it")])
    if day == 2:
        a = [PIC(rng, q, k, CEL_POOL) for q, k in take(CEL_Q * 2, 8, v, "k9d2a")]
        b = [WORDF(rng, k, ans, ["birthday", "fireworks night", "harvest"], "Which celebration?") for k, ans in
             take([("cake", "birthday"), ("fireworks", "fireworks night"), ("pumpkin", "harvest"), ("balloon", "birthday"), ("gift", "birthday"), ("lantern", "fireworks night")], 4, v, "k9d2b")]
        return sheet(9, 2, t, "People celebrate in many ways.", "Example: Which is for a birthday?  " + ARROW + "  cake", [pics(a, "Part A – Celebrations")])
    if day == 3:
        a = [PIC(rng, q, k, ["water", "apple", "bed", "coat", "house", "family", "game", "candy"]) for q, k in take(NEED_ALL, 6, v, "k9d3a")]
        return sheet(9, 3, t, "We are all different and the same. Count the people. Everyone has needs.", "Example: Count the people with a hat.",
                     [sec("Part A – Count the people", "people", people_q(rng, 4), 1, 92), pics(a, "Part B – What do all people need?")])
    if day == 4:
        a = [PIC(rng, q, k, FP_POOL) for q, k in take(FP_Q, 7, v, "k9d4a")]
        b = [WORD(rng, k, LBL[k], lw(FP_POOL), "What is this?") for k in take(FP_POOL, 6, v, "k9d4b")]
        return sheet(9, 4, t, "Many First Peoples of BC have lived with the land and water for a very long time.", "Example: Which did people paddle?  " + ARROW + "  canoe",
                     [pics(a, "Part A – Land and water"), words(b, "Part B – Name it")])
    a = [PIC(rng, q, k, CEL_POOL) for q, k in take(CEL_Q, 3, v, "k9d5a")]
    b = [PIC(rng, q, k, FP_POOL) for q, k in take(FP_Q, 3, v, "k9d5b")]
    c_ = [PICF(rng, "Which is the Canadian flag?", "flag_canada", ["flag_canada", "flag_blue", "flag_green"])]
    return sheet(9, 5, t, "Review day! Then draw your picture.", "Example: Which is the Canadian flag?  " + ARROW + "  red and white flag",
                 [pics(a + b + c_, "Canada and celebrations"), draw(["Draw how your family celebrates.", "Draw your favourite celebration."][v])])


# ============================================================== UNIT 10
STAGE = ["baby", "girl", "mom", "grandma"]
SEASON = {"flower": "spring", "sun": "summer", "leaf_fall": "fall", "snowflake": "winter"}
SEAS_Q = [("Which season is cold and snowy?", "snowflake"), ("Which season is hot and sunny?", "sun"), ("Which shows spring?", "flower"), ("Which shows fall?", "leaf_fall"),
          ("Which shows winter?", "snowflake"), ("Which shows summer?", "sun"), ("When do leaves change color?", "leaf_fall"), ("When do flowers bloom?", "flower")]
GROUPS = {"vehicles": ["car", "bus", "bike", "train", "plane", "truck"], "places": ["school", "hospital", "store", "library", "bank", "park"],
          "helpers": ["doctor", "teacher", "farmer", "cook", "police", "builder"], "food": ["apple", "bread", "milk", "cookie", "water"]}


def odd_item(rng):
    g1, g2 = rng.sample(list(GROUPS), 2)
    three = rng.sample(GROUPS[g1], 3)
    odd = rng.choice(GROUPS[g2])
    opts = three + [odd]
    rng.shuffle(opts)
    return ("Which one does not belong?", opts), "ABCD"[opts.index(odd)]


def pattern_item(rng, pool):
    a, b, c = rng.sample(pool, 3)
    kind = rng.choice(["ab", "aab", "abc"])
    seqs = {"ab": ([a, b, a, b, a], b), "aab": ([a, a, b, a, a], b), "abc": ([a, b, c, a, b], c)}
    shown, ans = seqs[kind]
    opts = list({a, b, c} if kind == "abc" else {a, b, c})
    rng.shuffle(opts)
    return ("What comes next?", shown, opts), "ABCD"[opts.index(ans)]


def U10(day, rng, v):
    t = "Past, Present & Time"
    inst = "Look at the pictures. Pick the best answer."
    if day == 1:
        fixed = [("Who is the oldest?", "grandma", ["baby", "grandma", "mom"]), ("Who is the youngest?", "baby", ["girl", "baby", "grandma"]),
                 ("Who grows up to be a grown-up?", "girl", ["girl", "grandma", "mom"]), ("Who has lived the longest?", "grandma", ["mom", "girl", "grandma"])]
        a = [PICF(rng, q, c, o) for q, c, o in fixed]
        w = [WORDF(rng, k, ans, ["baby", "child", "grown-up", "grandparent"], "Which age?") for k, ans in take([("baby", "baby"), ("girl", "child"), ("mom", "grown-up"), ("grandma", "grandparent"), ("boy", "child"), ("dad", "grown-up")], 6, v, "k10d1")]
        pt = []
        for _ in range(4):
            sh = ["baby", "girl", "mom"]
            pt.append((("What comes next as a person grows?", sh, ["grandma", "baby", "girl"]), None))
        pt = [PICF(rng, "Who comes next as a person grows?", "mom", ["mom", "baby", "girl"])] + []
        return sheet(10, 1, t, "People grow and change over time.", "Example: baby, child, grown-up, grandparent", [pics(a, "Part A – Young and old"), words(w, "Part B – Which age?")])
    if day == 2:
        spec = make_calendar(rng)
        return sheet(10, 2, t, "A calendar shows the days of the month. A week has 7 days.", "Example: Count the days across one row.",
                     [sec("Calendar", "diagram", [(spec, None)], 1, 152), eqs(calendar_questions(rng, spec, 5), "Read the calendar"),
                      sec("Clocks", "clock", [((h, 0), f"{h}:00") for h in take(list(range(1, 13)), 3, v, "k10d2")], 3, 104)])
    if day == 3:
        a = []
        for _ in range(4):
            a.append(PIC(rng, "Which is from long ago?", rng.choice(OLD), NEW))
        for _ in range(4):
            new = rng.choice(["car", "lamp", "computer", "phone"])
            a.append(PIC(rng, "Which is new?", new, OLD + ["canoe"]) if False else PICF(rng, "Which is new?", new, [new] + rng.sample(OLD, 2)))
        return sheet(10, 3, t, "Long ago, people used different things than we do today.", "Example: Which is from long ago?  " + ARROW + "  horse cart", [pics(a, "Old or new?")])
    if day == 4:
        a = [PIC(rng, q, k, list(SEASON)) for q, k in take(SEAS_Q, 8, v, "k10d4a")]
        w = [WORDF(rng, k, s, ["spring", "summer", "fall", "winter"], "Which season?") for k, s in take(list(SEASON.items()) * 2, 6, v, "k10d4b")]
        return sheet(10, 4, t, "There are four seasons. They come in the same order every year.", "Example: Which season is cold and snowy?  " + ARROW + "  winter",
                     [pics(a, "Part A – Seasons"), words(w, "Part B – Which season?")])
    odd = [odd_item(rng) for _ in range(4)]
    pat = [pattern_item(rng, ["apple", "ball", "star" if False else "sun", "car", "house", "tree", "bread", "book"]) for _ in range(4)]
    return sheet(10, 5, t, "Challenge day! Find the odd one out. Finish the patterns. Then draw!", "Example: car, bus, train, apple  " + ARROW + "  apple does not belong",
                 [pics(odd, "Part A – Odd one out"), sec("Part B – What comes next?", "picp", pat, 2, 126),
                  draw(["Draw yourself as a baby and now.", "Draw yourself as a grown-up."][v])])


# ------------------------------------------------------------------ calendar
WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def make_calendar(rng):
    return {"type": "calendar", "start": rng.randint(0, 6), "days": 30, "month": rng.choice(["April", "June", "September", "November"])}


def calendar_questions(rng, spec, n):
    st, nd = spec["start"], spec["days"]
    wd = lambda d: WEEKDAYS[(st + d - 1) % 7]
    qs = []
    d = rng.randint(3, 27)
    qs.append((f"What day of the week is the {d}th?  ____", wd(d)))
    d2 = rng.randint(2, 28)
    qs.append((f"What day of the week is the {d2}th?  ____", wd(d2)))
    day = rng.choice(WEEKDAYS)
    qs.append((f"How many {day}s are in this month?  ____", sum(1 for x in range(1, nd + 1) if wd(x) == day)))
    qs.append(("How many days are in a week?  ____", 7))
    first = wd(1)
    qs.append(("What day of the week is the 1st?  ____", first))
    qs.append((f"How many days are in this month?  ____", nd))
    rng.shuffle(qs)
    return [(q, str(a)) for q, a in qs[:n]]


UNITS = {1: U1, 2: U2, 3: U3, 4: U4, 5: U5, 6: U6, 7: U7, 8: U8, 9: U9, 10: U10}


def unit_sheets(u, variant=0):
    return [fit(UNITS[u](d, random.Random(u * 100 + d + variant * 1000), variant)) for d in range(1, 6)]


def checkup_a():
    rng = random.Random(3555)
    s = [pics([PIC(rng, "Which face is happy?", "happy", FEELS), PIC(rng, "Who is the baby?", "baby", FAM), PICF(rng, "What do you sleep in?", "bed", ["bed", "shirt", "ball"]),
               PIC(rng, "Which home floats?", "houseboat", HOMES)], "My family and home"),
         words([WORD(rng, "school", "school", lw(PLACES), "What place is this?"), WORD(rng, "doctor", "doctor", lw(HELP), "Who is this helper?"),
                WORD(rng, "teacher", "teacher", lw(HELP), "Who is this helper?"), WORD(rng, "library", "library", lw(PLACES), "What place is this?")], "Places and helpers"),
         pics([PIC(rng, "Which tool does a firefighter use?", "hose", TOOLPOOL), PIC(rng, "Where do you borrow books?", "library", PLACES),
               PIC(rng, "Which place helps us get well?", "hospital", PLACES), PIC(rng, "Where do you buy food?", "store", PLACES)], "Helpers and places"),
         words([WORDF(rng, "apple", "need", ["need", "want"], "Need or want?"), WORDF(rng, "candy", "want", ["need", "want"], "Need or want?"),
                WORDF(rng, "doctor", "service", ["good", "service"], "Good or service?"), WORDF(rng, "bread", "good", ["good", "service"], "Good or service?")], "Needs, wants, goods, services"),
         sec("Money", "coins", [((["coin_dime", "coin_nickel"], "How much money?  ____"), "15¢"), ((["coin_quarter", "coin_dime"], "How much money?  ____"), "35¢")], 2, 74)]
    return sheet(0, "A", "Check-Up: Units 1–5", "Show what you know! Do your best on every question.", "Aim for 90% or more before moving on to Unit 6.", s)


def final_test():
    rng = random.Random(3999)
    spec = {"type": "map", "rows": 3, "cols": 4, "cells": {(0, 0): "school", (0, 2): "park", (1, 1): "library", (1, 3): "store", (2, 0): "hospital", (2, 2): "bank"}, "deco": {(0, 3): "tree", (2, 3): "tree"}}
    s = [sec("Read the map", "diagram", [(spec, None)], 1, 176),
         eqs([("What is in row 1, column 1?  (school / bank / store)", "school"), ("What is east (right) of the library?  (park / store / bank)", "store"),
              ("How many buildings are on the map?  ____", "6")], ""),
         words([WORDF(rng, "bus", "land", ["land", "water", "air"], "Where does it travel?"), WORDF(rng, "ferry", "water", ["land", "water", "air"], "Where does it travel?"),
                WORDF(rng, "plane", "air", ["land", "water", "air"], "Where does it travel?"), WORDF(rng, "horsecart", "long ago", ["long ago", "today"], "Long ago or today?")], "Getting around"),
         pics([PICF(rng, "What do you wear to ride a bike?", "helmet", ["helmet", "umbrella", "shoe"]), PICF(rng, "Which says thank you?", "say_thanks", ["say_thanks", "say_go", "say_give"]),
               PICF(rng, "Which is the Canadian flag?", "flag_canada", ["flag_canada", "flag_blue", "flag_green"]), PICF(rng, "Which is for a birthday?", "cake", ["cake", "pumpkin", "hose"])], "Safety, kindness and Canada"),
         pics([PICF(rng, "Which season is cold and snowy?", "snowflake", ["snowflake", "sun", "flower"]), PICF(rng, "Who is the oldest?", "grandma", ["baby", "grandma", "mom"])], "Seasons and time"),
         sec("Clocks", "clock", [((4, 0), "4:00"), ((9, 0), "9:00"), ((12, 0), "12:00")], 3, 104)]
    return sheet(0, "F", "Final Test: Units 1–10", "You made it! Show everything you have learned.", "Aim for 90% or more. Then it's certificate time!", s)
