# LIVE-EMPTY-001 — Live with no source, and Live with a source but no channels

Status: **proposed**, owner report 2026-10-30
([design#45](https://github.com/viptv-org/design/issues/45)). Nothing here is
built yet.
Design commit: `bf8ac45` (this repository). Implementation:
[app#304](https://github.com/viptv-org/app/issues/304).
Source revision: app `da1b7de6` (`origin/edge`, 2026-10-30):
`features/live/LiveRoute.kt`, `LiveScreen.kt`, `TvLiveScreen.kt` and
`LiveFilters.kt`. Owner-only writes: backend `f30b2f5`
([backend#149](https://github.com/viptv-org/backend/pull/149)) on `origin/edge`,
not yet promoted to `main`.

## Intent

The Live page is two different stories and it tells neither: with no live
source configured it draws a filter chip over an empty page, one line and a
button into the whole of Settings. With a source configured but no channels
coming back it shows the same line again, so a broken provider looks like an
unconfigured account and the viewer is never told which it is.

Give the first state a designed, unmistakably VIPTV broadcast scene that says
what Live is and how to start it, and give the second state its own, cheaper
treatment with the reason and a retry. Hide the filter row when there is
nothing to filter, and stop sending people to a Settings page the signed-in
account may not be allowed to change.

## Which state the page shows

Only the page's own facts decide, in this order.

| Condition | State |
|---|---|
| A filter is applied (Favourites, a group or a source) | Today's filtered-empty line, unchanged |
| `LivePage.connections` is empty, or the page answered `NeedsConfiguration` | **No source** (LIVE-EMPTY-001A) |
| The page has connections and zero channels, and a request is in flight | **Still loading** (LIVE-EMPTY-001B loading) |
| The page has connections and zero channels after it answered | **No channels** (LIVE-EMPTY-001B) |
| Any channels | Today's page, unchanged |

`LivePage.connections` is the page's live-capable connection list for this
profile (the app filters it by `enabled` for its Source chip), so it answers "is
a source configured" without guessing from an error string. The guide (`liveGuides`) is not a Live source and never satisfies
`connections`.

## No source (LIVE-EMPTY-001A)

The page becomes one broadcast frame: a full-bleed night-stadium illustration
behind a short, left-set text block.

- **Visible:** the artwork, an eyebrow, a one-line headline, a body line naming
  both routes (an IPTV connection with Xtream or M3U, or a live add-on), and the
  actions allowed for this account.
- **Not visible:** every filter chip (Favourites, Group, Source), the channel
  preview, the guide, the channel list and the progress bar. Nothing on the page
  is a filter, so the row that only filters has no reason to exist.
- **Headline and body:** `copy.md` owns the exact strings.

Actions, by who is looking:

| Viewer | Action block |
|---|---|
| Owner account session | Primary **Set up live TV**, secondary **Add-ons** |
| Member account session | No action; the who line **Only the household owner can set up live TV.** |
| Paired TV (a device session) | No action; the who line **Manage live TV from a signed-in phone, computer or the web dashboard.** |
| Local mode (no account) | Primary plus secondary; the device owns its own sources |

The who line occupies the action block's place, so the copy never moves between
the two forms. The facts come from the account identity the app already reads
(`/api/auth/me`): `account.role` is `owner`, `member` or `device`, and
`capabilities.manage_account` says whether this session may change household
settings at all — false for a paired TV, true for a browser and for a native
account session ([app#300](https://github.com/viptv-org/app/issues/300) puts
that capability on the app's state; this state reads the same two fields and
depends on neither landing first). Local mode is the app's own local build. The
identity is requested when this state first appears. Until it answers, the text
block draws without an action block or who line and reserves their height; the
primary takes focus the frame it appears. No other loading state is drawn for
this.

**Set up live TV** opens Settings › Source integrations (Xtream and M3U live
there). **Add-ons** opens Settings › Add-ons. Both are the existing destinations;
nothing new is routed. A member or a paired TV never reaches either from here,
because the server answers `403 owner_required` /
`403 account_session_required` to a source write, and the empty state says so
before the tap instead of after it.

## Sources, no channels (LIVE-EMPTY-001B)

No artwork: this is a working page whose source did not answer, not a first
run. The page ground is `bg` and the page keeps its normal inset.

- **Filter row:** the Source chip stays while more than one enabled connection
  exists, because switching source is the recovery path. Favourites and Group
  stay hidden while there are no channels: there is nothing yet to favourite or
  group.
- **Still loading:** no copy and no artwork. Six skeleton channel rows in the
  page's own row shape — TV rows 1728 × 72, 8 apart, with a 50-wide number bar
  and a 300-wide title bar; P and W rows a 64 × 48 logo block plus two text
  bars, 12 apart — in `surface-1` with the existing shimmer. The page's linear progress bar keeps
  running under the chrome. The page never says "No channels" while a request
  is still open.
- **Answered with no channels:** headline, the server's own human reason when it
  sent one (the app's `ServerMessages` filter still decides that), and
  **Try again** as the primary when the failure is retryable. **Source
  integrations** is the secondary whenever the viewer may change sources, and
  absent otherwise. No reason and no failure → the neutral body line in
  `copy.md`.
- **Empty after a filter** stays today's line, not this state.

Retry re-requests the same query with the same filters and shows the loading
form again. Back from Source integrations returns here.

## Artwork

Two hand-authored SVGs in the tokens' colours, both inventoried in
`assets/FILES.json` and described in `assets/ASSET_MANIFEST.md`:

| File | Size | Used by |
|---|---|---|
| `assets/illustrations/live-empty-stadium-wide.svg` | 1920 × 1080 | Tablet, desktop, web and TV, and any layout 640 dp wide or more |
| `assets/illustrations/live-empty-stadium-tall.svg` | 1080 × 1920 | Phone and any layout under 640 dp |

Both are one original composition: a floodlit night stadium seen from the
halfway line, with crowd silhouettes and camera flashes in the stands, a lit
pitch-side hoarding, the pitch's own lines and a centre circle, floodlights with
light beams, and a glowing `LIVE` scoreboard bug in the top right. There is no
team, league, logo, player, photograph or third-party asset in either file, and
nothing is traced from a capture.

- **Drawing:** paths, rectangles, circles and ellipses with linear and radial
  gradients only — no text, raster, filter, mask, pattern, blend mode or
  external reference, so an app can convert a file into a vector drawable
  without losing anything. Both files stay under 30 KB.
- **Palette:** `bg` `#0B0B0C` and `bg-oled` `#000000` for the scrim, the sky,
  the stands and the silhouettes; the `surface-1`–`surface-4` ladder for the
  pitch, the crowd tiers, the masts and the scoreboard; `text-primary`
  `#F4F2EE` for floodlights, lamps, pitch lines and the `LIVE` lettering;
  `accent` `#F5C542` for the hoarding light strip and the scoreboard clock; and
  `status.live` `#FF5A4E` for the scoreboard dot, which is the only red in the
  artwork. Lower opacities of the same colours build depth.
- **Scrim, baked in:** the wide file carries a left-to-right scrim (96 % at the
  left edge, 80 % at 26 %, 42 % at 44 %, 12 % at 56 %, 2 % at 72 %) and a
  bottom scrim; the tall file carries a bottom scrim (30 % at 45 %, 80 % at
  72 %, 100 % at the bottom) and a short top scrim. A page draws the file once
  and adds no overlay of its own, so the copy and actions always sit on the
  darkest part.
- **Placement:** the page area only — under the TV navigation, the phone header,
  the desktop rail and the browser title bar, which keep their own grounds.
  Cover, anchored centre: at 1920 × 948 the wide file loses 66 px at the top and
  66 at the bottom (empty sky and the pitch's near edge); a narrow window uses
  the tall file instead, so a phone never crops the wide scene to a sliver.
- **Not named:** the artwork is decorative. It carries no content description
  and no accessible text; the heading, body and actions are the page.

## Layout

Platform keys follow [components.md](../../viptv-design-system/components.md)
(P phone under 640 dp, W tablet, desktop and web at 640 dp or more, T TV).
Coordinates are reference coordinates; no canvas board draws this state, so the
measurements below are derived from the type roles and the page insets in
`components.md` and are marked as derived below.

**T — 1920 × 1080, navigation 132 tall, page area 1920 × 948, inset 96**

| Element | Geometry |
|---|---|
| Artwork | 1920 × 948, cover, centre |
| Text block | x 96, width 840, vertically centred: 236 to 712 |
| Eyebrow | 18/700, +0.08em, uppercase, `text-secondary`; 22 tall at y 236 |
| Headline | D 56/700, −0.02em, line 64, at most 2 lines; y 276 |
| Body | 26/400, line 38, at most 3 lines, width ≤ 820; y 426 |
| Primary | 72 tall, radius 36, 34 side padding, 26/700; y 574 |
| Secondary | 52 tall, radius 26, 24 side padding, 22/600; y 660 |
| Gaps | 18 eyebrow→headline, 22 headline→body, 34 body→primary, 14 primary→secondary |
| Focus fill | Primary and secondary are off-white when focused, white 0.12 when not; no accent |

**W — 640 dp and wider, page inset 40**

| Element | Geometry |
|---|---|
| Artwork | fills the page area, cover, centre |
| Text block | x = 40 (the Live page's own inset), width ≤ 620, vertically centred |
| Eyebrow | 12/700, +0.06em, uppercase, `text-secondary` |
| Headline | D 40/700, −0.02em, line 46, at most 2 lines |
| Body | 16/400, line 24, at most 3 lines |
| Primary | 48 tall, radius 24, 22 side padding, accent fill, `on-accent` 16/700 |
| Secondary | 40 tall, quiet text, 15/600, `text-secondary` |
| Gaps | 16, 20, 28, 12 as on T, in that order |

**P — 390 × 844, page gutter 16, bottom bar 80**

| Element | Geometry |
|---|---|
| Artwork | fills the page area, cover, centre |
| Text block | x 16, width 358, bottom-anchored 112 above the page's bottom edge |
| Eyebrow | 11/700, +0.08em, uppercase, `text-secondary` |
| Headline | D 34/700, −0.02em, line 40, at most 3 lines |
| Body | 15/400, line 22, at most 3 lines |
| Primary | 54 tall, radius 27, full block width, accent fill, `on-accent` 17/700 |
| Secondary | 44 tall, quiet text, 15/600, `text-secondary` |
| Gaps | 12, 16, 24, 10 as on T and W, in that order |

**LIVE-EMPTY-001B geometry.** Page inset and gutter as above; the block is the
top-left of the page area (T 96/60, W 40/40, P 16/24, each measured from the
page area's own origin) because the chip row sits directly above it. T headline 44/700 line
50, body 24/400 line 34; W headline 28/700 line 34, body 15/400 line 22; P
headline 20/700 line 26, body 14/400 line 21. Actions use each layout's primary
and secondary geometry above. Skeleton rows start where channel rows start
today.

## Focus, input and timing

- **T:** entering Live focuses the navigation's own Live tab, as on every TV
  page. The first Down enters the page on the primary; Down again reaches the
  secondary; Up returns to the navigation. Right and Left do nothing on either
  action. The artwork, eyebrow, headline, body and who line are not focus stops.
  A held OK presses the focused action once; it does not repeat, and there is no
  hold action anywhere in this state.
- **T return:** Back from Settings › Source integrations or Add-ons returns to
  Live on the primary, re-requesting the page. If the request now has channels,
  today's Live page shows instead.
- **W:** no autofocus. Tab reaches the primary, then the secondary; Enter and
  Space activate. A pointer press keeps the existing 0.97 scale and hover steps.
- **P and tablet:** taps. The primary is 54 tall, above the bottom bar; nothing
  in the block is inside the bar's fade.
- **Motion:** nothing animates in, loops or delays an action. The block and the
  artwork appear in the same frame as the page. On TV the primary's focus fill
  keeps the existing 150 ms fill; `reduced motion` leaves it as it is.
- **Live updates:** if the page request answers with channels while this state
  is shown (a source added on the phone), the state is replaced in place with no
  transition and focus moves to the first channel row.

## Copy

Exact strings live in [copy.md](../../viptv-design-system/copy.md#empty-states):
the eyebrow, headline, body, both actions, both who lines, and the no-channel
headline, body and retry. Retired: the app's `No channels are available for this
profile.`, its `Manage add-ons` button, and the page's empty-page `All channels`
button in the no-source state.

## Accessibility

- The headline is the page's heading; the eyebrow, body and who line are text in
  reading order. The artwork is announced as nothing.
- The primary and secondary are real buttons with their visible labels. The who
  line is not an action and is not focusable.
- The page never reports "no channels" while the request is open, and never
  announces an empty list to a screen reader before the request answers.
- Announcements already in place (favourite toggles, guide errors) are unchanged.

## Acceptance

1. **LIVE-EMPTY-01:** a profile with no live connection, opened on TV at
   1920 × 1080. The stadium artwork fills the page area under the navigation, the
    eyebrow, headline and body read against its dark left side, and there is no
    filter chip, no preview and no channel list anywhere on the page. The
    navigation's Live tab is focused; Down lands on **Set up live TV**.
2. **LIVE-EMPTY-02:** from LIVE-EMPTY-01, OK on the primary opens Settings on
    its **Source integrations** page; Back returns to Live with the primary
    focused and a re-requested page.
3. **LIVE-EMPTY-03:** the same profile on a phone at 390 × 844. The tall artwork
    covers the page area without letterboxing, the block sits above the bottom
    bar, and the primary is a full-width accent button.
4. **LIVE-EMPTY-04:** the same profile in a desktop window at 1440 × 900, in a
    browser at 1280 × 800, on a tablet at 1280 × 800 and with the desktop window
    narrowed to 600 wide. The first three use the wide artwork; the 600-wide
    window uses the tall one. No layout shows a chip.
5. **LIVE-EMPTY-05 (member):** signed in as a member, the page shows the
    headline, body and **Only the household owner can set up live TV.** and no
    button; Tab (or Down on TV) finds nothing in the block, and the page has no
    focus stop beyond the navigation.
6. **LIVE-EMPTY-06 (paired TV):** a TV paired to an owner account shows
    **Manage live TV from a signed-in phone, computer or the web dashboard.**
    and no button. The same account on the phone still shows both actions.
7. **LIVE-EMPTY-07 (local mode):** a local build shows both actions and they
    reach Settings › Source integrations and Settings › Add-ons.
8. **LIVE-EMPTY-08 (no channels, loading):** one connection configured, the
    request open. The Source chip is present when a second connection exists and
    absent with one; no "No channels" copy is visible; six skeleton rows and the
    progress bar are, on TV, phone and desktop.
9. **LIVE-EMPTY-09 (no channels, failure):** the request answers with zero
    channels and a reason. The headline, the server's human reason and **Try
    again** appear; there is no artwork; OK/Tap retries, returns to the loading
    form and then to this state if it fails again.
10. **LIVE-EMPTY-10 (no channels, empty answer):** zero channels, no reason,
    no failure. The neutral body line shows and no error styling appears.
11. **LIVE-EMPTY-11:** with a filter applied (Favourites on, or a group or
    source chosen) and zero matching channels, the page keeps today's filtered
    line and today's chips, and neither new state appears.
12. **LIVE-EMPTY-12 (recovery):** from LIVE-EMPTY-09 with two connections,
    switching the Source chip to the working connection replaces the state with
    the channel list; switching back reproduces it.
13. **LIVE-EMPTY-13:** a source added elsewhere while this state is shown
    replaces it with the channel list in place, with no animation, and the
    remote lands on the first channel row.

## Unknowns

- No device evidence: nothing here is built, and the geometry is derived, not
  board-drawn. A canvas board for the TV and phone states should follow.
- The issue's third next step, "find free live add-ons", has no destination in
  the product: there is no add-on directory, catalogue or recommendation list in
  the app, the web dashboard or the server. The body names the two routes that
  exist; a free-add-on directory needs its own design and its own route.
- How quickly the account identity answers is an app decision. This contract only
  says the action block waits for it and holds its height. A server that omits
  `capabilities.manage_account` is read through `account.role` (`device` means a
  paired TV).
- A paired TV cannot write sources at all, so its line names other devices
  rather than an action. Whether that line should become a QR code or a deep
  link to the dashboard is open, and no origin string is added to copy.
- The wide artwork's top and bottom 66 px are cropped at 1920 × 948. A future
  page area of a different shape (an ultra-wide window) changes the crop, not
  the composition, but it has not been looked at on a 2560 × 1080 window.