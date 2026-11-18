"""Generate every spoken line as its own wav (free local Kokoro TTS via sherpa-onnx, natural speed 1.0) and measure durations."""
import sys, os, json, numpy as np, soundfile as sf
sys.path.insert(0, '../tools/engine')
import timeline as TL, sherpa_onnx
M = os.path.expanduser('~/models/kokoro-int8-multi-lang-v1_0/')
LINES = json.load(open('script.json'))
lexf = M + 'lexicon-xus-en.txt'
miss = TL.fix_lexicon(lexf, [l['text'] for l in LINES])
print('lexicon-missing:', miss)
eng = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
    kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(model=M + 'model.int8.onnx', voices=M + 'voices.bin', tokens=M + 'tokens.txt',
    data_dir=M + 'espeak-ng-data', lexicon=lexf, dict_dir=M + 'dict'), num_threads=2)))
out = {}
for l in LINES:
    a = eng.generate(l['text'].replace('…', ','), sid=l['sid'], speed=1.0)
    x = TL.trim(np.array(a.samples, dtype=np.float32))
    sf.write(f"audio/{l['id']}.wav", x, 24000)
    out[l['id']] = len(x) / 24000
    print(l['id'], l['who'], round(out[l['id']], 2), l['text'])
json.dump(out, open('audio/durations.json', 'w'), indent=1)
