# DOWNLOADS-001 — Download episodes, seasons and series for offline playback

Status: **proposed**, owner request
([app#1185](https://github.com/viptv-org/app/issues/1185), storage limit and
expiry in [design#241](https://github.com/viptv-org/design/issues/241)).
Android phone and tablet first; desktop when `platformDownloads()` returns an
engine there. Web, iOS and TV show no download control, page or setting: a
platform without downloads leaves them absent, never disabled.

The shared contract is `downloads/Downloads.kt` in the app
(`DownloadState`, `DownloadItem`, `DownloadStorage`, `DownloadSettings`,
`Downloads`); the core PR owns it and this spec names its fields.

## Starting a download

| Where | Action | Downloads |
|---|---|---|
| Episode row (Details, every layout with downloads) | download control | that episode |
| Movie page, beside **Play** | **Download** | the movie |
| Series page actions | **Download season** | every released episode of the selected season |
| | **Download next 3** / **5** / **10** | that many released episodes from the next unwatched one |
| | **Download series** | every released episode |

A bulk action skips episodes already queued, downloading or downloaded. The
pressed control shows its new state in the same frame
([instant feedback](../../viptv-design-system/components.md#9-feedback)): the
row turns **Queued** before any network call.

## Source choice

A download uses the Best match ranking
([SRC-BEST-MATCH-001](source-best-match.md)) restricted to sources this device
plays **directly**; a source that needs the playback gateway is not
downloadable. Within that set: HTTP (debrid or direct) before torrent, nothing
above the quality cap, and the smaller file between equal ranks. A torrent is
used only when the device torrent runtime can write the whole file to storage.
The chosen release is remembered through source memory (binge group, source
fingerprint), so later episodes of the series take the same release.

The URL comes from playback admission with `"purpose":"download"`: no lease,
no Continue Watching or viewing side effects. An expired provider URL is
recovered by re-discovering the same release (fingerprint, then label and
size) and resuming with an HTTP `Range` request.

## States

`DownloadState`, as a row shows it:

| State | Control (episode row) | Downloads page line |
|---|---|---|
| none | download icon | — |
| `Queued` | ring, no fill | `Queued` |
| `Resolving` | spinning ring | `Finding a source` |
| `Downloading` | ring filled to progress | `[42]% · [1.1] of [2.6] GB` (`[1.1] GB` while the total is unknown) |
| `Paused` | ring at progress, pause glyph | `Paused · [42]%` |
| `WaitingForNetwork` | ring at progress, pause glyph | `Waiting for Wi‑Fi` (Wi‑Fi only on) or `Waiting for a connection` |
| `WaitingForSpace` | ring at progress, pause glyph | `Storage limit reached` |
| `Completed` | check | `[1080p] · [2.4] GB`, or `Watched · deletes in [23 h]` |
| `Failed` | alert icon | `Couldn't download` · the `failure` text |

A tap on the control:

- none or `Failed`: starts (or retries) the download.
- active (`Queued` to `WaitingForSpace`): a menu with **Pause** (or
  **Resume**) and **Cancel download**. Cancel removes the partial file.
- `Completed`: a menu with **Play**, **Delete download**, and **Keep** while an
  expiry is set (**Don't keep** while `keep` is on).

The Downloads page rows carry the same actions as buttons and menu items.

## Downloads page

Reached from a **Downloads** tab in the phone bottom bar after **My List**
(`Lucide.Download`), from the rail after **History** on tablet and desktop,
and from a **Downloads** entry at the top of **My List**. Title **Downloads**.

- Above the list a storage bar: used download bytes against the limit, with
  `[12.4] GB of [50] GB used · [31] GB free on this device` (`[12.4] GB used ·
  [31] GB free on this device` with **No limit**).
- Movies first, then series; each series groups its seasons, each season its
  episodes in order. A row: still or poster, `S1 E3 · [title]`, the state
  line, the control. A group header shows the series, its download count and
  total size, and **Delete** for the group.
- **Delete watched** in the header deletes every watched download at once and
  shows **Deleted [N] watched downloads**. It is absent when none is watched.
- Tapping a completed row plays the local file; any other row opens its menu.
- Empty: **No downloads yet** · `Download episodes from a title's page to
  watch them without a connection.` · **Browse** (to Home; absent offline).

## Offline

- `ApplicationState.offline` is true when the backend is unreachable. A
  banner at the top of every page reads `You're offline. Downloads still play.`
  with **Downloads**; it hides on the Downloads page.
- A start with no network at all opens straight to Downloads.
- A downloaded title plays its local file whether online or not; nothing
  calls admission. Subtitles and audio come from the file.
- Watch progress made offline is queued on the device and sent when the app
  is back online, in order, so Continue Watching is right afterwards.

## Smart downloads

Setting **Smart downloads**: Off (default), 1, 3, 5. With N on, for a series
the profile is watching, finishing an episode queues the next N released
episodes that are not downloaded and starts the watched-downloads expiry of
the finished one. The next unwatched downloaded episode of such a series is
protected from eviction.

## Storage limit

Setting **Storage limit**: 10 GB, 25 GB, 50 GB (default), 100 GB, **No
limit**; never more than the device's capacity minus 2 GB, so options above it
are absent. Before a download starts and while it grows, the engine keeps the
total download bytes under the limit by deleting completed downloads in this
order:

1. watched episodes, oldest `watchedAtMillis` first;
2. other completed downloads, oldest `lastPlayedAtMillis` first (never played
   counts by `addedAtMillis`, as older than any played one).

Never deleted to make space: a queued or downloading item, the item playing
now, and the protected smart-downloads episode. When nothing can be deleted
the new item stays in `WaitingForSpace` and starts by itself once space
frees (a deletion, a raised limit). The page shows above the list
**Storage limit reached** · `Raise the limit or delete downloads to continue.`
with **Raise limit** (opens the limit setting) and **Manage** (scrolls to the
largest group).

Every eviction is shown once, as a notice on the Downloads page the next time
it opens (or at once if open): **Removed [N] old downloads to make space**
(**Removed 1 old download to make space**). The removed rows are gone.

## Watched downloads expire

Setting **Delete watched downloads**: **Right after watching**, **After 1
hour**, **After 1 day** (default), **After 1 week**, **Never**. An episode is
watched (`watchedAtMillis`) when playback reaches 95 % or its credits; its
expiry (`expiresAtMillis`) counts from when the player is left. The row reads
`Watched · deletes in [23 h]` (`[45 min]`, `[6 d]`; **Right after watching**
deletes on leaving the player and shows no line). **Keep** cancels that
item's expiry and the line reads `Watched · kept`; **Don't keep** restarts it
from now. A movie follows the same rule.

## Settings › Downloads

Under **This device** ([ACCT-SPLIT-001](account-and-profile-settings.md)),
saved on the device. A change applies at once.

| Row | Description | Values | Default |
|---|---|---|---|
| `Download on Wi‑Fi only` | `Waits for Wi‑Fi before downloading.` | switch | on |
| `Download quality` | `Highest quality to download.` | `Best`, `1080p`, `720p`, `480p` | `1080p` |
| `Storage limit` | `Old downloads are deleted to stay under it.` | `10 GB`, `25 GB`, `50 GB`, `100 GB`, `No limit` | `50 GB` |
| `Delete watched downloads` | — | as above | `After 1 day` |
| `Smart downloads` | `Keeps the next episodes of a series you're watching downloaded.` | `Off`, `1`, `3`, `5` | `Off` |

Below the rows: `[12.4] GB used by downloads · [31] GB free`.

## Failure

| Cause | `failure` text |
|---|---|
| No directly playable source | `No downloadable source found.` |
| Source failed and re-discovery found no match | `The source stopped working.` |
| Device storage full (not the limit) | `Not enough space on this device.` |
| Anything else | `Something went wrong.` |

A failed row offers **Try again** and **Remove**.

## Acceptance

1. Tapping an episode's download control shows **Queued** in that frame; it
   moves through Finding a source and a filling ring to a check.
2. **Download next 3** from S1 E4 unwatched queues E4–E6 and skips any already
   downloaded.
3. With Wi‑Fi only on and mobile data, a queued item reads `Waiting for
   Wi‑Fi` and starts when Wi‑Fi returns.
4. In airplane mode the app opens on Downloads; a completed episode plays;
   its progress reaches Continue Watching after the network returns.
5. With a 10 GB limit and 9 GB used, a 2 GB download deletes a watched episode
   first, then the least recently played completed one, and the page shows
   **Removed 1 old download to make space**.
6. When everything stored is downloading, playing or protected, the new item
   reads `Storage limit reached` with **Raise limit** and **Manage**, and
   starts by itself after **Raise limit** to 25 GB.
7. With **After 1 day**, an episode finished and left reads `Watched · deletes
   in 23 h` an hour later and is gone a day later; **Keep** stops that.
8. With Smart downloads 3, finishing E2 queues the next three released
   episodes not yet downloaded.
9. Web, iOS and TV show no download control, page, tab or setting.
