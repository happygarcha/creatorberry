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
