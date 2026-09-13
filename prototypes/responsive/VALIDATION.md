# Responsive VIPTV alignment validation

2026-09-13. Implements [the VIPTV alignment specification](../../RESPONSIVE_VIPTV_ALIGNMENT.md), RUI-018–021, in the existing responsive study. The measured appearance reference is the canonical design visual system and TV-web `c228fac11e8def15d0906001db467cb84936ecbe`. The proposed responsive layout remains intact.

## Final checks

- TypeScript and Vite production build passed.
- **70 Playwright Chromium checks passed**, zero page exceptions or failed requests. One browser job, 256 MiB Node heap, no emulators or Gradle.
- Eight viewport sizes × three comparison layouts × two themes: 320×568, 390×844, 768×1024, 1024×600, 1440×900, 2560×1080, 3440×1440 and 900×400.
- Desktop measured 256×144 shelf artwork, 21px bold card title, 17px context, 24px gap, uppercase shelf labels, 12px action corners and original VIPTV navigation icons. Transport icons use the TV-web 28px box to account for source padding.
- Resting graphite action → white keyboard focus → dark icon/text inversion passed. Card frame opacity switches from 0.35 to 1.0 on its artwork only; action focus clears when focus moves to the card.
- Phone measured 17/14px card typography and 12px action corners, retaining the one-row primary/My List/More arrangement and ≥48px targets.
- Original avatar assets decoded; concentric profile-ring checks passed.
- All 13 imported component/avatar assets match both ASSET_SOURCES.json hashes and the design-owned originals.
- Existing startup/Home states, source loading/cancel/error, title-logo fallback, episode source identity and cancel focus, search, library, settings, Vizio handoff/native simulation, player controls and ultrawide alignment passed.
- Design link/asset validation passed (9 required documents, 697 canonical assets). No canonical asset was modified.

## Private visual review

Inspected phone and desktop Home, the large desktop episode grid and ultrawide layout. The previous small editorial typography, circular action styling and decorative copy were replaced by the existing VIPTV component hierarchy. Header and content remain aligned; hero art is still contained; cards and episode artwork retain 16:9 geometry. The study uses fictional media, so the illustration/title-logo content is not a production-media appearance comparison.

These are explicit component measurements, not a claimed 90% full-screen image match. Native Android, Roku, real Tizen/Vizio playback, Tauri packaging/fetch and physical remote behavior were not exercised. This task changes the design study, not production app releases. Shared-core pin remains `d1897fb8fc0401368074698f6b49f1941823f5e5`; no shared logic changed.

## Build identity

Final static study archive SHA-256: `d8aead5ac551f6a4f69bbe1adcc8f3eb33f6a8a83d81ddb3ad5881441dccbc89`. Private images and test output remain outside git under `/tmp/viptv-responsive-review`. This supersedes the previous 66-check study evidence. All future app adoption must pin the design revision and provide its own platform evidence.
