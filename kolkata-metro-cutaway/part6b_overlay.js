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
