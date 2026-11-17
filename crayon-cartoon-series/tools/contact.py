"""contact.py <frames_dir> <out.jpg> [prefix] [cols]: tile stills (sorted by time) into a contact sheet."""
import sys, glob, os
from PIL import Image
d, out = sys.argv[1], sys.argv[2]
pre = sys.argv[3] if len(sys.argv) > 3 else 'still'
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 3
fs = sorted(glob.glob(os.path.join(d, pre + '_*.png')))
sel = [f for f in fs]
if len(sys.argv) > 5:
    lo, hi = float(sys.argv[5]), float(sys.argv[6])
    sel = [f for f in fs if lo <= float(os.path.basename(f).split('_')[1][:-4]) <= hi]
ims = [Image.open(f).convert('RGB').resize((300, 533)) for f in sel]
rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (cols * 304, rows * 537), 'white')
for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 304, (i // cols) * 537))
sheet.save(out, quality=88); print(len(ims), 'frames ->', out)
