"""Export reusable stand-alone rig files (Milo, Pip, Ball, Basket)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lww_chars as C
out = sys.argv[1]
C.save_rig(lambda: C.build_milo("Milo"), os.path.join(out, "Milo_Rig.blend"))
C.save_rig(lambda: C.build_pip("Pip"), os.path.join(out, "Pip_Rig.blend"))
C.save_rig(lambda: (C.build_ball(), C.build_basket()), os.path.join(out, "Ball_And_Basket.blend"))
