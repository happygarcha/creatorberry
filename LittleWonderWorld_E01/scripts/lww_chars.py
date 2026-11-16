"""Little Wonder World - reusable character rigs (Milo, Pip), ball and basket.
Colours/proportions were read off E01_Original_Storyboard.png (see reference/character_sheet.png).
Convention: every bone has IDENTITY rest orientation (pointing +Y, roll 0) so pose rotations are
expressed directly in armature axes.  Characters face -Y (toward the 'front' camera);
character-left = +X.  Root bone sits on the ground at the origin.
Every mesh part is skinned 100% to ONE bone via vertex group + Armature modifier.
"""
import bpy, bmesh, math, random
from mathutils import Matrix, Vector, Euler

# ---------------------------------------------------------------- palette (from storyboard)
PAL = dict(
    skin=(0.80, 0.40, 0.22), skin_dark=(0.62, 0.28, 0.15), cheek=(0.95, 0.42, 0.36),
    hair=(0.055, 0.025, 0.012), shirt=(0.04, 0.42, 0.47), overall=(0.95, 0.60, 0.05),
    shoe=(0.92, 0.90, 0.88), bear=(0.55, 0.30, 0.12),
    eye_w=(0.95, 0.95, 0.93), iris=(0.10, 0.045, 0.02), mouth=(0.32, 0.03, 0.04), tongue=(0.85, 0.28, 0.30),
    pip=(0.20, 0.68, 0.38), pip_belly=(0.82, 0.90, 0.55), spike=(0.95, 0.40, 0.10), pip_cheek=(0.95, 0.45, 0.42),
)


def mat(name, color, rough=0.5, spec=0.4, emission=None):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    for k in ("Specular IOR Level", "Specular"):
        if k in b.inputs:
            b.inputs[k].default_value = spec
    if emission is not None:
        b.inputs["Emission Color"].default_value = (*emission, 1)
        b.inputs["Emission Strength"].default_value = 0.6
    m.diffuse_color = (*color, 1)
    return m


class Builder:
    """Accumulates bmesh geometry per (bone, material) then emits skinned objects."""
    def __init__(self, prefix):
        self.prefix = prefix
        self.g = {}

    def _bm(self, bone, matname):
        k = (bone, matname)
        if k not in self.g:
            self.g[k] = bmesh.new()
        return self.g[k]

    @staticmethod
    def _M(c, r, rot):
        return (Matrix.Translation(c) @ Euler(rot, 'XYZ').to_matrix().to_4x4() @
                Matrix.Diagonal((r[0], r[1], r[2], 1.0)))

    def ell(self, bone, mname, c, r, rot=(0, 0, 0), seg=20, ring=12):
        bm = self._bm(bone, mname)
        v = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=ring, radius=1.0)['verts']
        bmesh.ops.transform(bm, matrix=self._M(c, r, rot), verts=v)

    def cone(self, bone, mname, c, r, h, rot=(0, 0, 0), seg=8, r2=0.0):
        bm = self._bm(bone, mname)
        v = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=1.0, radius2=r2, depth=1.0)['verts']
        bmesh.ops.transform(bm, matrix=self._M(c, (r, r, h), rot), verts=v)

    def emit(self, arm, mats):
        objs = []
        for (bone, mname), bm in self.g.items():
            me = bpy.data.meshes.new(f"{self.prefix}_{bone}_{mname}")
            bm.to_mesh(me); bm.free()
            for p in me.polygons:
                p.use_smooth = True
            ob = bpy.data.objects.new(f"{self.prefix}_{bone}_{mname}", me)
            bpy.context.scene.collection.objects.link(ob)
            ob.data.materials.append(mats[mname])
            vg = ob.vertex_groups.new(name=bone)
            vg.add(list(range(len(me.vertices))), 1.0, 'REPLACE')
            md = ob.modifiers.new("Armature", 'ARMATURE'); md.object = arm
            ob.parent = arm
            objs.append(ob)
        self.g = {}
        return objs


def make_armature(name, bones):
    """bones: list of (name, parent, head). Identity rest orientation."""
    ad = bpy.data.armatures.new(name)
    ad.display_type = 'OCTAHEDRAL'
    arm = bpy.data.objects.new(name, ad)
    bpy.context.scene.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    arm.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    eb = {}
    for n, p, h in bones:
        e = ad.edit_bones.new(n)
        e.head = Vector(h); e.tail = Vector(h) + Vector((0, 0.04, 0)); e.roll = 0.0
        if p:
            e.parent = eb[p]
        eb[n] = e
    bpy.ops.object.mode_set(mode='OBJECT')
    for pb in arm.pose.bones:
        pb.rotation_mode = 'XYZ'
    return arm


# ================================================================= MILO
MILO_REST = dict(hip_z=0.30, ankle_z=0.05, thigh=0.125, shin=0.125, hipx=0.065)


def build_milo(prefix="Milo"):
    B = Builder(prefix)
    skin, hair = "M_skin", "M_hair"
    mats = dict(
        M_skin=mat("M_skin", PAL['skin'], 0.5), M_cheek=mat("M_cheek", PAL['cheek'], 0.6),
        M_hair=mat("M_hair", PAL['hair'], 0.45), M_shirt=mat("M_shirt", PAL['shirt'], 0.6),
        M_overall=mat("M_overall", PAL['overall'], 0.6), M_shoe=mat("M_shoe", PAL['shoe'], 0.45),
        M_bear=mat("M_bear", PAL['bear'], 0.7), M_eyew=mat("M_eyew", PAL['eye_w'], 0.15),
        M_iris=mat("M_iris", PAL['iris'], 0.15, 0.8), M_pupil=mat("M_pupil", (0, 0, 0), 0.1),
        M_hl=mat("M_hl", (1, 1, 1), 0.1, emission=(1, 1, 1)),
        M_mouth=mat("M_mouth", PAL['mouth'], 0.4), M_tongue=mat("M_tongue", PAL['tongue'], 0.4),
        M_nose=mat("M_nose", PAL['skin_dark'], 0.5),
    )
    hz, hx = MILO_REST['hip_z'], MILO_REST['hipx']
    bones = [("root", None, (0, 0, 0)), ("pelvis", "root", (0, 0, hz)), ("spine", "pelvis", (0, 0, 0.32)),
             ("head", "spine", (0, 0, 0.50)),
             ("eyeL", "head", (0.075, -0.145, 0.675)), ("eyeR", "head", (-0.075, -0.145, 0.675)),
             ("browL", "head", (0.075, -0.15, 0.755)), ("browR", "head", (-0.075, -0.15, 0.755)),
             ("mouth", "head", (0, -0.168, 0.575)), ("smile", "head", (0, -0.168, 0.575)),
             ("armL", "spine", (0.155, 0, 0.45)), ("foreL", "armL", (0.155, 0, 0.365)), ("handL", "foreL", (0.155, 0, 0.29)),
             ("armR", "spine", (-0.155, 0, 0.45)), ("foreR", "armR", (-0.155, 0, 0.365)), ("handR", "foreR", (-0.155, 0, 0.29)),
             ("thighL", "pelvis", (hx, 0, hz)), ("shinL", "thighL", (hx, 0, hz - 0.125)), ("footL", "shinL", (hx, 0, 0.05)),
             ("thighR", "pelvis", (-hx, 0, hz)), ("shinR", "thighR", (-hx, 0, hz - 0.125)), ("footR", "shinR", (-hx, 0, 0.05))]
    arm = make_armature(prefix + "_Rig", bones)
    # --- torso / clothes
    B.ell("spine", "M_shirt", (0, 0, 0.40), (0.135, 0.115, 0.125))
    B.ell("pelvis", "M_overall", (0, 0, 0.30), (0.14, 0.12, 0.10))
    B.ell("spine", "M_overall", (0, -0.092, 0.405), (0.088, 0.034, 0.078))        # bib
    B.ell("spine", "M_bear", (0, -0.124, 0.40), (0.03, 0.01, 0.03))               # bear patch
    for sx in (1, -1):
        B.ell("spine", "M_overall", (sx * 0.065, -0.03, 0.495), (0.02, 0.085, 0.015), rot=(0.25, 0, 0))   # straps
    # --- head
    B.ell("head", skin, (0, 0, 0.66), (0.19, 0.175, 0.17), seg=32, ring=20)
    for sx in (1, -1):
        B.ell("head", skin, (sx * 0.185, 0.0, 0.64), (0.034, 0.03, 0.042))                       # ears
        B.ell("head", "M_cheek", (sx * 0.105, -0.128, 0.595), (0.042, 0.016, 0.03))              # blush
    B.ell("head", "M_nose", (0, -0.172, 0.625), (0.02, 0.016, 0.016))
    # --- hair cap + curls
    B.ell("head", hair, (0, 0.035, 0.70), (0.205, 0.185, 0.17), seg=32, ring=18)
    rnd = random.Random(7)
    for i in range(70):
        th = rnd.uniform(0, 2 * math.pi); ph = rnd.uniform(0.0, 1.25)   # polar angle from top
        rx, ry, rz = 0.205, 0.19, 0.18
        px = rx * math.sin(ph) * math.cos(th); py = 0.035 + ry * math.sin(ph) * math.sin(th); pz = 0.70 + rz * math.cos(ph)
        if py < -0.06 and pz < 0.80:
            continue
        r = rnd.uniform(0.032, 0.05)
        B.ell("head", hair, (px, py, pz), (r, r, r), seg=10, ring=7)
    for i in range(9):   # fringe curls above brow line
        x = -0.15 + i * 0.0375
        B.ell("head", hair, (x, -0.135 + 0.03 * abs(x) * 3, 0.800 - 0.012 * abs(x) * 4), (0.036, 0.034, 0.034), seg=10, ring=7)
    # --- face
    for n, sx in (("eyeL", 1), ("eyeR", -1)):
        c = (sx * 0.075, -0.145, 0.675)
        B.ell(n, "M_eyew", c, (0.054, 0.032, 0.060))
        B.ell(n, "M_iris", (c[0], c[1] - 0.019, c[2]), (0.040, 0.016, 0.045))
        B.ell(n, "M_pupil", (c[0], c[1] - 0.030, c[2]), (0.022, 0.008, 0.026), seg=12, ring=8)
        B.ell(n, "M_hl", (c[0] + sx * 0.012, c[1] - 0.035, c[2] + 0.017), (0.011, 0.005, 0.011), seg=8, ring=6)
    for n, sx in (("browL", 1), ("browR", -1)):
        B.ell(n, hair, (sx * 0.075, -0.152, 0.755), (0.048, 0.012, 0.012), rot=(0, sx * -0.2, 0), seg=10, ring=6)
    mo = (0, -0.168, 0.575)
    B.ell("mouth", "M_mouth", mo, (0.042, 0.014, 0.034), seg=16, ring=10)
    B.ell("mouth", "M_tongue", (mo[0], mo[1] - 0.003, mo[2] - 0.016), (0.026, 0.01, 0.014), seg=10, ring=6)
    for i in range(9):   # smile arc
        t = (i - 4) / 4.0
        B.ell("smile", "M_mouth", (t * 0.036, -0.168 - 0.004, 0.575 + (t * t - 0.6) * 0.016), (0.0078, 0.006, 0.0078), seg=8, ring=6)
    # --- arms
    for s, sx in (("L", 1), ("R", -1)):
        B.ell("arm" + s, "M_shirt", (sx * 0.155, 0, 0.415), (0.042, 0.042, 0.052))
        B.ell("fore" + s, skin, (sx * 0.155, 0, 0.33), (0.034, 0.034, 0.05))
        B.ell("hand" + s, skin, (sx * 0.155, 0, 0.275), (0.042, 0.036, 0.042))
        B.ell("hand" + s, skin, (sx * 0.155 + sx * -0.022, -0.02, 0.268), (0.016, 0.016, 0.022), seg=8, ring=6)  # thumb
    # --- legs
    for s, sx in (("L", 1), ("R", -1)):
        B.ell("thigh" + s, "M_overall", (sx * hx, 0, hz - 0.055), (0.058, 0.058, 0.082))
        B.ell("shin" + s, "M_overall", (sx * hx, 0, hz - 0.178), (0.05, 0.05, 0.075))
        B.ell("foot" + s, "M_shoe", (sx * hx, -0.028, 0.040), (0.058, 0.098, 0.047))
        B.ell("foot" + s, "M_shoe", (sx * hx, -0.04, 0.015), (0.06, 0.1, 0.014))
    B.emit(arm, mats)
    return arm


# ================================================================= PIP
PIP_REST = dict(hip_z=0.12, hipx=0.075)


def build_pip(prefix="Pip"):
    B = Builder(prefix)
    mats = dict(
        P_body=mat("P_body", PAL['pip'], 0.4, 0.5), P_belly=mat("P_belly", PAL['pip_belly'], 0.5),
        P_spike=mat("P_spike", PAL['spike'], 0.45), P_cheek=mat("P_cheek", PAL['pip_cheek'], 0.6),
        P_eyew=mat("P_eyew", PAL['eye_w'], 0.15), P_iris=mat("P_iris", PAL['iris'], 0.15, 0.8),
        P_pupil=mat("P_pupil", (0, 0, 0), 0.1), P_hl=mat("P_hl", (1, 1, 1), 0.1, emission=(1, 1, 1)),
        P_mouth=mat("P_mouth", PAL['mouth'], 0.4), P_tongue=mat("P_tongue", PAL['tongue'], 0.4),
        P_nose=mat("P_nose", (0.10, 0.35, 0.22), 0.5),
    )
    bones = [("root", None, (0, 0, 0)), ("body", "root", (0, 0, 0.12)), ("head", "body", (0, -0.02, 0.38)),
             ("eyeL", "head", (0.078, -0.135, 0.505)), ("eyeR", "head", (-0.078, -0.135, 0.505)),
             ("mouth", "head", (0, -0.205, 0.415)), ("smile", "head", (0, -0.205, 0.415)),
             ("armL", "body", (0.135, -0.03, 0.31)), ("armR", "body", (-0.135, -0.03, 0.31)),
             ("legL", "body", (0.075, 0, 0.12)), ("legR", "body", (-0.075, 0, 0.12)),
             ("tail1", "body", (0, 0.11, 0.17)), ("tail2", "tail1", (0, 0.27, 0.17)), ("tail3", "tail2", (0, 0.39, 0.19))]
    arm = make_armature(prefix + "_Rig", bones)
    B.ell("body", "P_body", (0, 0.0, 0.25), (0.155, 0.14, 0.17), seg=28, ring=16)
    B.ell("body", "P_belly", (0, -0.095, 0.24), (0.108, 0.05, 0.135))
    # head
    B.ell("head", "P_body", (0, -0.02, 0.48), (0.18, 0.165, 0.152), seg=32, ring=20)
    B.ell("head", "P_body", (0, -0.155, 0.435), (0.088, 0.072, 0.058))      # snout
    B.ell("head", "P_nose", (0.03, -0.222, 0.452), (0.011, 0.006, 0.008), seg=8, ring=6)
    B.ell("head", "P_nose", (-0.03, -0.222, 0.452), (0.011, 0.006, 0.008), seg=8, ring=6)
    for sx in (1, -1):
        B.ell("head", "P_cheek", (sx * 0.115, -0.128, 0.445), (0.04, 0.016, 0.03))
        B.cone("head", "P_spike", (sx * 0.15, 0.07, 0.50), 0.03, 0.09, rot=(-0.3, sx * 0.9, 0), seg=8)      # side fins
        B.cone("head", "P_spike", (sx * 0.11, 0.09, 0.56), 0.028, 0.08, rot=(-0.55, sx * 0.55, 0), seg=8)
    B.cone("head", "P_spike", (0, 0.05, 0.63), 0.032, 0.085, rot=(-0.25, 0, 0), seg=8)
    B.cone("head", "P_spike", (0, 0.11, 0.59), 0.028, 0.075, rot=(-0.6, 0, 0), seg=8)
    # eyes (big)
    for n, sx in (("eyeL", 1), ("eyeR", -1)):
        c = (sx * 0.078, -0.135, 0.505)
        B.ell(n, "P_eyew", c, (0.056, 0.034, 0.064))
        B.ell(n, "P_iris", (c[0], c[1] - 0.02, c[2]), (0.043, 0.017, 0.050))
        B.ell(n, "P_pupil", (c[0], c[1] - 0.031, c[2]), (0.024, 0.009, 0.029), seg=12, ring=8)
        B.ell(n, "P_hl", (c[0] + sx * 0.013, c[1] - 0.037, c[2] + 0.02), (0.012, 0.005, 0.012), seg=8, ring=6)
    mo = (0, -0.205, 0.415)
    B.ell("mouth", "P_mouth", mo, (0.045, 0.014, 0.034), seg=16, ring=10)
    B.ell("mouth", "P_tongue", (mo[0], mo[1] - 0.003, mo[2] - 0.016), (0.028, 0.01, 0.014), seg=10, ring=6)
    for i in range(9):
        t = (i - 4) / 4.0
        B.ell("smile", "P_mouth", (t * 0.045, mo[1] - 0.004, mo[2] + (t * t - 0.6) * 0.018), (0.0085, 0.006, 0.0085), seg=8, ring=6)
    # arms
    for s, sx in (("L", 1), ("R", -1)):
        B.ell("arm" + s, "P_body", (sx * 0.135, -0.04, 0.265), (0.038, 0.038, 0.072), rot=(0.25, 0, sx * 0.1))
        B.ell("arm" + s, "P_belly", (sx * 0.145, -0.06, 0.205), (0.038, 0.036, 0.038))
    # legs
    for s, sx in (("L", 1), ("R", -1)):
        B.ell("leg" + s, "P_body", (sx * 0.078, 0.0, 0.085), (0.062, 0.062, 0.075))
        B.ell("leg" + s, "P_body", (sx * 0.078, -0.035, 0.03), (0.063, 0.09, 0.036))
        for k in (-1, 0, 1):
            B.ell("leg" + s, "P_belly", (sx * 0.078 + k * 0.03, -0.115, 0.03), (0.016, 0.02, 0.016), seg=8, ring=6)
    # tail + back spikes
    B.ell("tail1", "P_body", (0, 0.19, 0.165), (0.075, 0.115, 0.07), rot=(-0.05, 0, 0))
    B.ell("tail2", "P_body", (0, 0.33, 0.175), (0.052, 0.085, 0.048), rot=(-0.12, 0, 0))
    B.ell("tail3", "P_body", (0, 0.43, 0.20), (0.032, 0.06, 0.03), rot=(-0.3, 0, 0))
    B.cone("body", "P_spike", (0, 0.13, 0.355), 0.034, 0.08, rot=(-0.9, 0, 0), seg=8)
    B.cone("body", "P_spike", (0, 0.145, 0.27), 0.033, 0.08, rot=(-1.25, 0, 0), seg=8)
    B.cone("tail1", "P_spike", (0, 0.20, 0.235), 0.03, 0.07, rot=(-1.45, 0, 0), seg=8)
    B.cone("tail2", "P_spike", (0, 0.33, 0.228), 0.025, 0.06, rot=(-1.5, 0, 0), seg=8)
    B.cone("tail3", "P_spike", (0, 0.43, 0.24), 0.02, 0.05, rot=(-1.5, 0, 0), seg=8)
    B.emit(arm, mats)
    return arm


# ================================================================= BALL & BASKET
def build_ball(r=0.17):
    me = bpy.data.meshes.new("Ball")
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=32, radius=r)
    bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new("RainbowBall", me)
    bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new("RainbowBall"); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); bs = nt.nodes.new("ShaderNodeBsdfPrincipled")
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    mad = nt.nodes.new("ShaderNodeMath"); mad.operation = 'MULTIPLY_ADD'
    mr = nt.nodes.new("ShaderNodeMapRange"); ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    nt.links.new(sep.outputs["X"], mad.inputs[0]); mad.inputs[1].default_value = 0.30
    nt.links.new(sep.outputs["Z"], mad.inputs[2])
    mr.inputs[1].default_value = -r * 1.1; mr.inputs[2].default_value = r * 1.1
    nt.links.new(mad.outputs[0], mr.inputs[0]); nt.links.new(mr.outputs[0], ramp.inputs[0])
    ramp.color_ramp.interpolation = 'CONSTANT'
    cols = [(0.80, 0.03, 0.04), (0.98, 0.26, 0.02), (1.0, 0.72, 0.03), (0.25, 0.70, 0.12), (0.08, 0.45, 0.95), (0.42, 0.13, 0.70)]
    el = ramp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*cols[5], 1); el[1].position = 1 / 6 * 5; el[1].color = (*cols[0], 1)
    for i in range(1, 5):
        e = el.new(i / 6.0); e.color = (*cols[5 - i], 1)
    nt.links.new(ramp.outputs["Color"], bs.inputs["Base Color"])
    bs.inputs["Roughness"].default_value = 0.28
    for k in ("Specular IOR Level", "Specular"):
        if k in bs.inputs:
            bs.inputs[k].default_value = 0.6
    nt.links.new(bs.outputs[0], out.inputs[0])
    ob.data.materials.append(m)
    return ob


def build_basket():
    """Wicker basket, local +Z = opening direction, origin at centre of base."""
    bm = bmesh.new()
    # body: tapered open cylinder
    ret = bmesh.ops.create_cone(bm, cap_ends=False, segments=40, radius1=0.2, radius2=0.25, depth=0.24)
    bmesh.ops.transform(bm, matrix=Matrix.Translation((0, 0, 0.12)), verts=ret['verts'])
    # base disc
    base = bmesh.ops.create_circle(bm, cap_ends=True, segments=40, radius=0.2)
    # rim torus ring
    for i in range(40):
        a = i / 40 * 2 * math.pi
    me = bpy.data.meshes.new("Basket"); bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new("WickerBasket", me)
    bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new("Wicker"); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord"); wv = nt.nodes.new("ShaderNodeTexWave")
    wv.wave_type = 'BANDS'; wv.bands_direction = 'Z'; wv.inputs["Scale"].default_value = 42; wv.inputs["Distortion"].default_value = 2.0
    wv2 = nt.nodes.new("ShaderNodeTexWave"); wv2.wave_type = 'BANDS'; wv2.bands_direction = 'X'; wv2.inputs["Scale"].default_value = 36
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = 'RGBA'
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (0.30, 0.14, 0.05, 1); ramp.color_ramp.elements[1].color = (0.72, 0.42, 0.16, 1)
    nt.links.new(tc.outputs["Object"], wv.inputs["Vector"]); nt.links.new(tc.outputs["Object"], wv2.inputs["Vector"])
    nt.links.new(wv.outputs["Fac"], ramp.inputs[0]); nt.links.new(ramp.outputs[0], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.8
    nt.links.new(wv.outputs["Fac"], nt.nodes.new("ShaderNodeBump").inputs["Height"])
    bump = nt.nodes[-1]; bump.inputs["Strength"].default_value = 0.4
    nt.links.new(bump.outputs[0], b.inputs["Normal"])
    ob.data.materials.append(m)
    # rim (torus) + handle arc as child objects
    parts = []
    for name, rad, tube, z, rot in (("rim", 0.25, 0.018, 0.24, 0),):
        tbm = bmesh.new()
        n_major, n_minor = 40, 8
        verts = []
        for i in range(n_major):
            a = i / n_major * 2 * math.pi
            ring = []
            for j in range(n_minor):
                bb = j / n_minor * 2 * math.pi
                rr = rad + tube * math.cos(bb)
                ring.append(tbm.verts.new((rr * math.cos(a), rr * math.sin(a), z + tube * math.sin(bb))))
            verts.append(ring)
        for i in range(n_major):
            for j in range(n_minor):
                tbm.faces.new((verts[i][j], verts[(i + 1) % n_major][j], verts[(i + 1) % n_major][(j + 1) % n_minor], verts[i][(j + 1) % n_minor]))
        tme = bpy.data.meshes.new("BasketRim"); tbm.to_mesh(tme); tbm.free()
        for p in tme.polygons:
            p.use_smooth = True
        tob = bpy.data.objects.new("BasketRim", tme); bpy.context.scene.collection.objects.link(tob)
        tob.data.materials.append(m); tob.parent = ob
    return ob


def save_rig(builder_fn, path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    a = builder_fn()
    bpy.ops.wm.save_as_mainfile(filepath=path)
    return a
