"""Extract a fixed character/prop reference sheet + palette from the ONE authoritative storyboard."""
import sys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
W, H = im.size
print("storyboard", W, H)
# panel crops (x0,y0,x1,y1) in storyboard pixels
crops = {
 "milo_pip_wide": (0, 175, 415, 430),
 "closeup_faces": (840, 145, 1252, 430),
 "high_five":     (1258, 530, 1672, 835),
 "ball":          (421, 270, 835, 430),
 "basket_pip":    (840, 530, 1252, 835),
 "bridge":        (0, 530, 415, 835),
}
sheet = Image.new("RGB", (1660, 1000), (250, 244, 235))
pos = [(0,0),(560,0),(1120,0),(0,520),(560,520),(1120,520)]
for (k, b), p in zip(crops.items(), pos):
    c = im.crop(b); c.thumbnail((540, 480)); sheet.paste(c, p)
sheet.save(out)
# palette sampling (storyboard px) -> printed for use in the build script
samples = {"milo_skin":(140,262),"milo_hair":(95,205),"milo_shirt":(105,338),"milo_overall":(60,385),
 "pip_body":(300,290),"pip_belly":(330,378),"pip_spike":(325,262),"ball_red":(205,350),"ball_blue":(238,392)}
for k,(x,y) in samples.items(): print(k, "#%02x%02x%02x"%im.getpixel((x,y)))
