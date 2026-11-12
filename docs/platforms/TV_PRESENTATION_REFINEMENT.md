# TV-PRESENTATION-114 — Sharp artwork, loading and controls

Status: owner-approved direction, proposed until implementation qualification.
Source revision is the design commit introducing this section. Implementation:
[tv-web #114](https://github.com/viptv-org/tv-web/issues/114). Applies to the shared
browser/webOS/Tizen and native Roku hosts. This scoped refinement supersedes older
Home preview blur, full-screen artwork and loading-copy requirements; other screens
and platform contracts retain their existing behavior. Private captures are review
evidence only and are not packaged assets.

For TV-web, the owner-approved TV-PRESENTATION-133 amendment below supersedes
the Home preview composition and pending-logo rules where stated. Other clients
retain their existing adoption and qualification status.

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

## TV-PRESENTATION-133 — Coherent branding and preview composition

Status: owner-approved TV-web direction, proposed until implementation
qualification. Source: [tv-web #133](https://github.com/viptv-org/tv-web/issues/133).
This is a scoped amendment to TV-PRESENTATION-114, not an unrelated design-pin
or cross-platform migration. Existing copy, focus order, release/700ms hold,
navigation, source intent and return-focus contracts are unchanged.

### Branding layout and readiness

Home shelf previews use one common branding origin for the logo, metadata and
synopsis. Moving between Continue Watching and portrait shelves moves that whole
layout coherently, including while replacement artwork is pending. The logo slot
is 640×120 at x96. Its y coordinate is
`max(96, 132 + max(0, shelfTitleY - 40 - 132 - 310) / 2)`; metadata begins 144px
below that origin and synopsis 194px below it. Current and retiring logos follow
the same target geometry, leaving at least 24px before metadata throughout motion.

Movie and series Details both compact their branding when focus enters episodes,
seasons or More Like This. The compact logo fits 220×68 at (96,54); a movie must
not leave its full 640×190 logo over the upward-moving metadata, synopsis or Play
button. The normal movie and series logo boxes remain 640×190 at (96,220) and
640×134 at (96,250). Existing movie body/list offsets and series episode/synopsis
visibility remain intact. Use a shared 220ms ease-out layout transition for logo
position/scale and corresponding summary/list movement. Reduced motion applies
the final geometry immediately. Reuse the prepared logo pixels during layout
motion rather than loading or rasterizing each intermediate size.

On Home and Details, a supplied but pending logo reserves its branding slot;
do not substitute the title merely because its pixels have not arrived. Title
text appears when no logo exists or loading has definitively failed. Preserve
the existing movie/series detail skeleton and restrained shared shimmer while
detail data is unavailable. There is no minimum loading delay, new loading copy
or navigation gate. Late callbacks cannot restore another title, route or scope.

### Artwork composition and cost

Non-Continue portrait/poster previews use a full-width 1920×1080 background
blurred through the existing image proxy with blur 8 and a 960×540 preview
decode, scaled by the device image-pixel policy. Keep the separate sharp
240×360 poster at (1584,144). Do not apply CSS, canvas or per-frame blur.

Featured and Continue/single-landscape previews retain the sharp clipped
right-side viewport at (480,0), 1440×810, and the existing black copy/lower mask.
Enlarge the image content by 4/3 inside that viewport: a centered 1920×1080 image
at local (-240,-135), clipped to the viewport. The visible subject grows about
one third while the rendering footprint and black branding ground remain stable.
Use cover fitting, no proxy blur, a bounded 1440×810 hero decode and a 1280×720
focused-preview decode. Detail's existing full-width composition stays unchanged.
Keep only the current/incoming presentation and existing bounded shelf/card pools;
no persistent bitmap cache or animation-loop image work is added.

### Acceptance for the amendment

- Traverse movie and series Details into/out of More Like This; synopsis and
  actions never paint over branding at the start, middle or end of motion.
- Traverse Continue Watching ↔ My List/portrait shelves with cached and delayed
  artwork. Both fading logos follow the same geometry as the summary; reverse
  direction before completion and retain the correct title and focus.
- Delay a supplied logo on first Details entry: its title is absent until actual
  logo failure, while a missing/failed logo has the ordinary title fallback.
  Existing data skeleton/shimmer and cancellation remain correct.
- Inspect actual proxy requests and private subject/text captures in WebGL and
  Canvas at 1920×1080 and 1540×754. Only portrait previews request blur 8 and a
  full-width background; single-image content is enlarged inside its right clip.
  Branding contrast, poster separation, reduced motion and bounded decode sizes
  remain correct. Browser evidence does not qualify physical firmware.

## TV-RESUME-135 — Authoritative saved time

Status: owner-approved shared TV direction, with implementation qualification
recorded by [tv-web #135](https://github.com/viptv-org/tv-web/issues/135) and
[backend #316](https://github.com/viptv-org/backend/issues/316). This changes
presentation, not history, source selection or playback intent. No new assets,
design-pin migration or unrelated-client adoption is required.

Continue Watching captions and Details omit `minutes left`, `seconds left` and
the corresponding remaining-time line. Keep typed episode coordinates, progress
bars, watched/rewatch facts and the ordinary metadata runtime. The player's
timeline clocks are unchanged.

The primary resume action reads **Resume at M:SS** below one hour and
**Resume at H:MM:SS** at or above one hour. Use the winning saved record's
positive millisecond position, flooring only the displayed seconds. A positive
subsecond position displays **Resume at 0:00** but retains its precise admission
position. Never multiply progress by a catalog runtime to invent display time.
An explicit absent/zero position uses the ordinary **Play** label. Next and
restart retain their existing Play/episode copy; restart stays at zero.

A fresh resolved action takes precedence over stale Home presentation. While
the action is pending, a known authoritative Home clock may supply its label;
an older server without that clock may retain plain **Resume**. A late result
from an obsolete title/profile cannot change the current action or admission
position. Explicit seek/retry positions and source replacement clocks retain
their existing ownership and take precedence over saved-position updates.

Keep the action height and typography. Resume controls use at least 360px width
in the 1920px reference frame and may grow to at most 520px to fit their label;
the adjacent My List control remains 20px after the action edge. The progress
bar follows the action width. Preserve the detail skeleton/shimmer, branding
motion, focus order, press/release/repeat/700ms hold and Back/return behavior.

Acceptance covers subminute, hour and subsecond positions; absent or mismatched
metadata runtime; no saved position; explicit restart/Next; specials/absolute
episode coordinates; active rewatch; stale Home versus fresh action; exact
admission seconds; no remaining-time copy and unclipped labels in Canvas and
WebGL. Physical firmware and other-client adoption remain separate evidence.

## Acceptance for TV-PRESENTATION-114

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
