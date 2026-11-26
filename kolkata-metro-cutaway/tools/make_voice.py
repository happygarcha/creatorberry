"""Hindi narration: Microsoft Edge neural voice hi-IN-MadhurNeural (+8%), one wav per line -> voice/vN.wav, voice/dur.json."""
import asyncio, json, os, subprocess, sys
import soundfile as sf
import edge_tts
from edge_tts import communicate as cm
cm._SSL_CTX.load_verify_locations(cafile='/root/.ccr/ca-bundle.crt')    # session proxy CA; verification stays on
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'voice')
L = json.load(open(os.path.join(P, 'lines.json'))); VOICE = os.environ.get('VOICE', 'hi-IN-MadhurNeural'); RATE = os.environ.get('RATE', '+8%')
async def main():
    D = {}
    for l in L:
        mp3 = os.path.join(P, l['id'] + '.mp3'); wav = os.path.join(P, l['id'] + '.wav')
        if not os.path.exists(wav): await edge_tts.Communicate(l['text'], VOICE, rate=RATE).save(mp3); subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp3, '-ac', '1', '-ar', '24000', wav], check=True); os.remove(mp3)
        y, sr = sf.read(wav); D[l['id']] = round(len(y) / sr, 3)
    json.dump(D, open(os.path.join(P, 'dur.json'), 'w'), indent=1); print(D)
asyncio.run(main())
