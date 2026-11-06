# SRC-ERROR-SLATE-001 — A source that plays one still image

Status: **proposed**, owner request 2026-11-06
([app#957](https://github.com/viptv-org/app/issues/957),
[design#146](https://github.com/viptv-org/design/issues/146)).
Not implemented yet.
Source revision: app `99c88652` on `edge`: `features/player/PlayerScreen.kt`,
`features/player/TvPlayerScreen.kt`, `features/player/PlayerFallbackNotice.kt`
(the existing player notice and its **Next source** action),
`player/PlayerSurface.kt` (the platform player surfaces) and
`state/ControllerPlayerSettings.kt` (the in-player Settings visit that returns
to playback). Platform keys follow
[components.md](../../viptv-design-system/components.md)
(P phone, T TV, D desktop app and web).

## Intent

Some providers answer an expired debrid token with a playable video instead of
an error: one still image carrying a message such as "Connection expired… Ref:
permission_denied", served as the whole title. The player has no way to tell it
from a title, so the viewer watches a slate and, worse, the position it records
counts as progress in the film.

Detect that from the frames the player is already presenting, and tell the
viewer once, without touching what is playing: a notice over the picture with
**Configure source** and **Choose another source**. The player never stops,
seeks or reopens the stream by itself.

## Detection contract

Sampling only reads frames that are already on screen: no extra seek, no extra
network request, no second decode, and nothing drawn over the picture is
included.

- **When:** three samples in the first 30 s of playback, at about 2 s, 8 s and
  20 s of the source's own clock. A sample is skipped rather than taken early:
  a sample is taken only while the player is playing and the position has
  advanced at least 1 s since the previous sample. Seeking, pausing or a
  buffering stall therefore never manufactures a match.
- **What:** the presented frame scaled to 32 × 18 grayscale, and from it a
  difference hash: for each row, the 31 comparisons between a pixel and its
  right neighbour (558 bits). Subtitles, controls and the notice itself are
  separate layers and never part of the sample.
- **Rule:** a source is a probable error slate when **every** sample is
  **identical** — the hashes have Hamming distance 0, not "similar". So a slow
  scene, a still talking head, film grain or any moving pixel keeps it quiet.
  Two identical samples are enough only when the stream's bitrate is also very
  low for its resolution (under 250 kbps per megapixel, read from the player's
  own metadata); three identical samples need no other evidence.
- **Never:** it does not fire for Live (a fixed camera can hold one frame), for
  the browser and iOS players (a cross-origin `<video>` frame cannot be read
  and AVPlayer has no frame-output path here — see [Parity](#parity)), while the
  player is paused, buffering, opened over an error, or within 10 s of a seek.
- **Cost:** one sample must stay under one decode-time frame. Measured at app
  `fix/957-error-slate-detect` on this host: D 0.15 ms per sample (0.9 % of a
  60 Hz frame) with no dropped frames in a 24 s run; T/Android 1.2–6.8 ms of
  GPU capture and 0.13–1.4 ms of main-thread CPU per sample on the software-GPU
  emulator, no extra decode and no extra seek. The figures and their method are
  in [app#957](https://github.com/viptv-org/app/pull/957).
- **Once:** one notice per source per player session. Changing source, or
  replaying the same source after choosing another one, may show it again.
- The notice says "might" because the evidence is probabilistic: a title that
  really is one still image for its first 20 s is reported the same way.

## The notice

One notice at a time, in the player's own notice position
([components.md §9](../../viptv-design-system/components.md#9-feedback)) and
never over the controls' own transport row.

Copy ([copy.md](../../viptv-design-system/copy.md#error-slate-notice-src-error-slate-001)):
**This source might not be working.**, the add-on line
**[Add-on] handed back this video. Its settings may need a new key.**, and the
actions **Configure source** and **Choose another source**.

- The add-on line names the provider that served the playing source. With no
  provider name the line reads
  **This source's settings may need a new key.** and **Configure source** opens
  Settings › Add-ons.
- **Configure source** opens Settings › Add-ons, the section where the add-on
  is installed, and returns to the player afterwards (the same in-player
  Settings visit as **Subtitles & audio settings**). Playback pauses there and
  resumes where it was, as it already does for that visit.
- **Choose another source** opens the source picker for this title, at the
  current position, exactly as the failure page's **Choose another source**
  does. Picking a source closes the notice; backing out of the picker returns
  to playback with the notice still up.
- Neither action stops playback. The notice is not modal, does not scrim, does
  not dim the picture and does not take focus by itself.

### Geometry and timing

| | Placement |
|---|---|
| P, tablet | Bottom centre, above the control layer, 16 from the side edges, max 650 wide, radius 12, `color.surface.2` at 0.86 |
| D | Bottom centre, 24 from the bottom edge and above the transport bar, max 560 wide, radius 12, `color.surface.2` at 0.86 |
| T | Bottom centre, above the transport bar (bottom 132 × scale), max 1100 × scale, radius 12 × scale, `color.surface.2` at 0.82 |

The title line is `color.text` (T: 26 × scale; D 14; P 13), the add-on line
`color.text.secondary` on the next line, and the actions sit under the copy:
**Configure source** as the quieter action, **Choose another source** as the
one filled action. On T both are 64 × scale tall, focusable, and reached with
Down from the controls; the notice is drawn whether or not the control layer is
showing, so the viewer can act without waiting for it.

It stays 30 s of playback, then leaves on its own. It also leaves at once when
the viewer chooses another source, the title ends, the player closes, or the
source fails. It does not reappear for that source in the same session, and it
never queues behind another notice: it is the only player notice shown while it
is up (an audio-language notice and a seek notice wait, and a newer audio
notice replaces nothing while it is visible).

Announced once to assistive technology when it appears (polite live region):
"This source might not be working. Configure source. Choose another source."

## Acceptance

1. A static slate of at least 25 s (one image, low bitrate) shows the notice at
   about 20 s; playback continues, the timeline keeps running and the notice
   leaves after 30 s.
2. A normal title never shows it: moving picture, a slow scene and a still
   talking head all keep the samples different.
3. Two identical samples with a low bitrate for the resolution show it at about
   8 s.
4. **Choose another source** opens the picker at the current position; picking
   a source closes the notice and plays; backing out keeps the notice and the
   position.
5. **Configure source** opens Settings › Add-ons with the player behind it;
   Back returns to the player at the same position, paused→resumed as today.
6. Live, web and iOS never show it; a paused player, a seek and a buffering
   stall never produce a sample.
7. On T the notice is reachable with Down from the controls and never takes
   focus when it appears; on P and D it is drawn above the control layer and
   its buttons are 44 tall.
8. Nothing about playback changes on its own: no seek, no source change, no
   pause, and no progress is written for a timestamp that was never decoded.

## Parity

| Platform | Detection | Notice | Evidence |
|---|---|---|---|
| T (Android TV), P (Android phone and tablet) | `PixelCopy` of the presented video surface into a 32 × 18 bitmap | yes | app#957: emulator `emulator-5580` cost run; the detector's clip tests are desktop tests |
| D (desktop app) | the frame the mpv renderer already handed to the UI | yes | app#957: mpv software render path cost run |
| Web | none: a cross-origin stream taints the canvas, so its frames cannot be read | no | — |
| iOS | none: AVPlayer has no frame-output path in this app | no | — |

Not device-verified on a physical TV or phone: the Android figures come from
the software-GPU emulator, which is the only Android evidence recorded so far.