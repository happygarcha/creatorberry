// ---------- Glass, plant pot, drop ----------
const HX = -442, HZ = -126, HY0 = -380;           // hose tip
const cupG = new THREE.Group(); root.add(cupG);
add(cupG, [new THREE.CylinderGeometry(42, 36, 120, 36, 1, true).translate(HX, -480, HZ), new THREE.CylinderGeometry(36, 36, 3, 36).translate(HX, -540, HZ)], M.glassF);
const cupWater = add(cupG, [new THREE.CylinderGeometry(39, 36.5, 1, 36).translate(0, 0.5, 0)], M.accent); cupWater.position.set(HX, -537, HZ);
const potG = new THREE.Group(); root.add(potG);
add(potG, [new THREE.CylinderGeometry(52, 38, 84, 32, 1, true).translate(HX, -498, HZ), new THREE.CylinderGeometry(38, 38, 3, 24).translate(HX, -540, HZ), new THREE.CylinderGeometry(54, 54, 8, 32).translate(HX, -452, HZ)], M.shell);
{ const lv = []; for (let k = 0; k < 6; k++) { const a = k * Math.PI * 2 / 6, g = new THREE.SphereGeometry(30, 14, 10); g.scale(1, 0.18, 0.5); g.rotateZ(0.6); g.rotateY(a); g.translate(HX + Math.cos(a) * 34, -430 + (k % 2) * 16, HZ - Math.sin(a) * 34); lv.push(g); }
  add(potG, lv, M.white); add(potG, [cylX(2.4, 70, HX, -445, HZ, 8).rotateZ(Math.PI / 2).translate(0, 0, 0)], M.mid); }
const dropM = add(root, [new THREE.SphereGeometry(4.4, 14, 10)], M.accent);
// ---------- Bedroom (section): floor, wall, bed with sleeper, window with an opening sash, CO2 dots ----------
const room = new THREE.Group(); scene.add(room);
add(room, [box(5200, 40, 3700, 0, -2390, 1700), box(5200, 3050, 6, 0, -2350, -140)], RM.room);
add(room, [box(1600, 450, 1900, 1300, -2350, 1250), box(1600, 520, 50, 1300, -1900, 270)], RM.room);
add(room, [box(1560, 110, 1860, 1300, -1900, 1250), box(520, 120, 360, 1050, -1790, 470)], RM.cloth);
add(room, [new THREE.SphereGeometry(120, 20, 14).translate(1050, -1690, 520), new THREE.SphereGeometry(200, 20, 14).scale(2.6, 0.5, 2.1).translate(1300, -1710, 1150)], RM.cloth);
add(room, [box(1200, 60, 40, -1300, -1580, -135), box(1200, 60, 40, -1300, -150, -135), box(60, 1430, 40, -1900, -1580, -135), box(60, 1430, 40, -700, -1580, -135), box(1300, 22, 90, -1300, -1612, -135)], RM.frame);
const sash = new THREE.Group(); sash.position.set(-1870, 0, -118); room.add(sash);
add(sash, [box(560, 1330, 22, 280, -1520, 0)], RM.glass); add(sash, [box(14, 1330, 30, 0, -1520, 0), box(14, 1330, 30, 560, -1520, 0)], RM.frame);
const CO2 = [];
{ const r = mulberry(55); for (let i = 0; i < 110; i++) { const m = add(room, [new THREE.SphereGeometry(24, 10, 8)], RM.co2); const p = V3(300 + r() * 1900, -2250 + r() * 1750, 330 + r() * 1950); CO2.push({ m, p, t: K.co2[0] + r() * (K.co2[1] - K.co2[0] - 1), s: 0.7 + r() * 0.6 }); } }
// ---------- Germs (rod bacteria) and the dive section ----------
const germs = [];
{ const r = mulberry(7); for (let i = 0; i < 18; i++) { const m = add(Lpan.g, [new THREE.CapsuleGeometry(2.3, 8, 4, 8).rotateZ(Math.PI / 2)], M.germ);
    m.position.set(-330 + r() * 150, -47.4, -52 + r() * 104); m.rotation.y = r() * 3; germs.push({ m, t: K.germs[0] + i * 0.22 }); } }
// ---------- Scene state ----------
const clipPlane = new THREE.Plane(), clipPlane2 = new THREE.Plane();
const guides = new THREE.Group(); root.add(guides);
const gMat = new THREE.LineDashedMaterial({ color: 0x8f8e8a, dashSize: 9, gapSize: 7 });
function settle(u) { if (u <= 0) return 0; if (u >= 1) return 1; return eio(Math.min(1, u / 0.78)) + Math.sin(Math.PI * seg(u, 0.62, 1)) * 0.025; }
function liftOf(L, t) {
  const k = L.name === 'shell' ? 0 : L.name === 'coil' ? 1 : -1; if (k < 0) return 0;
  const up = settle(seg(t, K.lift + k * K.liftStep, K.lift + k * K.liftStep + K.liftDur));
  const dn = eio(seg(t, K.close[0] + (1 - k) * 0.22, K.close[0] + (1 - k) * 0.22 + 0.9));
  return up * (1 - dn);
}
function pathAt(t) {
  const run = seg(t, K.pathRun[0], K.pathRun[1]); let v = t < K.pathRun[0] ? 0 : (0.45 * run + 0.55 * ss(run));
  if (t > 46.2) v = Math.min(v, 1 - eio(seg(t, 46.2, 47.6)));           // drains back
  const again = seg(t, 52.9, 55.0); if (t > 52.5) v = 0.4 * again + 0.6 * ss(again);   // the ending: lit once more, source to end
  return v;
}
const dropPeriod = 2.15;
function dropState(t) {                       // returns {y, s, hit, n}: swelling, falling and the count of drops that have landed
  const t0 = 1.0; if (t < t0) return { y: HY0, s: 0, hit: -9, n: 0 };
  const n = Math.floor((t - t0) / dropPeriod), u = (t - t0) - n * dropPeriod;
  const swell = 0.75, fall = 0.42;
  let y = HY0, s = 1;
  if (u < swell) s = eo(u / swell); else if (u < swell + fall) { const f = u - swell; y = HY0 - 0.5 * 1043 * f * f; } else s = 0;
  return { y, s: Math.max(s, 0.001), hit: u - (swell + fall), n: n + (u >= swell + fall ? 1 : 0), idx: n };
}
function setScene(t) {
  for (const L of LAYERS) { const e = liftOf(L, t); L.g.position.set(0, e * (L.name === 'shell' ? 270 : 130), e * (L.name === 'shell' ? 70 : 0)); L.e = e; }
  fanG.rotation.x = t * 1.7;
  CTL.uPath.value = pathAt(t);
  const ds = dropState(t); dropM.position.set(HX, ds.y, HZ); dropM.scale.setScalar(ds.s); dropM.visible = t < 49.5 && ds.s > 0.002 && ds.hit < 0;
  const lvl = 24 + Math.min(40, ds.n * 2.2) + (ds.hit >= 0 ? 0 : 0);
  cupWater.scale.set(1, lvl, 1);
  const swapCup = eio(seg(t, 50.4, 51.6));
  cupG.position.x = -330 * swapCup; cupG.visible = swapCup < 0.999; potG.position.x = 330 * (1 - swapCup); potG.visible = swapCup > 0.001;
  const rv = eo(seg(t, K.roomIn[0], K.roomIn[1])) * (1 - eo(seg(t, K.roomOut[0], K.roomOut[1])));
  room.visible = rv > 0.001; room.scale.setScalar(0.25 + 0.75 * rv);
  sash.rotation.y = -0.62 * eo(seg(t, K.latch, K.latch + 1.4));
  for (const c of CO2) { const u = t - c.t, vis = u > 0 && room.visible; c.m.visible = vis; if (vis) { c.m.position.copy(c.p).add(V3(0, u * 38, Math.sin(u + c.p.x) * 14)); c.m.scale.setScalar(c.s * back(seg(u, 0, 0.4), 2)); } }
  for (const g of germs) { const u = t - g.t, vis = u > 0 && t < K.close[1]; g.m.visible = vis; if (vis) g.m.scale.setScalar(back(seg(u, 0, 0.35), 2.4)); }
  // dashed assembly guides while the shell and the coil are lifted (tone layer only; they grow with the lift)
  for (const l of guides.children) l.geometry.dispose(); guides.clear();
  const eS = Lshell.e, eC = Lcoil.e;
  if (eS > 0.02) for (const [x, z] of [[-410, 100], [410, 100], [-410, -100], [410, -100]]) { const a = V3(x, 150, z), b = V3(x, 150 + 270 * eS, z + 70 * eS); const g = new THREE.BufferGeometry().setFromPoints([a, b]); const l = new THREE.Line(g, gMat); l.computeLineDistances(); l.layers.set(GUIDE); guides.add(l); }
  if (eC > 0.02) for (const x of [-390, 390]) { const a = V3(x, 86, 0), b = V3(x, 86 + 130 * eC, 0); const g = new THREE.BufferGeometry().setFromPoints([a, b]); const l = new THREE.Line(g, gMat); l.computeLineDistances(); l.layers.set(GUIDE); guides.add(l); }
  root.updateMatrixWorld(true);
}
// section planes: a front-to-back sweep leaves the unit cut through its middle (z <= cz); it slides away before the dive, which cuts across the pan (x <= -172)
const clipPlane3 = new THREE.Plane();
function secZ(t) { if (t < K.sweep[0] - 0.3) return 400; const a = lerp(112, -2, eio(seg(t, K.sweep[0], K.sweep[1]))); const b = eio(seg(t, 35.2, 36.1)); const c = eio(seg(t, 38.9, 39.5)); return t < 35.2 ? a : lerp(-2, 400, b); }
function sweepClip(t) { const c = secZ(t); clipPlane.set(V3(0, 0, -1), c); return c; }
// ---------- Cameras: [az, el, ln(dist), target x, y, z, frame offset ox, oy] ----------
const mainCam = new THREE.PerspectiveCamera(18, PX / PY, 1, 30000);
const CAM = track([
  [0.0, [28, 14, L_(430), -442, -400, -126, -330, -40]],
  [2.6, [34, 15, L_(500), -442, -400, -126, -330, -40]],
  [5.2, [36, 10, L_(900), -400, -330, -110, -330, -40]],
  [7.4, [34, 10, L_(2500), -100, -170, -40, -360, -20]],
  [9.2, [30, 12, L_(2900), 0, -170, 0, -380, -20]],
  [13.8, [24, 14, L_(2800), 0, -170, 0, -380, -20]],
  [15.0, [58, 13, L_(2600), 0, -150, 0, -390, -20]],
  [21.8, [52, 12, L_(2500), 0, -150, 0, -390, -20]],
  [24.6, [16, 9, L_(8600), 450, -1100, 450, -430, -20]],
  [31.5, [10, 8, L_(9000), 450, -1150, 500, -430, -20]],
  [33.8, [10, 8, L_(6400), 150, -600, 100, -380, -20]],
  [35.4, [38, 16, L_(3100), 0, -170, 0, -380, -20]],
  [36.4, [52, 20, L_(1300), -120, -50, 0, -300, -40]],
  [37.8, [84, 22, L_(430), -172, -48, 0, -150, -30]],
  [38.7, [88, 24, L_(300), -172, -48, 0, 0, 0]],
  [39.3, [30, 14, L_(2800), -60, -190, -40, -300, -40]],
  [43.0, [26, 14, L_(2900), -60, -190, -40, -300, -40]],
  [47.4, [22, 12, L_(3000), -40, -170, -60, -330, -20]],
  [49.0, [20, 8, L_(1700), -300, -300, -110, -380, -20]],
  [52.0, [18, 8, L_(1000), -430, -380, -126, -330, -40]],
  [54.6, [16, 9, L_(3900), 0, -150, -40, -520, -20]],
  [57.5, [6, 8, L_(4100), 0, -150, -40, -530, -20]],
  [60.0, [0, 7.5, L_(4200), 0, -150, -40, -530, -20]],
]);
const tgtV = new THREE.Vector3();
function camFrom(arr, jit, cam = mainCam) {
  const [az, el, ld, lx, ly, lz, ox, oy] = arr; const dist = Math.exp(ld);
  tgtV.set(lx, ly, lz);
  const a = az * Math.PI / 180, e = el * Math.PI / 180;
  cam.position.set(tgtV.x + Math.sin(a) * Math.cos(e) * dist, tgtV.y + Math.sin(e) * dist, tgtV.z + Math.cos(a) * Math.cos(e) * dist);
  cam.up.set(0, 1, 0); cam.lookAt(tgtV);
  cam.near = clamp(dist * 0.02, 0.15, 60); cam.far = 30000; cam.updateMatrixWorld();
  cam.setViewOffset(PX, PY, ox + jit[0], oy + jit[1], PX, PY); cam.updateProjectionMatrix(); return cam;
}
const camAt = (t, jit = [0, 0]) => camFrom(CAM(t), jit);
const magCam = new THREE.PerspectiveCamera(18, 1, 1, 8000);
const MAGSZ = 560;
function magAt(t, jit = [0, 0]) {
  const u = seg(t, K.mag[0], K.mag[1]);
  const arr = [88 - 6 * u, 26 - 6 * u, L_(330 + 40 * u), -190, -47, 0, jit[0] + 0, jit[1] + 0];
  camFrom(arr, [0, 0], magCam); magCam.setViewOffset(MAGSZ, MAGSZ, jit[0], jit[1], MAGSZ, MAGSZ); magCam.aspect = 1; magCam.updateProjectionMatrix(); return magCam;
}
