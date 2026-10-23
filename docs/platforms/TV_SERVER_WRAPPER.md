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
