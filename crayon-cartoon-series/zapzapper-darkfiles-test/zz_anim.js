'use strict';
// Zapzapper Dark Files - 60 s animation test. Deterministic: renderAt(t) poses everything from t alone.
const Z = window.ZZ, NS = 'http://www.w3.org/2000/svg';
const $ = id => document.getElementById(id);
const clamp = (x, a, b) => Math.max(a, Math.min(b, x)), lerp = (a, b, u) => a + (b - a) * u;
const sm = u => { u = clamp(u, 0, 1); return u * u * (3 - 2 * u); };
const seg = (t, a, b) => clamp((t - a) / (b - a), 0, 1);
const D2R = Math.PI / 180;
function kf(t, p) { if (t <= p[0][0]) return p[0][1]; for (let i = 0; i < p.length - 1; i++) if (t < p[i + 1][0]) return lerp(p[i][1], p[i + 1][1], sm((t - p[i][0]) / (p[i + 1][0] - p[i][0]))); return p[p.length - 1][1]; }
function kfl(t, p) { if (t <= p[0][0]) return p[0][1]; for (let i = 0; i < p.length - 1; i++) if (t < p[i + 1][0]) return lerp(p[i][1], p[i + 1][1], (t - p[i][0]) / (p[i + 1][0] - p[i][0])); return p[p.length - 1][1]; }
function kfv(t, p) { return [kf(t, p.map(q => [q[0], q[1][0]])), kf(t, p.map(q => [q[0], q[1][1]]))]; }
function herm(t, p) {
  if (t <= p[0][0]) return p[0][1];
  for (let i = 0; i < p.length - 1; i++) if (t < p[i + 1][0]) {
    const [t0, x0, v0] = p[i], [t1, x1, v1] = p[i + 1], d = t1 - t0, u = (t - t0) / d, u2 = u * u, u3 = u2 * u;
    return (2 * u3 - 3 * u2 + 1) * x0 + (u3 - 2 * u2 + u) * d * v0 + (-2 * u3 + 3 * u2) * x1 + (u3 - u2) * d * v1;
  }
  return p[p.length - 1][1];
}
const hash = n => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };

// ------------------------------------------------------------------ IK
const L1 = 50, L2 = 48, T1 = 31, T2 = 31, HIP = 9, SHX = 30, SHY = -73, PEL0 = -62;
function ik(H, F, l1, l2, pref) {
  let dx = F[0] - H[0], dy = F[1] - H[1], dist = Math.hypot(dx, dy) || 1e-6;
  const d = clamp(dist, Math.abs(l1 - l2) + .5, l1 + l2 - .3), ux = dx / dist, uy = dy / dist;
  const a = (l1 * l1 - l2 * l2 + d * d) / (2 * d), h = Math.sqrt(Math.max(0, l1 * l1 - a * a));
  const mx = H[0] + ux * a, my = H[1] + uy * a, k1 = [mx - uy * h, my + ux * h], k2 = [mx + uy * h, my - ux * h];
  const end = [H[0] + ux * d, H[1] + uy * d];
  const dot = (k1[0] - mx) * pref[0] + (k1[1] - my) * pref[1];
  return [dot >= 0 ? k1 : k2, end];
}
const rotv = (v, a) => [v[0] * Math.cos(a) - v[1] * Math.sin(a), v[0] * Math.sin(a) + v[1] * Math.cos(a)];

// ------------------------------------------------------------------ figure
function makeFig(key, parent) {
  const D = Z.chars[key], g = document.createElementNS(NS, 'g'); g.id = 'fig_' + key;
  const faces = Object.keys(D.faces).map(e => `<g class="fx" data-e="${e}" style="display:none">${D.faces[e]}</g>`).join('');
  const ink = '#161616';
  const limb = (c, w) => `<path class="${c}o" fill="none" stroke="${ink}" stroke-width="${w + 4.4}" stroke-linecap="round" stroke-linejoin="round"/>`;
  const limbf = (c, w, col) => `<path class="${c}f" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
  g.innerHTML =
    `<ellipse class="sh" cx="0" cy="2" rx="46" ry="9" fill="#000" opacity=".26"/>` +
    limb('lgB', 6.4) + limb('lgF', 6.4) + limbf('lgB', 6.4, D.trousers) + limbf('lgF', 6.4, D.trousers) +
    `<ellipse class="shB" rx="11" ry="5.2" fill="${ink}"/><ellipse class="shF" rx="11" ry="5.2" fill="${ink}"/>` +
    `<g class="torso"><g transform="translate(0,${-PEL0})">${D.torso}</g>` +
    `<g class="headg"><g transform="translate(0,150)">${D.headbase}${D.hair}<g class="feat">${faces}` +
    `<g class="blink" style="display:none"><rect x="-27" y="-210" width="54" height="17" fill="${D.skin}"/><path d="M-21 -198 Q-14 -194 -7 -198 M7 -198 Q14 -194 21 -198" stroke="${ink}" stroke-width="3.2" fill="none" stroke-linecap="round"/></g>` +
    `<g class="mouth"><circle cx="0" cy="-174" r="11.5" fill="${D.skin}"/>` +
    `<ellipse class="m1" cx="0" cy="-173" rx="5.5" ry="6" fill="${ink}"/><ellipse class="m2" cx="0" cy="-172" rx="8.5" ry="9.5" fill="${ink}"/><path class="m3" d="M-8 -176 Q0 -160 8 -176 Z" fill="${ink}"/></g>` +
    `${D.glasses}</g></g></g></g>` +
    limb('arB', 6.4) + limb('arF', 6.4) + limbf('arB', 6.4, D.coat) + limbf('arF', 6.4, D.coat) +
    `<circle class="hdB" r="6.4" fill="${D.skin}" stroke="${ink}" stroke-width="2.8"/><circle class="hdF" r="6.4" fill="${D.skin}" stroke="${ink}" stroke-width="2.8"/>`;
  parent.appendChild(g);
  const q = s => g.querySelector(s), qa = s => [...g.querySelectorAll(s)];
  return { g, key, torso: q('.torso'), headg: q('.headg'), feat: q('.feat'), fx: qa('.fx'), blink: q('.blink'), mouth: q('.mouth'), m: [null, q('.m1'), q('.m2'), q('.m3')],
           lgBo: q('.lgBo'), lgBf: q('.lgBf'), lgFo: q('.lgFo'), lgFf: q('.lgFf'), arBo: q('.arBo'), arBf: q('.arBf'), arFo: q('.arFo'), arFf: q('.arFf'),
           hdB: q('.hdB'), hdF: q('.hdF'), shB: q('.shB'), shF: q('.shF'), sh: q('.sh'), curE: null, last: {} };
}
const pts = (a, b, c) => `M${a[0].toFixed(1)} ${a[1].toFixed(1)}L${b[0].toFixed(1)} ${b[1].toFixed(1)}L${c[0].toFixed(1)} ${c[1].toFixed(1)}`;

// P: x, gy, s, f, pdy, lean, head, look, expr, mouth, blink, feet [[bx,by],[fx,fy]] local, hands [B,F] world|null, phi, wk
function setFig(F, P) {
  const fs = P.f >= 0 ? 1 : -1, s = P.s;
  F.g.setAttribute('transform', `translate(${P.x.toFixed(2)} ${P.gy.toFixed(2)}) scale(${(P.f * s).toFixed(4)} ${s})`);
  const wk = P.wk || 0, phi = P.phi || 0;
  const bob = -2.4 * wk * (1 - Math.cos(4 * Math.PI * phi)) / 2;
  const tt = P.t || 0, sd = F.key === 'reed' ? 0 : 1.7, tr = P.trem || 0;
  const pdy = (P.pdy || 0) + bob + .9 * Math.sin(2.1 * tt + sd), lean = (P.lean || 0) + 3 * wk + .9 * Math.sin(1.3 * tt + sd) + tr * 1.4 * Math.sin(tt * 23 + sd);
  const pel = [0, PEL0 + pdy];
  F.torso.setAttribute('transform', `translate(0 ${pel[1].toFixed(2)}) rotate(${lean.toFixed(2)})`);
  F.headg.setAttribute('transform', `translate(0 ${SHY - 15}) rotate(${((P.head || 0) + 1.3 * Math.sin(1.1 * tt + sd * 2) + tr * 2.2 * Math.sin(tt * 27 + sd)).toFixed(2)})`);
  // feet
  let feet = P.feet;
  if (!feet) {
    const A = 33, H = 14, f1 = u => { u -= Math.floor(u); return u < .6 ? [A - 2 * A * u / .6, 0] : (() => { const v = (u - .6) / .4; return [-A + 2 * A * sm(v), -H * Math.sin(Math.PI * v)]; })(); };
    const a = f1(phi), b = f1(phi + .5);
    feet = [[lerp(-11, a[0], wk), lerp(0, a[1], wk)], [lerp(11, b[0], wk), lerp(0, b[1], wk)]];
  }
  const kn = [], ft = [];
  [[-1, F.lgBo, F.lgBf, F.shB], [1, F.lgFo, F.lgFf, F.shF]].forEach(([sd, po, pf, sh], i) => {
    const H = [sd * HIP, pel[1]], [k, e] = ik(H, feet[i], T1, T2, [1, -.15]);
    const d = pts(H, k, e); po.setAttribute('d', d); pf.setAttribute('d', d);
    sh.setAttribute('cx', (e[0] + 4).toFixed(1)); sh.setAttribute('cy', (e[1] - 1).toFixed(1)); ft.push(e);
  });
  // arms: world targets -> local
  const w2l = w => [(w[0] - P.x) / (fs * s), (w[1] - P.gy) / s];
  const lr = lean * D2R, hw = [null, null];
  [[-1, P.hands && P.hands[0], F.arBo, F.arBf, F.hdB, 0], [1, P.hands && P.hands[1], F.arFo, F.arFf, F.hdF, 1]].forEach(([sd, tw, po, pf, hd, i]) => {
    const sh = rotv([sd * SHX, SHY], lr); const S = [pel[0] + sh[0], pel[1] + sh[1]];
    let tgt;
    if (tw) tgt = w2l(tw);
    else tgt = [sd * 50 + (i === 0 ? 1 : -1) * 22 * Math.sin(2 * Math.PI * phi) * wk, -72 + pdy * .7];
    const [el, en] = ik(S, tgt, L1, L2, [sd * .9, .35]);
    const d = pts(S, el, en); po.setAttribute('d', d); pf.setAttribute('d', d);
    hd.setAttribute('cx', en[0].toFixed(1)); hd.setAttribute('cy', en[1].toFixed(1));
    hw[i] = [P.x + en[0] * fs * s, P.gy + en[1] * s];
  });
  F.last = { hands: hw, feet: ft, f: P.f, x: P.x, gy: P.gy, s, lean };
  // face
  const e = P.expr || 'neutral';
  if (F.curE !== e) { F.fx.forEach(n => n.style.display = n.dataset.e === e ? '' : 'none'); F.curE = e; }
  F.feat.setAttribute('transform', `translate(${((P.look || 0) * 6.5).toFixed(2)} ${(P.nod || 0).toFixed(2)})`);
  F.blink.style.display = P.blink ? '' : 'none';
  [1, 2, 3].forEach(i => F.m[i].style.display = (P.mouth === i) ? '' : 'none');
  F.mouth.style.display = P.mouth ? '' : 'none';
  return F.last;
}

// ------------------------------------------------------------------ choreography
const GYR = 580, GYM = 598, SR = .95, SM = .97;
const SHELF_X0 = 1100, SHELF_Y = 556, BOLT = [[1117, 560], [1273, 560]];
const DOOR = { x0: 1085, w: 120, yt: 340, yb: 555 };
const IN = { desk: [3640, 3890], rec: [3850, 436] };
const LINE_T = { n1a: .5, n1b: 4.5, r1: 11.3, m1: 17.3, n2: 23.6, m2: 36.4, r2: 45.4, n3: 47.9, g1: 55.0 };
const shelfD = t => 250 * sm(seg(t, 28.4, 30.9)) + (t > 28.4 && t < 30.9 ? 2.2 * Math.sin(t * 19) * Math.sin(Math.PI * seg(t, 28.4, 30.9)) : 0);
const doorA = t => 76 * sm(seg(t, 34.3, 36.7));
const handleRot = t => 38 * sm(seg(t, 33.4, 33.9)) * (1 - sm(seg(t, 36.5, 36.9)));
const doorFar = t => DOOR.x0 + DOOR.w * Math.cos(doorA(t) * D2R);
const handlePos = t => [doorFar(t) - 16 * Math.cos(doorA(t) * D2R), 470 + 0.45 * handleRot(t)];
const speedOf = (xf, t) => Math.abs(xf(t + .02) - xf(t - .02)) / .04;
function distTable(xf) { const N = 60 * 240 + 1, c = new Float32Array(N); for (let i = 1; i < N; i++) c[i] = c[i - 1] + Math.abs(xf(i / 240) - xf((i - 1) / 240)); return c; }
const distAt = (c, t) => { const i = clamp(t * 240, 0, c.length - 1.001), k = Math.floor(i); return lerp(c[k], c[k + 1], i - k); };
const STRIDE = 114;

// --- Reed
function reedX(t) {
  if (t < 41) {
    if (t < 26.4) return herm(t, [[0, -154, 140], [9.1, 1120, 140], [9.9, 1218, 0], [26.4, 1218, 0]]);
    if (t < 27.9) return herm(t, [[26.4, 1218, 0], [26.7, 1212, -110], [27.6, 1050, -60], [27.9, 1036, 0]]);
    if (t < 30.9) return 1036 + shelfD(t);
    if (t < 32.2) return herm(t, [[30.9, 1286, 0], [31.2, 1284, -30], [32.2, 1262, 0]]);
    if (t < 34.3) return 1262;
    if (t < 36.7) return handlePos(t)[0] + 70;
    if (t < 38.2) return handlePos(36.7)[0] + 70;
    return herm(t, [[38.2, handlePos(36.7)[0] + 70, 0], [38.7, handlePos(36.7)[0] + 66, -55], [41.0, 1090, -35]]);
  }
  return herm(t, [[41.0, 4235, -95], [44.6, 3925, -20], [45.2, 3925, 0]]);
}
const reedDist = distTable(reedX);
// --- Morgan
function morganX(t) {
  if (t < 41.5) {
    if (t < 22.9) return herm(t, [[0, -345, 140], [9.3, 957, 140], [9.9, 975, 0], [22.9, 975, 0]]);
    if (t < 24.3) return herm(t, [[22.9, 975, 0], [23.3, 985, 60], [24.1, 1062, 0]]);
    if (t < 27.7) return 1062;
    if (t < 28.4) return herm(t, [[27.7, 1062, 0], [28.4, 1128, 0]]);
    if (t < 30.95) return 1128 + shelfD(t);
    return herm(t, [[30.95, 1378, 0], [31.5, 1362, -50], [33.4, 1335, -40], [34.0, 1325, 0]]);
  }
  return herm(t, [[41.5, 4245, -95], [45.4, 4040, -30], [46.2, 4040, 0]]);
}
const morganDist = distTable(morganX);

// facing (continuous: scale x = f*s)
const flip = (t, a, b, from, to) => lerp(from, to, sm(seg(t, a, b)));
function reedF(t) {
  if (t < 26.4) return 1;
  if (t < 27.75) return flip(t, 26.4, 26.7, 1, -1);
  if (t < 30.7) return flip(t, 27.75, 28.05, -1, 1);
  if (t < 57.4) return flip(t, 30.7, 31.0, 1, -1);
  return flip(t, 57.4, 57.7, -1, 1);
}
function morganF(t) {
  if (t < 10.0) return 1;
  if (t < 10.9) return flip(t, 10.0, 10.3, 1, -1);
  if (t < 30.9) return flip(t, 11.1, 11.4, -1, 1);
  return flip(t, 30.9, 31.2, 1, -1);
}
// mouth states from the real audio envelope of each line
function mouthAt(t, who) {
  for (const l of Z.lines) {
    if (l.who !== who) continue; const k = Math.floor((t - l.t0) * 30);
    if (k >= 0 && k < l.env.length) { const e = l.env[k]; return e > .5 ? 2 : e > .22 ? 1 : e > .09 ? (k % 2 ? 1 : 0) : 0; }
  }
  return 0;
}
const blinkAt = (t, seed) => { const per = 3.2 + seed * .37, ph = (t + seed * 1.3) % per; return ph < .13; };

// world-space helpers for props that are driven by the hands
const PR = {};   // filled by renderAt each frame: world props placements

function reedPose(t) {
  const x = reedX(t), f = reedF(t), spd = speedOf(reedX, t), wk = sm(spd / 28), phi = distAt(reedDist, t) / STRIDE;
  const P = { t, trem: sm(seg(t, 55.0, 55.3)), x, gy: GYR, s: SR, f, pdy: 0, lean: 0, head: 0, look: 0, expr: 'neutral', mouth: mouthAt(t, 'REED'), blink: blinkAt(t, 1), wk, phi, hands: [null, null], feet: null };
  const hands = [null, null];
  const fl = { on: true, tgt: [x + 340 * (f >= 0 ? 1 : -1), 556], hold: null };   // flashlight in the BACK (B) hand
  const front = { prop: null };
  // ---- S1/S2 walk in: flashlight swings over the floor and wall, then settles on the shelf
  if (t < 9.9) {
    const sw = Math.sin(t * 1.7);
    fl.tgt = [x + 330, kf(t, [[0, 560], [4, 520], [6.5, 470], [9.6, 500]]) + 40 * sw];
    P.expr = t > 6 ? 'determined' : 'neutral'; P.head = 2 * Math.sin(t * 1.3);
    P.look = t < 4 ? 0 : (t < 5 ? .6 : 0);
  }
  // ---- S2: crouch and examine the bolts (back flashlight stays on the bolts)
  const crouch = (a, b, c, d) => sm(seg(t, a, b)) * (1 - sm(seg(t, c, d)));
  P.pdy = 30 * crouch(9.9, 10.7, 26.0, 26.9);
  P.lean = 18 * crouch(9.9, 10.7, 26.0, 26.9);
  if (P.pdy > 1) { P.feet = [[-14, 0], [22, 0]]; }
  if (t >= 9.9 && t < 26.9) {
    fl.tgt = [BOLT[1][0] + 14, BOLT[1][1] + 6];
    const hb = [BOLT[1][0] - 10 + 0, BOLT[1][1] - 4];
    // front hand: reaches to the bolt head at 9.4, taps it twice (metal tap) 11.0 / 11.5, rests on knee while he talks
    const reach = sm(seg(t, 10.7, 11.2)) * (1 - sm(seg(t, 13.6, 14.2)));
    const tap = (t > 12.4 && t < 12.65) ? Math.sin((t - 12.4) / .25 * Math.PI) : ((t > 12.9 && t < 13.15) ? Math.sin((t - 12.9) / .25 * Math.PI) : 0);
    P.head = 14 * crouch(9.9, 10.7, 26, 26.9) - (t > 18.0 && t < 23 ? 24 * sm(seg(t, 18.0, 18.6)) * (1 - sm(seg(t, 22.2, 22.9))) : 0);
    P.look = (t < 18.0 ? 0.7 : (t < 22.5 ? -1 : .7));              // turns his head toward Morgan / the strip on her line
    P.expr = t > 17.3 && t < 22.5 ? 'surprised' : 'determined';
    if (t < 23.2) {
      const kneeRest = [x + 26, GYR - 38];
      hands[1] = [lerp(kneeRest[0], hb[0], reach), lerp(kneeRest[1], hb[1] - 3 * tap, reach)];
      hands[1][1] -= 6 * tap * reach;
    }
  }
  // ---- S4: Reed's bolt (wrench from the coat pocket, 4 ratchet strokes, lift, drop)
  const T0 = 23.4;
  if (t >= 23.0 && t < 26.9) {
    const pocket = [x + 22 * 0.95 * (f >= 0 ? 1 : -1), GYR - (62 - P.pdy + 4) * .95 + 0];
    const pk = (() => { const p = reedPocket(P); return p; })();
    const reachP = sm(seg(t, 23.0, 23.4)), toBolt = sm(seg(t, 23.7, 24.1)), lift = sm(seg(t, T0 + 1.9, T0 + 2.4));
    const ang = ratchet(t, T0 + .7, T0 + 1.9, 4);
    const hbolt = [BOLT[1][0], BOLT[1][1] - 10 - 16 * sm(seg(t, T0 + .7, T0 + 1.9)) - 34 * lift];
    let h;
    if (t < 23.7) h = [lerp(x + 20, pk[0], reachP), lerp(GYR - 40, pk[1], reachP)];
    else h = [lerp(pk[0], hbolt[0] - 6, toBolt), lerp(pk[1], hbolt[1], toBolt)];
    hands[1] = h;
    front.prop = 'wrench'; front.ang = ang; front.pocketPhase = t < 23.7 && reachP < .8;
    P.expr = 'determined';
  }
  if (t >= 26.0 && t < 26.9) { const u = sm(seg(t, 26.0, 26.9)); }
  // ---- S4: pushing the shelf (front hand on the left upright), then S5 door
  if (t >= 27.8 && t < 30.95) {
    const hp = [SHELF_X0 + shelfD(t) - 2, 436];
    hands[1] = [lerp(x + 24, hp[0], sm(seg(t, 27.8, 28.3))), lerp(GYR - 100, hp[1], sm(seg(t, 27.8, 28.3)))];
    P.lean = 10 + 6 * sm(seg(t, 28.4, 29.0));
    P.expr = 'determined'; fl.tgt = [x + 300, 500];
    if (t >= 28.4 && t < 30.9) P.look = 0;
  }
  if (t >= 30.95 && t < 33.1) {
    fl.tgt = [1150, 470]; P.expr = 'neutral';
    if (t > 32.3) hands[1] = [lerp(x - 22, handlePos(t)[0] + 2, sm(seg(t, 32.3, 33.1))), lerp(GYR - 80, handlePos(t)[1], sm(seg(t, 32.3, 33.1)))];
  }
  if (t >= 33.1 && t < 38.2) {
    const hp = handlePos(t); hands[1] = [hp[0] + 3, hp[1] - 1];
    fl.tgt = [1135, 470]; P.expr = t > 36.5 ? 'surprised' : 'determined';
    P.look = 0; P.head = t > 36.7 ? -4 : 0;
  }
  if (t >= 38.2 && t < 41.0) { fl.tgt = [1110, 470]; P.expr = 'determined'; }
  // walking into the doorway: step away from the camera (smaller + higher) as he passes through the door plane
  if (t >= 38.2 && t < 41.0) {
    const u = sm(seg(t, 38.9, 40.8)); P.s = lerp(SR, SR * .7, u); P.gy = lerp(GYR, GYR - 36, u);
  }
  // ---- S6: interior
  if (t >= 41.0) {
    const e = sm(seg(t, 41.0, 41.9)); P.s = lerp(SR * .8, SR, e); P.gy = lerp(GYR - 22, GYR, e);
    fl.tgt = reedBeam(t); P.expr = 'determined';
    if (t > 44.8) P.pdy = 0;
    // point at the recorder (front arm straight at it) 45.2-47.9
    const pt = sm(seg(t, 45.0, 45.7)) * (1 - sm(seg(t, 48.4, 49.0)));
    if (t < 51.0) {
      if (pt > .01) hands[1] = [lerp(x - 20, IN.rec[0] + 26, pt), lerp(GYR - 95, IN.rec[1] - 14, pt)];
      P.head = -4 * pt; P.look = -.6 * pt;
    }
    if (t >= 51.0) {
      // pick up: hand to the recorder (51.0-51.5), lift toward the chest (51.5-52.3), hold; thumb presses play 52.5
      const a = sm(seg(t, 50.6, 51.3)), b = sm(seg(t, 51.3, 52.3));
      const rest = [IN.rec[0] + 10, IN.rec[1] + 24], up = [x - 56, GYR - 135];
      const h0 = [lerp(x - 22, rest[0], a), lerp(GYR - 95, rest[1], a)];
      hands[1] = [lerp(h0[0], up[0], b), lerp(h0[1], up[1], b)];
      // shock recoil when the girl speaks
      const rc = sm(seg(t, 55.0, 55.25)) * (1 - sm(seg(t, 55.6, 56.4)));
      hands[1][0] += 8 * rc; P.lean = -8 * rc; P.feet = null;
      P.expr = t < 54.9 ? 'worried' : 'shocked';
      if (t >= 56.3) P.expr = 'shocked';
      P.look = t < 52.5 ? -.7 : (t < 56.6 ? -.9 : (t < 58 ? 0 : .8));
      P.head = t >= 56.5 ? -5 : 0;
      // body turns toward Morgan at 57.4 (see reedF); eyes on her
    }
    if (t < 51.0 && t < 44.6) P.head = 3 * Math.sin(t * 2);
  }
  P.hands = hands;
  return { P, fl, front };
}
function reedPocket(P) {   // world position of the coat pocket flap (front hand side)
  const fs = P.f >= 0 ? 1 : -1, l = [23, -85 + (P.pdy || 0)], r = (P.lean || 0) * D2R, p = rotv([l[0], l[1] - (PEL0 + (P.pdy || 0))], r);
  return [P.x + (p[0]) * fs * P.s, P.gy + (PEL0 + (P.pdy || 0) + p[1]) * P.s];
}
function ratchet(t, a, b, n) {   // wrench rocking: forward stroke (turn), return swing, repeated n times; returns degrees
  if (t < a) return 0; if (t > b) return 0;
  const u = (t - a) / (b - a) * n, k = u - Math.floor(u);
  return k < .55 ? -38 * sm(k / .55) : -38 * (1 - sm((k - .55) / .45));
}
function reedBeam(t) {
  return kfv(t, [[41.0, [4040, 560]], [41.9, [3930, 540]], [42.5, [3800, 470]], [43.0, [3790, 470]], [43.9, [3570, 410]], [44.5, [3560, 410]], [44.9, [3380, 470]], [45.0, [3380, 470]], [45.9, [3760, 458]], [46.6, [3850, 440]], [52, [3850, 440]], [53, [3850, 440]], [60, [3850, 440]]]);
}
// --- Morgan
function morganPose(t) {
  const x = morganX(t), f = morganF(t), spd = speedOf(morganX, t), wk = sm(spd / 28), phi = distAt(morganDist, t) / STRIDE;
  const P = { t, trem: sm(seg(t, 55.0, 55.3)), x, gy: GYM, s: SM, f, pdy: 0, lean: 0, head: 0, look: 0, expr: 'neutral', mouth: mouthAt(t, 'MORGAN'), blink: blinkAt(t, 2), wk, phi, hands: [null, null], feet: null };
  const fl = { on: true, tgt: [x + 330, 540] };
  const hands = [null, null]; const front = { prop: null };
  if (t < 9.9) {
    fl.tgt = [x + 320, 545 - 40 * Math.sin(t * 1.4 + 1) + kf(t, [[0, 0], [7, -60], [9.6, -25]])]; P.head = 2 * Math.sin(t * 1.1 + 1);
    P.expr = t > 5 ? 'determined' : 'neutral';
  }
  // 9.8-10.9 she checks behind (faces left, light sweeping the basement); then turns to Reed (see morganF) and lights the shelf
  if (t >= 9.9 && t < 11.1) { fl.tgt = [x - 330 + 120 * Math.sin((t - 9.9) * 3), 540]; P.expr = 'worried'; }
  if (t >= 11.1 && t < 15.0) { fl.tgt = kfv(t, [[11.1, [1040, 520]], [12.5, [1090, 500]], [14.6, [1050, 450]], [15.0, [1000, 460]]]); P.expr = 'neutral'; P.look = .5 + .3 * sm(seg(t, 11.0, 11.8)); P.head = 0; }
  // S3: sweep behind the shelf: beam travels along the wall edge, lands on the strip of blue paint at 16.7
  if (t >= 15.0 && t < 23.0) {
    fl.tgt = kfv(t, [[15.0, [1000, 460]], [16.9, [1090, 440]], [18.0, [1093, 380]], [19.6, [1093, 505]], [21.0, [1093, 430]], [22.9, [1093, 430]]]);
    P.expr = t > 16.7 ? 'surprised' : 'determined'; P.head = t > 16.7 ? 4 : 0; P.look = .8;
    if (t > 17.0) hands[1] = [lerp(x + 30, x + 78, sm(seg(t, 17.0, 17.6))), lerp(GYM - 70, GYM - 150, sm(seg(t, 17.0, 17.6)))];  // points toward the strip while speaking
    if (t > 19.2) hands[1] = null;
    { const u = sm(seg(t, 15.0, 15.8)) * (1 - sm(seg(t, 22.3, 22.9))); hands[0] = [lerp(x - 50 * (f >= 0 ? 1 : -1), x + 34 * (f >= 0 ? 1 : -1), u), lerp(GYM - 72, GYM - 148, u)]; }
  }
  // S4: walks to the right bolt, crouches, ratchet
  if (t >= 23.0 && t < 27.7) {
    fl.tgt = t < 24.4 ? [x + 260, 500] : [BOLT[0][0] + 18, BOLT[0][1] + 8];
    const cr = sm(seg(t, 24.4, 25.0)) * (1 - sm(seg(t, 27.1, 27.7)));
    P.pdy = 30 * cr; P.lean = 17 * cr; if (cr > .02) P.feet = [[-14, 0], [22, 0]];
    P.head = 12 * cr; P.expr = 'determined';
    const T0 = 25.3;
    if (t >= 24.9) {
      const pk = reedPocket(P);
      const reachP = sm(seg(t, 24.9, 25.2)), toBolt = sm(seg(t, 25.35, 25.75)), lift = sm(seg(t, T0 + 1.9, T0 + 2.35));
      const hbolt = [BOLT[0][0], BOLT[0][1] - 10 - 16 * sm(seg(t, T0 + .6, T0 + 1.9)) - 34 * lift];
      let h; if (t < 25.35) h = [lerp(x + 20, pk[0], reachP), lerp(GYM - 40, pk[1], reachP)]; else h = [lerp(pk[0], hbolt[0] - 6, toBolt), lerp(pk[1], hbolt[1], toBolt)];
      hands[1] = h; front.prop = 'wrench'; front.ang = ratchet(t, T0 + .6, T0 + 1.9, 4); front.pocketPhase = t < 25.35 && reachP < .8;
    }
  }
  // S4: both push
  if (t >= 28.4 && t < 30.95) {
    const hp = [1190 + shelfD(t), 470]; const u = sm(seg(t, 28.0, 28.5));
    hands[1] = [lerp(x + 24, hp[0], u), lerp(GYM - 100, hp[1], u)];
    P.lean = 10 + 6 * sm(seg(t, 28.4, 29.0)); P.expr = 'determined'; fl.tgt = [x + 300, 500];
  }
  if (t >= 30.95 && t < 41.5) {
    fl.tgt = t < 33.0 ? [1180, 470] : kfv(t, [[33.0, [1160, 470]], [34.3, [1130, 470]], [35.5, [1110, 470]], [41.0, [1105, 470]]]);
    P.expr = t > 34.3 ? 'surprised' : 'determined'; if (t > 36.3) P.expr = 'worried';
    P.look = 0;
  }
  if (t >= 41.5) {
    const e = sm(seg(t, 41.5, 42.4)); P.s = lerp(SM * .8, SM, e); P.gy = lerp(GYM - 22, GYM, e);
    fl.tgt = kfv(t, [[41.5, [4020, 540]], [43.0, [3900, 500]], [44.3, [3750, 470]], [46.0, [3720, 455]], [52, [3850, 440]], [60, [3850, 440]]]);
    P.expr = 'determined';
    if (t >= 52.0) { P.expr = t < 54.9 ? 'worried' : 'shocked'; }
    if (t >= 55.0) { const rc = sm(seg(t, 55.0, 55.25)) * (1 - sm(seg(t, 55.6, 56.4))); P.lean = -6 * rc; P.expr = 'shocked'; }
    P.look = t < 56.5 ? -.5 : -1;
    if (t > 57.4) hands[1] = [x - 38, GYM - 105];   // hand rises toward her mouth
    if (t > 57.4) { const u = sm(seg(t, 57.4, 58.2)); hands[1] = [lerp(x - 20, x - 40, u), lerp(GYM - 90, GYM - 148, u)]; }
  }
  P.hands = hands; return { P, fl, front };
}

// ------------------------------------------------------------------ camera (hard cuts at 7/15/23/32/41/51/56 s)
function camAt(t) {
  const L = (a, b, c) => kfl(t, [[a[0], a[1]], [b[0], b[1]]]);
  if (t < 7) return [kfl(t, [[0, 520], [7, 640]]), 392, 1.0];
  if (t < 15) return [kfl(t, [[7, 900], [15, 1090]]), kfl(t, [[7, 424], [15, 446]]), kfl(t, [[7, 1.28], [15, 1.4]])];
  if (t < 23) return [kfl(t, [[15, 1100], [23, 1110]]), 432, kfl(t, [[15, 1.9], [23, 2.05]])];
  if (t < 32) return [kfl(t, [[23, 1150], [28, 1190], [31, 1300], [32, 1300]]), 444, kfl(t, [[23, 1.35], [28, 1.35], [32, 1.2]])];
  if (t < 41) return [kfl(t, [[32, 1230], [38, 1190], [41, 1135]]), kfl(t, [[32, 444], [38, 440], [41, 470]]), kfl(t, [[32, 1.65], [38, 1.7], [41, 2.5]])];
  if (t < 51) return [kfl(t, [[41, 4150], [46, 3880], [51, 3830]]), 450, kfl(t, [[41, 1.55], [46, 1.8], [51, 2.0]])];
  if (t < 56) return [kfl(t, [[51, 3850], [52.3, 3850]]), kfl(t, [[51, 430], [52.4, 398]]), kfl(t, [[51, 1.8], [52.4, 3.3]])];
  return [3960, 418, 1.95];
}

// ------------------------------------------------------------------ beams + dust
const BEAM_A = 11.5 * D2R;
function beamPoly(tip, ang, L) {
  const pts = [tip], n = 6;
  for (let i = 0; i <= n; i++) { const a = ang - BEAM_A + 2 * BEAM_A * i / n; pts.push([tip[0] + Math.cos(a) * L, tip[1] + Math.sin(a) * L]); }
  return pts.map(p => p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
}
const DUST = Array.from({ length: 150 }, (_, i) => ({ x0: hash(i) , y0: hash(i + 500), r: .9 + hash(i + 900) * 1.7, ph: hash(i + 1300) * 6.3 }));

// ------------------------------------------------------------------ build DOM
let figR, figM, els = {};
function build() {
  const w = $('world');
  w.insertAdjacentHTML('beforeend', `<g id="bgB">${Z.art.basement}</g><g id="bgI">${Z.art.interior}</g>`);
  // interior objects (revealed one at a time) + recorder
  Object.keys(Z.art.iobj).forEach(k => w.insertAdjacentHTML('beforeend', `<g id="io_${k}">${Z.art.iobj[k]}</g>`));
  // door: base wall-coloured cover for the strip reveal, door polygon, handle
  w.insertAdjacentHTML('beforeend',
    `<polygon id="doorP" fill="#2b6cc4" stroke="#161616" stroke-width="3.6" stroke-linejoin="round"/><g id="doorD"></g>` +
    `<g id="handle"><circle r="7" fill="#c9b36a" stroke="#161616" stroke-width="2.6"/><path d="M0 0 H-24" stroke="#161616" stroke-width="9" stroke-linecap="round"/><path d="M0 0 H-24" stroke="#d8c27a" stroke-width="5" stroke-linecap="round"/></g>` +
    `<rect id="stripCover" x="1085" y="340" width="15" height="215" fill="#283246"/>` +
    `<g id="holes"><ellipse cx="1117" cy="563" rx="9" ry="3.6" fill="#07080c"/><ellipse cx="1273" cy="563" rx="9" ry="3.6" fill="#07080c"/></g>` +
    `<g id="shelf">${Z.art.shelf}</g>` +
    `<g id="bolt0"><g class="bsc">${Z.art.bolt}</g></g><g id="bolt1"><g class="bsc">${Z.art.bolt}</g></g>`);
  // darkness overlay (strong, masked by the beams) -> dust -> characters -> props -> light glow -> uniform grade
  w.insertAdjacentHTML('beforeend',
    `<rect id="dark" x="-900" y="-400" width="5600" height="1500" fill="#03050b" mask="url(#dm)"/>` +
    `<g id="dust" clip-path="url(#bclip)"></g><g id="chars"></g><g id="props"></g>` +
    `<g id="glow"><polygon id="gl1" fill="#ffe6a0" opacity=".13" filter="url(#bl2)"/><polygon id="gl2" fill="#ffe6a0" opacity=".13" filter="url(#bl2)"/>` +
    `<circle id="lamp1" r="9" fill="#fff3c2" opacity=".9" filter="url(#bl2)"/><circle id="lamp2" r="9" fill="#fff3c2" opacity=".9" filter="url(#bl2)"/></g>` +
    `<rect id="grade" x="-900" y="-400" width="5600" height="1500" fill="#0a1020" opacity=".16"/>`);
  figM = makeFig('morgan', $('chars')); figR = makeFig('reed', $('chars'));
  // props in world layer (above characters): flashlights, wrench(es), recorder, thumb, hit sparks
  $('props').insertAdjacentHTML('beforeend',
    `<g id="flR">${Z.art.flash}</g><g id="flM">${Z.art.flash}</g><g id="wrR">${Z.art.wrench}</g><g id="wrM">${Z.art.wrench}</g>` +
    `<g id="pocketR"></g>` +
    `<g id="rec"><g id="recbody">${Z.art.rec}</g><g id="scr"></g><g id="recbtn"><circle r="4.6" cy="19" fill="#3fbf6a" stroke="#161616" stroke-width="2"/><path d="M-1.6 16.8 L2.6 19 L-1.6 21.2 Z" fill="#0b2a14"/></g><g id="recglow"></g></g>` +
    `<circle id="gripH" r="6.2" fill="#f3cda1" stroke="#161616" stroke-width="2.8"/><g id="thumbg"><ellipse id="thumb" rx="4.6" ry="6.2" fill="#f3cda1" stroke="#161616" stroke-width="2.4"/></g>`);
  // waveform bars
  let bars = ''; for (let i = 0; i < 9; i++) bars += `<rect class="wb" x="${-11 + i * 2.7}" y="-5" width="1.9" height="3" fill="#59f08a"/>`;
  $('scr').innerHTML = `<rect id="scrfill" x="-13" y="-16" width="26" height="19" rx="3" fill="#0d3a1f" opacity="0"/>${bars}<circle id="scrdot" cx="9" cy="-12" r="1.6" fill="#ff4b4b" opacity="0"/>`;
  els.wb = [...document.querySelectorAll('.wb')];
  // dust
  $('dust').innerHTML = DUST.map(() => '<circle fill="#fff"/>').join(''); els.dust = [...$('dust').children];
  els.caps = [];
  Z.caps.forEach((c, i) => {
    const full = (c.label ? c.label + ' ' : '') + c.text; let l1 = full, l2 = '';
    if (full.length > 56) { const m = full.lastIndexOf(' ', Math.floor(full.length / 2) + 6); l1 = full.slice(0, m); l2 = full.slice(m + 1); }
    const sz = Math.min(38, 1120 / (Math.max(l1.length, l2.length) * .57)), lab = c.label ? c.label.length + 1 : 0;
    const ln = (s, y, off) => `<text x="640" y="${y}" text-anchor="middle" font-size="${sz.toFixed(1)}"><tspan fill="${c.col}">${s.slice(0, Math.max(0, lab - off))}</tspan><tspan fill="#fff">${s.slice(Math.max(0, lab - off))}</tspan></text>`;
    $('capsg').insertAdjacentHTML('beforeend', `<g class="cap" data-i="${i}" style="display:none">${l2 ? ln(l1, 624, 0) + ln(l2, 664, l1.length + 1) : ln(l1, 660, 0)}</g>`);
  });
  els.caps = [...document.querySelectorAll('.cap')];
}

// ------------------------------------------------------------------ frame
function propAt(id, p, ang, sc) { $(id).setAttribute('transform', `translate(${p[0].toFixed(1)} ${p[1].toFixed(1)}) rotate(${ang.toFixed(1)}) scale(${sc || 1})`); }
const vis = (id, on) => { const e = $(id); const d = on ? '' : 'none'; if (e.style.display !== d) e.style.display = d; };
function lampOf(S, fl) {
  const hb = S.hands[0], tgt = fl.tgt, ang = Math.atan2(tgt[1] - hb[1], tgt[0] - hb[0]);
  return { hand: hb, ang, tip: [hb[0] + Math.cos(ang) * 32, hb[1] + Math.sin(ang) * 32] };
}
window.renderAt = function (t) {
  if (!figR) build();
  const R = reedPose(t), M = morganPose(t);
  const SRr = setFig(figR, R.P), SMr = setFig(figM, M.P);
  const inRoom = t >= 41.0;
  vis('bgB', !inRoom); vis('bgI', inRoom);
  ['boxes', 'phone_gear', 'desk', 'handset'].forEach(k => vis('io_' + k, inRoom));
  ['doorP', 'doorD', 'handle', 'stripCover', 'holes', 'shelf', 'bolt0', 'bolt1'].forEach(k => vis(k, !inRoom));
  // camera
  const c = camAt(t);
  $('cam').setAttribute('transform', `translate(640 360) scale(${c[2].toFixed(4)}) translate(${(-c[0]).toFixed(2)} ${(-c[1]).toFixed(2)})`);
  // ---- shelf, door, bolts (basement)
  if (!inRoom) {
    const d = shelfD(t); $('shelf').setAttribute('transform', `translate(${SHELF_X0 + d} ${SHELF_Y})`);
    $('stripCover').setAttribute('opacity', (1 - sm(seg(t, 16.75, 17.15))).toFixed(3));
    // door polygon on hinges (hinge left, swings inward = away from the viewer)
    const a = doorA(t) * D2R, fx = DOOR.x0 + DOOR.w * Math.cos(a), k = 34 * Math.sin(a);
    $('doorP').setAttribute('points', `${DOOR.x0},${DOOR.yt} ${fx.toFixed(1)},${(DOOR.yt + k).toFixed(1)} ${fx.toFixed(1)},${(DOOR.yb - k).toFixed(1)} ${DOOR.x0},${DOOR.yb}`);
    const pn = (u0, u1, v0, v1) => { const xa = DOOR.x0 + DOOR.w * u0 * Math.cos(a), xb = DOOR.x0 + DOOR.w * u1 * Math.cos(a), ya = k * u0, yb = k * u1;
      const ht = DOOR.yb - DOOR.yt; return `${xa.toFixed(1)},${(DOOR.yt + ht * v0 + ya * (1 - 2 * v0)).toFixed(1)} ${xb.toFixed(1)},${(DOOR.yt + ht * v0 + yb * (1 - 2 * v0)).toFixed(1)} ${xb.toFixed(1)},${(DOOR.yt + ht * v1 + yb * (1 - 2 * v1)).toFixed(1)} ${xa.toFixed(1)},${(DOOR.yt + ht * v1 + ya * (1 - 2 * v1)).toFixed(1)}`; };
    $('doorD').innerHTML = [[.12, .88, .08, .46], [.12, .88, .54, .92]].map(q => `<polygon points="${pn(...q)}" fill="#245aa6" stroke="#161616" stroke-width="2.4"/>`).join('');
    const hp = handlePos(t); $('handle').setAttribute('transform', `translate(${hp[0].toFixed(1)} ${hp[1].toFixed(1)}) rotate(${(-handleRot(t) * .55).toFixed(1)})`);
    // bolts: rise during the ratchet strokes, lift out with the wrench, fall to the floor
    boltState(0, t, 25.3, BOLT[0], [1086, 574], M, 1);
    boltState(1, t, 23.4, BOLT[1], [1296, 577], R, 1);
  }
  // ---- held props (world layer)
  const fR = lampOf(SRr, R.fl), fM = lampOf(SMr, M.fl);
  propAt('flR', fR.hand, fR.ang / D2R, 1); propAt('flM', fM.hand, fM.ang / D2R, 1);
  // wrenches
  wrenchProp('wrR', R, SRr, t); wrenchProp('wrM', M, SMr, t);
  vis('pocketR', false);
  // ---- recorder (picked up by Reed at 51)
  recorder(t, SRr, R);
  // ---- beams
  const b1 = beamPoly(fR.tip, fR.ang, inRoom ? 640 : 520), b2 = beamPoly(fM.tip, fM.ang, inRoom ? 640 : 520);
  ['mb1', 'cb1', 'gl1'].forEach(id => $(id).setAttribute('points', b1)); ['mb2', 'cb2', 'gl2'].forEach(id => $(id).setAttribute('points', b2));
  $('lamp1').setAttribute('cx', fR.tip[0]); $('lamp1').setAttribute('cy', fR.tip[1]); $('lamp2').setAttribute('cx', fM.tip[0]); $('lamp2').setAttribute('cy', fM.tip[1]);
  $('dark').setAttribute('opacity', (inRoom ? .955 : .70).toString());
  // mask patches for interior objects once revealed (remain faintly visible)
  [['p_desk', 42.2, .5], ['p_gear', 43.5, .5], ['p_box', 44.4, .5], ['p_hand', 45.3, .5], ['p_rec', 45.9, .75]].forEach(([id, t0, a]) => { $(id).setAttribute('opacity', (inRoom ? a * sm(seg(t, t0, t0 + .6)) : 0).toFixed(3)); });
  // ---- dust (world-fixed motes, visible where the beams cross them)
  const reg = inRoom ? [3250, 4200] : [850, 1500];
  els.dust.forEach((e, i) => {
    const q = DUST[i], x = reg[0] + q.x0 * (reg[1] - reg[0]) + 14 * Math.sin(t * .45 + q.ph) + 5 * t * .3 % 1, y = 300 + q.y0 * 270 + 10 * Math.sin(t * .6 + q.ph * 2) - 6 * Math.sin(t * .2 + q.ph);
    e.setAttribute('cx', x.toFixed(1)); e.setAttribute('cy', y.toFixed(1)); e.setAttribute('r', q.r.toFixed(2)); e.setAttribute('opacity', (.35 + .5 * Math.abs(Math.sin(t * 1.1 + q.ph * 3))).toFixed(2));
  });
  // ---- captions + fades
  els.caps.forEach((e, i) => { const c = Z.caps[i], on = t >= c.t0 && t < c.t1; if (e.style.display !== (on ? '' : 'none')) e.style.display = on ? '' : 'none'; });
  const fade = t < .35 ? 1 - t / .35 : 0, xfade = Math.max(0, 1 - Math.abs(t - 41.0) / .01) * 0;
  const nb = t >= 59.9 ? 1 : Math.max(fade, 0);
  $('blackout').setAttribute('opacity', nb.toFixed(3));
  const cutIn = .7 * (t >= 40.55 && t < 41.0 ? sm(seg(t, 40.55, 40.95)) : (t >= 41.0 && t < 41.35 ? 1 - sm(seg(t, 41.0, 41.35)) : 0));
  $('xblack').setAttribute('opacity', cutIn.toFixed(3));
  window.__dbg = { R: R.P.x, M: M.P.x };
};
function boltState(i, t, T0, base, floorP, who, _) {
  const el = $('bolt' + i), sc = el.querySelector('.bsc');
  const rise = 16 * sm(seg(t, T0 + .7, T0 + 1.9)), lift = 34 * sm(seg(t, T0 + 1.9, T0 + 2.4));
  const fallT = t - (T0 + 2.4); let pos;
  if (t < T0 + .7) pos = [base[0], base[1]];
  else if (t < T0 + 2.4) pos = [base[0], base[1] - 10 - rise - lift * 0 + 0];
  else {
    const fr = who.fl && who.front ? who.front : null; // dropped from the wrench socket: parabola to the floor spot
    const sx = base[0], sy = base[1] - 10 - 16 - 34, g = 1900, tt = Math.max(0, fallT), vx = (floorP[0] - sx) / .32;
    const x = sx + Math.min(tt, .32) * vx, y = Math.min(floorP[1], sy + .5 * g * tt * tt);
    pos = [x, y];
  }
  // while it is still in the socket it follows the wrench (hand) vertically
  if (t >= T0 + 1.9 && t < T0 + 2.4) pos = [base[0], base[1] - 10 - 16 - lift];
  el.setAttribute('transform', `translate(${pos[0].toFixed(1)} ${pos[1].toFixed(1)}) rotate(${(t >= T0 + .7 && t < T0 + 1.9 ? 360 * 2 * seg(t, T0 + .7, T0 + 1.9) : 0)}) `);
  vis('bolt' + i, true);
}
function wrenchProp(id, W, S, t) {
  const e = $(id), fr = W.front;
  if (fr.prop !== 'wrench') { vis(id, false); return; }
  vis(id, true);
  const h = S.hands[1]; const bolt = (id === 'wrR') ? BOLT[0] : BOLT[1];
  const atBolt = h[1] < bolt[1] + 40 && Math.abs(h[0] - (bolt[0] - 6)) < 24;
  // socket centre sits at the hand; the handle rocks by the ratchet angle (pointing toward the character's facing side)
  const ang = (W.P.f >= 0 ? 1 : -1) < 0 ? 180 - (fr.ang || 0) : (fr.ang || 0);
  propAt(id, [h[0] + 6 * (W.P.f >= 0 ? 1 : -1), h[1] - 3], ang, .9);
  e.style.opacity = fr.pocketPhase ? 0 : 1;
}
function recorder(t, S, R) {
  // sits on the desk until Reed picks it up (51.0-52.3), then follows his front hand exactly
  const rest = [IN.rec[0], IN.rec[1]];
  const grab = sm(seg(t, 51.2, 51.5));
  const h = S.hands[1];
  let pos = rest, ang = 0;
  if (t >= 51.2) { pos = [lerp(rest[0], h[0] - 10, grab), lerp(rest[1], h[1] - 24, grab)]; ang = lerp(0, -4, grab); if (t >= 51.5) { pos = [h[0] - 10, h[1] - 24]; ang = -4; } }
  vis('gripH', t >= 51.2); $('gripH').setAttribute('cx', h[0].toFixed(1)); $('gripH').setAttribute('cy', h[1].toFixed(1));
  if (t < 51.2) { pos = rest; }
  vis('rec', t >= 41.0);
  propAt('rec', pos, ang, 1);
  const pressed = t > 52.5;
  const pr = sm(seg(t, 52.38, 52.48)) * (1 - sm(seg(t, 52.55, 52.66)));
  $('recbtn').setAttribute('transform', `translate(0 ${(1.6 * pr).toFixed(2)})`);
  // thumb dot sweeps to the button and presses
  const th = sm(seg(t, 52.0, 52.4)) * (1 - sm(seg(t, 52.7, 53.1)));
  vis('thumbg', t >= 51.5 && t < 53.2);
  const tp = [pos[0] + lerp(15, 0, th), pos[1] + lerp(30, 21, th) + 1.6 * pr];
  $('thumb').setAttribute('cx', tp[0].toFixed(1)); $('thumb').setAttribute('cy', tp[1].toFixed(1));
  // screen lights up at the press, waveform animates in sync with the girl's voice (real audio envelope) over static
  const on = t > 52.55, lit = on ? Math.min(1, (t - 52.55) / .1) : 0;
  $('scrfill').setAttribute('opacity', lit.toFixed(2)); $('scrdot').setAttribute('opacity', on && ((Math.floor(t * 2) % 2) === 0) ? 1 : 0);
  const g1 = Z.lines.find(l => l.id === 'g1');
  els.wb.forEach((b, i) => {
    let h2 = 0;
    if (on) {
      const tt = t - i * .035, k = Math.floor((tt - g1.t0) * 30), env = (k >= 0 && k < g1.env.length) ? g1.env[k] : 0;
      const stat = (t < g1.t0 - .05 ? .22 : .07) * (.4 + hash(Math.floor(t * 24) * 13 + i));
      h2 = clamp(1.2 + (env * 13 * (.6 + .6 * hash(i + 3.3 + Math.floor(t * 12)))) + stat * 9, 1, 15);
      if (t > g1.t0 + g1.env.length / 30 + .6) h2 = 1.2 + .8 * hash(Math.floor(t * 10) + i);
    }
    b.setAttribute('height', h2.toFixed(1)); b.setAttribute('y', (-6.5 - h2 / 2).toFixed(1));
  });
}
window.__events = function () {
  // footstep / action events derived from the SAME motion functions that drive the animation
  const ev = [];
  const steps = (xf, dist, who, t0, t1) => {
    let prev = null;
    for (let t = t0; t < t1; t += 1 / 240) {
      const wk = sm(speedOf(xf, t) / 28), phi = distAt(dist, t) / STRIDE, a = Math.floor(phi * 1), b = Math.floor(phi + .5);
      if (prev && wk > .45) { if (a !== prev[0]) ev.push({ t: +t.toFixed(3), k: 'step', who }); if (b !== prev[1]) ev.push({ t: +t.toFixed(3), k: 'step', who }); }
      prev = [a, b];
    }
  };
  steps(reedX, reedDist, 'R', 0, 60); steps(morganX, morganDist, 'M', 0, 60);
  return ev;
};
// QC hook: residual between the hand the animation asked for (a world target on an object) and where the IK actually placed it
window.__contacts = function () {
  if (!figR) build();
  const groups = { 'Reed -> bolt wrench': [23.9, 25.0, 'R'], 'Morgan -> bolt wrench': [25.8, 26.9, 'M'], 'Reed -> shelf (push)': [28.5, 30.8, 'R'], 'Morgan -> shelf (push)': [28.6, 30.8, 'M'],
    'Reed -> door handle / door': [33.2, 38.0, 'R'], 'Reed -> recorder': [51.4, 55.0, 'R'], 'Reed -> bolt tap': [11.3, 14.0, 'R'] };
  const out = {};
  for (const [k, [a, b, who]] of Object.entries(groups)) {
    let mx = 0, n = 0;
    for (let t = a; t < b; t += 1 / 30) {
      const S = who === 'R' ? reedPose(t) : morganPose(t), F = who === 'R' ? figR : figM, last = setFig(F, S.P);
      const tg = S.P.hands[1]; if (!tg) continue;
      mx = Math.max(mx, Math.hypot(last.hands[1][0] - tg[0], last.hands[1][1] - tg[1])); n++;
    }
    out[k] = { max: mx, n };
  }
  return out;
};
