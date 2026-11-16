"""Render a frame range of the baked episode .blend (Cycles, CPU).
usage: python3 -I render_frames.py <blend> <outdir> <start> <end> [step] [--res PCT_OF_1080] [--samples N]
Skips frames that already exist, so it can be restarted / split across processes."""
import sys, os, bpy
a = sys.argv[1:]
blend, outdir, f0, f1 = a[0], a[1], int(a[2]), int(a[3])
step = int(a[4]) if len(a) > 4 and a[4].isdigit() else 1
pct = int(a[a.index('--res') + 1]) if '--res' in a else 100
bpy.ops.wm.open_mainfile(filepath=blend)
sc = bpy.context.scene
sc.render.resolution_percentage = pct
if '--samples' in a: sc.cycles.samples = int(a[a.index('--samples') + 1])
if '--threads' in a:
    sc.render.threads_mode = 'FIXED'; sc.render.threads = int(a[a.index('--threads') + 1])
os.makedirs(outdir, exist_ok=True)
for f in range(f0, f1 + 1, step):
    path = os.path.join(outdir, f"f{f:04d}.png")
    if os.path.exists(path): continue
    sc.frame_set(f); sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("DONE", f, flush=True)
