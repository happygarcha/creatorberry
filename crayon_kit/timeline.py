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
