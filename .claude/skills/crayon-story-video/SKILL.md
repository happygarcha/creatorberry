---
name: "crayon-story-video"
description: "Make Crayon Capital-style cartoon story videos (a founder or company's rise told as a dry-humoured cartoon drama) for 16:9 YouTube or 9:16 Reels, rendered from code to MP4."
---

# Crayon-style story video

Use this for **story-driven explainers about AI companies, founders, deals and turning points** ("How Anthropic got to $2 trillion", "The kid who bet $35B on AI", "Why OpenAI almost died"). The video tells one person's or company's arc like a short film. A flat 2D cartoon world with **thick black outlines and cel shading**. A cast of **big round heads on bean bodies with stick legs**: the hero in colour, named side characters with white faces, the anonymous public as a grey silhouette crowd. Characters **act out scenes and speak lines**. Spoken lines appear as **white handwriting with a little tick** next to the speaker. Silent gags go in **white speech boxes**. **Black cards with typed handwriting** carry chapter titles and punchlines. The camera never stops moving: slow pushes, reveal pull-outs, punches onto details.

Two outputs from the same kit and the same script format:
- **YouTube long-form:** 16:9, 1920×1080, 8–20 min, chapters.
- **Instagram Reels / Shorts:** 9:16, 1080×1920, 40–90 s, one arc.

The pipeline:
1. The script becomes a voice track. The voice is the clock (`timeline.py`).
2. Every shot is built from SVG with the kit (`cc_kit.py`) or a shot template (`cc_shots.py`).
3. A keyframe runtime animates the shots, Playwright captures frames and ffmpeg encodes them.
4. Storyboard stills come first. The full render happens only after the user approves them.

**Originality rules (non-negotiable).** This copies a *style*, not a channel:
- Never reproduce Crayon Capital's characters, host mascot, name or thumbnails.
- Design the creator's own host mascot (see §2) and the cast for each story.
- **No real logos or product UIs.** Company names go on signs, plaques and newspapers in the kit's hand caps. `wordmark()` gives a generic icon plus the name. Brand colours are fine.
- **Real people appear as generic cast members.** They get one costume cue (hoodie, leather jacket, glasses, beard) plus a name label or plaque, never a facial likeness.
- Quotes attributed to real people must be real and sourced. Invented skit lines must be obviously comedic or framed as paraphrase ("basically:").

---

## 1. What the reference does (measured on 5 videos, 94 min)
The five reference videos cover J.P. Morgan, Steve Jobs/Apple, Anthropic, an AI hedge-fund founder and Elon Musk/SpaceX. 720p/1080p, 30 fps.

| Metric | Measured | Use |
|---|---|---|
| Length | 16.7–21.4 min | 10–18 min long-form |
| Shots | 239–373 per video | ~15 per minute |
| Cut rate | 12–17 per min | 14–16 per min |
| Shot length | median 3.0–4.2 s · p10 1.0–1.8 s · p90 5.8–9.2 s | one shot per sentence, 2–6 s; set-pieces up to 10 s |
| Narration | 138–153 wpm overall | budget 145 wpm (1,450 words ≈ 10 min) |
| Phrasing | speech in short bursts (mean 1.9 s); 85% of pauses are 0.3–1.2 s; ~12 pauses > 0.6 s per minute | `timeline.py` gaps: 0.35 s inside a sentence, 0.75 s after a full stop |
| Black cards | 0.6–2.1 per min, 2.5–9.7% of runtime, 1–5 s each | ~1.3 per min |
| Camera | ~85% of shots move: push-in 27–47%, pull-out reveal 12–43%, pan 11–26%, static 15–19% | see §3 |
| Music | soft bed ~12 dB under the voice (one video almost dry); outro music under the end card | `sfx_cc.bed` |
| End card | black "Subscribe" in brush script, 10–19 s | `end_card()` |
| Sponsor | 1 mid-roll at 4–6 min, ~60–75 s, entered via a story line ("…you'd become history." → "To simplify your chat history…") | §5 |

---

## 2. The look

**Linework and fill:**
- Every shape has a near-black outline `#161616`: ~4 px on characters, ~3 px on props and architecture, ~2 px on inner detail (canvas px; the render is 1.5×).
- Flat fills with **one hard-edged shade** on the side away from the light: heads, bodies and robots get a darker crescent clipped inside the shape (`_shade_clip`).
- No paper grain, no vignette, no gradients except the spotlight cone, the info backdrop blob and the globe glow.
- Glass gets two diagonal white streaks (windows, picture frames).
- Every standing figure gets a soft grey ellipse shadow under the feet.

**Palette** (constants in `cc_kit.py`):
- cream wall `#F5E2B3` · wood `#6B452E` · dark wood `#4E3121` · panelling `#5E3C29`
- info blue-grey `#8DA1B1` · stage `#232326` · red `#C0392F` · green `#3F9A50` · gold plaques `#D8A43A`
- Each video picks a **grade**: warm cream and wood for historical stories; cool desaturated greys and purples (`#8E9196`, `#7C7F99` walls) for tech stories; navy and teal night scenes for crisis chapters. Keep one grade per chapter.

**The cast (`person()`):**
- **Build:** a big round head (r 44, ~35% of the height) with dot eyes. Brows appear only for emotion; the mouth is one stroke. The body is a bean; arms and legs are thin black sticks with no hands or feet.
- **Expressions:** `neutral happy grin smug sad worried angry surprised shocked crying determined closed talk`.
- **Hero:** skin colour, a fixed outfit and **one signature trait**, visible in every shot. The reference uses a bulbous nose, a beard, round glasses or curly hair. Lock it in a model-sheet dict and reuse the dict (`DAD = dict(...)`).
- **Named side characters:** white faces (`skin='white'`) plus one costume cue (top hat, fedora, lab coat, moustache) and a plaque or label the first time they appear.
- **The public:** `crowd()`, overlapping grey silhouettes, sometimes with hats. Use it for markets, panics, audiences and "everyone".
- **AI models and products:** `robot()`, personified with a visor, glowing eyes and a chest emblem. Give each model a distinct body or emblem colour and a name tag. Use them for model races, podiums and robots doing a job.
- **Host mascot (`mascot()`):** the channel's narrator avatar. It pops into frame, big, for fourth-wall asides ("Just kidding. Let's be real for a second."), sponsor reads and the CTA. Build it from the creator's own look (hair, glasses, signature outfit) so the cartoon becomes a face the audience recognises. Ask once, then keep it identical forever.
- **Acting is small:** a head turn (`look=±5`, `flip`), an arm pose (`point_r`, `phone`, `chin`, `shrug`, `hold`, `present`, `up`, `hips`), walking (`walk=(t0, t1)` + a `tx` slide) and mouth flaps on voiced lines (`talk=(t0, t1)`). Pop-ins, sweat or tears for emphasis.

**Settings:**
- desk office (the workhorse, `office()` + `t_desk`), boardroom table, street with buildings, home living room
- spotlight stage (character introductions), blue-grey info backdrop (infographics), space with Earth (scale hooks)
- black (cards), comic panels (phone calls, "every department"), newspaper or document close-ups

**Shot sizes (vary them like a film):**
- wide establishing → medium two-shot → close-up on the line → **over-the-shoulder** reverse
- **extreme close-ups of objects:** a door handle, a signature, a stamped document, a typed letter
- top-down (maps, papers spread on a desk, railway tracks)
- split-screen with a jagged lightning divider for phone fights

---

## 3. Motion grammar
1. **Cut on the thought.** Each sentence or phrase gets a new shot. Hard cuts by default. Use a 0.3–0.5 s fade through black only between chapters (`xin`/`xout`).
2. **Every shot moves:**
   - **Push-in** 5–10%, linear, over the whole shot (`push(d, 1.07)`). The default.
   - **Reveal pull-out:** start at 1.35–1.5×, ease out to 1.0 over 2.4–3.5 s, then hold (`pull`). Use it for establishing shots, for "this is X" and to reveal a crowd.
   - **Pan** across a wide scene (`pan(d, dx)`, scaled 1.06–1.12 so the edges never show).
   - **Detail punch:** fast push to ~1.7–1.9× on a detail (a document, a face, a number) with ease-out, a hold, then back (`punch`, with `cam_o` on the detail).
3. **Dialogue appears whole.** A voiced line is on screen exactly while it is spoken (`appear(t0)`), with no typing. Bubbles **pop**. Thought clouds pop in, and their pictures pop in after them.
4. **Typing is for narration:**
   - black-card lines type on with the voice (`typewrite(t0, t1)`)
   - place captions and name labels type at ~16–18 characters per second
   - chapter titles appear instantly
5. **Infographics build on the words:** box A pops on its number, the arrow wipes, box B pops, then the label pops 0.45 s later. Bars grow with a back-ease; chart lines draw on.
6. **Panels slide in one per beat** (0.3 s, ease-out), e.g. four phone calls, four rejections.
7. **The strobe montage** (cold opens only): the company name stays fixed while the background flips every 0.12 s through 4–5 worlds it touches, then holds.
8. **Bookend:** the last minute re-uses earlier shots (a 0.7–1.5 s flashback montage of key moments), then the closing line.

---

## 4. Text system (the signature; get this right)
| Device | Looks | Rule |
|---|---|---|
| **Voiced line** `say()` | white Caveat 600, thin dark outline + soft shadow, a short white tick pointing at the mouth | The character actually says it in the VO (a character voice). It sits within ~1.5 head-widths of the speaker's head and moves with the scene. |
| **Silent gag** `bubble()` | white rounded box, black outline, tail, dark handwriting | The narrator keeps talking and paraphrases it ("His mother had one rule…" + box "College-educated parents only!"). Use it for jokes and for what people "would say". |
| **Shout** `bubble(shout=True)` | spiky burst | "Call an ambulance!", "Whaat?!" |
| **Thought** `thought()` | scalloped cloud + two trailing dots, a picture inside (rifles, a robot, a price) | plans, temptations, misunderstandings |
| **Narration card** `t_card()` | black, white Caveat ~44 px (54 in 9:16), typed with the voice | Punchlines and turns, often mid-sentence: "It did neither." / "Then comes the part that breaks him." / "Okay, back to the video." |
| **Chapter card** `t_card(title=True)` | black, larger, instant | 3–6 per video: "The Making of a …", "The Rise", "The Turning Point", "The $2 Trillion Bet" |
| **Place/date** `place_caption()` | white handwriting bottom-left, typed | first shot of every new place or time jump: "Connecticut, 1837.", "1980s, San Francisco." |
| **Name label** `label_arrow()` | white handwriting + curved arrow, typed | the first appearance of each named person |
| **Plaques and signs** `plaque()`, `sign()`, `post_sign()` | hand caps (Patrick Hand SC, skewed) on gold, wood or white | job titles, company names, places, "WALL STREET" |
| **Numbers** `price_box()`, `stat_card()`, `big text on black` | red/green boxes, a white card with big green caps, an old number struck through with a red line | **every number in the VO appears on screen** |
| **End card** `end_card()` | "Subscribe" in Caveat Brush on black | last 10–20 s, outro music |

Fonts come from npm `@fontsource` (Caveat, Caveat Brush, Patrick Hand SC), loaded locally. Never use any other font.

---

## 5. Story and script
**Long-form structure (12–18 min; scale proportionally):**
| Time | Beat | Notes |
|---|---|---|
| 0:00–0:25 | **Cold open** | Formula: **"This is X."** (name over its world) → **the present-day stake** (a giant number or event) → **the paradox** ("But he didn't lose because he was wrong. He lost because he was right.") → **the question** ("So how did one private banker become powerful enough to save America?") → **the pivot to origin** ("It all started with a kid named Dario." / "Well… meet young Morgan."). Strobe montage, newspaper, a spotlight on the hero. |
| 0:25 | Chapter 1 card | "The Making of a …" / "The Kid Who …" / "The Boy Who …" |
| 0:25–4:00 | **Origin** | place/date caption, family skit (2–4 voiced lines), the one childhood detail you will call back at the end, first lucky break or first scandal, "In simple terms, …" explanations |
| ~4:00–6:00 | **Sponsor slot** (if any) | Enter through a story line, mascot read, generic UI mock with lavender label pills, URL bar, "Click the link in the description", then a card "Okay, back to the video." |
| 4:00–13:00 | **Chapters 2–4** | each opens with a titled card, a setup scene, a rule-of-three escalation, a skit, an infographic of the key number, and ends on a **cliffhanger line** ("And next, he will control an entire industry.") |
| 13:00–16:00 | **Climax and judgement** | hearings, IPOs, crashes; a sharp quotable exchange; a "the problem is…" reflection ("A person is not a system.") |
| last 60 s | **Bookend** | the present day again, a flashback montage of key shots, the callback to the childhood detail, a real quote or a forward-looking line ("Now we wait and see if the kid actually reaches Mars.") → Subscribe card |

**Script voice:**
- Short declarative phrases; one image per phrase. Sentences often split across two shots ("…started collapsing. / Even the government turned to him for help.").
- Dry understatement and deflation: "Sensible. / Less sensible." "Freshly baked nepotism." "Okay, *extremely* disappointed."
- **Skits:** 2–6 voiced back-and-forth lines between characters, with the comic beat last ("This man is insane.").
- **Plain-English mechanics:** "In simple terms, he learned who had money, who needed money, and how to stand between them." Explain one mechanism per infographic.
- Rule of three, concrete numbers, then a modern-money conversion ("$480 million, about $17 billion today").
- Use "you" sparingly, for scale comparisons ("If you have $1, you are closer to him than he is to Elon.").
- **Call back** at least two early details in the ending.

**Script format = `script.json`** (one entry per shot; the shot list *is* the script):
```json
{"voices": {"N": 16, "dario": 13, "mom": 3}, "gap": [0.35, 0.75],
 "shots": [{"id": "c1_04", "vo": [{"text": "His father is an Italian leather craftsman."}], "min": 1.5},
           {"id": "c1_05", "vo": [{"text": "Leave him alone.", "who": "dario"}]},
           {"id": "c1_06", "min": 2.0}]}
```
- `who` picks the voice. The narrator is `N`; voiced dialogue uses the character's voice.
- Shots without `vo` are silent: chapter cards, establishing beats. Give them a `min`.
- Write numbers naturally ("$2 trillion", "2014", "LLMs"); `timeline.py` speaks them correctly. Add `"say"` only for names TTS mangles.

---

## 6. Reels (9:16) adaptation
- **Length 40–90 s; one arc** (one origin story, one deal, one scandal). Cut every 1.5–2.5 s (~25–35 cuts per minute), with the hook in the first 1.5 s ("This 24-year-old lost $35 billion… by being right.").
- **Structure:**
  1. hook: stake + paradox, 0–4 s
  2. "It started in …" plus a place caption
  3. 3–5 story beats, at least one voiced skit and one number card
  4. the twist
  5. a callback line
  6. CTA: the creator's usual ending, e.g. "Follow for part 2" or "Comment STORY and I'll send you the sources". The mascot can deliver it.
- **At most one** black card, ≤ 1 s, used as the punchline. Chapter titles become the on-screen hook text instead.
- **Layout:**
  - Canvas 720×1280 (renders at 1080×1920). Keep faces, text and numbers between **12% and 72% of the height**; Reels UI covers the bottom ~25% and the right edge.
  - Characters ~1.25–1.3× their 16:9 scale, heads at 45–55% of the height.
  - Two-shots stack diagonally; panels become a 2×2 grid; infographics go top-to-bottom with the arrow pointing down.
  - Text minimums: voiced lines 52, bubbles 46, cards 54–60, place captions 52, plaques 28.
  - Every template in `cc_shots.py` already does this when `set_format('9:16')`.
- **Cutting a Reel from a long video:** take one chapter's script entries, tighten the lines, add the hook and CTA shots, and rebuild with the same build code in 9:16. Never crop the 16:9 render.
- Loudness −14 LUFS; burn nothing else on top (the dialogue text already is the caption system).

---

## 7. Workflow
0. **Intake.** If anything is missing, ask once:
   - the topic and angle
   - format (YouTube 16:9, Reel 9:16, or both) and target length
   - voice: the user's recording or scratch TTS
   - the host mascot's look (first video only)
   - a sponsor or brand integration, if any
   Defaults: 10 min long-form, TTS narrator `N = 16` (US male, calm), character voices from `11, 13, 17, 18` (male) and `3, 9` (female).
1. **Research.** Verify every number, date, quote and name in current sources; keep a sources list for the description. Paraphrase real people unless the quote is verified.
2. **Script → `script.json`.** One entry per shot, ~145 wpm. Mark which lines are voiced dialogue (`who`), silent bubbles and cards. Check: 14–16 shots per minute, ~1.3 cards per minute, every number shown.
3. **Model sheet:**
   - one dict per character (skin, suit, hair, signature trait) and one background function per location (`office('#A9B4BC', night=True)`)
   - render a sheet of the cast and locations as stills and show it to the user
4. **Voice:**
   - `python3 timeline.py tts script.json vo` writes `vo.wav` and `vo.json`. Fix any `WARNING not in the TTS lexicon` words with `"say"`.
   - Or record yourself reading the script with natural pauses, then run `python3 timeline.py align script.json narration.wav vo`.
5. **Build** one file per chapter (`ch1.py` … each returns a list of `scene()`s from `vo.json`). Use `cc_shots` templates for most shots and hand-build the set-pieces with `cc_kit` + `G()` keyframes. One `page()` per chapter keeps the HTML small.
6. **Storyboard.** Render one still per shot (`render.py page.html sb --stills t1,t2,…` at ~70% of each shot), tile them into contact sheets, and **get approval before the full render**.
7. **Render** each chapter: `python3 render.py $PWD/ch1.html ch1.mp4 <start> <end>`. Expect ~0.09 s per frame on 2 vCPU, so a 10-min video takes ~25 min. Concatenate with `ffmpeg -f concat -safe 0 -i parts.txt -c copy video.mp4`.
8. **Sound:**
   - templates push SFX cues into `cc_shots.CUES`; add your own with `cue(name, t)`
   - music sections per chapter mood: `warm`, `tense`, `mystery`, `triumph`, with `dips` under cards
   - mix with `sfx_cc.bed` + `sfx_base.mix`, normalised to −14 LUFS
   - real SFX samples override the synths: drop `pop.wav`, `whoosh.wav`, `paper.wav`, `ding.wav`, etc. into `~/sfx`
   - mux: `ffmpeg -i video.mp4 -i final.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out.mp4`
9. **QA** (§11), then deliver the MP4, an SRT built from `vo.json`, chapter timestamps for the description, and the sources.

---

## 8. Setup
```bash
pip install --break-system-packages playwright sherpa-onnx soundfile numpy scipy pillow
python3 -m playwright install chromium   # or use an installed google-chrome; render.py auto-detects it
mkdir -p ~/fonts && npm i --prefix ~/fonts @fontsource/caveat @fontsource/caveat-brush @fontsource/patrick-hand-sc
mkdir -p ~/models && cd ~/models
B=https://github.com/k2-fsa/sherpa-onnx/releases/download
curl -sSL -O $B/tts-models/kokoro-int8-multi-lang-v1_0.tar.bz2 && tar xjf kokoro-int8-multi-lang-v1_0.tar.bz2
curl -sSL -O $B/asr-models/sherpa-onnx-whisper-base.en.tar.bz2 && tar xjf sherpa-onnx-whisper-base.en.tar.bz2
curl -sSL -O $B/asr-models/silero_vad.onnx
```
- Write the files in §9 into one folder (`kit/`) exactly as given.
- Hugging Face is often blocked in sandboxes; GitHub releases and npm usually work.
- Smoke test:
  ```bash
  python3 cc_example.py script && python3 timeline.py tts script.json vo && python3 cc_example.py build 16:9
  python3 render.py $PWD/example.html ex.mp4 0 36.6
  ```

---

## 9. Code

### runtime.js: deterministic keyframe player (`renderAt(t)`). Props: `o s sx sy tx ty r blur wipe draw chars words count`. Eases: `io o i l b h`.
```js
(function () {
  // Deterministic keyframe player. renderAt(T) shows the shots active at T and sets every animated prop.
  const FW = window.__FW || 1280, FH = window.__FH || 720;
  const E = {
    io: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
    o: t => 1 - Math.pow(1 - t, 3),
    i: t => t * t * t,
    l: t => t,
    b: t => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); },
    h: t => 0,
  };
  const items = [];
  const scenes = [...document.querySelectorAll('[data-start]')].map(el => ({
    el, start: +el.dataset.start, end: +el.dataset.end, xin: +(el.dataset.xin || 0), xout: +(el.dataset.xout || 0)
  }));
  document.querySelectorAll('[data-kf]').forEach(el => {
    const keys = JSON.parse(el.dataset.kf).sort((a, b) => a[0] - b[0]);
    const props = {};
    keys.forEach(([t, p, e]) => { for (const k in p) (props[k] = props[k] || []).push([t, p[k], e || 'io']); });
    const sc = el.closest('[data-start]');
    const it = { el, props, o: (el.dataset.o || (FW / 2) + ' ' + (FH / 2)).split(' ').map(Number), start: sc ? +sc.dataset.start : 0,
                 wb: el.dataset.wb ? el.dataset.wb.split(' ') : null, svg: el instanceof SVGElement };
    if (props.draw) {
      it.paths = [...el.querySelectorAll('path,line,polyline,circle,ellipse,rect')].concat(el.matches('path,line,polyline') ? [el] : [])
        .filter(p => (p.getAttribute('stroke') || 'none') !== 'none');
      it.paths.forEach(p => { p.setAttribute('pathLength', '1'); p.style.strokeDasharray = '1 1'; });
    }
    if (props.chars) { it.tnodes = []; const walk = n => { n.childNodes.forEach(c => { if (c.nodeType === 3) it.tnodes.push([c, c.textContent]); else walk(c); }); }; walk(el); it.nch = it.tnodes.reduce((a, [, s]) => a + s.length, 0); }
    if (props.words) it.words = [...el.querySelectorAll('.w')];
    if (props.count) it.fmt = el.dataset.fmt || 'int';
    if (it.svg) el.style.transformBox = 'view-box';
    items.push(it);
  });
  function val(arr, t) {
    if (t <= arr[0][0]) return arr[0][1];
    for (let i = 0; i < arr.length - 1; i++) {
      const [t0, v0] = arr[i], [t1, v1, e] = arr[i + 1];
      if (t < t1) { const p = t1 > t0 ? E[e]((t - t0) / (t1 - t0)) : 1; return v0 + (v1 - v0) * p; }
    }
    return arr[arr.length - 1][1];
  }
  const money = v => '$' + Math.round(v).toLocaleString('en-US');
  window.renderAt = function (T) {
    scenes.forEach(s => {
      const on = T >= s.start && T < s.end;
      s.el.style.display = on ? 'block' : 'none';
      if (on) {
        let op = 1;
        if (s.xin) op = Math.min(op, (T - s.start) / s.xin);
        if (s.xout) op = Math.min(op, (s.end - T) / s.xout);
        s.el.style.opacity = Math.max(0, Math.min(1, op));
      }
    });
    items.forEach(it => {
      const t = T - it.start, P = it.props, g = (k, d) => P[k] ? val(P[k], t) : d;
      const el = it.el;
      if (P.o) el.style.opacity = Math.max(0, Math.min(1, g('o', 1)));
      if (P.s || P.sx || P.sy || P.tx || P.ty || P.r) {
        const s = g('s', 1);
        el.style.transformOrigin = it.o[0] + 'px ' + it.o[1] + 'px';
        el.style.transform = 'translate(' + g('tx', 0) + 'px,' + g('ty', 0) + 'px) rotate(' + g('r', 0) + 'deg) scale(' + (s * g('sx', 1)) + ',' + (s * g('sy', 1)) + ')';
      }
      if (P.blur) { const b = g('blur', 0); el.style.filter = b > 0.05 ? 'blur(' + b + 'px)' : 'none'; }
      if (P.wipe) {
        const w = Math.max(0, Math.min(1, g('wipe', 1)));
        if (it.wb) {
          const [x0, y0, x1, y1, d] = it.wb; const X0 = +x0, Y0 = +y0, X1 = +x1, Y1 = +y1;
          let ins;
          if (d === 'r') ins = '0px ' + (FW - (X0 + (X1 - X0) * w)) + 'px 0px 0px';
          else if (d === 'l') ins = '0px 0px 0px ' + (X1 - (X1 - X0) * w) + 'px';
          else if (d === 'd') ins = '0px 0px ' + (FH - (Y0 + (Y1 - Y0) * w)) + 'px 0px';
          else ins = (Y1 - (Y1 - Y0) * w) + 'px 0px 0px 0px';
          el.style.clipPath = w >= 1 ? 'none' : 'inset(' + ins + ')';
        } else el.style.clipPath = w >= 1 ? 'none' : 'inset(0 ' + ((1 - w) * 100) + '% 0 0)';
      }
      if (P.draw) {
        const d = Math.max(0, Math.min(1, g('draw', 1)));
        it.paths.forEach(p => { p.style.strokeDashoffset = String(1 - d); p.style.visibility = d <= 0.001 ? 'hidden' : 'visible'; });
      }
      if (P.chars) {  // typewriter: reveal characters in document order
        let n = Math.round(Math.max(0, Math.min(1, g('chars', 1))) * it.nch);
        it.tnodes.forEach(([node, full]) => { const k = Math.max(0, Math.min(full.length, n)); node.textContent = full.slice(0, k); n -= full.length; });
      }
      if (P.words) {
        const w = g('words', 1) * it.words.length;
        it.words.forEach((s, i) => { s.style.opacity = Math.max(0, Math.min(1, (w - i) * 2.5)); });
      }
      if (P.count) {
        const v = g('count', 0);
        el.textContent = it.fmt === 'int' ? Math.round(v).toLocaleString('en-US') : it.fmt === 'money' ? money(v) : v.toFixed(1);
      }
    });
  };
  window.__ready = true;
})();
```

### animlib.py: format switch, keyframe presets, camera moves, `scene()` and `page()`.
```python
"""Keyframe presets, camera moves, shot wrapper and page assembly. Times are seconds LOCAL to the shot.
Call set_format('16:9') or set_format('9:16') before building anything."""
import json, os

FW, FH = 1280, 720   # logical canvas; render.py captures at 1.5x -> 1920x1080 or 1080x1920


def set_format(fmt):
    global FW, FH
    FW, FH = (1280, 720) if fmt == '16:9' else (720, 1280)
    return FW, FH


def J(k): return json.dumps(k, separators=(',', ':')).replace("'", '&#39;')


def A(html, keys, o=None, wb=None):
    """Full-frame HTML wrapper with a keyframe track; children use frame coordinates."""
    at = f" data-kf='{J(keys)}'" + (f' data-o="{o[0]} {o[1]}"' if o else '') + (f' data-wb="{" ".join(map(str, wb))}"' if wb else '')
    return f'<div class="a"{at} style="position:absolute;left:0;top:0;width:{FW}px;height:{FH}px;pointer-events:none">{html}</div>'


def G(inner, keys, o=None):
    """SVG <g> with a keyframe track (origin in viewBox px)."""
    return f"<g data-kf='{J(keys)}'" + (f' data-o="{o[0]} {o[1]}"' if o else '') + f'>{inner}</g>'


# ---- element presets
def pop(t, d=.28, s0=.6): return [[t, {'o': 0, 's': s0}], [t + .04, {'o': 1}], [t + d, {'s': 1}, 'b']]
def appear(t): return [[t - .001, {'o': 0}], [t, {'o': 1}, 'h']]          # hard on (dialogue lines, labels)
def vanish(t): return [[t - .001, {'o': 1}], [t, {'o': 0}, 'h']]
def fade(t, d=.25): return [[t, {'o': 0}], [t + d, {'o': 1}]]
def fout(t, d=.2): return [[t, {'o': 1}], [t + d, {'o': 0}]]
def wipe(t, d=.35): return [[t, {'wipe': 0}], [t + d, {'wipe': 1}, 'o']]
def slide(t, dx=0, dy=0, d=.32): return [[t, {'tx': dx, 'ty': dy, 'o': 0}], [t + .03, {'o': 1}], [t + d, {'tx': 0, 'ty': 0}, 'o']]
def draw(t, d=.4): return [[t, {'draw': 0}], [t + d, {'draw': 1}, 'o']]
def typewrite(t0, t1): return [[t0, {'chars': 0}], [t1, {'chars': 1}, 'l']]
def type_cps(t0, text, cps=22): return typewrite(t0, t0 + max(.15, len(text) / cps))
def count(t0, t1, v0, v1, e='o'): return [[t0, {'count': v0}], [t1, {'count': v1}, e]]
def slam(t, s0=1.8): return [[t, {'o': 0, 's': s0}], [t + .12, {'o': 1, 's': .95}, 'i'], [t + .22, {'s': 1}, 'o']]
def shake(t, amp=6, d=.24):
    return [[t, {'tx': 0}]] + [[t + d * (i + 1) / 5, {'tx': v}, 'l'] for i, v in enumerate([amp, -amp * .8, amp * .5, -amp * .3, 0])]
def bob(t0, t1, amp=4, period=.5, p='ty'):
    k, t, up = [[t0, {p: 0}]], t0, True
    while t < t1:
        t += period / 2; k.append([round(t, 3), {p: -amp if up else 0}, 'io']); up = not up
    return k
def wiggle(t0, t1, amp=4, period=.3, p='r'):
    k, t, s = [[t0, {p: 0}]], t0, 1
    while t < t1:
        t += period / 2; k.append([round(t, 3), {p: amp * s}, 'io']); s = -s
    return k + [[t + period / 2, {p: 0}, 'io']]
def flicker(t0, t1, period=.24, on_first=True):
    """Alternate visibility (mouth flap: give the open mouth flicker(), the closed mouth flicker(on_first=False))."""
    k, t, on = [[t0 - .001, {'o': 0 if on_first else 1}]], t0, on_first
    while t < t1:
        k.append([round(t, 3), {'o': 1 if on else 0}, 'h']); t += period / 2; on = not on
    return k + [[round(t1, 3), {'o': 0 if on_first else 1}, 'h']]


# ---- camera presets (apply to the shot via scene(cam=...))
def push(d, s1=1.07, s0=1.0, tx1=0, ty1=0): return [[0, {'s': s0, 'tx': 0, 'ty': 0}], [d, {'s': s1, 'tx': tx1, 'ty': ty1}, 'l']]
def pull(d, s0=1.4, s1=1.0, dur=None, tx0=0, ty0=0):
    """Reveal: start tight, ease out to the wide frame, then hold."""
    dur = dur or min(d, 3.2)
    return [[0, {'s': s0, 'tx': tx0, 'ty': ty0}], [dur, {'s': s1, 'tx': 0, 'ty': 0}, 'io']]
def pan(d, dx, dy=0, s=1.12): return [[0, {'s': s, 'tx': dx / 2, 'ty': dy / 2}], [d, {'s': s, 'tx': -dx / 2, 'ty': -dy / 2}, 'l']]
def punch(t, s1=1.7, d=.7, hold=None, back=.7, base=1.0):
    """Fast push to a detail (set the shot's cam origin on the detail), hold, optionally return."""
    k = [[0, {'s': base}], [t, {'s': base}], [t + d, {'s': s1}, 'o']]
    if hold is not None: k += [[t + d + hold, {'s': s1}], [t + d + hold + back, {'s': base}, 'io']]
    return k


def scene(start, end, inner, bg='#000', cam=None, cam_o=None, z=1, xin=0, xout=0):
    """One shot. start/end are GLOBAL seconds; every key inside is LOCAL to start. xin/xout = fade from/to black."""
    x = (f' data-xin="{xin}"' if xin else '') + (f' data-xout="{xout}"' if xout else '')
    o = cam_o or (FW / 2, FH / 2)
    c = (f"<div data-kf='{J(cam)}' data-o=\"{o[0]} {o[1]}\" style=\"position:absolute;inset:0\">" if cam
         else '<div style="position:absolute;inset:0">')
    return (f'<div data-start="{start:.3f}" data-end="{end:.3f}"{x} style="position:absolute;left:0;top:0;width:{FW}px;height:{FH}px;'
            f'overflow:hidden;display:none;z-index:{z};background:{bg}">{c}{inner}</div></div>')


def page(scenes, head='', bg='#000'):
    rt = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runtime.js')).read()
    return (f'<!doctype html><html><head><meta charset="utf-8">{head}<style>html,body{{margin:0;background:{bg}}}'
            f'#stage{{position:relative;width:{FW}px;height:{FH}px;overflow:hidden}}</style></head><body data-fw="{FW}" data-fh="{FH}">'
            f'<div id="stage">{"".join(scenes)}</div><script>window.__FW={FW};window.__FH={FH};</script><script>{rt}</script></body></html>')


def local_fonts(root, specs):
    """@font-face CSS from npm @fontsource packages: npm i --prefix <root> @fontsource/<pkg>.
    specs = [(family, pkg, weight, style)]."""
    css = ''.join(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};"
                  f"src:url(file://{root}/node_modules/@fontsource/{pkg}/files/{pkg}-latin-{w}-{st}.woff2)}}" for fam, pkg, w, st in specs)
    return f'<style>{css}</style>'
```

### render.py: frames to H.264 at 1.5× the canvas, or PNG stills for the storyboard.
```python
"""render.py page.html out.mp4 start end [--fps 30]   -> H.264 at 1.5x the canvas (1920x1080 or 1080x1920)
   render.py page.html prefix --stills t1,t2,...     -> PNG stills (storyboard)"""
import asyncio, sys, subprocess, shutil, re
from playwright.async_api import async_playwright


async def main(html, out, t0=0.0, t1=None, fps=30, stills=None):
    src = open(html).read(2_000_000)
    fw = int(re.search(r'data-fw="(\d+)"', src).group(1)); fh = int(re.search(r'data-fh="(\d+)"', src).group(1))
    exe = shutil.which('google-chrome') or shutil.which('chromium') or None
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=exe, args=['--allow-file-access-from-files', '--disable-gpu'])
        pg = await b.new_page(viewport={'width': fw, 'height': fh}, device_scale_factor=1.5)
        await pg.goto('file://' + html); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
        if stills:
            for t in stills:
                await pg.evaluate(f'renderAt({t})'); await pg.screenshot(path=f'{out}_{t:07.2f}.png')
        else:
            ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-',
                                   '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
            n = int(round((t1 - t0) * fps))
            for i in range(n):
                await pg.evaluate(f'renderAt({t0 + i / fps})')
                ff.stdin.write(await pg.screenshot(type='jpeg', quality=92))
                if i % 150 == 0: print(f'{t0 + i / fps:.1f}s', flush=True)
            ff.stdin.close(); ff.wait()
        await b.close()

a = sys.argv
fps = int(a[a.index('--fps') + 1]) if '--fps' in a else 30
if '--stills' in a:
    asyncio.run(main(a[1], a[2], stills=[float(x) for x in a[a.index('--stills') + 1].split(',')]))
else:
    asyncio.run(main(a[1], a[2], float(a[3]), float(a[4]), fps))
```

### timeline.py: voice-first timing: TTS per character (or align your own recording), numbers and acronyms spelled out, lexicon gaps fixed.
```python
"""Voice-first timing: the narration is the clock, every shot lasts as long as its lines plus a breath.
  python3 timeline.py tts   script.json out [lex us|gb]   -> out.wav + out.json (TTS scratch voice, one speaker per role)
  python3 timeline.py align script.json narration.wav out -> out.json (your own recording, matched to the script)
script.json = {"voices": {"N": 16, "dad": 11, "kid": 18}, "gap": [0.35, 0.8],
               "shots": [{"id": "s1", "vo": [{"text": "This is Nova Labs.", "who": "N"}, ...], "min": 1.2, "tail": 0.5}, ...]}
  - a shot with no "vo" is silent (black cards with no narration, place captions): give it "min".
  - "who" picks the voice; voiced dialogue lines use the character's voice, everything else the narrator "N".
  - "say" (optional) = spoken spelling when the display text would be mispronounced ("$2T" -> "two trillion dollars").
out.json = {"total": T, "shots": [{"id", "start", "end", "lines": [{"text", "who", "t0", "t1", "words": [[w, t0, t1], ...]}]}]}
Every time inside a shot (t0/t1/words) is LOCAL to that shot - use it directly in the shot's keyframes."""
import sys, json, os, difflib, numpy as np, soundfile as sf

MD = os.environ.get('MODELS', os.path.expanduser('~/models'))
SR = 24000


def word_times(text, L, lead=0.0):
    ws = text.split()
    wt = [len(w.strip('.,:;!?…—"')) + 1.2 + (2.2 if w[-1] in '.,:;!?…' else 0) for w in ws]
    tot, acc, out = sum(wt), 0, []
    for w, k in zip(ws, wt):
        t0 = lead + L * acc / tot
        acc += k
        out.append([w, round(t0, 3), round(lead + L * acc / tot, 3)])
    return out


def trim(x, thr=.005):
    i = np.where(np.abs(x) > thr)[0]
    return x if len(i) == 0 else x[max(0, i[0] - int(.03 * SR)): i[-1] + int(.06 * SR)]


ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = 'x x twenty thirty forty fifty sixty seventy eighty ninety'.split()


def num_words(n):
    n = int(n)
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ('' if n % 10 == 0 else ' ' + ONES[n % 10])
    if n < 1000: return ONES[n // 100] + ' hundred' + ('' if n % 100 == 0 else ' ' + num_words(n % 100))
    for v, w in ((10 ** 12, 'trillion'), (10 ** 9, 'billion'), (10 ** 6, 'million'), (1000, 'thousand')):
        if n >= v: return num_words(n // v) + ' ' + w + ('' if n % v == 0 else ' ' + num_words(n % v))


def spoken(text):
    """Display text -> what TTS should say: numbers, years, $, % and acronyms written out."""
    import re
    def money(m):
        num, scale = m.group(1).replace(',', ''), (m.group(2) or '').strip()
        if '.' in num and not scale:
            d, c = num.split('.'); return f"{num_words(d)} dollars{' and ' + num_words(c.ljust(2, '0')[:2]) + ' cents' if int(c) else ''}"
        w = ' point '.join([num_words(num.split('.')[0])] + ([' '.join(ONES[int(ch)] for ch in num.split('.')[1])] if '.' in num else []))
        return f'{w} {scale + " " if scale else ""}dollars'
    t = re.sub(r'\$([\d,]+(?:\.\d+)?)(\s+(?:thousand|million|billion|trillion))?', money, text)
    t = re.sub(r'(\d+(?:\.\d+)?)%', lambda m: m.group(1) + ' percent', t)
    def year(m):
        n = int(m.group(0))
        if 1100 <= n <= 1999 or 2010 <= n <= 2099: return num_words(n // 100) + ' ' + (num_words(n % 100) if n % 100 >= 10 else ('hundred' if n % 100 == 0 else 'oh ' + num_words(n % 100)))
        return num_words(n)
    t = re.sub(r'\b(1[1-9]\d\d|20\d\d)s\b', lambda m: year(re.match(r'\d+', m.group(0))).replace('ty', 'ties') if m.group(0)[-3] != '0' else year(re.match(r'\d+', m.group(0))) + 's', t)
    t = re.sub(r'\b(1[1-9]\d\d|20\d\d)\b', year, t)
    t = re.sub(r'(\d+)\.(\d+)', lambda m: num_words(m.group(1)) + ' point ' + ' '.join(ONES[int(c)] for c in m.group(2)), t)
    t = re.sub(r'[\d,]*\d', lambda m: num_words(m.group(0).replace(',', '')), t)
    LET = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'ay bee see dee ee eff gee aitch eye jay kay el em en oh pee queue are ess tee you vee double-you ex why zee'.split()))
    t = re.sub(r"\b([A-Z]{2,5})(s?)\b", lambda m: ' '.join(LET[c] for c in m.group(1)) + ('s' if m.group(2) else ''), t)
    return t


def fix_lexicon(lexf, texts):
    """Kokoro silently DROPS words missing from its lexicon. Derive entries for inflections (-s, -ed, -ing, 's,
    hyphenated) from base words, append them to the lexicon and return what is still missing."""
    import re
    lex = {}
    for line in open(lexf, encoding='utf-8'):
        p = line.rstrip('\n').split(' ', 1)
        if len(p) == 2: lex[p[0]] = p[1]
    vl = set('p t k f θ s ʃ tʃ'.split())
    def guess(w):
        if w in lex: return lex[w]
        if '-' in w:
            parts = [guess(x) for x in w.split('-') if x]
            return ' '.join(parts) if all(parts) else None
        for suf in ("'s", 's', 'es'):
            if w.endswith(suf) and len(w) > len(suf) + 2:
                b = guess(w[:-len(suf)])
                if b: last = b.split()[-1]; return b + (' ᵻ z' if last in ('s', 'z', 'ʃ', 'ʒ', 'tʃ', 'dʒ') else (' s' if last in vl else ' z'))
        if w.endswith('ed') and len(w) > 4:
            for base in (w[:-2], w[:-1], w[:-3]):
                b = lex.get(base)
                if b: last = b.split()[-1]; return b + (' ᵻ d' if last in ('t', 'd') else (' t' if last in vl else ' d'))
        if w.endswith('ing') and len(w) > 5:
            for base in (w[:-3], w[:-3] + 'e', w[:-4]):
                if base in lex: return lex[base] + ' ɪ ŋ'
        if w.endswith('ly') and w[:-2] in lex: return lex[w[:-2]] + ' l i'
        return None
    add, missing = {}, set()
    for t in texts:
        for w in re.findall(r"[a-z][a-z'\-]*", t.lower()):
            w = w.strip("'-")
            if not w or w in lex or w in add: continue
            gph = guess(w)
            if gph: add[w] = gph
            else: missing.add(w)
    if add:
        with open(lexf, 'a', encoding='utf-8') as f: f.write(''.join(f'{k} {v}\n' for k, v in add.items()))
    return sorted(missing)


def gap_after(text, g):
    """Short breath inside a sentence, a longer one after a full stop / question (measured 0.3-1.2 s)."""
    return g[1] if text.rstrip()[-1:] in '.?!…' else g[0]


def layout(script, durs):
    """durs[(shot_i, line_i)] = seconds of audio. Returns timeline dict + placements [(global_t, key)]."""
    g = script.get('gap', [0.35, 0.8])
    t, shots, place = 0.0, [], []
    for si, sh in enumerate(script['shots']):
        st, lt, lines = t, 0.0, []
        for li, ln in enumerate(sh.get('vo', [])):
            L = durs[(si, li)]
            lines.append({'text': ln['text'], 'who': ln.get('who', 'N'), 't0': round(lt, 3), 't1': round(lt + L, 3),
                          'words': word_times(ln['text'], L, lt)})
            place.append((st + lt, (si, li)))
            lt += L + gap_after(ln['text'], g)
        if lines: lt = lines[-1]['t1'] + sh.get('tail', gap_after(lines[-1]['text'], g))
        lt = max(lt, sh.get('min', 0))
        shots.append({'id': sh['id'], 'start': round(st, 3), 'end': round(st + lt, 3), 'lines': lines})
        t = st + lt
    return {'total': round(t, 3), 'shots': shots}, place


def tts(script_p, out, lex='us'):
    import sherpa_onnx
    script = json.load(open(script_p))
    voices = script.get('voices', {'N': 16})
    M = f'{MD}/kokoro-int8-multi-lang-v1_0/'
    lexf = M + f'lexicon-x{lex}-en.txt'
    if not os.path.exists(lexf):  # words missing from the stock lexicon are SILENTLY DROPPED - add them here
        extra = {'apps': 'ˈ æ p s', 'resources': 'ɹ ˈ i s ɔ ɹ s ᵻ z', 'ai': 'ˌ e ɪ ˈ a ɪ', 'llm': 'ˌ ɛ l ɛ l ˈ ɛ m'}
        open(lexf, 'w').write(open(M + f'lexicon-{lex}-en.txt').read() + ''.join(f'{k} {v}\n' for k, v in extra.items()))
    say = {(si, li): ln.get('say', spoken(ln['text'])) for si, sh in enumerate(script['shots']) for li, ln in enumerate(sh.get('vo', []))}
    miss = fix_lexicon(lexf, say.values())
    if miss: print('WARNING - not in the TTS lexicon, these words will be SKIPPED: ' + ', '.join(miss) + '\n  -> give those lines a "say" spelling (e.g. "Anthropic" -> "an thropic").', file=sys.stderr)
    eng = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(model=M + 'model.int8.onnx', voices=M + 'voices.bin', tokens=M + 'tokens.txt',
                                                       data_dir=M + 'espeak-ng-data', lexicon=lexf, dict_dir=M + 'dict'), num_threads=2)))
    clips, durs = {}, {}
    for si, sh in enumerate(script['shots']):
        for li, ln in enumerate(sh.get('vo', [])):
            sid = voices.get(ln.get('who', 'N'), voices['N'])
            a = eng.generate(say[(si, li)], sid=sid, speed=ln.get('speed', script.get('speed', 1.0)))
            x = trim(np.array(a.samples, dtype=np.float32))
            clips[(si, li)], durs[(si, li)] = x, len(x) / SR
    tl, place = layout(script, durs)
    total = np.zeros(int((tl['total'] + 1) * SR), np.float32)
    for t, k in place:
        x = clips[k]; s = int(t * SR); total[s:s + len(x)] += x
    sf.write(out + '.wav', total, SR)
    json.dump(tl, open(out + '.json', 'w'), indent=1)
    print(f'{out}.wav  {tl["total"]:.1f}s  {len(tl["shots"])} shots')


def align(script_p, wav, out):
    """Match your own narration to the script: Whisper words -> script words (difflib), then shot times from the matches."""
    import sherpa_onnx
    from scipy.signal import resample_poly
    script = json.load(open(script_p))
    x, sr = sf.read(wav, dtype='float32')
    x = x.mean(1) if x.ndim > 1 else x
    x = resample_poly(x, 16000, sr).astype(np.float32)
    Wd = f'{MD}/sherpa-onnx-whisper-base.en/'
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=Wd + 'base.en-encoder.int8.onnx', decoder=Wd + 'base.en-decoder.int8.onnx', tokens=Wd + 'base.en-tokens.txt', num_threads=2)
    cfg = sherpa_onnx.VadModelConfig(); cfg.silero_vad.model = f'{MD}/silero_vad.onnx'; cfg.silero_vad.min_silence_duration = .25
    cfg.silero_vad.max_speech_duration = 20; cfg.sample_rate = 16000
    vad, heard = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=600), []
    def flush():
        while not vad.empty():
            seg = vad.front; st = seg.start / 16000; s = rec.create_stream(); s.accept_waveform(16000, np.array(seg.samples, np.float32)); rec.decode_stream(s)
            heard.extend([[w, st + a, st + b] for w, a, b in word_times(s.result.text.strip() or '-', len(seg.samples) / 16000)]); vad.pop()
    for i in range(0, len(x), 512): vad.accept_waveform(x[i:i + 512]); flush()
    vad.flush(); flush()
    norm = lambda w: ''.join(c for c in w.lower() if c.isalnum())
    sw = [(si, li, wi, w) for si, sh in enumerate(script['shots']) for li, ln in enumerate(sh.get('vo', [])) for wi, w in enumerate(ln.get('say', ln['text']).split())]
    sm = difflib.SequenceMatcher(None, [norm(w[3]) for w in sw], [norm(h[0]) for h in heard], autojunk=False)
    t_of = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n): t_of[a + k] = (heard[b + k][1], heard[b + k][2])
    # interpolate unmatched words
    known = sorted(t_of)
    for i in range(len(sw)):
        if i not in t_of:
            prev = max([k for k in known if k < i], default=None); nxt = min([k for k in known if k > i], default=None)
            p = t_of[prev][1] if prev is not None else 0.0; q = t_of[nxt][0] if nxt is not None else p + .4
            t_of[i] = (p, max(p + .05, q))
    lines = {}
    for i, (si, li, wi, w) in enumerate(sw): lines.setdefault((si, li), []).append((w, *t_of[i]))
    g = script.get('gap', [0.35, 0.8]); shots, prev_end = [], 0.0
    for si, sh in enumerate(script['shots']):
        ls = [lines[(si, li)] for li in range(len(sh.get('vo', [])))]
        st = prev_end
        if ls: st = min(st, ls[0][0][1] - .05) if shots else 0.0
        out_l = [{'text': ln['text'], 'who': ln.get('who', 'N'), 't0': round(w[0][1] - st, 3), 't1': round(w[-1][2] - st, 3),
                  'words': [[a, round(b - st, 3), round(c - st, 3)] for a, b, c in w]} for ln, w in zip(sh.get('vo', []), ls)]
        end = (ls[-1][-1][2] + sh.get('tail', g[0])) if ls else st + sh.get('min', 1.0)
        end = max(end, st + sh.get('min', 0))
        shots.append({'id': sh['id'], 'start': round(st, 3), 'end': round(end, 3), 'lines': out_l}); prev_end = end
    for a, b in zip(shots, shots[1:]): a['end'] = b['start']  # no gaps between shots
    json.dump({'total': shots[-1]['end'], 'shots': shots}, open(out + '.json', 'w'), indent=1)
    print(f'{out}.json  {shots[-1]["end"]:.1f}s  matched {len(t_of)}/{len(sw)} words')


if __name__ == '__main__':
    a = sys.argv
    if a[1] == 'tts': tts(a[2], a[3], a[4] if len(a) > 4 else 'us')
    else: align(a[2], a[3], a[4])
```

### sfx_base.py: synth core and the mixer (bed ducked under the voice, −14 LUFS).
```python
import json, subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
SR = 48000
rng = np.random.default_rng(3)
def env(n, a=.005, d=.2):
    t = np.arange(n) / SR
    return np.exp(-t / max(d, 1e-4)) * np.minimum(1, t / max(a, 1e-4))
def filt(x, f, kind, o=2): return sosfilt(butter(o, f, btype=kind, fs=SR, output='sos'), x)
def sine(f, d):
    n = int(d * SR)
    return np.sin(2 * np.pi * np.cumsum(np.broadcast_to(f, (n,))) / SR)
def noise(d): return rng.standard_normal(int(d * SR))
def tick(f=2200, d=.03, g=.3): return g * sine(f, .06) * env(int(.06 * SR), .001, d)
def click(g=.5): return g * filt(noise(.02), 2500, 'high') * env(int(.02 * SR), .0005, .004)
def thud(f=65, g=.8, d=.15):
    n = int(.35 * SR)
    return g * (sine(f * (1 + 1.5 * np.exp(-np.arange(n) / SR / .03)), .35) * env(n, .002, d) + .25 * filt(noise(.35), 400, 'low') * env(n, .001, .03))
def whoosh(d=.45, g=.4, lo=300, hi=4000):
    n, x, out = int(d * SR), noise(d), np.zeros(int(d * SR))
    for i in range(0, n, 256):
        fc = lo + (hi - lo) * np.sin(np.pi * i / n)
        out[i:i + 256] = filt(x[max(0, i - 2048):i + 256], [max(60, fc * .5), min(20000, fc * 1.5)], 'band')[-len(x[i:i + 256]):]
    return g * out * np.sin(np.pi * np.arange(n) / n) ** 1.5
def chime(f=880, g=.3, d=1.1):
    n = int(d * SR)
    return g * sum(a * sine(f * m, d) * env(n, .002, d * dd) for m, a, dd in ((1, 1, .5), (2.01, .5, .3), (3.02, .25, .2)))
def place(buf, x, t, gain=1.0, pan=0.0):
    s = int(t * SR)
    if 0 <= s < len(buf):
        x = x[:len(buf) - s]
        buf[s:s + len(x), 0] += x * gain * np.cos((pan + 1) * np.pi / 4) * 1.414
        buf[s:s + len(x), 1] += x * gain * np.sin((pan + 1) * np.pi / 4) * 1.414
def mix(vo_wav, fx, bed, out_wav, duck=.45):
    """fx/bed: (n,2) float arrays at 48 kHz. Bed is ducked under the voice; final file loudness-normalised to -14 LUFS (YouTube)."""
    n = len(fx)
    vo, vsr = sf.read(vo_wav, dtype='float32')
    vo = resample_poly(vo, SR, vsr)[:n]
    vo = np.pad(vo, (0, n - len(vo))) / (np.sqrt(np.mean(vo[np.abs(vo) > .01] ** 2)) + 1e-9) * .16
    d = 1 - duck * np.clip(filt(np.abs(vo), 8, 'low') / .05, 0, 1)
    o = np.tanh((vo[:, None] + fx * .55 + bed * d[:, None]) * 1.1) / 1.1
    sf.write(out_wav + '.tmp.wav', (o * .89 / np.max(np.abs(o))).astype(np.float32), SR)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out_wav + '.tmp.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', str(SR), out_wav], check=True)
```

### sfx_cc.py: music-bed moods and the light SFX palette; real samples in `~/sfx` override them.
```python
"""Sound palette for the story-cartoon style: a soft looped music bed (~12 dB under the voice, ducked while
speaking) plus light, sparse SFX. Real samples win: put <name>.wav files in $SFX_DIR (e.g. pop.wav, whoosh.wav,
paper.wav, ding.wav, thud.wav, phone.wav, crowd.wav, coins.wav, type.wav) and fx(name) loads them instead of synthesising."""
import os
from sfx_base import *

SFX_DIR = os.environ.get('SFX_DIR', os.path.expanduser('~/sfx'))


def _load(name):
    p = os.path.join(SFX_DIR, name + '.wav')
    if not os.path.exists(p): return None
    x, sr = sf.read(p, dtype='float32')
    x = x.mean(1) if x.ndim > 1 else x
    return resample_poly(x, SR, sr) if sr != SR else x


def tone(f, d, g=.3, decay=.6, partials=((1, 1), (2, .45), (3, .18), (4, .08))):
    """Soft piano/pluck note: decaying sine partials (vectorised, fast)."""
    n = int(d * SR); t = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * m / decay) for m, a in partials)
    return g * x * np.minimum(1, t / .004)


def pop(g=.35):
    d = .12; t = np.arange(int(d * SR)) / SR
    return g * np.sin(2 * np.pi * (900 - 2600 * t) * t) * np.exp(-t / .03)


def paper(g=.25):
    d = .35; n = int(d * SR)
    return g * filt(noise(d), [1500, 7000], 'band') * np.exp(-np.arange(n) / SR / .09) * (1 + .6 * np.sin(2 * np.pi * 30 * np.arange(n) / SR))


def ding(g=.28): return chime(1318, g, 1.2)


def coins(g=.2):
    out = np.zeros(int(.6 * SR))
    for k, f in enumerate((2637, 3136, 2349, 3520)):
        x = chime(f, .5, .3); s = int(k * .06 * SR); out[s:s + len(x)] += x[:len(out) - s]
    return g * out


def phone(g=.18, d=1.2):
    n = int(d * SR); t = np.arange(n) / SR
    bell = (np.sin(2 * np.pi * 1700 * t) + np.sin(2 * np.pi * 2100 * t)) * (np.sin(2 * np.pi * 20 * t) > 0)
    return g * bell * np.where((t % .6) < .4, 1, 0)


def crowd(d=3.0, g=.12):
    n = int(d * SR); t = np.arange(n) / SR
    return g * filt(noise(d), [300, 2500], 'band') * (0.7 + .3 * np.sin(2 * np.pi * 1.3 * t) * np.sin(2 * np.pi * .7 * t)) * np.minimum(1, np.minimum(t, d - t) / .3)


def typing(nchars, cps=22, g=.06):
    d = nchars / cps + .1; out = np.zeros(int(d * SR))
    for k in range(nchars):
        if rng.random() < .15: continue
        x = tick(rng.uniform(1800, 2600), .012, 1); s = int(k / cps * SR); out[s:s + len(x)] += x[:len(out) - s]
    return g * out


def boom(g=.5): return thud(48, g, .5)


SYNTH = {'pop': pop, 'whoosh': lambda: whoosh(.4, .3), 'paper': paper, 'ding': ding, 'thud': lambda: thud(60, .6, .14),
         'coins': coins, 'phone': phone, 'crowd': crowd, 'boom': boom, 'click': lambda: click(.4)}


def fx(name, **kw):
    x = _load(name)
    return x if x is not None else SYNTH[name](**kw)


MOODS = {  # chord roots + quality per bar, tempo
    'warm': (76, [(261.6, 'M'), (196.0, 'M'), (220.0, 'm'), (174.6, 'M')]),
    'tense': (70, [(220.0, 'm'), (174.6, 'M'), (261.6, 'M'), (196.0, 'M')]),
    'mystery': (60, [(146.8, 'm'), (146.8, 'm'), (155.6, 'M'), (130.8, 'M')]),
    'triumph': (84, [(261.6, 'M'), (349.2, 'M'), (392.0, 'M'), (261.6, 'M')]),
}


def bed_loop(mood='warm', bars=4, g=.16):
    """One seamless loop of soft arpeggiated piano (bars x 4 beats)."""
    bpm, prog = MOODS[mood]
    beat = 60 / bpm; L = int(bars * 4 * beat * SR)
    out = np.zeros(L + SR * 3)
    for b in range(bars):
        root, q = prog[b % len(prog)]
        third = root * (2 ** ((4 if q == 'M' else 3) / 12)); fifth = root * 1.5
        notes = [root, fifth, root * 2, third * 2, fifth * 2, third * 2, root * 2, fifth]
        for k, f in enumerate(notes):
            s = int((b * 4 + k * .5) * beat * SR); x = tone(f, 2.2, .22 if k else .3, .9); out[s:s + len(x)] += x
        x = tone(root / 2, 3.5, .35, 1.6, ((1, 1), (2, .3))); s = int(b * 4 * beat * SR); out[s:s + len(x)] += x
    tail = out[L:L + SR * 3].copy(); out = out[:L]; out[:len(tail)] += tail[:L]   # wrap the ring-out
    return g * filt(out, 5000, 'low')


def bed(total, sections, dips=()):
    """sections = [(t0, t1, mood)]; dips = [(t0, t1, gain)] e.g. under black cards or for a dramatic silence.
    Returns (n, 2) stereo array at 48 kHz."""
    n = int(total * SR); out = np.zeros(n)
    for t0, t1, mood in sections:
        lp = bed_loop(mood); s, e = int(t0 * SR), min(n, int(t1 * SR))
        seg = np.resize(lp, e - s)
        f = min(int(.8 * SR), (e - s) // 2); ramp = np.ones(e - s); ramp[:f] = np.linspace(0, 1, f); ramp[-f:] = np.linspace(1, 0, f)
        out[s:e] += seg * ramp
    for t0, t1, gn in dips:
        s, e = int(t0 * SR), min(n, int(t1 * SR)); out[s:e] *= gn
    return np.stack([out, out], 1)
```

### cc_kit.py: the look: cast, crowds, robots, the text devices, settings and props.
```python
"""Crayon-style story cartoon kit: thick black outlines, flat cel-shaded fills, round-head bean-body cast,
grey crowds, handwritten dialogue. All drawing is SVG in the logical canvas (1280x720 or 720x1280; see animlib.set_format).
Every function returns an SVG string. (x, y) for characters/props = the point on the ground between the feet / base."""
import math, random, html as _html
import animlib

# ------------------------------------------------------------------ palette
INK = '#161616'                      # every outline
LW = 4.2                             # character outline
LW2 = 3.2                            # props / architecture
LW3 = 2.2                            # inner detail lines
SKIN = {'peach': ('#F3CDA1', '#DDAE80'), 'tan': ('#E2B184', '#C8956A'), 'brown': ('#B9805A', '#9C6744'),
        'deep': ('#7E5238', '#683F29'), 'white': ('#FFFFFF', '#D8D8D8'), 'grey': ('#9A9A9A', '#7E7E7E')}
SUIT = {'black': ('#2B2C30', '#1D1E21'), 'navy': ('#2F3D5C', '#232E47'), 'brown': ('#6E4C36', '#573A28'),
        'grey': ('#8E9196', '#74777C'), 'maroon': ('#7C2F35', '#622328'), 'olive': ('#5E6440', '#4A4F31'),
        'cream': ('#EDE6D6', '#D3CAB6'), 'blue': ('#4D6FA3', '#3C5986'), 'teal': ('#3E7C7A', '#2F6260'),
        'green': ('#5C8A4E', '#4A7140'), 'orange': ('#D9772E', '#B95F20'), 'pink': ('#C66B86', '#A85570'),
        'hoodie': ('#3A3D44', '#2A2D33'), 'labcoat': ('#F4F4F2', '#D9D9D4')}
HAIR = {'black': '#222224', 'dark': '#3A2C24', 'brown': '#6E4A30', 'auburn': '#8A3F2A', 'blonde': '#D9B062', 'grey': '#BDBDBD', 'white': '#EDEDED'}
RED, GREEN, GOLD, BLUE = '#C0392F', '#3F9A50', '#D8A43A', '#3E6FA8'
CREAM_WALL, WOOD, WOOD_D, PANEL = '#F5E2B3', '#6B452E', '#4E3121', '#5E3C29'
INFO_BG, INFO_BLOB = '#8DA1B1', '#A9BAC6'
SCRIPT = "font-family:'Caveat',cursive;font-weight:600"      # dialogue, bubbles, cards, captions
SCRIPT_B = "font-family:'Caveat Brush','Caveat',cursive"     # end card / big words
CAPS = "font-family:'Patrick Hand SC',cursive"               # signs, plaques, labels, numbers
FONT_SPECS = [('Caveat', 'caveat', 400, 'normal'), ('Caveat', 'caveat', 600, 'normal'), ('Caveat', 'caveat', 700, 'normal'),
              ('Caveat Brush', 'caveat-brush', 400, 'normal'), ('Patrick Hand SC', 'patrick-hand-sc', 400, 'normal')]
_uid = [0]


def uid(p='u'):
    _uid[0] += 1
    return f'{p}{_uid[0]}'


def esc(t): return _html.escape(str(t), quote=False)
def W(): return animlib.FW
def H(): return animlib.FH


def g(x, y, s, inner, flip=False, rot=0):
    return f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot}) scale({-s if flip else s} {s})">{inner}</g>'


def fonts_head(root):
    return animlib.local_fonts(root, FONT_SPECS)


def frame_svg(inner, label=''):
    """Full-frame SVG for one shot (no grain, no vignette: the look is clean flat vector)."""
    return (f'<svg width="{W()}" height="{H()}" viewBox="0 0 {W()} {H()}" role="img" aria-label="{esc(label)}" '
            f'style="position:absolute;left:0;top:0;width:{W()}px;height:{H()}px">{inner}</svg>')


# ------------------------------------------------------------------ text primitives
def text(x, y, t, size, fam=SCRIPT, fill=INK, anchor='middle', stroke=None, sw=0, rot=0, skew=0, extra='', lh=1.08, kf=None):
    """Multi-line text ('\n'). stroke draws an outline behind the fill (paint-order)."""
    lines = str(t).split('\n')
    st = f'{fam};font-size:{size}px;fill:{fill}' + (f';stroke:{stroke};stroke-width:{sw}px;paint-order:stroke;stroke-linejoin:round' if stroke else '') + extra
    tf = (f' transform="translate({x} {y}) rotate({rot}) skewX({skew}) translate({-x} {-y})"') if (rot or skew) else ''
    y0 = y - (len(lines) - 1) * size * lh / 2
    spans = ''.join(f'<tspan x="{x}" y="{y0 + i * size * lh:.1f}">{esc(l)}</tspan>' for i, l in enumerate(lines))
    k = f" data-kf='{animlib.J(kf)}'" if kf else ''
    return f'<text text-anchor="{anchor}" dominant-baseline="middle" style="{st}"{tf}{k}>{spans}</text>'


def wtext(x, y, t, size, anchor='middle', kf=None, fam=None):
    """White handwriting with a thin dark outline and a soft offset shadow (dialogue, captions, labels)."""
    fam = fam or SCRIPT
    sh = text(x + size * .05, y + size * .07, t, size, fam, '#000000', anchor, stroke='#000000', sw=size * .1, extra=';opacity:.45', kf=kf)
    return sh + text(x, y, t, size, fam, '#FFFFFF', anchor, stroke='#151515', sw=size * .085, kf=kf)


def tw(t, size, fam='script'):
    """Rough text width (px) for layout of bubbles and tags."""
    k = .40 if fam == 'script' else .52
    return max(len(l) for l in str(t).split('\n')) * size * k


def caps(x, y, t, size, fill=INK, anchor='middle', rot=0, **kw):
    return text(x, y, t, size, CAPS, fill, anchor, rot=rot, skew=-7, **kw)


# ------------------------------------------------------------------ characters
def _shade_clip(shape, shade_shape, base, shade):
    cid = uid('c')
    return (f'<clipPath id="{cid}">{shape}</clipPath>{shape.replace("/>", f" fill=\"{base}\"/>", 1)}'
            f'<g clip-path="url(#{cid})">{shade_shape.replace("/>", f" fill=\"{shade}\"/>", 1)}</g>'
            f'{shape.replace("/>", f" fill=\"none\" stroke=\"{INK}\" stroke-width=\"{LW}\"/>", 1)}')


BODY = 'M-27 -150 Q0 -157 27 -150 Q45 -141 44 -102 Q43 -62 30 -56 Q0 -50 -30 -56 Q-43 -62 -44 -102 Q-45 -141 -27 -150 Z'
HEAD_C, HEAD_R = -196, 44


def _arms(pose, fill):
    """Thin black arms; pose name or ((hx,hy),(hx,hy)) hand points relative to the feet."""
    P = {'down': ((-54, -76), (54, -76)), 'hips': ((-58, -98), (58, -98)), 'point_r': ((-44, -80), (104, -142)),
         'point_l': ((-104, -142), (44, -80)), 'up': ((-62, -232), (62, -232)), 'wave': ((-44, -80), (70, -228)),
         'hold': ((-22, -104), (22, -104)), 'shrug': ((-74, -150), (74, -150)), 'phone': ((-54, -76), (34, -136)),
         'chin': ((-44, -80), (14, -166)), 'present': ((-44, -80), (96, -112)), 'cross': ((22, -110), (-22, -106))}
    hands = P.get(pose, pose) if isinstance(pose, str) else pose
    o = []
    for (hx, hy), sx in zip(hands, (-34, 34)):
        mx, my = (sx + hx) / 2 + (-10 if sx < 0 else 10), (-136 + hy) / 2 + 8
        o.append(f'<path d="M{sx} -136 Q{mx:.0f} {my:.0f} {hx} {hy}" fill="none" stroke="{INK}" stroke-width="{LW - .6}" stroke-linecap="round"/>')
    return ''.join(o)


def _legs(stance):
    if stance == 'walk':
        return (f'<path d="M-8 -60 L14 0 M8 -60 L-14 0" stroke="{INK}" stroke-width="{LW - .4}" stroke-linecap="round"/>')
    if stance == 'sit':
        return (f'<path d="M-12 -60 L-12 -40 L-30 -40 M12 -60 L12 -40 L-6 -40" fill="none" stroke="{INK}" stroke-width="{LW - .4}" stroke-linecap="round"/>')
    if stance == 'none':
        return ''
    return f'<path d="M-11 -60 L-12 0 M11 -60 L12 0" stroke="{INK}" stroke-width="{LW - .4}" stroke-linecap="round"/>'


def _hair(style, col, face):
    cy, r = HEAD_C, HEAD_R
    s = f'fill="{col}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"'
    if style == 'side':      # neat side part / short
        return (f'<path d="M-45 {cy + 6} C-50 {cy - 40} -26 {cy - 58} 2 {cy - 56} C30 {cy - 56} 50 {cy - 38} 45 {cy + 4} '
                f'C40 {cy - 18} 30 {cy - 26} 14 {cy - 28} C2 {cy - 18} -20 {cy - 22} -34 {cy - 26} C-40 {cy - 18} -42 {cy - 6} -45 {cy + 6} Z" {s}/>')
    if style == 'swoop':     # fringe swept to one side (young / modern)
        return (f'<path d="M-46 {cy + 8} C-52 {cy - 44} -10 {cy - 64} 22 {cy - 52} C44 {cy - 44} 52 {cy - 20} 45 {cy + 6} '
                f'C38 {cy - 14} 24 {cy - 18} 18 {cy - 34} C4 {cy - 12} -24 {cy - 10} -40 {cy - 14} Z" {s}/>')
    if style == 'curly':
        bumps = ''.join(f'<circle cx="{r * .92 * math.cos(a):.1f}" cy="{cy - 6 + r * .9 * math.sin(a):.1f}" r="15" {s}/>'
                        for a in [math.pi * (1.0 + i / 8) for i in range(9)])
        return bumps + f'<path d="M-42 {cy - 4} C-36 {cy - 40} 36 {cy - 40} 42 {cy - 4} C24 {cy - 20} -24 {cy - 20} -42 {cy - 4} Z" fill="{col}"/>'
    if style == 'bald':      # bald top, tufts on the sides (older men)
        return (f'<path d="M-46 {cy + 10} C-52 {cy - 6} -48 {cy - 24} -38 {cy - 30} C-40 {cy - 14} -40 {cy - 2} -34 {cy + 12} Z" {s}/>'
                f'<path d="M46 {cy + 10} C52 {cy - 6} 48 {cy - 24} 38 {cy - 30} C40 {cy - 14} 40 {cy - 2} 34 {cy + 12} Z" {s}/>')
    if style == 'long':
        return (f'<path d="M-48 {cy + 44} C-56 {cy - 30} -30 {cy - 60} 0 {cy - 58} C30 {cy - 60} 56 {cy - 30} 48 {cy + 44} '
                f'L34 {cy + 44} C38 {cy + 10} 36 {cy - 14} 28 {cy - 26} C10 {cy - 20} -16 {cy - 24} -30 {cy - 20} C-38 {cy - 6} -38 {cy + 14} -34 {cy + 44} Z" {s}/>')
    if style == 'bun':
        return (f'<circle cx="0" cy="{cy - 54}" r="17" {s}/>' + _hair('side', col, face))
    if style == 'spiky':
        return (f'<path d="M-45 {cy + 2} L-50 {cy - 30} L-34 {cy - 34} L-30 {cy - 58} L-12 {cy - 44} L0 {cy - 66} L12 {cy - 46} L30 {cy - 60} '
                f'L32 {cy - 36} L50 {cy - 30} L45 {cy + 2} C30 {cy - 22} -30 {cy - 22} -45 {cy + 2} Z" {s}/>')
    if style == 'buzz':
        return f'<path d="M-44 {cy - 4} C-42 {cy - 50} 42 {cy - 50} 44 {cy - 4} C28 {cy - 24} -28 {cy - 24} -44 {cy - 4} Z" {s}/>'
    return ''


def _hat(kind, col):
    cy = HEAD_C
    s = f'stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"'
    if kind == 'top':
        return (f'<rect x="-30" y="{cy - 112}" width="60" height="78" rx="5" fill="{col}" {s}/>'
                f'<rect x="-30" y="{cy - 50}" width="60" height="12" fill="{SUIT["black"][1]}" opacity=".8"/>'
                f'<ellipse cx="0" cy="{cy - 34}" rx="54" ry="11" fill="{col}" {s}/>')
    if kind == 'fedora':
        return (f'<path d="M-34 {cy - 34} C-36 {cy - 70} -20 {cy - 76} 0 {cy - 66} C20 {cy - 76} 36 {cy - 70} 34 {cy - 34} Z" fill="{col}" {s}/>'
                f'<rect x="-34" y="{cy - 46}" width="68" height="10" fill="{INK}" opacity=".55"/>'
                f'<ellipse cx="0" cy="{cy - 34}" rx="60" ry="12" fill="{col}" {s}/>')
    if kind == 'bowler':
        return (f'<path d="M-36 {cy - 32} C-36 {cy - 84} 36 {cy - 84} 36 {cy - 32} Z" fill="{col}" {s}/>'
                f'<ellipse cx="0" cy="{cy - 32}" rx="52" ry="10" fill="{col}" {s}/>')
    if kind == 'hard':
        return (f'<path d="M-42 {cy - 22} C-42 {cy - 76} 42 {cy - 76} 42 {cy - 22} Z" fill="{col}" {s}/>'
                f'<rect x="-52" y="{cy - 26}" width="104" height="10" rx="5" fill="{col}" {s}/>')
    if kind == 'grad':
        return (f'<rect x="-30" y="{cy - 50}" width="60" height="18" fill="{col}" {s}/>'
                f'<path d="M-64 {cy - 52} L0 {cy - 74} L64 {cy - 52} L0 {cy - 34} Z" fill="{col}" {s}/>'
                f'<path d="M30 {cy - 50} L42 {cy - 20}" stroke="{GOLD}" stroke-width="4"/>')
    if kind == 'cap':
        return (f'<path d="M-44 {cy - 18} C-46 {cy - 70} 44 {cy - 70} 44 {cy - 18} Z" fill="{col}" {s}/>'
                f'<path d="M30 {cy - 22} L76 {cy - 16} L44 {cy - 8} Z" fill="{col}" {s}/>')
    return ''


def face(expr='neutral', look=0, eye_y=HEAD_C - 2, mouth_open=False, nose=None, glasses=False, moustache=None, beard=None, skin=None):
    """Dot eyes, short brows only for emotion, one-stroke mouth. look = eye offset in px (-6..6)."""
    o, ey, lx, rx = [], eye_y, -14 + look, 14 + look
    ln = f'stroke="{INK}" stroke-width="3.2" stroke-linecap="round" fill="none"'
    if expr in ('closed', 'smug_closed'):
        o.append(f'<path d="M{lx - 6} {ey} Q{lx} {ey + 4} {lx + 6} {ey} M{rx - 6} {ey} Q{rx} {ey + 4} {rx + 6} {ey}" {ln}/>')
    elif expr == 'shocked':
        o.append(f'<ellipse cx="{lx}" cy="{ey}" rx="5.5" ry="7.5" fill="{INK}"/><ellipse cx="{rx}" cy="{ey}" rx="5.5" ry="7.5" fill="{INK}"/>')
    elif expr == 'crying':
        o.append(f'<path d="M{lx - 7} {ey + 2} L{lx + 6} {ey - 2} M{rx + 7} {ey + 2} L{rx - 6} {ey - 2}" {ln}/>')
    else:
        o.append(f'<ellipse cx="{lx}" cy="{ey}" rx="3.8" ry="5.4" fill="{INK}"/><ellipse cx="{rx}" cy="{ey}" rx="3.8" ry="5.4" fill="{INK}"/>')
    brow = {'angry': f'M{lx - 9} {ey - 15} L{lx + 6} {ey - 9} M{rx + 9} {ey - 15} L{rx - 6} {ey - 9}',
            'worried': f'M{lx - 8} {ey - 9} L{lx + 6} {ey - 15} M{rx + 8} {ey - 9} L{rx - 6} {ey - 15}',
            'sad': f'M{lx - 8} {ey - 9} L{lx + 6} {ey - 14} M{rx + 8} {ey - 9} L{rx - 6} {ey - 14}',
            'surprised': f'M{lx - 7} {ey - 16} Q{lx} {ey - 20} {lx + 7} {ey - 16} M{rx - 7} {ey - 16} Q{rx} {ey - 20} {rx + 7} {ey - 16}',
            'shocked': f'M{lx - 8} {ey - 19} Q{lx} {ey - 24} {lx + 8} {ey - 19} M{rx - 8} {ey - 19} Q{rx} {ey - 24} {rx + 8} {ey - 19}',
            'smug': f'M{lx - 8} {ey - 11} L{lx + 6} {ey - 11} M{rx - 6} {ey - 16} L{rx + 8} {ey - 12}',
            'determined': f'M{lx - 9} {ey - 13} L{lx + 6} {ey - 10} M{rx + 9} {ey - 13} L{rx - 6} {ey - 10}',
            'crying': f'M{lx - 8} {ey - 10} L{lx + 6} {ey - 15} M{rx + 8} {ey - 10} L{rx - 6} {ey - 15}'}.get(expr)
    if brow: o.append(f'<path d="{brow}" {ln}/>')
    my, mx = HEAD_C + 22, look * .6
    if nose == 'big':
        o.append(f'<ellipse cx="{mx}" cy="{HEAD_C + 8}" rx="11" ry="9" fill="#9C5866" stroke="{INK}" stroke-width="2.6"/>')
        my += 6
    elif nose == 'small':
        o.append(f'<path d="M{mx - 2} {HEAD_C + 4} Q{mx + 5} {HEAD_C + 10} {mx - 2} {HEAD_C + 13}" {ln}/>')
    if mouth_open or expr in ('surprised', 'talk'):
        o.append(f'<ellipse cx="{mx}" cy="{my + 1}" rx="5.5" ry="6.5" fill="{INK}"/>')
    elif expr == 'shocked':
        o.append(f'<ellipse cx="{mx}" cy="{my + 4}" rx="9" ry="12" fill="{INK}"/>')
    elif expr == 'crying':
        o.append(f'<path d="M{mx - 14} {my + 6} Q{mx} {my - 10} {mx + 14} {my + 6} Q{mx} {my + 14} {mx - 14} {my + 6} Z" fill="{INK}"/>'
                 f'<path d="M{lx} {ey + 6} L{lx - 3} {ey + 40} M{rx} {ey + 6} L{rx + 3} {ey + 40}" stroke="#8FD0F0" stroke-width="5" stroke-linecap="round"/>')
    elif expr in ('happy', 'grin'):
        o.append(f'<path d="M{mx - 12} {my - 3} Q{mx} {my + 13} {mx + 12} {my - 3} Z" fill="{INK}"/>' if expr == 'grin'
                 else f'<path d="M{mx - 10} {my - 2} Q{mx} {my + 9} {mx + 10} {my - 2}" {ln}/>')
    elif expr in ('sad', 'worried', 'angry'):
        o.append(f'<path d="M{mx - 8} {my + 4} Q{mx} {my - 3} {mx + 8} {my + 4}" {ln}/>')
    elif expr in ('smug', 'smug_closed'):
        o.append(f'<path d="M{mx - 8} {my + 1} Q{mx + 3} {my + 5} {mx + 10} {my - 4}" {ln}/>')
    else:
        o.append(f'<path d="M{mx - 6} {my + 1} L{mx + 6} {my + 1}" {ln}/>')
    if moustache:
        o.append(f'<path d="M{mx} {my - 6} C{mx - 6} {my - 12} {mx - 22} {my - 10} {mx - 24} {my + 2} C{mx - 14} {my - 2} {mx - 6} {my - 1} {mx} {my - 4} '
                 f'C{mx + 6} {my - 1} {mx + 14} {my - 2} {mx + 24} {my + 2} C{mx + 22} {my - 10} {mx + 6} {my - 12} {mx} {my - 6} Z" fill="{moustache}" stroke="{INK}" stroke-width="2.4"/>')
    if beard:
        o.append(f'<path d="M-42 {HEAD_C + 4} C-40 {HEAD_C + 40} -18 {HEAD_C + 50} 0 {HEAD_C + 50} C18 {HEAD_C + 50} 40 {HEAD_C + 40} 42 {HEAD_C + 4} '
                 f'C34 {HEAD_C + 18} 22 {HEAD_C + 14} 14 {HEAD_C + 22} C6 {HEAD_C + 16} -6 {HEAD_C + 16} -14 {HEAD_C + 22} C-22 {HEAD_C + 14} -34 {HEAD_C + 18} -42 {HEAD_C + 4} Z" '
                 f'fill="{beard}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    if glasses:
        o.append(f'<circle cx="{lx}" cy="{ey}" r="11" fill="rgba(255,255,255,.18)" stroke="{INK}" stroke-width="3"/>'
                 f'<circle cx="{rx}" cy="{ey}" r="11" fill="rgba(255,255,255,.18)" stroke="{INK}" stroke-width="3"/><path d="M{lx + 11} {ey} H{rx - 11}" {ln}/>')
    return ''.join(o)


def person(x, y, s=1, skin='peach', suit='black', shirt='#F7F7F5', tie=RED, hair='side', hair_col='black', hat=None, hat_col=None,
           expr='neutral', look=0, arms='down', stance='stand', glasses=False, moustache=None, beard=None, nose=None, flip=False,
           lapels=True, talk=None, extras='', body=None, back=False, walk=None):
    """The cast. (x, y) = feet on the ground; unscaled height ~250 px (head r=44 is ~35% of it).
    skin: SKIN key; suit: SUIT key (or (base, shade)); hair: side|swoop|curly|bald|long|bun|spiky|buzz|none.
    talk=(t0, t1): mouth flaps between closed and open while the voiced line plays.
    back=True: seen from behind (over-the-shoulder foregrounds): no face, hair covers the head, no lapels.
    walk=(t0, t1): legs scissor while walking (move the figure with G(..., slide/tx keys) at the same time)."""
    sk, sk_sh = SKIN[skin] if isinstance(skin, str) else skin
    su, su_sh = SUIT[suit] if isinstance(suit, str) else suit
    hc = HAIR.get(hair_col, hair_col)
    o = [f'<ellipse cx="0" cy="2" rx="46" ry="9" fill="#000" opacity=".16"/>']
    if walk:
        o.append(animlib.G(_legs('walk'), animlib.flicker(walk[0], walk[1], .5)) + animlib.G(_legs('stand'), animlib.flicker(walk[0], walk[1], .5, on_first=False)))
    else:
        o.append(_legs(stance))
    body_path = body or BODY
    o.append(_shade_clip(f'<path d="{body_path}"/>', '<ellipse cx="52" cy="-100" rx="34" ry="70"/>', su, su_sh))
    if back:
        o.append(_arms(arms, su))
        o.append(_shade_clip(f'<circle cx="0" cy="{HEAD_C}" r="{HEAD_R}"/>', f'<ellipse cx="{HEAD_R * .95:.0f}" cy="{HEAD_C + 6}" rx="{HEAD_R * .62:.0f}" ry="{HEAD_R * 1.25:.0f}"/>', sk, sk_sh))
        if hair not in ('none', None, 'bald'):
            o.append(f'<path d="M-45 {HEAD_C + 14} C-50 {HEAD_C - 40} -26 {HEAD_C - 56} 0 {HEAD_C - 56} C26 {HEAD_C - 56} 50 {HEAD_C - 40} 45 {HEAD_C + 14} C30 {HEAD_C + 26} -30 {HEAD_C + 26} -45 {HEAD_C + 14} Z" '
                     f'fill="{hc}" stroke="{INK}" stroke-width="{LW}"/>')
        elif hair == 'bald':
            o.append(_hair('bald', hc, None))
        if hat: o.append(_hat(hat, hat_col or SUIT['black'][0]))
        return g(x, y, s, ''.join(o), flip)
    if lapels:
        o.append(f'<path d="M-13 -151 L0 -116 L13 -151 Z" fill="{shirt}" stroke="{INK}" stroke-width="{LW3}" stroke-linejoin="round"/>')
        if tie: o.append(f'<path d="M-4 -148 L4 -148 L6 -126 L0 -116 L-6 -126 Z" fill="{tie}" stroke="{INK}" stroke-width="2"/>')
        o.append(f'<path d="M-16 -151 L-2 -110 M16 -151 L2 -110" stroke="{INK}" stroke-width="{LW3}" fill="none"/>')
    o.append(_arms(arms, su))
    head = f'<circle cx="0" cy="{HEAD_C}" r="{HEAD_R}"/>'
    if hair == 'long': o.append(_hair('long', hc, None))
    o.append(_shade_clip(head, f'<ellipse cx="{HEAD_R * .95:.0f}" cy="{HEAD_C + 6}" rx="{HEAD_R * .62:.0f}" ry="{HEAD_R * 1.25:.0f}"/>', sk, sk_sh))
    if hair not in ('long', 'none', None): o.append(_hair(hair, hc, None))
    elif hair == 'long':
        o.append(f'<path d="M-34 {HEAD_C - 18} C-16 {HEAD_C - 26} 10 {HEAD_C - 22} 30 {HEAD_C - 28} C26 {HEAD_C - 50} -26 {HEAD_C - 52} -34 {HEAD_C - 18} Z" fill="{hc}"/>')
    mc = HAIR.get(moustache, moustache) if moustache else None
    bc = HAIR.get(beard, beard) if beard else None
    if talk:
        t0, t1 = talk
        o.append(face(expr, look, nose=nose, glasses=glasses, moustache=mc, beard=bc))
        o.append(animlib.G(f'<circle cx="{look * .6}" cy="{HEAD_C + 23 + (6 if nose == "big" else 0)}" r="9" fill="{sk}"/>'
                           f'<ellipse cx="{look * .6}" cy="{HEAD_C + 23 + (6 if nose == "big" else 0)}" rx="6" ry="7" fill="{INK}"/>', animlib.flicker(t0, t1)))
    else:
        o.append(face(expr, look, nose=nose, glasses=glasses, moustache=mc, beard=bc))
    if hat: o.append(_hat(hat, hat_col or SUIT['black'][0]))
    if arms == 'phone':   # handset + hand in front of the head
        o.append(f'<path d="M34 -136 Q62 -150 50 -170" fill="none" stroke="{INK}" stroke-width="{LW - .6}" stroke-linecap="round"/>'
                 f'<path d="M30 -228 C52 -230 58 -206 54 -176 C52 -162 40 -156 30 -160 L34 -172 C42 -174 44 -190 42 -206 C40 -214 32 -216 26 -214 Z" fill="#2B2B2E" stroke="{INK}" stroke-width="3"/>'
                 f'<circle cx="50" cy="-172" r="8" fill="{sk}" stroke="{INK}" stroke-width="2.6"/>')
    o.append(extras)
    return g(x, y, s, ''.join(o), flip)


def extra(x, y, s=1, tone='white', suit='black', hat=None, expr='neutral', flip=False, **kw):
    """Background people: white faces (named minor characters) or grey (anonymous)."""
    return person(x, y, s, skin=tone, suit=suit, hat=hat, expr=expr, flip=flip, hair=kw.pop('hair', 'none'), **kw)


def crowd(x0, x1, y, rows=3, s=1.0, seed=1, tones=('#8B8B8B', '#9C9C9C', '#777777', '#A8A8A8'), hats=.2):
    """Grey silhouette crowd (the anonymous public): overlapping heads + bodies, back rows smaller."""
    rnd = random.Random(seed)
    o = []
    for r in range(rows):
        sc = s * (0.78 + 0.11 * r)
        yy = y - (rows - 1 - r) * 34 * s
        n = int((x1 - x0) / (78 * sc)) + 1
        for i in range(n):
            cx = x0 + i * 78 * sc + rnd.uniform(-14, 14) * sc
            c = rnd.choice(tones)
            hat = ''
            if rnd.random() < hats:
                hat = f'<rect x="-22" y="-122" width="44" height="34" rx="4" fill="#5E5E5E" stroke="{INK}" stroke-width="3"/><ellipse cx="0" cy="-88" rx="38" ry="8" fill="#5E5E5E" stroke="{INK}" stroke-width="3"/>'
            o.append(g(cx, yy, sc, f'<path d="M-40 40 Q-42 -30 0 -32 Q42 -30 40 40 Z" fill="{c}" stroke="{INK}" stroke-width="3.4"/>'
                                   f'<circle cx="0" cy="-62" r="32" fill="{c}" stroke="{INK}" stroke-width="3.4"/>{hat}'))
    return ''.join(o)


def robot(x, y, s=1, body='#8C9199', emblem='#E06B3C', mark='✱', eyes='#47E2F0', expr='neutral', arms='down', name=None, flip=False):
    """A personified AI model / product: visor head with glowing eyes, chest emblem, stick limbs."""
    sh = '#6F747B'
    o = [f'<ellipse cx="0" cy="2" rx="46" ry="9" fill="#000" opacity=".16"/>', _legs('stand'), _arms(arms, body)]
    o.append(_shade_clip('<rect x="-44" y="-150" width="88" height="96" rx="26"/>', '<ellipse cx="54" cy="-100" rx="30" ry="70"/>', body, sh))
    o.append(f'<circle cx="0" cy="-104" r="17" fill="#3A3E45" stroke="{INK}" stroke-width="3"/>'
             + text(0, -103, mark, 26, "font-family:'DejaVu Sans',sans-serif;font-weight:700", emblem))
    o.append(_shade_clip('<rect x="-50" y="-246" width="100" height="88" rx="38"/>', '<ellipse cx="58" cy="-200" rx="32" ry="60"/>', body, sh))
    o.append(f'<rect x="-36" y="-226" width="72" height="42" rx="20" fill="#2B2F35" stroke="{INK}" stroke-width="3"/>')
    eh = 4 if expr == 'closed' else 9
    o.append(f'<rect x="-22" y="{-207 - eh / 2}" width="13" height="{eh}" rx="4" fill="{eyes}"/><rect x="9" y="{-207 - eh / 2}" width="13" height="{eh}" rx="4" fill="{eyes}"/>')
    if expr == 'angry':
        o.append(f'<path d="M-24 -218 L-8 -212 M24 -218 L8 -212" stroke="{eyes}" stroke-width="3"/>')
    o.append(f'<path d="M0 -246 V-262" stroke="{INK}" stroke-width="3.4"/><circle cx="0" cy="-266" r="6" fill="{emblem}" stroke="{INK}" stroke-width="2.4"/>')
    if name:
        o.append(f'<rect x="-30" y="-78" width="60" height="18" rx="3" fill="#F4F1E8" stroke="{INK}" stroke-width="2"/>' + caps(0, -69, name, 14))
    return g(x, y, s, ''.join(o), flip)


def mascot(x, y, s=1, expr='grin', arms='present', flip=False, talk=None, **kw):
    """The channel host who breaks the fourth wall (asides, sponsor reads). Re-style it to the creator; keep it constant."""
    d = dict(skin='peach', suit='brown', shirt='#F7F7F5', tie='#C0392F', hair='swoop', hair_col='dark', glasses=True)
    d.update(kw)
    return person(x, y, s, expr=expr, arms=arms, flip=flip, talk=talk, **d)


# ------------------------------------------------------------------ dialogue devices
def say(x, y, t, size=34, to=None, anchor='middle', kf=None):
    """VOICED line (the character speaks it in the VO): white handwriting with a dark outline, plus a short
    white tick pointing at the speaker's mouth (to=(x, y)). No box."""
    if anchor == 'middle':   # keep the line inside the frame
        hw = tw(t, size) / 2 + 24
        x = max(hw, min(W() - hw, x))
    o = wtext(x, y, t, size, anchor)
    if to:
        n = len(str(t).split('\n'))
        bx = x if anchor == 'middle' else (x + 20 if anchor == 'start' else x - 20)
        by = y + (n * size * 1.08) / 2 + 4 if to[1] > y else y - (n * size * 1.08) / 2 - 4
        dx, dy = to[0] - bx, to[1] - by
        L = math.hypot(dx, dy) or 1
        x0, y0 = bx + dx / L * 6, by + dy / L * 6
        x1, y1 = bx + dx / L * 24, by + dy / L * 24
        o += (f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" stroke="#1A1A1A" stroke-width="8" stroke-linecap="round"/>'
              f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" stroke="#FFFFFF" stroke-width="3.6" stroke-linecap="round"/>')
    return animlib.G(o, kf) if kf else o


def bubble(x, y, t, tail=None, size=28, w=None, kf=None, fill='#FFFFFF', shout=False):
    """UNVOICED gag line in a white box (the narrator keeps talking while we read it). Pops in."""
    lines = str(t).split('\n')
    bw = w or tw(t, size) + size * 1.3
    bh = len(lines) * size * 1.08 + size * .9
    o = ''
    if tail:
        tx, ty = tail
        bx0 = max(x - bw / 2 + 18, min(x + bw / 2 - 40, tx - 12))
        by = y + bh / 2 - 2 if ty > y else y - bh / 2 + 2
        o += f'<path d="M{bx0:.0f} {by:.0f} L{tx:.0f} {ty:.0f} L{bx0 + 24:.0f} {by:.0f} Z" fill="{fill}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    if shout:
        pts = []
        for i in range(28):
            a = 2 * math.pi * i / 28
            rr = 1.0 if i % 2 == 0 else 0.86
            pts.append(f'{x + bw / 2 * 1.12 * rr * math.cos(a):.0f},{y + bh / 2 * 1.25 * rr * math.sin(a):.0f}')
        o += f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    else:
        o += f'<rect x="{x - bw / 2:.0f}" y="{y - bh / 2:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="{size * .5:.0f}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
        if tail:  # hide the tail's base line inside the box
            tx, ty = tail
            bx0 = max(x - bw / 2 + 18, min(x + bw / 2 - 40, tx - 12))
            by = y + bh / 2 if ty > y else y - bh / 2
            o += f'<path d="M{bx0 + 2:.0f} {by:.0f} H{bx0 + 22:.0f}" stroke="{fill}" stroke-width="5"/>'
    o += text(x, y + 1, t, size, SCRIPT, INK)
    return animlib.G(o, kf if kf is not None else animlib.pop(0.0), (x, y))


def thought(cx, cy, w, h, inner='', trail=None, kf=None, t=None, size=28):
    """Thought cloud with scalloped edge; inner = SVG drawn inside (icons, a mini scene) or text t."""
    n = 14
    circ = []
    for i in range(n):
        a = 2 * math.pi * i / n
        circ.append((cx + w / 2 * .82 * math.cos(a), cy + h / 2 * .78 * math.sin(a), min(w, h) * .2))
    edge = ''.join(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r:.0f}" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>' for px, py, r in circ)
    fillc = ''.join(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r - 2.5:.0f}" fill="#FFFFFF"/>' for px, py, r in circ)
    core = f'<ellipse cx="{cx}" cy="{cy}" rx="{w * .42:.0f}" ry="{h * .4:.0f}" fill="#FFFFFF"/>'
    tr = ''
    if trail:
        tx, ty = trail
        for k, rr in ((.55, 11), (.8, 7)):
            px, py = cx + (tx - cx) * k, cy + h * .45 + (ty - cy - h * .45) * k
            tr += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rr}" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
    body = tr + edge + fillc + core + inner + (text(cx, cy, t, size, SCRIPT, INK) if t else '')
    return animlib.G(body, kf if kf is not None else animlib.pop(0.0, .3), (cx, cy))


def label_arrow(x, y, t, to, size=30, kf=None, curve=40):
    """Name/label in white handwriting with a curved arrow to the target (types on with animlib.type_cps)."""
    tx, ty = to
    sx, sy = x + (-10 if tx < x else 10), y + (size * .6 if ty > y else -size * .6)
    mx, my = (sx + tx) / 2 + (curve if tx < x else -curve), (sy + ty) / 2
    ang = math.atan2(ty - my, tx - mx)
    a1, a2 = ang + 2.6, ang - 2.6
    head = f'M{tx + 16 * math.cos(a1):.0f} {ty + 16 * math.sin(a1):.0f} L{tx} {ty} L{tx + 16 * math.cos(a2):.0f} {ty + 16 * math.sin(a2):.0f}'
    arr = f'M{sx:.0f} {sy:.0f} Q{mx:.0f} {my:.0f} {tx} {ty} {head}'
    o = (f'<path d="{arr}" fill="none" stroke="#1A1A1A" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{arr}" fill="none" stroke="#FFFFFF" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>')
    tx_kf = kf or None
    return o + wtext(x, y, t, size, 'middle', kf=tx_kf)


def place_caption(t, size=36, corner='bl', kf=None):
    """'Connecticut, 1837.' - white handwriting, bottom-left (or top-right), typed on. In 9:16 it sits above the Reels UI."""
    x, anc = (36, 'start') if corner in ('bl', 'tl') else (W() - 36, 'end')
    bottom = H() - 44 if W() > H() else H() * .74
    y = bottom if corner in ('bl', 'br') else (48 if W() > H() else H() * .12)
    return wtext(x, y, t, size, anc, kf=kf)


# ------------------------------------------------------------------ card shots (full frame)
def card(t, size=40, y=None, x=None, anchor='middle', kf=None):
    """Narration / chapter text on pure black. Give kf=animlib.type_cps(...) to type it on, or nothing for a hard cut."""
    return frame_svg(f'<rect width="{W()}" height="{H()}" fill="#000"/>' +
                     text(x if x is not None else W() / 2, y if y is not None else H() / 2, t, size, SCRIPT, '#FFFFFF', anchor, kf=kf), t)


def chapter(title, size=None):
    return card(title, size or (52 if W() > H() else 58))


def end_card(word='Subscribe'):
    return frame_svg(f'<rect width="{W()}" height="{H()}" fill="#000"/>' + text(W() / 2, H() / 2, word, 96 if W() > H() else 110, SCRIPT_B, '#FFFFFF'), word)


# ------------------------------------------------------------------ settings
def fill_bg(col): return f'<rect x="-200" y="-200" width="{W() + 400}" height="{H() + 400}" fill="{col}"/>'


def room(wall=CREAM_WALL, floor=WOOD, horizon=None, wainscot=None):
    """Interior: wall + floor (+ optional wood panelling below `wainscot` y)."""
    hz = horizon if horizon is not None else H() * .72
    o = [fill_bg(wall), f'<rect x="-200" y="{hz}" width="{W() + 400}" height="{H() - hz + 200}" fill="{floor}"/>',
         f'<path d="M-200 {hz} H{W() + 200}" stroke="{INK}" stroke-width="{LW2}"/>']
    if wainscot:
        o.append(f'<rect x="-200" y="{wainscot}" width="{W() + 400}" height="{hz - wainscot}" fill="{PANEL}" stroke="{INK}" stroke-width="{LW2}"/>')
        for xx in range(-160, W() + 200, 150):
            o.append(f'<rect x="{xx + 14}" y="{wainscot + 14}" width="122" height="{hz - wainscot - 28}" fill="none" stroke="#3E2719" stroke-width="2.4"/>')
    return ''.join(o)


def window(x, y, w, h, view='city', frame='#F4F1EA'):
    sky = {'city': '#AFC6D6', 'night': '#1F2B44', 'sky': '#A9D3EA', 'dusk': '#E9A47E'}.get(view, view)
    cid = uid('w')
    o = [f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#{cid})">', f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{sky}"/>']
    if view in ('city', 'night', 'dusk'):
        rnd = random.Random(int(x + y))
        bx = x
        while bx < x + w:
            bw, bh = rnd.uniform(.12, .22) * w, rnd.uniform(.25, .6) * h
            col = '#8CA5B8' if view == 'city' else ('#2E3C5A' if view == 'night' else '#B57A63')
            o.append(f'<rect x="{bx:.0f}" y="{y + h - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{col}"/>')
            for wy in range(int(y + h - bh + 10), int(y + h - 8), 18):
                for wx in range(int(bx + 6), int(bx + bw - 8), 14):
                    lit = '#F2D98B' if view == 'night' and rnd.random() < .4 else ('#C9D7E2' if view == 'city' else '#3A4867')
                    o.append(f'<rect x="{wx}" y="{wy}" width="6" height="8" fill="{lit}"/>')
            bx += bw + 4
    o.append(f'<path d="M{x + w * .15} {y + h} L{x + w * .55} {y} M{x + w * .3} {y + h} L{x + w * .7} {y}" stroke="#FFFFFF" stroke-width="10" opacity=".25"/></g>')
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{frame}" stroke-width="12"/>'
             f'<path d="M{x + w / 2} {y} V{y + h} M{x} {y + h / 2} H{x + w}" stroke="{frame}" stroke-width="8"/>'
             f'<rect x="{x - 6}" y="{y - 6}" width="{w + 12}" height="{h + 12}" fill="none" stroke="{INK}" stroke-width="{LW2}"/>'
             f'<rect x="{x + 6}" y="{y + 6}" width="{w - 12}" height="{h - 12}" fill="none" stroke="{INK}" stroke-width="2"/>')
    return ''.join(o)


def bookshelf(x, y, w, h, seed=2):
    rnd = random.Random(seed)
    cols = ['#9C3B32', '#2F4A6B', '#C9A24A', '#4E6B45', '#6B4A7A', '#B86A3A', '#3C3C3C', '#7A8A99']
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WOOD_D}" stroke="{INK}" stroke-width="{LW2}"/>']
    nsh = max(2, int(h / 95))
    sh = (h - 16) / nsh
    for i in range(nsh):
        sy = y + 8 + i * sh
        bx = x + 10
        while bx < x + w - 18:
            bw = rnd.uniform(12, 22); bh = sh * rnd.uniform(.62, .86)
            o.append(f'<rect x="{bx:.0f}" y="{sy + sh - bh - 6:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{rnd.choice(cols)}" stroke="{INK}" stroke-width="2"/>')
            bx += bw + rnd.uniform(0, 3)
        o.append(f'<rect x="{x}" y="{sy + sh - 6:.0f}" width="{w}" height="8" fill="{WOOD}" stroke="{INK}" stroke-width="2"/>')
    return ''.join(o)


def curtain(x, y, w, h, col='#A8343A', side='r'):
    sh = '#86262C'
    tie_y = y + h * .62
    inner = x + (w * .25 if side == 'r' else w * .75)
    o = [f'<path d="M{x} {y} H{x + w} V{y + h} H{inner} Q{inner + (w * .2 if side == "r" else -w * .2):.0f} {tie_y} {x + w / 2} {y} Z" fill="{col}" stroke="{INK}" stroke-width="{LW2}"/>']
    for k in (.3, .5, .7):
        o.append(f'<path d="M{x + w * k:.0f} {y + 10} Q{x + w * k + 8:.0f} {y + h * .5:.0f} {x + w * k:.0f} {y + h - 10}" stroke="{sh}" stroke-width="7" fill="none"/>')
    o.append(f'<rect x="{x + w * .2:.0f}" y="{tie_y - 10:.0f}" width="{w * .7:.0f}" height="22" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="2.6"/>')
    return ''.join(o)


def portrait(x, y, w, h, inner=''):
    cid = uid('pc')
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#6B4A31" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<clipPath id="{cid}"><rect x="{x + 14}" y="{y + 14}" width="{w - 28}" height="{h - 28}"/></clipPath>'
            f'<rect x="{x + 14}" y="{y + 14}" width="{w - 28}" height="{h - 28}" fill="#CFC4AE" stroke="{INK}" stroke-width="2"/>'
            f'<g clip-path="url(#{cid})">{inner}<path d="M{x + w * .25} {y + h} L{x + w * .6} {y} M{x + w * .45} {y + h} L{x + w * .8} {y}" stroke="#FFF" stroke-width="12" opacity=".22"/></g>')


def door(x, y, w, h, col='#7A5236', knob=GOLD):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<rect x="{x + w * .14}" y="{y + h * .08}" width="{w * .72}" height="{h * .36}" fill="none" stroke="{INK}" stroke-width="2.4"/>'
            f'<rect x="{x + w * .14}" y="{y + h * .52}" width="{w * .72}" height="{h * .4}" fill="none" stroke="{INK}" stroke-width="2.4"/>'
            f'<circle cx="{x + w * .84}" cy="{y + h * .5}" r="6" fill="{knob}" stroke="{INK}" stroke-width="2"/>')


def desk(cx, y, w=420, h=110, top=WOOD_D, front=WOOD):
    """Desk seen from the front; y = top surface. Put characters BEFORE the desk so it hides their legs."""
    return (f'<rect x="{cx - w / 2}" y="{y + 16}" width="{w}" height="{h}" fill="{front}" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<rect x="{cx - w / 2 - 16}" y="{y}" width="{w + 32}" height="20" rx="4" fill="{top}" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<rect x="{cx - w / 2 + 24}" y="{y + 40}" width="{w * .3}" height="{h * .45}" fill="none" stroke="{INK}" stroke-width="2.2"/>'
            f'<rect x="{cx + w / 2 - 24 - w * .3}" y="{y + 40}" width="{w * .3}" height="{h * .45}" fill="none" stroke="{INK}" stroke-width="2.2"/>')


def chair_back(cx, y, col='#3A2A22', w=130, h=190):
    return (f'<rect x="{cx - w / 2}" y="{y - h}" width="{w}" height="{h}" rx="{w * .3}" fill="{col}" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<path d="M{cx - w * .3} {y - h * .8} V{y - h * .2} M{cx} {y - h * .85} V{y - h * .2} M{cx + w * .3} {y - h * .8} V{y - h * .2}" stroke="#2A1D17" stroke-width="3"/>')


def papers(x, y, n=4, w=80, rot=0):
    o = ''.join(f'<rect x="{x + i * 1.5 - w / 2:.0f}" y="{y - i * 6:.0f}" width="{w}" height="10" fill="#FBFBF7" stroke="{INK}" stroke-width="2"/>' for i in range(n))
    return f'<g transform="rotate({rot} {x} {y})">{o}</g>'


def laptop(cx, y, s=1, screen='#9FB9C8', back=False):
    if back:
        return g(cx, y, s, f'<path d="M-70 0 L-62 -92 L62 -92 L70 0 Z" fill="#A9ADB3" stroke="{INK}" stroke-width="{LW2}"/><circle cx="0" cy="-48" r="9" fill="#C9CCD0"/>')
    return g(cx, y, s, f'<rect x="-62" y="-96" width="124" height="84" rx="6" fill="#3B3E44" stroke="{INK}" stroke-width="{LW2}"/>'
                       f'<rect x="-54" y="-88" width="108" height="68" fill="{screen}"/>'
                       f'<path d="M-80 0 L-66 -12 H66 L80 0 Z" fill="#A9ADB3" stroke="{INK}" stroke-width="{LW2}"/>')


def monitor(cx, cy, w, h, inner='', bez='#2D3036'):
    """Screen whose inner SVG is drawn in screen coordinates (0,0)-(w,h) via translate."""
    cid = uid('m')
    return (f'<rect x="{cx - 14}" y="{cy + h / 2}" width="28" height="44" fill="#5A5E66" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<rect x="{cx - 60}" y="{cy + h / 2 + 40}" width="120" height="12" rx="5" fill="#5A5E66" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<rect x="{cx - w / 2 - 14}" y="{cy - h / 2 - 14}" width="{w + 28}" height="{h + 28}" rx="10" fill="{bez}" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<clipPath id="{cid}"><rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}"/></clipPath>'
            f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" fill="#F3F4F6"/>'
            f'<g clip-path="url(#{cid})"><g transform="translate({cx - w / 2} {cy - h / 2})">{inner}</g></g>')


def chat_ui(w, h, prompt='', reply_lines=3, accent='#E06B3C'):
    """Generic chatbot screen (no real product UI)."""
    o = [f'<rect width="{w}" height="{h}" fill="#F6F5F2"/>', f'<rect width="{w}" height="{h * .12:.0f}" fill="#E9E6DF"/>',
         f'<rect x="{w * .45:.0f}" y="{h * .2:.0f}" width="{w * .5:.0f}" height="{h * .14:.0f}" rx="12" fill="#DCE6F0" stroke="{INK}" stroke-width="1.6"/>',
         text(w * .7, h * .27, prompt, max(12, h * .065), SCRIPT, INK)]
    o.append(f'<circle cx="{w * .08:.0f}" cy="{h * .46:.0f}" r="{h * .035:.0f}" fill="{accent}"/>')
    for i in range(reply_lines):
        o.append(f'<rect x="{w * .14:.0f}" y="{h * (.43 + i * .08):.0f}" width="{w * (.7 - .12 * (i == reply_lines - 1)):.0f}" height="{h * .035:.0f}" rx="4" fill="#C9C6BF"/>')
    o.append(f'<rect x="{w * .08:.0f}" y="{h * .82:.0f}" width="{w * .84:.0f}" height="{h * .1:.0f}" rx="10" fill="#FFFFFF" stroke="{INK}" stroke-width="1.6"/>')
    return ''.join(o)


def phone_old(x, y, s=1):
    return g(x, y, s, f'<ellipse cx="0" cy="0" rx="34" ry="10" fill="#2B2B2E" stroke="{INK}" stroke-width="3"/>'
                      f'<rect x="-6" y="-110" width="12" height="108" fill="#2B2B2E" stroke="{INK}" stroke-width="3"/>'
                      f'<path d="M-22 -124 Q0 -140 22 -124 L14 -110 H-14 Z" fill="#2B2B2E" stroke="{INK}" stroke-width="3"/>'
                      f'<path d="M6 -70 Q40 -74 46 -40" fill="none" stroke="{INK}" stroke-width="3"/><rect x="38" y="-46" width="16" height="28" rx="6" fill="#2B2B2E" stroke="{INK}" stroke-width="3"/>')


def smartphone(cx, cy, w=150, h=290, inner='', rot=0):
    cid = uid('sp')
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="20" fill="#2A2C31" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<clipPath id="{cid}"><rect x="{cx - w / 2 + 10}" y="{cy - h / 2 + 24}" width="{w - 20}" height="{h - 48}" rx="6"/></clipPath>'
            f'<rect x="{cx - w / 2 + 10}" y="{cy - h / 2 + 24}" width="{w - 20}" height="{h - 48}" rx="6" fill="#F4F4F2"/>'
            f'<g clip-path="url(#{cid})"><g transform="translate({cx - w / 2 + 10} {cy - h / 2 + 24})">{inner}</g></g>'
            f'<circle cx="{cx}" cy="{cy + h / 2 - 12}" r="6" fill="#4A4D54"/></g>')


def plaque(cx, y, t, w=None, size=20, fill=GOLD):
    """Desk name plate ('BANK PRESIDENT', 'CEO')."""
    w = w or tw(t, size, 'caps') + 34
    return (f'<path d="M{cx - w / 2} {y} L{cx - w / 2 + 8} {y - size - 14} H{cx + w / 2 - 8} L{cx + w / 2} {y} Z" fill="{fill}" stroke="{INK}" stroke-width="2.8" stroke-linejoin="round"/>'
            + caps(cx, y - (size + 14) / 2, t, size))


def sign(cx, cy, t, w=None, size=34, fill='#D9A441', col=INK, rot=0):
    """Wall/hanging sign plate in hand caps ('RAILROAD COMPANY')."""
    w = w or tw(t, size, 'caps') + 50
    h = size * 1.1 * len(str(t).split('\n')) + 22
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{INK}" stroke-width="{LW2}"/>'
            + caps(cx, cy + 2, t, size, col) + '</g>')


def post_sign(x, y, t, size=26, w=None):
    """Wooden sign on a post ('HUDSON RIVER', 'SAME WAY')."""
    w = w or tw(t, size, 'caps') + 36
    h = size * 1.1 * len(str(t).split('\n')) + 20
    return (f'<rect x="{x - 7}" y="{y - h - 70}" width="14" height="{h + 70}" fill="{WOOD}" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x - w / 2}" y="{y - h - 100}" width="{w}" height="{h}" rx="3" fill="#4A3324" stroke="{INK}" stroke-width="{LW2}"/>'
            + caps(x, y - h / 2 - 98, t, size, '#F2EBDD'))


def sky(top='#A9D3EA', ground=None, horizon=None):
    hz = horizon if horizon is not None else H() * .78
    o = fill_bg(top)
    if ground: o += f'<rect x="-200" y="{hz}" width="{W() + 400}" height="{H() + 200}" fill="{ground}"/><path d="M-200 {hz} H{W() + 200}" stroke="{INK}" stroke-width="{LW2}"/>'
    return o


def cloud(cx, cy, s=1):
    return g(cx, cy, s, f'<path d="M-60 10 Q-64 -14 -36 -16 Q-30 -40 -4 -34 Q14 -50 34 -30 Q62 -30 60 -2 Q66 14 46 16 H-46 Q-62 16 -60 10 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="2.6"/>')


def buildings(y, x0=-60, x1=None, seed=3, palette=('#D8CDB8', '#C9B79A', '#B9C3C9', '#E2DACB', '#A9AFA8'), hmin=.35, hmax=.75):
    """Row of flat facades with window grids standing on y."""
    x1 = x1 if x1 is not None else W() + 60
    rnd = random.Random(seed)
    o, x = [], x0
    while x < x1:
        bw, bh = rnd.uniform(110, 210), rnd.uniform(hmin, hmax) * y
        col = rnd.choice(palette)
        o.append(f'<rect x="{x:.0f}" y="{y - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{col}" stroke="{INK}" stroke-width="{LW2}"/>')
        for wy in range(int(y - bh + 18), int(y - 30), 34):
            for wx in range(int(x + 14), int(x + bw - 26), 30):
                o.append(f'<rect x="{wx}" y="{wy}" width="16" height="20" fill="#7E95A6" stroke="{INK}" stroke-width="1.8"/>')
        x += bw + rnd.uniform(-10, 6)
    return ''.join(o)


def skyline(y, col='#9FB3C2', seed=5):
    rnd = random.Random(seed)
    o, x = [], -60
    while x < W() + 60:
        bw, bh = rnd.uniform(40, 110), rnd.uniform(60, 220)
        o.append(f'<rect x="{x:.0f}" y="{y - bh:.0f}" width="{bw:.0f}" height="{bh + 2:.0f}" fill="{col}"/>')
        x += bw
    return ''.join(o)


def street(ground='#B9AE9B', sky_col='#A9D3EA', seed=3):
    hz = H() * .74
    return (sky(sky_col) + skyline(hz - 120, '#BFD0DA', seed + 1) + buildings(hz, seed=seed) +
            f'<rect x="-200" y="{hz}" width="{W() + 400}" height="{H()}" fill="{ground}"/><path d="M-200 {hz} H{W() + 200}" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<rect x="-200" y="{hz}" width="{W() + 400}" height="16" fill="#CFC6B6" stroke="{INK}" stroke-width="2.4"/>')


def stage(cx=None, floor_y=None, bg='#232326'):
    """Character-introduction spotlight: dark void, light cone from above, lit floor ellipse. Put the character at (cx, floor_y)."""
    cx = cx if cx is not None else W() / 2
    fy = floor_y if floor_y is not None else H() * .8
    gid = uid('sg')
    return (fill_bg(bg) + f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2E6C4" stop-opacity=".05"/>'
            f'<stop offset="1" stop-color="#F2E6C4" stop-opacity=".22"/></linearGradient></defs>'
            f'<path d="M{cx - 40} -40 L{cx + 40} -40 L{cx + 180} {fy} L{cx - 180} {fy} Z" fill="url(#{gid})"/>'
            f'<ellipse cx="{cx}" cy="{fy}" rx="230" ry="48" fill="#5A4E3A" opacity=".55"/><ellipse cx="{cx}" cy="{fy}" rx="185" ry="36" fill="#A08A60"/>')


def info_bg(col=INFO_BG, blob=INFO_BLOB):
    """Blue-grey explainer backdrop with a soft lighter blob (infographic shots)."""
    gid = uid('ib')
    return (fill_bg(col) + f'<defs><radialGradient id="{gid}"><stop offset="0" stop-color="{blob}"/><stop offset=".7" stop-color="{blob}" stop-opacity=".6"/>'
            f'<stop offset="1" stop-color="{blob}" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse cx="{W() / 2}" cy="{H() / 2}" rx="{W() * .46}" ry="{H() * .42}" fill="url(#{gid})"/>')


def rays_bg(col='#8DA1B1', ray='#A3B5C2', n=24):
    """Sunburst for logo/wordmark reveals and 'big moment' objects."""
    cx, cy, R = W() / 2, H() / 2, max(W(), H())
    o = [fill_bg(col)]
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + .5) / n
        o.append(f'<path d="M{cx} {cy} L{cx + R * math.cos(a0):.0f} {cy + R * math.sin(a0):.0f} L{cx + R * math.cos(a1):.0f} {cy + R * math.sin(a1):.0f} Z" fill="{ray}" opacity=".55"/>')
    return ''.join(o)


def burst(cx, cy, r=120, col='#F7D35C', n=14):
    """Spiky glow behind a 'eureka' object or a happy character."""
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        rr = r if i % 2 == 0 else r * .62
        pts.append(f'{cx + rr * math.cos(a):.0f},{cy + rr * math.sin(a):.0f}')
    return f'<polygon points="{" ".join(pts)}" fill="{col}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'


def blob(cx, cy, rx, ry=None, seed=1, n=9, jit=.32):
    """Smooth irregular closed path (continents, bushes, rocks, smoke)."""
    rnd = random.Random(seed); ry = ry or rx
    pts = [(cx + rx * (1 + rnd.uniform(-jit, jit)) * math.cos(2 * math.pi * i / n), cy + ry * (1 + rnd.uniform(-jit, jit)) * math.sin(2 * math.pi * i / n)) for i in range(n)]
    mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2) for i in range(n)]
    d = f'M{mids[-1][0]:.0f} {mids[-1][1]:.0f} ' + ' '.join(f'Q{pts[i][0]:.0f} {pts[i][1]:.0f} {mids[i][0]:.0f} {mids[i][1]:.0f}' for i in range(n)) + ' Z'
    return d


def globe(cx, cy, r, space=True):
    """Earth from space (hooks: 'one company, the whole world')."""
    rnd = random.Random(7)
    cid = uid('gl')
    o = [fill_bg('#141A2A')] if space else []
    if space:
        o += [f'<circle cx="{rnd.uniform(0, W()):.0f}" cy="{rnd.uniform(0, H()):.0f}" r="{rnd.uniform(.8, 2.2):.1f}" fill="#FFFFFF" opacity="{rnd.uniform(.4, .9):.2f}"/>' for _ in range(90)]
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 18}" fill="#5C8FC9" opacity=".18"/>')
    o.append(f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath><circle cx="{cx}" cy="{cy}" r="{r}" fill="#3E6FA8"/>')
    land = ''.join(f'<path d="{blob(cx + dx * r, cy + dy * r, k * r * .22, k * r * .3, seed=i + 3, n=11, jit=.45)}" fill="#6AA057" stroke="#2F5E2A" stroke-width="2.4"/>'
                   for i, (dx, dy, k) in enumerate(((-.55, -.35, 1.1), (-.35, .3, .9), (.25, -.45, .8), (.35, .15, 1.2), (.05, .7, .5), (-.8, .2, .5), (.75, -.1, .45))))
    o.append(f'<g clip-path="url(#{cid})">{land}<circle cx="{cx + r * .35}" cy="{cy}" r="{r}" fill="#000" opacity=".18"/></g>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="{LW2}"/>')
    return ''.join(o)


# ------------------------------------------------------------------ props: money, docs, charts, tech
def cash(x, y, s=1, rot=0):
    return g(x, y, s, f'<rect x="-44" y="-22" width="88" height="44" rx="4" fill="#7FBF6A" stroke="{INK}" stroke-width="3"/>'
                      f'<rect x="-36" y="-14" width="72" height="28" rx="3" fill="none" stroke="#3E7A34" stroke-width="2"/>'
                      + text(0, 1, '$', 26, CAPS, '#2F6A2A'), rot=rot)


def money_pile(cx, y, w=360, seed=4):
    rnd = random.Random(seed)
    return ''.join(cash(cx + rnd.uniform(-w / 2, w / 2) * (1 - k / 40), y - k * 4, rnd.uniform(.8, 1.1), rnd.uniform(-35, 35)) for k in range(36))


def money_bag(x, y, s=1, mark='$'):
    return g(x, y, s, f'<path d="M-46 -10 C-56 -60 -26 -86 -14 -96 L-22 -112 H22 L14 -96 C26 -86 56 -60 46 -10 C40 4 -40 4 -46 -10 Z" fill="#E2A65E" stroke="{INK}" stroke-width="3.4"/>'
                      f'<path d="M-18 -98 H18" stroke="{INK}" stroke-width="5"/>' + text(0, -44, mark, 44, CAPS, '#3E8E3A'))


def gold_bars(cx, y, n=6):
    o = []
    for i in range(n):
        r, c = divmod(i, 3)
        x = cx + (c - 1) * 70 + r * 35
        yy = y - r * 26
        o.append(f'<path d="M{x - 32} {yy} L{x - 24} {yy - 22} H{x + 24} L{x + 32} {yy} Z" fill="#E7B84A" stroke="{INK}" stroke-width="3"/>')
    return ''.join(o)


def document(cx, cy, w, h, title='', lines=6, rot=0, stamp=None, stamp_col=RED, sig=False, body_text=None):
    o = [f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" fill="#FBFAF6" stroke="{INK}" stroke-width="{LW2}"/>']
    if title: o.append(caps(cx, cy - h / 2 + 40, title, min(34, w / max(6, len(title)) * 1.6)))
    if body_text:
        o.append(text(cx - w / 2 + 26, cy - h / 2 + 90, body_text, 22, SCRIPT, INK, 'start', lh=1.15))
    else:
        for i in range(lines):
            yy = cy - h / 2 + 80 + i * 26
            if yy > cy + h / 2 - 50: break
            o.append(f'<path d="M{cx - w / 2 + 26} {yy} H{cx + w / 2 - 26 - (40 if i % 3 == 2 else 0)}" stroke="#555" stroke-width="2.4"/>')
    if sig: o.append(f'<path d="M{cx + w * .05} {cy + h / 2 - 40} c10 -20 20 10 30 -6 s16 14 26 -4 s14 10 30 -2" fill="none" stroke="{INK}" stroke-width="2.4"/>')
    if stamp:
        o.append(f'<g transform="rotate(-14 {cx} {cy + h * .18})"><rect x="{cx - w * .36}" y="{cy + h * .18 - 26}" width="{w * .72}" height="52" rx="6" fill="none" stroke="{stamp_col}" stroke-width="5"/>'
                 + caps(cx, cy + h * .18 + 2, stamp, 34, stamp_col) + '</g>')
    return f'<g transform="rotate({rot} {cx} {cy})">{"".join(o)}</g>'


def newspaper(cx, cy, w, h, headline, sub='', photo='', rot=0, masthead='THE DAILY LEDGER'):
    o = [f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" fill="#E9E7E1" stroke="{INK}" stroke-width="{LW2}"/>',
         caps(cx, cy - h / 2 + 30, masthead, 22), f'<path d="M{cx - w / 2 + 18} {cy - h / 2 + 48} H{cx + w / 2 - 18}" stroke="{INK}" stroke-width="2.4"/>',
         caps(cx, cy - h / 2 + 92 + headline.count('\n') * 24, headline, min(46, (w - 40) / max(8, max(len(l) for l in headline.split(chr(10)))) * 1.75))]
    py = cy - h / 2 + 140 + 48 * (headline.count('\n'))
    if sub: o.append(text(cx, py, sub, 22, SCRIPT, '#333')); py += 30
    pw, ph = w * .48, h - (py - (cy - h / 2)) - 30
    o.append(f'<rect x="{cx - w / 2 + 20}" y="{py}" width="{pw:.0f}" height="{ph:.0f}" fill="#BDBBB4" stroke="{INK}" stroke-width="2.4"/>{photo}')
    for i in range(int(ph / 18)):
        o.append(f'<path d="M{cx - w / 2 + 40 + pw} {py + 10 + i * 18} H{cx + w / 2 - 22}" stroke="#77756F" stroke-width="2.2"/>')
    return f'<g transform="rotate({rot} {cx} {cy})">{"".join(o)}</g>'


def chart(x, y, w, h, pts, col=RED, title='', board='#F8F6F0', kf_line=None):
    """Whiteboard chart; pts = values 0..1 left to right. kf_line=animlib.draw(t, d) draws the line on."""
    path = ' '.join(f'{"M" if i == 0 else "L"}{x + 30 + (w - 60) * i / (len(pts) - 1):.0f} {y + h - 30 - (h - 80) * v:.0f}' for i, v in enumerate(pts))
    line = f'<path d="{path}" fill="none" stroke="{col}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>'
    return (f'<rect x="{x - 10}" y="{y - 10}" width="{w + 20}" height="{h + 20}" fill="#6B4A31" stroke="{INK}" stroke-width="{LW2}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{board}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x + 24} {y + 40} V{y + h - 24} H{x + w - 20}" fill="none" stroke="{INK}" stroke-width="3"/>'
            + (caps(x + 26, y + 26, title, 24, INK, 'start') if title else '')
            + (animlib.G(line, kf_line) if kf_line else line))


def bars(x, y, w, h, vals, cols=None, labels=None, kf_t=None):
    """Bar chart on the current background; vals 0..1. kf_t = time the bars grow (staggered)."""
    n = len(vals)
    bw = w / (n * 1.5)
    o = [f'<path d="M{x} {y - h} V{y} H{x + w}" fill="none" stroke="{INK}" stroke-width="3.4"/>']
    for i, v in enumerate(vals):
        bx = x + bw * .5 + i * bw * 1.5
        c = (cols or [GREEN] * n)[i]
        bar = f'<rect x="{bx:.0f}" y="{y - h * v:.0f}" width="{bw:.0f}" height="{h * v:.0f}" fill="{c}" stroke="{INK}" stroke-width="3"/>'
        o.append(animlib.G(bar, [[0, {'sy': 0}], [kf_t + i * .12, {'sy': 0}], [kf_t + i * .12 + .4, {'sy': 1}, 'b']], (bx, y)) if kf_t is not None else bar)
        if labels: o.append(caps(bx + bw / 2, y + 22, labels[i], 18))
    return ''.join(o)


def price_box(cx, cy, t, fill=RED, size=44, w=None):
    w = w or tw(t, size, 'caps') + 40
    return f'<rect x="{cx - w / 2}" y="{cy - size * .9}" width="{w}" height="{size * 1.8}" fill="{fill}" stroke="{INK}" stroke-width="3"/>' + caps(cx, cy + 1, t, size, '#FFFFFF')


def stat_card(cx, cy, big, small='', col=GREEN, w=None, size=64):
    """'$22 BILLION / COMBINED VALUE' - white rounded card, big coloured hand caps."""
    w = w or max(tw(big, size, 'caps'), tw(small, 24, 'caps')) + 70
    h = size * 1.2 + (40 if small else 20)
    return (f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="14" fill="#FFFFFF" stroke="{INK}" stroke-width="3.4"/>'
            + caps(cx, cy - (12 if small else 0), big, size, col) + (caps(cx - w / 2 + 34, cy + h / 2 - 22, small, 22, INK, 'start') if small else ''))


def arrow(x0, y0, x1, y1, col=RED, w=26):
    """Chunky outlined block arrow."""
    a = math.atan2(y1 - y0, x1 - x0)
    L = math.hypot(x1 - x0, y1 - y0)
    hw, hl = w * .5, w * 1.3
    pts = [(0, -hw / 2), (L - hl, -hw / 2), (L - hl, -w * .8), (L, 0), (L - hl, w * .8), (L - hl, hw / 2), (0, hw / 2)]
    P = ' '.join(f'{x0 + px * math.cos(a) - py * math.sin(a):.0f},{y0 + px * math.sin(a) + py * math.cos(a):.0f}' for px, py in pts)
    return f'<polygon points="{P}" fill="{col}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'


def mark(x, y, ok=True, s=1):
    """Green check / red cross."""
    if ok:
        return f'<path d="M{x - 16 * s} {y} L{x - 4 * s} {y + 13 * s} L{x + 18 * s} {y - 15 * s}" fill="none" stroke="{GREEN}" stroke-width="{8 * s}" stroke-linecap="round" stroke-linejoin="round"/>'
    return f'<path d="M{x - 15 * s} {y - 15 * s} L{x + 15 * s} {y + 15 * s} M{x + 15 * s} {y - 15 * s} L{x - 15 * s} {y + 15 * s}" stroke="{RED}" stroke-width="{8 * s}" stroke-linecap="round"/>'


def calendar(cx, cy, month='MARCH 2024', circle=None, w=230, xs=0):
    """Desk calendar; circle = day index (0..27) to ring in red; xs = number of days crossed out."""
    h = w * .9
    o = [f'<path d="M{cx - w / 2} {cy + h / 2} L{cx - w / 2 + 16} {cy - h / 2} H{cx + w / 2 - 16} L{cx + w / 2} {cy + h / 2} Z" fill="#EDE6D3" stroke="{INK}" stroke-width="{LW2}"/>',
         f'<rect x="{cx - w / 2 + 16}" y="{cy - h / 2}" width="{w - 32}" height="{h * .2}" fill="{RED}" stroke="{INK}" stroke-width="{LW2}"/>',
         caps(cx, cy - h / 2 + h * .1 + 2, month, w * .09, '#FFFFFF')]
    for d in range(28):
        r, c = divmod(d, 7)
        x, y = cx - w / 2 + 34 + c * (w - 68) / 6, cy - h / 2 + h * .32 + r * h * .16
        o.append(caps(x, y, str(d + 1), w * .07))
        if d < xs: o.append(mark(x, y, False, .5))
        if circle == d: o.append(f'<ellipse cx="{x}" cy="{y}" rx="{w * .07}" ry="{w * .06}" fill="none" stroke="{RED}" stroke-width="3"/>')
    return ''.join(o)


def server_racks(x0, y, n=4, h=300, w=110, glow='#47E2F0'):
    o = []
    for i in range(n):
        x = x0 + i * (w + 16)
        o.append(f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" rx="6" fill="#3A3F48" stroke="{INK}" stroke-width="{LW2}"/>')
        for k in range(int(h / 34)):
            yy = y - h + 14 + k * 34
            o.append(f'<rect x="{x + 10}" y="{yy}" width="{w - 20}" height="22" rx="3" fill="#2A2E35" stroke="{INK}" stroke-width="1.6"/>'
                     f'<circle cx="{x + w - 22}" cy="{yy + 11}" r="3.4" fill="{glow if (i + k) % 3 else "#7CF08A"}"/>')
    return ''.join(o)


def wordmark(cx, cy, name, icon='spark', col='#FFFFFF', size=72, sub=None):
    """Generic company mark: a simple geometric icon + the name in hand caps. Never a real logo."""
    ic = {'spark': ''.join(f'<path d="M0 0 L{34 * math.cos(a):.0f} {34 * math.sin(a):.0f}" stroke="{col}" stroke-width="9" stroke-linecap="round"/>' for a in [i * math.pi / 4 for i in range(8)]),
          'ring': f'<circle r="28" fill="none" stroke="{col}" stroke-width="10"/>',
          'tri': f'<path d="M0 -32 L30 24 H-30 Z" fill="{col}"/>',
          'block': f'<rect x="-28" y="-28" width="56" height="56" rx="10" fill="{col}"/>'}.get(icon, '')
    tw_ = tw(name, size, 'caps')
    return (f'<g transform="translate({cx - tw_ / 2 - 30} {cy})">{ic}</g>' + caps(cx + 30, cy + 4, name, size, col)
            + (caps(cx, cy + size * .9, sub, size * .36, col) if sub else ''))


def jag_split(x, col='#111', w=26):
    """Lightning-shaped divider for two-sided phone calls / arguments (vertical, at x)."""
    pts = []
    y, k = -20, 0
    while y < H() + 40:
        pts.append((x + (w if k % 2 else -w), y)); y += 70; k += 1
    left = ' '.join(f'{px - 9:.0f},{py}' for px, py in pts)
    right = ' '.join(f'{px + 9:.0f},{py}' for px, py in reversed(pts))
    return f'<polygon points="{left} {right}" fill="{col}"/>'


def panel(x, y, w, h, inner, bg='#E6DCC6'):
    """Clipped comic panel (phone-call rows, split screens). inner uses frame coordinates."""
    cid = uid('p')
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'
            f'<g clip-path="url(#{cid})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>{inner}</g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-width="5"/>')
```

### cc_shots.py: shot templates, framed for 16:9 or 9:16, synced to `vo.json`, with automatic SFX cues.
```python
"""Shot templates: one call = one finished shot, framed for 16:9 or 9:16 (whatever animlib.set_format chose).
Each takes `sh` = the shot's entry from timeline.json ({start, end, lines:[{t0, t1, words}]}) so text and mouth
flaps land on the voice. Anything a template can't do: build the shot by hand with cc_kit + scene()."""
from animlib import *
from cc_kit import *


def V(): return W() < H()
def span(sh): return sh['start'], sh['end'], sh['end'] - sh['start']
def line(sh, i=0): return sh['lines'][i] if sh.get('lines') else {'t0': 0, 't1': sh['end'] - sh['start'], 'words': []}
CUES = []   # (sfx name, GLOBAL time, gain) collected by the templates; mix them in the sound step


def cue(name, t, gain=1.0): CUES.append([name, round(t, 3), gain])


def wt(sh, word):
    """Local time of the first word starting with `word` (any line of the shot), for syncing a reveal to the VO."""
    for ln in sh.get('lines', []):
        for w, t0, t1 in ln['words']:
            if w.lower().strip('.,!?:;"\'$').startswith(word.lower()): return t0
    return line(sh)['t0']
def head_y(feet, s): return feet - 196 * s          # head centre of a person() at scale s
def feet_for(head, s): return head + 196 * s         # feet y that puts the head centre at `head`


def t_card(sh, text_, title=False, z=1):
    """Black card. title=True: chapter title, hard cut, no typing. Otherwise the narration line types on with the voice."""
    st, en, d = span(sh)
    if title: return scene(st, en, chapter(text_), z=z)
    ln = line(sh)
    size = 44 if not V() else 54
    return scene(st, en, card(text_, size, kf=typewrite(ln['t0'], max(ln['t0'] + .3, ln['t1'] - .1))), z=z)


def t_spot(sh, who, s=None, label=None):
    """Character introduction: dark stage, light cone, the character fades up; optional typed name label + arrow."""
    st, en, d = span(sh)
    s = s or (1.5 if not V() else 1.9)
    cx, fy = W() / 2, H() * (.8 if not V() else .66)
    o = stage(cx, fy) + G(person(cx, fy, s, **who), fade(0, .35))
    cue('boom', st, .45)
    if label:
        lx, ly = (cx + 300, H() * .28) if not V() else (cx, H() * .18)
        o += label_arrow(lx, ly, label, (cx + 60, head_y(fy, s) - 20), 38 if not V() else 46, kf=type_cps(.4, label, 18))
    return scene(st, en, frame_svg(o, 'spotlight intro'), cam=push(d, 1.06))


def t_place(sh, setting, caption=None, reveal=True):
    """Establishing shot: pull-out reveal from 1.45x + typed place/date caption ('Pune, 2014.')."""
    st, en, d = span(sh)
    o = setting + (place_caption(caption, 40 if not V() else 52, kf=type_cps(.3, caption, 16)) if caption else '')
    return scene(st, en, frame_svg(o, caption or 'establishing'), cam=pull(d, 1.45, dur=min(2.6, d)) if reveal else push(d, 1.05))


def office(wall=CREAM_WALL, night=False, seed=2):
    """The default interior: wall, wood panelling, window (city), bookshelf, curtain."""
    if not V():
        return (room(wall, WOOD, H() * .76, wainscot=H() * .52) + bookshelf(30, 90, 190, 330, seed) +
                window(W() * .56, 60, 300, 220, 'night' if night else 'city') + curtain(W() - 190, 30, 160, 470))
    return (room(wall, WOOD, H() * .7, wainscot=H() * .46) + window(60, 110, 300, 250, 'night' if night else 'city') +
            bookshelf(W() - 220, 120, 190, 420, seed))


def t_desk(sh, who, bg=None, text_=None, voiced=True, plaque_txt=None, props='', s=None):
    """Medium shot of one character behind a desk (the workhorse of business stories)."""
    st, en, d = span(sh)
    bg = bg if bg is not None else office()
    s = s or (1.55 if not V() else 2.0)
    cx = W() / 2 if V() else W() * .42
    hy = H() * (.42 if not V() else .44)
    fy = feet_for(hy, s)
    dy = hy + 150 * s / 1.55
    ln = line(sh)
    o = [bg, chair_back(cx, dy + 10, w=150 * s, h=dy + 10 - (hy + 6 * s)),
         person(cx, fy, s, talk=(ln['t0'], ln['t1']) if (text_ and voiced) else None, **who),
         desk(cx, dy, (600 if not V() else 640), 400), papers(cx - 210, dy + 14, 6, 110), papers(cx + 210, dy + 14, 5, 110), props]
    if plaque_txt: o.append(plaque(cx, dy + 14, plaque_txt, size=22 if not V() else 28))
    if text_: o.append(_line(sh, text_, voiced, (cx, hy), s))
    return scene(st, en, frame_svg(''.join(o), 'desk shot'), cam=push(d, 1.05), cam_o=(cx, hy))


def _line(sh, text_, voiced, head, s, side=1):
    """Voiced -> white text + tick near the head, appears when the line starts. Unvoiced -> bubble pops on the line start."""
    ln = line(sh)
    hx, hy = head
    big = 40 if not V() else 52
    if voiced:
        if V(): x, y = W() / 2, hy - 44 * s - 150
        else: x, y = hx + side * (60 * s + tw(text_, big) / 2), hy - 44 * s - 30
        return say(x, max(60, y), text_, big, to=(hx + side * 30 * s, hy - 40 * s), kf=appear(ln['t0']))
    x = W() / 2 if V() else hx + side * (40 * s + tw(text_, 34) / 2)
    y = max(70, hy - 44 * s - (130 if V() else 90))
    cue('pop', sh['start'] + max(0, ln['t0'] - .05), .6)
    return bubble(x, y, text_, tail=(hx + side * 10 * s, hy - 48 * s), size=36 if not V() else 46, kf=pop(max(0, ln['t0'] - .05)))


def t_two(sh, a, b, speaker='a', text_=None, voiced=True, bg=None, sa=None, sb=None):
    """Two-shot: a (left) and b (right) facing each other; one of them says/bubbles the line."""
    st, en, d = span(sh)
    bg = bg if bg is not None else office()
    sa, sb = sa or (1.5 if not V() else 1.7), sb or (1.5 if not V() else 1.7)
    gy = H() * (.9 if not V() else .8)                      # both stand on the same floor line
    ha, hb = gy - 196 * sa, gy - 196 * sb
    xa, xb = (W() * .3, W() * .7) if not V() else (W() * .28, W() * .74)
    ln = line(sh)
    ta = dict(a); tb = dict(b)
    if text_ and voiced: (ta if speaker == 'a' else tb)['talk'] = (ln['t0'], ln['t1'])
    ta.setdefault('look', 5); tb.setdefault('look', -5)
    o = [bg, person(xa, feet_for(ha, sa), sa, **ta), person(xb, feet_for(hb, sb), sb, **tb)]
    if text_:
        hx, hy, s, side = (xa, ha, sa, 1) if speaker == 'a' else (xb, hb, sb, -1)
        o.append(_line(sh, text_, voiced, (hx, hy), s, side))
    return scene(st, en, frame_svg(''.join(o), 'two-shot'), cam=pan(d, 40 if not V() else 24, s=1.06))


def t_close(sh, who, text_=None, voiced=True, bg=None, s=None, side=1):
    """Close-up on a face (reactions, the key line). Mouth flaps while a voiced line plays."""
    st, en, d = span(sh)
    s = s or (2.4 if not V() else 3.0)
    hx, hy = (W() * .4, H() * .55) if not V() else (W() / 2, H() * .52)
    ln = line(sh)
    w = dict(who)
    if text_ and voiced: w['talk'] = (ln['t0'], ln['t1'])
    o = [bg if bg is not None else office(), person(hx, feet_for(hy, s), s, **w)]
    if text_: o.append(_line(sh, text_, voiced, (hx, hy), s, side))
    return scene(st, en, frame_svg(''.join(o), 'close-up'), cam=push(d, 1.06), cam_o=(hx, hy))


def t_ots(sh, front, back, text_=None, voiced=True, bg=None):
    """Over-the-shoulder: `back` (seen from behind) big in the near corner, `front` speaking to them."""
    st, en, d = span(sh)
    sf_, hy = (1.9 if not V() else 2.5), H() * (.42 if not V() else .46)
    fx = W() * .62 if not V() else W() * .58
    ln = line(sh)
    f = dict(front)
    if text_ and voiced: f['talk'] = (ln['t0'], ln['t1'])
    o = [bg if bg is not None else office(), person(fx, feet_for(hy, sf_), sf_, **f),
         person(W() * .14 if not V() else W() * .06, H() * (1.45 if not V() else 1.42), 2.4 if not V() else 3.0, back=True, **back)]
    if text_: o.append(_line(sh, text_, voiced, (fx, hy), sf_, 1 if not V() else -1))
    return scene(st, en, frame_svg(''.join(o), 'over the shoulder'), cam=push(d, 1.05))


def t_compare(sh, left, right, label=None, w_left=None, w_right=None, label_col=RED):
    """Infographic: [left box] -> [right box] + caps label on the blue-grey backdrop. Each pops on its word.
    left/right = (text, fill, word_to_sync)."""
    st, en, d = span(sh)
    cx, cy = W() / 2, H() / 2
    (lt, lf, lw), (rt, rf, rw) = left, right
    t1, t2 = wt(sh, lw), wt(sh, rw)
    cue('pop', st + t1, .6); cue('ding', st + t2, .6)
    if not V(): a, b = (cx - 300, cy - 30), (cx + 240, cy - 30)
    else: a, b = (cx, cy - 260), (cx, cy + 120)
    arr = arrow(a[0] + 110, a[1], b[0] - 170, b[1], RED, 40) if not V() else arrow(a[0], a[1] + 80, b[0], b[1] - 80, RED, 40)
    o = [info_bg(), G(price_box(*a, lt, fill=lf, size=56), pop(t1), a), G(arr, wipe(t2 - .25, .35)), G(price_box(*b, rt, fill=rf, size=56), pop(t2), b)]
    if label: o.append(G(caps(cx, cy + (120 if not V() else 300), label, 64, label_col), pop(t2 + .45), (cx, cy + 120)))
    return scene(st, en, frame_svg(''.join(o), 'comparison'), cam=push(d, 1.05))


def t_stat(sh, big, small='', bg=None, word=None, col=GREEN):
    """Big number on a white card over a scene (or the blue-grey backdrop): '$22 BILLION / COMBINED VALUE'."""
    st, en, d = span(sh)
    t = wt(sh, word) if word else .2
    cue('ding', st + t, .6)
    o = (bg if bg is not None else info_bg()) + G(stat_card(W() / 2, H() * (.62 if not V() else .55), big, small, col, size=72 if not V() else 64), pop(t), (W() / 2, H() * .6))
    return scene(st, en, frame_svg(o, big), cam=push(d, 1.04))


def t_news(sh, headline, sub='', word=None, photo=''):
    """Newspaper close-up; the sub-line gets a marker swipe on `word`."""
    st, en, d = span(sh)
    cx, cy = W() / 2, H() / 2
    nw, nh = (min(900, W() - 60), 560) if not V() else (W() - 120, 760)
    ws = headline.split()
    hl = headline if not V() or len(headline) < 16 else ' '.join(ws[:(len(ws) + 1) // 2]) + '\n' + ' '.join(ws[(len(ws) + 1) // 2:])
    sy = cy - nh / 2 + 140 + 48 * hl.count('\n')
    o = [fill_bg('#4A3324'), newspaper(cx, cy, nw, nh, hl, sub, photo, rot=-2)]
    cue('paper', st, .8)
    if sub: o.append(G(f'<g transform="rotate(-2 {cx} {cy})"><rect x="{cx - tw(sub, 22) / 2 - 14}" y="{sy - 17}" width="{tw(sub, 22) + 28}" height="34" fill="#6FA8E0" opacity=".55"/></g>',
                       wipe((wt(sh, word) if word else .4) - .3, .5)))
    return scene(st, en, frame_svg(''.join(o), headline), cam=push(d, 1.12), cam_o=(cx, sy))


def t_panels(sh, roles, wall='#DCD2BE', phone=True):
    """Row (16:9) or 2x2 grid (9:16) of panels sliding in one per beat; roles = [(plaque, person_kwargs)].
    Classic 'everyone is calling' / 'every department said no' beat."""
    st, en, d = span(sh)
    n = len(roles)
    o = [fill_bg('#000')]
    for i, (lab, kw) in enumerate(roles):
        if not V(): x0, y0, pw, ph = i * W() / n, 0, W() / n, H()
        else: x0, y0, pw, ph = (i % 2) * W() / 2, (i // 2) * H() / 2, W() / 2, H() / 2
        ps = 2.0 if not V() else 1.6
        k = dict(kw); k.setdefault('arms', 'phone' if phone else 'down'); k.setdefault('skin', 'white')
        inner = (person(x0 + pw / 2, y0 + ph * .42 + 196 * ps, ps, **k)
                 + f'<rect x="{x0}" y="{y0 + ph * .8}" width="{pw}" height="{ph * .2 + 2}" fill="{WOOD}" stroke="{INK}" stroke-width="3"/>'
                 + (phone_old(x0 + pw * .2, y0 + ph * .84, .7) if phone else '') + plaque(x0 + pw * .6, y0 + ph * .84 + 6, lab, size=22))
        t = -.05 + i * min(.6, d / (n + 1))
        keys = ([[0, {'tx': 60 if not V() else 0, 'ty': 0 if not V() else 40, 'o': 0}]] if i else []) + \
               [[t, {'tx': 60 if not V() else 0, 'ty': 0 if not V() else 40, 'o': 0}], [t + .03, {'o': 1}], [t + .3, {'tx': 0, 'ty': 0}, 'o']]
        o.append(G(panel(x0, y0, pw, ph, inner, wall), keys)); cue('whoosh', st + max(0, t), .35)
    if phone: cue('phone', st + .2, .4)
    return scene(st, en, frame_svg(''.join(o), 'panels'))


def t_logo(sh, name, icon='spark', sub=None, montage=None):
    """'This is <Company>.' Wordmark over sunburst rays; montage=[svg, ...] strobes backgrounds every 0.12 s first."""
    st, en, d = span(sh)
    cx, cy = W() / 2, H() / 2
    if montage:
        lay = []
        for i, b in enumerate(montage):
            keys, t, k = [[-.01, {'o': 1 if i == 0 else 0}]], 0.0, 0
            while t < d - .9:
                keys.append([round(t, 3), {'o': 1 if k % len(montage) == i else 0}, 'h']); t += .12; k += 1
            keys.append([round(t, 3), {'o': 1 if i == 0 else 0}, 'h'])
            lay.append(G(b, keys))
        bg = ''.join(lay) + f'<rect width="{W()}" height="{H()}" fill="#000" opacity=".25"/>'
        cue('whoosh', st, .5)
    else:
        bg = rays_bg()
    return scene(st, en, frame_svg(bg + wordmark(cx, cy, name, icon, '#FFFFFF', 84 if not V() else 64, sub), name), cam=push(d, 1.05))
```

### cc_example.py: the worked example (36 s, both formats); run it to check the setup.
```python
"""Worked example, ~36 s, 16:9 or 9:16 from the same script:
logo montage -> newspaper -> spotlight intro -> chapter card -> place reveal -> silent bubble gag ->
voiced skit (close-up + over-the-shoulder) -> typed card -> comparison infographic -> phone panels.
  python3 cc_example.py script            # writes script.json
  python3 timeline.py tts script.json vo  # scratch voices -> vo.wav + vo.json (the timing)
  python3 cc_example.py build 16:9        # or 9:16 -> example.html + cues.json
  python3 render.py $PWD/example.html ex.mp4 0 <total printed by build>
  python3 cc_example.py sound             # final.wav (VO + bed + SFX, -14 LUFS)
  ffmpeg -i ex.mp4 -i final.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest example.mp4"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from animlib import set_format, page, scene, G
cmd = sys.argv[1]
set_format(sys.argv[2] if len(sys.argv) > 2 else '16:9')
from cc_kit import *
from cc_shots import *

SCRIPT = {"voices": {"N": 16, "kid": 18, "dad": 11}, "gap": [0.35, 0.75], "shots": [
    {"id": "hook", "vo": [{"text": "This is Nova Labs."}], "tail": .4},
    {"id": "news", "vo": [{"text": "Next month, it goes public at a $2 trillion valuation."}]},
    {"id": "spot", "vo": [{"text": "But ten years ago, it was one kid with a laptop."}]},
    {"id": "chap", "min": 2.0},
    {"id": "city", "vo": [{"text": "Pune, 2014."}], "min": 2.6},
    {"id": "home", "vo": [{"text": "His father had exactly one plan for him."}, {"text": "Engineering."}]},
    {"id": "kid", "vo": [{"text": "I'm going to build a robot that does my homework.", "who": "kid"}]},
    {"id": "dad", "vo": [{"text": "Then it can also do the dishes.", "who": "dad"}]},
    {"id": "card", "vo": [{"text": "It did neither."}]},
    {"id": "info", "vo": [{"text": "His first server cost $50."}, {"text": "Today, the company is worth two trillion."}]},
    {"id": "phones", "vo": [{"text": "And suddenly, everybody wanted to talk to him."}], "tail": 1.0},
]}
if cmd == 'script':
    json.dump(SCRIPT, open(os.path.join(HERE, 'script.json'), 'w'), indent=1); sys.exit(print('wrote script.json'))

if cmd == 'sound':
    from sfx_cc import *
    c = json.load(open(os.path.join(HERE, 'cues.json')))
    n = int(c['total'] * SR) + SR
    f = np.zeros((n, 2))
    for name, t, gain in c['fx']: place(f, fx(name), t, gain)
    mix(os.path.join(HERE, 'vo.wav'), f, bed(c['total'] + 1, c['music'], c['dips'])[:n], os.path.join(HERE, 'final.wav'))
    sys.exit(print('wrote final.wav'))

TL = json.load(open(os.path.join(HERE, 'vo.json')))
sh = {s['id']: s for s in TL['shots']}
# The cast: fixed looks, reused in every shot (model sheet)
KID = dict(skin='brown', suit='blue', hair='swoop', hair_col='black', tie=None, lapels=False)
DAD = dict(skin='brown', suit='grey', hair='bald', hair_col='black', moustache='black', glasses=True)
FOUNDER = dict(skin='brown', suit='hoodie', hair='swoop', hair_col='black', tie=None, lapels=False)
WIDE = W() > H()

S = []
cx, cy, R = W() / 2, H() / 2, min(W(), H())
S.append(t_logo(sh['hook'], 'NOVA LABS', 'spark', montage=[globe(cx, cy, R * .36), fill_bg('#2B2F36') + server_racks(cx - 280, H() * .9, 5, H() * .7),
                                                            street(seed=5), fill_bg('#5A3C2A') + bookshelf(-20, -20, W() + 40, H() + 40, 9)]))
S.append(t_news(sh['news'], 'NOVA LABS GOING PUBLIC', 'targeting a $2 trillion valuation', word='$2'))
S.append(t_spot(sh['spot'], dict(FOUNDER, expr='determined', arms='hold', extras=laptop(0, -84, .55, back=True))))
S.append(t_card(sh['chap'], 'The Making of a Founder', title=True))
d = sh['city']['end'] - sh['city']['start']
gy = H() * (.95 if WIDE else .7)
walkers = (G(extra(W() * .2, gy, .9, 'white', 'brown', walk=(0, d)), [[0, {'tx': -80}], [d, {'tx': 120}, 'l']]) +
           G(extra(W() * .78, gy + 10, 1.0, 'white', 'navy', hat='fedora', flip=True, walk=(.2, d)), [[0, {'tx': 60}], [d, {'tx': -140}, 'l']]))
S.append(t_place(sh['city'], street('#B9AE9B', '#E9C79A', seed=11) + walkers, 'Pune, 2014.'))
S.append(t_two(sh['home'], dict(DAD, expr='smug', arms='point_r'), dict(KID, expr='worried'), 'a', 'Engineering.\nFinal answer.', voiced=False, sb=1.1 if WIDE else 1.25))
S.append(t_close(sh['kid'], dict(KID, expr='happy'), "I'm going to build a robot\nthat does my homework." if WIDE else "I'm going to build\na robot that does\nmy homework."))
S.append(t_ots(sh['dad'], dict(DAD, expr='smug'), dict(KID), 'Then it can also do the dishes.' if WIDE else 'Then it can also\ndo the dishes.'))
S.append(t_card(sh['card'], 'It did neither.'))
S.append(t_compare(sh['info'], ('$50', '#5E6B78', '$50'), ('$2 TRILLION', GREEN, 'two'), '40 BILLION X'))
S.append(t_panels(sh['phones'], [('INVESTOR', dict(suit='navy', expr='grin')), ('REPORTER', dict(suit='brown', hat='fedora', expr='surprised')),
                                 ('BANKER', dict(suit='black', hat='top', expr='grin')), ('RIVAL CEO', dict(suit='grey', expr='surprised'))]))

out = os.path.join(HERE, 'example.html')
open(out, 'w').write(page(S, fonts_head(os.path.expanduser('~/fonts'))))
tot = TL['total']
json.dump({'total': tot, 'fx': CUES, 'music': [[0, sh['chap']['start'], 'mystery'], [sh['chap']['end'], tot, 'warm']],
           'dips': [[sh['chap']['start'], sh['chap']['end'], .25], [sh['card']['start'], sh['card']['end'], .4]]},
          open(os.path.join(HERE, 'cues.json'), 'w'), indent=1)
print(f'wrote {out}  total {tot:.2f}s  shots {len(S)}')
```

---

## 10. Recipes (motion rule → code)
- **Any shot:** `scene(start, end, frame_svg(svg), cam=push(d, 1.07))`. `start`/`end` come from `vo.json`; every key inside is local to the shot.
- **Sync to a word:** `wt(sh, 'trillion')` gives the local time. Use it for pops, wipes, counters and stamps.
- **Voiced line:** `say(x, y, text, size, to=(mouth_x, mouth_y), kf=appear(ln['t0']))` + `person(..., talk=(ln['t0'], ln['t1']))`. Keep the text out of the face and within ~1.5 head-widths of it.
- **Silent gag:** `bubble(x, y, text, tail=(head_x, head_top), kf=pop(t))` while the narrator paraphrases it.
- **Reveal:** `cam=pull(d, 1.45, dur=2.6)` + `place_caption('Pune, 2014.', kf=type_cps(.3, 'Pune, 2014.', 16))`.
- **Detail punch:** `scene(..., cam=punch(t, 1.8, .8, hold=1.2), cam_o=(doc_x, doc_y))`.
- **Walk across:** `G(person(..., walk=(0, d)), [[0, {'tx': -200}], [d, {'tx': 200}, 'l']])`.
- **Enter, then talk:** `G(person(...), slide(0, dx=-300, d=.5))`.
- **Character intro:** `t_spot(sh, who, label='Dario Amodei')`. The name types on with a curved arrow.
- **Number beat:** `t_compare` (A → B), `t_stat` (one big number), `count(t0, t1, v0, v1)` on a `<tspan data-fmt="money">`, or `bars(..., kf_t=t)` for a comparison.
- **Every department said no:** `t_panels(sh, roles, phone=False)` with each person `expr='angry'`, plus `document(..., stamp='DECLINED')` close-ups.
- **Phone fight:** two halves with `jag_split(W()/2)`, each character on its own `panel()`, the lines as `say()`.
- **Scandal or press beat:** `t_news(sh, 'HEADLINE', 'sub line', word='…')`. For a newspaper montage, stack 3 `newspaper()`s with different rotations popping 0.3 s apart over a dimmed scene.
- **AI model race:** robots on a podium or track with `sign(…, 'AI RACE')`, each with its own emblem colour and name tag. Benchmarks become bars behind them.
- **Time jump:** `globe()` + a rewind glyph and a year in caps, or `calendar(…, xs=n)` with days crossed off.
- **Mascot aside:** a hard cut to the mascot big in the foreground (`mascot(x, H()*1.2, 3.0, talk=...)`) on a plain wall, with one voiced line, then a hard cut back.
- **Sponsor read:**
  1. enter from a story line
  2. mascot with a URL bar (`sign()` styled white across the top)
  3. 4–6 shots of a **generic** UI (`monitor(..., chat_ui(...))`) with lavender label pills (`sign(..., fill='#C9B8F2')`) naming each feature
  4. a `stat_card` with the price or discount
  5. `t_card('Okay, back to the video.')`
- **Chapter transition:** the previous shot gets `xout=.4`, then `t_card(title=True)`, then the next shot gets `xin=.3`.
- **Bookend montage:** re-call 4–6 earlier shot builders with shorter `sh` spans (0.7–1.5 s each), then the final line on black.

## 11. QA checklist
Pull a contact sheet at 2 fps and check the frames around every cut:
```bash
ffmpeg -i out.mp4 -vf "fps=2,scale=384:-1,tile=8x5" -frames:v 1 sheet.jpg
```
- [ ] 14–16 cuts per minute; no shot over ~8 s except set-pieces; every shot has camera motion except cards and panels.
- [ ] Voiced lines show white text + tick **exactly while spoken** and the speaker's mouth flaps. Silent lines are bubbles. Never both on one line.
- [ ] Every number in the VO is on screen (box, card, plaque, sign or counter).
- [ ] Each named person gets a label or plaque on first appearance; the cast looks identical every time.
- [ ] No text inside a face or off the frame. In 9:16, nothing important below 72% of the height or above 12%.
- [ ] Chapter cards are instant; narration cards type with the voice; place captions type.
- [ ] No real logos, no real product UIs, no likenesses; real quotes verified.
- [ ] The intelligibility check is clean: no lexicon warnings, or the words are fixed with `"say"`. Transcribe the VO back if unsure.
- [ ] Music ~12 dB under the voice, dips under cards; loudness −14 LUFS.
- [ ] The opening formula is complete in the first 25 s (name → stake → paradox → question → origin pivot); the ending calls back the origin.