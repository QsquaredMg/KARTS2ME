/* Karts2Me app shell: native polish layer + in-app account deletion.
   Works in the browser/PWA and inside the Capacitor wrapper. Safe to load before the app script. */
(function(){
  var C = window.Capacitor, native = !!(C && C.isNativePlatform && C.isNativePlatform());
  var plat = native ? C.getPlatform() : "web";
  var root = document.documentElement;
  root.classList.add(native ? "k2-native" : "k2-web", "k2-" + plat);
  window.K2M_WEB_ORIGIN = location.origin;

  /* ---- styles ---- */
  var css = [
    "html{-webkit-text-size-adjust:100%;}",
    "body{-webkit-tap-highlight-color:transparent;-webkit-touch-callout:none;overscroll-behavior-y:none;}",
    "button,[role=button],.card{-webkit-user-select:none;user-select:none;touch-action:manipulation;}",
    "input,textarea{-webkit-user-select:text;user-select:text;font-size:16px !important;}", /* stops iOS zoom-on-focus */
    "button{transition:transform .12s ease,opacity .12s ease,box-shadow .2s ease;}",
    "button:active:not(:disabled){transform:scale(.96);opacity:.9;}",
    ".card{transition:transform .15s ease,box-shadow .2s ease;}",
    "#screen>*{animation:k2in .28s cubic-bezier(.2,.7,.2,1);}",
    "@keyframes k2in{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:none;}}",
    ".modal{animation:k2pop .22s cubic-bezier(.2,.8,.2,1);}",
    "@keyframes k2pop{from{opacity:0;transform:scale(.94) translateY(10px);}to{opacity:1;transform:none;}}",
    ".sheet{animation:k2up .3s cubic-bezier(.2,.8,.2,1);}",
    "@keyframes k2up{from{transform:translateY(40px);opacity:0;}to{transform:none;opacity:1;}}",
    ".k2-native .phone{max-width:none;border-radius:0 !important;box-shadow:none !important;min-height:100dvh !important;}",
    ".k2-native body{padding:0 !important;background:var(--cream,#FAF8F3);}",
    ".k2-native .app-logo-badge{display:none;}",
    ".k2-native .screen{padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom);}",
    ".k2-native [style*='padding:48px 20px']{padding-top:20px !important;}",
    ".k2-native .topbar{padding-top:20px !important;}",
    "#k2-splash{position:fixed;inset:0;z-index:9999;background:linear-gradient(160deg,#073876,#0a4a9c);display:flex;flex-direction:column;align-items:center;justify-content:center;transition:opacity .45s ease,visibility .45s;}",
    "#k2-splash.k2-off{opacity:0;visibility:hidden;}",
    "#k2-splash img{width:96px;height:96px;border-radius:24px;box-shadow:0 12px 40px rgba(0,0,0,.35);animation:k2bounce 1.4s ease-in-out infinite;}",
    "#k2-splash p{color:#fff;font:600 20px/1 Inter,system-ui,sans-serif;margin:18px 0 0;letter-spacing:.02em;}",
    "@keyframes k2bounce{0%,100%{transform:translateY(0);}50%{transform:translateY(-8px);}}",
    "#k2-toast{position:fixed;left:50%;bottom:calc(24px + env(safe-area-inset-bottom));transform:translate(-50%,80px);background:#073876;color:#fff;padding:10px 16px;border-radius:99px;font:600 13px Inter,system-ui,sans-serif;z-index:9000;transition:transform .3s cubic-bezier(.2,.8,.2,1);box-shadow:0 8px 24px rgba(0,0,0,.25);max-width:90vw;}",
    "#k2-toast.k2-show{transform:translate(-50%,0);}",
    "#k2-toast.k2-bad{background:#C24B31;}",
    ".k2-skel{background:linear-gradient(90deg,#eee 25%,#f7f7f7 37%,#eee 63%);background-size:400% 100%;animation:k2sh 1.3s ease infinite;border-radius:12px;}",
    "@keyframes k2sh{0%{background-position:100% 50%;}100%{background-position:0 50%;}}",
    "@media (prefers-reduced-motion:reduce){*{animation:none !important;transition:none !important;}}"
  ].join("\n");
  var st = document.createElement("style"); st.id = "k2-shell-css"; st.textContent = css; document.head.appendChild(st);

  /* ---- haptics ---- */
  function haptic(kind){
    try{
      var H = C && C.Plugins && C.Plugins.Haptics;
      if(H){ kind === "success" ? H.notification({type:"SUCCESS"}) : kind === "heavy" ? H.impact({style:"HEAVY"}) : H.impact({style:"LIGHT"}); return; }
      if(navigator.vibrate) navigator.vibrate(kind === "heavy" ? 30 : 10);
    }catch(e){}
  }
  window.K2 = window.K2 || {}; window.K2.haptic = haptic;
  document.addEventListener("click", function(e){ if(e.target.closest && e.target.closest("button")) haptic("light"); }, true);

  /* ---- toast + offline ---- */
  var toastT;
  function toast(msg, bad){
    var t = document.getElementById("k2-toast");
    if(!t){ t = document.createElement("div"); t.id = "k2-toast"; document.body.appendChild(t); }
    t.textContent = msg; t.className = bad ? "k2-bad" : ""; void t.offsetWidth; t.classList.add("k2-show");
    clearTimeout(toastT); toastT = setTimeout(function(){ t.classList.remove("k2-show"); }, 3200);
  }
  window.K2.toast = toast;
  window.addEventListener("offline", function(){ toast("You're offline — reconnecting…", true); });
  window.addEventListener("online", function(){ toast("Back online"); });

  /* ---- branded splash (hides when app has rendered) ---- */
  function splash(){
    var s = document.createElement("div"); s.id = "k2-splash";
    s.innerHTML = '<img src="/icon-512.png" alt=""><p>Karts2Me</p>';
    document.body.appendChild(s);
    var gone = false;
    function hide(){ if(gone) return; gone = true; s.classList.add("k2-off"); setTimeout(function(){ s.remove(); }, 600);
      try{ var SS = C && C.Plugins && C.Plugins.SplashScreen; if(SS) SS.hide(); }catch(e){} }
    var scr = document.getElementById("screen");
    if(scr && window.MutationObserver){
      var mo = new MutationObserver(function(){ if(scr.children.length){ mo.disconnect(); setTimeout(hide, 250); } });
      mo.observe(scr, {childList:true});
      if(scr.children.length) hide();
    }
    setTimeout(hide, 3500);
  }

  /* ---- native chrome ---- */
  function nativeChrome(){
    if(!native) return;
    try{
      var P = C.Plugins || {};
      if(P.StatusBar){ P.StatusBar.setStyle({style:"DARK"}); if(plat === "android"){ P.StatusBar.setBackgroundColor({color:"#FAF8F3"}); P.StatusBar.setOverlaysWebView({overlay:false}); } }
      if(P.Keyboard){ P.Keyboard.setAccessoryBarVisible && P.Keyboard.setAccessoryBarVisible({isVisible:true}); }
      if(P.App && P.App.addListener){
        P.App.addListener("backButton", function(ev){
          var mb = document.getElementById("modalBackdrop");
          if(mb && !mb.classList.contains("hidden")){ mb.classList.add("hidden"); return; }
          var back = document.querySelector(".backbtn");
          if(back){ back.click(); return; }
          if(!ev.canGoBack) P.App.exitApp && P.App.exitApp();
        });
      }
    }catch(e){}
  }

  /* ---- account deletion ---- */
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }
  function openDelete(){
    var role = window.K2_ROLE || "rider";
    openModal(
      '<div class="modal-head"><p style="font-weight:700;font-size:16px;">Delete account</p><button class="modal-close" id="delClose">&times;</button></div>' +
      '<div class="modal-body">' +
        '<p style="font-size:13px;line-height:1.5;">This permanently removes your sign-in and personal details (name, phone, photo, saved notifications). It cannot be undone.</p>' +
        '<p style="font-size:12px;line-height:1.5;color:var(--slate);margin-top:8px;">Records we are required to keep &mdash; ride, payment' + (role === "driver" ? ', payout and identity-verification' : '') + ' history &mdash; are kept without your name attached.</p>' +
        '<p style="font-size:12px;font-weight:600;margin:14px 0 6px;">Type DELETE to confirm</p>' +
        '<input id="delConfirm" class="field" autocomplete="off" autocapitalize="characters" placeholder="DELETE">' +
        '<div id="delErr" class="errbox" style="display:none;"></div>' +
        '<button id="delGo" disabled style="width:100%;margin-top:14px;padding:14px;border:none;border-radius:14px;background:#C24B31;color:#fff;font-weight:700;font-size:15px;opacity:.45;">Delete my account</button>' +
        '<button id="delCancel" class="btn-ghost" style="margin-top:8px;">Cancel</button>' +
      '</div>'
    );
    var inp = document.getElementById("delConfirm"), go = document.getElementById("delGo"), err = document.getElementById("delErr");
    function fail(m){ err.textContent = m; err.style.display = "block"; go.disabled = false; go.style.opacity = 1; go.textContent = "Delete my account"; }
    document.getElementById("delClose").onclick = document.getElementById("delCancel").onclick = closeModal;
    inp.oninput = function(){ var ok = inp.value.trim().toUpperCase() === "DELETE"; go.disabled = !ok; go.style.opacity = ok ? 1 : .45; };
    go.onclick = async function(){
      go.disabled = true; go.textContent = "Deleting…"; err.style.display = "none"; haptic("heavy");
      var res = await sb.rpc("delete_my_account");
      if(res.error){
        fail(/function|schema cache|does not exist/i.test(res.error.message || "")
          ? "Self-service deletion isn't available yet. Email support@karts2me.com and we'll delete it within 30 days."
          : "Couldn't delete: " + res.error.message);
        return;
      }
      var code = res.data;
      if(code === 1 || code === 2){
        try{ await sb.auth.signOut(); }catch(e){}
        try{ localStorage.clear(); }catch(e){}
        closeModal(); haptic("success");
        alert("Your account has been deleted.");
        location.reload();
      } else if(code === -2){ fail("You have a ride in progress. Finish or cancel it first, then try again."); }
      else if(code === -3){ fail("Admin and operator accounts are removed by Karts2Me. Email support@karts2me.com."); }
      else { fail("Please sign in again and retry."); }
    };
  }
  window.K2.openDeleteAccount = openDelete;
  document.addEventListener("click", function(e){
    var b = e.target.closest && e.target.closest("#deleteAcctBtn");
    if(b){ e.preventDefault(); openDelete(); }
  });

  function init(){ splash(); nativeChrome(); }
  if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
