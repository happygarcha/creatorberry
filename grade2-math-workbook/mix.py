"""Turn a picture-only sheet into a balanced mix: some pictures + true/false, fill-in, matching, reading, writing."""
import math
import random
from english_generators import take, passage_sec, qlines
from generators import sec

PIC_KINDS = {"pic", "word", "picp", "count", "coins", "people"}
PIC_TARGET = {1: 6, 2: 6, 3: 4, 4: 4, 5: 4}


def trim_pics(sections, target):
    total = sum(len(s["cells"]) for s in sections if s["kind"] in PIC_KINDS)
    out = []
    for s in sections:
        if s["kind"] in PIC_KINDS and total > target:
            n = max(2, round(len(s["cells"]) * target / total))
            if s["cols"] == 2 and n % 2:
                n += 1
            s = dict(s)
            s["cells"] = s["cells"][:n]
        out.append(s)
    return out


def tf_sec(bank, n, v, key, head="True or false?"):
    items = [(f"{s}  (true / false)  ____", "true" if t else "false") for s, t in take(bank["tf"], n, v, key)]
    return sec(head, "eq", items, 1, 28)


def fill_secs(bank, n, v, key, head="Fill in the blank"):
    chosen = take(bank["fill"], n, v, key)
    words = [a for _, a in chosen]
    shuffled = list(words)
    random.Random(sum(map(ord, key))).shuffle(shuffled)
    return [sec("", "bank", [(shuffled, None)], 1, 38), sec(head, "eq", [(s, a) for s, a in chosen], 1, 28)]


def match_sec(bank, idx, v, key, head="Match. Write the letter."):
    pairs = bank["match"][idx % len(bank["match"])]
    left = [l for l, _ in pairs]
    rights = [r for _, r in pairs]
    order = list(range(4))
    rng = random.Random(sum(map(ord, key)) + v)
    for _ in range(20):
        rng.shuffle(order)
        if order != [0, 1, 2, 3]:
            break
    shown = [rights[i] for i in order]
    ans = ", ".join(f"{i + 1}-{'abcd'[order.index(i)]}" for i in range(4))
    return sec(head, "match", [({"left": left, "right": shown}, ans)], 1, 106)


def read_secs(bank, v, head="Read and answer"):
    title, text, qs = bank["read"][v % len(bank["read"])]
    p = passage_sec(title, text)
    p["head"] = head
    return [p, qlines(qs, 44)]


def short_sec(bank, n, v, key, head="Short answers"):
    s = qlines(take(bank["short"], n, v, key), 46)
    s["head"] = head
    return s


def write_sec(bank, v, head="Write"):
    pr, sample = bank["write"][v % len(bank["write"])]
    return sec(head, "write", [(pr, sample)], 1, 66)


def mixify(sh, bank, u, day, v):
    key = f"m{u}d{day}"
    secs = trim_pics(sh["sections"], PIC_TARGET[day])
    if day == 1:
        extra = fill_secs(bank, 5, v, key + "f") + [tf_sec(bank, 4, v, key + "t")]
    elif day == 2:
        extra = [tf_sec(bank, 6, v, key + "t"), short_sec(bank, 2, v, key + "s")]
    elif day == 3:
        extra = read_secs(bank, v) + [match_sec(bank, v, v, key + "m")]
    elif day == 4:
        extra = fill_secs(bank, 5, 1 - v, key + "f") + [match_sec(bank, 1 - v, v, key + "m"), write_sec(bank, v)]
    else:
        extra = [tf_sec(bank, 3, v, key + "t")] + fill_secs(bank, 3, v, key + "f") + [short_sec(bank, 1, v, key + "s"), write_sec(bank, 1 - v, "Write about your picture")]
    sh = dict(sh)
    sh["sections"] = secs + extra
    if sh["instr"].startswith("Look at the pictures. Pick the best answer"):
        sh["instr"] = "Do each part: look at the pictures, read, and write your answers."
    return sh
