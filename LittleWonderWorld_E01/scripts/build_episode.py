"""Little Wonder World E01 - build scene, choreograph, bake keyframes, save .blend
usage: python3 -I build_episode.py <out.blend> [--still F --out img.png --res 540]
Everything is a pure function of the frame number (apply_frame), then baked into real keyframes.
"""
import sys, os, math, random, bisect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector, Quaternion, Matrix, Euler
import lww_chars as C
import lww_world as W
from lww_world import sstep, yc, ground, slope, PILE_X, BASKET_X

FPS, NF = 30, 900
R_BALL = 0.17
rnd_ = random.Random(11)

# ----------------------------------------------------------------- tiny math helpers
def clamp(v, a, b): return max(a, min(b, v))
def lerp(a, b, t): return a + (b - a) * t
def seg(f, a, b): return clamp((f - a) / float(b - a), 0.0, 1.0)
def es(f, a, b): return sstep(seg(f, a, b))
def Rz(a): return Matrix.Rotation(a, 3, 'Z')

def mono(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; n = len(xs)
    d = [(ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]) for i in range(n - 1)]
    m = [d[0]] + [(d[i - 1] + d[i]) / 2 if d[i - 1] * d[i] > 0 else 0.0 for i in range(1, n - 1)] + [d[-1]]
    for i in range(n - 1):
        if d[i] == 0: m[i] = m[i + 1] = 0.0
        else:
            a, b = m[i] / d[i], m[i + 1] / d[i]; s = a * a + b * b
            if s > 9: t = 3 / math.sqrt(s); m[i] = t * a * d[i]; m[i + 1] = t * b * d[i]
    def f(x):
        if x <= xs[0]: return ys[0]
        if x >= xs[-1]: return ys[-1]
        i = bisect.bisect_right(xs, x) - 1; h = xs[i + 1] - xs[i]; t = (x - xs[i]) / h
        t2, t3 = t * t, t * t * t
        return (2 * t3 - 3 * t2 + 1) * ys[i] + (t3 - 2 * t2 + t) * h * m[i] + (-2 * t3 + 3 * t2) * ys[i + 1] + (t3 - t2) * h * m[i + 1]
    return f

def track(pts):
    """smoothstep-eased piecewise track [(f,v),...]"""
    fs = [p[0] for p in pts]
    def f(x):
        if x <= fs[0]: return pts[0][1]
        if x >= fs[-1]: return pts[-1][1]
        i = bisect.bisect_right(fs, x) - 1
        t = sstep((x - fs[i]) / float(fs[i + 1] - fs[i]))
        return lerp(pts[i][1], pts[i + 1][1], t)
    return f

def integ(vkeys, x0):
    v = track(vkeys); xs = [x0]
    for f in range(1, NF + 40):
        xs.append(xs[-1] + 0.5 * (v(f - 1) + v(f)) / FPS)
    return lambda f: xs[int(clamp(f, 0, NF + 39))] if abs(f - round(f)) < 1e-6 else lerp(xs[int(f)], xs[int(f) + 1], f - int(f))

# ----------------------------------------------------------------- choreography: world tracks
PY = yc(PILE_X) - 0.75           # leaf pile y
BY = yc(BASKET_X)                # basket y
# Milo longitudinal speed -> x
def _milo_speed_scale():
    V = 2.15
    for _ in range(30):
        x = integ([(0, 0), (283, 0), (300, V), (620, V), (642, 0)], -0.6)(642)
        V *= (23.45 - (-0.6)) / (x + 0.6)
    return V
VM = _milo_speed_scale()
V2 = 2.1
milo_x = integ([(0, 0), (283, 0), (300, VM), (620, VM), (642, 0), (690, 0), (704, V2), (733, V2), (751, 0), (795, 0), (802, -1.5), (816, -1.5), (824, 0)], -0.6)
def _fix():
    global V2
    for _ in range(30):
        mx = integ([(0, 0), (283, 0), (300, VM), (620, VM), (642, 0), (690, 0), (704, V2), (733, V2), (751, 0)], -0.6)(751)
        V2 *= (26.55 - 23.45) / (mx - 23.45 + 1e-6) if mx > 23.5 else 1.0
        globals()['milo_x'] = integ([(0, 0), (283, 0), (300, VM), (620, VM), (642, 0), (690, 0), (704, V2), (733, V2), (751, 0), (795, 0), (802, -1.5), (816, -1.5), (824, 0)], -0.6)
_fix()

def bridge_w(x): return sstep((x - 12.0) / 2.5) * (1 - sstep((x - 20.0) / 2.0))

def milo_y(f):
    x = milo_x(f)
    if f < 283: base = lerp(-0.05, -0.05, 0)
    else: base = -0.25
    y0 = lerp(-0.05, -0.25, es(f, 255, 300))
    y = yc(x) + y0 * (1 - bridge_w(x))
    k = sstep((x - 20.5) / 3.0)
    y = lerp(y, PY - 0.05, k) if f < 704 else y
    if f >= 690:
        wp = track([(690, PY - 0.05), (704, PY - 0.5), (718, PY - 0.95), (733, PY - 0.9), (751, BY - 0.35), (800, BY - 0.35), (822, PY + 0.02)])
        y = wp(f)
    return y

# Pip hops
HOP_P, HOP_F, HOP_D, HOP_T0 = 14, 10, 1.0, 292
PIP_X0 = 0.55
def _hops():
    xs = [PIP_X0]; k = 0
    while xs[-1] + HOP_D < PILE_X - 0.95: xs.append(xs[-1] + HOP_D)
    return xs
HOPX = _hops()
NHOP = len(HOPX) - 1
F_TUMBLE = HOP_T0 + NHOP * HOP_P           # frame where final slip hop begins
def pip_hop_state(f):
    """returns (x, hop_u in 0..1 flight else None, stance_t)"""
    if f < HOP_T0: return PIP_X0, None, 0
    k = int((f - HOP_T0) // HOP_P)
    if k >= NHOP: return HOPX[-1], None, 0
    u = (f - HOP_T0) - k * HOP_P
    if u < HOP_F:
        w = u / HOP_F
        return lerp(HOPX[k], HOPX[k + 1], w), w, 0
    return HOPX[k + 1], None, u - HOP_F

def pip_y(f):
    x = pip_hop_state(f)[0] if f < F_TUMBLE else HOPX[-1]
    if f < 40: return 0.38
    y0 = lerp(0.38, 0.42, es(f, 255, 300))
    y = yc(x) + y0 * (1 - bridge_w(x))
    k = sstep((x - 20.5) / 3.0)
    y = lerp(y, PY - 0.1, k)
    return y

# ball path (x along path), ball waypoints
ball_x = mono([(0, -0.20), (14, -0.20), (30, -0.0), (46, 0.35), (80, 1.25), (119, 2.4), (160, 4.4), (200, 6.6), (239, 8.7), (299, 11.2),
               (380, 13.2), (449, 14.5), (470, 15.4), (500, 17.5), (545, 19.9), (600, 23.2), (650, 25.6), (700, 26.8), (752, BASKET_X - 0.19)])
def ball_pos_raw(f):
    x = ball_x(f)
    y = yc(x) if x > 0.35 else 0.0 + (yc(x) if x > 0 else 0)
    z = ground(x, y) + R_BALL
    if f < 46: z += 0
    # bridge entry / exit bounces
    for fb, hb in ((458, 0.20), (548, 0.14)):
        if fb <= f <= fb + 16: z += hb * math.sin(math.pi * (f - fb) / 16.0)
    # basket lip
    xb = BASKET_X - 0.25
    if x > xb: z = max(z, ground(x, y) + R_BALL + 0.05 * sstep((x - xb) / 0.06))
    return Vector((x, y, z))

# ----------------------------------------------------------------- characters: IK/gait
A_L, B_L = 0.125, 0.125
def leg_ik(foot_f, foot_up, hip_z):
    """planar IK. returns (thigh_rx, shin_rx, foot_rx_world_compensation)"""
    tz = (0.05 + foot_up) - hip_z
    d = math.hypot(foot_f, tz); d = clamp(d, 0.03, A_L + B_L - 1e-3)
    phi = math.atan2(foot_f, -tz)
    al = math.acos(clamp((A_L ** 2 + d * d - B_L ** 2) / (2 * A_L * d), -1, 1))
    ga = math.acos(clamp((A_L ** 2 + B_L ** 2 - d * d) / (2 * A_L * B_L), -1, 1))
    pt = phi + al; ps = pt - (math.pi - ga)
    return -pt, -(ps - pt), ps   # rot_x thigh, rot_x shin(rel), shin world forward angle

def gait(phase, duty, S, lift):
    p = phase % 1.0
    if p < duty:
        u = p / duty; return S / 2 - S * u, 0.0
    u = (p - duty) / (1 - duty)
    return -S / 2 + S * sstep(u) , lift * math.sin(math.pi * u)

# ----------------------------------------------------------------- scene objects
S = {}
def setup():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 0, NF - 1
    sc.render.fps = FPS
    W.build_world()
    S['milo'] = C.build_milo("Milo"); S['pip'] = C.build_pip("Pip")
    S['ball'] = C.build_ball(R_BALL); S['basket'] = C.build_basket()
    S['basket'].rotation_mode = 'QUATERNION'; S['ball'].rotation_mode = 'QUATERNION'
    # flying leaves (each has its own mesh copy + one of the 4 leaf materials)
    lm = W.make_leaf_mesh()
    lmats = [bpy.data.materials[n] for n in ("lf1", "lf2", "lf3", "lf4")]
    S['leaves'] = []
    for i in range(110):
        me = lm.copy(); me.materials.append(lmats[i % 4])
        ob = bpy.data.objects.new(f"FlyLeaf{i:03d}", me); sc.collection.objects.link(ob)
        ob.rotation_mode = 'QUATERNION'; S['leaves'].append(ob)
    # camera
    cd = bpy.data.cameras.new("Cam"); cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = 36
    co = bpy.data.objects.new("Camera", cd); sc.collection.objects.link(co); sc.camera = co; S['cam'] = co
    # impact burst lines (high five)
    S['burst'] = []
    wm = C.mat("burst", (1, 1, 1), 0.5, 0.2, emission=(1, 1, 1))
    for i in range(5):
        me = bpy.data.meshes.new(f"Burst{i}")
        import bmesh
        bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.transform(bm, matrix=Matrix.Diagonal((0.012, 0.012, 0.09, 1)), verts=bm.verts)
        bm.to_mesh(me); bm.free(); ob = bpy.data.objects.new(f"Burst{i}", me); sc.collection.objects.link(ob)
        ob.data.materials.append(wm); ob.rotation_mode = 'XYZ'; S['burst'].append(ob)
    # render settings
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
    sc.cycles.samples = 16; sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    sc.cycles.max_bounces = 3; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 2
    sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.04
    sc.cycles.sample_clamp_indirect = 6.0
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, 100
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
    sc.view_settings.exposure = 0.0; sc.view_settings.gamma = 1.0
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'
    # shot markers
    for n, f in enumerate((0, 120, 240, 300, 450, 600, 750, 840)):
        sc.timeline_markers.new(f"Shot{n + 1}", frame=f)

# ----------------------------------------------------------------- leaves
LEAF_T = None
def leaf_state(i, f):
    r = random.Random(1000 + i)
    ang = r.uniform(0, 2 * math.pi); sp = r.uniform(0.6, 2.2); up = r.uniform(1.6, 3.6)
    ox, oy = r.uniform(-0.5, 0.5), r.uniform(-0.4, 0.4)
    spin = (r.uniform(-8, 8), r.uniform(-8, 8), r.uniform(-8, 8))
    t0 = F_TUMBLE + 15 + int(r.uniform(0, 4))
    base = Vector((PILE_X + ox, PY + oy, ground(PILE_X, PY) + 0.17))
    if f < t0:
        return base, Quaternion(Vector((r.random(), r.random(), r.random())).normalized(), r.uniform(0, 3)), False
    t = (f - t0) / FPS
    g = 7.0
    vx, vy = sp * math.cos(ang), sp * math.sin(ang)
    # air drag so leaves flutter
    k = 1.6
    px = base.x + vx * (1 - math.exp(-k * t)) / k; py = base.y + vy * (1 - math.exp(-k * t)) / k
    vz0 = up
    # light fall speed (terminal 0.8 m/s)
    tv = 0.9; kz = g / tv
    pz = base.z + (vz0 + tv) * (1 - math.exp(-kz * t)) / kz - tv * t
    gz = ground(px, py) + 0.03 + (0.12 if (px - PILE_X) ** 2 / 1.3 + (py - PY) ** 2 / 0.9 < 1 else 0)
    landed = pz <= gz
    if landed:
        # find landing time roughly; freeze
        tt = t
        while tt > 0:
            tt -= 0.02
            px = base.x + vx * (1 - math.exp(-k * tt)) / k; py = base.y + vy * (1 - math.exp(-k * tt)) / k
            pz = base.z + (vz0 + tv) * (1 - math.exp(-kz * tt)) / kz - tv * tt
            gz = ground(px, py) + 0.03 + (0.1 if (px - PILE_X) ** 2 / 1.3 + (py - PY) ** 2 / 0.9 < 1 else 0)
            if pz > gz: break
        pz = gz; t = max(tt, 0)
    flut = 0.5 * math.sin(t * 9 + i)
    q = (Quaternion((0, 0, 1), spin[2] * t) @ Quaternion((1, 0, 0), spin[0] * t * 0.6 + flut) @ Quaternion((0, 1, 0), spin[1] * t * 0.6))
    return Vector((px, py, pz)), q, True

# ----------------------------------------------------------------- characters: pose
def blink_amount(f, seed):
    r = random.Random(seed)
    b = 0.0
    t = r.randint(20, 60)
    while t < NF + 10:
        d = f - t
        if 0 <= d < 6: b = max(b, 1 - abs(d - 2.5) / 2.5 if d > 0 else 0)
        t += r.randint(75, 140)
    return clamp(b, 0, 1)

def look_angles(root_pos, root_yaw, root_pitch, eye_h, target):
    """angles (yaw about +Z positive towards character-left, pitch up positive) in the character frame"""
    rel = Rz(-root_yaw) @ (target - Vector((root_pos.x, root_pos.y, root_pos.z + eye_h)))
    yaw = math.atan2(rel.x, -rel.y); pit = math.atan2(rel.z, math.hypot(rel.x, rel.y))
    if rel.y > 0.0 and abs(yaw) > 1.5707:      # behind: clamp
        yaw = clamp(yaw, -1.2, 1.2)
    return yaw, pit

def set_look(p, target, blend=1.0, head_share=0.65, ylim=1.0):
    y, pt = look_angles(p['pos'], p['yaw'], 0, p['eye_h'], target)
    y = clamp(y - p.get('spine_yaw', 0), -2.0, 2.0)
    hy = clamp(y * head_share, -ylim, ylim); hp = clamp(pt * 0.5, -0.45, 0.5)
    ey = clamp(y - hy, -0.55, 0.55) * 1.0; ep = clamp(pt - hp, -0.4, 0.4)
    p['head_yaw'] = lerp(p['head_yaw'], hy, blend); p['head_up'] = lerp(p['head_up'], hp, blend)
    p['eye_yaw'] = lerp(p['eye_yaw'], ey, blend); p['eye_up'] = lerp(p['eye_up'], ep, blend)

def laugh(f, p, amp=1.0, rate=7.0):
    w = abs(math.sin(math.pi * f / rate))
    p['mouth'] = max(p['mouth'], (0.35 + 0.55 * w) * amp); p['squint'] = max(p['squint'], 0.65 * amp)
    if 'spine_pitch' in p: p['spine_pitch'] += 0.05 * math.sin(2 * math.pi * f / rate) * amp
    if 'pelvis_drop' in p: p['pelvis_drop'] += 0.006 * w * amp
    p['head_up'] += 0.08 * math.sin(2 * math.pi * f / (rate * 2))

def milo_params(f):
    p = dict(pos=Vector((milo_x(f), milo_y(f), 0)), yaw=math.radians(55), pitch=0.0, roll=0.0, pivot=(0, 0, 0.3),
             eye_h=0.68, pelvis_drop=0.0, spine_pitch=0.04, spine_yaw=0.0, head_yaw=0.0, head_up=0.0, eye_yaw=0.0, eye_up=0.0,
             squint=0.0, wide=1.0, mouth=0.0, mw=1.0, brow=0.0, blink=blink_amount(f, 5),
             L=[0.0, 0.05, 0.1], R=[0.0, 0.05, 0.1], gait_v=0.0, phase=0.0, lfoot=(0, 0), rfoot=(0, 0), bob=0.0, hip_sway=0.0)
    p['smile_w'] = 1.0
    x = p['pos'].x
    gz = ground(x, p['pos'].y); p['pos'].z = gz
    # ---------------- locomotion (shots 4-5 and later runs)
    vel = (milo_x(f + 1) - milo_x(f - 1)) * FPS / 2.0
    p['gait_v'] = vel
    # yaw schedule
    yaw = math.radians(55)
    yaw = lerp(yaw, math.radians(80), es(f, 120, 220))
    yaw = lerp(yaw, math.radians(40), es(f, 225, 245))
    yaw = lerp(yaw, math.radians(90), es(f, 282, 296))
    # shot 6/7 orientation
    yaw = lerp(yaw, math.radians(-60), es(f, 640, 656))     # turn to look at Pip (south-west... faces camera/pip)
    yaw = lerp(yaw, math.radians(90), es(f, 694, 704))
    yaw = lerp(yaw, math.radians(35), es(f, 750, 760))
    yaw = lerp(yaw, math.radians(-90), es(f, 794, 801)) if f >= 794 else yaw
    yaw = lerp(yaw, math.radians(-90), es(f, 800, 806)) if False else yaw
    p['yaw'] = yaw
    return p

def pose_dict_milo(f):
    p = milo_params(f)
    bp = ball_pos_raw(f) if f < 752 else ball_world(f)
    pipp = pip_params_light(f)
    # =================== shot 1 : roll the ball
    if f < 50:
        crouch = 0.085 * (1 - es(f, 22, 50))
        p['pelvis_drop'] = crouch; p['spine_pitch'] = 0.20 + 0.34 * (1 - es(f, 24, 50)) * (1 if f > 8 else 0.4)
        wind = es(f, 3, 11) * (1 - es(f, 11, 15))     # arms back
        thr = es(f, 11, 16) * (1 - es(f, 22, 40))     # arms forward / release
        a = 0.9 * (1 - wind) - 0.2 * wind + 0.5 * thr
        p['L'] = [a, 0.12, 0.55 * (1 - thr)]; p['R'] = [a, 0.12, 0.55 * (1 - thr)]
        p['mouth'] = 0.25; p['brow'] = 0.3
    if 44 <= f < 120:   # laughing together
        ls = es(f, 44, 52) * (1 - es(f, 96, 108))
        laugh(f, p, ls)
        p['L'] = [lerp(0.3, 0.1, es(f, 50, 70)), 0.15 + 0.25 * ls, 0.4]; p['R'] = [0.1, 0.15 + 0.25 * ls, 0.4]
    # looks
    if f < 14: set_look(p, bp)
    elif f < 40: set_look(p, bp)
    elif f < 62: set_look(p, pipp['head'])
    elif f < 84: set_look(p, pipp['head'])
    else: set_look(p, bp, es(f, 84, 94))
    # =================== shot 2: reaction
    if 100 <= f < 240:
        e = es(f, 100, 118)
        p['wide'] = 1 + 0.15 * e; p['mouth'] = max(p['mouth'] * (1 - e), 0.45 * e); p['brow'] = 0.9 * e
        up = e * (1 - es(f, 205, 238))
        p['L'] = [lerp(p['L'][0], 0.55, e), lerp(p['L'][1], 0.9, e), lerp(p['L'][2], 0.3, e)]
        p['R'] = [lerp(p['R'][0], 0.3, e), lerp(p['R'][1], 0.35, e), lerp(p['R'][2], 0.4, e)]
        p['spine_pitch'] = lerp(p['spine_pitch'], 0.0, e)
        p['squint'] = 0.0
        # arm wave: Milo reaches toward the ball, pulsing
        p['L'][0] += 0.15 * math.sin(f * 0.35)
    if 120 <= f < 300:
        set_look(p, bp, 1.0)
    # =================== shot 3: close-up "Oops!"
    if 240 <= f < 300:
        gasp = es(f, 244, 252) * (1 - es(f, 266, 276))
        p['mouth'] = 0.15 + 0.65 * gasp * (0.75 + 0.25 * math.sin(f * 1.1)) if 246 < f < 268 else 0.12
        p['mw'] = 0.55 if 246 < f < 268 else 1.0
        p['brow'] = 1.0; p['wide'] = 1.2
        reach = es(f, 244, 262) * (1 - es(f, 282, 296))
        p['L'] = [0.4 + 0.8 * reach, 0.45 + 0.35 * reach, 0.5 * (1 - reach) + 0.1]
        p['R'] = [0.25, 0.3, 0.4]
        p['L'][1] = 0.4 + 0.7 * reach
        look_t = Vector((milo_x(f) + 6, milo_y(f) - 0.4, 0.3))
        set_look(p, bp if f > 262 else Vector((milo_x(f) + 0.9, milo_y(f) - 3, 0.7)), 1.0)
        p['head_yaw'] = lerp(p['head_yaw'], 0.9, es(f, 266, 282))
        p['eye_yaw'] = lerp(p['eye_yaw'], 0.35, es(f, 266, 282)); p['eye_up'] = lerp(p['eye_up'], -0.2, es(f, 266, 282))
    # =================== run (300-640)
    run = es(f, 286, 304) * (1 - es(f, 628, 646))
    if run > 0.001 and f < 700:
        v = p['gait_v']
        S_, duty, lift = 0.40, 0.46, 0.06
        T_ph = v * duty / S_ / FPS
        # phase must be continuous: integrate by table
        ph = MILO_PHASE[int(f)]
        p['phase'] = ph
        fl, ul = gait(ph, duty, S_, lift); fr, ur = gait(ph + 0.5, duty, S_, lift)
        sc_ = clamp(v / 2.0, 0, 1)
        p['lfoot'] = (fl * sc_, ul * sc_); p['rfoot'] = (fr * sc_, ur * sc_)
        bob = abs(math.sin(math.pi * (ph * 2 + 0.2)))
        p['pelvis_drop'] = 0.03 - 0.025 * bob * sc_ * 1.0
        p['spine_pitch'] = 0.12 + 0.1 * sc_
        sw = math.sin(2 * math.pi * ph)
        p['L'] = [lerp(p['L'][0], 0.2 - 0.85 * sw * sc_, run), 0.2, lerp(p['L'][2], 1.3, run)]
        p['R'] = [lerp(p['R'][0], 0.2 + 0.85 * sw * sc_, run), 0.2, lerp(p['R'][2], 1.3, run)]
        p['hip_sway'] = 0.08 * sw * sc_
        p['spine_yaw'] = -0.12 * sw * sc_
        p['mouth'] = 0.3 + 0.1 * math.sin(f * 0.5); p['brow'] = 0.5; p['squint'] = 0.0; p['wide'] = 1.05
        p['roll'] = 0.05 * sw * sc_
        if f > 304:
            set_look(p, bp, 1.0)
    # =================== arrival at pile & check Pip (636-700)
    if 626 <= f < 706:
        e = es(f, 632, 650)
        p['spine_pitch'] = lerp(p['spine_pitch'], 0.55, e); p['pelvis_drop'] = lerp(p['pelvis_drop'], 0.07, e)
        p['L'] = [lerp(p['L'][0], 0.7, e), 0.15, lerp(p['L'][2], 0.25, e)]; p['R'] = [lerp(p['R'][0], 0.7, e), 0.15, lerp(p['R'][2], 0.25, e)]
        worry = e * (1 - es(f, 666, 676))
        p['brow'] = 0.9 * worry + 0.2; p['mouth'] = lerp(p['mouth'], 0.12 + 0.2 * worry, e)
        set_look(p, pipp['head'], 1.0)
        if f >= 668:
            ls = es(f, 668, 678) * (1 - es(f, 696, 706)); laugh(f, p, 0.9 * ls)
        p['wide'] = lerp(p['wide'], 1.0 + 0.1 * worry, e)
    # =================== dash around pile to basket (700-752)
    if 690 <= f < 760:
        v = p['gait_v']; sc_ = clamp(v / 2.0, 0, 1)
        ph = MILO_PHASE[int(f)]
        fl, ul = gait(ph, 0.46, 0.40, 0.06); fr, ur = gait(ph + 0.5, 0.46, 0.40, 0.06)
        p['lfoot'] = (fl * sc_, ul * sc_); p['rfoot'] = (fr * sc_, ur * sc_)
        sw = math.sin(2 * math.pi * ph)
        e = es(f, 700, 710) * (1 - es(f, 742, 754))
        p['L'] = [lerp(p['L'][0], 0.2 - 0.85 * sw * sc_, e), 0.2, lerp(p['L'][2], 1.3, e)]
        p['R'] = [lerp(p['R'][0], 0.2 + 0.85 * sw * sc_, e), 0.2, lerp(p['R'][2], 1.3, e)]
        p['pelvis_drop'] = lerp(p['pelvis_drop'], 0.03 - 0.025 * abs(math.sin(math.pi * (ph * 2 + 0.2))) * sc_, e)
        p['spine_pitch'] = lerp(p['spine_pitch'], 0.18, e); p['hip_sway'] = 0.08 * sw * sc_ * e
        p['mouth'] = lerp(p['mouth'], 0.3, e); p['squint'] = lerp(p['squint'], 0.0, e)
        set_look(p, bp, 1.0)
    # =================== shot 7 : catch with basket, help Pip
    if 750 <= f < 840:
        e = es(f, 750, 758)
        p['mouth'] = 0.25 * e + 0.1; p['brow'] = 0.3
        # reach & crouch to basket 756-776, carry 776-790, set down 790-804
        reach = es(f, 756, 772) * (1 - es(f, 800, 812))
        p['spine_pitch'] = lerp(0.1, 0.55, reach); p['pelvis_drop'] = 0.08 * reach
        p['L'] = [lerp(0.2, 1.05, reach), 0.12, lerp(0.3, 0.5, reach)]; p['R'] = [lerp(0.2, 1.05, reach), 0.12, lerp(0.3, 0.5, reach)]
        # standing feet idle
        set_look(p, bp if f < 774 else basket_world_pos(f) + Vector((0, 0, 0.1)), 1.0)
        if f >= 800:
            # help Pip: right hand (character-left? facing Pip)
            hp = es(f, 806, 822) * (1 - es(f, 836, 840) * 0)
            p['L'] = [lerp(p['L'][0], 0.75, hp), lerp(p['L'][1], 0.15, hp), lerp(p['L'][2], 0.2, hp)]
            p['R'] = [lerp(p['R'][0], 0.2, hp), 0.12, 0.3]
            p['spine_pitch'] = lerp(p['spine_pitch'], 0.4, hp) - 0.35 * es(f, 826, 840)
            p['pelvis_drop'] = lerp(p['pelvis_drop'], 0.05, hp) * (1 - es(f, 826, 840))
            set_look(p, pipp['head'], 1.0)
            p['mouth'] = 0.4 * hp + 0.1; p['brow'] = 0.3
        if f >= 826:
            laugh(f, p, 0.8 * es(f, 826, 838))
    if 794 <= f < 830:
        v = p['gait_v']; sc_ = clamp(abs(v) / 2.0, 0, 1)
        ph = MILO_PHASE[int(f)]
        fl, ul = gait(ph, 0.55, 0.30, 0.04); fr, ur = gait(ph + 0.5, 0.55, 0.30, 0.04)
        p['lfoot'] = (fl * sc_, ul * sc_); p['rfoot'] = (fr * sc_, ur * sc_)
    # =================== shot 8 : high five, "Yay!"
    if f >= 838:
        e = es(f, 838, 846)
        yaw8 = lerp(p['yaw'], math.radians(180), es(f, 828, 846))
        p['yaw'] = yaw8
        hf = es(f, 856, 866) * (1 - es(f, 893, 899))
        p['spine_pitch'] = 0.04; p['pelvis_drop'] = 0.0
        p['L'] = [lerp(0.2, 0.2, hf), lerp(0.1, 1.6, hf), lerp(0.1, 0.7, hf)]     # raised hand to the side (toward Pip)
        p['L'] = [0.15 + 0.1 * hf, 0.15 + 1.35 * hf, 0.2 + 0.2 * hf]
        p['R'] = [0.1, 0.12, 0.2]
        yay = es(f, 862, 868) * (1 - es(f, 886, 896))
        p['mouth'] = max(0.1, 0.9 * yay * (0.8 + 0.2 * math.sin(f * 0.9))); p['squint'] = 0.85 * es(f, 856, 866)
        p['brow'] = 0.5; p['wide'] = 1.0
        p['head_up'] = 0.1 * es(f, 858, 868); p['spine_pitch'] = -0.05 * es(f, 858, 870)
        p['pelvis_drop'] = 0.015 * math.sin(f * 0.8) * yay
        set_look(p, cam_pos(f), 1.0, 0.8) if f < 856 else None
        if f >= 856:
            p['head_yaw'] = lerp(p['head_yaw'], 0.0, 0.7); p['eye_yaw'] *= 0.5
    return p

MILO_PHASE = []

def pip_params_light(f):
    """cheap lookups for other characters' head positions"""
    s = pip_state(f)
    return dict(head=Vector((s['pos'].x, s['pos'].y, s['pos'].z + 0.5)) if not s.get('lying') else Vector((s['pos'].x, s['pos'].y, s['pos'].z + 0.35)))

def pip_state(f):
    """position/orientation of Pip at frame f"""
    x, w, st = pip_hop_state(f)
    y = pip_y(f)
    yaw = math.radians(-55)
    if f > 100: yaw = lerp(yaw, math.radians(-10), es(f, 120, 220))
    yaw = lerp(yaw, math.radians(40), es(f, 225, 245))
    yaw = lerp(yaw, math.radians(90), es(f, 284, 296))
    z = ground(x, y)
    s = dict(pos=Vector((x, y, z)), yaw=yaw, pitch=0.0, flight=w, stance=st, lying=False)
    if f >= F_TUMBLE:
        ft = f - F_TUMBLE
        # final slip hop: lands on the leaf pile and tumbles backwards
        xp = lerp(HOPX[-1], PILE_X - 0.1, sstep(seg(ft, 0, 12)))
        yp = lerp(y, PY, sstep(seg(ft, 0, 12)))
        zg = ground(xp, yp)
        arc = 0.22 * 4 * seg(ft, 0, 12) * (1 - seg(ft, 0, 12))
        s['pos'] = Vector((xp, yp, zg + arc)); s['flight'] = seg(ft, 0, 12) if ft < 12 else None
        s['yaw'] = lerp(math.radians(90), math.radians(15), es(f, F_TUMBLE + 10, F_TUMBLE + 34))
        s['lying'] = ft > 14
    return s

def pose_dict_pip(f):
    st = pip_state(f)
    p = dict(pos=st['pos'], yaw=st['yaw'], pitch=0.0, roll=0.0, pivot=(0, 0, 0.25), eye_h=0.5, spine_yaw=0.0,
             squash=0.0, head_yaw=0.0, head_up=0.0, eye_yaw=0.0, eye_up=0.0, squint=0.0, wide=1.0, mouth=0.0, mw=1.0, blink=blink_amount(f, 9),
             L=[0.0, 0.15, 0.0], R=[0.0, 0.15, 0.0], legs=[0.0, 0.0], body_pitch=0.0, tail_amp=0.25, tail_rate=0.11, lift=0.0, brow=0.0)
    pos = p['pos']
    bp = ball_pos_raw(f) if f < 752 else ball_world(f)
    mp = milo_head(f)
    # idle bounce & tail wag
    idle = math.sin(f * 0.21)
    p['squash'] = 0.02 * idle
    # ---------------- shot 1
    if f < 120:
        p['mouth'] = 0.35 if f > 4 else 0.2
        p['L'] = [0.5, 0.3, 0.3]; p['R'] = [0.5, 0.3, 0.3]
        tap = es(f, 40, 45) * (1 - es(f, 45, 53))
        p['L'] = [0.5 + 0.7 * tap, 0.3, 0.3 * (1 - tap)]; p['R'] = [0.5 + 0.7 * tap, 0.3, 0.3 * (1 - tap)]
        p['body_pitch'] = 0.18 * tap + 0.05 * es(f, 20, 40)
        p['tail_amp'] = 0.5
        set_look(dict_ref(p), bp)
        set_look(p, bp if f < 56 else mp, 1.0)
        if f >= 46:
            ls = es(f, 48, 56) * (1 - es(f, 100, 118)); laugh(f, p, ls, 6.0)
            p['lift'] = 0.0; p['squash'] += 0.04 * abs(math.sin(f * 0.45)) * ls
            p['tail_amp'] = 0.7
        if f >= 96:
            set_look(p, bp, es(f, 96, 106))
    # ---------------- shot 2/3: react
    if 120 <= f < 300:
        e = es(f, 112, 126)
        p['wide'] = 1 + 0.2 * e * (1 - es(f, 262, 272) * 0.5); p['mouth'] = lerp(p['mouth'], 0.5, e) * (1 - 0.0)
        up = e
        p['L'] = [0.4, 0.4 + 0.6 * e, 0.0]; p['R'] = [0.4, 0.4 + 0.6 * e, 0.0]
        hop = 0.07 * math.sin(math.pi * seg(f, 130, 146)) if 130 <= f < 146 else 0.0
        p['lift'] = hop
        set_look(p, bp, 1.0)
        if 240 <= f < 300:
            p['mouth'] = 0.35 if 252 <= f < 276 else 0.1
            p['mw'] = 0.6 if 252 <= f < 276 else 1.0
            blink_f = es(f, 262, 265) * (1 - es(f, 265, 270)); p['blink'] = max(p['blink'], blink_f)
            p['head_yaw'] = lerp(p['head_yaw'], 0.0, 0.0)
            set_look(p, bp, 1.0)
            if f >= 270: p['head_yaw'] = lerp(p['head_yaw'], -0.6, es(f, 270, 284))
    # ---------------- hopping
    if f >= 286 and f < F_TUMBLE + 20:
        w = st['flight']
        if w is not None and f < F_TUMBLE:
            ph = w
            p['lift'] = 0.24 * 4 * w * (1 - w)
            p['legs'] = [0.75 * math.sin(math.pi * w), 0.75 * math.sin(math.pi * w)]
            p['squash'] = -0.12 * math.sin(math.pi * w) + 0.04
            p['body_pitch'] = 0.18 + 0.12 * math.sin(math.pi * w)
            p['L'] = [0.1, 0.9 + 0.5 * math.sin(math.pi * w), 0.0]; p['R'] = [0.1, 0.9 + 0.5 * math.sin(math.pi * w), 0.0]
            p['pos'] = Vector((pos.x, pos.y, pos.z))
        elif f < F_TUMBLE:
            u = st['stance']
            sq = math.sin(math.pi * clamp(u / 4.0, 0, 1))
            p['squash'] = 0.22 * sq; p['body_pitch'] = 0.2 * (1 - sq)
            p['legs'] = [-0.45 * sq, -0.45 * sq]
            p['L'] = [0.2, 0.5, 0.0]; p['R'] = [0.2, 0.5, 0.0]
        p['mouth'] = lerp(0.45, 0.2, 0.5) + 0.1 * math.sin(f * 0.5); p['wide'] = 1.05
        p['tail_amp'] = 0.5; p['tail_rate'] = 0.3
        set_look(p, bp, 1.0, 0.7)
    # ---------------- tumble (leaf pile)
    if f >= F_TUMBLE:
        ft = f - F_TUMBLE
        if ft < 14:
            w = ft / 12.0
            p['legs'] = [0.6 * math.sin(math.pi * clamp(w, 0, 1)), 0.2]; p['squash'] = -0.1 * math.sin(math.pi * clamp(w, 0, 1))
            p['L'] = [0.3, 1.2, 0.0]; p['R'] = [0.3, 1.2, 0.0]; p['body_pitch'] = 0.2
            p['wide'] = 1.25; p['mouth'] = 0.5; p['mw'] = 0.7
        # slip + fall backwards
        fall = es(f, F_TUMBLE + 9, F_TUMBLE + 30)
        bounce = 0.06 * math.sin(math.pi * es(f, F_TUMBLE + 30, F_TUMBLE + 42)) * (1 - es(f, F_TUMBLE + 42, F_TUMBLE + 48))
        p['pitch'] = -(1.30 * fall - 0.10 * es(f, F_TUMBLE + 30, F_TUMBLE + 44)) + 0.0
        p['body_pitch'] = lerp(p['body_pitch'], -0.15, fall)
        p['legs'] = [lerp(p['legs'][0], -1.0, fall) + 0.12 * math.sin(f * 0.55) * fall, lerp(p['legs'][1], -0.9, fall) - 0.12 * math.sin(f * 0.55) * fall]
        p['L'] = [lerp(p['L'][0], 0.2, fall), lerp(p['L'][1], 1.3, fall), 0.0]; p['R'] = [lerp(p['R'][0], 0.2, fall), lerp(p['R'][1], 1.3, fall), 0.0]
        # centre of body sits in the leaves
        pos = st['pos']
        zl = ground(pos.x, pos.y) + 0.26
        p['pos'] = Vector((pos.x, pos.y, lerp(pos.z, zl - 0.25, fall) + bounce))
        p['wide'] = 1.0 + 0.2 * (1 - fall)
        # laughing in the leaves
        ls = es(f, F_TUMBLE + 30, F_TUMBLE + 44)
        if f > F_TUMBLE + 30:
            laugh(f, p, ls, 6.5); p['mouth'] = max(p['mouth'], 0.5 * ls)
            p['squash'] += 0.04 * abs(math.sin(f * 0.5)) * ls
            p['tail_amp'] = 0.8; p['tail_rate'] = 0.5
            p['L'] = [0.3 + 0.2 * math.sin(f * 0.5), 1.0, 0.0]; p['R'] = [0.3 - 0.2 * math.sin(f * 0.5), 1.0, 0.0]
        if f <= F_TUMBLE + 30:
            set_look(p, bp, 1.0)
        else:
            set_look(p, milo_head(f), 1.0)
    # ---------------- shots 7/8
    if f >= 750:
        pos = Vector((PILE_X, PY, ground(PILE_X, PY)))
        up = es(f, 818, 838)
        seat = -(1.30 - 0.10)
        p['pitch'] = lerp(-1.20, 0.0, up) + 0.04 * math.sin(f * 0.3) * (1 - up)
        yaw = math.radians(15)
        yaw = lerp(yaw, math.radians(-60 if False else 180), es(f, 834, 850))      # Pip faces the shot-8 camera (+Y side)
        p['yaw'] = lerp(math.radians(15), math.radians(0), es(f, 780, 800)) if f < 834 else yaw
        p['yaw'] = lerp(p['yaw'], math.radians(180), es(f, 834, 850)) if f >= 834 else lerp(math.radians(15), math.radians(10), 1)
        zl = ground(pos.x, pos.y) + lerp(0.26 - 0.25, 0.0, up) + lerp(0.0, 0.0, up)
        p['pos'] = Vector((pos.x + lerp(0, 0, up), pos.y, zl + lerp(0.0, 0.0, up)))
        lay = 1 - up
        p['legs'] = [lerp(-1.0, 0.0, up) + 0.1 * math.sin(f * 0.5) * lay, lerp(-0.9, 0.0, up) - 0.1 * math.sin(f * 0.5) * lay]
        p['body_pitch'] = lerp(-0.15, 0.0, up)
        p['tail_amp'] = 0.7; p['tail_rate'] = 0.35
        giggle = 1 - es(f, 800, 812)
        laugh(f, p, 0.9 * giggle, 6.5)
        p['L'] = [0.3, 1.0 * lay + 0.2, 0.0]; p['R'] = [0.3, 1.0 * lay + 0.2, 0.0]
        # reaching up for Milo's hand
        rch = es(f, 806, 818) * (1 - es(f, 836, 842))
        p['R'] = [lerp(p['R'][0], 0.8, rch), lerp(p['R'][1], 0.3, rch), 0.0]
        p['mouth'] = max(p['mouth'], 0.35 * es(f, 806, 820))
        set_look(p, milo_head(f), 1.0, 0.7) if f < 840 else None
        p['squash'] = 0.04 * math.sin(f * 0.4) * lay
        if f >= 836:
            hf = es(f, 856, 866) * (1 - es(f, 893, 899))
            p['L'] = [0.2, 0.2, 0.0]
            p['R'] = [0.2 + 0.0 * hf, 0.2 + 1.7 * hf, 0.0]
            yay = es(f, 862, 868) * (1 - es(f, 886, 896))
            p['mouth'] = max(0.15, 0.95 * yay * (0.8 + 0.2 * math.sin(f * 0.9))); p['squint'] = 0.8 * es(f, 858, 866)
            p['squash'] = 0.05 * math.sin(f * 0.8) * yay
            p['head_yaw'] *= 0.5; p['lift'] = 0.03 * abs(math.sin(f * 0.7)) * yay
            p['tail_amp'] = 0.9; p['tail_rate'] = 0.45
            set_look(p, cam_pos(f), 1.0, 0.8) if f < 856 else None
    return p

def dict_ref(p): return p

def milo_head(f):
    x, y = milo_x(f), milo_y(f)
    return Vector((x, y, ground(x, y) + 0.62))

# ----------------------------------------------------------------- ball, basket
BALL_Q = []
BASKET = {}
def basket_lying_pos(): return Vector((BASKET_X, BY, ground(BASKET_X, BY) + 0.22))
def basket_lying_q(): return Quaternion((0, 1, 0), -math.pi / 2)   # opening toward -X

def milo_root_xform(f):
    pr = milo_params(f)
    return Vector((milo_x(f), milo_y(f), ground(milo_x(f), milo_y(f)))), pr['yaw']

def basket_world(f):
    """returns (loc, quat)"""
    lp, lq = basket_lying_pos(), basket_lying_q()
    f_pick, f_up, f_down, f_set = 764, 782, 794, 806
    if f < f_pick: return lp, lq
    mp, myaw = milo_root_xform(f_pick)
    fwd = Rz(myaw) @ Vector((0, -1, 0))
    carry = mp + fwd * 0.36 + Vector((0, 0, 0.20))
    carryq = Quaternion((0, 0, 1), myaw)
    # set down beside Milo (to his left = toward east ... ) on the ground, upright
    side = Rz(myaw) @ Vector((1, 0, 0))
    down = mp + fwd * 0.45 + side * 0.0 + Vector((0, 0, 0)); down.z = ground(down.x, down.y)
    downq = Quaternion((0, 0, 1), myaw + 0.3)
    if f < f_up:
        t = sstep(seg(f, f_pick, f_up)); loc = lp.lerp(carry, t); loc.z += 0.10 * math.sin(math.pi * t)
        return loc, lq.slerp(carryq, t)
    if f < f_down: return carry, carryq
    t = sstep(seg(f, f_down, f_set)); loc = carry.lerp(down, t); loc.z += 0.06 * math.sin(math.pi * t)
    return loc, carryq.slerp(downq, t)

def basket_world_pos(f): return basket_world(f)[0]

def ball_world(f):
    loc, q = basket_world(f)
    return loc + (q @ Vector((0, 0, 0.19)))

def cam_pos(f): return CAM_TRACK(f)[0]

# ----------------------------------------------------------------- cameras
def lookat(pos, tgt, roll=0.0):
    d = (tgt - pos).normalized()
    q = d.to_track_quat('-Z', 'Y')
    if roll: q = q @ Quaternion((0, 0, 1), roll)
    return q

def CAM_TRACK(f):
    """returns (position, target, lens, roll)"""
    if f < 120:    # S1 wide eye-level, slow dolly in
        t = f / 119.0
        pos = Vector((lerp(0.30, 0.10, t), lerp(-2.9, -2.4, t), lerp(0.40, 0.38, t)))
        tg = Vector((lerp(-0.05, 0.0, t), 0.0, lerp(0.40, 0.38, t)))
        return pos, tg, 48.0, 0.0
    if f < 240:    # S2 low-angle tracking: ball rolls away down the path
        bx = ball_x(f); t = (f - 120) / 119.0
        by = yc(bx)
        pos = Vector((bx + 1.15, by - 1.45, ground(bx, by - 1.45) + 0.12 + 0.0))
        tg = Vector((bx - 0.55, by + 0.2, ground(bx, by) + 0.75))
        return pos, tg, 30.0, 0.0
    if f < 300:    # S3 tight reaction two-shot
        t = (f - 240) / 59.0
        mx, px = milo_x(f), 0.55
        cxm = (mx + px) / 2.0 - 0.12
        pos = Vector((cxm + lerp(0.0, 0.08, t), lerp(-1.7, -1.55, t), 0.55))
        tg = Vector((cxm + lerp(0.0, 0.05, t), 0.0, 0.50))
        return pos, tg, 33.0, 0.0
    if f < 450:    # S4 side tracking through the flowers
        mx = milo_x(f); px = pip_hop_state(f)[0]
        cx = (mx + px) / 2.0 + 0.05
        yy = yc(cx)
        gz = ground(cx, yy)
        pos = Vector((cx, yy - 3.0, gz + 0.45))
        tg = Vector((cx + 0.1, yy, gz + 1.15))
        return pos, tg, 42.0, 0.0
    if f < 600:    # S5 3/4 view of the bridge; camera follows the action across it
        t = (f - 450) / 149.0
        bx = ball_x(f); mx = milo_x(f)
        cx = clamp(0.5 * (bx + mx) + 0.6, 15.0, 22.0)
        gz = ground(clamp(cx, 15.0, 20.0), 0)
        pos = Vector((cx - 2.0, -4.4, gz + 0.5))
        tg = Vector((cx + 0.2, 0.0, gz + 1.0))
        return pos, tg, 38.0, 0.0
    if f < 750:    # S6 medium fixed camera on the leaf pile
        pos = Vector((PILE_X + 0.2, PY - 2.7, ground(PILE_X, PY) + 0.50))
        tg = Vector((PILE_X + 0.2, PY, ground(PILE_X, PY) + 1.0))
        return pos, tg, 38.0, 0.0
    if f < 840:    # S7 medium: basket + leaves
        t = (f - 750) / 89.0
        cx = lerp(25.9, 25.7, t)
        pos = Vector((cx, PY - 3.0, ground(PILE_X, PY) + 0.55))
        tg = Vector((cx, PY, ground(PILE_X, PY) + 1.0))
        return pos, tg, 36.0, 0.0
    # S8 front medium (from the +Y side: Milo left, Pip right as in the storyboard)
    t = (f - 840) / 59.0
    cx = PILE_X + 0.48
    cyy = PY + 2.5 - 0.1 * t
    pos = Vector((cx, cyy, ground(PILE_X, PY) + 0.72))
    tg = Vector((cx, PY - 1.0, ground(PILE_X, PY) + 0.62))
    return pos, tg, 44.0, 0.0

# ----------------------------------------------------------------- apply a frame
def bone(arm, n): return arm.pose.bones[n]

def apply_char(arm, p, kind, f, recorder):
    pb = arm.pose.bones
    yaw, pitch = p['yaw'], p['pitch']
    Ryaw = Rz(yaw)
    Rl = Matrix.Rotation(pitch, 3, 'X') @ Matrix.Rotation(p['roll'], 3, 'Y')
    Rf = Ryaw @ Rl
    c = Vector(p['pivot'])
    loc = p['pos'] + Ryaw @ c - Rf @ c
    root = pb['root']; root.rotation_mode = 'QUATERNION'
    root.location = loc; root.rotation_quaternion = Rf.to_quaternion()
    def rot(n, x=0.0, y=0.0, z=0.0, loc=None, scale=None):
        b = pb[n]; b.rotation_mode = 'XYZ'; b.rotation_euler = (x, y, z)
        if loc is not None: b.location = loc
        if scale is not None: b.scale = scale
    mouth_open = clamp(p['mouth'], 0, 1)
    msz = (p['mw'] * (0.85 + 0.9 * mouth_open), 1.0, max(mouth_open * 1.6, 0.001))
    ssm = clamp(1.0 - mouth_open * 9.0, 0.0, 1.0)
    ssz = (max(p['mw'] * ssm, 0.001), max(ssm, 0.001), max(ssm, 0.001))
    eye_sc = lambda: (p['wide'], p['wide'], p['wide'] * (1 - 0.92 * max(p['blink'], p['squint'])))
    if kind == 'milo':
        spine_p = p['spine_pitch']; ph_ = p['pelvis_drop']
        rot('pelvis', 0, 0, p['hip_sway'], loc=(0, 0, -ph_))
        rot('spine', spine_p, 0, p['spine_yaw'])
        rot('head', -p['head_up'], 0, p['head_yaw'] - 0.5 * p['spine_yaw'])
        for n, sx in (("eyeL", 1), ("eyeR", -1)):
            rot(n, -p['eye_up'], 0, p['eye_yaw'], scale=eye_sc())
        for n in ("browL", "browR"):
            rot(n, 0, 0, 0, loc=(0, 0, 0.018 * p['brow']))
        rot('mouth', 0, 0, 0, scale=msz); rot('smile', 0, 0, 0, scale=ssz)
        for s, a, sx in (("L", p['L'], 1), ("R", p['R'], -1)):
            rot("arm" + s, -a[0], -sx * a[1], 0)
            rot("fore" + s, -a[2], 0, 0)
        # legs: IK in root frame
        hip_z = 0.30 - ph_
        sl = slope(p['pos'].x)
        for s, ft in (("L", p['lfoot']), ("R", p['rfoot'])):
            ff, up = ft
            # lateral-stand offsets + slope compensation (ground rises ahead of the foot)
            up_ = up + sl * ff * math.cos(yaw - math.pi / 2 + math.pi / 2 * 0)  # slope along heading approx
            th, sh, sw = leg_ik(ff, max(0.0, up_), hip_z)
            rot("thigh" + s, th, 0, 0); rot("shin" + s, sh, 0, 0); rot("foot" + s, -(th + sh) + 0.25 * (up > 0.01), 0, 0)
    else:  # pip
        sq = p['squash']
        rot('body', p['body_pitch'], 0, 0, loc=(0, 0, p['lift']), scale=(1 - sq * 0.5, 1 - sq * 0.5, 1 + sq))
        rot('head', -p['head_up'], 0, p['head_yaw'])
        for n in ("eyeL", "eyeR"):
            rot(n, -p['eye_up'], 0, p['eye_yaw'], scale=eye_sc())
        rot('mouth', 0, 0, 0, scale=msz); rot('smile', 0, 0, 0, scale=ssz)
        for s, a, sx in (("L", p['L'], 1), ("R", p['R'], -1)):
            rot("arm" + s, -a[0], -sx * a[1] * 0.8, 0)
        rot("legL", p['legs'][0], 0, 0); rot("legR", p['legs'][1], 0, 0)
        tw = f * p['tail_rate']; am = p['tail_amp']
        rot('tail1', 0.05 * math.sin(tw * 0.5), 0, am * 0.55 * math.sin(tw))
        rot('tail2', 0, 0, am * 0.7 * math.sin(tw - 0.9)); rot('tail3', 0, 0, am * 0.9 * math.sin(tw - 1.8))

def burst_state(f):
    hf = es(f, 862, 866) * (1 - es(f, 880, 892))
    return hf

def apply_frame(f):
    sc = bpy.context.scene
    pm = pose_dict_milo(f); pp = pose_dict_pip(f)
    apply_char(S['milo'], pm, 'milo', f, None); apply_char(S['pip'], pp, 'pip', f, None)
    # ball
    if f < 752: bpos = ball_pos_raw(f)
    else: bpos = ball_world(f)
    S['ball'].location = bpos
    S['ball'].rotation_quaternion = BALL_Q[f] if f < len(BALL_Q) else BALL_Q[-1]
    bl, bq = basket_world(f)
    S['basket'].location = bl; S['basket'].rotation_quaternion = bq
    # leaves
    for i, ob in enumerate(S['leaves']):
        pos, q, fl = leaf_state(i, f)
        ob.location = pos; ob.rotation_quaternion = q
    # burst
    hf = burst_state(f)
    cx = PILE_X + 0.47; cz = ground(PILE_X, PY) + 0.80
    for i, ob in enumerate(S['burst']):
        a = math.radians(-60 + i * 30)
        ob.location = (cx + math.sin(-a) * 0.0 + 0.0, PY + 0.2, cz + 0.28)
        r = 0.28
        ob.location = Vector((cx + r * math.sin(a) * 0 + (i - 2) * 0.0, PY + 0.55, cz + 0.12 + 0.1 * abs(i - 2))) if False else Vector((cx + 0.14 * (i - 2) * 1.0, PY + 0.2, cz + 0.34 - 0.04 * abs(i - 2)))
        ob.rotation_euler = (0, math.radians((i - 2) * 24), 0) if False else (math.radians(0), math.radians(-(i - 2) * 22), 0)
        s = max(hf, 0.0001); ob.scale = (s, s, s)
    # camera
    pos, tg, lens, roll = CAM_TRACK(f)
    S['cam'].location = pos; S['cam'].rotation_mode = 'QUATERNION'; S['cam'].rotation_quaternion = lookat(pos, tg, roll)
    S['cam'].data.lens = lens

def precompute():
    # Milo gait phase table (continuous, speed-matched), ball roll quaternions
    MILO_PHASE.clear(); ph = 0.0
    S_, duty = 0.40, 0.46
    for f in range(NF + 5):
        v = abs((milo_x(f + 1) - milo_x(f - 1)) * FPS / 2.0)
        ph += v * duty / S_ / FPS
        MILO_PHASE.append(ph)
    BALL_Q.clear(); q = Quaternion((1, 0, 0, 0)); prev = ball_pos_raw(0)
    for f in range(NF):
        cur = ball_pos_raw(f) if f < 752 else ball_world(f)
        if f >= 752:
            loc, bq = basket_world(f); BALL_Q.append(bq @ Quaternion((0.3, 0.5, 0.1), 0.6) if False else q); continue
        d = Vector((cur.x - prev.x, cur.y - prev.y, 0))
        if d.length > 1e-6:
            axis = Vector((0, 0, 1)).cross(d.normalized()); ang = d.length / R_BALL
            q = Quaternion(axis, ang) @ q
        BALL_Q.append(q.copy()); prev = cur
    # when in basket the ball keeps its final orientation
    return

def bake():
    sc = bpy.context.scene
    objs = [S['milo'], S['pip'], S['ball'], S['basket'], S['cam']] + S['leaves'] + S['burst']
    for f in range(NF):
        sc.frame_set(f)
        apply_frame(f)
        for arm in (S['milo'], S['pip']):
            for pb in arm.pose.bones:
                if pb.name == 'root':
                    pb.keyframe_insert('location', frame=f); pb.keyframe_insert('rotation_quaternion', frame=f)
                else:
                    pb.keyframe_insert('rotation_euler', frame=f); pb.keyframe_insert('location', frame=f); pb.keyframe_insert('scale', frame=f)
        for ob in (S['ball'], S['basket']):
            ob.keyframe_insert('location', frame=f); ob.keyframe_insert('rotation_quaternion', frame=f)
        for ob in S['leaves']:
            ob.keyframe_insert('location', frame=f); ob.keyframe_insert('rotation_quaternion', frame=f)
        for ob in S['burst']:
            ob.keyframe_insert('scale', frame=f); ob.keyframe_insert('location', frame=f); ob.keyframe_insert('rotation_euler', frame=f)
        S['cam'].keyframe_insert('location', frame=f); S['cam'].keyframe_insert('rotation_quaternion', frame=f)
        S['cam'].data.keyframe_insert('lens', frame=f)
    # constant interpolation for camera => exact cuts
    def all_fcurves(idb):
        ad = idb.animation_data
        if not ad or not ad.action: return []
        a = ad.action
        try:
            return list(a.fcurves)
        except Exception:
            out = []
            for l in a.layers:
                for s_ in l.strips:
                    for cb in s_.channelbags: out += list(cb.fcurves)
            return out
    for idb in (S['cam'], S['cam'].data):
        for fc in all_fcurves(idb):
            for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'
    for ob in S['leaves'] + [S['ball']] + [S['milo'], S['pip']]:
        for fc in all_fcurves(ob):
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    out_blend = argv[0] if argv and argv[0].endswith('.blend') else None
    still = None; res = 1080; outimg = None; samples = None
    for i, a in enumerate(argv):
        if a == '--still': still = [int(v) for v in argv[i + 1].split(',')]
        if a == '--out': outimg = argv[i + 1]
        if a == '--res': res = int(argv[i + 1])
        if a == '--samples': samples = int(argv[i + 1])
    setup(); precompute()
    sc = bpy.context.scene
    if samples: sc.cycles.samples = samples
    if still:
        sc.render.resolution_percentage = int(100 * res / 1080)
        for f in still:
            sc.frame_set(f); apply_frame(f)
            sc.render.filepath = f"{outimg}_{f:04d}.png"
            bpy.ops.render.render(write_still=True)
    else:
        bake()
        sc.frame_set(0)
        bpy.ops.wm.save_as_mainfile(filepath=out_blend)
        print("saved", out_blend)
