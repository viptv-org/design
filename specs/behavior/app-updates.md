# AND-APP-UPDATE-001 — Android in-app updates from GitHub Releases

Status: **proposed**, owner requested 2026-10-11. Android (phones, Android TV,
Fire TV) adopts it first. Release packaging, versioning and `update.json` are
owned by the Android repository (`VERSIONING.md`). Other clients are out of
scope; Roku, TV-web and desktop keep their own delivery.

## Intent

Sideloaded Android installs learn about a newer beta release and install it
from inside the app, without a store, a computer or ADB. There is one channel:
the latest GitHub release. The backend is not versioned; release notes ask
people to update their server to its latest version.

## Availability

- Only release builds (built from a version tag) check for updates.
  Development builds show the version only and never offer an update.
- An update is **available** when the latest release has a higher version code
  than the installed app and supports the device's Android version. A release
  that needs a newer Android version is never offered.
- The app downloads only the release's own APK and installs it only when its
  size and checksum match the release's `update.json`.

## When the app checks

1. **On launch:** after the first signed-in screen is shown, at most once every
   6 hours. The check runs quietly; no spinner, no error if it fails.
2. **On demand:** from **Settings › About VIPTV › Check for updates**, any time.

A check never runs, prompts or installs while the player is open. A launch
prompt that becomes due while the player is open waits until the viewer leaves
the player.

## Launch prompt

When a launch check finds an available version the viewer has not dismissed,
show the dialog:

- Title **`Update available`**
- Description **`VIPTV {version} is ready to install. Update your VIPTV server to its latest version too.`**
- Buttons **`Update now`** (focused first on TV) · **`Later`**

`Later` and Back close it and remember that version: the launch prompt does not
appear again for it. A newer release prompts again. Settings always shows an
available version.

## Settings

The **About VIPTV** row shows:

| State | Row detail |
|---|---|
| Development build | `Version {version}` |
| Up to date or unknown | `Version {version}` |
| Update available | `Version {version} · Update available` |

Choosing the row opens the **About VIPTV** dialog with the description
`VIPTV {version}` + blank line + `Your shows, channels and progress. All in one place.`
followed by one status line, and these buttons:

| State | Status line | Buttons |
|---|---|---|
| Development build | `Updates are off for development builds.` | `Close` |
| Not checked / up to date | `You're up to date.` (after a check) or none | `Check for updates` · `Close` |
| Checking | `Checking for updates…` | `Check for updates` (no effect while checking) · `Close` |
| Available | `VIPTV {new} is available.` | `Update now` · `Close` |
| Check failed | `Couldn't check for updates. Check your connection and try again.` | `Check for updates` · `Close` |

The first button keeps its position while the status changes, so TV focus
stays on it (`Check for updates` becomes `Update now` when a release is
found). On TV the first button takes focus when the dialog opens. Back closes
the dialog and returns focus to the About VIPTV row.

## Update flow

`Update now` (from the prompt or Settings) runs these steps:

1. **Permission.** If Android requires the viewer to allow VIPTV to install
   apps, the **Updating screen** ([below](#updating-screen)) carries the
   permission step: title **`Allow updates`**, description
   `Allow VIPTV to install apps in the screen that opens, then come back to
   finish the update.`, platform line
   `The update continues by itself when you come back.` and buttons
   **`Open settings`** · **`Later`**. `Open settings` opens the system setting
   for VIPTV. When the viewer returns with permission granted, the install
   continues by itself. Returning without it shows the same step again.
   - When the device has no such setting screen (some Fire TV models), the
     description instead reads
     `On Fire TV, open Settings › My Fire TV › Developer options › Install
     unknown apps, turn on VIPTV, then come back.`
     with buttons **`Try again`** · **`Later`**.
2. **Download.** Dialog **`Downloading update`**, description
   `VIPTV {new} · {percent}%`, button **`Cancel`**. Cancel or Back stops the
   download and discards it. A download already verified for that version is
   reused, so this step is skipped.
3. **Install.** The **Updating screen** covers the app while the APK goes into
   Android's installer session, and stays up behind Android's confirmation and
   the replacement of the process ([below](#updating-screen)). Where the
   platform can reopen VIPTV it does so at once on a fresh task, still signed
   in with settings and progress kept, and confirms `Updated to {version}`;
   where it cannot, the screen says to open the app again.
4. **Failure.** **`Couldn't update VIPTV`** with one description and
   **`Try again`**, plus the dialog's own dismiss action (`Close` in the About
   dialog, `Later` on the update prompt):
   - network or server error: `Check your connection and try again.`
   - checksum or size mismatch: `The download was incomplete or damaged. Try again.`
   - the viewer cancelled the system confirmation: no dialog; the Updating
     screen goes away and that version is not offered again this session.
   - installation rejected by Android: the Updating screen goes away and the
     prompt returns as **`Couldn't update VIPTV`** with
     `Android didn't install the update.` and buttons **`Try again`** ·
     **`Later`**.

## Updating screen

Status: **proposed**; recorded 2026-10-28 from the implementation in
viptv-org/app at `81cf5ae` (PR [app#145](https://github.com/viptv-org/app/pull/145),
issue app#139). Code: `updates/AppUpdatingScreen.kt`, `updates/AppUpdater.kt`,
`updates/UpdatePolicy.kt` (`showUpdatingScreen`, `backIgnoredWhileUpdating`),
`androidMain/updates/UpdateRelaunchReceiver.kt` and
`androidMain/updates/AndroidAppUpdatePlatform.kt`. App renders in
`docs/evidence/2026-10-28-app-updating-screen/` (phone 390 × 844, TV
1920 × 1080) were inspected privately and are not committed here. **No canvas
board exists yet** (app `docs/DESIGN_GAPS.md` GAP-065), so the copy below is
normative and the geometry is the provisional implementation, unmeasured
against a board.

### User intent

Choosing **Install** used to leave the previous page on screen with no feedback
until the app disappeared. One full-screen cover now owns the app from that
press until Android has replaced the process: it says what is happening, how
far the write got and what happens next.

### Entry and exit

- **Entry:** the viewer chooses **Install** on the update prompt (phone bottom
  banner, TV corner card) or the Settings update action, with a verified build
  ready. The prompt is hidden from that moment and never sits on top of the
  screen.
- **Exit into the update:** Android installs and replaces the process. Where
  the platform can reopen the app it does so at once (`MY_PACKAGE_REPLACED`) on
  the new build, clearing the old task so the app opens on its start screen
  rather than a stale page, and the new build confirms **`Updated to
  {version}`**.
- **Exit back to the app:** an install Android rejects, a cancel in Android's
  confirmation, or **`Later`** on the permission step. The first goes back to
  the prompt's failure form; the other two go back to the page the viewer was
  on, and that version is not offered again this session (**Later**).
- The screen is never shown over the player or the sign-in screens: the prompt
  is not shown there, so Install cannot be chosen from them.

### Copy by state

| State | Title | Body | Progress | Line under the bar | Actions |
|---|---|---|---|---|---|
| The APK is written into Android's installer session | **`Updating VIPTV to {version}…`** | `Writing the update. Android asks you to confirm before it installs.` | Determinate bar and **`{N}%`** | `VIPTV restarts by itself when the update is installed.` | none |
| The session is committed and Android shows its confirmation, or is already replacing the process | **`Updating VIPTV to {version}…`** | `Confirm the update in the dialog Android is showing.` | Indeterminate bar, no percent | same restart line | none |
| Android needs "Install unknown apps" | **`Allow updates`** | `Allow VIPTV to install apps in the screen that opens, then come back to finish the update.` | none | `The update continues by itself when you come back.` | **`Open settings`** · **`Later`** |
| The same permission step where the device has no such setting screen (some Fire TV models) | **`Allow updates`** | `On Fire TV, open Settings › My Fire TV › Developer options › Install unknown apps, turn on VIPTV, then come back.` | none | same line | **`Try again`** · **`Later`** |

- `{version}` is the offered build's `versionName`, for example
  `0.1.1301+7a2c1b9`; the title uses the single-character ellipsis `…`.
- Where the platform cannot reopen the app after replacing it, the line under
  the bar reads `VIPTV closes when the update is installed. Open it again to
  finish.` instead of the restart line. Android can reopen it, so Android TV,
  Fire TV, phones and tablets show the restart line.
- Neither the writing nor the confirming state offers an action: the system
  installer owns the decision at that point.
- The layout has no other text: no step counter, no download speed, no
  remaining time, no cancel action. There is no empty or disabled state: the
  screen is either writing, confirming, or asking for the permission.

### Progress

The bar counts what has been written into Android's `PackageInstaller` session
(the copy of the already-verified APK, in 64 KiB chunks), not the feed download
that finished before the prompt appeared.

- The percent is the rounded-down fraction of the APK's size, so it starts at
  `0%`, moves in chunk-sized jumps and reaches `100%` as the write ends.
- As soon as the session is committed the percent disappears and the bar
  becomes indeterminate, because Android's confirmation and the process
  replacement are no longer measurable.
- A feed with no usable size (`size` 0) shows the indeterminate bar from the
  start and never shows a percent.
- The permission step shows no bar at all.

### Layout

Provisional implementation values in dp, text sizes in sp, to be replaced by
the board:

| | Phone and tablet | TV |
|---|---|---|
| Cover | full screen, opaque `color.bg`; safe-area insets; 32 padding | full screen, opaque `color.bg`; no inset change |
| Column | max 420 wide, centred horizontally and vertically, 16 gaps | 120 × scale side inset, centred vertically (`scale` = width ÷ 1920) |
| V mark | 56 | 120 × scale |
| Title | `headlineSmall`, `color.text.primary`, centred | 56 × scale bold, 68 × scale line height, centred |
| Body | `bodyLarge`, `color.text.secondary`, centred | 28 × scale, 40 × scale line height, centred |
| Percent | 13 sp, 8 above the bar, `color.text.body` | 24 × scale above the bar |
| Bar | column width × 6, `color.accent.default` on `color.surface.2`, rounded | 760 × scale wide, 8 × scale tall |
| Line under the bar | `bodySmall`, `color.text.tertiary`, centred | 24 × scale, 34 × scale line height, centred |
| Actions (permission step) | **`Later`** (`color.text.secondary`) then the primary (`color.accent.default`, semibold), 8 apart, centred, no container | 48 × scale below the line: primary 320 × 80 × scale, **`Later`** 200 × 80 × scale, 16 × scale apart |

The colours above are the design-system roles the implementation draws from
(`color.bg`, the surface, text and accent roles; the raised surfaces are
`Palette.raised` = `color.surface.2`). The Material type styles it names
(`headlineSmall`, `bodyLarge`, `bodySmall`, `bodyMedium`) and the dp gaps still
need mapping onto the design-system type ramp and spacing on the board.

**After the update:** **`Updated to {version}`** is a bar at the bottom centre
(16 from the edges, radius 12, `color.surface.2`, 20 × 12 padding, semibold
`bodyMedium`). It has no action, never blocks the page, and the TV layout keeps
the same density-pixel sizes instead of scaling them — a board has to set the
TV size.

### Focus and inputs

- **Phone and tablet:** the cover takes every touch; nothing behind it reacts,
  and there is no tap-outside or swipe to dismiss.
- **TV:** the screen itself takes focus while it offers nothing to choose, so a
  D-pad press cannot reach the page behind it. On the permission step the
  primary action (**`Open settings`**, or **`Try again`** on Fire TV) takes
  focus **700 ms** after the screen appears, so the OK press that chose Install
  cannot also open the system screen; **`Later`** is one step away.
- **Back:** while the APK is being written and once the session is committed,
  Back does nothing — Android cannot cancel the install at that point. On the
  permission step **`Later`** leaves the screen, and Back should do the same;
  the shipped app leaves Back to the page behind the cover instead, so Back
  currently changes the hidden page or leaves the app
  ([app#146](https://github.com/viptv-org/app/issues/146)). This contract is not
  met by the current build.
- No long-press, repeat or hold does anything on this screen.

### Failure and recovery

| Cause | What the viewer sees |
|---|---|
| Android rejects the install (`Failed` after an install attempt) | The screen goes away; the prompt returns with **`Couldn't update VIPTV`**, `Android didn't install the update.`, **`Try again`** · **`Later`**. **`Try again`** starts a fresh session and shows the Updating screen again. |
| The verified file changed on disk before the write | The screen goes away; the prompt returns with **`Couldn't update VIPTV`**, `The download was damaged. VIPTV will try again later.`, **`Try again`** · **`Later`**. |
| The viewer cancels Android's confirmation | The screen goes away, the page returns and no prompt is shown for that version this session. |
| The viewer leaves the app (Home) during the confirmation | Nothing is drawn on return: the app comes back with the update ready and the prompt's **`Install`** again, and a new press starts a fresh session, because Android never gave that session an answer. |
| The viewer chooses **`Later`** on the permission step | The screen goes away and that version is not offered again this session. |

### Timing

| Event | Timing |
|---|---|
| Screen appears | at once on the Install press, before the first chunk is written |
| Percent and bar | one update per 64 KiB chunk written into the session |
| Bar becomes indeterminate | when the session is committed, before Android's confirmation appears |
| TV permission-step focus | 700 ms after the screen appears |
| **`Updated to {version}`** | shown after the relaunch for 6 s, then removed; a second announcement restarts the 6 s |

### Accessibility

- The bar is one progress indicator with platform progress semantics (the
  implementation exposes a `ProgressBarRangeInfo`) and the percent is a text
  label above it, so assistive technology reads the value in words.
- The permission-step actions are ordinary buttons: on phone and tablet in
  reading order **`Later`** then the primary action, on TV the primary action
  first and focused. Touch targets follow the button rules and the TV actions
  keep the standard focus treatment.
- Unknown: whether the screen appearing or the percent changing is announced as
  a live region, and whether a reduced-motion variant of the indeterminate bar
  exists. No board, no measurement and no screen-reader run exist yet.

### Platform scope

Android only (phones, tablets, Android TV, Fire TV), as part of
AND-APP-UPDATE-001. Roku, the desktop app, the browser and TV-web never show
it: they do not install themselves.

## Acceptance

1. **AND-APP-UPDATE-01:** a development build shows `Version 0.1.0` and
   `Updates are off for development builds.`, and never prompts.
2. **AND-APP-UPDATE-02:** a release build older than the latest release shows
   the launch prompt once after sign-in; `Later` suppresses it for that version
   across restarts; Settings still shows `· Update available`.
3. **AND-APP-UPDATE-03:** `Update now` without install permission shows
   `Allow updates` on the Updating screen; granting it in system settings and
   returning continues the install by itself; the updated app opens signed in.
4. **AND-APP-UPDATE-04:** the launch prompt never appears and no check runs
   while the player is open; it appears after leaving the player if due.
5. **AND-APP-UPDATE-05:** `Check for updates` on the latest release shows
   `You're up to date.`; with no network it shows the check-failed line.
6. **AND-APP-UPDATE-06:** a damaged download shows the checksum message and
   nothing is installed; cancelling the download leaves no file behind.
7. **AND-APP-UPDATE-07:** every dialog is reachable and dismissable with a TV
   remote (D-pad, OK, Back) on Android TV and Fire TV.
8. **AND-APP-UPDATE-08:** choosing `Install` on a 390-wide phone covers the page
   with the Updating screen: `Updating VIPTV to 0.1.1301…`,
   `Writing the update. Android asks you to confirm before it installs.`, a
   determinate bar with `{N}%` and
   `VIPTV restarts by itself when the update is installed.` The `Update ready`
   prompt is gone, and a tap where the page's controls were does nothing.
9. **AND-APP-UPDATE-09:** the same press on 1920-wide Android TV covers the page
   with the same screen; D-pad presses move nothing, and Back does nothing while
   the APK is written and after the session is committed.
10. **AND-APP-UPDATE-10:** without the install permission, `Install` shows
    `Allow updates` with
    `Allow VIPTV to install apps in the screen that opens, then come back to finish the update.`,
    `The update continues by itself when you come back.` and `Open settings` ·
    `Later`; on a Fire TV without that screen it shows the Fire TV path with
    `Try again` · `Later`. Returning with permission allowed continues the
    install without another press; returning without it shows the same step;
    `Later` leaves the screen and does not offer that version again this session.
11. **AND-APP-UPDATE-11:** an install Android rejects leaves the screen and the
    prompt returns with `Couldn't update VIPTV`,
    `Android didn't install the update.`, `Try again` · `Later`; `Try again`
    shows the Updating screen again and `Later` returns to the page.
12. **AND-APP-UPDATE-12:** cancelling Android's confirmation leaves the screen,
    returns the page the viewer was on, installs nothing and shows no prompt for
    that version until the app restarts.
13. **AND-APP-UPDATE-13:** when Android installs the update and reopens VIPTV,
    the app opens on its start screen, still signed in with settings and
    progress kept, and `Updated to {version}` sits at the bottom for six seconds
    and then goes away on its own.
