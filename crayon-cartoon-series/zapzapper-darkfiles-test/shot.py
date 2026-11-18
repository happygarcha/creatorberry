import asyncio, sys
from playwright.async_api import async_playwright
async def m(ts, scale=1):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files','--disable-gpu','--no-sandbox'])
        pg = await b.new_page(viewport={'width':1280,'height':720}, device_scale_factor=scale)
        msgs=[]; pg.on('console', lambda m: msgs.append(m.text)); pg.on('pageerror', lambda e: msgs.append('ERR '+str(e)))
        await pg.goto('file:///home/user/creatorberry/crayon-cartoon-series/zapzapper-darkfiles-test/zz.html'); await pg.wait_for_timeout(600)
        for t in ts:
            await pg.evaluate(f'renderAt({t})'); await pg.screenshot(path=f'frames/s_{t:06.2f}.png')
        print('\n'.join(msgs[:10])); await b.close()
asyncio.run(m([float(x) for x in sys.argv[1].split(',')]))
