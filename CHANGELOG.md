# Design changes

## 2026-10-28 — TV filters are the same chips and the right panel

[FILTER-CHIP-001](viptv-design-system/components.md#2-chips-and-segmented-controls)
now records TV as implemented: app#121 (PR
[app#148](https://github.com/viptv-org/app/pull/148)) moved Browse /
Discover / Movies / Series / Anime, My List and the source picker onto the same
one-row dropdown chips as phone, tablet, desktop and web. Browse reads
**Catalog: Popular · Sort: Required · Genre: Any · Languages: Any · Free only ·
Search: Any**, My List **List: My List · Type: All · Sort by: Last watched ·
Status: Any · Genre: Any**, the source picker **Quality: All · Source: All
sources**, and the Catalog + Filters chips, the applied-chip strip and the
"Show results" full-page surface are gone. The only TV-specific part is the
container of the list: the right panel, 760 × scale wide over the 0.6 scrim with
the chip's title as its heading and 72 × scale rows, focus opening on the
current option. A pick applies at once — a single choice closes the panel, a
multiple stays open — and Back, Escape, the scrim or a pick close only the
panel, returning the remote to the chip that opened it. Chips are focus stops in
one row: the remote enters on the first chip, Left/Right walk it, and Clear
resets the facets and leaves the remote on the row.

`components.md` §2 gains the TV reading of the pattern and its chip geometry,
§5 the panel's rows and focus, §8 the container and its close rules, and the
implemented contracts name `BrowseFilterBar` / `LibraryFilterBar` /
`SourceFilters`, `LocalTvScale` and `TvFilterBarTest`. The retired TV filter
boards are marked superseded beside the desktop and phone ones: `Tv3Movies` and
`Tv3MoviesCatalogs` for the Catalog + Filters chips and applied strip,
`Tv3MoviesFilters` and `Tv3MoviesFilterText` for the full-page surface, and
`Tv3MyList` for its type segments and Sort pill. No board is re-exported, and
`decisions.md`'s 2026-10-19 TV filter decision carries the supersession.

Refs [app#121](https://github.com/viptv-org/app/issues/121),
[design#34](https://github.com/viptv-org/design/issues/34).

## 2026-10-28 — Proposed: the Android Updating screen and its copy

[AND-APP-UPDATE-001](specs/behavior/app-updates.md#updating-screen) records what
app#139 shipped (PR [app#145](https://github.com/viptv-org/app/pull/145),
`81cf5ae`) while the spec stays **proposed**: choosing **Install** now covers
the app with one full-screen Updating screen until Android has replaced the
process. It shows **Updating VIPTV to [version]…**, the write progress as a bar
with **"[N]%"**, becomes indeterminate behind Android's confirmation, carries
the install-permission step (**Allow updates**, **Open settings** or Fire TV's
**Try again**, **Later**) on the same cover instead of the prompt's dialog, and
makes Back do nothing while the session commits. An install Android rejects
returns to the prompt as **Couldn't update VIPTV** · **Android didn't install
the update.** · **Try again** · **Later**. Where the app can reopen itself it
does, and confirms **Updated to [version]** at the bottom for six seconds.
`copy.md` gains the strings, `components.md` §8 the cover and §9 the
confirmation bar, and `decisions.md` the entry.

No canvas board shows the screen (app `docs/DESIGN_GAPS.md` GAP-064 and
GAP-065), so the recorded geometry is the implementation's, unmeasured against
a board, and the section says so. The contract is retitled **Android in-app
updates** and its source corrected to what the app actually reads — the
signed-in server's `<server origin>/updates/android/update.json` feed (app#64) —
with GitHub Releases named as the planned future source (owner decision
2026-10-27) and acceptance for a missing, malformed and rejected feed. The
spec's permission step keeps its earlier wording honest by moving the copy to
the screen, and Back on the permission step is still the page's Back rather
than Later ([app#146](https://github.com/viptv-org/app/issues/146)). Refs
[app#139](https://github.com/viptv-org/app/issues/139),
[design#32](https://github.com/viptv-org/design/issues/32).

## 2026-10-28 — The dropdown chip and its list are the one filter pattern

[FILTER-CHIP-001](viptv-design-system/components.md#2-chips-and-segmented-controls)
records the rule the owner set on 2026-10-27 and the implementation in
app#117 (PR [app#130](https://github.com/viptv-org/app/pull/130), open while
this entry lands). Browse / Discover / Movies / Series / Anime, My List and
the source picker filter through one horizontal, scrolling row of dropdown
chips at the top of the page: the catalog or list chip first, a group divider,
one chip per facet, and a "Clear" chip at the end while anything is set. Each
chip opens the shared choice list — the anchored popover on desktop, web and
tablet, the bottom sheet on a phone — which adds a search field past 8 rows,
ticks checkboxes and respects the provider's cap for a multiple choice, and
applies a text filter on Enter or Done. A chip is filled while its value
differs from the page default. Picking applies at once: no "Filters" toggle,
no second panel and no Apply or "Show results" button. A set of 2–3 options,
an on/off filter and a text filter are all that same chip.

This retires the phone "Filters" toggle and applied-chip strip, the My List
filter sheet and segmented type chips, the source picker's chip rows, the
`W3Browse` filter rail, and the app#57 / app#59 segments-or-dropdown threshold.
**TV is out of scope for that PR:** it keeps the Catalog + Filters chips and
the "Show results" surface until [app#121](https://github.com/viptv-org/app/issues/121).
`components.md` §2 gains the rules, §5 the list content and §8 the containers;
`copy.md` gains the chip and list strings; the implemented component contracts
record `FilterBar.kt` / `SearchableSelect.kt` and the `FilterPatternScanTest`
that keeps the retired surfaces gone. No board is re-exported yet, and the
canvas frames that draw the retired filter forms need one.

Refs [app#117](https://github.com/viptv-org/app/issues/117), [design#30](https://github.com/viptv-org/design/issues/30).

## 2026-10-27 — Proposed: Phone and tablet pull-to-refresh

[REFRESH-PULL-001](specs/behavior/pull-to-refresh.md) records what the KMP
app shipped in app#35 (`b55f942`), with the My List rule from app#74
(`3aa4a3e`). On phone and tablet layouts, pulling down at the very top of
Home, My List, History or Details shows the Material 3 indicator and reloads
the page at once. On My List the very top means the collapsing header is
fully expanded. A pull released before the threshold does nothing. The pull
skips the revision check and rebuilds Home even when nothing changed. It
otherwise follows HOME-ADDON-001's quiet rules: no cover, no scroll reset, and
a failure keeps the shown data with no error. An expired session goes to
sign-in as usual. TV, the desktop app and the browser have no gesture. The source
picker, Browse, Calendar, Live, Search and Settings have none either, because
their loaders empty the page first. There is no copy.

The indicator is the Material default: a `color.text.secondary` arc on a
`color.surface.2` disc. That makes it the one non-accent spinner, an exception
recorded against the Spinner rule (`components.md` §3) and the README accent
principle. `components.md` §3 and §9, `copy.md`, the README, HOME-ADDON-001
and phone research note 8 ("skeletons not spinners", which covers first loads
only) gain pointers. No board is superseded. Owner request 2026-10-26
([app#1](https://github.com/viptv-org/app/issues/1),
[design#23](https://github.com/viptv-org/design/issues/23)). There is no
device evidence yet, and no canvas board shows the indicator.

## 2026-10-27 — Proposed: Wider desktop/web source drawer and no best-match hint

[SRC-DRAWER-001](specs/behavior/source-drawer.md) records what the KMP app
shipped in app#86 (`f80aa91`). The desktop and web source drawer is now
min(720, 55 % of the window) wide, never narrower than 460; at 1440 it is 720.
Other desktop drawers, the tablet drawer, the phone sheet and the TV panel are
unchanged. On web, the drawer opened from a title's Details dialog now stacks
over that dialog behind its 0.55 scrim. Focus starts on its ×, and Escape, the
× or a scrim click close only the drawer and return to the unchanged dialog.
The hint "Play always starts the best match. Change … in Settings › Playback."
is removed on every layout. TV keeps its status line only while add-ons
answer ("Checking add-ons · N sources so far") or a stream opens ("Opening
stream…"). `components.md` §8, `copy.md` and the README overview are amended.
The `D3Sources`, `D3SourcesEmpty`, `D3SourcesTorrent`, `CmpDesk3`, `M3Sources`,
`Tv3Sources` and `Tv3SourcesLoading` boards are listed as superseded until the
canvas re-exports them. Owner decision 2026-10-27
([app#60](https://github.com/viptv-org/app/issues/60),
[design#24](https://github.com/viptv-org/design/issues/24)). No device
evidence yet, and a board for the drawer over the web Details dialog is still
needed.

## 2026-10-27 — Proposed: Next-episode autoplay countdown and its setting

[PLAY-NEXT-AUTOPLAY-001](specs/behavior/next-episode-autoplay.md) records
what the KMP app shipped in app#48 and app#77. When a series episode ends, the
next-episode panel opens over the last frame. Its primary action counts down
10 seconds ("Next episode in 9", with a ring that empties; reduced motion keeps
only the number) and then plays the next episode. Any viewer action cancels it
for that end: the secondary action, Back/Escape, a seek, or any key or pointer
press. Finales, movies and live channels never count down. Settings › Playback
gains **Autoplay next episode**, on by default and stored per device because
the profile preference API has no field for it. The TV footnote reads "Starts
automatically. Press any button to cancel." while counting and "Nothing plays
on its own." otherwise.

This resolves the conflict between the Roku contract, AND-037 and
`decisions.md` #1 (a countdown) and the TV, phone and desktop boards ("Nothing
plays on its own"). The Roku baseline stays frozen and AND-037 is marked
superseded. Decision #1, the Up Next component, copy, the `up-next-countdown`
token (now 10000ms) and the research notes are amended. "Nothing ever plays on its
own" is retired from the `Next episode button` setting description. Owner
decision 2026-10-27 ([app#65](https://github.com/viptv-org/app/issues/65),
[design#26](https://github.com/viptv-org/design/issues/26)). Canvas boards for
the countdown and the setting row are still needed.

## 2026-10-27 — Black and white V app icon and TV banner master

`assets/brand/app-icon/` is the square app-icon and TV-banner master for
Android, Android TV and Fire TV: a white Bricolage Grotesque ExtraBold V on
black, an adaptive-icon foreground and monochrome layer, and a 320×180 banner
(the white "VIPTV" wordmark on black). Roku branding is unchanged. `assets/brand/tools/make_app_icon.py` generates it
reproducibly; provenance is in
[the asset manifest](assets/ASSET_MANIFEST.md#app-icon-and-tv-banner-master).
It replaces the amber V the KMP app shipped. Owner decision 2026-10-27
([design#21](https://github.com/viptv-org/design/issues/21)).

## 2026-10-26 — Proposed: Best matches source group, ranked as sources arrive

[SRC-BEST-MATCH-001](specs/behavior/source-best-match.md#source-groups-best-matches-and-all-sources)
now groups the source list in both Best match and Always ask: a **Best
matches** group with the top five rows that pass the hard filters, then **All
sources** in ranking order. Rows are ranked and grouped as providers answer
instead of being shown in arrival order and reordered at the end; re-ranking
keeps TV focus on the same source and the phone scroll anchor in place once the
viewer has navigated. The shared ranking supplies membership and the marker;
headers are non-focusable headings (copy in `copy.md`).
Best match autoplay is unchanged. Owner request 2026-10-26
([design#20](https://github.com/viptv-org/design/issues/20)); header boards
are still needed.

## 2026-10-22 — KMP subtitle mode and vertical TV Subtitles & audio

PLAY-SUBTITLE-MODE-001 is adopted by the KMP app: **Subtitles** offers Always /
`When audio isn't [language]` / Never on Subtitles & audio, and TV Playback drops
**Start with subtitles**. TV Subtitles & audio becomes one vertical Up/Down list
with the preview beside it (owner decision; canvas board pending).

## 2026-10-22 — Proposed: Best match autoplay, ranking and fallback

[SRC-BEST-MATCH-001](specs/behavior/source-best-match.md) replaces "wait for
every provider, then play the top row" with an early-start countdown that any
list navigation cancels. Ranking now covers device decode support, one
preferred-audio setting with dub/dual-audio evidence tiers, release type (WEB
and BluRay first, camera releases never autoplayed), an off-by-default
HDR/Dolby Vision preference, torrent health and per-series binge groups. A
failed Best match start tries the next source, at most three attempts.
`PLAYBACK_CAPABILITIES.md` names this as the one exception to explicit source
selection. Canvas boards are still needed.

## 2026-10-19 — Second canvas re-export: browse, source integrations, missing screens

The owner's design AI produced the requested boards (see
`plans/DESIGN_REQUEST-2026-10-18.md`): 264 screens now (tv 56, phone 69, tablet
18, desktop 55, web 40, simkl 26). New: browse page sets with catalog pickers,
facet filters and loading/empty/error states (D3/M3/T3/W3Browse*, Tv3Movies*),
source-integration settings and configure forms for VIPTV Sources, Xtream and
M3U with all states (SetSources, SourcesViptu/M3u/Xtream/Remove/Empty/Torrent),
parental controls, recovery codes, About/Display, TV add-on manual entry, and
card/row state sheets. The IPTV provider sign-in boards were removed per owner
decision (M3U and Xtream remain Live TV source integrations). The canvas data
dictionary (`reference/canvas-data-dictionary.md`) documents the generic field
shapes the boards draw from. Screens rendered with `tools/screenshots.mjs`
(scale 1) and stored as WebP q85.

## 2026-10-18 — Full canvas re-export: 197 current screens

The owner supplied the current canvas export (chat artifact
`ded73220-d76b-426c-8ea2-57d74c2d8473`). This replaces the reference screen set
wholesale: 197 boards — tv 37, phone 53, tablet 11, desktop 40, web 30, simkl
26 — including the previously missing season menu boards (`D3TitleSeason`,
`M3SeasonSheet`), tablet and Simkl surface sets, offline fonts, the canvas token
file (`reference/canvas-tokens.json`), per-platform research notes
(`viptv-design-system/notes/`) and the TV focus/row-motion demo
(`reference/extras/tv-focus-and-rows.html`). Screens were rendered with the
export's `tools/screenshots.mjs` (Playwright, scale 1) and stored as WebP q85.
Naming changed to the canvas prefixes: `M3*` phone, `T3*` tablet, `D3*`
desktop, `W3*` web, `Tv3*` TV, `Sk*` Simkl; the previous export's short names
(`Desk*`, `Web*`, `Ph*`, `Tv*`, `Main`, `Title`) are retired. The 9 component
sheets remain from the 2026-09-23 export; where a sheet and a new board
disagree, the new board wins. Notable canvas rules now visible in the boards:
primary buttons are off-white (accent stays on progress, marks/logo and
toggles); hero art is a framed 16:9 card with a blurred ambient fill; sign-in
methods on every platform are browser, email code, password, another device,
IPTV provider (Xtream/M3U) or no account; the desktop title bar hides search
until a profile is chosen. `copy.md`, `components.md` and `decisions.md` still
describe parts of the previous export and need follow-up passes against the
new boards.

## 2026-10-18 — Remove the IPTV provider sign-in method

Sign-in never included an IPTV provider method in this specification (see copy.md
Sign-in): VIPTV accounts sign in with a username and password, a browser/device
flow, or use local mode. An implementation draft exposed "IPTV provider (Xtream
Codes login or an M3U playlist)" as a sign-in option on TV, phone and desktop;
it was removed to restore parity with the specified sign-in set. M3U and Xtream
remain available as Live TV source integrations in Settings, not as sign-in.
Additionally, password sign-in fields are labelled "Username" (matching the
account system and WebSignIn reference); the field never required an email
address.

## 2026-10-18 — Stremio import in the KMP web and phone clients

The owner approved moving IMP-001 into the KMP app for the browser build and
Android phone and tablet, behind an "Import from Stremio" settings entry after
Devices, with the full dashboard feature set on each. TV, desktop and local mode
have no import UI. Signed-in device sessions may import into their own selected,
unrestricted profile, including adopting Stremio add-ons, as devices can already
manage shared add-ons. Long verification steps get an honest busy message and no
short client timeout, and failed add-ons are identified on their rows. Flow,
copy and history rules are otherwise unchanged.

## 2026-10-11 — Remove the v1 backend surface

After the verified 2026-10-09 cutover, BE-002 drops the `client_update_required`
stubs for retired media/setup/organizer namespaces and the unversioned
`/api/addons` routes; both now answer as unknown routes. Add-on management is
`/api/v2/addons` only. Paired viewing devices with a selected profile may manage
the account's shared add-ons there, preserving the existing TV/Roku settings
behavior; parent restrictions still apply. No screens or copy change.

## 2026-10-07 — Actionable source startup diagnostics

NT-09 requires the measured native preparation stage to survive its first
deadline through FFI and asynchronous completion. Cache preparation, metadata,
initialization, local endpoint, typed control-network failures and retiring work
have distinct closed explanations. The existing recovery dialog includes the
validated diagnostic code. Media3 failures preserve their measured numeric code
and HTTP status where present. No dependency text or source identifiers enter
display/log data; recovery actions, focus and delivery authority remain intact.

## 2026-10-07 — Bounded native torrent piece cache

The owner approved rolling pieces for large native Android video inputs. NT-10
requires bounded retained bytes, large-offset/backward reads, exact-file authority,
independent grants and joined retirement. The aggregate 2 GiB ceiling remains;
large inputs reserve 256 MiB instead of full logical payload. Capacity failure
copy describes observed cache admission rather than source size. Existing
recovery actions and layout remain unchanged; Android decode evidence is separate.

## 2026-10-07 — Observed native playback failure explanations

Amend SRC-TORRENT-NATIVE-001 with closed observed reason codes and exact safe
copy for acquisition/metadata deadlines, full-torrent cache budget, storage/cache,
metadata/file mismatch, grant expiry, connectivity and codec support. NT-09
requires native/actual-WASM copy agreement and safe asynchronous preservation.
Unknown failures remain generic; deadlines never imply absent seeders. Existing
recovery, focus, layout and source intent remain unchanged. Adapter/engine facts
and device acceptance require their own evidence.

## 2026-10-07 — Organize plans and engineering documentation

Grouped implementation plans under `plans/` and architecture, playback, platform,
process and historical references under `docs/`. Added navigation indexes and
updated live document links, agent pointers and validation paths. Existing
behavior specifications, visual assets and immutable historical references
retain their locations and meaning; this reorganization does not advance client
design pins or establish new implementation evidence.

## 2026-10-07 — Proposed episode annotations implementation plan

Added EPISODE-ANNOTATIONS-001: native filler/recap badges and manual intro/outro
skipping backed by replaceable metadata adapters, followed by separately gated
general-media lookup, opt-in automation and optional media analysis. The plan
defines repo ownership, proposed versioned reads, identity/applicability rules,
budgets and acceptance. Normative geometry/canvas exports, provider permissions,
implementation, immutable adoption and device evidence remain pending.

## 2026-10-06 — Approved Android native torrent contract

Owner-approved SRC-TORRENT-NATIVE-001 for local Markdown ticket 01 closes
negotiation, native request/grant JSON, exact-index v1 VOD, metadata bounds,
public peer/DHT privacy, lease/revocation, independent grant capabilities,
authorization-epoch cache limits, acquisition/quiescence and archive-free gates.
BE-002, gateway exclusions and playback capability/recovery rules reference this
narrow Android exception. Existing UI, source/resume/history and gateway HLS
remain unchanged. Approval is for implementation only; immutable consumer
adoption, engine/backend/core/Android implementation and qualification remain
pending. No production activation or physical-device claim follows.

## 2026-10-02 — Proposed add-on torrent gateway sources

Specified SRC-TORRENT-GATEWAY-001 for gateway issue 15: existing account-owned
add-on discovery retains opaque source handles while opt-in authorized gateways
prepare torrent/archive HLS for web, desktop and Android. The draft defines
supported input normalization, file selection, capability/scope checks, private
source metadata, safe producer copy and lease cancellation. Native peer delivery,
progressive integration and qualification remain separate; review and adoption
are pending.

## 2026-10-02 — Narrow phone watched-caption wrapping

Clarified AND-EPISODE-WATCHED-001: the complete badge wraps below the episode
number when a narrow phone text column cannot fit both. Artwork and the
44 dp options target retain their geometry; neither label is ellipsized.
The 320 dp native fixture exposed the constraint before Android publication.

## 2026-10-02 — Android completed episode indicators

Specified proposed AND-EPISODE-WATCHED-001 for Android TV and phone episode
cards: a readable check and Watched badge beside the episode number uses the
current profile's saved completion fact. Partial progress retains its bar,
completed episodes omit it, and updates cannot leak across profiles or recycled
cards. Rendering and device acceptance remain pending.

## 2026-10-02 — Website player Fit / Fill

Specified WEB-PLAYER-FIT-001 for the responsive website player. Fit shows the
whole video; Fill crops it to cover the viewport. The accessible toggle beside
Fullscreen applies to HTML video and MediaBunny canvas without changing the
playback session. Phone/desktop browser evidence and device checks are pending.

## 2026-10-02 — Android TV media rows reach the right edge

Specified AND-TV-ROW-EDGE-001: horizontal media card rows, including Popular
movies and Details episodes, reach the native Android TV viewport's right edge
with room for the focus ring. Header/text safe insets and card geometry remain;
TV-web retains its 1824 px bound. Android implementation and device evidence
are pending.

## 2026-10-02 — Android TV episode-number jump

Specified AND-EPISODE-JUMP-001: a compact chip beside the season badge opens
native numeric input and jumps to an exact episode in the current season by
scrolling and focusing its card. Invalid input stays editable; cancellation
preserves the row. Playback and hero Play/Resume remain unchanged. Android TV
implementation and device evidence are pending.

## 2026-10-01 — Native Android TV keyboard

Specified AND-KEYBOARD-001: Android TV uses its native device input method in
Search and text-entry dialogs, preserving catalog shelves, masked parent PIN,
Done/Cancel, keyboard-first Back and field/result return focus. Other TV
platforms retain their keyboard UI; native acceptance remains pending.

## 2026-10-01 — Distinct source producers and truthful outcomes

Specified SRC-PROVIDERS-001: source filters retain each observed configured
producer's identity and name, including zero-result and safe failed add-ons.
The picker explains unsupported formats and keeps partial playable rows usable.

## 2026-10-01 — Continue Watching episode source return

Specified CW-SOURCE-BACK-001: cancelling an episode's source picker from Continue
Watching opens its parent show details and Back restores the originating card.
Android and React/SolidTV implementation evidence remains pending.

## 2026-10-01 — Source picker descriptions and discovery status

Specified SRC-OVERFLOW-001 for Android phone/TV and responsive React/SolidTV:
every source description uses a two-line fixed window with focus/hover overflow
motion and reduced-motion fallback. Discovery shows a visible spinner and status
through partial results. Implementation and device evidence remain pending.

## 2026-09-30 — Android phone presentation and player track menus

Specified AND-042 for design issue 6. Phone Home now opens on the rounded hero,
the bottom navigation shows icons only, and cards carry minimal captions.
Catalog shelves are headed by content type, phone Home shows live channels as
logo tiles, and the bar is 6dp with lifted progress. Loading uses skeletons.
Phone and TV player audio/subtitle menus follow PhPlayerSubs and TvPlayerSubs.
Only AND-038's Home header remote entry changes; other TV geometry is
unchanged. Emulator and device evidence remain separate.

## 2026-09-30 — Canvas source, reference provenance and repository status

Recorded the VIPTV Redesign canvas as the visual source for the redesign beside
its committed `viptv-design-system/` export. Added `reference/FILES.json`
(SHA-256 and canvas-export source for all 453 reference files), verified by
`scripts/validate.py`. Clarified that canvas renders are allowed design
artifacts while app/device captures stay forbidden. Updated docs/architecture/REPOSITORIES.md
with current status, design-pin mechanism and specs for every repository,
including core, playback-gateway, workspace and desktop. No behavior change.

## 2026-09-30 — Android silent foreground identity validation

Specified AND-041 for Android issue 4: stable authenticated phone/TV presentation
during bounded foreground validation, coalesced refresh, actionable recovery,
explicit revocation and cancellation. Existing background-stop, exact-source
absolute Resume, native playback policy, geometry and assets remain unchanged.
Actual authenticated media and per-device/visual evidence remain required.

## 2026-09-30 — Bounded bidirectional admin VOD matching

Specified ADM-002-VOD-WINDOW for web issue 5: three retained title pages,
automatic reverse reload, complete owned-provider selection, scoped cancellation,
retry and dialog Back/scroll/focus restoration. Keeps ADM-002 tokens and row
geometry. Synthetic encrypted 100k-title HTTPS and per-viewport evidence remain
required; this design change alone establishes no rendered or device acceptance.

Review clarification: idle/failed dialogs dismiss without saving; a submitted
save retains the existing disabled-dismissal state until completion or a bounded
30-second timeout. A browser Back cannot undo an already submitted server write.

## TV-only LightningJS renderer migration proposed — 2026-09-24
Authorized a staged replacement of the React TV renderer and custom D-pad focus registry with one LightningJS Blits UI for Tizen, Vizio and LG webOS. The 1920×1080 current TV output and behavior are the 1:1 migration baseline; the pinned design images remain a separate design-parity reference. Phone web, responsive web and Tauri desktop retain their React entry. TV launchers remain on the existing renderer until matched-content pixel comparisons, remote flows and platform checks qualify the new entry. See docs/platforms/TV_IMPLEMENTATION.md. No parity or device claim is made by this spec update.

## VIPTV design system — 2026-09-23
Adopted [viptv-design-system/](viptv-design-system/README.md) as the single visual design for phone, desktop (Tauri), web and TV: `tokens/tokens.json` (source of truth), component rules, copy, settled decisions and reference screens. Removed the former visual layer (`tokens/`, `scripts/gen-tokens.mjs`, `specs/visual/`, RESPONSIVE_UI/PRODUCTION/VIPTV_ALIGNMENT, DESKTOP_LAYOUT, TV_WEB_UI_REBUILD, ANDROID_UI_REBUILD, TV_CANDIDATE_2026_09_12); they remain in git history. Behavior contracts under `specs/behavior/` are unchanged.

## Initial extraction — 2026-09-12
Captured the Roku baseline at vynxc/viptv@7d6b413 and established design-first cross-platform governance. This changes repository ownership, not Roku behavior. Android-only imports and proposed platform adapters are tracked separately from current Roku behavior.

## Baseline precision audit
Added exact dynamic guide geometry, search debounce/focus/partial-failure behavior and server-owned queue completion/cache rules. These clarify existing behavior without changing it. Source citations use the published split runtime snapshots.

## TV platform implementation
Authorized Android TV Compose and one shared Tizen/Vizio React frontend, with platform playback modules and design-based visual/remote testing. The baseline UX is preserved; host exit and on-screen keyboard equivalents are documented in docs/platforms/TV_IMPLEMENTATION.md.

## 2026-09-12 TV implementation candidate

Added the Android TV/shared Tizen-Vizio implementation checkpoint and owner-requested deferred joint testing. No Roku behavior or visual contract changed.

## 2026-09-12 — Resume identity extraction correction

Corrected the behavioral contract from addon plus human source name to addon plus nonempty server-authored source fingerprint. `Util.brs:45–59` at the frozen Roku revision already requires fingerprint equality. This repairs an extraction error; it does not change Roku or introduce a new UX. Added same-name/different-fingerprint and legacy missing-fingerprint acceptance cases.

## 2026-09-13 — Shared TV-web rebuild and design synchronization

Authorized the Roku-matching presentation replacement for the shared Tizen/Vizio frontend. TV_WEB_UI_REBUILD.md indexes complete screen/state acceptance against the existing normative visual and interaction specs without duplicating geometry. docs/process/DESIGN_SYNC.md defines immutable design adoption, vendored snapshot/asset integrity, separate freshness checks and per-platform parity evidence. Figma-first authoring is proposed for a future explicit adoption decision; the versioned design repository remains authoritative. No completed visual or device acceptance is claimed here.

## 2026-09-13 — Rail and action alignment extraction precision

Corrected the rail origin, row spacing and V-mark geometry from frozen Roku MainScene.xml, and made ActionRow horizontal/vertical centering explicit for Settings. These are source-backed extraction corrections, not Roku changes. Documented the shared TV-web existing source-quality filter as a retained implementation adaptation with explicit acceptance and parity limits; no owner-approved exception or completed parity is claimed.

## 2026-09-13 — Shared TV rebuild delivery

Recorded the shared React replacement, scoped 43-unit/49-browser validation, Settings/Search comparisons, source-filter difference, and immutable sync/PR workflow in TV_WEB_UI_REBUILD.md (removed; see git history). Physical TVs and other matched-content visual states remain pending.

## 2026-09-14 — Responsive history and populated-card corrections

Specified RUI-023 in RESPONSIVE_PRODUCTION.md (removed; see git history): actual page history and return context, top-left Back, OLED in Settings, direct live-channel activation, real Continue Watching semantics, stacked hero focus stability and contained live logos. These are owner-requested corrections under implementation; browser and hardware results remain separate evidence.

## 2026-09-17 — Shared platform matrix and playback consolidation decision

Recorded the accepted platform matrix (shared tv-web UI for web, Tizen, Vizio and desktop; Android keeps its own UI; no transcode on Android and desktop, probe-first on web, native-preferred on Tizen, managed-allowed on Vizio), the WebCodecs-not-WebAssembly browser gate, the verified absence of a deployed Vizio cast receiver, and the decision that tv-web's player stack becomes the canonical implementation moved into the video package while video's guest-js backends are replaced. No behavior changed; Roku remains the frozen baseline. See [docs/adr/0003-shared-platform-matrix-and-playback-consolidation.md](docs/adr/0003-shared-platform-matrix-and-playback-consolidation.md).

## 2026-09-18 — Desktop-first layout specification
 
Recorded the desktop shell decisions: a non-expanding left sidebar, no max
width with a window minimum instead of mobile breakpoints, hover/focus card
affordance, a hero with its own catalog-mix data decoupled from Continue
Watching, and card selection navigating directly to the info page instead of
mutating the hero. The layout shares tv-web components per the
shared-platform matrix; implementation is tracked separately.

## 2026-09-19 — Desktop frameless titlebar and sidebar refinement

Specified the integrated 30px desktop titlebar spanning the full width of the
window with isolated drag regions and no-drag button isolation, a 54px compact
left sidebar anchored beneath the titlebar, and scrollbar slot containment
starting beneath the header.

## 2026-09-20 — Desktop window decorations, player overlay, and selector UX

Specified frameless Wayland window resizing via 8-zone directional handles and
native outline/rounding (`10px`), titlebar focus elimination (`tabIndex={-1}` and
transparent focus override), back navigation in desktop header, windowed player
titlebar retention with fullscreen toggle, 2.5s player controls timeout, grey
buffered seekbar progress, live TV mute toggle semantic, sleek anchored audio and
subtitle popup cards with active track indicators, fixed 44x44 action buttons, and
compact 60px live TV channel rows.



## 2026-09-21 — Proposed local addon mode contract

Added [docs/archive/LOCAL_MODE.md](docs/archive/LOCAL_MODE.md) proposing account-free operation of the shared viewing client from an on-device addon registry: build-level availability (never in the backend-hosted flavor), sign-in-screen entry, a versioned registry schema with install/remove/error states, discover reuse of the RUI-030 hierarchy with the shared negotiation rules, direct-first playback without server sessions, and privacy rules treating manifest URLs as credentials. Watch-state is explicitly out of scope. Status: proposed; no adoption is claimed for any platform.

## 2026-09-21 — Local addon mode schema amendment

Amended docs/archive/LOCAL_MODE.md LM-002: the registry stores `nextOrdinal` and each addon a stable `ordinal` (a monotonic install counter, never reused) so addon selection survives restarts and removals. No other behavior changed.
## 2026-10-02 — AND-043 Title source summary

Specify Android Title discovery lifetime, shared Core ranking, safe source summary
copy and manual-picker adoption, with empty/failure/cancellation acceptance. The
TvTitle positive-progress WATCHING marker now has explicit state semantics and
geometry; completed episodes retain the existing Watched badge. Proposed scope
for design#6; emulator and physical parity remain independently unverified.
