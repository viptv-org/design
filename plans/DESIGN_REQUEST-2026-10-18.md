# VIPTV — design requests (what the canvas does not cover yet)

For the design AI: these screens exist in the app but have **no board in the
2026-10-18 canvas export**. Design them with the same tokens, type roles,
focus rules and component vocabulary as the existing boards. Data shapes below
are the real fields the app has — design only what the data can fill; mark
anything you wish existed and we will tell you if it can be added.

---

## 1. Settings → Source integrations (all platforms: TV, phone, tablet, desktop, web)

**What it is.** Configure the built-in "VIPTV Sources" engine (a TMDB API key
plus optional provider list) and the Live TV providers (Xtream Codes, M3U
playlist). Per-profile credentials; values are write-only (never displayed
after saving). Currently there is **no board for any of this** on any platform.

**Screens needed**

1. **Integrations list** (a settings section, not a dialog):
   one row/card per installed integration.
2. **Configure page** (full screen on TV, dialog/page elsewhere) for each
   integration type.
3. **Remove confirmation** (existing pattern: confirm dialog with the
   consequence spelled out).

**Data per row (list page)**

```
name            "VIPTV Sources" | "Xtream live TV" | "M3U live TV"
state           one of: Ready | Needs configuration | Unavailable on this connection
connection_id   null until configured
```

**VIPTV Sources configure form**

```
credential_fields[1]:
  id        "tmdb_api_key"
  label     "TMDB API key"
  required  true
  secret    true            (masked entry)
provider_choices[]: up to ~20 direct-stream providers, ids like
  "videasy", "vidlink", "vidfast", "cineby", ... (English-only set)
  each: { id, label }
maximum_providers  12        (leave empty = default selection)
```

**Xtream form** `server_url (required, url) · username (required) · password (required, secret)`
**M3U form** `playlist_url (required, secret) · epg_url (optional, secret)`

**States to draw:** unconfigured, configured ("Replace configuration"),
saving (busy), validation error, unavailable (engine not present), remove
confirm. On TV: full-screen page, TV keyboard entry, dpad-focusable provider
rows, Save/Cancel as TV buttons; Back returns to the list. **No X buttons on
TV** — Back is the close affordance. On phone: bottom-sheet or dialog;
desktop/web: centered dialog. Provider rows are multi-select chips with a
selected-count ("3 of 12").

**Copy to respect:** credentials are never displayed after saving; "Values
stay on this device"; configuration applies to the current profile.

---

## 2. Movies / Series browse pages (update the existing boards)

The existing `Tv3Movies`, `Tv3Browse`, `D3Browse`, `SkDiscover` boards are the
starting point, but the real data shape has more than they show. Redraw with:

**Header / provider switch.** Catalogs come from the selected browsing
provider — a **Stremio add-on catalog** (e.g. Cinemeta "Popular", "IMDb Top")
or **Simkl lists**. Data:

```
catalog: { id, name ("Popular", "IMDb Top 250", "Trending"), type (movie|series|anime),
           connection_name ("Cinemeta", "Simkl") }
```

Design the provider/catalog switcher (TV: a row of catalogs or a sheet;
desktop/web: dropdown or sidebar; phone: sheet) and a small "Data from Simkl"
attribution wherever a Simkl catalog is shown.

**Facet filters.** Controls are a list of typed facets (server-driven, so the
UI must handle any of these kinds):

```
control: { id, label, kind: Text | SingleChoice | MultiChoice | Toggle | Number | Date,
           required, choices[] { value, label }, maximum_selections? }
typical:  Genre (MultiChoice), Sort (SingleChoice: Popularity, Rating, Year, A-Z),
          Decade/Year (SingleChoice or Number), Rating (SingleChoice: Any, 7+, 8+, 9+),
          keywords (Text)
```

TV: filters open as a full-screen sheet/panel with dpad navigation
(see `Tv3Browse`, `SkTvFilters` for the pattern); phone: bottom sheet
(`SkMFilters`); desktop/web: a filter rail or popover. Show applied-filter
chips above the grid.

**Cards.** Same grid/row geometry as the canvas, with these real fields:

```
card: {
  title
  poster (2:3)  and/or landscape (16:9)
  metadata: { year, runtime_minutes (movies), genres[], rating (IMDb 0-10),
              certification ("TV-MA") }
  progress         0..1 (Continue-watching style; only when watching)
  badges[]         e.g. "Watched", "New episode", "Simkl"
  kind             movie | series | anime
}
```

**States to draw:** loading (skeleton grid), empty ("Nothing matches these
filters"), error + retry, filter sheet open with selections, more pages
loading as you scroll (no "Load more" button — the grid appends), and the
**Simkl variant** of the grid (Simkl cards can also carry list context:
"In Watchlist", "Completed", "Watching" — draw a badge treatment).

**Series-specific additions** (Movies page stays as the canvas has it):
season/episode counts ("4 seasons · 38 episodes" from Simkl when available),
airing status badge ("Returning", "Ended"), and "Up next · S4 E16" style
labels for shows the viewer is watching. These come from Simkl progress;
mark them Simkl-attributed.

---

## 3. Smaller missing screens (optional, but the app renders them)

- **Recovery codes screen** — after account creation/recovery: code display,
  copy/write-down step, "Done" (no board exists).
- **Parental controls settings content** — the sidebar entry exists in boards,
  the content pages (age rating picker, approved titles, parent PIN) do not.
- **Sources sheet empty/error states** — `Tv3SourcesLoading` covers loading;
  add: "N providers returned torrent links this TV cannot stream directly.
  Add a debrid service (for example TorBox)…" and "VIPTV Sources could not
  run. Check its TMDB key in Settings…" error states.
- **TV add-on manual entry** — `Tv3SetAddons` shows the QR flow; the manual
  URL entry dialog (address field + Install/Cancel) has no board.
- **Display settings** (theme/accent/OLED) and **About** content pages.

---

## Platform rules (from the canvas, restated for these boards)

- TV 1920×1080, safe area 96×54, focus = off-white inversion or 3px inner
  ring, no scaling, no key hints, no X buttons (Back closes).
- Phone 390×844, bottom sheets, 44px targets.
- Desktop 1440×900, icon rail, dialogs 460, popovers for filters.
- Web 1280×800 (and 1920 variant), tablet 2-column at 1024+.
- Accent only for progress, marks/logo and toggles; primary buttons off-white.
- Loading = skeletons, never "Loading…" pages; no "Load more" buttons.
