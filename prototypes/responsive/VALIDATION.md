# Responsive study validation

Validation applies to this branch's fictional browser study only. The final build and browser run passed on 2026-09-13. It does not qualify a Tizen/Vizio decoder, Android/Compose rendering, Tauri transport, SmartCast hardware, or an existing app release.

The automated browser checks use one Chromium instance sequentially, with a 256 MiB Node heap. No emulator, Android build, Gradle daemon, Rust rebuild or real TV command is part of this validation. Viewport dimensions are CSS pixels, not a claim about device pixel density.

Expected coverage: seven viewport sizes × three hero variants × two appearance themes; real Rust fixture initialization; explicit landscape hero; 16:9 cards; token equality; no page horizontal overflow; profile selection outline; source spinner/cancel/error/retry; web native-app handoff; native pairing/rejected PIN/launch failure/retry/acknowledgement/remote; simulated seek/captions/Escape focus return; local shelf navigation; context-menu shortcut; next episode identity; all principal study routes at phone/short desktop/desktop sizes; Home loading/empty/error/missing-art.

Private browser images are inspected for typography, contained artwork, wrapping, card geometry, profile ring alignment and reachability. They are not committed and are not a measured Roku similarity score.

## Final results

- Clean dependency install from the committed lockfile: passed (28 packages; no inherited TV-web dependencies).
- TypeScript and Vite production build: passed.
- Playwright Chromium: **56 checks passed**, zero page exceptions or failed requests, against the static LAN build.
- Viewports: 320×568, 390×844, 768×1024, 1024×600, 1440×900, 2560×1080 and 900×400; each tested with A/B/C and Cinema/OLED.
- Full design link/asset validator: passed, 9 required documents and 697 existing asset files.
- Vendored core artifact hash verification: passed for all five files.
- Private visual review: A at phone/desktop/ultrawide, B at narrow phone/short desktop, C at desktop, profile chooser and Vizio launch-acknowledgement remote sheet. Artwork is contained; phone navigation and modal actions remain reachable; the avatar's ring is centered on its circular surface.

Browser inspection found and corrected a Linux font fallback resolving to monospace, collapsed-navigation accessible names, hidden-art CSS precedence, and normalized episode titles being mistaken for episode names. Next preview now shows the actual S1 E4 episode context while retaining the parent series title. These corrections are part of the final successful build.

## Build identity

The final static study archive SHA-256 is `ca5ca9cdb03be7abea9161420f3fcefc5b26e98ecac253494901abcf9cc9a70f`. Screenshots, archive and output logs remain outside the repository.

## Remaining checks before adoption

A is the recommended starting direction: contained landscape artwork and separate copy stay readable without depending on window aspect ratio. B trades artwork prominence for density and gives narrow copy more wrapping; C puts the queue first. The alternatives are available for owner review, not automatically selected production variants.

These checks do not measure 90% Roku visual parity; responsive layouts deliberately adapt the shell while retaining shared cards and semantics. No Android renderer, device font scale, real touchscreen, mobile Safari, native Tauri window/secure fetch, physical TV remote, AVPlay decoder, Vizio Conjure, or real-media codec path was tested. Platform-specific acceptance and the unimplemented screen inventory remain explicit in RESPONSIVE_UI.md. All future clients must resolve the typed data/action gaps and record their own design pin plus runtime evidence.
