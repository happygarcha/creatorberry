// Kolkata underwater metro · Line-Art Cutaway film (Hindi). Model in metres (vertical scale x5, labelled), traced live from normal/depth edges (three line weights);
// one accent colour (#0a84ff) only for water. Page contract: window.render(t), window.DUR, window.EV, window.TEXTS, window.READY.
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
const SANS = '"Plex Sans", "Noto Deva", sans-serif', MONO = '"Plex Mono", "Noto Deva", monospace';
const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
const L_ = Math.log;
const VO = TLJ.vo;
// ---------- Timeline (whole-film seconds; narration starts v1 0.8, v2 10.3, v3 25.4, v4 35.3, v5 47.5, v6 58.7, v7 66.9) ----------
const K = {
  title1: [0.9, 9.4],
  sweep: [3.0, 6.2], trainA: [5.4, 10.4],
  route: [10.4, 24.6], trainC: [11.4, 22.4], lblWest: [11.4, 15.2], lblEast: [18.6, 24.3], dateA: [16.7, 20.3], dateB: [20.4, 24.6],
  tunnel: [25.4, 34.6], dimLen: [25.9, 34.2], trainB: [26.4, 31.6], watch: [29.9, 34.4],
  cutA: [34.2, 35.1],
  tbm: [35.3, 47.0], lblHead: [36.5, 41.0], lblRing: [40.0, 46.4], lblWater: [44.2, 46.9], tbmRun: [35.6, 46.0],
  cutB: [46.8, 47.6],
  stn: [47.6, 58.4], dimDepth: [50.6, 57.9], floors: [54.0, 57.4], lblStn: [48.4, 54.0],
  out: [58.7, 66.6], lblBoat: [62.2, 66.2], lblMetro: [63.8, 66.6],
  hatch: [66.4, 67.0], irisC: [67.0, 67.8], card: 67.9, logo: [68.0, 68.7],
};
const LOGO = new Image(); LOGO.src = 'logo.png'; await LOGO.decode();
const T_LIKE = VO.v7 + 0.1, T_SHARE = VO.v7 + 1.0, T_SUB = VO.v7 + 1.95;
// ---------- Renderer ----------
const canvas = document.getElementById('gl');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: true, premultipliedAlpha: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(PX, PY, false);
renderer.outputColorSpace = THREE.LinearSRGBColorSpace;
renderer.setClearColor(0xffffff, 0);
renderer.autoClear = false;

// ---------- Material: one shader, two modes (0 = greyscale tone, 1 = normal + linear depth) ----------
const U = { uMode: { value: 0 } };
const CTL = { uBuilt: { value: 1e5 } };      // tunnel lining / bore exist only where world x < uBuilt (the boring machine's progress)
const VS = `
#include <clipping_planes_pars_vertex>
varying vec3 vN; varying vec3 vWN; varying vec2 vUv; varying float vVZ; varying vec3 vWP;
void main(){
  vec4 mvPosition = modelViewMatrix * vec4(position,1.);
  vN = normalize(normalMatrix*normal);
  vWN = normalize(mat3(modelMatrix)*normal);
  vUv = uv; vVZ = -mvPosition.z; vWP = (modelMatrix*vec4(position,1.)).xyz;
  gl_Position = projectionMatrix*mvPosition;
  #include <clipping_planes_vertex>
}`;
const FS = `
#include <clipping_planes_pars_fragment>
uniform float uMode; uniform vec3 uColor; uniform float uKind; uniform float uBuilt;
varying vec3 vN; varying vec3 vWN; varying vec2 vUv; varying float vVZ; varying vec3 vWP;
float hatch(float period){ float h = mod(gl_FragCoord.x + gl_FragCoord.y, period); return smoothstep(0.6, 1.6, h) * (1. - smoothstep(2.6, 3.6, h)); }
void main(){
  #include <clipping_planes_fragment>
  if(uKind>7.5 && uKind<9.5 && vWP.x > uBuilt) discard;       // 8 = lining, 9 = bore: not built yet
  if(uMode>0.5){
    vec3 n = normalize(vN); if(!gl_FrontFacing) n = vec3(0.,0.,1.);
    gl_FragColor = vec4(n, vVZ); return;
  }
  if(uKind>9.5){                                                // 10 = water: accent hatching on a pale tint, on every face
    vec3 c = mix(vec3(.88,.94,1.), uColor, hatch(9.)*.9); gl_FragColor = vec4(c,1.); return;
  }
  if(uKind>8.5){                                                // 9 = bore: the empty inside of the tunnel, plain light
    gl_FragColor = vec4(uColor*(gl_FrontFacing ? .97 : 1.), 1.); return;
  }
  bool lit = (uKind>6.5 && uKind<7.5);
  if(!gl_FrontFacing){                                          // section faces: hatching
    vec3 c = lit ? uColor : mix(vec3(.90), vec3(.34), hatch(10.));
    gl_FragColor = vec4(c,1.); return;
  }
  vec3 n = normalize(vWN);
  vec3 L = normalize(vec3(-.35,1.,.55));
  float d = max(dot(n,L),0.);
  float tone = .82 + .18*d + .03*n.y;
  vec3 col = uColor;
  if(uKind>3.5 && uKind<4.5){ col = mix(vec3(.88), vec3(.56), hatch(10.)); tone = 1.; }
  if(lit) tone = .94 + .06*d;
  gl_FragColor = vec4(col*min(tone,1.0), 1.);
}`;
function mat(hex, kind = 0) {
  return new THREE.ShaderMaterial({ uniforms: { uMode: U.uMode, uBuilt: CTL.uBuilt, uColor: { value: new THREE.Color(hex) }, uKind: { value: kind } },
    vertexShader: VS, fragmentShader: FS, side: THREE.DoubleSide, clipping: true });
}
const M = {
  ground: mat(0xf2f2ee), skyline: mat(0xe6e6e2, 4), white: mat(0xfbfbf9), metal: mat(0xededea), metal2: mat(0xdcdcd8), dark: mat(0x555553), mid: mat(0x9a9a97),
  water: mat(ACC_GL, 10), accent: mat(ACC_GL, 7), lining: mat(0xe4e3de, 8), bore: mat(0xf5f5f1, 9), yellow: mat(0xe8e6de),
};
const scene = new THREE.Scene();
const root = new THREE.Group(); scene.add(root);
// ---------- Geometry helpers (metres) ----------
const box = (w, h, d, x, y, z) => new THREE.BoxGeometry(w, h, d).translate(x, y + h / 2, z);
const cylX = (r, len, x, y, z, s = 24, open = false) => new THREE.CylinderGeometry(r, r, len, s, 1, open).rotateZ(Math.PI / 2).translate(x, y, z);
function bar(a, b, r = 1.1, sg = 6) {
  const A = V3(...a), B = V3(...b), d = B.clone().sub(A), len = d.length();
  const g = new THREE.CylinderGeometry(r, r, len, sg); g.translate(0, len / 2, 0);
  g.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(V3(0, 1, 0), d.normalize())); g.translate(A.x, A.y, A.z); return g;
}
function extZ(pts, z0, z1) {                  // polygon in (x, y) extruded along z
  const sh = new THREE.Shape(); pts.forEach(([x, y], i) => i ? sh.lineTo(x, y) : sh.moveTo(x, y));
  const g = new THREE.ExtrudeGeometry(sh, { depth: z1 - z0, bevelEnabled: false }); g.translate(0, 0, z0); return g;
}
function clean(g) { g = g.index ? g.toNonIndexed() : g; for (const k of Object.keys(g.attributes)) if (!['position', 'normal', 'uv'].includes(k)) g.deleteAttribute(k); if (!g.attributes.uv) g.setAttribute('uv', new THREE.BufferAttribute(new Float32Array(g.attributes.position.count * 2), 2)); return g; }
function add(group, geos, m) { if (!geos.length) return null; const mesh = new THREE.Mesh(mergeGeometries(geos.map(clean)), m); group.add(mesh); return mesh; }
const rng = mulberry(20261126);

// ---------- Ground block: profile in (x, y), vertical scale x5; river x -260..260 (bed -80 = 16 m), station shaft x -390..-300 (33 m = -165) ----------
const ZH = 30, RIVER_X = 260, BED = -80, SHAFT = [-392, -300], SHAFT_D = -165, TUN_Y = -149, TUN_R = 16;
const CHANNEL = [[-260, 0], [-225, -76], [-100, BED], [100, BED], [225, -76], [260, 0]];
add(root, [extZ([[-700, 0], [SHAFT[0], 0], [SHAFT[0], SHAFT_D], [SHAFT[1], SHAFT_D], [SHAFT[1], 0], ...CHANNEL, [700, 0], [700, -300], [-700, -300]], -ZH, ZH)], M.ground);
add(root, [box(SHAFT[1] - SHAFT[0], -SHAFT_D, 1, (SHAFT[0] + SHAFT[1]) / 2, SHAFT_D, -ZH + 0.5)], M.bore);    // far wall of the shaft, so the cavity reads as a room
const water = add(root, [extZ(CHANNEL, -ZH + 0.5, ZH - 0.5)], M.water);
// ---------- Tunnel: bore (plain inside) + lining rings every 3.2 m, x -345 .. 690 ----------
const TX0 = -345, TX1 = 690;
add(root, [cylX(TUN_R, TX1 - TX0, (TX0 + TX1) / 2, TUN_Y, 0, 32, true)], M.bore);
{ const rings = []; for (let x = TX0; x < TX1; x += 3.2) rings.push(cylX(TUN_R + 1.6, 2.5, x + 1.2, TUN_Y, 0, 28, true)); add(root, rings, M.lining); }
add(root, [box(TX1 - TX0, 2.2, 22, (TX0 + TX1) / 2, TUN_Y - TUN_R + 0.2, 0)], M.metal2);      // track bed
// ---------- Train: 3 cars, nose to +x ----------
const trainG = new THREE.Group(); root.add(trainG);
{ const cars = [], wins = [];
  for (let k = 0; k < 3; k++) { const cx = -k * 24; cars.push(box(22, 14, 17, cx, TUN_Y - TUN_R + 2.4, 0)); for (let j = 0; j < 4; j++) wins.push(box(3.2, 5, 17.4, cx - 8 + j * 5.4, TUN_Y - TUN_R + 8, 0)); }
  cars.push(box(5, 11, 15, 13.5, TUN_Y - TUN_R + 2.4, 0));
  add(trainG, cars, M.white); add(trainG, wins, M.dark); }
// ---------- Boring machine (TBM) at the tunnel face ----------
const tbmG = new THREE.Group(); root.add(tbmG);
const headG = new THREE.Group(); tbmG.add(headG);
add(tbmG, [cylX(TUN_R - 0.4, 34, -17, TUN_Y, 0, 32), cylX(TUN_R - 0.2, 4, 2, TUN_Y, 0, 32)], M.metal);
add(tbmG, [box(12, 10, 14, -44, TUN_Y - TUN_R + 3, 0), box(12, 10, 14, -58, TUN_Y - TUN_R + 3, 0), box(10, 7, 12, -72, TUN_Y - TUN_R + 3, 0)], M.metal2);
{ const sp = []; for (let k = 0; k < 8; k++) { const g = box(2.2, 2 * TUN_R - 2, 3.5, 0, -(TUN_R - 1), 0).rotateX(k * Math.PI / 8); sp.push(g); }
  add(headG, [cylX(TUN_R, 3, 5.5, 0, 0, 32), ...sp.map(g => g.translate(6, 0, 0))], M.dark);
  const teeth = []; for (let k = 0; k < 12; k++) { const a = k * Math.PI / 6; teeth.push(new THREE.SphereGeometry(1.8, 8, 6).translate(8, Math.sin(a) * (TUN_R - 2), Math.cos(a) * (TUN_R - 2))); }
  add(headG, teeth, M.mid); }
headG.position.set(0, TUN_Y, 0); tbmG.userData.baseY = 0;
// ---------- Station: 11 floor slabs (3 m each, x5 = 15), escalator, platform ----------
const floors = [];
{ const SW = SHAFT[1] - SHAFT[0] - 4, cx = (SHAFT[0] + SHAFT[1]) / 2;
  for (let k = 1; k <= 11; k++) { const m = add(root, [box(SW, 1.6, 52, 0, 0, 0)], M.yellow); m.position.set(cx, -k * 15, -2); floors.push({ m, k, t: K.floors[0] + (k - 1) * 0.27 }); }
  add(root, [box(SW, 2.5, 52, cx, TUN_Y - TUN_R - 1.2, -2)], M.metal2);
  add(root, [bar([SHAFT[0] + 12, -3, 8], [SHAFT[1] - 12, SHAFT_D + 18, 8], 1.8), bar([SHAFT[0] + 12, -3, 14], [SHAFT[1] - 12, SHAFT_D + 18, 14], 1.8)], M.mid); }
// ---------- Surface: Howrah-style cantilever bridge, banks, boats, fish ----------
{ const bars = [], dk = [];
  const top = [[-260, 36], [-205, 70], [-150, 122], [-75, 98], [0, 86], [75, 98], [150, 122], [205, 70], [260, 36]];
  for (const z of [-22, 22]) {
    for (let i = 0; i < top.length - 1; i++) bars.push(bar([top[i][0], top[i][1], z], [top[i + 1][0], top[i + 1][1], z], 1.9));
    bars.push(bar([-260, 24, z], [260, 24, z], 2.2));
    for (let x = -240; x <= 240; x += 20) { const yy = (x2 => { for (let i = 0; i < top.length - 1; i++) if (x2 >= top[i][0] && x2 <= top[i + 1][0]) return lerp(top[i][1], top[i + 1][1], (x2 - top[i][0]) / (top[i + 1][0] - top[i][0])); return 36; })(x);
      bars.push(bar([x, 24, z], [x, yy, z], 0.9)); bars.push(bar([x, 24, z], [x + 20, (x + 20 >= -260 && x + 20 <= 260) ? yy + 6 : yy, z], 0.8)); }
    for (const tx of [-150, 150]) { bars.push(bar([tx - 5, 0, z], [tx - 3, 122, z], 3.2)); bars.push(bar([tx + 5, 0, z], [tx + 3, 122, z], 3.2)); }
  }
  for (const tx of [-150, 150]) for (let y = 20; y <= 120; y += 25) bars.push(bar([tx, y, -22], [tx, y, 22], 1.4));
  dk.push(box(520, 3, 48, 0, 22, 0));
  add(root, bars, M.metal); add(root, dk, M.metal2);
  const r = mulberry(31), sk = [];
  for (let i = 0; i < 14; i++) { const w = 22 + r() * 26, h = 20 + r() * 80; sk.push(box(w, h, 40, 285 + i * 30 + r() * 6, 0, -4)); sk.push(box(w, h * 0.8, 40, -285 - i * 30 - r() * 6, 0, -4)); }
  add(root, sk.filter(g => { const b = new THREE.Box3().setFromBufferAttribute(g.attributes.position); return !(b.max.x > SHAFT[0] && b.min.x < SHAFT[1]); }), M.skyline); }
const boats = [];
for (const [cx, A, w, s] of [[-60, 120, .08, 1], [120, 90, .06, .85], [-170, 55, .05, .7]]) {
  const g = new THREE.Group(); add(g, [extZ([[-16, 3], [16, 3], [11, -5], [-11, -5]], -4, 4), box(14, 8, 7, -2, 3, 0)], M.white); add(g, [bar([5, 3, 0], [5, 30, 0], 0.7), extZ([[5, 29], [5, 8], [20, 8]], -0.6, 0.6)], M.metal);
  g.scale.setScalar(s * 1.6); g.userData = { cx, A, w, z: -10 - boats.length * 3 }; root.add(g); boats.push(g); }
const fishes = [];
for (let i = 0; i < 4; i++) { const g = new THREE.Group(); const b = new THREE.SphereGeometry(5, 10, 8); b.scale(1.7, 0.8, 0.5);
  add(g, [b, extZ([[-8, 0], [-14, 5], [-14, -5]], -0.5, 0.5)], M.white); g.userData = { x0: -150 + i * 95, y: -26 - (i % 2) * 18, ph: i * 1.3 }; g.position.z = -9; root.add(g); fishes.push(g); }
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
  const nameFont = `600 26px ${SANS}`;
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
  if (spec) wipeText(c, spec, tx, ly + 25, seg(u, 0.3, 0.7), `400 19px ${MONO}`, GRAPH, 0, out);
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
    c.font = `500 24px ${MONO}`; const tw = c.measureText(text).width; c.fillStyle = PAPER; c.fillRect(-tw / 2 - 8, -12, tw + 16, 24);
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
// ---------- Subtitles: bottom-left plate, Hindi (the film's language), up to two lines ----------
function wrap(text, font, maxW) {
  const words = text.split(' '), lines = []; let cur = '';
  for (const w of words) { const t = cur ? cur + ' ' + w : w; if (cur && textW(t, font, 0.3) > maxW) { lines.push(cur); cur = w; } else cur = t; }
  lines.push(cur); return lines;
}
function subtitles(c, t) {
  if (!SUBS) return;
  const s = TLJ.subs.find(s => t >= s.t0 && t < s.t1); if (!s) return;
  const a = Math.min(1, (t - s.t0) / 0.12, (s.t1 - t) / 0.12);
  const f = `400 31px ${SANS}`, lines = wrap(s.hi, f, 1100);
  const w = Math.max(...lines.map(l => textW(l, f, 0))), h = 24 + lines.length * 46;
  const y0 = 1040 - h;
  c.save(); c.globalAlpha = clamp(a);
  c.fillStyle = 'rgba(246,245,240,0.9)'; c.fillRect(48, y0, w + 44, h);
  c.fillStyle = INK; c.fillRect(48, y0, 3, h);
  c.font = f; c.fillStyle = INK;
  lines.forEach((l, i) => c.fillText(l, 72, y0 + 16 + 30 + i * 46));
  c.restore();
}
const P = (x, y, z) => proj(V3(x, y, z));
const wp = (L, p) => V3(...p).applyMatrix4(L.g.matrixWorld);
const PL = (L, p) => proj(wp(L, p));
const statement = (c, t, lines, [t0, t1], y, size = 84) => {
  const p0 = seg(t, t0, t0 + 0.4), out0 = seg(t, t1 + lines.length * 0.12, t1 + lines.length * 0.12 + 0.45);
  if (p0 > 0 && out0 < 1) {
    const f = `600 ${size}px ${SANS}`, w = Math.max(...lines.map(ln => ln.reduce((a, [txt]) => a + textW(txt, f, -1), 0))), h = lines.length * (size + 14) + 26;
    c.save(); c.globalAlpha = 0.93 * p0 * (1 - out0); c.fillStyle = PAPER; c.fillRect(70, y - size - 10, w + 56, h); c.fillStyle = INK; c.fillRect(70, y - size - 10, 4, h); c.restore();
  }
  lines.forEach((ln, i) => {
    const d = t0 + i * 0.28, p = seg(t, d, d + 0.55), out = seg(t, t1 + i * 0.12, t1 + i * 0.12 + 0.45);
    let x = 96; const f = `600 ${size}px ${SANS}`;
    ln.forEach(([txt, acc]) => { wipeText(c, txt, x, y + i * (size + 14), p, f, acc ? ACC : INK, -1, out); x += textW(txt, f, -1); });
  });
};
const trainPos = (t) => trainX(t) - 12;
function overlay(t, c) {
  // hook
  statement(c, t, [[['नदी के ', 0]], [['नीचे ', 0], ['मेट्रो', 1]]], K.title1, 300, 100);
  { const p = seg(t, 3.4, 4.2) * (1 - seg(t, 66.0, 66.4)); if (p > 0) { c.save(); c.globalAlpha = p; c.font = `500 15px ${MONO}`; c.fillStyle = FAINT; c.letterSpacing = '1.5px'; c.textAlign = 'right'; c.fillText('ऊर्ध्वाधर स्केल ×5', 1860, 54); c.restore(); } }
  tag(c, t, [1.3, 5.2], P(0, 86, 22), { dx: 140, dy: -80, name: 'हावड़ा ब्रिज' });
  tag(c, t, [3.6, 8.6], P(150, -10, 0), { dx: 150, dy: 80, name: 'हुगली नदी', accent: true });
  tag(c, t, [6.4, 10.2], P(120, TUN_Y + 8, 0), { dx: 120, dy: 90, name: 'मेट्रो सुरंग', spec: 'नदी तल के नीचे' });
  // route
  tag(c, t, [11.4, 15.2], P(-346, -70, 0), { dx: 160, dy: -130, name: 'हावड़ा मैदान', spec: 'पश्चिम किनारा' });
  tag(c, t, [18.6, 24.3], P(430, TUN_Y, 0), { dx: -110, dy: -170, name: 'एस्प्लेनेड की ओर →', spec: 'पूर्व दिशा' });
  statement(c, t, [[['उद्घाटन', 0]], [['6 मार्च 2024', 1]]], K.dateA, 320, 84);
  statement(c, t, [[['यात्रियों के लिए', 0]], [['15 मार्च 2024', 1]]], K.dateB, 320, 84);
  // tunnel length + stopwatch
  { const p = seg(t, K.dimLen[0], K.dimLen[0] + 1.4), al = 1 - seg(t, K.dimLen[1], K.dimLen[1] + 0.4);
    if (p > 0) dimLine(c, P(-260, -178, 0), P(260, -178, 0), 55, '520 मीटर', p, al, 26); }
  statement(c, t, [[['520 ', 1], ['मीटर', 0]], [['सुरंग', 0]]], [K.tunnel[0] + 0.1, 34.4], 320, 100);
  { const p = seg(t, K.watch[0], K.watch[0] + 0.5), out = seg(t, K.watch[1], K.watch[1] + 0.4); if (p > 0 && out < 1) {
      const cx = 260, cy = 640, R = 90 * back(p, 2); c.save(); c.globalAlpha = 1 - out; c.strokeStyle = INK; c.lineWidth = 3; c.fillStyle = PAPER;
      c.beginPath(); c.arc(cx, cy, R, 0, Math.PI * 2); c.fill(); c.stroke(); c.fillRect(cx - 12, cy - R - 16, 24, 14); c.strokeRect(cx - 12 + .5, cy - R - 16 + .5, 24, 14);
      for (let k = 0; k < 12; k++) { const a = k * Math.PI / 6; c.beginPath(); c.moveTo(cx + Math.sin(a) * (R - 6), cy - Math.cos(a) * (R - 6)); c.lineTo(cx + Math.sin(a) * (R - 14), cy - Math.cos(a) * (R - 14)); c.lineWidth = 2; c.stroke(); }
      const ha = eio(seg(t, K.watch[0] + 0.3, K.watch[1] - 0.6)) * Math.PI * 1.88; c.strokeStyle = ACC; c.lineWidth = 4; c.beginPath(); c.moveTo(cx, cy); c.lineTo(cx + Math.sin(ha) * (R - 18), cy - Math.cos(ha) * (R - 18)); c.stroke();
      c.fillStyle = INK; c.beginPath(); c.arc(cx, cy, 6, 0, Math.PI * 2); c.fill(); c.restore();
      wipeText(c, '≈ 45 सेकंड', cx - 78, cy + R + 52, seg(t, K.watch[0] + 0.5, K.watch[0] + 1.0), `600 34px ${SANS}`, INK, 0, out); } }
  // boring machine
  statement(c, t, [[['मशीन से', 0]], [['खुदी सुरंग', 1]]], [K.tbm[0] + 0.1, 41.2], 320, 92);
  { const x = tbmX(t); tag(c, t, K.lblHead, P(x + 6, TUN_Y + 10, 0), { dx: 140, dy: -170, name: 'कटर हेड', spec: 'मिट्टी काटता है' });
    tag(c, t, K.lblRing, P(x - 85, TUN_Y + 17, 0), { dx: -120, dy: -130, name: 'कंक्रीट के छल्ले', spec: 'पीछे जुड़ते जाते हैं' });
    tag(c, t, K.lblWater, P(x - 20, -40, 0), { dx: 80, dy: -20, name: 'ऊपर: नदी का पानी', accent: true }); }
  statement(c, t, [[['पानी अंदर', 0]], [['नहीं आएगा', 1]]], [44.3, 46.9], 320, 92);
  // station
  statement(c, t, [[['सबसे गहरा', 1]], [['स्टेशन', 0]]], [K.stn[0] + 0.1, 53.8], 320, 100);
  tag(c, t, K.lblStn, P(-346, -165, 0), { dx: 180, dy: 70, name: 'हावड़ा मैदान स्टेशन', spec: 'भारत का सबसे गहरा' });
  { const p = seg(t, K.dimDepth[0], K.dimDepth[0] + 1.6), al = 1 - seg(t, K.dimDepth[1], K.dimDepth[1] + 0.4); if (p > 0) dimLine(c, P(-404, 0, 0), P(-404, SHAFT_D, 0), 48, '≈ 33 मीटर', p, al, 11); }
  statement(c, t, [[['ग्यारह मंज़िल', 0]], [['जितना गहरा', 1]]], [K.floors[0] - 0.2, 58.4], 320, 92);
  floors.forEach(f => { const u = t - f.t; if (u > 0 && t < K.floors[1] + 4) { const q = P(-392 + 8, -f.k * 15 + 8, 20); badge(c, q[0], q[1], String(f.k), seg(u, 0, 0.35), f.k === 11, 13); } });
  // finale
  statement(c, t, [[['ऊपर नावें,', 0]], [['नीचे ', 0], ['मेट्रो', 1]]], [K.out[0] + 0.2, 66.3], 320, 100);
  tag(c, t, K.lblBoat, V3(0, 0, 0).set(...[boats[0].position.x, 28, boats[0].position.z]) && P(boats[0].position.x, 28, boats[0].position.z), { dx: 100, dy: -110, name: 'ऊपर: नावें' });
  tag(c, t, K.lblMetro, P(trainPos(t) > 4000 ? 200 : 200, TUN_Y + 8, 0), { dx: 80, dy: 110, name: 'नीचे: मेट्रो', accent: true });
}
function overlayTexts(T, c) { overlay(T, c); }
// ---------- Closing frame: logo + LIKE / SHARE / SUBSCRIBE (line-art icons, ink only) ----------
const P_LIKE = ['M8 46 H30 V94 H8 Z', 'M34 94 V48 L50 12 Q62 6 64 20 L58 40 H90 Q102 42 99 54 L92 84 Q90 94 78 94 Z'];
const P_BELL = 'M0 -26 C-20 -26 -27 -6 -27 12 L-34 26 H34 L27 12 C27 -6 20 -26 0 -26 Z';
function drawCard(c, T) {
  const cx = 520, cy = 470, lp = seg(T, K.logo[0], K.logo[1]), R = 215 * back(lp, 1.7);
  if (lp > 0) { c.save(); c.beginPath(); c.arc(cx, cy, Math.max(1, R * 0.985), 0, Math.PI * 2); c.clip(); c.drawImage(LOGO, cx - R, cy - R, 2 * R, 2 * R); c.restore();
    c.save(); c.strokeStyle = INK; c.lineWidth = 3; c.beginPath(); c.arc(cx, cy, R + 8, 0, Math.PI * 2); c.stroke(); c.restore(); }
  { const f = `700 66px ${SANS}`, w = textW('ZAPZAPPER', f, 4); wipeText(c, 'ZAPZAPPER', cx - w / 2, cy + 215 + 92, seg(T, K.logo[1], K.logo[1] + 0.7), f, INK, 4, 0); }
  const rows = [['लाइक', 340, T_LIKE], ['शेयर', 500, T_SHARE], ['सब्सक्राइब', 660, T_SUB]], ix = 1010, tx = 1100;
  rows.forEach(([word, y, t0], k) => {
    const p = seg(T, t0 - 0.05, t0 + 0.4); if (p <= 0) return;
    c.save(); c.strokeStyle = INK; c.lineWidth = 3.2; c.fillStyle = PAPER; const s = back(seg(T, t0 - 0.1, t0 + 0.3), 2);
    c.translate(ix, y - 40); c.scale(1.5 * s, 1.5 * s); c.translate(-52, -52);
    if (k === 0) { const press = Math.sin(Math.PI * seg(T, t0 + 0.05, t0 + 0.45)); c.translate(0, press * 8); P_LIKE.forEach(d => { const q = new Path2D(d); c.fill(q); c.stroke(q); }); }
    if (k === 1) { c.beginPath(); c.moveTo(82, 22); c.lineTo(26, 52); c.lineTo(82, 82); c.stroke(); [[82, 22], [26, 52], [82, 82]].forEach(([x, y2]) => { c.beginPath(); c.arc(x, y2, 15, 0, Math.PI * 2); c.fill(); c.stroke(); }); }
    c.restore();
    wipeText(c, word, tx, y, p, `600 ${word === 'सब्सक्राइब' ? 84 : 100}px ${SANS}`, INK, -1, 0);
    if (k === 2) {   // a pill outline under SUBSCRIBE, pressed once, and the bell rings
      const q = seg(T, t0 + 0.1, t0 + 0.6); if (q > 0) { c.save(); c.strokeStyle = INK; c.lineWidth = 3; const w = textW('सब्सक्राइब', `600 84px ${SANS}`, -1) + 60, h = 130; c.beginPath(); c.roundRect(tx - 30, y - 98, w * eo(q), h, 65); c.stroke(); c.restore(); }
      const bp = seg(T, t0 + 0.2, t0 + 0.55); if (bp > 0) { const bx = tx + textW('सब्सक्राइब', `600 84px ${SANS}`, -1) + 120, by = y - 36, ring = Math.sin((T - t0 - 0.3) * 26) * 0.5 * Math.exp(-(T - t0 - 0.3) * 1.6) * (T > t0 + 0.3 ? 1 : 0);
        c.save(); c.translate(bx, by - 28); c.rotate(ring); c.scale(1.8 * back(bp, 2), 1.8 * back(bp, 2)); c.strokeStyle = INK; c.lineWidth = 2.4; c.fillStyle = PAPER; const bl = new Path2D(P_BELL); c.fill(bl); c.stroke(bl); c.beginPath(); c.arc(0, 34, 7, 0, Math.PI * 2); c.fill(); c.stroke(); c.restore(); }
    }
  });
}

// ---------- Thumbnail overlay (?thumb=1): big statement left, logo bottom-left ----------
function thumbOverlay(c) {
  const f = `700 150px ${SANS}`;
  c.save(); c.fillStyle = 'rgba(246,245,240,0.94)'; c.fillRect(60, 90, 480, 760); c.fillStyle = INK; c.fillRect(60, 90, 6, 760); c.restore();
  [[["नदी के", 0]], [["नीचे", 0]], [["मेट्रो!", 1]]].forEach((ln, i) => { c.save(); c.font = f; c.fillStyle = ln[0][1] ? ACC : INK; c.fillText(ln[0][0], 90, 270 + i * 190); c.restore(); });
  c.save(); c.fillStyle = INK; c.fillRect(94, 790, 340, 5); c.restore();
  const R = 70, cx = 164, cy = 905; c.save(); c.beginPath(); c.arc(cx, cy, R * 0.985, 0, Math.PI * 2); c.clip(); c.drawImage(LOGO, cx - R, cy - R, 2 * R, 2 * R); c.restore();
  c.save(); c.strokeStyle = INK; c.lineWidth = 3; c.beginPath(); c.arc(cx, cy, R + 6, 0, Math.PI * 2); c.stroke(); c.restore();
  c.save(); c.font = `700 44px ${SANS}`; c.letterSpacing = '3px'; c.fillStyle = INK; c.fillText('ZAPZAPPER', 270, 920); c.restore();
}
// ---------- A frame ----------
function frameAt(T) {
  drawPaper();
  renderer.setRenderTarget(null); renderer.setClearColor(0xffffff, 0); renderer.clear();
  ov.clearRect(0, 0, PX, PY);
  const clipOf = (tt) => { if (Q.get('noclip')) return []; sweepClip(tt); return [clipPlane]; };
  if (T < K.hatch[1]) renderView('main', { x: 0, y: 0, w: PX, h: PY }, (dt, j) => { const tt = clamp(T + dt, 0, FILM); setScene(tt); return { cam: camAt(tt, j), clip: clipOf(tt) }; }, { guides: false });
  setScene(T); camAt(T);
  if (Q.get('thumb')) thumbOverlay(ov); else if (T < K.hatch[1]) overlay(T, ov); else drawCard(ov, T);
  // cuts between sections: hatching fills the frame, then a round hole opens (the same hatch as the section faces)
  for (const [a, b] of [K.cutA, K.cutB]) {
    if (T >= a - 0.45 && T < a) { ov.save(); ov.globalAlpha = ss(seg(T, a - 0.45, a)); hatchFill(ov, c => c.rect(0, 0, PX, PY)); ov.restore(); }
    if (T >= a && T < b) { const o = [960, 540], r = 2300 * ei(seg(T, a, b)) + 2; hatchFill(ov, c => { c.rect(0, 0, PX, PY); c.moveTo(o[0] + r, o[1]); c.arc(o[0], o[1], r, 0, Math.PI * 2); });
      ov.save(); ov.strokeStyle = INK; ov.lineWidth = 2; ov.beginPath(); ov.arc(o[0], o[1], r, 0, Math.PI * 2); ov.stroke(); ov.restore(); }
  }
  if (T > K.hatch[0] && T < K.irisC[0]) { ov.save(); ov.globalAlpha = ss(seg(T, K.hatch[0], K.hatch[1])); hatchFill(ov, c => c.rect(0, 0, PX, PY)); ov.restore(); }
  if (T >= K.irisC[0] && T < K.irisC[1]) {
    const o = [520, 470], r = 1700 * ei(seg(T, K.irisC[0], K.irisC[1])) + 2;
    hatchFill(ov, c => { c.rect(0, 0, PX, PY); c.moveTo(o[0] + r, o[1]); c.arc(o[0], o[1], r, 0, Math.PI * 2); });
    ov.save(); ov.strokeStyle = INK; ov.lineWidth = 2; ov.beginPath(); ov.arc(o[0], o[1], r, 0, Math.PI * 2); ov.stroke(); ov.restore();
  }
  subtitles(ov, T);
}
// ---------- Sound events ----------
function buildEV() {
  const ev = [];
  ev.push({ t: K.title1[0], type: 'type', d: 0.8, pan: -0.6 });
  ev.push({ t: K.sweep[0], type: 'sweep', d: K.sweep[1] - K.sweep[0], pan: 0.1, pan1: 0.4 });
  ev.push({ t: K.trainA[0], type: 'train', d: K.trainA[1] - K.trainA[0], pan: -0.4, pan1: 0.5 });
  [1.3, 3.6, 6.4, K.lblWest[0], K.lblEast[0]].forEach((t, i) => ev.push({ t, type: 'tick', pan: -0.3 + 0.1 * i }));
  ev.push({ t: K.dateA[0], type: 'type', d: 0.8, pan: -0.6 }); ev.push({ t: K.dateB[0], type: 'type', d: 0.8, pan: -0.6 });
  ev.push({ t: K.dimLen[0], type: 'ruler', d: 1.2, pan: 0 }); ev.push({ t: K.tunnel[0] + 0.1, type: 'type', d: 0.8, pan: -0.6 });
  ev.push({ t: K.trainB[0], type: 'train', d: K.trainB[1] - K.trainB[0], pan: -0.4, pan1: 0.5 });
  ev.push({ t: K.watch[0], type: 'glass', pan: -0.5 }); for (let i = 0; i < 6; i++) ev.push({ t: K.watch[0] + 0.5 + i * 0.7, type: 'tick', pan: -0.5 });
  for (const [a, b] of [K.cutA, K.cutB]) ev.push({ t: a, type: 'iris', d: b - a, pan: -0.2 });
  ev.push({ t: K.tbmRun[0], type: 'dive', d: K.tbmRun[1] - K.tbmRun[0] - 0.4, pan: 0 });
  [K.lblHead[0], K.lblRing[0], K.lblWater[0], K.tbm[0] + 0.1].forEach(t => ev.push({ t, type: 'tick', pan: 0.1 }));
  for (let i = 0; i < 9; i++) ev.push({ t: K.tbmRun[0] + 1.2 + i * 1.1, type: 'seat', pan: 0.3, v: 0.5 });
  ev.push({ t: K.stn[0] + 0.1, type: 'type', d: 0.9, pan: -0.6 }); ev.push({ t: K.lblStn[0], type: 'tick', pan: 0 });
  ev.push({ t: K.dimDepth[0], type: 'ruler', d: 1.4, pan: -0.3 });
  floors.forEach(f => ev.push({ t: f.t, type: 'pop', pan: -0.2 }));
  ev.push({ t: K.out[0] + 0.2, type: 'type', d: 1.0, pan: -0.6 }); ev.push({ t: K.lblBoat[0], type: 'tick', pan: 0 }); ev.push({ t: K.lblMetro[0], type: 'tick', pan: 0.2 });
  ev.push({ t: K.hatch[0], type: 'whoosh', d: 0.8, pan: 0 });
  ev.push({ t: K.irisC[0], type: 'iris', d: K.irisC[1] - K.irisC[0], pan: -0.2 }); ev.push({ t: K.logo[0] + 0.1, type: 'glass', pan: -0.3 });
  [T_LIKE, T_SHARE, T_SUB].forEach(t => ev.push({ t, type: 'tick', pan: 0.2 })); ev.push({ t: T_SUB + 0.3, type: 'glass', pan: 0.4 });
  return ev.filter(e => e.t >= FROM && e.t < TO).sort((a, b) => a.t - b.t).map(e => ({ ...e, t: +(e.t - FROM).toFixed(4) }));
}
window.DUR = +(TO - FROM).toFixed(4);
window.TEXTS = (t) => { const T = FROM + t; CAPTURE = []; setScene(T); camAt(T); ov.clearRect(0, 0, PX, PY); overlayTexts(T, ov); const r = CAPTURE; CAPTURE = null; return r; };
window.render = (t) => frameAt(FROM + t);
const fontsToLoad = [`600 20px "Plex Sans"`, `400 20px "Plex Sans"`, `400 20px "Plex Mono"`, `500 20px "Plex Mono"`, `400 20px "Noto Deva"`, `600 20px "Noto Deva"`, `700 20px "Noto Deva"`];
await Promise.all(fontsToLoad.map(f => document.fonts.load(f, 'ABC abc 0123 नदी मेट्रो')));
await document.fonts.ready;
window.EV = buildEV(); window.render(0); window.READY = true;
