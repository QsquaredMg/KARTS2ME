# Karts2Me

Monorepo for the four Karts2Me web apps, each a standalone static site (no build step) wired to the shared Supabase backend.

```
karts2me/
├── rider/       — rider PWA (booking, payment via Stripe, push notifications)
├── driver/      — driver PWA (category application, accept rides, earnings)
├── operator/    — operator dashboard (zones, vehicles, pricing, events)
└── admin/       — platform admin backend (approvals, operator verification)
```

Each folder is a fully self-contained static site: `index.html` + (where present) `manifest.json`, `sw.js`, `logo.png`. No build tooling — Vercel serves these as static output.

## Connecting to Vercel

These four folders map to **four separate Vercel projects** (already live at `kart2me-rider`, `kart2me-driver`, `kart2me-operator`, `kart2me-admin`). To connect this repo as the source for each:

1. Push this repo to GitHub (see below).
2. In each existing Vercel project → **Settings → Git** → connect this repository.
3. In each project's **Settings → General → Root Directory**, set it to the matching subfolder:
   - `kart2me-rider` → Root Directory: `rider`
   - `kart2me-driver` → Root Directory: `driver`
   - `kart2me-operator` → Root Directory: `operator`
   - `kart2me-admin` → Root Directory: `admin`
4. Framework Preset: **Other** (static files, no build command needed).
5. Once connected, every push to `main` auto-deploys that project from its subfolder.

## Backend

All four apps point at the same live Supabase project (`ajmtwylkhmwoistuewox`) and its Edge Functions (`create-payment-intent`, `stripe-webhook`, `notify-new-ride-request`, `notify-ride-accepted`). Supabase URL and anon key are embedded client-side in each app (anon key is safe to expose — it's rate-limited and RLS-scoped).

## Known gaps

- `operator/` and `admin/` still use the placeholder icon, not the final Karts2Me logo — pending redeploy.
- No custom domain (`karts2me.com`) attached yet.
