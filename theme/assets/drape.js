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
    var ringEl = $("[data-reel-ring]", reel), stageEl = $(".dw-reel-stage", reel), rItems = $$(".dw-reel-item", reel);
    var still = matchMedia("(prefers-reduced-motion: reduce)").matches;
    var count = rItems.length || 1, stepDeg = 360 / count;
    rItems.forEach(function (el, i) { el.style.setProperty("--ry", (i * stepDeg).toFixed(2) + "deg"); });
    var ang = -20, vel = still ? 0 : 0.1, base = still ? 0 : 0.1, dragging = false, lastX = 0, travelled = 0, onScreen = true, rafId = 0;
    var paint = function () { ringEl.style.transform = "rotateY(" + ang.toFixed(2) + "deg)"; };
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
      var rest = cells.map(function (c) { return c.dataset.handle; }).filter(function (h) { return !inAny[h]; });
      if (rest.length && Object.keys(subMap).length) {
        subMap.__more = rest;
        var mb = document.createElement("button");
        mb.type = "button"; mb.className = "dw-subchip"; mb.dataset.sub = "__more"; mb.setAttribute("aria-pressed", "false");
        mb.textContent = subBox.dataset.moreLabel || "More";
        subBox.appendChild(mb);
      }
      var setSub = function (value, fromUser) {
        subNow = value;
        $$(".dw-subchip", subBox).forEach(function (b) { var on = b.dataset.sub === value; b.classList.toggle("is-on", on); b.setAttribute("aria-pressed", on ? "true" : "false"); });
        applyFilter();
        if (fromUser) { try { history.replaceState(null, "", location.pathname + location.search + (value ? "#" + value : "")); } catch (e) {} }
      };
      subBox.addEventListener("click", function (e) { var b = e.target.closest(".dw-subchip"); if (b) setSub(b.dataset.sub, true); });
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
})();
