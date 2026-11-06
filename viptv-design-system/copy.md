# UI copy

These are the exact strings used on the screens. Text in `[brackets]` is a placeholder or proposed value, not final copy. Sentence case everywhere except eyebrows (uppercase) and product names.

## Names

- **My List** is the saved-titles list, everywhere (the nav tab, page title, menu item and toasts). Do not use "Library" or "Watchlist".
- **Continue Watching** is the in-progress list: the second segment of My List, and the Home shelf ("Continue watching" as a shelf heading).
- **Watch on TV** is the phone-to-TV remote, proposed for Android phone and tablet ([AND-038](../docs/platforms/ANDROID_DESIGN.md#and-038--android-phone-and-tablet-vizio-remote-2026-11-02)); it is not built yet. No layout has an **On TV** rail item or a Settings row for it today; a TV signs in with **Settings › Account › Add a device** (`components.md` §11 keeps the design).
- Search placeholder: **"Search movies and series"** (desktop and web show no keyboard-shortcut hint).
- Android TV native input: **"Results"**, **"Done"**, **"Unlock"**, **"Cancel"**. The device owns IME action labels; the app shows no custom keyboard or jump-to-results hint.
- Android TV episode jump (AND-EPISODE-JUMP-001): chip **"Episode #"**; dialog **"Jump to episode"**; field **"Episode number"**; actions **"Go"**, **"Cancel"**; invalid input **"Episode not found in this season."**
- Android completed episode (AND-EPISODE-WATCHED-001): visible and accessible badge **"Watched"**.

Continue Watching card, caught up (a series the profile has finished as far as it is released):

- Phone, tablet, desktop, web: **`S3 E4 · Watched`** under the title, then **`S3 E5 · Nov 4`** on its own line; **`S3 E5 coming soon`** while the next episode has no air date. With nothing announced: **`S3 E4 · Watched`** alone.
- TV: **`S3 E4`** then **`S3 E5 · Nov 4`** (or **`S3 E5 coming soon`**) on the card's one meta line, the corner check saying watched. With nothing announced: **`S3 E4`** and the check.
- An episode with no season reads **`E4`**. The air date is the month and day, in the device's locale and never the year (**`4 nov.`** in French).
- Spoken as drawn: "Show, S3 E4 · Watched, S3 E5 · Nov 4" on phone, tablet, desktop and web; "Show, S3 E4, Watched, S3 E5 · Nov 4" on TV.

Details episode selector, air date and upcoming (EPISODE-AIR-DATE-001):

- A released episode shows its air date under the caption: month, day and year in the device's locale (**`Mar 4, 2026`**, French **`4 mars 2026`**).
- A planned episode shows **`Upcoming · Airs Mar 11`** under the caption; with no announced date it shows **`Upcoming`** alone. The upcoming air date is month and day only, no year.
- An episode with no date that is not upcoming shows no date; the row stays the same height whether or not a date exists.
- Opening an upcoming episode explains **`This episode isn't out yet.`** instead of fetching sources.

Title detail Starring line:

- The detail hero reads **`Starring [names]`** — up to three top-billed cast names, comma-separated, in billing order — on one muted line under the description. A title with no cast names shows no Starring line.

Responsive player picture mode (WEB-PLAYER-FIT-001): visible toggle **"Fit"** / **"Fill"**, the word alone with no icon; accessible actions **"Fill video"** / **"Fit video"**.

Player Audio & subtitles panel ([PLAY-TRACKS-001](../specs/behavior/player-audio-subtitles-panel.md)):

- Panel title **Audio & subtitles**; accessible pane name **Audio and subtitles**; the × is **Close track selection**.
- Audio column heading **Audio**, collapsed to **Default audio** with zero or one track.
- Subtitles column heading **Subtitles**; the first row is **Off**; the empty note is **No subtitle tracks available**. A subtitle row's primary line is the language name (**English**, **Croatian**) and its secondary line the source (**OpenSubtitles v3**); several sources of one language join with ** · **.
- Inline settings rows share the Settings page copy: **Show subtitles** (**Always** · **When audio isn’t [language]** · **Never**), **Language** (**Default** when none), **Size** (**Small** · **Medium** · **Large**), **Background** (**None** · **Box**).
- The footer link stays **Subtitles & audio settings**.

Next-episode end panel (PLAY-NEXT-AUTOPLAY-001):
- TV: eyebrow **"Next episode"**; primary **"Next episode in [N]"** while counting, otherwise **"Play next episode"**; secondary **"Keep watching credits"**; caption **"[Series] · Credits"**.
- TV footnote: **"Starts automatically. Press any button to cancel."** while counting; **"Nothing plays on its own."** with the setting off or after a cancel.
- Phone, desktop and web: eyebrow **"Up next"**; primary **"Next episode in [N]"** while counting, otherwise **"Next episode"**; secondary **"Watch credits"**. No footnote.
- Settings › Playback: **"Autoplay next episode"**, described as **"Plays the next episode after a 10-second countdown. Applies to this device."** The phone group heading is **"Next episode"**. The `Next episode button` row reads **"Shows during the credits"**, without "Nothing ever plays on its own".

Source groups (proposed, SRC-BEST-MATCH-001): source list group headers **"Best matches"** and **"All sources"**, displayed uppercase as group labels and announced as headings. The row marker stays **"Best match"**.

Source row menu (proposed, SRC-ROW-MENU-001): **"Play this source"**, **"Source details"**, **"Configure [add-on]"**, **"Hide this add-on's sources"**, **"Cancel"**. **Configure** names the add-on the source came from (**"Configure Torrentio"**); a source whose add-on reports no name reads **"Configure this add-on"**. Hiding leaves **"No matching sources. Choose another provider or quality."** where the hidden rows were.

Source picker status (proposed, [SRC-DRAWER-001](../specs/behavior/source-drawer.md#no-best-match-hint)): no layout shows a hint about how Play picks a source. **"Play always starts the best match. Change … in Settings › Playback."** is retired on phone, tablet, desktop/web and TV. The TV status line under the list reads **"Finding sources"** while nothing has arrived, **"Still checking sources"** once sources have arrived but discovery is still in flight, and **"Opening stream…"** (or the current opening stage) while a stream opens. It is hidden otherwise.

Phone title source-summary row (AND-043): accessible name **"Choose source"**. With a best source it reads a quality badge — **"Auto"** when the source reports no quality — then **`[provider] · [N sources]`**, singular **`1 source`**. A settled discovery with no rows reads **"No sources found"**; a failed or timed-out discovery with no rows reads **"Sources unavailable"**.

Pull-to-refresh (proposed, [REFRESH-PULL-001](../specs/behavior/pull-to-refresh.md#copy)): no copy. The indicator has no label, and no toast or error reports the result. An expired session shows the existing **"Session expired. Sign in again."** on sign-in.

App update screens (proposed, [AND-APP-UPDATE-001](../specs/behavior/app-updates.md#updating-screen)): choosing **Install** covers the app with the Updating screen. Title **"Updating VIPTV to [versionName]…"**; while the APK is written into Android's installer session the body reads **"Writing the update. Android asks you to confirm before it installs."** and the progress reads **"[N]%"**; while Android's confirmation is up the body reads **"Confirm the update in the dialog Android is showing."** and the bar is indeterminate. The line under it reads **"VIPTV restarts by itself when the update is installed."**, or **"VIPTV closes when the update is installed. Open it again to finish."** where the app cannot reopen itself. The permission step is the same screen: **"Allow updates"**, **"Allow VIPTV to install apps in the screen that opens, then come back to finish the update."**, **"The update continues by itself when you come back."**, **"Open settings"** · **"Later"** (Fire TV without that screen: the settings path and **"Try again"** · **"Later"**). An install Android rejects comes back on the prompt as **"Couldn't update VIPTV"**, **"Android didn't install the update."**, **"Try again"** · **"Later"**. After the relaunch **"Updated to [versionName]"** sits at the bottom for six seconds.

Server-required update (proposed, [AND-APP-UPDATE-001](../specs/behavior/app-updates.md)): a `client_update_required` answer raises a notice titled **"Update required"** reading **"Update VIPTV to use this server's current catalog and playback APIs."** with **"Update"** · **"Not now"**; **Update** opens the in-app updater on Android and reloads the page on the web, and desktop, which has no in-app delivery path, shows **"Not now"** alone.

Filter bar and chip lists (FILTER-CHIP-001, `components.md` §2): a chip reads **"[Title]: [value]"** — "Genre: Any", "Genre: Comedy", "Sort: Popular", "Type: All", "Quality: All", "Source: All sources", "Catalog: Popular" — and an unset required chip reads **"[Title]: Required"**. The row ends with **"Clear"** (an × icon and the word) while any filter is set. A list's search field is **"Search [title]"** ("Search genre", "Search catalogs", "Search lists", "Search sources") and a text filter's field is **"Enter [title]"**; pointer layouts add **"Press Enter to apply"**. Rows read **"Current"** on a single choice's pick, **"· unavailable"** on an option that cannot be picked, and the clearing row is **"Any"**, or the control's own **"All"** / **"All sources"**. An empty search says **"No matches for [text]"**. The sheet's accessible close label is "Close".

## Empty states

| Where | Copy |
|---|---|
| My List | Your list is empty. Add titles with the + button. · **Browse Home** |
| My List, no matches | No matching titles. Try changing or clearing the filters. · **Clear filters** |
| My List, results still arriving | **Loading matching titles…** · Results update as metadata becomes available. |
| My List, first read failed | **Couldn’t load My List** · the message the request read · **Try again** |
| Continue Watching | Nothing in progress. Titles you start watching appear here. |
| Continue Watching, first read failed | **Couldn’t load Continue Watching** · the message the request read, otherwise **Check the connection and try again.** · **Try again** |
| Home, no catalogs | **No catalogs are available.** · Add or enable a catalog add-on in Settings. · **Open settings** |
| Home, catalogs with no titles | **No titles yet** · Your catalogs answered with nothing for this profile. · **Try again** |
| Home, first read failed | **Couldn’t load Home** · the message the request read · **Try again** |
| Home, an action failed | never a page state: the failure stays on the control that acted, as §9 rule 5 of [components.md](components.md#9-feedback) says |
| Calendar, nothing scheduled | Nothing is scheduled in these dates. · **Manage integrations** |
| Calendar, no source | The calendar needs series in My List or a Simkl connection. · **Manage integrations** |
| Calendar, empty day | None of your shows air this day. (All shows: No releases for this day.) |
| Calendar, first read failed | **Couldn’t load the calendar** · the message the request read · **Try again** |
| Discover, no catalogs | No catalogs are available. Add or enable a catalog add-on in Settings. |
| Discover, required filter | Choose the required filters to browse this catalog. |
| Discover, no titles | No titles yet |
| Search, no results | No matching titles |
| Search, no query | **Recent** · **Clear** · **Trending searches** |
| Search, provider failed | **This search provider could not respond. Try again.** · **Try again** |
| Search, some results unavailable | **Some search results are unavailable. Try again.** · **Try again** |
| Live, no source (LIVE-EMPTY-001) | Eyebrow **LIVE TV** · **Live TV isn't set up yet.** · **Add an IPTV connection with Xtream or M3U, or install a live add-on. Channels, the guide and favourites appear here.** · **Set up live TV** · **Add-ons** |
| Live, no source, member (LIVE-EMPTY-001) | **Only the household owner can set up live TV.** |
| Live, no source, paired TV (LIVE-EMPTY-001) | **Manage live TV from a signed-in phone, computer or the web dashboard.** |
| Live, no channels (LIVE-EMPTY-001) | **No channels came back.** · the server's own human reason when it sent one, otherwise **This source is set up, but it isn't sending channels.** · **Try again** · **Source integrations** |
| Live, first request failed (LIVE-EMPTY-001) | **Could not load Live TV.** · the message the request read, otherwise **Something went wrong. Try again.** · **Try again** · **Source integrations** |
| Live, empty category | No channels here yet. Choose another category. (TV / desktop: "…another filter.") |
| Live search, phone | No channels match your search. |
| Live search, desktop / TV | No channels match your search. |
| Sources, finding | Finding sources. Sources appear here as they arrive. |
| Sources, provider pending | Still checking [provider] |
| Sources, provider empty | No playable sources from [provider] |
| Sources, provider unsupported (proposed, SRC-TORRENT-GATEWAY-001) | [provider] returned formats this app cannot play. Choose another source. |
| Sources, unsupported API format (proposed, SRC-TORRENT-GATEWAY-001) | This source format is not supported. Choose another source. |
| Sources, in-progress label before rows | Finding sources |
| Sources, in-progress label after rows | Still checking sources |
| Sources, none | No sources available. Check your add-ons in Settings. |
| Sources, filtered out | No matching sources. Choose another provider or quality. |
| Sources, failed | **Couldn't load sources.** · the message the request read, otherwise **Something went wrong. Try again.** · **Try again** |
| Live details, no guide | No guide information. You can still watch this channel. |
| Local mode, no addons | Install an addon to start browsing. |

Live, no source ([LIVE-EMPTY-001](../specs/behavior/live-empty-state.md)) replaces
three app strings that were never in this file: **"No channels are available for
this profile."**, the **"Manage add-ons"** button and the **"All channels"**
button in that state. The filtered Live line and its **"All channels"** button
stay for a filtered page. Live with no channels never says "No channels" while
the request is still open, and its loading form has no copy at all. The app
ships **Only the household owner can set up live TV.** as the member line and
shows a member no setup actions; the owner gate also hides the no-channels
**Source integrations** secondary
([viptv-org/app#492](https://github.com/viptv-org/app/pull/492)). A first Live
request that fails with no page is a failure, not an empty answer: it reads
**Could not load Live TV.** and the message the request read, never **No
channels came back.**
([viptv-org/app#541](https://github.com/viptv-org/app/issues/541)).

A search result area's failure line sits under the heading of the provider that
failed, and under the scope row when no provider returned anything. Its **Try
again** re-runs the query the viewer already typed, for every provider, so
nothing has to be retyped
([viptv-org/app#821](https://github.com/viptv-org/app/pull/822)). A failure line
repeats once per failed provider and never replaces the results that loaded.

## Live

Live preview (LIVE-PREVIEW-001): the preview frames the programme the guide picked by the clock, not by the selection. Phone draws the **LIVE** badge, the progress bar and **"[N] min left"** only while it is on air; before it starts the line reads **"Starts at [time] · [N] min"**, where [N] is the programme's own length, and after it ends **"Ended"**. A programme that is not on air carries no LIVE badge and no bar. TV and the desktop preview keep their **"start – end"** line and append **" · [N] min left"** while it is on air, **" · [N] min"** before it starts and **" · Ended"** after it ends.

- **Preview:** the channel line reads **"[number] · [channel]"** (**101 · BBC One HD**), then the programme's title, then the description on TV and the desktop; phone stops after the status line. Tablet, desktop and the browser draw **Watch** (play icon) as the primary beside it and **Full guide** (grid icon) when the channel has a guide that day; the guide replaces the preview and a **Show preview** text button brings it back. Phone has no actions: tapping the card starts the channel.
- **Favourite:** one control, one wording. **Favourite channel** saves it, **Remove favourite channel** removes it, **Saving…** replaces the label while the write is in flight, and **Retry** (rotate icon) replaces it once with the server's own line above when the save failed. The phone channel rows' star carries the same two labels as its accessible name, and the filter chip is **Favourites**.
- **TV preview:** the same star action under the programme, and the artwork tile beside it is one focus stop reading **OK to watch** (play icon) over the picture.
- **Channel rows** (phone, tablet, desktop): the programme on now, then **"[start]–[end]"** beside the progress bar, then **"Next: [programme] [time]"** when the guide knows what follows. The row's thumbnail carries the channel number under its artwork.
- **Favourites with nothing to show:** **No favourite channels from [source].**, **No favourite channels from this source.** when the server named no source, or **Loading favourite channels…** while the first read is still open, with the **All channels** action.

## Calendar

- **Chip row:** **Type: All** (default), **Type: TV**, **Type: Anime** or **Type: Movies**; **Shows: Your shows** (default) or **Shows: All**; the week actions **Previous week**, **This week** and **Next week**; and the week's range, its first and last day, each the month, day and year in the device's locale, joined by **–** (**Nov 6, 2026 – Nov 12, 2026**; French **6 nov. 2026 – 12 nov. 2026**). One row filters first on tablet, desktop, web and TV; phone puts the week actions and the range on the row above and **Clear** with the filters. **Previous week** and **Next week** are absent at the 52-week ends.
- **Day strip:** phone cells read the weekday's short form (**Mon**) over the day's number (**13**), with a dot under a day that has releases; wider layouts read **Today**, **Tomorrow** or the weekday's full name (**Friday**), shortened to the short form when the name does not fit its column. The phone's group heading repeats the day: **Today** beside **Nov 6, 2026**.
- **Release row:** the time (**8:00 PM**, or the 24-hour form on a 24-hour device), the title, then **"S[season] E[episode] · [episode title]"** (**S4 E3 · Negotiating with Tigers**), and the badge **Your show** when the release comes from the profile's own list (My List or Continue Watching).
- **Row action:** once the release has aired, **Find S3 E3** for an episode or **Find sources** for a movie; before it airs the row has no action.
- **TV preview:** the title, **Your show**, the description, and one action — **View details** (info icon) when there is nothing to play, otherwise the row's own action label with the play icon — and, when the release did not come from the profile's own list, **Data from Simkl** under it.
- **Fallback:** when nothing from the viewer's list airs in the visible week, **Nothing from your list this week — showing all releases.** sits above the list, which then shows every public release.

## My List

- The **History** row above the grid reads **History** over **Everything you've played**, with a chevron, and opens the viewing history.

## Details

A title's page (`components.md` §6). Phone and tablet switch sections with the tabs **Episodes**, **More like this** and **Details**; desktop and web stack **Episodes** and **More like this**; TV shelves them under the hero.

- Hero actions: **Play**, or **Resume** while the profile is part way through, with the episode named: **Resume S1 E3**, **Play S1 E3**. The restart beside it is **Play from the beginning** (the title menu's same action is **Watch from the beginning**). A part way episode's progress line reads **14m left**, or **Almost done** under 1 minute. The play trigger's accessible name while it starts is **Starting playback**.
- Above the actions, the same line on every layout: the kind (**Series**) on phone, tablet and desktop, the year, the runtime (**44m**, **1h 40m**), genres joined **Drama / Mystery**, the rating **★ 8.0**, then presentation badges (**4K**, **HDR**) and a certification such as **TV-MA**. The Starring line under the description has its own entry above.
- Episode list: a row's caption is `[number]. [title]`, the phone row adds its runtime (**44m**, **1h 4m**) and **14m left** for the episode being continued, and the episode being played from this page reads **Now playing**. Air dates and upcoming rows are in the [Details episode selector](#names) entry above. The season picker reads **Season 1**, **Specials** for season 0 and **Other episodes** for unnumbered episodes; a season's count is **6 episodes** or **1 episode**. TV's chip reads **Season 1**, or **Episodes** when the title has one season, and its jump chip **Episode #**.
- Details tab facts: the label column reads **Season** / **Seasons**, **Episode** / **Episodes**, **Votes** and **Also known as**.
- Source row under Play: **Auto** while the best source has no quality, then `[provider] · [N sources]` (**1 source** in the singular); a settled search with no rows reads **No sources found** and a failed one **Sources unavailable**. Its accessible name is **Choose source**. TV's source button is **Best match**.
- My List: **My List** under the phone control, **Add to My List** / **Remove from My List** as the control's accessible name and the tablet and web label, **Saving…** while the write runs, and on failure the line **Could not save this change. Try again.** with **Retry**.
- Failures and cover: **This title couldn’t load** with **The provider didn’t return this title’s details.**, **Try again** and **Go back**; **Loading title details** while it reads. TV's dialog is **Title options**, and **No trailer is available for this title.** is its body. The web dialog's close action is **Close details (Esc)** and its pane name **Title details**; TV's season selector closes with **Close seasons** and the picker **Choose season**.
- Signed out: **Sign in**, **Sign in to watch**, and **Already using VIPTV on a TV? Sign in here with the same account.**

## Toasts, notices and loading

- Added to My List
- Removed from My List (**Undo**, §9 toast)
- Removed from Continue Watching (**Undo**, §9 toast)
- Could not save your profile. Please try again. (error, Dismiss)
- [VIPTV could not start.] (startup error, Try again)
- The stream could not seek there. (player notice)
- Error-slate notice ([SRC-ERROR-SLATE-001](../specs/behavior/error-slate-detect.md)): **This source might not be working.** Then **[Add-on] handed back this video. Its settings may need a new key.** (no provider name: **This source's settings may need a new key.**) with **Configure source** and **Choose another source**.
- Preparing playback…
- Player opening screen (proposed, [SRC-BEST-MATCH-001](../specs/behavior/source-best-match.md) and [components §9](components.md#9-feedback)): the dimmed title art fills with real startup progress and the status line under it names the stage. It reuses the existing lines — **Finding sources**, **Still checking sources**, **Opening [provider] [quality]…** — and never shows a percentage or a byte counter, so no string is added.
- Loading more titles… / Loading more channels… / Loading more channels… [120] of [860]
- Paging footer: a finished list reads **"You’ve reached the end."**; a later page that fails reads **"Couldn’t load more"** with a **Retry** button.
- Still checking [2] addons
- Partial add-on failure (ADDON-FAILURE-001): a Browse/Discover page that loaded shows this above the grid and a Details page near the metadata, only when some results loaded — **`[Add-on] didn't respond`** (two add-ons: **`[Add-on] and [Add-on] didn't respond`**; more: **`[Add-on] and [N] more didn't respond`**) with the action **Manage add-ons** opening Settings › Add-ons. It never replaces or hides the results that loaded.
- Can't reach the backend. The backend is down or unreachable. Retrying in [n] seconds; this clears itself once the backend answers.
- Pending labels (on the acted element, never a toast; §1 button state): **Saving…** · **Removing…** · **Installing…** · **Connecting…** · **Checking…** · **Signing in…** · the play-trigger **Starting playback** (accessible name). The failure line that follows a revert is the existing inline error with **Retry**, not a toast.

## Errors

- The username or password is incorrect.
- Incorrect PIN. Try again.
- Enter a 4–8 digit parent PIN
- Enter a name to continue.
- Enter a value for this required filter.
- Enter an HTTPS manifest URL.
- That does not look like an addon URL.
- This addon is already installed.
- This source could not be played / The selected source did not become ready in time.
- Playback failure page: **This source stopped working**; `[Source] didn’t respond. Choose another source.` (`to continue from [time]` when playback had a position above 0); **Try [next source]**, **Choose another source**, **Back**.
- Playback could not be restored
- The TV could not complete this request.
- VIPTV receiver is unavailable (HTTP [status]). The TV was not launched.
- VIPTV receiver did not serve its app bundle. The TV was not launched.
- Could not check the VIPTV receiver. Check your connection and try again.
- The TV accepted the launch request. Check its screen to confirm VIPTV opened.
- This code expired. (sign-in code; TV pairing offers **Try again**, phone and desktop **New code**)

## Native playback failure reasons (SRC-TORRENT-NATIVE-001)

These strings replace the generic native startup explanation only when a
platform reports the corresponding observed fact to shared Rust. Unknown
failures use `native_playback_failed`. A deadline is not proof of absent peers
or seeders. Raw engine/player text, hashes, URLs, paths and credentials are never
presentation inputs. Existing recovery actions and geometry remain as specified
in [the native contract](../specs/behavior/torrent-native-android.md).

| Observed reason | Exact copy |
|---|---|
| `native_playback_failed` | The selected source could not start on this device. Try another source or retry playback. |
| `native_acquisition_timeout` | This device took too long to prepare the selected source. Try another source or retry playback. |
| `native_metadata_timeout` | No torrent metadata arrived from peers before the startup deadline. Check DHT/network access or choose another source. |
| `native_session_timeout` | The device timed out creating its torrent network session. Check network access and retry playback. |
| `native_cache_preparation_timeout` | The device timed out preparing local torrent storage. Check free space and retry after the previous stream has stopped. |
| `native_initialization_timeout` | Torrent metadata arrived, but the local torrent engine did not initialize in time. Retry playback or check device storage. |
| `native_loopback_timeout` | The torrent initialized, but the local playback endpoint did not open in time. Retry playback. |
| `native_session_unavailable` | The device could not create its torrent network session. Check network access and retry playback. |
| `native_initialization_failed` | Torrent metadata arrived, but initializing its local storage or torrent engine failed. Check device storage or choose another source. |
| `native_loopback_unavailable` | The torrent initialized, but its local playback endpoint could not be opened. Retry playback. |
| `native_retirement_pending` | The previous torrent is still closing. Wait a moment and retry playback. |
| `native_dns_unavailable` | The device could not resolve the playback server address. Check DNS or your network connection. |
| `native_tls_failed` | The secure connection to the playback server failed. Check the device clock and server certificate. |
| `native_connection_failed` | The device could not establish a network connection to the playback server. Check that the server is running and reachable. |
| `native_control_timeout` | The playback server did not respond before the request deadline. Check server health and your connection. |
| `native_payload_limit` | The device's playback cache has no room for this stream. Stop another stream, choose another source or retry playback. |
| `native_storage_unavailable` | This device could not reserve storage for playback. Free some space, choose another source or retry playback. |
| `native_cache_unavailable` | The device's playback cache is unavailable. Choose another source or retry playback. |
| `native_metadata_invalid` | This source has invalid or unsupported torrent file information. Choose another source. |
| `native_file_unavailable` | The exact file selected by this source is missing or does not match its file information. Refresh the sources or choose another source. |
| `native_authorization_expired` | This playback session has expired. Start playback again to reconnect. |
| `native_network_unavailable` | This device could not connect to the selected source. Check your connection, choose another source or retry playback. |
| `native_codec_unsupported` | This device cannot decode the selected source's audio or video format. Choose another source or retry playback. |

Native failure messages append a blank line and `Diagnostic: <observed reason>`
using only the validated closed code in the table. This is visible in the existing
recovery dialog and can be quoted when reporting a failure.

## Player

Controls and states on every platform (`components.md` §10). Phone, tablet and web show the picture mode toggle **Fit** / **Fill** (see the [picture mode](#names) entry above), and the track panel's strings are in the [Audio & subtitles](#names) entry above.

- Transport: **Play** / **Pause**, **Forward 10 seconds**, **Back 10 seconds**, **Mute or unmute**, **Volume**, **Enter fullscreen** / **Exit fullscreen**, **Hide controls** / **Show controls**, **Lock** / **Unlock controls**, **Close playback**, **Episodes** with **Close episodes**, the track panel button **Audio & subtitles**, and **Streams** for the compact audio/subtitle button.
- Timeline: the position and duration labels read `[12:48]` / `[52:10]`, TV adds **Ends at 8:42**, the slider's accessible label is **Playback position**, TV's timeline description begins **Position.**, and TV's frame preview is **Seek preview**.
- Skip prompts: **Skip intro**, **Skip recap**, **Skip credits**. At the end of an episode the panel is **Up next** with **Watch credits** or **Keep watching credits** and **Play next episode**, and with autoplay on the action counts down **Next episode in 8** (its own contract and timing are in [next-episode-autoplay.md](../specs/behavior/next-episode-autoplay.md)). TV adds **Starts automatically. Press any button to cancel.** while the countdown runs and **Nothing plays on its own.** once it stops.
- Loading and failure: **Starting playback** while an output opens; **This source stopped working** with the failure line and **Try [next source]** / **Choose another source** / **Back** are in the [Errors](#errors) list above; **This source might not be working.** with **Next source** or **Choose another source** on the fallback notice; **This device can’t decode this stream.** when the device cannot decode the stream, and TV's **This TV can’t decode this stream. Choose another source — the 4K Dolby Vision releases are not supported by this device’s decoder.** The player's title line reads the playable's title, or **Playback** when it has none.
- Tracks: a subtitle failure reads **Couldn't load subtitles.** and an audio failure **Couldn't switch audio.**, each on the row that failed. The track panel's own strings — **Audio & subtitles**, **Audio**, **Default audio**, **Subtitles**, **Off**, **No subtitle tracks available**, **Show subtitles**, **Language**, **Size**, **Background** with **Small** / **Medium** / **Large** / **None** / **Box** — are recorded in the [Audio & subtitles](#names) entry above; TV's picker offers **Extra large** as a fourth subtitle size.

## Dialogs

| Dialog | Title | Actions |
|---|---|---|
| Sign out | Sign out of VIPTV on this phone? (tablet, desktop and web: "Sign out of VIPTV on this device?"; TV: "Sign out of this TV?") | "Your profiles and progress stay on your account." · Sign out (danger) · Cancel |
| Change connection, local mode | Change connection? | "Your local library and progress stay on this device. You'll choose a server or local mode next." (TV: "Your local library and progress stay on this TV. You'll choose a server or local mode next.") · Change connection (danger) · Cancel |
| Sign out of all devices | Sign out of all devices? | "Every device, including this browser, will need to sign in again. Your profiles, lists and history stay on your account." · Cancel · Sign out of all devices (danger) |
| Sign out a device | Sign out [device name]? | "This device will need to sign in again. Your profiles, lists and history stay on your account." · Cancel · Sign out (danger) |
| Delete account | Delete account | "This deletes [name]'s account, its profiles, their history, My List, add-ons and paired devices. It cannot be undone." · Cancel · Delete account (danger) |
| Delete profile | Delete profile | "Delete [name]? This permanently removes this profile's watch history, favorites and preferences." Cancel · Delete profile (danger) |
| Remove from My List | Remove from My List? | "“{title}” leaves this list. Watched history is preserved." · Cancel · Remove (danger) · then the §9 toast with **Undo** |
| Remove from Continue Watching | Remove from Continue Watching? | "“{title}” leaves this list. Watched history is preserved." · Cancel · Remove (danger) · then the §9 toast with **Undo** |
| Remove addon | Remove [Addon]? | "Its catalogs leave this device." (local mode) · Cancel · Remove (danger) |
| Manage addon (TV) | Manage [Addon] | Enable / Disable · Reconfigure (only when the add-on is configurable) · Remove add-on (danger) · Cancel |
| Reconfigure add-on (TV, configurable add-ons only) | Reconfigure [Addon] | "Scan this code with a phone or computer camera to change [Addon]'s settings." · the configure address in text · "This code expires in 5 minutes." · New code · Close. A link the server refuses reads "Couldn't get the configure link." with the server's own line when it sent one, · Try again · Close |
| Parent PIN | Enter parent PIN (TV sign-out: "Enter parent PIN to sign out") | "Enter the parent PIN to continue." (TV: "Use your remote or a connected keyboard.") · Done · Cancel |
| Watch on TV (Android phone and tablet, proposed) | Watch on TV | "Connect to a Vizio SmartCast TV on the same network." |
| Watch on TV, browser (proposed, not implemented) | Watch on TV | "TV pairing is available in a VIPTV desktop app with SmartCast support…" · Close |
| App update (Android) | Update ready · Update required · Couldn't update VIPTV | See the [app updates contract](../specs/behavior/app-updates.md) for descriptions · Install · Later · Try again |
| Updating screen (Android, proposed) | Updating VIPTV to [version]… · Allow updates | A full-screen cover rather than a dialog; copy, states and failure flow in [app-updates.md](../specs/behavior/app-updates.md#updating-screen) · Open settings · Try again · Later |

## Sign-in and entry

The entry surfaces: Connect and the sign-in choice, the password panels, TV pairing, device pairing, the device-approval page, the profile picker and the startup screen. A **bold** string is a control that is drawn or an accessible name; a quoted string is body copy or a status line.

### Connect and the sign-in choice

- Browser (`ConnectScreen`): heading **Welcome back**, "Sign in to your VIPTV server.", the fields **Username** and **Password** with **Show password** / **Hide password**, **Sign in** (**Signing in…** while it runs), **Create account**, **Use recovery code** and, on local builds, **Use this device without an account**.
- A connection that cannot offer the method the viewer chose says so on that method's own screen with **Use a password instead**: browser "Browser sign-in is not available on this connection yet.", another device "Device approval is not available on this connection yet.". Desktop without pairing reads "Device sign-in requires a server connection." with **All sign-in options**.
- Phone and tablet (`MobileSignIn`), desktop and web (`DesktopSignIn`): heading **Sign in to VIPTV** over "Pick whichever is easiest. They all reach the same account.", then **Continue in browser** · "Approve this sign-in through your server", **Use a password**, **Use another device** · "Scan a code and approve this sign-in", **Create account** · "Open your server’s web sign-in page", and on local builds **Use without an account** · "Everything stays on this device". **All sign-in options** returns from a step.
- Password panels: heading **Sign in with a password** (TV: eyebrow **Use a password** over **Sign in with your password**) with the fields **Username** and **Password**, **Show password** / **Hide password**, **Sign in** (**Signing in…** while it runs), **Forgot password?** (inactive with "Enter your server address first." while no address is set), **Use another server** (desktop: **Hide server address** while the field is open), and on TV "Typing with a remote is slow. Scanning a code with your phone is quicker.".
- TV welcome (`TvWelcome`): the wordmark over "Your shows, channels and progress. All in one place.", **Sign in** and, on local builds, **Use without an account**; local builds read "Your addons and playback stay on this device. No account, profiles, or sync." under the actions.
- TV choice (`TvSignInChoice`): heading **Sign in to VIPTV**, **Use your phone** · "Scan a QR code — quickest", **Use a browser** · "Go to a web address and type a code", **Use a password**, local builds **Use without an account** · "Everything stays on this TV", and beside the artwork "All of these reach the same VIPTV account. You can add more ways to sign in later from your phone or computer.".

### Create account and recovery

The browser's sign-up and recovery forms state each field's rule as a hint under the field while the value follows it, and replace that hint with an inline error line (components.md §4) once it breaks:

- **Create account** (`BrowserAccountForm`): heading **Create your account**, "Create an account on this server. You’ll receive a recovery code to keep somewhere safe.", the fields **Username**, **Display name**, **Password** and **Confirm password**, **Create account**, and **Back to sign in**.
- **Recover account**: heading **Recover your account**, "Use the recovery code you saved when creating your account. This changes your password and signs out existing devices.", the fields **Username**, **Recovery code**, **New password** and **Confirm password**, **Recover account**, and **Back to sign in**.
- **Username**: hint "Letters, numbers, or . _ - @. Up to 80 characters."; errors "Use letters, numbers, or . _ - @ only." and "Use at most 80 characters.".
- **Display name**: hint "Up to 80 characters."; error "Use at most 80 characters.".
- **Password** (sign-up) and **New password** (recovery): hint "At least 12 characters."; errors "Use at least 12 characters." and "Use at most 256 characters.".
- **Recovery code**: hint "The code you saved when creating your account."; error "Use at most 256 characters.".
- **Confirm password**: "Passwords do not match." while the two differ, with no hint of its own.
- While a rule is broken the submit action stays disabled and the field that broke it carries the danger border and its error line, the same shape as the change-password form's "At least 12 characters.".

### TV pairing

The TV pairs by QR code or by a browser, both halves on one screen:

- **Scan with your phone** · "Point your camera at the code. You’ll finish on your phone and this TV signs in by itself." over the QR code; with no code yet, "Request a sign-in code, then scan it with your phone." over the empty code tile.
- **Use any browser** with the numbered steps **1 Go to** [viptv.syek.tech/device] and **2 Enter this code** [AB12CD34EF], "Code expires in [m:ss]" beside **New code**. **Use another server** replaces the server. Before a code arrives the empty code tile reads **Sign-in code**, the browser address **Your server** (**Creating a code…** while it is requested) and the code slot **No code** (**Waiting…** while it is requested).
- The status line under the board reads "Creating your sign-in code…" while a code is requested, "Request a sign-in code to continue." with none, and "Waiting for you to sign in…" while the code waits. An expired code reads "This code expired." and the action becomes **Try again**.

### Device pairing (phone, desktop and web)

- **Use another device** over "Scan this code with another device, or go to [address] and enter the code. Sign in there and approve this device.", the QR code, **Code** [AB12CD34EF] with "Expires in [m:ss]", and **New code** · **Use another server**. The status reads "Creating a sign-in code…" or "Waiting for approval…". Before a code arrives the QR tile reads **No code**, the code reads **—** (**Creating…** while it is requested), and the address falls back to "your server’s device sign-in page" (**your server** beside the browser action).
- Browser variant (**Continue in browser**): heading **Finish signing in in your browser**; with no code, "Create a sign-in link, then approve this device in your browser." and **Create a new code**; with a code, "We opened [address]. This window connects by itself when you’re done." or, when it did not open, "Approve this device at [address]. This window connects by itself when you’re done.", beside **Open browser again** and **Copy link**. A browser that cannot open reads "Could not open your browser. Copy the link to continue.". **All sign-in options** returns.

### Device approval page (/device)

- **Checking your session...** while the account session restores.
- Code step: **Enter the code on your TV** · "You'll find it on your TV under Sign in.", the **Device code** field and **Continue** (enabled at eight digits), then **Enter a different code**. A signed-in phone reads "Signed in as [username] - " with **Not you?**, and **Scan the code on your TV** opens its camera where the device has one.
- Confirm step: **Sign in to this TV?** · "Only continue if the code matches the one on your TV." over the device's name and its code in groups of four, with **Waiting for approval** or **Approved** beside it, then **Sign in the TV** · **Deny**.
- Done: **Device signed in** · "It can now pick its profile." · **Add another device**. Denied: **Denied** · "That device will not be signed in." · **Add another device**.
- A page without a session reads **Sign in to continue** · "Approve the TV with your VIPTV account." with **Username**, **Password** and **Sign in**; an unreachable server reads "Could not reach your server. Try again.".

### Startup screen

- The wordmark over the startup progress and **Getting VIPTV ready…**, with **Change connection**; the screen's accessible name is **Starting VIPTV**. Every layout that shares the entry screen draws it while the saved session restores ([STARTUP-RECOVERY-001](../specs/behavior/startup-recovery.md)).
- Startup recovery ([STARTUP-RECOVERY-001](../specs/behavior/startup-recovery.md)): when the saved session can't reach the server, the entry screen shows the reason — **"Could not reach your server. Check the connection and try again."** for a transport failure, the server's own message on a 5xx — and **"Try again"** under it. An expired session reads the existing **"Session expired. Sign in again."** and offers no action.

### Server address

- The dialog is titled **Server address** with the field **HTTPS server address** and **Connect** (phone and desktop: **Continue**). Every server-address field shares one error, drawn inline under the field (components.md §4): **"Enter an HTTPS server address, without a page path."** It covers a non-HTTPS address, a page path, a query or fragment, and embedded credentials.

### Profile picker

- **Who's watching?** · **Manage profiles** · **Done** while managing · **Add a profile** (the dialog is titled **Add a profile** with the **Name** field and **Add** / **Cancel**) · the per-profile action **Edit profile**.
- A PIN-protected profile draws the lock glyph; its accessible name is **Locked**. "A space for their favorites, shows, and discoveries." · **Find your favorite** · "[468] avatars. Pick a world, then pick your character."


## Settings

[ACCT-SPLIT-001](../specs/behavior/account-and-profile-settings.md) groups Settings into **Profile**, **Playback**, **This device** and **Account**, in that order, on every platform.

- Rows — Profile: **Profile** · **Linked services** · **Parental controls** · **Import from Stremio**. Playback: **Playback** · **Subtitles & audio**. This device: **Display** (TV) · **About** · **Help**. Account: **Account** · **Password** · **Household PIN** · **Devices & sessions** · **Add a device** · **Add-ons** · **Source integrations** · **Sign out** · **Delete account**.
- The profile card above the groups reads the profile's name with **Switch profile**. On TV the rail entry is **Switch profile**, beside a separate **Profile** entry that opens the page below.
- Profile page: **Name** · **Avatar** · **Kids profile** ("Limits titles, search and Live for this profile.") · **Maturity limit** ("Titles above this rating are hidden for this profile"; values **All ratings**, `G` `PG` `PG-13` `R` `NC-17`, `TV-Y` `TV-Y7` `TV-G` `TV-PG` `TV-14` `TV-MA`) · **Approved titles** ("Only these titles show in the kids library") · **Profile lock** ("Ask for a PIN before this profile opens") · **Language** ("Default audio and subtitles for this profile") · **Delete profile**.
- Profile page dialogs: **Name** (one field, **Save** / **Cancel**) · **Choose an avatar** (**Cancel**) · **Maturity limit** — "Titles above this rating are hidden for this profile", **Movies up to** and **Series up to** the rating labels, **All ratings**, **Allow titles with no rating**, "Unrated titles and titles whose ratings disagree stay hidden unless you allow them.", **Save** / **Cancel**. · **Set profile PIN** / **Change profile PIN** — "Ask for a PIN before this profile opens.", **Current PIN**, **New PIN** (a locked profile reads **New PIN (blank removes the lock)**), **Save PIN**, **Remove PIN**, **Cancel**. · **Delete [name]?** — "This permanently removes this profile's watch history, favorites and preferences.", **Delete profile** (danger) / **Cancel**. A write in flight keeps its dialog and draws the pending label on the acted control (**Saving…**, **Deleting…**).
- Household PIN step (Profile page, Manage profiles, Switch profile): the action titles **Turn on Kids profile** · **Turn off Kids profile** · **Change the maturity limit** · **Change this profile's name** · **Change this profile's avatar** · **Delete this profile** · **Add a profile** · **Switch profile**, over "Enter the household PIN to change this profile." (switching: "Enter the household PIN to switch profiles."), the **Household PIN** field, **Continue** / **Cancel**, and "Incorrect PIN. Try again." A refusal keeps its own line: `parent_required` "Enter the household PIN to change this profile.", `owner_required` "Only the account owner can change household settings.", `account_session_required` "Manage this from a signed-in phone, computer or the web dashboard.", anything else "This action is not available for this profile."
- Manage profiles: **Edit profile** · **Change avatar** · **Name** · **Audio & subtitles** · **Maturity rating** · **Delete profile** (**Delete [name]?** with the Profile page's body) · local builds "A local PIN keeps profiles separate in the app. The device owner can access local files." · a preference this connection cannot change reads "This connection does not provide this profile preference yet."
- Parental controls: "The household PIN is required to leave a restricted profile or manage settings from it. Each profile has its own age limit." · a locked household reads "Enter the parent PIN to manage this household." with **Unlock parental controls** · **Profile restrictions** with one row per profile — **Kids profile · movies [rating] · series [rating]**, **Kids profile · movies [rating] · other titles up to age [age]** (and the series form), **Kids profile · up to age [age]**, **Kids profile · limits unavailable**, **Kids restrictions off**; **Leave PIN set** / **No leave PIN** / "Leave PIN status unavailable" — then **Edit restrictions**, **Change leave PIN** / **Set leave PIN**, **Approved and blocked titles**, **Household PIN in Account** · **Restrictions for [name]**: **Kids restrictions**, **Maximum age** ("Used for any kind without its own rating limit."), **Movies up to** / **Series up to**, **Allow titles with no rating**, **Save restrictions** / **Cancel** · "Set a parent PIN before enabling kids restrictions." · **Change parent PIN** / **Set parent PIN** / **Remove parent PIN?** — "The household PIN will be removed. Kids restrictions must be off for every profile.", **Current PIN**, **New PIN**, **Confirm new PIN**, "Use 4 to 8 digits. Keep your parent PIN private.", "PINs do not match.", "Use 4 to 8 digits.", "Turn off kids restrictions on all profiles before removing the PIN." · leave PIN: "Ask for this PIN before leaving [name]'s profile.", **Change [name]'s leave PIN** / **Set [name]'s leave PIN**, **Remove PIN**, "The current PIN for this profile was not accepted. Check it and try again."
- Approved and blocked titles: **Approved titles** · **Blocked titles** ("Blocked titles stay hidden for [name], even when they are approved.") · the search field and "No matching titles.", "These results are unavailable. Try searching again.", "No searchable integrations are available for this profile." · **Load more approvals** / **Load more blocked titles** · **Approve this title?** ("Allow [title] for [name]? The server checks the title before saving.") · **Remove this approval?** ("Remove [title] from [name]'s approved titles? The profile's age restrictions will apply again.") · **Unblock this title?** ("Show [title] to [name] again? This profile's age restrictions still apply.") · **Block this title?** ("Hide [title] from [name]? A block outranks an approval.") · empty "No titles have been approved for [name]." / "No titles are blocked for [name]." · "Title approved for [name].", "Approval removed. The profile's age restrictions apply again.", "[title] is blocked for [name].", "Adult titles cannot be approved."
- Add-ons: a configurable add-on's row carries **Reconfigure** next to **Remove** and **Reconfigure** opens its configure page in the browser; a server that will not hand out the link leaves "Couldn't get the configure link." on the page with **Try again**. The TV row's hold-OK panel is **Manage [Addon]**.
- Settings notes and refusals: **Watching as** · the profile card's account row reads "Connected to a server" or "Using this device locally" · TV sign-out "Your profiles and progress stay on your account." · "The primary profile cannot be deleted." · "Profile limit reached." A page that fails to load keeps the rows it has, one error line and a retry.
- Account page: **Name**, **Username** `@[username]`, **Role** **Owner** / **Member**. There is no email row.
- Household PIN: "Use a 4–8 digit PIN to protect leaving kids profiles. Turn off kids mode on all profiles before removing the PIN." A blocked removal reads "Turn off kids restrictions on all profiles before removing the PIN."
- Devices: "Everywhere [name]'s account is signed in. Signing a device out doesn't delete anything from the account." · a row reads **Now** or **Signed in [when]**, and **This device** for the one in use · empty "No other devices are signed in." · **Sign out of all devices**.
- Change password: **Current password** · **New password** · **Confirm new password** · **Change password** · **Cancel** · "Password changed. Other devices stay signed in." · "That password is not correct." · "Passwords do not match." · "Too many attempts. Wait a minute and try again." · "Could not change your password. Try again."
- Delete account: type the username to confirm ("Type [username] to confirm"), the account password, plus the household PIN when one is set. "The username or password is not correct." · "The parent PIN is not correct." · "Other accounts still need an owner. Have them delete their accounts first." · "Could not delete your account. Nothing was changed. Try again." Success signs out with "Your account was deleted."
- A TV cannot manage the account: those rows are disabled with "Manage this from a signed-in phone, computer or the web dashboard.", and **Devices & sessions** opens read-only with that line in place of its sign-out actions.

## Watch on TV (phone remote) — proposed for Android phone and tablet

The remote is proposed for the KMP app on Android phone and tablet
([AND-038](../docs/platforms/ANDROID_DESIGN.md#and-038--android-phone-and-tablet-vizio-remote-2026-11-02)),
superseding the earlier exclusion; no layout shows the **Watch on TV** row it
starts from until it ships (`components.md` §11). A TV signs in with
**Settings › Account › Add a device**.

- Settings row (Android phone and tablet): **Watch on TV** · "Use this phone as a Vizio TV remote" · value "Off" until a TV is paired, then the TV name.
- Intro: "Use this phone as your TV remote" / "Works with Vizio SmartCast TVs on the same Wi‑Fi as this phone. It's off until you set it up." Points: "Arrows, OK, Back, play and volume for your TV." · "Opens VIPTV on the TV in one tap." · "What's playing on this phone stays here. Nothing is sent to the TV." Note: "VIPTV searches your local network only to find your TV." Button: **Set up a TV**.
- Choose your TV: "Looking for Vizio TVs on your Wi‑Fi…" · "Don't see your TV?" / "Turn the TV on, then check it's on the same Wi‑Fi as this phone. It can take a few seconds to show up." · **Enter IP address**.
- Permission off: "VIPTV can't look for TVs" / "Local network access is off for VIPTV. Turn it on in your phone's settings, then come back here." · **Open phone settings** (Manual IP entry does not bypass a network permission denial).
- IP entry: "Enter your TV's IP address" / "Find it on the TV under Settings › Network." · **Connect** · **Cancel**.
- PIN: "Enter the PIN on your TV" / "[TV name] is showing a 4-digit PIN." · "Pairs as soon as all 4 digits are in." · **New PIN** · **Cancel**.
- Connected: "Connected to [TV name]" / "You can control it from this phone now." · Remote button: "Shows at the top of Home, Live and My List." · **Open the remote** · **Done**.
- One-time tip: "Your TV remote" / "It stays up here on Home, Live and My List. Turn it off in Settings › Watch on TV." · **Got it**.
- Remote: "Connected · [IP]" · "Not reachable" · **Open VIPTV on TV** · Buttons / Swipe · "Swipe to move · Tap for OK" · Back · Play · Pause · Volume. Offline: "Can't reach [TV name]" / "Turn the TV on and check it's on the same Wi‑Fi as this phone." · **Try again** · **Pair again**.
- Settings: Remote button ("At the top of Home, Live and My List") · Vibrate on press · Keep screen on ("While the remote is open") · Change TV ("Pair a different Vizio TV") · Forget this TV ("Turns off Watch on TV").
- Forget: "Forget [TV name]?" / "The remote button goes away. You can set up a TV again at any time." · **Forget TV** (danger) · **Cancel**.

## Copy decisions (2026-10-19)

- A guide/stream notice is **source-scoped**: "Guide data isn’t available for this
  source yet. You can still watch this channel." It never claims a per-channel
  failure and never renders above the category chips.
- Empty and failure are separate messages on every list: "Nothing matches these
  filters" (with Clear all) versus "Couldn’t load this catalog" (with Try again).
- A row that fails shows a titled card — "Couldn’t load this row" plus the
  provider's message plus "Try again" — never the provider text alone in a button.
- "Could not load" strings are never used for a title page; it is "This title
  couldn’t load" with a Go back action.
- Server-originated messages are mapped to human copy before display; a raw
  backend string ("API route not found") never reaches the UI.
