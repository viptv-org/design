# Design changes

## 2026-09-13 — Responsive study revision after owner review

Replaced the detached desktop sidebar with content-aligned top navigation, adopted the existing transparent viptv wordmark and core-projected title logos, replaced small episode rows with large landscape cards, and rebuilt phone action groups as primary / My list / More. The supplied Behance detail reference informed hierarchy and affordances while VIPTV colors/cards and contained artwork remain. RUI-014–017 specify geometry, logo fallback, source/episode identity and return behavior. Core title-logo contract and generated bridges are additive; the study remains off-main and simulated.

## 2026-09-13 — Proposed responsive UI and OLED contract

Added [RESPONSIVE_UI.md](RESPONSIVE_UI.md): a proposed responsive mobile-web/Tauri desktop contract aligned to the unadopted responsive study. It specifies ordinary vertically scrolling documents, contained `heroImage` artwork without CSS backgrounds or gradients, A/B/C feature variants, study-derived card/type/gap/breakpoint/OLED tokens, current wire mappings and typed gaps, future screen/input/error/return inventory, and proposed acceptance. Android mobile remains Compose. It specifies Android/Tauri-only Vizio SmartCast pairing and Conjure launch of hosted VIPTV, with honest browser limits: no mirroring, casting, native app installation, or playback-confirmation claim. Added versioned responsive tokens and a browser study with 56 passing checks, plus explicit per-platform adoption/persistence/window/input rules. The study simulates sources, profiles, playback, SmartCast, mutations, and persistence; no platform adoption, screenshot, parity, or physical-device evidence is claimed.

## Initial extraction — 2026-09-12
Captured the Roku baseline at vynxc/viptv@7d6b413 and established design-first cross-platform governance. This changes repository ownership, not Roku behavior. Android-only imports and proposed platform adapters are tracked separately from current Roku behavior.

## Baseline precision audit
Added exact dynamic guide geometry, search debounce/focus/partial-failure behavior and server-owned queue completion/cache rules. These clarify existing behavior without changing it. Source citations use the published split runtime snapshots.

## TV platform implementation
Authorized Android TV Compose and one shared Tizen/Vizio React frontend, with platform playback modules and design-based visual/remote testing. The baseline UX is preserved; host exit and on-screen keyboard equivalents are documented in TV_IMPLEMENTATION.md.

## 2026-09-12 TV implementation candidate

Added the Android TV/shared Tizen-Vizio implementation checkpoint and owner-requested deferred joint testing. No Roku behavior or visual contract changed.

## 2026-09-12 — Resume identity extraction correction

Corrected the behavioral contract from addon plus human source name to addon plus nonempty server-authored source fingerprint. `Util.brs:45–59` at the frozen Roku revision already requires fingerprint equality. This repairs an extraction error; it does not change Roku or introduce a new UX. Added same-name/different-fingerprint and legacy missing-fingerprint acceptance cases.

## 2026-09-13 — Shared TV-web rebuild and design synchronization

Authorized the Roku-matching presentation replacement for the shared Tizen/Vizio frontend. TV_WEB_UI_REBUILD.md indexes complete screen/state acceptance against the existing normative visual and interaction specs without duplicating geometry. DESIGN_SYNC.md defines immutable design adoption, vendored snapshot/asset integrity, separate freshness checks and per-platform parity evidence. Figma-first authoring is proposed for a future explicit adoption decision; the versioned design repository remains authoritative. No completed visual or device acceptance is claimed here.

## 2026-09-13 — Rail and action alignment extraction precision

Corrected the rail origin, row spacing and V-mark geometry from frozen Roku MainScene.xml, and made ActionRow horizontal/vertical centering explicit for Settings. These are source-backed extraction corrections, not Roku changes. Documented the shared TV-web existing source-quality filter as a retained implementation adaptation with explicit acceptance and parity limits; no owner-approved exception or completed parity is claimed.

## 2026-09-13 — Shared TV rebuild delivery

Recorded the shared React replacement, scoped 43-unit/49-browser validation, Settings/Search comparisons, source-filter difference, and immutable sync/PR workflow in [TV_WEB_UI_REBUILD.md](TV_WEB_UI_REBUILD.md). Physical TVs and other matched-content visual states remain pending.
