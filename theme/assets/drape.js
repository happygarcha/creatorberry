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
})();
