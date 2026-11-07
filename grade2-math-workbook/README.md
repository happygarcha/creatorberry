# Grade 2 Math Mastery Workbook

A printable, Kumon-style (small steps, repetition, mastery) math workbook for Grade 2.

- `Grade2_Math_Mastery_Workbook.pdf` – the finished workbook (127 pages, US Letter)
- `generators.py` – problem generators (answers are computed from the problems)
- `build_workbook.py` – layout engine; run `python3 build_workbook.py` (needs `reportlab`)

Contents: parent guide, learning path (Common Core Grade 2 codes), progress tracker,
10 units (1 lesson + 5 days x 2 sheets A/B each), Check-Up (Units 1-5), Final Test,
certificate, and a full answer key.

## Grade 2 English Mastery Workbook

Same structure as the math book (10 units, 1 lesson + 5 days x 2 sheets A/B each, Check-Up,
Final Test, certificate, answer key), 128 pages.

- `Grade2_English_Mastery_Workbook.pdf` - the finished workbook
- `english_generators.py` - word banks, passages and sheet generators
- `build_english.py` - English lessons/art/front matter; reuses the layout engine in `build_workbook.py`

Run `python3 build_english.py`. Units: alphabet & ABC order, short/long vowels, blends/digraphs/word
families, nouns/verbs/plurals, sentences & punctuation, opposites/synonyms/compounds, past tense/
contractions/prefixes, reading comprehension, adjectives/homophones/word meaning, writing & challenges.
