/* Drapewell Discover theme script: hero slideshow, product options, cart drawer, card glow. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  /* Motion (vanilla build of Framer Motion, assets/motion.js): springs for entrances and presses. CSS stays as the fallback. */
  var Mo = window.Motion, mo = !!(Mo && Mo.animate && !reduce);
  if (mo) document.documentElement.classList.add("mo");
  function clearStyle(el, props) { props.forEach(function (p) { el.style.removeProperty(p); }); }
  function enter(el, from, to, props, delay, spring) {
    /* set the start values first so there is no flash, then spring to the end values and hand control back to CSS */
    Object.keys(from).forEach(function (k) { el.style.setProperty(k, from[k]); });
    var done = function () { clearStyle(el, props); };
    Mo.animate(el, to, Object.assign({ type: "spring", stiffness: 170, damping: 21, delay: delay || 0 }, spring || {})).finished.then(done, done);
  }
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var money = function (cents) {
    try { return new Intl.NumberFormat(document.documentElement.lang || undefined, { style: "currency", currency: (window.Shopify && Shopify.currency && Shopify.currency.active) || "CAD" }).format(cents / 100); }
    catch (e) { return "$" + (cents / 100).toFixed(2); }
  };

  /* ---------- add-to-cart flight ---------- */
  function fly(img) {
    if (reduce || !img || !img.getBoundingClientRect || !img.src) return;
    var target = $$("[data-open-cart]").filter(function (e) { var r = e.getBoundingClientRect(); return r.width && r.height && r.bottom > 0 && r.top < innerHeight; })[0];
    if (!target || !img.animate) return;
    var a = img.getBoundingClientRect(), b = target.getBoundingClientRect();
    var c = document.createElement("img"); c.src = img.currentSrc || img.src; c.alt = ""; c.className = "fly";
    c.style.cssText = "left:" + a.left + "px;top:" + a.top + "px;width:" + a.width + "px;height:" + a.height + "px";
    document.body.appendChild(c);
    var dx = b.left + b.width / 2 - (a.left + a.width / 2), dy = b.top + b.height / 2 - (a.top + a.height / 2);
    c.animate([{ transform: "translate(0,0) scale(1)", opacity: 1, borderRadius: "16px" }, { transform: "translate(" + dx + "px," + dy + "px) scale(0.05)", opacity: 0.25, borderRadius: "50%" }], { duration: 650, easing: "cubic-bezier(0.5, 0, 0.2, 1)" }).onfinish = function () { c.remove(); };
  }

  /* ---------- cart ---------- */
  var drawer = $("#cart-drawer");
  var cart = { items: [], total_price: 0, item_count: 0 };
  var lastCount = null;
  function paintCount() { $$("[data-cart-total]").forEach(function (el) { el.textContent = money(cart.total_price); }); $$("[data-cart-count]").forEach(function (el) { el.textContent = cart.item_count; if (lastCount !== null && cart.item_count > lastCount && !reduce) {
        if (mo) { Mo.animate(el, { scale: 1.5 }, { duration: 0.12, ease: "easeOut" }).finished.then(function () { Mo.animate(el, { scale: 1 }, { type: "spring", stiffness: 380, damping: 14 }); }); }
        else { el.classList.remove("bump"); void el.offsetWidth; el.classList.add("bump"); }
      } }); lastCount = cart.item_count; }
  var cartAnimTotal = null, cartQty = {};
  function paintCart() {
    paintCount();
    if (!drawer) return;
    var box = $("#cart-lines", drawer);
    box.innerHTML = cart.items.length ? cart.items.map(function (l, idx) {
      return '<div class="line" data-key="' + esc(l.key) + '" style="--n:' + idx + '"><div class="th">' + (l.image ? '<img src="' + esc(l.image.replace(/(\.[a-z]+)(\?|$)/i, "_160x$1$2")) + '" alt="" loading="lazy">' : "") + '</div>' +
        '<div class="d"><a href="' + esc(l.url) + '">' + esc(l.product_title) + '</a>' + (l.variant_title && l.variant_title !== "Default Title" ? "<span>" + esc(l.variant_title) + "</span>" : "") +
        '<div class="q"><button type="button" data-line="' + l.key + '" data-q="' + (l.quantity - 1) + '" aria-label="Fewer">−</button><output>' + l.quantity + '</output><button type="button" data-line="' + l.key + '" data-q="' + (l.quantity + 1) + '" aria-label="More">+</button><button type="button" class="rm" data-line="' + l.key + '" data-q="0">Remove</button></div></div>' +
        '<div class="pr">' + money(l.final_line_price) + "</div></div>";
    }).join("") : '<p class="empty">Your cart is empty.</p>';
    var subEl = $("#cart-sub", drawer);
    if (mo && drawer.open && cartAnimTotal !== null && cartAnimTotal !== cart.total_price) {
      var fromT = cartAnimTotal, toT = cart.total_price;
      Mo.animate(fromT, toT, { duration: 0.55, ease: [0.2, 0.7, 0.2, 1], onUpdate: function (v) { subEl.textContent = money(Math.round(v)); } }).finished.then(function () { subEl.textContent = money(toT); });
      Mo.animate(subEl, { scale: [1.12, 1] }, { type: "spring", stiffness: 340, damping: 16 });
    } else subEl.textContent = money(cart.total_price);
    cartAnimTotal = cart.total_price;
    if (mo && drawer.open) {
      var seen = {};
      $$(".line", drawer).forEach(function (ln) {
        var k = ln.dataset.key, q = parseInt($("output", ln).textContent, 10); seen[k] = q;
        if (!(k in cartQty)) enter(ln, { opacity: "0", translate: "36px 0px" }, { opacity: 1, translate: ["36px 0px", "0px 0px"] }, ["opacity", "translate"], 0, { stiffness: 210, damping: 22 });
        else if (cartQty[k] !== q) {
          var dir = q > cartQty[k] ? 1 : -1;
          Mo.animate($("output", ln), { opacity: [0.2, 1], translate: ["0px " + dir * 10 + "px", "0px 0px"] }, { type: "spring", stiffness: 420, damping: 24 });
          Mo.animate($(".pr", ln), { opacity: [0.3, 1], translate: ["0px 8px", "0px 0px"] }, { type: "spring", stiffness: 300, damping: 22 });
        }
      });
      cartQty = seen;
      var emp = $(".empty", drawer); if (emp) Mo.animate(emp, { opacity: [0, 1], scale: [0.9, 1] }, { type: "spring", stiffness: 260, damping: 18 });
    } else {
      cartQty = {}; $$(".line", drawer).forEach(function (ln) { cartQty[ln.dataset.key] = parseInt($("output", ln).textContent, 10); });
    }
    var co = $("#cart-co", drawer); co.href = cart.items.length ? quickHref() : "/cart"; co.setAttribute("aria-disabled", String(!cart.items.length));
    paintNudge();
    paintUpsell();
  }
  /* ---------- Buy 2, save 10% progress bar: counts cart items whose product is in the offer collection ---------- */
  function paintNudge() {
    var box = $("#offer-nudge"); if (!box) return;
    var ids = (box.dataset.offerIds || "").split(",").filter(Boolean);
    var q = 0; if (ids.length) cart.items.forEach(function (i) { if (ids.indexOf(String(i.product_id)) > -1) q += i.quantity; });
    box.hidden = !ids.length || q === 0;
    var done = q >= 2;
    $("[data-on-text]", box).textContent = done ? "Offer unlocked: 10% off your offer items is applied at checkout." : "Add 1 more offer item to save 10%.";
    $("[data-on-fill]", box).style.width = (done ? 100 : q === 1 ? 50 : 0) + "%";
    $("[role=progressbar]", box).setAttribute("aria-valuenow", String(Math.min(q, 2)));
    $("[data-on-link]", box).hidden = done;
    box.dataset.unlocked = done ? "1" : "0";
    tickQuick();
  }

  /* ---------- extra 1% for checking out within 15 minutes of unlocking the offer ----------
     Per-browser and one-time: the clock starts when the shopper first has 2 offer items, the extra 1% is the Shopify
     the quick-checkout code (set with /discount/<code>, applied at checkout), and when the 15 minutes are over the code cookie
     is removed and this browser never gets the window again. Without localStorage nothing is shown, because it could not be enforced. */
  var QUICK = { ms: 15 * 60 * 1000, key: "dw_quick1" }, quickTimer = null, quickBusy = false, quickRefreshed = false;
  function quickState() {
    try { var v = JSON.parse(localStorage.getItem(QUICK.key) || "null"); return v && typeof v.start === "number" ? v : null; } catch (e) { return false; }
  }
  /* the code is only handed out by the server to a cart that really holds 2 offer items (templates/cart.quick.liquid) */
  function quickFetchCode() {
    return fetch("/cart?view=quick", { credentials: "same-origin" }).then(function (r) { return r.text(); }).then(function (t) {
      var c = (t || "").trim(); if (!/^[A-Za-z0-9-]{12,48}$/.test(c)) throw 0; return c;
    });
  }
  /* while the 15 minutes run, the checkout link carries the code itself, so checkout does not depend on the cookie alone */
  function quickHref() {
    var st = quickState();
    return st && st.code && st.start + QUICK.ms > Date.now() ? "/checkout?discount=" + encodeURIComponent(st.code) : "/checkout";
  }
  /* once the window is over, the code must also leave the CART (Shopify keeps a code on the cart, so going back from checkout and checking out again would keep it) */
  var quickClearing = null, QUICK_CODE_RE = /^(ADDITIONAL-|[0-9a-f]{32}$)/i;
  function quickExpired() { var st = quickState(); return !!(st && st.start + QUICK.ms <= Date.now()); }
  function quickClearCart() {
    if (quickClearing) return quickClearing;
    quickClearing = fetch("/cart.js", { credentials: "same-origin" }).then(function (r) { return r.json(); }).then(function (c) {
      var has = (c.discount_codes || []).some(function (d) { return QUICK_CODE_RE.test(String(d.code)); });
      if (!has) return;
      return fetch("/cart/update.js", { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ discount: "" }) });
    }).catch(function () {});
    return quickClearing;
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest('button[name="checkout"], #cart-co'); if (!b) return;
    if (quickExpired() && (b.id !== "cart-co" || cart.items.length)) {
      e.preventDefault(); dropQuickCode();
      quickClearCart().then(function () { location.href = "/checkout"; });
      return;
    }
    if (b.id === "cart-co" || quickHref() === "/checkout") return;
    e.preventDefault(); location.href = quickHref();
  });
  window.addEventListener("pageshow", function (ev) { if (ev.persisted) { quickClearing = null; tickQuick(); } });
  function paintCheckoutLink() { var co = $("#cart-co", drawer); if (co && cart.items.length) co.href = quickHref(); }
  function dropQuickCode() { document.cookie = "discount_code=; Max-Age=0; path=/"; }
  function tickQuick() {
    if (quickExpired()) { dropQuickCode(); quickClearCart(); }
    var boxes = $$(".offer-nudge"); if (!boxes.length) return;
    var st = quickState();
    if (st === false) { $$("[data-on-q]").forEach(function (el) { el.hidden = true; }); return; }
    var unlocked = boxes.some(function (b) { return b.dataset.unlocked === "1"; });
    if (!st && unlocked) {
      /* the clock starts only after the code was received and applied, so the promise on screen is always true */
      if (quickBusy) return; quickBusy = true;
      quickFetchCode().then(function (code) {
        return fetch("/discount/" + code, { credentials: "same-origin" }).then(function () {
          localStorage.setItem(QUICK.key, JSON.stringify({ start: Date.now(), code: code })); quickRefreshed = true; quickBusy = false; tickQuick();
        });
      }).catch(function () { quickBusy = false; });
      return;
    }
    /* once per page load, while the window runs: fetch the current code again and re-apply it (covers a changed code or a lost cookie) */
    if (st && unlocked && !quickRefreshed && st.start + QUICK.ms > Date.now() && !quickBusy) {
      quickRefreshed = true;
      quickFetchCode().then(function (code) {
        return fetch("/discount/" + code, { credentials: "same-origin" }).then(function () {
          try { localStorage.setItem(QUICK.key, JSON.stringify({ start: st.start, code: code })); } catch (e) {} paintCheckoutLink();
        });
      }).catch(function () {});
    }
    if (!st) { $$("[data-on-q]").forEach(function (el) { el.hidden = true; }); return; }
    var left = st.start + QUICK.ms - Date.now(), txt;
    if (left > 0) { var m = Math.floor(left / 60000), sec = Math.floor(left / 1000) % 60; txt = "Additional 1% off is applied at checkout. Keep it by ordering within " + m + ":" + (sec < 10 ? "0" : "") + sec + ". One time per browser."; }
    else { dropQuickCode(); quickClearCart(); txt = "The additional 1% offer has ended. Your 10% offer discount still applies."; }
    paintCheckoutLink();
    $$("[data-on-q]").forEach(function (el) { el.hidden = false; el.textContent = txt; });
    if (left > 0 && !quickTimer) quickTimer = setInterval(tickQuick, 1000);
    if (left <= 0 && quickTimer) { clearInterval(quickTimer); quickTimer = null; }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", tickQuick); else tickQuick();

  /* ---------- cart upsell: Shopify's related-product recommendations for the newest cart item ---------- */
  var upCache = {}, upSig = "";
  function renderUp(list) {
    var sec = $("#cart-up"), ul = $("#cart-up-list"); if (!sec || !ul) return;
    var inCart = cart.items.map(function (i) { return i.product_id; });
    var show = list.filter(function (p) { return p.available && inCart.indexOf(p.id) < 0; }).slice(0, 3);
    sec.hidden = !show.length;
    var addTxt = sec.dataset.addTxt || "Add", chooseTxt = sec.dataset.chooseTxt || "Choose an option";
    ul.innerHTML = show.map(function (p) {
      var vs = (p.variants || []).filter(function (v) { return v.available; });
      var single = p.variants && p.variants.length === 1 && vs.length === 1;
      var lbl = esc(addTxt) + ": " + esc(p.title);
      var btn = single ? '<button type="button" class="up-add" data-up-add="' + vs[0].id + '" aria-label="' + lbl + '"><span aria-hidden="true">+</span></button>'
                       : '<button type="button" class="up-add" data-up-pick aria-expanded="false" aria-label="' + lbl + '"><span aria-hidden="true">+</span></button>';
      var pick = single ? "" : '<div class="up-pick"><select aria-label="' + esc(chooseTxt) + ": " + esc(p.title) + '">' + vs.map(function (v) { var vi = v.featured_image && (v.featured_image.src || v.featured_image); return '<option value="' + v.id + '"' + (vi ? ' data-img="' + esc(qimg(vi, 160)) + '"' : "") + ">" + esc(v.title || (v.options || []).join(" / ")) + (v.price != null && v.price !== p.price ? " — " + money(v.price) : "") + "</option>"; }).join("") + '</select><button type="button" class="up-go" data-up-confirm>' + esc(addTxt) + "</button></div>";
      return '<li class="up"><a class="up-th" href="' + esc(p.url) + '"><span class="ph">' + (p.featured_image ? '<img src="' + esc(qimg(p.featured_image, 160)) + '" alt="" loading="lazy">' : "") + '</span></a>' +
        '<div class="up-d"><a href="' + esc(p.url) + '">' + esc(p.title) + '</a><span>' + money(p.price) + "</span></div>" + btn + pick + "</li>";
    }).join("");
    var sig = show.map(function (p) { return p.id; }).join(",");
    if (mo && drawer && drawer.open && sig && sig !== upSig) $$(".up", ul).forEach(function (li, i) { enter(li, { opacity: "0", translate: "0px 14px" }, { opacity: 1, translate: ["0px 14px", "0px 0px"] }, ["opacity", "translate"], 0.1 + i * 0.08); });
    upSig = sig;
  }
  function paintUpsell() {
    var sec = $("#cart-up"); if (!sec) return;
    if (!cart.items.length) { sec.hidden = true; return; }
    var pid = cart.items[0].product_id;
    if (upCache[pid]) return renderUp(upCache[pid]);
    fetch("/recommendations/products.json?product_id=" + pid + "&limit=6&intent=related", { headers: { Accept: "application/json" } })
      .then(function (r) { return r.ok ? r.json() : { products: [] }; })
      .then(function (d) { upCache[pid] = d.products || []; if (cart.items[0] && cart.items[0].product_id === pid) renderUp(upCache[pid]); })
      .catch(function () {});
  }
  function loadCart() { return fetch("/cart.js", { headers: { Accept: "application/json" } }).then(function (r) { return r.json(); }).then(function (c) { cart = c; paintCart(); return c; }).catch(function () {}); }
  function openCart() {  /* also exposed for quick view */ if (!drawer || !drawer.showModal) { location.href = "/cart"; return; } loadCart().then(function () {
      if (drawer.open) return;
      var lines = mo ? $$(".line", drawer) : [];
      lines.forEach(function (l) { l.style.opacity = "0"; l.style.translate = "28px 0px"; });
      drawer.showModal();
      lines.forEach(function (l, i) { enter(l, { opacity: "0", translate: "28px 0px" }, { opacity: 1, translate: ["28px 0px", "0px 0px"] }, ["opacity", "translate"], 0.12 + i * 0.07); });
      if (mo) {
        var hd = $(".cart-in header", drawer);
        if (hd) enter(hd, { opacity: "0", translate: "0px -12px" }, { opacity: 1, translate: ["0px -12px", "0px 0px"] }, ["opacity", "translate"], 0.08);
        $$(".cart-in footer > *", drawer).forEach(function (el, i) { enter(el, { opacity: "0", translate: "0px 16px" }, { opacity: 1, translate: ["0px 16px", "0px 0px"] }, ["opacity", "translate"], 0.2 + i * 0.05); });
        $$(".up", drawer).forEach(function (li, i) { enter(li, { opacity: "0", translate: "0px 14px" }, { opacity: 1, translate: ["0px 14px", "0px 0px"] }, ["opacity", "translate"], 0.4 + i * 0.08); });
        var emp0 = $(".empty", drawer); if (emp0) Mo.animate(emp0, { opacity: [0, 1], scale: [0.92, 1] }, { type: "spring", stiffness: 240, damping: 18, delay: 0.15 });
      }
    }); }
  if (drawer) {
    drawer.addEventListener("click", function (e) {
      if (e.target === drawer || e.target.closest("[data-close-cart]")) return drawer.close();
      var ua = e.target.closest("[data-up-add]");
      if (ua) { ua.disabled = true; fetch("/cart/add.js", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify({ id: ua.dataset.upAdd, quantity: 1 }) }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(loadCart).catch(function () { ua.disabled = false; }); return; }
      var up = e.target.closest("[data-up-pick]");
      if (up) { var row = up.closest(".up"), o = !row.classList.contains("open"); row.classList.toggle("open", o); up.setAttribute("aria-expanded", String(o)); if (o) { var sel = $("select", row); if (sel) sel.focus(); } return; }
      var uc = e.target.closest("[data-up-confirm]");
      if (uc) { var sv = $("select", uc.closest(".up")); if (!sv || !sv.value) return; uc.disabled = true; fetch("/cart/add.js", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify({ id: sv.value, quantity: 1 }) }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(loadCart).catch(function () { uc.disabled = false; }); return; }
      var b = e.target.closest("[data-line]"); if (!b) return;
      var sendChange = function () {
        fetch("/cart/change.js", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify({ id: b.dataset.line, quantity: parseInt(b.dataset.q, 10) }) })
          .then(function (r) { return r.json(); }).then(function (c) {
            cart = c; paintCart();
            /* emptied the cart: let the message show for a beat, then slide the drawer away */
            if (!c.items.length) setTimeout(function () { if (!cart.items.length && drawer.open) drawer.close(); }, reduce ? 400 : 1100);
          });
      };
      var gone = b.closest(".line");
      if (mo && gone && b.dataset.q === "0") { var go = function () { sendChange(); }; Mo.animate(gone, { opacity: 0, translate: "48px 0px" }, { duration: 0.24, ease: [0.4, 0, 1, 1] }).finished.then(go, go); }
      else sendChange();
    });
  }
  /* upsell: show the chosen variant's own picture in the row */
  if (drawer) drawer.addEventListener("change", function (e) {
    var sel = e.target.closest && e.target.closest(".up-pick select"); if (!sel) return;
    var u = sel.selectedOptions[0] && sel.selectedOptions[0].dataset.img, im = $(".up-th img", sel.closest(".up")); if (!u || !im) return;
    if (reduce || !im.animate) { im.src = u; return; }
    var pre = new Image(); pre.onload = function () { im.animate([{ opacity: 1 }, { opacity: 0.15 }], { duration: 120, fill: "forwards" }).onfinish = function () { im.src = u; im.animate([{ opacity: 0.15 }, { opacity: 1 }], { duration: 260, fill: "forwards" }); }; }; pre.onerror = function () { im.src = u; }; pre.src = u;
  });
  document.addEventListener("click", function (e) { var t = e.target.closest("[data-open-cart]"); if (t) { e.preventDefault(); openCart(); } });
  loadCart();

  /* ---------- product page ---------- */
  var pdp = $("[data-product]");
  if (pdp) {
    var data = JSON.parse($("[data-product-json]").textContent);
    var form = $("#product-form"), idInput = $("[data-variant-id]", form), addBtn = $("[data-add]", form), msg = $("[data-msg]", form), priceEl = $("[data-price]");
    var qty = $("[data-qty-input]", form), out = $("[data-qty-out]", form);
    var addLabel = addBtn.textContent;
    function selected() { var vals = []; $$("[data-option]:checked", form).forEach(function (r) { vals[parseInt(r.dataset.option, 10) - 1] = r.value; }); return vals; }
    function find(vals) { return data.variants.filter(function (v) { return vals.every(function (x, i) { return x === undefined || v.options[i] === x; }); })[0]; }
    function swapMain(url) { var main = $("[data-main-image] img"), fig = $("[data-main-image]"); if (!main) return; if (reduce) { main.removeAttribute("srcset"); main.removeAttribute("width"); main.removeAttribute("height"); main.src = url; return; } fig.classList.add("swap"); setTimeout(function () { main.removeAttribute("srcset"); main.removeAttribute("width"); main.removeAttribute("height"); main.src = url; fig.classList.remove("swap"); }, 220); }
    var shipEl = $("[data-ship]");
    function shipBand(list, g) { var out = null; String(list || "").split(",").some(function (pair) { var p = pair.split(":"); if (g <= parseFloat(p[0])) { out = p[1]; return true; } return false; }); return out; }
    function shipFor(g) {
      if (!shipEl || !(g > 0)) return;
      var ca = shipBand(shipEl.dataset.shipCa, g), us = shipBand(shipEl.dataset.shipUs, g);
      var strong = shipEl.querySelectorAll("strong");
      if (ca && us && strong.length === 2) { strong[0].textContent = "CA$" + ca; strong[1].textContent = "CA$" + us; }
    }
    function sync() {
      var vals = selected(); var need = data.options.length;
      var complete = vals.filter(Boolean).length === need;
      var v = complete ? find(vals) : null;
      if (!need) v = data.variants[0];
      if (v) { shipFor(v.weight); }
      if (v) { idInput.value = v.id; priceEl.innerHTML = money(v.price) + (v.compare_at_price > v.price ? '<s class="was">' + money(v.compare_at_price) + '</s><span class="off">-' + Math.floor((v.compare_at_price - v.price) * 100 / v.compare_at_price) + "%</span>" : ""); addBtn.disabled = !v.available; addBtn.textContent = v.available ? addLabel : "Sold out"; msg.textContent = v.available ? "" : "Sold out."; }
      else { addBtn.disabled = !complete ? false : true; msg.textContent = complete ? "That combination is not available." : ""; if (complete) addBtn.disabled = true; }
      /* dim values that no variant offers given the other choices */
      $$(".opt-group", form).forEach(function (g, gi) {
        $$("[data-option]", g).forEach(function (inp) {
          var test = vals.slice(); test[gi] = inp.value;
          var ok = data.variants.some(function (x) { return test.every(function (y, i) { return y === undefined || x.options[i] === y; }) && x.available; });
          inp.parentElement.style.opacity = ok ? "" : "0.45";
        });
      });
      if (v && v.featured_image && v.featured_image.src) { var main = $("[data-main-image] img"); if (main && !main.src.includes(v.featured_image.src.split("?")[0].split("/").pop().split(".")[0])) { swapMain(v.featured_image.src.replace(/(\.[a-z]+)(\?|$)/i, "_1200x$1$2")); } }
    }
    form.addEventListener("change", function (e) { if (e.target.matches("[data-option]")) sync(); });
    $("[data-qty-less]", form).addEventListener("click", function () { qty.value = Math.max(1, +qty.value - 1); out.textContent = qty.value; });
    $("[data-qty-more]", form).addEventListener("click", function () { qty.value = Math.min(9, +qty.value + 1); out.textContent = qty.value; });
    form.addEventListener("submit", function (e) {
      e.preventDefault(); if (addBtn.disabled) return;
      addBtn.disabled = true;
      fetch("/cart/add.js", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify({ id: idInput.value, quantity: +qty.value }) })
        .then(function (r) { if (!r.ok) throw new Error("add failed"); return r.json(); })
        .then(function () { fly($("[data-main-image] img")); addBtn.classList.add("is-ok"); addBtn.textContent = "Added ✓"; loadCart().then(function () { setTimeout(function () { addBtn.disabled = false; addBtn.classList.remove("is-ok"); addBtn.textContent = addLabel; openCart(); }, reduce ? 0 : 700); }); })
        .catch(function () { addBtn.disabled = false; msg.textContent = "Could not add that to the cart. Try again."; });
    });
    $$("[data-thumb]").forEach(function (b) { b.addEventListener("click", function () {
      swapMain(b.dataset.thumb);
      $$("[data-thumb]").forEach(function (x) { x.setAttribute("aria-current", String(x === b)); }); b.focus();
    }); });
    /* product video: its thumbnail swaps the main photo for the player; any photo thumbnail or a colour change swaps back */
    var vpane = $("[data-video-pane]"), vthumb = $("[data-thumb-video]"), vfig = $("[data-main-image]");
    if (vpane && vthumb && vfig) {
      var vvid = $("video", vpane);
      var showVideo = function (on) {
        vpane.hidden = !on; vfig.hidden = on; vthumb.setAttribute("aria-current", String(on));
        if (on) $$("[data-thumb]").forEach(function (x) { x.setAttribute("aria-current", "false"); });
        else if (vvid) vvid.pause();
      };
      vthumb.addEventListener("click", function () { showVideo(true); });
      $$("[data-thumb]").forEach(function (b) { b.addEventListener("click", function () { showVideo(false); }); });
      form.addEventListener("change", function (e) { if (e.target.matches("[data-option]") && !vpane.hidden) showVideo(false); });
    }
    var fig = $("[data-main-image]");
    if (fig && fine) fig.addEventListener("pointermove", function (e) { var r = fig.getBoundingClientRect(); fig.style.setProperty("--zx", (((e.clientX - r.left) / r.width) * 100).toFixed(0) + "%"); fig.style.setProperty("--zy", (((e.clientY - r.top) / r.height) * 100).toFixed(0) + "%"); }, { passive: true });
    /* swipe the gallery on touch screens */
    var thumbBtns = $$("[data-thumb]");
    if (fig && thumbBtns.length > 1) {
      var gx = 0, gy = 0;
      fig.addEventListener("touchstart", function (e) { gx = e.touches[0].clientX; gy = e.touches[0].clientY; }, { passive: true });
      fig.addEventListener("touchend", function (e) {
        var t = e.changedTouches[0], dx = t.clientX - gx, dy = t.clientY - gy; if (Math.abs(dx) < 48 || Math.abs(dx) < Math.abs(dy) * 1.4) return;
        var at = thumbBtns.findIndex(function (b) { return b.getAttribute("aria-current") === "true"; }), n = (at + (dx < 0 ? 1 : -1) + thumbBtns.length) % thumbBtns.length;
        fig.style.setProperty("--dir", dx < 0 ? 1 : -1); thumbBtns[n].click();
      }, { passive: true });
    }

    /* sticky add-to-cart bar (phones) */
    var sticky = $("[data-sticky]"), sBtn = $("[data-sticky-btn]"), sPrice = $("[data-sticky-price]");
    if (sticky && "IntersectionObserver" in window) {
      document.body.appendChild(sticky); /* out of any transformed ancestor so position:fixed stays on the viewport */
      var mirror = function () { sBtn.disabled = addBtn.disabled; sBtn.textContent = addBtn.textContent; sBtn.classList.toggle("is-ok", addBtn.classList.contains("is-ok")); sPrice.textContent = priceEl.textContent; };
      new MutationObserver(mirror).observe(form, { subtree: true, childList: true, attributes: true, characterData: true });
      new MutationObserver(mirror).observe(priceEl, { childList: true, characterData: true, subtree: true });
      new IntersectionObserver(function (en) { var e = en[0]; sticky.hidden = e.isIntersecting || e.boundingClientRect.top > 0; mirror(); }).observe(addBtn);
    }

    /* recently viewed */
    try {
      var KEY = "dw-recent", list = JSON.parse(localStorage.getItem(KEY) || "[]");
      if (!Array.isArray(list)) list = [];
      var others = list.filter(function (x) { return x && x.h !== data.handle; });
      var me = { h: data.handle, t: data.title, i: data.featured_image || "", p: data.price };
      localStorage.setItem(KEY, JSON.stringify([me].concat(others).slice(0, 10)));
      var row = $("[data-recent-row]"), box = $("[data-recent]");
      if (row && others.length) {
        row.innerHTML = others.slice(0, 6).map(function (x) {
          return '<a class="mini-card" href="/products/' + esc(x.h) + '"><span class="ph">' + (x.i ? '<img src="' + esc(String(x.i).replace(/(\.[a-z]+)(\?|$)/i, "_300x$1$2")) + '" alt="" loading="lazy">' : "") + '</span><span class="t">' + esc(x.t) + '</span><span class="p">' + money(x.p) + "</span></a>";
        }).join("");
        box.hidden = false;
      }
    } catch (e) { /* storage blocked: skip */ }
    sync();
  }

  /* ---------- quick view ---------- */
  var quick = $("#quick"), qin = $("#quick-in");
  function qimg(src, w) { return String(src || "").replace(/(\.[a-z]+)(\?|$)/i, "_" + w + "x$1$2"); }
  function openQuick(handle) {
    if (!quick || !quick.showModal) { location.href = "/products/" + handle; return; }
    fetch("/products/" + encodeURIComponent(handle) + ".js", { headers: { Accept: "application/json" } }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (p) {
      var names = (p.options || []).map(function (o) { return typeof o === "string" ? o : o.name; });
      var opt = function (v) { return v.options || [v.option1, v.option2, v.option3].filter(Boolean); };
      var plain = p.variants.length === 1 && names.length <= 1 && /default title/i.test(opt(p.variants[0])[0] || "");
      var first = p.variants.filter(function (v) { return v.available; })[0] || p.variants[0], pick = opt(first).slice();
      var groups = plain ? "" : names.map(function (n, gi) {
        var vals = []; p.variants.forEach(function (v) { var x = opt(v)[gi]; if (vals.indexOf(x) < 0) vals.push(x); });
        return '<fieldset class="opt-group"><legend>' + esc(n) + '</legend><div class="chips">' + vals.map(function (x) { return '<label class="chipb"><input type="radio" name="q-' + gi + '" value="' + esc(x) + '" data-qopt="' + gi + '"' + (pick[gi] === x ? " checked" : "") + "><span>" + esc(x) + "</span></label>"; }).join("") + "</div></fieldset>";
      }).join("");
      qin.innerHTML = '<div class="grab" data-grab aria-hidden="true"><i></i></div><button type="button" class="x" data-qclose aria-label="Close">Close</button>' +
        '<figure class="ph tall"><img data-qimg alt="" src="' + esc(qimg(p.featured_image, 800)) + '"></figure>' +
        '<div class="q-info"><h2>' + esc(p.title) + '</h2><p class="p-price" data-qprice></p>' + groups +
        '<button type="button" class="btn primary" data-qadd></button><p class="msg" data-qmsg role="status" aria-live="polite"></p>' +
        '<a class="more" href="' + esc(p.url) + '">View full details &rarr;</a></div>';
      var cur;
      var paint = function () {
        cur = p.variants.filter(function (v) { return opt(v).every(function (x, i) { return x === pick[i]; }); })[0];
        var b = $("[data-qadd]", qin), m = $("[data-qmsg]", qin);
        $("[data-qprice]", qin).textContent = cur ? money(cur.price) : "";
        b.disabled = !cur || !cur.available; b.textContent = !cur ? "Unavailable" : cur.available ? "Add to cart" : "Sold out"; m.textContent = cur ? "" : "That combination is not available.";
        if (cur && cur.featured_image && cur.featured_image.src) { var im = $("[data-qimg]", qin), u = qimg(cur.featured_image.src, 800); if (im.getAttribute("src") !== u) im.src = u; }
      };
      qin.onchange = function (e) { if (e.target.matches("[data-qopt]")) { pick[+e.target.dataset.qopt] = e.target.value; paint(); } };
      qin.onclick = function (e) {
        if (e.target.closest("[data-qclose]")) return quick.close();
        var b = e.target.closest("[data-qadd]"); if (!b || b.disabled) return;
        b.disabled = true;
        fetch("/cart/add.js", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify({ id: cur.id, quantity: 1 }) })
          .then(function (r) { if (!r.ok) throw 0; return r.json(); })
          .then(function () { var im = $("[data-qimg]", qin); fly(im); quick.close(); loadCart().then(function () { setTimeout(openCart, reduce ? 0 : 650); }); })
          .catch(function () { b.disabled = false; $("[data-qmsg]", qin).textContent = "Could not add that to the cart. Try again."; });
      };
      paint(); quick.showModal();
    }).catch(function () { location.href = "/products/" + handle; });
  }
  if (quick) {
    quick.addEventListener("click", function (e) { if (e.target === quick) quick.close(); });
    /* drag the grab handle down to dismiss (phones) */
    var qy = 0, qd = 0, dragging = false;
    quick.addEventListener("pointerdown", function (e) { if (!e.target.closest("[data-grab]")) return; dragging = true; qy = e.clientY; qd = 0; quick.style.transition = "none"; quick.setPointerCapture && quick.setPointerCapture(e.pointerId); });
    quick.addEventListener("pointermove", function (e) { if (!dragging) return; qd = Math.max(0, e.clientY - qy); quick.style.transform = "translateY(" + qd + "px)"; });
    var endDrag = function () { if (!dragging) return; dragging = false; quick.style.transition = ""; quick.style.transform = ""; if (qd > 110) quick.close(); };
    quick.addEventListener("pointerup", endDrag); quick.addEventListener("pointercancel", endDrag);
  }
  document.addEventListener("click", function (e) { var q = e.target.closest("[data-quick]"); if (q) { e.preventDefault(); openQuick(q.dataset.quick); } });


  /* ---------- room accordion ---------- */
  $$(".sub-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var li = btn.closest(".room"), open = !li.classList.contains("is-open");
      li.classList.toggle("is-open", open); btn.setAttribute("aria-expanded", String(open));
    });
  });

  /* ---------- hero slideshow ---------- */
  var hero = $("[data-hero]");
  if (hero) {
    var slides = $$(".slide", hero), dots = $$("[data-go]", hero), bar = $("[data-hero-prog]", hero), pauseBtn = $("[data-hero-pause]", hero);
    var cur = 0, timer = 0, paused = false;
    function enterSlide(sl) {
      var copy = $$(".hero-copy.stagger > *", sl), art = $(".hero-art .ph", sl), price = $(".hero-price", sl);
      copy.forEach(function (el, i) { enter(el, { opacity: "0", translate: "0px 22px" }, { opacity: 1, translate: ["0px 22px", "0px 0px"] }, ["opacity", "translate"], 0.15 + i * 0.09, { stiffness: 150, damping: 20 }); });
      if (price) enter(price, { opacity: "0", translate: "0px 10px" }, { opacity: 1, translate: ["0px 10px", "0px 0px"] }, ["opacity", "translate"], 0.55);
      if (art) enter(art, { opacity: "0", "--hs": "0.9", "--hr": "3" }, { opacity: 1, "--hs": 1, "--hr": 0 }, ["opacity", "--hs", "--hr"], 0.1, { stiffness: 90, damping: 16 });
    }
    function show(i, initial) {
      if (!slides.length) return; cur = (i + slides.length) % slides.length;
      hydrate(slides[cur]);
      slides.forEach(function (s, k) { var on = k === cur; s.classList.toggle("is-active", on); if (on) s.removeAttribute("aria-hidden"); else s.setAttribute("aria-hidden", "true"); $$("a", s).forEach(function (a) { a.tabIndex = on ? 0 : -1; }); });
      dots.forEach(function (d, k) { d.setAttribute("aria-pressed", String(k === cur)); });
      hero.style.setProperty("--hue", slides[cur].dataset.hue);
      /* the first slide is already visible from the server HTML: never hide and re-animate it on load (that delayed the largest paint) */
      if (mo && !initial) enterSlide(slides[cur]);
      if (bar) { bar.classList.remove("run"); void bar.offsetWidth; if (!reduce && !initial) bar.classList.add("run"); }
    }
    /* autoplay waits for the first touch, key, scroll or click (or 15 s) so the slide change never repaints a bigger image into the load measurement */
    var armed = false, armT = 0;
    function hydrate(sl) { $$("img[data-defer]", sl).forEach(function (im) { im.removeAttribute("data-defer"); if (im.dataset.srcset) im.srcset = im.dataset.srcset; if (im.dataset.src) im.src = im.dataset.src; }); }
    function arm() { if (armed) return; armed = true; clearTimeout(armT); slides.forEach(hydrate); start(); if (bar && !reduce && !paused) { bar.classList.remove("run"); void bar.offsetWidth; bar.classList.add("run"); } }
    function start() { clearInterval(timer); if (!armed || paused || document.hidden || slides.length < 2) return; timer = setInterval(function () { show(cur + 1); }, reduce ? 8000 : 6000); }
    function go(n) { armed = true; show(n); start(); }
    dots.forEach(function (d) { d.addEventListener("click", function () { go(parseInt(d.dataset.go, 10)); }); });
    var prev = $("[data-hero-prev]", hero), next = $("[data-hero-next]", hero);
    if (prev) prev.addEventListener("click", function () { go(cur - 1); }); if (next) next.addEventListener("click", function () { go(cur + 1); });
    if (pauseBtn) pauseBtn.addEventListener("click", function () { paused = !paused; pauseBtn.setAttribute("aria-pressed", String(paused)); pauseBtn.textContent = paused ? "▶" : "❚❚"; pauseBtn.setAttribute("aria-label", paused ? "Play slideshow" : "Pause slideshow"); if (bar) bar.style.animationPlayState = paused ? "paused" : "running"; start(); });
    var sx = 0, sy = 0;
    hero.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
    hero.addEventListener("touchend", function (e) { var t = e.changedTouches[0], dx = t.clientX - sx, dy = t.clientY - sy; if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.4) go(cur + (dx < 0 ? 1 : -1)); }, { passive: true });
    document.addEventListener("visibilitychange", start);
    hero.addEventListener("pointermove", function (e) { if (reduce) return; var r = hero.getBoundingClientRect(); hero.style.setProperty("--px", ((e.clientX - r.left) / r.width - 0.5).toFixed(3)); hero.style.setProperty("--py", ((e.clientY - r.top) / r.height - 0.5).toFixed(3)); hero.style.setProperty("--gx", (((e.clientX - r.left) / r.width) * 100).toFixed(0) + "%"); hero.style.setProperty("--gy", (((e.clientY - r.top) / r.height) * 100).toFixed(0) + "%"); }, { passive: true });
    show(0, true);
    armT = setTimeout(arm, 15000);
    ["pointerdown", "touchstart", "keydown", "scroll", "wheel"].forEach(function (ev) { addEventListener(ev, arm, { once: true, passive: true }); });
  }

  /* ---------- card glow + tilt ---------- */
  if (fine && !reduce) {
    document.addEventListener("pointermove", function (e) {
      var c = e.target.closest && e.target.closest(".card"); if (!c) return;
      var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      c.style.setProperty("--rx", ((0.5 - y) * 6).toFixed(2) + "deg"); c.style.setProperty("--ry", ((x - 0.5) * 8).toFixed(2) + "deg");
    }, { passive: true });
    document.addEventListener("pointerout", function (e) { var c = e.target.closest && e.target.closest(".card"); if (c && !c.contains(e.relatedTarget)) { c.style.setProperty("--rx", "0deg"); c.style.setProperty("--ry", "0deg"); } });
  }

  /* ---------- scroll reveal for cards, image shimmer, magnetic buttons ---------- */
  function observeCards(cards) {
  if ("IntersectionObserver" in window && mo && Mo.inView) {
    /* Motion: cards spring up with a stagger across whatever batch scrolls into view together */
    var queue = [], raf = 0;
    var flush = function () {
      raf = 0;
      queue.splice(0).forEach(function (el, i) {
        var cim = el.querySelector(".ph img");
        if (cim) Mo.animate(cim, { scale: [1.12, 1] }, { duration: 1, ease: [0.2, 0.7, 0.2, 1], delay: Math.min(i, 7) * 0.06 });
        Mo.animate(el, { opacity: [0, 1], translate: ["0px 28px", "0px 0px"] }, { type: "spring", stiffness: 170, damping: 21, delay: Math.min(i, 7) * 0.06 })
          .finished.then(function () { el.classList.add("in"); el.style.opacity = ""; el.style.translate = ""; }, function () { el.classList.add("in"); });
      });
    };
    Mo.inView(cards, function (el) {
      if (el.motionSeen) return;
      el.motionSeen = true; queue.push(el);
      if (!raf) raf = requestAnimationFrame(flush);
    }, { margin: "0px 0px -6% 0px" });
  } else if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) { entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } }); }, { rootMargin: "0px 0px -6% 0px" });
    cards.forEach(function (c, i) { c.style.setProperty("--d", i % 6); io.observe(c); });
  } else { cards.forEach(function (c) { c.classList.add("in"); }); }
  }
  observeCards($$(".card"));

  function markLoaded(img) { var ph = img.closest(".ph"); if (ph) ph.classList.add("ld"); }
  $$(".ph img").forEach(function (img) { if (img.complete) markLoaded(img); });
  document.addEventListener("load", function (e) { if (e.target.tagName === "IMG") markLoaded(e.target); }, true);
  document.addEventListener("error", function (e) { if (e.target.tagName === "IMG") markLoaded(e.target); }, true);
  setTimeout(function () { $$(".ph:not(.ld)").forEach(function (p) { p.classList.add("ld"); }); }, 6000);

  if (fine && !reduce) {
    $$(".btn.primary, .cart-btn, .hero-actions .btn").forEach(function (b) { b.classList.add("magnet"); });
    document.addEventListener("pointermove", function (e) {
      $$(".magnet").forEach(function (el) {
        var r = el.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2, dx = e.clientX - cx, dy = e.clientY - cy, reach = Math.max(r.width, r.height) * 0.8;
        if (Math.hypot(dx, dy) < reach) el.style.translate = (dx * 0.16).toFixed(1) + "px " + (dy * 0.24).toFixed(1) + "px"; else if (el.style.translate) el.style.translate = "";
      });
    }, { passive: true });
  }
  /* ---------- homepage motion: hero parallax, feed and footer entrances, top bar drop-in, heading reveal ---------- */
  if (mo) {
    var heroEl = $("[data-hero]");
    if (heroEl) {
      var hp = 0, hraf = 0;
      var hpaint = function () {
        hraf = 0; var r = heroEl.getBoundingClientRect(), p = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height)));
        if (Math.abs(p - hp) > 0.002) { hp = p; heroEl.style.setProperty("--hp", p.toFixed(3)); }
      };
      addEventListener("scroll", function () { if (!hraf) hraf = requestAnimationFrame(hpaint); }, { passive: true });
      hpaint();
    }
    var bar = $("[data-topbar]");
    if (bar) enter(bar, { translate: "0px -100%", opacity: "0" }, { translate: ["0px -100%", "0px 0px"], opacity: 1 }, ["translate", "opacity"], 0.05, { stiffness: 190, damping: 24 });
    $$(".side.right .mini li").forEach(function (li, i) {
      enter(li, { opacity: "0", translate: "24px 0px" }, { opacity: 1, translate: ["24px 0px", "0px 0px"] }, ["opacity", "translate"], 0.55 + i * 0.06);
    });
    if (Mo.inView) {
      var fh = $(".feed-head");
      if (fh) Mo.inView(fh, function () { fh.classList.add("in"); enter($("h2", fh), { opacity: "0", translate: "0px 18px" }, { opacity: 1, translate: ["0px 18px", "0px 0px"] }, ["opacity", "translate"], 0, { stiffness: 150, damping: 20 }); });
      var foot = $(".site-foot");
      if (foot) Mo.inView(foot, function () {
        $$("li, .fine", foot).forEach(function (el, i) { enter(el, { opacity: "0", translate: "0px 12px" }, { opacity: 1, translate: ["0px 12px", "0px 0px"] }, ["opacity", "translate"], i * 0.05); });
      }, { margin: "0px 0px -8% 0px" });
    }
  }

  /* ---------- product page motion: info column, gallery, price and quantity ticks, add-to-cart pop, size guide, trust row ---------- */
  var pdpEl = $("[data-product]");
  if (mo && pdpEl) {
    $$(".buy.stagger > *").forEach(function (el, i) {
      enter(el, { opacity: "0", translate: "0px 22px" }, { opacity: 1, translate: ["0px 22px", "0px 0px"] }, ["opacity", "translate"], 0.1 + i * 0.07, { stiffness: 150, damping: 20 });
    });
    var pm = $("[data-main-image] img");
    if (pm) {
      Mo.animate(pm, { scale: [1.08, 1] }, { duration: 1.1, ease: [0.2, 0.7, 0.2, 1] });
      new MutationObserver(function () { Mo.animate(pm, { scale: [1.05, 1] }, { duration: 0.7, ease: [0.2, 0.7, 0.2, 1] }); }).observe(pm, { attributes: true, attributeFilter: ["src"] });
    }
    $$(".thumbs li").forEach(function (li, i) { enter(li, { opacity: "0", translate: "0px 14px" }, { opacity: 1, translate: ["0px 14px", "0px 0px"] }, ["opacity", "translate"], 0.35 + i * 0.05); });
    /* the price (and the sticky bar's price) nudge up when a different variant is chosen */
    [$("[data-price]"), $("[data-sticky-price]")].forEach(function (el) {
      if (!el) return;
      new MutationObserver(function () { Mo.animate(el, { opacity: [0.25, 1], translate: ["0px 10px", "0px 0px"] }, { type: "spring", stiffness: 260, damping: 22 }); }).observe(el, { childList: true, characterData: true, subtree: true });
    });
    /* the quantity number rolls up or down */
    var qo = $("[data-qty-out]");
    if (qo) {
      var lastQ = parseInt(qo.textContent, 10) || 1;
      new MutationObserver(function () {
        var n = parseInt(qo.textContent, 10) || lastQ, dir = n >= lastQ ? 1 : -1; lastQ = n;
        Mo.animate(qo, { opacity: [0.2, 1], translate: ["0px " + dir * 10 + "px", "0px 0px"] }, { type: "spring", stiffness: 420, damping: 24 });
      }).observe(qo, { childList: true, characterData: true, subtree: true });
    }
    /* add to cart: the button pops when it turns to "Added" */
    var ab = $("[data-add]");
    if (ab) {
      var wasOk = false;
      new MutationObserver(function () {
        var ok = ab.classList.contains("is-ok"); if (ok && !wasOk) Mo.animate(ab, { scale: 1.07 }, { duration: 0.12, ease: "easeOut" }).finished.then(function () { Mo.animate(ab, { scale: 1 }, { type: "spring", stiffness: 380, damping: 13 }); });
        wasOk = ok;
      }).observe(ab, { attributes: true, attributeFilter: ["class"] });
    }
    /* size guide: its contents ease in when it opens */
    $$(".size-guide").forEach(function (d) {
      d.addEventListener("toggle", function () {
        if (!d.open) return; var body = $(".sg-body", d); if (body) Mo.animate(body, { opacity: [0, 1], translate: ["0px -10px", "0px 0px"] }, { type: "spring", stiffness: 240, damping: 24 });
      });
    });
    /* trust row, reviews and the recently viewed row spring in as they scroll into view */
    if (Mo.inView) {
      var trust = $$(".trust-list li");
      if (trust.length) { trust.forEach(function (el) { el.style.opacity = "0"; }); Mo.inView(".trust-list", function () { trust.forEach(function (el, i) { enter(el, { opacity: "0", translate: "0px 16px" }, { opacity: 1, translate: ["0px 16px", "0px 0px"] }, ["opacity", "translate"], i * 0.08); }); }, { margin: "0px 0px -8% 0px" }); }
      var rvw = $("[data-reviews]");
      if (rvw) { rvw.style.opacity = "0"; Mo.inView(rvw, function () { enter(rvw, { opacity: "0", translate: "0px 18px" }, { opacity: 1, translate: ["0px 18px", "0px 0px"] }, ["opacity", "translate"], 0); }, { margin: "0px 0px -6% 0px" }); }
    }
    var recRow = $("[data-recent-row]");
    if (recRow) new MutationObserver(function () {
      if (recRow.dataset.in) return; recRow.dataset.in = "1";
      Array.prototype.slice.call(recRow.children).forEach(function (el, i) { enter(el, { opacity: "0", translate: "0px 14px" }, { opacity: 1, translate: ["0px 14px", "0px 0px"] }, ["opacity", "translate"], i * 0.06); });
    }).observe(recRow, { childList: true });
  }

  /* ---------- collection, rooms and search pages: heading words rise, accent bar draws, sort bar and pager spring in ---------- */
  var pgHead = $(".page-head");
  if (mo && pgHead) {
    var pgH1 = $("h1", pgHead);
    if (pgH1 && !pgH1.children.length && pgH1.textContent.trim().length < 90) {
      var pgTxt = pgH1.textContent.trim().replace(/\s+/g, " "), words = pgTxt.split(" "), srSpan = document.createElement("span");
      pgH1.textContent = ""; srSpan.className = "sr-only"; srSpan.textContent = pgTxt; pgH1.appendChild(srSpan);
      words.forEach(function (w, i) {
        var outer = document.createElement("span"), inner = document.createElement("span");
        outer.className = "w"; outer.setAttribute("aria-hidden", "true"); inner.textContent = w; outer.appendChild(inner); pgH1.appendChild(outer);
        if (i < words.length - 1) pgH1.appendChild(document.createTextNode(" "));
        enter(inner, { translate: "0px 115%" }, { translate: ["0px 115%", "0px 0px"] }, ["translate"], 0.05 + i * 0.07, { stiffness: 170, damping: 20 });
      });
      pgHead.style.setProperty("--ul", "0");
      Mo.animate(pgHead, { "--ul": 1 }, { duration: 0.9, ease: [0.2, 0.7, 0.2, 1], delay: 0.25 });
    }
    [$(".prose", pgHead), $(".sortbar", pgHead)].forEach(function (el, i) {
      if (el) enter(el, { opacity: "0", translate: "0px 14px" }, { opacity: 1, translate: ["0px 14px", "0px 0px"] }, ["opacity", "translate"], 0.3 + i * 0.1);
    });
    var emptySt = $(".empty-state"); if (emptySt) enter(emptySt, { opacity: "0", translate: "0px 18px" }, { opacity: 1, translate: ["0px 18px", "0px 0px"] }, ["opacity", "translate"], 0.3);
    var pagerEl = $(".pager");
    if (pagerEl && Mo.inView) {
      var pgKids = Array.prototype.slice.call(pagerEl.children); pgKids.forEach(function (el) { el.style.opacity = "0"; });
      Mo.inView(pagerEl, function () { pgKids.forEach(function (el, i) { enter(el, { opacity: "0", translate: "0px 14px" }, { opacity: 1, translate: ["0px 14px", "0px 0px"] }, ["opacity", "translate"], i * 0.05); }); }, { margin: "0px 0px -6% 0px" });
    }
  }

  /* ---------- secure checkout strip: top line draws, lock pops and glows, icons pop in then catch a sheen, facts slide up ---------- */
  $$(".co-strip").forEach(function (strip) {
    if (!mo || !Mo.inView) return;
    var icons = $$(".co-pay li", strip), lock = $(".co-secure svg", strip), word = $(".co-secure span", strip), facts = $$(".co-facts li", strip);
    strip.style.setProperty("--ul", "0");
    icons.concat(facts).forEach(function (el) { el.style.opacity = "0"; });
    if (word) word.style.opacity = "0";
    Mo.inView(strip, function () {
      Mo.animate(strip, { "--ul": 1 }, { duration: 0.8, ease: [0.2, 0.7, 0.2, 1] });
      if (lock) { enter(lock, { scale: "0.3", rotate: "-25deg" }, { scale: [0.3, 1], rotate: [-25, 0] }, ["scale", "rotate"], 0.1, { stiffness: 320, damping: 12 }); strip.classList.add("lit"); }
      if (word) enter(word, { opacity: "0", translate: "-8px 0px" }, { opacity: 1, translate: ["-8px 0px", "0px 0px"] }, ["opacity", "translate"], 0.2);
      icons.forEach(function (el, i) {
        enter(el, { opacity: "0", scale: "0.5", rotate: "-8deg" }, { opacity: 1, scale: [0.5, 1], rotate: [-8, 0] }, ["opacity", "scale", "rotate"], 0.3 + i * 0.06, { stiffness: 320, damping: 15 });
        Mo.animate(el, { "--sh": [-120, 120] }, { duration: 0.8, delay: 0.9 + i * 0.1, ease: "easeInOut" });
      });
      facts.forEach(function (el, i) { enter(el, { opacity: "0", translate: "0px 10px" }, { opacity: 1, translate: ["0px 10px", "0px 0px"] }, ["opacity", "translate"], 0.55 + icons.length * 0.04 + i * 0.12); });
    }, { margin: "0px 0px -4% 0px" });
  });

  /* ---------- 404 page: digits drop in, the magnifier drifts looking around, search box and button spring up ---------- */
  var nf = $(".nf");
  if (mo && nf) {
    $$(".nf-d", nf).forEach(function (d, i) { enter(d, { opacity: "0", translate: "0px -60px", rotate: String(i === 1 ? 0 : (i ? 8 : -8)) }, { opacity: 1, translate: ["0px -60px", "0px 0px"], rotate: [i === 1 ? 0 : (i ? 8 : -8), 0] }, ["opacity", "translate", "rotate"], 0.05 + i * 0.12, { stiffness: 150, damping: 11 }); });
    var nfIco = $(".nf-o svg", nf);
    if (nfIco) Mo.animate(nfIco, { translate: ["-10px -6px", "10px 6px"], rotate: [-12, 12] }, { duration: 2.2, repeat: Infinity, repeatType: "reverse", ease: "easeInOut", delay: 0.9 });
    [$(".nf-search", nf), $(".nf-go", nf)].forEach(function (el, i) { if (el) enter(el, { opacity: "0", translate: "0px 16px" }, { opacity: 1, translate: ["0px 16px", "0px 0px"] }, ["opacity", "translate"], 0.55 + i * 0.1); });
    var nfIn = $(".nf-search input", nf);
    if (nfIn) {
      nfIn.addEventListener("focus", function () { Mo.animate(nfIn, { scale: 1.03 }, { type: "spring", stiffness: 380, damping: 20 }); });
      nfIn.addEventListener("blur", function () { Mo.animate(nfIn, { scale: 1 }, { type: "spring", stiffness: 380, damping: 24 }); });
    }
    /* the digits lean toward the pointer */
    var nfCode = $(".nf-code", nf);
    if (nfCode && window.matchMedia("(hover: hover)").matches) window.addEventListener("pointermove", function (e) {
      var x = (e.clientX / window.innerWidth - 0.5) * 2, y = (e.clientY / window.innerHeight - 0.5) * 2;
      Mo.animate(nfCode, { "--nx": x * 10 + "px", "--ny": y * 6 + "px" }, { type: "spring", stiffness: 90, damping: 18 });
    }, { passive: true });
  }

  /* ---------- search page: result count rolls up, the searched words are highlighted, empty state icon bobs ---------- */
  function searchEnter() {
  var srchLine = $(".srch-line");
  if (mo && srchLine) {
    var cntEl = $("[data-count]", srchLine), cntTo = parseInt(cntEl && cntEl.textContent, 10);
    if (cntEl && cntTo > 0) Mo.animate(0, cntTo, { duration: Math.min(1.2, 0.4 + cntTo * 0.02), ease: [0.2, 0.7, 0.2, 1], delay: 0.3, onUpdate: function (v) { cntEl.textContent = Math.round(v); } }).finished.then(function () { cntEl.textContent = cntTo; });
    var qEl = $("[data-q]", srchLine);
    if (qEl) { qEl.style.setProperty("--qu", "0"); Mo.animate(qEl, { "--qu": 1 }, { duration: 0.8, ease: [0.2, 0.7, 0.2, 1], delay: 0.6 }); }
    /* highlight the searched words inside the product names, with a marker sweep */
    var words = (qEl ? qEl.textContent : "").toLowerCase().split(/\s+/).filter(function (w) { return w.length > 1; }).slice(0, 5);
    if (words.length) {
      var rx = new RegExp("(" + words.map(function (w) { return w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }).join("|") + ")", "ig");
      $$(".card .t").forEach(function (t) {
        var txt = t.textContent; if (!rx.test(txt)) { rx.lastIndex = 0; return; } rx.lastIndex = 0;
        var frag = document.createDocumentFragment();
        txt.split(rx).forEach(function (part, i) { if (i % 2) { var m = document.createElement("mark"); m.textContent = part; frag.appendChild(m); } else if (part) frag.appendChild(document.createTextNode(part)); });
        t.textContent = ""; t.appendChild(frag);
      });
      requestAnimationFrame(function () { $$(".card .t mark").forEach(function (m, i) { setTimeout(function () { m.classList.add("on"); }, 500 + Math.min(i, 12) * 60); }); });
    }
  }
  var srchIco = $(".srch-ico");
  if (mo && srchIco) Mo.animate(srchIco, { translate: ["0px -6px", "0px 6px"], rotate: [-6, 6] }, { duration: 1.6, repeat: Infinity, repeatType: "reverse", ease: "easeInOut" });
  }
  searchEnter();
  /* the sidebar search box lifts a little when focused */
  var srchIn = $(".side .search input");
  if (mo && srchIn) {
    srchIn.addEventListener("focus", function () { Mo.animate(srchIn, { scale: 1.03 }, { type: "spring", stiffness: 380, damping: 20 }); });
    srchIn.addEventListener("blur", function () { Mo.animate(srchIn, { scale: 1 }, { type: "spring", stiffness: 380, damping: 24 }); });
  }

  /* ---------- live search: only the results container is replaced, clearing the box brings back the default look ---------- */
  var sForm = $(".side .search"), sIn = sForm && $("input[name=q]", sForm), sMain = $("#main");
  if (sForm && sIn && sMain && window.fetch && window.DOMParser && history.pushState && window.AbortController) {
    var isSearchPath = function () { return /\/search\/?$/.test(location.pathname); };
    var onSearch = isSearchPath(), sSort = ($("#sort_by", sMain) || {}).value || "relevance", sCtl = null, sTimer = 0, sLast = onSearch ? sIn.value.trim() : null, sHref = location.href.split("#")[0];
    var sUrl = function (q) { return sForm.action.split("?")[0] + (q ? "?q=" + encodeURIComponent(q) + "&type=product" + (sSort && sSort !== "relevance" ? "&sort_by=" + encodeURIComponent(sSort) : "") : ""); };
    var swapIn = function (html, url, how, top) {
      var doc = new DOMParser().parseFromString(html, "text/html"), nMain = doc.querySelector("#main");
      if (!nMain) { location.href = url; return; }
      var cur = $(".shopify-section", sMain), nxt = $(".shopify-section", nMain);
      if (cur && nxt && cur.id === nxt.id) cur.innerHTML = nxt.innerHTML; else sMain.innerHTML = nMain.innerHTML;
      if (how === "push") history.pushState({ ls: 1 }, "", url); else history.replaceState({ ls: 1 }, "", url);
      sHref = location.href.split("#")[0];
      document.title = doc.title; onSearch = true;
      $$(".ph img", sMain).forEach(function (img) { if (img.complete) markLoaded(img); });
      observeCards($$(".card", sMain)); searchEnter();
      sMain.removeAttribute("aria-busy"); sForm.removeAttribute("data-busy");
      if (top) window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
    };
    var runSearch = function (q, top) {
      clearTimeout(sTimer); if (sCtl) sCtl.abort(); sCtl = new AbortController();
      sLast = q; sMain.setAttribute("aria-busy", "true"); sForm.setAttribute("data-busy", "");
      var url = sUrl(q), how = isSearchPath() ? "replace" : "push";
      fetch(url, { signal: sCtl.signal, credentials: "same-origin" })
        .then(function (r) { if (!r.ok) throw new Error("search " + r.status); return r.text(); })
        .then(function (html) { swapIn(html, url, how, top); })
        .catch(function (e) { if (e && e.name === "AbortError") return; location.href = url; });
    };
    /* landing on the search page (e.g. from the footer Search link): put the cursor in the search box and flag it */
    if (isSearchPath() && !sIn.value.trim()) {
      try { sIn.focus({ preventScroll: true }); } catch (err) { sIn.focus(); }
      sForm.classList.add("hint");
      sIn.addEventListener("input", function () { sForm.classList.remove("hint"); }, { once: true });
    }
    sForm.addEventListener("submit", function (e) { e.preventDefault(); runSearch(sIn.value.trim(), !onSearch); });
    /* the sort menu inside the results: re-runs the same search with the chosen order */
    sMain.addEventListener("change", function (e) {
      var sel = e.target.closest && e.target.closest("select[name=sort_by]"); if (!sel || !sel.closest(".sortbar") || !isSearchPath()) return; /* collection pages sort through their own form (onchange submit); handling it here too made the two fight */
      sSort = sel.value; runSearch(sIn.value.trim() || ($("[data-q]", sMain) || {}).textContent || "", false);
    });
    sIn.addEventListener("input", function () {
      if (!onSearch) return;
      var q = sIn.value.trim(); clearTimeout(sTimer);
      if (q === sLast || (q && q.length < 2)) return;
      sTimer = setTimeout(function () { runSearch(q, false); }, q ? 320 : 0);
    });
    window.addEventListener("popstate", function () { if (location.href.split("#")[0] !== sHref) location.reload(); });
  } else {
    document.addEventListener("change", function (e) { var sel = e.target.closest && e.target.closest(".sortbar select"); if (sel && sel.form && !sel.hasAttribute("onchange")) sel.form.submit(); });
  }

  /* press feedback: a quick spring squash on buttons, chips and thumbnails (delegated, so it also covers the cart drawer and quick view) */
  if (mo) {
    var PRESS = ".btn, .cart-btn, .to-top, .up-add, .search-go, .chipb span, .thumbs button, .hero-dots button, [data-hero-prev], [data-hero-next], .q button";
    var held = null;
    var release = function () { if (!held) return; var el = held; held = null; Mo.animate(el, { scale: 1 }, { type: "spring", stiffness: 520, damping: 14 }); };
    document.addEventListener("pointerdown", function (e) {
      var el = e.target.closest && e.target.closest(PRESS);
      if (!el || el.disabled || el.getAttribute("aria-disabled") === "true") return;
      held = el; Mo.animate(el, { scale: 0.94 }, { type: "spring", stiffness: 700, damping: 28 });
    }, { passive: true });
    ["pointerup", "pointercancel", "dragend"].forEach(function (t) { document.addEventListener(t, release, { passive: true }); });
  }
  /* back to top: appears once the visitor has scrolled well past the first screen */
  var toTop = $("[data-to-top]");
  if (toTop) {
    var tt = false, ttShow = false;
    var ttCheck = function () {
      tt = false; var on = (window.scrollY || document.documentElement.scrollTop) > window.innerHeight * 0.8;
      if (on === ttShow) return; ttShow = on; toTop.classList.toggle("show", on);
      toTop.tabIndex = on ? 0 : -1; if (on) toTop.removeAttribute("aria-hidden"); else toTop.setAttribute("aria-hidden", "true");
    };
    addEventListener("scroll", function () { if (!tt) { tt = true; requestAnimationFrame(ttCheck); } }, { passive: true });
    ttCheck();
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
      var m = $("#main"); if (m) { m.tabIndex = -1; m.focus({ preventScroll: true }); }
    });
  }

  /* reviews: if Judge.me's script never drew its widget, say so instead of leaving a blank block */
  var rv = $("[data-reviews]");
  if (rv) {
    var wbtn = $("[data-write-review]", rv);
    var jmLink = function () { return $(".jdgm-write-rev-link", rv) || $(".jdgm-write-rev-link"); };
    var reveal = function () { if (wbtn && jmLink()) wbtn.hidden = false; };
    if (wbtn) {
      wbtn.addEventListener("click", function () {
        var l = jmLink(); if (!l) return; l.click();
        setTimeout(function () { var f = $(".jdgm-form-wrapper, .jdgm-form", rv); if (f) f.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "center" }); }, 250);
      });
      addEventListener("load", function () { reveal(); setTimeout(reveal, 1500); setTimeout(reveal, 4000); });
    }
  }
  /* the empty-state message shows whenever the page holds no real review and no review form (Judge.me can leave an empty wrapper div, so counting children is not enough) */
  if (rv) addEventListener("load", function () { setTimeout(function () { var note = $("[data-reviews-soon]", rv); if (note && !$(".jdgm-rev, .jdgm-form, .jdgm-write-rev-link", rv)) { note.hidden = false; } }, 3500); });
  /* homepage feed: sort the products shown (collection and search pages sort on the server) */
  var homeSort = $("[data-home-sort]"), homeFeed = $("#feed");
  if (homeSort && homeFeed) {
    var homeCells = $$(".cell", homeFeed);
    homeCells.forEach(function (c, i) { c.setAttribute("data-i", i); });
    var num = function (el, k) { return Number(el.getAttribute("data-" + k)) || 0; };
    var homeBy = {
      featured: function (a, b) { return num(a, "i") - num(b, "i"); },
      "new": function (a, b) { return num(b, "new") - num(a, "new"); },
      price_asc: function (a, b) { return num(a, "price") - num(b, "price"); },
      price_desc: function (a, b) { return num(b, "price") - num(a, "price"); },
      az: function (a, b) { return a.getAttribute("data-title").localeCompare(b.getAttribute("data-title")); },
      za: function (a, b) { return b.getAttribute("data-title").localeCompare(a.getAttribute("data-title")); }
    };
    homeSort.addEventListener("change", function () {
      homeCells.slice().sort(homeBy[homeSort.value] || homeBy.featured).forEach(function (c) { homeFeed.appendChild(c); });
    });
  }
  document.addEventListener("error", function (e) { if (e.target.tagName === "IMG") e.target.style.visibility = "hidden"; }, true);
})();
