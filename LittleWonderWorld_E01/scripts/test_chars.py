import sys, bpy, math
sys.path.insert(0, "scripts")
import lww_chars as C
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
m = C.build_milo(); p = C.build_pip(); b = C.build_ball(); k = C.build_basket()
p.location = (0.6, 0, 0); m.location = (-0.3, 0, 0); b.location = (0.15, -0.5, 0.17); k.location = (0.9, -0.6, 0)
bpy.ops.mesh.primitive_plane_add(size=20); 
sc.render.engine = 'CYCLES'; sc.cycles.samples = 24; sc.cycles.use_denoising = True
sc.render.resolution_x = 960; sc.render.resolution_y = 540
w = bpy.data.worlds.new("w"); w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0.6, 0.75, 1, 1); sc.world = w
bpy.ops.object.light_add(type='SUN', rotation=(0.8, 0.3, 0.6)); bpy.context.object.data.energy = 3.5
bpy.ops.object.camera_add(location=(0.3, -2.3, 0.6), rotation=(math.radians(88), 0, 0)); sc.camera = bpy.context.object; sc.camera.data.lens = 40
sc.render.filepath = sys.argv[-1]
bpy.ops.render.render(write_still=True)
