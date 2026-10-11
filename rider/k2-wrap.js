/* Karts2Me universal wrapper: brand mark + cross-app switcher + path back to the home site. */
(function () {
  "use strict";
  var APP = document.documentElement.getAttribute("data-k2-app") || "";
  var HOME = "https://www.karts2me.com";
  var native = !!(window.Capacitor && window.Capacitor.isNativePlatform && window.Capacitor.isNativePlatform());
  var ICONS = {
    home: '<path d="M3 11.5 12 4l9 7.5"/><path d="M5 10v10h5v-6h4v6h5V10"/>',
    ride: '<path d="M5 17h14"/><path d="M6 17V9h12v8"/><path d="M4 9h16"/><circle cx="8" cy="19" r="1.6"/><circle cx="16" cy="19" r="1.6"/><path d="M8 9V5h8v4"/>',
    drive: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.4"/><path d="M12 3v6.6M3.6 14.5l6.2-1.7M20.4 14.5l-6.2-1.7"/>',
    operate: '<rect x="3" y="3" width="7.5" height="7.5" rx="2"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="2"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="2"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="2"/>',
    admin: '<path d="M12 3 4 6v6c0 4.5 3.4 8 8 9 4.6-1 8-4.5 8-9V6z"/><path d="m9 12 2 2 4-4"/>'
  };
  function svg(k) { return '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[k] + "</svg>"; }

  var ENTRIES = [
    { id: "home", t: "Karts2Me home", d: "Overview of the platform", href: HOME, show: true },
    { id: "rider", k: "ride", t: "Ride", d: "Book a cart or shuttle", href: "https://ride.karts2me.com", show: !native || APP === "rider" },
    { id: "driver", k: "drive", t: "Drive", d: "Earn on property fleets", href: "https://driver.karts2me.com", show: !native || APP === "driver" },
    { id: "operator", k: "operate", t: "Operate", d: "Run your property's fleet", href: "https://operator.karts2me.com", show: (!native || APP === "operator") && APP !== "admin" },
    { id: "admin", k: "admin", t: "Platform admin", d: "Karts2Me staff console", href: "https://admin.karts2me.com", show: APP === "admin" }
  ];

  // 1) Crisp brand mark everywhere our own logo raster was used (never touch operator-uploaded media).
  function swapLogos() {
    document.querySelectorAll("img").forEach(function (im) {
      var s = im.getAttribute("src") || "";
      if (/^(\/)?(logo\.png|icon-512\.png|icon-192\.png)$/.test(s) && !im.dataset.k2) {
        im.dataset.k2 = "1"; im.setAttribute("src", "/k2-mark.svg");
      }
    });
  }

  // 2) Switcher dialog
  var back, lastFocus;
  function build() {
    back = document.createElement("div");
    back.className = "k2-sw-back"; back.hidden = true;
    var items = ENTRIES.filter(function (e) { return e.show; }).map(function (e) {
      var cur = e.id === APP ? ' aria-current="page"' : "";
      return '<a href="' + e.href + '"' + cur + '><span class="ico">' + svg(e.k || e.id) + '</span><span><span class="t">' + e.t + '</span><span class="d">' + e.d + "</span></span></a>";
    }).join("");
    back.innerHTML = '<div class="k2-sw" role="dialog" aria-modal="true" aria-label="Karts2Me apps"><h2>Karts2Me</h2>' + items +
      '<div class="foot"><a href="' + HOME + '/privacy">Privacy</a><a href="mailto:support@karts2me.com">Support</a></div></div>';
    document.body.appendChild(back);
    back.addEventListener("click", function (e) { if (e.target === back) close(); });
    document.addEventListener("keydown", function (e) {
      if (!back.hidden && e.key === "Escape") { close(); }
      else if (!back.hidden && e.key === "Tab") {
        var f = back.querySelectorAll("a"); if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }
  function open() { if (!back) build(); lastFocus = document.activeElement; back.hidden = false; var a = back.querySelector("a[aria-current],a"); if (a) a.focus(); }
  function close() { if (back) back.hidden = true; if (lastFocus && lastFocus.focus) try { lastFocus.focus(); } catch (e) {} }

  // 3) Launchers
  function wireLaunchers() {
    // phone apps: replace the passive logo badge with a launcher button
    var badge = document.querySelector(".app-logo-badge");
    if (badge && !document.querySelector(".k2-launch")) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "k2-launch"; b.setAttribute("aria-label", "Karts2Me apps and home");
      b.innerHTML = '<img src="/k2-mark.svg" alt="">';
      badge.parentNode.insertBefore(b, badge); badge.style.display = "none";
      b.addEventListener("click", open);
    }
    // consoles: sidebar logo row
    document.querySelectorAll(".logo-row:not([data-k2])").forEach(function (r) {
      r.dataset.k2 = "1"; r.setAttribute("role", "button"); r.setAttribute("tabindex", "0"); r.setAttribute("aria-label", "Karts2Me apps and home");
      r.addEventListener("click", open);
      r.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } });
    });
    // auth boxes: path back to the home site
    document.querySelectorAll(".authbox:not([data-k2h])").forEach(function (a) {
      a.dataset.k2h = "1";
      var l = document.createElement("a"); l.className = "k2-home-link"; l.href = HOME; l.textContent = "← karts2me.com";
      a.appendChild(l);
    });
  }

  var pend = false;
  function tick() { pend = false; swapLogos(); wireLaunchers(); }
  function sched() { if (!pend) { pend = true; (window.requestAnimationFrame || setTimeout)(tick); } }
  new MutationObserver(sched).observe(document.documentElement, { childList: true, subtree: true });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", tick); else tick();
  window.K2 = window.K2 || {}; window.K2.openSwitcher = open;
})();
