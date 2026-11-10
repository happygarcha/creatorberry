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
      if (!dragging) { vel += (base - vel) * 0.04; ang += vel; paint(); }
      if (!still && onScreen && !document.hidden) rafId = requestAnimationFrame(loop);
    };
    var wake = function () { if (!rafId && !still && onScreen && !document.hidden) rafId = requestAnimationFrame(loop); };
    stageEl.addEventListener("pointerdown", function (e) { dragging = true; lastX = e.clientX; travelled = 0; vel = 0; });
    window.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      var dx = e.clientX - lastX; lastX = e.clientX; travelled += Math.abs(dx);
      ang += dx * 0.45; vel = dx * 0.45; paint();
    });
    var release = function () { if (dragging) { dragging = false; wake(); } };
    window.addEventListener("pointerup", release);
    window.addEventListener("pointercancel", release);
    reel.addEventListener("click", function (e) { if (travelled > 6) { e.preventDefault(); e.stopPropagation(); travelled = 0; } }, true);
    stageEl.addEventListener("pointerenter", function (e) { if (e.pointerType === "mouse") base = still ? 0 : 0.02; });
    stageEl.addEventListener("pointerleave", function () { base = still ? 0 : 0.1; });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { onScreen = en[0].isIntersecting; if (onScreen) wake(); }).observe(reel);
    document.addEventListener("visibilitychange", wake);
    paint(); wake();
  }
})();
