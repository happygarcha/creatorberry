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
