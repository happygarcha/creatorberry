"""Microsoft Edge neural Hindi TTS (hi-IN-MadhurNeural / hi-IN-SwaraNeural). usage: edge_hi_worker.py jobs.json
jobs = [{text, voice, out(.wav)}]. Trusts the session proxy CA in addition to certifi (verification stays on)."""
import asyncio, json, os, subprocess, sys, tempfile
import edge_tts
from edge_tts import communicate as cm
_ca = '/root/.ccr/ca-bundle.crt'
if os.path.exists(_ca): cm._SSL_CTX.load_verify_locations(cafile=_ca)

async def one(j):
    if os.path.exists(j['out']) and os.path.getsize(j['out']) > 1000: return
    mp3 = j['out'] + '.mp3'
    for k in range(4):
        try: await edge_tts.Communicate(j['text'], j['voice'], rate='+0%').save(mp3); break
        except Exception as e:
            if k == 3: raise
            await asyncio.sleep(2 * (k + 1))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp3, '-ac', '1', '-ar', '24000', j['out']], check=True); os.remove(mp3)

async def main():
    for j in json.load(open(sys.argv[1])): await one(j)
asyncio.run(main())
