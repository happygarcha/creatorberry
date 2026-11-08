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

## Grade 2 Science Mastery Workbook

Same structure again (10 units, 1 lesson + 5 days x 2 sheets A/B each, Check-Up, Final Test,
certificate, answer key), 128 pages, with drawn plant and water-cycle diagrams.

- `Grade2_Science_Mastery_Workbook.pdf` - the finished workbook
- `science_generators.py` - question banks, reading passages and sheet generators
- `build_science.py` - lessons, art, diagrams and front matter; reuses the shared layout engine

Run `python3 build_science.py`. Units: scientist skills, living things & plants, animals & habitats,
life cycles, matter, changing matter & the 3 Rs, water cycle, forces & motion, light/sound/heat,
weather/seasons/Earth.

## Grade 2 Social Studies Picture Workbook

Picture-first (very little reading): 10 units, 1 picture lesson + 5 days x 2 sheets A/B each, Check-Up,
Final Test, certificate, answer key, 126 pages. Every question is answered by choosing a picture, naming a
picture, counting, or reading a drawn map, graph, calendar or clock; Day 5 ends with a "Draw it!" box.

- `Grade2_SocialStudies_Picture_Workbook.pdf` - the finished workbook
- `sticons.py` - ~130 vector icons (people, places, vehicles, coins, symbols...) drawn in code, no image files
- `social_generators.py` - picture question generators
- `build_social.py` - picture lessons, maps/graphs/calendar drawers, front matter

Run `python3 build_social.py`.

## Grade 2 Health & Active Living Picture Workbook (Physical & Health Education)

Picture-first, 126 pages: 10 units (1 picture lesson + 5 days x 2 sheets A/B each), Check-Up, Final Test,
certificate, answer key. Drawn movement poses (run, jump, throw, catch...), body diagram, healthy plate,
foods, hygiene, feelings, fair play and outdoor-safety icons; Day 5 ends with a "Draw it!" box.

- `Grade2_PHE_Picture_Workbook.pdf` - the finished workbook
- `pheicons.py` - ~70 extra vector icons (action poses, body, food, hygiene, gear...)
- `phe_generators.py` - question generators
- `build_phe.py` - lessons, body/plate diagrams, front matter (reuses the picture drawers in `build_social.py`)

Run `python3 build_phe.py`. Units were rebuilt against the official BC Grade 2 PHE Big Ideas, Content and Curricular Competencies (curriculum.gov.bc.ca).


## Update: balanced mix, aligned to the official BC Grade 2 curriculum

The PHE and Social Studies workbooks were rebuilt as a **mix** (roughly a third pictures; the rest true/false,
fill-in-the-blank with a word bank, matching, short reading passages with questions, short answers and writing),
and aligned to the official Grade 2 Big Ideas / Content / Curricular Competencies on curriculum.gov.bc.ca.

- `Grade2_PHE_Workbook.pdf` - Health & Active Living (`build_phe.py`, `phe_generators.py`, `phe_text.py`, `pheicons.py`)
- `Grade2_SocialStudies_Workbook.pdf` - Social Studies (`build_ss.py`, `ss2_generators.py`, `ss_text.py`, `ss2icons.py`)
- shared: `mix.py` (turns picture sheets into mixed sheets), `mixdraw.py` (word bank + matching), `sticons.py` (icons)

Science still needs to be realigned to the official Grade 2 content (life cycles, changing materials, forces, water cycle).
