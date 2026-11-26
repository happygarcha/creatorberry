// ---------- Scene state ----------
const clipPlane = new THREE.Plane();
const TBM_X0 = -150, TBM_X1 = -20;
const tbmX = t => lerp(TBM_X0, TBM_X1, eio(seg(t, K.tbmRun[0], K.tbmRun[1])));
function trainX(t) {
  if (t >= K.trainA[0] && t <= K.trainA[1]) return lerp(-330, 760, ei(seg(t, K.trainA[0], K.trainA[1])) * 0.5 + 0.5 * seg(t, K.trainA[0], K.trainA[1]));
  if (t >= K.trainC[0] && t <= K.trainC[1]) return lerp(-330, 520, seg(t, K.trainC[0], K.trainC[1]));
  if (t >= K.trainB[0] - 0.4 && t <= K.trainB[1]) return lerp(-330, 760, seg(t, K.trainB[0], K.trainB[1]) * 0.9 + 0.1 * ss(seg(t, K.trainB[0], K.trainB[1])));
  if (t >= K.stn[0] - 0.4 && t < K.out[0]) return -330;
  return 5000;
}
function setScene(t) {
  trainG.position.set(trainX(t), 0, 0); trainG.visible = trainX(t) < 4000;
  const inTbm = t >= K.cutA[1] - 0.1 && t < K.cutB[0] + 0.2;
  tbmG.visible = inTbm; CTL.uBuilt.value = inTbm ? tbmX(t) - 2 : 1e5;
  if (inTbm) { tbmG.position.set(tbmX(t), 0, 0); headG.rotation.x = t * 1.6; }
  for (const b of boats) { const u = b.userData; b.position.set(u.cx + u.A * Math.sin(u.w * (t - 63.5)), Math.sin(t * 1.3 + u.cx) * 0.7 + 0.2, u.z); }
  for (const f of fishes) { const u = f.userData; f.position.x = -200 + ((u.x0 + 200 + 9 * t) % 400); f.position.y = u.y + Math.sin(t * 2 + u.ph) * 4; f.rotation.z = Math.sin(t * 3 + u.ph) * 0.06; }
  for (const f of floors) { const u = t - f.t, vis = t > K.floors[0] - 0.01 && t < K.floors[1] + 4; f.m.visible = vis && u > 0; if (f.m.visible) f.m.scale.set(back(seg(u, 0, 0.35), 1.8), 1, 1); }
  root.updateMatrixWorld(true);
}
function secZ(t) { return t < K.sweep[0] ? 45 : lerp(45, 0, eio(seg(t, K.sweep[0], K.sweep[1]))); }
function sweepClip(t) { clipPlane.set(V3(0, 0, -1), secZ(t)); }
// ---------- Cameras: [az, el, ln(dist), target x, y, z, frame offset ox, oy] ----------
const mainCam = new THREE.PerspectiveCamera(18, PX / PY, 1, 30000);
const CAM = track([
  [0.0, [26, 12, L_(1150), -20, 20, 0, -320, -20]],
  [3.0, [22, 11, L_(1100), -20, 10, 0, -320, -20]],
  [6.4, [8, 7, L_(1000), -40, -30, 0, -320, -20]],
  [9.6, [4, 5, L_(900), -120, -80, 0, -330, -20]],
  [11.4, [16, 6, L_(350), -290, -135, 0, -300, -20]],
  [22.4, [12, 6, L_(350), 500, -135, 0, -300, -20]],
  [25.2, [0, 3, L_(1500), 0, -90, 0, -300, -20]],
  [34.2, [0, 4, L_(1480), 0, -90, 0, -300, -20]],
  [35.3, [28, 9, L_(500), -140, -122, 0, -240, -10]],
  [41.0, [26, 8, L_(480), -85, -122, 0, -240, -10]],
  [46.8, [24, 8, L_(500), -10, -122, 0, -240, -10]],
  [47.6, [10, 6, L_(620), -346, -80, 0, -300, -10]],
  [54.0, [5, 3, L_(560), -346, -80, 0, -300, -10]],
  [58.4, [4, 3, L_(560), -346, -80, 0, -300, -10]],
  [58.7, [20, 10, L_(800), -250, -40, 0, -300, -10]],
  [62.2, [24, 12, L_(1250), -20, 10, 0, -330, -20]],
  [66.4, [28, 13, L_(1350), 0, 10, 0, -360, -20]],
  [74.0, [28, 13, L_(1350), 0, 10, 0, -360, -20]],
]);
const tgtV = new THREE.Vector3();
function camFrom(arr, jit, cam = mainCam) {
  const [az, el, ld, lx, ly, lz, ox, oy] = arr; const dist = Math.exp(ld);
  tgtV.set(lx, ly, lz);
  const a = az * Math.PI / 180, e = el * Math.PI / 180;
  cam.position.set(tgtV.x + Math.sin(a) * Math.cos(e) * dist, tgtV.y + Math.sin(e) * dist, tgtV.z + Math.cos(a) * Math.cos(e) * dist);
  cam.up.set(0, 1, 0); cam.lookAt(tgtV);
  cam.near = clamp(dist * 0.02, 0.5, 60); cam.far = 30000; cam.updateMatrixWorld();
  cam.setViewOffset(PX, PY, ox + jit[0], oy + jit[1], PX, PY); cam.updateProjectionMatrix(); return cam;
}
const camAt = (t, jit = [0, 0]) => camFrom(Q.get('thumb') ? [24, 13, L_(1300), 0, -10, 0, -470, -30] : CAM(t), jit);
