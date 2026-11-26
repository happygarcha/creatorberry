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
