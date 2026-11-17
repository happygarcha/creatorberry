"""scene_sheet.py <frames_dir> <t0> <t1> <out.jpg>: sheet of every still with t0 <= t < t1 (4 columns)."""
import sys, glob, os
from PIL import Image
d, t0, t1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
fs = [f for f in sorted(glob.glob(os.path.join(d, 'still_*.png'))) if t0 <= float(os.path.basename(f)[6:-4]) < t1]
ims = [Image.open(f).convert('RGB').resize((300, 533)) for f in fs]
cols = 4; rows = (len(ims) + cols - 1) // cols
sh = Image.new('RGB', (cols * 304, rows * 537), 'white')
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 304, (i // cols) * 537))
sh.save(out, quality=88); print(len(ims), out)
