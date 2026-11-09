/* Drapewell redesign: mobile menu drawer, desktop dropdown toggles, header shadow. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* mobile menu */
  var menu = $("#dw-menu");
  if (menu && typeof menu.showModal === "function") {
    $$("[data-menu-open]").forEach(function (b) { b.addEventListener("click", function () { menu.showModal(); }); });
    $$("[data-menu-close]", menu).forEach(function (b) { b.addEventListener("click", function () { menu.close(); }); });
    menu.addEventListener("click", function (e) { if (e.target === menu) menu.close(); });
    $$("a", menu).forEach(function (a) { a.addEventListener("click", function () { menu.close(); }); });
  }

  /* desktop dropdowns: hover/focus work in CSS; the chevron button toggles for touch and keyboard */
  var items = $$(".dw-nav-item.has-sub");
  function closeAll(except) {
    items.forEach(function (it) {
      if (it !== except) { it.classList.remove("is-open"); var b = $(".dw-sub-btn", it); if (b) b.setAttribute("aria-expanded", "false"); }
    });
  }
  items.forEach(function (it) {
    var btn = $(".dw-sub-btn", it);
    if (!btn) return;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = !it.classList.contains("is-open");
      closeAll(it);
      it.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function () { closeAll(null); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeAll(null); });

  /* header shadow once scrolled */
  var hdr = $(".dw-header");
  if (hdr) {
    var onScroll = function () { hdr.classList.toggle("is-stuck", window.scrollY > 8); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* floating capsule: turns and drifts as the page scrolls (skipped for reduced motion) */
  var cap = $(".dw-capsule");
  if (cap && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var ticking = false;
    var move = function () {
      var y = window.scrollY;
      cap.style.transform = "translate3d(0," + (Math.sin(y / 180) * 14) + "px,0) rotate(" + (-28 + y * 0.18) + "deg)";
      ticking = false;
    };
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(move); } }, { passive: true });
    move();
  }

  /* header height -> CSS var (the pinned hero sits right under the sticky header) */
  var setHdr = function () { if (hdr) document.documentElement.style.setProperty("--hdr", hdr.offsetHeight + "px"); };
  setHdr();
  window.addEventListener("resize", setHdr);

  /* ---------- hero ring: cards sit on an ellipse, scroll spins it, the end folds it into a stack ---------- */
  var ring = $("[data-ring]");
  if (ring) {
    var stage = $(".dw-ring-stage", ring), box = $("[data-ring-cards]", ring), now = $("[data-ring-now]", ring);
    var cards = $$(".dw-ring-card", ring), n = cards.length;
    var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
    var intro = reduce ? 1 : 0, prog = 0, shown = -1, W = 0, H = 0, cw = 0, raf = 0;
    var clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };
    var ease = function (t) { return 1 - Math.pow(1 - t, 3); };
    var smooth = function (a, b, v) { var t = clamp((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
    var measure = function () {
      var r = box.getBoundingClientRect(); W = r.width; H = r.height;
      cw = cards.length ? cards[0].offsetWidth : 150;
    };
    var layout = function () {
      raf = 0;
      var k = smooth(0.74, 0.98, prog);              /* fold into a stack at the end */
      var wide = W > 700;
      var rx = (wide ? W * 0.36 : W * 0.4) * (1 - 0.88 * k) * ease(intro);
      var ry = (wide ? H * 0.34 : H * 0.34) * (1 - 0.88 * k) * ease(intro);
      var cx = W / 2, cy = H * (wide ? 0.5 : 0.48);
      var spin = prog * Math.PI * 1.35;
      var arc = Math.PI * 2 * 0.86, best = -1, bestD = -1;
      for (var i = 0; i < n; i++) {
        var th = (i / n) * arc + spin + Math.PI * 0.55;
        var s = Math.sin(th), c = Math.cos(th);
        var d = (s + 1) / 2;                          /* 0 = back/top, 1 = front/bottom */
        var sc = (0.55 + 0.8 * d) * (1 + 0.15 * k) * (0.6 + 0.4 * ease(intro));
        var rot = c * -20 * (1 - k) + (i - n / 2) * 1.2 * k;
        var x = cx + rx * c, y = cy + ry * s;
        var el = cards[i];
        el.style.transform = "translate3d(" + (x - cw / 2).toFixed(1) + "px," + (y - cw / 2).toFixed(1) + "px,0) rotate(" + rot.toFixed(1) + "deg) scale(" + sc.toFixed(3) + ")";
        el.style.zIndex = String(Math.round(d * 100) + i);
        if (d > bestD) { bestD = d; best = i; }
      }
      if (best !== shown && now) {
        shown = best;
        var f = cards[best];
        now.textContent = (best + 1 < 10 ? "0" : "") + (best + 1) + " / " + n + " \u00b7 " + (f.dataset.title || "").slice(0, 38) + " \u00b7 " + (f.dataset.price || "");
      }
      if (now) now.style.opacity = k > 0.6 ? 0 : 1;
      var copy = $(".dw-ring-copy", ring);
      if (copy && W > 700) copy.style.opacity = String(1 - smooth(0.8, 1, prog) * 0.0);
    };
    var request = function () { if (!raf) raf = requestAnimationFrame(layout); };
    var onScroll = function () {
      if (reduce) return;
      var r = ring.getBoundingClientRect();
      var span = r.height - stage.offsetHeight;
      prog = span > 0 ? clamp(-r.top / span, 0, 1) : 0;
      request();
    };
    measure(); layout();
    cards.forEach(function (c) { c.classList.add("is-ready"); });
    window.addEventListener("resize", function () { measure(); onScroll(); request(); });
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    if (!reduce) {
      var t0 = performance.now();
      var step = function (t) { intro = clamp((t - t0) / 1500, 0, 1); layout(); if (intro < 1) requestAnimationFrame(step); };
      requestAnimationFrame(step);
    }
  }

  /* ---------- product grid (adapted from Codrops cbpShop, MIT): flip tile, favourites, option pop-overs ---------- */
  var FAV_KEY = "dw-fav";
  var readFavs = function () { try { return JSON.parse(localStorage.getItem(FAV_KEY) || "[]"); } catch (e) { return []; } };
  var writeFavs = function (a) { try { localStorage.setItem(FAV_KEY, JSON.stringify(a)); } catch (e) {} };
  var syncFavs = function () {
    var favs = readFavs();
    $$("[data-fav]").forEach(function (b) { b.setAttribute("aria-pressed", favs.indexOf(b.dataset.fav) > -1 ? "true" : "false"); });
  };
  var closePops = function (except) {
    $$(".pg-optcell.is-open").forEach(function (li) {
      if (li !== except) { li.classList.remove("is-open"); var b = $("[data-pg-opt]", li); if (b) b.setAttribute("aria-expanded", "false"); }
    });
  };
  document.addEventListener("click", function (e) {
    var rot = e.target.closest("[data-pg-rotate]");
    if (rot) {
      var item = $(".pg-item", rot.closest(".pg-stage"));
      var on = item.classList.toggle("is-flipped");
      rot.setAttribute("aria-pressed", on ? "true" : "false");
      return;
    }
    var fav = e.target.closest("[data-fav]");
    if (fav) {
      var list = readFavs(), h = fav.dataset.fav, at = list.indexOf(h);
      if (at > -1) list.splice(at, 1); else list.push(h);
      writeFavs(list); syncFavs();
      return;
    }
    var opt = e.target.closest("[data-pg-opt]");
    if (opt) {
      var li = opt.closest(".pg-optcell"), open = !li.classList.contains("is-open");
      closePops(li);
      li.classList.toggle("is-open", open);
      opt.setAttribute("aria-expanded", open ? "true" : "false");
      return;
    }
    if (!e.target.closest(".pg-tip")) closePops(null);
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closePops(null); });
  syncFavs();
  var mainEl = $("#main");
  if (mainEl && "MutationObserver" in window) new MutationObserver(function () { syncFavs(); }).observe(mainEl, { childList: true, subtree: true });
})();
