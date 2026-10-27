# REFRESH-PULL-001 — Phone and tablet pull-to-refresh

Status: **proposed**, owner request 2026-10-26
([app#1](https://github.com/viptv-org/app/issues/1),
[design#23](https://github.com/viptv-org/design/issues/23)). The KMP app
already implements it on phone and tablet layouts. It becomes baseline once
device evidence is recorded.
Source revisions:
- the gesture is app `b55f942`
  ([app#35](https://github.com/viptv-org/app/pull/35)):
  - `components/PullRefresh.kt`;
  - `pullToRefresh()` in `state/ControllerFreshness.kt`;
  - `PULL_REFRESH_SCREENS` in `App.kt`;
  - the app's `docs/SMART_REFRESH.md` §6;
- the My List interaction is app `3aa4a3e`
  ([app#74](https://github.com/viptv-org/app/pull/74)).

The owner asked for this while the app was being built, so this contract
records what shipped. The evidence is desktop UI tests that drive a real touch
drag on the full app at phone size (`PullToRefreshUiTest`,
`LibraryCollapsingHeaderUiTest`) and controller tests (`PullToRefreshTest`).
No device evidence is recorded yet.

## Intent

Give phone and tablet viewers the standard touch gesture for "show me what's
new now". Pulling down at the top of a page reloads that page from the server
straight away. It does so quietly, like the automatic refresh of
[HOME-ADDON-001](home-addon-refresh.md): the page stays usable, and a failure
leaves it as it was.

## Where it applies

- **Layouts:** native phone and tablet layouts only. TV, the desktop app and
  the browser (at any window width) have no gesture and show no indicator.
  They rely on the automatic refresh: foreground return and the Home check.
  This is a touch addition, not a platform exception, because no layout loses
  an action.
- **Pages:** Home, My List, History and Details.
- **No gesture:** the source picker over Details, Browse (Discover, Movies,
  Series, Anime), Calendar, Live, Search, Settings and the player. Their
  loaders empty the page before reloading, which breaks the rule that a failed
  reload keeps the shown data. They need quiet reloads first.
- On tablet the gesture covers the page area only, not the navigation rail.

## Gesture

The gesture is Material 3 pull-to-refresh with its default indicator. The
values below are the library defaults, not VIPTV tokens:

- **Start:** a touch drag downward while the page's scrolling content is at
  its very top. A downward drag while the page is scrolled down only scrolls
  it back (app#74 test). On My List the page is at its top only with the
  collapsing header fully expanded: the large title (tablet) and the History
  card showing.
- **Pull:** a 40 circular indicator comes down from the top edge, centred
  horizontally. It moves at half the finger's speed. Its arrow arc grows with
  the distance. The threshold is 80 of indicator travel, about 160 of finger
  travel.
- **Release before the threshold:** the indicator returns and nothing is
  requested. A pull of 46 dp of finger travel does nothing (app test).
- **Release past the threshold:** the indicator settles 80 below the top edge
  as an indeterminate spinner, and the reload starts at once.
- **Colours:** the indicator disc is `color.surface.2` with Material level-2
  elevation, and the arrow and spinner are `color.text.secondary`. These are
  the app's Material colour-scheme mappings `surfaceContainerHigh` and
  `onSurfaceVariant`.
- **During a reload:** pulling again does nothing until the indicator ends.
  The page underneath scrolls, taps and navigates as usual.

There are no other inputs. Tap, long-press and Back keep their meanings, and
there is no hold or repeat behaviour.

## What a pull reloads

A pull asks the quiet refresh lane for a full refresh **now**. It skips the
revisions check, so it has no "unchanged" short cut and no 2 s coalescing. It
rebuilds Home even when nothing changed. This is the one exception to
HOME-ADDON-001's rule that an unchanged revision fetches nothing. The rebuild
is the same one that follows playback:

- **Home:** shelves, Continue Watching, profiles and preferences. A catalog
  row the viewer has already paged keeps its loaded tail.
- **My List:** the page on display, with its current list, type and filters.
- **History:** the history list.
- **Details:** the title is fetched again and the episodes already loaded take
  their fresh watched state and progress. The episode list, season, paging and
  focus stay, and art the reply lacks is kept.

The add-on list (Settings › Add-ons) is not reloaded. On a device-local
connection the same pages rebuild from the device's library instead of the
server.

If an automatic check or refresh is already running, the pull's refresh runs
right after it in the same lane, and the indicator stays until both finish.

## States and recovery

- **While reloading:** the indicator spins over the current page. There is no
  global loading cover, no skeleton, no scroll reset and no "refreshing" text.
  An operation the viewer started (a save, a source load, playback) is never
  cancelled.
- **Success:** the new data merges in place. The screen, scroll position and
  any surviving focus stay. The indicator goes away.
- **Failure** (network, server error): the shown data stays and no error or
  toast appears. The indicator goes away. The next pull or automatic check
  tries again.
- **Expired session (401):** the app goes to sign-in, as any expired session
  does.
- **Profile, account or connection change during a reload:** the late result
  is dropped (HAF-05). The indicator ends when the lane is idle.

## Return and navigation

- The indicator belongs to the page area, not to one page. If the viewer
  leaves for another page with the gesture while the reload runs (say Home to
  My List), the indicator stays until the reload finishes. Leaving for a page
  without the gesture hides it, and the reload still finishes in the
  background. Coming back while it runs shows the indicator again.
- Opening the source picker from Details turns the gesture off. Details stays
  composed behind the picker, so closing the picker returns to the same
  Details with the gesture on again.
- Back from Details, My List or History follows the usual return rules. A
  pull changes no navigation.

## Copy

There is none. The indicator has no label, and nothing reports success or
failure.

## Accessibility

While it spins, the indicator exposes an indeterminate progress value, so
screen readers can announce that the page is busy. The gesture has no
accessibility action. Screen-reader users get fresh data from the automatic
refresh on foreground return and while Home is visible (HOME-ADDON-001). The
spinner animates even with reduced motion, as the Material default does.

## Superseded

Nothing. No board shows a refresh gesture or rules one out. Two existing rules
are refined:

- **HOME-ADDON-001:** a deliberate pull is the one refresh that skips the
  revisions check and shows an indicator. Automatic refreshes stay invisible
  and check first.
- **"Skeletons, not spinners"** (phone research note 8, `components.md` §9,
  the README principle "Loading is a skeleton"): these rules govern first
  loads. The pull indicator is the one spinner over content that is already
  shown. First loads still use their skeletons.

## Acceptance

1. **REFRESH-PULL-01:** on a phone, pull Home down past the threshold. The
   indicator spins and the current Home stays on screen with no cover. The
   rebuilt Home replaces it in place, including a new Continue Watching card.
   The indicator then goes away and no error shows.
2. **REFRESH-PULL-02:** repeat on My List, History and Details on phone and
   tablet. Each reloads, the indicator ends, and the same page is still shown.
3. **REFRESH-PULL-03:** a short pull (released before the threshold) requests
   nothing and shows no spinner.
4. **REFRESH-PULL-04:** pull with nothing changed on the server. Home is still
   rebuilt, with no revisions check first.
5. **REFRESH-PULL-05:** fail the reload. The shown data stays, no error or
   toast appears, and the indicator ends. A later pull succeeds.
6. **REFRESH-PULL-06:** pull with an expired session. The app goes to
   sign-in.
7. **REFRESH-PULL-07:** pull while an automatic check is running. The forced
   refresh runs after it, and the indicator ends only after its own rebuild.
8. **REFRESH-PULL-08:** scroll My List down so History and the title collapse,
   then drag down. The list scrolls back and nothing reloads. A pull from the
   very top reloads.
9. **REFRESH-PULL-09:** on TV, the desktop app and a browser (wide or phone
   width), the same drag requests nothing and shows no indicator. On Browse,
   Calendar, Live, Search, Settings and the source picker it does nothing
   either.
10. **REFRESH-PULL-10:** pull on Home, then go to My List before the reload
    ends. The indicator shows there until it ends. Go to Browse instead and
    it is hidden. Return to Home and the refreshed data is shown.

## Unknowns

- No device evidence yet. emulator-5590 was signed into the owner's profile,
  so app#35 recorded desktop renders of the phone layout instead.
- The library defaults (threshold, drag resistance, elevation) follow the
  Compose Material 3 version the app builds with. They have not been measured
  on a device.
- A single drag that starts scrolled down and reaches the top: whether the
  rest of it counts toward the pull is untested.
- On a page whose content does not scroll (for example the My List empty
  state below the pinned controls), whether a drag outside the list starts a
  pull is untested.
- After a refresh, a new first card in a Home row can sit partly off-screen to
  the left ([app#26](https://github.com/viptv-org/app/issues/26)). The
  automatic refresh does the same.
- iOS shares the phone and tablet layouts, but nothing has been run there.
- No canvas board shows the indicator.
