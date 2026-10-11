#!/usr/bin/env python3
"""Generates the marketing site (home hub + 3 funnel pages) into /home. Run: python3 scripts/build-site.py"""
import os, json
OUT = os.path.join(os.path.dirname(__file__), "..", "home")
SITE = "https://www.karts2me.com"

def ic(path, size=22, sw=1.9):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'
I = {
 "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 "shield": '<path d="M12 3 4.5 6v5.5c0 4.4 3.1 7.7 7.5 9 4.4-1.3 7.5-4.6 7.5-9V6z"/><path d="m9 12 2 2 4-4"/>',
 "bolt": '<path d="M13 3 5 13.5h6L10 21l8-10.5h-6z"/>',
 "card": '<rect x="3" y="5.5" width="18" height="13" rx="3"/><path d="M3 10h18M7 15h3"/>',
 "split": '<circle cx="8" cy="8" r="3"/><circle cx="16" cy="16" r="3"/><path d="M10.2 10.2 13.8 13.8"/>',
 "clock": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2M9 3h6"/>',
 "star": '<path d="m12 3.5 2.6 5.4 5.9.8-4.3 4.1 1 5.9L12 16.9 6.8 19.7l1-5.9L3.5 9.7l5.9-.8z"/>',
 "route": '<circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H15a3.5 3.5 0 0 0 0-7H9a3.5 3.5 0 0 1 0-7h6.5"/>',
 "check": '<path d="m4.5 12.5 5 5 10-11"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "home": '<path d="M3 11.5 12 4l9 7.5"/><path d="M5 10v10h5v-6h4v6h5V10"/>',
 "drive": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.4"/><path d="M12 3v6.6M3.6 14.5l6.2-1.7M20.4 14.5l-6.2-1.7"/>',
 "grid": '<rect x="3" y="3" width="7.5" height="7.5" rx="2"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="2"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="2"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="2"/>',
 "cart": '<path d="M5 17h14"/><path d="M6 17V9h12v8"/><path d="M8 9V5h8v4"/><circle cx="8" cy="19" r="1.6"/><circle cx="16" cy="19" r="1.6"/>',
 "cal": '<rect x="3.5" y="5" width="17" height="15" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
 "tag": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.3"/>',
 "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.4"/><path d="M17 14c2.5 0 4.5 2 4.5 4.5"/>',
 "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
 "image": '<rect x="3" y="4" width="18" height="16" rx="3"/><circle cx="9" cy="10" r="1.8"/><path d="m21 16-5-5-8 8"/>',
 "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 18.5h2"/>',
 "wallet": '<path d="M4 7h14a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h11"/><circle cx="16.5" cy="13.5" r="1.3"/>',
 "id": '<rect x="3" y="5" width="18" height="14" rx="3"/><circle cx="9" cy="11" r="2.2"/><path d="M5.5 16c.6-1.6 2-2.4 3.5-2.4s2.9.8 3.5 2.4M15 10h3M15 13.5h3"/>',
 "toggle": '<rect x="2.5" y="7" width="19" height="10" rx="5"/><circle cx="16" cy="12" r="2.6"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/>',
 "build": '<path d="M4 21V8l8-5 8 5v13"/><path d="M9 21v-6h6v6M8 11h2M14 11h2"/>',
}

def head(title, desc, path, dark=True, extra=""):
    url = SITE + path
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#04204A">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="Karts2Me">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/site.css">
{extra}
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
'''

def nav(cur, cta_href, cta_label):
    def a(k, label, href):
        c = ' aria-current="page"' if k == cur else ""
        return f'<a href="{href}"{c}>{label}</a>'
    links = a("ride", "Ride", "/ride") + a("drive", "Drive", "/drive") + a("operate", "For properties", "/operate")
    return f'''<header class="site dark" id="top">
  <div class="wrap nav">
    <a class="brand" href="/" aria-label="Karts2Me home"><img src="/k2-mark.svg" alt="" width="36" height="36"><b>Karts<i>2</i>Me</b></a>
    <nav class="links" aria-label="Main">{links}</nav>
    <div class="nav-cta">
      <a class="btn btn-line" href="{cta_href.split("?")[0]}">Log in</a>
      <a class="btn btn-or" href="{cta_href}">{cta_label}</a>
      <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="drawer">{ic('<path d="M4 7h16M4 12h16M4 17h16"/>',24,2.2)}</button>
    </div>
  </div>
  <nav class="drawer" id="drawer" aria-label="Mobile">
    <a href="/ride">Ride</a><a href="/drive">Drive</a><a href="/operate">For properties</a>
    <a href="{cta_href.split("?")[0]}">Log in</a>
    <a class="btn btn-or" href="{cta_href}">{cta_label}</a>
  </nav>
</header>
'''

def footer():
    return f'''<footer class="site">
  <div class="wrap">
    <div class="ft">
      <div><a class="brand" href="/"><img src="/k2-mark.svg" alt="" width="36" height="36"><b>Karts<i>2</i>Me</b></a>
        <p>On-demand shuttle carts &amp; shuttles for resorts, campuses, stadiums, communities and events.</p></div>
      <div class="cols">
        <div><h4>Platform</h4><a href="/ride">Ride</a><a href="/drive">Drive &amp; earn</a><a href="/operate">For properties</a></div>
        <div><h4>Open an app</h4><a href="https://ride.karts2me.com">Rider app</a><a href="https://driver.karts2me.com">Driver app</a><a href="https://operator.karts2me.com">Operator dashboard</a></div>
        <div><h4>Company</h4><a href="/terms">Terms of Service</a><a href="/privacy">Privacy Policy</a><a href="/accessibility">Accessibility</a><a href="mailto:support@karts2me.com">support@karts2me.com</a></div>
      </div>
    </div>
    <div class="fb"><span>&copy; <span id="yr">2026</span> Karts2Me, a Q Squared LLC company.</span><span>Mini transit for properties that need it.</span></div>
  </div>
</footer>
<script src="/site.js" defer></script>
</body></html>
'''

def mcta(href, label):
    return f'<div class="mcta" id="mcta"><a class="btn btn-or btn-lg" href="{href}">{label}</a></div>'

def faq(items):
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)

def features(items, cls=""):
    return "".join(f'<div class="feat rv"><div class="ic">{ic(I[i])}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in items)

def steps(items):
    return "".join(f'<div class="step rv"><h3>{t}</h3><p>{d}</p></div>' for t, d in items)

def strip(items):
    return '<div class="strip"><div class="wrap">' + "".join(f'<div class="it"><div class="ic">{ic(I[i])}</div><div><b>{t}</b><span>{d}</span></div></div>' for i, t, d in items) + "</div></div>"

def also(items):
    return '<div class="also">' + "".join(f'<a class="rv" href="{h}"><div class="ic">{ic(I[i],26)}</div><div><b>{t}</b><span>{d}</span></div></a>' for i, t, d, h in items) + "</div>"

def cta_band(h, p, primary, secondary=None):
    sec = f'<a class="btn btn-line btn-lg" href="{secondary[0]}">{secondary[1]}</a>' if secondary else ""
    return f'<div class="on-dark"><div class="cta-band rv"><h2>{h}</h2><p>{p}</p><div class="cta-row"><a class="btn btn-or btn-lg" href="{primary[0]}">{primary[1]} {ic(I["arrow"],18,2.2)}</a>{sec}</div></div></div>'

def chips(items):
    return '<div class="chips">' + "".join(f'<span class="chip">{ic(I["check"],16,2.4)}{t}</span>' for t in items) + "</div>"

def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj) + "</script>"

ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "Karts2Me", "url": SITE, "logo": SITE + "/logo.png", "email": "support@karts2me.com", "parentOrganization": {"@type": "Organization", "name": "Q Squared LLC"}}

# ---------- mockups ----------
MAP_ROUTE = '<svg class="route" viewBox="0 0 290 560" preserveAspectRatio="none" aria-hidden="true"><path d="M60 330 C 110 250, 80 190, 150 170 S 230 130, 232 90" fill="none" stroke="#fff" stroke-width="11" stroke-linecap="round"/><path d="M60 330 C 110 250, 80 190, 150 170 S 230 130, 232 90" fill="none" stroke="#0B4FA8" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 11"/></svg>'

RIDER_PHONE = f'''<div class="stage" aria-hidden="true">
  <div class="phone"><div class="notch"></div><div class="scr">
    <div class="map"></div>{MAP_ROUTE}
    <span class="pin" style="left:50px;top:318px;background:#2F8F5B"></span><span class="pin" style="left:222px;top:78px;background:#FA8411"></span>
    <div class="sheetm"><div class="row"><div class="av">M</div><div style="flex:1"><h5>Marcus arriving</h5><small>Cart 12 · 4 seats</small></div><div style="text-align:right"><h5>3 min</h5><small>away</small></div></div>
    <div class="mbtn">Share ride details</div></div>
  </div></div>
  <div class="floatcard bob" style="left:-4px;top:70px"><span class="ic g">{ic(I["split"],18)}</span><div><b>Split the fare</b>with your group</div></div>
  <div class="floatcard bob d2" style="right:-14px;top:235px"><span class="ic">{ic(I["star"],18)}</span><div><b>Rate &amp; tip</b>after every ride</div></div>
</div>'''

DRIVER_PHONE = f'''<div class="stage" aria-hidden="true">
  <div class="phone"><div class="notch"></div><div class="scr" style="background:#fff">
    <div style="padding:52px 20px 0"><small style="color:#566074">Good afternoon</small><h5 style="font:700 22px var(--display);color:#04204A;margin:2px 0 14px">You're online</h5>
      <div class="row" style="background:#E5F5EC;border-radius:18px;padding:14px 16px"><div style="flex:1"><b style="font:700 15px var(--display);color:#1F7A4A">Accepting rides</b><br><small style="color:#3D6B52">Resort zone · Cart 7</small></div>
      <div style="width:50px;height:30px;border-radius:99px;background:#2F8F5B;position:relative"><i style="position:absolute;right:3px;top:3px;width:24px;height:24px;border-radius:50%;background:#fff"></i></div></div></div>
    <div class="sheetm" style="bottom:12px"><small style="color:#B45309;font-weight:650;letter-spacing:.06em">NEW REQUEST</small>
      <div class="row" style="margin-top:8px"><div style="flex:1"><h5>Clubhouse → Lodge</h5><small>2 riders · 0.6 mi</small></div><h5 style="font-size:20px">Accept</h5></div>
      <div style="height:6px;border-radius:99px;background:#E3E8F0;margin-top:12px;overflow:hidden"><i style="display:block;width:68%;height:100%;background:#FA8411"></i></div>
      <div class="mbtn">Accept ride</div></div>
  </div></div>
  <div class="floatcard bob" style="left:-14px;top:262px"><span class="ic b">{ic(I["wallet"],18)}</span><div><b>Paid out via Stripe</b>after completed rides</div></div>
  <div class="floatcard bob d2" style="right:-14px;top:18px"><span class="ic g">{ic(I["toggle"],18)}</span><div><b>You choose</b>when you're online</div></div>
</div>'''

OPERATOR_LAPTOP = f'''<div class="stage" aria-hidden="true" style="min-height:420px">
  <div class="laptop"><div class="bar"><i></i><i></i><i></i></div>
    <div class="dash"><aside><div class="lg"><img src="/k2-mark.svg" alt="">Karts2Me</div><span class="on">Overview</span><span>Rides</span><span>Fleet</span><span>Drivers</span><span>Zones</span><span>Events</span><span>Branding</span></aside>
    <main><h6>Today at your property</h6>
      <div class="kpis"><div class="kpi"><small>Rides</small><b>—</b></div><div class="kpi"><small>Carts out</small><b>—</b></div><div class="kpi"><small>Drivers</small><b>—</b></div></div>
      <div class="dmap map"><div class="zone" style="left:14%;top:22%;width:42%;height:52%"></div><div class="zone" style="left:58%;top:12%;width:30%;height:40%;border-color:#0B4FA8;background:rgba(11,79,168,.14)"></div></div>
      <div class="tbl"><div><span>Clubhouse → Lodge</span><span class="tag">Completed</span></div><div><span>Gate B → Section 114</span><span class="tag o">En route</span></div><div><span>Pool → Spa</span><span class="tag o">Requested</span></div></div>
    </main></div></div>
  <div class="floatcard bob" style="right:-8px;bottom:-6px"><span class="ic">{ic(I["tag"],18)}</span><div><b>Your rates</b>base, per-seat, per-mile</div></div>
</div>'''

# ---------- pages ----------
def page(path, filename, title, desc, cur, cta, hero_h1, hero_lead, hero_chips, mock, strip_items, steps_h, steps_p, step_items, feat_h, feat_p, feat_items, split, faq_items, band, also_items, ld_extra=None):
    h = head(title, desc, path, extra=jsonld(ORG) + (jsonld(ld_extra) if ld_extra else ""))
    h += nav(cur, cta[0], cta[1])
    h += f'''<main id="main">
<section class="hero on-dark"><div class="wrap hero-grid">
  <div><span class="eyebrow">{hero_lead[0]}</span>
  <h1 style="margin-top:18px">{hero_h1}</h1>
  <p class="lead">{hero_lead[1]}</p>
  <div class="cta-row"><a class="btn btn-or btn-lg" href="{cta[0]}">{cta[1]} {ic(I["arrow"],18,2.2)}</a><a class="btn btn-line btn-lg" href="{hero_lead[2][0]}">{hero_lead[2][1]}</a></div>
  {chips(hero_chips)}
  <p class="fine">{hero_lead[3]}</p></div>
  {mock}
</div></section>
{strip(strip_items)}
<section class="sec" id="how"><div class="wrap"><div class="head"><span class="eyebrow">How it works</span><h2>{steps_h}</h2><p class="lead">{steps_p}</p></div><div class="steps">{steps(step_items)}</div></div></section>
<section class="sec alt"><div class="wrap"><div class="head center"><span class="eyebrow">Features</span><h2>{feat_h}</h2><p class="lead">{feat_p}</p></div><div class="grid3">{features(feat_items)}</div></div></section>
<section class="sec"><div class="wrap split"><div class="rv"><span class="eyebrow">{split[0]}</span><h2 style="font-size:clamp(28px,3.6vw,42px);margin:14px 0 8px;letter-spacing:-.03em">{split[1]}</h2><p class="lead">{split[2]}</p><ul class="checks">{"".join(f'<li>{ic(I["check"],22,2.4)}<span><b>{b}</b> {t}</span></li>' for b,t in split[3])}</ul></div>
  <div class="panel rv"><h3>{split[4][0]}</h3><p>{split[4][1]}</p><div class="cta-row"><a class="btn btn-or" href="{cta[0]}">{cta[1]}</a></div></div></div></section>
<section class="sec alt" id="faq"><div class="wrap"><div class="head center"><span class="eyebrow">Questions</span><h2>Good to know before you start.</h2></div><div class="faq">{faq(faq_items)}</div></div></section>
<section class="sec" style="padding-bottom:0">{band}</section>
<section class="sec" style="padding-bottom:0"><div class="wrap"><div class="head"><span class="eyebrow">More from Karts2Me</span><h2 style="font-size:clamp(26px,3vw,36px)">One platform, three ways in.</h2></div>{also(also_items)}</div></section>
</main>
{mcta(cta[0], cta[1])}
'''
    h += footer()
    open(os.path.join(OUT, filename), "w").write(h)

RIDE_URL = "https://ride.karts2me.com/?signup=1"
DRIVE_URL = "https://driver.karts2me.com/?signup=1"
OP_URL = "https://operator.karts2me.com/?signup=1"
ALSO_RIDE = [("drive", "Drive & earn", "Pick up shifts on a property's cart fleet.", "/drive"), ("build", "Run a property?", "Put on-demand transit on your grounds.", "/operate")]
ALSO_DRIVE = [("cart", "Need a ride?", "Request a cart or shuttle on property.", "/ride"), ("build", "Run a property?", "Put on-demand transit on your grounds.", "/operate")]
ALSO_OP = [("cart", "See the rider experience", "What your guests and members will use.", "/ride"), ("drive", "See the driver experience", "How your drivers get work and get paid.", "/drive")]

# ===== RIDE =====
page("/ride", "ride.html",
  "Book a shuttle cart on property | Karts2Me", "Request a shuttle cart or shuttle at resorts, campuses, stadiums and communities. See your driver, track the ride, split the fare and tip in the app.",
  "ride", (RIDE_URL, "Book your first ride"),
  "Your ride, <em>on property</em>. On demand.",
  ("For riders", "Skip the wait and the walk. Request a shuttle cart from your phone, watch your driver arrive, and get where you're going across the property.", ("https://ride.karts2me.com", "I have an account"), "Available where your property, venue or event has turned Karts2Me on."),
  ["Free to sign up", "Pay in the app", "Track every ride"], RIDER_PHONE,
  [("shield", "Approved drivers", "Drivers apply and are approved before they take rides."), ("card", "Secure payments", "Card payments handled by Stripe. We never see your card number."), ("pin", "Built for properties", "Pickup and drop-off points set by the property.")],
  "Three taps from here to there.", "No stands, no phone calls, no guessing when the cart will show up.",
  [("Request", "Choose your pickup and drop-off on the property map, or hop on a scheduled shuttle route where one is running."), ("Meet your driver", "See who's coming and a live ETA. At properties with bidding turned on, you can choose the rate that works for you."), ("Ride, pay, rate", "Pay in the app, split the fare with your group, and leave a rating and tip when you arrive.")],
  "Everything a great ride needs.", "Designed for the way people actually move around resorts, campuses and venues.",
  [("route", "Live tracking", "Follow your driver in real time from request to drop-off."), ("split", "Split the fare", "Riding with friends? Everyone pays their share in the app."), ("clock", "Scheduled shuttles", "Hop on fixed routes where your property runs them."), ("tag", "Clear pricing", "See the price before you request. Some properties let you bid."), ("star", "Ratings &amp; tips", "Recognize great drivers with a rating and an in-app tip."), ("phone", "Works on your phone", "Install it to your home screen. No store download needed to start.")],
  ("Rider-first", "Made for the way you move.", "Whether it's a tee time, a lecture, or kickoff, Karts2Me gets you there without the hassle.", [("No account hoops.", "Sign up with your email and book in minutes."), ("Accessible by design.", "Built to WCAG 2.1 AA, with service animals welcome on every ride."), ("Delete anytime.", "You can delete your account and data from inside the app.")], ("Ready when you are.", "Create your free account and request your first ride.")),
  [("Where can I use Karts2Me?", "At any resort, campus, stadium, community or event where the property has turned Karts2Me on. Sign up, and the app shows you what's available near you."), ("How much does it cost?", "Signing up is free. Ride prices are set by each property and shown before you request. Some properties let riders bid on the rate."), ("How do I pay?", "In the app by card, processed securely by Stripe. You can split the fare with the people riding with you."), ("Are the drivers vetted?", "Drivers apply, submit identification, and are approved by the property before they can accept rides."), ("Can I bring a service animal or mobility device?", "Yes. Service animals are welcome on every ride, and drivers may not refuse or add charges because of a disability. See our accessibility page for details."), ("Can I delete my account?", "Yes, from inside the app at any time. Your personal data is removed as described in our Privacy Policy.")],
  cta_band("Your next ride is a few taps away.", "Create a free account and book a cart on your property.", (RIDE_URL, "Book your first ride"), ("https://ride.karts2me.com", "Log in")), ALSO_RIDE)

# ===== DRIVE =====
page("/drive", "drive.html",
  "Drive shuttle carts and earn | Karts2Me Driver", "Drive shuttle carts at resorts, campuses and venues on your schedule. Go online when you want, accept rides, and get paid out automatically through Stripe.",
  "drive", (DRIVE_URL, "Apply to drive"),
  "Drive carts. <em>Set your own pace.</em>",
  ("For drivers", "Pick up shifts on a property's cart fleet, go online when it suits you, and get paid out automatically after completed rides.", ("https://driver.karts2me.com", "Driver login"), "Open to drivers 18+ approved by the property. Availability depends on the property."),
  ["Go online when you want", "Automatic payouts", "Apply in minutes"], DRIVER_PHONE,
  [("toggle", "You control your time", "Toggle online or offline whenever you like."), ("wallet", "Paid through Stripe", "Payouts land in your connected account after rides."), ("shield", "Approved &amp; verified", "A simple application and ID check keeps everyone safe.")],
  "From application to first ride.", "A short path from sign-up to carrying riders.",
  [("Apply", "Create your account, add your details and an identification photo, and agree to the driver terms."), ("Get approved", "The property reviews your application. Once you're approved you can go online."), ("Drive &amp; get paid", "Accept requests, complete rides, and connect Stripe to receive your payouts.")],
  "Tools that make driving easy.", "Everything you need in one simple, phone-first app.",
  [("bolt", "Instant requests", "New ride requests appear with pickup, drop-off and rider count."), ("route", "Navigate on property", "See the route on the property map from pickup to drop-off."), ("wallet", "Earnings in one place", "Track completed rides and what you've earned."), ("id", "Simple onboarding", "Take your ID photo right in the app. No paperwork packets."), ("users", "Gig or employed", "Work as an independent driver or join a property's team, depending on the property."), ("phone", "Works on your phone", "Install to your home screen, or use the native app when it's available.")],
  ("Driver-friendly", "Built around the driver.", "A clear, fair workflow with the information you need before you accept.", [("See the ride first.", "Pickup, destination and rider count are shown up front."), ("Stay in control.", "Go offline anytime. No minimum hours inside the app."), ("Your data, your call.", "Location is shared only while you're on an active ride, and you can delete your account in the app.")], ("Start in a few minutes.", "Create your account and submit your application. It's free to apply.")),
  [("Do I need my own vehicle?", "Usually no. Properties provide the carts and shuttles. Your operator will tell you what's required at your property."), ("How and when do I get paid?", "Payouts are sent to the Stripe account you connect, after completed rides. Timing follows Stripe's payout schedule."), ("Am I an employee or an independent driver?", "It depends on the property. Some work with gig drivers, others employ their drivers. Your operator will tell you which applies."), ("What do I need to apply?", "You must be 18 or older and able to take a clear photo of your identification. The property reviews and approves your application."), ("When is my location shared?", "Only while you're on an active ride, so riders can see you coming. It's cleared when you delete your account."), ("Can I delete my account?", "Yes, from inside the driver app at any time.")],
  cta_band("Ready to hit the path?", "Apply to drive. It's free and takes a few minutes.", (DRIVE_URL, "Apply to drive"), ("https://driver.karts2me.com", "Driver login")), ALSO_DRIVE)

# ===== OPERATE =====
page("/operate", "operate.html",
  "On-demand shuttle software for properties | Karts2Me Operator", "Run on-demand shuttle cart service on your resort, campus, stadium or community. Manage zones, pricing, fleet, drivers and events from one dashboard.",
  "operate", (OP_URL, "Create operator account"),
  "Run your fleet <em>like a modern transit network.</em>",
  ("For properties &amp; operators", "Give guests, members and fans on-demand rides. Manage zones, pricing, carts, drivers and events from one dashboard, with your own branding.", ("mailto:support@karts2me.com?subject=Karts2Me%20for%20our%20property", "Talk to us"), "Launch on your own grounds. Bring your own drivers or recruit through the platform."),
  ["Your branding", "Your pricing", "Your zones"], OPERATOR_LAPTOP,
  [("grid", "One dashboard", "Rides, fleet, drivers, zones and events in one place."), ("tag", "You set the rates", "Base fares, per-seat and per-mile pricing, plus optional rider bidding."), ("card", "Payments built in", "Stripe handles rider payments and driver payouts.")],
  "Live on your property in four moves.", "Set it up once, then let the system do the dispatching.",
  [("Create your property", "Add your name, logo, contact details and the zones where service runs."), ("Add your fleet", "List vehicle types and individual carts with photos, status and ownership."), ("Bring your drivers", "Approve driver applications and review ID photos, or add your own team."), ("Open it up", "Turn on service. Riders request, drivers accept, and you watch it all live.")],
  "Everything to run it well.", "Operator tools designed for resorts, campuses, venues and communities.",
  [("pin", "Zones &amp; geofencing", "Draw the areas you serve and where pickups and drop-offs are allowed."), ("cart", "Fleet management", "Track vehicle types and individual carts, with photos and maintenance status."), ("users", "Driver management", "Review applications, view ID photos, and manage gig or employed drivers."), ("cal", "Events &amp; scheduling", "Plan event-night service and run scheduled shuttle routes."), ("chart", "Ride visibility", "See ride activity and manage requests as they happen."), ("image", "Your brand", "Upload your logo and show riders your contact info, website and socials.")],
  ("For operators", "Control without the overhead.", "Keep your guests moving without building software or hiring a dispatcher.", [("Your rules.", "Pricing, zones, hours and service types are yours to set."), ("Your drivers.", "Gig, employed, or both, with approval in your hands."), ("Your guests' trust.", "Riders see your branding and can contact you directly from the app.")], ("Let's put it on your property.", "Create an operator account to start, or tell us about your venue and we'll help you launch.")),
  [("What kinds of properties use Karts2Me?", "Resorts and golf clubs, campuses, stadiums and venues, HOAs and managed communities, and event grounds: anywhere carts or shuttles move people inside a bounded area."), ("Do I need my own carts and drivers?", "You bring the fleet. For drivers you can add your own team or approve gig drivers who apply through the platform."), ("How does pricing work for riders?", "You set base, per-seat and per-mile pricing, and can choose to let riders bid at your property. Riders see the price before they request."), ("How do payments and payouts work?", "Rider payments and driver payouts run through Stripe, so you don't handle card data or manual payouts."), ("How long does setup take?", "Creating your account, adding your zone and fleet, and approving drivers can be done in a single sitting. Tell us about your property and we'll help you launch."), ("What about insurance and licensing?", "Operators are responsible for the insurance, permits and regulatory requirements that apply to their property and vehicles. Talk to us if you have questions about getting set up.")],
  cta_band("Put your property in motion.", "Create an operator account today, or email us and we'll walk you through a launch.", (OP_URL, "Create operator account"), ("mailto:support@karts2me.com?subject=Karts2Me%20for%20our%20property", "Talk to us")), ALSO_OP)

# ===== HOME HUB =====
extra = jsonld(ORG) + jsonld({"@context": "https://schema.org", "@type": "WebSite", "name": "Karts2Me", "url": SITE})
h = head("Karts2Me | On-demand shuttle carts & shuttles for properties", "On-demand shuttle carts and shuttles for resorts, campuses, stadiums, communities and events. Request a ride, drive for pay, or run your property's fleet.", "/", extra=extra)
h += nav("", RIDE_URL, "Book a ride")
h += f'''<main id="main">
<section class="hero on-dark" style="padding-bottom:64px"><div class="wrap hero-grid" style="padding-bottom:40px">
  <div><span class="eyebrow">On-demand mini transit</span>
  <h1 style="margin-top:18px">Shuttle carts, <em>called like a ride.</em></h1>
  <p class="lead">Karts2Me brings on-demand transit to resorts, campuses, stadiums and communities. Request from your phone and a driver already on property comes to you.</p>
  <div class="cta-row"><a class="btn btn-or btn-lg" href="/ride">Book a ride {ic(I["arrow"],18,2.2)}</a><a class="btn btn-line btn-lg" href="/operate">Bring it to my property</a></div>
  {chips(["Resorts &amp; golf", "Campuses", "Stadiums &amp; events", "Communities"])}
  <p class="fine">Available where your property, venue or event has turned Karts2Me on.</p></div>
  {RIDER_PHONE}
</div></section>
<div class="wrap"><div class="paths">
  <a class="path" href="/ride"><div class="ic">{ic(I["cart"],26)}</div><h3>Ride</h3><p>Book a shuttle cart or shuttle anywhere Karts2Me is turned on. Track your driver, split the fare, tip after.</p><span class="go">Book a ride {ic(I["arrow"],18,2.2)}</span></a>
  <a class="path o" href="/drive"><div class="ic">{ic(I["drive"],26)}</div><h3>Drive</h3><p>Pick up shifts on a property's fleet, gig or employed. Go online when you want and get paid out automatically.</p><span class="go">Apply to drive {ic(I["arrow"],18,2.2)}</span></a>
  <a class="path g" href="/operate"><div class="ic">{ic(I["build"],26)}</div><h3>Operate</h3><p>Run zones, pricing, fleet, drivers and events from one dashboard, with your own branding.</p><span class="go">Launch on my property {ic(I["arrow"],18,2.2)}</span></a>
</div></div>
<section class="sec" id="how"><div class="wrap"><div class="head"><span class="eyebrow">How it works</span><h2>One route, start to finish.</h2><p class="lead">One system behind three connected apps, so riders, drivers and properties all see the same ride.</p></div>
<div class="steps">{steps([("Request", "A rider picks a drop-off on the property map or hops on a scheduled route."), ("Dispatch", "A driver on property accepts. The rider sees who's coming and a live ETA."), ("Ride &amp; settle", "Payment runs through Stripe, the driver is paid out, and the operator sees it all.")])}</div></div></section>
<section class="sec alt"><div class="wrap"><div class="head center"><span class="eyebrow">Where it runs</span><h2>Built for bounded properties, not open roads.</h2></div>
<div class="venues">
<div class="venue rv"><div class="ic">{ic(I["pin"])}</div><h3>Resorts &amp; golf clubs</h3><p>Cart paths between rooms, the course and the clubhouse.</p></div>
<div class="venue rv"><div class="ic">{ic(I["cal"])}</div><h3>Campuses</h3><p>Cross-quad shuttles for students, staff and visitors.</p></div>
<div class="venue rv"><div class="ic">{ic(I["star"])}</div><h3>Stadiums &amp; venues</h3><p>Gate-to-seat rides on gameday and event nights.</p></div>
<div class="venue rv"><div class="ic">{ic(I["home"])}</div><h3>HOAs &amp; communities</h3><p>Everyday cart transit within a managed neighborhood.</p></div>
</div></div></section>
<section class="sec"><div class="wrap"><div class="head center"><span class="eyebrow">Why Karts2Me</span><h2>Made to feel effortless for everyone involved.</h2></div>
<div class="grid3">{features([("shield","Approved drivers","Every driver applies and is approved by the property before taking rides."),("card","Payments handled","Stripe powers rider payments and driver payouts end to end."),("route","Live tracking","Riders follow the cart in real time from request to drop-off."),("tag","Property-set pricing","Operators set the rates, and some let riders bid."),("phone","Phone-first","Install to your home screen, or use the native app."),("users","Accessible by design","Built to WCAG 2.1 AA. Service animals welcome on every ride.")])}</div></div></section>
<section class="sec" style="padding-top:0"><div class="on-dark">{cta_band("Let's get you moving.", "Riders, drivers and properties all start in the same place.", ("/ride", "Book a ride"), ("/operate", "I run a property"))}</div></section>
</main>
{mcta("/ride", "Book a ride")}
'''
h += footer()
open(os.path.join(OUT, "index.html"), "w").write(h)

# sitemap, robots
urls = ["/", "/ride", "/drive", "/operate", "/accessibility", "/privacy", "/terms"]
open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print("built")
