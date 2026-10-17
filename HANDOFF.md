# VIPTV KMP Session Handoff — 2026-10-17

This handoff covers the `experiment/kmp-v2` KMP session: state of all repos,
deployments, runtimes, accounts, and exactly what remains. Read this before
continuing work in a new session.

## TL;DR

The KMP all-platforms plan is functionally complete: all four platforms
(Android, desktop, web/wasm, iOS compile) build, the full automated gates are
green, Simkl and real playback are certified with evidence, and the beta
deployment (`beta-viptv.syek.tech`) runs the KMP stack end-to-end. What remains
is runtime/hardware-gated qualification (iOS runtime, Windows/macOS desktop
runtime, 197-board sweep) plus the in-flight torrent port (see below).

## Repos & branches

- **`/mnt/ALPH/code/viptv-org/app`** — branch `experiment/kmp-v2`, fully
  committed and pushed through `f108f78` ("Complete KMP all-platforms
  session..." + native/core pointer update). Remote:
  `https://github.com/viptv-org/app.git`
- **`/mnt/ALPH/code/viptv-org/.worktrees/kmp-v2/backend`** — branch
  `experiment/kmp-v2`, committed and pushed through `ea82f19` ("Migrate all
  tests to unversioned API and split search rows per catalog"). Remote:
  `https://github.com/viptv-org/backend.git`
- **`/mnt/ALPH/code/viptv-org/app/native/core`** — own repo, was detached HEAD;
  session commit pushed to `experiment/kmp-v2` (44c5ceb). Remote:
  `https://github.com/viptv-org/core.git`
- **`design`** — clean, on `main`; carries this handoff (pushed).
  **`workspace`** — clean, nothing to commit.

## What's done (this session)

### Platforms
- **iOS**: `iosArm64`/`iosSimulatorArm64` targets with full `iosMain` actuals
  (19 expects). klib compile gate passes on Linux. Swift UniFFI bindings for
  the Rust `LocalEngine` generated into `app/native/adapters/ios/`. Runtime
  execution (framework linking, simulator) requires macOS/xtool — documented
  in root `AGENTS.md` (xtool not installable on this host; notes included).
- **Desktop**: Windows x64 + macOS aarch64 portable packages cross-built with
  bundled JREs. Linux `.deb` install/vault/startup verified earlier. Desktop
  JVM suite 318 green. 10 desktop UI issues fixed this session (direct play,
  Live TV overlap, min window size, source-selector wrap, Resume/Play-from-
  start, Streams button, seekbar design, search rows, home carousels).
- **Web/wasm**: deployed to beta at site root. Mobile-web fixes: session
  restore splash (no login flash), proactive token refresh, discover
  responsive layout, no-thumb progress bars, settings fixes, focus outlines
  disabled on compact browsers.
- **Android**: TV emulator APK installed and verified against beta domain —
  home screen renders Simkl-backed carousels via the real API (screenshot
  evidence in `/tmp/junie/session-261015-204504-m6uv/tv-app-launch.png`).
  Simkl is NOT required for the app to work — Cinemeta rows render without
  any Simkl link, and an unlinked Simkl just hides Simkl rows.

### Backend (unversioned API)
- All `/api/v2/*` and `/api/v3/*` routes removed; the API is unversioned
  `/api/*`. The KMP app and dashboard migrated to the new paths. Old tv-web
  page deleted; account dashboard at `/device`.
- Backend test migration complete: `cargo test --lib` 488 passed / 0 failed,
  full `cargo test` (12 integration binaries) green. Run tests with
  `SIMKL_CLIENT_ID=fixture SIMKL_CLIENT_SECRET=fixture-secret`.
- Search: multi-catalog addons split into per-catalog rows
  ("Addon · Catalog"). Home limits raised (10 catalogs / 16 rows).

### Deployments
- **`beta-viptv.syek.tech`** — image `viptv:kmp-beta-20261016-2` (rollback
  record at `.deploy-rollback/kmp-beta-20261016-2/DEPLOYED.md`, plus the
  earlier `kmp-beta-20261016`). KMP wasm app at site root (no `/tv/` prefix
  needed anymore). Addons installed for account `simkl-test` (profile 1
  "SIMKL Tester"): Cinemeta, Torrentio (Torbox variant + plain), PenguPlay.
  Health verified 200. Simkl OAuth on beta requires a fresh grant through
  `/api/profiles/1/simkl` authorize (old KATO link is legacy-table data the
  v3 surface doesn't read) — user was given an authorize URL.

### Torrent support (in flight — the one open work item)
- **Android torrent playback is proven** on a main Android branch
  (`TorrentRuntimeWorker` + scope-owner + failure handling). It is the
  reference implementation.
- **Web uses the gateway server for torrents** — already working.
- **Desktop native-torrent port**: delegated to a background agent
  ("Desktop native torrent port", Paseo agent ID
  `84ec1189-ca6a-42d4-b5a8-6e1fda733346`). It studied the Android reference
  but had not finished wiring the desktop equivalent when the session ended —
  **check its final report and the app repo diff for its landed work before
  continuing**. The web-platform gateway path needs no port.

## Accounts & credentials

- **Live QA backend**: `https://viptv.local.test:18445` — login `qa-parent` /
  `4oRyNs4mdk6SK7Df4Fgg8kGMQZHMpn6YHAmF9Xr0xPw`, profile 1 has Simkl linked
  (all 5 capabilities, clean counters). Backend restarted on the new binary
  (per-catalog search + home carousel limits live). Sessions were reset by
  the restart.
- **Beta**: account `simkl-test` / `9LdGArpwDSOF4wQSxn8U0iZGA4g`, profile 1
  "SIMKL Tester". Used for mobile-web play-flow verification.
- **Isolated fixture runtimes** live under `/mnt/ALPH/.viptv-qa/` — use for
  destructive tests; never unlink qa-parent.

## Evidence & docs

- `app/docs/KMP_COMPLETION_RECORD.md` — the honest completion record.
- `app/docs/REMAINING_KMP_WORK.md` — ledger (authoritative remaining-work tracker).
- Simkl E2E + real playback evidence: `/mnt/ALPH/.viptv-qa/unified-real-current-vxstvf2g/`
  (`simkl-e2e-*/summary.json`, `real-playback-current-*/summary.json`, sha256-pinned).
- Deployment records: `.deploy-rollback/kmp-beta-20261016{,-2}/DEPLOYED.md`.
- Root `AGENTS.md` — has the iOS/xtool section (constraints from this host).

## What remains (next session)

1. **Desktop native-torrent port** — NOT started (the agent was cancelled in
   its study phase; no torrent code landed, desktop compile verified clean).
   Use the Android `TorrentRuntimeWorker` as reference. Web needs nothing
   (gateway handles it).
2. (Commits/pushes are done — see "Repos & branches" for the final hashes.)
3. **iOS runtime qualification** — needs a macOS host or xtool; blocked on
   hardware/toolchain, not code.
4. **Windows/macOS desktop runtime runs** — artifacts exist; execution needs
   actual Windows/macOS environments.
5. **197-board fidelity sweep** — automated parity harness exists; run it.
6. **Android warm-Home budget row** — still open in the ledger.
7. **Physical-device/TV rows** — human-gated, not claimable from this host.

## Environment quirks (this host)

- X11 needs the live `XAUTHORITY` (check `/run/user/1000/xauth_*`; stale one
  fails with "Can't connect to X11 window server").
- Emulators: `viptv-native-tv-qa` (TV, API 36), `viptv-native-qa` (phone),
  `viptv-design-tv`, `viptv-design-phone`, `viptv-ui-trial`.
- Box is OOM-prone; keep cargo/gradle jobs capped (cargo -j2).
- `gateway.syek.tech` edge 403s plain `python-urllib` UAs — use browser-like UA.
- Deployments go through Dokploy+dockflare; see the `viptv-deploy` skill for
  the full quirk list (historical failed deploys reported as successful).
