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
    /* a category that has sub-categories only opens its list; it does not leave the page */
    $$(".dw-menu-parent", menu).forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        var d = a.closest("details");
        if (d) d.open = !d.open;
      });
    });
    $$("a", menu).forEach(function (a) {
      if (a.classList.contains("dw-menu-parent")) return;
      a.addEventListener("click", function () { menu.close(); });
    });
  }

  /* desktop dropdowns: hover/focus work in CSS; the chevron button toggles for touch and keyboard */
  var items = $$(".dw-nav-item.has-sub");
  function closeAll(except) {
    items.forEach(function (it) {
      if (it !== except) { it.classList.remove("is-open"); var b = $(".dw-sub-btn", it); if (b) b.setAttribute("aria-expanded", "false"); }
    });
  }
  items.forEach(function (it) {
    var btn = $(".dw-sub-btn", it), link = $(":scope > a", it);
    if (!btn) return;
    var toggle = function (e) {
      e.preventDefault();
      e.stopPropagation();
      var open = !it.classList.contains("is-open");
      closeAll(it);
      it.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    };
    btn.addEventListener("click", toggle);
    /* the category name opens its sub-categories instead of leaving the page */
    if (link) { link.setAttribute("aria-haspopup", "true"); link.addEventListener("click", toggle); }
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

  /* header height -> CSS var (the pinned hero sits right under the sticky header) */
  var setHdr = function () { if (hdr) document.documentElement.style.setProperty("--hdr", hdr.offsetHeight + "px"); };
  setHdr();
  window.addEventListener("resize", setHdr);

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
      if (li !== except) { li.classList.remove("is-open"); var b = $("[data-pg-opt]", li); if (b) b.setAttribute("aria-expanded", "false"); var ce = li.closest(".pg-cell"); if (ce) ce.classList.remove("pg-pop"); }
    });
  };
  /* phones: option choices open in a bottom sheet instead of a small pop-over */
  var sheet = null;
  var openSheet = function (btn, li) {
    if (!sheet) {
      sheet = document.createElement("dialog");
      sheet.className = "pg-sheet";
      sheet.setAttribute("aria-label", "Options");
      sheet.innerHTML = '<div class="pg-sheet-head"><div><h3 class="pg-sheet-t"></h3><p class="pg-sheet-s"></p></div><button type="button" class="pg-sheet-x" data-sheet-close>Close</button></div><div class="pg-sheet-list"></div>';
      document.body.appendChild(sheet);
      sheet.addEventListener("click", function (ev) {
        if (ev.target === sheet || ev.target.closest("[data-sheet-close]") || ev.target.closest("[data-quick]")) sheet.close();
      });
    }
    var cell = li.closest(".pg-cell"), title = cell && $(".pg-info .t", cell);
    $(".pg-sheet-t", sheet).textContent = btn.dataset.optName || "Options";
    $(".pg-sheet-s", sheet).textContent = title ? title.textContent.trim() : "";
    $(".pg-sheet-list", sheet).innerHTML = $(".pg-tip", li).innerHTML;
    sheet.showModal();
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
      var li = opt.closest(".pg-optcell");
      if (matchMedia("(max-width: 759px)").matches) { openSheet(opt, li); return; }
      var open = !li.classList.contains("is-open");
      closePops(li);
      li.classList.toggle("is-open", open);
      var cellEl = li.closest(".pg-cell");
      if (cellEl) cellEl.classList.toggle("pg-pop", open);
      opt.setAttribute("aria-expanded", open ? "true" : "false");
      return;
    }
    if (!e.target.closest(".pg-tip")) closePops(null);
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closePops(null); });
  syncFavs();
  var mainEl = $("#main");
  if (mainEl && "MutationObserver" in window) new MutationObserver(function () { syncFavs(); }).observe(mainEl, { childList: true, subtree: true });

  /* ---------- "Fresh this week" reel: slow auto-spin, drag to turn, slows on hover, pauses off-screen ---------- */
  var reel = $("[data-reel]");
  if (reel) {
    var ringEl = $("[data-reel-ring]", reel), stageEl = $(".dw-reel-stage", reel), rItems = $$(".dw-reel-item", reel), rods = $$(".dw-rod", reel);
    var still = matchMedia("(prefers-reduced-motion: reduce)").matches;
    var ang = -20, vel = still ? 0 : 0.1, base = still ? 0 : 0.1, dragging = false, lastX = 0, travelled = 0, onScreen = true, rafId = 0;

    /* The rail is a fixed oval. The badges slide along it at an even pace (spacing by arc length, not by angle),
       each one turned to face outward. A wide stage gets a wide oval with every badge; a phone gets a rounder, smaller
       oval with the first 8 so the badges stay big enough to read. */
    var A = 300, B = 150, perim = 1, table = [], TAB = 300, live = rItems.slice();
    /* the rail's outline is a rounded racetrack (a superellipse): flat-ish long sides, softly rounded ends */
    var N = 3.4, sgn = function (v) { return v < 0 ? -1 : 1; };
    var seX = function (th) { var s = Math.sin(th); return A * sgn(s) * Math.pow(Math.abs(s), 2 / N); };
    var seZ = function (th) { var c = Math.cos(th); return B * sgn(c) * Math.pow(Math.abs(c), 2 / N); };
    var buildTable = function () {
      table = [0]; var px = seX(0), pz = seZ(0), len = 0;
      for (var k = 1; k <= TAB; k++) { var th = k / TAB * Math.PI * 2, x = seX(th), z = seZ(th); len += Math.hypot(x - px, z - pz); table.push(len); px = x; pz = z; }
      perim = len;
    };
    var railSvg = function () {
      var pad = 17, w = A * 2 + pad * 2, h = B * 2 + pad * 2, pts = [];
      for (var k = 0; k <= 120; k++) { var th = k / 120 * Math.PI * 2; pts.push((A + pad + seX(th)).toFixed(1) + "," + (B + pad - seZ(th)).toFixed(1)); }
      return '<svg viewBox="0 0 ' + w.toFixed(0) + ' ' + h.toFixed(0) + '" width="100%" height="100%" preserveAspectRatio="none" aria-hidden="true">' +
        '<defs><linearGradient id="dwchrome" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9aa0a9"/><stop offset=".2" stop-color="#ffffff"/><stop offset=".42" stop-color="#7a808a"/><stop offset=".62" stop-color="#f3f4f6"/><stop offset=".82" stop-color="#9aa0a9"/><stop offset="1" stop-color="#e6e8ec"/></linearGradient></defs>' +
        '<polygon points="' + pts.join(" ") + '" fill="none" stroke="url(#dwchrome)" stroke-width="10" stroke-linejoin="round"/></svg>';
    };
    var thetaAt = function (s) {
      s = ((s % perim) + perim) % perim;
      var lo = 0, hi = TAB;
      while (hi - lo > 1) { var mid = (lo + hi) >> 1; if (table[mid] <= s) lo = mid; else hi = mid; }
      var f = (s - table[lo]) / ((table[hi] - table[lo]) || 1);
      return (lo + f) / TAB * Math.PI * 2;
    };
    var paint = function () {
      var n = live.length; if (!n) return;
      var s0 = ang / 360 * perim;
      for (var i = 0; i < n; i++) {
        var th = thetaAt(s0 + i * perim / n), x = seX(th), z = seZ(th);
        /* outward normal of the racetrack: the gradient of |x/A|^N + |z/B|^N */
        var nx = sgn(x) * Math.pow(Math.abs(x / A), N - 1) / A, nz = sgn(z) * Math.pow(Math.abs(z / B), N - 1) / B;
        var psi = Math.atan2(nx, nz) * 180 / Math.PI;
        /* badges on the far side would show their backs to the shopper, so they are mirrored round to face the front too;
           the mapping meets the near side at the ends of the rail (edge-on), so nothing flips suddenly */
        if (psi > 90) psi = 180 - psi; else if (psi < -90) psi = -180 - psi;
        live[i].style.transform = "translate3d(" + x.toFixed(1) + "px,0," + z.toFixed(1) + "px) rotateY(" + psi.toFixed(2) + "deg) translateX(-50%)";
      }
    };
    var layout = function () {
      var w = stageEl.clientWidth || 600, cw = rItems[0] ? rItems[0].offsetWidth : 150;
      var phone = w < 600, mid = w < 900;
      var limit = phone ? 8 : mid ? 10 : rItems.length;
      live = rItems.filter(function (el, i) { return i < limit; });
      rItems.forEach(function (el, i) { el.hidden = i >= limit; });
      if (phone) { A = cw * 1.3; B = cw * 1.05; }
      else if (mid) { A = w * 0.36; B = cw * 1.1; }
      else { A = Math.min(w * 0.41, 660); B = cw * 1.3; }
      reel.style.setProperty("--A", A.toFixed(0) + "px");
      reel.style.setProperty("--B", B.toFixed(0) + "px");
      var svg = railSvg();
      $$(".dw-reel-rail", reel).forEach(function (r) { r.innerHTML = svg; });
      rods.forEach(function (r, i) {
        var th = (Number(r.dataset.at) || (i * 60)) * Math.PI / 180;
        r.style.transform = "translate3d(" + seX(th).toFixed(1) + "px,-230px," + seZ(th).toFixed(1) + "px) translateX(-50%)";
      });
      buildTable(); paint();
    };
    layout();
    var resizeT = 0;
    window.addEventListener("resize", function () { clearTimeout(resizeT); resizeT = setTimeout(layout, 120); });
    var loop = function () {
      rafId = 0;
      if (!dragging && !pulling) { vel += (base - vel) * 0.04; ang += vel; paint(); }
      if (!still && onScreen && !document.hidden) rafId = requestAnimationFrame(loop);
    };
    var wake = function () { if (!rafId && !still && onScreen && !document.hidden) rafId = requestAnimationFrame(loop); };
    var pullCard = null, pullMode = "", pullY0 = 0, pullRaw = 0, pull = 0, holdT = 0, pulling = false, springRaf = 0, startX = 0, startY = 0, lastY = 0;
    var maxPull = function () { var w = rItems[0] ? rItems[0].offsetWidth : 150; return w * 0.95; };
    var applyPull = function (px) { pull = px; if (pullCard) pullCard.style.setProperty("--pull", px.toFixed(1) + "px"); };
    var springBack = function () {
      var card = pullCard, v = 0, from = pull;
      cancelAnimationFrame(springRaf);
      var step = function () {
        v += -pull * 0.16; v *= 0.8; pull += v;
        if (card) card.style.setProperty("--pull", pull.toFixed(1) + "px");
        if (Math.abs(pull) < 0.4 && Math.abs(v) < 0.4) { pull = 0; if (card) { card.style.setProperty("--pull", "0px"); card.classList.remove("is-pulled"); } return; }
        springRaf = requestAnimationFrame(step);
      };
      if (Math.abs(from) < 0.4) { if (card) card.classList.remove("is-pulled"); return; }
      springRaf = requestAnimationFrame(step);
    };
    var armPull = function () {
      pullMode = "pull"; pulling = true; dragging = false; vel = 0;
      pullY0 = lastY; pullRaw = 0;
      cancelAnimationFrame(springRaf);
      if (pullCard) pullCard.classList.add("is-pulled");
      if (navigator.vibrate) { try { navigator.vibrate(8); } catch (err) {} }
    };
    stageEl.addEventListener("pointerdown", function (e) {
      dragging = true; lastX = e.clientX; travelled = 0; vel = 0;
      startX = e.clientX; startY = lastY = e.clientY; pullMode = ""; pullCard = null;
      var hit = e.target.closest ? e.target.closest(".dw-reel-item") : null;
      if (hit && e.target.closest(".dw-id")) {
        pullCard = hit;
        if (e.pointerType !== "mouse") holdT = setTimeout(function () { if (!pullMode) armPull(); }, 240);
      }
    });
    stageEl.addEventListener("touchmove", function (e) { if (pullMode === "pull") e.preventDefault(); }, { passive: false });
    window.addEventListener("pointermove", function (e) {
      lastY = e.clientY;
      if (pullCard && !pullMode && e.pointerType === "mouse" && dragging) {
        var mx = e.clientX - startX, my = e.clientY - startY;
        if (Math.abs(mx) > 6 || Math.abs(my) > 6) { if (my > 0 && my > Math.abs(mx) * 1.1) armPull(); else pullMode = "rotate"; }
      }
      if (pullMode === "pull") {
        pullRaw = Math.max(0, e.clientY - pullY0);
        var mp = maxPull();
        applyPull(mp * Math.tanh(pullRaw / mp));
        travelled = 99;
        return;
      }
      if (!dragging) return;
      var dx = e.clientX - lastX; lastX = e.clientX; travelled += Math.abs(dx);
      ang += dx * 0.45; vel = dx * 0.45; paint();
    });
    var release = function () {
      clearTimeout(holdT);
      if (pullMode === "pull") { pulling = false; pullMode = ""; springBack(); dragging = false; wake(); return; }
      pullMode = "";
      if (dragging) { dragging = false; wake(); }
    };
    window.addEventListener("pointerup", release);
    window.addEventListener("pointercancel", release);
    reel.addEventListener("click", function (e) { if (travelled > 6) { e.preventDefault(); e.stopPropagation(); travelled = 0; } }, true);
    stageEl.addEventListener("pointerenter", function (e) { if (e.pointerType === "mouse") base = still ? 0 : 0.02; });
    stageEl.addEventListener("pointerleave", function () { base = still ? 0 : 0.1; });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { onScreen = en[0].isIntersecting; if (onScreen) wake(); }).observe(reel);
    document.addEventListener("visibilitychange", wake);
    paint(); wake();
  }

  /* ---------- homepage "New arrivals" sort: same swirl as the category pages (theme.js re-orders, this animates it) ---------- */
  var homeSel = $("[data-home-sort]"), homeFeed = $("#feed");
  if (homeSel && homeFeed && !$("[data-coll-sort]") && homeFeed.animate && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    homeSel.addEventListener("change", function () {
      var hc = $$(".cell", homeFeed), was = new Map();
      hc.forEach(function (c) { was.set(c, c.getBoundingClientRect()); });
      setTimeout(function () {
        var k = 0;
        $$(".cell", homeFeed).forEach(function (c) {
          var o = was.get(c); if (!o) return;
          var r = c.getBoundingClientRect(), dx = o.left - r.left, dy = o.top - r.top, delay = Math.min(k++, 16) * 28;
          if (Math.abs(dx) < 1 && Math.abs(dy) < 1) return;
          c.animate([
            { transform: "translate(" + dx + "px," + dy + "px) rotate(0deg) scale(1)" },
            { offset: 0.5, transform: "translate(" + dx * 0.38 + "px," + (dy * 0.38 - 18) + "px) rotate(" + ((Math.random() - 0.5) * 14) + "deg) scale(1.05)" },
            { transform: "none" }
          ], { duration: 780, delay: delay, easing: "cubic-bezier(.3,.8,.3,1)", fill: "backwards" });
        });
      }, 0);
    }, true);   /* capture: measure the cards before theme.js re-orders them */
  }

  /* ---------- category page: instant search within the products on the page ---------- */
  var cs = $("[data-coll-search]"), sortSel = $("[data-coll-sort]"), feedEl = $(".feed");
  if ((cs || sortSel) && feedEl) {
    var cells = $$(".cell", feedEl), none = $("[data-coll-none]"), term = $("[data-coll-term]"), site = $("[data-coll-site]");
    var paged = !!$(".pager");
    var calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
    var norm = function (t) { return String(t || "").toLowerCase().replace(/\s+/g, " ").trim(); };

    /* The shuffle, in three beats:
       1. cards that are going away tumble up and out,
       2. cards that stay swirl across to their new spots, tilting as they travel (FLIP),
       3. cards that arrive fly in from below with a bounce. */
    var rnd = function (n) { return (Math.random() - 0.5) * 2 * n; };
    var token = 0;
    var reflow = function (change, leaving) {
      var mine = ++token;
      cells.forEach(function (c) { if (c.getAnimations) c.getAnimations().forEach(function (a) { a.cancel(); }); });
      var play = !calm && !!feedEl.animate;
      var run = function () {
        if (mine !== token) return;
        var before = new Map();
        cells.forEach(function (c) { if (!c.hidden) before.set(c, c.getBoundingClientRect()); });
        change();
        cells.forEach(function (c) { if (c.getAnimations) c.getAnimations().forEach(function (a) { a.cancel(); }); });
        if (!play) return;
        var k = 0;
        cells.forEach(function (c) {
          if (c.hidden) return;
          var r = c.getBoundingClientRect(), o = before.get(c), delay = Math.min(k++, 16) * 28;
          if (o) {
            var dx = o.left - r.left, dy = o.top - r.top;
            if (Math.abs(dx) < 1 && Math.abs(dy) < 1) return;
            var tilt = rnd(7);
            c.animate([
              { transform: "translate(" + dx + "px," + dy + "px) rotate(0deg) scale(1)" },
              { offset: 0.5, transform: "translate(" + dx * 0.38 + "px," + (dy * 0.38 - 18) + "px) rotate(" + tilt + "deg) scale(1.05)" },
              { transform: "none" }
            ], { duration: 780, delay: delay, easing: "cubic-bezier(.3,.8,.3,1)", fill: "backwards" });
          } else {
            c.animate([
              { opacity: 0, transform: "translate(" + rnd(150) + "px," + (90 + Math.random() * 120) + "px) rotate(" + rnd(14) + "deg) scale(.6)" },
              { opacity: 1, transform: "none" }
            ], { duration: 700, delay: delay, easing: "cubic-bezier(.2,1.25,.3,1)", fill: "backwards" });
          }
        });
      };
      if (play && leaving && leaving.length) {
        leaving.forEach(function (c, i) {
          c.animate([
            { opacity: 1, transform: "none" },
            { opacity: 0, transform: "translate(" + rnd(90) + "px," + (-50 - Math.random() * 90) + "px) rotate(" + rnd(34) + "deg) scale(.5)" }
          ], { duration: 340, delay: Math.min(i, 8) * 16, easing: "cubic-bezier(.5,0,.9,.45)", fill: "forwards" });
        });
        setTimeout(run, 360);
      } else {
        run();
      }
    };

    /* search: hide the cards that don't match, the rest slide together */
    /* sub-category chips (for example Bathroom: Shower Curtains / Bath Mats) */
    var subMap = {}, subNow = "", subBox = $("[data-sub-chips]"), subData = $("[data-coll-subs]");
    if (subData) { try { subMap = JSON.parse(subData.textContent); } catch (e) { subMap = {}; } }
    var applyFilter = function () {
      var q = cs ? norm(cs.value) : "", parts = q ? q.split(" ") : [], shown = 0;
      var allowed = subNow && subMap[subNow] ? subMap[subNow] : null;
      var keep = cells.map(function (c) {
        var hay = norm(c.dataset.title), ok = parts.every(function (w) { return hay.indexOf(w) > -1; });
        if (ok && allowed) ok = allowed.indexOf(c.dataset.handle) > -1;
        if (ok) shown++;
        return ok;
      });
      var leaving = cells.filter(function (c, i) { return !c.hidden && !keep[i]; });
      reflow(function () { cells.forEach(function (c, i) { c.hidden = !keep[i]; }); }, leaving);
      if (none) {
        none.hidden = !((q || allowed) && shown === 0);
        if (term && cs) term.textContent = "“" + cs.value.trim() + "”";
        if (site && cs) site.href = (cs.form ? cs.form.action : "/search") + "?type=product&q=" + encodeURIComponent(cs.value.trim());
      }
    };
    if (subBox) {
      /* products that are in none of the sub-categories get their own chip, worked out here so new products are included */
      var inAny = {};
      Object.keys(subMap).forEach(function (k) { subMap[k].forEach(function (h) { inAny[h] = true; }); });
      var restCells = cells.filter(function (c) { return !inAny[c.dataset.handle]; });
      var moreBtn = null, moreRow = null;
      if (restCells.length && Object.keys(subMap).length) {
        moreBtn = document.createElement("button");
        moreBtn.type = "button"; moreBtn.className = "dw-subchip dw-subchip-more"; moreBtn.setAttribute("aria-pressed", "false");
        moreBtn.textContent = subBox.dataset.moreLabel || "More";
        subBox.appendChild(moreBtn);

        /* "More" opens a second row of chips. The groups come from the keyword lines in the theme settings
           ("Towels: towel, bath sheet"), matched against each leftover product's name, type and tags. */
        var slug = function (t) { return "g-" + String(t).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""); };
        var groups = [], used = {};
        String(subBox.dataset.moreGroups || "").split(/\r?\n/).forEach(function (line) {
          var at = line.indexOf(":"); if (at < 1) return;
          var label = line.slice(0, at).trim(), words = line.slice(at + 1).split(",").map(function (w) { return norm(w); }).filter(Boolean);
          if (!label || !words.length) return;
          /* each product goes under the first chip that matches it, so no product shows up under two chips */
          var hits = restCells.filter(function (c) { if (used[c.dataset.handle]) return false; var f = c.dataset.find || norm(c.dataset.title); return words.some(function (w) { return f.indexOf(w) > -1; }); });
          if (hits.length) { hits.forEach(function (c) { used[c.dataset.handle] = true; }); groups.push({ label: label, key: slug(label), handles: hits.map(function (c) { return c.dataset.handle; }) }); }
        });
        var leftover = restCells.filter(function (c) { return !used[c.dataset.handle]; });
        if (groups.length && leftover.length) groups.push({ label: "Other", key: "g-other", handles: leftover.map(function (c) { return c.dataset.handle; }) });

        if (groups.length) {
          moreRow = document.createElement("div");
          moreRow.className = "dw-more-row"; moreRow.hidden = true;
          groups.forEach(function (g, i) {
            subMap[g.key] = g.handles;
            var gb = document.createElement("button");
            gb.type = "button"; gb.className = "dw-subchip dw-subchip-sm"; gb.dataset.sub = g.key; gb.setAttribute("aria-pressed", "false");
            gb.style.setProperty("--i", i); gb.textContent = g.label;
            moreRow.appendChild(gb);
          });
          subBox.appendChild(moreRow);
          moreBtn.setAttribute("aria-expanded", "false");
          moreBtn.dataset.opener = "1";
        } else {
          subMap.__more = restCells.map(function (c) { return c.dataset.handle; });   /* no groups to offer: More just filters */
          moreBtn.dataset.sub = "__more";
        }
      }
      var openMore = function (open) {
        if (!moreRow) return;
        moreRow.hidden = !open;
        moreBtn.setAttribute("aria-expanded", open ? "true" : "false");
        moreBtn.classList.toggle("is-open", open);
      };
      /* wide screens have room: no "More" button, every group chip sits in the same row. Phones keep the More button. */
      if (moreRow) {
        var wideMq = matchMedia("(min-width: 760px)");
        var applyWide = function () {
          subBox.classList.toggle("is-wide", wideMq.matches);
          if (wideMq.matches) moreRow.hidden = false;
          else { moreRow.hidden = !(subNow && /^g-/.test(subNow)); moreBtn.classList.toggle("is-open", !moreRow.hidden); moreBtn.setAttribute("aria-expanded", moreRow.hidden ? "false" : "true"); }
        };
        applyWide();
        if (wideMq.addEventListener) wideMq.addEventListener("change", applyWide);
      }
      var setSub = function (value, fromUser) {
        subNow = value;
        $$(".dw-subchip", subBox).forEach(function (b) {
          if (b.dataset.opener) return;
          var on = b.dataset.sub === value; b.classList.toggle("is-on", on); b.setAttribute("aria-pressed", on ? "true" : "false");
        });
        if (moreBtn && moreBtn.dataset.opener) moreBtn.classList.toggle("has-on", /^g-/.test(value));
        if (/^g-/.test(value)) openMore(true);
        applyFilter();
        if (fromUser) { try { history.replaceState(null, "", location.pathname + location.search + (value ? "#" + value : "")); } catch (e) {} }
      };
      subBox.addEventListener("click", function (e) {
        var b = e.target.closest(".dw-subchip"); if (!b) return;
        if (b.dataset.opener) { openMore(moreRow.hidden); return; }   /* More only opens or closes the second row */
        setSub(b.dataset.sub, true);
      });
      var fromHash = decodeURIComponent((location.hash || "").slice(1));
      if (fromHash && subMap[fromHash]) setSub(fromHash, false);
    }
    if (cs) {
      cs.addEventListener("input", applyFilter);
      cs.form.addEventListener("submit", function (e) { if (cells.length && cs.value.trim()) e.preventDefault(); });
    }

    /* sort: re-order the cards on the page. Price, name and date are worked out here; the store's own orders
       (Featured, Best selling) are read from the server in the background and applied the same way. */
    if (sortSel) {
      var serverOrders = {}, current = sortSel.value;
      var local = {
        "price-ascending": function (a, b) { return a.dataset.price - b.dataset.price; },
        "price-descending": function (a, b) { return b.dataset.price - a.dataset.price; },
        "title-ascending": function (a, b) { return a.dataset.title.localeCompare(b.dataset.title); },
        "title-descending": function (a, b) { return b.dataset.title.localeCompare(a.dataset.title); },
        "created-ascending": function (a, b) { return a.dataset.new - b.dataset.new; },
        "created-descending": function (a, b) { return b.dataset.new - a.dataset.new; }
      };
      var place = function (list) { reflow(function () { list.forEach(function (c) { feedEl.appendChild(c); }); }); };
      var serverOrder = function (value) {
        if (serverOrders[value]) return Promise.resolve(serverOrders[value]);
        var u = new URL(location.href); u.searchParams.set("sort_by", value);
        return fetch(u.toString(), { credentials: "same-origin" }).then(function (r) { return r.text(); }).then(function (html) {
          var doc = new DOMParser().parseFromString(html, "text/html");
          var handles = $$(".feed .cell[data-handle]", doc).map(function (c) { return c.dataset.handle; });
          if (!handles.length) throw new Error("empty");
          return (serverOrders[value] = handles);
        });
      };
      var remember = function (value) {
        try { var u = new URL(location.href); u.searchParams.set("sort_by", value); history.replaceState(null, "", u.toString()); } catch (e) {}
      };
      /* fetch the store's own orders (Featured, Best selling) quietly after load, so those sorts shuffle at once */
      if (!paged) {
        var warm = function () {
          $$("option", sortSel).forEach(function (o) { if (!local[o.value]) serverOrder(o.value).catch(function () {}); });
        };
        if ("requestIdleCallback" in window) requestIdleCallback(warm, { timeout: 2500 }); else setTimeout(warm, 1200);
      }
      sortSel.addEventListener("change", function () {
        var value = sortSel.value, myPick = value;
        if (paged) { sortSel.form.submit(); return; }          /* several pages: the server has to do it */
        remember(value); current = value;
        if (local[value]) { place(cells.slice().sort(local[value])); return; }
        serverOrder(value).then(function (handles) {
          if (current !== myPick) return;
          var byHandle = {}; cells.forEach(function (c) { byHandle[c.dataset.handle] = c; });
          var list = handles.map(function (h) { return byHandle[h]; }).filter(Boolean);
          cells.forEach(function (c) { if (list.indexOf(c) < 0) list.push(c); });
          place(list);
        }).catch(function () { sortSel.form.submit(); });      /* anything unexpected: fall back to a normal reload */
      });
    }
  }

  /* ---------- dock magnification (like the macOS Dock): chips swell near the pointer, neighbours less, and spring back ---------- */
  if (matchMedia("(hover: hover) and (pointer: fine)").matches && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var DOCK_BOXES = ".dw-chips:not(.is-scroll), .dw-subchips", DOCK_ITEMS = ".dw-chip, .dw-subchip", RADIUS = 300, PEAK = 0.5, REACH = 70;
    var dockBox = null, dockItems = [], dockBase = [], dockRows = [], dockRaf = 0, dockX = 0, dockY = 0, sx = 0, sy = 0, dockIdle = 0;
    var dockReset = function () {
      cancelAnimationFrame(dockRaf); dockRaf = 0;
      if (!dockBox) return;
      dockBox.classList.remove("is-live");
      dockItems.forEach(function (el) { el.style.removeProperty("--m"); el.style.removeProperty("--dx"); el.style.removeProperty("z-index"); });
      dockBox = null; dockItems = []; dockBase = []; dockRows = [];
    };
    /* measure every chip where it sits at rest (transforms switched off for an instant), in page coordinates, and group the chips into rows */
    var dockMeasure = function () {
      dockBox.classList.add("dw-dock-measure");
      var sxp = window.scrollX, syp = window.scrollY;
      dockBase = dockItems.map(function (el) { var r = el.getBoundingClientRect(); return { l: r.left + sxp, t: r.top + syp, w: r.width, h: r.height }; });
      dockBox.classList.remove("dw-dock-measure");
      dockRows = [];
      dockBase.forEach(function (b, i) {
        var row = dockRows.filter(function (r) { return Math.abs(r.t - b.t) < 20; })[0];
        if (!row) { row = { t: b.t, idx: [] }; dockRows.push(row); }
        row.idx.push(i);
      });
      dockRows.forEach(function (row) { row.idx.sort(function (a, b) { return dockBase[a].l - dockBase[b].l; }); });
    };
    /* Dock maths: each chip's size follows a cosine curve of its distance to the pointer (1 + PEAK at the pointer, back to 1 at RADIUS),
       then each row is laid out again with the grown widths, so neighbours are pushed aside instead of being drawn over. */
    var dockPaint = function () {
      dockRaf = 0;
      if (!dockBox) return;
      sx += (dockX - sx) * 0.3; sy += (dockY - sy) * 0.3;
      var px = sx + window.scrollX, py = sy + window.scrollY, mags = [];
      dockBase.forEach(function (b, i) {
        var d = Math.hypot(px - (b.l + b.w / 2), (py - (b.t + b.h / 2)) * 1.25), t = Math.min(d / RADIUS, 1);
        mags[i] = 1 + PEAK * (1 + Math.cos(Math.PI * t)) / 2;
      });
      dockRows.forEach(function (row) {
        var first = dockBase[row.idx[0]], last = dockBase[row.idx[row.idx.length - 1]], grow = 0;
        row.idx.forEach(function (i) { grow += dockBase[i].w * (mags[i] - 1); });
        var frac = Math.max(0, Math.min(1, (px - first.l) / Math.max(1, last.l + last.w - first.l)));
        var left = first.l - grow * frac;                         /* the chip under the pointer stays roughly under it */
        row.idx.forEach(function (i, k) {
          var b = dockBase[i], nl = left;
          dockItems[i].style.setProperty("--dx", (nl + b.w * mags[i] / 2 - (b.l + b.w / 2)).toFixed(1) + "px");
          dockItems[i].style.setProperty("--m", mags[i].toFixed(3));
          dockItems[i].style.zIndex = String(Math.round(mags[i] * 100));
          var next = dockBase[row.idx[k + 1]];
          left += b.w * mags[i] + (next ? next.l - (b.l + b.w) : 0);
        });
      });
      if (Math.abs(dockX - sx) > 0.4 || Math.abs(dockY - sy) > 0.4 || Date.now() - dockIdle < 120) dockRaf = requestAnimationFrame(dockPaint);
    };
    document.addEventListener("pointermove", function (e) {
      if (e.pointerType !== "mouse") return;
      /* the effect starts a little before the pointer reaches the row and ends a little after it leaves, so it eases in and out */
      var box = e.target.closest ? e.target.closest(DOCK_BOXES) : null;
      if (!box && dockBox) {
        var br = dockBox.getBoundingClientRect();
        if (e.clientX > br.left - REACH && e.clientX < br.right + REACH && e.clientY > br.top - REACH && e.clientY < br.bottom + REACH) box = dockBox;
      }
      if (!box) { dockReset(); return; }
      if (box !== dockBox) {
        dockReset();
        dockBox = box; dockItems = $$(DOCK_ITEMS, box);
        dockItems.forEach(function (el) { el.classList.add("dw-dock-item"); });
        dockMeasure();
        box.classList.add("is-live");
        sx = e.clientX; sy = e.clientY;
      }
      dockX = e.clientX; dockY = e.clientY; dockIdle = Date.now();
      if (!dockRaf) dockRaf = requestAnimationFrame(dockPaint);
    }, { passive: true });
    document.addEventListener("pointerleave", dockReset);
    window.addEventListener("scroll", function () { if (dockBox && !dockRaf) { dockIdle = Date.now(); dockRaf = requestAnimationFrame(dockPaint); } }, { passive: true });
    /* the Dock's hop: a clicked chip jumps once */
    document.addEventListener("click", function (e) {
      var el = e.target.closest ? e.target.closest(DOCK_ITEMS) : null;
      if (el && el.animate) el.animate([{ translate: "0 0" }, { translate: "0 -22px", offset: .4 }, { translate: "0 0", offset: .7 }, { translate: "0 -8px", offset: .85 }, { translate: "0 0" }], { duration: 520, easing: "ease-out" });
    });
  }

  /* ---------- chat bubble: the chat app keeps its button inside its own sealed container, so the same pop animation is added there ---------- */
  if (!matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var chatTries = 0;
    var chatPop = setInterval(function () {
      chatTries++;
      var host = $("shopify-agent-runtime"), root = host && host.shadowRoot;
      if (root && $(".activator", root) && !$("#dw-chat-pop", root)) {
        var st = document.createElement("style");
        st.id = "dw-chat-pop";
        st.textContent =
          "@keyframes dwpop{0%,62%,100%{scale:1;rotate:0deg}68%{scale:1.2;rotate:-7deg}74%{scale:.94;rotate:6deg}80%{scale:1.1;rotate:-3deg}88%{scale:1;rotate:0deg}}" +
          "@keyframes dwring{0%,62%{box-shadow:0 0 0 0 rgba(240,90,50,0)}68%{box-shadow:0 0 0 0 rgba(240,90,50,.5)}100%{box-shadow:0 0 0 20px rgba(240,90,50,0)}}" +
          ".activator{animation:dwpop 7s ease-in-out 4.5s infinite,dwring 7s ease-out 4.5s infinite;transform-origin:50% 50%}" +
          ".activator:hover{animation:none}";
        root.appendChild(st);
        clearInterval(chatPop);
      }
      if (chatTries > 40) clearInterval(chatPop);
    }, 750);
  }

  /* the old theme's magnetic-button script nudges buttons toward the cursor; cancel any leftover nudge */
  $$(".magnet").forEach(function (b) { b.classList.remove("magnet"); b.style.translate = ""; });
  document.addEventListener("pointermove", function () {
    var cb = $(".dw-header .cart-btn"); if (cb && cb.style.translate) cb.style.translate = "";
  }, { passive: true });
})();
