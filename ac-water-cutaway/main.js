// AC water: DON'T DRINK IT · Line-Art Cutaway film (60 s). Model in millimetres, traced live from normal/depth edges (three line weights);
// one accent colour (#0a84ff) only for the water path. Page contract: window.render(t), window.DUR, window.EV, window.TEXTS, window.READY.
import * as THREE from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { clamp, lerp, seg, eio, eo, ei, ss, back, track, mulberry } from '/core/lib.js';

THREE.ColorManagement.enabled = false;
const Q = new URLSearchParams(location.search);
const TLJ = await (await fetch('timeline.json')).json();
const FILM = TLJ.end;
const FROM = +(Q.get('from') ?? 0), TO = +(Q.get('to') ?? FILM);
const SUBS = Q.get('subs') !== '0';
const PX = 1920, PY = 1080, SS = +(Q.get('ss') || 2), JIT = +(Q.get('jit') || 8);
const PAPER = '#f6f5f0', INK = '#141414', GRAPH = '#5a5955', FAINT = '#8a8984', ACC = '#0a84ff', ACC_GL = 0x0a84ff;
const SANS = '"Plex Sans", sans-serif', MONO = '"Plex Mono", monospace';
const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
const L_ = Math.log;

// ---------- Timeline (whole-film seconds; narration: v1 0.8, v2 5.4, v3 14.5, v4 22.8, v5 34.4, v6 39.3, v7 50.4) ----------
const K = {
  title1: [0.9, 4.7],
  sweep: [5.6, 8.9], pathRun: [8.4, 13.4], lblCoil: [7.2, 12.6], lblPan: [9.4, 12.8], lblPipe: [10.6, 13.6],
  moist: [14.6, 21.5], gauge: [14.8, 19.4], dryNote: [15.4, 21.8],
  roomIn: [22.4, 24.6], co2: [24.6, 31.4], sleep: [29.3, 33.2], latch: 31.4, fresh: [31.7, 33.9],
  roomOut: [33.7, 34.9],
  catch: [34.4, 39.0], lift: 34.7, liftStep: 0.45, liftDur: 1.1, dive: [36.0, 38.6], clipOn: 36.0, cut: 38.7, iris: [38.9, 39.7],
  mag: [39.6, 48.6], germs: [40.2, 45.0], metals: [45.5, 48.4], flood: [39.4, 41.4],
  close: [48.5, 50.3], carry: [50.3, 53.2], plant: [51.0, 52.0], title2: [50.4, 53.2],
  trace: [53.0, 55.0], block: [54.2, 59.9],
  hatch: [59.2, 59.8], irisC: [59.9, 60.7], card: 60.0, logo: [60.15, 60.9],
};
const VO = TLJ.vo;
const LOGO = new Image(); LOGO.src = 'logo.png'; await LOGO.decode();
const W8 = [[-0.6, 0.1], [0.24, 0.48], [0.48, 0.64], [0.64, 0.92]].map(([a]) => VO.v8 + Math.max(0, a));   // like, share, and, subscribe word starts
const T_LIKE = W8[0], T_SHARE = W8[1], T_SUB = W8[3];
// ---------- Renderer ----------
const canvas = document.getElementById('gl');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: true, premultipliedAlpha: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(PX, PY, false);
renderer.outputColorSpace = THREE.LinearSRGBColorSpace;
renderer.setClearColor(0xffffff, 0);
renderer.autoClear = false;

// ---------- Material: one shader, two modes (0 = greyscale tone, 1 = normal + linear depth) ----------
const U = { uMode: { value: 0 } };
const CTL = { uPath: { value: 0 } };        // the water path parameter: everything with aS < uPath is lit in the accent
const VS = `
#include <clipping_planes_pars_vertex>
attribute float aS;
varying vec3 vN; varying vec3 vWN; varying vec2 vUv; varying float vVZ; varying vec3 vWP; varying float vS;
void main(){
  vec4 mvPosition = modelViewMatrix * vec4(position,1.);
  vN = normalize(normalMatrix*normal);
  vWN = normalize(mat3(modelMatrix)*normal);
  vUv = uv; vVZ = -mvPosition.z; vWP = (modelMatrix*vec4(position,1.)).xyz; vS = aS;
  gl_Position = projectionMatrix*mvPosition;
  #include <clipping_planes_vertex>
}`;
const FS = `
#include <clipping_planes_pars_fragment>
uniform float uMode; uniform vec3 uColor; uniform vec3 uColor0; uniform float uKind; uniform float uPath;
varying vec3 vN; varying vec3 vWN; varying vec2 vUv; varying float vVZ; varying vec3 vWP; varying float vS;
float hatch(float period){ float h = mod(gl_FragCoord.x + gl_FragCoord.y, period); return smoothstep(0.6, 1.6, h) * (1. - smoothstep(2.6, 3.6, h)); }
void main(){
  #include <clipping_planes_fragment>
  if(uMode>0.5){
    vec3 n = normalize(vN); if(!gl_FrontFacing) n = vec3(0.,0.,1.);
    gl_FragColor = vec4(n, vVZ); return;
  }
  vec3 col = uColor; bool lit = false; float head = 0.;
  if(uKind>2.5 && uKind<3.5){                      // water path: lit along vS up to uPath
    lit = vS < uPath;
    head = lit ? smoothstep(.045, 0., uPath - vS) * step(uPath, .999) : 0.;
    col = lit ? mix(uColor, vec3(.70,.86,1.), head*.65) : uColor0;
  }
  if(uKind>6.5 && uKind<7.5){ lit = true; }        // always accent (the drop, the glass water)
  if(!gl_FrontFacing){                              // section faces: hatching; a lit path stays solid
    vec3 c = lit ? col : mix(vec3(.90), vec3(.34), hatch(10.));
    gl_FragColor = vec4(c,1.); return;
  }
  vec3 n = normalize(vWN);
  vec3 L = normalize(vec3(-.35,1.,.55));
  float d = max(dot(n,L),0.);
  float tone = .82 + .18*d + .03*n.y;
  if(uKind>3.5 && uKind<4.5 && !lit){ col = mix(vec3(.88), vec3(.56), hatch(10.)); tone = 1.; }   // plastic: light grey hatching
  if(lit) tone = .94 + .06*d;
  gl_FragColor = vec4(col*min(tone,1.0), 1.);
}`;
function mat(hex, kind = 0, hex0 = null, clip = true) {
  return new THREE.ShaderMaterial({
    uniforms: { uMode: U.uMode, uPath: CTL.uPath, uColor: { value: new THREE.Color(hex) }, uColor0: { value: new THREE.Color(hex0 ?? hex) }, uKind: { value: kind } },
    vertexShader: VS, fragmentShader: FS, side: THREE.DoubleSide, clipping: clip });
}
const M = {
  white: mat(0xfbfbf9), shell: mat(0xf2f2ee), plastic: mat(0xe6e6e2, 4), metal: mat(0xededea), metal2: mat(0xdcdcd8), fin: mat(0xf4f4f0),
  copper: mat(0xd9d4cc), dark: mat(0x555553), mid: mat(0x9a9a97), glass: mat(0xf0f0ec),
  glassF: Object.assign(mat(0xf0f0ec), {}), path: mat(ACC_GL, 3, 0xdededa), accent: mat(ACC_GL, 7), room: mat(0xf8f8f5), cloth: mat(0xe8e8e4), germ: mat(0x4a4a49),
};
M.glassF.side = THREE.FrontSide;
const RM = { room: mat(0xf8f8f5, 0, null, false), cloth: mat(0xe8e8e4, 0, null, false), frame: mat(0xdcdcd8, 0, null, false), glass: mat(0xf0f0ec, 0, null, false), co2: mat(0x9a9a97, 0, null, false) };
const scene = new THREE.Scene();
const root = new THREE.Group(); scene.add(root);
// ---------- Geometry helpers (mm) ----------
const box = (w, h, d, x, y, z) => new THREE.BoxGeometry(w, h, d).translate(x, y + h / 2, z);
const cylX = (r, len, x, y, z, s = 20) => new THREE.CylinderGeometry(r, r, len, s).rotateZ(Math.PI / 2).translate(x, y, z);
function extX(pts, x0, x1) {                 // polygon in (z, y) extruded along x from x0 to x1
  const sh = new THREE.Shape(); pts.forEach(([z, y], i) => i ? sh.lineTo(z, y) : sh.moveTo(z, y));
  const g = new THREE.ExtrudeGeometry(sh, { depth: x1 - x0, bevelEnabled: false }); g.rotateY(-Math.PI / 2); g.translate(x1, 0, 0); return g;
}
function clean(g) { g = g.index ? g.toNonIndexed() : g; for (const k of Object.keys(g.attributes)) if (!['position', 'normal', 'uv', 'aS'].includes(k)) g.deleteAttribute(k); if (!g.attributes.uv) g.setAttribute('uv', new THREE.BufferAttribute(new Float32Array(g.attributes.position.count * 2), 2)); return g; }
function add(group, geos, m) {
  if (!geos.length) return null;
  const gs = geos.map(clean);
  if (gs.some(g => g.attributes.aS)) gs.forEach(g => { if (!g.attributes.aS) g.setAttribute('aS', new THREE.BufferAttribute(new Float32Array(g.attributes.position.count), 1)); });
  else gs.forEach(g => g.deleteAttribute('aS'));
  const mesh = new THREE.Mesh(mergeGeometries(gs), m); group.add(mesh); return mesh;
}
function setS(g, fn) {
  const p = g.attributes.position, a = new Float32Array(p.count);
  for (let i = 0; i < p.count; i++) a[i] = fn(p.getX(i), p.getY(i), p.getZ(i), i);
  g.setAttribute('aS', new THREE.BufferAttribute(a, 1)); return g;
}
const rng = mulberry(20261126);
const LAYERS = [];
function layer(name, idx) { const g = new THREE.Group(); g.name = name; root.add(g); const L = { g, name, idx }; LAYERS.push(L); return L; }

// ---------- The indoor unit: 840 × 300 × 210 mm, wall side at -z, centre at the origin ----------
const AX = 420;                                   // half width
const Lback = layer('back', 0), Lpan = layer('pan', 0), Lfan = layer('fan', 0), Lcoil = layer('coil', 1), Lshell = layer('shell', 2);
// back plate with a mounting rail and the tube bundle exit
add(Lback.g, [box(840, 300, 5, 0, -150, -108), box(700, 18, 6, 0, 120, -103), box(700, 18, 6, 0, -138, -103)], M.plastic);
// shell: front panel, top cover with grille ribs, two end caps, chin and louvre
add(Lshell.g, [box(840, 252, 5, 0, -102, 103), box(840, 5, 206, 0, 147, 0), box(5, 300, 206, -420, -150, 0), box(5, 300, 206, 420, -150, 0), box(840, 48, 5, 0, -150, 103)], M.shell);
{ const ribs = []; for (let i = 0; i < 22; i++) ribs.push(box(800, 2.2, 3, 0, 152, -80 + i * 7.2)); add(Lshell.g, ribs, M.metal2); }
add(Lshell.g, [box(780, 5, 54, 0, -146, 64).rotateX(-0.35)], M.white);          // outlet louvre
// cross-flow fan (spins slowly): 18 blades between two end discs
const fanG = new THREE.Group(); fanG.position.set(0, -98, 14); Lfan.g.add(fanG);
{ const bl = [];
  for (let k = 0; k < 18; k++) { const a = k * Math.PI * 2 / 18; const g = new THREE.BoxGeometry(740, 20, 1.6); const m = new THREE.Matrix4().makeRotationX(a + 0.5); m.setPosition(0, 30 * Math.sin(a), 30 * Math.cos(a)); g.applyMatrix4(m); bl.push(g); }
  add(fanG, bl, M.metal); add(fanG, [cylX(42, 3, -372, 0, 0, 32), cylX(42, 3, 372, 0, 0, 32), cylX(42, 3, 0, 0, 0, 32)], M.metal2); add(fanG, [cylX(5, 760, 0, 0, 0, 12)], M.mid); }
// evaporator coil: 56 aluminium fins (Λ-shaped band, 0.8 mm) + 6 copper tubes + lead-solder joints
const COIL_OUT = [[-62, -34], [0, 86], [62, -34], [50, -34], [0, 60], [-50, -34]];
{ const fins = []; for (let i = 0; i < 56; i++) { const x = -380 + i * (760 / 55); fins.push(extX(COIL_OUT, x - 0.4, x + 0.4)); }
  add(Lcoil.g, fins, M.fin);
  const tub = [], sol = [];
  for (const f of [0.25, 0.55, 0.85]) for (const sd of [-1, 1]) { const z = sd * (56 - 56 * f), y = -34 + 107 * f; tub.push(cylX(3.4, 790, 0, y, z, 14)); }
  add(Lcoil.g, tub, M.copper);
  for (let i = 0; i < 8; i++) for (const sd of [-1, 1]) { const x = -396 + (i < 4 ? 0 : 1) * 0 + (i % 4) * 4; if (i < 4) sol.push(new THREE.SphereGeometry(5.5, 10, 8).translate(x + (i % 2) * 2, -4 + (i % 3) * 14, sd * 38)); }
  add(Lcoil.g, sol, M.dark); }
// water path (one accent): coil bottom edges (0–0.2) → drain pan (0.2–0.6, flows toward -x) → drain hose (0.6–1.0)
{ const dr = [];
  for (const sd of [-1, 1]) for (let i = 0; i < 20; i++) { const x = -370 + i * 39 + (sd > 0 ? 14 : 0), g = new THREE.SphereGeometry(3.6, 10, 8).translate(x, -39, sd * 57); dr.push(setS(g, () => 0.02 + 0.18 * ((x + 400) / 800))); }
  add(Lpan.g, dr, M.path);
  const film = []; for (const sd of [-1, 1]) film.push(setS(box(760, 1.8, 7, 0, -37, sd * 58), (x) => 0.02 + 0.18 * ((x + 400) / 800)));
  add(Lpan.g, film, M.path);
  add(Lpan.g, [extX([[-84, -30], [-74, -58], [74, -58], [84, -30], [77, -30], [68, -52], [-68, -52], [-77, -30]], -400, 400)], M.white);
  add(Lpan.g, [setS(box(796, 4.5, 126, 0, -52, 0), (x) => 0.2 + 0.4 * ((400 - x) / 800))], M.path);
  const curve = new THREE.CatmullRomCurve3([V3(-400, -50, 0), V3(-428, -52, -40), V3(-442, -62, -92), V3(-442, -90, -126), V3(-442, -260, -126), V3(-442, -380, -126)]);
  const tube = new THREE.TubeGeometry(curve, 90, 9, 14, false);
  add(Lpan.g, [setS(tube, (x, y, z, i) => 0.6 + 0.4 * (Math.floor(i / 15) / 90))], M.path);
  HOSE_CURVE = curve; }
var HOSE_CURVE;
const GUIDE = 2;
renderer.localClippingEnabled = true;
const unitMats = Object.values(M);          // only the AC unit is cut: the bedroom, the cup and the plant are never clipped
function setClip(p) { for (const m of unitMats) m.clippingPlanes = p.length ? p : null; }
// ---------- Post: tracing + downsampled accumulation ----------
const quadCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
const quadGeo = new THREE.PlaneGeometry(2, 2);
const VQ = `varying vec2 vUv; void main(){ vUv=uv; gl_Position=vec4(position.xy,0.,1.); }`;
const edgeMat = new THREE.ShaderMaterial({
  uniforms: { tC: { value: null }, tN: { value: null }, px: { value: new THREE.Vector2() }, rS: { value: 2.7 }, rO: { value: 1.7 }, rC: { value: 1.05 }, thD: { value: 0.0016 }, thO: { value: 0.012 }, thN: { value: 0.12 } },
  vertexShader: VQ,
  fragmentShader: `
  uniform sampler2D tC, tN; uniform vec2 px; uniform float rS, rO, rC, thD, thO, thN; varying vec2 vUv;
  float iz(vec4 s){ return s.a>0. ? 1./s.a : 0.; }
  void main(){
    vec4 c = texture2D(tC, vUv); vec4 n0 = texture2D(tN, vUv); float z0 = iz(n0); bool f0 = n0.a > 0.;
    float hf = abs(c.a - .5) < .2 ? 1. : 0.;
    float dS = 99.;
    for(int i=0;i<16;i++){
      float a = float(i)*0.392699; vec2 d = vec2(cos(a), sin(a));
      for(int k=1;k<=4;k++){ float r = float(k)*rS*0.3; vec2 o = vUv + d*px*r; vec4 s = texture2D(tN, o);
        if((s.a>0.) != f0){ dS = min(dS, r); }
        if(k<=2){ float ca = texture2D(tC, o).a; if(abs(ca - .5) < .2) hf = 1.; } }
    }
    float eS = hf > .5 ? 1. - smoothstep(rS*0.3, rS*0.62, dS) : 1. - smoothstep(rS*0.62, rS*1.12, dS);
    float eO = 0., eC = 0.;
    vec2 dirs[4]; dirs[0]=vec2(1.,0.); dirs[1]=vec2(0.,1.); dirs[2]=vec2(.7071,.7071); dirs[3]=vec2(.7071,-.7071);
    for(int i=0;i<4;i++){
      vec4 a = texture2D(tN, vUv + dirs[i]*px*rO), b = texture2D(tN, vUv - dirs[i]*px*rO);
      if(f0 && a.a>0. && b.a>0.){
        float za = iz(a), zb = iz(b), m = max(z0, max(za, zb));
        eO = max(eO, smoothstep(thO, thO*1.8, abs(za + zb - 2.*z0) / m));
      }
      vec4 a2 = texture2D(tN, vUv + dirs[i]*px*rC), b2 = texture2D(tN, vUv - dirs[i]*px*rC);
      if(f0 && a2.a>0. && b2.a>0.){
        float za = iz(a2), zb = iz(b2), m = max(z0, max(za, zb));
        eC = max(eC, smoothstep(thD, thD*2.2, abs(za + zb - 2.*z0) / m));
        eC = max(eC, smoothstep(thN, thN*1.8, 1.-dot(n0.xyz, a2.xyz)));
        eC = max(eC, smoothstep(thN, thN*1.8, 1.-dot(n0.xyz, b2.xyz)));
      }
    }
    vec3 inkS = vec3(.078), inkO = vec3(.11), inkC = vec3(.25);
    float wS = eS, wO = eO*.95, wC = eC*.78;
    if(hf > .5){ wO *= .8; wC *= .75; inkS = vec3(.30); inkO = vec3(.36); inkC = vec3(.52); }
    float e = max(wS, max(wO, wC));
    vec3 ink = wS >= max(wO, wC) ? inkS : (wO >= wC ? inkO : inkC);
    vec3 col = mix(c.rgb, ink, e);
    float al = max(c.a > .01 ? 1. : 0., e);
    gl_FragColor = vec4(col*al, al);
  }`, depthTest: false, depthWrite: false, blending: THREE.NoBlending });
const downMat = new THREE.ShaderMaterial({
  uniforms: { tE: { value: null }, px: { value: new THREE.Vector2() }, w: { value: 1 } },
  vertexShader: VQ,
  fragmentShader: `
  uniform sampler2D tE; uniform vec2 px; uniform float w; varying vec2 vUv;
  void main(){
    vec4 s = texture2D(tE, vUv + px*vec2(.5,.5)) + texture2D(tE, vUv + px*vec2(-.5,.5)) + texture2D(tE, vUv + px*vec2(.5,-.5)) + texture2D(tE, vUv + px*vec2(-.5,-.5));
    gl_FragColor = s*.25*w;
  }`, depthTest: false, depthWrite: false, transparent: true,
  blending: THREE.CustomBlending, blendEquation: THREE.AddEquation, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor });
const copyMat = new THREE.ShaderMaterial({
  uniforms: { tA: { value: null }, circ: { value: new THREE.Vector3() }, size: { value: new THREE.Vector2() }, fadeA: { value: new THREE.Vector2() }, fadeB: { value: new THREE.Vector2() }, fadeOn: { value: 0 } }, vertexShader: VQ,
  fragmentShader: `uniform sampler2D tA; uniform vec3 circ; uniform vec2 size; uniform vec2 fadeA, fadeB; uniform float fadeOn; varying vec2 vUv;
  void main(){ vec4 s = texture2D(tA, vUv); s = vec4(min(s.rgb, vec3(s.a)), min(s.a, 1.));
    if(fadeOn > .5){ vec2 p = vec2(vUv.x, 1. - vUv.y)*size; vec2 ab = fadeB - fadeA; float u = dot(p - fadeA, ab) / dot(ab, ab); s *= 1. - smoothstep(0., 1., u); }
    if(circ.z > 0.){ float d = distance(vUv*size, circ.xy); if(d > circ.z) discard;
      vec3 paper = vec3(.965,.961,.941); gl_FragColor = vec4(s.rgb + paper*(1.-s.a), 1.); return; }
    gl_FragColor = s; }`,
  depthTest: false, depthWrite: false, blending: THREE.NoBlending });
const quad = new THREE.Mesh(quadGeo, edgeMat); const quadScene = new THREE.Scene(); quadScene.add(quad);
const RT = {};
function targets(key, w, h) {
  if (RT[key]) return RT[key];
  const lin = { minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter };
  RT[key] = {
    c: new THREE.WebGLRenderTarget(w * SS, h * SS, { type: THREE.UnsignedByteType, ...lin }),
    n: new THREE.WebGLRenderTarget(w * SS, h * SS, { type: THREE.FloatType, minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter }),
    e: new THREE.WebGLRenderTarget(w * SS, h * SS, { type: THREE.UnsignedByteType, ...lin }),
    a: new THREE.WebGLRenderTarget(w, h, { type: THREE.HalfFloatType, ...lin }),
  };
  return RT[key];
}
function pass(t, cam, opt, wgt) {
  setClip(opt.clip || []);
  U.uMode.value = 1; cam.layers.set(0);
  scene.traverse(o => { if (o.userData.noND) o.visible = false; });
  renderer.setRenderTarget(t.n); renderer.setClearColor(0x000000, 0); renderer.clear(); renderer.render(scene, cam);
  scene.traverse(o => { if (o.userData.noND) o.visible = true; });
  U.uMode.value = 0; cam.layers.set(0); if (opt.guides) cam.layers.enable(GUIDE);
  renderer.setRenderTarget(t.c); renderer.setClearColor(0xffffff, 0); renderer.clear(); renderer.render(scene, cam);
  setClip([]);
  quad.material = edgeMat; edgeMat.uniforms.tC.value = t.c.texture; edgeMat.uniforms.tN.value = t.n.texture;
  edgeMat.uniforms.px.value.set(1 / t.c.width, 1 / t.c.height);
  renderer.setRenderTarget(t.e); renderer.clear(); renderer.render(quadScene, quadCam);
  quad.material = downMat; downMat.uniforms.tE.value = t.e.texture; downMat.uniforms.px.value.set(1 / t.e.width, 1 / t.e.height); downMat.uniforms.w.value = wgt;
  renderer.setRenderTarget(t.a); renderer.render(quadScene, quadCam);
}
const JOFF = [[-0.125, -0.375], [0.375, -0.125], [0.125, 0.375], [-0.375, 0.125], [0, 0], [0.25, 0.25], [-0.25, 0.25], [0.25, -0.25]];
const SHUTTER = 0.12 / 24;
// rect: screen pixels (origin top left); setup(dt, jitter) poses the scene and returns the camera
function renderView(key, rect, setup, opt = {}) {
  const t = targets(`${key}-${rect.w}x${rect.h}`, rect.w, rect.h);     // targets cached by size: as the magnifier grows it can't reuse a smaller target
  renderer.setRenderTarget(t.a); renderer.setClearColor(0x000000, 0); renderer.clear();
  for (let k = 0; k < JIT; k++) {
    const dt = JIT > 1 ? (k / (JIT - 1) - 0.5) * SHUTTER : 0;
    const r = setup(dt, JOFF[k % JOFF.length]);
    pass(t, r.cam, { ...opt, clip: r.clip || [] }, 1 / JIT);
  }
  quad.material = copyMat; copyMat.uniforms.tA.value = t.a.texture;
  copyMat.uniforms.fadeOn.value = 0;
  copyMat.uniforms.size.value.set(rect.w, rect.h); copyMat.uniforms.circ.value.set(rect.w / 2, rect.h / 2, opt.circle ? rect.w / 2 : 0);
  renderer.setRenderTarget(null); renderer.setViewport(rect.x, PY - rect.y - rect.h, rect.w, rect.h); renderer.setScissor(rect.x, PY - rect.y - rect.h, rect.w, rect.h); renderer.setScissorTest(true);
  renderer.render(quadScene, quadCam); renderer.setScissorTest(false); renderer.setViewport(0, 0, PX, PY);
}

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
const camAt = (t, jit = [0, 0]) => camFrom(Q.get('thumb') ? [30, 13, L_(2050), 0, -180, 0, -470, -30] : CAM(t), jit);
const magCam = new THREE.PerspectiveCamera(18, 1, 1, 8000);
const MAGSZ = 560;
function magAt(t, jit = [0, 0]) {
  const u = seg(t, K.mag[0], K.mag[1]);
  const arr = [88 - 6 * u, 26 - 6 * u, L_(330 + 40 * u), -190, -47, 0, jit[0] + 0, jit[1] + 0];
  camFrom(arr, [0, 0], magCam); magCam.setViewOffset(MAGSZ, MAGSZ, jit[0], jit[1], MAGSZ, MAGSZ); magCam.aspect = 1; magCam.updateProjectionMatrix(); return magCam;
}
// ---------- 2D: paper, labels, subtitles ----------
const bg = document.getElementById('bg').getContext('2d');
const ov = document.getElementById('ov').getContext('2d');
function proj(v, cam = mainCam) { const p = v.clone().project(cam); return [(p.x + 1) / 2 * PX, (1 - p.y) / 2 * PY, p.z]; }
function drawPaper() {
  bg.fillStyle = PAPER; bg.fillRect(0, 0, PX, PY);
  bg.strokeStyle = 'rgba(20,20,20,0.04)'; bg.lineWidth = 1;
  for (let x = 0; x <= PX; x += 40) { bg.beginPath(); bg.moveTo(x + .5, 0); bg.lineTo(x + .5, PY); bg.stroke(); }
  for (let y = 0; y <= PY; y += 40) { bg.beginPath(); bg.moveTo(0, y + .5); bg.lineTo(PX, y + .5); bg.stroke(); }
  bg.strokeStyle = 'rgba(20,20,20,0.15)';
  for (let x = 40; x < PX; x += 200) for (let y = 40; y < PY; y += 200) { bg.beginPath(); bg.moveTo(x - 5, y + .5); bg.lineTo(x + 6, y + .5); bg.moveTo(x + .5, y - 5); bg.lineTo(x + .5, y + 6); bg.stroke(); }
}
// entry: traced left to right; exit: wiped left to right (out = 0..1)
let CAPTURE = null;                 // window.TEXTS: records the text on screen in this frame (a whole text is reported from its first frame and no longer once its exit starts)
function wipeText(c, text, x, y, p, font, color, spacing = 0, out = 0) {
  if (p <= 0 || out >= 1) return 0;
  if (CAPTURE && out <= 0) { const px = +(/(\d+(?:\.\d+)?)px/.exec(font) || [0, 20])[1]; const w = textW(text, font, spacing); CAPTURE.push({ id: text, text, x0: Math.round(x), y0: Math.round(y - px), x1: Math.round(x + w), y1: Math.round(y + px * 0.3) }); }
  c.save(); c.font = font; c.fillStyle = color; c.textBaseline = 'alphabetic';
  if (spacing) c.letterSpacing = spacing + 'px';
  const w = c.measureText(text).width;
  const x0 = x - 4 + (w + 8) * eio(out), x1 = x - 4 + (w + 8) * eo(p);
  c.beginPath(); c.rect(x0, y - 200, Math.max(0, x1 - x0), 260); c.clip();
  c.fillText(text, x, y); c.restore(); return w;
}
function textW(text, font, spacing = 0) { ov.save(); ov.font = font; if (spacing) ov.letterSpacing = spacing + 'px'; const w = ov.measureText(text).width; ov.restore(); return w; }
function badge(c, x, y, label, p, accent = false, r = 15) {
  if (p <= 0) return;
  const s = back(p, 2.2);
  c.save(); c.translate(x, y); c.scale(s, s); c.beginPath(); c.arc(0, 0, r, 0, Math.PI * 2);
  if (accent) { c.fillStyle = ACC; c.fill(); c.fillStyle = '#fff'; } else { c.fillStyle = PAPER; c.fill(); c.lineWidth = 1.8; c.strokeStyle = INK; c.stroke(); c.fillStyle = INK; }
  c.font = `600 ${r * 1.08}px ${SANS}`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(label, 0, 1); c.restore();
}
function dot(c, x, y, col = INK, r = 3.2) { c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.fillStyle = col; c.fill(); }
function polyGrow(c, pts, p) {
  if (p <= 0) return null;
  const L = []; let tot = 0; for (let i = 1; i < pts.length; i++) { const l = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); L.push(l); tot += l; }
  let rem = tot * clamp(p); c.beginPath(); c.moveTo(pts[0][0], pts[0][1]); let end = pts[0];
  for (let i = 1; i < pts.length && rem > 0; i++) { const u = Math.min(1, rem / L[i - 1]); end = [lerp(pts[i - 1][0], pts[i][0], u), lerp(pts[i - 1][1], pts[i][1], u)]; c.lineTo(end[0], end[1]); rem -= L[i - 1]; }
  c.stroke(); return end;
}
// labels that follow a part: label placed beside the anchor at (dx, dy), a horizontal run + a leader to the anchor; shown within t0..t1, traced on entry, wiped on exit
function tag(c, t, [t0, t1], anchor, { dx, dy, name, spec, accent = false, bars = null }) {
  const u = t - t0; if (u <= 0 || t >= t1 + 0.45) return;
  const out = seg(t, t1, t1 + 0.4);
  const col = accent ? ACC : INK;
  const nameFont = `600 21px ${SANS}`;
  const nw = textW(name, nameFont, 1.4);
  const left = dx < 0;                      // when the label is left of the anchor, right-align the text to the bend
  const lx = anchor[0] + dx, ly = anchor[1] + dy;
  const tx = left ? lx - nw : lx + 12;
  c.save(); c.globalAlpha = 1 - out * 0.15;
  c.strokeStyle = col; c.lineWidth = 1.3;
  const knee = [left ? lx + 8 : lx, ly - 7];
  polyGrow(c, [anchor, knee, [left ? tx - 10 : tx + nw + 10, ly - 7]].slice(0, 2), seg(u, 0, 0.35) * (1 - out));
  if (seg(u, 0.05, 0.2) > 0 && out < 1) dot(c, anchor[0], anchor[1], col, 3.4 * back(seg(u, 0.02, 0.18), 2));
  wipeText(c, name, tx, ly, seg(u, 0.18, 0.5), nameFont, col, 1.4, out);
  if (spec) wipeText(c, spec, tx, ly + 25, seg(u, 0.3, 0.7), `400 15px ${MONO}`, GRAPH, 0, out);
  if (bars) drawBars(c, tx, ly + (spec ? 40 : 18), bars, seg(u, 0.25, 0.6) * (1 - out));
  c.restore();
}
// signal bars: n = current bar count (may be fractional; bars go hollow one by one as they drop)
function drawBars(c, x, y, n, p) {
  if (p <= 0) return;
  c.save(); c.globalAlpha *= p;
  c.font = `500 12px ${MONO}`; c.fillStyle = FAINT; c.letterSpacing = '2px'; c.fillText('SIGNAL', x, y + 22);
  for (let i = 0; i < 5; i++) {
    const h = 6 + i * 4, bx = x + 74 + i * 11, by = y + 24 - h;
    const f = clamp(n - i);
    c.strokeStyle = INK; c.lineWidth = 1.2; c.strokeRect(bx + .5, by + .5, 7, h);
    if (f > 0) { c.fillStyle = INK; c.fillRect(bx + .5, by + .5 + h * (1 - f), 7, h * f); }
  }
  c.restore();
}
// radiation arcs: outward from the antenna segment, k = strength 0..1
function arcs(c, p, away, t, k) {
  if (k <= 0.01) return;
  const ang = Math.atan2(away[1], away[0]);
  c.save(); c.strokeStyle = ACC;
  for (let i = 0; i < 3; i++) {
    const ph = ((t * 0.8 + i / 3) % 1);
    const r = 26 + ph * 90 * (0.35 + 0.65 * k);
    c.globalAlpha = k * (1 - ph) * 0.9; c.lineWidth = 2.2 * (1 - ph) + 0.6;
    c.beginPath(); c.arc(p[0], p[1], r, ang - 0.8, ang + 0.8); c.stroke();
  }
  c.restore();
}
// dimension line (two screen-space endpoints, offset off along the normal)
function dimLine(c, a, b, off, text, p = 1, al = 1, ticks = 0) {
  if (p <= 0 || al <= 0) return;
  c.save(); c.globalAlpha = al;
  const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy), nx = -dy / L * off, ny = dx / L * off;
  const A = [a[0] + nx, a[1] + ny], Bp = [b[0] + nx, b[1] + ny];
  const q1 = seg(p, 0, 0.3), q2 = seg(p, 0.15, 0.8), q3 = seg(p, 0.6, 1);
  c.strokeStyle = INK; c.fillStyle = INK; c.lineWidth = 1;
  if (off) { c.beginPath(); c.moveTo(a[0] + nx * 0.15, a[1] + ny * 0.15); c.lineTo(lerp(a[0] + nx * .15, A[0] + nx * .12, q1), lerp(a[1] + ny * .15, A[1] + ny * .12, q1));
    c.moveTo(b[0] + nx * 0.15, b[1] + ny * 0.15); c.lineTo(lerp(b[0] + nx * .15, Bp[0] + nx * .12, q1), lerp(b[1] + ny * .15, Bp[1] + ny * .12, q1)); c.stroke(); }
  const M0 = [(A[0] + Bp[0]) / 2, (A[1] + Bp[1]) / 2];
  c.lineWidth = 1.25; c.beginPath(); c.moveTo(lerp(M0[0], A[0], ss(q2)), lerp(M0[1], A[1], ss(q2))); c.lineTo(lerp(M0[0], Bp[0], ss(q2)), lerp(M0[1], Bp[1], ss(q2))); c.stroke();
  const ux = dx / L, uy = dy / L;
  if (ticks && q2 > 0) { c.lineWidth = 1; for (let i = 0; i <= ticks; i++) { const f = i / ticks; if (Math.abs(f - 0.5) > ss(q2) / 2 + 1e-6) continue; const P0 = [lerp(A[0], Bp[0], f), lerp(A[1], Bp[1], f)], hl = i % 5 === 0 ? 7 : 4; c.beginPath(); c.moveTo(P0[0] - uy * hl, P0[1] + ux * hl); c.lineTo(P0[0] + uy * hl, P0[1] - ux * hl); c.stroke(); } }
  if (q2 >= 1) for (const [P0, s] of [[A, 1], [Bp, -1]]) { c.beginPath(); c.moveTo(P0[0], P0[1]); c.lineTo(P0[0] + s * ux * 11 + uy * 3.5, P0[1] + s * uy * 11 - ux * 3.5); c.lineTo(P0[0] + s * ux * 11 - uy * 3.5, P0[1] + s * uy * 11 + ux * 3.5); c.closePath(); c.fill(); }
  if (q3 > 0 && text) {
    let ang = Math.atan2(dy, dx); if (ang > Math.PI / 2) ang -= Math.PI; if (ang < -Math.PI / 2) ang += Math.PI;
    c.translate(M0[0], M0[1]); c.rotate(ang);
    c.font = `500 18px ${MONO}`; const tw = c.measureText(text).width; c.fillStyle = PAPER; c.fillRect(-tw / 2 - 8, -12, tw + 16, 24);
    c.globalAlpha = al * ss(q3); c.fillStyle = INK; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(text, 0, 1);
  }
  c.restore();
}
// hatch pattern (the same as the plastic breaks), used for the "through the break" transition
function hatchFill(c, clipFn) {
  c.save(); c.beginPath(); clipFn(c); c.clip('evenodd');
  c.fillStyle = '#e0e0dc'; c.fillRect(0, 0, PX, PY);
  c.strokeStyle = '#8f8f8b'; c.lineWidth = 1.1;
  c.beginPath(); for (let k = -PY; k < PX + PY; k += 5) { c.moveTo(k, 0); c.lineTo(k - PY, PY); } c.stroke();
  c.restore();
}
// ---------- Subtitles: bottom-left plate, English only (the film's language), up to two lines ----------
function wrap(text, font, maxW) {
  const words = text.split(' '), lines = []; let cur = '';
  for (const w of words) { const t = cur ? cur + ' ' + w : w; if (cur && textW(t, font, 0.3) > maxW) { lines.push(cur); cur = w; } else cur = t; }
  lines.push(cur); return lines;
}
function subtitles(c, t) {
  if (!SUBS) return;
  const s = TLJ.subs.find(s => t >= s.t0 && t < s.t1); if (!s) return;
  const a = Math.min(1, (t - s.t0) / 0.12, (s.t1 - t) / 0.12);
  const f = `400 27px ${SANS}`, lines = wrap(s.en, f, 1080);
  const w = Math.max(...lines.map(l => textW(l, f, 0.3))), h = 22 + lines.length * 38;
  const y0 = 1040 - h;
  c.save(); c.globalAlpha = clamp(a);
  c.fillStyle = 'rgba(246,245,240,0.9)'; c.fillRect(48, y0, w + 44, h);
  c.fillStyle = INK; c.fillRect(48, y0, 3, h);
  c.font = f; c.letterSpacing = '0.3px'; c.fillStyle = INK;
  lines.forEach((l, i) => c.fillText(l, 72, y0 + 16 + 28 + i * 38));
  c.restore();
}
// ---------- Title block (engineering drawing): rows of [label, text] ruled cell by cell ----------
function titleBlock(c, u, x, y) {
  const rows = [['TITLE', "AC WATER: DRAIN IT, DON'T DRINK IT"], ['ROOM', 'NOT TOO DRY · LET FRESH AIR IN'], ['STYLE', 'LINE-ART CUTAWAY']];
  const RH = 62, LW = 104, WD = 820, H_ = rows.length * RH;
  c.save(); c.strokeStyle = INK;
  const g = eo(seg(u, 0, 0.45));
  c.lineWidth = 2; c.beginPath(); c.moveTo(x, y); c.lineTo(x + WD * g, y); c.moveTo(x, y + H_); c.lineTo(x + WD * g, y + H_); c.stroke();
  const gv = eo(seg(u, 0.2, 0.55));
  c.beginPath(); c.moveTo(x, y); c.lineTo(x, y + H_ * gv); c.moveTo(x + WD, y); c.lineTo(x + WD, y + H_ * gv); c.stroke();
  c.lineWidth = 1; c.beginPath(); c.moveTo(x + LW, y); c.lineTo(x + LW, y + H_ * gv);
  for (let i = 1; i < rows.length; i++) { c.moveTo(x, y + i * RH); c.lineTo(x + WD * eo(seg(u, 0.25 + i * 0.08, 0.6 + i * 0.08)), y + i * RH); }
  c.stroke(); c.restore();
  rows.forEach(([lab, en], i) => {
    const by = y + i * RH + RH / 2, d = 0.35 + i * 0.22;
    wipeText(c, lab, x + 18, by + 5, seg(u, d, d + 0.3), `500 13px ${MONO}`, FAINT, 2.4);
    wipeText(c, en, x + LW + 22, by + 8, seg(u, d + 0.1, d + 0.55), `600 ${i === 0 ? 27 : 22}px ${SANS}`, INK, i === 0 ? 0.6 : 1.0);
  });
}
// ---------- Overlay: statements in the left column, world-anchored labels, gauges ----------
const P = (x, y, z) => proj(V3(x, y, z));
const wp = (L, p) => V3(...p).applyMatrix4(L.g.matrixWorld);
const PL = (L, p) => proj(wp(L, p));
const statement = (c, t, lines, [t0, t1], y, size = 84) => lines.forEach((ln, i) => {
  const d = t0 + i * 0.28, p = seg(t, d, d + 0.55), out = seg(t, t1 + i * 0.12, t1 + i * 0.12 + 0.45);
  let x = 96; const f = `600 ${size}px ${SANS}`;
  ln.forEach(([txt, acc]) => { wipeText(c, txt, x, y + i * (size + 14), p, f, acc ? ACC : INK, -1, out); x += textW(txt, f, -1); });
});
function drawGauge(c, t) {
  const p = seg(t, K.gauge[0], K.gauge[0] + 0.6), out = seg(t, 21.6, 22.1); if (p <= 0 || out >= 1) return;
  const x0 = 96, x1 = 640, y = 560, X = v => lerp(x0, x1, v / 100);
  c.save(); c.globalAlpha = (1 - out);
  c.strokeStyle = INK; c.lineWidth = 1.5; c.beginPath(); c.moveTo(x0, y); c.lineTo(lerp(x0, x1, eo(p)), y); c.stroke();
  for (let v = 0; v <= 100; v += 10) { if (v / 100 > eo(p)) break; c.beginPath(); c.moveTo(X(v) + .5, y); c.lineTo(X(v) + .5, y + (v % 50 === 0 ? 14 : 8)); c.stroke(); }
  c.font = `400 13px ${MONO}`; c.fillStyle = GRAPH; c.letterSpacing = '1px'; [0, 50, 100].forEach(v => c.fillText(v + (v === 100 ? ' %' : ''), X(v) - 4, y + 32));
  if (p > 0.6) { c.save(); c.beginPath(); c.rect(X(30), y - 22, X(50) - X(30), 22); c.clip(); c.fillStyle = '#e4e4e0'; c.fillRect(X(30), y - 22, X(50) - X(30), 22); c.strokeStyle = '#8f8f8b'; c.lineWidth = 1;
    c.beginPath(); for (let k = -30; k < 300; k += 6) { c.moveTo(X(30) + k, y); c.lineTo(X(30) + k + 22, y - 22); } c.stroke(); c.restore(); c.strokeStyle = INK; c.strokeRect(X(30) + .5, y - 22 + .5, X(50) - X(30), 22); }
  wipeText(c, 'ROOM HUMIDITY', x0, y - 52, seg(t, K.gauge[0] + 0.1, K.gauge[0] + 0.7), `500 15px ${MONO}`, GRAPH, 3, out);
  wipeText(c, 'COMFORT BAND ABOUT 30 TO 50 %', X(30) - 40, y - 34 - 0, seg(t, K.gauge[0] + 0.7, K.gauge[0] + 1.3), `400 13px ${MONO}`, GRAPH, 1, out);
  const val = lerp(62, 24, eio(seg(t, K.gauge[0] + 0.6, K.gauge[1]))), mx = X(val);
  c.fillStyle = INK; c.beginPath(); c.moveTo(mx, y + 2); c.lineTo(mx - 8, y + 18); c.lineTo(mx + 8, y + 18); c.closePath(); c.fill();
  c.font = `500 26px ${MONO}`; c.fillText(Math.round(val) + ' %', mx - 24, y + 52);
  c.restore();
}
function overlay(t, c) {
  // hook statement
  statement(c, t, [[["DON'T ", 0], ["DRINK", 1]], [["IT.", 0]]], K.title1, 360);
  // section label + warm air arrows
  const sw = seg(t, K.sweep[0], K.sweep[1]);
  if (sw > 0 && t < 13.5) {
    const zc = secZ(t), al = Math.min(1, sw * 8, 1);
    const cs = [[-AX - 6, 152, zc], [AX + 6, 152, zc], [AX + 6, -152, zc], [-AX - 6, -152, zc]].map(p => P(...p));
    c.save(); c.globalAlpha = al; c.strokeStyle = '#8f8e8a'; c.lineWidth = 1; c.setLineDash([5, 4]);
    c.beginPath(); cs.forEach((p, i) => i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1])); c.closePath(); c.stroke(); c.setLineDash([]);
    c.font = `500 12px ${MONO}`; c.fillStyle = FAINT; c.letterSpacing = '2px'; c.fillText('SECTION', cs[1][0] - 90, cs[1][1] - 10); c.restore();
  }
  { const p = seg(t, 6.2, 6.9) * (1 - seg(t, 9.6, 10.1)); if (p > 0) {
      c.save(); c.globalAlpha = p; c.strokeStyle = GRAPH; c.fillStyle = GRAPH; c.lineWidth = 1.6; c.setLineDash([7, 6]);
      [[-250, 330, 170, -250, 165, 112], [-60, 360, 180, -60, 160, 100], [130, 340, 170, 130, 163, 108]].forEach(([x, y, z, x2, y2, z2], k) => { const a = P(x, y, z), b = P(x2, y2, z2), q = eo(seg(t, 6.2 + k * 0.18, 7.2 + k * 0.18)), e = [lerp(a[0], b[0], q), lerp(a[1], b[1], q)]; c.beginPath(); c.moveTo(a[0], a[1]); c.lineTo(e[0], e[1]); c.stroke(); });
      c.setLineDash([]); c.restore(); } }
  tag(c, t, K.lblCoil, PL(Lcoil, [-300, 46, 0]), { dx: -190, dy: -70, name: 'COLD COIL', spec: 'FINS + COPPER TUBES' });
  if (t > 6.3 && t < K.lblCoil[1] + 0.5) tag(c, t, [6.3, 7.8], P(-250, 175, 100), { dx: 150, dy: -90, name: 'WARM, HUMID AIR', spec: 'FROM THE ROOM' });
  tag(c, t, K.lblPan, PL(Lpan, [-150, -52, 0]), { dx: -170, dy: 90, name: 'DRAIN PAN', accent: true });
  tag(c, t, K.lblPipe, P(-442, -230, -126), { dx: -250, dy: 10, name: 'DRAIN PIPE', accent: true });
  // dry air: moisture leaves the room air and enters the coil (accent dots = water), gauge, statement
  { const mp = seg(t, K.moist[0], K.moist[0] + 0.4) * (1 - seg(t, K.moist[1] - 0.5, K.moist[1])); if (mp > 0) {
      c.save(); c.globalAlpha = mp;
      for (let i = 0; i < 9; i++) { const u = ((t * 0.34 + i / 9) % 1), sx = 520 - 330 * (i % 3) / 2, a = P(380 + (i % 3) * 140 - 200, 360 + (i * 37) % 160, 300 + (i % 4) * 60), b = P(0, 120, 60);
        const q = u * u * (3 - 2 * u), x = lerp(a[0], b[0], q) + Math.sin(u * 6 + i) * 10, y = lerp(a[1], b[1], q) + Math.cos(u * 6 + i) * 8; dot(c, x, y, ACC, 4.5 * (1 - 0.5 * u)); }
      c.restore(); } }
  statement(c, t, [[["DRY ", 0], ["AIR", 0]]], [15.0, 21.6], 330, 84);
  wipeText(c, 'SKIN · EYES · THROAT', 100, 418, seg(t, 18.6, 19.3), `500 24px ${MONO}`, GRAPH, 3, seg(t, 21.6, 22.1));
  drawGauge(c, t);
  // bedroom
  statement(c, t, [[['CLOSED ', 0], ['ROOM', 0]]], [K.roomIn[0] + 0.4, 29.0], 300, 84);
  { const q = seg(t, 25.4, 26.0) * (1 - seg(t, 29.3, 29.8)); if (q > 0) { wipeText(c, 'CO2 BUILDS UP OVERNIGHT', 100, 400, q, `500 26px ${MONO}`, GRAPH, 3, seg(t, 29.3, 29.8)); } }
  statement(c, t, [[['LESS DEEP ', 0]], [['SLEEP', 0]]], [29.3, 33.4], 300, 84);
  tag(c, t, [24.9, 29.0], P(1300, -1640, 900), { dx: 60, dy: -120, name: 'SLEEPER', spec: 'BREATHING OUT CO2' });
  tag(c, t, [26.0, 31.4], P(-1280, -850, -135), { dx: 20, dy: -130, name: 'WINDOW: CLOSED' });
  tag(c, t, [31.9, 34.2], P(-1280, -850, -135), { dx: 20, dy: -130, name: 'WINDOW: OPEN', spec: 'FRESH AIR IN' });
  { const p = seg(t, K.fresh[0], K.fresh[0] + 1.2) * (1 - seg(t, K.fresh[1], K.fresh[1] + 0.5)); if (p > 0) {
      c.save(); c.strokeStyle = GRAPH; c.lineWidth = 2; c.setLineDash([9, 7]);
      for (let k = 0; k < 3; k++) { const a = P(-1500 + k * 120, -800 - k * 60, -60), b = P(300 + k * 200, -1400 - k * 120, 700); c.beginPath(); c.moveTo(a[0], a[1]); const q = eo(p), e = [lerp(a[0], b[0], q), lerp(a[1], b[1], q)]; c.lineTo(e[0], e[1]); c.stroke(); }
      c.setLineDash([]); c.restore(); } }
  // the catch
  statement(c, t, [[['NOW THE ', 0]], [['CATCH.', 1]]], [K.catch[0] + 0.2, 38.2], 300, 84);
  tag(c, t, [35.9, 38.3], PL(Lcoil, [-300, 86, 0]), { dx: -180, dy: -60, name: 'COIL' });
  tag(c, t, [37.0, 38.4], PL(Lpan, [-120, -52, 40]), { dx: -190, dy: 100, name: 'DRAIN PAN', accent: true });
  tag(c, t, [37.9, 38.7], P(-442, -230, -126), { dx: -230, dy: 10, name: 'DRAIN PIPE', accent: true });
  // metals (world anchored on the lifted coil)
  tag(c, t, [K.metals[0], K.metals[1]], PL(Lcoil, [-200, 22, 56]), { dx: 170, dy: -110, name: 'COPPER TUBES', spec: 'PARTS CAN ADD METALS' });
  tag(c, t, [K.metals[0] + 1.1, K.metals[1]], PL(Lcoil, [-396, -4, 38]), { dx: 160, dy: 120, name: 'LEAD SOLDER' });
  // end: instruction + glass / pot
  statement(c, t, [[['DRAIN ', 0], ['IT.', 0]], [["DON'T ", 0], ['DRINK.', 1]]], [K.carry[0] + 0.1, 53.4], 330, 84);
  if (t > 50.5 && t < 51.7) { const p = seg(t, 50.6, 51.1), a = P(HX - 330 * eio(seg(t, 50.4, 51.6)), -480, HZ); c.save(); c.globalAlpha = (1 - seg(t, 51.3, 51.7)); c.strokeStyle = INK; c.lineWidth = 3;
    c.beginPath(); c.moveTo(a[0] - 40 * p, a[1] - 40 * p); c.lineTo(a[0] + 40 * p, a[1] + 40 * p); c.moveTo(a[0] + 40 * p, a[1] - 40 * p); c.lineTo(a[0] - 40 * p, a[1] + 40 * p); c.stroke(); c.restore(); }
  tag(c, t, [51.5, 53.4], P(HX, -430, HZ), { dx: 150, dy: -110, name: 'FOR PLANTS', spec: 'NOT FOR DRINKING' });
  // closing block
  if (t >= K.block[0]) titleBlock(c, (t - K.block[0]) / 2.0, 96, 560);
}
function overlayTexts(T, c) { overlay(T, c); }
// ---------- Closing frame: logo + LIKE / SHARE / SUBSCRIBE (line-art icons, ink only) ----------
const P_LIKE = ['M8 46 H30 V94 H8 Z', 'M34 94 V48 L50 12 Q62 6 64 20 L58 40 H90 Q102 42 99 54 L92 84 Q90 94 78 94 Z'];
const P_BELL = 'M0 -26 C-20 -26 -27 -6 -27 12 L-34 26 H34 L27 12 C27 -6 20 -26 0 -26 Z';
function drawCard(c, T) {
  const cx = 520, cy = 470, lp = seg(T, K.logo[0], K.logo[1]), R = 215 * back(lp, 1.7);
  if (lp > 0) { c.save(); c.beginPath(); c.arc(cx, cy, Math.max(1, R * 0.985), 0, Math.PI * 2); c.clip(); c.drawImage(LOGO, cx - R, cy - R, 2 * R, 2 * R); c.restore();
    c.save(); c.strokeStyle = INK; c.lineWidth = 3; c.beginPath(); c.arc(cx, cy, R + 8, 0, Math.PI * 2); c.stroke(); c.restore(); }
  { const f = `700 66px ${SANS}`, w = textW('ZAPZAPPER', f, 4); wipeText(c, 'ZAPZAPPER', cx - w / 2, cy + 215 + 92, seg(T, 60.7, 61.4), f, INK, 4, 0); }
  const rows = [['LIKE', 340, T_LIKE], ['SHARE', 500, T_SHARE], ['SUBSCRIBE', 660, T_SUB]], ix = 1010, tx = 1100;
  rows.forEach(([word, y, t0], k) => {
    const p = seg(T, t0 - 0.05, t0 + 0.4); if (p <= 0) return;
    c.save(); c.strokeStyle = INK; c.lineWidth = 3.2; c.fillStyle = PAPER; const s = back(seg(T, t0 - 0.1, t0 + 0.3), 2);
    c.translate(ix, y - 40); c.scale(1.5 * s, 1.5 * s); c.translate(-52, -52);
    if (k === 0) { const press = Math.sin(Math.PI * seg(T, t0 + 0.05, t0 + 0.45)); c.translate(0, press * 8); P_LIKE.forEach(d => { const q = new Path2D(d); c.fill(q); c.stroke(q); }); }
    if (k === 1) { c.beginPath(); c.moveTo(82, 22); c.lineTo(26, 52); c.lineTo(82, 82); c.stroke(); [[82, 22], [26, 52], [82, 82]].forEach(([x, y2]) => { c.beginPath(); c.arc(x, y2, 15, 0, Math.PI * 2); c.fill(); c.stroke(); }); }
    c.restore();
    wipeText(c, word, tx, y, p, `600 ${word === 'SUBSCRIBE' ? 92 : 110}px ${SANS}`, INK, -1, 0);
    if (k === 2) {   // a pill outline under SUBSCRIBE, pressed once, and the bell rings
      const q = seg(T, t0 + 0.1, t0 + 0.6); if (q > 0) { c.save(); c.strokeStyle = INK; c.lineWidth = 3; const w = textW('SUBSCRIBE', `600 92px ${SANS}`, -1) + 60, h = 130; c.beginPath(); c.roundRect(tx - 30, y - 98, w * eo(q), h, 65); c.stroke(); c.restore(); }
      const bp = seg(T, t0 + 0.2, t0 + 0.55); if (bp > 0) { const bx = tx + textW('SUBSCRIBE', `600 92px ${SANS}`, -1) + 120, by = y - 36, ring = Math.sin((T - t0 - 0.3) * 26) * 0.5 * Math.exp(-(T - t0 - 0.3) * 1.6) * (T > t0 + 0.3 ? 1 : 0);
        c.save(); c.translate(bx, by - 28); c.rotate(ring); c.scale(1.8 * back(bp, 2), 1.8 * back(bp, 2)); c.strokeStyle = INK; c.lineWidth = 2.4; c.fillStyle = PAPER; const bl = new Path2D(P_BELL); c.fill(bl); c.stroke(bl); c.beginPath(); c.arc(0, 34, 7, 0, Math.PI * 2); c.fill(); c.stroke(); c.restore(); }
    }
  });
}
// ---------- Thumbnail overlay (?thumb=1): big statement left, logo bottom-left ----------
function thumbOverlay(c) {
  const f = `700 168px ${SANS}`;
  [[["DON'T", 0]], [["DRINK", 1]], [["AC WATER", 0]]].forEach((ln, i) => { c.save(); c.font = f; c.letterSpacing = '-2px'; c.fillStyle = ln[0][1] ? ACC : INK; c.fillText(ln[0][0], 90, 300 + i * 175); c.restore(); });
  c.save(); c.fillStyle = INK; c.fillRect(94, 760, 340, 5); c.restore();
  const R = 78, cx = 170, cy = 900; c.save(); c.beginPath(); c.arc(cx, cy, R * 0.985, 0, Math.PI * 2); c.clip(); c.drawImage(LOGO, cx - R, cy - R, 2 * R, 2 * R); c.restore();
  c.save(); c.strokeStyle = INK; c.lineWidth = 3; c.beginPath(); c.arc(cx, cy, R + 6, 0, Math.PI * 2); c.stroke(); c.restore();
  c.save(); c.font = `700 44px ${SANS}`; c.letterSpacing = '3px'; c.fillStyle = INK; c.fillText('ZAPZAPPER', 280, 916); c.restore();
}
// ---------- A frame ----------
function frameAt(T) {
  drawPaper();
  renderer.setRenderTarget(null); renderer.setClearColor(0xffffff, 0); renderer.clear();
  ov.clearRect(0, 0, PX, PY);
  const clipOf = (tt) => { const cl = []; if (Q.get('noclip')) return cl; if (tt >= K.sweep[0] - 0.2 && tt < K.iris[0] + 0.1) { if (secZ(tt) < 399) { sweepClip(tt); cl.push(clipPlane); } if (tt >= K.clipOn) { clipPlane3.set(V3(-1, 0, 0), -172); cl.push(clipPlane3); } } return cl; };
  if (T < K.hatch[1]) renderView('main', { x: 0, y: 0, w: PX, h: PY }, (dt, j) => { const tt = clamp(T + dt, 0, FILM); setScene(tt); return { cam: camAt(tt, j), clip: clipOf(tt) }; }, { guides: true });
  setScene(T); camAt(T);
  // magnifier inset (39.6-48.6): the same model re-rendered close on the drain pan, cut at x = -172
  const mp = seg(T, K.mag[0], K.mag[0] + 0.6) * (1 - seg(T, K.mag[1] - 0.5, K.mag[1]));
  if (mp > 0.001) {
    const rad = MAGSZ / 2 * ss(mp), cx = 520, cy = 400, rect = { x: cx - MAGSZ / 2, y: cy - MAGSZ / 2, w: MAGSZ, h: MAGSZ };
    renderView('mag', rect, (dt, j) => { setScene(clamp(T + dt, 0, FILM)); clipPlane2.set(V3(-1, 0, 0), -172); return { cam: magAt(T, j), clip: [clipPlane2] }; }, { circle: true, guides: false });
    setScene(T);
    // paper outside the shrinking/growing circle is already the page; ring + connector + germ tags
    ov.save(); ov.strokeStyle = INK; ov.lineWidth = 2.4; ov.beginPath(); ov.arc(cx, cy, MAGSZ / 2, 0, Math.PI * 2); ov.stroke(); ov.restore();
    camAt(T); const a = PL(Lpan, [-172, -52, 0]); ov.save(); ov.strokeStyle = GRAPH; ov.lineWidth = 1.2; ov.setLineDash([6, 5]); ov.beginPath();
    const ang = Math.atan2(a[1] - cy, a[0] - cx); ov.moveTo(cx + Math.cos(ang) * MAGSZ / 2, cy + Math.sin(ang) * MAGSZ / 2); ov.lineTo(a[0], a[1]); ov.stroke(); ov.setLineDash([]); dot(ov, a[0], a[1], INK, 3.4); ov.restore();
    tag(ov, T, [K.germs[0] + 0.6, K.mag[1] - 0.6], [cx + 90, cy - 70], { dx: 200, dy: -150, name: 'GERMS', spec: 'IN SOME SYSTEMS: LEGIONELLA' });
  }
  if (Q.get('thumb')) thumbOverlay(ov); else if (T < K.hatch[1]) overlay(T, ov); else drawCard(ov, T);
  // through the cut: hatching fills the frame, then a round hole opens on the pan into the pulled-back view
  if (T > K.cut - 0.5 && T < K.iris[0]) { const k = seg(T, K.cut - 0.5, K.cut); ov.save(); ov.globalAlpha = ss(k); hatchFill(ov, c => c.rect(0, 0, PX, PY)); ov.restore(); }
  if (T > K.hatch[0] && T < K.irisC[0]) { ov.save(); ov.globalAlpha = ss(seg(T, K.hatch[0], K.hatch[1])); hatchFill(ov, c => c.rect(0, 0, PX, PY)); ov.restore(); }
  if (T >= K.irisC[0] && T < K.irisC[1]) {
    const o = [520, 470], r = 1700 * ei(seg(T, K.irisC[0], K.irisC[1])) + 2;
    hatchFill(ov, c => { c.rect(0, 0, PX, PY); c.moveTo(o[0] + r, o[1]); c.arc(o[0], o[1], r, 0, Math.PI * 2); });
    ov.save(); ov.strokeStyle = INK; ov.lineWidth = 2; ov.beginPath(); ov.arc(o[0], o[1], r, 0, Math.PI * 2); ov.stroke(); ov.restore();
  }
  if (T >= K.iris[0] && T < K.iris[1]) {
    const o = [960, 540], r = 2300 * ei(seg(T, K.iris[0], K.iris[1])) + 2;
    hatchFill(ov, c => { c.rect(0, 0, PX, PY); c.moveTo(o[0] + r, o[1]); c.arc(o[0], o[1], r, 0, Math.PI * 2); });
    ov.save(); ov.strokeStyle = INK; ov.lineWidth = 2; ov.beginPath(); ov.arc(o[0], o[1], r, 0, Math.PI * 2); ov.stroke(); ov.restore();
  }
  if (T < K.block[0] - 0.3 || T >= 60.8) subtitles(ov, T);
}
// ---------- Sound events ----------
function buildEV() {
  const ev = [];
  for (let n = 0; n < 6; n++) { const t0 = 1.0 + n * dropPeriod; if (t0 > 50) break; ev.push({ t: t0, type: 'swell', d: 0.75, pan: -0.5 }); ev.push({ t: t0 + 1.17, type: 'plink', pan: -0.5 }); }
  ev.push({ t: K.title1[0], type: 'type', d: 0.8, pan: -0.6 });
  ev.push({ t: K.sweep[0], type: 'sweep', d: K.sweep[1] - K.sweep[0], pan: 0.1, pan1: 0.4 });
  [[K.lblCoil[0], -0.4], [6.3, -0.2], [K.lblPan[0], -0.3], [K.lblPipe[0], -0.5]].forEach(([t, p]) => ev.push({ t, type: 'tick', pan: p }));
  ev.push({ t: K.pathRun[0], type: 'zip', d: K.pathRun[1] - K.pathRun[0], pan: -0.2, pan1: -0.4 });
  ev.push({ t: K.gauge[0], type: 'ruler', d: 0.7, pan: -0.5 }); ev.push({ t: K.gauge[0] + 0.7, type: 'barsdown', d: K.gauge[1] - K.gauge[0] - 0.6, pan: -0.5 });
  ev.push({ t: 15.0, type: 'type', d: 0.7, pan: -0.6 });
  ev.push({ t: K.roomIn[0], type: 'tip', d: 2.2, pan: 0 });
  for (let i = 0; i < 12; i++) ev.push({ t: K.co2[0] + i * 0.55, type: 'co2', pan: 0.3 });
  ev.push({ t: K.roomIn[0] + 0.4, type: 'type', d: 0.8, pan: -0.6 }); ev.push({ t: 29.3, type: 'type', d: 0.8, pan: -0.6 });
  ev.push({ t: K.latch, type: 'latch', pan: -0.4 }); ev.push({ t: K.fresh[0], type: 'air', d: 1.8, pan: -0.2 });
  ev.push({ t: K.catch[0] + 0.2, type: 'type', d: 0.9, pan: -0.6 });
  ev.push({ t: K.lift, type: 'lift', d: K.liftDur * 0.78, pan: 0 }); ev.push({ t: K.lift + K.liftDur * 0.78, type: 'seat', pan: 0, v: 0.7 });
  ev.push({ t: K.lift + K.liftStep, type: 'lift', d: K.liftDur * 0.78, pan: 0.1 }); ev.push({ t: K.lift + K.liftStep + K.liftDur * 0.78, type: 'seat', pan: 0.1, v: 0.6 });
  ev.push({ t: K.dive[0] + 0.4, type: 'dive', d: K.cut - K.dive[0] - 0.4, pan: 0 });
  ev.push({ t: K.iris[0], type: 'iris', d: K.iris[1] - K.iris[0], pan: -0.2 });
  ev.push({ t: K.mag[0], type: 'glass', pan: 0.4 });
  germs.forEach((g, i) => ev.push({ t: g.t, type: 'pop', pan: 0.3 + 0.05 * (i % 4) }));
  ev.push({ t: K.flood[0], type: 'flood', d: 1.6, pan: 0 });
  [K.metals[0], K.metals[0] + 1.1].forEach(t => ev.push({ t, type: 'tick', pan: -0.4, accent: false }));
  ev.push({ t: 46.2, type: 'drain', d: 1.4, pan: 0 });
  ev.push({ t: K.close[0], type: 'rejoin', d: 1.2, pan: 0 }); ev.push({ t: K.close[0] + 1.2, type: 'seat', pan: 0, v: 0.7 }); ev.push({ t: K.close[0] + 1.45, type: 'seat', pan: 0.1, v: 0.6 });
  ev.push({ t: K.carry[0] + 0.1, type: 'type', d: 1.0, pan: -0.6 }); ev.push({ t: 50.6, type: 'tick', pan: 0 }); ev.push({ t: 51.5, type: 'tick', pan: 0.3 });
  ev.push({ t: 50.5, type: 'whoosh', d: 0.9, pan: 0 });
  ev.push({ t: K.trace[0], type: 'trace', d: K.trace[1] - K.trace[0], pan: 0.2 });
  for (let i = 0; i < 6; i++) ev.push({ t: K.block[0] + 0.3 + i * 0.35, type: 'tick', pan: -0.5 });
  ev.push({ t: K.block[0] + 1.2, type: 'ruler', d: 0.6, pan: -0.5 });
  ev.push({ t: K.irisC[0], type: 'iris', d: K.irisC[1] - K.irisC[0], pan: -0.2 }); ev.push({ t: K.logo[0] + 0.1, type: 'glass', pan: -0.3 });
  [T_LIKE, T_SHARE, T_SUB].forEach((t, i) => ev.push({ t, type: 'tick', pan: 0.2 })); ev.push({ t: T_SUB + 0.3, type: 'glass', pan: 0.4 });
  return ev.filter(e => e.t >= FROM && e.t < TO).sort((a, b) => a.t - b.t).map(e => ({ ...e, t: +(e.t - FROM).toFixed(4) }));
}
window.DUR = +(TO - FROM).toFixed(4);
window.TEXTS = (t) => { const T = FROM + t; CAPTURE = []; setScene(T); camAt(T); ov.clearRect(0, 0, PX, PY); overlayTexts(T, ov); const r = CAPTURE; CAPTURE = null; return r; };
window.render = (t) => frameAt(FROM + t);
const fontsToLoad = [`600 20px "Plex Sans"`, `400 20px "Plex Sans"`, `400 20px "Plex Mono"`, `500 20px "Plex Mono"`];
await Promise.all(fontsToLoad.map(f => document.fonts.load(f, 'ABC abc 0123')));
await document.fonts.ready;
window.EV = buildEV(); window.render(0); window.READY = true;
