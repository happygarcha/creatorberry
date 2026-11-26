"""Hindi (Devanagari) text-to-speech, fully local. Piper hi_IN voices (pratham, priyamvada, rohan; MIT/CC0-style Piper voices from rhasspy/piper-voices)
run through onnxruntime; espeak-ng (espeakng-loader + phonemizer) converts Devanagari text to IPA.  Voice speed stays at natural 1.0 (length_scale 1.0).
  python3 hindi_tts.py "<text>" out.wav [voice]            voices: pratham (male), priyamvada (female), rohan (male)"""
import os, sys, json, re, unicodedata, numpy as np
MD = os.environ.get('HINDI_MODELS', os.path.expanduser('~/models/piper-hi'))
VOICES = {'pratham': 'hi_IN-pratham-medium', 'priyamvada': 'hi_IN-priyamvada-medium', 'rohan': 'hi_IN-rohan-medium'}
_sess, _phon = {}, [None]


def _phonemize(text):
    if _phon[0] is None:
        import espeakng_loader
        from phonemizer.backend.espeak.wrapper import EspeakWrapper
        EspeakWrapper.set_library(espeakng_loader.get_library_path()); EspeakWrapper.set_data_path(espeakng_loader.get_data_path())
        from phonemizer import phonemize
        _phon[0] = phonemize
    return _phon[0](text, language='hi', backend='espeak', strip=True, preserve_punctuation=True, with_stress=False)


def synth(text, voice='pratham', length_scale=1.0, noise=.667, noise_w=.8):
    import onnxruntime as ort
    name = VOICES[voice]
    if voice not in _sess:
        cfg = json.load(open(os.path.join(MD, name + '.onnx.json')))
        _sess[voice] = (ort.InferenceSession(os.path.join(MD, name + '.onnx'), providers=['CPUExecutionProvider']), cfg)
    s, cfg = _sess[voice]; idm = cfg['phoneme_id_map']
    ph = re.sub(r'\([a-z\-]+\)', '', _phonemize(text))            # drop language-switch tags
    ids = list(idm['^'])
    for ch in unicodedata.normalize('NFD', ph):
        if ch in idm: ids += idm[ch] + idm['_']
    ids += idm['$']
    feeds = {'input': np.array([ids], dtype=np.int64), 'input_lengths': np.array([len(ids)], dtype=np.int64), 'scales': np.array([noise, length_scale, noise_w], dtype=np.float32)}
    if cfg.get('num_speakers', 1) > 1: feeds['sid'] = np.array([0], dtype=np.int64)
    y = s.run(None, feeds)[0].squeeze().astype(np.float32)
    return y, cfg['audio']['sample_rate']


ROLE_VOICE = {'N': 'rohan', 'GUY': 'pratham', 'BANKER': 'pratham', 'FRIEND': 'priyamvada'}      # Piper fallback (rejected for quality)
PARLER_DESC = {   # Indic Parler-TTS named speakers; natural pace, close mic, no noise
    'N': 'Rohit speaks in a clear, natural, warm and expressive male voice at a calm moderate pace, with a very close recording that has no background noise.',
    'GUY': 'Aman speaks in a clear, expressive, slightly surprised male voice at a moderate pace, with a very close recording that has no background noise.',
    'BANKER': 'Rohit speaks in a confident, slightly smug male voice at a moderate pace, with a very close recording that has no background noise.',
    'FRIEND': 'Divya speaks in a clear, cheerful, expressive female voice at a moderate pace, with a very close recording that has no background noise.'}
PARLER_PY = os.path.expanduser('~/venvs/parler/bin/python')


def parler_prepare(script):
    """Synthesise every missing line in one worker run (model loads once); returns {(si, li): wav path}."""
    import hashlib, subprocess, tempfile
    jobs, paths = [], {}
    cdir = None
    return jobs, paths





def tts_script(script_p, out):
    """script.json (same shape as timeline.tts) -> out.wav + out.json (voice-first timeline). Voices stay at natural speed 1.0."""
    import soundfile as sf
    from scipy.signal import resample_poly
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import timeline as TL
    script = json.load(open(script_p)); clips, durs = {}, {}
    import hashlib, subprocess
    jobs = []
    for sh in script['shots']:
        for ln in sh.get('vo', []):
            who = ln.get('who', 'N'); txt = ln.get('say', ln['text'])
            cp = os.path.join(os.path.dirname(out), 'clips', f"parler_{who}_{hashlib.md5(txt.encode()).hexdigest()[:10]}.wav"); os.makedirs(os.path.dirname(cp), exist_ok=True)
            jobs.append({'text': txt, 'desc': PARLER_DESC[who], 'out': cp})
    jp = out + '_jobs.json'; json.dump(jobs, open(jp, 'w'), ensure_ascii=False)
    subprocess.run([PARLER_PY, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parler_hi_worker.py'), jp], check=True)
    for si, sh in enumerate(script['shots']):
        for li, ln in enumerate(sh.get('vo', [])):
            import hashlib
            who = ln.get('who', 'N'); txt = ln.get('say', ln['text'])
            cp = os.path.join(os.path.dirname(out), 'clips', f"parler_{who}_{hashlib.md5(txt.encode()).hexdigest()[:10]}.wav")   # cached: sampling is random, so a line is synthesised once and reused
            y, sr = sf.read(cp, dtype='float32')
            y = resample_poly(y, 24000, sr).astype(np.float32) if sr != 24000 else y
            r = np.sqrt(np.mean(y[np.abs(y) > 1e-3] ** 2)); y = y * (0.1 / max(r, 1e-6))            # equal loudness across the voices
            y = TL.trim(np.clip(y, -1, 1)); clips[(si, li)], durs[(si, li)] = y, len(y) / 24000
    tl, place = TL.layout(script, durs)
    total = np.zeros(int((tl['total'] + 1) * 24000), np.float32)
    for t, k in place:
        x = clips[k]; i = int(t * 24000); total[i:i + len(x)] += x
    sf.write(out + '.wav', total, 24000); json.dump(tl, open(out + '.json', 'w'), indent=1)
    print(f'{out}.wav  {tl["total"]:.1f}s  {len(tl["shots"])} shots')


if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'tts':
    tts_script(sys.argv[2], sys.argv[3]); sys.exit()
if __name__ == '__main__':
    import soundfile as sf
    y, sr = synth(sys.argv[1], sys.argv[3] if len(sys.argv) > 3 else 'pratham'); sf.write(sys.argv[2], y, sr); print(len(y) / sr, 's')
