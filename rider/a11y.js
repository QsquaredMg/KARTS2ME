/* Karts2Me accessibility layer (WCAG 2.1 AA). Runs after render, observes DOM changes. */
(function () {
  "use strict";
  var css = [
    ":focus-visible{outline:3px solid #1a73e8 !important;outline-offset:2px !important;}",
    ".k2-skip{position:absolute;left:-9999px;top:8px;background:#000;color:#fff;padding:10px 14px;border-radius:8px;z-index:100000;font:600 14px system-ui,sans-serif;}",
    ".k2-skip:focus{left:8px;}",
    ".k2-sr{position:absolute !important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;}",
    "button,[role=button],a,select,input[type=checkbox],input[type=radio]{min-height:24px;}",
    "@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms !important;animation-iteration-count:1 !important;transition-duration:.01ms !important;scroll-behavior:auto !important;}}"
  ].join("\n");
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  var uid = 0;
  function txt(el) { return (el.textContent || "").replace(/\s+/g, " ").trim(); }

  function fixImages(root) {
    root.querySelectorAll("img:not([alt])").forEach(function (img) {
      var src = (img.getAttribute("src") || "").toLowerCase();
      var label = img.getAttribute("title") || img.getAttribute("data-alt");
      if (!label) {
        if (src.indexOf("logo") > -1) label = "Karts2Me logo";
        else if (img.closest("button,a")) label = "";
        else label = "Photo";
      }
      img.setAttribute("alt", label);
    });
  }

  function fixButtons(root) {
    root.querySelectorAll("button,[role=button],a[href]").forEach(function (b) {
      if (b.hasAttribute("aria-label") || b.hasAttribute("aria-labelledby")) return;
      if (txt(b).replace(/[^\w]/g, "").length > 0) return;
      var img = b.querySelector("img[alt]:not([alt=''])");
      var label = b.getAttribute("title") || (img && img.alt) ||
        (b.id === "modalCloseBtn" || b.classList.contains("modal-close") ? "Close dialog" : "");
      if (!label) {
        var t = txt(b);
        if (/^[×✕xX✖]$/.test(t)) label = "Close";
        else if (t === "☰") label = "Menu";
        else if (t === "←" || t === "‹") label = "Back";
      }
      if (label) b.setAttribute("aria-label", label);
    });
  }

  function fixClickables(root) {
    root.querySelectorAll("[onclick]:not(button):not(a):not(input):not(select):not(textarea):not([role])").forEach(function (el) {
      el.setAttribute("role", "button");
      if (!el.hasAttribute("tabindex")) el.setAttribute("tabindex", "0");
    });
  }

  function fixLabels(root) {
    // Associate <label> with the next form control when not already linked.
    root.querySelectorAll("label:not([for])").forEach(function (lb) {
      if (lb.querySelector("input,select,textarea")) return;
      var ctl = lb.nextElementSibling;
      while (ctl && !/^(INPUT|SELECT|TEXTAREA)$/.test(ctl.tagName)) {
        var inner = ctl.querySelector && ctl.querySelector("input,select,textarea");
        if (inner) { ctl = inner; break; }
        ctl = ctl.nextElementSibling; if (!ctl) break;
        if (ctl && ctl.tagName === "LABEL") { ctl = null; break; }
      }
      if (ctl) {
        if (!ctl.id) ctl.id = "k2f" + (++uid);
        lb.setAttribute("for", ctl.id);
      }
    });
    // Unlabelled controls: fall back to placeholder / name / title.
    root.querySelectorAll("input:not([type=hidden]):not([type=checkbox]):not([type=radio]),select,textarea").forEach(function (c) {
      if (c.hasAttribute("aria-label") || c.hasAttribute("aria-labelledby")) return;
      if (c.id && root.querySelector('label[for="' + c.id + '"]')) return;
      if (c.closest("label")) return;
      var l = c.getAttribute("placeholder") || c.getAttribute("title") || c.getAttribute("name") || c.id;
      if (l) c.setAttribute("aria-label", l.replace(/[_-]/g, " "));
    });
    root.querySelectorAll("input[type=checkbox],input[type=radio]").forEach(function (c) {
      if (c.hasAttribute("aria-label") || c.closest("label")) return;
      if (c.id && root.querySelector('label[for="' + c.id + '"]')) return;
      var sib = c.nextElementSibling || c.parentElement;
      var l = sib && txt(sib);
      if (l) c.setAttribute("aria-label", l.slice(0, 80));
    });
    root.querySelectorAll("input[required],select[required],textarea[required]").forEach(function (c) {
      c.setAttribute("aria-required", "true");
    });
  }

  function fixLandmarks() {
    var host = document.getElementById("root") || document.querySelector(".app") || document.body;
    if (!document.querySelector("main,[role=main]") && host && host !== document.body) {
      host.setAttribute("role", "main");
      if (!host.id) host.id = "k2main";
    }
    if (!document.querySelector(".k2-skip") && host) {
      var a = document.createElement("a");
      a.className = "k2-skip"; a.href = "#" + host.id; a.textContent = "Skip to main content";
      a.addEventListener("click", function () { host.setAttribute("tabindex", "-1"); host.focus(); });
      document.body.insertBefore(a, document.body.firstChild);
    }
    var toast = document.querySelector("#toast,.toast");
    if (toast && !toast.getAttribute("role")) { toast.setAttribute("role", "status"); toast.setAttribute("aria-live", "polite"); }
  }

  // ---- Modal: role=dialog, focus trap, Escape, focus restore ----
  var lastFocus = null, wasOpen = false;
  function modalEls() { return { back: document.getElementById("modalBackdrop"), box: document.getElementById("modal") }; }
  function isOpen(m) { return m.back && !m.back.classList.contains("hidden") && m.back.offsetParent !== null; }
  function focusables(box) {
    return Array.prototype.filter.call(box.querySelectorAll('a[href],button:not([disabled]),input:not([disabled]):not([type=hidden]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])'), function (e) { return e.offsetParent !== null; });
  }
  function syncModal() {
    var m = modalEls(); if (!m.box) return;
    m.box.setAttribute("role", "dialog"); m.box.setAttribute("aria-modal", "true");
    var h = m.box.querySelector("h1,h2,h3,.modal-head");
    if (h) { if (!h.id) h.id = "k2mt"; m.box.setAttribute("aria-labelledby", h.id); }
    var open = isOpen(m);
    if (open && !wasOpen) {
      lastFocus = document.activeElement;
      var f = focusables(m.box);
      var first = m.box.querySelector("input:not([type=hidden]),select,textarea") || f[0];
      if (first) setTimeout(function () { first.focus(); }, 30);
    } else if (!open && wasOpen && lastFocus && lastFocus.focus) {
      try { lastFocus.focus(); } catch (e) {}
    }
    wasOpen = open;
  }
  document.addEventListener("keydown", function (e) {
    var m = modalEls();
    if (m.back && isOpen(m)) {
      if (e.key === "Escape") {
        var x = m.box.querySelector("#modalCloseBtn,.modal-close");
        if (x) { e.preventDefault(); x.click(); } else if (typeof window.closeModal === "function") window.closeModal();
        return;
      }
      if (e.key === "Tab") {
        var f = focusables(m.box); if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && (document.activeElement === first || !m.box.contains(document.activeElement))) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && (document.activeElement === last || !m.box.contains(document.activeElement))) { e.preventDefault(); first.focus(); }
      }
    }
    // Keyboard activation for role=button non-native elements
    if ((e.key === "Enter" || e.key === " ") && e.target && e.target.getAttribute && e.target.getAttribute("role") === "button" && !/^(BUTTON|A|INPUT)$/.test(e.target.tagName)) {
      e.preventDefault(); e.target.click();
    }
  }, true);

  var pending = false;
  function run() {
    pending = false;
    try { fixImages(document); fixButtons(document); fixClickables(document); fixLabels(document); fixLandmarks(); syncModal(); } catch (e) {}
  }
  function schedule() { if (!pending) { pending = true; (window.requestAnimationFrame || setTimeout)(run); } }
  new MutationObserver(schedule).observe(document.documentElement, { childList: true, subtree: true, attributes: true, attributeFilter: ["class"] });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run); else run();
})();
