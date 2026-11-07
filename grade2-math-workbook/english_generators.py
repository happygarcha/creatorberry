"""Problem generators for the Grade 2 English Mastery Workbook.

Same sheet format as generators.py. Every day function takes (day, rng, v) where
v = 0 for Sheet A and v = 1 for Sheet B.  Banks are split with take(), so Sheet A and
Sheet B use different items whenever the bank is big enough.
"""
import random
from reportlab.lib.utils import simpleSplit
from generators import sec, sheet, uniq

PAGE_W, PAGE_M = 612, 40
ARROW = "→"


def take(bank, n, v, key):
    b = list(bank)
    random.Random(sum(map(ord, key))).shuffle(b)
    return [b[(v * n + i) % len(b)] for i in range(n)]


def eq(text, ans):
    return (text, str(ans))


def passage_sec(title, text):
    lines = simpleSplit(text, "Helvetica", 11.5, PAGE_W - 2 * PAGE_M - 28)
    return sec("", "passage", [((title, text), None)], 1, 50 + 15 * len(lines))


def qlines(pairs, h=50):
    return sec("", "qline", [(q, str(a)) for q, a in pairs], 1, h)


# ============================================================ word banks
VOWELS = "aeiou"
CVC = [("cat", "a pet that purrs"), ("dog", "a pet that barks"), ("sun", "it shines in the day"),
       ("hat", "you wear it on your head"), ("pen", "you write with it"), ("bed", "you sleep in it"),
       ("cup", "you drink from it"), ("pig", "a farm animal that oinks"), ("bus", "a big vehicle for many people"),
       ("net", "used to catch fish"), ("box", "you put things in it"), ("mop", "you clean the floor with it"),
       ("fox", "a wild animal with a bushy tail"), ("jam", "sweet spread for toast"), ("leg", "you walk on it"),
       ("lip", "part of your mouth"), ("nut", "a squirrel eats it"), ("pot", "you cook soup in it"),
       ("web", "a spider makes it"), ("van", "a small truck"), ("wig", "fake hair"), ("log", "a piece of a tree"),
       ("mug", "a cup with a handle"), ("hen", "a female chicken"), ("rug", "a small carpet"),
       ("bug", "a tiny insect"), ("tub", "you take a bath in it"), ("map", "shows where places are"),
       ("fan", "keeps you cool"), ("bat", "a flying animal of the night")]
SHORT = {"a": ["cat", "hat", "map", "fan", "jam", "van", "bat", "mat"],
         "e": ["pen", "bed", "net", "leg", "hen", "web", "jet", "wet"],
         "i": ["pig", "lip", "wig", "sit", "fin", "lid", "bib", "pin"],
         "o": ["pot", "mop", "fox", "box", "log", "dog", "hop", "top"],
         "u": ["sun", "cup", "bus", "nut", "mug", "rug", "bug", "tub"]}
PAIRS = [("cap", "cape"), ("tap", "tape"), ("mad", "made"), ("kit", "kite"), ("rid", "ride"), ("hop", "hope"),
         ("not", "note"), ("cub", "cube"), ("tub", "tube"), ("pin", "pine"), ("fin", "fine"), ("hat", "hate"),
         ("rob", "robe"), ("mat", "mate"), ("bit", "bite"), ("win", "wine"), ("cut", "cute"), ("can", "cane"),
         ("dim", "dime"), ("pan", "pane")]
LONGW = ["bike", "cake", "home", "rope", "kite", "cube", "tube", "game", "nose", "bone", "lake", "gate"]
SHORTW = ["hat", "pen", "pig", "pot", "sun", "bed", "dog", "map", "cup", "sit", "hop", "web"]
VT = [("rain", "ai", "water that falls from clouds"), ("tail", "ai", "a dog wags it"),
      ("mail", "ai", "letters and packages"), ("train", "ai", "runs on tracks"),
      ("snail", "ai", "a slow animal with a shell"), ("day", "ay", "the opposite of night"),
      ("play", "ay", "what children do at recess"), ("tray", "ay", "you carry food on it"),
      ("tree", "ee", "has leaves and a trunk"), ("feet", "ee", "you wear shoes on them"),
      ("sheep", "ee", "gives us wool"), ("green", "ee", "the color of grass"),
      ("leaf", "ea", "falls from a tree in autumn"), ("beach", "ea", "sand and waves"),
      ("team", "ea", "a group that plays together"), ("bean", "ea", "a seed you can eat"),
      ("boat", "oa", "floats on water"), ("coat", "oa", "you wear it when it is cold"),
      ("road", "oa", "cars drive on it"), ("goat", "oa", "a farm animal that eats grass"),
      ("soap", "oa", "you wash with it")]
LONGCLOZE = [("I ride my ____ to school.", "bike", "bik"), ("Mom will bake a ____.", "cake", "cak"),
             ("We swam in the ____.", "lake", "lak"), ("I wear a warm ____.", "coat", "cot"),
             ("We sail in a ____.", "boat", "bot"), ("The ____ is green and tall.", "tree", "tre"),
             ("I wash my hands with ____.", "soap", "sop"), ("Please close the ____.", "gate", "gat"),
             ("My dog wags his ____.", "tail", "tal"), ("I have two ____.", "feet", "fet"),
             ("The ____ eats grass.", "goat", "got"), ("We play a ____ at recess.", "game", "gam"),
             ("I smell with my ____.", "nose", "nos"), ("A dog likes a ____.", "bone", "bon"),
             ("I go to school every ____.", "day", "da"), ("The ____ rides on tracks.", "train", "tran"),
             ("A ____ is a small seed you can eat.", "bean", "ben"), ("Dad will ____ the car.", "drive", "driv"),
             ("My ____ is where I live.", "home", "hom"), ("I jump with a ____.", "rope", "rop")]

DIG = [("ship", "sh", "sails on the sea"), ("shop", "sh", "a place to buy things"),
       ("shell", "sh", "found on the beach"), ("fish", "sh", "swims in water"),
       ("dish", "sh", "you eat food from it"), ("wish", "sh", "you make one on a star"),
       ("chip", "ch", "a crunchy snack"), ("chair", "ch", "you sit on it"),
       ("cheese", "ch", "made from milk"), ("lunch", "ch", "the meal at noon"),
       ("bench", "ch", "a seat in the park"), ("chick", "ch", "a baby hen"),
       ("thin", "th", "not fat"), ("thumb", "th", "your short, fat finger"),
       ("three", "th", "the number after two"), ("bath", "th", "you take one in a tub"),
       ("teeth", "th", "you brush them"), ("math", "th", "a school subject with numbers"),
       ("whale", "wh", "a giant sea animal"), ("wheel", "wh", "a car has four"),
       ("white", "wh", "the color of snow"), ("whisper", "wh", "to speak very quietly"),
       ("duck", "ck", "a bird that quacks"), ("sock", "ck", "you wear it on your foot"),
       ("clock", "ck", "tells the time"), ("truck", "ck", "a big vehicle that carries loads"),
       ("kick", "ck", "hit a ball with your foot")]
BLEND = [("frog", "fr", "a green animal that hops"), ("flag", "fl", "waves on a pole"),
         ("clap", "cl", "hit your hands together"), ("plum", "pl", "a purple fruit"),
         ("slide", "sl", "playground fun"), ("brush", "br", "you use it on your hair"),
         ("crab", "cr", "a sea animal with claws"), ("drum", "dr", "you beat it to make music"),
         ("grape", "gr", "a small round fruit that grows in bunches"), ("tree", "tr", "has leaves and a trunk"),
         ("star", "st", "twinkles at night"), ("smile", "sm", "a happy look on your face"),
         ("snake", "sn", "a long animal with no legs"), ("spoon", "sp", "you eat soup with it"),
         ("swim", "sw", "move through water"), ("black", "bl", "the color of coal"),
         ("glass", "gl", "you drink from it"), ("sled", "sl", "you ride it on snow"),
         ("twin", "tw", "one of two babies born together"), ("blue", "bl", "the color of the sky"),
         ("crown", "cr", "a king wears it"), ("stamp", "st", "you put it on a letter"),
         ("snow", "sn", "white and cold, falls in winter"), ("skate", "sk", "you glide on ice with these")]
BLEND_SET = ["fr", "fl", "cl", "pl", "sl", "br", "cr", "dr", "gr", "tr", "st", "sm", "sn", "sp", "sw", "bl", "gl", "tw", "sk"]
FAM = {"at": ["c", "b", "h", "m", "r", "s", "f", "p"], "an": ["c", "f", "m", "p", "r", "v", "t"],
       "ig": ["b", "d", "p", "w", "f", "j"], "op": ["h", "m", "t", "p"], "ug": ["b", "h", "m", "r", "j", "d"],
       "ack": ["b", "p", "s", "bl", "tr"], "ell": ["b", "t", "w", "s", "sh"], "ill": ["h", "f", "m", "w", "sp"],
       "ake": ["c", "l", "m", "t", "b", "sn"], "ight": ["l", "n", "r", "br", "f"]}

NOUNS = ["dog", "girl", "teacher", "park", "ball", "school", "cat", "farm", "book", "baby", "doctor", "chair",
         "bird", "beach", "cup", "horse", "tree", "hat", "store", "boy"]
VERBS = ["run", "jump", "swim", "eat", "sing", "read", "write", "play", "climb", "draw", "sleep", "walk",
         "dance", "laugh", "throw", "kick", "hop", "skip"]
ADDS = ["cat", "dog", "book", "bird", "hat", "cup", "tree", "car", "pen", "kite", "frog", "desk"]
ES = [("box", "boxes"), ("bus", "buses"), ("dish", "dishes"), ("watch", "watches"), ("fox", "foxes"),
      ("glass", "glasses"), ("brush", "brushes"), ("church", "churches"), ("kiss", "kisses"), ("wish", "wishes")]
IES = [("baby", "babies"), ("puppy", "puppies"), ("city", "cities"), ("fly", "flies"), ("lady", "ladies"),
       ("berry", "berries"), ("story", "stories"), ("penny", "pennies"), ("party", "parties"), ("bunny", "bunnies")]
IRR = [("child", "children"), ("man", "men"), ("woman", "women"), ("foot", "feet"), ("tooth", "teeth"),
       ("mouse", "mice"), ("goose", "geese"), ("sheep", "sheep"), ("fish", "fish"), ("deer", "deer"),
       ("person", "people"), ("leaf", "leaves"), ("wolf", "wolves"), ("knife", "knives")]

SENTS = ["The cat sleeps on the bed", "I like to read books", "Mom made a big cake", "We play in the park",
         "The sun is hot", "Birds can fly", "My dog loves to run", "She has a red hat",
         "The boy kicked the ball", "Dad drives a blue truck", "Fish swim in the sea", "We eat lunch at noon",
         "The baby is asleep", "Rain fell all day", "I can jump high", "The bus is late",
         "Ben draws a picture", "Leaves fall in autumn", "The girl sang a song", "We went to the zoo"]
FRAGS = ["The big brown dog", "Runs very fast", "In the park", "My best friend", "Under the table",
         "Eating a red apple", "A cold glass of milk", "Jumped over the log", "On a sunny day",
         "The little yellow bird", "Plays with a ball", "Next to the door", "Sleeping on the couch",
         "After school today", "The tall green tree"]
STMT = ["The dog is big", "We went to the park", "I like pizza", "My mom is a nurse", "Birds build nests",
        "School starts at eight", "The moon is bright", "Ben has a new bike", "Snow is cold", "I love my cat"]
QUEST = ["Where is my hat", "What is your name", "Can you swim", "Do you like pizza", "How old are you",
         "Who is at the door", "Is it time for lunch", "Why is the sky blue", "Which book is yours", "When does the show start"]
EXCL = ["Wow, that is huge", "Watch out", "I won the race", "Happy birthday", "Stop that", "What a great day",
        "Look at that rainbow", "Hooray, we did it", "Ouch, that hurt", "I can not believe it"]

ANT = [("hot", "cold"), ("big", "small"), ("up", "down"), ("fast", "slow"), ("happy", "sad"), ("day", "night"),
       ("open", "close"), ("hard", "soft"), ("wet", "dry"), ("old", "new"), ("full", "empty"), ("in", "out"),
       ("long", "short"), ("loud", "quiet"), ("near", "far"), ("clean", "dirty"), ("early", "late"),
       ("heavy", "light"), ("thick", "thin"), ("start", "stop"), ("win", "lose"), ("push", "pull"),
       ("buy", "sell"), ("laugh", "cry"), ("rich", "poor"), ("always", "never"), ("first", "last"),
       ("top", "bottom"), ("front", "back"), ("inside", "outside"), ("come", "go"), ("give", "take"),
       ("sweet", "sour"), ("smooth", "rough"), ("awake", "asleep"), ("deep", "shallow"), ("strong", "weak")]
SYN = [("big", "large"), ("little", "small"), ("glad", "happy"), ("quick", "fast"), ("start", "begin"),
       ("finish", "end"), ("pretty", "lovely"), ("shout", "yell"), ("smart", "clever"), ("angry", "mad"),
       ("stone", "rock"), ("tired", "sleepy"), ("scared", "afraid"), ("unhappy", "sad"), ("shut", "close"),
       ("kid", "child"), ("talk", "speak"), ("nice", "kind"), ("silent", "quiet"), ("huge", "giant"),
       ("jump", "leap"), ("sofa", "couch"), ("mend", "fix"), ("grin", "smile"), ("chilly", "cold"),
       ("simple", "easy"), ("hurry", "rush"), ("giggle", "laugh")]
COMP = [("sun", "flower"), ("rain", "bow"), ("tooth", "brush"), ("foot", "ball"), ("butter", "fly"),
        ("cup", "cake"), ("snow", "man"), ("base", "ball"), ("bed", "room"), ("back", "pack"), ("air", "plane"),
        ("star", "fish"), ("door", "bell"), ("pop", "corn"), ("fire", "fly"), ("sail", "boat"), ("sand", "box"),
        ("hair", "cut"), ("play", "ground"), ("news", "paper"), ("sea", "shell"), ("gold", "fish"),
        ("rain", "coat"), ("bird", "house"), ("moon", "light"), ("pan", "cake"), ("blue", "berry"), ("tooth", "paste")]

REG = {"add ed": [("walk", "walked"), ("jump", "jumped"), ("play", "played"), ("clean", "cleaned"),
                  ("look", "looked"), ("help", "helped"), ("paint", "painted"), ("want", "wanted"),
                  ("wash", "washed"), ("kick", "kicked"), ("open", "opened"), ("call", "called")],
       "drop e": [("bake", "baked"), ("like", "liked"), ("smile", "smiled"), ("dance", "danced"),
                  ("love", "loved"), ("save", "saved"), ("hope", "hoped"), ("race", "raced"), ("move", "moved")],
       "double": [("hop", "hopped"), ("stop", "stopped"), ("clap", "clapped"), ("plan", "planned"),
                  ("skip", "skipped"), ("drop", "dropped"), ("grab", "grabbed"), ("nod", "nodded")],
       "y to ied": [("cry", "cried"), ("try", "tried"), ("carry", "carried"), ("hurry", "hurried"),
                    ("worry", "worried"), ("study", "studied"), ("copy", "copied"), ("marry", "married")]}
IRRV = [("go", "went", "goed"), ("run", "ran", "runned"), ("eat", "ate", "eated"), ("see", "saw", "seed"),
        ("come", "came", "comed"), ("give", "gave", "gived"), ("take", "took", "taked"), ("make", "made", "maked"),
        ("sit", "sat", "sitted"), ("swim", "swam", "swimmed"), ("write", "wrote", "writed"),
        ("sing", "sang", "singed"), ("drink", "drank", "drinked"), ("fall", "fell", "falled"),
        ("get", "got", "getted"), ("find", "found", "finded"), ("buy", "bought", "buyed"), ("say", "said", "sayed"),
        ("tell", "told", "telled"), ("draw", "drew", "drawed"), ("fly", "flew", "flyed"), ("grow", "grew", "growed"),
        ("know", "knew", "knowed"), ("ride", "rode", "rided"), ("sleep", "slept", "sleeped")]
CONTR = [("do not", "don't"), ("is not", "isn't"), ("can not", "can't"), ("will not", "won't"), ("I am", "I'm"),
         ("he is", "he's"), ("she is", "she's"), ("it is", "it's"), ("we are", "we're"), ("they are", "they're"),
         ("you are", "you're"), ("I will", "I'll"), ("let us", "let's"), ("did not", "didn't"),
         ("was not", "wasn't"), ("are not", "aren't"), ("could not", "couldn't"), ("I have", "I've"),
         ("we will", "we'll"), ("that is", "that's")]
PRE = [("un", "happy", "unhappy"), ("un", "lock", "unlock"), ("un", "fair", "unfair"), ("un", "kind", "unkind"),
       ("un", "tie", "untie"), ("un", "do", "undo"), ("un", "safe", "unsafe"), ("un", "clear", "unclear"),
       ("re", "write", "rewrite"), ("re", "play", "replay"), ("re", "fill", "refill"), ("re", "paint", "repaint"),
       ("re", "build", "rebuild"), ("re", "heat", "reheat"), ("re", "use", "reuse"), ("re", "read", "reread")]
SUF = [("help", "ful", "helpful"), ("care", "ful", "careful"), ("joy", "ful", "joyful"),
       ("color", "ful", "colorful"), ("thank", "ful", "thankful"), ("care", "less", "careless"),
       ("hope", "less", "hopeless"), ("help", "less", "helpless"), ("teach", "er", "teacher"),
       ("farm", "er", "farmer"), ("paint", "er", "painter"), ("sing", "er", "singer"),
       ("jump", "er", "jumper"), ("play", "er", "player"), ("fear", "less", "fearless"), ("play", "ful", "playful")]

ADJ = ["red", "big", "tiny", "soft", "loud", "sweet", "sour", "shiny", "round", "sticky", "cold", "fuzzy",
       "sharp", "tall", "happy", "spicy", "yellow", "heavy"]
ADJN = ["apple", "pillow", "ball", "drum", "candy", "star", "lemon", "kitten", "pin", "tree", "cookie", "balloon",
        "cake", "box", "coin", "bear"]
ADJCLOZE = [("The soup is ____.", "hot", "jump"), ("I ate a ____ apple.", "red", "ran"),
            ("The ____ elephant walked slowly.", "huge", "quick?"), ("My bed is very ____.", "soft", "sing"),
            ("The ____ lemon made me frown.", "sour", "dig"), ("The ____ drum woke the baby.", "loud", "swim"),
            ("A ____ kitten sat on my lap.", "fluffy", "eat"), ("The ____ ice made my hand numb.", "cold", "jump"),
            ("She wore a ____ dress.", "pretty", "run"), ("The ____ star twinkled all night.", "bright", "hop"),
            ("I have a ____ puppy.", "tiny", "walk"), ("The ____ candy stuck to my teeth.", "sticky", "fly")]
ADJCLOZE = [(s, a, b if b != "quick?" else "sleep") for s, a, b in ADJCLOZE]
COMPAR = [("tall", "taller", "tallest"), ("big", "bigger", "biggest"), ("small", "smaller", "smallest"),
          ("fast", "faster", "fastest"), ("long", "longer", "longest"), ("hot", "hotter", "hottest"),
          ("happy", "happier", "happiest"), ("funny", "funnier", "funniest"), ("kind", "kinder", "kindest"),
          ("old", "older", "oldest"), ("cold", "colder", "coldest"), ("young", "younger", "youngest")]
HOMO = [("I can ____ a bird in the tree.", "see", "sea"), ("We swam in the ____.", "sea", "see"),
        ("The ____ is shining.", "sun", "son"), ("Her ____ is in third grade.", "son", "sun"),
        ("I ____ the answer.", "know", "no"), ("There is ____ milk left.", "no", "know"),
        ("Please ____ your name.", "write", "right"), ("Turn ____ at the corner.", "right", "write"),
        ("Can you ____ the music?", "hear", "here"), ("Come ____ and sit down.", "here", "hear"),
        ("The wind ____ my hat off.", "blew", "blue"), ("The sky is ____.", "blue", "blew"),
        ("The dog wagged its ____.", "tail", "tale"), ("I read a fairy ____.", "tale", "tail"),
        ("Let us ____ at the gate.", "meet", "meat"), ("We eat ____ for dinner.", "meat", "meet"),
        ("Our team ____ the game.", "won", "one"), ("I have ____ brother.", "one", "won"),
        ("I ____ an apple.", "ate", "eight"), ("She is ____ years old.", "eight", "ate"),
        ("Please ____ for me.", "wait", "weight"), ("The ____ of the box is heavy.", "weight", "wait"),
        ("I ate a juicy ____.", "pear", "pair"), ("I have a new ____ of shoes.", "pair", "pear"),
        ("I ____ my bike to school.", "rode", "road"), ("The ____ is long and straight.", "road", "rode"),
        ("A ____ lives in the forest.", "deer", "dear"), ("____ Grandma, I love you.", "Dear", "Deer"),
        ("I have ____ cats.", "two", "too"), ("I want to go, ____.", "too", "to"),
        ("We walk ____ school.", "to", "too"), ("The kids put on ____ coats.", "their", "there"),
        ("Look over ____.", "there", "their")]
MULTI = [("The bat flew out of the dark cave.", "bat", "a flying animal", "a stick for hitting a ball", 0),
         ("He swung the bat and hit the ball.", "bat", "a flying animal", "a stick for hitting a ball", 1),
         ("The dog's bark is loud.", "bark", "the sound a dog makes", "the outside of a tree", 0),
         ("The bark of the tree is rough.", "bark", "the sound a dog makes", "the outside of a tree", 1),
         ("I wear my watch on my wrist.", "watch", "to look at", "a small clock you wear", 1),
         ("Please watch the baby.", "watch", "to look at", "a small clock you wear", 0),
         ("The duck swam in the pond.", "duck", "a bird", "to bend down quickly", 0),
         ("Duck! The ball is coming!", "duck", "a bird", "to bend down quickly", 1),
         ("Please turn on the light.", "light", "not heavy", "what lets you see", 1),
         ("The box is light.", "light", "not heavy", "what lets you see", 0),
         ("She will ring the bell.", "ring", "jewelry for a finger", "to make a bell sound", 1),
         ("He gave her a gold ring.", "ring", "jewelry for a finger", "to make a bell sound", 0),
         ("I put the soup in a can.", "can", "a metal container", "is able to", 0),
         ("I can swim.", "can", "a metal container", "is able to", 1),
         ("Flowers bloom in spring.", "spring", "a season", "a metal coil", 0),
         ("The toy has a metal spring.", "spring", "a season", "a metal coil", 1),
         ("A fly sat on my food.", "fly", "to move through the air", "a small insect", 1),
         ("Birds fly south in winter.", "fly", "to move through the air", "a small insect", 0),
         ("Turn left at the corner.", "left", "the opposite of right", "went away from", 0),
         ("She left her book at school.", "left", "the opposite of right", "went away from", 1)]
CONTEXT = [("The enormous elephant was as big as a house.", "enormous", "very big", "very small"),
           ("The soup was scalding. I burned my tongue.", "scalding", "very hot", "very cold"),
           ("Mia was weary after the long walk, so she fell asleep.", "weary", "tired", "excited"),
           ("The room was silent. You could not hear a sound.", "silent", "quiet", "loud"),
           ("Ben was famished. He had not eaten all day.", "famished", "very hungry", "very sleepy"),
           ("The path was narrow, so only one person could walk at a time.", "narrow", "not wide", "very long"),
           ("The baby was delighted when she saw the puppy.", "delighted", "very happy", "angry"),
           ("It was a gloomy day. The sky was dark and gray.", "gloomy", "dark and dull", "bright and sunny"),
           ("He sprinted across the field because he was late.", "sprinted", "ran fast", "walked slowly"),
           ("The seed will sprout and grow into a plant.", "sprout", "begin to grow", "fall down"),
           ("The puppy was timid and hid behind the chair.", "timid", "shy and scared", "loud and wild"),
           ("Dad was furious when the glass broke.", "furious", "very angry", "very proud")]


# ====================================================================== units
def U1(day, rng, v):
    t = "Alphabet, Vowels & ABC Order"
    if day == 1:
        rows = []
        for _ in range(7):
            s = rng.randint(0, 17)
            L = [chr(97 + s + i) for i in range(8)]
            idx = sorted(rng.sample(range(1, 8), 2))
            rows.append(([None if i in idx else l for i, l in enumerate(L)], ", ".join(L[i] for i in idx)))

        def g():
            x = rng.randint(1, 24)
            L = chr(97 + x)
            if rng.random() < .5:
                return f"What letter comes after {L}?  ____", chr(98 + x)
            return f"What letter comes before {L}?  ____", chr(96 + x)
        return sheet(1, 1, t, "Write the missing letters. Then answer the questions.", "Example: a, b, __, d  " + ARROW + "  c",
                     [sec("Part A – Missing letters", "seq", rows, 1, 36),
                      sec("Part B – Before and after", "eq", uniq(g, 12), 2, 30)])
    if day == 2:
        ls = take(list("abcdefghijklmnopqrstuvwxyz"), 20, v, "u1d2")

        def cap(i, L):
            return (f"Write the capital letter for {L}:  ____", L.upper()) if i % 2 == 0 else \
                   (f"Write the small letter for {L.upper()}:  ____", L)
        a = [cap(i, L) for i, L in enumerate(ls)]
        vc = [(f"Is the letter '{L}' a vowel or a consonant?  ____", "vowel" if L in VOWELS else "consonant")
              for L in take(list("abcdefghijklmnopqrstuvwxyz"), 10, v, "u1d2b")]
        return sheet(1, 2, t, "Capital and small letters. The vowels are a, e, i, o, u.",
                     "Example: the capital letter for g is G", [sec("Part A – Capital & small letters", "eq", a, 2, 30),
                                                            sec("Part B – Vowel or consonant?", "eq", vc, 2, 30)])
    if day == 3:
        w1 = take(CVC, 12, v, "u1d3a")
        w2 = take(CVC, 12, v, "u1d3b")
        a = [(f"____{w[1:]}   ({c})", w[0]) for w, c in w1]
        b = [(f"{w[:2]}____   ({c})", w[2]) for w, c in w2]
        return sheet(1, 3, t, "Read the clue. Write the missing letter to finish the word.",
                     "Example: ____og (a pet that barks)  " + ARROW + "  d", [sec("Part A – First letter", "eq", a, 2, 30),
                                                                           sec("Part B – Last letter", "eq", b, 2, 30)])
    pool = ["cat", "ant", "bee", "dog", "egg", "fish", "goat", "hat", "ice", "jam", "kite", "lion", "moon", "nest",
            "owl", "pig", "queen", "rain", "sun", "tree", "van", "web", "yak", "zoo", "apple", "bird", "cake"]
    if day == 4:
        a = []
        for ws in [rng.sample(pool, 3) for _ in range(8)]:
            a.append((f"{', '.join(ws)}   " + ARROW + "   ____ , ____ , ____", ", ".join(sorted(ws))))
        b = []
        for _ in range(8):
            x, y = rng.sample(pool, 2)
            b.append((f"Which comes first in ABC order: {x} or {y}?  ____", min(x, y)))
        return sheet(1, 4, t, "Put the words in ABC order. Look at the first letter.",
                     "Example: cat, ant, bee  " + ARROW + "  ant, bee, cat",
                     [sec("Part A – Three words", "eq", a, 1, 30), sec("Part B – Which comes first?", "eq", b, 2, 30)])
    seqs = []
    for _ in range(3):
        s = rng.randint(0, 17)
        L = [chr(97 + s + i) for i in range(8)]
        idx = sorted(rng.sample(range(1, 8), 3))
        seqs.append(([None if i in idx else l for i, l in enumerate(L)], ", ".join(L[i] for i in idx)))
    vc = [(f"Is '{L}' a vowel or a consonant?  ____", "vowel" if L in VOWELS else "consonant")
          for L in take(list("abcdefghijklmnopqrstuvwxyz"), 6, v, "u1d5")]
    abc3 = [(f"{', '.join(ws)}   " + ARROW + "   ____ , ____ , ____", ", ".join(sorted(ws)))
            for ws in [rng.sample(pool, 3) for _ in range(4)]]
    groups = [("bat", "bag", "bed"), ("cap", "cat", "cow"), ("dig", "dog", "dot"), ("hat", "hen", "hug"),
              ("man", "map", "mop"), ("pan", "pen", "pig"), ("sad", "sit", "sun"), ("tap", "tin", "top")]
    same = []
    for g_ in take(groups, 3, v, "u1d5g"):
        sh = list(g_)
        rng.shuffle(sh)
        same.append((f"{', '.join(sh)}   " + ARROW + "   ____ , ____ , ____", ", ".join(sorted(g_))))
    return sheet(1, 5, t, "Review day! Letters, vowels and ABC order.", "Example: bat, bag, bed  " + ARROW + "  bag, bat, bed",
                 [sec("Part A – Missing letters", "seq", seqs, 1, 36), sec("Part B – Vowel or consonant?", "eq", vc, 2, 30),
                  sec("Part C – ABC order", "eq", abc3, 1, 30),
                  sec("Part D – Same first letter: look at the second letter", "eq", same, 1, 30)])


def U2(day, rng, v):
    t = "Short & Long Vowels"
    if day == 1:
        a = [(f"{w[0]}__{w[2]}   ({c})", w[1]) for w, c in take(CVC, 16, v, "u2d1a")]
        b = []
        for k, x in enumerate(take(list(VOWELS) * 2, 8, v, "u2d1b")):
            good = rng.choice(SHORT[x])
            other = rng.choice([o for o in VOWELS if o != x])
            bad = rng.choice(SHORT[other])
            opts = [good, bad]
            rng.shuffle(opts)
            b.append((f"Which word has the short {x} sound?  ({opts[0]} / {opts[1]})  ____", good))
        return sheet(2, 1, t, "Short vowels say their little sounds: a (cat), e (bed), i (pig), o (pot), u (sun).",
                     "Example: c__t (a pet that purrs)  " + ARROW + "  a",
                     [sec("Part A – Fill in the vowel", "eq", a, 2, 30), sec("Part B – Which word?", "eq", b, 1, 30)])
    if day == 2:
        a = [(f"{s} + e = ____", l) for s, l in take(PAIRS, 14, v, "u2d2a")]
        lw = take(LONGW, 6, v, "u2d2b")
        sw = take(SHORTW, 6, v, "u2d2c")
        items = [(f"Does '{w}' have a long or short vowel sound?  ____", "long") for w in lw] + \
                [(f"Does '{w}' have a long or short vowel sound?  ____", "short") for w in sw]
        rng.shuffle(items)
        return sheet(2, 2, t, "A silent e at the end makes the vowel say its name.", "Example: cap + e = cape",
                     [sec("Part A – Add the silent e", "eq", a, 2, 30), sec("Part B – Long or short?", "eq", items, 1, 30)])
    if day == 3:
        c = []
        for w, team, clue in take(VT, 16, v, "u2d3"):
            other = rng.choice([x for x in ["ai", "ay", "ee", "ea", "oa"] if x != team])
            opts = [team, other]
            rng.shuffle(opts)
            c.append((f"{w.replace(team, '__', 1)}   ({clue})   [{opts[0]} / {opts[1]}]", team))
        return sheet(2, 3, t, "Two vowels can work together: ai, ay, ee, ea, oa. Pick the right pair.",
                     "Example: r__n (water from clouds) [ai / ay]  " + ARROW + "  ai  (rain)", [sec("", "eq", c, 1, 30)])
    if day == 4:
        c = []
        for s, good, bad in take(LONGCLOZE, 20, v, "u2d4"):
            o = [good, bad]
            rng.shuffle(o)
            c.append((f"{s}  ({o[0]} / {o[1]})", good))
        return sheet(2, 4, t, "Pick the correctly spelled word to finish each sentence.",
                     "Example: Mom will bake a ____. (cak / cake)  " + ARROW + "  cake", [sec("", "eq", c, 1, 30)])
    scr = []
    for w in take(LONGW + ["rain", "boat", "tree", "play"], 10, v, "u2d5"):
        ch = list(w)
        for _ in range(20):
            rng.shuffle(ch)
            if "".join(ch) != w:
                break
        scr.append((f"{''.join(ch)}   " + ARROW + "   ____", w))
    sl = [(f"Does '{w}' have a long or short vowel sound?  ____", "long" if w in LONGW else "short")
          for w in take(LONGW + SHORTW, 6, v, "u2d5b")]
    c = []
    for s, good, bad in take(LONGCLOZE, 4, v, "u2d5c"):
        o = [good, bad]
        rng.shuffle(o)
        c.append((f"{s}  ({o[0]} / {o[1]})", good))
    return sheet(2, 5, t, "Review day! Unscramble the words, then read and choose.", "Example: kaec  " + ARROW + "  cake",
                 [sec("Part A – Unscramble", "eq", scr, 2, 30), sec("Part B – Long or short?", "eq", sl, 1, 30),
                  sec("Part C – Choose the word", "eq", c, 1, 30)])


def _blank(word, part):
    return word.replace(part, "__", 1)


def U3(day, rng, v):
    t = "Blends, Digraphs & Word Families"
    if day == 1:
        c = []
        for w, d, clue in take(DIG, 20, v, "u3d1"):
            opts = [d] + rng.sample([x for x in ["sh", "ch", "th", "wh", "ck"] if x != d], 2)
            rng.shuffle(opts)
            c.append((f"{_blank(w, d)}   ({clue})   [{' / '.join(opts)}]", d))
        return sheet(3, 1, t, "Two letters can make one sound: sh, ch, th, wh, ck. Pick the pair that finishes the word.",
                     "Example: __ip (sails on the sea) [sh / ch / th]  " + ARROW + "  sh  (ship)", [sec("", "eq", c, 1, 30)])
    if day == 2:
        c = []
        for w, b_, clue in take(BLEND, 20, v, "u3d2"):
            opts = [b_] + rng.sample([x for x in BLEND_SET if x != b_], 2)
            rng.shuffle(opts)
            c.append((f"{_blank(w, b_)}   ({clue})   [{' / '.join(opts)}]", b_))
        return sheet(3, 2, t, "Blends are two letters that keep their own sounds. Pick the blend that finishes the word.",
                     "Example: __og (a green animal that hops) [fr / bl / st]  " + ARROW + "  fr  (frog)",
                     [sec("", "eq", c, 1, 30)])
    allw = [(o, r) for r, os in FAM.items() for o in os]
    if day == 3:
        c = [(f"{o} + {r} = ____", o + r) for o, r in take(allw, 30, v, "u3d3")]
        return sheet(3, 3, t, "Add the first sound (onset) to the word family to make a new word.",
                     "Example: c + at = cat", [sec("", "eq", c, 3, 30)])

    def rhyme(key, n):
        out = []
        for r_, o_ in take([(r, o) for r, os in FAM.items() for o in os], n, v, key):
            fam_words = [x + r_ for x in FAM[r_]]
            target = o_ + r_
            same = rng.choice([w for w in fam_words if w != target])
            other_r = rng.choice([r for r in FAM if r != r_])
            diff = rng.choice(FAM[other_r]) + other_r
            opts = [same, diff]
            rng.shuffle(opts)
            out.append((f"Which word rhymes with {target}?  ({opts[0]} / {opts[1]})  ____", same))
        return out
    if day == 4:
        return sheet(3, 4, t, "Words that rhyme end with the same sounds. Circle the rhyme.",
                     "Example: Which word rhymes with cat? (hat / hot)  " + ARROW + "  hat",
                     [sec("", "eq", rhyme("u3d4", 20), 2, 30)])
    dg = []
    for w, d, clue in take(DIG, 6, v, "u3d5a"):
        opts = [d] + rng.sample([x for x in ["sh", "ch", "th", "wh", "ck"] if x != d], 2)
        rng.shuffle(opts)
        dg.append((f"{_blank(w, d)}   ({clue})   [{' / '.join(opts)}]", d))
    bl = []
    for w, b_, clue in take(BLEND, 6, v, "u3d5b"):
        opts = [b_] + rng.sample([x for x in BLEND_SET if x != b_], 2)
        rng.shuffle(opts)
        bl.append((f"{_blank(w, b_)}   ({clue})   [{' / '.join(opts)}]", b_))
    bw = [(f"{o} + {r} = ____", o + r) for o, r in take(allw, 6, v, "u3d5c")]
    return sheet(3, 5, t, "Review day! Digraphs, blends, word families and rhymes.", "Example: b + ack = back",
                 [sec("Part A – Digraphs", "eq", dg, 1, 30), sec("Part B – Blends", "eq", bl, 1, 30),
                  sec("Part C – Word families", "eq", bw, 3, 30), sec("Part D – Rhymes", "eq", rhyme("u3d5d", 4), 2, 30)])


def _plural_items(bank, n, v, key, mode):
    out = []
    for w in take(bank, n, v, key):
        if mode == "s":
            out.append((f"one {w}, two ____", w + "s"))
        else:
            out.append((f"one {w[0]}, two ____", w[1]))
    return out


def U4(day, rng, v):
    t = "Nouns, Verbs & Plurals"
    if day == 1:
        items = [(f"Is '{w}' a noun or a verb?  ____", "noun") for w in take(NOUNS, 12, v, "u4d1a")] + \
                [(f"Is '{w}' a verb or a noun?  ____", "verb") for w in take(VERBS, 12, v, "u4d1b")]
        rng.shuffle(items)
        return sheet(4, 1, t, "A noun is a person, place or thing. A verb is an action word.",
                     "Example: dog = noun (a thing/animal); run = verb (an action)", [sec("", "eq", items, 2, 30)])

    def sentence():
        adj = rng.choice(["big", "little", "happy", "sleepy", "funny", "brown"])
        n = rng.choice(["dog", "cat", "girl", "boy", "bird", "horse", "baby", "teacher"])
        vb = rng.choice(["runs", "jumps", "sings", "eats", "swims", "walks", "plays", "reads"])
        tl = rng.choice(["fast", "high", "loudly", "in the park", "at school", "on the grass"])
        return f"The {adj} {n} {vb} {tl}.", n, vb
    if day == 2:
        ss = uniq(lambda: ((lambda s: (s[0], s))(sentence())), 16)
        a = [(f"{s[0]}   Noun: ____", s[1][1]) for s in ss[:8]]
        b = [(f"{s[0]}   Verb: ____", s[1][2]) for s in ss[8:]]
        return sheet(4, 2, t, "Read each sentence. Find the noun or the verb.", "Example: The big dog runs fast.  Noun: dog   Verb: runs",
                     [sec("Part A – Find the noun", "eq", a, 1, 30), sec("Part B – Find the verb", "eq", b, 1, 30)])
    if day == 3:
        a = _plural_items(ADDS, 8, v, "u4d3a", "s")
        b = [(f"one {w}, two ____", p) for w, p in take(ES, 8, v, "u4d3b")]
        c = [(f"one {w}, two ____", p) for w, p in take(IES, 8, v, "u4d3c")]
        return sheet(4, 3, t, "Plural means more than one. Add -s, add -es, or change y to ies.", "Example: one box, two boxes",
                     [sec("Part A – Add -s", "eq", a, 2, 30), sec("Part B – Add -es (s, x, ch, sh endings)", "eq", b, 2, 30),
                      sec("Part C – Change y to ies", "eq", c, 2, 30)])
    if day == 4:
        a = [(f"one {w}, two ____", p) for w, p in take(IRR, 8, v, "u4d4a")]
        mix = []
        for w, p in take(ES + IES, 12, v, "u4d4b"):
            mix.append((f"one {w}, two ____", p))
        return sheet(4, 4, t, "Some plurals change in a special way. Learn them by heart!", "Example: one child, two children",
                     [sec("Part A – Special plurals", "eq", a, 2, 30), sec("Part B – Mixed plurals", "eq", mix, 2, 30)])
    nv = [(f"Is '{w}' a noun or a verb?  ____", "noun") for w in take(NOUNS, 4, v, "u4d5a")] + \
         [(f"Is '{w}' a noun or a verb?  ____", "verb") for w in take(VERBS, 4, v, "u4d5b")]
    rng.shuffle(nv)
    pl = [(f"one {w}, two ____", p) for w, p in take(ES + IES + IRR, 8, v, "u4d5c")] + \
         [(f"one {w}, two ____", w + "s") for w in take(ADDS, 4, v, "u4d5d")]
    ss = uniq(lambda: ((lambda s: (s[0], s))(sentence())), 4)
    vb = [(f"{s[0]}   Verb: ____", s[1][2]) for s in ss]
    return sheet(4, 5, t, "Review day! Nouns, verbs and plurals.", "Example: one fly, two flies",
                 [sec("Part A – Noun or verb?", "eq", nv, 2, 30), sec("Part B – Plurals", "eq", pl, 2, 30),
                  sec("Part C – Find the verb", "eq", vb, 1, 30)])


NAMES = ["mia", "leo", "ava", "sam", "zoe", "ben", "lily", "max"]
PHR = ["has a red hat", "likes to swim", "went to the park", "can run fast", "reads a book", "plays with a ball"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = ["january", "march", "may", "june", "july", "august", "october", "december"]
CITIES = ["chicago", "dallas", "boston", "denver", "paris", "london"]


def _cap(s):
    return s[0].upper() + s[1:]


def _caps_item(rng):
    k = rng.choice("abcde")
    n = rng.choice(NAMES)
    if k == "a":
        c = f"{_cap(n)} {rng.choice(PHR)}."
    elif k == "b":
        c = f"We go to school on {_cap(rng.choice(DAYS))}."
    elif k == "c":
        c = f"My birthday is in {_cap(rng.choice(MONTHS))}."
    elif k == "d":
        c = f"{_cap(n)} lives in {_cap(rng.choice(CITIES))}."
    else:
        c = f"Today {_cap(n)} and I {rng.choice(['play', 'read', 'swim', 'draw'])} together."
        c = c.replace(" and I ", " and I ")
    return f"Rewrite with capital letters:  {c.lower()}", c


def _unscramble(bank, n, v, key, rng):
    out = []
    for s in take(bank, n, v, key):
        w = s.split()
        sh = list(w)
        for _ in range(20):
            rng.shuffle(sh)
            if sh != w:
                break
        out.append((f"Put the words in order:  {' / '.join(x.lower() if i else x.lower() for i, x in enumerate(sh))}", s + "."))
    return out


def U5(day, rng, v):
    t = "Sentences & Punctuation"
    if day == 1:
        c = [(f"{s}   Is this a complete sentence?  ____", "yes") for s in take(SENTS, 12, v, "u5d1a")] + \
            [(f"{s}   Is this a complete sentence?  ____", "no") for s in take(FRAGS, 12, v, "u5d1b")]
        rng.shuffle(c)
        return sheet(5, 1, t, "A sentence tells a whole idea: who or what, and what happens. Write yes or no.",
                     "Example: The cat sleeps on the bed  " + ARROW + "  yes     In the park  " + ARROW + "  no",
                     [sec("", "eq", c, 1, 30)])
    if day == 2:
        c = uniq(lambda: _caps_item(rng), 10)
        return sheet(5, 2, t, "Use capital letters for the first word, names, days, months, places, and the word I.",
                     "Example: mia lives in paris.  " + ARROW + "  Mia lives in Paris.", [qlines(c, 50)])
    if day == 3:
        items = [(f"{s} ____", ".") for s in take(STMT, 8, v, "u5d3a")] + \
                [(f"{s} ____", "?") for s in take(QUEST, 8, v, "u5d3b")] + \
                [(f"{s} ____", "!") for s in take(EXCL, 8, v, "u5d3c")]
        rng.shuffle(items)
        return sheet(5, 3, t, "Add the end mark: a period (.), a question mark (?) or an exclamation mark (!).",
                     "Example: Where is my hat ?  " + ARROW + "  ?", [sec("", "eq", items, 2, 30)])
    if day == 4:
        return sheet(5, 4, t, "Put the words in order to make a sentence. Start with a capital and end with a period.",
                     "Example: dog / the / barks  " + ARROW + "  The dog barks.",
                     [qlines(_unscramble(SENTS, 10, v, "u5d4", rng), 50)])
    c = [(f"{s}   Complete sentence?  ____", "yes") for s in take(SENTS, 3, v, "u5d5a")] + \
        [(f"{s}   Complete sentence?  ____", "no") for s in take(FRAGS, 3, v, "u5d5b")]
    rng.shuffle(c)
    p = [(f"{s} ____", ".") for s in take(STMT, 3, v, "u5d5c")] + [(f"{s} ____", "?") for s in take(QUEST, 3, v, "u5d5d")] + \
        [(f"{s} ____", "!") for s in take(EXCL, 2, v, "u5d5e")]
    rng.shuffle(p)
    return sheet(5, 5, t, "Review day! Sentences, end marks, capitals and word order.",
                 "Example: Do you like pizza ?  " + ARROW + "  ?",
                 [sec("Part A – Complete sentence?", "eq", c, 1, 30), sec("Part B – End marks", "eq", p, 2, 30),
                  sec("Part C – Capital letters", "qline", uniq(lambda: _caps_item(rng), 3), 1, 50),
                  sec("Part D – Word order", "qline", _unscramble(SENTS, 3, v, "u5d5f", rng), 1, 50)])


def _opt(rng, good, pool, avoid):
    bad = rng.choice([x for x in pool if x not in avoid and x != good])
    o = [good, bad]
    rng.shuffle(o)
    return o


def _ant_options(rng, v, key, n):
    allw = [w for p in ANT for w in p]
    out = []
    for a, b in take(ANT, n, v, key):
        a, b = (a, b) if rng.random() < .5 else (b, a)
        o = _opt(rng, b, allw, {a})
        out.append((f"The opposite of '{a}' is ____   ({o[0]} / {o[1]})", b))
    return out


def _syn_options(rng, v, key, n):
    allw = [w for p in SYN for w in p] + ["sad", "slow", "cold", "tiny"]
    out = []
    for a, b in take(SYN, n, v, key):
        a, b = (a, b) if rng.random() < .5 else (b, a)
        o = _opt(rng, b, allw, {a})
        out.append((f"Which word means the same as '{a}'?  ({o[0]} / {o[1]})  ____", b))
    return out


def U6(day, rng, v):
    t = "Opposites, Synonyms & Compound Words"
    if day == 1:
        return sheet(6, 1, t, "Opposites mean the reverse. Pick the opposite word.",
                     "Example: The opposite of 'hot' is ____ (cold / small)  " + ARROW + "  cold",
                     [sec("", "eq", _ant_options(rng, v, "u6d1", 20), 1, 30)])
    if day == 2:
        c = []
        for a, b in take(ANT, 20, v, "u6d2"):
            a, b = (a, b) if rng.random() < .5 else (b, a)
            c.append((f"The opposite of '{a}' starts with {b[0]}:  ____", b))
        return sheet(6, 2, t, "Write the opposite. The first letter will help you.",
                     "Example: The opposite of 'hot' starts with c:  " + ARROW + "  cold", [sec("", "eq", c, 1, 30)])
    if day == 3:
        return sheet(6, 3, t, "Synonyms are words that mean almost the same. Pick the synonym.",
                     "Example: Which word means the same as 'big'? (large / sad)  " + ARROW + "  large",
                     [sec("", "eq", _syn_options(rng, v, "u6d3", 20), 1, 30)])
    if day == 4:
        a = [(f"{x} + {y} = ____", x + y) for x, y in take(COMP, 14, v, "u6d4a")]
        b = [(f"{x} + ____ = {x}{y}", y) for x, y in take(COMP, 8, v, "u6d4b")]
        return sheet(6, 4, t, "A compound word is two small words put together.", "Example: sun + flower = sunflower",
                     [sec("Part A – Put them together", "eq", a, 2, 30), sec("Part B – What is missing?", "eq", b, 2, 30)])
    cl = [("It is ____ at night, so we need a light.  (dark / hot)", "dark"),
          ("The rock is ____, not soft.  (hard / wet)", "hard"),
          ("My brother is not tall. He is ____.  (short / loud)", "short"),
          ("The cat is ____, so it sleeps all day.  (sleepy / angry)", "sleepy"),
          ("The ice is ____. It makes my hands numb.  (cold / sweet)", "cold"),
          ("The room was ____. No one made a sound.  (quiet / sticky)", "quiet")]
    return sheet(6, 5, t, "Review day! Opposites, synonyms and compound words.", "Example: sun + flower = sunflower",
                 [sec("Part A – Opposites", "eq", _ant_options(rng, v, "u6d5a", 6), 1, 30),
                  sec("Part B – Synonyms", "eq", _syn_options(rng, v, "u6d5b", 6), 1, 30),
                  sec("Part C – Compound words", "eq", [(f"{x} + {y} = ____", x + y) for x, y in take(COMP, 6, v, "u6d5c")], 2, 30),
                  sec("Part D – Choose the word", "eq", take(cl, 3, v, "u6d5d"), 1, 30)])


def U7(day, rng, v):
    t = "Past Tense, Contractions & Word Endings"
    if day == 1:
        secs = []
        for head, key, n in [("Part A – Add -ed", "add ed", 5), ("Part B – Drop the e, add -ed", "drop e", 4),
                             ("Part C – Double the last letter, add -ed", "double", 4),
                             ("Part D – Change y to i, add -ed", "y to ied", 4)]:
            secs.append(sec(head, "eq", [(f"{a} " + ARROW + " ____ (past)", b) for a, b in take(REG[key], n, v, "u7d1" + key)], 2, 30))
        return sheet(7, 1, t, "Past tense tells what already happened. Most verbs add -ed.", "Example: walk " + ARROW + " walked",
                     secs)
    if day == 2:
        a = [(f"{x} " + ARROW + " ____ (past)", y) for x, y, _ in take(IRRV, 12, v, "u7d2a")]
        b = []
        for x, y, z in take(IRRV, 8, v, "u7d2b"):
            o = [y, z]
            rng.shuffle(o)
            b.append((f"Past of '{x}':  ({o[0]} / {o[1]})  ____", y))
        return sheet(7, 2, t, "Irregular verbs do not add -ed. They change in special ways.", "Example: go " + ARROW + " went",
                     [sec("Part A – Write the past tense", "eq", a, 2, 30), sec("Part B – Which is correct?", "eq", b, 1, 30)])
    if day == 3:
        a = [(f"{x} = ____", y) for x, y in take(CONTR, 12, v, "u7d3a")]
        b = [(f"{y} = ____", x) for x, y in take(CONTR, 12, v, "u7d3b")]
        return sheet(7, 3, t, "A contraction squeezes two words together. An apostrophe (') takes the place of missing letters.",
                     "Example: do not = don't", [sec("Part A – Make a contraction", "eq", a, 2, 30),
                                                  sec("Part B – Write the two words", "eq", b, 2, 30)])
    if day == 4:
        a = [(f"{p} + {w} = ____", r) for p, w, r in take([x for x in PRE if x[0] == "un"], 6, v, "u7d4a")]
        b = [(f"{p} + {w} = ____", r) for p, w, r in take([x for x in PRE if x[0] == "re"], 6, v, "u7d4b")]
        c = [(f"{w} + {s} = ____", r) for w, s, r in take(SUF, 10, v, "u7d4c")]
        return sheet(7, 4, t, "Prefixes go at the start: un- means not, re- means again. Suffixes go at the end.",
                     "Example: un + happy = unhappy;  care + ful = careful",
                     [sec("Part A – Prefix un- (not)", "eq", a, 2, 30), sec("Part B – Prefix re- (again)", "eq", b, 2, 30),
                      sec("Part C – Suffixes -ful, -less, -er", "eq", c, 2, 30)])
    reg = [x for k in REG.values() for x in k]
    a = [(f"{x} " + ARROW + " ____ (past)", y) for x, y in take(reg, 6, v, "u7d5a")]
    b = [(f"{x} " + ARROW + " ____ (past)", y) for x, y, _ in take(IRRV, 6, v, "u7d5b")]
    c = [(f"{x} = ____", y) for x, y in take(CONTR, 6, v, "u7d5c")]
    d = [(f"{p} + {w} = ____", r) for p, w, r in take(PRE, 3, v, "u7d5d")] + [(f"{w} + {s} = ____", r) for w, s, r in take(SUF, 3, v, "u7d5e")]
    return sheet(7, 5, t, "Review day! Past tense, contractions, prefixes and suffixes.", "Example: do not = don't",
                 [sec("Part A – Regular past tense", "eq", a, 2, 30), sec("Part B – Irregular past tense", "eq", b, 2, 30),
                  sec("Part C – Contractions", "eq", c, 2, 30), sec("Part D – Prefixes and suffixes", "eq", d, 2, 30)])


# ---------------------------------------------------------- reading passages
PASSAGES = [
    ("Sam's Hat", "Sam has a red hat. He wears it every day. One windy day, the hat blew away. Sam ran after it. "
     "A girl named Mia caught the hat and gave it back. Sam said, \"Thank you!\"",
     [("What color is Sam's hat?", "red"), ("What happened on the windy day?", "The hat blew away."),
      ("Who caught the hat?", "Mia"), ("What did Sam say to Mia?", "Thank you!"),
      ("True or false: Sam lost his hat forever.", "false")]),
    ("The Little Frog", "A little frog sat on a log. He saw a fly buzzing near the pond. The frog jumped high and caught the fly "
     "with his long tongue. Then he splashed into the water to cool off.",
     [("Where did the frog sit?", "on a log"), ("What did the frog see?", "a fly"),
      ("How did the frog catch the fly?", "with his long tongue"), ("What did the frog do last?", "He splashed into the water."),
      ("Is this story about a frog or a fish?", "a frog")]),
    ("A Rainy Day", "It rained all morning, so Ben and Ava could not play outside. They built a fort with blankets and chairs. "
     "Then they read books inside the fort. When the sun came out, they ran outside to jump in puddles.",
     [("Why could Ben and Ava not play outside?", "It rained."), ("What did they build?", "a fort"),
      ("What did they do inside the fort?", "They read books."), ("What did they do when the sun came out?", "They jumped in puddles."),
      ("How many children are in the story?", "two")]),
    ("Grandma's Garden", "Grandma has a garden behind her house. She plants carrots, beans and tomatoes each spring. Every day she "
     "waters the plants. In summer, Grandma picks the vegetables and makes a big soup for the family.",
     [("Where is the garden?", "behind Grandma's house"), ("When does Grandma plant the seeds?", "in spring"),
      ("What does Grandma do every day?", "She waters the plants."), ("What does she make in summer?", "a big soup"),
      ("Name one vegetable she plants.", "carrots, beans or tomatoes")]),
    ("The Lost Puppy", "Leo found a small puppy near the park. The puppy was wet and shaking. Leo wrapped it in his jacket and carried "
     "it home. His mom helped him put up signs. Two days later, a boy named Omar came to the door. \"That is my dog!\" he said "
     "with a big smile.",
     [("Where did Leo find the puppy?", "near the park"), ("How did the puppy look when Leo found it?", "wet and shaking"),
      ("What did Leo wrap the puppy in?", "his jacket"), ("Who came to the door?", "Omar"),
      ("Which happened first: Leo put up signs, or Leo found the puppy?", "Leo found the puppy."),
      ("How did Omar feel? How do you know?", "Happy (he smiled). Sample answer.")]),
    ("The Science Fair", "Zoe made a volcano for the science fair. She mixed baking soda and vinegar inside it. Foam bubbled out of "
     "the top like red lava. The judges clapped and gave Zoe a blue ribbon.",
     [("What did Zoe make?", "a volcano"), ("What two things did Zoe mix?", "baking soda and vinegar"),
      ("What came out of the top of the volcano?", "foam"), ("Who clapped?", "the judges"),
      ("What prize did Zoe get?", "a blue ribbon"), ("Why do you think the judges clapped?", "They liked the volcano. Sample answer.")]),
    ("Honey Bees", "Honey bees live in a hive. Each bee has a job. Some bees collect nectar from flowers. Others guard the hive or "
     "take care of baby bees. The bees turn nectar into honey. One bee makes only a tiny bit of honey, so the bees must work together.",
     [("Where do honey bees live?", "in a hive"), ("What do bees collect from flowers?", "nectar"),
      ("What do bees make from nectar?", "honey"), ("Why must the bees work together?", "One bee makes only a tiny bit of honey."),
      ("What is the main idea? (a) Bees work together to make honey. (b) Flowers have nectar.", "a")]),
    ("Penguins", "Penguins are birds that cannot fly, but they are great swimmers. Their wings work like flippers. Many penguins live "
     "in cold places in the south. A thick layer of fat and tight feathers keeps them warm. Penguins eat fish and tiny sea animals.",
     [("Can penguins fly?", "no"), ("What do penguin wings work like?", "flippers"),
      ("What keeps penguins warm?", "fat and tight feathers"), ("What do penguins eat?", "fish and tiny sea animals"),
      ("What is the main idea? (a) Penguins are birds that swim instead of fly. (b) Penguins are always cold.", "a")]),
    ("The Big Race", "On Saturday, the school had a race. Max was nervous because he was the smallest runner. At the start, he took a "
     "deep breath. Max ran as fast as he could, but two boys were ahead of him. Near the end, one boy tripped. Max stopped and helped "
     "him up. They crossed the line together. Everyone cheered the loudest for them.",
     [("When was the race?", "on Saturday"), ("Why was Max nervous?", "He was the smallest runner."),
      ("What did Max do when the boy tripped?", "He stopped and helped him up."), ("Did Max win the race?", "no"),
      ("Why did everyone cheer loudly?", "Max was kind and helped. Sample answer."),
      ("Which word describes Max best? (kind / lazy / rude)", "kind")]),
    ("A Walk in the Woods", "Nina and her dad walked in the woods on a cool autumn day. Red and gold leaves covered the path. Nina heard "
     "a tapping sound high in a tree. It was a woodpecker looking for bugs. Her dad whispered, \"Let us stay very still.\" They watched "
     "the bird until it flew away. Nina wanted to come back next weekend.",
     [("What season was it?", "autumn"), ("What covered the path?", "red and gold leaves"),
      ("What made the tapping sound?", "a woodpecker"), ("Why did Dad whisper?", "So they would not scare the bird. Sample answer."),
      ("How did Nina feel at the end?", "Happy / excited (she wanted to come back).")]),
]


def U8(day, rng, v):
    t = "Reading Stories & Comprehension"
    title, text, qs = PASSAGES[(day - 1) * 2 + v]
    instr = ["Read the story carefully. Then answer the questions in complete sentences.",
             "Read the story. Look back at the story to find each answer.",
             "Read the story. Some answers need two or more words.",
             "Read the facts. Then answer the questions. Look for the main idea.",
             "Challenge day! Read carefully and think about why things happen."][day - 1]
    return sheet(8, day, t, instr, "Tip: Underline the answer in the story, then write it on the line.",
                 [passage_sec(title, text), qlines(qs, 52),
                  sec("Think and write", "write", [("What do you think will happen next? Write one sentence.", "Answers vary."),
                                                   ("What was your favorite part? Write one sentence.", "Answers vary.")], 1, 62)])


def _adj_phrase(rng, v, key, n):
    pairs = [(a, w) for a in ADJ for w in ADJN]
    out = []
    for a, w in take(pairs, n, v, key):
        out.append((f"the {a} {w}   Adjective: ____", a))
    return out


def _adj_cloze(rng, v, key, n):
    out = []
    for s, good, bad in take(ADJCLOZE, n, v, key):
        o = [good, bad]
        rng.shuffle(o)
        out.append((f"{s}  ({o[0]} / {o[1]})", good))
    return out


def _homo(rng, v, key, n):
    out = []
    for s, good, bad in take(HOMO, n, v, key):
        o = [good, bad]
        rng.shuffle(o)
        out.append((f"{s}  ({o[0]} / {o[1]})", good))
    return out


def _multi(rng, v, key, n):
    out = []
    for s, w, a, b, ok in take(MULTI, n, v, key):
        out.append((f"{s}   Which meaning of '{w}' fits?  ({a} / {b})", [a, b][ok]))
    return out


def _context(rng, v, key, n):
    out = []
    for s, w, good, bad in take(CONTEXT, n, v, key):
        o = [good, bad]
        rng.shuffle(o)
        out.append((f"{s}   '{w}' means ____  ({o[0]} / {o[1]})", good))
    return out


def U9(day, rng, v):
    t = "Adjectives, Homophones & Word Meaning"
    if day == 1:
        return sheet(9, 1, t, "An adjective describes a noun: its color, size, shape, feeling or number.",
                     "Example: the red apple  " + ARROW + "  Adjective: red",
                     [sec("Part A – Find the adjective", "eq", _adj_phrase(rng, v, "u9d1a", 12), 2, 30),
                      sec("Part B – Choose the describing word", "eq", _adj_cloze(rng, v, "u9d1b", 6), 1, 30)])
    if day == 2:
        a = [(f"{x}:  one is {x}, two is ____, three is the ____", f"{y}, {z}") for x, y, z in take(COMPAR, 8, v, "u9d2")]
        return sheet(9, 2, t, "Add -er to compare two things and -est to compare three or more.",
                     "Example: tall:  one is tall, two is taller, three is the tallest",
                     [sec("Part A – Find the adjective", "eq", _adj_phrase(rng, v, "u9d2a", 8), 2, 30),
                      sec("Part B – Add -er and -est", "eq", a, 1, 30),
                      sec("Part C – Choose the describing word", "eq", _adj_cloze(rng, v, "u9d2c", 6), 1, 30)])
    if day == 3:
        return sheet(9, 3, t, "Homophones sound the same but have different spellings and meanings.",
                     "Example: I can ____ a bird. (see / sea)  " + ARROW + "  see",
                     [sec("", "eq", _homo(rng, v, "u9d3", 20), 1, 30)])
    if day == 4:
        return sheet(9, 4, t, "Some words have more than one meaning. Use the sentence to decide. Context clues help you with new words.",
                     "Example: 'Duck! The ball is coming!' (a bird / to bend down quickly)  " + ARROW + "  to bend down quickly",
                     [sec("Part A – Which meaning?", "qline", _multi(rng, v, "u9d4a", 6), 1, 50),
                      sec("Part B – Context clues", "qline", _context(rng, v, "u9d4b", 5), 1, 50)])
    return sheet(9, 5, t, "Review day! Adjectives, homophones, multiple meanings and context clues.",
                 "Example: I ____ an apple. (ate / eight)  " + ARROW + "  ate",
                 [sec("Part A – Adjectives", "eq", _adj_phrase(rng, v, "u9d5a", 4), 2, 30),
                  sec("Part B – Homophones", "eq", _homo(rng, v, "u9d5b", 6), 1, 30),
                  sec("Part C – Which meaning?", "qline", _multi(rng, v, "u9d5c", 3), 1, 50),
                  sec("Part D – Context clues", "qline", _context(rng, v, "u9d5d", 3), 1, 50)])


# ------------------------------------------------------------------ writing
STARTERS = [("My favorite animal is ____ because ____.", "Answers vary. Sample: My favorite animal is a dog because it is loyal."),
            ("On weekends, I like to ____.", "Answers vary. Sample: On weekends, I like to ride my bike."),
            ("My favorite food is ____ because ____.", "Answers vary. Sample: My favorite food is pizza because it is cheesy."),
            ("When I grow up, I want to be a ____.", "Answers vary. Sample: When I grow up, I want to be a teacher."),
            ("The best thing about school is ____.", "Answers vary. Sample: The best thing about school is recess."),
            ("I feel happy when ____.", "Answers vary. Sample: I feel happy when I play with my friends."),
            ("If I had a magic wand, I would ____.", "Answers vary. Sample: If I had a magic wand, I would fly."),
            ("My favorite season is ____ because ____.", "Answers vary. Sample: My favorite season is summer because I can swim."),
            ("One thing I am good at is ____.", "Answers vary. Sample: One thing I am good at is drawing."),
            ("I would like to visit ____ because ____.", "Answers vary. Sample: I would like to visit the zoo because I love animals."),
            ("My best friend is ____ and we like to ____.", "Answers vary. Sample: My best friend is Sam and we like to play soccer."),
            ("The scariest thing I know is ____.", "Answers vary. Sample: The scariest thing I know is thunder.")]
USEWORD = ["dog", "happy", "park", "jump", "blue", "friend", "rain", "pizza", "school", "bird", "ball", "moon"]
ORDER = [("A. Then she poured milk on top.  B. Mia took out a bowl.  C. Last, she ate her cereal.  D. First, she got up and was hungry.", "D, B, A, C"),
         ("A. He pumped up the tires.  B. Then Leo rode off to the park.  C. Leo found his bike.  D. Next, he put on his helmet.", "C, A, D, B"),
         ("A. The seed grew into a flower.  B. Zoe planted a seed.  C. Then she watered it every day.  D. Soon, a tiny sprout came up.", "B, C, D, A"),
         ("A. Dad put the cake in the oven.  B. Ben and Dad mixed the batter.  C. At last, they ate the warm cake.  D. First, they got eggs and flour.", "D, B, A, C"),
         ("A. They splashed in the water.  B. Ava and her mom drove to the beach.  C. Then they built a sand castle.  D. At night, they went home tired.", "B, A, C, D"),
         ("A. Sam put on his coat.  B. It started to snow.  C. Then he ran outside to play.  D. First, Sam looked out the window.", "D, B, A, C"),
         ("A. She said thank you.  B. Lily wrote a letter to Grandma.  C. A week later, Grandma wrote back.  D. Then Lily mailed it.", "B, D, C, A"),
         ("A. The baby bird flapped its wings.  B. The egg cracked open.  C. A tiny bird came out.  D. Soon, it flew away.", "B, C, A, D")]
EDIT = [("my cat is nameed tom", "My cat is named Tom."), ("we goed to the park", "We went to the park."),
        ("i like to play with my frend", "I like to play with my friend."), ("the dogs is runing fast", "The dogs are running fast."),
        ("she dont like peas", "She doesn't like peas."), ("what is your name", "What is your name?"),
        ("ben and me went to school", "Ben and I went to school."), ("the sun is hot today", "The sun is hot today."),
        ("did you see the rainbow", "Did you see the rainbow?"), ("my brother have a new bike", "My brother has a new bike."),
        ("they was happy to see us", "They were happy to see us."), ("mom made a big cake on friday", "Mom made a big cake on Friday.")]
BETTER = [("(a) I have a dog.  (b) I have a fluffy brown dog named Max.", "b"),
          ("(a) We ate lunch.  (b) We ate cheese sandwiches and apples for lunch.", "b"),
          ("(a) The girl ran.  (b) The little girl ran quickly down the long hall.", "b"),
          ("(a) It was a sunny day, and the warm sun made the pond sparkle.  (b) It was a day.", "a"),
          ("(a) My room is messy.  (b) My room has toys, books and socks all over the floor.", "b"),
          ("(a) The cookie smelled sweet and tasted warm and chewy.  (b) The cookie was good.", "a")]
MAINIDEA = [("1. Dogs make great pets. 2. They love to play. 3. My bike is red. 4. They keep us company.", "3"),
            ("1. Rain helps plants grow. 2. Rain fills the lakes. 3. Rain is good for the Earth. 4. I like pizza.", "4"),
            ("1. Winter is cold. 2. Snow covers the ground. 3. Kids wear hats and coats. 4. Frogs have long tongues.", "4"),
            ("1. Bats sleep in the day. 2. They hunt for food at night. 3. Bats are active at night. 4. My shoes are new.", "4"),
            ("1. Reading is fun. 2. Books take us to new places. 3. I eat lunch at noon. 4. I can learn new things from books.", "3"),
            ("1. Bees make honey. 2. They live in hives. 3. Cars drive on roads. 4. Bees work together.", "3")]
TITLES = [("Plants need sun, water and soil to grow. A seed takes in water and sends a root down. A little stem pushes up toward the light. Which is the best title? (a) How Plants Grow (b) My Pet Fish", "a"),
          ("A fire truck has a loud siren and a long ladder. Firefighters ride on it to get to fires fast. They use hoses to put out flames. Which is the best title? (a) Ice Cream Day (b) Fire Trucks", "b"),
          ("Maya took a flashlight into the dark cave. Her friends followed. They saw bats on the ceiling. Which is the best title? (a) A Cave Adventure (b) A Day at the Beach", "a"),
          ("A caterpillar eats leaves all day. Then it makes a cocoon. Later, it comes out as a butterfly. Which is the best title? (a) Rainy Weather (b) From Caterpillar to Butterfly", "b")]
PROMPTS5 = [("Write 4 sentences about your favorite place. Tell what it looks like and why you like it.",
             "Answers vary. Check: capitals, end marks, complete sentences, at least 4 sentences."),
            ("Write 4 sentences about a time you helped someone. Tell what happened first, next and last.",
             "Answers vary. Check: first/next/last words, capitals, end marks."),
            ("Write 4 sentences about what you would do on a rainy day.",
             "Answers vary. Check: capitals, end marks, complete sentences."),
            ("Write 4 sentences about your favorite animal. Use two describing words (adjectives).",
             "Answers vary. Check: two adjectives, capitals, end marks."),
            ("Write 4 sentences about a trip to the zoo. Use at least one past-tense verb.",
             "Answers vary. Check: past tense verbs, capitals, end marks."),
            ("Write 4 sentences about your best day ever. Use the words first, then and last.",
             "Answers vary. Check: sequence words, capitals, end marks.")]


def U10(day, rng, v):
    t = "Writing & Challenges"
    if day == 1:
        a = [(s, a_) for s, a_ in take(STARTERS, 4, v, "u10d1a")]
        b = [(f"Write a sentence using the word '{w}'.", "Answers vary. Check: the word is used and the sentence is complete.")
             for w in take(USEWORD, 3, v, "u10d1b")]
        return sheet(10, 1, t, "Finish each sentence in your own words. Use a capital letter and an end mark.",
                     "Example: My favorite animal is a dog because it is loyal.",
                     [sec("Part A – Finish the sentence", "write", a, 1, 76), sec("Part B – Use the word", "write", b, 1, 76)])
    if day == 2:
        a = [(f"Put the sentences in order. Write the letters.  {s}   ____ , ____ , ____ , ____", ans) for s, ans in take(ORDER, 4, v, "u10d2a")]
        e = [(f"Fix the sentence:  {s}", ans) for s, ans in take(EDIT, 4, v, "u10d2b")]
        return sheet(10, 2, t, "Put story sentences in order. Then fix the mistakes.",
                     "Example: First, I woke up. Then I ate. Last, I went to school.",
                     [sec("Part A – What happens first, next and last?", "qline", a, 1, 70), sec("Part B – Fix it", "qline", e, 1, 50)])
    if day == 3:
        e = [(f"Fix the sentence:  {s}", ans) for s, ans in take(EDIT, 6, v, "u10d3a")]
        b = [(f"Which sentence tells more?  {s}", ans) for s, ans in take(BETTER, 4, v, "u10d3b")]
        return sheet(10, 3, t, "Editing: fix capitals, spelling, end marks and verbs. Then choose the sentence with more details.",
                     "Example: my cat is nameed tom  " + ARROW + "  My cat is named Tom.",
                     [sec("Part A – Fix it", "qline", e, 1, 50), sec("Part B – Add details", "qline", b, 1, 50)])
    if day == 4:
        a = [(f"Which sentence does NOT belong? Write its number.  {s}", ans) for s, ans in take(MAINIDEA, 5, v, "u10d4a")]
        b = [(f"{s}", ans) for s, ans in take(TITLES, 3, v, "u10d4b")]
        return sheet(10, 4, t, "A paragraph is about one main idea. Find the sentence that does not belong. Pick the best title.",
                     "Example: 1. Dogs bark. 2. Dogs wag tails. 3. I like cake.  " + ARROW + "  3",
                     [sec("Part A – Which does not belong?", "qline", a, 1, 56), sec("Part B – Best title", "qline", b, 1, 70)])
    pr = take(PROMPTS5, 2, v, "u10d5")
    ch = passage_sec("My checklist", "[  ] I started each sentence with a capital letter.   [  ] I ended each sentence with . ? or !   "
                     "[  ] My sentences are complete.   [  ] I checked my spelling.")
    return sheet(10, 5, t, "Challenge day! Write like an author. Then use the checklist to check your work.",
                 "Example: First, I went to the park. Then I played on the swings. Last, I ate ice cream.",
                 [sec("Write", "write", pr, 1, 130), ch])


UNITS = {1: U1, 2: U2, 3: U3, 4: U4, 5: U5, 6: U6, 7: U7, 8: U8, 9: U9, 10: U10}


def _need(sc):
    """minimum row height a section needs so wrapped text never collides with the answer line"""
    if sc["kind"] in ("qline", "write"):
        n = max(len(simpleSplit(c[0], "Helvetica", 11.5, PAGE_W - 2 * PAGE_M - 30)) for c in sc["cells"])
        return 13 + 14 * n + (22 if sc["kind"] == "qline" else 30)
    return {"eq": 25, "seq": 34, "cmp": 34}.get(sc["kind"], sc["h"])


def fit(sh, avail=562):
    """Make a daily sheet fit one page: tighten rows first, then drop the last few items."""
    import math
    for sc in sh["sections"]:
        if sc["kind"] in ("qline", "write"):
            sc["h"] = max(sc["h"], _need(sc))

    def total():
        return sum((24 if sc["head"] else 4) + math.ceil(len(sc["cells"]) / sc["cols"]) * sc["h"] + 6
                   for sc in sh["sections"])
    while total() > avail:
        shrunk = False
        for sc in sh["sections"]:
            if sc["kind"] not in ("passage",) and sc["h"] > _need(sc):
                sc["h"] -= 1
                shrunk = True
        if not shrunk:
            big = max((sc for sc in sh["sections"] if sc["kind"] != "passage" and len(sc["cells"]) > sc["cols"]),
                      key=lambda sc: math.ceil(len(sc["cells"]) / sc["cols"]) * sc["h"])
            del big["cells"][-big["cols"]:]
    return sh


def unit_sheets(u, variant=0):
    return [fit(UNITS[u](d, random.Random(u * 100 + d + variant * 1000), variant)) for d in range(1, 6)]


# ----------------------------------------------------------- check / final
def checkup_a():
    rng = random.Random(1555)
    s = [sec("Alphabet & ABC order", "eq", [eq("What letter comes after m?  ____", "n"),
                                           eq("Is 'e' a vowel or a consonant?  ____", "vowel"),
                                           eq("cat, ant, bee   " + ARROW + "   ____ , ____ , ____", "ant, bee, cat")], 1, 30),
         sec("Vowels", "eq", [eq("c__t   (a pet that purrs)", "a"), eq("kite: long or short vowel?  ____", "long"),
                              eq("cap + e = ____", "cape"), eq("r__n   (water from clouds) [ai / ay]", "ai")], 2, 30),
         sec("Blends, digraphs & families", "eq", [eq("__ip   (sails on the sea) [sh / ch / th]", "sh"),
                                                  eq("__og   (a green animal that hops) [fr / bl / st]", "fr"),
                                                  eq("b + ack = ____", "back"),
                                                  eq("Which word rhymes with cat?  (hat / hot)  ____", "hat")], 1, 30),
         sec("Nouns, verbs & plurals", "eq", [eq("Is 'swim' a noun or a verb?  ____", "verb"), eq("Is 'park' a noun or a verb?  ____", "noun"),
                                              eq("one box, two ____", "boxes"), eq("one baby, two ____", "babies"),
                                              eq("one foot, two ____", "feet")], 2, 30),
         sec("Sentences", "eq", [eq("In the park   Complete sentence?  ____", "no"), eq("Where is my hat ____", "?"),
                                 eq("Wow, that is huge ____", "!")], 1, 30),
         sec("Capitals & word order", "qline", [("Rewrite with capital letters:  mia lives in paris.", "Mia lives in Paris."),
                                                ("Put the words in order:  dog / the / barks", "The dog barks.")], 1, 50)]
    return sheet(0, "A", "Check-Up: Units 1–5", "Show what you know! Do your best on every question.",
                 "Aim for 90% or more before moving on to Unit 6.", s)


def final_test():
    rng = random.Random(1999)
    s = [sec("Opposites & synonyms", "eq", _ant_options(rng, 0, "ft1", 2) + _syn_options(rng, 0, "ft2", 2), 1, 30),
         sec("Compound words", "eq", [eq("sun + flower = ____", "sunflower"), eq("rain + bow = ____", "rainbow"),
                                      eq("foot + ____ = football", "ball")], 3, 30),
         sec("Past tense & contractions", "eq", [eq("walk " + ARROW + " ____ (past)", "walked"), eq("go " + ARROW + " ____ (past)", "went"),
                                                 eq("hop " + ARROW + " ____ (past)", "hopped"), eq("do not = ____", "don't"),
                                                 eq("she is = ____", "she's"), eq("un + happy = ____", "unhappy")], 2, 30),
         sec("Adjectives & homophones", "eq", [eq("the shiny coin   Adjective: ____", "shiny"),
                                               eq("tall:  one is tall, two is ____, three is the ____", "taller, tallest")] +
                                              _homo(rng, 0, "ft3", 2), 1, 30),
         sec("Word meaning", "qline", _multi(rng, 0, "ft4", 2) + _context(rng, 0, "ft5", 2), 1, 50),
         passage_sec("The Snowy Day", "On Saturday, it snowed all morning. Ella put on her warm coat and red boots. She built a snowman in the "
                     "yard and gave him a carrot for a nose. Her little brother Tom added two black buttons for eyes. When they went inside, "
                     "Mom gave them hot chocolate."),
         qlines([("What day did it snow?", "Saturday"), ("What did Ella use for the snowman's nose?", "a carrot"),
                 ("Who added the buttons?", "Tom"), ("What did Mom give them?", "hot chocolate"),
                 ("Why do you think Ella wore a warm coat?", "Because it was cold. Sample answer.")], 46),
         sec("Writing", "qline", [("Fix the sentence:  my frend and me goed to the zoo", "My friend and I went to the zoo."),
                                  ], 1, 56)]
    return sheet(0, "F", "Final Test: Units 1–10", "You made it! Show everything you have learned.",
                 "Aim for 90% or more. Then it's certificate time!", s)
