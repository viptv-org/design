# VIPTV responsive design study

**Throwaway prototype on `prototype/responsive-ui-oled`; not a production app or release candidate.** Review it with [the proposed responsive contract](../../RESPONSIVE_UI.md) and [design tokens](../../tokens/responsive.json). Android phone remains Kotlin/Compose; this React study is its visual/interaction reference and the proposed shared responsive UI for mobile web, desktop web and Tauri. TV continues using its existing remote-first composition.

## Run and review

From this directory, with Node 22:

```sh
npm ci --ignore-scripts
npm run dev
```

Open `http://localhost:4180/`. On another device use the server's reachable LAN IP and expose port 4180 if running in a container. This study uses fictional local fixtures, not account credentials or the production API. The temporary LAN review installation is a static production build of this study; it is still a prototype.

The **Design study** control switches the following without changing the underlying contract:

- `?variant=A`: contained landscape artwork next to copy, stacked on phone. Recommended starting point.
- `?variant=B`: compact artwork and copy; discovery appears sooner.
- `?variant=C`: greeting and Continue watching before a secondary featured title.
- `&theme=oled`: pure-black canvas with the same artwork, cards, contrast and focus treatment.
- `&platform=tauri` or `&platform=android`: native SmartCast **simulation**. The default `web` host explains native-app handoff instead.

Keyboard arrows switch variants only while the study switcher has focus. Within a shelf, Left/Right stays in that shelf. Shift+F10/right-click and the visible More button open the same menu. Escape dismisses a modal and returns to its opener. Design-study controls are deliberately outside the proposed production UI.

Use the Settings screen to compare appearance. Try Home, Search, details/episodes, sources, the player controls, Live TV, Library and profile choice. The state selector exposes Home loading/empty/failure/missing-art and source-start failure. Native TV simulation uses a valid-looking address and any four-digit PIN except `0000`; that rejected PIN keeps the form open. Pairing → launch cancellation/failure/retry → acknowledged launch → remote are separate states. No network TV is contacted and no media is played.

## Shared data provenance and limits

`CORE_REF` pins `viptv-org/core` at `1bf880a1f8c826a09aae2995d903cf090859d1f6`. `vendor/` is an unchanged copy of that revision's generated TypeScript wire definitions, WASM JavaScript/types and WASM binary. `CORE_ARTIFACTS.sha256` verifies these copied artifacts from the design repository root:

```sh
sha256sum -c prototypes/responsive/CORE_ARTIFACTS.sha256
```

`src/data.ts` feeds fictional media/source fixtures through the actual Rust `normalize` bridge. Hero/poster/episode image selection, title/episode labels, normalized progress and primary-action labels come from `MediaPresentation`, not ad-hoc UI JSON. Normalized episode `name` is the parent series name; `episodeTitle`/`episodeLabel` supply the individual episode context. Raw provider payloads are never a rendering dependency.

This is not a complete Crux app adoption. Fixtures, source delay, profile/list state, local search, Next preview sequencing, player transport and SmartCast transitions are deliberate UI simulations. Actual controllers and player capabilities require host integration. Native Tauri fetch versus browser fetch is a host capability, independent of viewport; it must not migrate into screen components. The spec records missing typed screen/action/preferences/device state rather than pretending the existing bridge exposes it.

State resets on reload, except layout/theme/host values retained in this URL. There is no server auth, account pairing, durable profile choice, queue deletion/undo, profile management, guide backend, secure TV credential storage, real source discovery, playback, cross-device transfer, or live TV control. The simple player is a control-state preview; it is not codec or transcoding evidence. No app has adopted this design revision yet.

## Artwork provenance

`public/art/` contains twelve original geometric SVG study illustrations created for this prototype (six landscapes and six matching portrait crops/compositions). They depict fictional titles and carry no third-party stills, posters, photos, logos or screenshots. They are demonstration content, not the app's production asset catalog. Production app assets remain owned by `design/assets` and its existing provenance manifest. Icons are Lucide React (ISC); React is MIT. Generated core artifacts remain governed by the core repository and dependencies. No new licensing claim is made over copied code.

## Validation

```sh
NODE_OPTIONS=--max-old-space-size=256 npm run build
NODE_OPTIONS=--max-old-space-size=256 npm test
```

The browser command needs Playwright's compatible Chromium installed. Run one browser job at a time. It reads `PROTOTYPE_URL` (default `http://127.0.0.1:4180`) and writes private visual inspection files plus result JSON under `/tmp/viptv-responsive-review`. No screenshots belong in git or release assets. See [VALIDATION.md](VALIDATION.md) for the completed scope and remaining platform checks.

Future implementation should adopt the approved composition and immutable design/core pins, not merge this prototype's simulated transport/state into an app. Keep the alternatives off production until reviewed.
