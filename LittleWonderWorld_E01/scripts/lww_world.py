"""Little Wonder World - one garden scene. Shared geography functions + scene builder."""
import bpy, bmesh, math, random
import numpy as np
from mathutils import Matrix, Vector, Euler
from lww_chars import mat

BRIDGE_X0, BRIDGE_X1, STREAM_X = 15.0, 20.0, 17.5
PILE_X = 24.6
BASKET_X = 27.2


def sstep(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def g_base(x):
    return -1.2 * sstep((x - 1.0) / 9.0)


def ditch(x):
    return -1.25 * math.exp(-((x - STREAM_X) / 1.5) ** 2)


def yc(x):
    """centre line of the winding path"""
    return 0.5 * math.sin(0.32 * x) * (1 - math.exp(-((x - STREAM_X) / 3.0) ** 2))


def deck(x):
    u = (x - BRIDGE_X0) / (BRIDGE_X1 - BRIDGE_X0)
    u = max(0.0, min(1.0, u))
    return g_base(BRIDGE_X0) + 0.03 + 0.78 * (1 - (2 * u - 1) ** 2)


def terrain_z(x, y):
    z = g_base(x) + ditch(x)
    if y > 6.0: z += 0.07 * (y - 6.0) ** 2
    if y < -7.0: z += 0.05 * (-7.0 - y) ** 2
    return z


def ground(x, y=None):
    """height a character/ball stands on (bridge deck overrides the ditch)"""
    if BRIDGE_X0 <= x <= BRIDGE_X1:
        return deck(x)
    return terrain_z(x, yc(x) if y is None else y)


def slope(x):
    e = 0.05
    return (ground(x + e) - ground(x - e)) / (2 * e)


# ------------------------------------------------------------------ helpers
_TPL = {}
def _sphere_tpl(seg, ring):
    k = ("s", seg, ring)
    if k in _TPL: return _TPL[k]
    V = [(0, 0, 1)]
    for j in range(1, ring):
        th = math.pi * j / ring
        for i in range(seg):
            ph = 2 * math.pi * i / seg
            V.append((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)))
    V.append((0, 0, -1)); F = []
    for i in range(seg): F.append((0, 1 + i, 1 + (i + 1) % seg))
    for j in range(ring - 2):
        for i in range(seg):
            a = 1 + j * seg + i; b = 1 + j * seg + (i + 1) % seg
            F.append((a, a + seg, b + seg, b))
    last = len(V) - 1; base = 1 + (ring - 2) * seg
    for i in range(seg): F.append((last, base + (i + 1) % seg, base + i))
    _TPL[k] = (np.array(V, float), F); return _TPL[k]

def _cone_tpl(seg, r2, cap):
    k = ("c", seg, r2, cap)
    if k in _TPL: return _TPL[k]
    V = []
    for i in range(seg):
        a = 2 * math.pi * i / seg; V.append((math.cos(a), math.sin(a), -0.5))
    for i in range(seg):
        a = 2 * math.pi * i / seg; V.append((r2 * math.cos(a), r2 * math.sin(a), 0.5))
    F = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
    if cap:
        F.append(tuple(range(seg - 1, -1, -1)))
        if r2 > 0: F.append(tuple(range(seg, 2 * seg)))
    _TPL[k] = (np.array(V, float), F); return _TPL[k]

_CUBE = (np.array([(-.5, -.5, -.5), (.5, -.5, -.5), (.5, .5, -.5), (-.5, .5, -.5), (-.5, -.5, .5), (.5, -.5, .5), (.5, .5, .5), (-.5, .5, .5)], float),
         [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])

class Geo:
    """numpy-accumulated geometry (bmesh.ops is O(n) per call on huge meshes)"""
    def __init__(self):
        self.g = {}
    def _add(self, name, tpl, c, r, rot):
        V, F = tpl
        R = np.array(Euler(rot, 'XYZ').to_matrix())
        W_ = (V * np.array(r)) @ R.T + np.array(c)
        d = self.g.setdefault(name, [[], [], 0])
        d[0].append(W_); d[1].append([tuple(i + d[2] for i in f) for f in F]); d[2] += len(V)
    def ell(self, name, c, r, rot=(0, 0, 0), seg=12, ring=8):
        self._add(name, _sphere_tpl(seg, ring), c, r, rot)
    def cone(self, name, c, r, h, rot=(0, 0, 0), seg=6, r2=0.0, cap=True):
        self._add(name, _cone_tpl(seg, r2, cap), c, (r, r, h), rot)
    def box(self, name, c, s, rot=(0, 0, 0)):
        self._add(name, _CUBE, c, s, rot)
    def raw(self, name, verts, faces):
        d = self.g.setdefault(name, [[], [], 0])
        d[0].append(np.array(verts, float)); d[1].append([tuple(i + d[2] for i in f) for f in faces]); d[2] += len(verts)
    def emit(self, mats, smooth=True, prefix="W_"):
        out = {}
        for n, (vs, fs, cnt) in self.g.items():
            V = np.concatenate(vs); F = [f for chunk in fs for f in chunk]
            me = bpy.data.meshes.new(prefix + n); me.from_pydata(V.tolist(), [], F)
            for p in me.polygons: p.use_smooth = smooth
            ob = bpy.data.objects.new(prefix + n, me); bpy.context.scene.collection.objects.link(ob)
            ob.data.materials.append(mats[n]); out[n] = ob
        self.g = {}
        return out


def M(name, col, rough=0.6, spec=0.3, em=None):
    return mat(name, col, rough, spec, em)


def build_world(seed=3):
    rnd = random.Random(seed)
    sc = bpy.context.scene
    # ---------------------------------------------------------- terrain
    xs = np.arange(-10.0, 52.0, 0.2); ys = np.arange(-12.0, 16.0, 0.25)
    nx, ny = len(xs), len(ys)
    vx, vy = np.meshgrid(xs, ys, indexing='ij')
    vz = np.zeros_like(vx); pm = np.zeros_like(vx)
    for i, x in enumerate(xs):
        gx = g_base(x) + ditch(x); c = yc(x)
        for j, y in enumerate(ys):
            z = gx
            if y > 6.0: z += 0.07 * (y - 6.0) ** 2
            if y < -7.0: z += 0.05 * (-7.0 - y) ** 2
            vz[i, j] = z
            d = abs(y - c); pm[i, j] = 1 - sstep((d - 0.55) / 0.4)
    verts = np.stack([vx, vy, vz], -1).reshape(-1, 3)
    faces = []
    for i in range(nx - 1):
        for j in range(ny - 1):
            a = i * ny + j; faces.append((a, a + ny, a + ny + 1, a + 1))
    me = bpy.data.meshes.new("Terrain")
    me.from_pydata(verts.tolist(), [], faces)
    for p in me.polygons: p.use_smooth = True
    attr = me.attributes.new("pathmask", 'FLOAT', 'POINT'); attr.data.foreach_set("value", pm.reshape(-1))
    terr = bpy.data.objects.new("Terrain", me); sc.collection.objects.link(terr)
    tm = bpy.data.materials.new("TerrainMat"); tm.use_nodes = True
    nt = tm.node_tree; b = nt.nodes["Principled BSDF"]
    at = nt.nodes.new("ShaderNodeAttribute"); at.attribute_name = "pathmask"
    tc = nt.nodes.new("ShaderNodeTexCoord"); nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 1.6
    nz2 = nt.nodes.new("ShaderNodeTexNoise"); nz2.inputs["Scale"].default_value = 14
    g1 = nt.nodes.new("ShaderNodeMix"); g1.data_type = 'RGBA'
    g1.inputs[6].default_value = (0.20, 0.62, 0.10, 1); g1.inputs[7].default_value = (0.46, 0.78, 0.14, 1)
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"]); nt.links.new(tc.outputs["Object"], nz2.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], g1.inputs[0])
    d1 = nt.nodes.new("ShaderNodeMix"); d1.data_type = 'RGBA'
    d1.inputs[6].default_value = (0.66, 0.46, 0.24, 1); d1.inputs[7].default_value = (0.80, 0.60, 0.34, 1)
    nt.links.new(nz2.outputs["Fac"], d1.inputs[0])
    fin = nt.nodes.new("ShaderNodeMix"); fin.data_type = 'RGBA'
    nt.links.new(at.outputs["Fac"], fin.inputs[0]); nt.links.new(g1.outputs[2], fin.inputs[6]); nt.links.new(d1.outputs[2], fin.inputs[7])
    nt.links.new(fin.outputs[2], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.85
    bm_ = nt.nodes.new("ShaderNodeBump"); bm_.inputs["Strength"].default_value = 0.25; bm_.inputs["Distance"].default_value = 0.02
    nt.links.new(nz2.outputs["Fac"], bm_.inputs["Height"]); nt.links.new(bm_.outputs[0], b.inputs["Normal"])
    terr.data.materials.append(tm)

    # ---------------------------------------------------------- water
    wm = bpy.data.materials.new("Water"); wm.use_nodes = True
    wb = wm.node_tree.nodes["Principled BSDF"]
    wb.inputs["Base Color"].default_value = (0.10, 0.45, 0.80, 1); wb.inputs["Roughness"].default_value = 0.08
    wb.inputs["Emission Color"].default_value = (0.1, 0.4, 0.7, 1); wb.inputs["Emission Strength"].default_value = 0.25
    wn = wm.node_tree.nodes.new("ShaderNodeTexNoise"); wn.inputs["Scale"].default_value = 9; wn.inputs["Detail"].default_value = 4
    wbump = wm.node_tree.nodes.new("ShaderNodeBump"); wbump.inputs["Strength"].default_value = 0.15
    wm.node_tree.links.new(wn.outputs["Fac"], wbump.inputs["Height"]); wm.node_tree.links.new(wbump.outputs[0], wb.inputs["Normal"])
    bm = bmesh.new()
    wz = g_base(STREAM_X) - 1.12
    for a, b2 in ((STREAM_X - 3.0, STREAM_X + 3.0),):
        v = [bm.verts.new((a, -12, wz)), bm.verts.new((b2, -12, wz)), bm.verts.new((b2, 14, wz)), bm.verts.new((a, 14, wz))]
        bm.faces.new(v)
    wme = bpy.data.meshes.new("Water"); bm.to_mesh(wme); bm.free()
    wob = bpy.data.objects.new("Stream", wme); sc.collection.objects.link(wob); wob.data.materials.append(wm)

    G = Geo()
    mats = {}
    def mk(n, c, r=0.6, s=0.3, em=None): mats[n] = M(n, c, r, s, em); return n
    # ---------------------------------------------------------- bridge
    mk("wood", (0.55, 0.30, 0.12), 0.7); mk("wood_d", (0.32, 0.17, 0.07), 0.8); mk("rope", (0.80, 0.62, 0.32), 0.9); mk("rock", (0.50, 0.50, 0.55), 0.8)
    L = BRIDGE_X1 - BRIDGE_X0; n = 26
    by = lambda x: yc(x)
    for i in range(n):
        x0 = BRIDGE_X0 + L * i / n; x1 = BRIDGE_X0 + L * (i + 1) / n; xm = (x0 + x1) / 2
        z0, z1 = deck(x0), deck(x1)
        ang = -math.atan2(z1 - z0, x1 - x0)
        G.box("wood", (xm, 0, (z0 + z1) / 2 + 0.02), ((x1 - x0) * 0.93 / math.cos(ang) * 1.0, 1.25, 0.06), rot=(0, ang, 0))
    for sy in (-0.66, 0.66):
        for i in range(n):
            x0 = BRIDGE_X0 + L * i / n; x1 = BRIDGE_X0 + L * (i + 1) / n; xm = (x0 + x1) / 2
            z0, z1 = deck(x0), deck(x1); ang = -math.atan2(z1 - z0, x1 - x0)
            G.box("wood_d", (xm, sy, (z0 + z1) / 2 - 0.05), ((x1 - x0) * 1.05 / math.cos(ang), 0.07, 0.14), rot=(0, ang, 0))
            if i % 3 == 0:
                G.cone("wood_d", (xm, sy, deck(xm) + 0.22), 0.045, 0.44, seg=8)
            # rope rail
            G.ell("rope", (xm, sy, deck(xm) + 0.40), ((x1 - x0) * 0.6 / math.cos(ang), 0.022, 0.022), rot=(0, ang, 0), seg=8, ring=5)
    for k in range(14):  # rocks along banks
        x = STREAM_X + rnd.choice([-1, 1]) * rnd.uniform(1.3, 2.6); y = rnd.choice([-1, 1]) * rnd.uniform(0.9, 2.6)
        r = rnd.uniform(0.12, 0.3)
        G.ell("rock", (x, y, terrain_z(x, y) + r * 0.3), (r * 1.3, r, r * 0.8), rot=(0, 0, rnd.uniform(0, 3)), seg=10, ring=7)
    # ---------------------------------------------------------- cottage (pink, round window, tile roof)
    mk("wall", (0.95, 0.60, 0.62), 0.8); mk("roof", (0.55, 0.20, 0.14), 0.7); mk("trim", (0.95, 0.90, 0.78), 0.6)
    mk("glass", (0.45, 0.65, 0.85), 0.1, 0.8, em=(0.25, 0.4, 0.6)); mk("door", (0.35, 0.18, 0.10), 0.7); mk("vine", (0.15, 0.50, 0.12), 0.7)
    cx, cy = -3.0, 6.0
    G.box("wall", (cx, cy, 1.0), (4.0, 2.6, 2.0))
    hw, hl, hz0, hz1, ov = 1.75, 2.35, 2.0, 3.05, 0.25
    G.raw("roof", [(cx - hl - ov, cy - hw, hz0), (cx + hl + ov, cy - hw, hz0), (cx + hl + ov, cy + hw, hz0), (cx - hl - ov, cy + hw, hz0), (cx - hl - ov, cy, hz1), (cx + hl + ov, cy, hz1)],
          [(0, 1, 5, 4), (3, 4, 5, 2), (0, 4, 3), (1, 2, 5), (0, 3, 2, 1)])
    G.box("trim", (cx + 1.5, cy + 0.3, 3.0), (0.4, 0.4, 0.9))                       # chimney
    G.ell("glass", (cx - 1.0, cy - 1.32, 1.25), (0.5, 0.05, 0.62), seg=20, ring=12)
    G.ell("trim", (cx - 1.0, cy - 1.30, 1.25), (0.60, 0.045, 0.72), seg=20, ring=12)
    G.box("door", (cx + 1.0, cy - 1.31, 0.8), (0.8, 0.08, 1.5))
    for i in range(18):
        G.ell("vine", (cx - 1.9 + rnd.uniform(0, 0.4), cy - 1.35, 0.3 + i * 0.1), (0.14, 0.05, 0.1), seg=8, ring=5)
    # ---------------------------------------------------------- fence
    for x in np.arange(2.0, 13.0, 0.8):
        y = 3.3 + 0.1 * math.sin(x)
        G.box("wood", (x, y, terrain_z(x, y) + 0.3), (0.09, 0.09, 0.6))
    for z in (0.22, 0.46):
        for x in np.arange(2.0, 12.6, 0.8):
            y = 3.3 + 0.1 * math.sin(x)
            G.box("wood", (x + 0.4, y, terrain_z(x + 0.4, y) + z), (0.82, 0.04, 0.07))
    # ---------------------------------------------------------- trees
    mk("trunk", (0.38, 0.22, 0.10), 0.8); mk("leaf1", (0.25, 0.62, 0.12), 0.7); mk("leaf2", (0.45, 0.75, 0.15), 0.7); mk("leaf3", (0.12, 0.48, 0.15), 0.7)
    tpos = [(-8, 5), (2.5, 8.5), (7, 6.5), (11, 9), (14, 5.5), (22, 7), (26, 9), (30, 6), (-6, -9), (4, -9), (13, -10), (22, -9), (30, -10), (36, 3), (34, -5)]
    for (x, y) in tpos:
        h = rnd.uniform(2.6, 4.0); z0 = terrain_z(x, y)
        G.cone("trunk", (x, y, z0 + h * 0.3), 0.16, h * 0.6, seg=8, r2=0.1)
        for k in range(4):
            r = rnd.uniform(0.9, 1.5)
            G.ell(rnd.choice(["leaf1", "leaf2", "leaf3"]), (x + rnd.uniform(-0.7, 0.7), y + rnd.uniform(-0.7, 0.7), z0 + h * 0.7 + rnd.uniform(0, 1.2)), (r, r, r * 0.85), seg=12, ring=8)
    # distant hills
    mk("hill1", (0.55, 0.78, 0.45), 0.9); mk("hill2", (0.45, 0.70, 0.55), 0.9)
    for k in range(9):
        x = -20 + k * 11 + rnd.uniform(-3, 3)
        G.ell(rnd.choice(["hill1", "hill2"]), (x, 42, -2), (rnd.uniform(12, 18), 12, rnd.uniform(7, 11)), seg=16, ring=10)
        G.ell(rnd.choice(["hill1", "hill2"]), (x + 5, -40, -2), (rnd.uniform(12, 18), 12, rnd.uniform(6, 9)), seg=16, ring=10)
    # ---------------------------------------------------------- flowers & grass tufts
    cols = {"fl_pink": (0.95, 0.35, 0.60), "fl_white": (0.98, 0.95, 0.92), "fl_yellow": (1.0, 0.80, 0.10), "fl_purple": (0.60, 0.35, 0.90), "fl_orange": (1.0, 0.45, 0.12)}
    for k, c in cols.items(): mk(k, c, 0.55)
    mk("stem", (0.15, 0.50, 0.10), 0.7); mk("flc", (1.0, 0.85, 0.2), 0.6); mk("tuft1", (0.30, 0.70, 0.12), 0.7); mk("tuft2", (0.16, 0.50, 0.08), 0.7)
    for i in range(1500):
        x = rnd.uniform(-6, 40); d = rnd.choice([-1, 1]) * rnd.uniform(0.85, 4.5)
        if STREAM_X - 2.2 < x < STREAM_X + 2.2 and abs(d) < 3: continue
        y = yc(x) + d; z = terrain_z(x, y)
        if d < -2.3 and rnd.random() < 0.9: continue
        if abs(x - PILE_X) < 1.3 and -2.2 < d < 0.2: continue
        h = rnd.uniform(0.12, 0.38) 
        c = rnd.choice(list(cols))
        G.cone("stem", (x, y, z + h / 2), 0.012, h, seg=4, r2=0.008)
        rr = rnd.uniform(0.028, 0.045)
        for p in range(5):
            a = p / 5 * 2 * math.pi
            G.ell(c, (x + rr * 0.9 * math.cos(a), y + rr * 0.9 * math.sin(a), z + h), (rr * 0.8, rr * 0.8, rr * 0.35), rot=(0, 0, a), seg=8, ring=5)
        G.ell("flc", (x, y, z + h + 0.01), (rr * 0.5, rr * 0.5, rr * 0.4), seg=8, ring=5)
        if rnd.random() < 0.8:
            for q in range(2):
                a = rnd.uniform(0, 6.28)
                G.cone("tuft1", (x + 0.05 * math.cos(a), y + 0.05 * math.sin(a), z + 0.07), 0.015, 0.1, rot=(0.5 * math.cos(a), 0.5 * math.sin(a), 0), seg=3)
    for i in range(7000):
        x = rnd.uniform(-8, 44); y = rnd.uniform(-5.5, 9)
        if STREAM_X - 1.4 < x < STREAM_X + 1.4: continue
        if abs(y - yc(x)) < 0.6: continue
        z = terrain_z(x, y); h = rnd.uniform(0.08, 0.2)
        a = rnd.uniform(0, 6.28)
        G.cone("tuft1" if rnd.random() < 0.5 else "tuft2", (x, y, z + h * 0.45), 0.012, h * 0.7, rot=(0.35 * math.cos(a), 0.35 * math.sin(a), 0), seg=3)
    # ---------------------------------------------------------- leaf pile (static base)
    mk("lf1", (0.90, 0.35, 0.05), 0.6); mk("lf2", (1.0, 0.65, 0.05), 0.6); mk("lf3", (0.75, 0.18, 0.04), 0.6); mk("lf4", (0.90, 0.78, 0.15), 0.6)
    py = yc(PILE_X) - 0.75
    pz = terrain_z(PILE_X, py)
    for i in range(650):
        r = 0.95 * math.sqrt(rnd.random()); a = rnd.uniform(0, 6.28)
        x = PILE_X + 1.2 * r * math.cos(a) ; y = py + 0.9 * r * math.sin(a)
        zz = terrain_z(x, y) + 0.16 * (1 - r * r) + rnd.uniform(0, 0.03) + 0.01
        G.ell(rnd.choice(["lf1", "lf2", "lf3", "lf4"]), (x, y, zz), (0.07, 0.045, 0.006), rot=(rnd.uniform(-0.4, 0.4), rnd.uniform(-0.4, 0.4), rnd.uniform(0, 6.28)), seg=8, ring=4)
    G.ell("lf3", (PILE_X, py, pz + 0.03), (1.15, 0.85, 0.07), seg=20, ring=8)   # leaf bed
    # fallen leaves scattered around
    for i in range(160):
        x = PILE_X + rnd.uniform(-3.5, 3.5); y = yc(x) + rnd.uniform(-3, 0.5)
        G.ell(rnd.choice(["lf1", "lf2", "lf3", "lf4"]), (x, y, terrain_z(x, y) + 0.012), (0.06, 0.04, 0.005), rot=(0, 0, rnd.uniform(0, 6.28)), seg=8, ring=4)
    G.emit(mats)

    # ---------------------------------------------------------- lighting + sky
    w = bpy.data.worlds.new("Sky"); w.use_nodes = True; sc.world = w
    nt = w.node_tree; nt.nodes.clear()
    sky = nt.nodes.new("ShaderNodeTexSky"); sky.sky_type = 'SINGLE_SCATTERING'
    sky.sun_elevation = math.radians(38); sky.sun_rotation = math.radians(210); sky.sun_disc = False
    sky.air_density = 1.2
    bg = nt.nodes.new("ShaderNodeBackground"); bg.inputs["Strength"].default_value = 0.45
    out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(sky.outputs[0], bg.inputs[0]); nt.links.new(bg.outputs[0], out.inputs[0])
    ld = bpy.data.lights.new("Sun", 'SUN'); ld.energy = 2.6; ld.angle = math.radians(4); ld.color = (1.0, 0.93, 0.80)
    lo = bpy.data.objects.new("Sun", ld); sc.collection.objects.link(lo)
    dirv = Vector((0.45, 0.55, -0.75))    # travel direction of light: from front-left, behind camera
    lo.rotation_euler = dirv.to_track_quat('-Z', 'Y').to_euler()
    return dict(terrain=terr, water=wob, pile=(PILE_X, py, pz))


def make_leaf_mesh():
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=4, radius=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Diagonal((0.075, 0.048, 0.007, 1)), verts=bm.verts)
    me = bpy.data.meshes.new("LeafMesh"); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    return me
