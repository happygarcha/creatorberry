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
