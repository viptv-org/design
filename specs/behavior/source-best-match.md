# SRC-BEST-MATCH-001 — Best match source autoplay, ranking and fallback

Status: proposed, 2026-10-22; amended 2026-10-26 (Best matches group,
[design#20](https://github.com/viptv-org/design/issues/20)). Not implemented; no
device evidence.

Source revisions: design `fd43d6beed0c4800f77d4c770d9d8375311193b6`; app
`48bcefa97d451f862dad9c5b94bad3764b18f8f4`; backend
`ea311c3b9ce94b4f07de9823850ba7d7e9f4aed7`; the 2026-10-26 amendment also cites
app `f268625`. Prior art and citations:
[workspace research note](https://github.com/viptv-org/workspace/blob/main/docs/research/source-autoplay.md).
Owner decisions recorded 2026-10-22: any list navigation cancels autoplay; early
start with a visible countdown; one audio preference for every title type (no
anime override); automatic fallback to the next source, at most three attempts;
WEB and BluRay releases preferred; HDR/Dolby Vision preference exists but is off
by default. Owner request 2026-10-26: "the source selector should first sort by
our preference ranking system as a batch named something" (see
[Source groups](#source-groups-best-matches-and-all-sources)).

## Intent

A profile whose source selection is **Best match** presses Play and gets the
source it would most likely have chosen itself: playable on this device, in the
audio it asked for, from a good release, without waiting for the slowest
provider. **Always ask** is unchanged: nothing starts on its own. In both
modes ranking orders the list, groups it under **Best matches** and **All
sources**, and marks the first Best matches row **Best match** (see
[Source groups](#source-groups-best-matches-and-all-sources)).

## Baseline being replaced (app `48bcefa`)

- Autoplay waits until every provider finishes, then plays the top ranked row;
  if providers hit the one-minute ceiling it plays nothing
  (`ControllerCatalog.kt:229`).
- Only an activated row, Back or navigation cancels it; moving through the list
  does not.
- Ranking keys are quality-cap class, preferred-audio match, then height
  (`rank_sources` in the shared engine). `Original` audio means no language
  ranking. Release type, HDR/DV, dub/dual-audio, torrent health and device
  decode support are not considered, so a 4K Dolby Vision release can autoplay
  on a TV that cannot decode it.
- A failed start shows the error screen; there is no automatic next attempt.
- The picker lists rows in provider arrival order while discovery runs, then
  replaces the whole list with the ranked order once every provider finishes
  (app `f268625`, `ControllerCatalog.kt:227-236`). There are no groups, and the
  live picker never sets the Best match tag (`SourcesScreen.kt:33`; only the
  preview fixture shows it). Initial TV focus re-anchors to the top row when the head changes unless the viewer
  already moved (`TvSourcesScreen.kt:71`).

## Entry and exit

Entry: Play/Resume-with-new-source, an episode activation, or a next-episode
activation on a profile with `source_selection = "best"`. The Sources picker
opens as today and discovery streams rows into it.

Exits: playback of the chosen row; cancellation, which leaves the viewer on the
populated picker with focus where the cancelling action put it; Back, which
behaves exactly as Back on the picker does today; or exhausted fallback, which
leaves the viewer on the picker with failed rows annotated.

Exact-source Resume (same source as last time) and controlled next episode keep
their existing narrowly defined paths and do not use this countdown.

## Countdown

1. While discovery runs, rows are ranked continuously (below) and grouped as
   [Source groups](#source-groups-best-matches-and-all-sources) describes. Rows
   failing a hard filter never become the autoplay target.
2. The countdown starts as soon as one **early-start eligible** row exists:
   it passes hard filters, is in the best language tier for the profile, is
   within the quality cap, and its decode class is *supported* or *unknown*.
3. Countdown length is 3 s. If a better ranked eligible row arrives, the target
   switches and the countdown restarts, but never past the **hard deadline**.
4. Hard deadline: 20 s after discovery started. At the deadline, or when all
   providers finish (whichever is first), with no countdown running, a 3 s
   countdown starts for the best row surviving hard filters, eligible or not.
   With no survivor, nothing starts; the picker stays as today.
5. When the countdown reaches zero the target plays, exactly as if activated.

Copy (above the list, in the Source discovery status position):

- `Playing best match in 3` (counts 3, 2, 1), with the target's facts beneath it:
  `[quality] · [provider] · [release type] · [audio]`, for example
  `1080p · Torrentio · WEB-DL · Dual audio`. Unknown facts are omitted.
- Buttons: **Play now** (starts the target immediately) and **Cancel** (stops
  autoplay; picker stays).

Layout: not drawn on the canvas yet. **Needs a board** on TV, phone, tablet,
desktop and web before implementation; until then the strip reuses the
Source discovery status position and the standard button styles. Reference
coordinates are unknown.

Focus: the strip does not take initial focus; the first row keeps it as today.
On TV the strip's buttons are reachable with Up from the first row.

### What cancels the countdown

Any viewer-initiated action in the picker: any D-pad or arrow-key press (Up,
Down, Left, Right), a list scroll by touch, wheel or keyboard, activating a
row, **Cancel**, changing a provider or quality filter, opening Source details,
Back, or leaving the screen. **Play now** does not cancel; it plays.

Not cancelling: initial focus placement, rows arriving or re-ranking, pointer
hover without a click, window focus changes. A cancelled picker never restarts
autoplay for this discovery.

Accessibility: announce `Playing best match in 3 seconds. Press any key to
cancel.` once when the countdown starts and `Best match cancelled` on cancel;
do not announce every tick.

## Ranking

Rows are normalized once at ingestion (next section); ranking reads only the
structured fields, never display labels.

### Hard filters (autoplay and grouping)

These rows are never an autoplay or fallback target and never join the
**Best matches** group. In the list they remain visible and sort after every
other row:

- Camera, telesync, telecine, screener and R5 releases.
- 3D releases.
- Decode class *unsupported* (device reports it cannot decode the video codec,
  profile or resolution).
- Torrents reporting fewer than 5 seeders. Torrents with an unknown seeder
  count are not filtered.

### Order (each key breaks ties of the previous one)

1. **Decode class:** supported, unknown, risky. *Risky* is a Dolby Vision
   release without an HDR10/SDR base layer on a device without a Dolby Vision
   decoder, or a codec the device decodes only in software at this resolution.
2. **Language tier** (below).
3. **Quality cap class:** within cap, unknown height, over cap. With no profile
   cap the device's maximum decodable height is the cap.
4. **Series memory:** for an episode, a row from the same add-on binge group as
   the last successfully started episode of this series on this profile ranks
   first within its tier.
5. **Resolution:** highest first, within the cap.
6. **Release type:** WEB-DL and BluRay encodes; WEBRip; unknown; BluRay remux;
   HDTV, DVD and other rips. Remux sits below because its size makes starts
   slow; it is not filtered.
7. **HDR/Dolby Vision preference:** applies only if the profile changed it from
   **No preference**. *Prefer* ranks HDR10, HDR10+, HLG and decodable Dolby
   Vision first; *Avoid* ranks SDR first.
8. **Delivery:** direct HTTP(S) (including debrid) before torrents; among
   torrents, more seeders first.
9. Provider order, then arrival order (stable).

### Language tiers

The profile has one **Preferred audio** setting for every title type:
**Original language** or a specific language *L*. The title's original
language comes from its metadata (TMDB `original_language`); when it is
missing, **Original language** behaves as no language preference.

For requested language *L* (or the original language *O*):

| Tier | Release evidence |
|---|---|
| 1 | Audio languages explicitly include it. |
| 2 | Dual or multi audio whose listed languages do not include it, or list none (one track is usually the original). For a language other than *O*, also a **Dubbed** flag with no listed language. |
| 3 | No language evidence at all. When the requested language is *O* (chosen as **Original language** or named explicitly) this ties with tier 1, because most unmarked releases carry original audio. |
| 4 | Explicit languages without dual/multi audio that exclude it; for a requested *O*, also a **Dubbed** flag without dual/multi audio. Dual/multi audio always takes precedence over **Dubbed**, because PTT (and therefore Torrentio) marks every dual-audio release dubbed. |

Absence of a marker is never read as a specific language on its own; it is
original-language evidence only through the tier 3 rule. Some add-ons hide
English when it is the only language, and Torrentio removes Japanese from
anime language lines, which is why dual/multi audio never falls to tier 4.
Subtitle languages are never audio evidence.

After the source opens, the player selects the audio track in the preferred
language when the file has one (existing behaviour). If the file's actual
tracks contain no track in the requested language, show the notice
`This source has no [language] audio.` with **Next source** during a Best match
session, or with no action otherwise; playback continues.

## Source groups: Best matches and All sources

Applies to every source-selection mode (Best match and Always ask) and every
surface (TV, phone, tablet, desktop, web).

Rationale: the ranking above already decides which sources the viewer would
most likely pick. Showing its top rows as a named group lets a viewer on
**Always ask**, or one who cancelled a countdown, choose from a short trusted
set without reading the whole list. Ranking while rows arrive, rather than
reshuffling everything when the last provider answers, keeps the list from
jumping under the viewer at the moment they are likely to act. Owner request
2026-10-26 ([design#20](https://github.com/viptv-org/design/issues/20)).

### Membership

Group membership is computed over every row of this discovery, before the
provider and quality filters:

1. **Best matches:** the top-ranked rows that pass every
   [hard filter](#hard-filters-autoplay-and-grouping), at most **5**, in
   ranking order. Its first row carries the existing **Best match** marker
   (accent eyebrow).
2. **All sources:** every other row, in ranking order. Rows that pass the hard
   filters but rank below the fifth come first; hard-filtered rows come last,
   as the ranking already places them.

The provider and quality filters then hide rows in both groups without
changing membership. A row's group and the Best match marker therefore do not
depend on the filter: with a filter that hides the first Best matches row, no
visible row carries the marker. Fewer than five rows passing the hard filters
gives a shorter Best matches group; none gives an empty one.

### Headers

- A header labels each group: `Best matches` above the first group, `All
  sources` above the second (copy in `viptv-design-system/copy.md`).
- A header shows only while its group has at least one visible row. When
  Best matches has no visible row (empty, or every member filtered out) both
  headers hide and the list looks like a single ranked list. When All sources
  has no visible row only the Best matches header shows.
- Headers are part of the scrolling list, not sticky. They use the group label
  style of the desktop settings Section nav (uppercase, secondary text) in the
  list's text column. Header height, spacing and the TV/phone geometry are
  unknown: **needs a board** on every surface (open items). Until then the
  header must not change source row height (SRC-OVERFLOW-001).
- Headers are not focusable on TV or by keyboard and are not activatable by
  touch or pointer. Up/Down moves directly from the last visible Best matches
  row to the first visible All sources row and back. When focus moves to the
  first visible row of a group, the list scrolls so that group's header is
  visible too; at the top of the list the Best matches header is visible.
- Accessibility: each header is exposed as a heading (Android semantics
  `heading()`, web `role="heading"` level 3 or an `h3`), so screen reader
  heading navigation lands on it. Header changes are not announced on their
  own; the existing polite discovery status announcements are unchanged.

### Progressive ranking

1. Rows are ranked and grouped as they arrive. Every provider response is
   merged into the ranked list at the rows' ranked positions in one update; the
   list is never shown in arrival order and never reshuffled as a whole when
   discovery finishes.
2. An arrival can move rows between groups: a better row entering Best matches
   pushes its fifth row to the top of All sources. Rows can also move within a
   group.
3. **Initial placement:** until the viewer navigates in the list (any D-pad or
   arrow press, touch/wheel/keyboard scroll, or a filter change), focus on TV
   and keyboard surfaces stays on the first visible row, and phone, tablet and
   pointer lists stay scrolled to the top. A better row arriving there takes
   the first position, the marker and the initial focus. This is initial focus
   placement, so it does not cancel a countdown. If the picker opened with a
   selected row (the source currently playing or last chosen), initial focus
   goes to that row instead, as today.
4. **After the viewer navigates (TV, desktop/web keyboard):** focus stays on
   the same source, identified by its stable row identity, never by index,
   while rows are inserted or moved around it and even when it changes group.
   The list scrolls so the focused row keeps its on-screen position where the
   list length allows; otherwise the minimal scroll keeps it fully visible.
5. **After the viewer scrolls (phone, tablet, pointer):** the scroll anchor is
   kept: the first fully visible row keeps its on-screen position while rows
   are inserted or moved above or below it. If the anchor row itself moves,
   the list keeps the row that replaced it at that position, so the visible
   rows do not jump. A touch in progress (drag or fling) is never interrupted.
6. **Selected row:** a row with Source details open, a row being pressed, and
   the selected row from step 3 keep their identity across re-ranking.
   Activating a row (OK, tap, click, Enter) always acts on the source under the
   press at that moment.
7. Row moves may use the platform's standard list item placement animation;
   with reduced motion they are instant. Moves never change row height.
8. The provider ceiling, filters, discovery status and empty states are
   unchanged. When the ranking request itself fails, rows stay in the order
   already shown, without headers, and late arrivals append in arrival order.

### What changes for Best match autoplay

Nothing. The countdown, eligibility, hard deadline and fallback rules above are
unchanged, and the autoplay target is the first Best matches row:

- At the hard deadline or when every provider finishes, Countdown rule 4 picks
  the best row surviving hard filters, which is by definition the first Best
  matches row.
- In the early-start window the target is the highest ranked early-start
  eligible row (Countdown rule 2). That is the first Best matches row whenever
  that row is eligible. When it is not (for example it is supported but only in
  a lower language tier, while an *unknown*-decode row lower down is in the best
  tier), the existing rule targets the lower row; the countdown strip names it
  by its facts and the marker stays on the first row. This pre-existing edge is
  listed under open items, not changed here.
- Membership is computed before filters, so a provider or quality filter does
  not change the target; changing a filter cancels the countdown anyway.
- Fallback still walks the ranked rows that survive hard filters, which can
  continue past the fifth Best matches row into All sources.

## Normalized source facts

The shared engine (backend and its `core` copy) derives these fields from the
add-on's declared fields first and the release name second (`filename`, then
title lines), using PTT-equivalent rules (research note, section 3), with
fixture tests drawn from real add-on responses:

| Field | Values |
|---|---|
| `release_type` | `web_dl`, `webrip`, `bluray`, `remux`, `hdtv`, `dvd`, `other_rip`, `cam`, `unknown` |
| `three_d` | boolean |
| `dynamic_range` | list of `dv`, `hdr10_plus`, `hdr10`, `hdr`, `hlg`; empty means unknown, not SDR |
| `dv_base_layer` | `hdr10`, `sdr`, `none`, `unknown` |
| `audio_languages` | BCP-47 tags (existing field), audio evidence only |
| `audio_flags` | any of `dual`, `multi`, `dubbed` |
| `seeders` | integer or absent |
| `delivery` | `direct` or `torrent` (from the stream's transport, not text) |
| `binge_group` | the add-on's `behaviorHints.bingeGroup`, add-on scoped |

Rules: `Dual Audio`, `Dual`, `Multi`, `Multi Audio`, `Tri Audio`, `Dubbed`,
`Dub`, `Dubs`, `Dublado` and Torrentio's `Dubbed`/`Dual Audio`/`Multi Audio`
markers set flags; `Multi Subs`, `VOSTFR`, `Subbed` and hardsub markers are
subtitle evidence only. Flag emoji map to languages as today. Seeders come from
a declared field or Torrentio's `👤 N` marker.

Source rows show the release type and audio flags beside the quality badge
(for example `WEB-DL`, `Dual audio`, `Dubbed`). Needs a board; the two-line
description window (SRC-OVERFLOW-001) is unchanged.

## Device capability

The client sends its capabilities with every ranking request; the server never
guesses them. Android derives them from `MediaCodecList` and Media3 decoder
queries plus the display's HDR types: per codec (AVC, HEVC Main/Main10, AV1,
VP9) maximum hardware-decodable height, Dolby Vision decoder presence, display
HDR types, and audio decode/passthrough for AC-3, E-AC-3, TrueHD and DTS.
Each answer is *supported*, *unsupported* or *unknown*. Platforms without a
reliable query report *unknown*. Emulators report what their decoders report;
emulator results are not device evidence.

## Fallback

Only inside a Best match session (countdown-started or Play now), never after a
manual row activation:

1. A start failure is: a player error before the first frame, the
   undecodable state (clock advances with no frame), or no first frame within
   the startup deadline (20 s for direct sources; for torrents, the native
   torrent runtime's own startup errors and deadlines).
2. On a start failure the player shows
   `[reason]. Trying the next best source…` with the next target's facts and a
   **Stop** button, for 2 s, then opens the next ranked row that survives hard
   filters and has not failed in this session. **Stop** shows the existing
   failure screen.
3. At most three attempts per session, counting the first. After the third
   failure, return to the picker with the banner
   `3 sources couldn’t start on this device. Choose a source.` and the label
   `Didn’t start` on each failed row. Focus goes to the first row that has not
   failed.
4. A Dolby Vision decode failure demotes every other risky Dolby Vision row for
   the rest of the session.
5. Mid-playback stalls never switch sources; the existing buffering and failure
   behaviour applies.

The existing failure screen keeps its **Try [next source]**, **Choose another
source** and **Back** actions for manual sessions and after **Stop**.

## Settings

Playback preferences (profile scoped):

- **Source selection:** Best match / Always ask (unchanged).
- **Preferred audio:** `Original language` (renamed from `Original`) or a
  language. Applies to every title type.
- **HDR and Dolby Vision:** No preference (default) / Prefer / Avoid.
- **Preferred quality:** Auto / 4K / 1080p / 720p. **Auto** (formerly "Best
  available") means the device's own resolution: the client reports its
  display height snapped to 2160/1440/1080/720/480 with every ranking request,
  and the cap is the lower of the profile choice and the device. The row shows
  `Auto (this device: 1080p)` when the height is known. A source closest to the
  device therefore ranks first and higher resolutions sort into the over-cap
  class.

No release-type setting: the order above is fixed.

## Timing summary

| Timer | Value |
|---|---|
| Countdown | 3 s, restarts on a better target |
| Hard deadline | 20 s from discovery start |
| Provider ceiling | 60 s (unchanged; list only) |
| Direct-source startup deadline | 20 s to first frame |
| Fallback notice | 2 s |
| Attempts | 3 per session |

Changing a value needs a behaviour review.

## Acceptance scenarios

1. Best match, English preference, Torrentio returns a 4K Dolby Vision-only
   WEB-DL and a 1080p WEB-DL on a device without a DV decoder: the countdown
   targets the 1080p row; the 4K row is still listed.
2. A row becomes eligible at 1.5 s and a better one arrives at 3 s: the target
   switches and the countdown restarts; playback begins at 6 s.
3. During the countdown the viewer presses Down: the countdown disappears,
   focus moves to the second row, nothing plays, and no countdown returns when
   more rows arrive.
4. **Play now** starts the target immediately; Back during the countdown
   closes the picker as today.
5. Only slow providers: no eligible row by 20 s; the best surviving row gets a
   3 s countdown and plays. With only camera releases, nothing plays.
6. Original-language preference on an anime episode with original language
   Japanese: an unmarked release ranks first, then Torrentio's
   `Dual Audio / 🇬🇧`, then a `Dubbed` release that lists only English. With
   English preference: `Dual Audio / 🇬🇧` and the English `Dubbed` release
   (tier 1) rank above an unlisted `Dual Audio` (tier 2), which ranks above the
   unmarked release (tier 3).
7. A Torrentio release with no language line on an English-original movie with
   English preference ties tier 1; the same release on a Japanese-original
   anime with English preference is tier 3.
8. The first target fails to decode: the fallback notice appears, the second
   target starts. Three failures return to the picker with the banner and
   `Didn’t start` labels; focus is on the first unfailed row.
9. A manually activated row that fails shows the existing failure screen and
   never auto-advances.
10. Next episode of a series started from binge group G: a G row ranks first
    within its language tier and decode class.
11. Always ask: no countdown appears; the list is grouped exactly as in Best
    match mode and the first Best matches row carries the Best match eyebrow.
12. A file whose actual audio has no track in the preferred language shows the
    no-audio notice; playback continues.
13. Groups, either mode: discovery returns seven rows passing the hard filters
    and two camera releases. The list shows the `Best matches` header, the top
    five in ranking order with the marker on the first, then the `All sources`
    header, the sixth and seventh rows, then the two camera rows.
14. Three rows pass the hard filters and nothing else arrives: only the
    `Best matches` header shows, above all three rows.
15. Only camera releases arrive: no header shows and the rows are listed in
    ranking order without a marker; in Best match mode nothing plays
    (scenario 5).
16. A provider filter hides all five Best matches rows: both headers hide and
    the filter's rows show as one ranked list without a marker. Clearing the
    filter restores both headers and the marker on the same row as before.
17. Progressive ranking, TV, viewer has not navigated: provider A returns three
    rows at 1 s and they appear ranked under `Best matches` with focus on the
    first. Provider B returns a better row at 4 s: it appears first, takes the
    marker and the focus, and in Best match mode the countdown retargets
    (scenario 2) rather than cancelling. At no point are rows shown in arrival
    order, and nothing reorders when the last provider finishes.
18. Progressive ranking, TV, viewer navigated: focus is on the fifth Best
    matches row when two better rows arrive. Focus stays on that same source,
    now the second All sources row, at the same on-screen position; Down moves
    to the row ranked below it; Up moves to the first All sources row, and Up
    again crosses the `All sources` header to the last Best matches row
    without stopping on the header.
19. Progressive ranking, phone: the viewer has scrolled so a mid-list row is
    the first fully visible row when rows arrive above it. That row stays at
    the same screen offset; the new rows are only seen by scrolling up. A
    viewer who has not scrolled sees the new best row at the top.
20. Screen reader on any surface: heading navigation lands on `Best matches`
    and `All sources`, each announced as a heading; on TV the D-pad never
    focuses a header.
21. Desktop/web pointer: Source details is open for a row when a re-rank moves
    it to All sources; the open details stay on that source, and closing them
    returns focus to the same row in its new position.

## Open items

- Canvas boards for the countdown strip, fallback notice, failed-row label,
  release/audio badges, the new HDR setting row and the `Best matches` /
  `All sources` group headers (height, spacing, placement relative to the
  discovery status and filter chips) on every surface.
- Whether the Best match marker, or the countdown target, should follow the
  other when the first Best matches row is not early-start eligible
  ([What changes for Best match autoplay](#what-changes-for-best-match-autoplay));
  today the marker stays on the first row.
- Whether series memory is stored server-side (cross-device) or per device;
  proposed: server-side per profile and series, reset by a manual pick of a
  different source.
- Web and desktop capability reporting.
- Whether the playback gateway can remux/convert an undecodable source instead
  of ranking it down (not investigated).
