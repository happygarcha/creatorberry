"""Problem generators for the Grade 2 Math Mastery Workbook.

Every sheet is a dict:
  unit, day, title, instr, example, sections=[{head, kind, cols, h, cells=[(data, answer)]}]
Answers are always computed from the problem data, so the key can never drift.
"""
import random

MINUS = "–"   # en dash: available in the standard PDF fonts
TIMES = "×"


# ----------------------------------------------------------------- helpers
def uniq(fn, n, tries=800):
    seen, out = set(), []
    for _ in range(tries):
        if len(out) >= n:
            break
        t = fn()
        if str(t[0]) in seen:
            continue
        seen.add(str(t[0]))
        out.append(t)
    return out


def sec(head, kind, cells, cols=1, h=30):
    return dict(head=head, kind=kind, cells=cells, cols=cols, h=h)


def eq(text, ans):
    return (text, str(ans))


def sheet(unit, day, title, instr, example, sections):
    return dict(unit=unit, day=day, title=title, instr=instr, example=example,
                sections=sections)


# ------------------------------------------------------- sequences / compare
def seq_row(rng, start, step, n, nblank, back=False):
    vals = [start + (-i if back else i) * step for i in range(n)]
    idx = sorted(rng.sample(range(1, n), nblank))
    data = [None if i in idx else v for i, v in enumerate(vals)]
    return data, ", ".join(str(vals[i]) for i in idx)


def seq_rows(rng, n_rows, lo, hi, step=1, n=8, nblank=2, back_every=0):
    rows = []
    for r in range(n_rows):
        back = bool(back_every) and r % back_every == back_every - 1
        span = (n - 1) * step
        if back:
            start = rng.randint(lo + span, hi)
            start -= start % step if step > 1 else 0
            start = max(start, lo + span)
        else:
            start = rng.randint(lo, hi - span)
            start -= start % step if step > 1 else 0
            start = max(start, lo)
        rows.append(seq_row(rng, start, step, n, nblank, back))
    return rows


def cmp_cells(rng, n, lo, hi, near=False):
    def g():
        a = rng.randint(lo, hi)
        if near:
            b = a + rng.choice([-9, -5, -3, -1, 1, 2, 4, 8, 10]) if rng.random() < .6 \
                else rng.randint(lo, hi)
        else:
            b = rng.randint(lo, hi)
        b = max(lo, min(hi, b))
        if rng.random() < .05:
            b = a
        return (a, b), "<" if a < b else ">" if a > b else "="
    return uniq(g, n)


# --------------------------------------------------------------- arithmetic
def add_facts(rng, n, amin, amax, bmin, bmax, cap=20):
    def g():
        a, b = rng.randint(amin, amax), rng.randint(bmin, bmax)
        if a + b > cap:
            return g()
        return f"{a} + {b} = ____", a + b
    return uniq(g, n)


def sub_facts(rng, n, amin, amax, bmin, bmax, cross_ten=False):
    def g():
        a, b = rng.randint(amin, amax), rng.randint(bmin, bmax)
        if b > a:
            return g()
        if cross_ten and not (a > 10 and b > a % 10 and b <= 9):
            return g()
        return f"{a} {MINUS} {b} = ____", a - b
    return uniq(g, n)


def missing_add(rng, n, total_lo, total_hi):
    def g():
        t = rng.randint(total_lo, total_hi)
        a = rng.randint(1, t - 1)
        return (f"{a} + ____ = {t}" if rng.random() < .5 else f"____ + {a} = {t}"), t - a
    return uniq(g, n)


def vert(nums, op):
    return (list(nums), op)


def vadd_nocarry(rng):
    while True:
        a, b = rng.randint(11, 88), rng.randint(11, 88)
        if a % 10 + b % 10 <= 9 and a // 10 + b // 10 <= 9:
            return vert((a, b), "+"), a + b


def vsub_noborrow(rng):
    while True:
        a, b = rng.randint(21, 99), rng.randint(11, 89)
        if a > b and a % 10 >= b % 10 and a // 10 >= b // 10:
            return vert((a, b), "-"), a - b


def vadd_carry(rng, one_digit=False):
    while True:
        a = rng.randint(11, 89)
        b = rng.randint(3, 9) if one_digit else rng.randint(11, 89)
        if a % 10 + b % 10 >= 10 and a + b < 100:
            return vert((a, b), "+"), a + b


def vsub_borrow(rng, one_digit=False):
    while True:
        a = rng.randint(21, 99)
        b = rng.randint(3, 9) if one_digit else rng.randint(12, 89)
        if a > b and a % 10 < b % 10:
            return vert((a, b), "-"), a - b


def vadd3(rng):
    while True:
        a, b, c = rng.randint(10, 40), rng.randint(10, 30), rng.randint(5, 25)
        if a + b + c < 100:
            return vert((a, b, c), "+"), a + b + c


def v3_add(rng):
    while True:
        a, b = rng.randint(101, 888), rng.randint(101, 888)
        if all(((a // 10 ** k) % 10 + (b // 10 ** k) % 10) <= 9 for k in range(3)):
            return vert((a, b), "+"), a + b


def v3_sub(rng):
    while True:
        a, b = rng.randint(201, 999), rng.randint(101, 899)
        if a > b and all(((a // 10 ** k) % 10) >= ((b // 10 ** k) % 10) for k in range(3)):
            return vert((a, b), "-"), a - b


def hor_two_digit(rng, n, kind):
    def g():
        if kind == "add":
            a, b = rng.randint(12, 79), rng.randint(11, 60)
            if a + b > 99:
                return g()
            return f"{a} + {b} = ____", a + b
        a, b = rng.randint(30, 99), rng.randint(11, 70)
        if b >= a:
            return g()
        return f"{a} {MINUS} {b} = ____", a - b
    return uniq(g, n)


# --------------------------------------------------------- word problems
NAMES = ["Mia", "Leo", "Ava", "Sam", "Zoe", "Ben", "Lily", "Max", "Nina", "Omar"]
ITEMS = ["apples", "stickers", "marbles", "cards", "pencils", "books", "shells",
         "balloons", "stamps", "cookies"]


def word(rng, kind, hi=20):
    n, m = rng.sample(NAMES, 2)
    it = rng.choice(ITEMS)
    if kind == "join":
        a = rng.randint(3, hi // 2)
        b = rng.randint(2, hi - a)
        t = rng.choice([
            f"{n} has {a} {it}. {m} gives {n} {b} more. How many {it} does {n} have now?",
            f"There are {a} {it} in a box and {b} {it} in a bag. How many {it} are there in all?",
            f"{n} picked {a} {it} on Monday and {b} {it} on Tuesday. How many {it} did {n} pick altogether?"])
        return t, a + b
    if kind == "sep":
        a = rng.randint(8, hi)
        b = rng.randint(2, a - 2)
        t = rng.choice([
            f"{n} had {a} {it}. {n} gave {b} {it} to {m}. How many {it} are left?",
            f"There were {a} {it} on the table. {b} {it} were taken away. How many {it} are left?"])
        return t, a - b
    if kind == "diff":
        a = rng.randint(8, hi)
        b = rng.randint(2, a - 2)
        return (f"{n} has {a} {it}. {m} has {b} {it}. How many more {it} does {n} have than {m}?",
                a - b)
    if kind == "two":
        a = rng.randint(10, hi // 2 + 10)
        b = rng.randint(5, hi // 2)
        c = rng.randint(3, a + b - 3)
        c = min(c, a + b - 1)
        return (f"{n} had {a} {it}. {n} got {b} more {it}, then gave {c} {it} away. "
                f"How many {it} does {n} have now?", a + b - c)
    if kind == "mult":
        g = rng.choice([2, 3, 4, 5])
        p = rng.choice([2, 3, 4, 5, 10])
        return (f"There are {g} bags. Each bag has {p} {it}. How many {it} are there in all?", g * p)
    if kind == "money":
        a = rng.choice(range(50, 100, 5))
        b = rng.choice(range(10, a, 5))
        return (f"{n} has {a}¢. A sticker costs {b}¢. How much money is left?", f"{a - b}¢")
    if kind == "money2":
        a, b = rng.choice(range(10, 50, 5)), rng.choice(range(10, 50, 5))
        return (f"A pencil costs {a}¢ and an eraser costs {b}¢. How much do they cost together?",
                f"{a + b}¢")
    raise ValueError(kind)


def words(rng, kinds, n, hi):
    out, i = [], 0
    seen = set()
    while len(out) < n:
        t = word(rng, kinds[i % len(kinds)], hi)
        i += 1
        if t[0] in seen:
            continue
        seen.add(t[0])
        out.append((t[0], str(t[1])))
    return out


# --------------------------------------------------------------- time / money
def clock_cells(rng, n, minutes):
    def g():
        h, m = rng.randint(1, 12), rng.choice(minutes)
        return (h, m), f"{h}:{m:02d}"
    return uniq(g, n)


COINS = [("penny", "pennies", 1), ("nickel", "nickels", 5), ("dime", "dimes", 10),
         ("quarter", "quarters", 25)]


def coin_cells(rng, n, max_total=99):
    def g():
        k = rng.choice([2, 3])
        picks = sorted(rng.sample(COINS, k), key=lambda c: -c[2])
        parts, total = [], 0
        for one, many, v in picks:
            q = rng.randint(1, 3 if v < 25 else 2)
            total += q * v
            parts.append(f"{q} {one if q == 1 else many}")
        if total > max_total:
            return g()
        return ", ".join(parts) + " = ____¢", total
    return uniq(g, n)


def later_cells(rng, n):
    def g():
        h = rng.randint(1, 9)
        d = rng.randint(1, 3)
        return f"Start at {h}:00. What time is it {d} hour{'s' if d > 1 else ''} later? ____", f"{h + d}:00"
    return uniq(g, n)


# ---------------------------------------------------------------- the units
def U1(day, rng):
    t = "Counting & Comparing to 100"
    if day == 1:
        rows = seq_rows(rng, 14, 1, 20, 1, 8, 2)
        return sheet(1, 1, t, "Write the missing numbers in the boxes.", "Example: 4, 5, __, 7  →  6",
                     [sec("", "seq", rows, 1, 36)])
    if day == 2:
        rows = seq_rows(rng, 14, 1, 50, 1, 8, 3)
        return sheet(1, 2, t, "Write the missing numbers in the boxes.", "Example: 21, __, 23, 24  →  22",
                     [sec("", "seq", rows, 1, 36)])
    if day == 3:
        def g():
            k = rng.choice("abc")
            x = rng.randint(11, 98)
            if k == "a":
                return f"What comes after {x}?  ____", x + 1
            if k == "b":
                return f"What comes before {x}?  ____", x - 1
            return f"{x - 1}, ____, {x + 1}", x
        cells = uniq(g, 24)
        return sheet(1, 3, t, "Write the number that comes before, after, or between.",
                     "Example: What comes after 29?  →  30",
                     [sec("", "eq", cells, 2, 32)])
    if day == 4:
        rows = seq_rows(rng, 14, 30, 100, 1, 8, 3, back_every=3)
        return sheet(1, 4, t, "Write the missing numbers. Some rows count backwards!",
                     "Example: 58, 57, __, 55  →  56", [sec("", "seq", rows, 1, 36)])
    cmpc = cmp_cells(rng, 16, 10, 99, near=True)

    def order():
        a = rng.sample(range(10, 99), 3)
        return f"{a[0]}, {a[1]}, {a[2]}   →  ____ , ____ , ____", ", ".join(map(str, sorted(a)))
    return sheet(1, 5, t, "Write <, > or = in the circle. Then put the numbers in order.",
                 "Example: 47 (>) 39  because 4 tens is more than 3 tens.",
                 [sec("Part A – Which is bigger?", "cmp", cmpc, 4, 36),
                  sec("Part B – Write the numbers from smallest to biggest", "eq",
                      uniq(order, 5), 1, 32)])


def U2(day, rng):
    t = "Adding Within 20"
    if day == 1:
        c = add_facts(rng, 30, 0, 10, 0, 2)
        return sheet(2, 1, t, "Add. Try to finish in 5 minutes!", "Example: 7 + 2 = 9",
                     [sec("", "eq", c, 3, 30)])
    if day == 2:
        dbl = [(f"{a} + {a} = ____", a + a) for a in range(1, 11)]
        rng.shuffle(dbl)
        c2 = add_facts(rng, 16, 1, 10, 3, 4, cap=14)
        return sheet(2, 2, t, "Doubles are easy to remember. Add.", "Example: 6 + 6 = 12",
                     [sec("Part A – Doubles", "eq", dbl, 3, 30),
                      sec("Part B – Adding 3 and 4", "eq", c2, 3, 30)])
    if day == 3:
        mk = []
        for a in range(0, 11):
            mk.append((f"{a} + ____ = 10", 10 - a))
        rng.shuffle(mk)
        c2 = add_facts(rng, 18, 0, 10, 0, 10, cap=10)
        return sheet(2, 3, t, "Find the numbers that make 10, then add.", "Example: 6 + ____ = 10  →  4",
                     [sec("Part A – Make ten", "eq", mk, 3, 30),
                      sec("Part B – Sums up to 10", "eq", c2, 3, 30)])
    if day == 4:
        def g4():
            a, b = rng.randint(2, 9), rng.randint(2, 9)
            if a + b < 11:
                return g4()
            return f"{a} + {b} = ____", a + b
        c = uniq(g4, 20)
        m = missing_add(rng, 8, 11, 18)
        return sheet(2, 4, t, "Add. Hint: make a ten first! 8 + 5 → 8 + 2 = 10, then 10 + 3 = 13.",
                     "Example: 9 + 6 = 15",
                     [sec("Part A – Sums 11 to 18", "eq", c, 3, 30),
                      sec("Part B – Find the missing number", "eq", m, 3, 30)])
    c = add_facts(rng, 18, 1, 12, 1, 10)
    m = missing_add(rng, 6, 8, 20)
    w = words(rng, ["join"], 3, 20)
    return sheet(2, 5, t, "Review day! Add, find the missing numbers, and solve the problems.",
                 "Example: 7 + ____ = 12  →  5",
                 [sec("Part A – Fast facts", "eq", c, 3, 30),
                  sec("Part B – Missing numbers", "eq", m, 3, 30),
                  sec("Part C – Word problems", "word", w, 1, 78)])


def U3(day, rng):
    t = "Subtracting Within 20"
    if day == 1:
        c = sub_facts(rng, 30, 0, 10, 0, 2)
        return sheet(3, 1, t, "Subtract. Try to finish in 5 minutes!", f"Example: 8 {MINUS} 2 = 6",
                     [sec("", "eq", c, 3, 30)])
    if day == 2:
        a = [(f"10 {MINUS} {b} = ____", 10 - b) for b in range(0, 11)]
        rng.shuffle(a)
        c = sub_facts(rng, 18, 3, 14, 3, 4)
        return sheet(3, 2, t, "Take away from 10, then take away 3 and 4.", f"Example: 10 {MINUS} 6 = 4",
                     [sec("Part A – Taking away from 10", "eq", a, 3, 30),
                      sec("Part B – Taking away 3 and 4", "eq", c, 3, 30)])
    if day == 3:
        c = sub_facts(rng, 30, 3, 10, 1, 9)
        return sheet(3, 3, t, "Subtract. Think: what plus the small number makes the big number?",
                     f"Example: 9 {MINUS} 4 = 5 (because 4 + 5 = 9)", [sec("", "eq", c, 3, 30)])
    if day == 4:
        c = sub_facts(rng, 30, 11, 18, 2, 9, cross_ten=True)
        return sheet(3, 4, t, "Subtract. Hint: go back to 10 first! 14 {0} 6 → 14 {0} 4 = 10, then 10 {0} 2 = 8.".format(MINUS),
                     f"Example: 15 {MINUS} 7 = 8", [sec("", "eq", c, 3, 30)])

    def fam():
        a, b = rng.randint(2, 9), rng.randint(3, 9)
        return f"{a} + {b} = {a + b}, so {a + b} {MINUS} {b} = ____", a
    fm = uniq(fam, 8)
    c = []
    for _ in range(12):
        if rng.random() < .5:
            a, b = rng.randint(2, 12), rng.randint(2, 8)
            if a + b <= 20:
                c.append((f"{a} + {b} = ____", a + b))
                continue
        a, b = rng.randint(8, 19), rng.randint(2, 9)
        c.append((f"{a} {MINUS} {b} = ____", a - b))
    w = words(rng, ["sep", "diff", "sep"], 3, 20)
    return sheet(3, 5, t, "Review day! Look at the + and – signs carefully.",
                 f"Example: 6 + 7 = 13, so 13 {MINUS} 7 = 6",
                 [sec("Part A – Fact families", "eq", fm, 2, 30),
                  sec("Part B – Mixed practice", "eq", c, 3, 30),
                  sec("Part C – Word problems", "word", w, 1, 78)])


def U4(day, rng):
    t = "Two-Digit Add & Subtract"
    if day == 1:
        tens = []
        for _ in range(12):
            if rng.random() < .5:
                a, b = rng.randint(1, 8) * 10, rng.randint(1, 8) * 10
                if a + b <= 100:
                    tens.append((f"{a} + {b} = ____", a + b))
                    continue
            a = rng.randint(3, 9) * 10
            b = rng.randint(1, a // 10 - 1) * 10
            tens.append((f"{a} {MINUS} {b} = ____", a - b))
        ones = []
        for _ in range(12):
            if rng.random() < .5:
                a, b = rng.randint(11, 88), rng.randint(1, 9)
                if a % 10 + b <= 9:
                    ones.append((f"{a} + {b} = ____", a + b))
                    continue
            a = rng.randint(21, 99)
            b = rng.randint(1, max(1, a % 10)) if a % 10 else 0
            ones.append((f"{a} {MINUS} {b} = ____", a - b))
        return sheet(4, 1, t, "Add or subtract the tens, or the ones.", "Example: 40 + 30 = 70   and   45 + 3 = 48",
                     [sec("Part A – Tens", "eq", tens, 3, 30),
                      sec("Part B – Tens and ones", "eq", ones, 3, 30)])
    if day == 2:
        c = uniq(lambda: vadd_nocarry(rng), 20)
        return sheet(4, 2, t, "Add. Start with the ones column, then the tens.", "Example: 32 + 45 = 77",
                     [sec("", "vert", c, 5, 78)])
    if day == 3:
        c = uniq(lambda: vsub_noborrow(rng), 20)
        return sheet(4, 3, t, "Subtract. Start with the ones column, then the tens.", f"Example: 68 {MINUS} 35 = 33",
                     [sec("", "vert", c, 5, 78)])
    if day == 4:
        c = uniq(lambda: vadd_nocarry(rng) if rng.random() < .5 else vsub_noborrow(rng), 20)
        return sheet(4, 4, t, "Look at the sign first! Then add or subtract.", "Example: 56 + 23 = 79",
                     [sec("", "vert", c, 5, 78)])
    c = hor_two_digit(rng, 12, "add")[:6] + hor_two_digit(rng, 12, "sub")[:6]
    c = [x for x in c]
    w = words(rng, ["join", "sep", "diff"], 3, 90)
    return sheet(4, 5, t, "Review day! Solve the number puzzles and the word problems.",
                 "Example: 54 + 23 = 77", [sec("Part A – Mixed practice", "eq", c, 3, 30),
                                           sec("Part B – Word problems", "word", w, 1, 78)])


def U5(day, rng):
    t = "Regrouping: Carry & Borrow"
    if day == 1:
        c = uniq(lambda: vadd_carry(rng, one_digit=True), 20)
        return sheet(5, 1, t, "Add. When the ones make 10 or more, carry 1 ten.", "Example: 38 + 7 = 45",
                     [sec("", "vert", c, 5, 78)])
    if day == 2:
        c = uniq(lambda: vadd_carry(rng), 20)
        return sheet(5, 2, t, "Add. Carry a ten when you need to.", "Example: 38 + 27 = 65",
                     [sec("", "vert", c, 5, 78)])
    if day == 3:
        c = uniq(lambda: vsub_borrow(rng, True), 10) + uniq(lambda: vsub_borrow(rng), 10)
        return sheet(5, 3, t, "Subtract. When the top ones are too small, borrow 1 ten.", f"Example: 52 {MINUS} 27 = 25",
                     [sec("", "vert", c, 5, 78)])
    if day == 4:
        gens = [lambda: vadd_carry(rng, True), lambda: vadd_carry(rng),
                lambda: vsub_borrow(rng, True), lambda: vsub_borrow(rng)]
        c = uniq(lambda: rng.choice(gens)(), 20)
        return sheet(5, 4, t, "Look at the sign first! Carry or borrow when needed.", "Example: 46 + 38 = 84",
                     [sec("", "vert", c, 5, 78)])
    a = uniq(lambda: vadd3(rng), 5)
    h = hor_two_digit(rng, 20, "add")[:5] + hor_two_digit(rng, 20, "sub")[:5]
    w = words(rng, ["two", "join", "sep"], 3, 60)
    return sheet(5, 5, t, "Review day! Three numbers to add, then mixed practice.", "Example: 12 + 23 + 30 = 65",
                 [sec("Part A – Add three numbers", "vert", a, 5, 100),
                  sec("Part B – Mixed practice", "eq", h, 3, 30),
                  sec("Part C – Word problems", "word", w, 1, 78)])


def U6(day, rng):
    t = "Place Value to 1000"
    if day == 1:
        def g():
            n = rng.randint(101, 999)
            return f"{n} = ____ hundreds ____ tens ____ ones", f"{n // 100}, {n // 10 % 10}, {n % 10}"

        def g2():
            h, te, o = rng.randint(1, 9), rng.randint(0, 9), rng.randint(0, 9)
            return f"{h} hundreds, {te} tens, {o} ones = ____", h * 100 + te * 10 + o
        return sheet(6, 1, t, "Break each number into hundreds, tens and ones.",
                     "Example: 345 = 3 hundreds 4 tens 5 ones",
                     [sec("Part A – Take it apart", "eq", uniq(g, 10), 2, 32),
                      sec("Part B – Put it together", "eq", uniq(g2, 8), 2, 32)])
    if day == 2:
        def g():
            n = rng.randint(101, 999)
            return f"{n // 100 * 100} + {n // 10 % 10 * 10} + {n % 10} = ____", n

        def g2():
            n = rng.randint(111, 999)
            pos = rng.randint(0, 2)
            d = n // 10 ** pos % 10
            if d == 0:
                return g2()
            nm = ["ones", "tens", "hundreds"][pos]
            return f"In {n}, the digit {d} is in the {nm} place. Its value is ____", d * 10 ** pos
        return sheet(6, 2, t, "Write the number. Then find the value of each digit.",
                     "Example: 300 + 40 + 5 = 345",
                     [sec("Part A – Expanded form", "eq", uniq(g, 10), 2, 32),
                      sec("Part B – Value of a digit", "eq", uniq(g2, 6), 1, 32)])
    if day == 3:
        c = cmp_cells(rng, 20, 100, 999, near=True)
        return sheet(6, 3, t, "Write <, > or = in the circle. Look at the hundreds first!",
                     "Example: 456 (<) 478  because the tens: 5 < 7",
                     [sec("", "cmp", c, 4, 38)])
    if day == 4:
        r = []
        r += seq_rows(rng, 4, 100, 900, 10, 7, 3)
        for _ in range(3):
            s = rng.randint(1, 3) * 100
            r.append(seq_row(rng, s, 100, 7, 3))
        for _ in range(3):
            s = rng.randint(2, 40) * 5
            r.append(seq_row(rng, s, 5, 8, 3))

        def g():
            n = rng.randint(120, 880)
            k = rng.choice([("10 more than", 10), ("10 less than", -10), ("100 more than", 100), ("100 less than", -100)])
            return f"{k[0]} {n} = ____", n + k[1]
        return sheet(6, 4, t, "Skip count by 5s, 10s and 100s. Then find 10 or 100 more and less.",
                     "Example: 100 more than 345 = 445",
                     [sec("Part A – Skip counting", "seq", r, 1, 36),
                      sec("Part B – More and less", "eq", uniq(g, 10), 2, 30)])

    def order():
        a = rng.sample(range(100, 999), 3)
        return f"{a[0]}, {a[1]}, {a[2]}  →  ____ , ____ , ____", ", ".join(map(str, sorted(a)))
    a = uniq(lambda: v3_add(rng), 5) + uniq(lambda: v3_sub(rng), 5)
    return sheet(6, 5, t, "Review day! Add and subtract 3-digit numbers, then order them.",
                 "Example: 234 + 125 = 359",
                 [sec("Part A – Add and subtract", "vert", a, 5, 78),
                  sec("Part B – Smallest to biggest", "eq", uniq(order, 3), 1, 32)])


def U7(day, rng):
    t = "Skip Counting & Multiplying"
    if day == 1:
        r = []
        for _ in range(12):
            s = rng.choice([0, 2, 4, 6, 8, 10, 12]) if rng.random() < .6 else rng.choice([1, 3, 5, 7, 9])
            r.append(seq_row(rng, s if s else 2, 2, 8, 3))
        return sheet(7, 1, t, "Count by 2s. Write the missing numbers.", "Example: 2, 4, __, 8  →  6",
                     [sec("", "seq", r, 1, 36)])
    if day == 2:
        r = [seq_row(rng, rng.choice([5, 10, 15]), 5, 8, 3) for _ in range(6)]
        r += [seq_row(rng, rng.choice([10, 20, 30]), 10, 8, 3) for _ in range(6)]
        r += [seq_row(rng, rng.choice([20, 40, 60]), 5, 8, 3, True) for _ in range(0)]
        return sheet(7, 2, t, "Count by 5s, then by 10s. Write the missing numbers.", "Example: 5, 10, __, 20  →  15",
                     [sec("Part A – Count by 5s", "seq", r[:4], 1, 36),
                      sec("Part B – Count by 10s", "seq", r[4:], 1, 36)])
    if day == 3:
        g = []
        for _ in range(6):
            a, b = rng.randint(2, 5), rng.randint(2, 5)
            g.append(((a, b), f"{a} groups of {b} = {a * b}"))

        def r():
            a, b = rng.randint(2, 5), rng.choice([2, 3, 4, 5, 10])
            return (" + ".join([str(b)] * a) + " = ____   or   " + f"{a} {TIMES} {b} = ____"), f"{a * b}"
        return sheet(7, 3, t, "Count the groups and the dots. Write how many in all.",
                     f"Example: 3 groups of 4 = 4 + 4 + 4 = 12, so 3 {TIMES} 4 = 12",
                     [sec("Part A – Equal groups", "groups", g, 2, 96),
                      sec("Part B – Repeated addition", "eq", uniq(r, 6), 1, 32)])
    if day == 4:
        c = []
        for n in (2, 5, 10):
            for k in range(1, 11):
                c.append((f"{n} {TIMES} {k} = ____", n * k))
        rng.shuffle(c)
        return sheet(7, 4, t, "Multiply. Use skip counting to help you!", f"Example: 5 {TIMES} 4 = 20",
                     [sec("", "eq", c, 3, 30)])

    def oe():
        n = rng.randint(1, 40)
        return f"Is {n} odd or even?  ____", "even" if n % 2 == 0 else "odd"
    mixed = []
    for _ in range(9):
        a, b = rng.choice([2, 3, 4, 5, 10]), rng.randint(1, 10)
        mixed.append((f"{a} {TIMES} {b} = ____", a * b))
    w = words(rng, ["mult"], 2, 50)
    return sheet(7, 5, t, "Review day! Odd or even, mixed times tables, and word problems.",
                 "Example: Is 14 odd or even?  →  even (it ends in 4)",
                 [sec("Part A – Odd or even?", "eq", uniq(oe, 6), 2, 30),
                  sec("Part B – Multiply", "eq", mixed, 3, 30),
                  sec("Part C – Word problems", "word", w, 1, 78)])


def U8(day, rng):
    t = "Telling Time & Counting Money"
    if day == 1:
        return sheet(8, 1, t, "Write the time shown on each clock.", "Example: short hand on 3, long hand on 12  →  3:00",
                     [sec("", "clock", clock_cells(rng, 12, [0]), 3, 104)])
    if day == 2:
        return sheet(8, 2, t, "Write the time. The long hand on 6 means half past.", "Example: short hand past 7, long hand on 6  →  7:30",
                     [sec("", "clock", clock_cells(rng, 12, [0, 30]), 3, 104)])
    if day == 3:
        return sheet(8, 3, t, "Write the time. Count by 5s around the clock.", "Example: long hand on 3  →  15 minutes  →  4:15",
                     [sec("", "clock", clock_cells(rng, 12, [5 * i for i in range(12)]), 3, 104)])
    if day == 4:
        facts = [("1 dime = ____¢", 10), ("1 nickel = ____¢", 5), ("1 quarter = ____¢", 25),
                 ("1 penny = ____¢", 1), ("2 nickels = ____¢", 10), ("4 quarters = ____¢", 100)]
        return sheet(8, 4, t, "Count the money. Start with the biggest coin!",
                     "Example: 1 quarter, 1 dime, 3 pennies = 25 + 10 + 3 = 38¢",
                     [sec("Part A – Coin facts", "eq", [(a, str(b)) for a, b in facts], 3, 30),
                      sec("Part B – Count the coins", "eq", coin_cells(rng, 12), 1, 30)])
    w = words(rng, ["money", "money2"], 3, 60)
    return sheet(8, 5, t, "Review day! Time and money together.",
                 "Example: Start at 3:00. 2 hours later → 5:00",
                 [sec("Part A – Time later", "eq", later_cells(rng, 4), 1, 30),
                  sec("Part B – Clocks", "clock", clock_cells(rng, 3, [0, 15, 30, 45]), 3, 104),
                  sec("Part C – Money word problems", "word", w, 1, 70)])


SHAPES = [("triangle", 3), ("square", 4), ("rectangle", 4), ("pentagon", 5), ("hexagon", 6), ("octagon", 8)]


def U9(day, rng):
    t = "Shapes, Measuring & Fractions"
    if day == 1:
        c = []
        for nm, s in SHAPES:
            c.append((f"A {nm} has ____ sides.", s))
            c.append((f"A {nm} has ____ corners.", s))
        c += [("A circle has ____ straight sides.", 0), ("A cube has ____ flat faces.", 6)]
        rng.shuffle(c)
        return sheet(9, 1, t, "Fill in the blanks about shapes.", "Example: A triangle has 3 sides and 3 corners.",
                     [sec("", "eq", c, 2, 32)])
    if day == 2:
        c = [("Which is longer: 1 foot or 1 inch?  ____", "1 foot"),
             ("Which is longer: 1 meter or 1 centimeter?  ____", "1 meter"),
             ("12 inches = ____ foot", 1), ("100 centimeters = ____ meter", 1),
             ("Which is shorter: a pencil or a bus?  ____", "pencil"),
             ("A pencil is 7 in. long. A crayon is 3 in. long. How much longer is the pencil? ____ in.", 4),
             ("A ribbon is 15 cm. Another ribbon is 9 cm. How much longer is the first? ____ cm", 6),
             ("A table is 8 ft long. A rug is 5 ft long. How much shorter is the rug? ____ ft", 3),
             ("Use a ruler: the line is 6 cm. A line twice as long is ____ cm", 12),
             ("Would you measure a room in inches or feet?  ____", "feet"),
             ("Would you measure a bean in centimeters or meters?  ____", "centimeters"),
             ("2 feet = ____ inches", 24)]
        return sheet(9, 2, t, "Measure and compare lengths.", "Example: 12 inches = 1 foot",
                     [sec("", "eq", [(a, str(b)) for a, b in c], 1, 30)])
    if day == 3:
        def g():
            p = rng.choice([2, 3, 4, 6, 8])
            return (p, rng.randint(1, p - 1)), None
        cells = []
        for (p, s), _ in uniq(g, 12):
            cells.append(((p, s), f"{s}/{p}"))
        return sheet(9, 3, t, "Write the fraction. The bottom number is the equal parts. The top is the shaded parts.",
                     "Example: 3 shaded out of 4 equal parts = 3/4",
                     [sec("", "frac", cells, 3, 66)])
    if day == 4:
        def g():
            d, nm = rng.choice([(2, "Half"), (3, "A third"), (4, "A fourth")])
            n = d * rng.randint(2, 6 if d > 2 else 10)
            return f"{nm} of {n} = ____", n // d
        cmpf = [("Which is bigger: 1/2 or 1/4?  ____", "1/2"), ("Which is bigger: 1/3 or 1/2?  ____", "1/2"),
                ("Which is bigger: 1/4 or 1/3?  ____", "1/3"), ("How many halves make a whole? ____", 2),
                ("How many fourths make a whole? ____", 4), ("How many thirds make a whole? ____", 3)]
        return sheet(9, 4, t, "Share equally to find a half, a third or a fourth.",
                     "Example: Half of 10 = 5 (10 shared into 2 equal groups)",
                     [sec("Part A – Share equally", "eq", uniq(g, 12), 2, 30),
                      sec("Part B – Fractions", "eq", [(a, str(b)) for a, b in cmpf], 1, 30)])
    data = []
    for _ in range(3):
        a, b, c = rng.randint(3, 9), rng.randint(3, 9), rng.randint(3, 9)
        while len({a, b, c}) < 3:
            a, b, c = rng.randint(3, 9), rng.randint(3, 9), rng.randint(3, 9)
        fruit = rng.sample(["apples", "pears", "plums", "peaches", "lemons"], 3)
        data.append((a, b, c, fruit))
    qs = []
    for a, b, c, f in data:
        hdr = f"A graph shows {f[0]}: {a}, {f[1]}: {b}, {f[2]}: {c}. "
        qs.append((hdr + "How many fruits are there in all?", str(a + b + c)))
        top = max((a, f[0]), (b, f[1]), (c, f[2]))
        low = min((a, f[0]), (b, f[1]), (c, f[2]))
        qs.append((hdr + f"How many more {top[1]} than {low[1]}?", str(top[0] - low[0])))
    qs = qs[:5]
    rev = [("A hexagon has ____ sides.", 6), ("Half of 16 = ____", 8), ("100 cm = ____ m", 1),
           ("A fourth of 12 = ____", 3)]
    return sheet(9, 5, t, "Review day! Read the graph facts and solve.",
                 "Example: apples 5, pears 3. How many more apples? 5 – 3 = 2",
                 [sec("Part A – Graph problems", "word", qs, 1, 62),
                  sec("Part B – Quick review", "eq", [(a, str(b)) for a, b in rev], 2, 30)])


def U10(day, rng):
    t = "Word Problems & Challenges"
    if day == 1:
        w = words(rng, ["join", "sep", "diff"], 6, 20)
        return sheet(10, 1, t, "Read carefully. Write a number sentence, then the answer.",
                     "Example: 8 apples, 5 more.  8 + 5 = 13", [sec("", "word", w, 1, 78)])
    if day == 2:
        w = words(rng, ["join", "sep", "diff"], 6, 90)
        return sheet(10, 2, t, "Read carefully. Write a number sentence, then the answer.",
                     "Example: 45 stickers, 18 given away.  45 – 18 = 27", [sec("", "word", w, 1, 78)])
    if day == 3:
        w = words(rng, ["two"], 5, 40)
        return sheet(10, 3, t, "These problems have TWO steps. Do one step at a time.",
                     "Example: 12 + 5 = 17, then 17 – 4 = 13", [sec("", "word", w, 1, 82)])
    if day == 4:
        w = words(rng, ["mult", "money", "money2", "mult", "sep", "join"], 6, 60)
        return sheet(10, 4, t, "Is it adding, subtracting or multiplying? Decide, then solve.",
                     f"Example: 3 bags with 5 each.  3 {TIMES} 5 = 15", [sec("", "word", w, 1, 78)])

    def riddle():
        n = rng.randint(20, 90)
        k = rng.choice([("I am 10 more than", 10), ("I am 10 less than", -10), ("I am 5 more than", 5), ("I am double", None)])
        if k[1] is None:
            n = rng.randint(3, 25)
            return f"I am double {n}. What number am I?  ____", n * 2
        return f"{k[0]} {n}. What number am I?  ____", n + k[1]

    def pattern():
        step, s = rng.choice([2, 3, 4, 5, 10]), rng.randint(1, 10)
        v = [s + step * i for i in range(5)]
        return f"{v[0]}, {v[1]}, {v[2]}, {v[3]}, ____", v[4]

    def balance():
        a, b = rng.randint(2, 9), rng.randint(2, 9)
        c = rng.randint(1, a + b - 1)
        return f"{a} + {b} = ____ + {c}", a + b - c

    def digit():
        a, b = rng.randint(11, 59), rng.randint(11, 39)
        return f"{a // 10}____ + {b} = {a + b}", a % 10
    return sheet(10, 5, t, "Challenge day! Think carefully – you can do it!",
                 "Example: 4 + 5 = ____ + 3  →  6",
                 [sec("Part A – Who am I?", "eq", uniq(riddle, 6), 1, 32),
                  sec("Part B – What comes next?", "eq", uniq(pattern, 4), 2, 32),
                  sec("Part C – Make both sides equal", "eq", uniq(balance, 4), 2, 32),
                  sec("Part D – Missing digit", "eq", uniq(digit, 4), 2, 32)])


UNITS = {1: U1, 2: U2, 3: U3, 4: U4, 5: U5, 6: U6, 7: U7, 8: U8, 9: U9, 10: U10}


def unit_sheets(u, variant=0):
    """variant 0 = Sheet A, 1 = Sheet B (same skills, new problems)."""
    return [UNITS[u](d, random.Random(u * 100 + d + variant * 1000)) for d in range(1, 6)]


# ---------------------------------------------------------------- check-ups
def checkup_a():
    rng = random.Random(555)
    s = [sec("Counting", "seq", seq_rows(rng, 3, 20, 100, 1, 8, 3), 1, 36),
         sec("Which is bigger?", "cmp", cmp_cells(rng, 4, 10, 99, True), 4, 36),
         sec("Add", "eq", add_facts(rng, 6, 3, 12, 2, 9), 3, 30),
         sec("Subtract", "eq", sub_facts(rng, 6, 8, 18, 2, 9), 3, 30),
         sec("Two-digit, no regrouping", "vert", [vadd_nocarry(rng), vadd_nocarry(rng),
                                                  vsub_noborrow(rng), vsub_noborrow(rng)], 4, 78),
         sec("Carry and borrow", "vert", [vadd_carry(rng), vadd_carry(rng, True),
                                          vsub_borrow(rng), vsub_borrow(rng, True)], 4, 78),
         sec("Word problems", "word", words(rng, ["join", "sep"], 2, 60), 1, 78)]
    return sheet(0, "A", "Check-Up: Units 1–5", "Show what you know! Do your best on every question.",
                 "Aim for 90% or more before moving on to Unit 6.", s)


def final_test():
    rng = random.Random(999)
    s = [sec("Place value", "eq", [eq("352 = ____ hundreds ____ tens ____ ones", "3, 5, 2"),
                                    eq("600 + 40 + 7 = ____", 647),
                                    eq("100 more than 538 = ____", 638),
                                    eq("10 less than 470 = ____", 460)], 2, 32),
         sec("Which is bigger?", "cmp", cmp_cells(rng, 4, 100, 999, True), 4, 36),
         sec("3-digit add & subtract", "vert", [v3_add(rng), v3_sub(rng), vadd_carry(rng), vsub_borrow(rng)], 4, 78),
         sec("Skip counting & times tables", "eq", [eq(f"2 {TIMES} 7 = ____", 14), eq(f"5 {TIMES} 6 = ____", 30),
                                                    eq(f"10 {TIMES} 8 = ____", 80), eq("5, 10, 15, ____", 20),
                                                    eq("Is 27 odd or even?  ____", "odd"),
                                                    eq("4 + 4 + 4 = ____", 12)], 3, 30),
         sec("Time", "clock", clock_cells(rng, 3, [0, 15, 30, 45]), 3, 104),
         sec("Money", "eq", coin_cells(rng, 2), 1, 30),
         sec("Fractions", "frac", [((4, 3), "3/4"), ((3, 1), "1/3"), ((8, 5), "5/8")], 3, 66),
         sec("Shapes, measuring & sharing", "eq", [eq("A hexagon has ____ sides.", 6), eq("12 inches = ____ foot", 1),
                                                    eq("Half of 18 = ____", 9)], 3, 30),
         sec("Word problems", "word", words(rng, ["two", "mult", "money"], 3, 50), 1, 82)]
    return sheet(0, "F", "Final Test: Units 1–10", "You made it! Show everything you have learned.",
                 "Aim for 90% or more. Then it's certificate time!", s)
