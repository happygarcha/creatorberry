"""Picture-based generators for the Grade 2 Physical & Health Education workbook.

Aligned to the BC Grade 2 PHE curriculum (Big Ideas, Curricular Competencies and Content as published at
curriculum.gov.bc.ca): fundamental movement skills (non-locomotor / locomotor / manipulative), types of physical
activity (individual & dual, rhythmic, games), 60-90 minutes of daily activity, the 1-5 exertion scale, effects of
activity on the body, healthy eating, illness prevention, accessing support, safety strategies, substances,
emotions, self-identity, and safety / fair play / leadership.
"""
import random
import pheicons  # noqa: F401  (adds poses/food/hygiene icons)
from english_generators import take, fit, ARROW
from generators import sec, sheet
from sticons import LBL
from social_generators import (PIC, PICF, WORD, WORDF, lw, pics, words, eqs, draw, make_graph, pattern_item)

inst = "Look at the pictures. Pick the best answer."

# ---- official Grade 2 movement skill lists
NONLOC = ["balance", "bend", "twist", "lift"]                    # non-locomotor ("on the spot")
LOCO = ["roll", "jump", "hop", "run", "gallop"]                  # locomotor (travelling)
MANIP = ["bounce", "throw", "catch", "kick", "strike"]           # manipulative (objects / balls)
SKILLS14 = NONLOC + LOCO + MANIP
KIND = {**{k: "on the spot" for k in NONLOC}, **{k: "travelling" for k in LOCO}, **{k: "with a ball" for k in MANIP}}
KINDW = ["on the spot", "travelling", "with a ball"]
# ---- types of physical activity
SOLO = ["skiprope", "swim", "run", "bike", "yoga", "hulahoop"]   # individual & dual activities
RHYTHM = ["dance", "gymnastics"]
GAMES = ["tag", "parachute", "simonsays"]
ATYPE = {**{k: "alone or with a partner" for k in SOLO}, **{k: "rhythm" for k in RHYTHM}, **{k: "game with rules" for k in GAMES}}
ATYPEW = ["alone or with a partner", "rhythm", "game with rules"]
ACTIVE = SOLO + RHYTHM + GAMES + ["kick", "canoe", "playground", "throw", "jump"]
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
ADULTS = ["mom", "dad", "grandma", "grandpa", "teacher", "doctor"]


def _draw(prompts, v):
    return draw(prompts[v])


# ============================================================== UNIT 1  Physical literacy
BODYQ = [("Which letter shows the head?", "A"), ("Which letter shows the arm?", "B"), ("Which letter shows the leg?", "C"), ("Which letter shows the foot?", "D"),
         ("Which letter do you use to think?", "A"), ("Which letter do you use to throw?", "B"), ("Which letter do you use to run?", "C"), ("Which letter do you stand on?", "D")]
USEQ = [("Which one uses your arms most?", "throw", ["throw", "kick", "sit_tv"]), ("Which one uses your legs most?", "run", ["run", "catch", "sleep"]),
        ("Which needs your eyes and hands?", "catch", ["catch", "sleep", "sit_tv"]), ("Which one needs good balance?", "balance", ["balance", "sit_tv", "sleep"]),
        ("Which one moves your whole body?", "swim", ["swim", "sit_tv", "sleep"]), ("Which one turns your body?", "twist", ["twist", "sit_tv", "sleep"]),
        ("Which one uses your feet with a ball?", "kick", ["kick", "throw", "catch"]), ("Which one uses your hands with a ball?", "bounce", ["bounce", "kick", "run"])]


def U1(day, rng, v):
    t = "My Body & Physical Literacy"
    if day == 1:
        a = [PIC(rng, q, k, BODYP) for q, k in take(BODY_USE * 2, 8, v, "p1d1a")]
        b = [WORD(rng, k, LBL[k], lw(BODYP), "What body part is this?") for k in take(BODYP * 2, 8, v, "p1d1b")]
        return sheet(1, 1, t, inst, "Example: What do you use to see?  " + ARROW + "  eye", [pics(a, "Part A – What do we use?"), words(b, "Part B – Name the part")])
    if day == 2:
        a = [(f"{q}  ____", ans) for q, ans in take(BODYQ, 8, v, "p1d2")]
        return sheet(1, 2, t, "Look at the body. Write the letter.", "Example: Which letter shows the head?  " + ARROW + "  A",
                     [sec("Look at the body", "diagram", [({"type": "body"}, None)], 1, 176), eqs(a, "Which letter?")])
    if day == 3:
        a = [WORD(rng, k, LBL[k], lw(SKILLS14), "What is this person doing?") for k in take(SKILLS14 * 2, 14, v, "p1d3")]
        return sheet(1, 3, t, "Name how people move.", "Example: What is this person doing?  " + ARROW + "  jumping", [words(a, "Name the move")])
    if day == 4:
        a = [PICF(rng, q, c, o) for q, c, o in take(USEQ, 8, v, "p1d4")]
        return sheet(1, 4, t, inst, "Example: Which one uses your arms most?  " + ARROW + "  throwing", [pics(a, "Which body part works hard?")])
    a = [PIC(rng, q, k, BODYP) for q, k in take(BODY_USE, 3, v, "p1d5a")]
    b = [WORD(rng, k, LBL[k], lw(SKILLS14), "What is this person doing?") for k in take(SKILLS14, 4, v, "p1d5b")]
    c_ = [PICF(rng, q, c, o) for q, c, o in take(USEQ, 3, v, "p1d5c")]
    return sheet(1, 5, t, "Review day! Then draw your picture.", "Example: What do you use to hear?  " + ARROW + "  ear",
                 [pics(a + c_, "Body and movement"), words(b, "Name the move"), _draw(["Draw your favourite way to move.", "Draw your body and how it moves."], v)])


# ============================================================== UNIT 2  Fundamental movement skills
GEAR = [("What do you use to skip?", "rope"), ("What do you use to ride?", "bike"), ("What do you throw and kick?", "ball"), ("What do you use to hit a ball?", "bat"),
        ("What do you spin around your waist?", "hoop"), ("What do you wear to glide on ice?", "skates"), ("What do you slide on in snow?", "sled"), ("What protects your head on a bike?", "helmet")]
GEARP = ["rope", "bike", "ball", "bat", "hoop", "skates", "sled", "helmet"]


def U2(day, rng, v):
    t = "Fundamental Movement Skills"
    if day == 1:
        a = [WORDF(rng, k, KIND[k], KINDW, "Which kind of move?") for k in take(list(KIND) * 2, 14, v, "p2d1")]
        return sheet(2, 1, t, "On the spot: balance, bend, twist, lift. Travelling: roll, jump, hop, run, gallop. With a ball: bounce, throw, catch, kick, strike.",
                     "Example: jumping  " + ARROW + "  travelling     catching  " + ARROW + "  with a ball", [words(a, "Which kind of move?")])
    if day == 2:
        a = [PIC(rng, f"Which one is {LBL[k]}?", k, SKILLS14) for k in take(SKILLS14 * 2, 10, v, "p2d2")]
        return sheet(2, 2, t, inst, "Example: Which one is jumping?  " + ARROW + "  pick the jumper", [pics(a, "Find the move")])
    if day == 3:
        a = [PIC(rng, q, k, GEARP) for q, k in take(GEAR, 8, v, "p2d3a")]
        b = [WORD(rng, k, LBL[k], lw(GEARP), "What is this?") for k in take(GEARP, 6, v, "p2d3b")]
        return sheet(2, 3, t, inst, "Example: What do you use to skip?  " + ARROW + "  skipping rope", [pics(a, "Part A – What do we use?"), words(b, "Part B – Name it")])
    if day == 4:
        a = [pattern_item(rng, SKILLS14) for _ in range(6)]
        return sheet(2, 4, t, "Look at the pattern. What move comes next?", "Example: run, jump, run, jump, ?  " + ARROW + "  run", [sec("What comes next?", "picp", a, 2, 126)])
    a = [WORDF(rng, k, KIND[k], KINDW, "Which kind of move?") for k in take(list(KIND), 4, v, "p2d5a")]
    b = [PIC(rng, f"Which one is {LBL[k]}?", k, SKILLS14) for k in take(SKILLS14, 3, v, "p2d5b")]
    c_ = [PIC(rng, q, k, GEARP) for q, k in take(GEAR, 3, v, "p2d5c")]
    return sheet(2, 5, t, "Review day! Then draw your picture.", "Example: catching  " + ARROW + "  with a ball",
                 [words(a, "Which kind of move?"), pics(b + c_, "Moves and gear"), _draw(["Draw yourself doing a ball skill.", "Draw yourself balancing or twisting."], v)])


# ============================================================== UNIT 3  Ways to be active (types, 60-90 minutes, where)
OPP = [("playground", "at school"), ("school", "at school"), ("house", "at home"), ("sofa", "at home"), ("park", "in the community"), ("lake", "in the community"),
       ("ocean", "in the community"), ("mountain", "in the community")]
OPPW = ["at school", "at home", "in the community"]
EQUIP = [("ball", "with equipment"), ("skiprope", "with equipment"), ("bike", "with equipment"), ("kite", "with equipment"), ("hulahoop", "with equipment"),
         ("run", "without equipment"), ("dance", "without equipment"), ("hop", "without equipment"), ("yoga", "without equipment"), ("tag", "without equipment")]


def U3(day, rng, v):
    t = "Ways to Be Active Every Day"
    if day == 1:
        items = [(k, "active") for k in take(ACTIVE, 8, v, "p3d1a")] + [(k, "not active") for k in take(NOTACT * 2, 6, v, "p3d1b")]
        rng.shuffle(items)
        a = [WORDF(rng, k, ans, ["active", "not active"], "Active or not?") for k, ans in items]
        return sheet(3, 1, t, "Get 60 to 90 minutes of active play every day! It helps your whole well-being.", "Example: running  " + ARROW + "  active     watching TV  " + ARROW + "  not active", [words(a, "Active or not?")])
    if day == 2:
        a = [WORDF(rng, k, ATYPE[k], ATYPEW, "Which kind of activity?") for k in take(list(ATYPE) * 2, 14, v, "p3d2")]
        return sheet(3, 2, t, "You can be active alone or with a partner, to music and rhythm, or in games with rules.", "Example: swimming  " + ARROW + "  alone or with a partner     dancing  " + ARROW + "  rhythm",
                     [words(a, "Which kind of activity?")])
    if day == 3:
        a = []
        for k in take(["run", "swim", "dance", "skiprope", "bike", "jump"] * 2, 6, v, "p3d3a"):
            n = rng.randint(3, 9)
            a.append(((k, n, "Each = 10 minutes. How many minutes?  ____"), n * 10))
        b = []
        for k in take(["run", "swim", "dance", "skiprope", "bike", "jump"] * 2, 4, v, "p3d3b"):
            n = rng.randint(3, 9)
            b.append(((k, n, "Each = 10 minutes. 60 minutes or more?  ____"), "yes" if n >= 6 else "no"))
        return sheet(3, 3, t, "Count the active play. Each picture is 10 minutes. Aim for 60 to 90 minutes a day!", "Example: 6 pictures = 60 minutes",
                     [sec("Part A – How many minutes?", "count", a, 2, 62), sec("Part B – Is it enough?", "count", b, 2, 62)])
    if day == 4:
        a = [WORDF(rng, k, p, OPPW, "Where can you be active?") for k, p in take(OPP * 2, 8, v, "p3d4a")]
        b = [WORDF(rng, k, p, ["with equipment", "without equipment"], "Equipment?") for k, p in take(EQUIP, 6, v, "p3d4b")]
        return sheet(3, 4, t, "You can be active at school, at home and in your community, with or without equipment.", "Example: playground  " + ARROW + "  at school",
                     [words(a, "Part A – Where?"), words(b, "Part B – Equipment?")])
    items = [(k, "active") for k in take(ACTIVE, 2, v, "p3d5a")] + [(k, "not active") for k in take(NOTACT, 2, v, "p3d5b")]
    rng.shuffle(items)
    a = [WORDF(rng, k, ans, ["active", "not active"], "Active or not?") for k, ans in items]
    b = [WORDF(rng, k, ATYPE[k], ATYPEW, "Which kind of activity?") for k in take(list(ATYPE), 3, v, "p3d5c")]
    c_ = [WORDF(rng, k, p, OPPW, "Where can you be active?") for k, p in take(OPP, 3, v, "p3d5d")]
    return sheet(3, 5, t, "Review day! Then draw your picture.", "Example: tag  " + ARROW + "  game with rules",
                 [words(a + b + c_, "Ways to be active"), _draw(["Draw your favourite active game.", "Draw where you like to be active."], v)])


# ============================================================== UNIT 4  Effects of activity, exertion 1-5, rest
EFFECT_Q = [("Which shows sweating?", "sweat"), ("Which shows muscles working?", "muscle"), ("Which shows feeling thirsty?", "glass"), ("Which shows breathing harder?", "breath_hard"),
            ("Which shows feeling good?", "happy")]
EFFECT_P = ["sweat", "muscle", "glass", "breath_hard", "happy", "sleep"]
EXNUM = ["exert1", "exert2", "exert3", "exert4", "exert5"]
REST = [("What helps your body rest?", "bed", ["bed", "run", "ball"]), ("What do you drink when you are thirsty?", "water", ["water", "chips", "candy"]),
        ("When do we sleep?", "moon", ["moon", "sun", "run"]), ("When are you awake and playing?", "sun", ["sun", "moon", "bed"]),
        ("What helps your heart slow down?", "sleep", ["sleep", "run", "jump"]), ("Which one helps you cool down after play?", "walk", ["walk", "jump", "skiprope"])]


def U4(day, rng, v):
    t = "How My Body Feels When I Move"
    if day == 1:
        a = [PIC(rng, q, k, EFFECT_P) for q, k in take(EFFECT_Q * 3, 10, v, "p4d1")]
        return sheet(4, 1, t, "When we are active we breathe harder, sweat, get thirsty, use our muscles and feel good.", "Example: Which shows sweating?  " + ARROW + "  the sweaty face", [pics(a, "What happens when we move?")])
    if day == 2:
        fixed = [("Which number feels hottest?", "exert5", ["exert1", "exert3", "exert5"]), ("Which number is cold?", "exert1", ["exert1", "exert4", "exert5"]),
                 ("Which number is warm?", "exert3", ["exert1", "exert3", "exert5"]), ("Which number is getting warmer?", "exert2", ["exert2", "exert4", "exert5"]),
                 ("Which number is getting hot?", "exert4", ["exert1", "exert2", "exert4"]), ("After running hard, which number fits best?", "exert5", ["exert1", "exert2", "exert5"]),
                 ("When you are resting, which number fits best?", "exert1", ["exert1", "exert4", "exert5"]), ("After a slow walk, which number fits best?", "exert2", ["exert2", "exert4", "exert5"])]
        a = [PICF(rng, q, c, o) for q, c, o in take(fixed, 8, v, "p4d2a")]
        b = [(q, ans) for q, ans in [("Number 1 means  (cold / very hot)", "cold"), ("Number 5 means  (very hot / cold)", "very hot"), ("Number 3 means  (warm / cold)", "warm"),
                                     ("Number 2 means  (getting warmer / very hot)", "getting warmer"), ("Number 4 means  (getting hot / cold)", "getting hot")]]
        return sheet(4, 2, t, "Use the 1 to 5 scale to tell how hot your body feels: 1 cold, 3 warm, 5 very hot.", "Example: Number 5 means very hot",
                     [sec("The exertion scale", "diagram", [({"type": "exert"}, None)], 1, 96), pics(a, "Part A – Pick the number"), eqs(b[:3], "Part B – What does it mean?")])
    if day == 3:
        q2 = [("Which pumps blood?", "heart"), ("Which helps you breathe?", "lungs"), ("Which one beats?", "heart"), ("Which one fills with air?", "lungs")]
        a = [PIC(rng, q, k, ["heart", "lungs", "hand", "foot", "ear", "eye"]) for q, k in take(q2 * 2, 6, v, "p4d3a")]
        b = [(("heart", n, "Count the beats.  ____"), n) for n in (rng.randint(3, 9) for _ in range(4))]
        return sheet(4, 3, t, "Your heart pumps blood. Your lungs bring in air. Active play makes them work harder.", "Example: Which pumps blood?  " + ARROW + "  heart",
                     [pics(a, "Part A – Heart and lungs"), sec("Part B – Count the heartbeats", "count", b, 2, 62)])
    if day == 4:
        fast, slow = ["run", "swim", "skiprope", "jump", "dance"], ["sit_tv", "sleep", "walk"]
        a = []
        for i in range(6):
            q = "Which makes your heart beat fastest?" if i % 2 == 0 else "Which makes you breathe harder?"
            good = rng.choice(fast)
            a.append(PICF(rng, q, good, [good] + rng.sample(slow, 2)))
        b = [PICF(rng, q, c, o) for q, c, o in take(REST, 4, v, "p4d4b")]
        return sheet(4, 4, t, "Hard play makes your heart beat faster. Rest, sleep and water help your body.", "Example: Which makes your heart beat fastest?  " + ARROW + "  running",
                     [pics(a, "Part A – Fast heart"), pics(b, "Part B – Rest and recover")])
    a = [PIC(rng, q, k, EFFECT_P) for q, k in take(EFFECT_Q, 3, v, "p4d5a")]
    fixed = [("Which number feels hottest?", "exert5", ["exert1", "exert3", "exert5"]), ("Which number is cold?", "exert1", ["exert1", "exert4", "exert5"]), ("Which number is warm?", "exert3", ["exert1", "exert3", "exert5"])]
    b = [PICF(rng, q, c, o) for q, c, o in take(fixed, 2, v, "p4d5b")]
    c_ = [PICF(rng, q, c, o) for q, c, o in take(REST, 2, v, "p4d5c")]
    return sheet(4, 5, t, "Review day! Then draw your picture.", "Example: Which shows sweating?  " + ARROW + "  the sweaty face",
                 [pics(a + b + c_, "Moving and resting"), _draw(["Draw how your body feels after running.", "Draw what you do to rest."], v)])


# ============================================================== UNIT 5  Healthy eating & energy
def group_q(rng, n):
    out = []
    spec = [("Which one is a fruit or vegetable?", VEGFRUIT), ("Which one is a grain food?", GRAINS), ("Which one is a protein food?", PROTEIN)]
    for i in range(n):
        q, grp = spec[i % 3]
        good = rng.choice(grp)
        others = [f for f in FOODALL if f not in grp]
        out.append(PICF(rng, q, good, [good] + rng.sample(others, 2)))
    return out


ENERGY = [("Which gives you energy to play?", "banana", ["banana", "candy", "chips"]), ("Which gives you energy to grow?", "egg", ["egg", "donut", "cookie"]),
          ("Which gives you energy to learn?", "bread", ["bread", "candy", "cake"]), ("Which helps you grow strong?", "salmon", ["salmon", "chips", "donut"]),
          ("Which gives you energy for a long walk?", "rice", ["rice", "candy", "juice"]), ("Which helps you play and think?", "orange", ["orange", "cookie", "chips"])]
HELPERS = [("Who can help you choose healthy foods?", "mom", ["mom", "ball", "kite"]), ("Who can help you learn about healthy foods?", "teacher", ["teacher", "game", "candy"]),
           ("Who can you ask about healthy foods?", "doctor", ["doctor", "kite", "chips"]), ("Who makes meals with you?", "dad", ["dad", "ball", "donut"])]


def U5(day, rng, v):
    t = "Healthy Eating & Energy"
    if day == 1:
        items = [(k, "everyday") for k in take(EVERY, 9, v, "p5d1a")] + [(k, "sometimes") for k in take(SOMETIMES, 6, v, "p5d1b")]
        rng.shuffle(items)
        a = [WORDF(rng, k, ans, ["everyday", "sometimes"], "Everyday or sometimes food?") for k, ans in items]
        return sheet(5, 1, t, "Eat lots of vegetables, fruits, whole grains and protein. Choose water.", "Example: apple  " + ARROW + "  everyday     candy  " + ARROW + "  sometimes", [words(a, "Everyday or sometimes?")])
    if day == 2:
        a = group_q(rng, 6)
        return sheet(5, 2, t, "A healthy plate: half vegetables and fruits, a quarter grains, a quarter protein.", "Example: Which is a fruit or vegetable?  " + ARROW + "  carrot",
                     [sec("My healthy plate", "diagram", [({"type": "plate"}, None)], 1, 176),
                      eqs([("Which part is biggest?  (vegetables & fruits / grains / protein)", "vegetables & fruits"), ("Which part has bread and rice?  (grains / protein / vegetables & fruits)", "grains"),
                           ("Which part has eggs and fish?  (protein / grains / vegetables & fruits)", "protein")], "Look at the plate"), pics(a, "Which food?")])
    if day == 3:
        a = [PICF(rng, q, c, o) for q, c, o in take(ENERGY, 6, v, "p5d3a")]
        b = [PICF(rng, q, c, o) for q, c, o in HELPERS]
        return sheet(5, 3, t, "Foods give us energy to grow, play and learn. Ask a trusted adult to help you choose.", "Example: Which gives you energy to play?  " + ARROW + "  banana",
                     [pics(a, "Part A – Food for energy"), pics(b, "Part B – Who can help?")])
    if day == 4:
        a = []
        for _ in range(6):
            keys = rng.sample(VEGFRUIT + GRAINS + PROTEIN, rng.randint(3, 6))
            a.append(((keys, "How many different foods?  ____"), len(keys)))
        fixed = [("Which drink is best every day?", "water", ["water", "juice", "cake"]), ("Which is a healthy snack?", "apple", ["apple", "candy", "chips"]),
                 ("Which is a healthy breakfast?", "egg", ["egg", "donut", "cookie"]), ("Which is a crunchy healthy snack?", "carrot", ["carrot", "chips", "cookie"])]
        b = [PICF(rng, q, c, o) for q, c, o in take(fixed, 4, v, "p5d4b")]
        return sheet(5, 4, t, "Try a variety of foods! Count the different foods on each plate.", "Example: apple, bread, egg  " + ARROW + "  3 different foods",
                     [sec("Part A – How many different foods?", "coins", a, 2, 74), pics(b, "Part B – Healthy choices")])
    items = [(k, "everyday") for k in take(EVERY, 3, v, "p5d5a")] + [(k, "sometimes") for k in take(SOMETIMES, 3, v, "p5d5b")]
    rng.shuffle(items)
    a = [WORDF(rng, k, ans, ["everyday", "sometimes"], "Everyday or sometimes?") for k, ans in items]
    return sheet(5, 5, t, "Review day! Then draw your picture.", "Example: broccoli  " + ARROW + "  everyday",
                 [words(a, "Everyday or sometimes?"), pics(group_q(rng, 3) + [PICF(rng, q, c, o) for q, c, o in take(ENERGY, 1, v, "p5d5c")], "Which food?"),
                  _draw(["Draw a healthy meal with different foods.", "Draw a healthy snack."], v)])


# ============================================================== UNIT 6  Illness prevention & healthy practices
HYG = [("What do you use to wash your hands?", "soap"), ("What do you use to dry your hands?", "towel"), ("What cleans your teeth?", "toothbrush"), ("Where do you take a bath?", "tub"),
       ("What keeps the sun off your head?", "sunhat"), ("What protects your skin from the sun?", "sunscreen"), ("What do you use to blow your nose?", "tissue"), ("What do you turn on to get water?", "tap")]
HYGP = ["soap", "towel", "toothbrush", "tub", "sunhat", "sunscreen", "tissue", "tap"]
STEPS = [("What do you do first when washing hands?", "tap"), ("What comes next after wetting your hands?", "soap"), ("What is the last step?", "towel"), ("What washes the soap away?", "tap")]
SICK = [("What do you do when you cough?", "cough", ["cough", "ball", "kite"]), ("What do you need when you are sick?", "bed", ["bed", "run", "skiprope"]),
        ("Where do you stay when you are sick?", "house", ["house", "park", "playground"]), ("What do you use for a sneeze?", "tissue", ["tissue", "ball", "kite"]),
        ("Which shows someone who is sick?", "sick", ["sick", "happy", "proud"]), ("What helps stop germs from spreading?", "soap", ["soap", "germ", "candy"]),
        ("Who can help when you are sick?", "doctor", ["doctor", "ball", "kite"]), ("What do you do when you feel sick?", "bed", ["bed", "tag", "swim"])]


def U6(day, rng, v):
    t = "Healthy Habits & Preventing Illness"
    if day == 1:
        a = [PIC(rng, q, k, HYGP) for q, k in take(HYG * 2, 10, v, "p6d1")]
        return sheet(6, 1, t, inst, "Example: What do you use to wash your hands?  " + ARROW + "  soap", [pics(a, "What do we use?")])
    if day == 2:
        a = [PIC(rng, q, k, ["tap", "soap", "towel", "tissue"]) for q, k in take(STEPS * 3, 8, v, "p6d2")]
        return sheet(6, 2, t, "Wash hands: wet, soap, scrub, rinse, dry.", "Example: What do you do first?  " + ARROW + "  turn on the tap", [pics(a, "Washing hands")])
    if day == 3:
        a = [PICF(rng, q, c, o) for q, c, o in take(SICK, 8, v, "p6d3a")]
        b = [WORDF(rng, k, ans, ["yes", "no"], q) for k, ans, q in
             take([("cough", "yes", "Cover your mouth when you cough?"), ("bed", "yes", "Rest when you are sick?"), ("house", "yes", "Stay home when you are sick?"),
                   ("tissue", "yes", "Throw away used tissues?"), ("soap", "yes", "Wash hands after the bathroom?"), ("toothbrush", "no", "Share a toothbrush?")], 6, v, "p6d3b")]
        return sheet(6, 3, t, "Germs spread when we are sick. Cover coughs, wash hands, rest and stay home.", "Example: Cover your mouth when you cough?  " + ARROW + "  yes",
                     [pics(a, "Part A – When you are sick"), words(b, "Part B – Yes or no?")])
    if day == 4:
        fixed = [("What do you wear in the sun?", "sunhat", ["sunhat", "toque", "mittens"]), ("What do you put on your skin in the sun?", "sunscreen", ["sunscreen", "soap", "tissue"]),
                 ("What helps your teeth?", "toothbrush", ["toothbrush", "candy", "donut"]), ("What do you need for a good rest?", "bed", ["bed", "helmet", "sunhat"]),
                 ("What do you drink every day?", "water", ["water", "juice", "cake"]), ("What helps you stay clean?", "tub", ["tub", "ball", "kite"]),
                 ("What do you use to blow your nose?", "tissue", ["tissue", "towel", "soap"]), ("What keeps your hands clean?", "soap", ["soap", "ball", "tissue"])]
        a = [PICF(rng, q, c, o) for q, c, o in take(fixed, 8, v, "p6d4")]
        return sheet(6, 4, t, "Healthy habits protect you and others.", "Example: What helps your teeth?  " + ARROW + "  toothbrush", [pics(a, "Healthy habits")])
    a = [PIC(rng, q, k, HYGP) for q, k in take(HYG, 3, v, "p6d5a")]
    b = [PICF(rng, q, c, o) for q, c, o in take(SICK, 3, v, "p6d5b")]
    c_ = [WORDF(rng, k, ans, ["yes", "no"], q) for k, ans, q in [("cough", "yes", "Cover your mouth when you cough?"), ("toothbrush", "no", "Share a toothbrush?")]]
    return sheet(6, 5, t, "Review day! Then draw your picture.", "Example: What cleans your teeth?  " + ARROW + "  toothbrush",
                 [pics(a + b, "Healthy habits"), words(c_, "Yes or no?"), _draw(["Draw how you stay healthy.", "Draw what you do to stop germs."], v)])


# ============================================================== UNIT 7  Emotions & self-identity
FEEL = ["happy", "sad", "angry", "surprised", "tired", "worried", "proud"]
FEELW = {"happy": "happy", "sad": "sad", "angry": "angry", "surprised": "surprised", "tired": "sleepy", "worried": "worried", "proud": "proud"}
SCEN = [("You get a gift.", "happy"), ("Your ice cream falls.", "sad"), ("Someone takes your toy.", "angry"), ("A loud noise!", "surprised"), ("It is bedtime.", "tired"),
        ("Your friend moves away.", "sad"), ("You have a big test.", "worried"), ("You learned to ride a bike!", "proud"), ("It is your birthday.", "happy"), ("You win a game.", "proud")]
STRAT = [("What helps when you feel angry?", "lungs"), ("What helps when you feel sad?", "hug"), ("What helps when you feel worried?", "talk"), ("What helps when you feel tired?", "bed"),
         ("What helps when you have lots of energy?", "run"), ("What helps when you feel bored?", "crayon"), ("What helps you calm down?", "music"), ("What helps when you feel scared?", "talk")]
STRATP = ["lungs", "hug", "talk", "bed", "run", "crayon", "music"]
SELF = [("You learned to ride a bike.", "proud"), ("You learned to swim.", "proud"), ("You tried a new food.", "proud"), ("You helped a friend.", "proud"), ("You kept trying.", "proud"),
        ("You read a whole book.", "proud")]
CELEB = [("Which is a birthday treat?", "cake", ["cake", "hose", "tap"]), ("Which lights up the night sky?", "fireworks", ["fireworks", "bed", "soap"]),
         ("Which is a present?", "gift", ["gift", "tap", "towel"]), ("Which hangs for Lunar New Year?", "lantern", ["lantern", "tap", "soap"]),
         ("Which do families enjoy cooking and eating together?", "bread", ["bread", "hose", "helmet"])]


def U7(day, rng, v):
    t = "Feelings & Who I Am"
    if day == 1:
        a = [PIC(rng, f"Which face is {FEELW[f]}?", f, FEEL) for f in take(FEEL * 2, 10, v, "p7d1a")]
        b = [WORD(rng, f, FEELW[f], [FEELW[x] for x in FEEL], "How does this face feel?") for f in take(FEEL * 2, 6, v, "p7d1b")]
        return sheet(7, 1, t, "All feelings are OK. Name the feeling.", "Example: Which face is sad?  " + ARROW + "  the sad face", [pics(a, "Part A – Find the face"), words(b, "Part B – Name the feeling")])
    if day == 2:
        a = [PIC(rng, q, f, FEEL) for q, f in take(SCEN, 10, v, "p7d2")]
        return sheet(7, 2, t, "How would you feel?", "Example: You get a gift.  " + ARROW + "  happy", [pics(a, "How do you feel?")])
    if day == 3:
        a = [PIC(rng, q, k, STRATP) for q, k in take(STRAT, 8, v, "p7d3")]
        return sheet(7, 3, t, "We can manage our feelings. There are many ways to feel better.", "Example: What helps when you feel angry?  " + ARROW + "  deep breaths", [pics(a, "What helps?")])
    if day == 4:
        a = [PIC(rng, q + " How do you feel?", f, FEEL) for q, f in take(SELF, 5, v, "p7d4a")]
        b = [PICF(rng, q, c, o) for q, c, o in take(CELEB, 4, v, "p7d4b")]
        return sheet(7, 4, t, "Be proud of what you can do. Families have special traditions and celebrations.", "Example: You learned to ride a bike.  " + ARROW + "  proud",
                     [pics(a, "Part A – I am proud"), pics(b, "Part B – Family celebrations")])
    a = [PIC(rng, f"Which face is {FEELW[f]}?", f, FEEL) for f in take(FEEL, 3, v, "p7d5a")]
    b = [PIC(rng, q, k, STRATP) for q, k in take(STRAT, 3, v, "p7d5b")]
    c_ = [PIC(rng, q, f, FEEL) for q, f in take(SCEN, 2, v, "p7d5c")]
    return sheet(7, 5, t, "Review day! Then draw your picture.", "Example: You get a gift.  " + ARROW + "  happy",
                 [pics(a + b + c_, "Feelings and ideas"), _draw(["Draw something you are proud of.", "Draw how you feel today."], v)])


# ============================================================== UNIT 8  Friends, fair play, leadership, communication
KIND_SAY = [("Which is a kind thing to say?", "say_goodgame"), ("Which is a kind thing to say?", "say_nicetry"), ("Which is a kind way to join in?", "say_play"),
            ("Which is a kind thing to say?", "say_thanks"), ("Which says sorry?", "say_sorry"), ("Which is a kind way to say hi?", "say_hello")]
BADSAY = {"say_cant", "say_go", "say_give"}
FAIRQ = [("Which shows taking turns?", "turns"), ("Which shows sharing?", "sharing"), ("Which shows including everyone?", "include"), ("Which shows a team?", "team"),
         ("Who helps a team?", "coach"), ("What does a coach use?", "whistle"), ("What do you use to listen?", "ear"), ("What do you use to tell how you feel?", "talk")]
FAIRP = ["turns", "sharing", "include", "team", "coach", "whistle", "ear", "talk"]


def U8(day, rng, v):
    t = "Friends, Fair Play & Leadership"
    if day == 1:
        a = []
        for q, good in take(KIND_SAY * 2, 10, v, "p8d1"):
            a.append(PICF(rng, q, good, [good] + rng.sample(sorted(BADSAY), 2)))
        return sheet(8, 1, t, "Good communication and kind words help us make friends.", "Example: Which is a kind thing to say?  " + ARROW + "  “Good game!”", [pics(a, "Kind words")])
    if day == 2:
        a = [PIC(rng, q, k, FAIRP) for q, k in take(FAIRQ, 10, v, "p8d2")]
        return sheet(8, 2, t, "Fair play means taking turns, sharing, listening and including everyone.", "Example: Which shows taking turns?  " + ARROW + "  the 1 and 2 picture", [pics(a, "Fair play")])
    if day == 3:
        a = [PIC(rng, q, k, FAIRP) for q, k in take([("Who helps a team?", "coach"), ("What does a coach use?", "whistle"), ("Which shows a team?", "team"), ("Which shows including everyone?", "include")] * 2, 8, v, "p8d3")]
        return sheet(8, 3, t, "Leaders help others play safely and fairly. Everyone can be a leader.", "Example: Who helps a team?  " + ARROW + "  coach", [pics(a, "Leaders and teams")])
    if day == 4:
        a = []
        for _ in range(6):
            n = rng.randint(2, 5)
            k = rng.choice([2, 3])
            a.append(((rng.choice(["girl", "boy"]), n, f"Each kid gets {k} turns. How many turns in all?  ____"), n * k))
        sh = []
        for _ in range(4):
            f = rng.choice([2, 3, 4])
            n = f * rng.randint(2, 3)
            sh.append((("ball", n, f"Share with {f} friends. Each gets ____"), n // f))
        return sheet(8, 4, t, "Take turns and share fairly so everyone can play.", "Example: 3 kids, 2 turns each  " + ARROW + "  6 turns",
                     [sec("Part A – Fair turns", "count", a, 2, 62), sec("Part B – Share fairly", "count", sh, 2, 62)])
    a = [PICF(rng, q, good, [good] + rng.sample(sorted(BADSAY), 2)) for q, good in take(KIND_SAY, 3, v, "p8d5a")]
    b = [PIC(rng, q, k, FAIRP) for q, k in take(FAIRQ, 4, v, "p8d5b")]
    return sheet(8, 5, t, "Review day! Then draw your picture.", "Example: Which shows sharing?  " + ARROW + "  the sharing picture",
                 [pics(a + b, "Fair play and kindness"), _draw(["Draw you and a friend playing fair.", "Draw a kind thing you did."], v)])


# ============================================================== UNIT 9  Safety strategies, support, substances
TRUST_Q = [("Who is a trusted adult you can ask?", ["mom", "ball", "kite"], "mom"), ("Who is a trusted adult you can ask?", ["game", "teacher", "candy"], "teacher"),
           ("Who is a trusted adult you can ask?", ["dad", "kite", "ball"], "dad"), ("Who is a trusted adult you can ask?", ["candy", "grandma", "game"], "grandma"),
           ("Who can you ask about health at school?", ["teacher", "ball", "kite"], "teacher"), ("Who can check if you are healthy?", ["doctor", "ball", "game"], "doctor"),
           ("Who can you tell if something feels unsafe?", ["mom", "kite", "candy"], "mom"), ("Who can you tell at school?", ["game", "teacher", "ball"], "teacher")]
STRONG = [("Which is a strong voice for an unsafe moment?", "say_stop", ["say_stop", "say_hello", "say_goodgame"]), ("What can you say if you feel unsafe?", "say_no", ["say_no", "say_thanks", "say_hello"]),
          ("What can you say if something feels wrong?", "say_dontlike", ["say_dontlike", "say_thanks", "say_goodgame"]), ("Which is a strong “stop” voice?", "say_stop", ["say_stop", "say_sorry", "say_hello"]),
          ("What can you say if someone makes you uncomfortable?", "say_no", ["say_no", "say_hello", "say_nicetry"]), ("What do you use to call for help?", "phone", ["phone", "ball", "kite"])]
PRIVATE = [("house", "keep private", "Your home address?"), ("phone", "keep private", "Your phone number?"), ("computer", "keep private", "Your password?"),
           ("crayon", "OK to share", "Your favourite colour?"), ("ball", "OK to share", "Your favourite game?"), ("apple", "OK to share", "Your favourite fruit?")]
MEDQ = [("Who can give you medicine?", "mom", ["mom", "ball", "kite"]), ("Which should only a trusted adult give you?", "medicine", ["medicine", "apple", "milk"]),
        ("Which should you never taste or drink?", "cleaner", ["cleaner", "water", "milk"]), ("Who can help with medicine?", "doctor", ["doctor", "ball", "game"]),
        ("What do you do if you find medicine?", "dad", ["dad", "tag", "kite"]), ("Which is not for drinking?", "cleaner", ["cleaner", "juice", "milk"])]
GEARQ = [("What do you wear on a bike?", "helmet", ["helmet", "sunhat", "mittens"]), ("What do you wear in a boat?", "lifejacket", ["lifejacket", "helmet", "toque"]),
         ("What do you wear in the sun?", "sunhat", ["sunhat", "toque", "mittens"]), ("Where do you cross the street?", "crosswalk", ["crosswalk", "stop", "bin_trash"]),
         ("What tells cars to stop?", "stop", ["stop", "crosswalk", "helmet"]), ("What do you put on your skin in the sun?", "sunscreen", ["sunscreen", "toque", "snowboots"]),
         ("What do you wear in the snow?", "toque", ["toque", "sunhat", "lifejacket"]), ("What keeps your hands warm?", "mittens", ["mittens", "sunhat", "helmet"])]


def U9(day, rng, v):
    t = "Staying Safe & Getting Help"
    if day == 1:
        a = [PICF(rng, q, c, o) for q, o, c in take(TRUST_Q * 2, 10, v, "p9d1a")]
        b = [WORD(rng, k, LBL[k], lw(ADULTS), "Who is this trusted adult?") for k in take(ADULTS * 2, 4, v, "p9d1b")]
        return sheet(9, 1, t, "Trusted adults can help with health questions and when you feel unsafe.", "Example: Who is a trusted adult you can ask?  " + ARROW + "  mom",
                     [pics(a, "Part A – Who can help?"), words(b, "Part B – Name the helper")])
    if day == 2:
        a = [PICF(rng, q, c, o) for q, c, o in take(STRONG * 2, 8, v, "p9d2a")]
        b = [WORDF(rng, k, ans, ["keep private", "OK to share"], q) for k, ans, q in take(PRIVATE, 6, v, "p9d2b")]
        return sheet(9, 2, t, "If something feels unsafe: use a strong voice, get away if you can, and tell a trusted adult. Keep private information private.",
                     "Example: Your home address?  " + ARROW + "  keep private", [pics(a, "Part A – Strong voice"), words(b, "Part B – Private or OK to share?")])
    if day == 3:
        a = [PICF(rng, q, c, o) for q, c, o in take(MEDQ * 2, 8, v, "p9d3a")]
        b = [WORDF(rng, k, ans, ["ask a trusted adult", "never taste it", "OK to take myself"], "What should you do?") for k, ans in
             take([("medicine", "ask a trusted adult"), ("cleaner", "never taste it"), ("medicine", "ask a trusted adult"), ("cleaner", "never taste it")], 4, v, "p9d3b")]
        return sheet(9, 3, t, "Medicine and cleaning sprays can be harmful if used the wrong way. Always ask a trusted adult.", "Example: Which should only a trusted adult give you?  " + ARROW + "  medicine",
                     [pics(a, "Part A – Medicine and cleaners"), words(b, "Part B – What should you do?")])
    if day == 4:
        a = [PICF(rng, q, c, o) for q, c, o in take(GEARQ, 8, v, "p9d4")]
        return sheet(9, 4, t, "Stay safe while you play, in every season.", "Example: What do you wear on a bike?  " + ARROW + "  helmet", [pics(a, "Safe play")])
    a = [PICF(rng, q, c, o) for q, o, c in take(TRUST_Q, 3, v, "p9d5a")]
    b = [PICF(rng, q, c, o) for q, c, o in take(STRONG, 2, v, "p9d5b")]
    c_ = [PICF(rng, q, c, o) for q, c, o in take(MEDQ, 2, v, "p9d5c")]
    d_ = [PICF(rng, q, c, o) for q, c, o in take(GEARQ, 1, v, "p9d5d")]
    return sheet(9, 5, t, "Review day! Then draw your picture.", "Example: Who can you tell if something feels unsafe?  " + ARROW + "  a trusted adult",
                 [pics(a + b + c_ + d_, "Staying safe"), _draw(["Draw a trusted adult who helps you.", "Draw how you stay safe."], v)])


# ============================================================== UNIT 10  Components of healthy living
def odd_items(rng, n, big=True):
    groups = {"on the spot": NONLOC, "travelling moves": LOCO, "ball skills": MANIP, "everyday foods": ["apple", "carrot", "broccoli", "banana", "bread", "egg"],
              "sometimes foods": SOMETIMES, "clean-up things": ["soap", "towel", "tap", "toothbrush"], "feelings": ["happy", "sad", "angry", "proud", "worried"],
              "trusted adults": ["mom", "dad", "teacher", "doctor", "grandma"]}
    out = []
    for _ in range(n):
        g1, g2 = rng.sample(list(groups), 2)
        three = rng.sample(groups[g1], 3)
        o = rng.choice(groups[g2])
        opts = three + [o]
        rng.shuffle(opts)
        out.append((("Which one does not belong?", opts), "ABCD"[opts.index(o)]))
    return out


def U10(day, rng, v):
    t = "Healthy Living Together: Review & Challenge"
    if day == 1:
        a = [PICF(rng, "What is a good warm-up?", "stretch", ["stretch", "sit_tv", "sleep"]), PICF(rng, "What is a good cool-down?", "walk", ["walk", "run", "skiprope"]),
             PICF(rng, "What do you drink after play?", "water", ["water", "juice", "candy"]), PICF(rng, "What do you wear on a bike?", "helmet", ["helmet", "sunhat", "mittens"]),
             PICF(rng, "What helps you rest?", "bed", ["bed", "run", "kite"]), PICF(rng, "Which number feels very hot?", "exert5", ["exert1", "exert3", "exert5"])]
        pat = [pattern_item(rng, SKILLS14) for _ in range(4)]
        return sheet(10, 1, t, "A healthy day: move, eat well, rest, stay clean, feel good, stay safe.", "Example: warm up, play, cool down  " + ARROW + "  stretch, run, walk",
                     [pics(a, "Part A – A healthy day"), sec("Part B – What comes next?", "picp", pat, 2, 126)])
    if day == 2:
        keys = ["run", "swim", "bike", "dance", "skiprope", "jump"]
        spec = make_graph(rng, keys, 3)
        it = spec["items"]
        top = max(it, key=lambda x: x[1])
        low = min(it, key=lambda x: x[1])
        qs = [(f"Which was done on the most days?  ({' / '.join(rng.sample([LBL[k] for k, _ in it], 3))})", LBL[top[0]]),
              (f"Which was done on the fewest days?  ({' / '.join(rng.sample([LBL[k] for k, _ in it], 3))})", LBL[low[0]])]
        for k, n in it:
            qs.append((f"On how many days did we do {LBL[k]}?  ____", n))
        qs.append((f"How many more days {LBL[it[0][0]]} than {LBL[it[1][0]]}?  ____ (0 if fewer)", max(it[0][1] - it[1][1], 0)))
        qs.append(("How many active days in all?  ____", sum(n for _, n in it)))
        return sheet(10, 2, t, "Our class counted active days. Read the graph.", "Example: The tallest bar has the most days.",
                     [sec("Active days this week", "diagram", [(spec, None)], 1, 176), eqs([(q, str(a_)) for q, a_ in qs], "Questions")])
    if day == 3:
        items = [(k, "everyday") for k in take(EVERY, 2, v, "p10d3a")] + [(k, "sometimes") for k in take(SOMETIMES, 2, v, "p10d3b")]
        a = [WORDF(rng, k, ans, ["everyday", "sometimes"], "Everyday or sometimes?") for k, ans in items]
        b = [PIC(rng, q, k, HYGP) for q, k in take(HYG, 2, v, "p10d3c")]
        c_ = [PIC(rng, q, f, FEEL) for q, f in take(SCEN, 2, v, "p10d3d")]
        d_ = [PICF(rng, q, c, o) for q, o, c in take(TRUST_Q, 2, v, "p10d3e")]
        e_ = [PICF(rng, q, c, o) for q, c, o in take(GEARQ, 2, v, "p10d3f")]
        return sheet(10, 3, t, "Mixed review of healthy living.", "Example: Which is a healthy snack?  " + ARROW + "  apple",
                     [words(a, "Food"), pics(b + c_ + d_ + e_, "Habits, feelings and safety")])
    if day == 4:
        return sheet(10, 4, t, "Find the one that does not belong.", "Example: run, hop, jump, apple  " + ARROW + "  apple does not belong", [pics(odd_items(rng, 8), "Odd one out")])
    a = [PICF(rng, q, c, o) for q, c, o in take(GEARQ, 2, v, "p10d5a")]
    b = [PIC(rng, q, k, HYGP) for q, k in take(HYG, 2, v, "p10d5b")]
    pat = [pattern_item(rng, SKILLS14) for _ in range(2)]
    return sheet(10, 5, t, "Challenge day! Odd one out, patterns, and a drawing.", "Example: What comes next?  " + ARROW + "  follow the pattern",
                 [pics(a + b + odd_items(rng, 2), "Healthy living"), sec("What comes next?", "picp", pat, 2, 126),
                  _draw(["Draw your healthy, active day.", "Draw how you will stay healthy."], v)])


UNITS = {1: U1, 2: U2, 3: U3, 4: U4, 5: U5, 6: U6, 7: U7, 8: U8, 9: U9, 10: U10}


def unit_sheets(u, variant=0):
    return [fit(UNITS[u](d, random.Random(u * 100 + d + variant * 1000), variant)) for d in range(1, 6)]


def checkup_a():
    rng = random.Random(4555)
    s = [pics([PIC(rng, "What do you use to see?", "eye", BODYP), PIC(rng, "Which one is twisting?", "twist", SKILLS14), PIC(rng, "Which one is rolling?", "roll", SKILLS14),
               PICF(rng, "Which makes your heart beat fastest?", "run", ["run", "sleep", "sit_tv"])], "Body and moves"),
         words([WORDF(rng, "catch", "with a ball", KINDW, "Which kind of move?"), WORDF(rng, "balance", "on the spot", KINDW, "Which kind of move?"),
                WORDF(rng, "gallop", "travelling", KINDW, "Which kind of move?"), WORDF(rng, "dance", "rhythm", ATYPEW, "Which kind of activity?"),
                WORDF(rng, "tag", "game with rules", ATYPEW, "Which kind of activity?")], "Moves and activities"),
         pics([PICF(rng, "Which shows sweating?", "sweat", ["sweat", "sleep", "happy"]), PICF(rng, "Which number feels very hot?", "exert5", ["exert1", "exert3", "exert5"]),
               PICF(rng, "Which drink is best every day?", "water", ["water", "juice", "cake"]), PICF(rng, "Which is a fruit or vegetable?", "carrot", ["carrot", "bread", "candy"])], "Body and food"),
         words([WORDF(rng, "apple", "everyday", ["everyday", "sometimes"], "Everyday or sometimes?"), WORDF(rng, "candy", "sometimes", ["everyday", "sometimes"], "Everyday or sometimes?"),
                WORDF(rng, "skiprope", "alone or with a partner", ATYPEW, "Which kind of activity?")], "Food and activity")]
    return sheet(0, "A", "Check-Up: Units 1–5", "Show what you know! Do your best on every question.", "Aim for 90% or more before moving on to Unit 6.", s)


def final_test():
    rng = random.Random(4999)
    s = [pics([PIC(rng, "What do you use to wash your hands?", "soap", HYGP), PICF(rng, "What do you do when you cough?", "cough", ["cough", "ball", "kite"]),
               PICF(rng, "Where do you stay when you are sick?", "house", ["house", "park", "playground"]), PICF(rng, "Which face is sad?", "sad", ["happy", "sad", "angry"])], "Healthy habits and feelings"),
         pics([PIC(rng, "What helps when you feel angry?", "lungs", STRATP), PICF(rng, "Which is a kind thing to say?", "say_goodgame", ["say_goodgame", "say_cant", "say_go"]),
               PIC(rng, "Which shows taking turns?", "turns", FAIRP), PIC(rng, "Who helps a team?", "coach", FAIRP)], "Calm, kind and fair"),
         pics([PICF(rng, "Which is a strong voice for an unsafe moment?", "say_stop", ["say_stop", "say_hello", "say_goodgame"]), PICF(rng, "Who is a trusted adult you can ask?", "teacher", ["game", "teacher", "candy"]),
               PICF(rng, "Which should only a trusted adult give you?", "medicine", ["medicine", "apple", "milk"]), PICF(rng, "What do you wear on a bike?", "helmet", ["helmet", "sunhat", "mittens"])], "Staying safe"),
         words([WORDF(rng, "carrot", "fruit or vegetable", ["fruit or vegetable", "grain", "protein"], "Which group?"), WORDF(rng, "bread", "grain", ["fruit or vegetable", "grain", "protein"], "Which group?"),
                WORDF(rng, "egg", "protein", ["fruit or vegetable", "grain", "protein"], "Which group?"), WORDF(rng, "playground", "at school", OPPW, "Where can you be active?")], "Food and activity"),
         sec("What comes next?", "picp", [pattern_item(rng, SKILLS14) for _ in range(2)], 2, 126)]
    return sheet(0, "F", "Final Test: Units 1–10", "You made it! Show everything you have learned.", "Aim for 90% or more. Then it's certificate time!", s)
