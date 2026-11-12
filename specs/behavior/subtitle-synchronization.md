# PLAY-SUBTITLE-SYNC-001 — Background subtitle timing

Status: proposed opt-in implementation. Source revision is the design commit
introducing this section. Architecture and qualification gates:
[research plan](https://github.com/viptv-org/workspace/blob/main/docs/research/subtitle-sync.md).
No synthetic fixture or successful compile establishes synchronization accuracy.

Playback always begins with original or exact-identity cached timing. Analysis
never gates startup, replaces the video source or restarts playback. Native
desktop/mobile analysis stays local; unsupported paths remain unavailable with
original/manual timing. Web uses the existing authenticated playback gateway.

## Entry and copy

The existing **Audio & subtitles** picker exposes **Find provider subtitles** when
the delivery supports provider captions, even if no embedded tracks exist. The
provider list uses server-owned candidate labels, with **Off** first. Selection
retains its language/source identity and existing caption appearance preferences.

For a selected provider track supporting live correction, **Subtitle timing
(0.0 s)** opens the existing single-column picker layout; display the current
signed manual delay in place of 0.0. Do not add a fourth clipped column.
Its state heading is one of **Original timing**, **Checking automatic timing**,
**Automatic timing (prototype)**, **Automatic timing unavailable**, or **Manual
timing**. Actions are **Earlier by 0.5 s**, **Later by 0.5 s**, and **Reset automatic
timing**. Unsupported hosts do not advertise automatic analysis as available.

Native clients with a qualified local acquisition path may expose **Automatic
timing (experimental)** with **Off**/**On** in the existing picker. It defaults
Off and may be session-scoped. On is an explicit reset/resume: clear the session's
manual delay and accepted automatic mapping, start a fresh local generation, and
use original timing while observing. Never replace the player or change output
mode. Off stops observation/automatic updates and restores original timing plus
any explicit manual delay. Manual changes while enabled freeze automatic updates
until Reset or a subsequent explicit Off→On. Unsupported audio paths show unavailable rather than
enabling server analysis. A test-only APK toggle is acquisition evidence, not a
completed user-facing app integration.

Earlier/later add −0.5/+0.5 content seconds to the accepted automatic mapping and
freeze later automatic updates. Reset clears manual delay and the current automatic
view, begins a fresh analysis generation, and immediately retains original timing
while analysis runs. Ordinary playback speed changes do not multiply this delay.
An uncertain or mismatched result leaves current timing intact.

## Lifecycle and input

Up/Down selects rows; OK applies the action immediately without leaving playback.
Back closes the timing/provider menu and restores the originating player control;
closing discovery fences late results so they cannot reopen it. Repeat and 700ms
hold behavior remain that of the existing picker. Provide the same visible
actions for keyboard/pointer input and meaningful current-state labels.

Source/audio/subtitle changes, Off, lease expiry and player exit invalidate old
generations. Accept only matching identities and monotonic observation/correction
revisions. Keep alignment separate from the authoritative source/player timeline
origin; cue updates derive from canonical intervals, never repeatedly retimed cues.
Manual override always wins. Cache only proven exact media/audio/subtitle identity;
otherwise keep correction session-only.

## Availability and acceptance

The initial gateway prototype is limited to retained, zero-origin VOD transport
stream HLS and trusted configured VAD/estimator workers. Direct/progressive/live,
unqualified seek origins, other containers and unsupported native hosts abstain.
Fixed offset and drift are distinct capabilities; a 120s observation path does not
qualify drift requiring separated evidence over at least 10 minutes.

Verify provider-only picker reachability; original timing during analysis; accepted
correction without video restart; manual earlier/later and explicit reset; Off,
track/source replacement, seeks, speed changes, expiry and late callbacks; foreign
lease/profile refusal; overload/worker failure; and no stale or doubled-origin
corrections. Test Chrome/Firefox/Safari separately and record actual native audio
acquisition, CPU/memory/network, held-out accuracy and sustained battery/thermal
results. Unexecuted platforms remain unqualified, not implicitly server-backed.
