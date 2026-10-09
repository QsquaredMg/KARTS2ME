# Karts2Me native apps (Capacitor)

Two thin native shells that load the live web apps (`rider.karts2me.com`, `driver.karts2me.com`)
and add native chrome (splash, status bar, haptics, back button, keyboard) via `shell.js`.
Web deploys update the apps instantly; store re-submission is only needed when native config/plugins change.

## One-time setup (any machine with Node 18+)
```
cd mobile/rider            # or mobile/driver
npm install
npx cap add android        # and/or: npx cap add ios   (iOS needs a Mac + Xcode)
npx cap sync
```
Icons/splash: `npm i -D @capacitor/assets` then put a 1024x1024 `assets/icon-only.png` and a 2732x2732 `assets/splash.png`
(navy #073876 background, logo centered) in the project and run `npx capacitor-assets generate`.

## Android (Google Play)
1. Install Android Studio. `npx cap open android`.
2. Build > Generate Signed Bundle (AAB). Keep the keystore safe — losing it blocks updates.
3. Play Console ($25 one-time): create app, upload AAB, fill Data safety (location, name, email, phone, payments via Stripe; account deletion = in-app + support@karts2me.com), privacy URL `https://rider.karts2me.com/privacy.html`.
4. New personal accounts must run a closed test (12+ testers, 14 days) before production; org accounts need D-U-N-S.
5. Driver app: declare background location use + a short demo video; add `ACCESS_BACKGROUND_LOCATION` and a foreground-service notification.

## iOS (App Store)
1. Apple Developer Program ($99/yr; org enrollment needs D-U-N-S). `npx cap open ios`, set Team + signing.
2. Add Info.plist strings: `NSLocationWhenInUseUsageDescription` (and for driver `NSLocationAlwaysAndWhenInUseUsageDescription`, plus Background Modes > Location updates), camera/photo if used.
3. Archive > upload to App Store Connect > TestFlight, then submit.
4. Review risk (Guideline 4.2 "minimum functionality"): mitigated by native splash/haptics/push/geolocation; enable push (APNs key in Supabase/your push sender) before submitting. Provide a reviewer demo account.
5. Account deletion (5.1.1(v)) is in-app: Home > Delete account (requires `db/delete_my_account.sql` applied in Supabase).

## Driver background location
`@capacitor-community/background-geolocation` keeps GPS flowing with the screen off during an active ride. Hook into
`startLocationSharing()`/`stopLocationSharing()` in `driver/index.html`: when `Capacitor.isNativePlatform()`, call
`BackgroundGeolocation.addWatcher({backgroundMessage:"Sharing your location with your rider", backgroundTitle:"Karts2Me ride active", requestPermissions:true, distanceFilter:10}, cb)` and write to `drivers.current_lat/lng` as the web path does.

## Remote-URL note
Because `server.url` is remote, the app needs connectivity; `www/index.html` is the offline fallback with a Retry button.
Stripe requires https, which this satisfies on both platforms.
