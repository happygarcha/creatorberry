"""Problem generators for the Grade 2 Science Mastery Workbook (same sheet format as the others)."""
import math
import random
from english_generators import take, passage_sec, qlines, fit, ARROW
from generators import sec, sheet, uniq

# ------------------------------------------------------------------ helpers
def indef(x):
    return ("an " if x[0] in "aeiou" else "a ") + x


def Indef(x):
    t = indef(x)
    return t[0].upper() + t[1:]


def _longfix(sh):
    """very long one-column lines wrap instead of shrinking: show them as written-answer lines"""
    for sc in sh["sections"]:
        if sc["kind"] == "eq" and sc["cols"] == 1 and max(len(c[0]) for c in sc["cells"]) > 92:
            sc["kind"] = "qline"
            sc["h"] = max(sc["h"], 46)
    return sh


def _opts(rng, good, wrongs, k=2):
    ws = [w for w in wrongs if w != good]
    o = [good] + rng.sample(ws, min(k, len(ws)))
    rng.shuffle(o)
    return o


def mc(rng, q, good, wrongs, k=2):
    o = " / ".join(_opts(rng, good, wrongs, k))
    return (f"{q}  ({o})" if "____" in q else f"{q}  ({o})  ____"), good


def tf(stmt, truth):
    return f"{stmt}  True or false?  ____", "true" if truth else "false"


def mcs(rng, bank, n, v, key):
    return [mc(rng, q, g, w) for q, g, w in take(bank, n, v, key)]


def tfs(bank, n, v, key):
    return [tf(s, t) for s, t in take(bank, n, v, key)]


def order_item(rng, title, steps):
    idx = list(range(len(steps)))
    sh = idx[:]
    for _ in range(30):
        rng.shuffle(sh)
        if sh != idx:
            break
    letters = "ABCDEFG"
    shown = "   ".join(f"{letters[k]}. {steps[i]}" for k, i in enumerate(sh))
    ans = ", ".join(letters[sh.index(i)] for i in idx)
    blanks = " , ".join(["____"] * len(steps))
    return f"{title}   {shown}   Put in order:  {blanks}", ans


NOTE = ("Write what you learned or draw a picture.", "Answers vary. Check: accurate science idea, complete sentence.")


def notebook(n=1, h=70):
    return sec("My science notebook", "write", [("Write one new thing you learned today. Add a picture if you like.",
                                               "Answers vary. Check: accurate science idea in a complete sentence.")] * n, 1, h)


# ============================================================== UNIT 1
ORGANS = ["eyes", "ears", "nose", "tongue", "skin"]
SENSE_ACT = [("see a rainbow", "eyes"), ("hear a bell", "ears"), ("smell a flower", "nose"), ("taste a lemon", "tongue"),
             ("feel a soft blanket", "skin"), ("hear a dog bark", "ears"), ("see a bird in a tree", "eyes"),
             ("smell fresh bread", "nose"), ("taste ice cream", "tongue"), ("feel hot sand", "skin"),
             ("hear music", "ears"), ("see the stars", "eyes"), ("smell smoke", "nose"), ("feel cold water", "skin"),
             ("taste salty chips", "tongue"), ("hear thunder", "ears")]
DESC = [("A lemon tastes ____.", "sour", ["loud", "soft"]), ("Sugar tastes ____.", "sweet", ["rough", "quiet"]),
        ("Ice feels ____.", "cold", ["sour", "loud"]), ("Sandpaper feels ____.", "rough", ["sweet", "quiet"]),
        ("A feather feels ____.", "soft", ["sour", "loud"]), ("A drum sounds ____.", "loud", ["sweet", "sticky"]),
        ("A whisper sounds ____.", "quiet", ["sour", "rough"]), ("A rock feels ____.", "hard", ["sweet", "loud"]),
        ("Honey feels ____.", "sticky", ["quiet", "sour"]), ("A fire feels ____.", "hot", ["quiet", "sweet"]),
        ("A mirror looks ____.", "shiny", ["sour", "loud"]), ("A pillow feels ____.", "soft", ["sour", "loud"])]
TOOLS = [("how long a pencil is", "ruler"), ("how hot or cold the air is", "thermometer"),
         ("how heavy an apple is", "balance scale"), ("how much juice is in a jug", "measuring cup"),
         ("the tiny parts of a leaf", "magnifying glass"), ("how long a race takes", "stopwatch"),
         ("how wide a book is", "ruler"), ("how warm your soup is", "thermometer"),
         ("how much a bag of rice weighs", "balance scale"), ("how much water fits in a bottle", "measuring cup"),
         ("a tiny bug's legs", "magnifying glass"), ("how long it takes to run 10 steps", "stopwatch")]
TOOLNAMES = ["ruler", "thermometer", "balance scale", "measuring cup", "magnifying glass", "stopwatch"]
OBS = [("The leaf is green.", True), ("This is the prettiest leaf.", False), ("The rock feels rough.", True),
       ("Rocks are boring.", False), ("The water is 5 degrees.", True), ("Rain is the worst weather.", False),
       ("The ball is round.", True), ("Soccer is the best sport.", False), ("The cup holds 200 mL.", True),
       ("Snow is cold and white.", True), ("Broccoli tastes yucky.", False), ("The box weighs 2 kilograms.", True),
       ("Spiders are scary.", False), ("The plant grew 3 cm.", True), ("Blue is the nicest color.", False),
       ("The ice cube melted in 10 minutes.", True), ("Dogs are better than cats.", False), ("The feather is soft.", True)]
TESTQ = [("Which paper towel soaks up more water?", True), ("What is the best color?", False),
         ("Do plants grow taller in sun or in shade?", True), ("Is pizza yummy?", False),
         ("Does a heavier ball roll farther?", True), ("Which pet is the cutest?", False),
         ("Does ice melt faster in the sun or in the shade?", True), ("Is summer better than winter?", False),
         ("Does sugar dissolve faster in warm water or cold water?", True), ("Which song is the nicest?", False)]
STEPSETS = [("Steps of an investigation.", ["Ask a question", "Make a prediction", "Do the test", "Record what you see"]),
            ("How to use a magnifying glass.", ["Hold the object", "Bring the glass close to it", "Move the glass back until it is clear", "Draw what you see"]),
            ("Measuring with a ruler.", ["Line the object up at 0", "Look at the end of the object", "Read the number", "Write the length with its unit"]),
            ("Sharing your results.", ["Collect your data", "Make a chart", "Say what you found", "Ask what others found"])]
FAIR = [("To test which ball bounces higher, what must stay the same?", "the height you drop it from",
         ["the color of the ball", "the day of the week"]),
        ("To test if plants grow better in sun, what must stay the same?", "the amount of water",
         ["the place of the pot", "the plant's name"]),
        ("To test which paper towel soaks up more, what must stay the same?", "the amount of water poured",
         ["the brand of towel", "the color of the cup"]),
        ("To test how far a toy car rolls, what must stay the same?", "the ramp height",
         ["the car's color", "the time of day"]),
        ("In a fair test, how many things do we change?", "one", ["all of them", "none"]),
        ("After a test, we ____ what we found.", "record", ["forget", "hide"])]
SAFETY = [("Taste things from the science table.", False), ("Tell the teacher if something spills.", True),
          ("Wash your hands after an experiment.", True), ("Run around the room with scissors.", False),
          ("Wear goggles when your teacher says to.", True), ("Put unknown things in your mouth.", False),
          ("Follow the directions carefully.", True), ("Smell chemicals by putting your nose right on them.", False),
          ("Clean up your work area when you finish.", True), ("Touch a hot plate to see if it is hot.", False)]


def U1(day, rng, v):
    t = "Being a Scientist: Senses & Tools"
    if day == 1:
        a = [mc(rng, f"You {x} with your ____.", y, ORGANS, 2) for x, y in take(SENSE_ACT, 12, v, "s1d1a")]
        b = [mc(rng, q, g, w) for q, g, w in take(DESC, 8, v, "s1d1b")]
        return sheet(1, 1, t, "Scientists use their senses to observe. Choose the best word.",
                     "Example: You hear a bell with your ____ (ears / eyes / nose)  " + ARROW + "  ears",
                     [sec("Part A – Which sense?", "eq", a, 1, 30), sec("Part B – Describing words", "eq", b, 1, 30)])
    if day == 2:
        a = [mc(rng, f"Which tool measures {x}?", y, TOOLNAMES, 2) for x, y in take(TOOLS, 8, v, "s1d2a")]
        b = []
        for _ in range(6):
            p, q = rng.randint(10, 20), rng.randint(3, 9)
            b.append((f"A pencil is {p} cm long. A crayon is {q} cm long. How much longer is the pencil?  ____ cm", p - q))
        return sheet(1, 2, t, "Use the right tool to measure. Then solve the measuring problems.",
                     "Example: Which tool measures how long a pencil is? (ruler / clock)  " + ARROW + "  ruler",
                     [sec("Part A – Choose the tool", "eq", a, 1, 30), sec("Part B – Measuring problems", "eq", b, 1, 30)])
    if day == 3:
        a = [(f"{s}  Observation or opinion?  ____", "observation" if t_ else "opinion") for s, t_ in take(OBS, 12, v, "s1d3a")]
        b = [(f"{s}  Can you test this?  ____", "yes" if t_ else "no") for s, t_ in take(TESTQ, 6, v, "s1d3b")]
        return sheet(1, 3, t, "An observation is what you see, hear, smell, taste or feel. An opinion is what you think.",
                     "Example: The leaf is green.  " + ARROW + "  observation      Rocks are boring.  " + ARROW + "  opinion",
                     [sec("Part A – Observation or opinion?", "eq", a, 1, 30), sec("Part B – Can it be tested?", "eq", b, 1, 30)])
    if day == 4:
        o = [order_item(rng, ttl, st) for ttl, st in take(STEPSETS, 4, v, "s1d4a")]
        data = []
        for _ in range(4):
            a_, b_ = rng.randint(6, 12), rng.randint(3, 9)
            data.append((f"In a test, {a_} objects floated and {b_} objects sank. How many objects were tested?", a_ + b_))
        f = mcs(rng, FAIR, 4, v, "s1d4c")
        return sheet(1, 4, t, "Put the steps in order. Read the data. Think about fair tests.",
                     "Example: Ask a question, make a prediction, do the test, record what you see.",
                     [sec("Part A – Put the steps in order", "qline", o, 1, 70), sec("Part B – Read the data", "qline", data, 1, 44),
                      sec("Part C – Fair tests", "eq", f, 1, 30)])
    pas = [("Mia's Magnifier", "Mia looked at a leaf with a magnifying glass. She saw tiny lines called veins. She counted five big veins and "
            "drew them in her notebook. Then she measured the leaf with a ruler. It was 8 cm long.",
            [("What tool did Mia use to look closely?", "a magnifying glass"), ("What did she draw in her notebook?", "the veins"),
             ("How long was the leaf?", "8 cm")]),
           ("Testing Paper Planes", "Leo made two paper planes. One was big and one was small. He threw each plane three times and counted "
            "how many steps it flew. The small plane flew 6 steps. The big plane flew 4 steps.",
            [("How many paper planes did Leo make?", "two"), ("Which plane flew farther?", "the small plane"),
             ("What did Leo do three times?", "He threw each plane.")])][v]
    s_ = take(SAFETY, 6, v, "s1d5s")
    return sheet(1, 5, t, "Review day! Read the investigation. Then answer the questions about safety and tools.",
                 "Example: Wash your hands after an experiment.  " + ARROW + "  true",
                 [passage_sec(pas[0], pas[1]), qlines(pas[2], 44),
                  sec("Safety first", "eq", [tf(s, x) for s, x in s_], 1, 30),
                  sec("Which tool?", "eq", [mc(rng, f"Which tool measures {x}?", y, TOOLNAMES) for x, y in take(TOOLS, 3, v, "s1d5t")], 1, 30)])


# ============================================================== UNIT 2
LIVE = ["dog", "tree", "bird", "flower", "fish", "ant", "grass", "frog", "cat", "worm", "bee", "horse", "spider", "mouse", "cactus", "rose bush"]
NON = ["rock", "chair", "ball", "water", "car", "cloud", "book", "sand", "shoe", "toy", "pencil", "spoon", "wagon", "blanket", "window", "bicycle"]
NEEDS_MC = [("All living things need ____ to stay alive.", "water", ["candy", "toys"]),
            ("Animals need ____ for energy.", "food", ["paint", "music"]), ("Animals need ____ to breathe.", "air", ["sand", "rocks"]),
            ("Plants need ____ to make their food.", "sunlight", ["noise", "wind chimes"]),
            ("Plants take in water through their ____.", "roots", ["leaves", "flowers"]),
            ("A home where an animal lives is called a ____.", "habitat", ["hobby", "hat"]),
            ("Living things grow and ____.", "change", ["rust", "melt"]),
            ("A bird builds a nest for shelter and to ____.", "raise babies", ["do homework", "play games"]),
            ("Living things need space to ____.", "grow", ["freeze", "rust"]),
            ("People need food, water, air and ____.", "shelter", ["candy", "television"]),
            ("A fish takes what it needs from the ____.", "water", ["sand", "grass"]),
            ("Living things can have ____.", "babies", ["rust", "puddles"])]
NEEDS_TF = [("A rock needs food to grow.", False), ("Plants need sunlight.", True), ("A chair is a living thing.", False),
            ("All animals need water.", True), ("Plants can live without water.", False), ("A tree is alive.", True),
            ("A toy needs air to live.", False), ("Animals can live without air.", False), ("Living things grow.", True),
            ("Nonliving things can have babies.", False), ("A flower is a living thing.", True), ("Clouds are alive.", False)]
PARTS = [("roots", "takes in water from the soil"), ("stem", "holds the plant up and carries water"),
         ("leaves", "makes food using sunlight"), ("flower", "makes seeds"), ("seed", "can grow into a new plant"),
         ("fruit", "holds the seeds")]
PLANT_Q = [("Which letter shows the roots?", "D"), ("Which letter shows the stem?", "C"), ("Which letter shows the leaves?", "B"),
           ("Which letter shows the flower?", "A"), ("Which letter shows the part that takes in water from the soil?", "D"),
           ("Which letter shows the part that holds the plant up?", "C"), ("Which letter shows the part that makes food using sunlight?", "B"),
           ("Which letter shows the part that makes seeds?", "A")]
EAT = [("carrot", "root"), ("celery", "stem"), ("lettuce", "leaves"), ("broccoli", "flower"), ("apple", "fruit"),
       ("spinach", "leaves"), ("beet", "root"), ("cauliflower", "flower"), ("tomato", "fruit"), ("pea", "seed"),
       ("radish", "root"), ("asparagus", "stem"), ("cabbage", "leaves"), ("strawberry", "fruit"), ("corn kernel", "seed"),
       ("sunflower seed", "seed")]
PARTNAMES = ["root", "stem", "leaves", "flower", "fruit", "seed"]
GROW = [("apple seed", "apple tree"), ("acorn", "oak tree"), ("sunflower seed", "sunflower"), ("bean seed", "bean plant"),
        ("pumpkin seed", "pumpkin plant"), ("Douglas-fir seed", "Douglas-fir tree"), ("cedar seed", "cedar tree"),
        ("corn seed", "corn plant"), ("pea seed", "pea plant"), ("maple seed", "maple tree")]


def U2(day, rng, v):
    t = "Living Things & Plants"
    if day == 1:
        L = [(f"Is a {x} living or non-living?  ____", "living") for x in take(LIVE, 8, v, "s2d1a")]
        N = [(f"Is a {x} living or non-living?  ____", "non-living") for x in take(NON, 8, v, "s2d1b")]
        c = L + N
        rng.shuffle(c)
        return sheet(2, 1, t, "Living things grow, need food/water/air, and have babies. Non-living things do not.",
                     "Example: A tree is living. A rock is non-living.", [sec("", "eq", c, 2, 30)])
    if day == 2:
        a = mcs(rng, NEEDS_MC, 10, v, "s2d2a")
        b = tfs(NEEDS_TF, 8, v, "s2d2b")
        return sheet(2, 2, t, "Living things have needs. Choose the best word and decide true or false.",
                     "Example: Animals need ____ for energy. (food / paint)  " + ARROW + "  food",
                     [sec("Part A – What do living things need?", "eq", a, 1, 30), sec("Part B – True or false?", "eq", b, 1, 30)])
    if day == 3:
        a = [mc(rng, f"Which part of a plant {j}?", p, [x[0] for x in PARTS if x[0] != p], 2) for p, j in take(PARTS, 6, v, "s2d3a")]
        d = [(f"{q}  ____", ans) for q, ans in take(PLANT_Q, 6, v, "s2d3b")]
        return sheet(2, 3, t, "Learn the parts of a plant and what each part does.",
                     "Example: Which part of a plant makes seeds?  " + ARROW + "  flower",
                     [sec("Part A – Plant part jobs", "eq", a, 1, 30), sec("Look at the plant", "diagram", [("plant", None)], 1, 170),
                      sec("Part B – Use the picture", "eq", d, 1, 30)])
    if day == 4:
        a = [mc(rng, f"When we eat a {x}, we eat the ____ of the plant.", y, PARTNAMES, 2) for x, y in take(EAT, 8, v, "s2d4a")]
        g = [mc(rng, f"An {x} grows into a ____." if x[0] in "aeiou" else f"A {x} grows into a ____.", y, [z for _, z in GROW], 2)
             for x, y in take(GROW, 6, v, "s2d4b")]
        n_ = [mc(rng, "Plants need sunlight, air, soil and ____ to grow.", "water", ["candy", "toys"]),
              mc(rng, "Which would a plant NOT need to grow?", "soda", ["sunlight", "water"]),
              mc(rng, "A seed needs water and warmth to ____.", "sprout", ["freeze", "melt"])]
        return sheet(2, 4, t, "Plants give us food. Seeds grow into new plants.", "Example: We eat the ____ of a carrot. (root / fruit)  " + ARROW + "  root",
                     [sec("Part A – Which plant part do we eat?", "eq", a, 1, 30), sec("Part B – What does it grow into?", "eq", g, 1, 30),
                      sec("Part C – What do plants need?", "eq", n_, 1, 30)])
    pas = [("How a Seed Grows", "A seed needs water and warmth to wake up. First, a tiny root grows down into the soil. Then a shoot grows up toward "
            "the light. Leaves open and make food from sunlight. Soon the plant can make flowers and new seeds.",
            [("What does a seed need to wake up?", "water and warmth"), ("What grows down into the soil first?", "a tiny root"),
             ("What do leaves use to make food?", "sunlight")]),
           ("A Bean Plant Experiment", "Ava planted three bean seeds. She put one pot in the sun, one in a dark closet, and one by a window. "
            "She gave each pot the same water. After ten days, the plant in the closet was pale and weak. The plants in the light were tall and green.",
            [("What did Ava change?", "where the pots sat (the light)"), ("What stayed the same?", "the amount of water"),
             ("Which plant was pale and weak?", "the one in the closet"), ("What do plants need to grow well?", "light (sunlight)")])][v]
    r = [(f"Is a {x} living or non-living?  ____", "living") for x in take(LIVE, 3, v, "s2d5a")] + \
        [(f"Is a {x} living or non-living?  ____", "non-living") for x in take(NON, 3, v, "s2d5b")]
    rng.shuffle(r)
    return sheet(2, 5, t, "Review day! Read the investigation, then review living things and plants.",
                 "Example: A seed needs water and warmth to sprout.",
                 [passage_sec(pas[0], pas[1]), qlines(pas[2], 44), sec("Living or non-living?", "eq", r, 2, 30),
                  sec("Plant parts", "eq", [mc(rng, f"Which part of a plant {j}?", p, [x[0] for x in PARTS if x[0] != p]) for p, j in take(PARTS, 3, v, "s2d5c")], 1, 30)])


# ============================================================== UNIT 3
CLASSES = ["mammal", "bird", "fish", "reptile", "amphibian", "insect"]
COVER = ["fur", "feathers", "scales", "moist skin", "a hard shell"]
ANIM = [("dog", "mammal", "fur", "land", None), ("cow", "mammal", "fur", "land", "herbivore"),
        ("horse", "mammal", "fur", "land", "herbivore"), ("rabbit", "mammal", "fur", "land", "herbivore"),
        ("lion", "mammal", "fur", "land", "carnivore"), ("bear", "mammal", "fur", "land", "omnivore"),
        ("deer", "mammal", "fur", "land", "herbivore"), ("whale", "mammal", None, "water", "carnivore"),
        ("dolphin", "mammal", None, "water", "carnivore"), ("seal", "mammal", "fur", "land and water", "carnivore"),
        ("pig", "mammal", None, "land", "omnivore"), ("raccoon", "mammal", "fur", "land", "omnivore"),
        ("eagle", "bird", "feathers", "land", "carnivore"), ("duck", "bird", "feathers", "land and water", "omnivore"),
        ("owl", "bird", "feathers", "land", "carnivore"), ("penguin", "bird", "feathers", "land and water", "carnivore"),
        ("crow", "bird", "feathers", "land", "omnivore"), ("robin", "bird", "feathers", "land", None),
        ("salmon", "fish", "scales", "water", "carnivore"), ("shark", "fish", "scales", "water", "carnivore"),
        ("goldfish", "fish", "scales", "water", None), ("trout", "fish", "scales", "water", None),
        ("snake", "reptile", "scales", "land", "carnivore"), ("lizard", "reptile", "scales", "land", None),
        ("crocodile", "reptile", "scales", "land and water", "carnivore"),
        ("frog", "amphibian", "moist skin", "land and water", "carnivore"), ("toad", "amphibian", "moist skin", "land", None),
        ("salamander", "amphibian", "moist skin", "land and water", None),
        ("butterfly", "insect", "a hard shell", "land", None), ("ant", "insect", "a hard shell", "land", None),
        ("bee", "insect", "a hard shell", "land", None), ("ladybug", "insect", "a hard shell", "land", "carnivore"),
        ("grasshopper", "insect", "a hard shell", "land", "herbivore"), ("beetle", "insect", "a hard shell", "land", None)]
ADAPT = [("A duck has webbed feet to help it ____.", "swim", ["fly", "sleep"]),
         ("A giraffe has a long neck to reach ____.", "high leaves", ["deep water", "the ground"]),
         ("A polar bear has thick fur to stay ____.", "warm", ["cool", "wet"]),
         ("A fish uses gills to breathe ____.", "underwater", ["in trees", "on rocks"]),
         ("Bats sleep in the day and hunt at ____.", "night", ["noon", "breakfast"]),
         ("A woodpecker has a strong beak to ____.", "peck wood", ["swim", "dig holes in sand"]),
         ("A frog has strong back legs to ____.", "jump", ["fly", "climb trees only"]),
         ("An owl has big eyes to see in the ____.", "dark", ["sun", "water"]),
         ("A skunk sprays a bad smell to ____.", "protect itself", ["find food", "build a nest"]),
         ("A chameleon changes color to ____.", "hide", ["swim", "sing"]),
         ("A turtle's shell ____.", "protects it", ["helps it fly", "makes it fast"]),
         ("A beaver's flat tail helps it ____.", "swim", ["fly", "sing"]),
         ("A cougar has sharp claws to help it ____.", "catch food", ["swim", "fly"]),
         ("Salmon swim up rivers to lay ____.", "eggs", ["seeds", "nuts"]),
         ("A bear sleeps in a den all winter. This is called ____.", "hibernation", ["migration", "swimming"]),
         ("Many birds fly to warmer places for winter. This is called ____.", "migration", ["hibernation", "hatching"])]


def U3(day, rng, v):
    t = "Animals & Their Habitats"
    if day == 1:
        c = [mc(rng, f"{Indef(a[0])} is a ____.", a[1], CLASSES, 2) for a in take(ANIM, 22, v, "s3d1")]
        return sheet(3, 1, t, "Animals belong to groups: mammal, bird, fish, reptile, amphibian, insect.",
                     "Example: A dog is a ____ (mammal / fish / insect)  " + ARROW + "  mammal", [sec("", "eq", c, 1, 30)])
    if day == 2:
        cov = [a for a in ANIM if a[2]]
        a = [mc(rng, f"{Indef(x[0])} is covered with ____.", x[2], COVER, 2) for x in take(cov, 12, v, "s3d2a")]
        b = []
        for cl in take(CLASSES, 8, v, "s3d2b"):
            good = rng.choice([x[0] for x in ANIM if x[1] == cl])
            wr = [x[0] for x in ANIM if x[1] != cl]
            b.append(mc(rng, f"Which of these is a {cl}?", good, wr, 2))
        return sheet(3, 2, t, "Each group has special body parts: fur, feathers, scales, moist skin, a hard shell.",
                     "Example: A robin is covered with ____ (feathers / scales)  " + ARROW + "  feathers",
                     [sec("Part A – Body coverings", "eq", a, 1, 30), sec("Part B – Which animal?", "eq", b, 1, 30)])
    if day == 3:
        H = ["land", "water", "land and water"]
        hab = [a for a in ANIM if a[3]]
        a = [mc(rng, f"Where does {indef(x[0])} live?", x[3], H, 2) for x in take(hab, 10, v, "s3d3a")]
        dt = [a for a in ANIM if a[4]]
        b = [mc(rng, f"{Indef(x[0])} is a ____.", x[4], ["herbivore", "carnivore", "omnivore"], 2) for x in take(dt, 8, v, "s3d3b")]
        c = [mc(rng, "Herbivores eat ____.", "only plants", ["only animals", "only rocks"]),
             mc(rng, "Carnivores eat ____.", "other animals", ["only plants", "only rocks"]),
             mc(rng, "Omnivores eat ____.", "plants and animals", ["only plants", "only air"])]
        return sheet(3, 3, t, "A habitat is where an animal lives. Herbivores eat plants, carnivores eat animals, omnivores eat both.",
                     "Example: Where does a whale live? (land / water)  " + ARROW + "  water",
                     [sec("Part A – Habitats", "eq", a, 1, 30), sec("Part B – What do they eat?", "eq", b, 1, 30),
                      sec("Part C – Word meanings", "eq", c, 1, 30)])
    if day == 4:
        return sheet(3, 4, t, "Animals have body parts and behaviours that help them survive (adaptations).",
                     "Example: A duck has webbed feet to help it ____ (swim / sleep)  " + ARROW + "  swim",
                     [sec("", "eq", mcs(rng, ADAPT, 16, v, "s3d4"), 1, 30)])
    pas = [("Pacific Salmon", "Pacific salmon are born in rivers. They swim out to the ocean, where they grow big. When they are adults, "
            "they swim back up the river to lay eggs. Bears, eagles and people eat salmon. Many First Peoples have depended on salmon for food for a very long time.",
            [("Where are salmon born?", "in rivers"), ("Where do salmon grow big?", "in the ocean"),
             ("What do adult salmon do when they come back to the river?", "They lay eggs."), ("Name one animal that eats salmon.", "bear or eagle (or people)")]),
           ("Orcas", "Orcas live in the ocean along the coast of British Columbia. They are mammals, not fish. Orcas breathe air through a blowhole "
            "on top of their heads. They live in family groups called pods. Some orcas eat fish, and others hunt seals.",
            [("Are orcas fish or mammals?", "mammals"), ("How do orcas breathe?", "through a blowhole"),
             ("What is a group of orcas called?", "a pod")])][v]
    c = [mc(rng, f"{Indef(a[0])} is a ____.", a[1], CLASSES, 2) for a in take(ANIM, 5, v, "s3d5a")]
    h = [mc(rng, f"Where does {indef(a[0])} live?", a[3], ["land", "water", "land and water"]) for a in take([x for x in ANIM if x[3]], 3, v, "s3d5b")]
    ad = mcs(rng, ADAPT, 2, v, "s3d5c")
    return sheet(3, 5, t, "Review day! Read about a BC animal, then review animal groups and habitats.",
                 "Example: A salmon is a ____ (fish / bird)  " + ARROW + "  fish",
                 [passage_sec(pas[0], pas[1]), qlines(pas[2], 44), sec("Animal groups", "eq", c, 1, 30),
                  sec("Habitats and adaptations", "eq", h + ad, 1, 30)])


# ============================================================== UNIT 4
CYC = {"butterfly": ["egg", "caterpillar", "chrysalis", "butterfly"], "frog": ["egg", "tadpole", "froglet", "frog"],
       "chicken": ["egg", "chick", "hen"], "plant": ["seed", "sprout", "young plant", "adult plant"],
       "ladybug": ["egg", "larva", "pupa", "ladybug"], "salmon": ["egg", "alevin", "fry", "adult salmon"],
       "human": ["baby", "child", "teenager", "adult"]}
BABY = [("dog", "puppy"), ("cat", "kitten"), ("cow", "calf"), ("horse", "foal"), ("sheep", "lamb"), ("duck", "duckling"),
        ("bear", "cub"), ("pig", "piglet"), ("deer", "fawn"), ("goat", "kid"), ("kangaroo", "joey"), ("lion", "cub")]
LIFE_MC = [("A caterpillar makes a ____ before it becomes a butterfly.", "chrysalis", ["nest", "web"]),
           ("A seed needs water and warmth to ____.", "sprout", ["freeze", "melt"]),
           ("Frogs lay their eggs in ____.", "water", ["trees", "sand"]),
           ("A tadpole breathes with ____ and lives in water.", "gills", ["wings", "horns"]),
           ("A hen lays ____.", "eggs", ["seeds", "pups"]),
           ("Pacific salmon return to the river to lay ____.", "eggs", ["seeds", "nuts"]),
           ("A baby salmon just out of the egg is called an ____.", "alevin", ["calf", "kitten"]),
           ("An adult plant can make new ____.", "seeds", ["shoes", "eggs"]),
           ("A butterfly drinks ____ from flowers.", "nectar", ["milk", "soda"]),
           ("Chicks hatch from ____.", "eggs", ["seeds", "cocoons"]),
           ("All living things are born, grow, and then ____.", "have young", ["turn to stone", "disappear"]),
           ("A butterfly stays inside the chrysalis while it ____.", "changes", ["sleeps outside", "eats leaves"])]
LIFE_TF = [("A caterpillar is the same as a butterfly.", False), ("A tadpole lives in water.", True),
           ("A puppy is a baby dog.", True), ("All animals hatch from eggs.", False), ("Plants have life cycles too.", True),
           ("A seed is the first stage of a plant's life cycle.", True), ("A chick comes out of an egg.", True),
           ("A kitten grows up to be a cow.", False), ("Humans have a life cycle.", True),
           ("A chrysalis comes after the caterpillar.", True), ("A frog begins life as an egg.", True),
           ("A butterfly lays eggs.", True)]


def _cyc_after(rng, n, v, key, before=False):
    items = []
    for c, st in CYC.items():
        for i in range(len(st) - 1):
            if before:
                items.append((f"In the {c} life cycle, what comes just before the {st[i + 1]}?", st[i], [x for x in st if x != st[i]] + ["egg", "adult"]))
            else:
                items.append((f"In the {c} life cycle, what comes just after the {st[i]}?", st[i + 1], [x for x in st if x != st[i + 1]] + ["seed", "baby"]))
    return [mc(rng, q, g, w) for q, g, w in take(items, n, v, key)]


def U4(day, rng, v):
    t = "Life Cycles"
    if day == 1:
        return sheet(4, 1, t, "A life cycle shows how a living thing grows and changes. Follow the stages in order.",
                     "Example: In the frog life cycle, what comes just after the egg?  " + ARROW + "  tadpole",
                     [sec("Part A – What comes next?", "eq", _cyc_after(rng, 12, v, "s4d1a"), 1, 30),
                      sec("Part B – What comes before?", "eq", _cyc_after(rng, 8, v, "s4d1b", True), 1, 30)])
    if day == 2:
        o = []
        for c, st in take(list(CYC.items()), 6, v, "s4d2"):
            o.append(order_item(rng, f"The {c} life cycle.", st))
        return sheet(4, 2, t, "Put the stages of each life cycle in order. Write the letters.",
                     "Example: A. caterpillar  B. egg  C. butterfly  D. chrysalis  " + ARROW + "  B, A, D, C",
                     [sec("", "qline", o, 1, 72)])
    if day == 3:
        a = [mc(rng, f"A baby {x} is called a ____.", y, [b for _, b in BABY], 2) for x, y in take(BABY, 12, v, "s4d3a")]
        b = mcs(rng, LIFE_MC, 8, v, "s4d3b")
        return sheet(4, 3, t, "Many young animals have special names. Learn how animals begin life.",
                     "Example: A baby dog is called a ____ (puppy / calf)  " + ARROW + "  puppy",
                     [sec("Part A – Baby animal names", "eq", a, 1, 30), sec("Part B – Life cycle facts", "eq", b, 1, 30)])
    if day == 4:
        a = mcs(rng, LIFE_MC, 12, v + 0, "s4d4a")
        b = tfs(LIFE_TF, 8, v, "s4d4b")
        cnt = [(f"How many stages are in the {c} life cycle shown in this book?  ____", len(st)) for c, st in take(list(CYC.items()), 4, v, "s4d4c")]
        return sheet(4, 4, t, "More about life cycles: choose the best word, decide true or false, and count the stages.",
                     "Example: A hen lays ____ (eggs / seeds)  " + ARROW + "  eggs",
                     [sec("Part A – Fill in", "eq", a, 1, 30), sec("Part B – True or false?", "eq", b, 1, 30),
                      sec("Part C – Count the stages", "eq", cnt, 1, 30)])
    pas = [("A Butterfly's Story", "A butterfly begins as a tiny egg on a leaf. A caterpillar hatches and eats leaves all day. When it is big enough, "
            "it hangs from a twig and forms a chrysalis. Inside, it changes. After about two weeks, a butterfly comes out and dries its wings.",
            [("Where does the egg start?", "on a leaf"), ("What does the caterpillar eat?", "leaves"),
             ("What is the stage inside called?", "the chrysalis"), ("About how long does it stay inside?", "two weeks")]),
           ("From Tadpole to Frog", "Frogs lay eggs in ponds. Tiny tadpoles hatch and swim with their tails. They breathe with gills. Slowly, back legs grow, "
            "then front legs. The tail gets shorter. At last the froglet becomes a frog that can live on land and in water.",
            [("Where do frogs lay eggs?", "in ponds"), ("What do tadpoles use to swim?", "their tails"),
             ("Which legs grow first?", "the back legs"), ("Where can an adult frog live?", "on land and in water")])][v]
    return sheet(4, 5, t, "Review day! Read about a life cycle, then put stages in order.", "Example: egg, caterpillar, chrysalis, butterfly",
                 [passage_sec(pas[0], pas[1]), qlines(pas[2], 44),
                  sec("Put in order", "qline", [order_item(rng, f"The {c} life cycle.", st) for c, st in take(list(CYC.items()), 2, v, "s4d5o")], 1, 72),
                  sec("Quick review", "eq", _cyc_after(rng, 3, v, "s4d5q"), 1, 30)])


# ============================================================== UNIT 5
SOLID = ["rock", "ice", "book", "spoon", "ball", "chair", "wooden block", "coin", "pencil", "shoe", "brick", "key"]
LIQUID = ["water", "milk", "juice", "cooking oil", "rain", "soup", "honey", "paint", "shampoo", "lemonade"]
GAS = ["air", "steam", "oxygen", "helium", "water vapour", "the air in a balloon"]
PROPS = [("sandpaper", "rough"), ("a pillow", "soft"), ("a rock", "hard"), ("a mirror", "shiny"), ("a rubber band", "stretchy"),
         ("a sponge", "absorbent"), ("a window", "transparent"), ("a wooden door", "opaque"), ("a raincoat", "waterproof"),
         ("honey", "sticky"), ("a steel spoon", "strong"), ("a feather", "light")]
PROPNAMES = ["rough", "soft", "hard", "shiny", "stretchy", "absorbent", "transparent", "opaque", "waterproof", "sticky", "strong", "light", "smooth"]
MATERIAL = [("spoon", "metal"), ("window", "glass"), ("T-shirt", "cloth"), ("tire", "rubber"), ("grocery bag", "plastic"),
            ("table", "wood"), ("book page", "paper"), ("candle", "wax"), ("boot", "rubber"), ("jar", "glass"),
            ("bike frame", "metal"), ("sweater", "wool")]
MATNAMES = ["metal", "glass", "cloth", "rubber", "plastic", "wood", "paper", "wax", "wool"]
FLOAT = ["cork", "wooden block", "plastic duck", "leaf", "foam ball", "beach ball", "ice cube", "feather"]
SINK = ["rock", "coin", "marble", "metal spoon", "brick", "nail", "key", "toy car made of metal"]
RIDDLE = [("I keep my own shape. What am I?", "solid", ["liquid", "gas"]),
          ("I take the shape of my container and I can be poured. What am I?", "liquid", ["solid", "gas"]),
          ("I spread out to fill all the space I can. What am I?", "gas", ["solid", "liquid"]),
          ("Which state of matter can you squeeze into a smaller space?", "gas", ["solid", "liquid"]),
          ("Ice is a ____.", "solid", ["liquid", "gas"]), ("Steam is a ____.", "gas", ["solid", "liquid"]),
          ("Which one has a shape you can hold in your hand? ", "solid", ["liquid", "gas"]),
          ("Juice in a cup is a ____.", "liquid", ["solid", "gas"]), ("The air we breathe is a ____.", "gas", ["solid", "liquid"]),
          ("A rock keeps its shape because it is a ____.", "solid", ["liquid", "gas"]),
          ("Water poured into a bowl takes the shape of the bowl. Water is a ____.", "liquid", ["solid", "gas"]),
          ("Matter is anything that takes up space and has ____.", "mass", ["color", "noise"])]


def U5(day, rng, v):
    t = "Matter: Solids, Liquids & Gases"
    if day == 1:
        c = [(f"Is {x} a solid, a liquid, or a gas?  ____", "solid") for x in take(SOLID, 8, v, "s5d1a")] + \
            [(f"Is {x} a solid, a liquid, or a gas?  ____", "liquid") for x in take(LIQUID, 6, v, "s5d1b")] + \
            [(f"Is {x} a solid, a liquid, or a gas?  ____", "gas") for x in take(GAS, 4, v, "s5d1c")]
        rng.shuffle(c)
        return sheet(5, 1, t, "Matter is anything that takes up space. It can be a solid, a liquid or a gas.",
                     "Example: Is a rock a solid, a liquid or a gas?  " + ARROW + "  solid", [sec("", "eq", c, 1, 30)])
    if day == 2:
        a = [mc(rng, f"Which word describes {x}?", y, PROPNAMES, 2) for x, y in take(PROPS, 10, v, "s5d2a")]
        b = [mc(rng, f"A {x} is usually made of ____.", y, MATNAMES, 2) for x, y in take(MATERIAL, 8, v, "s5d2b")]
        return sheet(5, 2, t, "Properties describe how a material looks and feels. Objects are made of different materials.",
                     "Example: A spoon is usually made of ____ (metal / wax)  " + ARROW + "  metal",
                     [sec("Part A – Describe it", "eq", a, 1, 30), sec("Part B – What is it made of?", "eq", b, 1, 30)])
    if day == 3:
        c = [(f"Will a {x} float or sink in water?  ____", "float") for x in take(FLOAT, 7, v, "s5d3a")] + \
            [(f"Will a {x} float or sink in water?  ____", "sink") for x in take(SINK, 7, v, "s5d3b")]
        rng.shuffle(c)
        ab = [("Does a sponge absorb water?", "yes"), ("Does a plastic bag absorb water?", "no"),
              ("Does a paper towel absorb water?", "yes"), ("Does aluminum foil absorb water?", "no"),
              ("Does a cotton cloth absorb water?", "yes"), ("Does a raincoat absorb water?", "no")]
        return sheet(5, 3, t, "Some things float and some sink. Some materials soak up water (absorb) and some do not.",
                     "Example: Will a cork float or sink?  " + ARROW + "  float",
                     [sec("Part A – Float or sink?", "eq", c, 2, 30), sec("Part B – Does it absorb water?", "eq", [(q + "  ____", a) for q, a in take(ab, 6, v, "s5d3c")], 1, 30)])
    if day == 4:
        return sheet(5, 4, t, "Solid, liquid or gas? Use what you know about how each one behaves.",
                     "Example: I keep my own shape. What am I? (solid / liquid)  " + ARROW + "  solid",
                     [sec("", "eq", mcs(rng, RIDDLE, 12, v, "s5d4"), 1, 30)])
    pas = [("Everything Is Matter", "Matter is anything that takes up space and has mass. Rocks, water and air are all matter. A solid keeps its shape. "
            "A liquid takes the shape of its container. A gas spreads out to fill all the space it can.",
            [("What is matter?", "anything that takes up space and has mass"), ("Which state of matter keeps its shape?", "a solid"),
             ("Which state spreads out to fill its space?", "a gas")]),
           ("The Sink or Float Test", "Sam tested four objects in a tub of water. The cork and the plastic duck floated. The coin and the rock sank. "
            "Sam wrote each result in a chart.",
            [("Which objects floated?", "the cork and the plastic duck"), ("Which objects sank?", "the coin and the rock"),
             ("How did Sam keep his results?", "in a chart")])][v]
    c = [(f"Is {x} a solid, a liquid, or a gas?  ____", s_) for x, s_ in
         [(a, "solid") for a in take(SOLID, 2, v, "s5d5a")] + [(a, "liquid") for a in take(LIQUID, 2, v, "s5d5b")] + [(a, "gas") for a in take(GAS, 2, v, "s5d5c")]]
    rng.shuffle(c)
    return sheet(5, 5, t, "Review day! Read about matter, then review states, properties and materials.",
                 "Example: Is milk a solid, a liquid or a gas?  " + ARROW + "  liquid",
                 [passage_sec(pas[0], pas[1]), qlines(pas[2], 44), sec("States of matter", "eq", c, 1, 30),
                  sec("Properties and materials", "eq", [mc(rng, f"A {x} is usually made of ____.", y, MATNAMES) for x, y in take(MATERIAL, 3, v, "s5d5d")] +
                      [mc(rng, f"Which word describes {x}?", y, PROPNAMES) for x, y in take(PROPS, 2, v, "s5d5e")], 1, 30)])


# ============================================================== UNIT 6
CHG = [("When ice gets warm, it ____.", "melts", ["freezes", "evaporates"]), ("When water gets very cold, it ____.", "freezes", ["melts", "boils"]),
       ("When water is heated a lot, it turns into ____.", "steam", ["ice", "sand"]),
       ("Steam turns back into water drops when it ____.", "cools", ["melts", "grows"]),
       ("A puddle disappears on a sunny day because the water ____.", "evaporates", ["freezes", "melts"]),
       ("Melted chocolate gets hard again when it is ____.", "cooled", ["heated", "stirred"]),
       ("Butter melts when it is ____.", "warmed", ["cooled", "frozen"]),
       ("Water freezing is a change from a liquid to a ____.", "solid", ["gas", "puddle"]),
       ("Water evaporating is a change from a liquid to a ____.", "gas", ["solid", "puddle"]),
       ("Ice melting is a change from a solid to a ____.", "liquid", ["gas", "rock"]),
       ("Wet clothes dry on a clothesline when the water ____.", "evaporates", ["freezes", "melts"]),
       ("Drops of water on a cold glass come from water ____ in the air.", "vapour", ["rocks", "sand"])]
VOCAB = [("The word for ice turning into water is ____.", "melting", ["freezing", "evaporation"]),
         ("The word for water turning into ice is ____.", "freezing", ["melting", "evaporation"]),
         ("The word for water turning into water vapour is ____.", "evaporation", ["melting", "freezing"]),
         ("The word for water vapour turning into water drops is ____.", "condensation", ["melting", "freezing"])]
REV = [("melting an ice cube", True), ("freezing juice into an ice pop", True), ("folding a piece of paper", True),
       ("cutting a piece of paper into bits", False), ("baking cookies", False), ("burning a log", False),
       ("cooking an egg", False), ("popping popcorn", False), ("melting butter", True), ("stretching a rubber band", True),
       ("tearing paper", False), ("blowing up a balloon", True), ("toasting bread", False), ("crushing a can", False),
       ("building with blocks", True), ("making ice cubes", True)]
DISS = [("sugar", True), ("salt", True), ("sand", False), ("rice", False), ("pebbles", False), ("drink powder", True),
        ("cooking oil", False), ("marbles", False)]
MIXTF = [("A mixture is made when two or more things are put together.", True), ("Salt dissolves in water.", True),
         ("Sand dissolves in water.", False), ("You can pick the raisins out of a trail mix.", True),
         ("Oil and water mix together well.", False), ("Stirring helps sugar dissolve faster.", True),
         ("A fruit salad is a mixture.", True), ("Rocks dissolve in water.", False)]
BINS = [("a banana peel", "compost"), ("an apple core", "compost"), ("egg shells", "compost"), ("grass clippings", "compost"),
        ("a newspaper", "recycle"), ("a cardboard box", "recycle"), ("a glass jar", "recycle"), ("a tin can", "recycle"),
        ("a plastic bottle", "recycle"), ("a milk jug", "recycle"), ("a broken toy", "garbage"), ("a candy wrapper", "garbage"),
        ("a used tissue", "garbage"), ("leaves from the yard", "compost"), ("a paper bag", "recycle"), ("a juice box", "recycle")]
RRR = [("Using less paper is ____.", "reducing", ["reusing", "recycling"]), ("Using a jar again to hold pencils is ____.", "reusing", ["reducing", "recycling"]),
       ("Turning old cans into new things is ____.", "recycling", ["reusing", "reducing"]),
       ("Bringing your own water bottle helps us ____ waste.", "reduce", ["burn", "buy"]),
       ("Giving outgrown clothes to a friend is ____.", "reusing", ["reducing", "recycling"]),
       ("Food scraps turn into soil in the ____.", "compost bin", ["garbage can", "toy box"])]


def U6(day, rng, v):
    t = "Changing Matter & the 3 Rs"
    if day == 1:
        return sheet(6, 1, t, "Heating and cooling can change matter. Choose the best word.",
                     "Example: When ice gets warm, it ____ (melts / freezes)  " + ARROW + "  melts",
                     [sec("Part A – What happens?", "eq", mcs(rng, CHG, 12, v, "s6d1a"), 1, 30),
                      sec("Part B – Science words", "eq", [mc(rng, q, g, w) for q, g, w in VOCAB], 1, 30)])
    if day == 2:
        c = [(f"{x}.  Can you change it back?  ____", "yes" if r else "no") for x, r in take(REV, 18, v, "s6d2")]
        return sheet(6, 2, t, "Some changes can be undone (like melting). Others cannot (like baking).",
                     "Example: Melting an ice cube. Can you change it back?  " + ARROW + "  yes (freeze it)", [sec("", "eq", c, 1, 30)])
    if day == 3:
        a = [(f"Does {x} dissolve in water?  ____", "yes" if d else "no") for x, d in take(DISS, 8, v, "s6d3a")]
        return sheet(6, 3, t, "A mixture is two or more things together. Some things dissolve in water.",
                     "Example: Does sugar dissolve in water?  " + ARROW + "  yes",
                     [sec("Part A – Does it dissolve?", "eq", a, 2, 30), sec("Part B – True or false?", "eq", tfs(MIXTF, 8, v, "s6d3b"), 1, 30)])
    if day == 4:
        a = [(f"Which bin? {x}  (recycle / compost / garbage)  ____", y) for x, y in take(BINS, 12, v, "s6d4a")]
        return sheet(6, 4, t, "Reduce, reuse, recycle! Sort the waste into the right bin.",
                     "Example: A banana peel goes in the ____ (compost / garbage)  " + ARROW + "  compost",
                     [sec("Part A – Which bin?", "eq", a, 1, 30), sec("Part B – The 3 Rs", "eq", mcs(rng, RRR, 6, v, "s6d4b"), 1, 30)])
    pas = [("What Happens to Our Garbage?", "Many communities in British Columbia sort their waste into bins. Food scraps go in the compost bin and "
            "turn into soil. Cans, bottles and paper go in the recycling bin to be made into new things. Only what is left goes in the garbage. "
            "Sorting helps keep our land clean.",
            [("Where do food scraps go?", "in the compost bin"), ("What can cans and bottles be made into?", "new things"),
             ("Why do we sort our waste?", "to keep our land clean")]),
           ("Melting Ice", "Zoe put an ice cube on a plate in the sun and another on a plate in the shade. The ice in the sun melted in 10 minutes. "
            "The ice in the shade took 25 minutes. Zoe learned that heat makes ice melt faster.",
            [("Which ice cube melted first?", "the one in the sun"), ("How long did the shade ice cube take?", "25 minutes"),
             ("What did Zoe learn?", "Heat makes ice melt faster.")])][v]
    return sheet(6, 5, t, "Review day! Read the passage, then review changes of matter and the 3 Rs.",
                 "Example: Melting ice. Can you change it back?  " + ARROW + "  yes",
                 [passage_sec(pas[0], pas[1]), qlines(pas[2], 44),
                  sec("Changes", "eq", mcs(rng, CHG, 4, v, "s6d5a") + [(f"{x}.  Can you change it back?  ____", "yes" if r else "no") for x, r in take(REV, 3, v, "s6d5b")], 1, 30),
                  sec("Bins and 3 Rs", "eq", [(f"Which bin? {x}  (recycle / compost / garbage)  ____", y) for x, y in take(BINS, 3, v, "s6d5c")] + mcs(rng, RRR, 2, v, "s6d5d"), 1, 30)])


# ============================================================== UNIT 7
WTF = [("Water is a liquid at room temperature.", True), ("All living things need water.", True), ("Ocean water is salty.", True),
       ("Lakes and rivers are salty like the ocean.", False), ("Rain is a form of water.", True), ("Plants do not need water.", False),
       ("Ice is frozen water.", True), ("Steam is a liquid.", False), ("We can drink ocean water safely.", False),
       ("Water covers most of the Earth.", True), ("Clouds are made of tiny drops of water or ice.", True), ("Snow is a kind of frozen water.", True)]
WSOURCE = [("Which is a source of fresh water?", "a river", ["the ocean", "a sandbox"]), ("Which water is salty?", "the ocean", ["a river", "rain"]),
           ("Rain falls from ____.", "clouds", ["trees", "mountains"]), ("A big, deep body of fresh water is a ____.", "lake", ["desert", "forest"]),
           ("A stream of fresh water that flows to the sea is a ____.", "river", ["hill", "cloud"]),
           ("Water that falls from the sky is called ____.", "precipitation", ["evaporation", "condensation"])]
WSTATE = [("Ice is water as a ____.", "solid", ["liquid", "gas"]), ("Water you drink is a ____.", "liquid", ["solid", "gas"]),
          ("Water vapour is a ____.", "gas", ["solid", "liquid"]), ("Steam is water as a ____.", "gas", ["solid", "liquid"]),
          ("Water freezes when it gets very ____.", "cold", ["hot", "loud"]), ("Water turns to steam when it gets very ____.", "hot", ["cold", "quiet"]),
          ("Snow is water as a ____.", "solid", ["liquid", "gas"]), ("Rain is water as a ____.", "liquid", ["solid", "gas"]),
          ("Frost on a window is water as a ____.", "solid", ["liquid", "gas"]), ("Fog is made of tiny drops of ____.", "water", ["sand", "milk"]),
          ("A glacier is a huge river of ____.", "ice", ["steam", "sand"]), ("When ice melts it becomes ____.", "water", ["steam", "sand"])]
WCYC = [("The Sun heats water and it turns into water vapour. This is called ____.", "evaporation", ["condensation", "precipitation"]),
        ("Water vapour cools and makes clouds. This is called ____.", "condensation", ["evaporation", "precipitation"]),
        ("Rain, snow and hail falling from clouds is called ____.", "precipitation", ["evaporation", "condensation"]),
        ("Rain flows into rivers, lakes and the ocean. This is called ____.", "collection", ["condensation", "evaporation"]),
        ("What gives the energy that starts the water cycle?", "the Sun", ["the Moon", "the wind"]),
        ("Water vapour is a ____ you cannot see.", "gas", ["solid", "liquid"])]
WDIAG = [("Which letter shows the Sun?", "A"), ("Which letter shows a cloud?", "B"), ("Which letter shows rain falling?", "C"),
         ("Which letter shows the lake?", "D"), ("Which letter shows where evaporation starts?", "D"),
         ("Which letter shows where condensation makes clouds?", "B")]
WORDER = [("The water cycle.", ["The Sun heats the water", "Water vapour rises", "Clouds form", "Rain falls"]),
          ("What happens to a puddle.", ["Rain makes a puddle", "The Sun warms the puddle", "The water evaporates", "The puddle disappears"]),
          ("Making rain.", ["Water vapour cools", "Tiny drops join together", "Drops get heavy", "Rain falls"])]
SAVE = [("Which saves water?", "turning off the tap while brushing teeth", ["leaving the hose running", "taking a very long shower"]),
        ("Which saves water?", "fixing a dripping tap", ["washing the car every day", "leaving the tap on"]),
        ("Which wastes water?", "leaving the tap running", ["using a bucket", "turning off the tap"]),
        ("A good way to save water is to take a ____ shower.", "short", ["very long", "hot all day"]),
        ("We can keep water clean by never putting ____ in streams.", "garbage", ["fish", "rain"]),
        ("We use water for drinking, cooking, and ____.", "washing", ["burning", "freezing toys"]),
        ("Plants and animals both need clean ____.", "water", ["paint", "glue"]),
        ("Collecting rain in a barrel to water plants ____ water.", "saves", ["wastes", "pollutes"])]


def U7(day, rng, v):
    t = "Water & the Water Cycle"
    if day == 1:
        a = tfs(WTF, 12, v, "s7d1a")
        b = mcs(rng, WSOURCE, 6, v, "s7d1b")
        return sheet(7, 1, t, "Water is essential to all living things. Learn where water is found.",
                     "Example: All living things need water.  " + ARROW + "  true",
                     [sec("Part A – True or false?", "eq", a, 1, 30), sec("Part B – Where is water?", "eq", b, 1, 30)])
    if day == 2:
        return sheet(7, 2, t, "Water can be a solid (ice), a liquid (water) or a gas (water vapour).",
                     "Example: Ice is water as a ____ (solid / gas)  " + ARROW + "  solid",
                     [sec("", "eq", mcs(rng, WSTATE, 12, v, "s7d2"), 1, 30)])
    if day == 3:
        dq = [(f"{q}  ____", a) for q, a in take(WDIAG, 4, v, "s7d3d")]
        return sheet(7, 3, t, "Water moves in a cycle: evaporation, condensation, precipitation, collection.",
                     "Example: Water turns into water vapour. This is called ____ (evaporation)",
                     [sec("Part A – Water cycle words", "eq", mcs(rng, WCYC, 6, v, "s7d3a"), 1, 30),
                      sec("Look at the water cycle", "diagram", [("wcycle", None)], 1, 170),
                      sec("Part B – Use the picture", "eq", dq, 1, 30)])
    if day == 4:
        o = [order_item(rng, ttl, st) for ttl, st in take(WORDER, 2, v, "s7d4o")]
        return sheet(7, 4, t, "Put water cycle events in order. Then learn how to save and protect water.",
                     "Example: Sun heats water, vapour rises, clouds form, rain falls.",
                     [sec("Part A – Put in order", "qline", o, 1, 72), sec("Part B – Saving water", "eq", mcs(rng, SAVE, 8, v, "s7d4b"), 1, 30)])
    pas = [("The Water Cycle", "The Sun heats water in oceans and lakes. The water turns into water vapour and rises into the air. High up, the vapour "
            "cools and forms clouds. When clouds get heavy, rain or snow falls. The water flows back to rivers, lakes and the ocean, and the cycle starts again.",
            [("What heats the water?", "the Sun"), ("What forms when water vapour cools?", "clouds"), ("Name two kinds of precipitation.", "rain and snow")]),
           ("Water Is Life", "All living things need water. Many First Peoples in British Columbia teach that water is a gift and must be protected. "
            "People keep rivers and lakes clean for salmon, plants and everyone who drinks. We can help by turning off the tap and never putting garbage in streams.",
            [("Who needs water?", "all living things"), ("What do many First Peoples teach about water?", "It is a gift and must be protected."),
             ("Name one way we can help.", "turn off the tap (or keep streams clean)")])][v]
    return sheet(7, 5, t, "Review day! Read about water, then review the water cycle.", "Example: Rain, snow and hail are called precipitation.",
                 [passage_sec(pas[0], pas[1]), qlines(pas[2], 44), sec("States of water", "eq", mcs(rng, WSTATE, 3, v, "s7d5a"), 1, 30),
                  sec("Water cycle and saving water", "eq", mcs(rng, WCYC, 3, v, "s7d5b") + mcs(rng, SAVE, 2, v, "s7d5c"), 1, 30)])


# ============================================================== UNIT 8
PP = [("kick a ball", "push"), ("pull a wagon", "pull"), ("open a drawer", "pull"), ("close a door", "push"), ("zip a zipper", "pull"),
      ("push a swing", "push"), ("throw a ball", "push"), ("play tug of war", "pull"), ("pull a sled", "pull"),
      ("push a shopping cart", "push"), ("press a doorbell", "push"), ("pull a rope", "pull"), ("push a lawn mower", "push"),
      ("pull open a bag of chips", "pull")]
MOTION = [("A force can make an object ____.", "start moving", ["turn into water", "disappear"]),
          ("A bigger push makes a ball go ____.", "farther", ["shorter", "backwards only"]),
          ("A heavy box is ____ to push than a light box.", "harder", ["easier", "quieter"]),
          ("To make a swing go higher, give a ____ push.", "bigger", ["smaller", "sleepy"]),
          ("A force can make an object ____.", "stop", ["sing", "freeze"]),
          ("A push or pull can change the ____ of a moving object.", "direction", ["taste", "color"]),
          ("A ball rolls ____ when you push it gently.", "slowly", ["faster than a car", "up the wall"]),
          ("An object at rest stays still until a ____ moves it.", "force", ["color", "sound"]),
          ("Pulling a wagon makes it move ____ you.", "toward", ["away from", "around"]),
          ("Pushing a door makes it move ____ you.", "away from", ["toward", "around"]),
          ("Forces are pushes and ____.", "pulls", ["sounds", "colors"]), ("A stronger force makes an object move ____.", "faster", ["slower", "quieter"])]
GRAV = [("Gravity pulls things ____.", "down", ["up", "sideways"]), ("When you let go of a ball, it ____.", "falls", ["floats away", "turns into air"]),
        ("Which surface has more friction?", "carpet", ["ice", "a wet slide"]), ("Which surface has less friction?", "ice", ["sandpaper", "carpet"]),
        ("Friction ____ moving objects.", "slows", ["speeds up", "paints"]), ("Rubbing your hands together makes them warm because of ____.", "friction", ["gravity", "magnets"]),
        ("Wheels help things move because they ____ friction.", "reduce", ["make", "paint"]),
        ("A toy car slows down faster on ____.", "grass", ["smooth ice", "a wet floor"]),
        ("Rain falls down because of ____.", "gravity", ["friction", "magnets"]),
        ("Gravity is a force that pulls objects toward the ____.", "Earth", ["Sun only", "sky"]),
        ("Rough surfaces have ____ friction.", "more", ["less", "no"]), ("Smooth, slippery surfaces have ____ friction.", "less", ["more", "the most"])]
MAGY = ["paper clip", "iron nail", "steel can", "pair of scissors", "steel screw", "iron chain"]
MAGN = ["plastic spoon", "wooden block", "sheet of paper", "rubber eraser", "glass marble", "aluminum foil", "pencil", "rubber band"]
MAGP = [("Like poles of two magnets ____.", "push apart", ["pull together", "do nothing"]), ("Opposite poles of two magnets ____.", "pull together", ["push apart", "melt"]),
        ("A magnet has a north pole and a ____ pole.", "south", ["east", "middle"]), ("Magnets can pull on some ____.", "metals", ["plastics", "papers"]),
        ("A magnet is strongest at its ____.", "poles", ["middle", "label"]), ("Two north poles will ____.", "repel", ["attract", "stick"])]


def U8(day, rng, v):
    t = "Forces & Motion"
    if day == 1:
        c = [(f"To {x}, you use a ____ (push / pull).", y) for x, y in take(PP, 14, v, "s8d1")]
        return sheet(8, 1, t, "A force is a push or a pull. Is it a push or a pull?",
                     "Example: To kick a ball, you use a push.", [sec("", "eq", c, 1, 30)])
    if day == 2:
        return sheet(8, 2, t, "Forces make objects start moving, stop, speed up, slow down or change direction.",
                     "Example: A force can make an object ____ (start moving / disappear)  " + ARROW + "  start moving",
                     [sec("", "eq", mcs(rng, MOTION, 12, v, "s8d2"), 1, 30)])
    if day == 3:
        return sheet(8, 3, t, "Gravity pulls things down. Friction slows things that rub together.",
                     "Example: Gravity pulls things ____ (down / up)  " + ARROW + "  down", [sec("", "eq", mcs(rng, GRAV, 12, v, "s8d3"), 1, 30)])
    if day == 4:
        c = [(f"Will a magnet pick up {indef(x)}?  ____", "yes") for x in take(MAGY, 5, v, "s8d4a")] + \
            [(f"Will a magnet pick up {indef(x)}?  ____", "no") for x in take(MAGN, 5, v, "s8d4b")]
        rng.shuffle(c)
        return sheet(8, 4, t, "Magnets pull on some metals like iron and steel. They have a north and a south pole.",
                     "Example: Will a magnet pick up an iron nail?  " + ARROW + "  yes",
                     [sec("Part A – Magnetic or not?", "eq", c, 2, 30), sec("Part B – Magnet poles", "eq", mcs(rng, MAGP, 6, v, "s8d4c"), 1, 30)])
    pas = [("Playground Forces", "On the playground, Ben pushes the swing and it moves away. Mia pulls the wagon behind her. A ball rolls down the slide "
            "because of gravity. The sandbox slows down Ben's toy truck because of friction.",
            [("What force pulls the ball down the slide?", "gravity"), ("What slows the toy truck?", "friction"), ("Is pulling a wagon a push or a pull?", "a pull")]),
           ("Magnet Fun", "Lily tested a magnet on seven things. The magnet stuck to an iron nail, a paper clip, and a steel can. It did not stick to a pencil, "
            "an eraser, a wooden block, or a plastic cup. Lily learned that magnets pull on some metals.",
            [("Which three things stuck to the magnet?", "the iron nail, the paper clip and the steel can"), ("Did the magnet stick to the wooden block?", "no"),
             ("What did Lily learn?", "Magnets pull on some metals.")])][v]
    return sheet(8, 5, t, "Review day! Read about forces, then review push, pull, gravity and magnets.",
                 "Example: To zip a zipper, you use a pull.",
                 [passage_sec(pas[0], pas[1]), qlines(pas[2], 44),
                  sec("Push or pull?", "eq", [(f"To {x}, you use a ____ (push / pull).", y) for x, y in take(PP, 4, v, "s8d5a")], 1, 30),
                  sec("Forces and magnets", "eq", mcs(rng, GRAV, 3, v, "s8d5b") + mcs(rng, MAGP, 2, v, "s8d5c") +
                      [(f"Will a magnet pick up {indef(x)}?  ____", y) for x, y in [(take(MAGY, 1, v, "s8d5d")[0], "yes"), (take(MAGN, 1, v, "s8d5e")[0], "no")]], 1, 30)])


# ============================================================== UNIT 9
LSRC = ["the Sun", "a lamp", "a candle", "a flashlight", "a campfire", "lightning", "a light bulb", "a firefly"]
NOLSRC = ["the Moon", "a mirror", "a book", "a tree", "a rock", "a table", "a window", "a pillow"]
TRANSP = [("a glass window", "transparent"), ("clear water", "transparent"), ("plastic wrap", "transparent"), ("wax paper", "translucent"),
          ("tissue paper", "translucent"), ("frosted glass", "translucent"), ("a wooden door", "opaque"), ("a brick", "opaque"),
          ("cardboard", "opaque"), ("a metal pan", "opaque"), ("a book", "opaque"), ("a clear plastic cup", "transparent")]
SHADOW = [("A shadow forms when an object ____ light.", "blocks", ["makes", "paints"]),
          ("Shadows are longest in the early morning and ____.", "evening", ["noon", "lunch"]),
          ("Shadows are shortest at ____.", "noon", ["sunset", "sunrise"]),
          ("To make a bigger shadow, move the object ____ the light.", "closer to", ["farther from", "behind"]),
          ("You cannot make a shadow without a source of ____.", "light", ["sound", "wind"]),
          ("A shadow is always on the side ____ the light.", "away from", ["facing", "above"]),
          ("Which material makes the darkest shadow?", "opaque", ["transparent", "clear"])]
SOUND = [("Sound is made when things ____.", "vibrate", ["freeze", "melt"]), ("A mouse squeaks with a ____ sound.", "high", ["low", "silent"]),
         ("A lion roars with a ____ sound.", "low", ["high", "tiny"]), ("A big drum makes a ____ sound.", "low", ["high", "silent"]),
         ("A whistle makes a ____ sound.", "high", ["low", "quiet"]), ("A bird chirp is a ____ sound.", "high", ["low", "rumble"]),
         ("Thunder is a ____ sound.", "low", ["high", "tiny"]), ("Which is louder?", "a shout", ["a whisper", "a sigh"]),
         ("Sound travels through the ____ to reach your ears.", "air", ["paint", "snow only"]),
         ("A guitar string makes sound when it ____.", "shakes", ["melts", "sleeps"]), ("We hear sound with our ____.", "ears", ["eyes", "elbows"]),
         ("A very loud sound can hurt your ____.", "ears", ["knees", "hair"]), ("A tuba makes a ____ sound.", "low", ["high", "silent"]),
         ("A tiny bell makes a ____ sound.", "high", ["low", "rumble"])]
HEAT = [("The Sun gives Earth light and ____.", "heat", ["noise", "snow"]), ("Heat moves from hot things to ____ things.", "cold", ["loud", "bigger"]),
        ("Ice melts faster in the ____.", "sun", ["shade", "freezer"]), ("Which would keep you warmest outside in winter?", "a wool sweater", ["a T-shirt", "shorts"]),
        ("Which can be a source of heat?", "a campfire", ["an ice cube", "a snowman"]), ("A dark shirt gets ____ in the Sun than a white shirt.", "hotter", ["colder", "wetter"]),
        ("A battery gives energy to a ____.", "toy", ["book", "rock"]), ("Wind gives energy to a ____.", "sailboat", ["spoon", "pencil"]),
        ("Food gives energy to ____.", "people and animals", ["rocks", "chairs"]), ("Which uses electricity?", "a lamp", ["a book", "a rock"]),
        ("Plants use ____ to make food.", "sunlight", ["wind", "sound"]), ("A hot cocoa will stay warm longest in a ____.", "foam cup", ["metal cup", "paper plate"])]


def U9(day, rng, v):
    t = "Energy: Light, Sound & Heat"
    if day == 1:
        c = [(f"Is {x} a source of light?  ____", "yes") for x in take(LSRC, 6, v, "s9d1a")] + \
            [(f"Is {x} a source of light?  ____", "no") for x in take(NOLSRC, 6, v, "s9d1b")]
        rng.shuffle(c)
        return sheet(9, 1, t, "A source of light makes its own light. The Moon only reflects light from the Sun.",
                     "Example: Is the Sun a source of light?  " + ARROW + "  yes", [sec("", "eq", c, 1, 30)])
    if day == 2:
        a = [mc(rng, f"Light passes through {x}. It is ____." if y == "transparent" else f"{x[0].upper() + x[1:]} is ____.", y, ["transparent", "translucent", "opaque"], 2)
             for x, y in take(TRANSP, 6, v, "s9d2a")]
        a = [mc(rng, f"Is {x} transparent, translucent, or opaque?", y, ["transparent", "translucent", "opaque"], 2) for x, y in take(TRANSP, 8, v, "s9d2a")]
        return sheet(9, 2, t, "Transparent: see clearly. Translucent: light, not clear. Opaque: no light passes. Shadows form when light is blocked.",
                     "Example: Is a wooden door transparent, translucent or opaque?  " + ARROW + "  opaque",
                     [sec("Part A – Materials and light", "eq", a, 1, 30), sec("Part B – Shadows", "eq", mcs(rng, SHADOW, 6, v, "s9d2b"), 1, 30)])
    if day == 3:
        return sheet(9, 3, t, "Sound is made when things vibrate. Sounds can be loud or quiet, high or low.",
                     "Example: A mouse squeaks with a ____ sound (high / low)  " + ARROW + "  high", [sec("", "eq", mcs(rng, SOUND, 14, v, "s9d3"), 1, 30)])
    if day == 4:
        return sheet(9, 4, t, "Energy makes things happen. The Sun gives light and heat.",
                     "Example: The Sun gives Earth light and ____ (heat / noise)  " + ARROW + "  heat", [sec("", "eq", mcs(rng, HEAT, 12, v, "s9d4"), 1, 30)])
    pas = [("Sounds Around Us", "Sound is made when things vibrate. When you pluck a guitar string, it shakes back and forth and makes a sound. A big drum "
            "makes a low sound. A tiny bell makes a high sound. Sound travels through the air to your ears.",
            [("How is sound made?", "when things vibrate"), ("Which makes a low sound?", "a big drum"), ("What carries sound to your ears?", "the air")]),
           ("Sun Power", "The Sun gives us light and heat. Plants use sunlight to make food. A dark shirt gets hotter in the Sun than a white shirt. "
            "Solar panels turn sunlight into electricity. Without the Sun, Earth would be dark and very cold.",
            [("Name two things the Sun gives us.", "light and heat"), ("What do plants use sunlight for?", "to make food"),
             ("Which shirt gets hotter in the Sun?", "the dark shirt")])][v]
    return sheet(9, 5, t, "Review day! Read about energy, then review light, sound and heat.", "Example: A whistle makes a high sound.",
                 [passage_sec(pas[0], pas[1]), qlines(pas[2], 44),
                  sec("Light", "eq", [(f"Is {x} a source of light?  ____", "yes") for x in take(LSRC, 2, v, "s9d5a")] +
                      [(f"Is {x} a source of light?  ____", "no") for x in take(NOLSRC, 2, v, "s9d5b")] +
                      [mc(rng, f"Is {x} transparent, translucent, or opaque?", y, ["transparent", "translucent", "opaque"]) for x, y in take(TRANSP, 2, v, "s9d5c")], 1, 30),
                  sec("Sound and heat", "eq", mcs(rng, SOUND, 3, v, "s9d5d") + mcs(rng, HEAT, 3, v, "s9d5e"), 1, 30)])


# ============================================================== UNIT 10
WEA = [("Water falling from clouds in drops is ____.", "rain", ["fog", "wind"]), ("Frozen water falling as soft flakes is ____.", "snow", ["rain", "hail"]),
       ("Balls of ice that fall from storm clouds are ____.", "hail", ["fog", "rain"]), ("Moving air is called ____.", "wind", ["snow", "rain"]),
       ("A thermometer measures ____.", "temperature", ["rain", "wind"]), ("A rain gauge measures how much ____ fell.", "rain", ["wind", "sun"]),
       ("A wind sock shows which way the ____ blows.", "wind", ["rain", "sun"]), ("On a rainy day, wear a ____.", "raincoat", ["swimsuit", "sandals"]),
       ("On a snowy day, wear ____.", "warm boots", ["sandals", "shorts"]), ("On a hot sunny day, wear a ____.", "sun hat", ["scarf", "snow suit"]),
       ("Thunder and lightning happen in a ____.", "storm", ["fog", "snowfall"]), ("A low cloud near the ground is ____.", "fog", ["hail", "wind"])]
SEASON = [("Flowers bloom and baby animals are born in ____.", "spring", ["winter", "fall"]), ("The days are long and warm in ____.", "summer", ["winter", "spring"]),
          ("Leaves change color in ____.", "fall", ["spring", "summer"]), ("It is cold with snow in ____.", "winter", ["summer", "spring"]),
          ("The season after winter is ____.", "spring", ["fall", "summer"]), ("The season after spring is ____.", "summer", ["winter", "fall"]),
          ("The season after summer is ____.", "fall", ["winter", "spring"]), ("The season after fall is ____.", "winter", ["summer", "spring"]),
          ("How many seasons are in a year?", "four", ["two", "seven"]), ("July is in ____.", "summer", ["winter", "spring"]),
          ("January is in ____.", "winter", ["summer", "spring"]), ("October is in ____.", "fall", ["spring", "summer"]),
          ("April is in ____.", "spring", ["fall", "winter"]), ("Many birds fly south in ____.", "fall", ["spring", "summer"]),
          ("Bears begin to hibernate in late ____.", "fall", ["spring", "summer"]), ("People swim outside the most in ____.", "summer", ["winter", "fall"])]
SKY = [("The Sun is a ____.", "star", ["planet", "moon"]), ("The Sun appears to rise in the ____.", "east", ["west", "south"]),
       ("The Sun appears to set in the ____.", "west", ["east", "north"]), ("We have day and night because Earth ____.", "spins", ["melts", "stops"]),
       ("It is night when our side of Earth faces ____ the Sun.", "away from", ["toward", "into"]),
       ("The Moon shines because it ____ light from the Sun.", "reflects", ["makes", "eats"]),
       ("The Moon looks like different shapes. These are called ____.", "phases", ["seasons", "storms"]),
       ("Earth is a ____.", "planet", ["star", "moon"]), ("The Moon goes around the ____.", "Earth", ["Sun only", "clouds"]),
       ("The Sun is the center of our ____.", "solar system", ["kitchen", "classroom"]),
       ("A day is about ____ hours long.", "24", ["7", "60"]), ("Stars look tiny because they are very ____.", "far away", ["small and close", "wet"])]
EARTH = [("Which helps the Earth?", "planting a tree", ["littering", "wasting water"]), ("Which is a natural resource?", "water", ["a toy", "a shoe"]),
         ("Trees give us wood, shade and clean ____.", "air", ["candy", "plastic"]), ("We can protect nature by picking up ____.", "litter", ["flowers in parks", "baby birds"]),
         ("Turning off lights when you leave a room saves ____.", "energy", ["sound", "snow"]), ("Walking or biking instead of driving helps keep the ____ clean.", "air", ["pencils", "tables"]),
         ("Which is NOT a natural resource?", "a plastic toy", ["water", "soil"]), ("Healthy soil helps ____ grow.", "plants", ["plastic", "rocks only"])]
RESULTS = [("Brand A soaked up 20 mL, Brand B soaked up 35 mL, Brand C soaked up 10 mL. Which towel is best at soaking up water?", "Brand B"),
           ("Plant 1 grew 6 cm. Plant 2 grew 11 cm. Plant 3 grew 3 cm. Which plant grew the most?", "Plant 2"),
           ("The red car rolled 40 cm, the blue car rolled 55 cm, and the green car rolled 25 cm. Which car rolled the farthest?", "the blue car"),
           ("Ice in the sun melted in 12 min. Ice in the shade melted in 30 min. How many minutes longer did the shade ice take?", "18 minutes"),
           ("A magnet picked up 9 paper clips. A weaker magnet picked up 4. How many more did the stronger magnet pick up?", "5"),
           ("We tested 8 objects. 5 floated. How many sank?", "3")]
PLAN = [("Plan an investigation: Which will melt an ice cube faster, a sunny window or a shady shelf? Write your question and your prediction.",
         "Answers vary. Check: a testable question and a prediction (e.g. The ice will melt faster in the sun)."),
        ("Plan an investigation: Which toy car goes farther, on carpet or on a wood floor? Tell what you will change and what stays the same.",
         "Answers vary. Check: change the floor surface; keep the car, ramp and push the same."),
        ("Plan an investigation: Do seeds sprout faster in warm or in cool places? Write what you will do, step by step.",
         "Answers vary. Check: steps in order, one thing changed, fair test."),
        ("Plan an investigation: Which material is best for a raincoat: paper, plastic, or cloth? Write your prediction.",
         "Answers vary. Check: a prediction (plastic likely) and how to test it."),
        ("Plan an investigation: Does a bigger magnet pick up more paper clips? Tell how you will test it.",
         "Answers vary. Check: same paper clips, count what each magnet picks up."),
        ("Plan an investigation: Which makes a higher sound, a short ruler or a long ruler plucked over a table edge? Write your prediction.",
         "Answers vary. Check: prediction (short ruler higher) and a fair test.")]


def U10(day, rng, v):
    t = "Weather, Seasons & Earth"
    if day == 1:
        return sheet(10, 1, t, "Weather changes from day to day. Scientists measure and record it with tools.",
                     "Example: A thermometer measures ____ (temperature / wind)  " + ARROW + "  temperature", [sec("", "eq", mcs(rng, WEA, 12, v, "s10d1"), 1, 30)])
    if day == 2:
        return sheet(10, 2, t, "There are four seasons: spring, summer, fall and winter. Each has its own weather.",
                     "Example: Leaves change color in ____ (fall / spring)  " + ARROW + "  fall", [sec("", "eq", mcs(rng, SEASON, 16, v, "s10d2"), 1, 30)])
    if day == 3:
        return sheet(10, 3, t, "The Sun, Moon and Earth move in space. Day and night happen because Earth spins.",
                     "Example: The Sun is a ____ (star / planet)  " + ARROW + "  star", [sec("", "eq", mcs(rng, SKY, 12, v, "s10d3"), 1, 30)])
    if day == 4:
        return sheet(10, 4, t, "Earth gives us air, water, soil and plants. We can take care of them.",
                     "Example: Which helps the Earth? (planting a tree / littering)  " + ARROW + "  planting a tree",
                     [sec("Part A – Caring for Earth", "eq", mcs(rng, EARTH, 8, v, "s10d4a"), 1, 30),
                      sec("Part B – Weather and seasons", "eq", mcs(rng, WEA, 4, v, "s10d4b") + mcs(rng, SEASON, 4, v, "s10d4c"), 1, 30)])
    res = [(q, a) for q, a in take(RESULTS, 3, v, "s10d5r")]
    fair = mcs(rng, FAIR, 3, v, "s10d5f")
    pl = take(PLAN, 2, v, "s10d5p")
    return sheet(10, 5, t, "Challenge day! Read results, think about fair tests, and plan your own investigation.",
                 "Example: Plant 1 grew 6 cm. Plant 2 grew 11 cm. Which grew more?  " + ARROW + "  Plant 2",
                 [sec("Part A – Read the results", "qline", res, 1, 56), sec("Part B – Fair tests", "eq", fair, 1, 30),
                  sec("Part C – Plan an investigation", "write", pl, 1, 118)])


UNITS = {1: U1, 2: U2, 3: U3, 4: U4, 5: U5, 6: U6, 7: U7, 8: U8, 9: U9, 10: U10}


def unit_sheets(u, variant=0):
    return [fit(_longfix(UNITS[u](d, random.Random(u * 100 + d + variant * 1000), variant))) for d in range(1, 6)]


# ----------------------------------------------------------- check / final
def _pick(rng, bank, n, key):
    return [mc(rng, q, g, w) for q, g, w in take(bank, n, 0, key)]


def checkup_a():
    rng = random.Random(2555)
    s = [sec("Scientist skills", "eq", [mc(rng, "You hear a bell with your ____.", "ears", ORGANS), mc(rng, "Which tool measures how long a pencil is?", "ruler", TOOLNAMES),
                                        tf("The leaf is green is an observation.", True), tf("A fair test changes only one thing.", True)], 1, 30),
         sec("Living things & plants", "eq", [("Is a frog living or non-living?  ____", "living"), ("Is a chair living or non-living?  ____", "non-living"),
                                              mc(rng, "Which part of a plant takes in water from the soil?", "roots", PARTNAMES),
                                              mc(rng, "When we eat a carrot, we eat the ____ of the plant.", "root", PARTNAMES)], 1, 30),
         sec("Animals", "eq", [mc(rng, "A salmon is a ____.", "fish", CLASSES), mc(rng, "A robin is covered with ____.", "feathers", COVER),
                               mc(rng, "A cow is a ____.", "herbivore", ["herbivore", "carnivore", "omnivore"]),
                               mc(rng, "A duck has webbed feet to help it ____.", "swim", ["fly", "sleep"])], 1, 30),
         sec("Life cycles", "eq", [mc(rng, "In the frog life cycle, what comes just after the egg?", "tadpole", ["froglet", "frog"]),
                                   mc(rng, "A baby dog is called a ____.", "puppy", ["kitten", "calf"]),
                                   mc(rng, "A caterpillar makes a ____ before it becomes a butterfly.", "chrysalis", ["nest", "web"])], 1, 30),
         sec("Matter", "eq", [("Is milk a solid, a liquid, or a gas?  ____", "liquid"), ("Is a rock a solid, a liquid, or a gas?  ____", "solid"),
                              ("Will a coin float or sink in water?  ____", "sink"), mc(rng, "A spoon is usually made of ____.", "metal", MATNAMES)], 1, 30)]
    return sheet(0, "A", "Check-Up: Units 1–5", "Show what you know! Do your best on every question.",
                 "Aim for 90% or more before moving on to Unit 6.", s)


def final_test():
    rng = random.Random(2999)
    s = [sec("Changes in matter", "eq", [mc(rng, "When ice gets warm, it ____.", "melts", ["freezes", "evaporates"]),
                                         ("Baking cookies. Can you change it back?  ____", "no"), ("Which bin? a banana peel  (recycle / compost / garbage)  ____", "compost")], 1, 30),
         sec("Water", "eq", [mc(rng, "The Sun heats water and it turns into water vapour. This is called ____.", "evaporation", ["condensation", "precipitation"]),
                             mc(rng, "Rain, snow and hail falling from clouds is called ____.", "precipitation", ["evaporation", "condensation"]),
                             mc(rng, "Water vapour is a ____.", "gas", ["solid", "liquid"])], 1, 30),
         sec("Forces and magnets", "eq", [("To pull a wagon, you use a ____ (push / pull).", "pull"), mc(rng, "Gravity pulls things ____.", "down", ["up", "sideways"]),
                                          ("Will a magnet pick up an iron nail?  ____", "yes"), mc(rng, "Friction ____ moving objects.", "slows", ["speeds up", "paints"])], 1, 30),
         sec("Light, sound and heat", "eq", [("Is a candle a source of light?  ____", "yes"), mc(rng, "A mouse squeaks with a ____ sound.", "high", ["low", "silent"]),
                                             mc(rng, "The Sun gives Earth light and ____.", "heat", ["noise", "snow"])], 1, 30),
         sec("Weather and seasons", "eq", [mc(rng, "A thermometer measures ____.", "temperature", ["rain", "wind"]),
                                           mc(rng, "Leaves change color in ____.", "fall", ["spring", "summer"]),
                                           mc(rng, "The Sun is a ____.", "star", ["planet", "moon"])], 1, 30),
         passage_sec("Plants in the Dark", "Noor put a bean plant in a dark closet and another by a sunny window. She gave both the same water. After a week, "
                     "the plant in the closet was pale and weak. The plant by the window was tall and green."),
         qlines([("What did Noor change?", "where the plants were (light)"), ("What stayed the same?", "the water"),
                 ("Which plant grew better?", "the one by the window"), ("What do plants need?", "sunlight")], 44)]
    return sheet(0, "F", "Final Test: Units 1–10", "You made it! Show everything you have learned.",
                 "Aim for 90% or more. Then it's certificate time!", s)
