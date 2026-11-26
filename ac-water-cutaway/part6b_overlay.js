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
  if (T < K.hatch[1]) overlay(T, ov); else drawCard(ov, T);
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
