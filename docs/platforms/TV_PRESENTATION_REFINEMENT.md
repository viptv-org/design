# TV-PRESENTATION-114 — Sharp artwork, loading and controls

Status: owner-approved direction, proposed until implementation qualification.
Source revision is the design commit introducing this section. Implementation:
[tv-web #114](https://github.com/viptv-org/tv-web/issues/114). Applies to the shared
browser/webOS/Tizen and native Roku hosts. This scoped refinement supersedes older
Home preview blur, full-screen artwork and loading-copy requirements; other screens
and platform contracts retain their existing behavior. Private captures are review
evidence only and are not packaged assets.

## Home and Continue Watching

In the 1920×1080 frame, sharp landscape artwork occupies x480, y0, 1440×810.
Use cover fitting with a 1440×810 hero decode and a 960×540 focused-preview decode,
scaled by the existing device image-pixel policy; request no blur.
The left title area remains page ground through x760 and fades smoothly to clear
at x1520. The lower mask fades from clear at y350 to page ground at y810. Compose
these masks once below the foreground logo/text. Do not dim clearlogos or display
a hard image edge. Detail artwork keeps its separate mask.

Retain coherent prepared artwork and metadata through slow loads; late responses
cannot paint over another title or route. Missing/failed art leaves the page ground
and usable title/actions. Preserve the existing bounded shelf/card pools, focus
memory, scroll restoration and current hero rotation policy.

The current hero marker is a 48×4 high-contrast segment, with at least 6px of visible
selected fill while running and full fill when parked. Inactive segments are 16×4.
Use ordinary renderer geometry with bounded update work, including on native Roku
and Canvas; selection must not depend on a WebGL-only shader. The vertical row
marker is 4px wide at x1848, outside the card viewport ending at x1824. Its 220px
column follows the shelf but is clamped to y806, retaining a 54px bottom margin.

## Detail and source loading

Pending detail content uses placeholders matching the reserved title/logo,
metadata, synopsis, actions and episode/recommendation slots. Select movie/series
geometry from the known title kind. Do not flash a Loading label or a previous
title's content. Placeholder animation is a restrained shared opacity pulse;
reduced motion uses a static state. Stop animation/timers on completion or exit.
There is no artificial minimum loading delay. Real failures retain retry and Back.

Source preparation uses the current title's sharp right-side artwork over dark
ground, a centered 800×180 logo/title slot at x560,y250 and a 56px progress indicator
centered near x960,y540. Prefer a valid clearlogo, with the title immediately
available as fallback when absent, pending or failed. Keep the slot stable and
never wait for art before starting video. Normal opening needs no redundant
Loading/Opening text; retain **Press Back to cancel**. Discovery, failure and retry
remain truthful states. Hide the source drawer visually during opening while
retaining its logical selection for failure/cancellation recovery. Late results
cannot reopen a cancelled attempt; release admitted playback resources exactly once.

## Player controls and input

Play/Pause and adjacent Audio & subtitles/Source controls share 56px height,
22px icons and 12px inter-button gaps. Play begins at x96 with 160px width, so the
next control starts at x268. Preserve existing labels and capabilities; do not
expose unavailable actions to achieve a symmetrical row.

One distinct Back press dismisses the innermost menu, then visible controls while
playback continues, then exits playback when neither is open. Held/repeated Back
must not cascade through these levels. Support native **Back**, Escape and existing
platform equivalents. During a managed seek, Back may dismiss chrome without
discarding the in-flight seek. Loading/buffering progress is separate from chrome
visibility and cannot force dismissed controls back onscreen. Source-opening Back
cancels that attempt. Actual exit retains lease cleanup and return-focus behavior.
Other directional, OK, release and 700ms hold/context actions retain their contracts.

## Acceptance

- Inspect bright/dark art, missing/failed logos and slow/stale responses in WebGL,
  Canvas and the native host; text/marker contrast must remain readable.
- Traverse first/last shelves and hero; marker never overlaps cards or exits the
  viewport. Returning preserves selected card and scroll.
- Delay movie and series detail responses: only correctly placed placeholders
  appear, with static reduced-motion rendering and no Loading-text flash.
- Select a source with/without a logo; verify stable centered preparation, no drawer
  bleed, immediate playback eligibility, cancellation and failure recovery.
- During playing, buffering and seeking, verify rendered controls disappear on
  Back while the video/session continues. Repeated-key events do not exit; the
  next distinct Back after chrome dismissal exits and releases the session.

Record screenshots privately and browser/native-build/device evidence separately.
No frame-rate or physical-device qualification follows from this specification.
