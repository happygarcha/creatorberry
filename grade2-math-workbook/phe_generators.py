"""Picture-based generators for the Grade 2 Physical & Health Education workbook."""
import random
import pheicons  # noqa: F401  (adds poses/food/hygiene icons)
from english_generators import take, fit, ARROW
from generators import sec, sheet
from sticons import LBL
from social_generators import (PIC, PICF, WORD, WORDF, lw, pics, words, eqs, draw, make_graph, pattern_item)

inst = "Look at the pictures. Pick the best answer."

TRAVEL = ["run", "jump", "hop", "walk"]
STAY = ["balance", "stretch", "bend"]
BALLSK = ["throw", "catch", "kick", "bounce"]
POSE14 = TRAVEL + STAY + BALLSK + ["swim", "dance", "skiprope"]
KIND = {**{k: "travel" for k in TRAVEL}, **{k: "stay in place" for k in STAY}, **{k: "ball skill" for k in BALLSK}}
ACTIVE = ["run", "jump", "hop", "swim", "dance", "skiprope", "kick", "walk", "bike", "canoe", "playground", "throw"]
NOTACT = ["sit_tv", "sleep", "game", "tv", "sofa"]
BODYP = ["eye", "ear", "nose", "hand", "foot", "heart", "lungs"]
BODY_USE = [("What do you use to see?", "eye"), ("What do you use to hear?", "ear"), ("What do you use to smell?", "nose"),
            ("What do you use to throw?", "hand"), ("What do you use to kick?", "foot"), ("What pumps your blood?", "heart"),
            ("What do you use to breathe?", "lungs")]
EVERY = ["apple", "banana", "orange", "carrot", "broccoli", "bread", "rice", "egg", "salmon", "beans", "water", "milk"]
SOMETIMES = ["candy", "cookie", "chips", "donut", "juice", "cake"]
VEGFRUIT = ["apple", "banana", "orange", "carrot", "broccoli"]
GRAINS = ["bread", "rice"]
PROTEIN = ["egg", "salmon", "beans"]
FOODALL = VEGFRUIT + GRAINS + PROTEIN + ["milk", "water", "candy", "cookie", "chips", "donut", "juice"]


def _blank_draw(prompts, v):
    return draw(prompts[v])


# ============================================================== UNIT 1
BODYQ = [("Which letter shows the head?", "A"), ("Which letter shows the arm?", "B"), ("Which letter shows the leg?", "C"), ("Which letter shows the foot?", "D"),
         ("Which letter do you use to think?", "A"), ("Which letter do you use to throw?", "B"), ("Which letter do you use to run?", "C"), ("Which letter do you stand on?", "D")]
USEQ = [("Which one uses your arms most?", "throw", ["throw", "kick", "sit_tv"]), ("Which one uses your legs most?", "run", ["run", "catch", "sleep"]),
        ("Which needs your eyes and hands?", "catch", ["catch", "sleep", "sit_tv"]), ("Which one needs good balance?", "balance", ["balance", "sit_tv", "sleep"]),
        ("Which one moves your whole body?", "swim", ["swim", "sit_tv", "sleep"]), ("Which one stretches your muscles?", "stretch", ["stretch", "sit_tv", "sleep"]),
        ("Which one uses your feet with a ball?", "kick", ["kick", "throw", "catch"]), ("Which one uses your hands with a ball?", "bounce", ["bounce", "kick", "run"])]


def U1(day, rng, v):
    t = "My Body & How It Moves"
    if day == 1:
        a = [PIC(rng, q, k, BODYP) for q, k in take(BODY_USE * 2, 8, v, "p1d1a")]
        b = [WORD(rng, k, LBL[k], lw(BODYP), "What body part is this?") for k in take(BODYP * 2, 8, v, "p1d1b")]
        return sheet(1, 1, t, inst, "Example: What do you use to see?  " + ARROW + "  eye", [pics(a, "Part A – What do we use?"), words(b, "Part B – Name the part")])
    if day == 2:
        a = [(f"{q}  ____", ans) for q, ans in take(BODYQ, 8, v, "p1d2")]
        return sheet(1, 2, t, "Look at the body. Write the letter.", "Example: Which letter shows the head?  " + ARROW + "  A",
                     [sec("Look at the body", "diagram", [({"type": "body"}, None)], 1, 176), eqs(a, "Which letter?")])
    if day == 3:
        a = [WORD(rng, k, LBL[k], lw(POSE14), "What is this person doing?") for k in take(POSE14 * 2, 14, v, "p1d3")]
        return sheet(1, 3, t, "Name how people move.", "Example: What is this person doing?  " + ARROW + "  running", [words(a, "Name the move")])
    if day == 4:
        a = [PICF(rng, q, c, o) for q, c, o in take(USEQ, 8, v, "p1d4")]
        return sheet(1, 4, t, inst, "Example: Which one uses your arms most?  " + ARROW + "  throwing", [pics(a, "Which body part works hard?")])
    a = [PIC(rng, q, k, BODYP) for q, k in take(BODY_USE, 3, v, "p1d5a")]
    b = [WORD(rng, k, LBL[k], lw(POSE14), "What is this person doing?") for k in take(POSE14, 4, v, "p1d5b")]
    c_ = [PICF(rng, q, c, o) for q, c, o in take(USEQ, 3, v, "p1d5c")]
    return sheet(1, 5, t, "Review day! Then draw your picture.", "Example: What do you use to hear?  " + ARROW + "  ear",
                 [pics(a + c_, "Body and movement"), words(b, "Name the move"), _blank_draw(["Draw your favourite way to move.", "Draw your body and how it moves."], v)])


# ============================================================== UNIT 2
GEAR = [("What do you use to skip?", "rope"), ("What do you use to ride?", "bike"), ("What do you throw and kick?", "ball"), ("What protects your head on a bike?", "helmet"),
        ("What do you wear to glide on ice?", "skates"), ("What do you slide on in snow?", "sled"), ("What flies in the wind?", "kite"), ("What do you wear to go down a snowy hill?", "ski")]
GEARP = ["rope", "bike", "ball", "helmet", "skates", "sled", "kite", "ski"]


def U2(day, rng, v):
    t = "Moving Skills"
    if day == 1:
        a = [WORDF(rng, k, KIND[k], ["travel", "stay in place", "ball skill"], "Which kind of move?") for k in take(list(KIND) * 2, 14, v, "p2d1")]
        return sheet(2, 1, t, "Some moves travel. Some stay in one place. Some use a ball.", "Example: running  " + ARROW + "  travel     catching  " + ARROW + "  ball skill", [words(a, "Which kind of move?")])
    if day == 2:
        a = [PIC(rng, f"Which one is {LBL[k]}?", k, POSE14) for k in take(POSE14 * 2, 10, v, "p2d2")]
        return sheet(2, 2, t, inst, "Example: Which one is jumping?  " + ARROW + "  pick the jumper", [pics(a, "Find the move")])
    if day == 3:
        a = [PIC(rng, q, k, GEARP) for q, k in take(GEAR, 8, v, "p2d3a")]
        b = [WORD(rng, k, LBL[k], lw(GEARP), "What is this?") for k in take(GEARP, 6, v, "p2d3b")]
        return sheet(2, 3, t, inst, "Example: What do you use to skip?  " + ARROW + "  skipping rope", [pics(a, "Part A – What do we use?"), words(b, "Part B – Name it")])
    if day == 4:
        a = [pattern_item(rng, TRAVEL + STAY + ["swim", "dance"]) for _ in range(6)]
        return sheet(2, 4, t, "Look at the pattern. What move comes next?", "Example: run, jump, run, jump, ?  " + ARROW + "  run", [sec("What comes next?", "picp", a, 2, 126)])
    a = [WORDF(rng, k, KIND[k], ["travel", "stay in place", "ball skill"], "Which kind of move?") for k in take(list(KIND), 4, v, "p2d5a")]
    b = [PIC(rng, f"Which one is {LBL[k]}?", k, POSE14) for k in take(POSE14, 3, v, "p2d5b")]
    c_ = [PIC(rng, q, k, GEARP) for q, k in take(GEAR, 3, v, "p2d5c")]
    return sheet(2, 5, t, "Review day! Then draw your picture.", "Example: catching  " + ARROW + "  ball skill",
                 [words(a, "Which kind of move?"), pics(b + c_, "Moves and gear"), _blank_draw(["Draw yourself doing a ball skill.", "Draw yourself jumping or running."], v)])


# ============================================================== UNIT 3
PLACEQ = [("Where can you ride a bike?", "park"), ("Where can you slide and swing?", "playground"), ("Where can you swim?", "lake"), ("Where can you hike?", "mountain"),
          ("Where can you paddle a canoe?", "river"), ("Where can you kick a ball with friends?", "park"), ("Where can you play in the trees?", "forest"), ("Where can you swim in salt water?", "ocean")]
PLACEP = ["park", "playground", "lake", "mountain", "river", "forest", "ocean", "island"]


def U3(day, rng, v):
    t = "Active Play Every Day"
    if day == 1:
        items = [(k, "active") for k in take(ACTIVE, 8, v, "p3d1a")] + [(k, "not active") for k in take(NOTACT * 2, 6, v, "p3d1b")]
        rng.shuffle(items)
        a = [WORDF(rng, k, ans, ["active", "not active"], "Active or not?") for k, ans in items]
        return sheet(3, 1, t, "Active play makes your body strong. Aim for 60 minutes a day!", "Example: running  " + ARROW + "  active     watching TV  " + ARROW + "  not active", [words(a, "Active or not?")])
    if day == 2:
        a = []
        for _ in range(10):
            ac, na = rng.choice(ACTIVE), rng.choice(NOTACT)
            a.append(PICF(rng, "Which is more active?", ac, [ac, na]))
        return sheet(3, 2, t, inst, "Example: Which is more active?  " + ARROW + "  running, not watching TV", [pics(a, "Which is more active?")])
    if day == 3:
        a = []
        for k in take(["run", "swim", "dance", "skiprope", "bike", "jump"] * 2, 6, v, "p3d3a"):
            n = rng.randint(2, 8)
            a.append(((k, n, "Each = 10 minutes. How many minutes?  ____"), n * 10))
        b = []
        for k in take(["run", "swim", "dance", "skiprope", "bike", "jump"] * 2, 4, v, "p3d3b"):
            n = rng.randint(3, 8)
            b.append(((k, n, "Each = 10 minutes. 60 minutes or more?  ____"), "yes" if n >= 6 else "no"))
        return sheet(3, 3, t, "Count the active play. Each picture is 10 minutes.", "Example: 3 pictures = 30 minutes",
                     [sec("Part A – How many minutes?", "count", a, 2, 62), sec("Part B – Is it enough?", "count", b, 2, 62)])
    if day == 4:
        a = [PIC(rng, q, k, PLACEP) for q, k in take(PLACEQ, 8, v, "p3d4")]
        return sheet(3, 4, t, inst, "Example: Where can you swim?  " + ARROW + "  lake", [pics(a, "Where can you play?")])
    items = [(k, "active") for k in take(ACTIVE, 3, v, "p3d5a")] + [(k, "not active") for k in take(NOTACT, 3, v, "p3d5b")]
    rng.shuffle(items)
    a = [WORDF(rng, k, ans, ["active", "not active"], "Active or not?") for k, ans in items]
    b = [PIC(rng, q, k, PLACEP) for q, k in take(PLACEQ, 3, v, "p3d5c")]
    return sheet(3, 5, t, "Review day! Then draw your picture.", "Example: swimming  " + ARROW + "  active",
                 [words(a, "Active or not?"), pics(b, "Where can you play?"), _blank_draw(["Draw your favourite active game.", "Draw a place where you love to play."], v)])


# ============================================================== UNIT 4
REST = [("What helps your body rest?", "bed", ["bed", "run", "ball"]), ("What do you drink when you are thirsty?", "water", ["water", "chips", "candy"]),
        ("When do we sleep?", "moon", ["moon", "sun", "run"]), ("When are you awake and playing?", "sun", ["sun", "moon", "bed"]),
        ("What helps your heart slow down?", "sleep", ["sleep", "run", "jump"]), ("Which one helps you cool down after play?", "walk", ["walk", "jump", "skiprope"])]


def U4(day, rng, v):
    t = "Heart, Breathing & Resting"
    if day == 1:
        q2 = [("Which pumps blood?", "heart"), ("Which helps you breathe?", "lungs"), ("Which one beats?", "heart"), ("Which one fills with air?", "lungs")]
        a = [PIC(rng, q, k, ["heart", "lungs", "hand", "foot", "ear", "eye"]) for q, k in take(q2 * 2, 6, v, "p4d1a")]
        b = [((("heart", rng.randint(3, 9), "Count the beats.  ____")), None) for _ in range(4)]
        b = [(d, d[1]) for d, _ in b]
        return sheet(4, 1, t, "Your heart pumps blood. Your lungs bring in air.", "Example: Which pumps blood?  " + ARROW + "  heart",
                     [pics(a, "Part A – Heart and lungs"), sec("Part B – Count the heartbeats", "count", b, 2, 62)])
    if day == 2:
        fast, slow = ["run", "swim", "skiprope", "jump", "dance"], ["sit_tv", "sleep", "walk", "stretch"]
        a = []
        for i in range(6):
            q = "Which makes your heart beat fastest?" if i % 2 == 0 else "Which makes you breathe harder?"
            a.append(PICF(rng, q, rng.choice(fast), [rng.choice(fast)] + rng.sample(slow, 2)) if False else None)
        a = []
        for i in range(6):
            q = "Which makes your heart beat fastest?" if i % 2 == 0 else "Which makes you breathe harder?"
            good = rng.choice(fast)
            a.append(PICF(rng, q, good, [good] + rng.sample(slow, 2)))
        b = [PICF(rng, "Which means “too hard, slow down”?", "breath_hard", ["breath_easy", "breath_talk", "breath_hard"]),
             PICF(rng, "Which means “easy”?", "breath_easy", ["breath_easy", "breath_talk", "breath_hard"]),
             PICF(rng, "Which means “just right”?", "breath_talk", ["breath_easy", "breath_talk", "breath_hard"]),
             PICF(rng, "Which means you are working very hard?", "breath_hard", ["breath_easy", "breath_talk", "breath_hard"])]
        return sheet(4, 2, t, "Hard play makes your heart beat fast and your breathing hard. Listen to your body!", "Example: Which makes your heart beat fastest?  " + ARROW + "  running",
                     [pics(a, "Part A – Fast heart"), pics(b, "Part B – The talk test")])
    if day == 3:
        a = [PICF(rng, q, c, o) for q, c, o in take(REST * 2, 8, v, "p4d3")]
        return sheet(4, 3, t, "Rest, sleep and water help your body.", "Example: What helps your body rest?  " + ARROW + "  bed", [pics(a, "Rest and recovery")])
    if day == 4:
        fast = ["run", "swim", "skiprope", "jump", "dance"]
        slow = ["sit_tv", "sleep"]
        items = [(k, "faster") for k in take(fast, 5, v, "p4d4a")] + [(k, "slower") for k in slow * 2]
        rng.shuffle(items)
        a = [WORDF(rng, k, ans, ["faster", "slower"], "Does your heart beat faster or slower?") for k, ans in items[:9]]
        return sheet(4, 4, t, "Active play makes your heart beat faster. Rest makes it slower.", "Example: running  " + ARROW + "  faster", [words(a, "Faster or slower?")])
    a = [PICF(rng, q, c, o) for q, c, o in take(REST, 3, v, "p4d5a")]
    b = [PIC(rng, q, k, ["heart", "lungs", "hand", "foot"]) for q, k in take([("Which pumps blood?", "heart"), ("Which helps you breathe?", "lungs")], 2, v, "p4d5b")]
    c_ = [WORDF(rng, k, "faster", ["faster", "slower"], "Heart beat?") for k in take(["run", "swim", "jump"], 2, v, "p4d5c")] + [WORDF(rng, "sleep", "slower", ["faster", "slower"], "Heart beat?")]
    return sheet(4, 5, t, "Review day! Then draw your picture.", "Example: running  " + ARROW + "  heart beats faster",
                 [pics(a + b, "Heart, lungs and rest"), words(c_, "Faster or slower?"), _blank_draw(["Draw what you do to rest.", "Draw how you feel after running."], v)])


# ============================================================== UNIT 5
def group_q(rng, n, v, key):
    out = []
    spec = [("Which one is a fruit or vegetable?", VEGFRUIT), ("Which one is a grain food?", GRAINS), ("Which one is a protein food?", PROTEIN)]
    for i, _ in enumerate(range(n)):
        q, grp = spec[i % 3]
        good = rng.choice(grp)
        others = [f for f in FOODALL if f not in grp]
        out.append(PICF(rng, q, good, [good] + rng.sample(others, 2)))
    return out


def U5(day, rng, v):
    t = "Healthy Eating"
    if day == 1:
        items = [(k, "everyday") for k in take(EVERY, 9, v, "p5d1a")] + [(k, "sometimes") for k in take(SOMETIMES, 6, v, "p5d1b")]
        rng.shuffle(items)
        a = [WORDF(rng, k, ans, ["everyday", "sometimes"], "Everyday or sometimes food?") for k, ans in items]
        return sheet(5, 1, t, "Eat lots of vegetables, fruits, whole grains and protein. Choose water.", "Example: apple  " + ARROW + "  everyday     candy  " + ARROW + "  sometimes", [words(a, "Everyday or sometimes?")])
    if day == 2:
        a = group_q(rng, 6, v, "p5d2")
        b = [(f"{q}  ____", ans) for q, ans in [("Which part is biggest?", "vegetables & fruits"), ("Which part has bread and rice?", "grains"), ("Which part has eggs and fish?", "protein")]]
        return sheet(5, 2, t, "A healthy plate: half vegetables and fruits, a quarter grains, a quarter protein.", "Example: Which is a fruit or vegetable?  " + ARROW + "  carrot",
                     [sec("My healthy plate", "diagram", [({"type": "plate"}, None)], 1, 176),
                      eqs([("Which part is biggest?  (vegetables & fruits / grains / protein)", "vegetables & fruits"), ("Which part has bread and rice?  (grains / protein / vegetables & fruits)", "grains"),
                           ("Which part has eggs and fish?  (protein / grains / vegetables & fruits)", "protein")], "Look at the plate"), pics(a, "Which food?")])
    if day == 3:
        fixed = [("Which drink is best every day?", "water", ["water", "juice", "cake"]), ("Which is a healthy snack?", "apple", ["apple", "candy", "chips"]),
                 ("Which is a healthy breakfast?", "egg", ["egg", "donut", "cookie"]), ("Which drink is best with lunch?", "water", ["juice", "water", "candy"]),
                 ("Which snack gives you energy?", "banana", ["banana", "candy", "donut"]), ("Which is a healthy lunch?", "salmon", ["salmon", "chips", "cookie"]),
                 ("Which is best after sports?", "water", ["water", "candy", "chips"]), ("Which is a crunchy healthy snack?", "carrot", ["carrot", "chips", "cookie"]),
                 ("Which is good for breakfast?", "bread", ["bread", "candy", "donut"]), ("Which is a healthy dinner food?", "rice", ["rice", "cake", "chips"])]
        a = [PICF(rng, q, c, o) for q, c, o in take(fixed, 10, v, "p5d3")]
        return sheet(5, 3, t, inst, "Example: Which drink is best every day?  " + ARROW + "  water", [pics(a, "Healthy choices")])
    if day == 4:
        fixed = [("Which is yellow?", "banana", ["banana", "carrot", "broccoli"]), ("Which is orange?", "carrot", ["carrot", "broccoli", "apple"]), ("Which is green?", "broccoli", ["broccoli", "banana", "carrot"]),
                 ("Which is red?", "apple", ["apple", "banana", "broccoli"]), ("Which grows on a tree?", "apple", ["apple", "carrot", "bread"]), ("Which comes from a hen?", "egg", ["egg", "rice", "beans"]),
                 ("Which swims in water?", "salmon", ["salmon", "bread", "carrot"]), ("Which is made from grain?", "bread", ["bread", "banana", "egg"])]
        a = [PICF(rng, q, c, o) for q, c, o in take(fixed, 8, v, "p5d4a")]
        b = [WORDF(rng, k, g, ["fruit or vegetable", "grain", "protein"], "Which group?") for k, g in
             take([(k, "fruit or vegetable") for k in VEGFRUIT] + [(k, "grain") for k in GRAINS] + [(k, "protein") for k in PROTEIN], 6, v, "p5d4b")]
        return sheet(5, 4, t, "Eat a rainbow of foods!", "Example: Which is yellow?  " + ARROW + "  banana", [pics(a, "Part A – Colours and sources"), words(b, "Part B – Food groups")])
    items = [(k, "everyday") for k in take(EVERY, 3, v, "p5d5a")] + [(k, "sometimes") for k in take(SOMETIMES, 3, v, "p5d5b")]
    rng.shuffle(items)
    a = [WORDF(rng, k, ans, ["everyday", "sometimes"], "Everyday or sometimes?") for k, ans in items]
    return sheet(5, 5, t, "Review day! Then draw your picture.", "Example: broccoli  " + ARROW + "  everyday",
                 [words(a, "Everyday or sometimes?"), pics(group_q(rng, 4, v, "p5d5c"), "Which food?"), _blank_draw(["Draw your favourite healthy meal.", "Draw a healthy snack."], v)])


# ============================================================== UNIT 6
HYG = [("What do you use to wash your hands?", "soap"), ("What do you use to dry your hands?", "towel"), ("What cleans your teeth?", "toothbrush"), ("Where do you take a bath?", "tub"),
       ("What keeps the sun off your head?", "sunhat"), ("What protects your skin from the sun?", "sunscreen"), ("What do you use to blow your nose?", "tissue"), ("What do you turn on to get water?", "tap")]
HYGP = ["soap", "towel", "toothbrush", "tub", "sunhat", "sunscreen", "tissue", "tap"]
STEPS = [("What do you do first when washing hands?", "tap"), ("What comes next after wetting your hands?", "soap"), ("What is the last step?", "towel"), ("What washes the soap away?", "tap")]


def U6(day, rng, v):
    t = "Healthy Habits & Staying Clean"
    if day == 1:
        a = [PIC(rng, q, k, HYGP) for q, k in take(HYG * 2, 10, v, "p6d1")]
        return sheet(6, 1, t, inst, "Example: What do you use to wash your hands?  " + ARROW + "  soap", [pics(a, "What do we use?")])
    if day == 2:
        a = [PIC(rng, q, k, ["tap", "soap", "towel", "tissue"]) for q, k in take(STEPS * 3, 8, v, "p6d2")]
        return sheet(6, 2, t, "Wash hands: wet, soap, scrub, rinse, dry.", "Example: What do you do first?  " + ARROW + "  turn on the tap", [pics(a, "Washing hands")])
    if day == 3:
        a = [PIC(rng, "Which is a germ?", "germ", ["germ", "apple", "ball"]), PIC(rng, "Which helps stop germs?", "soap", ["soap", "germ", "candy"]),
             PIC(rng, "What do you use to cover a sneeze?", "tissue", ["tissue", "ball", "kite"]), PIC(rng, "Which helps stop germs?", "tap", ["tap", "germ", "donut"])]
        b = [WORDF(rng, k, ans, ["yes", "no"], q) for k, ans, q in
             take([("toothbrush", "no", "Share a toothbrush?"), ("soap", "yes", "Wash hands with soap?"), ("tissue", "yes", "Cover a sneeze?"), ("towel", "yes", "Dry hands well?"),
                   ("toothbrush", "yes", "Brush teeth every day?"), ("tap", "yes", "Wash after the bathroom?")], 6, v, "p6d3b")]
        return sheet(6, 3, t, "Germs can make us sick. Healthy habits stop germs.", "Example: Wash hands with soap?  " + ARROW + "  yes",
                     [pics(a, "Part A – Germs"), words(b, "Part B – Yes or no?")])
    if day == 4:
        fixed = [("What do you wear on a bike?", "helmet", ["helmet", "sunhat", "mittens"]), ("What do you wear in a boat?", "lifejacket", ["lifejacket", "helmet", "toque"]),
                 ("What do you wear in the sun?", "sunhat", ["sunhat", "toque", "mittens"]), ("What do you put on your skin in the sun?", "sunscreen", ["sunscreen", "soap", "tissue"]),
                 ("Where do you cross the street?", "crosswalk", ["crosswalk", "stop", "bin_trash"]), ("What tells cars to stop?", "stop", ["stop", "crosswalk", "helmet"]),
                 ("What do you wear to sleep well? ", "bed", ["bed", "helmet", "sunhat"]), ("What helps your teeth?", "toothbrush", ["toothbrush", "candy", "donut"])]
        a = [PICF(rng, q, c, o) for q, c, o in take(fixed, 8, v, "p6d4")]
        fixed2 = a
        return sheet(6, 4, t, "Healthy habits keep us safe and healthy.", "Example: What do you wear on a bike?  " + ARROW + "  helmet", [pics(a, "Stay safe and healthy")])
    a = [PIC(rng, q, k, HYGP) for q, k in take(HYG, 4, v, "p6d5a")]
    b = [PIC(rng, q, k, ["tap", "soap", "towel", "tissue"]) for q, k in take(STEPS, 2, v, "p6d5b")]
    c_ = [WORDF(rng, k, ans, ["yes", "no"], q) for k, ans, q in [("toothbrush", "no", "Share a toothbrush?"), ("soap", "yes", "Wash hands with soap?")]]
    return sheet(6, 5, t, "Review day! Then draw your picture.", "Example: What cleans your teeth?  " + ARROW + "  toothbrush",
                 [pics(a + b, "Healthy habits"), words(c_, "Yes or no?"), _blank_draw(["Draw how you stay clean.", "Draw a healthy habit."], v)])


# ============================================================== UNIT 7
FEEL = ["happy", "sad", "angry", "surprised", "tired", "worried", "proud"]
FEELW = {"happy": "happy", "sad": "sad", "angry": "angry", "surprised": "surprised", "tired": "sleepy", "worried": "worried", "proud": "proud"}
SCEN = [("You get a gift.", "happy"), ("Your ice cream falls.", "sad"), ("Someone takes your toy.", "angry"), ("A loud noise!", "surprised"), ("It is bedtime.", "tired"),
        ("Your friend moves away.", "sad"), ("You have a big test.", "worried"), ("You learned to ride a bike!", "proud"), ("It is your birthday.", "happy"), ("You win a game.", "proud")]
STRAT = [("What helps when you feel angry?", "lungs"), ("What helps when you feel sad?", "hug"), ("What helps when you feel worried?", "talk"), ("What helps when you feel tired?", "bed"),
         ("What helps when you have lots of energy?", "run"), ("What helps when you feel bored?", "crayon"), ("What helps you calm down?", "music"), ("What helps when you feel scared?", "talk")]
STRATP = ["lungs", "hug", "talk", "bed", "run", "crayon", "music"]


def U7(day, rng, v):
    t = "Feelings & Well-Being"
    if day == 1:
        a = [PIC(rng, f"Which face is {FEELW[f]}?", f, FEEL) for f in take(FEEL * 2, 10, v, "p7d1a")]
        b = [WORD(rng, f, FEELW[f], [FEELW[x] for x in FEEL], "How does this face feel?") for f in take(FEEL * 2, 6, v, "p7d1b")]
        return sheet(7, 1, t, "All feelings are OK. Name the feeling.", "Example: Which face is sad?  " + ARROW + "  the sad face", [pics(a, "Part A – Find the face"), words(b, "Part B – Name the feeling")])
    if day == 2:
        a = [PIC(rng, q, f, FEEL) for q, f in take(SCEN, 10, v, "p7d2")]
        return sheet(7, 2, t, "How would you feel?", "Example: You get a gift.  " + ARROW + "  happy", [pics(a, "How do you feel?")])
    if day == 3:
        a = [PIC(rng, q, k, STRATP) for q, k in take(STRAT, 8, v, "p7d3")]
        return sheet(7, 3, t, "There are many ways to feel better.", "Example: What helps when you feel angry?  " + ARROW + "  deep breaths", [pics(a, "What helps?")])
    if day == 4:
        pairs = [("sad", "hug / talk"), ("angry", "deep breaths"), ("tired", "rest"), ("worried", "hug / talk"), ("happy", "share it"), ("surprised", "deep breaths"), ("proud", "share it")]
        a = [WORDF(rng, f, ans, ["deep breaths", "rest", "hug / talk", "share it"], "What would help?") for f, ans in take(pairs * 2, 10, v, "p7d4")]
        return sheet(7, 4, t, "Match the feeling to a helpful idea.", "Example: sad  " + ARROW + "  hug / talk", [words(a, "What would help?")])
    a = [PIC(rng, f"Which face is {FEELW[f]}?", f, FEEL) for f in take(FEEL, 3, v, "p7d5a")]
    b = [PIC(rng, q, k, STRATP) for q, k in take(STRAT, 3, v, "p7d5b")]
    c_ = [PIC(rng, q, f, FEEL) for q, f in take(SCEN, 2, v, "p7d5c")]
    return sheet(7, 5, t, "Review day! Then draw your picture.", "Example: You get a gift.  " + ARROW + "  happy",
                 [pics(a + b + c_, "Feelings and ideas"), _blank_draw(["Draw something that makes you feel calm.", "Draw how you feel today."], v)])


# ============================================================== UNIT 8
KIND_SAY = [("Which is a kind thing to say?", "say_goodgame"), ("Which is a kind thing to say?", "say_nicetry"), ("Which is a kind way to join in?", "say_play"),
            ("Which is a kind thing to say?", "say_thanks"), ("Which says sorry?", "say_sorry"), ("Which is a kind way to say hi?", "say_hello")]
SAYP = ["say_goodgame", "say_nicetry", "say_play", "say_thanks", "say_sorry", "say_hello", "say_cant", "say_go", "say_give"]
BADSAY = {"say_cant", "say_go", "say_give"}
FAIRQ = [("Which shows taking turns?", "turns"), ("Which shows sharing?", "sharing"), ("Which shows including everyone?", "include"), ("Which shows a team?", "team"),
         ("Who helps a team?", "coach"), ("What does a coach use?", "whistle"), ("Which shows being a good friend?", "hug"), ("Which shows teamwork?", "team")]
FAIRP = ["turns", "sharing", "include", "team", "coach", "whistle", "hug", "ball"]


def U8(day, rng, v):
    t = "Friends, Fair Play & Leadership"
    if day == 1:
        a = []
        for q, good in take(KIND_SAY * 2, 10, v, "p8d1"):
            bad = rng.sample(sorted(BADSAY), 2)
            a.append(PICF(rng, q, good, [good] + bad))
        return sheet(8, 1, t, "Kind words help everyone feel included.", "Example: Which is a kind thing to say?  " + ARROW + "  “Good game!”", [pics(a, "Kind words")])
    if day == 2:
        a = [PIC(rng, q, k, FAIRP) for q, k in take(FAIRQ, 10, v, "p8d2")]
        return sheet(8, 2, t, "Fair play means taking turns, sharing and including everyone.", "Example: Which shows taking turns?  " + ARROW + "  the 1 and 2 picture", [pics(a, "Fair play")])
    if day == 3:
        a = [PIC(rng, q, k, FAIRP) for q, k in take([("Who helps a team?", "coach"), ("What does a coach use?", "whistle"), ("Which shows a team?", "team"), ("Which shows a good leader helping?", "hug")] * 2, 8, v, "p8d3")]
        b = [WORDF(rng, k, ans, ["leader", "teammate"], "Is this a leader or teammate?") for k, ans in [("coach", "leader"), ("team", "teammate"), ("turns", "teammate"), ("coach", "leader")]]
        return sheet(8, 3, t, "Leaders help others. Everyone can be a leader.", "Example: Who helps a team?  " + ARROW + "  coach", [pics(a, "Leaders and teams")])
    if day == 4:
        a = []
        for _ in range(6):
            n = rng.randint(2, 5)
            k = rng.choice([2, 3])
            a.append((((rng.choice(["girl", "boy"]), n, f"Each kid gets {k} turns. How many turns in all?  ____")), n * k))
        sh = []
        for _ in range(4):
            f = rng.choice([2, 3, 4])
            n = f * rng.randint(2, 3)
            sh.append((("ball", n, f"Share with {f} friends. Each gets ____"), n // f))
        return sheet(8, 4, t, "Take turns and share fairly so everyone can play.", "Example: 3 kids, 2 turns each  " + ARROW + "  6 turns",
                     [sec("Part A – Fair turns", "count", a, 2, 62), sec("Part B – Share fairly", "count", sh, 2, 62)])
    a = []
    for q, good in take(KIND_SAY, 3, v, "p8d5a"):
        a.append(PICF(rng, q, good, [good] + rng.sample(sorted(BADSAY), 2)))
    b = [PIC(rng, q, k, FAIRP) for q, k in take(FAIRQ, 4, v, "p8d5b")]
    return sheet(8, 5, t, "Review day! Then draw your picture.", "Example: Which shows sharing?  " + ARROW + "  the sharing picture",
                 [pics(a + b, "Fair play and kindness"), _blank_draw(["Draw you and a friend playing fair.", "Draw a kind thing you did."], v)])


# ============================================================== UNIT 9
SNOWQ = [("Which can you do on snow?", "ski"), ("Which can you slide on?", "sled"), ("Which can you do in water?", "swim"), ("Which do you paddle?", "canoe"), ("Which can you do on a trail?", "walk"),
         ("What flies in the wind?", "kite"), ("Which do you ride in the park?", "bike"), ("Which can you do on ice?", "skates")]
SNOWP = ["ski", "sled", "swim", "canoe", "walk", "kite", "bike", "skates"]
DRESS = [("What do you wear in the snow?", "toque", ["toque", "sunhat", "lifejacket"]), ("What keeps your hands warm?", "mittens", ["mittens", "sunhat", "helmet"]),
         ("What keeps your feet warm and dry?", "snowboots", ["snowboots", "sunhat", "kite"]), ("What do you use in the rain?", "umbrella", ["umbrella", "sunhat", "mittens"]),
         ("What do you wear in the sun?", "sunhat", ["sunhat", "toque", "mittens"]), ("What do you put on in the sun?", "sunscreen", ["sunscreen", "toque", "snowboots"]),
         ("What do you wear near deep water?", "lifejacket", ["lifejacket", "toque", "mittens"]), ("What do you wear on a bike?", "helmet", ["helmet", "sunhat", "snowboots"]),
         ("What keeps your head warm?", "toque", ["toque", "sunscreen", "umbrella"]), ("What keeps you dry in rain?", "coat", ["coat", "sunhat", "kite"])]
SAFEQ = [("What do you need near deep water?", "lifejacket"), ("What protects your skin?", "sunscreen"), ("What keeps your head safe on a bike?", "helmet"),
         ("Where do you cross the street?", "crosswalk"), ("What tells you to stop?", "stop"), ("What keeps your hands warm?", "mittens"), ("What shades your face?", "sunhat"), ("What do you wear in a boat?", "lifejacket")]
SAFEP = ["lifejacket", "sunscreen", "helmet", "crosswalk", "stop", "mittens", "sunhat", "toque"]
NATQ = [("Where does garbage go?", "bin_trash"), ("What do we plant?", "tree"), ("Which can we use again?", "bin_recycle"), ("Which do people paddle?", "canoe"),
        ("What do you carry on a hike?", "backpack"), ("What do you drink on a hike?", "water"), ("Where can you hike?", "mountain"), ("Which is a big forest tree in BC?", "cedar")]
NATP = ["bin_trash", "tree", "bin_recycle", "canoe", "backpack", "water", "mountain", "cedar"]


def U9(day, rng, v):
    t = "Outdoor Fun & Staying Safe"
    if day == 1:
        a = [PIC(rng, q, k, SNOWP) for q, k in take(SNOWQ * 2, 10, v, "p9d1")]
        return sheet(9, 1, t, "There is fun to be had in every season. Many First Peoples enjoy being on the land and water.", "Example: Which can you do on snow?  " + ARROW + "  ski", [pics(a, "Outdoor fun")])
    if day == 2:
        a = [PICF(rng, q, c, o) for q, c, o in take(DRESS, 10, v, "p9d2")]
        return sheet(9, 2, t, "Dress for the weather.", "Example: What do you wear in the snow?  " + ARROW + "  warm hat", [pics(a, "What do you wear?")])
    if day == 3:
        a = [PIC(rng, q, k, SAFEP) for q, k in take(SAFEQ * 2, 10, v, "p9d3")]
        return sheet(9, 3, t, "Protect yourself and others outdoors.", "Example: What do you need near deep water?  " + ARROW + "  life jacket", [pics(a, "Stay safe")])
    if day == 4:
        a = [PIC(rng, q, k, NATP) for q, k in take(NATQ * 2, 10, v, "p9d4")]
        return sheet(9, 4, t, "Take care of nature while you play.", "Example: Where does garbage go?  " + ARROW + "  garbage can", [pics(a, "Care for nature")])
    a = [PIC(rng, q, k, SNOWP) for q, k in take(SNOWQ, 3, v, "p9d5a")]
    b = [PICF(rng, q, c, o) for q, c, o in take(DRESS, 3, v, "p9d5b")]
    c_ = [PIC(rng, q, k, SAFEP) for q, k in take(SAFEQ, 3, v, "p9d5c")]
    return sheet(9, 5, t, "Review day! Then draw your picture.", "Example: Which can you slide on?  " + ARROW + "  sled",
                 [pics(a + b + c_, "Outdoor fun and safety"), _blank_draw(["Draw your favourite outdoor game.", "Draw how you dress for the weather."], v)])


# ============================================================== UNIT 10
ORDER3 = [(["stretch", "run", "walk"], "What comes first? (warm up)", "stretch"), (["stretch", "run", "walk"], "What comes last? (cool down)", "walk"),
          (["stretch", "run", "water"], "What do you do after you finish? ", "water")]


def U10(day, rng, v):
    t = "Moving Together: Review & Challenge"
    if day == 1:
        a = [PICF(rng, "What is a good warm-up?", "stretch", ["stretch", "sit_tv", "sleep"]), PICF(rng, "What is a good cool-down?", "walk", ["walk", "run", "skiprope"]),
             PICF(rng, "What do you drink after play?", "water", ["water", "juice", "candy"]), PICF(rng, "What do you wear on a bike?", "helmet", ["helmet", "sunhat", "mittens"]),
             PICF(rng, "What helps you rest?", "bed", ["bed", "run", "kite"]), PICF(rng, "What makes your heart beat fast?", "run", ["run", "sleep", "sit_tv"])]
        pat = [pattern_item(rng, TRAVEL + STAY + ["swim", "dance"]) for _ in range(4)]
        return sheet(10, 1, t, "A good workout: warm up, play, cool down, drink water, rest.", "Example: warm up, play, cool down  " + ARROW + "  stretch, run, walk",
                     [pics(a, "Part A – A healthy workout"), sec("Part B – What comes next?", "picp", pat, 2, 126)])
    if day == 2:
        keys = ["run", "swim", "bike", "dance", "skiprope", "jump"]
        spec = make_graph(rng, keys, 3)
        qs = []
        it = spec["items"]
        top = max(it, key=lambda x: x[1])
        low = min(it, key=lambda x: x[1])
        qs.append((f"Which was done on the most days?  ({' / '.join(rng.sample([LBL[k] for k, _ in it], 3))})", LBL[top[0]]))
        qs.append((f"Which was done on the fewest days?  ({' / '.join(rng.sample([LBL[k] for k, _ in it], 3))})", LBL[low[0]]))
        for k, n in it:
            qs.append((f"On how many days did we do {LBL[k]}?  ____", n))
        qs.append((f"How many more days {LBL[it[0][0]]} than {LBL[it[1][0]]}?  ____ (0 if fewer)", max(it[0][1] - it[1][1], 0)))
        qs.append(("How many active days in all?  ____", sum(n for _, n in it)))
        return sheet(10, 2, t, "Our class counted active days. Read the graph.", "Example: The tallest bar has the most days.",
                     [sec("Active days this week", "diagram", [(spec, None)], 1, 176), eqs([(q, str(a_)) for q, a_ in qs], "Questions")])
    if day == 3:
        items = [(k, "everyday") for k in take(EVERY, 2, v, "p10d3a")] + [(k, "sometimes") for k in take(SOMETIMES, 2, v, "p10d3b")]
        a = [WORDF(rng, k, ans, ["everyday", "sometimes"], "Everyday or sometimes?") for k, ans in items]
        b = [PIC(rng, q, k, HYGP) for q, k in take(HYG, 3, v, "p10d3c")]
        c_ = [PIC(rng, q, f, FEEL) for q, f in take(SCEN, 3, v, "p10d3d")]
        d_ = [PIC(rng, q, k, SAFEP) for q, k in take(SAFEQ, 3, v, "p10d3e")]
        return sheet(10, 3, t, "Mixed review of healthy habits.", "Example: Which is a healthy snack?  " + ARROW + "  apple",
                     [words(a, "Food"), pics(b + c_ + d_, "Habits, feelings and safety")])
    if day == 4:
        groups = {"ball skills": BALLSK, "travelling moves": TRAVEL, "everyday foods": ["apple", "carrot", "broccoli", "banana", "bread", "egg"], "sometimes foods": SOMETIMES,
                  "clean-up things": ["soap", "towel", "tap", "toothbrush"], "winter gear": ["toque", "mittens", "snowboots", "ski"]}
        odd = []
        for _ in range(8):
            g1, g2 = rng.sample(list(groups), 2)
            three = rng.sample(groups[g1], 3)
            o = rng.choice(groups[g2])
            opts = three + [o]
            rng.shuffle(opts)
            odd.append((("Which one does not belong?", opts), "ABCD"[opts.index(o)]))
        return sheet(10, 4, t, "Find the one that does not belong.", "Example: run, hop, jump, apple  " + ARROW + "  apple does not belong", [pics(odd, "Odd one out")])
    a = [PICF(rng, q, c, o) for q, c, o in take(DRESS, 2, v, "p10d5a")]
    b = [PIC(rng, q, k, HYGP) for q, k in take(HYG, 2, v, "p10d5b")]
    pat = [pattern_item(rng, POSE14) for _ in range(2)]
    odd = []
    groups = {"ball skills": BALLSK, "travelling moves": TRAVEL, "everyday foods": ["apple", "carrot", "broccoli", "banana"], "clean-up things": ["soap", "towel", "tap", "toothbrush"]}
    for _ in range(2):
        g1, g2 = rng.sample(list(groups), 2)
        three = rng.sample(groups[g1], 3)
        o = rng.choice(groups[g2])
        opts = three + [o]
        rng.shuffle(opts)
        odd.append((("Which one does not belong?", opts), "ABCD"[opts.index(o)]))
    return sheet(10, 5, t, "Challenge day! Odd one out, patterns, and a drawing.", "Example: What comes next?  " + ARROW + "  follow the pattern",
                 [pics(a + b + odd, "Healthy active me"), sec("What comes next?", "picp", pat, 2, 126), _blank_draw(["Draw your healthy, active day.", "Draw how you will stay healthy."], v)])


UNITS = {1: U1, 2: U2, 3: U3, 4: U4, 5: U5, 6: U6, 7: U7, 8: U8, 9: U9, 10: U10}


def unit_sheets(u, variant=0):
    return [fit(UNITS[u](d, random.Random(u * 100 + d + variant * 1000), variant)) for d in range(1, 6)]


def checkup_a():
    rng = random.Random(4555)
    s = [pics([PIC(rng, "What do you use to see?", "eye", BODYP), PIC(rng, "Which pumps blood?", "heart", BODYP), PIC(rng, "Which one is jumping?", "jump", POSE14),
               PICF(rng, "Which is more active?", "run", ["run", "sit_tv"])], "Body, moves and activity"),
         words([WORDF(rng, "catch", "ball skill", ["travel", "stay in place", "ball skill"], "Which kind of move?"), WORDF(rng, "balance", "stay in place", ["travel", "stay in place", "ball skill"], "Which kind of move?"),
                WORDF(rng, "run", "faster", ["faster", "slower"], "Heart beat?"), WORDF(rng, "sleep", "slower", ["faster", "slower"], "Heart beat?")], "Moves and heart"),
         pics([PIC(rng, "Where can you swim?", "lake", PLACEP), PICF(rng, "Which makes you breathe harder?", "run", ["run", "sleep", "sit_tv"]),
               PICF(rng, "Which drink is best every day?", "water", ["water", "juice", "cake"]), PICF(rng, "Which is a fruit or vegetable?", "carrot", ["carrot", "bread", "candy"])], "Play, heart and food"),
         words([WORDF(rng, "apple", "everyday", ["everyday", "sometimes"], "Everyday or sometimes?"), WORDF(rng, "candy", "sometimes", ["everyday", "sometimes"], "Everyday or sometimes?")], "Food")]
    return sheet(0, "A", "Check-Up: Units 1–5", "Show what you know! Do your best on every question.", "Aim for 90% or more before moving on to Unit 6.", s)


def final_test():
    rng = random.Random(4999)
    s = [pics([PIC(rng, "What do you use to wash your hands?", "soap", HYGP), PIC(rng, "What do you use to dry your hands?", "towel", HYGP),
               PIC(rng, "What do you wear on a bike?", "helmet", ["helmet", "sunhat", "toque"]), PICF(rng, "Which face is sad?", "sad", ["happy", "sad", "angry"])], "Healthy habits and feelings"),
         pics([PIC(rng, "What helps when you feel angry?", "lungs", STRATP), PICF(rng, "Which is a kind thing to say?", "say_goodgame", ["say_goodgame", "say_cant", "say_go"]),
               PIC(rng, "Which shows taking turns?", "turns", FAIRP), PIC(rng, "Who helps a team?", "coach", FAIRP)], "Calm, kind and fair"),
         pics([PICF(rng, "What do you wear in the snow?", "toque", ["toque", "sunhat", "lifejacket"]), PICF(rng, "What do you put on in the sun?", "sunscreen", ["sunscreen", "toque", "snowboots"]),
               PIC(rng, "Which do people paddle?", "canoe", NATP), PICF(rng, "Which can you do on snow?", "ski", ["ski", "swim", "canoe"])], "Outdoors"),
         words([WORDF(rng, "carrot", "fruit or vegetable", ["fruit or vegetable", "grain", "protein"], "Which group?"), WORDF(rng, "bread", "grain", ["fruit or vegetable", "grain", "protein"], "Which group?"),
                WORDF(rng, "egg", "protein", ["fruit or vegetable", "grain", "protein"], "Which group?"), WORDF(rng, "chips", "sometimes", ["everyday", "sometimes"], "Everyday or sometimes?")], "Food"),
         sec("What comes next?", "picp", [pattern_item(rng, TRAVEL + STAY) for _ in range(2)], 2, 126)]
    return sheet(0, "F", "Final Test: Units 1–10", "You made it! Show everything you have learned.", "Aim for 90% or more. Then it's certificate time!", s)
