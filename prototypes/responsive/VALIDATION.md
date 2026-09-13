# Responsive study validation — owner-feedback revision

Validated 2026-09-13. Applies only to this off-main interactive design study, using fictional media and simulated playback/SmartCast.

## Results

- TypeScript and Vite production build: passed.
- Playwright Chromium: **66 checks passed**, zero page exceptions or failed requests. The intentional malformed-logo fixture returns HTTP 200 and verifies visible text fallback.
- Matrix: eight viewports × three Home variants × two themes (48 combinations): 320×568, 390×844, 768×1024, 1024×600, 1440×900, 2560×1080, 3440×1440 and 900×400.
- Existing source/loading/cancellation/error/retry, profile ring, search/empty state, Vizio handoff/native simulation, playback controls, keyboard/context menu, episode identity and principal-route checks passed.
- New checks: header/main left edge and width match at 3440px; no sidebar margin; transparent title logo and accessible heading; desktop episode art ≥260px and 16:9; three mobile actions on one row with ≥48px targets across A/B/C; large swipeable episode cards; third-episode identity and cancel focus restoration; failed-logo text fallback.
- Design link/asset validator: passed (9 required documents, 697 existing assets).
- Copied core artifacts: all five hashes passed. Core `d1897fb8fc0401368074698f6b49f1941823f5e5` passed its 36 Rust tests, WASM contract checks, strict Clippy, formatting and TypeScript validation separately.

One browser job and a 256 MiB Node heap were used. No emulator, Android/Gradle build or real TV/media command ran. The shared-core additive field was compiled with one Cargo job; Kotlin/TypeScript interfaces and WASM were regenerated.

## Visual inspection

Private images were reviewed at 3440×1440 and phone sizes for the centered header, transparent title mark, clean action grouping and larger episode art, plus the desktop episode grid. Navigation now shares the bounded content frame rather than occupying the far left of an ultrawide display. Phone actions use the single pill/circle group. Episode source cancellation returns focus by stable episode ID after the series detail remounts.

The supplied Behance images were viewed privately to identify action hierarchy and title/episode presentation. No reference screenshot, movie still or reference branding is packaged. The study uses original fictional SVG illustrations/title logos and the unchanged design-owned transparent viptv wordmark.

## Build identity and limitations

Final study archive SHA-256: `51879fdc64ddb1ddc9c2cced74cac7993b100011aafdd6b807c9fb50bdc070dc`. Private visual evidence and test JSON are under `/tmp/viptv-responsive-review`, outside git. This supersedes the first study's 56-check result; both remain limited browser evidence.

The shared core now exposes title logos, but the other application repos have not adopted this new pin. Android/Compose rendering, native Tauri fetch/window behavior, mobile Safari, physical TV input, AVPlay/codec playback and actual Conjure remain unverified here. This is not a Roku similarity percentage or production release. Adoption still follows the immutable design/core pin and platform evidence process in RESPONSIVE_UI.md and DESIGN_SYNC.md.
