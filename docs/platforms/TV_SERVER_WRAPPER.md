# TV-web server wrapper — TV-REMOTE-001

Status: approved implementation scope, rendered acceptance pending.
Source: owner-approved TV-web rebuild, 2026-10-23; Tv3 reference boards at
07c76e0858ea62896aba88002cee2483d5d4796f.

SolidTV implements the 1920×1080 Tv3 boards, including their top navigation,
Onest typography, billboard, browsing transition, source panel and focus states.
The older rail/component sheets do not override these boards. Responsive React
browser/desktop layouts are outside this adoption.

Accounts are required. Omit guest/local sign-in, device-local providers and
torrents, downloads, casting, unsupported sign-in methods and episode annotations
without server support. Calendar is explicitly deferred because there is no TV
Calendar reference board; remove its navigation item and close the gap using the
board's existing spacing. Do not show dead controls for omitted features.

The server owns catalog and source order, availability, profile preferences,
history, resume, next-episode and playback authorization. The TV renders those
facts and submits intent. Focus, text input, scroll windows, animation, decoding,
request cancellation and lease execution remain platform effects. Credentials
may persist; there is no offline library or local execution fallback.

Use existing server capabilities to omit unavailable settings/actions. Parent
authorization is the account PIN, not a fabricated per-profile PIN. A failed
mutation leaves the confirmed value intact and offers retry. Back cancels the
current operation or overlay and restores its invoking focus. Source selection
is explicit; decoder errors cannot trigger locally chosen fallback. Next episode
requires activation. Existing 700 ms hold actions remain available through
visible menus, without adding remote-key hints to the new boards.

Acceptance: compare each applicable Tv3 state with matched content, recording
geometry and privately inspected image differences. Exercise entry, loading,
success, empty/error, cancellation and return focus; test profile isolation and
late responses. Record browser, real media and physical TV results separately.
No app captures belong in this repository. Server changes must remain additive
and compatible with the concurrent Roku implementation.

## My List query controls

Keep the Tv3MyList header geometry: server-returned type choices in the left
segmented control and the server sort label/current value in the right pill.
The shared Library API may advertise additional filters absent from the board.
Expose those through a Filters entry in the Sort menu, using the existing TV
choice panel, rather than adding another header pill. If the server advertises
filters without sort, the same right pill is labelled Filters. Omit controls
that the server does not advertise. Values, ordering and reset defaults come
from the Library snapshot; the board's Last watched value is fixture content,
not a client default. Filter edits are a draft: Clear previews `default_query`,
Apply reads the server result, and Back discards the draft. Failed Apply keeps
the confirmed list and the draft available for retry. This is TV-web's access
path for the existing shared query contract, not a change to Roku's KMP layout.

## Search inputs and returned content

Use Tv3Search's 520×72 input at (96,140), the two wide Space/Delete keys followed
by six columns of alphanumeric keys at (96,236), and 212×318 result posters
starting at (700,196), with 16px horizontal gaps. The credentials/name editor
keeps its separate punctuation/case keyboard. Query changes retire the previous
request and its selectable results immediately; typing and navigation remain
available while a response is pending. Search errors offer retry without
disabling the keyboard. Preserve the server's result order.

Channel search uses the existing scoped Live query when advertised. Do not
construct query suggestions from title strings or invent channel numbers or
current-program captions absent from the response. Those reference elements
remain omitted until their server projections exist. This does not remove the
supported channel-search feature or its reference geometry.

## Device entry and profile selection

Follow Tv3Splash, Tv3Welcome, Tv3SignIn and Tv3Profiles geometry and motion.
Welcome has the supported Sign in action only. Keep its poster wall opacity
and radial vignette separate; inherited opacity must be applied once, including
rounded artwork. Splash remains indeterminate. Reduced motion freezes the wall,
indicator and pairing pulse, and shows the final profile entrance positions.

Pairing opens in the board's passive waiting state. Any directional press focuses
New code; OK also activates it directly. Its URI, QR, code and expiry come from
the server. Display the expiry as a decreasing duration from a monotonic clock.
New code immediately clears the abandoned code and QR while the request is
pending. Back cancels the request and polling and returns to Welcome's Sign in;
a late reply must not reopen pairing. Failure offers retry; expiry never implies
successful authentication. Keep the QR at 300×300 inside the 340×340 white tile.
The longer server URI may wrap to two lines, moving the following step/code down.

Profiles use full 200×200 artwork clipped to the 28px radius. The selected tile
has an inset 4px white focus ring; locked labels use the inline lock. Keep the
450ms entrance and 60ms per-tile stagger. Add and Manage appear only when the
server advertises their corresponding capabilities. Down reaches Manage only
when present, Up returns to the selected profile, and horizontal movement stays
inside the returned profiles/Add sequence. Existing hold/menu access also obeys
the server's management capabilities. Empty and failed states retain the shared
retry and Back handling; no local profile is invented.

Acceptance includes matched private captures, rounded-opacity pixel checks,
normal/reduced motion, countdown and cancelled refresh, and a profile set with
all management capabilities unavailable. Browser geometry permits up to one
physical pixel of DOM/canvas rounding at 1920×1080; record larger differences
rather than widening that tolerance. These are web-TV states, not Roku redesigns.
