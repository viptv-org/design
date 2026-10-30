# ACCT-SPLIT-001 — Account, profile and device settings

Status: **proposed**, owner report 2026-10-30
([design#40](https://github.com/viptv-org/design/issues/40)). Nothing here is
built yet: the KMP app and the web dashboard both still mix account, profile and
device settings in one list.

Source revisions: the KMP app's Settings at app `d2db87f`
(`features/settings/`, `state/SettingsPage.kt`, `state/SettingsRoute.kt`) and the
archived dashboard at web `d2d5b27` (`src/AccountApp.tsx`, `src/AdminShell.tsx`,
`src/AccountScreens.tsx`, `src/ParentalControls.tsx`). Backend routes are cited
from `server/src/routes.rs`, `server/src/auth/middleware.rs` and
`server/src/kids/` in viptv-org/backend.

Reference boards exist for the parts, not for the split: `M3Settings`,
`T3Settings`, `D3SetGeneral`, `W3Account`, `W3Recovery`, `M3Recovery`,
`D3Recovery`, `W3Parental`, `M3Parental`, `M3ProfileEdit`, `Tv3ProfileEdit`,
`Tv3SetAbout`, `Tv3SetParental`, `Tv3SignOut`, `SkSettings` and `SkSettingsOff`
in `viptv-design-system/reference/screens/`. Where a board and this contract
disagree, this contract wins for the group order and the row lists; the boards
win for geometry and type.

## Intent

Settings is one door with four rooms. A viewer changes the thing they are
looking at: the person watching (Profile), how it plays (Playback), the machine
in their hand (This device), or the household they signed in to (Account). An
account-level action is never mixed into a profile page, and a profile action is
never shown as if it changed the whole household.

The current app gets this wrong in three ways: phone shows one flat list with
Playback, Add-ons, Account, Devices, Parental controls, Help and About as
siblings; desktop and web put Playback and Subtitles inside a sidebar headed
**Account**; TV has one flat rail with **Account** and **Profiles** next to each
other, so "Account" reads as "my profile". The dashboard (`AdminShell`) already
groups its nav as *Your profile*, *Your account* and *Operator*.

## Who owns what

Every row below is one setting or one action, with its real owner. "Account" and
"Profile" are the terms in [CONTEXT.md](../../CONTEXT.md).

| Setting or action | Owner | Backend today |
|---|---|---|
| Display name, `@username`, role | Account | `GET /auth/me`; no edit route |
| Password | Account | none — `POST /auth/recover` only, which needs a recovery code |
| Recovery codes | Account | issued once at register/recover; no list or regenerate route |
| Household PIN | Account | `GET /parent/status`, `POST /parent/unlock`, `PUT /parent/pin` |
| Add-ons (inventory) | Account | `GET/POST /addons`, `PATCH/DELETE /addons/:id` |
| Add-on on/off for a profile | Profile | `GET/PUT /profiles/:id/addon-activation`, `GET/PUT /profiles/:id/integrations` |
| Source integrations (VIPTV Sources, Xtream, M3U, IPTV connections) | Account | `GET/PUT /profiles/:id/source-integrations`, `GET/POST/PATCH/DELETE /iptv/connections` |
| Devices and sessions | Account | `GET /account/devices`, `DELETE /account/devices`, `DELETE /account/devices/:id`, `DELETE /auth/sessions` |
| Add a device (pairing code approval) | Account | `POST /auth/device/lookup|approve|deny` |
| Delete account | Account | none |
| Profile name and avatar | Profile | `PATCH /profiles/:id`, `DELETE /profiles/:id` |
| Kids flag and age limit | Profile | `GET/PUT /profiles/:id/kids` |
| Approved and blocked titles | Profile | `GET/POST /profiles/:id/approvals`, `GET /parent/search` |
| Profile lock (local builds) | Device + profile | local store only |
| Language: default audio and subtitles | Profile | `GET/PUT /profiles/:id/preferences` |
| Source selection, quality, HDR, subtitle mode, size and colour | Profile | `GET/PUT /profiles/:id/preferences` |
| Linked services (Simkl) | Profile | `GET/DELETE /profiles/:id/simkl`, `POST /profiles/:id/simkl/authorize` |
| Import from Stremio | Profile | `POST /profiles/:id/imports/stremio/preview|…/review|…/apply` |
| Autoplay next episode | Device | app-local; `PLAY-NEXT-AUTOPLAY-001` |
| Display (accent, text size, reduce motion, screen saver, fit) | Device | TV local store |
| Watch on TV (pairing and remote) | Device | local store |
| App updates, diagnostics, licences | Device | GitHub releases |

There is **no sign-in email** anywhere: an account is a `username`, a display
`name` and a password, and nothing sends mail. The identity page shows the
display name and `@username`, never an email row.

Simkl is profile-scoped because it tracks one person's viewing; it lives under
Profile. No account-wide link exists, so the Account group has no **Linked
services** row until one does.

## The four groups

The same four groups, in this order, on every platform. A row appears only
where the platform implements it.

| Group | Rows |
|---|---|
| **Profile** | Profile · Linked services · Parental controls · Import from Stremio |
| **Playback** | Playback · Subtitles & audio |
| **This device** | Display (TV) · Watch on TV (phone, tablet) · Notifications (only where implemented) · About · Help |
| **Account** | Account · Password · Household PIN · Devices & sessions · Add a device · Add-ons · Source integrations · Sign out · Delete account |

- **Profile** opens the page in [Profile](#profile): the current profile's name,
  avatar, kids flag, maturity limit, approved titles, lock, language, linked
  services and delete. The shell's profile card above the groups carries the
  switcher, so only TV needs a separate **Switch profile** entry (in its rail).
- **Parental controls** is the existing per-profile limits page (every profile's
  kids flag, age limit, approved and blocked titles). The household PIN that
  gates it is an account value and sits under Account. app#255 makes every one
  of those controls adjustable in the app.
- **Playback** and **Subtitles & audio** stay one page each, per profile, as
  `PLAY-NEXT-AUTOPLAY-001` and `PLAY-SUBTITLE-MODE-001` define them. **Autoplay
  next episode** keeps its note **"Plays the next episode after a 10-second
  countdown. Applies to this device."**
- **This device** holds what changes this machine only. **Display** exists on TV.
  **Watch on TV** exists on phone and tablet. **Notifications** appears only once
  it has a real page (app#243); until then no layout shows the row, because a row
  that opens "not available on this connection yet" is not a setting.
- **Account** holds the household's own state, and it is visible to everyone
  signed in: signing out and approving a device must stay reachable from a
  member's TV and phone. See [Account](#account) for the rows a device session
  cannot use.

Local mode (no server) keeps the same shell. Profile and Playback rows that need
a server are absent rather than disabled, This device keeps its rows, and Account
holds **Sign out** only, whose row reads **Change connection** in local mode.

## Settings shell per platform

### Phone (390 × 844)

`M3Settings` geometry, unchanged: header 102 high over a 0.78 ground with a 48
row inside it (44 back button, 17/700 centred title), content padding 110 / 16 /
120, groups 18 apart, group card radius 14 on a 0.06 white fill with rows
8 / 16 padded and a hairline between them, row label 15/600, note 13/500 in
`text-secondary`, value 14/400 in `text-secondary`, chevron in `text-tertiary`,
44 minimum target.

- The profile card stays at the top, above the first group: 56 avatar, name
  18/700, **Switch profile** 14/500, chevron.
- **Group label:** 11/700, +0.08em, uppercase, `text.tertiary`, 8 above its card
  and 2 below the previous card. No board draws group labels on phone; the type
  role is the eyebrow from `tokens.json` and the spacing follows the 18 group
  gap it sits inside.
- Sub-pages replace the list (pushed page with a 48 back row), never a dialog,
  except the dialogs named in [Inputs](#inputs).
- **Sign out** is the last row of the Account group, danger text, and opens the
  existing confirmation.

### Tablet (1194 × 834)

`T3Settings` two-pane: 360 rail with 40 / 16 padding, rows 10 / 12 padded at
radius 14 with a 44 avatar in the profile card, section rows
8 / 16 at radius 12, 15/600 labels, the current row on a 0.10 white fill; detail
pane from x 360 with 40 padding, page title 26/700, group card radius 16 on a
0.05 white fill with 6 padding and 8 / 16 rows, note 13/500, value 14/400, toggle
45 × 26.

- Rail group labels: 11/700 uppercase, `text.tertiary`, 12/16 padding, 12 above
  the group's first row and 16 below its last.
- The rail keeps the profile card above the groups and the groups scroll under
  it; the detail pane scrolls on its own.

### Desktop app (1440 × 900)

`D3SetGeneral` two-pane: 260 rail with 28 / 16 padding, rows 8 / 12 at radius 8,
14/600 labels, the current row on a 0.10 white fill; content from x 260 with
28 / 48 padding, page title 24/700, group cards radius 12 on a 0.05 white fill
with 4 padding and 8 / 16 rows at radius 12, label 15/600, note 13/500, value
14/400, toggle 45 × 26, inline action 32 high at radius 10 with a 0.14 inset
ring.

- Rail group labels: 12/700, +0.06em, uppercase, `text.tertiary`, 8/12 padding.
- The desktop app is pointer-only (`DESK-PLAYBACK-2026-10-03`): no keyboard
  focus ring, no Tab order, no arrow navigation. Group labels are headings for
  assistive technology and nothing more.

### Web (1280 × 800, 1440 × 900)

`W3Account`: `main` on a 100 / 57 / 40 grid with 48 gap and columns
`240px minmax(0, 760px)`; nav title 26/700 with 0 / 12 / 14 padding; nav rows
min-height 40, 8 / 16 padded at radius 8, 14/600, current row on a 0.10 white
fill; content page title 24/700, lead line 14/400 `text-secondary`, group card on
a 0.05 white fill with 14 / 16 rows, an icon tile 40 at radius 10 on a 0.08
white fill, label 15/600, note 13/500, inline action 32 high at radius 10 with a
0.14 inset ring and 13/700, destructive action 240 × 40 at radius 12 on a
`rgba(229,72,77,0.14)` fill in `#FF8A80`.

- Nav group labels: 12/700 uppercase, `text.tertiary`, 12/16 padding.
- A window narrower than 640 uses the phone layout instead.

### TV (1920 × 1080)

`Tv3SetAbout` / `Tv3SignOut` geometry, unchanged: 560 sidebar on `surface-1`
with the **Settings** title at 96 / 96 (44/700), rows 440 × 72 at x 72 from
y 196, 24 side padding, radius 12, icon 28 and 18 gap, 26/500 label and 26/700
when current; content column at x 640, 1184 wide, page title 40/700, rows
1184 × 96 at radius 14 with 28 side padding, label 26/600, note 20/500, value
24/500, 8 gap between rows; a destructive row is 80 high with `#FF8A80` text.

- The rail gains **Profile** and its **Profiles** entry is renamed **Switch
  profile**, so the page and the switcher are not confusable. **Profile** opens
  the page in [Profile](#profile).
- Rail group labels sit in the expanded 520 labelled menu
  (`components.md` §7): 18/700, +0.08em, uppercase, `text.tertiary`,
  24 × scale above a group's first row and 8 × scale below its last. They are
  not focus stops.
- `Tv3SetParental` keeps its title **Parental controls** and moves under Profile:
  it lists every profile's limits with the profile pills at the top. The
  household PIN's last row (**PIN to leave [name]'s profile**) opens the PIN
  dialog from there, so TV needs no separate Household PIN page.

## Profile

One page, the current profile, title **Profile** (phone, tablet, desktop, web)
and the same rows on TV. Every row edits the profile that is selected; the
profile switcher at the top of the shell changes which one.

| Row | Value | Note | Opens |
|---|---|---|---|
| Name | `[name]` | — | Text entry (dialog on TV and desktop, sheet on phone) |
| Avatar | — (thumbnail at left) | — | The avatar picker: worlds as chips, a grid page at a time (15 on phone, 18 on tablet, desktop and TV), Previous / Next, **"[468] avatars. Pick a world, then pick your character."** |
| Kids profile | On / Off | **"Limits titles, search and Live for this profile."** | A toggle. Turning it on asks for the household PIN when none is set for the session |
| Maturity limit | **All ratings** or the chosen rating | **"Titles above this rating are hidden for this profile"** | Choice list: `G` `PG` `PG-13` `R` `NC-17` for movies and `TV-Y` `TV-Y7` `TV-G` `TV-PG` `TV-14` `TV-MA` for series, as `Tv3SetParental` draws them |
| Approved titles | `[N]` | **"Only these titles show in the kids library"** | The approved-titles page (`/parent/search` plus the profile's approvals). Shown only while Kids profile is on |
| Profile lock | On / Off | **"Ask for a PIN before this profile opens"** | Local builds: set, change or remove a 4–8 digit local PIN. Server accounts: the row opens Parental controls, because the household PIN is what locks a kids profile |
| Language | **"[Audio language] · [Subtitle language]"**, or **"Original language"** when unset | **"Default audio and subtitles for this profile"** | Playback › Subtitles & audio, which owns the one editor for these values |
| Delete profile | — | Danger row | **Delete [name]?** · **"This permanently removes this profile's watch history, favorites and preferences."** · Cancel · Delete profile (danger) |

- **Kids flag, maturity limit and approved titles are the same values** the
  Parental controls page edits. Whichever page saves, both show the new value.
- **Delete profile** is absent when it is the account's only profile, and when
  the server reports the profile as primary (`canDelete` false).
- **Language** is a summary, not a second editor: it opens the page that already
  holds the preferred audio and subtitle languages, so the two can never
  disagree. Menus are English only; no row offers a menu language.
- After a successful save the page stays put and shows the new value. A failed
  save keeps the typed value in the field and shows the error line; the row's
  stored value does not change.
- Back from Profile returns to the row that opened it on every layout, and on TV
  the remote returns to the **Profile** rail row.

## Account

Title **Account**. Rows, in order, each its own page or dialog:

1. **Account** — the identity page: **Name** `[display name]`, **Username**
   `@[username]`, **Role** `Owner` or `Member`. Read-only, because no route edits
   them. The name is set when the account is created.
2. **Password** — the page in [Change password](#change-password-proposed).
3. **Household PIN** — set, change or remove the household PIN: **"Use a 4–8
   digit PIN to protect leaving kids profiles. Turn off kids mode on all profiles
   before removing the PIN."** Removing it is disabled while any profile has kids
   mode on, with **"Turn off kids restrictions on all profiles before removing
   the PIN."**
4. **Devices & sessions** — the page in [Devices and sessions](#devices-and-sessions).
5. **Add a device** — the existing code-entry page (**Add a device**, **"Open
   VIPTV on the other device, choose Sign in, then enter the code it shows."**,
   8-character code, Continue → confirm → done/denied).
6. **Add-ons** — the existing inventory page. Add-ons belong to the account; the
   switch on a row enables one for the current profile and the page says so.
7. **Source integrations** — VIPTV Sources, Xtream and M3U connections.
8. **Sign out** — danger, last but one, with the existing confirmation
   (**Sign out of this device?** / TV **Sign out of this TV?**).
9. **Delete account** — danger, last, the page in
   [Delete account](#delete-account-proposed).

A TV device session cannot manage the account: the server answers
`account_session_required` for anything but reading. On TV, **Password**,
**Household PIN**, **Delete account** and the sign-out buttons inside Devices &
sessions are shown disabled with **"Manage this from a signed-in phone, computer
or the web dashboard."** The rest of the group stays usable, because a TV must be
able to sign out and read its devices.

Operator surfaces (service health, providers, gateway grants, accounts) stay in
the web dashboard and are not rows in the app. Account-level pages the app
does implement beyond the list above sit after **Source integrations** and
before **Sign out** — today Xtream connections (app#271), VOD matches
(app#272) and playback gateways (app#273).

## Change password (proposed)

Needs a backend route; none exists (`POST /auth/recover` only resets a password
with a recovery code). Until it exists the row is absent rather than dead.

Page title **Change password**, three fields: **Current password**, **New
password** (at least 12 characters, matching the register rule), **Confirm new
password**. Primary **Change password**, secondary **Cancel**.

- Success: return to the Account page and show **"Password changed. Other devices
  stay signed in."** — accurate, because no route revokes them; offering
  **"Sign out other devices"** is the Devices page's job.
- Wrong current password: inline **"That password is not correct."** on the
  Current password field; the field is cleared, the new password is kept.
- Mismatch: inline **"Passwords do not match."** under Confirm.
- Rate limited: **"Too many attempts. Wait a minute and try again."**
- Server or network failure: **"Could not change your password. Try again."**
- Back, Cancel and Escape leave without saving and change nothing.

## Devices and sessions

The existing page (`W3Account` board), unchanged in shape:

- Lead: **"Everywhere [name]'s account is signed in. Signing a device out doesn't
  delete anything from the account."**
- One row per signed-in device: a 40 icon tile, the device name 15/600 (for
  example **"This browser · Chrome on macOS"**, **"Living room TV"**), and
  **Now** or **Signed in [when]**. The current device reads **This device** in
  place of a sign-out action.
- **Sign out** on each other row, opening **Sign out this device?** ·
  **"It will need a new code to sign in again."** · Cancel · Sign out (danger).
- **Sign out of all devices** below the list (240 × 40, danger fill), disabled on
  the device you are using, opening **Sign out of all devices?** · **"Every other
  device has to sign in again. This one stays signed in."** · Cancel · Sign out
  all (danger).
- Empty: **"No other devices are signed in."** Loading: three 68-high skeleton
  rows. Failure: the error line plus **Retry**, with the list left as it was.
- Refresh after every successful sign-out; a row that disappears stays gone.

## Delete account (proposed)

Needs a backend route; none exists. Until it exists the row is absent.

Page title **Delete account**, danger. Body: **"This deletes [name]'s account,
its profiles, their history, My List, add-ons and paired devices. It cannot be
undone."** Fields: the account's username typed to confirm, and the household PIN
when one is set. Primary **Delete account** (danger, disabled until the typed
username matches exactly), secondary **Cancel**.

- Success: the app clears its session and opens the sign-in screen with
  **"Your account was deleted."**
- Wrong username or PIN: inline error, both fields kept.
- Failure: **"Could not delete your account. Nothing was changed. Try again."**
- Back, Cancel and Escape leave without deleting.

## Entry, Back and focus

- **Phone:** the Settings row on the profile sheet opens the list; the back arrow
  in the 48 header row leaves it. A sub-page's back arrow returns to the list with
  the list's scroll position kept. Android Back does the same. The groups do not
  change the list's position, so a viewer who was on Add-ons returns to Add-ons'
  row.
- **Tablet, desktop, web:** the rail is the navigation; opening a row never hides
  it, and the rail keeps the current row filled. Browser and app Back leave
  Settings. Desktop has no focus ring at all.
- **TV:** the rail is one focus column; Left from a content row returns to the
  rail row that opened the page, Up/Down clamp inside each column, and Back
  returns to the rail with the same row focused. A dialog returns the remote to
  the row that opened it. Nothing in the split changes these rules; only the row
  order and the two new rows do.
- Opening Settings from the player and pressing Back returns to the player
  (`settingsReturnsToPlayer` today) with the page it left, unchanged by this
  split.

## Inputs

- **Tap/OK** opens a row, toggles a switch, or picks a choice. Every row is one
  target; a row's value and chevron are inside it.
- **Long press, repeat and hold** do nothing in Settings on any layout; there is
  no hidden action behind a row.
- **Keyboard:** text fields are editable by clicking and typing on desktop; the
  TV uses the device IME (`AND-KEYBOARD-001`), and Back dismisses the IME before
  it leaves the dialog.
- Destructive rows and dialogs keep Cancel neutral and unfocused-by-default on
  desktop and TV, and put the destructive action second on phone.

## States

- **Loading:** the page's rows are drawn from what the app already has; a page
  whose data is still arriving shows its own skeleton rows (Devices) or its
  existing progress line (Parental controls). No page shows a full-screen spinner.
- **Failure:** the page keeps its title and any rows it can draw, and shows one
  error line plus a retry action. A failed save never claims success.
- **Empty:** Devices **"No other devices are signed in."**; Approved titles
  **"No approved titles yet."**; Linked services shows the connect action.
- **Disabled:** a row is disabled only when the server would reject it, with the
  reason as its note; otherwise the row is absent.
- **Session expired:** any page's 401 goes to sign-in with **"Session expired.
  Sign in again."**, as it does today.
- **Profile or account changed elsewhere:** late replies are dropped, never shown
  under the new profile (`HAF-05`, `pull-to-refresh.md`).

## Accessibility

- Group labels are headings for assistive technology, not list items, and are
  skipped by the TV remote.
- Every row is one node with its label, its value and its note, plus its role:
  switch rows expose on/off, choice rows expose the current value, and a disabled
  row exposes disabled with its note.
- Icon-only controls (avatar change, back, close) keep 44 targets on phone and
  tablet and an `aria-label`/content description.
- Contrast follows the tokens: labels `text-primary`, notes and values
  `text-secondary`, disabled 0.4 opacity with `text-tertiary`.
- The danger rows are the only red text on the page; focus never uses accent.

## Platform equivalents

| Action | Phone / tablet | Desktop / web | TV |
|---|---|---|---|
| Switch profile | Profile card → **Switch profile** | Rail profile card → **Switch profile** | **Switch profile** rail row → Who's watching? |
| Delete profile | Dialog over the Profile page | Dialog over the Profile page | Full-page dialog, Cancel focused |
| Sign out | Danger row → confirmation | Danger row → confirmation | Danger row → confirmation (`Tv3SignOut`) |
| Household PIN | Own page with 4–8 digit fields | Own page | Last row of Parental controls |
| Devices | Own page | Own page | The same list, read-only: sign-out actions are disabled with their reason |
| Add a device | Own page, code entry | Own page, code entry | Not on TV; a TV pairs itself |

Every action keeps a stated equivalent. TV shows the account rows it cannot use
as disabled with the reason, its devices list is read-only, and the pages that
need a browser session say where to use them.

## Acceptance

1. **ACCT-SPLIT-01** On phone, desktop and TV, open Settings. Four labelled
   groups appear in the order Profile, Playback, This device, Account, and no row
   sits outside a group except the profile card.
2. **ACCT-SPLIT-02** The Account group shows Account, Password, Household PIN,
   Devices & sessions, Add a device, Add-ons, Source integrations, Sign out and
   Delete account; no row in it changes a single profile's playback.
3. **ACCT-SPLIT-03** The Playback group holds Playback and Subtitles & audio; on
   desktop and web the sidebar is no longer titled Account, and neither page is
   reachable from the Account group.
4. **ACCT-SPLIT-04** Profile opens the current profile's page; changing the name
   saves and the Profile page, the profile card and the switcher all show the new
   name without a restart. Cancelling changes nothing.
5. **ACCT-SPLIT-05** Turning Kids profile on asks for the household PIN when none
   is set; with the PIN set, the maturity limit and approved titles rows appear
   and save. The Parental controls page shows the same values after returning.
6. **ACCT-SPLIT-06** Language on the Profile page shows the profile's audio and
   subtitle languages, and opens Subtitles & audio; saving a language there is
   visible on the Profile row when it is shown again.
7. **ACCT-SPLIT-07** Delete profile on the only profile is absent; on a second
   profile it asks **Delete [name]?** and, on confirmation, returns to the
   profile switcher with the profile gone. Cancel returns to the Profile page.
8. **ACCT-SPLIT-08** Simkl appears under Profile › Linked services, not under
   Account, and links and unlinks for the selected profile only. Switching
   profiles shows that profile's link state.
9. **ACCT-SPLIT-09** On TV, the rail shows group labels, a **Profile** row and a
   **Switch profile** row; the remote walks the labels without stopping on them,
   Left returns to the rail row that opened a page, and Back from a page lands on
   that row.
10. **ACCT-SPLIT-10** On TV, Password, Household PIN, Delete account and the
    per-device sign-out actions are disabled with **"Manage this from a signed-in
    phone, computer or the web dashboard."**, while Sign out and the devices list
    still work.
11. **ACCT-SPLIT-11** Change password with a wrong current password shows
    **"That password is not correct."** and saves nothing; with a mismatch shows
    **"Passwords do not match."**; on success returns to Account with
    **"Password changed. Other devices stay signed in."**
12. **ACCT-SPLIT-12** Delete account is disabled until the typed username matches;
    a wrong PIN fails without deleting anything; success clears the session and
    shows **"Your account was deleted."** on sign-in.
13. **ACCT-SPLIT-13** In local mode, no Account rows that need a server appear,
    the Account group holds **Change connection**, and the Profile page offers the
    local profile PIN instead of a household PIN.
14. **ACCT-SPLIT-14** A failed load on Devices and on Parental controls keeps the
    page, shows one error line and a retry, and retrying recovers. An expired
    session from any row goes to sign-in with **"Session expired. Sign in again."**
15. **ACCT-SPLIT-15** On phone, Back from a sub-page returns to the list at the
    same scroll position with the same row visible; on tablet, desktop and web
    the rail stays visible and keeps the current row filled throughout.

## Superseded

- `M3Settings`, `T3Settings` and `D3SetGeneral` draw one flat list and put
  **Account** last with no group labels. Their geometry and type stand; their row
  lists are replaced by the four groups above.
- `W3Account`'s nav is titled **Account** and lists Profiles, Devices, Add-ons,
  Source integrations, Parental controls, Playback and Subtitles & audio. Its
  geometry, row shapes and destructive button stand; the nav is retitled
  **Settings** with the four groups, and Playback, Subtitles & audio and Parental
  controls move out of the account group.
- `Tv3SignOut` and `Tv3SetAbout` list Account, Profiles, Playback, Subtitles &
  audio, Add-ons, Source integrations, Display, Parental controls, About with no
  group labels. The rail gains the four labels, **Profile**, and **Switch
  profile** in place of **Profiles**.
- The app's current `AccountSettingsSidebar` (web), `SettingsSidebar` (desktop,
  phone) and `TvSettingsSidebar` row lists are replaced. `DESIGN_GAPS`-style
  placeholder pages (**Notifications**, **General**) are not carried over.
- The issue text's "sign-in email" and "owner only" are corrected here: there is
  no email, and account rows are gated by the server's device-session rule, not
  by an owner role.

## Unknowns

- No board shows group labels on phone, tablet, desktop or TV, or the Profile
  page. Their geometry is derived from the type roles and the surrounding board
  spacing and is marked above; a canvas board should follow.
- **No route changes a password or deletes an account.** Both pages are specified
  and stay absent until the routes exist.
- **No route lists or regenerates recovery codes.** `W3Recovery`, `M3Recovery`
  and `D3Recovery` cannot be built as drawn; the Account page has no Recovery
  codes row until a route exists.
- **No route edits the account's display name or username.**
- **No per-profile menu language exists** and the app has one string language, so
  the Language row covers audio and subtitles only.
- **Owner versus member is not enforced for account settings.** The backend's
  `require_household_manager` rejects only device (TV) sessions, so a member's
  browser session can change the household PIN today. The disabled-row rule here
  covers TV device sessions; a member restriction needs a backend rule first.
- Whether the household PIN should be asked for before **Delete account** even
  when none is set is unverified with the owner.
- No device evidence exists for any layout; nothing here has been built.
