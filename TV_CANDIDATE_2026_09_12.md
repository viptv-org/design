# TV implementation and joint testing checkpoint — 2026-09-12

Android TV uses native Compose in `viptv-org/android` (execution issue #3). Tizen and Vizio share React UI in `viptv-org/tv-web` (spec #1, execution #2), with AVPlay on Tizen and HTML media/backend delivery on Vizio. Backend candidate `af35a6a` adds a separate `/tv` static mount and has not been deployed. Roku runtime and production configuration are unchanged.

## Current acceptance

Shared TV web candidate `0775e4d` passed hosted [34717122751](https://github.com/viptv-org/tv-web/actions/runs/34717122751): 40 unit tests, 40 browser tests, 28 intentional platform exclusions, build and platform packaging. Browser evidence includes real Chromium WebM decoding; HTTP contracts; profile/PIN cancellation; queue hold and corrections; exact Resume identity; Discover filters; partial Search failures; managed seek/subtitle requests; same-account IPTV Next; the three-distinct-source continuation bound; and explicit failed-source Retry/manual source choice preserving position. Tests are not physical Tizen/Vizio evidence. See `tv-web/tests/PARITY_MATRIX.md` for remaining cases.

Android candidate `1a67fe9` passed hosted [34716881231](https://github.com/viptv-org/android/actions/runs/34716881231) and was installed as an update on the authorized Android 14/API 34 onn. Streaming Device 4K pro. Pairing remained intact. Real profile/data/artwork, explicit source decoding, progress with a nonempty fingerprint and Back to Sources were observed. Exact-source Resume from an isolated QA history position of 120 seconds decoded video and displayed the full title duration of 6624.896 seconds.

That device pass found two material failures: focused Home actions did not activate with remote OK, and managed playback's PAUSED position advanced as its HLS window moved. The pause began at 177.168 seconds and later exit saved 259.013 seconds without resumed playback. Timeline labels also clipped/misaligned visually. These are failed acceptance cases, not passes. Follow-on code corrects focus modifier order, captures a managed pause anchor and resumes from that exact source/position, and adjusts overlay geometry. Hosted candidate `c15c334` failed compilation on an invalid import; replacement `cd3e9fc` is building and requires physical retest. Additional track-dialog paging/focus corrections are awaiting a follow-on build.

## Remaining acceptance

Verify Android remote OK and 700 ms hold/release suppression; pause beyond a rolling HLS window; resumed and paused seek; track replacement; controlled Next/cancellation; dialog Back/focus restoration; and expanded Guide, Search, Discover, profile/avatar and Settings flows. Passing compilation or an earlier APK does not certify these changes.

Tizen packaging is an unsigned hosted launcher candidate. Samsung signing, remote-hosted AVPlay and physical remote/codec behavior require a real device. Vizio model-specific HLS/codec/track behavior also remains unverified. Transcoding is last resort; current implementations do not claim MediaBunny support.

## Test discipline

The owner deferred emulators after server OOM. Use hosted Android builds with one worker, no local Gradle/emulator. Local browser runs use one worker and a 256 MB Node heap, coordinated between agents. Keep machine access only in ignored mode-0600 `DEV.local.md`; pairing codes are temporary. Install APK updates with stable development signing to preserve pairing.

Use the dedicated temporary QA profile for playback/history changes, then stop playback and delete only its recorded owned ID while retaining all original profiles. Screenshots stay private and ignored, never in repositories or release assets. Record immutable source/run/device evidence in each app's `TESTING.md`; do not equate fixtures with device acceptance.

The existing visual and behavior specs remain normative. Design revision `8344c91` corrected extracted Resume identity to actual frozen Roku: addon ID plus a nonempty stable fingerprint. Display names and ephemeral IDs never authorize automatic Resume. Player control coordinates are relative to their row origin, as clarified in `3611564`. These extraction corrections do not change Roku behavior.
