(function () {
  // Deterministic keyframe player. renderAt(T) shows the shots active at T and sets every animated prop.
  const FW = window.__FW || 1280, FH = window.__FH || 720;
  const E = {
    io: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
    o: t => 1 - Math.pow(1 - t, 3),
    i: t => t * t * t,
    l: t => t,
    b: t => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); },
    h: t => 0,
  };
  const items = [];
  const scenes = [...document.querySelectorAll('[data-start]')].map(el => ({
    el, start: +el.dataset.start, end: +el.dataset.end, xin: +(el.dataset.xin || 0), xout: +(el.dataset.xout || 0)
  }));
  document.querySelectorAll('[data-kf]').forEach(el => {
    const keys = JSON.parse(el.dataset.kf).sort((a, b) => a[0] - b[0]);
    const props = {};
    keys.forEach(([t, p, e]) => { for (const k in p) (props[k] = props[k] || []).push([t, p[k], e || 'io']); });
    const sc = el.closest('[data-start]');
    const it = { el, props, o: (el.dataset.o || (FW / 2) + ' ' + (FH / 2)).split(' ').map(Number), start: sc ? +sc.dataset.start : 0,
                 wb: el.dataset.wb ? el.dataset.wb.split(' ') : null, svg: el instanceof SVGElement };
    if (props.draw) {
      it.paths = [...el.querySelectorAll('path,line,polyline,circle,ellipse,rect')].concat(el.matches('path,line,polyline') ? [el] : [])
        .filter(p => (p.getAttribute('stroke') || 'none') !== 'none');
      it.paths.forEach(p => { p.setAttribute('pathLength', '1'); p.style.strokeDasharray = '1 1'; });
    }
    if (props.chars) { it.tnodes = []; const walk = n => { n.childNodes.forEach(c => { if (c.nodeType === 3) it.tnodes.push([c, c.textContent]); else walk(c); }); }; walk(el); it.nch = it.tnodes.reduce((a, [, s]) => a + s.length, 0); }
    if (props.words) it.words = [...el.querySelectorAll('.w')];
    if (props.count) it.fmt = el.dataset.fmt || 'int';
    if (it.svg) el.style.transformBox = 'view-box';
    items.push(it);
  });
  function val(arr, t) {
    if (t <= arr[0][0]) return arr[0][1];
    for (let i = 0; i < arr.length - 1; i++) {
      const [t0, v0] = arr[i], [t1, v1, e] = arr[i + 1];
      if (t < t1) { const p = t1 > t0 ? E[e]((t - t0) / (t1 - t0)) : 1; return v0 + (v1 - v0) * p; }
    }
    return arr[arr.length - 1][1];
  }
  const money = v => '$' + Math.round(v).toLocaleString('en-US');
  window.renderAt = function (T) {
    scenes.forEach(s => {
      const on = T >= s.start && T < s.end;
      s.el.style.display = on ? 'block' : 'none';
      if (on) {
        let op = 1;
        if (s.xin) op = Math.min(op, (T - s.start) / s.xin);
        if (s.xout) op = Math.min(op, (s.end - T) / s.xout);
        s.el.style.opacity = Math.max(0, Math.min(1, op));
      }
    });
    items.forEach(it => {
      const t = T - it.start, P = it.props, g = (k, d) => P[k] ? val(P[k], t) : d;
      const el = it.el;
      if (P.o) el.style.opacity = Math.max(0, Math.min(1, g('o', 1)));
      if (P.s || P.sx || P.sy || P.tx || P.ty || P.r) {
        const s = g('s', 1);
        el.style.transformOrigin = it.o[0] + 'px ' + it.o[1] + 'px';
        el.style.transform = 'translate(' + g('tx', 0) + 'px,' + g('ty', 0) + 'px) rotate(' + g('r', 0) + 'deg) scale(' + (s * g('sx', 1)) + ',' + (s * g('sy', 1)) + ')';
      }
      if (P.blur) { const b = g('blur', 0); el.style.filter = b > 0.05 ? 'blur(' + b + 'px)' : 'none'; }
      if (P.wipe) {
        const w = Math.max(0, Math.min(1, g('wipe', 1)));
        if (it.wb) {
          const [x0, y0, x1, y1, d] = it.wb; const X0 = +x0, Y0 = +y0, X1 = +x1, Y1 = +y1;
          let ins;
          if (d === 'r') ins = '0px ' + (FW - (X0 + (X1 - X0) * w)) + 'px 0px 0px';
          else if (d === 'l') ins = '0px 0px 0px ' + (X1 - (X1 - X0) * w) + 'px';
          else if (d === 'd') ins = '0px 0px ' + (FH - (Y0 + (Y1 - Y0) * w)) + 'px 0px';
          else ins = (Y1 - (Y1 - Y0) * w) + 'px 0px 0px 0px';
          el.style.clipPath = w >= 1 ? 'none' : 'inset(' + ins + ')';
        } else el.style.clipPath = w >= 1 ? 'none' : 'inset(0 ' + ((1 - w) * 100) + '% 0 0)';
      }
      if (P.draw) {
        const d = Math.max(0, Math.min(1, g('draw', 1)));
        it.paths.forEach(p => { p.style.strokeDashoffset = String(1 - d); p.style.visibility = d <= 0.001 ? 'hidden' : 'visible'; });
      }
      if (P.chars) {  // typewriter: reveal characters in document order
        let n = Math.round(Math.max(0, Math.min(1, g('chars', 1))) * it.nch);
        it.tnodes.forEach(([node, full]) => { const k = Math.max(0, Math.min(full.length, n)); node.textContent = full.slice(0, k); n -= full.length; });
      }
      if (P.words) {
        const w = g('words', 1) * it.words.length;
        it.words.forEach((s, i) => { s.style.opacity = Math.max(0, Math.min(1, (w - i) * 2.5)); });
      }
      if (P.count) {
        const v = g('count', 0);
        el.textContent = it.fmt === 'int' ? Math.round(v).toLocaleString('en-US') : it.fmt === 'money' ? money(v) : v.toFixed(1);
      }
    });
  };
  window.__ready = true;
})();
